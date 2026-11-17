/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * fleet-fuel-cost-check.js —— 车队油耗与运费核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**物流车队每月核账时**，财务 / 车管必须把「车辆油耗与运费台账」
 * 逐车逐月核一遍：行驶里程、百公里油耗定额、油卡加油量、油费、过路费、单车运费收入。
 * 油耗明显高于定额，通常意味着**偷油、私车公用、里程漏记或油卡管理漏洞** ——
 * 这些都能用表**内部的算术关系**查出来，不需要任何外部数据。完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   定额油耗   = 行驶里程 ÷ 100 × 百公里油耗定额
 *   油耗差异   = 油卡加油量 − 定额油耗（**可以为负**：负数是省油，不是错）
 *   单车成本   = 油费金额 + 过路费
 *   油卡充值额 ≈ 油卡加油量 × 油品单价
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**油耗定额、油品单价与运费单价（各车队、各线路都不同）：
 *    一律以表里给的为准，只对"明显超出常见区间"做**提示**并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '定额油耗复算（行驶里程 ÷ 100 × 百公里油耗定额 = 定额油耗）',
  '油耗差异复算（油卡加油量 − 定额油耗 = 油耗差异）',
  '合计行逐列复核',
  '同一车牌同一月份重复行检测',
  '空白与占位符检测',
  '数量或金额为负检测',
];

const CHECKS_WITHHELD = [
  '单车油耗超定额比例超过参考上限（10%）提示（参考口径）',
  '单车收入低于成本（油费金额 + 过路费）提示',
  '油卡加油量与油卡充值额不一致检测（充值额 vs 加油量 × 油品单价）',
  '里程为零却有油耗检测',
  '百公里油耗偏离参考区间（20~50L/100km）提示（参考口径）',
];

const OUT_OF_SCOPE = [
  '认定"偷油"行为、责任与赔偿（那是纪检 / 司法判断；本工具只给算术差异与线索）',
  '判断百公里油耗定额、油品单价、运费单价本身是否合理（以本单位定额文件与运输合同为准）',
  '核对加油小票、油卡流水、过磅单与运费结算单的真实性（需要你先导出成文本贴进来）',
  '处理跨月预充值、油卡余额结转、未用油量与线路归属的期间划分',
];

/* 参考区间：仅供"明显超出"时提示，不构成定额 */
const OVER_QUOTA_REF = 0.10;            // 单车油耗超定额比例参考上限：10%
const CONSUMPTION_REF = [20, 50];       // 实测百公里油耗参考区间（L/100km）

const SAMPLE_TEXT = [
  '月份\t车牌号\t行驶里程\t百公里油耗定额\t定额油耗\t油卡加油量\t油耗差异\t油品单价\t油卡充值额\t油费金额\t过路费\t运费收入',
  '2026-01\t京A12345\t5000.00\t30.00\t1500.00\t1480.00\t-20.00\t7.50\t11100.00\t11100.00\t1200.00\t15000.00',
  '2026-01\t京A67890\t4200.00\t28.00\t1176.00\t1140.00\t-36.00\t7.50\t8550.00\t8550.00\t900.00\t13500.00',
  '2026-02\t京A12345\t6000.00\t30.00\t1800.00\t1760.00\t-40.00\t7.50\t13200.00\t13200.00\t1500.00\t18000.00',
  '合计\t\t15200.00\t\t4476.00\t4380.00\t-96.00\t\t32850.00\t32850.00\t3600.00\t46500.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的前面。
  //    「百公里油耗定额」里含有「油耗定额」四个字 —— 若把「油耗定额」所属的角色排在前面，
  //    它会把「百公里油耗定额」整列**抢走**，两列落到同一个角色、后一列覆盖前一列：
  //    不报缺列、不报错，只是从此**静默算错**（里程 ÷ 100 × 定额那一列变成定额值）。
  period: ['月份', '所属月份', '期间', '所属期'],
  plate: ['车牌号', '车牌', '车号'],
  mileage: ['行驶里程', '里程'],
  fuelStd: ['百公里油耗定额', '百公里油耗', '油耗定额'],
  fuelQuota: ['定额油耗', '应耗油量'],
  fuelActual: ['油卡加油量', '实际加油量', '加油量'],
  fuelDiff: ['油耗差异', '油耗差'],
  fuelPrice: ['油品单价', '燃油单价', '单价'],
  cardRecharge: ['油卡充值额', '油卡充值金额', '充值额'],
  fuelCost: ['油费金额', '燃油费金额', '油费'],
  tollCost: ['过路费', '通行费', '路桥费'],
  revenue: ['运费收入', '单车收入', '运费'],
};

const LABELS = {
  period: '月份', plate: '车牌号', mileage: '行驶里程', fuelStd: '百公里油耗定额',
  fuelQuota: '定额油耗', fuelActual: '油卡加油量', fuelDiff: '油耗差异',
  fuelPrice: '油品单价', cardRecharge: '油卡充值额', fuelCost: '油费金额',
  tollCost: '过路费', revenue: '运费收入',
};

const REQUIRED = ['period', 'plate', 'mileage', 'fuelStd', 'fuelQuota', 'fuelActual', 'fuelDiff'];
/* 可加总的列：比率 / 单价列（百公里油耗定额、油品单价）**不在其中** —— 比率不能相加 */
const SUM_ROLES = ['mileage', 'fuelQuota', 'fuelActual', 'fuelDiff', 'cardRecharge',
  'fuelCost', 'tollCost', 'revenue'];
/* "为负"要查的数量与金额列。⚠️ 油耗差异**故意不在其中**：差异为负 = 实际比定额省，是好事 */
const NEG_ROLES = ['mileage', 'fuelStd', 'fuelQuota', 'fuelActual', 'fuelPrice',
  'cardRecharge', 'fuelCost', 'tollCost', 'revenue'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|全年合计|累计)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|待核实)$/i.test(s);
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
  const s = String(raw).trim()
    .replace(/[,，\s¥￥$]/g, '')
    .replace(/\/100\s*km$/i, '')
    .replace(/\/百公里$/, '')
    .replace(/(公里|千米|km|升|L|元|度)$/i, '')
    .replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

function who(it) {
  const period = String((it && it.period) || '').trim();
  const plate = String((it && it.plate) || '').trim();
  const tag = [period, plate].filter(Boolean).join(' ');
  return tag ? `第 ${it.line} 行（${tag}）` : `第 ${it.line} 行`;
}

/* ================================ 免费档检查项 ================================
 * ⚠️ 约定：**每个 check 函数都返回数组**，调用处一律 `for (const f of checkX(it)) findings.push(f);`。
 *    不要在这里混用"返回对象 / 返回数组"两种风格 —— 一旦把返回空数组的函数写成 `if (x) push(x)`，
 *    空数组是**真值**，会被当成一条发现塞进结论里（本仓库刚踩过）。
 * ========================================================================== */

function checkFuelQuota(it) {
  const out = [];
  const mileage = normNumber(it.mileage);
  const std = normNumber(it.fuelStd);
  const stated = normNumber(it.fuelQuota);
  if (mileage === null || std === null || stated === null) return out;
  const expect = round2((mileage / 100) * std);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '定额油耗复算不符', line: it.line,
    message: `${who(it)}：行驶里程 ${mileage.toFixed(2)} ÷ 100 × 百公里油耗定额 ${std.toFixed(2)} 应为 ${expect.toFixed(2)} 升，表里定额油耗是 ${stated.toFixed(2)} 升，相差 ${round2(stated - expect).toFixed(2)} 升。`,
  });
  return out;
}

function checkFuelDiff(it) {
  const out = [];
  const actual = normNumber(it.fuelActual);
  const quota = normNumber(it.fuelQuota);
  const stated = normNumber(it.fuelDiff);
  if (actual === null || quota === null || stated === null) return out;
  const expect = round2(actual - quota);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '油耗差异复算不符', line: it.line,
    message: `${who(it)}：油卡加油量 ${actual.toFixed(2)} − 定额油耗 ${quota.toFixed(2)} = ${expect.toFixed(2)} 升，表里油耗差异是 ${stated.toFixed(2)} 升，相差 ${round2(stated - expect).toFixed(2)} 升。`,
  });
  return out;
}

function checkNegatives(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v < -TOL) {
      out.push({
        level: 'P0', category: '数量或金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回或红字建议单独列示，不要混在正常行里。`,
      });
    }
  }
  return out;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各车各行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const period = String(it.period || '').trim();
    const plate = String(it.plate || '').trim();
    if (!period && !plate) continue;
    const key = `${period}|${plate}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一车牌同一月份重复行', line: it.line,
        message: `${who(it)}与第 ${seen.get(key)} 行是同一个车牌同一个月份 —— 里程、油耗与运费会被重复统计。`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 这一行算不出油耗定额，请补齐。`,
        });
      }
    }
  }
  return out;
}

/* 完整档（付费）检查项：只在 paid 为真时执行（形态 B —— 付费函数散落在文件中，由 strip 工具按引用摘除） */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到台账正文（text）—— 请把「月份 / 车牌号 / 行驶里程 / 百公里油耗定额 / 定额油耗 / 油卡加油量 / 油耗差异」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何车辆明细行');
  }

  const findings = [];
  for (const it of t.items) {
    for (const f of checkFuelQuota(it)) findings.push(f);
    for (const f of checkFuelDiff(it)) findings.push(f);
    for (const f of checkNegatives(it)) findings.push(f);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const plates = new Set();
  const periods = new Set();
  let mileageTotal = 0; let fuelTotal = 0; let revenueTotal = 0; let costTotal = 0;
  for (const it of t.items) {
    const p = String(it.plate === undefined ? '' : it.plate).trim();
    const m = String(it.period === undefined ? '' : it.period).trim();
    if (p) plates.add(p);
    if (m) periods.add(m);
    const a = normNumber(it.mileage); if (a !== null) mileageTotal += a;
    const b = normNumber(it.fuelActual); if (b !== null) fuelTotal += b;
    const c = normNumber(it.revenue); if (c !== null) revenueTotal += c;
    const d = normNumber(it.fuelCost); if (d !== null) costTotal += d;
    const e = normNumber(it.tollCost); if (e !== null) costTotal += e;
  }

  const result = {
    status: 'success',
    service_type: 'FLEET_FUEL_COST_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      vehicles: plates.size,
      mileage_total: round2(mileageTotal),
      fuel_actual_total: round2(fuelTotal),
      revenue_total: round2(revenueTotal),
      cost_total: round2(costTotal),
      over_quota_ref: OVER_QUOTA_REF,
      consumption_ref: CONSUMPTION_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: '本版本只执行：' + CHECKS_GIVEN.join('、') + '；未执行的检查项见 scope.checks_not_run。',
    disclaimer: '只核"里程 ÷ 100 × 定额 = 定额油耗""加油量 − 定额油耗 = 油耗差异""油费 + 过路费 ≤ 运费收入"这类**表内勾稽**，'
      + '**不规定**油耗定额、油品单价与运费单价（以本单位定额文件与运输合同为准）；'
      + '油耗偏高只是**线索**，是否偷油要另行取证；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
