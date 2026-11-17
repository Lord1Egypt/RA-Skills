/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * drg-settlement-check.js —— 医保结算清单与 DRG 入组核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**医院医保办每个月**。DRG/DIP 付费下，医保结算清单（连同病案首页）
 * 上传前必须把这张表核一遍：主要诊断 / 手术操作 / 费用明细要与 DRG 入组结果、结算金额对得上。
 * 这张表算错，方向只有两个 —— **医保拒付**（医院垫的钱拿不回来）或**医院亏损**
 * （按错的权重组结算，或者未入组被按最低档清算）。两条都会在月度清算、医保局审核
 * 与等级评审上暴露出来。
 *
 * 好消息是：钱的部分每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   个人自付   = 费用总额 − 医保支付金额      （等价：医保支付金额 = 费用总额 − 个人自付）
 *   合计行各列 = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**主要诊断选得对不对、手术操作有没有漏填、DRG 分组结果本身对不对、
 *    权重与支付标准是否符合本地政策（那些属于病案编码、分组器与医保政策判断）：
 *    表里的主要诊断、手术操作、DRG 组代码、权重、支付标准一律**以你填的为准**，
 *    本工具只核表内勾稽与档位提示，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，再把付费检查包进
 *    以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER ——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '个人自付复算（费用总额 − 医保支付金额 = 个人自付）',
  '医保支付金额复算（费用总额 − 个人自付 = 医保支付金额；与上式双向勾稽，同一笔差异只报一条）',
  '合计行逐列复核',
  '同一病历号重复行检测',
  '空白与占位符检测',
  '金额或权重为负检测',
];

const CHECKS_WITHHELD = [
  'DRG 组代码为空或含占位符提示（未入组）',
  '权重超出参考区间（0~10）提示',
  '医保支付金额大于费用总额提示',
  '同一病历号重复入组提示',
  '高低倍率病例（费用总额偏离 DRG 支付标准 ±50%）提示',
];

const OUT_OF_SCOPE = [
  '判断主要诊断选得对不对、手术操作有没有漏填（主诊断选择规则与手术操作填报规范属于病案编码与临床判断，请找病案室 / 医保办）',
  '判断 DRG 分组结果本身对不对（分组器版本、ADRG/DRG 入组规则、并发症与合并症的认定属于分组器与本地医保政策）',
  '判断权重、费率与 DRG 支付标准是否符合本地政策（权重表与费率每年调整，以医保局公布口径为准）',
  '处理 DIP 付费、按项目付费、特病单议、异地就医与基金监管口径之间的差异',
  '判断高倍率 / 低倍率病例该按什么规则结算（本工具只提示"偏离了"，结算口径以本地政策为准）',
  '读取 HIS / 病案系统 / 医保结算系统导出的文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '结算期间\t病历号\t主要诊断编码\t主要诊断名称\t手术操作编码\t手术操作名称\tDRG组代码\tDRG组名称\t权重\tDRG支付标准\t费用总额\t医保支付金额\t个人自付\t个人自费',
  '2026-01\tZY2026001\tI50.900\t心力衰竭\t无\t无\tFR29\t心力衰竭组\t0.8654\t8500.00\t9000.00\t6300.00\t2700.00\t300.00',
  '2026-01\tZY2026002\tJ18.900\t肺炎\t无\t无\tES15\t呼吸系统感染组\t1.2345\t9600.00\t10200.00\t7140.00\t3060.00\t0.00',
  '2026-02\tZY2026003\tK35.900\t急性阑尾炎\t47.0900\t阑尾切除术\tGK29\t阑尾切除术组\t1.5678\t12000.00\t12800.00\t8960.00\t3840.00\t0.00',
  '合计\t\t\t\t\t\t\t\t3.6677\t30100.00\t32000.00\t22400.00\t9600.00\t300.00',
].join('\n');

const TOL = 0.01;
const WEIGHT_MIN = 0;         // 权重参考区间下限
const WEIGHT_MAX = 10;        // 权重参考区间上限
const MULTIPLE_TOL = 0.5;     // 高低倍率：费用总额偏离 DRG 支付标准 ±50%

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的别名在前**，裸词兜底放最后。三条硬要求都在这里：
  //    · 「DRG组代码」必须排在裸「代码」前（病组代码不能被别的"…代码"列抢走）；
  //    · 「医保支付金额」「结算金额」必须排在裸「金额」前（否则医保支付金额会被当成费用总额）；
  //    · 「费用总额」必须排在裸「总额」前；「主要诊断编码」必须排在「主要诊断」前；
  //    · 「手术操作编码」必须排在裸「手术操作」前；「个人自付」与「个人自费」必须分开（自付≠自费）。
  period: ['结算期间', '结算月份', '费用期间', '住院期间', '所属期间', '所属期', '期间', '月份'],
  caseNo: ['病历号', '病案号', '住院号', '住院流水号', '病例号', '就诊号', '患者编号'],
  mainDiagCode: ['主要诊断编码', '主诊断编码', '主要诊断代码', '主诊断码', '诊断编码', '疾病编码', 'ICD编码'],
  mainDiagName: ['主要诊断名称', '主诊断名称', '主要诊断', '主诊断'],
  procCode: ['手术操作编码', '手术操作代码', '手术编码', '操作编码'],
  procName: ['手术操作名称', '手术及操作名称', '手术操作', '手术名称'],
  drgCode: ['DRG组代码', 'DRG分组代码', 'DRG组别代码', 'DRG代码', '病组代码', '代码'],
  drgName: ['DRG组名称', 'DRG组别名称', 'DRG名称', '病组名称'],
  weight: ['DRG权重', '病组权重', '权重', 'RW'],
  refPay: ['DRG支付标准', 'DRG付费标准', '病组支付标准', '参考支付标准', '支付标准', '基准金额', '参考金额'],
  insurancePay: ['医保支付金额', '医保基金支付金额', '医保统筹支付金额', '基金支付金额', '统筹支付金额', '医保结算金额', '结算金额', '医保支付'],
  selfPay: ['个人自付金额', '个人自付', '自付金额', '患者自付'],
  selfFund: ['个人自费金额', '个人自费', '自费金额', '全自费'],
  totalAmount: ['医疗费用总额', '费用总额', '费用总金额', '住院总费用', '总费用', '费用合计', '总额', '金额'],
};

const LABELS = {
  period: '结算期间', caseNo: '病历号', mainDiagCode: '主要诊断编码', mainDiagName: '主要诊断名称',
  procCode: '手术操作编码', procName: '手术操作名称', drgCode: 'DRG组代码', drgName: 'DRG组名称',
  weight: '权重', refPay: 'DRG支付标准', insurancePay: '医保支付金额', selfPay: '个人自付',
  selfFund: '个人自费', totalAmount: '费用总额',
};

/**
 * 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数）。
 * ⚠️ 刻意**不含** DRG组代码 / 权重 / DRG支付标准 / 手术操作：
 *    · DRG组代码与权重是否为空，是完整档的独立检查项（见 CHECKS_WITHHELD），
 *      放进必需列就等于免费档把付费结论送出去了；
 *    · 无手术病例合法（内科病例手术操作列本来就是空），不设成必需列。
 */
const REQUIRED = ['period', 'caseNo', 'mainDiagCode', 'totalAmount', 'insurancePay', 'selfPay'];
/** 合计行逐列复核的列 */
const SUM_ROLES = ['weight', 'refPay', 'totalAmount', 'insurancePay', 'selfPay', 'selfFund'];
/**
 * 免费档负值检测覆盖的列：费用、支付、自付自费与权重。
 * ⚠️ 负数只按"格子里填的原文"判：由勾稽式**推出来**的个人自付为负（= 医保支付金额大于费用总额）
 *    属于完整档的独立检查项，免费档不在勾稽式里重复下结论。
 */
const NEGATIVE_ROLES = ['totalAmount', 'insurancePay', 'selfPay', 'selfFund', 'refPay', 'weight'];
/** 金额列（两位小数）与权重列（四位小数）的显示口径 */
const MONEY_ROLES = ['totalAmount', 'insurancePay', 'selfPay', 'selfFund', 'refPay'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空|不详)$/i.test(s);
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
const fmt = (role, v) => (MONEY_ROLES.indexOf(role) >= 0 ? v.toFixed(2) : v.toFixed(4));

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

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const c = it && it.caseNo !== undefined ? String(it.caseNo).trim() : '';
  return c ? `${p}「${c}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const caseKeyOf = (it) => {
  const c = it && it.caseNo !== undefined ? String(it.caseNo).trim() : '';
  return c || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkSelfPayIdentity(it) {
  const out = [];
  const total = normNumber(it.totalAmount);
  if (total === null) return out;
  const pay = normNumber(it.insurancePay);
  const self = normNumber(it.selfPay);
  // 双向勾稽：① 个人自付 = 费用总额 − 医保支付金额；② 医保支付金额 = 费用总额 − 个人自付。
  // 两式代数等价，但"哪一式算得出来"取决于哪些格填了值 —— 两式都算，任一式对不上就报，
  // 且**同一笔差异只报一条**（取一），绝不因为两式同时失败就报两条。
  const derivedSelf = pay === null ? null : round2(total - pay);   // 由①推出的个人自付
  const derivedPay = self === null ? null : round2(total - self);  // 由②推出的医保支付金额
  // 医保支付金额 > 费用总额 ⇒ 推出来的个人自付是负数：这件事本身是「医保支付金额大于费用总额」，
  // 由完整档单独认定（见 CHECKS_WITHHELD）。免费档不在这里重复下结论，也不谎报成勾稽不符。
  if ((derivedSelf !== null && derivedSelf < -TOL) || (derivedPay !== null && derivedPay < -TOL)) return out;
  const badSelf = derivedSelf !== null && self !== null && Math.abs(derivedSelf - self) > TOL;
  const badPay = derivedPay !== null && pay !== null && Math.abs(derivedPay - pay) > TOL;
  if (!badSelf && !badPay) return out;
  const parts = [];
  if (derivedSelf !== null) {
    parts.push(`费用总额 ${total.toFixed(2)} − 医保支付金额 ${pay.toFixed(2)} = ${derivedSelf.toFixed(2)}，`
      + `表里「个人自付」是 ${self === null ? '（空）' : self.toFixed(2)}`);
  }
  if (derivedPay !== null) {
    parts.push(`费用总额 ${total.toFixed(2)} − 个人自付 ${self.toFixed(2)} = ${derivedPay.toFixed(2)}，`
      + `表里「医保支付金额」是 ${pay === null ? '（空）' : pay.toFixed(2)}`);
  }
  out.push({
    level: 'P0', category: '个人自付与医保支付金额勾稽不符', line: it.line,
    message: `${who(it)}：${parts.join('；')}。`
      + '这三格必须闭合：个人自付 = 费用总额 − 医保支付金额（等价于 医保支付金额 = 费用总额 − 个人自付）。'
      + '对不上通常是自付列抄错，或者医保支付金额取错了口径'
      + '（把个人账户支付 / 大病保险 / 医疗救助也算进了基金支付）。'
      + '医保局是按结算清单拨付的，差一分都要追回。',
  });
  return out;
}

function checkTotalRow(totals, items) {
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
    if (Math.abs(stated - sum) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${fmt(role, stated)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 ${fmt(role, sum)}，`
        + `相差 ${fmt(role, stated - sum)}。合计行就是月度清算与医保局拨付的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const c = it.caseNo !== undefined ? String(it.caseNo).trim() : '';
    const p = it.period !== undefined ? String(it.period).trim() : '';
    if (!c || !p) continue;                          // 空病历号 / 空期间由空白检测报，这里跳过
    const key = `${c}|${p}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一病历号重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一病历号、同一结算期间又出现了 —— `
          + '要么是清单重复粘贴了一行，要么是同一份结算被拆成两行（比如按两个险种各建一行）。'
          + '多出来的那一行会把费用、支付金额与权重都重复计一遍，合计与拨付金额永远对不平。',
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
            + '这一列缺失时与它相关的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额或权重为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${fmt(role, v)}（负数）—— 费用、支付金额、自付自费与权重都不该为负；`
        + '冲销 / 红字应在清单外单独说明，不能让负值混进合计。',
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到医保结算清单与 DRG 入组核对表正文（text）—— 请把「结算期间 / 病历号 / 主要诊断编码 / 主要诊断名称 / 手术操作 / DRG组代码 / DRG组名称 / 权重 / DRG支付标准 / 费用总额 / 医保支付金额 / 个人自付 / 个人自费」这张表（含表头）贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `医保结算清单与 DRG 入组核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何病例明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkSelfPayIdentity(it));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicates(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let weightTotal = 0;
  let amountTotal = 0;
  let payTotal = 0;
  for (const it of t.items) {
    const w = normNumber(it.weight);
    if (w !== null) weightTotal += w;
    const a = normNumber(it.totalAmount);
    if (a !== null) amountTotal += a;
    const p = normNumber(it.insurancePay);
    if (p !== null) payTotal += p;
  }

  const result = {
    status: 'success',
    service_type: 'DRG_SETTLEMENT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      total_amount_total: round2(amountTotal),
      insurance_pay_total: round2(payTotal),
      drg_weight_total: Math.round(weightTotal * 10000) / 10000,
      weight_range: [WEIGHT_MIN, WEIGHT_MAX],
      multiple_tolerance: MULTIPLE_TOL,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: groups.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"个人自付 = 费用总额 − 医保支付金额"这类**表内勾稽**、合计行、重复与空缺，'
      + '以及 DRG 入组的档位提示；**不判断主要诊断选得对不对、手术操作有没有漏填、'
      + 'DRG 分组结果本身对不对、权重与支付标准是否符合本地政策**（以病案室 / 医保办与医保局口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
