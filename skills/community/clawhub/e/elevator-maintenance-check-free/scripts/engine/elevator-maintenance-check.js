#!/usr/bin/env node
/**
 * elevator-maintenance-check.js —— 电梯维保与年检记录核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：电梯是**法定周期设备**。有资质的维保单位必须**每 15 天维保一次**、每年**定期检验一次**；
 * 物业要保存维保记录、故障与困人救援记录、检验报告。
 * 「维保记录缺失 / 间隔超 15 天」「年检过期仍在用」「困人救援超 30 分钟」都是监管**直接处罚项**，
 * 也是物业最容易被投诉与索赔的地方。电梯管理员/物业每月必须核：维保间隔、项目齐全性、年检有效期、
 * 故障与救援闭环、维保单位资质。
 *
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 * 免费档只做这张台账的逐行算术与勾稽（六项）：
 *   ① 维保间隔（同一电梯相邻两次维保日期间隔 ≤ 15 天）  ② 年检有效期（维保/检查日期 ≤ 定期检验有效期至）
 *   ③ 维保次数勾稽（按 15 天周期推算应有次数 vs 实际次数） ④ 同一电梯同一维保日期重复登记
 *   ⑤ 合计行逐列复核（数量类列）  ⑥ 空白/占位符/日期格式/状态值非法
 * 完整档另有五项（困人救援超时 / 维保项目不齐 / 故障闭环 / 维保单位资质有效期覆盖 / 分组汇总清单）。
 * 本版本**不做**"电梯是否真的按期维保过"的现场认定，**不做**检验合格与否的判定，**不做**行政处罚认定。
 *
 * 完整档的五项检查由一个**布尔开关**打开（共用源码里开关只在 `run` 里声明一次，五项检查都包在对应的付费分支里）。
 * 免费包里那一份由 tools/strip_free_engine.py 把开关与整段付费实现一并摘掉 —— 摘掉后仍是可运行的免费档引擎。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定电梯是否"真的做过"维保、不替代检验机构的定期检验结论、不判定困人救援过程是否合规处置、
 *          不读 .xlsx/.pdf 原件、不联网核验维保单位资质证书真伪；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CYCLE_DAYS = 15;                       // 法定维保周期：每 15 天一次（半月保）
const TOL = 0.01;
const ALLOWED_STATUS = ['正常', '故障', '停用', '检修'];

const CHECKS_GIVEN = [
  '维保间隔超期（同一电梯相邻两次维保日期间隔 ≤ 15 天，超期逐梯逐次给出超期天数）',
  '年检超期（维保/检查日期 ≤ 定期检验有效期至，超期给出超期天数）',
  '维保次数不足（按 15 天周期由首末维保日期推算应有次数，与实际维保次数逐梯勾稽，给缺次）',
  '维保记录重复登记（同一电梯同一维保日期出现两次及以上即点名）',
  '合计行不符（合计行数量类列 —— 维保项目数 / 应有项目数 / 救援到达时间 —— 必须等于明细行同列之和）',
  '关键字段缺失与非法值（空白/占位符、日期格式、状态值（正常/故障/停用/检修）、数量为负或看不懂）',
];

const CHECKS_WITHHELD = [
  '困人救援超时（救援到达时间 > 30 分钟，逐台点名电梯与超时分钟数，按超时降序）',
  '维保项目不齐（维保项目数 < 应有项目数，逐台点名并给出缺项数）',
  '故障闭环（故障日期 → 故障恢复日期是否在规定时限内；未闭环按已停机天数排序）',
  '维保单位资质有效期覆盖（维保日期 ≤ 资质到期日，超期点名到维保单位）',
  '分维保单位 × 分楼栋汇总清单（按超期与故障数排序，给出可整改动作与 consolidated_actions）',
];

const OUT_OF_SCOPE = [
  '判定电梯是否"真的做过"维保、维保作业质量是否合格（本工具只核台账字面记录；现场作业与实物由维保单位与检验机构负责）',
  '替代检验机构的定期检验结论（本工具只核「定期检验有效期至」与维保日期两列的先后关系，不判电梯是否合格）',
  '判定困人救援过程是否合规处置、是否造成人身伤害（本工具只核「救援到达时间(分钟)」这一列的分钟数）',
  '读取 .xlsx / .pdf 原件、联网核验维保单位资质证书真伪、替代特种设备监管部门的行政处罚认定',
];

// 样例：一张**干净**的电梯维保与年检记录台账 —— 三台梯、各两次半月保（间隔 14 天），
// 维保日期都在定期检验有效期内，维保项目数与应有项目数一致，无重复登记，合计行与明细行相符。
const SAMPLE_TEXT = [
  '电梯编号\t使用登记证号\t安装位置\t楼栋\t维保单位\t维保单位资质到期日\t维保日期\t维保项目数\t应有项目数\t定期检验有效期至\t状态\t故障日期\t救援到达时间(分钟)\t故障恢复日期\t备注',
  'DT-A-001\t梯1101050012\tA座1号客梯\tA座\t华信电梯工程技术有限公司\t2027-06-30\t2026-03-05\t26\t26\t2027-01-31\t正常\t\t\t\t半月保',
  'DT-A-001\t梯1101050012\tA座1号客梯\tA座\t华信电梯工程技术有限公司\t2027-06-30\t2026-03-19\t26\t26\t2027-01-31\t正常\t\t\t\t半月保',
  'DT-B-002\t梯1101050023\tB座2号货梯\tB座\t华信电梯工程技术有限公司\t2027-06-30\t2026-03-05\t24\t24\t2027-08-15\t正常\t\t\t\t半月保',
  'DT-B-002\t梯1101050023\tB座2号货梯\tB座\t华信电梯工程技术有限公司\t2027-06-30\t2026-03-19\t24\t24\t2027-08-15\t正常\t\t\t\t半月保',
  'DT-C-003\t梯1101050034\t门诊楼3号医用梯\t门诊楼\t恒安电梯维保有限公司\t2026-11-30\t2026-03-06\t30\t30\t2026-12-31\t正常\t\t\t\t半月保',
  'DT-C-003\t梯1101050034\t门诊楼3号医用梯\t门诊楼\t恒安电梯维保有限公司\t2026-11-30\t2026-03-20\t30\t30\t2026-12-31\t正常\t\t\t\t半月保',
  '合计\t\t\t\t\t\t\t160\t160\t\t\t\t0\t\t数量类列合计',
].join('\n');

// 表头级必需列（缺列 ⇒ 材料不足，只报缺哪一列，**绝不给结论**）
const REQUIRED_ROLES = [
  'elevatorNo', 'regNo', 'location', 'vendor', 'maintDate', 'maintItems',
  'requiredItems', 'inspectionDue', 'status', 'faultDate', 'rescueMinutes', 'recoveryDate',
];

// 单元格级必需字段（空白/占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['elevatorNo', '电梯编号'],
  ['regNo', '使用登记证号'],
  ['location', '安装位置'],
  ['vendor', '维保单位'],
  ['maintDate', '维保日期'],
  ['maintItems', '维保项目数'],
  ['requiredItems', '应有项目数'],
  ['inspectionDue', '定期检验有效期至'],
  ['status', '状态'],
];

// 日期列（用于「日期格式非法」判定）
const DATE_FIELDS = [
  ['maintDate', '维保日期'],
  ['inspectionDue', '定期检验有效期至'],
  ['faultDate', '故障日期'],
  ['recoveryDate', '故障恢复日期'],
  ['vendorQualDue', '维保单位资质到期日'],
];

// 数量列（用于「数量无法解析 / 数量为负」判定）
const COUNT_FIELDS = [
  ['maintItems', '维保项目数'],
  ['requiredItems', '应有项目数'],
  ['rescueMinutes', '救援到达时间(分钟)'],
];

// 数量类列：合计行必须等于明细行同列之和
const SUM_ROLES = ['maintItems', 'requiredItems', 'rescueMinutes'];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    踩过 6 次：顺序一错，宽泛词会抢走更具体的列（守卫见 tools/header_map_check.py）。
//    本表的雷区：「维保单位资质到期日」不能被「维保单位」抢走；
//    「定期检验有效期至」「维保日期」「故障日期」「故障恢复日期」「救援到达时间」这五个日期/时间列
//    必须按具体度排（先年检有效期、再维保日期、再资质到期日、再故障日期、再恢复日期、最后救援到达时间）；
//    「应有项目数」不能被「维保项目数」抢走。
const ROLES = {
  inspectionDue: ['定期检验有效期至', '定期检验有效期', '检验有效期至', '年检有效期至', '下次检验日期'],
  maintDate: ['维保日期', '保养日期', '维护保养日期', '维保时间'],
  vendorQualDue: ['维保单位资质到期日', '资质有效期至', '资质到期日', '许可证到期日', '资质有效期'],
  faultDate: ['故障日期', '故障发生日期', '报障日期', '困人日期'],
  recoveryDate: ['故障恢复日期', '恢复日期', '修复日期', '恢复时间'],
  rescueMinutes: ['救援到达时间', '到达时间', '救援时间', '救援用时'],
  elevatorNo: ['电梯编号', '设备编号', '电梯代码', '梯号'],
  regNo: ['使用登记证号', '使用登记证编号', '登记证号', '使用登记证', '注册代码'],
  location: ['安装位置', '使用地点', '安装地点', '设备位置', '位置'],
  building: ['楼栋', '楼号', '栋号', '建筑', '分区'],
  vendor: ['维保单位', '保养单位', '维保公司', '维保方'],
  maintItems: ['维保项目数', '保养项目数', '已检项目数', '实检项目数', '维保项目'],
  requiredItems: ['应有项目数', '应检项目数', '标准项目数', '规定项目数', '应有项目'],
  status: ['状态', '运行状态', '设备状态'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  elevatorNo: '电梯编号',
  regNo: '使用登记证号',
  location: '安装位置',
  building: '楼栋',
  vendor: '维保单位',
  vendorQualDue: '维保单位资质到期日',
  maintDate: '维保日期',
  maintItems: '维保项目数',
  requiredItems: '应有项目数',
  inspectionDue: '定期检验有效期至',
  status: '状态',
  faultDate: '故障日期',
  rescueMinutes: '救援到达时间(分钟)',
  recoveryDate: '故障恢复日期',
  note: '备注',
};

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张电梯维保与年检记录台账补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「维保合规」，也不说「维保不合规」。',
  };
}

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核)$/i.test(s);
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

/**
 * 日期 → UTC 毫秒（当日 00:00）。
 * 只认这几种写法：2026-03-05 / 2026/3/5 / 2026.3.5 / 2026年3月5日 / 20260305（可带 " 08:30" 时间尾巴）。
 * 看不懂就返回 null —— **绝不猜**（例如不把 "3月5日" 猜成某一年）。
 */
function normDate(raw) {
  const s0 = String(raw == null ? '' : raw).trim();
  if (!s0) return null;
  const m0 = /^([0-9]{4}[-/.][0-9]{1,2}[-/.][0-9]{1,2}|[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日?|[0-9]{8})\s+[0-9]{1,2}:[0-9]{2}/.exec(s0);
  const s = (m0 ? m0[1] : s0).replace(/年|月/g, '-').replace(/日/g, '').replace(/[./]/g, '-');
  let y = null;
  let mo = null;
  let d = null;
  const m1 = /^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})$/.exec(s);
  const m2 = /^([0-9]{4})([0-9]{2})([0-9]{2})$/.exec(s);
  if (m1) { y = Number(m1[1]); mo = Number(m1[2]); d = Number(m1[3]); }
  else if (m2) { y = Number(m2[1]); mo = Number(m2[2]); d = Number(m2[3]); }
  else return null;
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const ms = Date.UTC(y, mo - 1, d);
  const back = new Date(ms);
  if (back.getUTCFullYear() !== y || back.getUTCMonth() !== mo - 1 || back.getUTCDate() !== d) return null;
  return ms;
}

const pad2 = (n) => (n < 10 ? '0' + n : String(n));

function fmtDay(ms) {
  const d = new Date(ms);
  return `${d.getUTCFullYear()}-${pad2(d.getUTCMonth() + 1)}-${pad2(d.getUTCDate())}`;
}

function dayDiff(a, b) {
  return Math.round((b - a) / 86400000);
}

/** 合计行判定：只看定位列（电梯编号 / 使用登记证号 / 安装位置 / 维保单位），不看备注，免得“备注里写了合计”被误判 */
function looksLikeTotal(it) {
  const vals = [it.elevatorNo, it.regNo, it.location, it.vendor];
  return vals.some((v) => /^(合计|小计|总计|汇总)/.test(String(v == null ? '' : v).trim()));
}

/** 电梯标识：优先电梯编号，其次使用登记证号，都没有就按行号（这样“缺编号”不会被静默合并成同一台梯） */
function liftKey(it) {
  const a = String(it.elevatorNo == null ? '' : it.elevatorNo).trim();
  if (a) return a;
  const b = String(it.regNo == null ? '' : it.regNo).trim();
  return b || `(第${it.line}行)`;
}

function who(it) {
  return `第 ${it.line} 行「${liftKey(it)}」`;
}

function finding(level, category, it, diff, message, advice) {
  const f = { level, category, line: it.line, lift: liftKey(it), message };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  const raw = String(it.raw == null ? '' : it.raw).trim();
  f.evidence = raw.length > 240 ? raw.slice(0, 240) + '…' : raw;   // 原文依据：行号 + 原文行内容
  return f;
}

/** 解析成 {header, cols, items, dataItems, totalRows, totals, missingRoles, missingColumns, error}；行是**扁平**对象 */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], dataItems: [], totalRows: [], totals: {},
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
    it.isTotal = looksLikeTotal(it);
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const dataItems = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);

  // 合计**只算明细行**：合计行自己不能再被加一遍（否则每一张带合计行的表都会误报合计不符）
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(dataItems.reduce((acc, it) => {
      const n = normNumber(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header, cols, items, dataItems, totalRows, totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

/* ============================ 免费档检查（六项） ============================ */

/** ① 维保间隔：同一电梯相邻两次维保日期间隔 ≤ 15 天 */
function checkInterval(items) {
  const out = [];
  const byLift = new Map();
  for (const it of items) {
    const k = liftKey(it);
    if (!byLift.has(k)) byLift.set(k, []);
    byLift.get(k).push(it);
  }
  for (const rows of byLift.values()) {
    const dated = rows.filter((r) => normDate(r.maintDate) !== null)
      .sort((a, b) => (normDate(a.maintDate) - normDate(b.maintDate)) || (a.line - b.line));
    for (let i = 1; i < dated.length; i++) {
      const prev = dated[i - 1];
      const cur = dated[i];
      const gap = dayDiff(normDate(prev.maintDate), normDate(cur.maintDate));
      if (gap <= CYCLE_DAYS) continue;
      out.push(finding('P0', '维保间隔超期', cur, gap - CYCLE_DAYS,
        `${who(cur)}：维保日期 ${fmtDay(normDate(cur.maintDate))} 距上一次维保 ${fmtDay(normDate(prev.maintDate))}`
        + `（第 ${prev.line} 行）间隔 ${gap} 天，超过每 15 天一次的法定周期 ${gap - CYCLE_DAYS} 天。`,
        '电梯必须由有资质的维保单位每 15 天维保一次，间隔超期属监管直接处罚项。'
        + '先补齐漏做的维保并留档（补做日期要写实际到场日期），再查为什么漏做：排班漏项、维保单位未按期到场，还是记录根本没填。'));
    }
  }
  return out;
}

/** ② 年检有效期：本次维保/检查日期 ≤ 定期检验有效期至 */
function checkInspectionDue(items) {
  const out = [];
  for (const it of items) {
    const due = normDate(it.inspectionDue);
    const day = normDate(it.maintDate);
    if (due === null || day === null) continue;      // 缺失/格式错交给第 ⑥ 项
    if (day <= due) continue;
    const over = dayDiff(due, day);
    out.push(finding('P0', '年检超期', it, over,
      `${who(it)}：本次维保/检查日期 ${fmtDay(day)} 已晚于定期检验有效期至 ${fmtDay(due)}，超期 ${over} 天 —— `
      + '这段时间里这台梯属“年检过期仍在用”。',
      '定期检验过期期间不得继续载客：立即停梯并联系检验机构安排定期检验，检验合格前不得恢复使用；'
      + '同时核对该梯的使用登记证与上一份检验报告。'));
  }
  return out;
}

/** ③ 维保次数勾稽：按 15 天周期由首末维保日期推算应有次数，与实际维保次数逐梯对比 */
function checkMaintenanceCount(items) {
  const out = [];
  const byLift = new Map();
  for (const it of items) {
    const k = liftKey(it);
    if (!byLift.has(k)) byLift.set(k, []);
    byLift.get(k).push(it);
  }
  for (const [lift, rows] of byLift) {
    const parsed = rows.map((r) => ({ it: r, ms: normDate(r.maintDate) }))
      .filter((x) => x.ms !== null)
      .sort((a, b) => (a.ms - b.ms) || (a.it.line - b.it.line));
    if (!parsed.length) continue;
    const uniq = [];
    for (const x of parsed) {
      if (!uniq.length || uniq[uniq.length - 1].ms !== x.ms) uniq.push(x);
    }
    const first = uniq[0].ms;
    const last = uniq[uniq.length - 1].ms;
    const span = dayDiff(first, last);
    const expected = Math.floor(span / CYCLE_DAYS) + 1;
    const actual = uniq.length;
    if (actual >= expected) continue;
    const anchor = uniq[uniq.length - 1].it;
    out.push(finding('P0', '维保次数不足', anchor, expected - actual,
      `${who(anchor)}：${lift} 在本表内的维保日期从 ${fmtDay(first)} 到 ${fmtDay(last)} 共 ${span} 天，`
      + `按每 15 天一次推算应维保 ${expected} 次，实际只有 ${actual} 次（${uniq.map((u) => fmtDay(u.ms)).join('、')}），缺 ${expected - actual} 次。`,
      '这一段里漏做的维保要逐次补做并留档；如果维保其实做了、只是记录没进台账，把维保单位签字的原始记录补录进台账。'));
  }
  return out;
}

/** ④ 同一电梯同一维保日期重复登记 */
function checkDuplicateRegistration(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const ms = normDate(it.maintDate);
    if (ms === null) continue;                       // 日期缺失/格式错交给第 ⑥ 项
    const key = `${liftKey(it)}|${fmtDay(ms)}`;
    if (seen.has(key)) {
      const first = seen.get(key);
      out.push(finding('P0', '维保记录重复登记', it, undefined,
        `${who(it)}：${liftKey(it)} 在 ${fmtDay(ms)} 这一天已经出现过（第 ${first.line} 行）—— 同一电梯同一维保日期重复登记。`,
        '一次维保只应有一条记录：重复登记会让“实际维保次数”虚高、把真正的漏保盖住。'
        + '确认哪一条是原始记录后删掉重复行，不要用两行记同一次维保。'));
    } else {
      seen.set(key, it);
    }
  }
  return out;
}

/** ⑤ 合计行逐列复核（数量类列：维保项目数 / 应有项目数 / 救援到达时间） */
function checkTotalsRow(t) {
  const out = [];
  for (const tr of (t.totalRows || [])) {
    for (const role of SUM_ROLES) {
      const raw = tr[role];
      if (isBlank(raw)) continue;                    // 合计行没写的列不判，也不当 0
      const got = normNumber(raw);
      const want = t.totals[role];
      if (got === null) {
        out.push(finding('P1', '数量无法解析', tr, undefined,
          `${who(tr)}：合计行「${LABELS[role]}」的值「${String(raw).trim()}」不是可识别的数量。`,
          '合计行只填数字（可以为 0）；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      const diff = round2(got - want);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P0', '合计行不符', tr, diff,
        `${who(tr)}：合计行「${LABELS[role]}」写的是 ${got}，逐行复算的合计是 ${want}，`
        + `差 ${diff > 0 ? '多' : '少'} ${Math.abs(diff)}。`,
        '合计行必须等于明细行同列之和：偏多通常是把已删掉的行的数留在了合计里，偏少通常是漏了某一台梯或某一次维保。'
        + '建议合计一律用公式，不要手填。'));
    }
  }
  return out;
}

/** ⑥ 关键字段缺失 / 日期格式 / 状态值 / 数量非法 */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    const st = String(it.status == null ? '' : it.status).trim();

    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (st === '故障' && isBlank(it.faultDate)) miss.push('故障日期');   // 状态说故障，就必须有故障日期
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }

    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDate(raw) !== null) continue;
      out.push(finding('P1', '日期格式非法', it, undefined,
        `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
        + '（只认 2026-03-05 / 2026/3/5 / 2026.3.5 / 2026年3月5日 / 20260305 这几种写法）。',
        '把日期改成 2026-03-05 这种写法再跑；本工具不会替你猜一个日期，也不会按别的顺序解读'
        + '（“2026年3月”“3月5号”这类写法没法算维保间隔）。'));
    }

    if (st && !ALLOWED_STATUS.some((s) => s === st)) {
      out.push(finding('P1', '状态值非法', it, undefined,
        `${who(it)}：「状态」的值「${st}」不在允许的取值里（正常 / 故障 / 停用 / 检修）。`,
        '状态决定后面几项怎么算：写“已修复”“OK”“好了”这类自由文本，会让故障闭环与救援超时两项判不了。'));
    }

    for (const [role, label] of COUNT_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数量无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数量（只认数字）。`,
          '把数量改成纯数字形态再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P1', '数量无法解析', it, n,
          `${who(it)}：「${label}」是负数（${n}）—— 数量类字段不应为负。`,
          '确认是填错了还是把符号写反了；负数会让合计与勾稽全部失真。'));
      }
    }
  }
  return out;
}

/* ===== 完整档（付费）才执行的五项检查：都在付费分支里调用，免费包里整段会被摘掉 ===== */

/** 付费①：困人救援超时（救援到达时间 > 30 分钟） */
/** 付费②：维保项目不齐（维保项目数 < 应有项目数） */
/** 付费③：故障闭环（故障日期 → 故障恢复日期；未闭环给已停机天数） */
/** 付费④：维保单位资质有效期覆盖（维保日期 ≤ 资质到期日） */
/** 付费⑤：分维保单位 × 分楼栋汇总清单（按超期与故障数排序，给出可整改动作） */
/** 付费：困人救援超时排序（点名电梯 + 分钟数，按超时分钟数降序） */
/** 付费：未闭环故障按已停机天数降序 */
/** 付费：本表基准日 = 表内最晚的维保日期。停机天数按它算，结果不随“今天是几号”漂移 */
/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的电梯维保与年检记录台账']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的电梯维保与年检记录台账']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的电梯维保与年检记录台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }

  const dataItems = t.dataItems || [];
  if (!dataItems.length) {
    return insufficient(['至少一行电梯维保明细（现在只有表头或只有合计行，没有可核对的明细行）']);
  }

  const findings = [];
  const notRun = [];

  for (const f of checkInterval(dataItems)) findings.push(f);
  for (const f of checkInspectionDue(dataItems)) findings.push(f);
  for (const f of checkMaintenanceCount(dataItems)) findings.push(f);
  for (const f of checkDuplicateRegistration(dataItems)) findings.push(f);
  for (const f of checkTotalsRow(t)) findings.push(f);
  for (const f of checkFieldIntegrity(dataItems)) findings.push(f);

  let checksExecuted = CHECKS_GIVEN;

  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const elevatorCount = new Set(dataItems.map((it) => liftKey(it))).size;
  const result = {
    findings,
    summary: {
      rows: dataItems.length,
      elevators: elevatorCount,
      maintenance_records: dataItems.filter((it) => normDate(it.maintDate) !== null).length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      maint_items_total: t.totals.maintItems,
      required_items_total: t.totals.requiredItems,
      rescue_minutes_total: t.totals.rescueMinutes,
      basis: '电梯必须由有资质的维保单位**每 15 天维保一次**：同一电梯相邻两次维保日期间隔不得超过 15 天；'
        + '本次维保/检查日期（即维保日期）不得晚于该梯的定期检验有效期至；'
        + '按 15 天周期由首末维保日期推算的应有维保次数，不得多于实际维保次数；'
        + '同一电梯同一维保日期只能登记一次；'
        + '合计行（数量类列：维保项目数 / 应有项目数 / 救援到达时间）必须等于明细行同列之和；'
        + '状态只认 正常 / 故障 / 停用 / 检修，日期只认 2026-03-05 这类可解析的写法。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: checksExecuted,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对、该有的记录都在**，'
      + '不代表电梯真的按期做过维保、检验机构真的判过合格、维保作业本身合规，也不代表救援过程处置得当 —— '
      + '那些不在本工具范围内。';
  }

  result.scope = {
    checks: checksExecuted,
    checks_not_run: notRun,
    rows: dataItems.length,
    total_rows: (t.totalRows || []).length,
    elevators: elevatorCount,
    columns_recognized: t.cols.filter((c) => c.role).length,
    maint_items_total: t.totals.maintItems,
    required_items_total: t.totals.requiredItems,
    rescue_minutes_total: t.totals.rescueMinutes,
  };



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
