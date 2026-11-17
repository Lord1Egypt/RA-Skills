/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * property-utility-apportionment-check.js —— 物业公共能耗分摊核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每个月出账单之前**。物业公司每月都要把公共区域的水电
 * （公共照明、电梯、水泵、绿化）按面积或户数摊到各业主 / 商户头上，先核一遍再发账单、
 * 再公示。这张表算错，方向只有两个 —— **少摊**（钱收不回来，物业自己贴）或
 * **多摊**（业主在群里截图、拒缴、投诉到街道）。两条都会在催缴单、公示栏和投诉件上暴露出来。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   分摊额     = 公共能耗总额 × 分摊比例（比例列空着时：分摊基数 × 分摊单价）
 *   分摊额合计 = 各组公共能耗总额之和（总额按「期间 + 费用项目」去重，只算一次）
 *   合计行各列 = 明细行相加（公共能耗总额按「期间 + 费用项目」去重后相加）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**公共能耗总额本身真不真实、分摊方式（按面积 / 按户数 / 按人数 / 阶梯）
 *    是否合法有效、空置房该不该优惠、转供电加价是否合规：表里给的总额、基数、单价、比例
 *    一律**以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的档位开关算成一个布尔常量，再把付费检查包进
 *    以该常量为条件的代码块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关 / 条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '分摊额复算（公共能耗总额 × 分摊比例，或 分摊基数 × 分摊单价）',
  '分摊额合计 = 公共能耗总额 复算',
  '合计行逐列复核',
  '同一业主/单元重复行检测',
  '空白与占位符检测',
  '金额或比例为负检测',
];

const CHECKS_WITHHELD = [
  '分摊比例合计不等于 100% 提示',
  '分摊额超过公共能耗总额提示',
  '单价与合同/公示单价不一致提示',
  '空置房未按约定比例分摊提示',
  '同一期间重复分摊提示',
];

const OUT_OF_SCOPE = [
  '判断公共能耗总额本身是否真实、是否把物业自用电（办公室、门岗、广告位）混进了公共能耗（抄表与账务口径以供电 / 供水公司账单和物业账为准）',
  '核对分摊方式（按建筑面积 / 按户数 / 按人数 / 阶梯、以及各业态不同系数）是否符合物业服务合同与管理规约',
  '判断空置房、未售房、开发商产权房、公共部位是否应当分摊以及优惠口径（以合同、地方规定与业委会决议为准）',
  '处理转供电加价、增值税、公共收益冲抵、政府补贴、滞纳金等价格与税务问题',
  '读取物业收费系统 / Excel 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t费用项目\t公共能耗总额\t业主/单元\t分摊基数\t分摊单价\t分摊比例\t分摊额\t公示单价\t是否空置\t空置约定比例',
  '2026-06\t公共照明\t10000.00\t1号楼1单元101\t500.00\t10.00\t50.00%\t5000.00\t10.00\t否\t',
  '2026-06\t公共照明\t10000.00\t1号楼1单元102\t300.00\t10.00\t30.00%\t3000.00\t10.00\t否\t',
  '2026-06\t公共照明\t10000.00\t2号楼2单元201\t200.00\t10.00\t20.00%\t2000.00\t10.00\t否\t',
  '2026-06\t电梯用电\t6000.00\t1号楼1单元101\t250.00\t12.00\t50.00%\t3000.00\t12.00\t否\t',
  '2026-06\t电梯用电\t6000.00\t1号楼1单元102\t150.00\t12.00\t30.00%\t1800.00\t12.00\t否\t',
  '2026-06\t电梯用电\t6000.00\t2号楼2单元201\t100.00\t12.00\t20.00%\t1200.00\t12.00\t否\t',
  '2026-06\t绿化用水\t4000.00\t1号楼1单元101\t250.00\t8.00\t50.00%\t2000.00\t8.00\t否\t',
  '2026-06\t绿化用水\t4000.00\t1号楼1单元102\t150.00\t8.00\t30.00%\t1200.00\t8.00\t否\t',
  '2026-06\t绿化用水\t4000.00\t2号楼2单元201\t100.00\t8.00\t20.00%\t800.00\t8.00\t否\t',
  '合计\t\t20000.00\t\t2000.00\t\t\t20000.00\t\t\t',
].join('\n');

const TOL = 0.01;          // 金额容差：1 分（分摊额复算、合计勾稽）
const PCT_TOL = 0.0005;    // 比例容差：0.05 个百分点（换算成小数后比较）
const PRICE_TOL = 0.01;    // 单价容差：1 分

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前，否则更宽泛的词会把更具体的列**抢走**
  //    （「公示单价」不能被「单价」抢走、「空置约定比例」不能被「比例」也不能被「空置」抢走、
  //      「业主/单元」不能被别的列抢走）—— header_map_check 就是钉这个的。
  period: ['所属期间', '会计期间', '费用期间', '账单期间', '所属期', '期间', '月份', '月度'],
  project: ['费用项目', '能耗项目', '公摊项目', '费用类别', '费用类型', '项目名称', '项目'],
  totalCost: ['公共能耗总额', '公共区域能耗总额', '当期公共能耗总额', '公共能耗金额', '能耗总额', '公摊总额'],
  owner: ['业主/单元', '业主单元', '业主名称', '业主', '商户', '租户', '承租方', '房号', '单元', '铺位'],
  publishedPrice: ['公示单价', '合同约定单价', '合同单价', '备案单价', '公示价'],
  unitPrice: ['分摊单价', '公共能耗单价', '能耗单价', '单价'],
  vacantRatio: ['空置约定比例', '空置分摊比例', '约定空置比例', '空置房分摊比例', '空置比例'],
  ratio: ['分摊比例', '分摊率', '比例'],
  apportioned: ['分摊额', '应分摊金额', '分摊金额', '本期分摊额'],
  base: ['分摊基数', '分摊面积', '建筑面积', '计费面积', '面积', '户数'],
  vacancy: ['是否空置', '空置标识', '空置状态', '房屋状态', '空置'],
};

const LABELS = {
  period: '所属期间', project: '费用项目', totalCost: '公共能耗总额', owner: '业主/单元',
  base: '分摊基数', unitPrice: '分摊单价', ratio: '分摊比例', apportioned: '分摊额',
  publishedPrice: '公示单价', vacancy: '是否空置', vacantRatio: '空置约定比例',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'totalCost', 'owner', 'base', 'unitPrice', 'apportioned'];
/** 合计行里**直接相加**的列 */
const SUM_ROLES = ['base', 'apportioned'];
/** 合计行里**按「期间+费用项目」去重**再加的列（同一总额在每组多行里重复，只算一次） */
const DEDUP_ROLES = ['totalCost'];
/** 免费档负值检测覆盖的列：金额、单价、数量与比例都不该为负 */
const NEGATIVE_ROLES = ['totalCost', 'base', 'unitPrice', 'publishedPrice', 'apportioned', 'ratio'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;
const VACANT_WORDS = /^(是|空置|空置房|已空置|y|yes|true|1)$/i;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
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

/** 比例归一化成小数：`50%` ⇒ 0.5；`0.5` ⇒ 0.5；`50` ⇒ 0.5 */
function ratioValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const num2 = (n) => Number(n).toFixed(2);
const pct2 = (r) => `${(r * 100).toFixed(2)}%`;

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

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const projectKeyOf = (it) => (it && it.project !== undefined ? String(it.project).trim() : '');

const ownerKeyOf = (it) => (it && it.owner !== undefined ? String(it.owner).trim() : '');

/** 分组键 = 所属期间 + 费用项目：公共能耗总额是**这一组**的总额，同一组每行重复填 */
const groupKeyOf = (it) => `${periodKeyOf(it)}|${projectKeyOf(it)}`;

const who = (it) => {
  const parts = [
    it && it.period !== undefined ? String(it.period).trim() : '',
    projectKeyOf(it),
    ownerKeyOf(it),
  ].filter(Boolean).join(' / ');
  return parts ? `${parts}（第 ${it && it.line} 行）` : `第 ${it && it.line} 行`;
};

const groupLabel = (g) => (g.project ? `${g.period}「${g.project}」` : `${g.period}`);

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkApportionRecompute(it, group) {
  const out = [];
  const stated = normNumber(it.apportioned);
  if (stated === null) return out;
  const ratio = ratioValue(it.ratio);
  const total = group && group.total !== null && group.total !== undefined ? group.total : null;
  let expect = null;
  let how = '';
  if (ratio !== null && total !== null) {
    expect = round2(total * ratio);
    how = `公共能耗总额 ${num2(total)} × 分摊比例 ${pct2(ratio)}`;
  } else {
    const base = normNumber(it.base);
    const price = normNumber(it.unitPrice);
    if (base === null || price === null) return out;
    expect = round2(base * price);
    how = `分摊基数 ${num2(base)} × 分摊单价 ${num2(price)}`;
  }
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '分摊额复算不符', line: it.line,
    message: `${who(it)}：${how} = ${num2(expect)}，表里「分摊额」是 ${num2(stated)}，`
      + `相差 ${num2(round2(stated - expect))}。`
      + '分摊额是唯一会进账单的金额：这一格对不上，业主自己拿计算器一按就能算出来，'
      + '要么比例填错，要么金额填错，要么单价没跟着总额调整。',
  });
  return out;
}

function checkAllocationSum(items, groups) {
  const out = [];
  let expected = 0;
  let actual = 0;
  let n = 0;
  let rows = 0;
  let lastLine = null;
  for (const g of groups.values()) {
    if (g.total === null || g.total === undefined) continue;
    expected += g.total;
    n += 1;
    for (const it of g.rows) {
      const v = normNumber(it.apportioned);
      if (v !== null) { actual += v; rows += 1; lastLine = it.line; }
    }
  }
  if (!n || !rows) return out;
  expected = round2(expected);
  actual = round2(actual);
  if (Math.abs(actual - expected) <= TOL) return out;
  out.push({
    level: 'P0', category: '分摊额合计与公共能耗总额不符', line: lastLine,
    message: `本表 ${rows} 行明细的「分摊额」合计 ${num2(actual)}，`
      + `按「期间 + 费用项目」去重后 ${n} 组的「公共能耗总额」合计 ${num2(expected)}，`
      + `相差 ${num2(round2(actual - expected))}（同一总额在每组多行里只算一次）。`
      + '分摊额合计就是向业主公示、也是物业入账的总口径：与总额对不上，说明有能耗没摊下去'
      + '（物业自己贴）或者摊重了（多收业主的钱）。',
  });
  return out;
}

function checkTotalRow(totals, items, groups) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
    if (!n) continue;
    const expect = round2(sum);
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${num2(stated)}，本表 ${n} 行明细相加是 ${num2(expect)}，`
        + `相差 ${num2(round2(stated - expect))}。合计行就是公示与入账的取数口径，对不上说明有一边错。`,
    });
  }
  for (const role of DEDUP_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let expect = null;
    let n = 0;
    for (const g of groups.values()) {
      if (g.total === null || g.total === undefined) continue;
      expect = (expect === null ? 0 : expect) + g.total;
      n += 1;
    }
    if (expect === null || !n) continue;
    expect = round2(expect);
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${num2(stated)}，`
        + `按「期间 + 费用项目」去重后 ${n} 组的「${LABELS[role]}」相加是 ${num2(expect)}，`
        + `相差 ${num2(round2(stated - expect))}。`
        + '同一组多行重复填的同一个总额不能重复加总（否则总额会被放大成倍数）。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const o = ownerKeyOf(it);
    if (!o) continue;
    const key = `${groupKeyOf(it)}|${o}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一业主/单元重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行同一期间、同一费用项目、`
          + '同一业主/单元又出现一次 —— 要么是整行被复制粘贴重复了，要么是同一户被拆成两行'
          + '（比如既有"分摊"行又补了一行"调整"行）。多出来的那一行会把这一户的分摊额重复计一遍。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查'
            + '（公共能耗总额请在每组每一行都填上，合并单元格先取消合并再复制）。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = role === 'ratio' ? ratioValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = role === 'ratio' ? pct2(v) : num2(v);
    out.push({
      level: 'P0', category: '金额或比例为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 总额、基数、单价与比例都不该为负，`
        + '红字冲减 / 退补应单独列一行并在备注里说明，不能直接在本期分摊行里填负数。',
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 同一期间里两个不同的「费用项目」组，把同一笔钱按同一批业主、同样的金额又摊了一遍 */
function groupItems(items) {
  const m = new Map();
  for (const it of items) {
    const k = groupKeyOf(it);
    if (!m.has(k)) {
      m.set(k, {
        key: k, period: periodKeyOf(it), project: projectKeyOf(it),
        rows: [], total: null, totalLine: null,
      });
    }
    const g = m.get(k);
    g.rows.push(it);
    if (g.total === null) {
      const v = normNumber(it.totalCost);
      if (v !== null) { g.total = v; g.totalLine = it.line; }
    }
  }
  return m;
}

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到物业公共能耗分摊核对表正文（text）—— 请把「所属期间 / 费用项目 / 公共能耗总额 / 业主单元 / 分摊基数 / 分摊单价 / 分摊比例 / 分摊额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `物业公共能耗分摊核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何分摊明细行');
  }

  const groups = groupItems(t.items);
  const periods = new Set();
  for (const it of t.items) periods.add(periodKeyOf(it));

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkApportionRecompute(it, groups.get(groupKeyOf(it))));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkAllocationSum(t.items, groups));
  findings.push(...checkTotalRow(t.totals, t.items, groups));
  findings.push(...checkDuplicates(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let apportionedTotal = 0;
  for (const it of t.items) {
    const v = normNumber(it.apportioned);
    if (v !== null) apportionedTotal += v;
  }
  let utilityTotal = 0;
  let groupsWithTotal = 0;
  for (const g of groups.values()) {
    if (g.total === null) continue;
    utilityTotal += g.total;
    groupsWithTotal += 1;
  }

  const result = {
    status: 'success',
    service_type: 'PROPERTY_UTILITY_APPORTIONMENT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      groups: groups.size,
      groups_with_total: groupsWithTotal,
      totals_row: Boolean(t.totals && t.totals.row),
      apportioned_total: round2(apportionedTotal),
      utility_total: round2(utilityTotal),
      tolerance: TOL,
      ratio_tolerance: PCT_TOL,
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
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"公共能耗总额 × 分摊比例 = 分摊额""各组公共能耗总额之和 = 分摊额合计"这类**表内勾稽**'
      + '与档位提示，**不判断总额本身真不真实、分摊方式是否合法有效、空置房该不该优惠**'
      + '（以物业服务合同、管理规约、地方规定与业委会决议为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
