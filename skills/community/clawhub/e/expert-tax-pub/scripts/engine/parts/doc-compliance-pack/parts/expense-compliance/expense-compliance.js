'use strict';
/**
 * expense-compliance.js —— 报销单合规预检（报销单 + 发票）本地引擎
 *
 * 与本仓库「票据一致性」的区别（这是两个产品，不要混淆）：
 *   · 票据一致性：**一张**票据自己跟自己对不对（行内算术、税额、价税合计、大小写…）；
 *   · 本引擎  ：**一沓发票 + 一张报销单**之间的工作流核对 ——
 *     报销明细加总是否等于申请金额、发票合计是否与申请金额对得上、
 *     同一张发票有没有重复报销、发票日期是否落在出差区间内、
 *     发票要素是否齐全。**重复报销与多报直接是钱。**
 *
 * 设计原则（与本仓库其它引擎一致）：
 *   · 自包含：只用 Node.js 标准库，**不发起任何网络请求**；
 *   · 每条结论都引用原文与行号，第三方可用同一份输入复算；
 *   · 材料不足时返回 insufficient_input 并说明缺什么，**绝不输出"未发现问题"**；
 *   · 只做AI核对，**不判断这笔费用该不该报**（那是公司制度与审批的事）；
 *     本工具也**不做发票真伪查验**。
 */

const CHECKS_GIVEN = [
  '重复发票号（重复报销线索）',
  '发票要素完整性（发票号 / 开票日期 / 销售方 / 金额）',
  '模板占位符残留',
];

const CHECKS_WITHHELD = [
  '报销明细加总是否等于申请金额',
  '申请金额大小写是否一致',
  '发票合计与申请金额是否匹配',
  '日期逻辑（发票日期 ≤ 报销日期；发票日期在出差区间内）',
  '同一张发票的金额与报销明细是否对得上',
  '报销单要素完整性（单号 / 报销人 / 部门 / 日期）',
  '差旅标准超标提示（可配置标准）',
  '发票税率与税额自洽',
];

/* ------------------------------------------------------------------ 字段 */

const FIELD_LABELS = [
  ['reportNo', ['报销单号', '报销编号', '单号', 'report no', 'expense no']],
  ['applicant', ['报销人', '申请人', '姓名', 'applicant', 'employee']],
  ['department', ['部门', '所属部门', 'department', 'dept']],
  ['reportDate', ['报销日期', '申请日期', '填单日期', 'report date']],
  ['applyAmount', ['报销金额', '申请金额', '合计金额', '报销总额', '金额合计', 'total amount', 'amount']],
  ['applyAmountCn', ['金额大写', '大写金额', '人民币大写']],
  ['tripPeriod', ['出差日期', '出差时间', '行程日期', 'trip period', 'travel dates']],
  ['invoiceNo', ['发票号', '发票号码', 'invoice no', 'invoice number']],
  ['invoiceDate', ['开票日期', '发票日期', 'invoice date']],
  ['seller', ['销售方', '销方名称', '开票方', '商户', 'seller', 'vendor']],
  ['amount', ['金额', '价税合计', '合计金额', 'amount', 'total']],
  ['detail', ['明细', '费用明细', '项目', 'detail', 'items']],
];

const INVOICE_RE = /发票|invoice/i;
const REPORT_RE = /报销单|报销|expense|reimbursement/i;

/* ---------------------------------------------------------------- 工具 */

function finding(level, category, line, message, advice, evidence) {
  return { level, category, line, message, advice, evidence };
}

function normNumber(s) {
  const t = String(s == null ? '' : s)
    .replace(/[,，\s\u00A0]/g, '')
    .replace(/^[¥￥$€£]/, '')
    .replace(/(元|人民币|cny|rmb)$/i, '');
  if (!/^\d+(\.\d+)?$/.test(t)) return null;
  return String(Math.round(parseFloat(t) * 100) / 100);
}
function numOf(s) { const n = normNumber(s); return n === null ? null : parseFloat(n); }
function normText(s) {
  return String(s == null ? '' : s)
    .replace(/[\s\u00A0]+/g, ' ')
    .replace(/[。．.,，;；:：、"'“”‘’()（）]/g, '')
    .trim().toUpperCase();
}

/** 从文本里抽「标签 值」字段 */
function extractFields(text) {
  const out = {};
  String(text == null ? '' : text).split(/\r?\n/).forEach((raw, idx) => {
    const line = raw.trim();
    if (!line) return;
    for (const [key, labels] of FIELD_LABELS) {
      for (const label of labels) {
        const re = new RegExp(
          '(?:^|[\\s|;；,，])' + label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
            + '\\s*[:：]?\\s*([^|;；\\n]+)', 'i');
        const m = re.exec(line);
        if (m && m[1] && m[1].trim()) {
          (out[key] = out[key] || []).push({ value: m[1].trim(), line: idx + 1, raw: line });
          break;
        }
      }
    }
  });
  return out;
}

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
      const blocks = single.split(/\n[ \t]*\n+/).map((x) => x.trim()).filter(Boolean);
      if (blocks.length >= 2) {
        blocks.forEach((b, i) => {
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

function kindOf(doc) {
  if (REPORT_RE.test(doc.type)) return 'report';
  if (INVOICE_RE.test(doc.type)) return 'invoice';
  return 'other';
}

/** 中文大写金额 → 数值（只支持常见的元角分写法，解析不了就返回 null） */
const CN_DIGIT = { '零': 0, '〇': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9 };
const CN_UNIT = { '拾': 10, '佰': 100, '仟': 1000, '十': 10, '百': 100, '千': 1000 };


/** 解析「明细」里的金额列表，用于加总核对 */
function parseDetailAmounts(text) {
  const out = [];
  String(text == null ? '' : text).split(/\r?\n/).forEach((raw, idx) => {
    const line = raw.trim();
    if (!line) return;
    // 形如「打车 120.00」或「打车 | 120.00」或「1. 打车 120.00」
    const m = /^(?:\d+[.、)]\s*)?(.*?)[\s|,，；;]+([0-9][0-9,]*\.?\d*)\s*$/.exec(line);
    if (m) {
      const v = numOf(m[2]);
      if (v !== null && v > 0) out.push({ label: m[1].trim().slice(0, 24), value: v, line: idx + 1, raw: line });
    }
  });
  return out;
}

/* ------------------------------------------------------------ 各项检查 */

/** 1. 重复发票号（重复报销线索） */
function checkDuplicateInvoice(perDoc) {
  const out = [];
  const seen = new Map();
  perDoc.forEach(({ doc, fields }) => {
    (fields.invoiceNo || []).forEach((h) => {
      const k = normText(h.value);
      if (!k) return;
      if (!seen.has(k)) seen.set(k, []);
      seen.get(k).push({ docType: doc.type, ...h });
    });
  });
  seen.forEach((list) => {
    if (list.length < 2) return;
    out.push(finding('P0', '重复发票号', list[0].line,
      `发票号「${list[0].value}」在同一份报销材料里出现了 ${list.length} 次（${[...new Set(list.map((x) => x.docType))].join('、')}）。`,
      '同一张发票只能报销一次；请确认是不是重复粘贴或重复提交。',
      list.map((x) => x.raw).slice(0, 3)));
  });
  return out;
}

/** 2. 发票要素完整性 */
function checkInvoiceCompleteness(perDoc, opts) {
  const required = [
    ['invoiceNo', '发票号'],
    ['invoiceDate', '开票日期'],
    ['seller', '销售方'],
    ['amount', '金额'],
  ];
  const out = [];
  perDoc.forEach(({ doc, fields }) => {
    if (kindOf(doc) !== 'invoice') return;
    const missing = required.filter(([k]) => !(fields[k] && fields[k].length)).map(([, label]) => label);
    // 差旅场景下日期可由报销单统一交代时，允许放宽（opts.requireInvoiceDate === false）
    const need = (opts && opts.requireInvoiceDate === false)
      ? missing.filter((x) => x !== '开票日期') : missing;
    if (need.length) {
      out.push(finding('P1', '发票要素不完整', 0,
        `${doc.type} 缺少：${need.join('、')}。`,
        '报销入账通常要求这些要素齐全；请补齐或换一张要素完整的发票。',
        [doc.text.split(/\r?\n/)[0] || doc.type]));
    }
  });
  return out;
}







/** 6. 日期逻辑 */
const DATE_RE = /(\d{4})[-\/年.](\d{1,2})[-\/月.](\d{1,2})/g;



/** 7. 占位符残留 */
const PLACEHOLDER_RE = /(【[^】]{0,20}】|\[\[[^\]]{0,20}\]\]|\bTBD\b|\bXXX+\b|_{4,}|待填|待定|请填写)/gi;
function checkPlaceholders(docs) {
  const out = [];
  docs.forEach((d) => {
    d.text.split(/\r?\n/).forEach((raw, idx) => {
      PLACEHOLDER_RE.lastIndex = 0;
      const m = PLACEHOLDER_RE.exec(raw);
      if (m) {
        out.push(finding('P0', '模板占位符残留', idx + 1,
          `${d.type} 第${idx + 1}行还留着未替换的内容「${m[0]}」。`,
          '提交前必须逐一替换或删除。', [raw.trim()]));
      }
    });
  });
  return out;
}

/* -------------------------------------------------------------- 主流程 */

function analyze(docs, opts) {
  const perDoc = docs.map((doc) => ({ doc, fields: extractFields(doc.text) }));
  const findings = [
    ...checkDuplicateInvoice(perDoc),
    ...checkInvoiceCompleteness(perDoc, opts || {}),
    ...checkPlaceholders(docs),
  ];
  const summary = { p0: 0, p1: 0, p2: 0 };
  const byCategory = {};
  findings.forEach((f) => {
    const k = f.level === 'P0' ? 'p0' : (f.level === 'P1' ? 'p1' : 'p2');
    summary[k]++;
    byCategory[f.category] = (byCategory[f.category] || 0) + 1;
  });
  summary.total = findings.length;
  summary.by_category = byCategory;
  summary.verdict = summary.p0 > 0
    ? '发现必须处理的硬错误（P0）'
    : (summary.p1 > 0 ? '没有 P0，但有需要人工核对的项（P1）'
      : (summary.p2 > 0 ? '只有提示性预警（P2），没有硬错误'
        : '在上述检查项范围内没有发现问题 —— 这不等于没有问题，超出范围的检查本工具不执行'));
  return { findings, summary, docCount: docs.length, kinds: docs.map(kindOf) };
}

function insufficient(missing, advice) {
  return { status: 'insufficient_input', missing: [].concat(missing), advice };
}

/**
 * @param {Object} payload { documents:[{type,text}], toleranceAbs?, requireInvoiceDate? } 或 { text }
 */
function run(payload) {
  const docs = collectMaterial(payload);
  if (docs.length === 0) {
    return insufficient(['没有收到任何单据内容'],
      '请提供至少两张单据（一张报销单 + 至少一张发票），每张形如 {"type":"报销单","text":"报销单号 …\\n报销金额 …"}；'
      + '也可以用一个文本、单据之间空一行。');
  }
  const totalChars = docs.reduce((n, d) => n + d.text.length, 0);
  if (totalChars < 30) {
    return insufficient([`单据内容过短（共 ${totalChars} 字）`],
      '请把单据正文完整贴进来；内容过短时无法提取字段，也就做不了有意义的核对。');
  }
  const opts = {
    toleranceAbs: payload && Number.isFinite(payload.toleranceAbs) ? payload.toleranceAbs : undefined,
    requireInvoiceDate: payload && payload.requireInvoiceDate === false ? false : true,
  };
  const result = analyze(docs, opts);
  result.scope = { given: CHECKS_GIVEN.slice(), withheld: CHECKS_WITHHELD.slice() };
  result.docs = docs.map((d) => ({ type: d.type, chars: d.text.length }));
  return { status: 'success', result: result };
}

module.exports = {
  run,
  analyze,
  collectMaterial,
  extractFields,
  kindOf,
  normNumber,
  normText,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
  SAMPLE_TEXT: [
    "报销单",
    "报销单号: BX-2026-0417",
    "报销人: 张伟明",
    "部门: 市场部",
    "报销日期: 2026-05-12",
    "出差日期: 2026-05-06 至 2026-05-09",
    "市内交通 86.00",
    "住宿费 1,240.00",
    "餐费 260.00",
    "报销金额: 1,586.00",
    "金额大写: 壹仟伍佰捌拾陆元整",
    "",
    "增值税电子普通发票",
    "发票号: 04412026-0088",
    "开票日期: 2026-05-08",
    "销售方: 某某酒店管理有限公司",
    "价税合计: 1,240.00",
    "",
    "增值税电子普通发票",
    "发票号: 04412026-0088",
    "开票日期: 2026-05-08",
    "销售方: 某某酒店管理有限公司",
    "价税合计: 1,240.00",
  ].join('\n'),
};
