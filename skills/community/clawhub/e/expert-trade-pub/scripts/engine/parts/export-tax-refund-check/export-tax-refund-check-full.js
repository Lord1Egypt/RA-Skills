'use strict';
/**
 * export-tax-refund-check.js —— 出口退税申报与单证核对（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须做这件事：**每一票出口退税申报之前 / 每个申报期收尾时**。
 * 外贸企业（免退税）与生产企业（免抵退）都要把同一票货的申报表与单证摆在一起逐笔对：
 * 报关单、出口发票、收汇水单、商品编码适用退税率、申报退税额。金额与税率只要有一票对不上，
 * 退税审核就会卡住、甚至已退税额被追回，而函调要翻的单证本来就是这张表里已经填好的东西。
 *
 * 好消息是这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   退税额     = 出口额人民币 × 退税率                （逐行复算）
 *   应有退税额 = 出口额人民币 × 商品编码适用退税率      （订阅版：按文库档位复算并做差异归因）
 *   出口额人民币 = 外币离岸价 × 汇率                  （订阅版：汇率折算复算）
 *   合计行各列 = 明细行相加
 *   同一报关单号：同一所属期里同源行重复 = 粘重；横跨两个所属期 = 重复申报
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），不写盘、不读环境变量。

 * 契约：导出 run / parseTable / roleOf / normNumber / round2 / isBlank / splitRow /
 *      CHECKS_GIVEN / CHECKS_WITHHELD / OUT_OF_SCOPE / SAMPLE_TEXT / LABELS / SUM_ROLES。
 *
 * ⚠️ 付费实现集中在下面的形态 A 标记块里（免费包会被整块摘掉）；
 *    开关**只声明一次**，且**不要在注释里写出开关或条件语句的字面量** ——
 *    strip_free_engine 的残渣断言是**纯字符串包含**判断，注释里写一遍就会被判『没删干净』而整包回滚。
 * ⚠️ 本工具**不判断**这一票该不该退税、该按哪个版本的出口退税率文库、免抵退的
 *    "不得免征和抵扣税额"怎么算（那属于税法与申报口径判断）：表里的出口额、税率、退税额
 *    一律**以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号列出来。
 */

const CHECKS_GIVEN = [
  '退税额逐行复算（出口额人民币 × 退税率 = 退税额）',
  '申报表合计行与明细勾稽（合计行各列 = 明细行相加）',
  '报关单号与出口发票号一一对应及重复登记检测',
  '申报退税率与商品编码适用退税率档位一致性',
  '单证缺失与关键字段空缺检测（报关单 / 出口发票 / 收汇水单状态列）',
];

const CHECKS_WITHHELD = [
  '跨月与企业汇总台账异常（同一报关单横跨两个所属期或两家申报企业时逐组报出，并输出按所属期 / 申报企业的汇总台账）',
  '按差异金额排序的处理清单（按 |应有退税额 − 申报退税额| 从大到小排优先级，逐条带归因）',
  '汇率折算与出口额不符（外币离岸价 × 汇率 ≠ 出口额人民币）',
  '出口发票金额与出口额口径不符（同一票货的发票金额与出口额人民币应当一致）',
  '单证不齐仍计入本期申报（单证没齐就把退税额报进本期，应当挂账等单证齐）',
];

const OUT_OF_SCOPE = [
  '判断这一票货该不该退税、能不能退税（是否属于退税范围、是否已申报过、是否落入不予退税情形，属于税法判断，请咨询税务师）',
  '判断该商品编码应当适用哪个退税率（出口退税率文库的版本、商品编码归类与外购 / 自产口径，属于归类与税法判断）',
  '生产企业免抵退的"不得免征和抵扣税额""免抵退税额抵减额"与期末留抵的分配计算',
  '关税、增值税、消费税、免抵退税申报表的表间关系，以及收汇期限、函调、单证备案等合规期限判断',
  '读取电子税务局 / 单一窗口 / ERP / 报关行系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  ['所属期', '申报企业', '报关单号', '出口发票号', '商品编码', '商品编码适用退税率',
    '出口数量', '出口额人民币', '外币离岸价', '汇率', '出口发票金额', '计税金额',
    '退税率', '退税额', '报关单状态', '出口发票状态', '收汇水单状态'].join('\t'),
  ['2026-01', '华远进出口有限公司', 'BG-2026-0101', 'FP-2026-0001', '8528721000', '13%',
    '1000', '630000.00', '90000.00', '7.0000', '630000.00', '630000.00',
    '13%', '81900.00', '有', '有', '有'].join('\t'),
  ['2026-01', '华远进出口有限公司', 'BG-2026-0102', 'FP-2026-0002', '9013803000', '9%',
    '500', '306000.00', '45000.00', '6.8000', '306000.00', '306000.00',
    '9%', '27540.00', '有', '有', '有'].join('\t'),
  ['2026-02', '华远进出口有限公司', 'BG-2026-0201', 'FP-2026-0003', '6109100021', '13%',
    '2000', '840000.00', '120000.00', '7.0000', '840000.00', '840000.00',
    '13%', '109200.00', '有', '有', '有'].join('\t'),
  ['2026-02', '恒昌贸易（上海）有限公司', 'BG-2026-0202', 'FP-2026-0004', '8471300000', '9%',
    '800', '414000.00', '60000.00', '6.9000', '414000.00', '414000.00',
    '9%', '37260.00', '有', '有', '有'].join('\t'),
  ['2026-03', '恒昌贸易（上海）有限公司', 'BG-2026-0301', 'FP-2026-0005', '9403600000', '13%',
    '300', '216000.00', '30000.00', '7.2000', '216000.00', '216000.00',
    '13%', '28080.00', '有', '有', '有'].join('\t'),
  ['合计', '', '', '', '', '',
    '4600', '2406000.00', '345000.00', '', '2406000.00', '2406000.00',
    '', '283980.00', '', '', ''].join('\t'),
].join('\n');

const TOL = 0.01;              // 表内各列复算的容差（分）
const RATE_TOL = 0.0005;       // 税率容差：0.05 个百分点
const WORKLIST_MIN = 100;      // 处理清单的入单门槛（元）：低于此的差异只算尾差

/** 表头 → 角色。**顺序即优先级：更具体的别名必须排在更宽泛的前面**。
 *  「商品编码适用退税率」不能被「商品编码」抢走、「报关单状态」不能被「报关单号」抢走 ——
 *  顺序错一列，那一列就静默地不参与任何检查（跑起来不报错，只是永远查不出东西）。 */
const ROLES = {
  period: ['退税所属期', '申报所属期', '所属期', '所属月份', '所属期间', '期间', '月份'],
  enterprise: ['申报企业名称', '申报企业', '出口企业', '经营单位', '企业名称', '公司名称'],
  hsRate: ['商品编码适用退税率', '商品编码适用税率', '编码适用退税率', '文库退税率', '适用退税率', '退税率文库', '适用税率'],
  hsCode: ['商品编码', '商品编号', 'HS编码', 'hs编码', '海关编码', '税则号列'],
  declarationNo: ['海关报关单号', '出口报关单号', '报关单编号', '报关单号', '核销单号'],
  invoiceNo: ['出口发票号码', '出口发票编号', '出口发票号', '外销发票号', '发票号码', '发票号'],
  qty: ['出口数量', '申报出口数量', '出口商品数量', '成交数量', '数量'],
  exportAmount: ['出口额人民币', '出口货物人民币金额', '人民币出口额', '离岸价人民币', '出口额', '出口金额'],
  fxAmount: ['外币离岸价', '外币出口额', '离岸价外币', '成交总价外币', '外币金额', '原币金额'],
  fxRate: ['记账汇率', '折算汇率', '汇率', '牌价'],
  invoiceAmount: ['出口发票金额', '外销发票金额', '发票总金额', '发票金额'],
  taxBase: ['出口货物计税金额', '退税计税金额', '计税金额', '购进金额', '计税价格'],
  rebateRate: ['出口退税率', '申报退税率', '退税比例', '退税率'],
  rebateAmount: ['应退税额', '申报退税额', '可退税额', '退税金额', '退税额'],
  customsDoc: ['报关单状态', '报关单齐备', '报关单是否齐备'],
  invoiceDoc: ['出口发票状态', '出口发票齐备', '出口发票是否齐备'],
  receiptDoc: ['收汇水单状态', '收汇凭证状态', '收汇单据状态', '收汇水单'],
};

const LABELS = {
  period: '所属期', enterprise: '申报企业', hsRate: '商品编码适用退税率', hsCode: '商品编码',
  declarationNo: '报关单号', invoiceNo: '出口发票号', qty: '出口数量',
  exportAmount: '出口额人民币', fxAmount: '外币离岸价', fxRate: '汇率',
  invoiceAmount: '出口发票金额', taxBase: '计税金额', rebateRate: '退税率',
  rebateAmount: '退税额', customsDoc: '报关单状态', invoiceDoc: '出口发票状态',
  receiptDoc: '收汇水单状态',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'declarationNo', 'invoiceNo', 'hsCode', 'hsRate', 'qty',
  'exportAmount', 'rebateRate', 'rebateAmount', 'customsDoc', 'invoiceDoc', 'receiptDoc'];
/** 订阅版复算用的列：没给不算材料不足，但订阅版会如实说明"这几列没给、这几项没核" */
const OPTIONAL = ['enterprise', 'fxAmount', 'fxRate', 'invoiceAmount', 'taxBase'];
/** 合计行逐列复核的列（税率列、单号列、状态列不可加总） */
const SUM_ROLES = ['qty', 'exportAmount', 'fxAmount', 'invoiceAmount', 'taxBase', 'rebateAmount'];
/** 单证状态列（缺失即报） */
const DOC_ROLES = ['customsDoc', 'invoiceDoc', 'receiptDoc'];
/** 关键字段：空了这一行的复算就做不了 */
const KEEP_ROLES = ['declarationNo', 'invoiceNo', 'hsCode', 'qty', 'exportAmount',
  'rebateRate', 'hsRate', 'rebateAmount'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|汇总：)$/;
const DOC_MISSING_WORDS = /^(缺|缺失|没有|无|未齐|不齐|未到|待收|待补|否|no|n\/a)$/i;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|空|待填|待补|待定|未填)$/i.test(s);
}

function roleOf(header) {
  const h = String(header === undefined || header === null ? '' : header)
    .replace(/[\s（）()【】\[\]]/g, '');
  if (h === '') return null;
  for (const role of Object.keys(ROLES)) {
    if (ROLES[role].some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

/** 数字归一化：`1,050.00` / `¥1050` / `(120)` 都能认；认不出返回 null（**不猜**） */
function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim();
  if (s === '') return null;
  s = s.replace(/[,，\s¥￥$]/g, '');
  if (/^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  s = s.replace(/[()]/g, '').replace(/%$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

/** 退税率归一化成小数：`13%` ⇒ 0.13；`0.13` ⇒ 0.13；`13` ⇒ 0.13 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text === undefined || text === null ? '' : text)
    .split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) {
    return { items: [], totals: {}, missingColumns: null, missingOptional: [], header: [], roles: [] };
  }
  const header = splitRow(raw[0]);
  const roles = header.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const missingOptional = OPTIONAL.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
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
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return { items, totals, missingColumns, missingOptional, header, roles };
}

const str = (v) => (v === undefined || v === null ? '' : String(v).trim());

const who = (it) => {
  const p = str(it && it.period) || `第 ${it && it.line} 行`;
  const n = [str(it && it.declarationNo), str(it && it.invoiceNo)].filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodOf = (it) => str(it && it.period) || `第 ${it && it.line} 行`;
const enterpriseOf = (it) => str(it && it.enterprise) || '（未填申报企业）';

/** 这一行缺哪几张单证（空 / 占位符 / 写着「缺」这类词都算缺） */
function docMissingOf(it) {
  const out = [];
  for (const role of DOC_ROLES) {
    const v = str(it && it[role]);
    if (isBlank(v) || DOC_MISSING_WORDS.test(v)) out.push(role);
  }
  return out;
}

/** 调用某个检查函数并把它的**发现数组**并进 target。
 *  返回 null（没有结论）时一律跳过 —— 绝不把 null 当结论、也不让引擎抛异常。 */
function pushAll(target, fn, a, b) {
  const r = fn(a, b);
  if (Array.isArray(r)) target.push.apply(target, r);
}

/* ================================ 本包检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkRebateRecompute(it) {
  const out = [];
  const amount = normNumber(it.exportAmount);
  const rate = rateValue(it.rebateRate);
  const stated = normNumber(it.rebateAmount);
  if (amount === null || rate === null || stated === null) return out;
  const expect = round2(amount * rate);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '退税额复算不符', line: it.line,
    message: `${who(it)}：出口额人民币 ${amount.toFixed(2)} × 退税率 ${(rate * 100).toFixed(2)}% `
      + `= ${expect.toFixed(2)}，表里「退税额」填的是 ${stated.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`
      + '退税额就是这一格：算多了会被追回并加收滞纳金，算少了是自己的钱没退回来。',
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
    const expect = round2(sum);
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的`
        + `「${LABELS[role]}」相加是 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
        + '申报表的取数口径就是这张表的合计行：合计是手打或从别处粘来的，明细改了它没跟着改，'
        + '报上去的表与附送单证就对不上。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seenRow = new Map();
  const byDecl = new Map();
  const byInv = new Map();
  for (const it of items) {
    const p = str(it.period);
    const d = str(it.declarationNo);
    const v = str(it.invoiceNo);
    if (p && d && v) {
      const key = `${p}|${d}|${v}`;
      if (seenRow.has(key)) {
        out.push({
          level: 'P1', category: '报关单号与出口发票号重复登记', line: it.line,
          message: `${who(it)}与第 ${seenRow.get(key)} 行完全同源（同一所属期、同一报关单号、同一出口发票号）—— `
            + '要么是重复粘贴了一行，要么是同一票货被拆成两行登记。'
            + '多出来的那一行会把出口额与退税额重复计一遍，退税额当场虚增。',
        });
      } else seenRow.set(key, it.line);
    }
    if (d) {
      if (!byDecl.has(d)) byDecl.set(d, []);
      byDecl.get(d).push(it);
    }
    if (v) {
      if (!byInv.has(v)) byInv.set(v, []);
      byInv.get(v).push(it);
    }
  }
  for (const [d, rows] of byDecl) {
    const invoices = [];
    for (const it of rows) {
      const v = str(it.invoiceNo);
      if (v && invoices.indexOf(v) < 0) invoices.push(v);
    }
    if (invoices.length < 2) continue;
    out.push({
      level: 'P1', category: '报关单号与出口发票号重复登记', line: rows[0].line,
      message: `报关单号「${d}」在本表里对应 ${invoices.length} 张出口发票（${invoices.join('、')}，`
        + `第 ${rows.map((r) => r.line).join('、')} 行）—— 报关单号与出口发票号应当一一对应：`
        + '一票一单对应多张发票时要有拆单说明，否则函调时"这一票到底出口了多少"说不清。',
    });
  }
  for (const [v, rows] of byInv) {
    const decls = [];
    for (const it of rows) {
      const d = str(it.declarationNo);
      if (d && decls.indexOf(d) < 0) decls.push(d);
    }
    if (decls.length < 2) continue;
    out.push({
      level: 'P1', category: '报关单号与出口发票号重复登记', line: rows[0].line,
      message: `出口发票号「${v}」在本表里对应 ${decls.length} 张报关单（${decls.join('、')}，`
        + `第 ${rows.map((r) => r.line).join('、')} 行）—— 一张出口发票对应多张报关单 = 发票被重复使用或`
        + '发票号填串了，退税申报里这条最容易被比对出来。',
    });
  }
  return out;
}

function checkRateTier(it) {
  const out = [];
  const declared = rateValue(it.rebateRate);
  const applicable = rateValue(it.hsRate);
  if (declared === null || applicable === null) return out;
  if (Math.abs(declared - applicable) <= RATE_TOL) return out;
  out.push({
    level: 'P0', category: '退税率与商品编码档位不一致', line: it.line,
    message: `${who(it)}：申报用的退税率是 ${(declared * 100).toFixed(2)}%，`
      + `商品编码「${str(it.hsCode)}」对应的适用退税率是 ${(applicable * 100).toFixed(2)}%，`
      + `相差 ${round2((declared - applicable) * 100).toFixed(2)} 个百分点 —— `
      + '退税率跟着商品编码走：编码归类错了，或者用了已过期的退税率文库，'
      + '算出来的退税额就是错的（多退要追回，少退是自己亏）。先把编码与文库版本核准，再改退税额。',
  });
  return out;
}

function checkDocMissing(it) {
  const out = [];
  for (const role of docMissingOf(it)) {
    out.push({
      level: 'P0', category: '单证缺失', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是空的或写着"${str(it[role]) || '空'}"—— `
        + '出口退税申报要靠这几张单证互相印证：缺哪一张就补哪一张，'
        + '单证没齐时既不要先报、也不要把空值当成"没问题"静默跳过。',
    });
  }
  for (const role of KEEP_ROLES) {
    if (!isBlank(it[role])) continue;
    out.push({
      level: 'P0', category: '关键字段缺失或占位符', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${str(it[role]) || '空'}）—— `
        + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，'
        + '不要让空值静默跳过检查，更不要用 0 顶上。',
    });
  }
  return out;
}

/* ===== 以下为订阅版才执行的检查 ===== */
/* 免费包会被 strip_free_engine 从这一行整块摘到 run 函数之前：
   下面这些函数名在免费引擎里**一个都不会出现**。 */

/** 归因：这一行退税额对不上，最可能是哪一类原因 */
function attributionOf(it) {
  const declared = rateValue(it.rebateRate);
  const applicable = rateValue(it.hsRate);
  if (declared !== null && applicable !== null && Math.abs(declared - applicable) > RATE_TOL) return '退税率档位';
  if (docMissingOf(it).length) return '单证不齐';
  const fx = normNumber(it.fxAmount);
  const rate = normNumber(it.fxRate);
  const amount = normNumber(it.exportAmount);
  if (fx !== null && rate !== null && amount !== null && Math.abs(fx * rate - amount) > TOL) return '汇率折算';
  const invoice = normNumber(it.invoiceAmount);
  if (invoice !== null && amount !== null && Math.abs(invoice - amount) > TOL) return '金额口径';
  return '其他（需人工复核）';
}

/** 应有退税额 = 出口额人民币 × 商品编码适用退税率，与申报退税额逐行复算 */
function checkTierGap(it) {
  const out = [];
  const amount = normNumber(it.exportAmount);
  const applicable = rateValue(it.hsRate);
  const stated = normNumber(it.rebateAmount);
  if (amount === null || applicable === null || stated === null) return out;
  const expect = round2(amount * applicable);
  const gap = round2(stated - expect);
  if (Math.abs(gap) <= TOL) return out;
  const why = attributionOf(it);
  out.push({
    level: 'P1', category: '适用档位应有退税额与申报退税额不符', line: it.line,
    attribution: why, gap_amount: Math.abs(gap),
    message: `${who(it)}：出口额人民币 ${amount.toFixed(2)} × 商品编码适用退税率 `
      + `${(applicable * 100).toFixed(2)}% = 应有 ${expect.toFixed(2)}，`
      + `申报退税额是 ${stated.toFixed(2)}，相差 ${gap.toFixed(2)}（归因：${why}）—— `
      + '申报退税额与"按适用档位算出来的钱"必须一致：不一致要么是退税率用错档，'
      + '要么是出口额 / 计税口径串了，要么是汇率折算用了别的口径。',
  });
  return out;
}

function checkFxRecompute(it) {
  const out = [];
  const fx = normNumber(it.fxAmount);
  const rate = normNumber(it.fxRate);
  const amount = normNumber(it.exportAmount);
  if (fx === null || rate === null || amount === null) return out;
  const expect = round2(fx * rate);
  if (Math.abs(expect - amount) <= TOL) return out;
  out.push({
    level: 'P1', category: '汇率折算与出口额不符', line: it.line,
    attribution: '汇率折算', gap_amount: Math.abs(round2(amount - expect)),
    message: `${who(it)}：外币离岸价 ${fx.toFixed(2)} × 汇率 ${rate.toFixed(4)} = ${expect.toFixed(2)}，`
      + `表里「出口额人民币」是 ${amount.toFixed(2)}，相差 ${round2(amount - expect).toFixed(2)}—— `
      + '出口额人民币是退税额的计算基数：汇率用了哪一天、哪一档（记账汇率还是结汇汇率）'
      + '必须写清楚，折算口径不一致会让退税额整票算错。',
  });
  return out;
}

function checkInvoiceVsExportAmount(it) {
  const out = [];
  const invoice = normNumber(it.invoiceAmount);
  const amount = normNumber(it.exportAmount);
  if (invoice === null || amount === null) return out;
  const gap = round2(invoice - amount);
  if (Math.abs(gap) <= TOL) return out;
  out.push({
    level: 'P1', category: '出口发票金额与出口额口径不符', line: it.line,
    attribution: '金额口径', gap_amount: Math.abs(gap),
    message: `${who(it)}：出口发票金额 ${invoice.toFixed(2)}，出口额人民币 ${amount.toFixed(2)}，`
      + `相差 ${gap.toFixed(2)}—— 同一票货的出口发票金额与报关口径出口额应当一致：`
      + '差额大，要么是发票少开 / 多开，要么是报关时改了总价而发票没重开，'
      + '要么是把非本票的货款记到了这一行。这两张单证不一致是出口退税函调最常见的起因。',
  });
  return out;
}

function checkDocGapHold(it) {
  const out = [];
  const missing = docMissingOf(it);
  if (!missing.length) return out;
  const stated = normNumber(it.rebateAmount);
  if (stated === null || stated <= TOL) return out;
  out.push({
    level: 'P1', category: '单证不齐仍计入本期申报', line: it.line,
    attribution: '单证不齐', gap_amount: stated,
    message: `${who(it)}：单证还没齐（缺 ${missing.map((r) => LABELS[r]).join('、')}），`
      + `却已经把退税额 ${stated.toFixed(2)} 计进本期申报—— 单证不齐的票应当先挂账、`
      + '等单证齐了再申报：先报后补容易被要求转出或退回，还会把本期的申报数搅乱。',
  });
  return out;
}

/** 跨月 / 跨企业汇总台账：同一报关单号横跨两个所属期或两家申报企业 = 重复申报的头号特征 */
function checkLedger(items) {
  const out = [];
  const m = new Map();
  for (const it of items) {
    const d = str(it.declarationNo);
    if (!d) continue;
    if (!m.has(d)) m.set(d, []);
    m.get(d).push(it);
  }
  for (const [d, rows] of m) {
    if (rows.length < 2) continue;
    const periods = [];
    const enterprises = [];
    for (const it of rows) {
      const p = periodOf(it);
      if (periods.indexOf(p) < 0) periods.push(p);
      const e = enterpriseOf(it);
      if (enterprises.indexOf(e) < 0) enterprises.push(e);
    }
    const where = rows.map((r) => `第 ${r.line} 行（${periodOf(r)} / ${enterpriseOf(r)}）`).join('、');
    if (periods.length >= 2) {
      out.push({
        level: 'P1', category: '跨月与企业汇总台账异常', line: rows[0].line,
        attribution: '重复申报', declaration_no: d,
        message: `报关单号「${d}」在本表里横跨 ${periods.length} 个所属期：${periods.join('、')}`
          + `（${where}）—— 一票报关单只能申报一次出口退税：横跨两个所属期出现，`
          + '要么是上一期已经报过、这一期又报了一遍，要么是把同一票货拆到两期里各报一部分。'
          + '跨月汇总台账一比就出来，查到要全额退回。',
      });
    } else if (enterprises.length >= 2) {
      out.push({
        level: 'P1', category: '跨月与企业汇总台账异常', line: rows[0].line,
        attribution: '跨企业重复', declaration_no: d,
        message: `报关单号「${d}」在本表里出现在 ${enterprises.length} 家申报企业：`
          + `${enterprises.join('、')}（${where}）—— 同一票报关单只能由一家企业申报：`
          + '要么是代理出口 / 自营出口的主体填错了，要么是两家企业各报了一遍，'
          + '重复的那一份会被要求退回。',
      });
    }
  }
  return out;
}

/** 跨月 / 跨企业汇总台账（数据段，不是结论）：按 所属期 × 申报企业 汇总申报数与应有数 */
function buildLedger(items) {
  const groups = new Map();
  for (const it of items) {
    const key = `${periodOf(it)}|${enterpriseOf(it)}`;
    if (!groups.has(key)) {
      groups.set(key, {
        period: periodOf(it), enterprise: enterpriseOf(it), rows: 0,
        qty: 0, export_total: 0, declared_total: 0, expected_total: 0, gap: 0, lines: [],
      });
    }
    const g = groups.get(key);
    g.rows += 1;
    g.lines.push(it.line);
    const qty = normNumber(it.qty);
    if (qty !== null) g.qty += qty;
    const amount = normNumber(it.exportAmount);
    const applied = rateValue(it.hsRate);
    const stated = normNumber(it.rebateAmount);
    if (amount !== null) g.export_total += amount;
    if (stated !== null) g.declared_total += stated;
    if (amount !== null && applied !== null) g.expected_total += round2(amount * applied);
  }
  const byGroup = [];
  for (const g of groups.values()) {
    g.qty = round2(g.qty);
    g.export_total = round2(g.export_total);
    g.declared_total = round2(g.declared_total);
    g.expected_total = round2(g.expected_total);
    g.gap = round2(g.declared_total - g.expected_total);
    byGroup.push(g);
  }
  byGroup.sort((a, b) => String(a.period).localeCompare(String(b.period))
    || String(a.enterprise).localeCompare(String(b.enterprise)));
  return { groups: byGroup, group_count: byGroup.length, rows: items.length };
}

/** 按差异金额排序的处理清单（数据段）：|应有退税额 − 申报退税额| 从大到小排优先级 */
function buildWorklist(items) {
  const rows = [];
  for (const it of items) {
    const amount = normNumber(it.exportAmount);
    const applied = rateValue(it.hsRate);
    const stated = normNumber(it.rebateAmount);
    if (amount === null || applied === null || stated === null) continue;
    const gap = round2(stated - round2(amount * applied));
    if (Math.abs(gap) < WORKLIST_MIN) continue;
    rows.push({
      line: it.line, who: who(it),
      period: periodOf(it), enterprise: enterpriseOf(it),
      declaration_no: str(it.declarationNo),
      stated: stated, expected: round2(amount * applied),
      gap_amount: Math.abs(gap), attribution: attributionOf(it),
    });
  }
  rows.sort((a, b) => (b.gap_amount - a.gap_amount) || (a.line - b.line));
  rows.forEach((r, i) => { r.rank = i + 1; });
  return rows;
}

/** 差异归因分布（数据段）：退税率档位 / 汇率折算 / 金额口径 / 单证不齐 / 其他 */
function buildAttribution(items) {
  const buckets = { '退税率档位': 0, '汇率折算': 0, '金额口径': 0, '单证不齐': 0, '其他（需人工复核）': 0 };
  const byLine = [];
  for (const it of items) {
    const amount = normNumber(it.exportAmount);
    const applied = rateValue(it.hsRate);
    const stated = normNumber(it.rebateAmount);
    const gap = (amount !== null && applied !== null && stated !== null)
      ? round2(stated - round2(amount * applied)) : 0;
    const missing = docMissingOf(it);
    const fx = normNumber(it.fxAmount);
    const fxRate = normNumber(it.fxRate);
    const fxBad = (fx !== null && fxRate !== null && amount !== null)
      && Math.abs(round2(fx * fxRate) - amount) > TOL;
    const invoice = normNumber(it.invoiceAmount);
    const invoiceBad = (invoice !== null && amount !== null) && Math.abs(round2(invoice - amount)) > TOL;
    if (Math.abs(gap) <= TOL && !missing.length && !fxBad && !invoiceBad) continue;
    const why = attributionOf(it);
    buckets[why] = (buckets[why] || 0) + 1;
    byLine.push({ line: it.line, who: who(it), attribution: why, gap_amount: Math.abs(gap) });
  }
  return { buckets: buckets, by_line: byLine };
}

/* ================================== 主入口 ================================== */

function run(payload) {
  const p = payload && typeof payload === 'object' ? payload : {};
  const paid = Boolean(p && (p.full || p.credit || p.token));
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = typeof p.text === 'string' ? p.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到出口退税申报与单证对照表正文（text）—— 请把「所属期 / 申报企业 / '
      + '报关单号 / 出口发票号 / 商品编码 / 商品编码适用退税率 / 出口数量 / 出口额人民币 / 外币离岸价 / '
      + '汇率 / 出口发票金额 / 计税金额 / 退税率 / 退税额 / 报关单状态 / 出口发票状态 / 收汇水单状态」'
      + '这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `出口退税申报与单证对照表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${t.header.join(' / ') || '(一个都没认出来)'}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何申报明细行');
  }

  const periods = new Set();
  const enterprises = new Set();
  const declarations = new Set();
  let qtyTotal = 0;
  let exportTotal = 0;
  let declaredTotal = 0;
  let expectedTotal = 0;
  for (const it of t.items) {
    periods.add(periodOf(it));
    enterprises.add(enterpriseOf(it));
    const d = str(it.declarationNo);
    if (d) declarations.add(d);
    const qty = normNumber(it.qty);
    if (qty !== null) qtyTotal += qty;
    const amount = normNumber(it.exportAmount);
    if (amount !== null) exportTotal += amount;
    const stated = normNumber(it.rebateAmount);
    if (stated !== null) declaredTotal += stated;
    const applied = rateValue(it.hsRate);
    if (amount !== null && applied !== null) expectedTotal += round2(amount * applied);
  }

  const findings = [];
  const notRun = [];
  for (const it of t.items) {
    pushAll(findings, checkRebateRecompute, it);
    pushAll(findings, checkRateTier, it);
    pushAll(findings, checkDocMissing, it);
    if (paid) {
      pushAll(findings, checkTierGap, it);
      pushAll(findings, checkFxRecompute, it);
      pushAll(findings, checkInvoiceVsExportAmount, it);
      pushAll(findings, checkDocGapHold, it);
    }
  }
  pushAll(findings, checkTotalRow, t.totals, t.items);
  pushAll(findings, checkDuplicates, t.items);
  if (paid) {
    pushAll(findings, checkLedger, t.items);
  }
  if (!paid) notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const executed = CHECKS_GIVEN.concat(CHECKS_WITHHELD);

  let note = `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`;
  if (paid) {
    note = `完整档执行全部 ${executed.length} 项检查（免费档的 ${CHECKS_GIVEN.length} 项 +`
      + ` 完整档追加的 ${CHECKS_WITHHELD.length} 项）。`;
  }

  const result = {
    status: 'success',
    service_type: 'EXPORT_TAX_REFUND_CHECK',
    scope: {
      checks: paid ? executed : CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      enterprises: enterprises.size,
      declarations: declarations.size,
      totals_row: Boolean(t.totals && t.totals.row),
      qty_total: round2(qtyTotal),
      export_total: round2(exportTotal),
      rebate_total: round2(declaredTotal),
      expected_total: round2(expectedTotal),
      gap_total: round2(declaredTotal - expectedTotal),
      missing_optional: t.missingOptional || [],
      tolerance: TOL,
      rate_tolerance: RATE_TOL,
      worklist_min: WORKLIST_MIN,
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
    note: note,
    disclaimer: '只核「出口额人民币 × 退税率 = 退税额」「合计行 = 明细之和」「报关单号与出口发票号一一对应」'
      + '以及完整档的「按适用档位应有退税额 / 汇率折算 / 发票口径」这类**表内勾稽与档位提示**，'
      + '**不判断这一票该不该退税、适用哪个退税率文库、免抵退的不得免征和抵扣税额怎么算**'
      + '（以税法与主管税务机关口径为准）；结论可由第三方用同一份输入复算。',
  };
  if (paid) {
    result.ledger = buildLedger(t.items);
    result.worklist = buildWorklist(t.items);
    result.attribution = buildAttribution(t.items);
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
