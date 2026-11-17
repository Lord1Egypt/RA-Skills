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

const CHECKS_FULL_EXTRA = [
  '报销明细加总是否等于申请金额',
  '申请金额大小写是否一致',
  '发票合计与申请金额是否匹配',
  '日期逻辑（发票日期 ≤ 报销日期；发票日期在出差区间内）',
  '同一张发票的金额与报销明细是否对得上',
  '报销单要素完整性（单号 / 报销人 / 部门 / 日期）',
  '差旅标准超标提示（可配置标准）',
  '发票税率与税额自洽',
];

// 订阅版**没有**未执行项：这个引擎无条件执行全部检查（含上面的追加项）。
// 早先这里留着本包那份数组，导致对外 JSON 说"未执行"、实际却都跑了 —— 口径必须与行为一致。
const CHECKS_WITHHELD = [];

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
function cnNumberToValue(str) {
  let t = String(str == null ? '' : str).trim().replace(/^人民币/, '').replace(/[整正]$/, '');
  if (!t) return null;
  let intPart = t, fracPart = '';
  const m = /^(.*?)[元圆](.*)$/.exec(t);
  if (m) { intPart = m[1]; fracPart = m[2]; }
  const readSection = (s) => {
    let total = 0, cur = 0, seen = false;
    for (const ch of s) {
      if (CN_DIGIT[ch] !== undefined) { cur = CN_DIGIT[ch]; seen = true; }
      else if (CN_UNIT[ch] !== undefined) { total += (cur || 1) * CN_UNIT[ch]; cur = 0; seen = true; }
      else if (ch === '万') { total = (total + cur) * 1e4; cur = 0; seen = true; }
      else if (ch === '亿') { total = (total + cur) * 1e8; cur = 0; seen = true; }
      else if (ch === '零' || ch === '〇') { seen = true; }
      else return null;
    }
    return seen ? total + cur : null;
  };
  let yuan = 0;
  if (intPart) {
    const v = readSection(intPart);
    if (v === null) return null;
    yuan = v;
  }
  let frac = 0;
  if (fracPart) {
    let rest = fracPart;
    const j = /([零〇壹贰叁肆伍陆柒捌玖])角/.exec(rest);
    if (j) { frac += CN_DIGIT[j[1]] * 0.1; rest = rest.replace(j[0], ''); }
    const f = /([零〇壹贰叁肆伍陆柒捌玖])分/.exec(rest);
    if (f) { frac += CN_DIGIT[f[1]] * 0.01; rest = rest.replace(f[0], ''); }
    rest = rest.replace(/[零〇]/g, '').trim();
    if (rest) return null;
  }
  return yuan + frac;
}

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

/** 3. 报销明细加总 = 申请金额 */
function checkDetailSum(perDoc) {
  const out = [];
  perDoc.forEach(({ doc, fields }) => {
    if (kindOf(doc) !== 'report') return;
    const apply = fields.applyAmount && numOf(fields.applyAmount[0].value);
    if (apply == null) return;
    const details = parseDetailAmounts(doc.text)
      .filter((d) => !/报销金额|申请金额|合计|总额|大写/.test(d.label));
    if (details.length < 2) return;   // 明细不足两条时不做加总判断（避免误报）
    const sum = Math.round(details.reduce((n, d) => n + d.value, 0) * 100) / 100;
    if (Math.abs(sum - apply) > 0.02) {
      out.push(finding('P0', '明细加总与申请金额不符', fields.applyAmount[0].line,
        `报销明细共 ${details.length} 条、合计 ${sum.toFixed(2)}，但申请金额写的是 ${apply.toFixed(2)}（差 ${Math.abs(sum - apply).toFixed(2)}）。`,
        '核对明细是否有漏记或金额抄错。',
        details.map((d) => d.raw).slice(0, 5)));
    }
  });
  return out;
}

/** 4. 大小写一致 */
function checkCapital(perDoc) {
  const out = [];
  perDoc.forEach(({ doc, fields }) => {
    if (kindOf(doc) !== 'report') return;
    const small = fields.applyAmount && numOf(fields.applyAmount[0].value);
    const capRaw = fields.applyAmountCn && fields.applyAmountCn[0].value;
    if (small == null || !capRaw) return;
    const cap = cnNumberToValue(capRaw);
    if (cap === null) {
      out.push(finding('P2', '大写金额无法解析', fields.applyAmountCn[0].line,
        `大写金额「${capRaw}」无法解析成数值，因此没有做大小写互校。`,
        '请确认大写金额写法是否规范（如「壹仟贰佰元整」）。', [fields.applyAmountCn[0].raw]));
      return;
    }
    if (Math.abs(cap - small) > 0.02) {
      out.push(finding('P0', '大小写金额不一致', fields.applyAmountCn[0].line,
        `申请金额小写是 ${small.toFixed(2)}，大写写的是「${capRaw}」（约 ${cap.toFixed(2)}）。`,
        '两者必须一致；以实际发生额为准改正后重新提交。',
        [fields.applyAmount[0].raw, fields.applyAmountCn[0].raw]));
    }
  });
  return out;
}

/** 5. 发票合计 vs 申请金额 */
function checkInvoiceTotal(perDoc, opts) {
  const tolAbs = Number.isFinite(opts && opts.toleranceAbs) ? opts.toleranceAbs : 0.02;
  const out = [];
  const invs = perDoc.filter(({ doc }) => kindOf(doc) === 'invoice');
  if (invs.length === 0) return out;
  const rep = perDoc.find(({ doc }) => kindOf(doc) === 'report');
  if (!rep) return out;
  const apply = rep.fields.applyAmount && numOf(rep.fields.applyAmount[0].value);
  if (apply == null) return out;
  const amounts = invs
    .map(({ doc, fields }) => {
      const h = (fields.amount && fields.amount[0]) || (fields.gross && fields.gross[0]);
      const v = h ? numOf(h.value) : null;
      return v === null ? null : { v, raw: h.raw, docType: doc.type };
    })
    .filter(Boolean);
  if (amounts.length !== invs.length) return out;   // 有发票没金额 → 不做合计判断（要素完整性另有检查）
  const sum = Math.round(amounts.reduce((n, a) => n + a.v, 0) * 100) / 100;
  if (Math.abs(sum - apply) > tolAbs) {
    out.push(finding('P1', '发票合计与申请金额不符', 0,
      `${invs.length} 张发票金额合计 ${sum.toFixed(2)}，申请金额是 ${apply.toFixed(2)}（差 ${Math.abs(sum - apply).toFixed(2)}）。`,
      '请确认是否有发票漏附，或申请金额是否含未附票的费用。',
      amounts.map((a) => a.raw).slice(0, 5)));
  }
  return out;
}

/** 6. 日期逻辑 */
const DATE_RE = /(\d{4})[-\/年.](\d{1,2})[-\/月.](\d{1,2})/g;
function datesIn(text) {
  const out = [];
  String(text || '').split(/\r?\n/).forEach((raw, idx) => {
    DATE_RE.lastIndex = 0;
    let m;
    while ((m = DATE_RE.exec(raw)) !== null) {
      const y = +m[1], mo = +m[2], d = +m[3];
      if (mo >= 1 && mo <= 12 && d >= 1 && d <= 31) {
        out.push({ key: y * 10000 + mo * 100 + d, line: idx + 1, raw: raw.trim() });
      }
    }
  });
  return out;
}
function checkDates(perDoc) {
  const out = [];
  const rep = perDoc.find(({ doc }) => kindOf(doc) === 'report');
  const invs = perDoc.filter(({ doc }) => kindOf(doc) === 'invoice');
  if (!rep) return out;

  const repDates = datesIn(rep.doc.text);
  const repDate = repDates.length ? Math.max(...repDates.map((x) => x.key)) : null;

  // 报销日期 vs 发票日期：发票不应晚于报销日期
  if (repDate) {
    invs.forEach(({ doc, fields }) => {
      const h = fields.invoiceDate && fields.invoiceDate[0];
      if (!h) return;
      const ds = datesIn(h.value);
      if (!ds.length) return;
      const d = ds[0].key;
      if (d > repDate) {
        out.push(finding('P1', '发票日期晚于报销日期', h.line,
          `${doc.type} 的开票日期「${h.value}」晚于报销日期 —— 先有票才能报，请核对日期是否抄错。`,
          '核对开票日期与报销日期；若确为跨期报销，请按公司制度说明。', [h.raw]));
      }
    });
  }

  // 出差区间 vs 发票日期
  const trip = rep.fields.tripPeriod && rep.fields.tripPeriod[0];
  if (trip) {
    const td = datesIn(trip.value);
    if (td.length >= 2) {
      const lo = Math.min(...td.map((x) => x.key)), hi = Math.max(...td.map((x) => x.key));
      invs.forEach(({ doc, fields }) => {
        const h = fields.invoiceDate && fields.invoiceDate[0];
        if (!h) return;
        const ds = datesIn(h.value);
        if (!ds.length) return;
        const d = ds[0].key;
        if (d < lo || d > hi) {
          out.push(finding('P2', '发票日期不在出差区间内', h.line,
            `${doc.type} 的开票日期「${h.value}」不在出差区间「${trip.value}」内。`,
            '若属于合理情况（如提前订票、事后补票），请保留说明；否则请核对。', [trip.raw, h.raw]));
        }
      });
    }
  }
  return out;
}

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
    ...checkDetailSum(perDoc),
    ...checkCapital(perDoc),
    ...checkInvoiceTotal(perDoc, opts || {}),
    ...checkDates(perDoc),
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
  result.scope = { given: CHECKS_GIVEN.slice(), withheld: [] };
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
  cnNumberToValue,
  parseDetailAmounts,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
  CHECKS_FULL_EXTRA,
  CHECKS_EXECUTED: CHECKS_GIVEN.concat(CHECKS_FULL_EXTRA),
  CHECKS_OUT_OF_SCOPE: [
    '判断这笔费用该不该报（那是公司制度与审批流程的事）',
    '发票真伪查验与代码号码规则校验',
    '差旅标准是否超标的最终认定',
    '给出税务、审计或法律意见',
    '从扫描件/图片里识别文字（需要你先把文字贴进来）',
  ],
  SAMPLE_TEXT: [
    '报销单',
    '报销单号: BX-2026-0417',
    '报销人: 张伟明',
    '部门: 市场部',
    '报销日期: 2026-05-12',
    '出差日期: 2026-05-06 至 2026-05-09',
    '市内交通 86.00',
    '住宿费 1,240.00',
    '餐费 260.00',
    '报销金额: 1,586.00',
    '金额大写: 壹仟伍佰捌拾陆元整',
    '',
    '增值税电子普通发票',
    '发票号: 04412026-0088',
    '开票日期: 2026-05-08',
    '销售方: 某某酒店管理有限公司',
    '价税合计: 1,240.00',
    '',
    '增值税电子普通发票',
    '发票号: 04412026-0088',
    '开票日期: 2026-05-08',
    '销售方: 某某酒店管理有限公司',
    '价税合计: 1,240.00',
  ].join('\n'),
};
