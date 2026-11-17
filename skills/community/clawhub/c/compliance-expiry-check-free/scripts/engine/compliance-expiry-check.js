#!/usr/bin/env node
/**
 * compliance-expiry-check.js —— 证照与特种设备年检到期台账核对（免费档 / 完整档共用源码）
 *
 * 真实痛点：**制造 / 物业 / 建筑 / 物流企业每个月做合规检查、每年做审计时，都必须把证照与
 * 特种设备台账核一遍**。台账上有营业执照、各类资质与许可证、危化品经营许可证、特种设备
 * 使用登记证与年检记录，各自的检验周期不同（电梯与压力容器常见 12 个月、危化品经营许可证
 * 常见 36 个月、排污许可证常见 60 个月……），到期日一多，人眼只能靠"感觉"；
 * 而**证照或特种设备逾期未检 = 罚款甚至停产**，逾期本身就是最典型的"每月都要看一遍"的事。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * 不发起任何网络请求（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现，第三方可用同一份输入复算）：
 *   有效期至     = 上次检验日期 + 检验周期（月）        （日对齐、月末夹取）
 *   距到期天数   = 有效期至 − 基准日                   （基准日取**台账内最新日期**，不取系统当天）
 *   状态一致性   = 状态写「有效」而到期日早于基准日 / 状态写「已逾期」而到期日晚于基准日
 *   到期风险分级 = 已逾期（含逾期天数与风险等级）/ 30、60、90 天内到期排期（按到期日与风险排序）
 *
 * 口径（必须写清楚，否则算出来是错的）：
 *   · 日期可写 2026-06-01 / 2026/6/1 / 20260601 / 2026年6月1日；
 *   · 检验周期以「月」为单位（电梯/压力容器常见 12，危化品经营许可证常见 36）；
 *   · **基准日**优先取表内「检查基准日」列的最大日期；没有这一列时取表内所有日期的最大值
 *     —— 一律不取系统当天，保证同输入同结论。
 *
 * 免费档执行 7 项（逐项复算 + 状态一致性 + 倒挂 / 周期 / 重复 / 空缺）；
 * 完整档在此基础上多出**一种能力**：到期风险分级 + 按紧迫度排序的处理清单（见 CHECKS_WITHHELD）。
 * ⛔ 只核台账内部的日期与状态一致性，**不给法律意见**；材料不足时**绝不给结论**。
 *
 * 调用契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 */
/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';

const CHECKS_GIVEN = [
  '有效期至勾稽（上次检验日期 + 检验周期月数，日对齐、月末夹取）',
  '距到期天数勾稽（有效期至 − 基准日；基准日取台账内最新日期，不取系统当天）',
  '状态与到期情况一致性检测（写「有效」却已过期 / 写「已逾期」却未到期）',
  '日期倒挂检测（有效期至早于上次检验日期）',
  '检验周期非正检测',
  '重复证照编号检测',
  '空白、占位符、无法识别的日期或数值检测',
];

const CHECKS_WITHHELD = [
  '到期风险分级：已逾期未检（含逾期天数与风险等级）',
  '30 / 60 / 90 天内到期排期（按到期日与风险排序）',
  '无检验记录或记录缺失检测（上次检验日期 / 检验周期缺失）',
  '责任部门缺失与同一设备重复登记检测',
  '年检费用与预算差异检测（表内同时有「年检费用」与「预算费用」两列时执行）',
  '按紧迫度排序的处理清单（到期风险清单 + 台账质量问题待办，每条带台账行号与建议动作）',
];

const OUT_OF_SCOPE = [
  '判断证照是否需要年检、检验周期应该是多少（周期以证照/设备上的实际规定与检验报告为准）',
  '给出法律意见或认定行政处罚后果（逾期风险等级是内部管理口径，不是法律结论）',
  '代替检验机构判定设备是否合格、是否可以使用（那要现场检验与检验报告）',
  '处理跨法人主体、跨台账的分摊与合并（请每个主体一张表）',
  '读取 .xlsx 或市场监管/特种设备系统的导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '检查基准日\t证照/设备名称\t证照编号\t类别\t上次检验日期\t检验周期（月）\t有效期至\t距到期天数\t状态\t年检费用\t预算费用\t责任部门',
  '2026-06-01\t曳引驱动乘客电梯（1号梯）\t梯110044********0001\t特种设备\t2025-11-20\t12\t2026-11-20\t172\t有效\t4800.00\t4800.00\t设备动力部',
  '2026-06-01\t曳引驱动乘客电梯（2号梯）\t梯110044********0002\t特种设备\t2025-09-15\t12\t2026-09-15\t106\t有效\t4800.00\t4800.00\t设备动力部',
  '2026-06-01\t固定式压力容器（储气罐）\t容110044********0017\t特种设备\t2025-12-10\t12\t2026-12-10\t192\t有效\t2600.00\t2600.00\t设备动力部',
  '2026-06-01\t危险化学品经营许可证\t沪危化经字2024第0301号\t许可证\t2024-09-30\t36\t2027-09-30\t486\t有效\t0.00\t0.00\t安全环保部',
  '2026-06-01\t排污许可证\t91310115MA1K3XYZ7Q001V\t许可证\t2025-05-20\t60\t2030-05-20\t1449\t有效\t1200.00\t1200.00\t安全环保部',
  '2026-06-01\t建筑业企业资质证书（市政公用工程）\tD2310123456\t资质\t2024-12-31\t60\t2029-12-31\t1309\t有效\t0.00\t0.00\t工程管理部',
  '2026-06-01\t营业执照\t91310115MA1K3XYZ7Q\t营业执照\t2026-01-20\t12\t2027-01-20\t233\t有效\t0.00\t0.00\t综合管理部',
].join('\n');

const TOL = 0.01;
const PLACEHOLDER = /^(待填|待补|待定|待核|待办|xxx|xxx\.xx|\?+|tbd|n\/?a|无|暂无|略)$/i;
const TOTAL_WORDS = /^(合计|总计|小计|共计|total)/i;
const DEVICE_RE = /特种设备|电梯|压力容器|压力管道|锅炉|起重机械|叉车|厂车/;
const EXPIRED_WORDS = /已逾期|逾期|过期|已失效|失效|超期/;
const VALID_WORDS = /有效|正常|在有效期|已年检|已检验|合格|已登记/;

const ROLES = {
  // ⚠️ 顺序即优先级，更具体的别名在前 —— 不能让「预算费用」被「费用」抢走、
  //    也不能让「有效期至」被宽泛别名抢走（这两个坑本仓库都踩过，见 tools/header_map_check.py）。
  basis: ['检查基准日', '台账基准日', '核对基准日', '基准日', '检查日期', '核对日期'],
  item: ['证照设备名称', '证照/设备名称', '证照名称', '设备名称', '名称'],
  certNo: ['证照编号', '设备编号', '证书编号', '使用登记证号', '编号'],
  type: ['证照类别', '设备类别', '类别', '类型'],
  lastDate: ['上次检验日期', '上次检验日', '检验日期', '上次年检日期', '年检日期', '检验日'],
  cycle: ['检验周期月', '检验周期', '周期月数', '周期月'],
  expiry: ['有效期至', '有效期止', '到期日', '有效期'],
  daysLeft: ['距到期天数', '剩余天数', '到期天数', '剩余'],
  status: ['检验状态', '证照状态', '状态'],
  budget: ['预算费用', '年检预算', '预算'],
  fee: ['年检费用', '检验费用', '年检费', '费用'],
  dept: ['责任部门', '负责部门', '归口部门', '部门'],
};

const LABELS = {
  basis: '检查基准日', item: '证照/设备名称', certNo: '证照编号', type: '类别',
  lastDate: '上次检验日期', cycle: '检验周期（月）', expiry: '有效期至', daysLeft: '距到期天数',
  status: '状态', fee: '年检费用', budget: '预算费用', dept: '责任部门',
};

const REQUIRED = ['basis', 'item', 'certNo', 'type', 'lastDate', 'cycle', 'expiry', 'daysLeft', 'status'];
const OPTIONAL_ROLES = ['fee', 'budget', 'dept'];
const DATE_ROLES = ['basis', 'lastDate', 'expiry'];
const NUM_ROLES = ['cycle', 'daysLeft'];

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
  return s === '' || /^[-—–/]+$/.test(s) || /^(n\/?a|无|暂无|待填|待补|待定)$/i.test(s);
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

const round2 = (n) => Math.round(n * 100) / 100;
const pad2 = (n) => String(n).padStart(2, '0');

function daysInMonth(y, m) {         // m 为 1~12
  return new Date(Date.UTC(y, m, 0)).getUTCDate();
}

/** 日期归一化成 YYYY-MM-DD；认不出返回 null（**不猜**，由「日期无法识别」检查项报出来） */
function normDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  let m = /^(\d{4})[-/.年](\d{1,2})[-/.月](\d{1,2})日?$/.exec(s);
  if (!m) m = /^(\d{4})(\d{2})(\d{2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (y < 1900 || y > 2999) return null;
  if (mo < 1 || mo > 12) return null;
  if (d < 1 || d > daysInMonth(y, mo)) return null;
  return `${y}-${pad2(mo)}-${pad2(d)}`;
}

function dayNum(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso || ''));
  if (!m) return null;
  return Math.round(Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3])) / 86400000);
}

/** 起算日 + 月数（日对齐、月末夹取）：2025-11-20 起 12 个月 ⇒ 2026-11-20 */
function addMonths(iso, months) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso || ''));
  if (!m) return null;
  const total = Number(m[1]) * 12 + (Number(m[2]) - 1) + Math.trunc(months);
  const ny = Math.floor(total / 12);
  const nm = (total % 12) + 1;
  const nd = Math.min(Number(m[3]), daysInMonth(ny, nm));
  return `${ny}-${pad2(nm)}-${pad2(nd)}`;
}

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: [], missingColumns: [], cols: [], present: [] };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const present = [...new Set(roles.filter(Boolean))];
  const missingColumns = REQUIRED.filter((r) => present.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i] };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      if (row[role] === undefined) row[role] = v;
      if (role === 'item' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) totals.push(row);
    else items.push(row);
  }
  return { items, totals, missingColumns, cols: headers, present };
}

const who = (it) => {
  const n = String(it.item === undefined ? '' : it.item).trim();
  const c = String(it.certNo === undefined ? '' : it.certNo).trim();
  if (!n && !c) return `台账第 ${it.line} 行`;
  return `台账第 ${it.line} 行「${n || '(未命名)'}」${c ? '（证照编号 ' + c + '）' : ''}`;
};

const numOf = (it, role) => normNumber(it[role]);
const rawOf = (it, role) => String(it[role] === undefined || it[role] === null ? '' : it[role]).trim();

/** 基准日：优先取「检查基准日」列的最大日期；否则取表内所有日期的最大值 —— 一律不取系统当天 */
function resolveBasis(t) {
  let best = null;
  for (const it of t.items) {
    const d = normDate(it.basis);
    if (d !== null && (best === null || d > best)) best = d;
  }
  if (best !== null) {
    return { iso: best, source: '台账「检查基准日」列中的最新日期（不取系统当天）' };
  }
  for (const it of t.items) {
    for (const role of DATE_ROLES) {
      const d = normDate(it[role]);
      if (d !== null && (best === null || d > best)) best = d;
    }
  }
  return {
    iso: best,
    source: best === null ? '无法确定' : '台账中出现过的最新日期（表内未写「检查基准日」列）',
  };
}

/* ================================ 免费档检查项 ================================ */

function checkExpiry(it) {
  const last = normDate(it.lastDate);
  const months = numOf(it, 'cycle');
  const stated = normDate(it.expiry);
  if (last === null || months === null || stated === null) return null;
  if (months <= 0) return null;                 // 周期非正由专门那一项报，这里不重复报
  const expect = addMonths(last, months);
  if (expect === null || expect === stated) return null;
  return {
    level: 'P0', category: '有效期至与复算不符', line: it.line,
    message: `${who(it)}的有效期至是 ${stated}，按 上次检验日期 ${last} + 检验周期 ${Math.trunc(months)} 个月`
      + `（日对齐、月末夹取）应为 ${expect}。`,
    advice: '有效期按"上次检验日 + 周期"复算一次最省事：周期填错一档、年份加错一年，都会在这里露出来。',
  };
}

function checkDaysLeft(it, basisIso) {
  const expiry = normDate(it.expiry);
  const stated = numOf(it, 'daysLeft');
  const b = dayNum(basisIso);
  const e = dayNum(expiry);
  if (stated === null || b === null || e === null) return null;
  const expect = e - b;
  if (expect === stated) return null;
  return {
    level: 'P1', category: '距到期天数与复算不符', line: it.line,
    message: `${who(it)}的距到期天数是 ${stated}，按 有效期至 ${expiry} − 基准日 ${basisIso} 应为 ${expect} 天。`,
    advice: '距到期天数只能按台账自己写明的基准日算；不要按"打开表格的那天"重算，否则同一份台账每天结论都不同。',
  };
}

/** 状态词 → 期望的到期情况；认不出的状态词（如"待检""即将到期"）不做判定 */
function statusKind(raw) {
  const s = String(raw === undefined || raw === null ? '' : raw).trim();
  if (!s) return null;
  if (EXPIRED_WORDS.test(s)) return 'expired';
  if (VALID_WORDS.test(s)) return 'valid';
  return null;
}

function checkStatus(it, basisIso) {
  const expiry = normDate(it.expiry);
  const kind = statusKind(it.status);
  const b = dayNum(basisIso);
  const e = dayNum(expiry);
  if (kind === null || b === null || e === null) return null;
  if (kind === 'valid' && e < b) {
    return {
      level: 'P0', category: '状态与到期情况不一致', line: it.line,
      message: `${who(it)}的状态写「${rawOf(it, 'status')}」，但有效期至 ${expiry} 已经早于基准日 ${basisIso}`
        + `（过期 ${b - e} 天）—— 状态没跟着更新。`,
      advice: '台账状态是月度检查的第一眼：过期了还写"有效"，等于把逾期这件事藏起来，检查就会漏掉。',
    };
  }
  if (kind === 'expired' && e >= b) {
    return {
      level: 'P1', category: '状态与到期情况不一致', line: it.line,
      message: `${who(it)}的状态写「${rawOf(it, 'status')}」，但有效期至 ${expiry} 晚于基准日 ${basisIso}`
        + `（还有 ${e - b} 天到期）—— 状态与到期日对不上。`,
      advice: '状态与到期日必须能互相解释；写成"已逾期"会让同事重复催办，也可能掩盖真正的逾期项。',
    };
  }
  return null;
}

function checkDateOrder(it) {
  const out = [];
  const last = normDate(it.lastDate);
  const stated = normDate(it.expiry);
  const b = normDate(it.basis);
  if (last !== null && stated !== null && stated < last) {
    out.push({
      level: 'P0', category: '日期倒挂：有效期至早于上次检验日期', line: it.line,
      message: `${who(it)}的有效期至（${stated}）早于上次检验日期（${last}），这个顺序不成立。`,
      advice: '两列填反了、或者检验周期填成了负数；倒挂的日期算出来的到期风险一定是错的。',
    });
  }
  if (last !== null && b !== null && last > b) {
    out.push({
      level: 'P1', category: '日期倒挂：上次检验日期晚于基准日', line: it.line,
      message: `${who(it)}的上次检验日期（${last}）晚于基准日（${b}）—— 要么基准日写旧了，要么这行填的是计划。`,
      advice: '基准日应当取台账最新一次核对日；把未来的检验计划写进"上次检验日期"会让整张表的复算落空。',
    });
  }
  return out;
}

function checkCycle(it) {
  const months = numOf(it, 'cycle');
  if (months === null) return null;
  if (months > 0) return null;
  return {
    level: 'P0', category: '检验周期非正', line: it.line,
    message: `${who(it)}的检验周期（月）是 ${months} —— 周期必须是正数（电梯/压力容器常见 12，危化品经营许可证常见 36）。`,
    advice: '周期填 0 会让有效期至等于上次检验日、填负数会让到期日倒着走；两种都会把到期风险分级带偏。',
  };
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = rawOf(it, 'certNo');
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '重复证照编号', line: it.line,
        message: `证照编号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一编号出现两行会让"到期项"被数两遍；多台设备请各自登记各自的编号，别复制粘贴。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = rawOf(it, role);
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这一行就算不出到期情况；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
    for (const role of DATE_ROLES) {
      const s = rawOf(it, role);
      if (s === '' || isBlank(s) || PLACEHOLDER.test(s)) continue;
      if (normDate(s) === null) {
        out.push({
          level: 'P0', category: '日期无法识别', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是「${s}」，认不出是哪一天。`,
          advice: '日期请写成 2026-06-01 / 2026/6/1 / 20260601 / 2026年6月1日 这几种之一；认不出的日期本工具不做猜测。',
        });
      }
    }
    for (const role of NUM_ROLES) {
      const s = rawOf(it, role);
      if (s === '' || isBlank(s) || PLACEHOLDER.test(s)) continue;
      if (normNumber(s) === null) {
        out.push({
          level: 'P0', category: '数值无法识别', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是「${s}」，认不出数字。`,
          advice: '数值列只写数字；写"约一年""见备注"这类描述无法参与复算，请改成月数与天数。',
        });
      }
    }
  }
  return out;
}

/* ====================== 完整档（付费）追加的检查项与清单 ====================== */

/** 到期风险分级：逐行算 距到期天数 → 分档 → 排序（已逾期优先，其次按到期日与台账行号） */
/** 处理清单之一：到期风险清单（按紧迫度排序，每条带台账行号与建议动作） */
/** 处理清单之二：台账质量问题待办（缺记录 / 缺部门 / 重复登记 / 费用差异），每条带行号与动作 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到台账正文（text）—— 请把含表头的证照与特种设备年检到期台账贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账表头缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(String(text).split(/\r?\n/)[0]).join(' / ')}`,
      '从证照/设备台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何证照或设备明细行');
  }
  const basis = resolveBasis(t);
  if (basis.iso === null) {
    return insufficient([
      '一个可识别的日期也找不到（「检查基准日」「上次检验日期」「有效期至」至少要有其一）',
      '基准日口径：优先取表内「检查基准日」列的最大日期；没有这一列时取表内所有日期的最大值 —— 不取系统当天',
    ]);
  }

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkExpiry(it); if (a) findings.push(a);
    const b = checkDaysLeft(it, basis.iso); if (b) findings.push(b);
    const c = checkStatus(it, basis.iso); if (c) findings.push(c);
    for (const d of checkDateOrder(it)) findings.push(d);
    const e = checkCycle(it); if (e) findings.push(e);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  const byLine = (x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category));
  findings.sort(byLine);
  const summarize = (list) => {
    const q0 = list.filter((f) => f.level === 'P0').length;
    const q1 = list.filter((f) => f.level === 'P1').length;
    const q2 = list.filter((f) => f.level === 'P2').length;
    return {
      rows: t.items.length,
      total: list.length,
      p0: q0,
      p1: q1,
      p2: q2,
      verdict: q0 > 0 ? 'ERROR_FOUND' : (list.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    };
  };

  const optionalPresent = {};
  for (const role of OPTIONAL_ROLES) optionalPresent[role] = t.present.indexOf(role) >= 0;

  let noteText = `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`;


  const result = {
    status: 'success',
    service_type: 'COMPLIANCE_EXPIRY_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_executed: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      skipped_total_rows: t.totals.length,
      basis_date: basis.iso,
      basis_source: basis.source,
      optional_columns_present: optionalPresent,
      date_convention: '日期可写 2026-06-01 / 2026/6/1 / 20260601 / 2026年6月1日；'
        + '有效期至 = 上次检验日期 + 检验周期（月，日对齐、月末夹取）；距到期天数 = 有效期至 − 基准日',
      basis_convention: '基准日取台账内最新日期（优先「检查基准日」列，其次表内所有日期），不取系统当天',
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: summarize(findings),
    checks_out_of_scope: OUT_OF_SCOPE,
    note: noteText,
    disclaimer: '只核对台账内部的日期、状态与算术一致性，不给法律意见、不判断证照是否需要年检、'
      + '不代替检验机构判定设备是否可用；每条结论都带台账原文行号，可由第三方用同一份输入复算。',
  };



  if (findings.length === 0) {
      result.verdict_note = '本次实际执行的免费检查项都通过了。这只说明这张台账的日期与状态按免费口径算得对；'
        + '到期风险分级、30/60/90 天排期、无检验记录、责任部门缺失、同一设备重复登记、'
        + '年检费用与预算差异与处理清单这几类检查本次没有执行，见 scope.checks_not_run。';
    
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, normDate, dayNum, addMonths, isBlank, round2, daysInMonth, statusKind, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, ROLES, REQUIRED, OPTIONAL_ROLES, DATE_ROLES, NUM_ROLES, TOL,
};
