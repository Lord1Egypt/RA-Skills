#!/usr/bin/env node
/**
 * equipment-maintenance-cost-check-full.js —— 设备维保与备件领用费用核对（免费档 / 完整档共用源码）
 *
 * 真实痛点：制造业 / 物业 / 物流的**设备科每月结账前**都要把这张表核一遍，
 * 而它是三条串行算式加三处最容易漏钱的地方：
 *   ① 工时费 = 维修工时 × 工时单价
 *   ② 备件金额 = 领用数量 × 备件单价
 *   ③ 月度维保费用 = Σ(工时费 + 备件金额 + 外委实际结算)，再与月度维保预算比
 *   漏钱的三处（免费档**只看得到、判不出**，完整档才逐条落地）：
 *   · 保修期内（含质保期内）的保养/维修本该由厂家免费做，台账里却计了钱；
 *   · 外委维修的**实际结算 > 报价**，没人拿报价单对过结算单；
 *   · 备件**领用数量 > 出库数量**，领用单与出库单是两本账。
 * 月份一多、设备一多、备件一多，人眼核这三处几乎必漏。
 *
 * 与已有能力的区别：进销存 / 库存账实类能力核的是**仓库数量与库存金额**；
 * 本能力核的是**维保费用口径**（工时费、备件金额、外委结算、月度预算归集），
 * 并落点在"该找谁、要回多少钱"。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查保修合同与厂家系统、不调用大模型；材料不足不给结论。
 */
'use strict';

const CHECKS_GIVEN = [
  '工时费复算（维修工时 × 工时单价）',
  '备件金额复算（领用数量 × 备件单价）',
  '月度维保费用归集与预算对比（工时费 + 备件金额 + 外委实际结算）',
  '合计行逐列复核（工时费 / 备件金额 / 外委实际结算）',
  '整行内容重复检测（同一设备同一备件的行被复制了一遍）',
  '同一行既有自修费用又有外委结算（重复计费嫌疑）',
  '关键字段空缺或占位符检测',
  '明细出现负值检测（冲销、退库需要单独列行）',
];

const CHECKS_WITHHELD = [
  '保修期内应免费却计费判定（在保设备被收了工时费 / 备件费 / 外委结算）',
  '外委维修实际结算超报价判定（超支金额与超支比例）',
  '备件领用超领判定（领用数量 > 出库数量，差额按备件单价折成金额）',
  '按金额排序的处理清单（该找谁、要回多少钱，逐条带原文行号）',
];

const OUT_OF_SCOPE = [
  '判断一台设备到底在不在保修期内（本工具只认你填的「保修状态」列，不读合同、不查厂家系统）',
  '判断外委超报价是否有正当理由（变更单、追加项目属商务判断，不在算术范围）',
  '判断备件单价、工时单价是否合理（那是采购比价与工时定额的事）',
  '处理备件退库、质保返修、跨月费用分摊等特殊口径（请把它们单独列行）',
  '给出税务或成本会计意见；读取 .xlsx（需要你先导出成文本贴进来）',
];

// 样例本身就是一张**干净**的维保台账与备件领用单（跑出来 0 条结论）：
// 两个月份、7 行明细、1 行合计；保修期内的那台只登记发生、金额为 0。
const SAMPLE_TEXT = [
  ['费用归属月份', '设备编号', '设备名称', '维保类型', '维修工时', '工时单价', '工时费',
    '备件编号', '备件名称', '领用数量', '出库数量', '备件单价', '备件金额',
    '外委报价', '实际结算', '保修状态', '月度维保预算'],
  ['2026-03', 'EQ-001', '注塑机', '保养', '6', '80', '480', 'SP-1001', '液压油滤芯', '2', '2', '120', '240', '', '', '已过保', '6000'],
  ['2026-03', 'EQ-002', '空压机', '维修', '4', '100', '400', 'SP-1002', '空气滤芯', '3', '3', '60', '180', '', '', '已过保', '6000'],
  ['2026-03', 'EQ-003', '电动叉车', '外委', '', '', '', '', '', '', '', '', '', '3000', '2900', '已过保', '6000'],
  ['2026-03', 'EQ-004', '数控车床', '保养', '', '', '0', '', '', '', '', '', '0', '', '', '保修期内', '6000'],
  ['2026-04', 'EQ-001', '注塑机', '保养', '5', '80', '400', 'SP-1001', '液压油滤芯', '2', '2', '120', '240', '', '', '已过保', '7000'],
  ['2026-04', 'EQ-005', '冷却塔', '维修', '8', '75', '600', 'SP-1004', '密封圈', '4', '4', '35', '140', '', '', '已过保', '7000'],
  ['2026-04', 'EQ-006', '螺杆机', '外委', '', '', '', '', '', '', '', '', '', '5000', '5000', '已过保', '7000'],
  ['合计', '', '', '', '', '', '1880', '', '', '', '', '', '800', '', '7900', '', ''],
].map((r) => r.join('\t')).join('\n');

const TOL = 0.01;          // 金额容差：1 分
const QTY_TOL = 1e-9;      // 数量容差

// ⚠️ 关键词顺序就是判据：更具体的词必须排在更宽泛的前面（tools/header_map_check.py 会机械复核）。
//    「工时费」「工时单价」必须排在「工时」之前，否则整列会被 hours 抢走。
const ROLES = {
  period: ['费用归属月份', '归属月份', '月份', '期间'],
  equip: ['设备编号', '资产编号', '设备号', '资产号'],
  equipName: ['设备名称', '资产名称'],
  kind: ['维保类型', '保养类型', '工单类型'],
  laborFee: ['工时费', '人工费', '工时金额'],
  rate: ['工时单价', '小时单价', '工时费率'],
  hours: ['维修工时', '工时'],
  partAmt: ['备件金额', '备件费'],
  partPrice: ['备件单价', '备件价格'],
  qty: ['领用数量', '领用数'],
  issued: ['出库数量', '出库数'],
  budget: ['月度维保预算', '维保预算', '月度预算'],
  partNo: ['备件编号', '备件编码', '备件号'],
  partName: ['备件名称', '材料名称'],
  quote: ['外委报价', '外包报价', '外委单价'],
  settle: ['实际结算', '结算金额', '外委结算'],
  warranty: ['保修状态', '质保状态', '保修期'],
};

const LABELS = {
  period: '费用归属月份', equip: '设备编号', equipName: '设备名称', kind: '维保类型',
  hours: '维修工时', rate: '工时单价', laborFee: '工时费', partNo: '备件编号',
  partName: '备件名称', qty: '领用数量', issued: '出库数量', partPrice: '备件单价',
  partAmt: '备件金额', quote: '外委报价', settle: '实际结算', warranty: '保修状态',
  budget: '月度维保预算',
};

// 表头必须能认出来的列（缺了就不给任何结论）；出库数量 / 外委报价 / 实际结算 / 保修状态等
// 列可以没有，那种情况下依赖它们的检查会**如实**进 checks_not_run，不会被伪造成执行过。
const REQUIRED = ['period', 'equip', 'equipName', 'kind', 'hours', 'rate', 'laborFee',
  'qty', 'partPrice', 'partAmt', 'budget'];
// 合计行逐列复核的列
const SUM_ROLES = ['laborFee', 'partAmt', 'settle'];
// 每一行都必须有的结构性字段（按值判，不按表头判）
const STRUCT_ROLES = ['period', 'equip', 'kind', 'budget'];

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
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
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
  return { cols, items, totals, roles: have };
}

const num = (it, role) => normNumber(it.byRole[role]);
const amt = (it, role) => {
  const v = num(it, role);
  return v === null ? 0 : v;
};
const fmt = (n) => Number(n).toFixed(2);
const rawOf = (it, role) => String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();

const who = (it) => {
  const no = rawOf(it, 'equip') || '(无设备编号)';
  const nm = rawOf(it, 'equipName');
  const pno = rawOf(it, 'partNo');
  const pnm = rawOf(it, 'partName');
  const part = (pno || pnm) ? `的备件「${pno} ${pnm}」` : '的维保工单';
  return `设备「${no} ${nm}」${part}（第 ${it.line} 行）`;
};

// 本行进入月度归集的费用：工时费 + 备件金额 + 外委实际结算
const rowCost = (it) => round2(amt(it, 'laborFee') + amt(it, 'partAmt') + amt(it, 'settle'));

// 外委行只记「外委报价 / 实际结算」，自修行只记「工时费 / 备件金额」——认不出类型时不猜
function isOutsourced(it) {
  const k = rawOf(it, 'kind');
  if (!k) return null;
  if (/外委|外包|委外|外协/.test(k)) return true;
  if (/保养|维修|自修|巡检|点检|大修|小修/.test(k)) return false;
  return null;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkLaborFee(it) {
  const h = num(it, 'hours');
  const r = num(it, 'rate');
  const stated = num(it, 'laborFee');
  if (h === null || r === null || stated === null) return null;
  const expect = round2(h * r);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '工时费与复算不符', line: it.line, raw: it.raw,
    message: `${who(it)}的工时费是 ${fmt(stated)}，按 维修工时 ${h} × 工时单价 ${fmt(r)} 应为 ${fmt(expect)}。`,
    advice: '工时费只能按"元/小时 × 小时数"算；包干价要先拆成工时与单价，否则这一列随时会对不上。',
  };
}

function checkPartAmount(it) {
  const q = num(it, 'qty');
  const p = num(it, 'partPrice');
  const stated = num(it, 'partAmt');
  if (q === null || p === null || stated === null) return null;
  const expect = round2(q * p);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '备件金额与复算不符', line: it.line, raw: it.raw,
    message: `${who(it)}的备件金额是 ${fmt(stated)}，按 领用数量 ${q} × 备件单价 ${fmt(p)} 应为 ${fmt(expect)}。`,
    advice: '备件金额要按领用数量乘单价；数量或单价有一格是估的，这一行就核不动。',
  };
}

function checkDoubleCount(it) {
  const self = round2(amt(it, 'laborFee') + amt(it, 'partAmt'));
  const settle = num(it, 'settle');
  if (settle === null || self <= TOL) return null;
  return {
    level: 'P1', category: '同一行既有自修费用又有外委结算', line: it.line, raw: it.raw,
    message: `${who(it)}同时记了自修费用 ${fmt(self)} 元（工时费 ${fmt(amt(it, 'laborFee'))} + 备件金额 ${fmt(amt(it, 'partAmt'))}）和外委实际结算 ${fmt(settle)} 元。`,
    advice: '外委维修的工时与备件由服务商承担：外委行请把工时费、备件金额两列留空，只填报价与实际结算；两边都填，一次维修就被算了两遍费用。',
  };
}

function checkPeriodBudget(items) {
  const out = [];
  const groups = new Map();
  for (const it of items) {
    const p = rawOf(it, 'period') || '(未填月份)';
    if (!groups.has(p)) groups.set(p, []);
    groups.get(p).push(it);
  }
  for (const [p, rows] of groups) {
    const actual = round2(rows.reduce((s, it) => s + rowCost(it), 0));
    const budgets = [];
    for (const it of rows) {
      const b = num(it, 'budget');
      if (b !== null && budgets.indexOf(b) < 0) budgets.push(b);
    }
    if (!budgets.length) continue;   // 预算一列空着：本期不做预算对比（空缺检测会单独报）
    if (budgets.length > 1) {
      out.push({
        level: 'P1', category: '同一月份出现多个预算值', line: rows[0].line, raw: rows[0].raw,
        message: `${p} 各行填的「月度维保预算」不一样（${budgets.map(fmt).join(' / ')} 元），本工具按第一次出现的 ${fmt(budgets[0])} 元对比。`,
        advice: '同一月份的预算只能有一个口径（要么都是本月预算、要么都留空）；有人填月预算、有人填全年预算，这个结论就没有意义了。',
      });
    }
    const budget = budgets[0];
    const diff = round2(actual - budget);
    if (diff > TOL) {
      const pct = budget > 0 ? round2(diff / budget * 100) : null;
      out.push({
        level: 'P1', category: '月度维保费用超出预算', line: rows[0].line, raw: rows[0].raw,
        message: `${p} 实际归集 ${fmt(actual)} 元（工时费 + 备件金额 + 外委实际结算），月度维保预算 ${fmt(budget)} 元，超预算 ${fmt(diff)} 元${pct === null ? '' : `（超 ${pct}%）`}。`,
        advice: '超预算要能说出是哪几台设备、哪几笔外委推上去的：把本月明细按设备归类，再核一次预算口径（含税/不含税、含不含外委）。',
      });
    }
  }
  return out;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => s + amt(it, role), 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line, raw: t.raw,
        message: `合计行的「${LABELS[role]}」是 ${fmt(stated)}，各明细行相加是 ${fmt(sum)}，相差 ${fmt(stated - sum)}。`,
        advice: '要么明细行漏了工单，要么合计行没跟着更新；合计行是给领导看的那一行，错了整张表的可信度都没了。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  const KEY_ROLES = ['period', 'equip', 'partNo', 'kind', 'hours', 'qty', 'laborFee', 'partAmt', 'settle'];
  for (const it of items) {
    const key = KEY_ROLES.map((r) => rawOf(it, r)).join('|');
    if (key.replace(/\|/g, '') === '') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '整行内容重复', line: it.line, raw: it.raw,
        message: `第 ${seen.get(key)} 行与第 ${it.line} 行内容完全相同（同一月份 ${rawOf(it, 'period')}、同一设备「${rawOf(it, 'equip')}」、同一备件「${rawOf(it, 'partNo')}」）。`,
        advice: '多半是从上一条复制过来忘了改：先确认是不是一次维修被登记了两遍；确实发生了两次，请补上不同的工单号或备件批次。',
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
    for (const role of STRUCT_ROLES) {
      const s = rawOf(it, role);
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段空缺或为占位符', line: it.line, raw: it.raw,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '这一格决定这笔费用归到哪台设备、哪个月；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
    const outsourced = isOutsourced(it);
    if (outsourced === true) {
      if (num(it, 'settle') === null) {
        out.push({
          level: 'P0', category: '关键字段空缺或为占位符', line: it.line, raw: it.raw,
          message: `${who(it)}标成外委（${rawOf(it, 'kind')}），但「实际结算」是空的（${rawOf(it, 'settle') || '空'}）。`,
          advice: '外委行只需要填「外委报价」与「实际结算」；结算金额没有，这笔费用既归不了集、也没法判断有没有超报价。',
        });
      }
    } else if (outsourced === false) {
      for (const role of ['laborFee', 'partAmt']) {
        if (num(it, role) === null) {
          out.push({
            level: 'P0', category: '关键字段空缺或为占位符', line: it.line, raw: it.raw,
            message: `${who(it)}是自修（${rawOf(it, 'kind')}），但「${LABELS[role]}」是空的（${rawOf(it, role) || '空'}）。`,
            advice: '自修行要填工时费与备件金额（这次没用备件就填 0，不要留空）；留空会让月度归集少算这笔钱。',
          });
        }
      }
    }
  }
  return out;
}

function checkNegatives(items) {
  const out = [];
  const CHECKED = ['hours', 'rate', 'laborFee', 'qty', 'issued', 'partPrice', 'partAmt', 'quote', 'settle'];
  for (const it of items) {
    for (const role of CHECKED) {
      const v = num(it, role);
      if (v !== null && v < -TOL) {
        out.push({
          level: 'P1', category: '明细出现负值', line: it.line, raw: it.raw,
          message: `${who(it)}的「${LABELS[role]}」是 ${v}。`,
          advice: '冲销、退库、红字结算请单独列一行并在备注写明原因；负数混在明细里，月度归集不是漏算就是重算。',
        });
      }
    }
  }
  return out;
}

/* ===== 以下函数只有完整档会调用（免费包里没有它们的实现） ===== */

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的设备维保台账与备件领用单（要能认出「费用归属月份」「设备编号」「维保类型」'
      + '「维修工时」「工时单价」「工时费」「领用数量」「备件单价」「备件金额」「月度维保预算」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从维保台账 / 备件领用系统导出后，连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一行维保工单明细（「合计」行不算明细）']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkLaborFee(it); if (a) findings.push(a);
    const b = checkPartAmount(it); if (b) findings.push(b);
    const c = checkDoubleCount(it); if (c) findings.push(c);
  }
  for (const f of checkPeriodBudget(t.items)) findings.push(f);
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  for (const f of checkNegatives(t.items)) findings.push(f);

  let actions = [];
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => s + amt(it, role), 0));

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      periods: new Set(t.items.map((it) => rawOf(it, 'period') || '(未填月份)')).size,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      labor_fee_total: sumOf('laborFee'),
      part_amount_total: sumOf('partAmt'),
      outsourced_settle_total: sumOf('settle'),
      maintenance_cost_total: round2(sumOf('laborFee') + sumOf('partAmt') + sumOf('settle')),
      basis: '工时费 = 维修工时 × 工时单价；备件金额 = 领用数量 × 备件单价；'
        + '月度维保费用 = Σ(工时费 + 备件金额 + 外委实际结算)，与「月度维保预算」对比；合计行逐列复核。'
        + '只报"超预算"，不报"低于预算"。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  result.scope = {
    tier: 'free',
    checks_run: CHECKS_GIVEN,
    checks_not_run: notRun,
    out_of_scope: OUT_OF_SCOPE,
  };

  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明这张表按上面写明的口径算得对；'
      + '保修期起止、外委报价是否含税等商务事实，本工具不替你判断。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, REQUIRED, SUM_ROLES,
};
