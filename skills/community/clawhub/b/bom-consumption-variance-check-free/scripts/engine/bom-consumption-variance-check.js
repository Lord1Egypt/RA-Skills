#!/usr/bin/env node
/**
 * bom-consumption-variance-check.js —— BOM 用量与损耗差异核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**制造业成本会计每月结账、年度盘点审计都必须把这张表核一遍**。
 * 生产工单与物料清单（BOM）放一起，每一条用量差异都能用表上的数字算出来对错：
 *
 *   标准用量 = 单位用量 × 产出数量          （BOM 定额：单位用量里已经含了定额损耗）
 *   用量差异 = 实际领料 − 退料 − 标准用量    （正数 = 超耗，负数 = 少耗）
 *   损耗率   = 用量差异 ÷ 标准用量           （超出约定上限就是超耗）
 *
 * 超耗不查就是成本黑洞：偷料、报废未报、串料、退料没冲减，全都藏在这三条算式后面；
 * 而"差异该算到哪个工单/产品头上"正是车间与财务每月吵的那件事。
 *
 * 免费档只做**逐行复算 + 合计逐列勾稽 + 重复物料行 / 空缺 / 负值**（见 CHECKS_GIVEN）；
 * 完整档（付费）在此之上多出**一种能力：超耗归因 + 处理清单**（见 CHECKS_WITHHELD）——
 * 超耗按产品/工单归因并算出金额（差异 × 单价）、串料（物料投到了 BOM 之外的工单）、
 * 替代料未登记、退料未冲减、损耗率超约定上限，最后按金额从大到小给出带行号与建议动作的清单。
 *
 * 与已有能力的区别：`inventory-cost-flow-check` 核的是**成本流转与计价**（发出/结存单价、结转）；
 * `inventory-check` 核的是**数量盘点**（账实是否一致）；本能力核的是**用量差异**
 * —— 同一张工单上"标准用量 vs 实际领料−退料"，按工单/产品归因超耗。三者层面不同。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查 BOM 文库与工艺路线、不调用大模型；材料不足不给结论；不给审计意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '标准用量勾稽复算（标准用量 = 单位用量 × 产出数量）',
  '用量差异勾稽复算（用量差异 = 实际领料 − 退料 − 标准用量）',
  '损耗率勾稽复算（损耗率 = 用量差异 ÷ 标准用量）',
  '合计行逐列复核（标准用量 / 实际领料 / 退料 / 用量差异 四列的合计是否等于各行之和）',
  '重复物料行检测（同一工单同一物料出现多行）',
  '关键字段空缺与占位符检测',
  '单位用量与产出数量非正检测、数量与单价为负检测',
];

const CHECKS_WITHHELD = [
  '超耗归因（按产品/工单汇总超耗数量与金额：用量差异 × 单价）',
  '串料检测（同一物料被投到 BOM 归属工单之外）',
  '替代料未登记检测（标为替代料但没有替代登记单号）',
  '退料未冲减检测（用量差异漏减了退料）',
  '损耗率超出约定上限检测（超耗，金额 = 用量差异 × 单价）',
  '按金额从大到小排序的处理清单（超耗 / 串料 / 替代料未登记 / 退料未冲减，每条带行号与建议动作）',
];

const OUT_OF_SCOPE = [
  '判断 BOM 单位用量与损耗定额本身定得对不对（那是工艺/工程定额的事，本工具只按你填的定额复算）',
  '核对领料单、退料单、报废单的签字与审批流程',
  '处理单位换算与计量误差（请先把同一物料的单位统一，再贴进来）',
  '判断"超耗该由车间还是采购担责"，也不做绩效考核与责任认定',
  '读取 .xlsx / ERP 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '工单号\t产品名称\t物料编码\t物料名称\tBOM归属工单\t单位用量\t产出数量\t标准用量\t实际领料\t退料\t用量差异\t损耗率\t损耗率上限\t单价\t是否替代料\t替代登记单号',
  'WO-2606-001\t电机外壳\tA1001\t冷轧钢板\tWO-2606-001\t1.02\t1000\t1020.00\t1028.00\t0.00\t8.00\t0.78%\t2.00%\t6.50\t否\t',
  'WO-2606-001\t电机外壳\tA1002\t漆包线\tWO-2606-001\t0.85\t1000\t850.00\t862.00\t4.00\t8.00\t0.94%\t2.00%\t28.00\t否\t',
  'WO-2606-002\t齿轮箱\tB2001\t合金钢\tWO-2606-002\t2.50\t600\t1500.00\t1509.00\t0.00\t9.00\t0.60%\t1.50%\t9.80\t否\t',
  'WO-2606-002\t齿轮箱\tB2002\t轴承\tWO-2606-002\t4.00\t600\t2400.00\t2412.00\t0.00\t12.00\t0.50%\t1.50%\t15.20\t否\t',
  '合计\t\t\t\t\t\t\t5770.00\t5811.00\t4.00\t37.00\t\t\t\t\t',
].join('\n');

const TOL = 0.01;        // 数量与金额都保留两位小数
const PCT_TOL = 0.02;    // 损耗率保留两位小数，容差 0.02 个百分点

// ⚠️ 表头角色映射：**更具体的词必须排在更宽泛的前面**（本仓库踩过两次的坑，见 tools/header_map_check.py）。
//    这里有三处顺序是刻意的，改顺序会让某一列被"抢走"（不报错，只是静默算错）：
//      · BOM归属工单 必须在 工单号 之前（否则「BOM归属工单」会被「工单」抢走）；
//      · 物料编码 必须在 物料名称 之前（否则「物料编码」会被「物料」抢走）；
//      · 损耗率上限 必须在 损耗率 之前（否则「损耗率上限」会被「损耗率」抢走）。
const ROLES = {
  bomOrder: ['BOM归属工单', 'BOM适用工单', 'BOM工单', '配方工单', '适用工单'],
  workOrder: ['工单号', '生产工单', '生产订单号', '派工单号', '工单'],
  product: ['产品名称', '成品名称', '产品编码', '产品', '品名'],
  materialCode: ['物料编码', '物料编号', '材料编码', '料号'],
  materialName: ['物料名称', '材料名称', '物料'],
  unitUsage: ['单位用量', '单位耗用', '单耗'],
  outputQty: ['产出数量', '完工数量', '入库数量', '产量', '产出'],
  standardQty: ['标准用量', '标准耗用量', '定额用量'],
  issued: ['实际领料', '领料数量', '实领数量', '实际用量', '领料'],
  returned: ['退料数量', '退料', '退回数量', '退库数量'],
  variance: ['用量差异', '差异数量', '耗用差异', '超耗数量'],
  lossCap: ['损耗率上限', '允许损耗率', '损耗上限', '超耗阈值'],
  lossRate: ['损耗率', '差异率', '超耗率'],
  price: ['标准单价', '单位成本', '单价'],
  substFlag: ['是否替代料', '替代料标记', '替代标志', '替代料'],
  substDoc: ['替代登记单号', '替代审批单号', '替代单号', '替代登记'],
};

const LABELS = {
  bomOrder: 'BOM归属工单', workOrder: '工单号', product: '产品名称', materialCode: '物料编码',
  materialName: '物料名称', unitUsage: '单位用量', outputQty: '产出数量', standardQty: '标准用量',
  issued: '实际领料', returned: '退料', variance: '用量差异', lossCap: '损耗率上限',
  lossRate: '损耗率', price: '单价', substFlag: '是否替代料', substDoc: '替代登记单号',
};

// 缺了这些列就算不出用量差异，直接不给结论（材料不足绝不给结论）
const REQUIRED = ['bomOrder', 'workOrder', 'product', 'materialCode', 'materialName', 'unitUsage',
  'outputQty', 'standardQty', 'issued', 'returned', 'variance', 'lossCap', 'lossRate', 'price',
  'substFlag', 'substDoc'];

// 「替代登记单号」为空是正常的（非替代料本来就没有单号），「是否替代料」为空也算非替代料，
// 所以这两列不参与"空缺"检查 —— 它们由完整档的替代料检查负责。
const VALUE_ROLES = REQUIRED.filter((r) => r !== 'substDoc' && r !== 'substFlag');

// 合计行逐列复核的列（产出数量按物料行重复出现，不能相加）
const SUM_ROLES = ['standardQty', 'issued', 'returned', 'variance'];

const NEG_ROLES = ['standardQty', 'issued', 'returned', 'variance', 'price'];

// 这几个角色必须是正数：单位用量、产出数量（为 0 或负数时标准用量没有意义）
const POSITIVE_ROLES = ['unitUsage', 'outputQty'];

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
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
    .replace(/(公斤|千克|kg|KG|吨|t|件|个|米|支|台)$/, '')
    .replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;

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
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const first = String(cells[0] || '').trim();
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true;
      totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `第 ${it.line} 行（工单 ${it.byRole.workOrder || '未填'}／产品 ${it.byRole.product || '未填'}`
  + `／物料 ${it.byRole.materialCode || it.byRole.materialName || '未填'}）`;

/* ===== 免费档：逐行复算 + 合计勾稽 + 重复行 / 空缺 / 非正与负值 ===== */

function checkStandardQty(it) {
  const unit = num(it, 'unitUsage');
  const out = num(it, 'outputQty');
  const stated = num(it, 'standardQty');
  if (unit === null || out === null || stated === null) return null;
  const expect = round2(unit * out);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '标准用量与复算不符', line: it.line,
    message: `${who(it)}的标准用量是 ${stated.toFixed(2)}，按 单位用量 ${unit} × 产出数量 ${out.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '标准用量 = 单位用量 × 产出数量（BOM 定额）；这一列错了，后面的用量差异和损耗率会跟着一起错。',
  };
}

function checkVariance(it) {
  const issued = num(it, 'issued');
  const returned = num(it, 'returned');
  const std = num(it, 'standardQty');
  const stated = num(it, 'variance');
  if (issued === null || returned === null || std === null || stated === null) return null;
  const expect = round2(issued - returned - std);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '用量差异与复算不符', line: it.line,
    message: `${who(it)}的用量差异是 ${stated.toFixed(2)}，按 实际领料 ${issued.toFixed(2)} − 退料 ${returned.toFixed(2)} `
      + `− 标准用量 ${std.toFixed(2)}，应为 ${expect.toFixed(2)}。`,
    advice: '用量差异 = 实际领料 − 退料 − 标准用量：退料必须冲减，否则差异会虚高（完整档会指出是不是漏退了）。',
  };
}

function checkLossRate(it) {
  const variance = num(it, 'variance');
  const std = num(it, 'standardQty');
  const stated = num(it, 'lossRate');
  if (variance === null || std === null || stated === null) return null;
  if (Math.abs(std) <= 1e-9) return null;
  const expect = round2(variance / std * 100);
  if (Math.abs(expect - stated) <= PCT_TOL) return null;
  return {
    level: 'P1', category: '损耗率与复算不符', line: it.line,
    message: `${who(it)}的损耗率是 ${stated}%，按 用量差异 ${variance.toFixed(2)} ÷ 标准用量 ${std.toFixed(2)} 应为 ${expect}%。`,
    advice: '损耗率 = 用量差异 ÷ 标准用量：分母是标准用量（定额），不是实际领料；口径不同会让超耗看起来"没超"。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = num(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `第 ${t.line} 行 合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
          + `相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了工单，要么合计行没跟着更新；合计行正是给成本分析与审计看的那一行。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = `${String(it.byRole.workOrder || '').trim()}|${String(it.byRole.materialCode || '').trim()}`;
    if (key === '|' || key.endsWith('|')) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '重复物料行', line: it.line,
        message: `工单 ${it.byRole.workOrder} 的物料「${it.byRole.materialCode}」在第 ${seen.get(key)} 行已出现，`
          + `第 ${it.line} 行再次出现。`,
        advice: '同一工单同一物料只应有一行：拆成多行时合计与差异会被重复统计（也常是重复领料/串料的痕迹）。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of VALUE_ROLES) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这条物料的用量就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

function checkNonPositive(it) {
  const out = [];
  for (const role of POSITIVE_ROLES) {
    const v = num(it, role);
    if (v !== null && v <= 0) {
      out.push({
        level: 'P0', category: '单位用量或产出数量非正', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v}。`,
        advice: '标准用量以这两列为乘数：为 0 或负数时这条物料的定额与差异都没有意义（投产数量请填真实的完工/入库数）。',
      });
    }
  }
  return out;
}

function checkNegatives(items) {
  const out = [];
  for (const it of items) {
    for (const role of NEG_ROLES) {
      const v = num(it, role);
      if (v !== null && v < -TOL) {
        out.push({
          level: 'P0', category: '数量或单价为负', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}。`,
          advice: '这几列按口径都不该为负：退料/报废请填在「退料」列，别用负数冲在领料或差异里（会让合计看不出来）。',
        });
      }
    }
  }
  return out;
}

/* ===== 以下函数只在完整档被调用（免费包里没有这些实现，它们的结论也不在免费档输出里） ===== */

const SUBSTITUTE_RE = /^(是|y|yes|true|1|√|✓|替代|已替代|已登记)$/i;

/** 超耗归因：按 工单 + 产品 汇总"超出标准用量"的部分与金额（用量差异 × 单价），金额从大到小。 */
/** 处理清单：按金额从大到小，每条带行号、类别与建议动作。 */
function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的生产工单领料明细（要能认出「工单号」「产品名称」「物料编码」「BOM归属工单」「单位用量」'
      + '「产出数量」「标准用量」「实际领料」「退料」「用量差异」「损耗率」「损耗率上限」「单价」'
      + '「是否替代料」「替代登记单号」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从工单领料明细/ERP 导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）；'
      + '「BOM归属工单」= 该物料按 BOM 应投的工单（用来查串料）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一行工单领料明细行（合计行不算明细）']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkStandardQty(it); if (a) findings.push(a);
    const b = checkVariance(it); if (b) findings.push(b);
    const c = checkLossRate(it); if (c) findings.push(c);
  }
  // ⚠️ 每个检查函数都按 `|| []` 兜底：函数被钉成 return null（变异测试）时不该把整个引擎带崩。
  for (const role of SUM_ROLES) {
    for (const f of (checkTotalRow(t.totals, t.items, role) || [])) findings.push(f);
  }
  for (const f of (checkDuplicates(t.items) || [])) findings.push(f);
  for (const f of (checkBlanks(t.items) || [])) findings.push(f);
  for (const it of t.items) {
    for (const f of (checkNonPositive(it) || [])) findings.push(f);
  }
  for (const f of (checkNegatives(t.items) || [])) findings.push(f);

  let overuse = [];
  let actions = [];
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const stdTotal = sumOf('standardQty');
  const varianceTotal = sumOf('variance');
  const actionAmountTotal = round2(actions.reduce((s, a) => s + a.amount, 0));

  const result = {
    findings,
    overuse_by_group: overuse,
    action_plan: actions,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      standard_qty_total: stdTotal,
      issued_total: sumOf('issued'),
      returned_total: sumOf('returned'),
      variance_total: varianceTotal,
      loss_rate_pct: Math.abs(stdTotal) > 1e-9 ? round2(varianceTotal / stdTotal * 100) : null,
      overuse_amount_total: 0,
      action_amount_total: actionAmountTotal,
      basis: '标准用量 = 单位用量 × 产出数量；用量差异 = 实际领料 − 退料 − 标准用量；'
        + '损耗率 = 用量差异 ÷ 标准用量；合计行逐列复核（标准用量/实际领料/退料/用量差异）。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    scope: {
      rows: t.items.length,
      checks: CHECKS_GIVEN,
      withheld: CHECKS_WITHHELD,
      checks_not_run: notRun,
      standard_qty_total: stdTotal,
      issued_total: sumOf('issued'),
      returned_total: sumOf('returned'),
      variance_total: varianceTotal,
      overuse_amount_total: 0,
      action_amount_total: actionAmountTotal,
    },
  };
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**，'
      + '不代表 BOM 定额本身定得合理、也不代表领料与退料的审批流程合规 —— 那些不在本工具范围内。';
  }


  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, VALUE_ROLES,
};
