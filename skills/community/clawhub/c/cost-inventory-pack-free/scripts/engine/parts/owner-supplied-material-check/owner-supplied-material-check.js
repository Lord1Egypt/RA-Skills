#!/usr/bin/env node
/**
 * owner-supplied-material-check.js —— 甲供材料与分包领用核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**建筑 / 装饰 / 安装工程每月计量与竣工结算时必做**。
 * 甲方把钢材、商品混凝土、电缆、防水卷材这些材料直接供到工地（甲供材），分包单位凭领用单领走、
 * 用不完退库；结算时甲方按「领用数量 × 单价」把钱从分包结算款里抵扣掉。这条链上每一环都是钱：
 *   ① 领用数量 = 进场数量 − 退库数量（领多领少都要有单据说清）
 *   ② 领用金额 = 领用数量 × 单价
 *   ③ 结算抵扣金额 = 领用金额（甲方抵扣要与分包领用对得上）
 * 领用超过应领用就是**超领**，按合同要扣款；退库没冲减就是**多扣分包的钱**；
 * 抵扣漏扣则是甲方自己少扣、材料款白送。台账一长（几十种材料 × 几个分包），人眼逐行复算极易错。
 *
 * 谁 / 何时 / 为何：项目成本员与分包结算员在**每月计量报量与竣工结算**这两个节点上核这张表；
 * 甲供材对不上就是甲方扣款、分包扯皮，谁也说服不了谁。
 *
 * 与已有能力的区别：本仓库的「三单匹配」一类能力核的是**采购订单 / 入库单 / 发票**三者一致；
 * 本能力核的是**甲供材台账与分包领用 / 退库 / 结算抵扣**这条领用链（含超领扣款判定），层面不同。
 *
 * 对外契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查合同文库、不调用大模型；材料不足**绝不给结论**；不给法律或造价鉴定意见。
 * 每个结论都带原文行号（`line`）与出处（分包单位 / 材料名称），第三方可用同一份输入复算。
 */
/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';

const CHECKS_GIVEN = [
  '领用数量勾稽（领用数量 = 进场数量 − 退库数量）',
  '领用金额勾稽（领用金额 = 领用数量 × 单价）',
  '结算抵扣金额勾稽（结算抵扣金额 = 领用金额）',
  '合计行逐列复核（进场 / 退库 / 领用数量、领用金额、结算抵扣金额）',
  '重复材料行检测（同一分包单位 + 同一材料出现多行）',
  '关键字段缺失与占位符检测',
  '数量或金额为负检测',
];

const CHECKS_WITHHELD = [
  '超领判定（领用数量 > 进场数量 − 退库数量）与超领金额（超领数量 × 单价）',
  '无领用单的领用检测（领用数量 > 0 但领用单号空缺）',
  '退库未冲减检测（有退库数量，结算抵扣仍按进场数量多扣）',
  '单价与合同单价不一致检测（含差额金额）',
  '甲供材抵扣漏扣检测（有领用金额，但结算抵扣金额为 0 或空缺）',
  '结算前处理清单（按涉及金额排序、逐条带原文行号与建议动作）',
];

const OUT_OF_SCOPE = [
  '判断材料单价本身是否合理、是否与市场价一致（合同约定优先）',
  '处理甲供材的增值税、发票与甲供材计税口径（那是税务的事）',
  '处理损耗率、定额含量、材料节约分成等商务条款的合法性',
  '给出法律意见或造价鉴定结论；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '材料名称\t分包单位\t单位\t进场数量\t退库数量\t领用数量\t领用单号\t单价\t合同单价\t领用金额\t结算抵扣金额',
  '螺纹钢 HRB400\t华建劳务\t吨\t120.000\t4.000\t116.000\tLL-2026-001\t4200.00\t4200.00\t487200.00\t487200.00',
  '商品混凝土 C30\t华建劳务\t立方米\t800.000\t0.000\t800.000\tLL-2026-002\t460.00\t460.00\t368000.00\t368000.00',
  '电缆 YJV-4x95\t安装分公司\t米\t1500.000\t60.000\t1440.000\tLL-2026-003\t88.50\t88.50\t127440.00\t127440.00',
  '防水卷材 SBS\t安装分公司\t平方米\t2400.000\t0.000\t2400.000\tLL-2026-004\t32.00\t32.00\t76800.00\t76800.00',
  '铝合金门窗\t门窗分包\t平方米\t360.000\t12.000\t348.000\tLL-2026-005\t680.00\t680.00\t236640.00\t236640.00',
  '合计\t—\t—\t5180.000\t76.000\t5104.000\t\t\t\t1296080.00\t1296080.00',
].join('\n');

const TOL = 0.01;        // 金额容差：分
const TOL_Q = 0.005;     // 数量容差：千分位（台账数量一般保留 3 位小数）

// ⚠️ 角色顺序 = 匹配优先级：**更具体的词必须排在更宽泛的前面**（本仓库踩过两次的坑，
//    见 tools/header_map_check.py）。这里的关键次序：
//    「领用单号」要在「领用数量」前；「结算抵扣金额」要在「领用金额」前；
//    「合同单价」要在「单价」前；「进场数量 / 退库数量 / 领用数量」要在任何宽泛的「数量」前。
const ROLES = {
  orderNo: ['领用单号', '领料单号', '领料单', '单据号'],
  deduction: ['结算抵扣金额', '结算抵扣', '甲供材抵扣', '甲供抵扣', '抵扣金额'],
  amount: ['领用金额', '领料金额', '材料金额', '金额'],
  contractPrice: ['合同单价', '合同价', '约定单价', '合同价格'],
  price: ['单价'],
  received: ['进场数量', '进场', '到货数量', '验收数量', '入库数量'],
  returned: ['退库数量', '退库', '退还数量', '退回数量'],
  issued: ['领用数量', '领料数量', '实领数量', '领用'],
  material: ['材料名称', '材料编码', '材料', '品名'],
  sub: ['分包单位', '分包商', '分包'],
  unit: ['单位', '计量单位'],
};

const LABELS = {
  material: '材料名称', sub: '分包单位', unit: '单位',
  received: '进场数量', returned: '退库数量', issued: '领用数量', orderNo: '领用单号',
  price: '单价', contractPrice: '合同单价', amount: '领用金额', deduction: '结算抵扣金额',
};

const REQUIRED = ['material', 'sub', 'received', 'returned', 'issued', 'price', 'amount', 'deduction'];
const SUM_ROLES = ['received', 'returned', 'issued', 'amount', 'deduction'];
const QTY_ROLES = ['received', 'returned', 'issued'];
const MONEY_ROLES = ['price', 'amount', 'deduction'];

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
const round3 = (n) => Math.round(n * 1000) / 1000;

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
const qty = (it, role) => normNumber(it.byRole[role]);

function who(it) {
  const sub = String(it.byRole.sub || '').trim() || '(未填分包单位)';
  const mat = String(it.byRole.material || '').trim() || '(未填材料名称)';
  return `第 ${it.line} 行 分包单位「${sub}」的材料「${mat}」`;
}

/* ---------- 免费层：逐行复算 + 合计勾稽 + 重复 / 空缺 / 负值 ---------- */

function checkIssuedQty(it) {
  const received = qty(it, 'received');
  const returned = qty(it, 'returned');
  const issued = qty(it, 'issued');
  if (received === null || returned === null || issued === null) return null;
  const expect = round3(received - returned);
  if (Math.abs(expect - issued) <= TOL_Q) return null;
  return {
    level: 'P0', category: '领用数量与复算不符', line: it.line,
    message: `${who(it)}的领用数量是 ${issued}，按 进场数量 ${received} − 退库数量 ${returned} = ${expect}，应为 ${expect}。`,
    advice: '领用数量是结算抵扣的基数：领多了要按合同扣款，领少了甲方就少抵扣，两种都要拿领用单说清。',
  };
}

function checkIssuedAmount(it) {
  const issued = qty(it, 'issued');
  const price = num(it, 'price');
  const amount = num(it, 'amount');
  if (issued === null || price === null || amount === null) return null;
  const expect = round2(issued * price);
  if (Math.abs(expect - amount) <= TOL) return null;
  return {
    level: 'P0', category: '领用金额与复算不符', line: it.line,
    message: `${who(it)}的领用金额是 ${amount.toFixed(2)}，按 领用数量 ${issued} × 单价 ${price.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '领用金额是抵扣与超领扣款的基数，这一格错了后面每一格都跟着错。',
  };
}

function checkDeductionMatch(it) {
  const amount = num(it, 'amount');
  const deduction = num(it, 'deduction');
  if (amount === null || deduction === null) return null;
  if (Math.abs(amount - deduction) <= TOL) return null;
  return {
    level: 'P0', category: '结算抵扣金额与领用金额不符', line: it.line,
    message: `${who(it)}的结算抵扣金额是 ${deduction.toFixed(2)}，而领用金额是 ${amount.toFixed(2)}，`
      + `相差 ${round2(deduction - amount).toFixed(2)}。`,
    advice: '甲供材抵扣必须与分包领用金额对得上：少扣是甲方材料款没收回来，多扣是占了分包的钱。',
  };
}

function checkTotalColumn(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const isQtyRole = QTY_ROLES.indexOf(role) >= 0;
    const rd = isQtyRole ? round3 : round2;
    const sum = rd(items.reduce((s, it) => {
      const n = num(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    const tol = isQtyRole ? TOL_Q : TOL;
    if (Math.abs(sum - stated) > tol) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `第 ${t.line} 行 合计行的「${LABELS[role]}」是 ${stated}，各明细行相加是 ${sum}，相差 ${rd(stated - sum)}。`,
        advice: '要么明细行漏了材料 / 分包，要么合计行没跟着更新；抵扣金额就是按合计走的。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const sub = String(it.byRole.sub || '').trim();
    const mat = String(it.byRole.material || '').trim();
    if (!sub && !mat) continue;
    const key = `${sub}||${mat}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一分包单位的同一材料出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现过同样的「分包单位 + 材料名称」，第 ${it.line} 行再次出现。`,
        advice: '同一材料分批进场是正常的，但要按批次分行并各自带领用单号；若两行是同一笔，抵扣与领用会一起翻倍。',
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
    for (const role of REQUIRED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这一行的账就算不出来；补齐前本工具不会用 0 或默认值替你填（退库为 0 也要显式写 0）。',
        });
      }
    }
  }
  return out;
}

function checkNegatives(items) {
  const out = [];
  for (const it of items) {
    for (const role of QTY_ROLES.concat(MONEY_ROLES)) {
      const v = num(it, role);
      if (v === null) continue;
      if (v >= -TOL) continue;
      out.push({
        level: 'P0', category: '数量或金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v}，为负数。`,
        advice: '负的进场 / 领用 / 单价 / 金额只会是填错或符号写反：台账里不存在"负数领用"。',
      });
    }
  }
  return out;
}

/* ---------- 完整档追加：超领与扣款判定（免费档不含这些实现） ---------- */

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的甲供材台账（要能认出「材料名称」「分包单位」「进场数量」「退库数量」'
      + '「领用数量」「单价」「领用金额」「结算抵扣金额」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从甲供材台账 / 领用汇总表导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一行甲供材明细行（不能只有合计行）']);

  const findings = [];
  const notRun = [];
  const actions = [];

  for (const it of t.items) {
    const a = checkIssuedQty(it); if (a) findings.push(a);
    const b = checkIssuedAmount(it); if (b) findings.push(b);
    const c = checkDeductionMatch(it); if (c) findings.push(c);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalColumn(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  for (const f of checkNegatives(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const sumQty = (role) => round3(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const summary = {
    rows: t.items.length,
    total: findings.length,
    p0: findings.filter((f) => f.level === 'P0').length,
    p1: findings.filter((f) => f.level === 'P1').length,
    p2: findings.filter((f) => f.level === 'P2').length,
    received_total: sumQty('received'),
    returned_total: sumQty('returned'),
    issued_total: sumQty('issued'),
    amount_total: sumOf('amount'),
    deduction_total: sumOf('deduction'),
    basis: '领用数量 = 进场数量 − 退库数量；领用金额 = 领用数量 × 单价；结算抵扣金额 = 领用金额；'
      + '合计行逐列复核（进场 / 退库 / 领用数量、领用金额、结算抵扣金额）。',
  };

  const scope = {
    tier: 'free',
    rows: t.items.length,
    amount_total: summary.amount_total,
    deduction_total: summary.deduction_total,
    checks_run: CHECKS_GIVEN,
    checks_not_run: notRun,
  };
  scope.withheld = CHECKS_WITHHELD;

  const result = {
    findings,
    actions,
    summary,
    scope,
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对**，'
      + '不代表材料单价合理、也不代表超领扣款条款该怎么执行 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, round3, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, ROLES, REQUIRED, SUM_ROLES, TOL, TOL_Q,
};
