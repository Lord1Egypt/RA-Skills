/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * freight-loss-claim-check-full.js —— 货运破损理赔与承运商扣款核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**发货方（货主）的财务 / 物流成本岗**，在**每月与承运商对账、
 * 承运商从应付运费里直接扣掉破损理赔款之后**。一张《货运破损理赔与承运商扣款明细表》上
 * 每一格都能手算复现，而每月都要吵的就是这几处：
 *   · 理赔金额按「货值 × 赔付比例 − 免赔额」算，三个因子任何一个抄错，赔款当场差一截；
 *   · 承运商扣款（从应付运费里直接扣掉的赔款）**不能大于**理赔金额 —— 多扣就是白扣；
 *   · 同一张运单被录进两行（重复粘贴最常见）⇒ 赔款与扣款一起算了两遍；
 *   · 赔付比例超过运输合同约定的上限，整行赔款都要重算；
 *   · 货值 / 比例 / 免赔额 / 理赔金额 / 扣款金额这些关键格留空、写占位符或写成负数，整行复算不出来。
 *
 * 表内勾稽（每一步都能被第三方用同一份输入复算）：
 *   理赔金额   = 货值 × 赔付比例 − 免赔额
 *   扣款金额   ≤ 理赔金额
 *   合计行各列 = 各明细行逐列相加（完整档）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）、**不写任何文件、不读环境变量**。
 *
 * 免费档执行 5 项；完整档追加 5 项（见 CHECKS_WITHHELD），其中最后一项是免费档**结构上做不到**的：
 * 「跨承运商 × 跨期汇总台账与按差异金额排序的处理清单」—— 免费档只有逐行结论，没有汇总层。
 *
 * ⚠️ 本工具**不判断**货值该按销售价还是成本价、赔付比例与免赔额是否符合运输合同、
 *    破损是否真实发生、承运商扣款是否真的已经从运费里扣到（那些属于运输合同、现场凭证与
 *    银行流水的核定）：表里的货值、赔付比例、免赔额、扣款金额一律**以你填的为准**，
 *    本工具只核表内勾稽，并把可疑处按原文行号与运单号列出来。
 *
 * 形态说明：本文件用**形态 A**（付费实现集中成一块，块首是一条横线包住的付费检查区注释），
 * 免费包由 tools/strip_free_engine.py 把那条注释到主入口之间的整块连同运行时的付费分支一起摘掉。
 * ⛔ 注释里不写付费开关那一行的字面量，也不写它的条件语句字面量（摘除工具的残渣断言按字符串包含判定）。
 */

const CHECKS_GIVEN = [
  '理赔金额复算（货值 × 赔付比例 − 免赔额 = 理赔金额）',
  '扣款金额不得超过理赔金额（多扣检测）',
  '同一承运商同一期间同一运单号重复行检测',
  '赔付比例超过合同赔付上限检测',
  '关键字段缺失、为占位符或为负数检测',
];

const CHECKS_WITHHELD = [
  '合计行勾稽（合计行各列 = 各明细行逐列相加，不符时报出差异金额并定位差异行）',
  '同一运单号对应多个理赔单号检测（同一票货重复报案 / 单号张冠李戴）',
  '理赔金额差异归因（按 货值口径 / 赔付比例 / 免赔额 / 重复扣款 逐因子回代，指出差异出在哪一个口径）',
  '同一承运商同一期间同一理赔单号重复计扣判定',
  '跨承运商 × 跨期汇总台账与差异处理清单（按承运商 × 期间汇总货值 / 理赔 / 扣款 / 未收回金额与争议金额，按金额排序，逐条带原文行号）',
];

const OUT_OF_SCOPE = [
  '判断货值该按销售价、成本价还是申报价，以及赔付比例与免赔额是否符合运输合同（本工具只核表内算术，以你填的货值与比例为准）',
  '判断承运商扣款是否真的已经从应付运费里扣到、是否已开红字发票或收据（要拿运费结算单与银行流水核，本工具不连接任何系统取数）',
  '判断破损是否真实发生、责任在承运商还是发货方、这一票到底该不该赔（那属于运输合同、现场照片与签收凭证的核定）',
  '判断保险理赔与承运商扣款的先后顺序、代位求偿、往来对账与账务分录',
  '计算增值税进项转出、企业所得税税前扣除，或处理跨月调整与红冲',
  '读取 Excel / TMS / 财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '理赔期间\t承运商编码\t承运商名称\t运单号\t理赔单号\t货值\t赔付比例\t免赔额\t理赔金额\t扣款金额\t合同赔付上限\t破损件数\t货值口径\t扣款事由\t结案日期\t备注',
  '2026-05\tSH-A\t华东承运商\tYD2026050001\tLP2026050001\t10000.00\t0.60\t600.00\t5400.00\t5000.00\t0.70\t3\t销售价\t运输破损按合同赔付\t2026-05-18\t已从5月运费中扣款',
  '2026-05\tSH-A\t华东承运商\tYD2026050002\tLP2026050002\t12000.00\t0.50\t200.00\t5800.00\t3500.00\t0.60\t2\t销售价\t运输破损按合同赔付\t2026-05-20\t已从5月运费中扣款',
  '2026-05\tSH-A\t华东承运商\tYD2026050003\tLP2026050003\t12000.00\t0.70\t600.00\t7800.00\t7800.00\t0.80\t4\t销售价\t运输破损按合同赔付\t2026-05-22\t已从5月运费中扣款',
  '2026-05\tJS-B\t苏南承运商\tYD2026050004\tLP2026050004\t5000.00\t0.80\t0.00\t4000.00\t4000.00\t0.80\t1\t申报价\t运输破损按合同赔付\t2026-05-25\t已从5月运费中扣款',
  '2026-05\tJS-B\t苏南承运商\tYD2026050005\tLP2026050005\t20000.00\t0.55\t1000.00\t10000.00\t9000.00\t0.60\t5\t申报价\t运输破损按合同赔付\t2026-05-28\t已从5月运费中扣款',
  '2026-06\tSH-A\t华东承运商\tYD2026060001\tLP2026060001\t6000.00\t0.60\t300.00\t3300.00\t3000.00\t0.70\t2\t销售价\t运输破损按合同赔付\t2026-06-15\t已从6月运费中扣款',
  '合计\t\t\t\t\t65000.00\t\t\t36300.00\t32300.00\t\t17\t\t\t\t',
].join('\n');

const TOL = 0.01;
const RATIO_TOL = 0.0005;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前，兜底的宽泛别名在后。
  //    「理赔期间」排最前；「承运商编码」必须排在「承运商名称」前（否则编码被 carrierName 的「承运商」抢走）；
  //    「货值口径」必须排在「货值」前（否则口径列被 goodsValue 的「货值」吃掉）；
  //    「合同赔付比例上限」必须排在「赔付比例」前；「扣款事由」必须排在「扣款金额」前
  //    （否则事由列被 deductAmount 的「扣款」吃掉）。
  period: ['理赔期间', '结算期间', '所属期间', '理赔月份', '所属月份', '账期', '期间', '月份', '月度'],
  carrierCode: ['承运商编码', '承运商代码', '物流商编码', '承运编码', '承运商号', '供应商编码'],
  carrierName: ['承运商名称', '承运商简称', '承运商全称', '物流商名称', '机构名称', '承运商'],
  waybill: ['运单编号', '运单号', '货运单号', '快递单号', '面单号', '运单'],
  claimNo: ['理赔单号', '理赔编号', '索赔单号', '报案号', '理赔单'],
  valueBasis: ['货值口径', '计价口径', '价值口径', '价值依据', '口径'],
  goodsValue: ['货值金额', '申报货值', '货物价值', '货物金额', '货物原值', '货值'],
  rateCap: ['合同赔付比例上限', '赔付比例上限', '合同赔付上限', '赔付上限', '合同上限', '比例上限'],
  rate: ['赔付比例', '赔偿比例', '赔付比率', '赔付率'],
  deductible: ['绝对免赔额', '免赔金额', '免赔额', '起赔额'],
  claimAmount: ['理赔金额', '赔付金额', '赔偿金额', '理赔额'],
  reason: ['扣款事由', '扣款原因', '扣款说明', '事由', '原因'],
  deductAmount: ['扣款金额', '承运商扣款', '扣款额', '罚款金额', '扣款'],
  damagedQty: ['破损件数', '报损件数', '破损数量', '件数', '数量'],
  closeDate: ['结案日期', '结案时间', '理赔日期', '核定日期', '结案日', '日期'],
  memo: ['备注', '附注', '说明', '依据'],
};

const LABELS = {
  period: '理赔期间', carrierCode: '承运商编码', carrierName: '承运商名称', waybill: '运单号',
  claimNo: '理赔单号', valueBasis: '货值口径', goodsValue: '货值', rateCap: '合同赔付上限',
  rate: '赔付比例', deductible: '免赔额', claimAmount: '理赔金额', reason: '扣款事由',
  deductAmount: '扣款金额', damagedQty: '破损件数', closeDate: '结案日期', memo: '备注',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不拿 0 去替你假设"这一票不赔"）。
 *  没有破损理赔的承运商请把「货值 / 理赔金额 / 扣款金额 / 免赔额」都填 0，不要留空 ——
 *  「填 0」表示"确实没有"，"留空"表示"不知道"，这两者不能混。 */
const REQUIRED = ['period', 'carrierCode', 'waybill', 'claimNo', 'goodsValue', 'rate',
  'deductible', 'claimAmount', 'deductAmount', 'rateCap'];

/** 合计行逐列复核的列：**不含赔付比例、免赔额与合同上限**（比率加总没有意义，它们另做判定）。 */
const SUM_ROLES = ['goodsValue', 'claimAmount', 'deductAmount', 'damagedQty'];

const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：)$/;
const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a|-+)$/i;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不齐时本工具不做任何认定，也不套用默认值'
      + '（缺一列就报缺列，不会替你按 0 算"这一票没有理赔"）。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function cell(v) {
  return v === undefined || v === null ? '' : String(v).trim();
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = cell(header).replace(/[\s（）()]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

/** 数字归一化：`12,000.00` / `¥12000` / `(12000)`（会计负数）/ `60%` 都认。`60%` 按百分数折成 0.60。
 *  比例列写 `0.6` 或 `60%` 都行；写 `60` 表示 6000%，本工具不会替你猜。 */
function normNumber(raw) {
  if (isBlank(raw)) return null;
  const t = String(raw).trim();
  const neg = /^\(.*\)$/.test(t);
  const isPct = /%\s*$/.test(t);
  const s = (neg ? t.replace(/[()]/g, '') : t).replace(/[,，\s¥￥$%]/g, '');
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  const v = isPct ? n / 100 : n;
  return neg ? -v : v;
}

const round2 = (n) => Math.round(n * 100) / 100;
const num = (row, role) => normNumber(row[role]);

function parseTable(text) {
  const src = String(text).split(/\r?\n/);
  const raw = [];
  for (let i = 0; i < src.length; i++) {
    if (src[i].trim() !== '') raw.push({ line: i + 1, text: src[i] });
  }
  if (!raw.length) {
    return { error: 'empty', items: [], totals: { row: null, line: 0, rows: 0 }, cols: [], missingColumns: [] };
  }
  const headers = splitRow(raw[0].text);
  const cols = headers.map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingColumns = REQUIRED.filter((r) => !have.has(r)).map((r) => LABELS[r] || r);
  if (missingColumns.length) {
    return { error: 'no_header', items: [], totals: { row: null, line: 0, rows: 0 }, cols, missingColumns };
  }
  const items = [];
  let totalRow = null;
  let totalRows = 0;
  for (let i = 1; i < raw.length; i++) {
    const fields = splitRow(raw[i].text);
    const row = { line: raw[i].line, raw: raw[i].text };
    cols.forEach((c, idx) => {
      if (!c.role) return;
      if (row[c.role] === undefined) row[c.role] = fields[idx] === undefined ? '' : fields[idx];
    });
    if (TOTAL_WORDS.test(cell(fields[0]))) {
      // 一份材料里拼了多期 / 多个承运商时会出现多行「合计 / 小计」：只把**最后一行**当对账总额
      // （对账单总额在最后），前面的是分组小计；行数记进 totals.rows 让人看得见，不静默丢数据。
      totalRow = row;
      totalRows += 1;
    } else {
      items.push(row);
    }
  }
  return {
    items,
    totals: { row: totalRow, line: totalRow ? totalRow.line : 0, rows: totalRows },
    cols,
    missingColumns: [],
  };
}

function who(it) {
  const code = cell(it.carrierCode) || '(未填承运商编码)';
  const name = cell(it.carrierName);
  const wb = cell(it.waybill) || '(未填运单号)';
  const cn = cell(it.claimNo);
  return `承运商「${code}${name ? ' ' + name : ''}」运单 ${wb}${cn ? ` / 理赔单 ${cn}` : ''}`;
}

function groupKeyOf(it) {
  return `${cell(it.carrierCode) || '(未填承运商编码)'}|${cell(it.period) || '(未填期间)'}`;
}

/* ============================ 免费档执行的检查项 ============================ */

function checkClaimRecompute(it) {
  const gv = num(it, 'goodsValue');
  const rate = num(it, 'rate');
  const ded = num(it, 'deductible');
  const stated = num(it, 'claimAmount');
  if (gv === null || rate === null || ded === null || stated === null) return null;
  const expect = round2(gv * rate - ded);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '理赔金额复算不符', line: it.line,
    amount: round2(Math.abs(stated - expect)),
    message: `${who(it)}的理赔金额是 ${stated.toFixed(2)}，按 货值 ${gv.toFixed(2)} × 赔付比例 `
      + `${round2(rate * 100)}% − 免赔额 ${ded.toFixed(2)} = ${expect.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '理赔金额是后面所有加减项的地基。先确认这张单的**货值口径**（销售价 / 成本价 / 申报价）'
      + '与**赔付比例档**，再看免赔额是不是按合同逐票扣的，最后才改理赔金额 —— '
      + '三个因子里任何一个错一档，这一票的赔款就跟着错。',
  };
}

function checkDeductOverClaim(it) {
  const claim = num(it, 'claimAmount');
  const ded = num(it, 'deductAmount');
  if (claim === null || ded === null) return null;
  if (ded <= claim + TOL) return null;
  const over = round2(ded - claim);
  return {
    level: 'P0', category: '扣款金额大于理赔金额（多扣）', line: it.line,
    amount: over,
    message: `${who(it)}的承运商扣款是 ${ded.toFixed(2)}，大于本行理赔金额 ${claim.toFixed(2)}，`
      + `多扣 ${over.toFixed(2)} —— 承运商从应付运费里扣走的钱超过了这一票核定的赔款。`,
    advice: '扣款金额是承运商直接从运费里扣掉的赔款，最多只能扣到理赔金额为止。'
      + '先把这一票的理赔核定单与运费结算单摆在一起：常见错法是按原报损金额扣了、'
      + '而核定后免赔额没扣掉，或者同一票在运费里扣了两次（另见重复行检测）。',
  };
}

function checkDuplicateWaybill(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = groupKeyOf(it);
    const wb = cell(it.waybill);
    if (!wb || isBlank(wb)) continue;
    const k = `${key}|${wb}`;
    if (seen.has(k)) {
      const claim = num(it, 'claimAmount');
      const deduct = num(it, 'deductAmount');
      out.push({
        level: 'P1', category: '同一承运商同一期间同一运单号重复行', line: it.line,
        amount: round2(Math.abs(claim === null ? 0 : claim) + Math.abs(deduct === null ? 0 : deduct)),
        message: `${who(it)}在第 ${seen.get(k)} 行已经录过一次，第 ${it.line} 行又出现一次 —— `
          + '同一票货的理赔金额与承运商扣款都被算了两遍。',
        advice: '先看是不是重复粘贴 / 重复导单（对账表里最常见）。确属同一票货分两段定损的，'
          + '请拆成两行、各写清扣款事由与不同理赔单号，不要共用同一个运单号。',
      });
    } else {
      seen.set(k, it.line);
    }
  }
  return out;
}

function checkRateOverCap(it) {
  const rate = num(it, 'rate');
  const cap = num(it, 'rateCap');
  if (rate === null || cap === null) return null;
  if (rate <= cap + RATIO_TOL) return null;
  const gv = num(it, 'goodsValue');
  const excess = gv === null ? 0 : round2(gv * (rate - cap));
  return {
    level: 'P1', category: '赔付比例超过合同赔付上限', line: it.line,
    amount: excess,
    message: `${who(it)}的赔付比例是 ${round2(rate * 100)}%，超过合同赔付上限 `
      + `${round2(cap * 100)}%${gv === null ? '' : `（按货值 ${gv.toFixed(2)} 折算超出上限的赔款约 ${excess.toFixed(2)}）`}。`,
    advice: '合同赔付上限是这一票赔款的天花板。先回到运输合同看清上限是按票、按货值档还是按品类定的，'
      + '再确认这一票适用哪一档；比例填错（把 60% 写成 0.6 之外的写法）也会触发这里。',
  };
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = cell(it[role]);
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这一行就复算不出来。本工具不会用 0 或默认值替你填：'
            + '这一票确实没有破损就请把 货值 / 理赔金额 / 扣款金额 / 免赔额 都填 0，'
            + '留空表示"不知道"，两者不能混。',
        });
        continue;
      }
      const n = normNumber(s);
      if (n !== null && n < 0) {
        out.push({
          level: 'P0', category: '关键字段为负数', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是负数（${s}）—— 这一列的金额不可能为负。`,
          advice: '金额列出现负号，多半是会计负数写法（`(1200)`）被原样填进来，'
            + '或者把"冲回"的行用负号混在明细里。请改成正数并在备注里写清冲回依据，'
            + '本工具按正数口径复算，不会替你猜负号的含义。',
        });
      }
    }
  }
  return out;
}

function run(payload) {
  const p = payload;
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到货运破损理赔与承运商扣款明细表的正文（text）—— 请把'
      + '「理赔期间 / 承运商编码 / 运单号 / 理赔单号 / 货值 / 赔付比例 / 免赔额 / 理赔金额 / '
      + '扣款金额 / 合同赔付上限」这张表（含表头）整段贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `表头缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(String(text).split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或每行都是合计行），没有任何破损理赔与扣款明细行');
  }

  const carriers = new Set();
  const periods = new Set();
  for (const it of t.items) {
    carriers.add(cell(it.carrierCode));
    periods.add(cell(it.period));
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkClaimRecompute(it);
    if (a) findings.push(a);
    const b = checkDeductOverClaim(it);
    if (b) findings.push(b);
    const c = checkRateOverCap(it);
    if (c) findings.push(c);
  }
  findings.push.apply(findings, checkBlanks(t.items));
  findings.push.apply(findings, checkDuplicateWaybill(t.items));



  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);
  const checksExecuted = CHECKS_GIVEN.slice();

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let goodsTotal = 0;
  let claimTotal = 0;
  let deductTotal = 0;
  let qtyTotal = 0;
  for (const it of t.items) {
    const a = num(it, 'goodsValue');
    if (a !== null) goodsTotal += a;
    const b = num(it, 'claimAmount');
    if (b !== null) claimTotal += b;
    const c = num(it, 'deductAmount');
    if (c !== null) deductTotal += c;
    const d = num(it, 'damagedQty');
    if (d !== null) qtyTotal += d;
  }
  goodsTotal = round2(goodsTotal);
  claimTotal = round2(claimTotal);
  deductTotal = round2(deductTotal);
  qtyTotal = round2(qtyTotal);

  let tierNote = `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 result 里的 checks_withheld。`;


  const result = {
    status: 'success',
    service_type: 'FREIGHT_LOSS_CLAIM_CHECK',
    scope: {
      checks: checksExecuted,
      checks_not_run: notRun,
      rows: t.items.length,
      carriers: carriers.size,
      periods: periods.size,
      totals_row: Boolean(t.totals.row),
      totals_rows: t.totals.rows || 0,
      goods_value_total: goodsTotal,
      claim_amount_total: claimTotal,
      deduct_amount_total: deductTotal,
      damaged_qty_total: qtyTotal,
      paid_in_total: deductTotal,
      outstanding_total: round2(claimTotal - deductTotal),
      statement_claim_total: t.totals.row ? num(t.totals.row, 'claimAmount') : null,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      carriers: carriers.size,
      periods: periods.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_executed: checksExecuted,
    checks_withheld: notRun,
    checks_given: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    note: tierNote,
    disclaimer: '只核「货值 × 赔付比例 − 免赔额 = 理赔金额」「扣款金额 ≤ 理赔金额」'
      + '「合计行各列 = 各明细行逐列相加」这类**表内勾稽**，不判断货值该按销售价还是成本价、'
      + '赔付比例与免赔额是否符合运输合同、破损是否真实发生、扣款是否真的已从运费中扣到'
      + '（以运输合同、现场凭证与银行流水为准）；每条结论都带原文行号与运单号，可由第三方用同一份输入复算。',
  };



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, REQUIRED, SUM_ROLES,
};
