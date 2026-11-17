#!/usr/bin/env node
/**
 * ip-annuity-check-full.js —— 知识产权年费与续展台账核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**有商标/专利的企业每年（年费按年/按月分批）都必须把这张台账核一遍**。
 * 台账口径是三条能互相验证的算式 + 一串日期：
 *   ① 下次缴费日 = 上次缴费日 + 缴费周期（年 / 月）
 *   ② 已缴合计   = 官费 + 代理费
 *   ③ 到期天数   = 下次缴费日 − 基准日（**基准日 = 台账内最新日期**）
 * 漏缴年费的代价不是那笔年费：**专利权会终止、商标会被撤销**，恢复要交滞纳金，
 * 有的情形**根本恢复不了** —— 损失远超年费本身。所以这份台账必须逐行核、核到行。
 *
 * 与已有能力的区别：`compliance-expiry-check` 核的是**证照与特种设备的年检到期台账**（谁什么时候该年检）；
 * 本能力核的是**知识产权权利维持台账**（申请号/权利人/缴费周期/官费/代理费/续展与转让），
 * 材料形态与算式都不同。
 *
 * 边界（硬要求）：**不判断任何国家/地区的官费标准与滞纳金费率**（那要查官方费率表）。
 * 官费、代理费、滞纳金档位**全部由输入提供**；本引擎只核表内可算的关系与日期一致性。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查官费文库、不调用大模型；材料不足不给结论；不给法律意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '下次缴费日复算（上次缴费日 + 缴费周期，年/月）',
  '已缴合计复算（官费 + 代理费）',
  '到期天数额（下次缴费日 − 基准日；基准日取台账内最新日期）',
  '申请号重复检测（同一申请号出现多行）',
  '关键字段空缺与占位符检测',
  '缴费周期非正 / 认不出单位检测',
  '日期倒挂检测（下次缴费日不晚于上次缴费日、转让日早于上次缴费日）',
  '缴费金额缺失检测（官费/代理费/已缴合计三者不齐）',
];

const CHECKS_WITHHELD = [
  '逾期待缴清单（含逾期月数与滞纳金档位提示，档位由输入给出）',
  '90 天与 180 天内到期排期表',
  '台账状态与缴费记录一致性（已放弃/已转让却仍挂着待缴）',
  '同一申请号重复计费（一行以上有实缴金额即计入重复收费）',
  '代理费异常（显著高于同表多数口径，超中位数倍数由输入给出）',
];

const OUT_OF_SCOPE = [
  '判断任何国家/地区的官费标准、年费减缴比例与滞纳金费率（那要查官方费率表；官费/代理费/滞纳金档位请由输入提供）',
  '代替官方期限监控与缴费：本工具只核台账，不代缴、不代报，也不承担期限责任',
  '判断权利是否真的有效/可恢复（放弃、撤销、转让的效力属于法律判断）',
  '给出法律意见或代理策略；读取 .xlsx（需要你先导出成文本或 JSON 贴进来）',
];

const SAMPLE_TEXT = [
  '申请号\t权利人\t类型\t名称\t上次缴费日\t缴费周期(月)\t下次缴费日\t官费\t代理费\t已缴合计\t状态\t转让状态\t转让日\t核对日\t滞纳金档位',
  // 基准日 = 台账内最新日期 = 核对日 2026-09-15
  'ZL201810123456.7\t某某科技有限公司\t发明专利\t一种数据处理方法\t2025-09-15\t36\t2028-09-15\t900.00\t1200.00\t2100.00\t已缴\t未转让\t\t2026-09-15\t',
  'ZL202020987654.3\t某某科技有限公司\t实用新型\t一种检测装置\t2024-10-10\t12\t2025-10-10\t1500.00\t600.00\t2100.00\t未缴\t未转让\t\t2026-09-15\tT4',
  '国作登字-2020-F-00012345\t某某科技有限公司\t著作权\t某软件V1.0\t2025-06-15\t12\t2026-06-15\t600.00\t900.00\t1500.00\t待缴\t未转让\t\t2026-09-15\tT1',
  'ZL202030005555.4\t某某科技有限公司\t外观设计\t标贴（二）\t2024-11-30\t24\t2026-11-30\t800.00\t1200.00\t2000.00\t已缴\t未转让\t\t2026-09-15\t',
  'ZL202130001111.2\t某某科技有限公司\t外观设计\t包装盒（一）\t2024-10-01\t24\t2026-10-01\t800.00\t1200.00\t2000.00\t待缴\t未转让\t\t2026-09-15\t',
  'ZL202010555555.1\t某某科技有限公司\t发明专利\t一种控制电路\t2025-08-20\t12\t2026-08-20\t900.00\t6000.00\t6900.00\t已放弃\t未转让\t\t2026-09-15\tT2',
  'ZL202010555555.1\t某某科技有限公司\t发明专利\t一种控制电路\t2026-08-20\t12\t2027-08-20\t900.00\t1000.00\t1900.00\t已放弃\t未转让\t\t2026-09-15\tT2',
  '第87654321号\t某某科技有限公司\t商标\t某某标\t2024-08-20\t12\t2025-08-20\t1000.00\t0.00\t1000.00\t已缴\t未转让\t\t2026-09-15\t',
  '第87654321号\t某某科技有限公司\t商标\t某某标\t2025-08-20\t12\t2027-02-12\t1000.00\t1300.00\t2300.00\t已转让\t已转让\t2026-08-15\t2026-09-15\tT1',
  'ZL201910777777.9\t某某科技有限公司\t发明专利\t一种封装结构\t2024-09-01\t待定\t2025-09-01\t900.00\t1000.00\t1900.00\t已缴\t未转让\t\t2026-09-15\tT2',
  'ZL202130001111.2\t某某科技有限公司\t外观设计\t包装盒（一）\t2025-09-20\t12\t2025-09-20\t800.00\t1200.00\t2000.00\t已缴\t未转让\t\t2026-09-15\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库踩过两次的坑，见 tools/header_map_check.py）：
  //    「转让日」不能被「转让状态」抢走；「已缴合计」不能被「缴」类宽泛词抢走；
  //    「滞纳金档位」不能被「金」类宽泛词抢走。
  transferDate: ['转让日', '转让日期'],
  transferState: ['转让状态', '转让情况', '是否转让'],
  nextPaid: ['下次缴费日', '下次缴款日', '下次年费日', '下次缴费日期'],
  lastPaid: ['上次缴费日', '上次缴款日', '上次年费日', '上次缴费日期'],
  cycle: ['缴费周期', '年费周期', '缴费间隔', '续展周期'],
  officialFee: ['官费', '官方费用', '规费'],
  agentFee: ['代理费', '代理服务费', '代理机构费'],
  paidTotal: ['已缴合计', '已缴金额', '实缴合计', '实缴金额', '已缴总额'],
  lateTier: ['滞纳金档位', '滞纳金档', '滞纳档次', '滞纳金等级'],
  baseDate: ['核对基准日', '数据基准日', '基准日', '核对日', '数据截止日'],
  appNo: ['申请号', '申请号码', '注册号', '专利号', '登记号'],
  holder: ['权利人', '专利权人', '商标权人', '著作权人', '申请人'],
  ipType: ['类型', '知识产权类型', '权利类型', '种类'],
  state: ['当前状态', '台账状态', '法律状态', '权利状态', '状态'],
  name: ['名称', '商标名称', '专利名称', '作品名称', '标的名'],
};

const LABELS = {
  appNo: '申请号', holder: '权利人', ipType: '类型', name: '名称',
  lastPaid: '上次缴费日', cycle: '缴费周期(月)', nextPaid: '下次缴费日',
  officialFee: '官费', agentFee: '代理费', paidTotal: '已缴合计',
  state: '状态', transferState: '转让状态', transferDate: '转让日', lateTier: '滞纳金档位',
};

const REQUIRED = ['appNo', 'holder', 'lastPaid', 'cycle', 'nextPaid', 'officialFee',
  'agentFee', 'paidTotal', 'state'];
const FEE_ROLES = ['officialFee', 'agentFee', 'paidTotal'];

/** 行内字段出现顺序 = 明细列（给 header_map_check 的"列数别丢"判据用） */
const ROW_ROLES = ['appNo', 'holder', 'ipType', 'name', 'lastPaid', 'cycle', 'nextPaid',
  'officialFee', 'agentFee', 'paidTotal', 'state', 'transferState', 'transferDate', 'lateTier'];

/** 默认的代理费异常判据：高于同表中位数的这个倍数才算异常（口径因所而异，可由输入覆盖） */
const DEFAULT_AGENT_FEE_MAX_RATIO = 1.5;

/** 订阅版动作清单的排序（P0 最急） */
const PAID_RANK = { P0: 0, P1: 1, P2: 2 };

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

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()【】\[\]:：]/g, '');
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

const round2 = (n) => Math.round(n * 100) / 100;

/** YYYY-MM-DD / YYYY/MM/DD / YYYY年M月D日 / YYYYMMDD -> YYYY-MM-DD；认不出返回 null */
function parseDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  let m = s.match(/^(\d{4})\s*[-/.年]\s*(\d{1,2})\s*[-/.月]\s*(\d{1,2})\s*日?$/);
  if (!m) m = s.match(/^(\d{4})(\d{2})(\d{2})$/);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const probe = new Date(Date.UTC(y, mo - 1, d));
  if (probe.getUTCFullYear() !== y || probe.getUTCMonth() !== mo - 1 || probe.getUTCDate() !== d) return null;
  return `${String(y).padStart(4, '0')}-${String(mo).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
}

/** YYYY-MM-DD 加 n 个月（月末自动收敛：01-31 加 1 个月 = 02-28） */
function addMonths(iso, n) {
  const [y, m, d] = String(iso).split('-').map(Number);
  const first = new Date(Date.UTC(y, m - 1 + n, 1));
  const lastDay = new Date(Date.UTC(first.getUTCFullYear(), first.getUTCMonth() + 1, 0)).getUTCDate();
  const day = Math.min(d, lastDay);
  return `${String(first.getUTCFullYear()).padStart(4, '0')}-`
    + `${String(first.getUTCMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
}

function addDays(iso, n) {
  const [y, m, d] = String(iso).split('-').map(Number);
  const t = new Date(Date.UTC(y, m - 1, d));
  t.setUTCDate(t.getUTCDate() + n);
  return `${String(t.getUTCFullYear()).padStart(4, '0')}-`
    + `${String(t.getUTCMonth() + 1).padStart(2, '0')}-${String(t.getUTCDate()).padStart(2, '0')}`;
}

const dayDiff = (fromIso, toIso) => Math.round(
  (Date.parse(`${toIso}T00:00:00Z`) - Date.parse(`${fromIso}T00:00:00Z`)) / 86400000);

/** 整月数：base 比 due 晚多少个月（向下取整；已逾期但不满整月的按 1 个月，避免出现"已过去 0 个月"） */
function monthsBetween(dueIso, baseIso) {
  if (dayDiff(dueIso, baseIso) <= 0) return 0;
  const [dy, dm, dd] = String(dueIso).split('-').map(Number);
  const [by, bm, bd] = String(baseIso).split('-').map(Number);
  let months = (by - dy) * 12 + (bm - dm);
  if (bd < dd) months -= 1;
  return Math.max(1, months);
}

/** 缴费周期：值里的单位优先；值里没写单位就按表头里的单位；再没有按"年"。单位必须认得出来。 */
function parseCycle(rawValue, header) {
  if (isBlank(rawValue)) return { ok: false, reason: '空缺' };
  const s = String(rawValue).trim();
  const n = normNumber(s);
  if (n === null) return { ok: false, reason: `认不出数字（"${s}"）` };
  if (n <= 0) return { ok: false, reason: `周期必须为正数（"${s}"）` };
  const head = String(header || '');
  let unit;
  if (/月/.test(s)) unit = 'month';
  else if (/年/.test(s)) unit = 'year';
  else if (/月/.test(head)) unit = 'month';
  else if (/年/.test(head)) unit = 'year';
  else if (n >= 12 && Number.isInteger(n)) unit = 'month';   // 惯例：≥12 的整数周期按"月"理解
  else unit = 'year';
  const months = unit === 'year' ? n * 12 : n;
  if (!Number.isFinite(months) || months <= 0) return { ok: false, reason: `周期换算不出来（"${s}"）` };
  return { ok: true, months, label: unit === 'month' ? `${n} 个月` : `${n} 年` };
}

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { error: 'empty' };
  const cols = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
  }
  const items = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i] };
    let seen = 0;
    cols.forEach((c, idx) => {
      if (c.role && row[c.role] === undefined) {
        row[c.role] = cells[idx] === undefined ? '' : cells[idx];
        seen += 1;
      }
    });
    if (!seen) continue;
    items.push(row);
  }
  return { cols, items };
}

const num = (it, role) => normNumber(it[role]);
const day = (it, role) => parseDate(it[role]);

/**
 * 基准日 = **台账内最新日期**。
 * 「台账内日期」= 上次缴费日 / 转让日 / 显式基准日；**下次缴费日属于未来的排期日，天然晚于今天**，
 * 拿它当基准会把整表都判成逾期（实测过的坑），所以只有在台账里**没有**显式基准日（核对日）列时，
 * 才退而把下次缴费日也算进来 —— 并且如实写进 basis_source。
 */
function basisDateOf(items) {
  const hasBaseCol = items.some((it) => it.baseDate !== undefined);
  const roles = hasBaseCol ? ['baseDate', 'lastPaid', 'transferDate']
    : ['baseDate', 'lastPaid', 'transferDate', 'nextPaid'];
  let best = null;
  for (const it of items) {
    for (const role of roles) {
      const d = day(it, role);
      if (d && (best === null || d > best)) best = d;
    }
  }
  return { date: best, source: hasBaseCol ? '台账内最新日期（含核对日列）' : '台账内最新日期（含下次缴费日）' };
}

const who = (it) => {
  const no = String(it.appNo === undefined ? '' : it.appNo).trim() || '(申请号空缺)';
  const nm = String(it.name === undefined ? '' : it.name).trim();
  const tp = String(it.ipType === undefined ? '' : it.ipType).trim();
  return `${tp ? `${tp} ` : ''}${nm ? `「${nm}」` : ''}（申请号 ${no}）`;
};

/* ================= 所有档位都执行的检查（免费层） ================= */

/** 下次缴费日 = 上次缴费日 + 缴费周期（年/月） */
function checkNextDate(it) {
  const last = day(it, 'lastPaid');
  const stated = day(it, 'nextPaid');
  if (!last || !stated) return null;
  const cyc = parseCycle(it.cycle, it.__cycleHeader || '缴费周期(月)');
  if (!cyc.ok) return null;                       // 周期本身由"周期非正"那条负责报
  const expect = addMonths(last, cyc.months);
  if (expect === stated) return null;
  return {
    level: 'P0', category: '下次缴费日与复算不符', line: it.line,
    message: `${who(it)}的下次缴费日是 ${stated}，`
      + `按 上次缴费日 ${last} + ${cyc.label} 应为 ${expect}。`,
    advice: '下次缴费日是排期与失权判定的基准，错一天就可能错过缴费窗口；请按缴费通知单核回原值。',
  };
}

/** 已缴合计 = 官费 + 代理费 */
function checkPaidTotal(it) {
  const off = num(it, 'officialFee');
  const ag = num(it, 'agentFee');
  const stated = num(it, 'paidTotal');
  if (off === null || ag === null || stated === null) return null;
  const expect = round2(off + ag);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '已缴合计与复算不符', line: it.line,
    message: `${who(it)}的已缴合计是 ${stated.toFixed(2)}，`
      + `按 官费 ${off.toFixed(2)} + 代理费 ${ag.toFixed(2)} 应为 ${expect.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '已缴合计与官费+代理费对不上，通常是有笔款没入账或被重复计入；金额口径要与缴费凭证一致。',
  };
}

/** 到期天数 = 下次缴费日 − 基准日（基准日 = 台账内最新日期）—— 逐行数值，进 days_left，不单独出结论 */
function daysLeftOf(it, basis) {
  const stated = day(it, 'nextPaid');
  if (!stated || !basis) return null;
  return dayDiff(basis, stated);
}

/** 同一申请号出现多行 */
function checkDuplicateAppNo(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.appNo === undefined ? '' : it.appNo).trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一申请号出现多行', line: it.line,
        message: `申请号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一权利多行会让年费与代理费一起被重复统计；确认哪一行才是本年度该核的那条。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

/** 关键字段空缺或占位符 */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = String(it[role] === undefined ? '' : it[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔年费就排不出期；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

/** 缴费周期非正 / 认不出单位 */
function checkCycleInvalid(items) {
  const out = [];
  for (const it of items) {
    const cyc = parseCycle(it.cycle, it.__cycleHeader || '缴费周期(月)');
    if (cyc.ok) continue;
    out.push({
      level: 'P0', category: '缴费周期非正或认不出单位', line: it.line,
      message: `${who(it)}的缴费周期是「${String(it.cycle === undefined ? '' : it.cycle).trim() || '空'}」：${cyc.reason}。`,
      advice: '周期必须是正数并写清单位（12 / 12个月 / 1年）；周期为 0 或负数会让下次缴费日永远算不出来。',
    });
  }
  return out;
}

/** 日期倒挂：下次缴费日不晚于上次缴费日；转让日早于上次缴费日 */
function checkDateOrder(items) {
  const out = [];
  for (const it of items) {
    const last = day(it, 'lastPaid');
    const next = day(it, 'nextPaid');
    if (last && next && next <= last) {
      out.push({
        level: 'P0', category: '日期倒挂', line: it.line,
        message: `${who(it)}的下次缴费日 ${next} 不晚于上次缴费日 ${last}。`,
        advice: '两个日期贴反了或有一处打错；先按缴费凭证改回，再重跑核对。',
      });
    }
    const tr = day(it, 'transferDate');
    if (tr && last && tr < last) {
      out.push({
        level: 'P1', category: '日期倒挂', line: it.line,
        message: `${who(it)}的转让日 ${tr} 早于上次缴费日 ${last}。`,
        advice: '转让后通常由受让人承担后续年费；两个日期矛盾时以转让登记文件为准。',
      });
    }
  }
  return out;
}

/** 缴费金额缺失：官费/代理费/已缴合计三者不齐 */
function checkFeeMissing(items) {
  const out = [];
  for (const it of items) {
    for (const role of FEE_ROLES) {
      const s = String(it[role] === undefined ? '' : it[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '缴费金额缺失', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」没有金额（${s || '空'}），缺了这一项就算不出「官费 + 代理费」。`,
          advice: '金额要么填数、要么明确写 0；留空会让这一行的费用口径不可复算。',
        });
      }
    }
  }
  return out;
}

/* ===== 以下为订阅版才执行的检查 ===== */

/** 滞纳金档位：**档位表由输入给出**，本引擎只负责按逾期月数落档 */
function tierForMonths(months, tiers) {
  if (!Array.isArray(tiers)) return null;
  for (const t of tiers) {
    const max = normNumber(t && t.maxMonths);
    if (max === null) continue;
    if (months <= max) {
      const min = normNumber(t && t.minMonths);
      return {
        tier: String((t && t.tier) || '').trim() || '(未命名档位)',
        range: `${min === null ? 0 : min}~${max} 个月`,
      };
    }
  }
  return null;
}

/** 逾期待缴清单：下次缴费日已过基准日、且状态不是「已缴」的行 */
function checkOverdueList(items, basis, tiers) {
  const out = [];
  for (const it of items) {
    const due = day(it, 'nextPaid');
    if (!due || !basis) continue;
    const left = dayDiff(basis, due);
    if (left >= 0) continue;                                      // 还没到期
    const st = String(it.state === undefined ? '' : it.state).trim();
    if (/已缴|已缴费|已缴纳|已续展|已付/.test(st)) continue;        // 本期已缴，不算逾期
    const months = monthsBetween(due, basis);
    const tier = tierForMonths(months, tiers);
    const owed = num(it, 'officialFee');
    out.push({
      level: 'P0', category: '已逾期待缴（失权风险）', line: it.line,
      urgency: -months,                                          // 逾期越久排越前
      amount: owed === null ? 0 : owed,
      message: `${who(it)}的下次缴费日 ${due} 已过去 ${months} 个月（逾期 ${Math.abs(left)} 天，基准日 ${basis}），`
        + `状态是「${st || '空'}」；`
        + (tier
          ? `按输入给出的档位表落在「${tier.tier}」（${tier.range}），请按官方缴费通知单的滞纳金金额缴纳。`
          : '输入里没有这份档位表，所以本次不出滞纳金档位结论。')
        + '官费口径以输入为准，本工具不判断任何国家/地区的费率标准。',
      advice: '逾期未缴会导致专利权终止或商标被撤销，恢复要交滞纳金、有的情形无法恢复：'
        + '今天就按缴费通知单确认应缴金额与官方截止日，能缴先缴。',
    });
  }
  return out;
}

/** 90 天 / 180 天内到期排期表（不含已逾期的，逾期在上一条报） */
function checkDueSchedule(items, basis) {
  const out = [];
  if (!basis) return out;
  for (const it of items) {
    const due = day(it, 'nextPaid');
    if (!due) continue;
    const left = dayDiff(basis, due);
    if (left < 0) continue;
    const st = String(it.state === undefined ? '' : it.state).trim();
    if (/已缴|已缴费|已缴纳|已续展|已付/.test(st) && left > 180) continue;
    const off = num(it, 'officialFee');
    const amount = off === null ? 0 : off;
    if (left <= 90) {
      out.push({
        level: 'P0', category: '90 天内到期排期', line: it.line, amount,
        message: `${who(it)}距下次缴费日（${due}）只剩 ${left} 天，本行官费 ${off === null ? '(未填)' : off.toFixed(2)}。`,
        advice: '90 天内到期的最急：先确认缴费金额与官方窗口，安排付款与凭证归档，别等到最后一周。',
      });
    } else if (left <= 180) {
      out.push({
        level: 'P1', category: '180 天内到期排期', line: it.line, amount,
        message: `${who(it)}距下次缴费日（${due}）还有 ${left} 天，本行官费 ${off === null ? '(未填)' : off.toFixed(2)}。`,
        advice: '180 天内到期的先纳入本季度排期：确认预算、核对权利人是否发生变更。',
      });
    }
  }
  return out;
}

/** 台账状态与缴费记录一致性：已放弃/已转让却仍挂着待缴与费用 */
function checkStateConsistency(items) {
  const out = [];
  const abandoned = /放弃|撤回|失效|终止|注销/;
  const transferred = /已转让|转让完成|已过户/;
  for (const it of items) {
    const st = String(it.state === undefined ? '' : it.state).trim();
    const ts = String(it.transferState === undefined ? '' : it.transferState).trim();
    const owed = num(it, 'officialFee');
    const hasFee = owed !== null && owed > 0;
    const pending = /未缴|待缴|待付|欠费/.test(st);
    if (abandoned.test(st) && (pending || hasFee)) {
      out.push({
        level: 'P1', category: '已放弃但台账仍挂着待缴', line: it.line,
        amount: hasFee ? owed : 0,
        message: `${who(it)}的状态是「${st}」，但此行仍挂着官费 ${owed === null ? '(未填)' : owed.toFixed(2)}`
          + `${pending ? '与「待缴/未缴」标记' : ''}。`,
        advice: '已放弃的权利不该再出现在待缴清单里：确认放弃文件后把该行状态与应付金额一起更新，'
          + '否则会在排期里被当成还要缴的年费，白占预算。',
      });
    }
    if (transferred.test(st) || transferred.test(ts)) {
      if (hasFee || pending) {
        out.push({
          level: 'P1', category: '已转让但台账未更新', line: it.line,
          amount: hasFee ? owed : 0,
          message: `${who(it)}已转让（状态「${st || '空'}」/ 转让状态「${ts || '空'}」，`
            + `转让日 ${String(it.transferDate === undefined ? '' : it.transferDate).trim() || '(未填)'}），`
            + `但此行仍挂着官费 ${owed === null ? '(未填)' : owed.toFixed(2)}${pending ? '与「待缴」标记' : ''}。`,
          advice: '转让登记后后续年费通常由受让人承担：把权利人、缴费义务人与付款人一起改掉，'
            + '并按转让文件确认交接日之前的年费由谁缴。',
        });
      }
    }
  }
  return out;
}

/** 同一申请号重复计费：同一申请号多行、且至少一行有实缴金额 */
function checkDoubleCharge(items) {
  const byKey = new Map();
  for (const it of items) {
    const key = String(it.appNo === undefined ? '' : it.appNo).trim();
    if (!key) continue;
    if (!byKey.has(key)) byKey.set(key, []);
    byKey.get(key).push(it);
  }
  const out = [];
  for (const [key, group] of byKey) {
    if (group.length < 2) continue;
    const paidRows = group.filter((it) => {
      const v = num(it, 'paidTotal');
      return v !== null && v > 0;
    });
    if (!paidRows.length) continue;
    const sum = round2(paidRows.reduce((s, it) => s + (num(it, 'paidTotal') || 0), 0));
    out.push({
      level: 'P0', category: '同一申请号重复计费', line: paidRows[paidRows.length - 1].line,
      amount: sum,
      message: `申请号「${key}」在 ${group.map((it) => '第 ' + it.line + ' 行').join('、')} 共出现 ${group.length} 次，`
        + `其中 ${paidRows.length} 行有实缴金额，合计 ${sum.toFixed(2)}。`,
      advice: '同一申请号的费用只能入账一次：确认哪一行是本年度实际缴费，另一行改状态或标注作废，别重复付款。',
    });
  }
  return out;
}

/** 代理费异常：显著高于同表多数口径（超过中位数的倍数由输入给出） */
function checkAgentFeeOutlier(items, ratio) {
  const fees = [];
  for (const it of items) {
    const v = num(it, 'agentFee');
    if (v !== null && v > 0) fees.push(v);
  }
  if (fees.length < 3) return [];                 // 少于 3 行没有"多数口径"可比
  const sorted = fees.slice().sort((a, b) => a - b);
  const mid = sorted.length % 2
    ? sorted[(sorted.length - 1) / 2]
    : round2((sorted[sorted.length / 2 - 1] + sorted[sorted.length / 2]) / 2);
  if (!(mid > 0)) return [];
  const limit = round2(mid * ratio);
  const out = [];
  for (const it of items) {
    const v = num(it, 'agentFee');
    if (v === null || v <= 0) continue;
    if (v <= limit) continue;
    out.push({
      level: 'P1', category: '代理费异常', line: it.line, amount: v,
      message: `${who(it)}的代理费是 ${v.toFixed(2)}，本表中位数是 ${mid.toFixed(2)}，`
        + `超过中位数的 ${ratio} 倍（阈值 ${limit.toFixed(2)}）。`,
      advice: '同一批业务里代理费口径应当接近：确认这笔是不是含了官费、加急费或其他权利的费用，'
        + '或是代理机构报错了价；分不清就先要报价单。',
    });
  }
  return out;
}

/** 订阅版的处理清单：按紧迫度（P0→P2）与金额排序，每条给出建议动作 */
function buildActions(result, items) {
  const byLine = new Map();
  for (const it of items) byLine.set(it.line, it);
  return result.findings.map((f) => {
    const it = byLine.get(f.line) || {};
    return {
      level: f.level, category: f.category, line: f.line,
      app_no: String(it.appNo === undefined ? '' : it.appNo).trim(),
      amount: f.amount === undefined ? 0 : f.amount,
      urgency: f.urgency === undefined ? 0 : f.urgency,
      message: f.message,
      action: f.advice,
    };
  }).sort((a, b) => (PAID_RANK[a.level] - PAID_RANK[b.level])
    || (a.urgency - b.urgency) || (b.amount - a.amount) || (a.line - b.line));
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的知识产权台账（要能认出「申请号」「权利人」「上次缴费日」「缴费周期」'
      + '「下次缴费日」「官费」「代理费」「已缴合计」「状态」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一条知识产权明细行']);

  // 缴费周期的单位可能写在表头里、行里只写数字 —— 把表头单位记到行上
  const cycleHeader = (t.cols.find((c) => c.role === 'cycle') || {}).header || '缴费周期(月)';
  for (const it of t.items) it.__cycleHeader = cycleHeader;

  // 基准日按硬要求取**台账内最新日期**；整表一个日期都认不出时才退回调用方给的基准日
  const basisInfo = basisDateOf(t.items);
  const basis = basisInfo.date || parseDate(payload && payload.baseDate);
  if (!basis) {
    return insufficient([
      '至少一个能认出来的日期（上次缴费日 / 下次缴费日 / 转让日 / 核对日）',
      '日期写法：2026-03-15 或 2026/3/15 或 2026年3月15日 或 20260315',
    ]);
  }

  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  const tiers = (payload && (payload.lateTiers || payload.late_tiers)) || null;
  const ratioArg = payload ? (payload.agentFeeMaxRatio || payload.agent_fee_max_ratio) : null;
  const ratio = (normNumber(ratioArg) !== null && normNumber(ratioArg) > 0)
    ? normNumber(ratioArg) : DEFAULT_AGENT_FEE_MAX_RATIO;

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkNextDate(it); if (a) findings.push(a);
    const b = checkPaidTotal(it); if (b) findings.push(b);
  }
  for (const f of checkDuplicateAppNo(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  for (const f of checkCycleInvalid(t.items)) findings.push(f);
  for (const f of checkDateOrder(t.items)) findings.push(f);
  for (const f of checkFeeMissing(t.items)) findings.push(f);

  if (paid) {
    // 订阅版比本包**多一种能力**：不是多几个数，而是把"逐项复算"升级成
    // **失权风险判定 + 可执行的处理清单**（下面这些检查 + actions）。
    for (const f of checkOverdueList(t.items, basis, tiers)) findings.push(f);
    for (const f of checkDueSchedule(t.items, basis)) findings.push(f);
    for (const f of checkStateConsistency(t.items)) findings.push(f);
    for (const f of checkDoubleCharge(t.items)) findings.push(f);
    for (const f of checkAgentFeeOutlier(t.items, ratio)) findings.push(f);
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }
  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const countOf = (c) => findings.filter((f) => f.category === c).length;
  const daysLeft = {};
  for (const it of t.items) {
    const due = day(it, 'nextPaid');
    if (!due) continue;
    daysLeft[`line${it.line}`] = {
      next_paid: due,
      days_left: daysLeftOf(it, basis),
      state: String(it.state === undefined ? '' : it.state).trim(),
    };
  }

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      basis_date: basis,
      basis_source: basisInfo.date ? basisInfo.source : '调用方给的基准日（台账里没有可认的日期）',
      official_fee_total: round2(t.items.reduce((s, it) => s + (num(it, 'officialFee') || 0), 0)),
      agent_fee_total: round2(t.items.reduce((s, it) => s + (num(it, 'agentFee') || 0), 0)),
      paid_total: round2(t.items.reduce((s, it) => s + (num(it, 'paidTotal') || 0), 0)),
      duplicate_appno_rows: countOf('同一申请号出现多行'),
      date_inverted_rows: countOf('日期倒挂'),
      basis: '下次缴费日 = 上次缴费日 + 缴费周期（年/月）；已缴合计 = 官费 + 代理费；'
        + '到期天数 = 下次缴费日 − 基准日（基准日取台账内最新日期）；'
        + '官费、代理费、滞纳金档位一律由输入提供 —— 本工具不判断任何国家/地区的费率标准。',
    },
    columns: t.cols.map((c) => c.header),
    days_left: daysLeft,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    scope: {
      rows: t.items.length,
      checks_run: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
      checks_not_run: paid ? [] : CHECKS_WITHHELD,
      basis_date: basis,
    },
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (paid) {
    result.actions = buildActions(result, t.items);
    result.scope.actions = result.actions.length;
  }
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对**，'
      + '不代表官费金额本身符合官方费率、也不代表缴费义务已履行完毕 —— 那些要对照官方缴费通知单，不在本工具范围内。';
  }
  return { status: 'success', result };
}

// 样例本身就是"故意有问题"的演示稿（医生型的表：命中即是要展示的结论）——
// 用常量声明而不是 exports 里的行内属性，`strip_free_engine` 摘付费函数时不会把它一起摘掉
const SAMPLE_HAS_FINDINGS = true;

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, dayTruth: dayDiff,
  parseDate, addMonths, addDays, dayDiff, monthsBetween, parseCycle, basisDateOf,
  CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
  LABELS, ROW_ROLES, DEFAULT_AGENT_FEE_MAX_RATIO, SAMPLE_HAS_FINDINGS,
};
