/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * award-contract-consistency-check.js —— 中标结果与合同一致性核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**中标后、合同签订前**，招标人（或代理机构）必须把
 * 合同草案与中标结果逐项对一遍 —— 《招标投标法》第四十六条要求合同"按照招标文件和中标人的
 * 投标文件订立"，**实质性内容不得背离**；中标价、工期、质量标准、中标人名称任何一处不一致，
 * 轻则被质疑、重则合同无效或被行政监督处罚。这是每个项目签合同前都要做一次的活。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 输入是一张**逐要素对照表**（这是行业里真实存在的表：左边"中标通知书"，右边"合同草案"）：
 *   要素 | 中标通知书 | 合同草案
 *
 * 免费档执行 5 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 */

const CHECKS_GIVEN = [
  '金额要素一致性核对（中标价 / 合同价）',
  '文本要素一致性核对（中标人 / 项目名称 / 工期等）',
  '必备要素齐全检测',
  '要素重复检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '签订时限检测（中标通知书发出后 30 日内订立合同）',
  '金额差异超过容忍比例检测（实质性偏离）',
  '实质性条款偏离词表扫描（延长/下调/免除/放弃等）',
  '不可核对表述检测（详见/另行约定/待定 等不能当"一致"）',
  '单侧缺失检测（一侧有值、另一侧为空 => 不可比）',
];

const OUT_OF_SCOPE = [
  '判断合同条款是否合法有效（那需要法律意见）',
  '核对技术标、施工组织设计等非要素性内容',
  '比对招标文件原文与合同草案（本表只核中标结果与合同）',
  '读取 .docx / .pdf 合同原件（需要你先摘成这张对照表）',
];

const SAMPLE_TEXT = [
  '要素\t中标通知书\t合同草案',
  '项目名称\t市政道路工程施工\t市政道路工程施工',
  '中标人\t豫州第一建筑工程有限公司\t豫州第一建筑工程有限公司',
  '中标价\t1286400.00\t1286400.00',
  '工期\t240 日历天\t240 日历天',
  '质量标准\t合格\t合格',
  '付款方式\t按月计量支付 80%\t按月计量支付 80%',
  '中标通知书发出日期\t2026-03-20\t2026-03-20',
  '合同签订日期\t2026-04-10\t2026-04-10',
].join('\n');

const TOL = 0.01;
const TOL_RATE = 0.003;              // 金额实质性偏离：>0.3%
const SIGN_DAYS = 30;                // 中标通知书发出后 30 日内订立合同

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的在前
  item: ['要素', '项目', '条目', '内容项'],
  notice: ['中标通知书', '通知书', '中标结果'],
  contract: ['合同草案', '合同', '协议'],
  note: ['备注', '说明'],
};

const LABELS = { item: '要素', notice: '中标通知书', contract: '合同草案', note: '备注' };
const REQUIRED = ['item', 'notice', 'contract'];

const REQUIRED_ITEMS = [
  ['项目名称', /项目名称|工程名称/],
  ['中标人', /中标人|中标单位|承包人|供应商/],
  ['中标价', /中标价|中标金额|合同价|合同金额|价款/],
  ['工期', /工期|交货期|服务期|履行期限/],
  ['质量标准', /质量标准|质量要求|验收标准/],
  ['付款方式', /付款方式|支付方式|付款条件/],
  ['合同签订日期', /签订日期|签约日期/],
];

const AMOUNT_ITEM = /价|金额|款|费率|单价/;
const NOTICE_DATE_ITEM = /中标通知书发出日期|发出日期|通知书日期/;
const SIGN_DATE_ITEM = /合同签订日期|签订日期|签约日期/;

const DEVIATION_WORDS = ['延长', '顺延', '下调', '上调', '免除', '免收', '放弃', '不予支付', '不承担', '另行约定', '据实结算', '以实际发生为准'];
const UNCHECKABLE = /详见|另行约定|待定|待商定|以合同为准|按实结算|略|暂定|不适用/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|\/)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

/** 文本归一化：去空白与常见标点，全角转半角后再比 */
function normText(v) {
  return String(v === undefined || v === null ? '' : v)
    .replace(/[\s\u3000]+/g, '')
    .replace(/[（）()【】\[\]「」“”"'’‘]/g, '')
    .replace(/[，,。.；;：:、]/g, '');
}

const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], missingColumns: null };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    roles.forEach((role, c) => {
      if (!role) return;
      row[role] = cells[c] === undefined ? '' : cells[c];
    });
    if (!isBlank(row.item)) items.push(row);
  }
  return { items, missingColumns };
}

const who = (it) => (it && it.item ? `「${String(it.item).trim()}」` : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkAmount(it) {
  const name = String(it.item || '');
  if (!AMOUNT_ITEM.test(name)) return null;
  const a = normNumber(it.notice);
  const b = normNumber(it.contract);
  if (a === null || b === null) return null;
  if (Math.abs(a - b) <= TOL) return null;
  const rate = a !== 0 ? Math.abs(b - a) / Math.abs(a) : null;
  return {
    level: 'P0', category: '金额要素不一致', line: it.line,
    message: `${who(it)}在中标通知书里是 ${a.toFixed(2)}，合同草案里是 ${b.toFixed(2)}，相差 ${round2(b - a).toFixed(2)}`
      + (rate === null ? '。' : `（${(rate * 100).toFixed(3)}%）。`),
  };
}

function checkText(it) {
  const name = String(it.item || '');
  if (AMOUNT_ITEM.test(name)) return null;                    // 金额已在 checkAmount 里按数值比
  if (NOTICE_DATE_ITEM.test(name) || SIGN_DATE_ITEM.test(name)) return null;  // 日期单独处理
  const a = normText(it.notice);
  const b = normText(it.contract);
  if (!a || !b) return null;
  if (a === b) return null;
  return {
    level: 'P0', category: '文本要素不一致', line: it.line,
    message: `${who(it)}在中标通知书里是「${String(it.notice).trim()}」，合同草案里是「${String(it.contract).trim()}」—— 两边写法不同（已忽略空格与标点差异）。`,
  };
}

function checkRequiredItems(items) {
  const out = [];
  for (const [label, re] of REQUIRED_ITEMS) {
    const hit = items.some((it) => re.test(String(it.item || '')));
    if (!hit) {
      out.push({
        level: 'P1', category: '必备要素缺失', line: 0,
        message: `对照表里没有「${label}」这一要素 —— 它属于合同实质性内容，必须逐项对过。`,
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = normText(it.item);
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一要素出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 至少有一行是多余的，结论会因此不确定。`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    if (isBlank(it.item)) continue;
    if (isBlank(it.notice) && isBlank(it.contract)) {
      out.push({
        level: 'P0', category: '要素两栏都为空', line: it.line,
        message: `${who(it)}的中标通知书与合同草案两栏都是空的（或占位符）—— 这一行等于没填。`,
      });
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到对照表正文（text）—— 请把「要素 / 中标通知书 / 合同草案」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `对照表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何要素行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkAmount(it); if (a) findings.push(a);
    const b = checkText(it); if (b) findings.push(b);

  }
  for (const f of checkRequiredItems(t.items)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);


  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const consistent = t.items.filter((it) => {
    const a = normText(it.notice); const b = normText(it.contract);
    return a && b && a === b;
  }).length;

  const result = {
    status: 'success',
    service_type: 'AWARD_CONTRACT_CONSISTENCY_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      items: t.items.length,
      items_identical: consistent,
      sign_deadline_days: SIGN_DAYS,
      amount_tolerance_rate: TOL_RATE,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      items: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'DEVIATION_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只做"中标结果与合同草案是否逐要素一致"的客观比对，不判断条款是否合法有效；'
      + '结论可由第三方用同一份对照表复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, normText, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
