#!/usr/bin/env node
/**
 * tower-crane-inspection-check-full.js —— 塔式起重机备案与检测核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：塔式起重机（塔机）是**建筑起重机械**，总包、租赁单位、监理与安监四方手里都有一本
 * 「塔机台账」。安监来项目上查的第一份资料就是它，而每月必须核一遍的硬项是：
 *   ① 检测有效期覆盖：第三方检测报告上的「检测日期 + 下次检测日期」必须盖住本次核对基准日，
 *      超期未检还在吊装是**停工整改 + 事故责任**级问题（塔机倾覆事故几乎都伴随超期或超载）；
 *   ② 备案与持证：使用登记证（有的地方是产权备案 + 使用登记两道）不得为空；司机（塔式起重机司机）
 *      与信号工（信号司索工）都必须持特种作业操作证，证件有效期要覆盖核对基准日；
 *   ③ 检测结论：结论写了「不合格」或只写了「复检」，就等于没有可用的检测结论；
 *   ④ 一本台账里同一台设备只应有一行（重复登记会让两个检测周期各算一套）；
 *   ⑤ 合计行（设备台数、检测台数）必须与明细行加总一致；
 *   ⑥ 关键字段缺失 / 日期非法 / 数值为负 —— 这些是"看起来查过了其实没查"的根源。
 *   核错一项就可能让一台超期塔机继续吊装 —— 所以每条结论都必须能拿原文复算。
 *
 * 本文件同时服务**订阅版（买断版）**与**本包**两个包：
 *   · 订阅版执行全部检查项（免费六项 + 追加五项：超期未检仍在用、停用/已拆除塔机仍在使用记录、
 *     无证上岗、顶升加节与附着验收断档、分产权单位与分使用项目的汇总清单）；
 *   · 本包只执行免费六项。追加项的实现在免费包里被 `tools/strip_free_engine.py` 整块摘除，
 *     免费包的 `CHECKS_WITHHELD` 里只剩**说明文本**，不是实现。
 *
 * 跨表材料用 `--- 段名 ---` 分行送入（**不要用等号包裹的段名**，那是批量入口 batch.mjs 的多期分隔符）：
 *   `--- 塔机使用运行记录 ---`（设备编号 / 记录日期 / 当班司机 / 当班信号工）
 *   `--- 特种作业人员持证名单 ---`（人员姓名 / 工种 / 证件有效期）
 *   `--- 顶升加节与附着验收记录 ---`（设备编号 / 顶升次序 / 验收日期 / 验收结论）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定这台塔机该不该检、不判定检测报告与证件本身的真伪、不判定现场是否真的停用或拆除、
 *          不读 .xlsx / .pdf 原件、不联网核验备案与证件；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '检测有效期覆盖（核对基准日 ≤ 下次检测日期；超期逐台给出已超期天数）',
  '使用登记证与特种作业人员证覆盖（使用登记证号不得为空；司机 / 信号工都要填，且「证件有效期」要覆盖核对基准日；缺证 / 过期逐台点名）',
  '检测结论核对（结论非「合格」逐台点名：写「不合格」按 P0，只写「复检」视为复检未闭环）',
  '同一设备编号重复登记（一本塔机台账里设备编号唯一）',
  '合计行逐列复核（数量类列：设备台数、检测台数）',
  '字段合法性（关键字段缺失、日期格式非法、数值为负或非法、运行状态与检测结论取值非法）',
];

const CHECKS_WITHHELD = [
  '超期未检仍在用（下次检测日期已过且运行状态=在用；按超期天数降序点名并附已超期天数）',
  '停用 / 已拆除塔机仍出现在使用运行记录（跨表交叉核对：台账运行状态为停用或已拆除，却在「塔机使用运行记录」段里出现，逐条点出记录原文行号）',
  '无证上岗（使用运行记录里的当班司机 / 当班信号工不在「特种作业人员持证名单」里、工种与岗位不符、或证件有效期早于当次作业记录日期）',
  '顶升加节与附着验收记录断档（按设备把顶升次序与验收记录逐次配对，缺哪一次就点哪一次）',
  '分产权单位与分使用项目的汇总清单（按超期天数降序，每组给出可整改动作，并附逐台整改清单）',
];

const OUT_OF_SCOPE = [
  '判定这台塔机该不该检、该做定期检测还是安装（拆卸）告知、该不该办理使用登记（那是检验检测机构、总包与住建主管部门的法定口径，本工具只核台账日期与结论字段是否自洽）',
  '判定检测报告本身的真实性、检测机构资质与检测结论的技术依据是否成立（那是检验检测机构与监管部门的判定权）',
  '判定现场是否真的停了 / 拆了、顶升加节作业是否真的做过（本工具只核台账与使用运行记录 / 验收记录的字面一致性）',
  '读取 .xlsx / .pdf 原件、联网核验使用登记证 / 特种作业操作证 / 检测报告的真伪，替代项目安全员或安监部门的认定',
];

// 样例：一本**干净**的塔机备案与检测台账 —— 四台塔机、两个在建项目、两家产权单位，
// 检测有效期覆盖核对基准日、备案号与司机 / 信号工证件都在有效期内、检测结论都是「合格」、
// 设备编号不重复、合计行与明细一致；三段跨表材料（使用运行记录 / 持证名单 / 顶升验收）
// 也逐条自洽：没有停用设备在跑、没有无证上岗、顶升次序连续。**全表零命中**。
const SAMPLE_TEXT = [
  '设备编号\t设备名称\t产权单位\t使用项目\t使用登记证号\t检测日期\t检测结论\t下次检测日期\t司机\t信号工\t证件有效期\t运行状态\t设备台数\t检测台数\t核对基准日\t备注',
  'TC-2026-001\t塔式起重机 QTZ80\t华远机械租赁\t云锦花园1号楼项目\t苏建登字2026-0101\t2025-06-20\t合格\t2026-06-20\t赵大勇\t钱小梅\t2027-03-15\t在用\t1\t1\t2026-04-30\t检测合格',
  'TC-2026-002\t塔式起重机 QTZ63\t华远机械租赁\t云锦花园1号楼项目\t苏建登字2026-0102\t2025-07-05\t合格\t2026-07-05\t孙志强\t李桂芳\t2027-05-20\t在用\t1\t1\t2026-04-30\t检测合格',
  'TC-2026-003\t塔式起重机 QTZ125\t恒达设备租赁\t星港商务中心项目\t苏建登字2026-0203\t2025-09-12\t合格\t2026-09-12\t周建华\t吴秀英\t2028-01-10\t在用\t1\t1\t2026-04-30\t检测合格',
  'TC-2026-004\t塔式起重机 QTZ80\t恒达设备租赁\t星港商务中心项目\t苏建登字2026-0204\t2025-05-18\t合格\t2026-05-18\t郑海峰\t王丽娟\t2027-11-30\t在用\t1\t1\t2026-04-30\t检测合格',
  '合计\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t4\t4\t—\t4 台塔机、4 台已检测由明细行加总',
  '--- 塔机使用运行记录 ---',
  '设备编号\t记录日期\t当班司机\t当班信号工',
  'TC-2026-001\t2026-04-01\t赵大勇\t钱小梅',
  'TC-2026-001\t2026-04-02\t赵大勇\t钱小梅',
  'TC-2026-002\t2026-04-01\t孙志强\t李桂芳',
  'TC-2026-003\t2026-04-03\t周建华\t吴秀英',
  'TC-2026-004\t2026-04-04\t郑海峰\t王丽娟',
  '--- 特种作业人员持证名单 ---',
  '人员姓名\t工种\t证件有效期',
  '赵大勇\t塔式起重机司机\t2027-03-15',
  '钱小梅\t信号司索工\t2027-06-30',
  '孙志强\t塔式起重机司机\t2027-05-20',
  '李桂芳\t信号司索工\t2028-02-28',
  '周建华\t塔式起重机司机\t2028-01-10',
  '吴秀英\t信号司索工\t2028-09-30',
  '郑海峰\t塔式起重机司机\t2027-11-30',
  '王丽娟\t信号司索工\t2029-01-31',
  '--- 顶升加节与附着验收记录 ---',
  '设备编号\t顶升次序\t验收日期\t验收结论',
  'TC-2026-001\t1\t2026-03-05\t合格',
  'TC-2026-002\t1\t2026-03-08\t合格',
  'TC-2026-003\t1\t2026-03-20\t合格',
  'TC-2026-003\t2\t2026-04-10\t合格',
].join('\n');

const TOL = 0.01;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'deviceNo', 'deviceName', 'ownerUnit', 'regCertNo', 'inspectDate', 'inspectConclusion',
  'nextInspectDate', 'driver', 'signaler', 'certExpiry', 'runStatus', 'checkDate',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['deviceNo', '设备编号'],
  ['deviceName', '设备名称/型号'],
  ['ownerUnit', '产权单位'],
  ['regCertNo', '使用登记证号'],
  ['inspectDate', '检测日期'],
  ['inspectConclusion', '检测结论'],
  ['nextInspectDate', '下次检测日期'],
  ['driver', '司机'],
  ['signaler', '信号工'],
  ['certExpiry', '证件有效期'],
  ['runStatus', '运行状态'],
  ['checkDate', '核对基准日'],
];

// 日期列（格式非法逐格点名）
const DATE_FIELDS = [
  ['inspectDate', '检测日期'],
  ['nextInspectDate', '下次检测日期'],
  ['certExpiry', '证件有效期'],
  ['checkDate', '核对基准日'],
];

// 数值列（为负 / 无法解析逐格点名）
const NUMBER_FIELDS = [
  ['deviceCount', '设备台数'],
  ['inspectCount', '检测台数'],
];

// 运行状态只认这四个值（建筑起重机械台账口径）
const RUN_STATUSES = ['在用', '停用', '已拆除', '检修'];

// 检测结论只认这四个值：合格 / 不合格 / 复检 / 复检合格
const CONCLUSION_PASS = '合格';
const CONCLUSION_FAIL = '不合格';
const CONCLUSION_RECHECK = '复检';
const CONCLUSION_RECHECK_PASS = '复检合格';
const CONCLUSIONS = [CONCLUSION_PASS, CONCLUSION_FAIL, CONCLUSION_RECHECK, CONCLUSION_RECHECK_PASS];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词就会把更具体的列抢走（本仓库踩过多次，见 tools/header_map_check.py）。
//    本表的坑位有三处，都必须按「更具体 → 更宽泛」排：
//      ① 日期列：下次检测日期 / 检测日期 / 验收日期 / 记录日期 —— 兜底的 '日期' 只能放在最后；
//      ② 岗位列：当班司机 / 当班信号工 必须排在 司机 / 信号工 前面；
//      ③ 结论列：验收结论 排在 检测结论 前面。
const ROLES = {
  deviceNo: ['设备编号', '备案编号', '设备代码', '设备备案号', '塔机编号'],
  deviceName: ['设备名称', '设备型号', '塔机型号', '规格型号', '设备名'],
  regCertNo: ['使用登记证号', '登记证号', '使用登记编号', '产权备案号'],
  nextInspectDate: ['下次检测日期', '下次检测日', '下次检验日期', '下次检测'],
  inspectDate: ['检测日期', '检测日', '检验日期', '上次检测日期'],
  acceptConclusion: ['验收结论', '附着验收结论'],
  inspectConclusion: ['检测结论', '检测评定', '检验结论'],
  liftSeq: ['顶升次序', '顶升次数', '加节次序', '顶升序号', '次序'],
  acceptDate: ['验收日期', '验收日', '附着验收日期'],
  recordDate: ['记录日期', '使用记录日期', '运行日期', '作业日期', '日期'],
  driverOnDuty: ['当班司机', '当班塔机司机'],
  signalerOnDuty: ['当班信号工', '当班司索信号工'],
  driver: ['司机', '塔机司机', '起重司机'],
  signaler: ['信号工', '司索信号工', '信号司索工', '指挥工'],
  personName: ['人员姓名', '姓名', '持证人'],
  jobType: ['工种', '作业类别', '作业种类'],
  certExpiry: ['证件有效期', '证件到期日', '人员证有效期', '有效期至'],
  ownerUnit: ['产权单位', '产权方', '出租单位', '使用单位', '所属单位', '单位'],
  project: ['使用项目', '项目名称', '工程项目', '项目', '工地'],
  runStatus: ['运行状态', '使用状态', '塔机状态', '机械状态'],
  // ⚠️ 检测台数 必须排在 设备台数 前面：否则「设备台数」里的兜底关键词 '台数'
  //    会把「检测台数」抢走（两列落到同一个角色 ⇒ 检测台数整列静默不参与合计复核）。
  inspectCount: ['检测台数', '检测数量', '已检测台数'],
  deviceCount: ['设备台数', '设备数量', '台数'],
  checkDate: ['核对基准日', '核对日期', '核查日期', '基准日期', '基准日'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  deviceNo: '设备编号',
  deviceName: '设备名称/型号',
  ownerUnit: '产权单位',
  project: '使用项目',
  regCertNo: '使用登记证号',
  inspectDate: '检测日期',
  inspectConclusion: '检测结论',
  nextInspectDate: '下次检测日期',
  driver: '司机',
  signaler: '信号工',
  certExpiry: '证件有效期',
  runStatus: '运行状态',
  deviceCount: '设备台数',
  inspectCount: '检测台数',
  checkDate: '核对基准日',
  recordDate: '记录日期',
  driverOnDuty: '当班司机',
  signalerOnDuty: '当班信号工',
  personName: '人员姓名',
  jobType: '工种',
  liftSeq: '顶升次序',
  acceptDate: '验收日期',
  acceptConclusion: '验收结论',
  note: '备注',
};

const SUM_ROLES = ['deviceCount', 'inspectCount'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这本塔机台账补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）；'
      + '跨表材料（使用运行记录 / 持证名单 / 顶升验收记录）用 `--- 段名 ---` 单独起段。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「覆盖」，也不说「超期」。',
  };
}

/** 全角 → 半角（Excel 导出的台账里 ０-９ 与 ．－％ 经常是全角） */
function toHalfWidth(raw) {
  return String(raw == null ? '' : raw)
    .replace(/[\uFF01-\uFF5E]/g, (ch) => String.fromCharCode(ch.charCodeAt(0) - 0xFEE0))
    .replace(/\u3000/g, ' ');
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = toHalfWidth(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^[-+]?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace(/[+%]/g, ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = toHalfWidth(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核|暂无)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

/** 日期归一化成 YYYY-MM-DD；认不出来返回 null（认不出来绝不当成今天） */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  let s = toHalfWidth(raw).trim();
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  s = s.replace(/[年月]/g, '-').replace(/日/g, '').replace(/[.／/]/g, '-').replace(/\s+/g, '');
  if (/^\d{8}$/.test(s)) s = s.slice(0, 4) + '-' + s.slice(4, 6) + '-' + s.slice(6, 8);
  const m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const dt = new Date(Date.UTC(y, mo - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return m[1] + '-' + String(mo).padStart(2, '0') + '-' + String(d).padStart(2, '0');
}

const DAY_MS = 86400000;
function dayNum(iso) {
  const p = iso.split('-').map(Number);
  return Date.UTC(p[0], p[1] - 1, p[2]) / DAY_MS;
}
/** b − a（整天数，正数表示 b 在 a 之后） */
function daysBetween(a, b) {
  return dayNum(b) - dayNum(a);
}

const SECTION_RE = /^\s*-{2,}\s*(.+?)\s*-{2,}\s*$/;
function isSectionMarker(line) {
  return SECTION_RE.test(String(line == null ? '' : line));
}

function roleOf(header) {
  const h = toHalfWidth(header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

const TOTAL_LABEL = /^(合计|小计|总计|总合计|合\s*计)$/;
/** 合计行不是设备明细：逐台检查要跳过它，只有「合计行逐列复核」那一项会用到它 */
function isTotalRow(it) {
  const no = String(it.deviceNo == null ? '' : it.deviceNo).trim();
  const name = String(it.deviceName == null ? '' : it.deviceName).trim();
  return TOTAL_LABEL.test(no) || TOTAL_LABEL.test(name);
}

/**
 * 解析成 {header, cols, items, detail, totalRows, totals, missingRoles, missingColumns, error}。
 * items 是**扁平**对象：{line, raw, isTotal, 角色:值…}；遇到 `--- 段名 ---` 就停（后面是另一张表）。
 */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (isSectionMarker(rawLines[i])) break;
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], detail: [], totalRows: [], totals: {},
      missingRoles: REQUIRED_ROLES.slice(), missingColumns: REQUIRED_ROLES.map((r) => LABELS[r]),
    };
  }

  const header = splitRow(rows[0].raw);
  const cols = header.map((h, k) => ({ header: h, role: roleOf(h), index: k }));
  const items = [];
  for (let r = 1; r < rows.length; r++) {
    const cells = splitRow(rows[r].raw);
    const it = { line: rows[r].line, raw: rows[r].raw };
    for (const c of cols) {
      if (!c.role) continue;
      it[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
    }
    it.isTotal = isTotalRow(it);
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(detail.reduce((acc, it) => {
      const n = normNumber(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    detail,
    totalRows,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

function who(it) {
  const name = String(it.deviceName == null ? '' : it.deviceName).trim();
  const no = String(it.deviceNo == null ? '' : it.deviceNo).trim();
  return `第 ${it.line} 行「${name || no || '未命名塔机'}${name && no ? ' / ' + no : ''}」`;
}

const cell = (it, role) => String(it[role] == null ? '' : it[role]).trim();

/** 每条结论都带原文依据：行号 + 设备编号 + 该行原文（截断），可被第三方用同一口径复算 */
function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    device_no: String(it.deviceNo == null ? '' : it.deviceNo).trim(),
    evidence: String(it.raw == null ? '' : it.raw).slice(0, 200),
    message,
  };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/** 台账里第一个能认出来的核对基准日（逐行没填时兜底；逐行填了就以逐行为准） */
function baseDateOf(items) {
  for (const it of items) {
    const d = normDate(it.checkDate);
    if (d) return d;
  }
  return null;
}
const baseOf = (it, base) => normDate(it.checkDate) || base;

/* ============================ 本包检查（六项） ============================ */

function checkInspectionValidity(items, base) {
  // ① 检测有效期覆盖：核对基准日 ≤ 下次检测日期；不覆盖就报超期天数（逐台）
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const next = normDate(it.nextInspectDate);
    const b = baseOf(it, base);
    if (!next || !b) continue;                    // 缺字段 / 格式非法交给第 ⑥ 项点名
    const over = daysBetween(next, b);
    if (over <= 0) continue;
    const status = cell(it, 'runStatus');
    out.push(finding(status === '在用' ? 'P0' : 'P1', '检测超期', it, over,
      `${who(it)}：核对基准日 ${b} 已晚于下次检测日期 ${next}，**已超期 ${over} 天**`
      + `（检测日期 ${cell(it, 'inspectDate') || '(未填)'}，运行状态 ${status || '(未填)'}，`
      + `产权单位 ${cell(it, 'ownerUnit') || '(未填)'}）。`,
      '建筑起重机械检测超期仍在用是停工整改项：先按上面天数把定期检测排进本月计划，'
      + '在用塔机要先停用挂牌；检测合格并把新的下次检测日期填回台账后再恢复吊装。别只改台账日期。'));
  }
  return out;
}

function checkRegistrationAndCertificates(items, base) {
  // ② 使用登记证 + 特种作业人员证：登记证号不得为空；司机 / 信号工都要填，证件有效期要覆盖核对基准日
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const b = baseOf(it, base);

    const no = cell(it, 'regCertNo');
    if (isBlank(no)) {
      out.push(finding('P1', '使用登记证缺失', it, undefined,
        `${who(it)}：使用登记证号是空的 —— 塔机投入使用前要办理使用登记（有的地方是产权备案 + 使用登记两道），`
        + `缺证就说不上"已备案"（产权单位 ${cell(it, 'ownerUnit') || '(未填)'}）。`,
        '去工程所在地住建主管部门的起重机械备案 / 使用登记窗口补办，把证号与办理日期填回台账；'
        + '这一步不做，后面所有"台账齐不齐"的结论都站不住。'));
    }

    const drv = cell(it, 'driver');
    const sig = cell(it, 'signaler');
    const missingPeople = [];
    if (isBlank(drv)) missingPeople.push('司机');
    if (isBlank(sig)) missingPeople.push('信号工');
    if (missingPeople.length) {
      out.push(finding('P1', '特种作业人员证过期或缺失', it, undefined,
        `${who(it)}：${missingPeople.join('、')}这一栏是空的 —— 塔式起重机司机与信号司索工都必须持证上岗，`
        + '人名空着这一项就永远核不了（缺的是人，不是"没问题"）。',
        '把本台塔机当班司机与信号工的姓名逐台补进台账（并与持证名单对得上），再补各自的证件有效期。'));
    }

    const exp = cell(it, 'certExpiry');
    if (isBlank(exp)) {
      out.push(finding('P1', '特种作业人员证过期或缺失', it, undefined,
        `${who(it)}：证件有效期是空的 —— 司机 ${drv || '(未填)'} / 信号工 ${sig || '(未填)'} 的证件到期日没有填，`
        + `无法判断是否覆盖核对基准日 ${b || '(未填)'}。`,
        '「证件有效期」按**本台塔机当班司机与信号工中较早到期的那一个**填写（从严口径）；'
        + '两人各自的到期日在持证名单里逐人维护。证件在别处的也必须在台账里能点到。'));
    } else {
      const d = normDate(exp);
      if (d && b && daysBetween(d, b) > 0) {
        const over = daysBetween(d, b);
        out.push(finding('P0', '特种作业人员证过期或缺失', it, over,
          `${who(it)}：证件有效期 ${d}，早于核对基准日 ${b}，**已过期 ${over} 天**`
          + `（司机 ${drv || '(未填)'} / 信号工 ${sig || '(未填)'}）。`,
          '证件过期期间不得独立操作：先安排复审或换人，复审通过后再把这台塔机交回原持证人；'
          + '台账上的「证件有效期」要跟着持证名单一起更新。'));
      }
    }
  }
  return out;
}

function checkConclusions(items) {
  // ③ 检测结论：非「合格」逐台点名 —— 不合格 P0，只写「复检」视为复检未闭环
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const c = cell(it, 'inspectConclusion');
    if (isBlank(c)) continue;                    // 缺结论交给第 ⑥ 项点名
    const idate = cell(it, 'inspectDate') || '(未填)';
    const ndate = cell(it, 'nextInspectDate') || '(未填)';
    if (c === CONCLUSION_FAIL) {
      out.push(finding('P0', '检测结论不合格', it, undefined,
        `${who(it)}：检测结论写的是「不合格」（检测日期 ${idate}，下次检测日期 ${ndate}）—— `
        + '不合格的塔机不得继续使用；台账上留着这一行、运行状态还写着「'
        + (cell(it, 'runStatus') || '(未填)') + '」更危险。',
        '不合格塔机立即停用挂牌、撤离或整修：整修后重新做检测并拿到合格报告，'
        + '再把结论改成「合格」并更新下次检测日期；整修期间不得安排吊装作业。'));
    } else if (c === CONCLUSION_RECHECK) {
      out.push(finding('P1', '复检未闭环', it, undefined,
        `${who(it)}：检测结论只写了「复检」（检测日期 ${idate}，下次检测日期 ${ndate}）—— `
        + '说明首检没通过、要复检，而**复检结论还没有写回台账**，这一行现在等于没有可用的检测结论。',
        '复检做完后把结论改成「合格」或「复检合格」，并把复检报告归档；'
        + '复检未出结论前该塔机不得投入吊装作业，这一条要写进整改单闭环。'));
    }
  }
  return out;
}

function checkDuplicateDevice(items) {
  // ④ 同一设备编号重复登记：一本台账里设备编号唯一
  const out = [];
  const first = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const no = cell(it, 'deviceNo');
    if (!no) continue;
    if (first.has(no)) {
      out.push(finding('P0', '设备重复登记', it, undefined,
        `${who(it)}：设备编号「${no}」在第 ${first.get(no)} 行已经出现过 —— 同一台塔机重复登记。`
        + `本次这行名称是「${cell(it, 'deviceName') || '(未填)'}」，产权单位「${cell(it, 'ownerUnit') || '(未填)'}」。`,
        '一台塔机在一本台账里只应有一行：重复登记会让两个检测周期、两套证件各算一套，'
        + '极容易出现"其中一行超期了却没人发现"。合并成一行，历史检测记录写进备注。'));
    } else {
      first.set(no, it.line);
    }
  }
  return out;
}

function checkTotals(items, cols) {
  // ⑤ 合计行逐列复核：数量类列（设备台数、检测台数）的合计行必须等于明细行加总
  const out = [];
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  for (const tr of totalRows) {
    for (const role of SUM_ROLES) {
      if (!cols.some((c) => c.role === role)) continue;
      const raw = tr[role];
      if (isBlank(raw)) continue;
      const declared = normNumber(raw);
      if (declared === null) {
        out.push(finding('P1', '合计行不符', tr, undefined,
          `第 ${tr.line} 行合计行的「${LABELS[role]}」值是「${String(raw).trim()}」，不是可识别的数字。`,
          '合计行只能写数字；请核对是否把单位（台）写进了单元格里，或写成了「4台」这种带文字的形态。'));
        continue;
      }
      const actual = round2(detail.reduce((acc, it) => {
        const n = normNumber(it[role]);
        return acc + (n === null ? 0 : n);
      }, 0));
      const diff = round2(declared - actual);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P1', '合计行不符', tr, diff,
        `第 ${tr.line} 行合计行的「${LABELS[role]}」写着 ${declared}，但上面 ${detail.length} 行明细逐行加总是 ${actual}，`
        + `差 ${diff}（合计 − 明细）。`,
        '合计行必须等于明细行逐列加总：先看有没有明细行被隐藏 / 筛选掉了，'
        + '再看是不是把停用、已拆除的塔机漏统计或少统计了。'
        + '（本工具只核这一个合计行，不替你去别的表里找补。）'));
    }
  }
  return out;
}

function checkFieldIntegrity(items) {
  // ⑥ 空白 / 占位符 / 日期格式 / 数值为负 / 运行状态与检测结论取值非法
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了（例如下次检测日期空着就判不了检测覆盖，司机空着就判不了持证）；'
        + '补全后重跑，本工具不会替你猜一个默认值。'));
    }

    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDate(raw) === null) {
        out.push(finding('P1', '日期格式非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
          + '（只认 2026-04-30 / 2026/4/30 / 2026年4月30日 / 20260430 这几种形态）。',
          '把日期改成 2026-04-30 这种形态再跑；日期认不出来时本工具不会拿它去算超期天数。'));
      }
    }

    for (const [role, label] of NUMBER_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数值为负或非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数字。`,
          '台数必须是纯数字（如 1）；写成「一台」「壹」这类形态本工具一律不给结论。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数值为负或非法', it, n,
          `${who(it)}：「${label}」是负数（${n}）—— 台账里的台数出现负数，通常是填反了或写成了红字。`,
          '确认是红字冲销还是填错方向；确属冲销的请写在备注里并保留原值，别直接改成正数。'));
      }
    }

    const status = cell(it, 'runStatus');
    if (status && RUN_STATUSES.indexOf(status) < 0) {
      out.push(finding('P1', '运行状态非法', it, undefined,
        `${who(it)}：运行状态写的是「${status}」，不在允许的四个值里（${RUN_STATUSES.join(' / ')}）。`,
        '运行状态会直接决定"超期未检仍在用"与"停用塔机还在跑"这两类结论：'
        + '按实际情况改成 在用 / 停用 / 已拆除 / 检修 之一（拆掉的写「已拆除」，别写「拆除完成」「已拆」）。'));
    }

    const concl = cell(it, 'inspectConclusion');
    if (concl && CONCLUSIONS.indexOf(concl) < 0) {
      out.push(finding('P1', '检测结论非法', it, undefined,
        `${who(it)}：检测结论写的是「${concl}」，不在允许的四个值里（${CONCLUSIONS.join(' / ')}）。`,
        '检测结论必须是这四个值之一：合格 / 不合格 / 复检 / 复检合格。'
        + '写成「基本合格」「合格（附条件）」这类自由文本，本工具无法判断它算不算通过。'));
    }
  }
  return out;
}

/* ============================ 跨表材料解析（订阅版） ============================ */

function parseSections(text) {
  // 把每个 `--- 段名 ---` 之后的每一段单独当一张表解析
  // （主台账之后的塔机使用运行记录 / 持证名单 / 顶升验收记录都在这里）
  const lines = String(text == null ? '' : text).split(/\r?\n/);
  const found = [];
  let cur = null;
  for (let i = 0; i < lines.length; i++) {
    const m = SECTION_RE.exec(lines[i]);
    if (m) {
      cur = { name: m[1].trim(), lines: [], start: i + 2 };
      found.push(cur);
      continue;
    }
    if (!cur) continue;
    cur.lines.push(lines[i]);
  }
  const out = {};
  for (const s of found) {
    if (!s.lines.some((l) => String(l).trim() !== '')) continue;
    const t = parseTable(s.lines.join('\n'));
    for (const it of t.items) it.line += (s.start - 1);       // 行号换回**全文**行号，才能对上原文
    out[s.name] = t;
  }
  return out;
}

function pickSection(sections, re) {
  for (const n of Object.keys(sections || {})) {
    if (re.test(n)) return { name: n, table: sections[n] };
  }
  return null;
}

function readRunRecords(sections) {
  // 塔机使用运行记录：设备编号 / 记录日期 / 当班司机 / 当班信号工
  const hit = pickSection(sections, /使用运行记录|塔机运行记录|使用记录/);
  if (!hit) return { present: false, name: '', rows: [], missing: [] };
  const table = hit.table;
  const missing = [];
  if (!table.cols.some((c) => c.role === 'deviceNo')) missing.push('设备编号');
  if (!table.cols.some((c) => c.role === 'recordDate')) missing.push('记录日期');
  const rows = (table.items || []).map((it) => ({
    line: it.line,
    device_no: cell(it, 'deviceNo'),
    date: normDate(it.recordDate),
    date_raw: cell(it, 'recordDate'),
    driver: cell(it, 'driverOnDuty'),
    signaler: cell(it, 'signalerOnDuty'),
    raw: String(it.raw == null ? '' : it.raw).slice(0, 200),
  }));
  return { present: true, name: hit.name, rows, missing };
}

function readCertRoster(sections) {
  // 特种作业人员持证名单：人员姓名 / 工种 / 证件有效期
  const hit = pickSection(sections, /持证名单|特种作业人员|人员持证|操作证名单/);
  if (!hit) return { present: false, name: '', rows: [], byName: new Map(), missing: [] };
  const table = hit.table;
  const missing = [];
  if (!table.cols.some((c) => c.role === 'personName')) missing.push('人员姓名');
  if (!table.cols.some((c) => c.role === 'certExpiry')) missing.push('证件有效期');
  const rows = (table.items || []).map((it) => ({
    line: it.line,
    name: cell(it, 'personName'),
    job: cell(it, 'jobType'),
    expiry: cell(it, 'certExpiry'),
    raw: String(it.raw == null ? '' : it.raw).slice(0, 200),
  }));
  const byName = new Map();
  for (const r of rows) {
    if (!r.name) continue;
    const prev = byName.get(r.name);
    if (!prev) { byName.set(r.name, r); continue; }
    // 同一人重复登记时取**较早到期**的那条（从严），并保留能认出来的工种
    const a = normDate(prev.expiry);
    const b = normDate(r.expiry);
    if (b && (!a || b < a)) byName.set(r.name, r);
    else if (!prev.job && r.job) prev.job = r.job;
  }
  return { present: true, name: hit.name, rows, byName, missing };
}

function readLiftRecords(sections) {
  // 顶升加节与附着验收记录：设备编号 / 顶升次序 / 验收日期 / 验收结论
  const hit = pickSection(sections, /顶升|加节|附着|验收记录/);
  if (!hit) return { present: false, name: '', rows: [], byDevice: new Map(), missing: [] };
  const table = hit.table;
  const missing = [];
  if (!table.cols.some((c) => c.role === 'deviceNo')) missing.push('设备编号');
  if (!table.cols.some((c) => c.role === 'liftSeq')) missing.push('顶升次序');
  const rows = (table.items || []).map((it) => ({
    line: it.line,
    device_no: cell(it, 'deviceNo'),
    seq: normNumber(it.liftSeq),
    seq_raw: cell(it, 'liftSeq'),
    date: normDate(it.acceptDate),
    conclusion: cell(it, 'acceptConclusion'),
    raw: String(it.raw == null ? '' : it.raw).slice(0, 200),
  }));
  const byDevice = new Map();
  for (const r of rows) {
    if (!r.device_no) continue;
    if (!byDevice.has(r.device_no)) byDevice.set(r.device_no, []);
    byDevice.get(r.device_no).push(r);
  }
  return { present: true, name: hit.name, rows, byDevice, missing };
}

function buildRunIndex(runRecords) {
  const byDevice = new Map();
  for (const r of (runRecords && runRecords.rows) || []) {
    if (!r.device_no) continue;
    if (!byDevice.has(r.device_no)) byDevice.set(r.device_no, []);
    byDevice.get(r.device_no).push(r);
  }
  return byDevice;
}

/* ============================ 订阅版（买断）检查（五项） ============================ */

function checkOverdueInUse(it, ctx) {
  // 追加①：超期未检仍在用 —— 下次检测日期已过 且 运行状态=在用（P0，附超期天数）
  if (it.isTotal) return [];
  const status = cell(it, 'runStatus');
  if (status !== '在用') return [];
  const next = normDate(it.nextInspectDate);
  const b = baseOf(it, ctx.base);
  if (!next || !b) return [];
  const over = daysBetween(next, b);
  if (over <= 0) return [];
  return [finding('P0', '超期未检仍在用', it, over,
    `${who(it)}：下次检测日期 ${next} 已过 ${over} 天，运行状态却是「在用」—— `
    + `**超期未检仍在吊装**（产权单位 ${cell(it, 'ownerUnit') || '(未填)'}，`
    + `使用项目 ${cell(it, 'project') || '(未填)'}，司机 ${cell(it, 'driver') || '(未填)'}）。`,
    '这是安监直接下停工整改通知、出事故要追责的那一类：**当天停用**该塔机并挂停用牌、'
    + '书面报项目安全部与产权单位，联系检测机构安排定期检测；检测合格并更新下次检测日期后再恢复吊装。')];
}

function checkStaleInRecords(it, ctx) {
  // 追加②：停用 / 已拆除塔机仍出现在使用运行记录里（跨表交叉核对，点运行记录行号）
  if (it.isTotal) return [];
  const status = cell(it, 'runStatus');
  if (status !== '停用' && status !== '已拆除') return [];
  const no = cell(it, 'deviceNo');
  if (!no) return [];
  const rows = ctx.byDevice.get(no) || [];
  if (!rows.length) return [];
  const lines = rows.map((r) => r.line);
  const show = lines.slice(0, 8).join('、');
  const dates = rows.map((r) => r.date || r.date_raw).filter(Boolean).slice(0, 5).join('、');
  return [finding('P0', '停用拆除设备仍在使用记录', it, rows.length,
    `${who(it)}：台账运行状态是「${status}」，但「${ctx.runRecords.name || '塔机使用运行记录'}」段里还有 `
    + `${rows.length} 条该设备的使用记录（原文第 ${show} 行${lines.length > 8 ? ' 等' : ''}`
    + `${dates ? '，记录日期 ' + dates : ''}）。`,
    '停用 / 已拆除的塔机不得再投入使用：先核实是"记录没停"（人员照旧排班吊装）还是"手续没办"，'
    + '停用设备要断电、挂牌、上锁，已拆除的要办理注销并在台账与使用记录里同步停更。'
    + '两种都要留下书面核实记录。')];
}

function checkUncertifiedOperator(ctx) {
  // 追加③：无证上岗 —— 使用运行记录里的当班司机 / 当班信号工不在持证名单、工种不符、或证件已过期
  const out = [];
  const run = ctx.runRecords;
  const roster = ctx.roster;
  if (!run || !run.present || !roster || !roster.present) return out;
  for (const r of run.rows) {
    const posts = [
      { post: '当班司机', name: r.driver, want: '司机' },
      { post: '当班信号工', name: r.signaler, want: '信号' },
    ];
    for (const p of posts) {
      if (!p.name) continue;
      const rec = roster.byName.get(p.name);
      const refDate = r.date || ctx.base;
      const refRaw = r.date_raw || (ctx.base || '(未填)');
      const anchor = { line: r.line, raw: r.raw, deviceNo: r.device_no };
      if (!rec) {
        out.push(finding('P0', '无证上岗', anchor, undefined,
          `使用运行记录第 ${r.line} 行（塔机 ${r.device_no || '(未填)'}，记录日期 ${refRaw}）：`
          + `${p.post}「${p.name}」在「${roster.name || '特种作业人员持证名单'}」里找不到 —— `
          + '名单里没有这个人，就是无证上岗。',
          '先让这个人停止作业并核实现场到底谁在指挥 / 操作：'
          + '把持证人员姓名与操作证到期日补进名单，未取证的要先取证再排班，名单与排班要能一一对上。'));
        continue;
      }
      const job = String(rec.job || '');
      if (job && job.indexOf(p.want) < 0) {
        out.push(finding('P0', '无证上岗', anchor, undefined,
          `使用运行记录第 ${r.line} 行（塔机 ${r.device_no || '(未填)'}，记录日期 ${refRaw}）：`
          + `${p.post}「${p.name}」在持证名单里的工种是「${job}」，与当班岗位不符 —— `
          + '拿信号司索工证去开塔机（或反过来）都属于无证上岗。',
          '按人证岗一致原则重新排班：塔式起重机司机必须持司机操作证、信号工必须持信号司索工操作证，'
          + '同一人不得跨岗位代班；名单里的工种要按操作证原文填写。'));
      }
      const exp = normDate(rec.expiry);
      if (exp && refDate && daysBetween(exp, refDate) > 0) {
        const over = daysBetween(exp, refDate);
        out.push(finding('P0', '无证上岗', anchor, over,
          `使用运行记录第 ${r.line} 行（塔机 ${r.device_no || '(未填)'}，记录日期 ${refRaw}）：`
          + `${p.post}「${p.name}」的操作证有效期 ${exp}，早于当次作业日期 ${refDate}，**作业当天已过期 ${over} 天**。`,
          '证件过期当天起就不得独立操作：立刻停排该人员的班次、安排复审或换持证人员，'
          + '复审通过后的班次才有效；台账「证件有效期」与排班表要同步更新。'));
      }
    }
  }
  return out;
}

function checkLiftRecordGaps(it, ctx) {
  // 追加④：顶升加节 / 附着验收记录断档 —— 按设备把顶升次序逐次配对，缺哪一次点哪一次
  if (it.isTotal) return [];
  const lift = ctx.lift;
  if (!lift || !lift.present) return [];
  const no = cell(it, 'deviceNo');
  if (!no) return [];
  const rows = lift.byDevice.get(no) || [];
  if (!rows.length) return [];
  const out = [];
  const seen = new Map();
  for (const r of rows) {
    if (r.seq !== null && Number.isInteger(r.seq) && r.seq >= 1 && !seen.has(r.seq)) seen.set(r.seq, r);
  }
  const maxSeq = rows.reduce((m, r) => (r.seq !== null && r.seq >= 1 ? Math.max(m, r.seq) : m), 0);
  for (let k = 1; k <= maxSeq; k++) {
    if (seen.has(k)) continue;
    const prev = seen.get(k - 1) || rows[0];
    out.push(finding('P1', '顶升加节验收断档', { line: prev.line, raw: prev.raw, deviceNo: no }, undefined,
      `${who(it)}：第 ${k - 1} 次顶升加节 / 附着验收记录在第 ${prev.line} 行，`
      + `之后**缺了第 ${k} 次验收**（该设备验收记录共 ${rows.length} 条，最大次序 ${maxSeq}）—— `
      + `第 ${k} 次顶升加节没有验收就进到了下一次。`,
      '顶升加节与附着必须"每加一次、验一次"：把第 ' + k + ' 次的验收记录（验收单、检测机构复核意见、'
      + '监理签认页）找出来补进这份台账；找不到就先停住后续顶升作业，别用"补签"掩盖漏验收。'));
  }
  for (const r of rows) {
    const c = String(r.conclusion || '');
    if (c && !/^合格/.test(c)) {
      out.push(finding('P0', '顶升加节验收断档', { line: r.line, raw: r.raw, deviceNo: no }, undefined,
        `${who(it)}：第 ${r.seq === null ? '(次序未填)' : r.seq} 次顶升加节 / 附着验收记录（第 ${r.line} 行）的`
        + `验收结论是「${c}」，不是「合格」—— 验收没通过就不能继续顶升加节。`,
        '验收不合格的顶升加节必须整改后重新验收：先停住后续加节与吊装作业，'
        + '按验收意见整改（附着间距、连接件、垂直度）并重新组织验收，验收合格前不得继续顶升。'));
    }
  }
  return out;
}

function buildDeviceAggregates(items, ctx, paidFindings) {
  // 追加⑤ 的取数：逐台算超期天数、停用拆除却有记录、无证上岗次数、顶升验收断档次
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const no = cell(it, 'deviceNo');
    const status = cell(it, 'runStatus');
    const b = baseOf(it, ctx.base);
    const next = normDate(it.nextInspectDate);
    let overdue = 0;
    if (next && b) {
      const d = daysBetween(next, b);
      if (d > 0) overdue = d;
    }
    const rows = no ? (ctx.byDevice.get(no) || []) : [];
    const uncert = paidFindings.filter((f) => f.category === '无证上岗' && f.device_no === no).length;
    const liftMissing = paidFindings.filter((f) => f.category === '顶升加节验收断档' && f.device_no === no).length;
    const stale = (status === '停用' || status === '已拆除') && rows.length > 0;
    out.push({
      line: it.line,
      device_no: no,
      device_name: cell(it, 'deviceName'),
      owner_unit: cell(it, 'ownerUnit') || '(未填产权单位)',
      project: cell(it, 'project') || '(未填项目)',
      status,
      overdue_days: overdue,
      overdue_in_use: overdue > 0 && status === '在用',
      stale,
      stale_records: stale ? rows.length : 0,
      uncertified_count: uncert,
      lift_missing: liftMissing,
      records: rows.length,
    });
  }
  return out;
}

function groupActionFor(v) {
  // 追加⑤：每一组给一条可整改动作（先解决最要命的：超期未检仍在用）
  if (v.overdue_in_use_devices > 0) {
    return `立即停用本组 ${v.overdue_in_use_devices} 台超期未检仍在用的塔机（断电挂牌），`
      + '当天报项目安全部并联系检测机构定期检测';
  }
  if (v.stale_devices > 0) {
    return `核实本组 ${v.stale_devices} 台停用 / 已拆除塔机的使用记录并停更，补齐停用挂牌或拆除注销手续`;
  }
  if (v.uncertified_count > 0) {
    return `本组有 ${v.uncertified_count} 次无证上岗记录：停排相关人员班次，按人证岗一致重新排班并把操作证补进名单`;
  }
  if (v.lift_missing > 0) {
    return `补齐本组 ${v.lift_missing} 次顶升加节 / 附着验收记录，未验收不得继续顶升`;
  }
  if (v.overdue_devices > 0) {
    return `把本组 ${v.overdue_devices} 台检测超期塔机排进本月定期检测计划，检测合格后更新下次检测日期`;
  }
  return '本组未发现检测超期 / 停用拆除仍记录 / 无证上岗 / 顶升验收断档问题，保持现有台账与记录连续性即可';
}

function buildRollup(agg) {
  // 追加⑤：分产权单位 × 分使用项目的汇总清单（按超期天数降序）
  const blank = () => ({
    devices: 0, overdue_devices: 0, overdue_in_use_devices: 0,
    overdue_days_max: 0, overdue_days_total: 0,
    stale_devices: 0, stale_records: 0, uncertified_count: 0, lift_missing: 0, records: 0,
  });
  const add = (bk, a) => {
    bk.devices += 1;
    if (a.overdue_days > 0) {
      bk.overdue_devices += 1;
      bk.overdue_days_total = round2(bk.overdue_days_total + a.overdue_days);
      bk.overdue_days_max = Math.max(bk.overdue_days_max, a.overdue_days);
    }
    if (a.overdue_in_use) bk.overdue_in_use_devices += 1;
    if (a.stale) { bk.stale_devices += 1; bk.stale_records += a.stale_records; }
    bk.uncertified_count += a.uncertified_count;
    bk.lift_missing += a.lift_missing;
    bk.records += a.records;
    return bk;
  };
  const problemCount = (v) => v.overdue_devices + v.stale_devices + v.uncertified_count + v.lift_missing;
  const byOwner = new Map();
  const byProject = new Map();
  const byOwnerProject = new Map();
  for (const a of agg) {
    const ko = a.owner_unit;
    const kp = a.project;
    const kop = ko + ' × ' + kp;
    if (!byOwner.has(ko)) byOwner.set(ko, blank());
    if (!byProject.has(kp)) byProject.set(kp, blank());
    if (!byOwnerProject.has(kop)) byOwnerProject.set(kop, blank());
    add(byOwner.get(ko), a);
    add(byProject.get(kp), a);
    add(byOwnerProject.get(kop), a);
  }
  const toRows = (map, keyName) => [...map.entries()]
    .map(([k, v]) => Object.assign({ [keyName]: k, action: groupActionFor(v), problems: problemCount(v) }, v))
    .sort((x, y) => (y.overdue_days_max - x.overdue_days_max)
      || (y.problems - x.problems)
      || (y.overdue_days_total - x.overdue_days_total)
      || String(x[keyName]).localeCompare(String(y[keyName])));
  const total = agg.reduce((acc, a) => add(acc, a), blank());
  total.problems = problemCount(total);
  return {
    by_owner_unit: toRows(byOwner, 'owner_unit'),
    by_project: toRows(byProject, 'project'),
    by_owner_unit_project: toRows(byOwnerProject, 'owner_unit_project'),
    total,
    basis: '按「产权单位」「使用项目」「产权单位 × 使用项目」三档分组：每组给出设备台数、检测超期设备数、'
      + '超期未检仍在用设备数、超期天数（最大 / 合计）、停用或已拆除却有使用记录的设备数与记录条数、'
      + '无证上岗次数、顶升加节验收断档次；排序按「超期天数最大 → 问题条数 → 超期天数合计」降序，'
      + '每组附一条可整改动作。产权单位与项目没填的行归入「(未填产权单位)」「(未填项目)」。',
  };
}

function buildConsolidatedActions(agg) {
  // 追加⑤：把每台塔机的问题合并成一张整改清单（超期天数降序 → 行号）
  const rows = [];
  for (const a of agg) {
    const issues = [];
    if (a.overdue_in_use) issues.push(`超期未检仍在用 ${a.overdue_days} 天`);
    else if (a.overdue_days > 0) issues.push(`检测超期 ${a.overdue_days} 天`);
    if (a.stale) issues.push(`台账已${a.status}但使用记录仍有 ${a.stale_records} 条`);
    if (a.uncertified_count > 0) issues.push(`无证上岗 ${a.uncertified_count} 次`);
    if (a.lift_missing > 0) issues.push(`顶升加节验收断档 ${a.lift_missing} 次`);
    if (!issues.length) continue;
    let action;
    if (a.overdue_in_use) action = '当天停用挂牌 → 报项目安全部与产权单位 → 联系检测机构定期检测 → 合格并更新下次检测日期后恢复吊装';
    else if (a.stale) action = '现场核实是否真的停了 / 拆了 → 断电挂牌或办理注销 → 台账与使用记录同步停更';
    else if (a.uncertified_count > 0) action = '停排相关人员班次 → 按人证岗一致重新排班 → 操作证与持证名单同步补全';
    else if (a.lift_missing > 0) action = '停住后续顶升 → 找回缺失次数的验收记录 → 补齐后经监理签认再继续';
    else action = '排进本月定期检测计划 → 检测合格后更新检测日期与下次检测日期 → 归档检测报告';
    rows.push({
      device_no: a.device_no,
      device_name: a.device_name,
      owner_unit: a.owner_unit,
      project: a.project,
      line: a.line,
      status: a.status,
      level: (a.overdue_in_use || a.stale || a.uncertified_count > 0) ? 'P0' : 'P1',
      overdue_days: a.overdue_days,
      uncertified_count: a.uncertified_count,
      lift_missing: a.lift_missing,
      issue: issues.join('；'),
      action,
    });
  }
  rows.sort((x, y) => (y.overdue_days - x.overdue_days)
    || (x.line - y.line));
  return rows.map((r, i) => Object.assign({ seq: i + 1 }, r));
}

/* ============================ 入口 ============================ */

function sourceLabel() {
  return '一本含表头的塔机台账（设备编号 / 设备名称 / 产权单位 / 使用登记证号 / 检测日期 / 检测结论 / '
    + '下次检测日期 / 司机 / 信号工 / 证件有效期 / 运行状态 / 核对基准日）';
}

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：' + sourceLabel()]);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：' + sourceLabel()]);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的塔机台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.detail.length) {
    return insufficient(['至少一行塔机明细（现在只有表头或只有合计行，没有可核对的塔机）']);
  }

  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  const base = baseDateOf(t.items);
  const findings = [];
  const notRun = [];
  const dataNotes = [];
  let rollup = null;
  let consolidated = null;

  for (const f of checkInspectionValidity(t.items, base)) findings.push(f);
  for (const f of checkRegistrationAndCertificates(t.items, base)) findings.push(f);
  for (const f of checkConclusions(t.items)) findings.push(f);
  for (const f of checkDuplicateDevice(t.items)) findings.push(f);
  for (const f of checkTotals(t.items, t.cols)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  if (paid) {
    const sections = parseSections(text);
    const runRecords = readRunRecords(sections);
    const roster = readCertRoster(sections);
    const lift = readLiftRecords(sections);
    const ctx = { base, runRecords, roster, lift, byDevice: buildRunIndex(runRecords) };

    const paidFindings = [];
    for (const it of t.items) {
      for (const f of checkOverdueInUse(it, ctx)) paidFindings.push(f);
      for (const f of checkStaleInRecords(it, ctx)) paidFindings.push(f);
      for (const f of checkLiftRecordGaps(it, ctx)) paidFindings.push(f);
    }
    for (const f of checkUncertifiedOperator(ctx)) paidFindings.push(f);

    if (!runRecords.present) {
      dataNotes.push('材料里没有 `--- 塔机使用运行记录 ---` 段：停用 / 已拆除塔机仍出现在使用记录这一项'
        + '本次**没有执行** —— 这不等于没问题。');
    } else if (runRecords.missing.length) {
      dataNotes.push('「' + runRecords.name + '」段里认不出这些必需列：' + runRecords.missing.join('、')
        + '；停用 / 已拆除塔机仍出现在使用记录这一项本次**没有完整执行** —— 不等于没问题。');
    }
    if (!roster.present) {
      dataNotes.push('材料里没有 `--- 特种作业人员持证名单 ---` 段：无证上岗这一项本次**没有执行**'
        + '（它要「塔机使用运行记录」与「持证名单」两段同时提供）—— 不等于没问题。');
    } else if (roster.missing.length) {
      dataNotes.push('「' + roster.name + '」段里认不出这些必需列：' + roster.missing.join('、')
        + '；无证上岗本次**没有完整执行** —— 不等于没问题。');
    }
    if (!lift.present) {
      dataNotes.push('材料里没有 `--- 顶升加节与附着验收记录 ---` 段：顶升加节 / 附着验收断档这一项本次**没有执行**'
        + ' —— 不等于没问题。');
    } else if (lift.missing.length) {
      dataNotes.push('「' + lift.name + '」段里认不出这些必需列：' + lift.missing.join('、')
        + '；顶升加节验收断档本次**没有完整执行** —— 不等于没问题。');
    }

    const agg = buildDeviceAggregates(t.items, ctx, paidFindings);
    rollup = buildRollup(agg);
    consolidated = buildConsolidatedActions(agg);

    for (const f of paidFindings) findings.push(f);
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const deviceTotal = t.totals.deviceCount;
  const inspectTotal = t.totals.inspectCount;
  const overdueRows = findings.filter((f) => f.category === '检测超期');
  const overdueMax = overdueRows.reduce((m, f) => Math.max(m, f.diff || 0), 0);

  const result = {
    findings,
    summary: {
      rows: t.detail.length,
      total_rows: t.totalRows.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      device_count_total: deviceTotal,
      inspect_count_total: inspectTotal,
      overdue_devices: overdueRows.length,
      overdue_days_max: overdueMax,
      check_date: base,
      basis: '核对基准日（表内「核对基准日」，逐行为准、缺行用表内第一个能认出的）≤ 下次检测日期才算检测有效期被覆盖；'
        + '使用登记证号不得为空，司机 / 信号工都必须填，且「证件有效期」（本台塔机当班司机与信号工中较早到期的那一个）'
        + '要覆盖核对基准日；检测结论只认 合格 / 不合格 / 复检 / 复检合格（不合格按 P0，只写「复检」视为复检未闭环）；'
        + '同一设备编号在一本台账里唯一；合计行（设备台数、检测台数）必须等于明细行逐列加总；'
        + '运行状态只认 在用 / 停用 / 已拆除 / 检修 四个值。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这本塔机台账按上面写明的口径算得对、'
      + '备案与检测日期和检测结论字段都自洽**，不代表这台塔机的检测结论本身合规、'
      + '不代表现场隐患已经整改闭环、也不代表使用登记证与特种作业操作证的真伪已经核验 —— 那些不在本工具范围内。'
      + (dataNotes.length ? '（注意：' + dataNotes.join('；') + '）' : '');
  }

  const scope = {
    checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.detail.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    device_count_total: deviceTotal,
    inspect_count_total: inspectTotal,
    check_date: base,
  };
  result.scope = scope;
  if (dataNotes.length) result.data_notes = dataNotes;

  if (paid) {
    result.rollup = rollup;
    result.consolidated_actions = consolidated;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, normDate, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
