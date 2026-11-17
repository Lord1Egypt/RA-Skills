'use strict';
/**
 * piece-rate-wage-check.js —— 计件工资与工序单价核对（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须做这件事：**有计件工的企业（制造 / 服装 / 电子组装）每个月发薪前**
 * 都要把计件工资表核一遍 —— 工序单价 × 合格数量对不对、返工与报废扣款有没有重复扣、
 * 低于保底的人补差补了没有、应付计件工资与考勤/产量记录对不对得上。
 * 这三个错是发薪日最容易引发劳资纠纷的地方：**单价用错档、返工扣款重复扣、
 * 合格数与产量记录不符** —— 员工第一时间就会来问，钱发出去就很难追回。
 *
 * 与已有能力的区别（**这条必须写清楚，否则就是重复品**）：
 *   `payroll-check`（工资表发放前核对）核的是工资表的**个税 / 社保 / 合计口径**这一层
 *   （实发 = 应发 − 扣款、个税按累计预扣税率表）；
 *   本能力核的是**计件产量 × 工序单价**这一层（计件工资、返工/报废扣款、保底补差、应付计件工资）。
 *   两者层面不同，可以在同一个月里各跑一遍。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * 不发起任何网络请求（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   计件工资       = 合格数量 × 工序单价
 *   净计件工资     = 计件工资 − 返工扣款 − 报废扣款
 *   应付计件工资   = 净计件工资 + 保底补差 + 加班补差
 *   保底补差       = max(0, 保底工资 − 净计件工资)        ← 低于保底要补、高于保底不补
 *   可计数量       = 产量 − 返工数量 − 报废数量            ← 产量记录勾稽口径
 *
 * 口径（写进结果里，第三方可用同一份输入复算）：
 *   · 金额容差 0.01 元，数量容差 0.02；
 *   · 表里没有的扣款/补差列按 0 参与应付勾稽，并在 scope.missing_columns 里如实列出；
 *   · 扣款与补差一律按**票面填写的金额**参与勾稽 —— 本工具不规定扣款标准。
 *
 * 本包执行 7 项；订阅版追加 5 项（见 CHECKS_WITHHELD）：
 *   工序单价档归因 + 保底补差复算 + 返工/报废重复扣 + 产量记录不平，
 *   并把「发薪前必须先处理哪些人、差多少钱」做成一张按差额排序的处理清单。
 * 材料不足时**绝不给结论**。
 * 调用契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 不给劳动法或薪酬合规意见，只核这张表内部可算的关系。
 */

const CHECKS_GIVEN = [
  '计件工资复算（合格数量 × 工序单价）',
  '应付计件工资勾稽（计件工资 − 返工扣款 − 报废扣款 + 保底补差 + 加班补差）',
  '合格数量超过产量检测',
  '负值检测（数量 / 单价 / 金额 / 扣款 / 补差）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '同一员工同一工序重复行检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '工序单价与工序标准单价不符检测（标准单价取 payload.std_rates，未提供时取同一工序多数行所用单价）',
  '保底补差复算（保底补差 = 保底工资 − 净计件工资，低于保底要补、高于保底不补）',
  '返工 / 报废扣款重复扣检测（扣款折合数量超过这一行的不合格数量）',
  '计件工资与产量记录不平检测（产量 − 返工数量 − 报废数量 ≠ 合格数量）',
  '发薪前必须处理清单与差异归因（按差额从大到小排序，逐条带员工 / 工序行号、建议动作与归因口径）',
];

const OUT_OF_SCOPE = [
  '判断工序单价、保底工资、加班补差该定多少（那是劳动合同、集体协议与公司薪酬制度的事）',
  '判断返工/报废扣款该不该扣、该扣多少（那是质检与公司制度的事；本工具只核票面金额之间的算术关系）',
  '核考勤工时与加班费是否符合劳动法（不核工时合规，也不给法律意见）',
  '把这张表与银行代发流水、个税申报表、考勤系统做跨系统核对（本工具只核这一张表内部的勾稽）',
  '读取 .xlsx 或考勤/ERP 系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '员工\t小组\t工序\t工序单价\t产量\t合格数量\t返工数量\t报废数量\t计件工资\t返工扣款\t报废扣款\t保底工资\t保底补差\t加班补差\t应付计件工资',
  '张美玲\t一组\t锁边\t1.20\t1200\t1150\t30\t20\t1380.00\t36.00\t24.00\t1500.00\t180.00\t0.00\t1500.00',
  '张美玲\t一组\t车缝\t0.85\t2400\t2320\t50\t30\t1972.00\t42.50\t25.50\t1500.00\t0.00\t0.00\t1904.00',
  '李建国\t二组\t锁边\t1.20\t1500\t1450\t35\t15\t1740.00\t42.00\t18.00\t1500.00\t0.00\t120.00\t1800.00',
  '李建国\t二组\t包装\t0.45\t3600\t3500\t60\t40\t1575.00\t27.00\t18.00\t1500.00\t0.00\t0.00\t1530.00',
  '王秀兰\t二组\t车缝\t0.85\t900\t860\t25\t15\t731.00\t21.25\t12.75\t1500.00\t803.00\t0.00\t1500.00',
  '王秀兰\t二组\t包装\t0.45\t1600\t1550\t30\t20\t697.50\t13.50\t9.00\t1500.00\t825.00\t0.00\t1500.00',
  '合计\t\t\t\t11200\t10830\t230\t140\t8095.50\t182.25\t107.25\t\t1808.00\t120.00\t9734.00',
].join('\n');

const TOL = 0.01;       // 金额容差
const QTY_TOL = 0.02;   // 数量容差

const ROLES = {
  // ⚠️ 顺序即优先级，更具体的别名必须排在更宽泛的前面（本仓库踩过两次的坑，见 tools/header_map_check.py）：
  //    「工序单价」要在「工序」之前（否则单价列会被工序列抢走）；
  //    「应付计件工资」要在「计件工资」之前；「保底补差」要在「保底工资」之前。
  worker: ['员工姓名', '员工', '姓名', '工人', '人员'],
  team: ['小组', '班组', '组别', '分组'],
  rate: ['工序单价', '计件单价', '单价'],
  process: ['工序名称', '工序编号', '工序号', '工序'],
  qtyOk: ['合格数量', '合格数', '良品数', '合格品数'],
  qtyOut: ['产量', '生产数量', '完成数量', '投产数量', '送检数量'],
  reworkQty: ['返工数量', '返工数'],
  scrapQty: ['报废数量', '报废数', '废品数量'],
  payable: ['应付计件工资', '应付工资', '应付金额', '实付计件工资'],
  makeUp: ['保底补差', '保底差额', '保底补足'],
  guarantee: ['保底工资', '保底标准', '保底线', '最低工资', '保底'],
  overtime: ['加班补差', '加班补贴', '加班补'],
  amount: ['计件工资', '计件金额', '计件收入'],
  reworkDeduct: ['返工扣款', '返工扣减', '返工扣'],
  scrapDeduct: ['报废扣款', '报废扣减', '报废扣'],
};

const LABELS = {
  worker: '员工', team: '小组', rate: '工序单价', process: '工序',
  qtyOk: '合格数量', qtyOut: '产量', reworkQty: '返工数量', scrapQty: '报废数量',
  amount: '计件工资', payable: '应付计件工资', reworkDeduct: '返工扣款',
  scrapDeduct: '报废扣款', guarantee: '保底工资', makeUp: '保底补差', overtime: '加班补差',
};

const REQUIRED = ['worker', 'process', 'rate', 'qtyOk', 'amount', 'payable'];
const NUMERIC_ROLES = ['rate', 'qtyOut', 'qtyOk', 'reworkQty', 'scrapQty', 'amount',
  'reworkDeduct', 'scrapDeduct', 'guarantee', 'makeUp', 'overtime', 'payable'];
const SUM_ROLES = ['qtyOut', 'qtyOk', 'reworkQty', 'scrapQty', 'amount',
  'reworkDeduct', 'scrapDeduct', 'makeUp', 'overtime', 'payable'];
const OPTIONAL_COLUMNS = ['team', 'qtyOut', 'reworkQty', 'scrapQty', 'reworkDeduct',
  'scrapDeduct', 'guarantee', 'makeUp', 'overtime'];

const TOTAL_WORDS = /^(合计|总计|小计|共计|汇总|total)/i;
const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a|无|略)$/i;

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
const str = (v) => String(v === undefined || v === null ? '' : v).trim();

function parseTable(text) {
  const raw = String(text === null || text === undefined ? '' : text)
    .split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { error: 'empty' };
  const headers = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const missing = REQUIRED.filter((r) => !headers.some((c) => c.role === r));
  if (missing.length) return { error: 'no_header', missingColumns: missing.map((r) => LABELS[r]) };
  const has = {};
  for (const c of headers) if (c.role) has[c.role] = true;
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], has: has };
    headers.forEach((c, idx) => {
      if (c.role && row[c.role] === undefined) row[c.role] = cells[idx] === undefined ? '' : cells[idx];
    });
    if (TOTAL_WORDS.test(str(cells[0]))) { row.isTotal = true; totals.push(row); } else { items.push(row); }
  }
  return { headers, items, totals, has };
}

const numOf = (it, role) => normNumber(it[role]);

/**
 * 金额类取值：
 *   · 表里**根本没有这一列** ⇒ 返回 0（按"没有这项扣款/补差"参与勾稽，并在 scope.missing_columns 里写明）；
 *   · 列存在但这一格**空白或占位符** ⇒ 返回 null（这一行跳过勾稽，由空白检测负责报出来）。
 * 绝不把"空格子"当 0 —— 那会把数据缺口悄悄算成一个结论。
 */
function moneyOf(it, role) {
  if (!it.has || !it.has[role]) return 0;
  return normNumber(it[role]);
}

const who = (it) => `员工「${str(it.worker) || '(未填姓名)'}」的工序「${str(it.process) || '(未填工序)'}」（第 ${it.line} 行）`;
const whoRow = (it) => ({ worker: str(it.worker), process: str(it.process) });

/* ------------------------------- 本包检查 ------------------------------- */

function checkPieceWage(it) {
  const qty = numOf(it, 'qtyOk');
  const rate = numOf(it, 'rate');
  const stated = numOf(it, 'amount');
  if (qty === null || rate === null || stated === null) return null;
  const expect = round2(qty * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  const diff = round2(stated - expect);
  return {
    level: 'P0', category: '计件工资与复算不符', line: it.line, impact: diff, ...whoRow(it),
    message: `${who(it)}：票面计件工资 ${stated.toFixed(2)}，按 合格数量 ${qty} × 工序单价 ${rate.toFixed(2)} 应为 ${expect.toFixed(2)}（相差 ${diff.toFixed(2)}）。`,
    advice: '按 合格数量 × 工序单价 重算这一行：先确认是数量录错、还是单价用错档；重算后才轮到应付计件工资。',
    evidence: [it.raw],
  };
}

function checkPayable(it) {
  const amount = numOf(it, 'amount');
  const payable = numOf(it, 'payable');
  const rw = moneyOf(it, 'reworkDeduct');
  const sc = moneyOf(it, 'scrapDeduct');
  const mk = moneyOf(it, 'makeUp');
  const ot = moneyOf(it, 'overtime');
  if ([amount, payable, rw, sc, mk, ot].some((v) => v === null)) return null;
  const expect = round2(amount - rw - sc + mk + ot);
  if (Math.abs(expect - payable) <= TOL) return null;
  const diff = round2(payable - expect);
  return {
    level: 'P0', category: '应付计件工资与复算不符', line: it.line, impact: diff, ...whoRow(it),
    message: `${who(it)}：票面应付计件工资 ${payable.toFixed(2)}，按 计件工资 ${amount.toFixed(2)} − 返工扣款 ${rw.toFixed(2)} `
      + `− 报废扣款 ${sc.toFixed(2)} + 保底补差 ${mk.toFixed(2)} + 加班补差 ${ot.toFixed(2)} 应为 ${expect.toFixed(2)}（相差 ${diff.toFixed(2)}）。`,
    advice: '应付计件工资就是发出去的钱：按这条算式重算，多发就在发薪前调整，少发要补。',
    evidence: [it.raw],
  };
}

function checkQtyOverOutput(it) {
  if (!it.has || !it.has.qtyOut) return null;
  const ok = numOf(it, 'qtyOk');
  const out = numOf(it, 'qtyOut');
  if (ok === null || out === null) return null;
  if (ok <= out + QTY_TOL) return null;
  const rate = numOf(it, 'rate');
  return {
    level: 'P0', category: '合格数量超过产量', line: it.line,
    impact: rate === null ? null : round2((ok - out) * rate), ...whoRow(it),
    message: `${who(it)}：合格数量 ${ok} 大于产量 ${out}（多 ${round2(ok - out)} 件）。`,
    advice: '合格数不可能多于产量：先核对该员工的产量记录与质检记录，确认这两个数各自的口径。',
    evidence: [it.raw],
  };
}

function checkNegative(it) {
  const out = [];
  for (const role of NUMERIC_ROLES) {
    if (!it.has || !it.has[role]) continue;
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P1', category: '出现负值', line: it.line, impact: null, ...whoRow(it),
      message: `${who(it)}：「${LABELS[role]}」填的是 ${v}（负数）。`,
      advice: '数量、单价、扣款、补差为负通常是录错符号；发薪前改正，否则应付计件工资会反向。',
      evidence: [it.raw],
    });
  }
  return out;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  const label = LABELS[role] || role;
  for (const t of totals) {
    const stated = numOf(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = numOf(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: t.line,
      impact: round2(stated - sum), worker: '(合计行)', process: '',
      message: `合计行的「${label}」写的是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}（相差 ${round2(stated - sum).toFixed(2)}）。`,
      advice: '合计行没跟着更新（或明细漏行）：重算合计；计件工资总额错了，发放总额就跟着错。',
      evidence: [t.raw, `${items.length} 行明细`],
    });
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const w = str(it.worker).replace(/\s/g, '');
    if (!w) continue;
    const key = `${w}|${str(it.process).replace(/\s/g, '')}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一员工同一工序出现多行', line: it.line, impact: null, ...whoRow(it),
        message: `员工「${str(it.worker)}」的工序「${str(it.process)}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '确认是否重复录入：同一员工同一工序重复计酬，计件工资与扣款会一起翻倍。',
        evidence: [it.raw],
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
      const s = str(it[role]);
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line, impact: null, ...whoRow(it),
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这一行的计件工资就算不出来；补齐前本工具不会用 0 或默认值替你填。',
          evidence: [it.raw],
        });
      }
    }
  }
  return out;
}

/* ===== 以下为订阅版才执行的检查 ===== */
/* 这一整段（到 function run 之前）会被 tools/strip_free_engine.py 整块摘掉，免费包里不留残渣：
   checkRateTier / checkMakeUp / checkDoubleDeduct / checkProductionBalance 这四个追加检查、
   buildRateStandard（工序标准单价）、buildAttribution（差异归因）、buildPayrollActions（发薪前处理清单）。
   位置必须在**免费检查之后**：形态 A 是"从 MARKER 删到 function run"，放在免费检查之前会把免费档也删掉。 */

/**
 * 每个工序的「标准单价」：
 *   · 优先用 payload.std_rates（{"锁边":"1.20"} 这种，公司自己的工序价目表）；
 *   · 没给就取**同一工序在表里多数行所用的那个单价**（并列时取金额较大的那档），
 *     这正是"同一道工序在表里出现了两个单价档"这一最常见的错。
 */
function buildRateStandard(items, stdRates) {
  const byProcess = new Map();
  for (const it of items) {
    const p = str(it.process);
    const r = normNumber(it.rate);
    if (!p || r === null) continue;
    if (!byProcess.has(p)) byProcess.set(p, new Map());
    const m = byProcess.get(p);
    m.set(r, (m.get(r) || 0) + 1);
  }
  const out = new Map();
  for (const [p, m] of byProcess) {
    let best = null;
    for (const [r, cnt] of m) {
      if (best === null || cnt > best.count || (cnt === best.count && r > best.value)) best = { value: r, count: cnt };
    }
    out.set(p, {
      standard: best.value,
      tiers: Array.from(m.keys()).sort((a, b) => a - b),
      rows: best.count,
      source: '表内同一工序多数行所用单价',
    });
  }
  if (stdRates && typeof stdRates === 'object') {
    for (const [p, v] of Object.entries(stdRates)) {
      const n = normNumber(v);
      const key = str(p);
      if (n === null || !key) continue;
      const cur = out.get(key) || { tiers: [], rows: 0 };
      out.set(key, { standard: n, tiers: cur.tiers, rows: cur.rows, source: 'payload.std_rates' });
    }
  }
  return out;
}

function checkRateTier(it, std) {
  const p = str(it.process);
  const rate = numOf(it, 'rate');
  const rec = std && std.get(p);
  if (!rec || rate === null) return null;
  if (Math.abs(rate - rec.standard) <= TOL) return null;
  const qty = numOf(it, 'qtyOk');
  const impact = qty === null ? null : round2((rate - rec.standard) * qty);
  return {
    level: 'P1', category: '工序单价与工序标准单价不符', line: it.line, impact: impact, ...whoRow(it),
    message: `${who(it)}：工序单价 ${rate.toFixed(2)}，该工序的标准单价是 ${rec.standard.toFixed(2)}`
      + `（来源：${rec.source}；这道工序在表里出现过 ${rec.tiers.join(' / ')} 档）`
      + (impact === null ? '。' : `，按合格数量 ${qty} 折算差额 ${impact.toFixed(2)}。`),
    advice: '与工序标准单价核对：确认是本月调价（要有审批依据）还是填错档；按正确单价重算这一行的计件工资与应付。',
    evidence: [it.raw, `标准单价来源：${rec.source}`],
  };
}

function checkMakeUp(it) {
  const guarantee = numOf(it, 'guarantee');
  const amount = numOf(it, 'amount');
  const mk = numOf(it, 'makeUp');
  const rw = moneyOf(it, 'reworkDeduct');
  const sc = moneyOf(it, 'scrapDeduct');
  if (guarantee === null || amount === null || mk === null || rw === null || sc === null) return null;
  const net = round2(amount - rw - sc);
  const expect = round2(Math.max(0, guarantee - net));
  if (Math.abs(expect - mk) <= TOL) return null;
  return {
    level: 'P1', category: '保底补差与复算不符', line: it.line, impact: round2(mk - expect), ...whoRow(it),
    message: `${who(it)}：票面保底补差 ${mk.toFixed(2)}，按 保底工资 ${guarantee.toFixed(2)} − 净计件工资`
      + `（计件工资 ${amount.toFixed(2)} − 返工扣款 ${rw.toFixed(2)} − 报废扣款 ${sc.toFixed(2)} = ${net.toFixed(2)}）`
      + `应为 ${expect.toFixed(2)}。`,
    advice: '低于保底要补、高于保底不补：按这条算式重算补差，少了员工会来找，多了是白发的钱。',
    evidence: [it.raw],
  };
}

function checkDoubleDeduct(it) {
  if (!it.has || (!it.has.reworkDeduct && !it.has.scrapDeduct) || !it.has.qtyOut) return null;
  const rate = numOf(it, 'rate');
  const ok = numOf(it, 'qtyOk');
  const out = numOf(it, 'qtyOut');
  const rw = numOf(it, 'reworkDeduct');
  const sc = numOf(it, 'scrapDeduct');
  if (rate === null || rate <= 0 || ok === null || out === null || rw === null || sc === null) return null;
  const dedQty = (rw + sc) / rate;
  const badQty = out - ok;
  if (dedQty <= badQty + QTY_TOL) return null;
  return {
    level: 'P1', category: '返工或报废扣款重复扣', line: it.line,
    impact: round2((dedQty - badQty) * rate), ...whoRow(it),
    message: `${who(it)}：返工扣款 ${rw.toFixed(2)} + 报废扣款 ${sc.toFixed(2)} 按工序单价 ${rate.toFixed(2)} 折合 ${round2(dedQty)} 件，`
      + `但这一行只有 ${round2(badQty)} 件不合格（产量 ${out} − 合格数量 ${ok}）。`,
    advice: '同一批不合格品不要既算返工又算报废：核对扣款折合数量与不合格数量，重复扣的部分发薪前退回。',
    evidence: [it.raw],
  };
}

function checkProductionBalance(it) {
  if (!it.has || !it.has.qtyOut || !it.has.reworkQty || !it.has.scrapQty) return null;
  const out = numOf(it, 'qtyOut');
  const ok = numOf(it, 'qtyOk');
  const rq = numOf(it, 'reworkQty');
  const sq = numOf(it, 'scrapQty');
  if (out === null || ok === null || rq === null || sq === null) return null;
  const expect = round2(out - rq - sq);
  if (Math.abs(expect - ok) <= QTY_TOL) return null;
  const rate = numOf(it, 'rate');
  const impact = rate === null ? null : round2((ok - expect) * rate);
  return {
    level: 'P1', category: '计件工资与产量记录不平', line: it.line, impact: impact, ...whoRow(it),
    message: `${who(it)}：按产量记录复算 产量 ${out} − 返工数量 ${rq} − 报废数量 ${sq} = ${expect}，`
      + `但这一行的合格数量写的是 ${ok}（相差 ${round2(ok - expect)} 件）`
      + (impact === null ? '。' : `，按工序单价折算 ${impact.toFixed(2)}。`)
      + '计件工资是按合格数量计的，两者不平说明这一行的计酬数量与产量记录对不上。',
    advice: '按 产量 − 返工数量 − 报废数量 重算可计数量，与合格数量对齐后再计酬；不平的行先查质检与工序交接记录。',
    evidence: [it.raw],
  };
}

/** 差异归因：按类别、按员工把差额汇总出来（订阅版独有）。 */
function buildAttribution(findings) {
  const byCategory = {};
  const byWorker = new Map();
  for (const f of findings) {
    const c = byCategory[f.category] || (byCategory[f.category] = { count: 0, amount_diff: 0, lines: [] });
    c.count += 1;
    c.lines.push(f.line);
    if (typeof f.impact === 'number') c.amount_diff = round2(c.amount_diff + f.impact);
    const w = f.worker || '(未填姓名)';
    const rec = byWorker.get(w) || { worker: w, count: 0, amount_diff: 0, lines: [], categories: [] };
    rec.count += 1;
    rec.lines.push(f.line);
    if (typeof f.impact === 'number') rec.amount_diff = round2(rec.amount_diff + f.impact);
    if (rec.categories.indexOf(f.category) < 0) rec.categories.push(f.category);
    byWorker.set(w, rec);
  }
  const workers = Array.from(byWorker.values()).sort((a, b) =>
    (Math.abs(b.amount_diff) - Math.abs(a.amount_diff)) || String(a.worker).localeCompare(String(b.worker)));
  for (const w of workers) w.lines.sort((a, b) => a - b);
  return {
    by_category: byCategory,
    by_worker: workers,
    basis: '差额口径（正数 = 表里多算 / 多发，负数 = 少算 / 少发）：'
      + '金额类 = 票面 − 复算；单价类 = (票面单价 − 标准单价) × 合格数量；'
      + '扣款类 = (扣款折合数量 − 不合格数量) × 工序单价；数量类 = (票面数量 − 复算数量) × 工序单价。',
  };
}

/** 订阅版独有的那一种能力：**发薪前必须处理清单**。
 * 把逐行复算升级成"发薪前先动哪几条"—— 按差额从大到小排，每条都带员工/工序行号与建议动作。
 */
const LEVEL_RANK = { P0: 0, P1: 1, P2: 2 };

function buildPayrollActions(findings) {
  // ⚠️ `LEVEL_RANK['P0']` 是 0，写 `LEVEL_RANK[x] || 9` 会把 P0 当成最低优先级 —— 必须显式判 undefined。
  const rank = (lv) => (Object.prototype.hasOwnProperty.call(LEVEL_RANK, lv) ? LEVEL_RANK[lv] : 9);
  const abs = (f) => (typeof f.impact === 'number' ? Math.abs(f.impact) : -1);
  const list = findings.slice().sort((a, b) =>
    (abs(b) - abs(a)) || (rank(a.level) - rank(b.level)) || (a.line - b.line));
  return list.map((f, i) => ({
    priority: i + 1,
    level: f.level,
    line: f.line,
    worker: f.worker || '',
    process: f.process || '',
    category: f.category,
    amount_diff: typeof f.impact === 'number' ? f.impact : null,
    action: f.advice || '人工复核这一行',
    basis: `第 ${f.line} 行 · 员工 ${f.worker || '(未填姓名)'} · 工序 ${f.process || '(未填工序)'} · ${f.category}`,
    evidence: f.evidence || [],
  }));
}

/* --------------------------------- 主入口 --------------------------------- */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象（收到的是 ${typeof payload}）—— 请用 {"text": "含表头的计件工资表文本"}`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient(['没有收到计件工资表正文（text）—— 请把**含表头**的计件工资表贴进来']);
  }
  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['非空的计件工资表正文']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的计件工资表（要能认出「员工」「工序」「工序单价」「合格数量」「计件工资」「应付计件工资」）',
      `本次没认出来的必需列：${t.missingColumns.join('、')}`,
      '从 Excel 连表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  // ⚠️ 空数组在 JS 里是真值：`if ([])` 会成立 —— 必须判长度。
  if (!t.items.length) {
    return insufficient(['表头下面至少一行的计件明细（员工 × 工序）']);
  }

  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkPieceWage(it); if (a) findings.push(a);
    const b = checkPayable(it); if (b) findings.push(b);
    const c = checkQtyOverOutput(it); if (c) findings.push(c);
    for (const d of checkNegative(it)) findings.push(d);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  if (paid) {
    const rateStd = buildRateStandard(t.items, (payload && payload.std_rates) || null);
    for (const it of t.items) {
      const a = checkRateTier(it, rateStd); if (a) findings.push(a);
      const b = checkMakeUp(it); if (b) findings.push(b);
      const c = checkDoubleDeduct(it); if (c) findings.push(c);
      const d = checkProductionBalance(it); if (d) findings.push(d);
    }
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

  const byLine = (x, y) => (x.line - y.line) || (String(x.category).localeCompare(String(y.category)));
  findings.sort(byLine);

  const summarize = (list) => {
    const q0 = list.filter((f) => f.level === 'P0').length;
    const q1 = list.filter((f) => f.level === 'P1').length;
    const q2 = list.filter((f) => f.level === 'P2').length;
    return {
      rows: t.items.length,
      workers: new Set(t.items.map((it) => str(it.worker)).filter(Boolean)).size,
      processes: new Set(t.items.map((it) => str(it.process)).filter(Boolean)).size,
      total: list.length,
      p0: q0,
      p1: q1,
      p2: q2,
      verdict: q0 > 0 ? 'ERROR_FOUND' : (list.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
    };
  };
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = numOf(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const missingColumns = [];
  for (const role of OPTIONAL_COLUMNS) {
    if (!t.has[role]) missingColumns.push(`「${LABELS[role]}」列（表里没有）`);
  }
  const skipped = [];
  if (!t.has.qtyOut) skipped.push('表里没有「产量」列，因此「合格数量超过产量检测」与产量勾稽未执行');
  if (!t.has.reworkDeduct && !t.has.scrapDeduct) {
    skipped.push('表里没有返工/报废扣款列，因此应付计件工资按 0 扣款勾稽');
  }
  if (!t.totals.length) skipped.push('表里没有合计行，因此「合计行逐列复核」未执行');

  const conventions = [
    '计件工资 = 合格数量 × 工序单价',
    '应付计件工资 = 计件工资 − 返工扣款 − 报废扣款 + 保底补差 + 加班补差',
    `金额容差 ${TOL} 元、数量容差 ${QTY_TOL}`,
    '表里没有的扣款/补差列按 0 参与勾稽（见 missing_columns）；列存在但格子空白 ⇒ 这一行跳过勾稽并单独报出来',
    '扣款与补差一律按票面填写的金额参与勾稽，本工具不规定扣款标准',
  ];
  if (paid) {
    conventions.push('保底补差 = max(0, 保底工资 − 净计件工资)');
    conventions.push('可计数量 = 产量 − 返工数量 − 报废数量（与合格数量比对）');
    conventions.push('工序标准单价：payload.std_rates 优先，否则取同一工序多数行所用单价（并列取金额较大档）');
  }

  let noteText = `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`;
  if (paid) noteText = '完整档执行全部检查项（免费 7 项 + 追加 5 项），并把「发薪前必须先处理哪些人、差多少钱」做成按差额排序的处理清单。';

  const result = {
    service_type: 'PIECE_RATE_WAGE_CHECK',
    tier: paid ? 'full' : 'free',
    scope: {
      checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN.slice(),
      checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      columns: t.headers.map((c) => c.header),
      qty_out_total: sumOf('qtyOut'),
      qty_ok_total: sumOf('qtyOk'),
      rework_qty_total: sumOf('reworkQty'),
      scrap_qty_total: sumOf('scrapQty'),
      amount_total: sumOf('amount'),
      rework_deduct_total: sumOf('reworkDeduct'),
      scrap_deduct_total: sumOf('scrapDeduct'),
      make_up_total: sumOf('makeUp'),
      overtime_total: sumOf('overtime'),
      payable_total: sumOf('payable'),
      conventions: conventions,
      missing_columns: missingColumns,
      skipped_checks: skipped,
      tolerance: TOL,
      qty_tolerance: QTY_TOL,
      executed_locally: true,
      network_used: false,
    },
    findings: findings,
    summary: summarize(findings),
    checks_out_of_scope: OUT_OF_SCOPE,
    note: noteText,
    disclaimer: '只核对这张表内部的算术与勾稽（计件工资、返工/报废扣款、保底补差、应付计件工资、合计）；'
      + '不判断工序单价、保底工资、扣款标准定得合不合理，也不给劳动法或薪酬合规意见。'
      + '每条结论都带原文行号与原文片段，可由第三方用同一份输入和同一口径复算。',
  };

  if (paid) {
    const rateStd = buildRateStandard(t.items, (payload && payload.std_rates) || null);
    result.rate_standard = Array.from(rateStd.entries()).map(([p, v]) => ({
      process: p, standard: v.standard, tiers: v.tiers, rows: v.rows, source: v.source,
    }));
    // 订阅版独有的那一种能力：差异归因 + 发薪前必须处理清单（整体会被 strip_free_engine 摘掉）
    result.attribution = buildAttribution(findings);
    result.payroll_actions = buildPayrollActions(findings);
    result.summary = summarize(findings);
    result.summary.actions = result.payroll_actions.length;
    result.summary.attributed_diff_total = round2(result.payroll_actions
      .reduce((s, a) => s + (typeof a.amount_diff === 'number' ? a.amount_diff : 0), 0));
  }

  if (findings.length === 0) {
    if (paid) {
      result.verdict_note = '本次实际执行的全部检查项都通过了。这只说明这张表按上面写明的口径算得对，'
        + '不代表工序单价、保底工资、扣款标准定得合理 —— 那些不在本工具范围内。';
    } else {
      result.verdict_note = '本次实际执行的免费检查项都通过了。这只说明这张表按免费口径算得对；'
        + '单价档归因、保底补差复算、返工/报废重复扣、产量记录不平与发薪前处理清单这几类检查本次没有执行，'
        + '见 scope.checks_not_run。';
    }
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
  SAMPLE_TEXT, LABELS, ROLES, SUM_ROLES, NUMERIC_ROLES, REQUIRED, TOL, QTY_TOL,
};
