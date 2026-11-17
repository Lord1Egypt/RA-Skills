#!/usr/bin/env node
/**
 * safety-hazard-rectification-check.js —— 安全隐患排查整改闭环核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点（《安全生产法》的隐患排查治理制度，制造/建筑/物业/危化每月都要做）：
 *   ① 排查出的隐患要**登记**（隐患编号、发现日期、位置、类型、等级、责任部门与责任人）；
 *   ② 要**定整改期限**并在期限内**整改完成** —— 超期未整改是检查时的直接处罚项；
 *   ③ 整改后要**验收销号** —— 台账上「隐患有、整改没闭环」是最常见的处罚项；
 *   ④ 重大隐患要**报告并挂牌督办**，上报日期不能空着；
 *   ⑤ 同一位置反复出现同一类隐患（说明整改没到根因）也是处罚与追责的重点。
 * 安环部每月必须把这张台账核一遍才能交差，而这一步几乎全是跨列日期算术与勾稽。
 *
 * 本文件是**订阅版（买断版）**：在本包六项逐行核对之上，多出五类能力 ——
 * 反复出现的隐患（同一位置 + 同一隐患类型 ≥3 次）、按责任部门分组的按期整改率与验收闭环率、
 * 责任人未闭环超载、同一隐患类型的整改期限口径一致性、分部门×隐患等级的汇总清单。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定现场隐患是否真实存在或是否已消除、不判定整改措施是否有效、
 *          不判定安全生产条件是否合规、不读 .xlsx/.pdf 原件、不联网核验编号与督办牌真伪；
 *          材料不足**一律不给结论**。
 *
 * ⚠️ 免费包由 `tools/strip_free_engine.py` 从本文件摘出：付费实现只被入口里那一个布尔开关包着，
 *    开关**只在入口声明一次**；写注释时不要复述开关那一行的源码（残渣断言是纯字符串包含判断）。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '整改时限达标（发现日期 + 规定整改期限(天) 与整改完成日期比，超期即列出超期天数）',
  '整改未闭环（状态未到 已验收/已销号，或整改完成日期/验收日期为空 ⇒ 逐条点名，按已超期天数排序）',
  '重大隐患上报勾稽（隐患等级 = 重大的记录必须有上报日期，缺失逐条点名）',
  '同一位置 + 同一隐患类型重复出现（点名历史行号与出现次数）',
  '合计行逐列复核（隐患条数 / 整改条数 / 验收条数 与逐行点数对不上即报出差额）',
  '空白/占位符/日期格式/状态值非法（状态只认 待整改、整改中、已整改待验收、已验收、已销号）',
];

const CHECKS_WITHHELD = [
  '反复出现的隐患（同一位置 + 同一隐患类型在统计期内出现 3 次及以上 ⇒ 列为反复出现，给次数与最早/最近发现日期）',
  '按期整改率与验收闭环率（按责任部门分组算两项比率，低于阈值逐部门点名）',
  '责任人未闭环超载（同一责任人的未闭环隐患数 大于 表内「责任人未闭环上限」⇒ 点名）',
  '整改期限口径不一致（同一隐患类型在不同行给了不同的规定整改期限 ⇒ 点名并列出各行期限与行号）',
  '分部门×隐患等级汇总清单（按未闭环数排序，给出可整改动作）',
];

const OUT_OF_SCOPE = [
  '判定现场隐患是否真实存在、是否已经消除（那是现场复查与验收人员的判断）—— 本工具只核台账上登记的字面信息',
  '判定整改措施是否有效、是否落到制度与责任人（本工具只核台账里有没有写、日期算不算得通）',
  '判定企业安全生产条件是否合规、是否达到法定要求（那是应急管理部门的执法认定权，本工具不做）',
  '读取 .xlsx / .pdf 原件、识别手写签名与整改照片、联网核验隐患编号与挂牌督办牌真伪',
  '替代安全评价报告、事故调查报告、法律意见或行政执法文书',
];

/* ============================ 内置样例 ============================ */

// 样例：一张**干净**的隐患排查治理台账 —— 六条隐患全部整改完成并验收销号、期限都没超、
// 重大隐患都写了上报日期、合计行的三个数量与逐行点数一致、没有同一位置+同一类型的重复隐患。
// 列顺序：隐患编号 发现日期 隐患位置 隐患类型 隐患等级 责任部门 责任人 规定整改期限(天)
//         整改完成日期 验收日期 状态 上报日期 责任人未闭环上限 隐患条数 整改条数 验收条数
const SAMPLE_HEADER = [
  '隐患编号', '发现日期', '隐患位置', '隐患类型', '隐患等级', '责任部门', '责任人',
  '规定整改期限(天)', '整改完成日期', '验收日期', '状态', '上报日期', '责任人未闭环上限',
  '隐患条数', '整改条数', '验收条数',
];
const SAMPLE_ROWS = [
  ['YH2026-001', '2026-03-03', '1号车间东侧配电柜', '电气线路老化', '一般', '生产一部', '周立群',
    '15', '2026-03-12', '2026-03-14', '已验收', '', '2', '', '', ''],
  ['YH2026-002', '2026-03-05', '危化品库房通风口', '通风不良', '重大', '安环部', '沈玉坤',
    '10', '2026-03-11', '2026-03-13', '已验收', '2026-03-06', '1', '', '', ''],
  ['YH2026-003', '2026-03-07', '3号仓库消防通道', '通道堆物占用', '一般', '仓储部', '郭敏之',
    '7', '2026-03-10', '2026-03-12', '已验收', '', '2', '', '', ''],
  ['YH2026-004', '2026-03-09', '二号楼施工电梯', '限位装置失灵', '重大', '工程部', '汪鹏举',
    '5', '2026-03-12', '2026-03-15', '已验收', '2026-03-10', '1', '', '', ''],
  ['YH2026-005', '2026-03-11', '食堂燃气管道接口', '燃气微量泄漏', '重大', '后勤部', '李承泽',
    '3', '2026-03-12', '2026-03-13', '已销号', '2026-03-11', '1', '', '', ''],
  ['YH2026-006', '2026-03-13', '锅炉房压力表', '压力表超期未检', '一般', '设备部', '陈思远',
    '20', '2026-03-20', '2026-03-22', '已验收', '', '3', '', '', ''],
  ['合计', '', '', '', '', '', '', '', '', '', '', '', '', '6', '6', '6'],
];
const SAMPLE_TEXT = [SAMPLE_HEADER.join('\t')]
  .concat(SAMPLE_ROWS.map((r) => r.join('\t')))
  .join('\n');

/* ============================ 口径常量 ============================ */

// 汇总行（合计行）的识别字样：第一格是这些字样之一 ⇒ 该行按合计行处理，不算隐患明细
const TOTALS_LABELS = ['合计', '总计', '小计', '合计数'];

// 闭环状态：只有到这两个状态才算闭环（销号是验收通过后的终止态）
const CLOSED_STATUSES = ['已验收', '已销号'];

// 允许的状态取值（写别的值就是取值非法，逐条点名）
const STATUS_VALUES = ['待整改', '整改中', '已整改待验收', '已验收', '已销号'];

// 允许的隐患等级取值
const LEVEL_VALUES = ['一般', '重大'];

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'hazardNo', 'foundDate', 'location', 'hazardType', 'level', 'dept', 'owner',
  'deadlineDays', 'rectifyDate', 'acceptDate', 'status', 'reportDate',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['hazardNo', '隐患编号'],
  ['foundDate', '发现日期'],
  ['location', '隐患位置'],
  ['hazardType', '隐患类型'],
  ['level', '隐患等级'],
  ['dept', '责任部门'],
  ['owner', '责任人'],
  ['deadlineDays', '规定整改期限(天)'],
  ['status', '状态'],
];

// 日期列（用于「格式非法」与「日期前后矛盾」判定）
const DATE_FIELDS = [
  ['foundDate', '发现日期'],
  ['rectifyDate', '整改完成日期'],
  ['acceptDate', '验收日期'],
  ['reportDate', '上报日期'],
];

// 合计行的三个数量类列：填报值角色 → 逐行点数的键 → 中文名
const TOTALS_PAIRS = [
  ['totalCount', 'count', '隐患条数'],
  ['totalRectified', 'rectified', '整改条数'],
  ['totalAccepted', 'accepted', '验收条数'],
];

// 合计行里允许填报的数量类角色（其余列在合计行上忽略）
const TOTALS_DECLARED_ROLES = ['totalCount', 'totalRectified', 'totalAccepted'];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的词必须排在更宽泛的词前面。
//    顺序一错，宽泛词就会抢走更具体的列（本仓库已踩过六次，见 tools/header_map_check.py）。
//    本产品的具体度排序要点：「责任人未闭环上限」必须先于「责任人」，
//    「整改完成日期」必须先于「整改日期」，「隐患条数/整改条数/验收条数」不能与日期列混排。
const ROLES = {
  hazardNo: ['隐患编号', '隐患代码', '隐患序号', '隐患单号', '编号'],
  location: ['隐患位置', '隐患部位', '发生位置', '所在位置', '检查部位', '位置', '部位'],
  hazardType: ['隐患类型', '隐患类别', '隐患描述', '隐患内容', '问题类型', '类型', '类别'],
  level: ['隐患等级', '隐患级别', '风险等级', '等级', '级别'],
  dept: ['责任部门', '责任单位', '整改部门', '所属部门', '部门', '车间'],
  ownerLimit: ['责任人未闭环上限', '未闭环上限', '人均未闭环上限', '未闭环阈值', '超载阈值'],
  owner: ['整改责任人', '责任人', '负责人', '责任人姓名'],
  deadlineDays: ['规定整改期限', '整改期限', '整改时限', '规定期限', '期限天数', '期限'],
  foundDate: ['发现日期', '隐患发现日期', '排查日期', '检查日期', '发现时间', '检查时间'],
  rectifyDate: ['整改完成日期', '完成整改日期', '实际整改完成日期', '整改完成时间', '整改完成', '整改日期'],
  acceptDate: ['验收日期', '验收时间', '销号日期', '验收通过日期', '验收销号日期'],
  reportDate: ['上报日期', '报告日期', '挂牌督办日期', '上报时间', '上报政府日期'],
  totalCount: ['隐患条数', '隐患总数', '隐患数量', '隐患合计'],
  totalRectified: ['整改条数', '已整改条数', '整改数量'],
  totalAccepted: ['验收条数', '已验收条数', '验收数量'],
  status: ['整改状态', '隐患状态', '闭环状态', '处置状态', '状态'],
};

const LABELS = {
  hazardNo: '隐患编号',
  location: '隐患位置',
  hazardType: '隐患类型',
  level: '隐患等级',
  dept: '责任部门',
  ownerLimit: '责任人未闭环上限',
  owner: '责任人',
  deadlineDays: '规定整改期限(天)',
  foundDate: '发现日期',
  rectifyDate: '整改完成日期',
  acceptDate: '验收日期',
  reportDate: '上报日期',
  totalCount: '隐患条数',
  totalRectified: '整改条数',
  totalAccepted: '验收条数',
  status: '状态',
};

// 数量类列（逐行求和；合计行上的三个数量列由「合计行逐列复核」单独比对，不参与求和）
const SUM_ROLES = ['deadlineDays'];

// 按期整改率 / 验收闭环率的默认阈值（可在入参里用 rate_threshold 覆盖，写 90 或 0.9 都可以）
const RATE_THRESHOLD_DEFAULT = 0.9;

// 反复出现的判定门槛（同一位置 + 同一隐患类型在统计期内出现次数 ≥ 此值）
const MIN_RECURRING = 3;

const MS_PER_DAY = 86400000;

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张台账补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「已闭环」，也不说「没闭环」。',
  };
}

const clean = (v) => String(v === undefined || v === null ? '' : v).trim();

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核|待确认)$/i.test(s);
}

/** 天数列的宽容解析：允许「15」「15天」「15 日」，其余交给 normNumber */
function normDays(raw) {
  if (raw === undefined || raw === null) return null;
  return normNumber(String(raw).replace(/[天日个]/g, ''));
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

function roleOf(header) {
  const h = String(header == null ? '' : header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

/** 日期解析：只认 YYYY-MM-DD / YYYY/M/D / YYYY.M.D / YYYY年M月D日 / YYYYMMDD，且必须是真实日历日 */
function parseDate(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim()
    .replace(/[年月]/g, '-')
    .replace(/日/g, '')
    .replace(/[./]/g, '-')
    .replace(/\s+/g, '');
  if (!s) return null;
  let m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (!m) m = /^(\d{4})(\d{2})(\d{2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const dt = new Date(Date.UTC(y, mo - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return dt;
}

const addDays = (dt, n) => new Date(dt.getTime() + n * MS_PER_DAY);
const dayDiff = (a, b) => Math.round((a.getTime() - b.getTime()) / MS_PER_DAY);
const fmtDate = (dt) => (dt ? dt.toISOString().slice(0, 10) : '');
const pct = (x) => `${round2(x * 100)}%`;

function who(it) {
  const no = clean(it.hazardNo);
  const loc = clean(it.location);
  const type = clean(it.hazardType);
  const tail = loc ? `（${loc}${type ? ' / ' + type : ''}）` : '';
  return `第 ${it.line} 行「${no || '未编号'}」${tail}`;
}

function finding(level, category, it, message, advice, metrics) {
  const f = { level, category, line: it.line, message };
  if (advice) f.advice = advice;
  if (metrics && typeof metrics === 'object') Object.assign(f, metrics);
  return f;
}

/** 按 keyOf 分组；keyOf 返回 null 的行不参与分组（例如位置/类型为空的行） */
function groupBy(items, keyOf) {
  const map = new Map();
  for (const it of items) {
    const k = keyOf(it);
    if (k === null) continue;
    if (!map.has(k)) map.set(k, []);
    map.get(k).push(it);
  }
  return map;
}

/** 同一位置 + 同一隐患类型的归组键（两者都非空才算） */
function repeatKey(it) {
  const loc = clean(it.location);
  const type = clean(it.hazardType);
  if (!loc || !type) return null;
  return loc + '\u0001' + type;
}

const SEP = '\u0001';
function splitKey(key) {
  const i = String(key).indexOf(SEP);
  return i < 0 ? [String(key), ''] : [String(key).slice(0, i), String(key).slice(i + 1)];
}

/** 解析成 {header, cols, items, totals, totalsRow, computed, missingRoles, missingColumns, error} */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], totals: {}, totalsRow: null,
      computed: { count: 0, rectified: 0, accepted: 0 },
      missingRoles: REQUIRED_ROLES.slice(), missingColumns: REQUIRED_ROLES.map((r) => LABELS[r]),
    };
  }

  const header = splitRow(rows[0].raw);
  const cols = header.map((h, k) => ({ header: h, role: roleOf(h), index: k }));
  const items = [];
  let totalsRow = null;

  for (let r = 1; r < rows.length; r++) {
    const cells = splitRow(rows[r].raw);
    // 合计行：第一格是「合计/总计/小计」⇒ 只取数量类列，不当隐患明细
    if (TOTALS_LABELS.indexOf(clean(cells[0])) >= 0 && !totalsRow) {
      const declared = {};
      for (const c of cols) {
        if (!c.role || TOTALS_DECLARED_ROLES.indexOf(c.role) < 0) continue;
        declared[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
      }
      totalsRow = { line: rows[r].line, raw: rows[r].raw, declared };
      continue;
    }
    const it = { line: rows[r].line, raw: rows[r].raw };
    for (const c of cols) {
      if (!c.role) continue;
      it[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
    }
    items.push(it);
  }

  const computed = {
    count: items.length,
    rectified: items.filter((it) => !isBlank(it.rectifyDate)).length,
    accepted: items.filter((it) => !isBlank(it.acceptDate)).length,
  };

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(items.reduce((acc, it) => {
      const n = normDays(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }

  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    totals,
    totalsRow,
    computed,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

/* ============================ 本包检查（六项） ============================ */

/** 1. 整改时限达标：发现日期 + 规定整改期限(天) 与 整改完成日期 比 */
function checkOverdue(items) {
  const out = [];
  for (const it of items) {
    const found = parseDate(it.foundDate);
    const limit = normDays(it.deadlineDays);
    const done = parseDate(it.rectifyDate);
    if (!found || limit === null || limit <= 0 || !done) continue;
    const due = addDays(found, limit);
    const late = dayDiff(done, due);
    if (late <= 0) continue;
    out.push(finding('P0', '整改超期', it,
      `${who(it)}：发现日期 ${fmtDate(found)}、规定整改期限 ${limit} 天 ⇒ 最迟应于 ${fmtDate(due)} 完成整改，`
      + `实际整改完成日期 ${fmtDate(done)}，超期 ${late} 天。`,
      '先确认整改完成日期的口径（要填实际整改完成那一天，不是验收通过日）；确属超期的，'
      + '把超期原因与延期审批补在备注里 —— 超期未整改是检查时的直接处罚项。',
      { days: late }));
  }
  return out;
}

/** 未闭环口径（免费第 2 项与订阅版多项共用）：closed 状态 + 两个日期齐才算闭环 */
function openInfo(it, asOf) {
  const status = clean(it.status);
  const closedStatus = CLOSED_STATUSES.indexOf(status) >= 0;
  const done = parseDate(it.rectifyDate);
  const accepted = parseDate(it.acceptDate);
  if (closedStatus && done && accepted) return null;

  const found = parseDate(it.foundDate);
  const limit = normDays(it.deadlineDays);
  let due = null;
  let days = null;
  if (found && limit !== null && limit > 0) {
    due = addDays(found, limit);
    days = asOf ? dayDiff(asOf, due) : null;
  }
  const reasons = [];
  if (!closedStatus) reasons.push(`状态是「${status || '(空)'}」，还没到「已验收/已销号」`);
  if (!done) reasons.push('整改完成日期为空');
  if (!accepted) reasons.push('验收日期为空');
  return { status, done, accepted, due, days, reasons };
}

function lateText(info) {
  if (!info.due) return '表内没有可用的发现日期或整改期限，算不出已超期天数';
  if (info.days === null) return `整改期限是 ${fmtDate(info.due)}（缺统计截止日，算不出已超期天数）`;
  if (info.days > 0) return `已超期 ${info.days} 天（整改期限 ${fmtDate(info.due)}）`;
  return `尚未到期（整改期限 ${fmtDate(info.due)}，距统计截止日还有 ${-info.days} 天）`;
}

/** 2. 整改未闭环：逐条点名，按已超期天数排序 */
function checkOpenLoop(items, asOf) {
  const out = [];
  for (const it of items) {
    const info = openInfo(it, asOf);
    if (!info) continue;
    out.push(finding((info.days !== null && info.days > 0) ? 'P0' : 'P1', '整改未闭环', it,
      `${who(it)}：${info.reasons.join('；')} ⇒ 这条隐患没有闭环。${lateText(info)}。`,
      '闭环三件套：整改完成日期 + 验收日期 + 状态到「已验收/已销号」。'
      + '台账上只写「已整改」不算闭环 —— 检查时看的就是验收销号这一栏。',
      info.days === null ? undefined : { days: info.days }));
  }
  out.sort((a, b) => ((b.days || 0) - (a.days || 0)) || (a.line - b.line));
  return out;
}

/** 3. 重大隐患必须有上报日期 */
function checkMajorReport(items) {
  const out = [];
  for (const it of items) {
    const level = clean(it.level);
    if (!/重大/.test(level)) continue;
    if (!isBlank(it.reportDate)) continue;
    out.push(finding('P0', '重大隐患未上报', it,
      `${who(it)}：隐患等级是「${level}」，但上报日期为空 —— 重大隐患按规定要报告并挂牌督办，这一栏空着就是没上报。`,
      '重大隐患要向上级或属地主管部门报告并挂牌督办：把上报日期与受理单位补进台账，'
      + '报告文号与督办牌编号写在备注里，别只在会上口头说过。'));
  }
  return out;
}

/** 4. 同一位置 + 同一隐患类型重复出现 */
function checkRepeatHazard(items) {
  const out = [];
  for (const [key, list] of groupBy(items, repeatKey)) {
    if (list.length < 2) continue;
    const parts = splitKey(key);
    const last = list[list.length - 1];
    const lines = list.map((x) => x.line);
    out.push(finding('P0', '同类隐患重复出现', last,
      `${who(last)}：「${parts[0]}」的「${parts[1]}」隐患在本次台账里出现 ${list.length} 次`
      + `（第 ${lines.join('、')} 行，最早第 ${lines[0]} 行）—— 同类隐患又出现，说明上一轮只处理了表面。`,
      '重复出现的同类隐患要看根因：是设备本体没换、还是作业习惯没改。'
      + '按「定人、定时、定措施、定资金、定预案」重做一次整改，并把根因写在备注里。',
      { count: list.length }));
  }
  return out;
}

/** 5. 合计行逐列复核（隐患条数 / 整改条数 / 验收条数） */
function checkTotals(parsed) {
  const out = [];
  const tr = parsed.totalsRow;
  if (!tr) return out;
  const parts = [];
  const metrics = {};
  for (const [declaredRole, computedKey, label] of TOTALS_PAIRS) {
    const declared = normNumber(tr.declared ? tr.declared[declaredRole] : null);
    const actual = parsed.computed[computedKey];
    if (declared === null || declared === actual) continue;
    const delta = round2(declared - actual);
    parts.push(`${label} 填了 ${declared}，逐行点数是 ${actual}（差 ${delta > 0 ? '+' : ''}${delta} 条）`);
    metrics[computedKey] = delta;
  }
  if (!parts.length) return out;
  out.push(finding('P1', '合计行复核不符', { line: tr.line },
    `第 ${tr.line} 行（合计行）：${parts.join('；')}。`,
    '合计行要等于逐行点数的结果：整改条数 = 整改完成日期非空的条数，验收条数 = 验收日期非空的条数。'
    + '先确认合计行是不是还停在上个月的数，或者有没有行被隐藏、漏贴。',
    Object.keys(metrics).length ? metrics : undefined));
  return out;
}

/** 6. 空白/占位符/日期格式/日期矛盾/状态值非法 */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    const missing = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (missing.length) {
      out.push(finding('P1', '字段与取值异常', it,
        `${who(it)}：这些必需字段是空的或占位符 —— ${missing.join('、')}。`,
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }

    const dts = {};
    for (const [role, label] of DATE_FIELDS) {
      if (isBlank(it[role])) continue;
      const dt = parseDate(it[role]);
      if (!dt) {
        out.push(finding('P1', '字段与取值异常', it,
          `${who(it)}：「${label}」的值「${clean(it[role])}」不是可识别的日期`
          + '（只认 YYYY-MM-DD、YYYY/M/D、YYYY.M.D、YYYY年M月D日、YYYYMMDD）。',
          '把日期改成 YYYY-MM-DD 格式再跑；本工具不会把看不懂的日期当成今天。'));
        continue;
      }
      dts[role] = dt;
    }
    if (dts.foundDate && dts.rectifyDate && dayDiff(dts.rectifyDate, dts.foundDate) < 0) {
      out.push(finding('P1', '字段与取值异常', it,
        `${who(it)}：整改完成日期 ${fmtDate(dts.rectifyDate)} 早于发现日期 ${fmtDate(dts.foundDate)} —— 日期前后矛盾。`,
        '先确认是不是把「计划完成日期」填进了整改完成日期，或者年份写错了；这类矛盾会让期限算术整条失效。'));
    }
    if (dts.rectifyDate && dts.acceptDate && dayDiff(dts.acceptDate, dts.rectifyDate) < 0) {
      out.push(finding('P1', '字段与取值异常', it,
        `${who(it)}：验收日期 ${fmtDate(dts.acceptDate)} 早于整改完成日期 ${fmtDate(dts.rectifyDate)} —— 整改还没完成就先验收了。`,
        '验收必须发生在整改完成之后；先核对两个日期的来源（验收单日期 vs 整改回复单日期）。'));
    }
    if (dts.foundDate && dts.reportDate && dayDiff(dts.reportDate, dts.foundDate) < 0) {
      out.push(finding('P1', '字段与取值异常', it,
        `${who(it)}：上报日期 ${fmtDate(dts.reportDate)} 早于发现日期 ${fmtDate(dts.foundDate)} —— 上报不可能发生在发现之前。`,
        '核对上报日期是不是抄成了报告文号里的其他日期；重大隐患的上报时间本身就是检查重点。'));
    }

    const status = clean(it.status);
    if (status && STATUS_VALUES.indexOf(status) < 0) {
      out.push(finding('P1', '字段与取值异常', it,
        `${who(it)}：状态值是「${status}」，不在允许取值里（${STATUS_VALUES.join('、')}）。`,
        '状态用词要统一到台账口径：待整改、整改中、已整改待验收、已验收、已销号；'
        + '写「已完成」「OK」「闭环」这类自造词会让闭环统计整项失效。'));
    }

    const level = clean(it.level);
    if (level && LEVEL_VALUES.indexOf(level) < 0) {
      out.push(finding('P1', '字段与取值异常', it,
        `${who(it)}：隐患等级值是「${level}」，不在允许取值里（${LEVEL_VALUES.join('、')}）。`,
        '等级只填「一般」或「重大」；等级填错会连带影响整改期限口径与上报要求。'));
    }

    if (!isBlank(it.deadlineDays)) {
      const limit = normDays(it.deadlineDays);
      if (limit === null) {
        out.push(finding('P1', '字段与取值异常', it,
          `${who(it)}：规定整改期限的值「${clean(it.deadlineDays)}」不是可识别的天数（只认数字，可带「天」）。`,
          '期限要填数字天数（例：15），别的写法会让「整改时限达标」整项算不出来。'));
      } else if (limit <= 0) {
        out.push(finding('P1', '字段与取值异常', it,
          `${who(it)}：规定整改期限是 ${limit} 天，不是正数。`,
          '整改期限必须是正的天数；零或负数会让期限比较得出荒谬结论。'));
      }
    }

    if (!isBlank(it.ownerLimit)) {
      const lim = normNumber(it.ownerLimit);
      if (lim === null || lim < 0) {
        out.push(finding('P1', '字段与取值异常', it,
          `${who(it)}：责任人未闭环上限的值「${clean(it.ownerLimit)}」不合法（应为非负数字）。`,
          '这一列是完整档判定「责任人超载」的阈值，填成文字会让该项无法判定。'));
      }
    }
  }
  return out;
}

/* ============================ 订阅版（买断版）追加的五项 ============================ */

/** 付费：反复出现的隐患索引（同一位置 + 同一类型出现 3 次及以上） */
function recurringIndex(items) {
  const idx = new Map();
  for (const [key, list] of groupBy(items, repeatKey)) {
    if (list.length < MIN_RECURRING) continue;
    const dates = list.map((x) => parseDate(x.foundDate)).filter(Boolean).sort((a, b) => a - b);
    idx.set(key, { list, first: dates.length ? dates[0] : null, last: dates.length ? dates[dates.length - 1] : null });
  }
  return idx;
}

/** 付费：反复出现 —— 每条只在其最后一次出现的那一行出结论 */
function checkRecurringHazard(it, ctx) {
  const key = repeatKey(it);
  if (key === null) return [];
  const g = ctx.recurring.get(key);
  if (!g) return [];
  if (g.list[g.list.length - 1].line !== it.line) return [];
  const parts = splitKey(key);
  const lines = g.list.map((x) => x.line);
  const span = (g.first && g.last)
    ? `，最早发现 ${fmtDate(g.first)}、最近发现 ${fmtDate(g.last)}`
    : '';
  return [finding('P0', '反复出现的隐患', it,
    `${who(it)}：「${parts[0]}」的「${parts[1]}」隐患在统计期内出现 ${g.list.length} 次`
    + `（第 ${lines.join('、')} 行）${span} —— 已经达到「反复出现」的程度。`,
    '反复出现的隐患要按重大隐患的力度处理：查根因（设备本体、作业习惯、还是制度缺失），'
    + '整改后再安排一次专项复查，并把复查结论写进台账。',
    { count: g.list.length })];
}

/** 付费：按责任部门算 按期整改率 / 验收闭环率 */
function rateIndex(items, asOf) {
  const by = new Map();
  for (const it of items) {
    const dept = clean(it.dept) || '(未填部门)';
    if (!by.has(dept)) {
      by.set(dept, { dept, total: 0, rectified: 0, on_time: 0, accepted: 0, open: 0, overdue: 0 });
    }
    const b = by.get(dept);
    b.total += 1;
    const found = parseDate(it.foundDate);
    const limit = normDays(it.deadlineDays);
    const done = parseDate(it.rectifyDate);
    const accepted = parseDate(it.acceptDate);
    if (done) {
      b.rectified += 1;
      if (found && limit !== null && limit > 0 && dayDiff(done, addDays(found, limit)) <= 0) b.on_time += 1;
    }
    if (accepted && CLOSED_STATUSES.indexOf(clean(it.status)) >= 0) b.accepted += 1;
    const info = openInfo(it, asOf);
    if (info) {
      b.open += 1;
      if (info.days !== null && info.days > 0) b.overdue += 1;
    }
  }
  for (const b of by.values()) {
    b.on_time_rate = b.rectified > 0 ? round2(b.on_time / b.rectified) : null;
    b.close_rate = b.total > 0 ? round2(b.accepted / b.total) : null;
  }
  return by;
}

/** 付费：按期整改率 / 验收闭环率低于阈值 —— 每个部门只出结论一次 */
function checkRateThreshold(it, ctx) {
  const dept = clean(it.dept) || '(未填部门)';
  const marker = 'rate' + SEP + dept;
  if (ctx.rateDone.has(marker)) return [];
  ctx.rateDone.add(marker);
  const b = ctx.rates.get(dept);
  if (!b) return [];
  const out = [];
  const th = ctx.threshold;
  if (b.on_time_rate !== null && b.on_time_rate < th) {
    out.push(finding('P1', '按期整改率偏低', { line: it.line },
      `责任部门「${dept}」的按期整改率只有 ${pct(b.on_time_rate)}`
      + `（${b.on_time}/${b.rectified} 条在期限内完成），低于 ${pct(th)} 阈值 —— 多是期限到了才补记录。`,
      '把该部门超期的几条单独拉出来看：是期限定得不合理，还是人手/材料没到位；'
      + '调整期限要走审批，不能事后改台账上的规定整改期限。',
      { rate: b.on_time_rate }));
  }
  if (b.close_rate !== null && b.close_rate < th) {
    out.push(finding('P2', '验收闭环率偏低', { line: it.line },
      `责任部门「${dept}」的验收闭环率只有 ${pct(b.close_rate)}`
      + `（${b.accepted}/${b.total} 条验收销号），低于 ${pct(th)} 阈值 —— 台账上有隐患、闭环没跟上。`,
      '先催验收：整改完成的要拉验收组签字销号；确实整改不了的，按延期或升级重大隐患的流程走，'
      + '不要让它在台账上一直挂着「整改中」。',
      { rate: b.close_rate }));
  }
  return out;
}

/** 付费：责任人未闭环超载 —— 阈值取表内「责任人未闭环上限」列，每个责任人只出结论一次 */
function checkOwnerOverload(it, ctx) {
  const owner = clean(it.owner);
  if (!owner) return [];
  if (ctx.ownerDone.has(owner)) return [];
  ctx.ownerDone.add(owner);
  const rows = ctx.byOwner.get(owner) || [];
  const open = rows.filter((x) => openInfo(x, ctx.asOf) !== null);
  if (!open.length) return [];
  const limits = rows.map((x) => normNumber(x.ownerLimit)).filter((n) => n !== null && n >= 0);
  if (!limits.length) return [];
  const limit = Math.max.apply(null, limits);
  if (open.length <= limit) return [];
  const lines = open.map((x) => x.line);
  return [finding('P1', '责任人未闭环超载', { line: open[open.length - 1].line },
    `责任人「${owner}」名下有 ${open.length} 条隐患未闭环，超过表内给定的上限 ${limit} 条`
    + `（未闭环的行：第 ${lines.join('、')} 行）—— 一个人扛这么多整改，期限上必然兜不住。`,
    '把未闭环的隐患重新派工或加人：超载状态下最容易出现「先销号、后整改」的假闭环，'
    + '那也是检查时最容易被抓的。',
    { count: open.length })];
}

/** 付费：同一隐患类型在不同行给了不同的规定整改期限 */
function checkDeadlineConsistency(it, ctx) {
  const type = clean(it.hazardType);
  if (!type) return [];
  if (ctx.typeDone.has(type)) return [];
  ctx.typeDone.add(type);
  const rows = ctx.byType.get(type) || [];
  const seen = new Map();
  for (const x of rows) {
    const n = normDays(x.deadlineDays);
    if (n === null) continue;
    if (!seen.has(n)) seen.set(n, []);
    seen.get(n).push(x.line);
  }
  if (seen.size < 2) return [];
  const parts = [...seen.entries()].sort((a, b) => a[0] - b[0])
    .map(([v, ls]) => `${v} 天（第 ${ls.join('、')} 行）`);
  return [finding('P1', '整改期限口径不一致', { line: rows[rows.length - 1].line },
    `隐患类型「${type}」在不同的行给了不同的规定整改期限：${parts.join('；')}`
    + ' —— 同一类隐患的期限口径应当一致。',
    '统一口径：要么按分级标准（一般/重大）定统一期限，要么在备注里写明这一条为什么特殊。'
    + '口径不一致会让「整改时限达标」这一项失去意义。',
    { count: seen.size })];
}

/** 付费：分部门 × 隐患等级汇总（按未闭环数排序） */
function deptLevelIndex(items, asOf) {
  const map = new Map();
  for (const it of items) {
    const dept = clean(it.dept) || '(未填部门)';
    const level = clean(it.level) || '(未填等级)';
    const key = dept + SEP + level;
    if (!map.has(key)) {
      map.set(key, { key, dept, level, total: 0, open: 0, overdue: 0, closed: 0, lines: [] });
    }
    const b = map.get(key);
    b.total += 1;
    b.lines.push(it.line);
    const info = openInfo(it, asOf);
    if (info) {
      b.open += 1;
      if (info.days !== null && info.days > 0) b.overdue += 1;
    } else {
      b.closed += 1;
    }
  }
  return [...map.values()].sort((a, b) => (b.open - a.open)
    || String(a.dept).localeCompare(String(b.dept))
    || String(a.level).localeCompare(String(b.level)));
}

/** 付费：分部门×等级汇总里未闭环的分组逐组点名（每个分组只出结论一次） */
function checkDeptLevel(it, ctx) {
  const key = (clean(it.dept) || '(未填部门)') + SEP + (clean(it.level) || '(未填等级)');
  if (ctx.bucketDone.has(key)) return [];
  ctx.bucketDone.add(key);
  const b = ctx.buckets.find((x) => x.key === key);
  if (!b || b.open <= 0) return [];
  return [finding(b.overdue > 0 ? 'P0' : 'P1', '分部门×等级汇总', { line: b.lines[b.lines.length - 1] },
    `「${b.dept}」的「${b.level}」隐患共 ${b.total} 条，其中 ${b.open} 条未闭环`
    + `${b.overdue ? `（已超期 ${b.overdue} 条）` : ''}（行：第 ${b.lines.join('、')} 行）。`,
    '按分部门×等级的清单开会销号：先处理已超期的，再处理本月到期的；'
    + '重大隐患未闭环的要同步报告给分管负责人。',
    { count: b.open })];
}

/** 付费：按等级严重度 + 超期天数/条数排出的可整改动作清单 */
function buildConsolidatedActions(findings) {
  const rank = { P0: 0, P1: 1, P2: 2 };
  return findings.slice().sort((a, b) => (rank[a.level] - rank[b.level])
    || ((b.days || 0) - (a.days || 0))
    || ((b.count || 0) - (a.count || 0))
    || (a.line - b.line)
    || String(a.category).localeCompare(String(b.category)))
    .map((f, i) => ({
      seq: i + 1,
      level: f.level,
      line: f.line,
      category: f.category,
      days: f.days === undefined ? null : f.days,
      count: f.count === undefined ? null : f.count,
      action: f.advice || '按本行原文逐条核对后在台账上补齐闭环信息。',
    }));
}

/** 统计截止日：取表内出现的最晚日期（确定性；不用系统时间，跑多少次结果都一样） */
function maxDate(items) {
  let best = null;
  for (const it of items) {
    for (const role of ['foundDate', 'rectifyDate', 'acceptDate', 'reportDate']) {
      const dt = parseDate(it[role]);
      if (dt && (!best || dt.getTime() > best.getTime())) best = dt;
    }
  }
  return best;
}

/** 阈值解析：0.9 / 90 / 90% 都当 90% 用；非法值退回默认 */
function resolveThreshold(raw) {
  const n = normNumber(raw);
  if (n === null) return RATE_THRESHOLD_DEFAULT;
  const v = n > 1 ? n / 100 : n;
  if (v <= 0 || v > 1) return RATE_THRESHOLD_DEFAULT;
  return v;
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的隐患排查治理台账（登记、责任、期限、整改、验收、状态、上报）']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的隐患排查治理台账（登记、责任、期限、整改、验收、状态、上报）']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的隐患排查治理台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行隐患明细（现在只有表头或合计行，没有可核对的隐患记录）']);
  }

  const asOf = maxDate(t.items);
  const notes = [];
  if (!asOf) {
    notes.push('表内没有一条可解析的日期 ⇒ 算不出「已超期天数」，相关结论只报缺失与未闭环，不报天数。');
  }
  if (!t.totalsRow) {
    notes.push('本表没有「合计」行 ⇒ 第 5 项「合计行逐列复核」本次未执行（不是通过）。');
  } else {
    const declared = TOTALS_PAIRS
      .filter(([role]) => normNumber(t.totalsRow.declared ? t.totalsRow.declared[role] : null) !== null);
    if (!declared.length) {
      notes.push('有「合计」行，但三个数量类列（隐患条数/整改条数/验收条数）都空着 ⇒ 第 5 项无可比对，本次未执行。');
    }
  }

  const paid = Boolean(p && (p.full || p.credit || p.token));
  const findings = [];
  const notRun = [];
  let paidExtras = null;

  for (const f of checkOverdue(t.items)) findings.push(f);
  for (const f of checkOpenLoop(t.items, asOf)) findings.push(f);
  for (const f of checkMajorReport(t.items)) findings.push(f);
  for (const f of checkRepeatHazard(t.items)) findings.push(f);
  for (const f of checkTotals(t)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  if (paid) {
    const ctx = {
      asOf,
      threshold: resolveThreshold(p.rate_threshold),
      recurring: recurringIndex(t.items),
      rates: rateIndex(t.items, asOf),
      byOwner: groupBy(t.items, (x) => (clean(x.owner) ? clean(x.owner) : null)),
      byType: groupBy(t.items, (x) => (clean(x.hazardType) ? clean(x.hazardType) : null)),
      buckets: deptLevelIndex(t.items, asOf),
      rateDone: new Set(),
      ownerDone: new Set(),
      typeDone: new Set(),
      bucketDone: new Set(),
    };
    for (const it of t.items) {
      for (const f of (checkRecurringHazard(it, ctx) || [])) findings.push(f);
      for (const f of (checkRateThreshold(it, ctx) || [])) findings.push(f);
      for (const f of (checkOwnerOverload(it, ctx) || [])) findings.push(f);
      for (const f of (checkDeadlineConsistency(it, ctx) || [])) findings.push(f);
      for (const f of (checkDeptLevel(it, ctx) || [])) findings.push(f);
    }
    paidExtras = { ctx };
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || ((y.days || 0) - (x.days || 0)));

  const openLoop = findings.filter((f) => f.category === '整改未闭环').slice()
    .sort((a, b) => ((b.days || 0) - (a.days || 0)) || (a.line - b.line));

  const summary = {
    rows: t.items.length,
    total: findings.length,
    p0: findings.filter((f) => f.level === 'P0').length,
    p1: findings.filter((f) => f.level === 'P1').length,
    p2: findings.filter((f) => f.level === 'P2').length,
    as_of: asOf ? fmtDate(asOf) : null,
    overdue_count: findings.filter((f) => f.category === '整改超期').length,
    open_loop_count: openLoop.length,
    major_unreported_count: findings.filter((f) => f.category === '重大隐患未上报').length,
    repeat_group_count: findings.filter((f) => f.category === '同类隐患重复出现').length,
    field_issue_count: findings.filter((f) => f.category === '字段与取值异常').length,
    totals_row_line: t.totalsRow ? t.totalsRow.line : null,
    declared_totals: t.totalsRow ? {
      count: normNumber(t.totalsRow.declared.totalCount),
      rectified: normNumber(t.totalsRow.declared.totalRectified),
      accepted: normNumber(t.totalsRow.declared.totalAccepted),
    } : null,
    computed_totals: t.computed,
    deadline_days_total: t.totals.deadlineDays,
    open_loop_ranked: openLoop.map((f) => ({ line: f.line, days: f.days === undefined ? null : f.days })),
    notes,
    basis: '整改时限 = 发现日期 + 规定整改期限(天)，与整改完成日期比较，超出即报超期天数；'
      + '闭环 = 状态到「已验收/已销号」且整改完成日期与验收日期都非空；'
      + '重大隐患必须有上报日期；同一位置 + 同一隐患类型出现 2 次即报重复出现；'
      + '合计行的隐患条数/整改条数/验收条数按逐行点数复核（整改条数 = 整改完成日期非空的行数，'
      + '验收条数 = 验收日期非空的行数）；统计截止日取表内最晚日期，'
      + '已超期天数 = 统计截止日 − 整改期限日。',
  };

  const result = {
    findings,
    summary,
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径自洽**：'
      + '期限算得通、该闭环的都闭环了、重大隐患都写了上报日期、合计行点数对得上。'
      + '不代表现场隐患已经消除、不代表整改措施有效、也不代表安全生产条件已经合规 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.items.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    as_of: summary.as_of,
    open_loop: summary.open_loop_count,
    overdue: summary.overdue_count,
  };
  result.scope = scope;

  if (paid && paidExtras) {
    const ctx = paidExtras.ctx;
    result.rate_summary = {
      threshold: ctx.threshold,
      by_dept: [...ctx.rates.values()].sort((a, b) => String(a.dept).localeCompare(String(b.dept))),
    };
    result.dept_level_summary = ctx.buckets.map((b) => ({
      dept: b.dept, level: b.level, total: b.total, open: b.open, overdue: b.overdue, closed: b.closed,
    }));
    result.consolidated_actions = buildConsolidatedActions(findings);
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
