'use strict';
/**
 * trade-doc-consistency.js —— 外贸单证「单单一致」AI核对（本地引擎）
 *
 * 为什么做这个：
 *   信用证项下，银行要逐张核对单据之间是否一致（"单单一致、单证一致"）。
 *   一旦出现不符点，银行会拒付并收**不符点费**（通常每笔 USD 50~100），
 *   货还可能压港产生滞箱费。而这件事在两个层面都是**确定性**的：
 *     · 单据之间的字段是否一致（发票号 / 信用证号 / 金额 / 数量 / 重量 / 港口 / 船名 …）
 *     · 单据内部的算术是否自洽（单价 × 数量 = 金额、毛重 − 皮重 = 净重、分项合计）
 *   所以它适合做成AI核对，而不是交给模型"读一遍发表意见"。
 *
 * 设计原则（与本仓库其它引擎一致）：
 *   · 自包含：只用 Node.js 标准库，**不发起任何网络请求**；
 *   · 每条结论都能被第三方用同一份输入复算：消息里直接引用原文；
 *   · 材料不足时返回 insufficient_input 并说明缺什么，**绝不输出"未发现问题"**；
 *   · 只做AI比对，**不判断单证是否会被银行接受**（那是银行与信用证条款的事）。
 *
 * 免费档只做这些（见 CHECKS_GIVEN），其余一律不执行（见 CHECKS_WITHHELD）。
 */

/* ------------------------------------------------------------------ 常量 */

const CHECKS_GIVEN = [
  '关键字段跨单据一致（发票号 / 合同号 / 信用证号）',
  '金额与币种跨单据一致',
  '数量 / 件数 / 重量跨单据一致',
  '港口 / 船名 / 唛头跨单据一致',
  '模板占位符残留',
];

const CHECKS_WITHHELD = [
  '行内算术（单价 × 数量 = 金额）',
  '分项金额加总与总额一致',
  '毛重 − 皮重 = 净重',
  '日期顺序（发票 ≤ 提单 ≤ 信用证有效期 / 最迟装运期）',
  '信用证金额上限与溢短装比例核对',
  '单据份数与正副本份数核对',
  '唛头逐行与箱号区间连续性',
  '原产地证 / 保险单与发票的关联字段核对',
];

/** 跨单据比对的关键字段：标签（中英） → 归一化后的字段名 */
const FIELD_LABELS = [
  ['invoiceNo', ['发票号', '发票号码', '发票编号', 'invoice no', 'invoice number', 'inv. no']],
  ['contractNo', ['合同号', '合同编号', 'contract no', 'contract number', 's/c no', 'sales contract']],
  ['lcNo', ['信用证号', '信用证号码', 'l/c no', 'lc no', 'credit no', 'letter of credit no', 'd/c no']],
  ['blNo', ['提单号', '提单号码', 'b/l no', 'bl no', 'bill of lading no', 'waybill no']],
  ['amount', ['总金额', '发票金额', '金额', 'total amount', 'amount', 'total value', 'value']],
  ['currency', ['币种', '货币', 'currency', 'ccy']],
  ['quantity', ['数量', '总数量', 'quantity', 'qty', 'total quantity']],
  ['packages', ['件数', '总件数', '箱数', 'packages', 'total packages', 'cartons', 'ctns']],
  ['grossWeight', ['毛重', 'gross weight', 'g.w.', 'gross wt']],
  ['netWeight', ['净重', 'net weight', 'n.w.', 'net wt']],
  ['vessel', ['船名', '船名航次', 'vessel', 'vessel name', 'ocean vessel']],
  ['portOfLoading', ['装运港', '起运港', 'port of loading', 'port of shipment', 'pol']],
  ['portOfDischarge', ['目的港', '卸货港', 'port of discharge', 'port of destination', 'pod']],
  ['marks', ['唛头', 'shipping marks', 'marks & nos', 'marks and numbers']],
];

/* ---------------------------------------------------------------- 工具函数 */

function finding(level, category, line, message, advice, evidence) {
  return { level, category, line, message, advice, evidence };
}

/** 金额/数量归一：去掉千分位、货币符号与单位，得到纯数字字符串 */
function normNumber(s) {
  const t = String(s == null ? '' : s)
    .replace(/[,，\s\u00A0]/g, '')
    .replace(/^[¥￥$€£]/, '')
    .replace(/(元|美元|美金|欧元|港币|日元|人民币|usd|eur|cny|rmb|hkd|jpy)$/i, '');
  if (!/^\d+(\.\d+)?$/.test(t)) return null;
  const n = parseFloat(t);
  // 用「放大取整再缩小」消掉浮点尾差
  return String(Math.round(n * 100) / 100);
}

/** 文本归一：用于名称/港口/船名这类"看着一样就算一样"的字段 */
function normText(s) {
  return String(s == null ? '' : s)
    .replace(/[\s\u00A0]+/g, ' ')
    .replace(/[。．.,，;；:：、"'“”‘’()（）]/g, '')
    .trim()
    .toUpperCase();
}

/**
 * 从一段文本里抽出「标签: 值」形式的字段。
 * 只认「标签后面紧跟分隔符或空格再跟值」的形态，避免把正文里的词误当字段。
 */
function extractFields(text) {
  const out = {};
  const lines = String(text == null ? '' : text).split(/\r?\n/);
  lines.forEach((raw, idx) => {
    const line = raw.trim();
    if (!line) return;
    for (const [key, labels] of FIELD_LABELS) {
      for (const label of labels) {
        // 标签 + 可选冒号/空格 + 值（取到行尾或下一个明显分隔）
        const re = new RegExp(
          '(?:^|[\\s|;；,，])' + label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
            + '\\s*[:：]?\\s*([^|;；\\n]+)',
          'i'
        );
        const m = re.exec(line);
        if (m && m[1] && m[1].trim()) {
          if (!out[key]) out[key] = [];
          out[key].push({ value: m[1].trim(), line: idx + 1, raw: line });
          break;
        }
      }
    }
  });
  return out;
}

/** 收集材料：支持 documents 数组，也支持单段 text（视为一张单据） */
function collectMaterial(payload) {
  const p = payload && typeof payload === 'object' ? payload : {};
  const docs = [];
  if (Array.isArray(p.documents)) {
    p.documents.forEach((d, i) => {
      if (!d) return;
      const text = typeof d === 'string' ? d : String(d.text != null ? d.text : (d.content != null ? d.content : ''));
      if (!text.trim()) return;
      const type = (d && (d.type || d.part || d.name)) || ('单据 ' + (i + 1));
      docs.push({ type: String(type).slice(0, 40), text: text });
    });
  } else {
    const single = p.text != null ? p.text : p.content;
    if (typeof single === 'string' && single.trim()) {
      // 也支持"一个文本框里粘多张单据"：**空行分隔**。
      // 由来：站点上的免费入口只有一个文本框，而"单单一致"至少需要两张单据；
      // 空行分隔是单证员粘贴时的自然做法，比要求他们手写 JSON 友好得多。
      const blocks = single.split(/\n[ \t]*\n+/).map((x) => x.trim()).filter(Boolean);
      if (blocks.length >= 2) {
        blocks.forEach((b, i) => {
          // 首行常是单据标题（如"商业发票 COMMERCIAL INVOICE"），用它当单据名更可读
          const first = (b.split('\n')[0] || '').trim().slice(0, 40);
          docs.push({ type: first || ('单据 ' + (i + 1)), text: b });
        });
      } else {
        docs.push({ type: p.type ? String(p.type).slice(0, 40) : '单据 1', text: single });
      }
    }
  }
  return docs;
}

/* ------------------------------------------------------------------ 各项检查 */

/** 1. 关键字段跨单据一致 */
function checkCrossDocument(docs) {
  const out = [];
  const perField = {};   // key → [{docType, value, norm, line}]
  docs.forEach((d) => {
    const f = extractFields(d.text);
    Object.keys(f).forEach((key) => {
      f[key].forEach((hit) => {
        (perField[key] = perField[key] || []).push({
          docType: d.type, value: hit.value, line: hit.line, raw: hit.raw,
        });
      });
    });
  });

  for (const [key, labels] of FIELD_LABELS) {
    const hits = perField[key];
    if (!hits || hits.length < 2) continue;   // 只出现在一张单据里 → 无从比对，不报
    const byDoc = new Map();
    hits.forEach((h) => { if (!byDoc.has(h.docType)) byDoc.set(h.docType, h); });
    if (byDoc.size < 2) continue;             // 同一张单据内出现多次，不算跨单据不一致

    const isNumber = ['amount', 'quantity', 'packages', 'grossWeight', 'netWeight'].includes(key);
    const norm = (v) => (isNumber ? (normNumber(v) || normText(v)) : normText(v));
    const groups = new Map();
    byDoc.forEach((h) => {
      const n = norm(h.value);
      if (!groups.has(n)) groups.set(n, []);
      groups.get(n).push(h);
    });
    if (groups.size <= 1) continue;

    const shown = [...groups.entries()].map(([, hs]) =>
      hs.map((h) => `${h.docType}「${h.value}」(第${h.line}行)`).join(' ')
    );
    out.push(finding(
      'P0', '跨单据字段不一致', 0,
      `字段「${labels[0]}」在各单据上写得不一样：${shown.join(' ／ ')}。`
      + `银行审单时单据之间必须一致，这类差异是最常见的不符点来源。`,
      '以信用证要求为准统一到同一个写法；改完再逐张核对一遍。',
      hits.map((h) => h.raw).filter((v, i, a) => a.indexOf(v) === i).slice(0, 4)
    ));
  }
  return out;
}







/** 5. 日期顺序 */



/** 6. 占位符残留 */
const PLACEHOLDER_RE = /(【[^】]{0,20}】|\[\[[^\]]{0,20}\]\]|\bTBD\b|\bXXX+\b|_{4,}|待填|待定|请填写|填写[:：]?$)/gi;
function checkPlaceholders(docs) {
  const out = [];
  docs.forEach((d) => {
    const lines = d.text.split(/\r?\n/);
    lines.forEach((raw, idx) => {
      PLACEHOLDER_RE.lastIndex = 0;
      const m = PLACEHOLDER_RE.exec(raw);
      if (m) {
        out.push(finding(
          'P0', '模板占位符残留', idx + 1,
          `${d.type} 第${idx + 1}行还留着未替换的内容「${m[0]}」。`,
          '递交银行前必须逐一替换或删除；这类残留会直接被退单。',
          [raw.trim()]
        ));
      }
    });
  });
  return out;
}

function analyze(docs) {
  const findings = [
    ...checkCrossDocument(docs),
    ...checkPlaceholders(docs),
  ];
  const summary = { p0: 0, p1: 0, p2: 0 };
  findings.forEach((f) => {
    const k = f.level === 'P0' ? 'p0' : (f.level === 'P1' ? 'p1' : 'p2');
    summary[k]++;
  });
  return { findings, summary, docCount: docs.length };
}

function insufficient(missing, advice) {
  return { status: 'insufficient_input', missing: [].concat(missing), advice };
}

/** 免费档入口：只做「关键字段跨单据一致」与「模板占位符残留」两类 */
function run(payload) {
  const docs = collectMaterial(payload);
  if (docs.length === 0) {
    return insufficient(['没有收到任何单证内容'],
      '请提供至少两张单据（一个文本里用空行分隔，或用 documents 数组）。只有一张时无法跨单据比对。');
  }
  const totalChars = docs.reduce((n, d) => n + d.text.length, 0);
  if (totalChars < 30) {
    return insufficient(['单证内容过短（共 ' + totalChars + ' 字）'],
      '请把单据正文完整贴进来；内容过短时无法提取字段。');
  }
  const result = analyze(docs);
  result.scope = { given: CHECKS_GIVEN.slice(), withheld: CHECKS_WITHHELD.slice() };
  result.docs = docs.map((d) => ({ type: d.type, chars: d.text.length }));
  return { status: 'success', result: result };
}

module.exports = {
  run,
  analyze,
  collectMaterial,
  extractFields,
  normNumber,
  normText,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
  SAMPLE_TEXT: [
    '商业发票 COMMERCIAL INVOICE', '发票号: INV-2026-0088', '合同号: SC-2026-117',
    '信用证号: LC-8891-2026', '币种: USD', '总金额: 48,500.00', '数量: 1,000 PCS',
    '装运港: SHANGHAI, CHINA', '',
    '装箱单 PACKING LIST', '发票号: INV-2026-0099', '合同号: SC-2026-117',
    '信用证号: LC-8891-2026', '总金额: 48,500.00', '数量: 1,000 PCS',
    '装运港: SHANGHAI, CHINA',
  ].join('\n'),
};
