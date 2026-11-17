'use strict';
/**
 * bank-reconciliation.js —— 银行流水对账（未达账项核对）本地引擎
 *
 * 为什么做这个：
 *   每家、每月都要对账：把**银行流水**和**企业账面记录**逐笔配对，
 *   找出"银行有、账上没有"与"账上有、银行没有"的**未达账项**，
 *   以及金额相近但不相等的**可疑配对**。
 *   这件事**完全是确定性的**（按金额与日期配对），却极其耗时 ——
 *   而市面上的 AI 会计工具多在"分类/识别"，**很少做真正的对账**。
 *
 * 设计原则（与本仓库其它引擎一致）：
 *   · 自包含：只用 Node.js 标准库，**不发起任何网络请求**；
 *   · 每条结论都引用原文（日期、金额、摘要），第三方可用同一份输入复算；
 *   · 材料不足时返回 insufficient_input 并说明缺什么，**绝不输出"未发现问题"**；
 *   · 只做配对与找差异，**不做会计判断**（哪些该做未达账项调整、是否要计提，是会计的事）。
 */

const CHECKS_GIVEN = [
  '逐笔自动配对（银行流水 ↔ 企业账面，按金额相等 + 日期在窗口内）',
  '未达账项清单（银行有账上无 / 账上有银行无，含笔数与合计）',
  '单侧重复记录检测（同日期同金额出现两次以上）',
  '两侧笔数与金额合计的对比表',
];

const CHECKS_FULL_EXTRA = [
  '可疑配对（金额相近但不相等，差在容差内）',
  '疑似跨期未达（另一侧有同金额记录，但日期超出匹配窗口）',
  '对账恒等式分析（成立性结论与口径诊断；防误读自检免费档也有）',
  '自定义匹配窗口与金额容差（dayWindow / toleranceAbs）',
];

// 订阅版**没有**未执行项：这个引擎无条件执行全部检查（含上面的追加项）。
// 早先这里留着本包那份数组，导致对外 JSON 说"未执行"、实际却都跑了 —— 口径必须与行为一致。
const CHECKS_WITHHELD = [];

/* ---------------------------------------------------------------- 工具 */

function finding(level, category, line, message, advice, evidence) {
  return { level, category, line, message, advice, evidence };
}

/** 金额归一：允许千分位、货币符号、括号负数、正负号 */
function normAmount(v) {
  if (v === null || v === undefined) return null;
  let t = String(v).trim().replace(/[,，\s\u00A0]/g, '');
  // 货币符号可能出现在负号之后（-¥1,240.00），所以不能只锚定行首 —— 全局去掉。
  t = t.replace(/[¥￥$€£]/g, '').replace(/(元|人民币|cny|rmb)$/i, '');
  if (/^\(.*\)$/.test(t)) t = '-' + t.slice(1, -1);            // (100.00) 表示负数
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  return Math.round(parseFloat(t) * 100) / 100;
}

const DATE_RE = /(\d{4})[-\/年.](\d{1,2})[-\/月.](\d{1,2})/;
function parseDate(s) {
  const m = DATE_RE.exec(String(s == null ? '' : s));
  if (!m) return null;
  const y = +m[1], mo = +m[2], d = +m[3];
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  return { key: y * 10000 + mo * 100 + d, text: `${y}-${String(mo).padStart(2, '0')}-${String(d).padStart(2, '0')}` };
}

/**
 * 从一行文本里抽 {date, amount, memo}。
 * 容错：日期可能写成 2026-05-08 / 2026/5/8 / 2026年5月8日；
 * 金额可能带千分位、货币符号、括号负数；其余部分当摘要。
 */
function parseLine(raw, idx) {
  const line = String(raw == null ? '' : raw).trim();
  if (!line) return null;
  const d = parseDate(line);
  // 金额：优先取带小数点的数，其次取带正负号/货币符号的数，最后取任意整数
  const amountPatterns = [
    // 括号负数必须排在前面：否则 (100.00) 会先被"带小数点的数字"规则匹配成 +100.00
    /\(\s*[¥￥$€£]?[\d,]+(?:\.\d{1,2})?\s*\)/g,
    /[-+]?[¥￥$€£]?\d{1,3}(?:,\d{3})+(?:\.\d{1,2})?/g,
    /[-+]?[¥￥$€£]?\d+\.\d{1,2}/g,
    /[-+]?[¥￥$€£]\d+/g,
  ];
  let amountStr = null;
  for (const re of amountPatterns) {
    const hits = line.match(re);
    if (hits && hits.length) { amountStr = hits[hits.length - 1]; break; }
  }
  if (amountStr === null) {
    // 没有小数也没有千分位时，取行里最后一个纯整数（避免把日期当金额）
    const stripped = line.replace(DATE_RE, ' ');
    const ints = stripped.match(/[-+]?\d+/g);
    if (ints && ints.length) amountStr = ints[ints.length - 1];
  }
  const amount = amountStr === null ? null : normAmount(amountStr);
  if (amount === null) return null;
  let memo = line
    .replace(DATE_RE, ' ')
    .replace(amountStr, ' ')
    .replace(/[\t|]+/g, ' ')
    .replace(/\s{2,}/g, ' ')
    .trim();
  if (!memo) memo = '(无摘要)';
  return { date: d ? d.key : null, dateText: d ? d.text : '(无日期)', amount, memo: memo.slice(0, 40), line: idx + 1, raw: line };
}

/** 解析一整段：优先 JSON 数组，否则按行解析 */
function parseEntries(input) {
  if (Array.isArray(input)) {
    return input.map((it, i) => {
      if (it && typeof it === 'object') {
        const amount = normAmount(it.amount != null ? it.amount : it.amt);
        if (amount === null) return null;
        const d = parseDate(it.date != null ? it.date : '');
        return {
          date: d ? d.key : null, dateText: d ? d.text : '(无日期)', amount,
          memo: String(it.memo != null ? it.memo : (it.desc != null ? it.desc : '(无摘要)')).slice(0, 40),
          line: i + 1, raw: `${it.date || ''} ${it.amount != null ? it.amount : it.amt} ${it.memo || it.desc || ''}`.trim(),
        };
      }
      return parseLine(it, i);
    }).filter(Boolean);
  }
  const text = typeof input === 'string' ? input : '';
  return text.split(/\r?\n/).map((l, i) => parseLine(l, i)).filter(Boolean);
}

/** 收集材料：{bank, book} 数组/文本，或一个 text（用「银行」/「账面」分节） */
function collectMaterial(payload) {
  const p = payload && typeof payload === 'object' ? payload : {};
  let bank = null, book = null;
  if (p.bank !== undefined || p.book !== undefined) {
    bank = parseEntries(p.bank);
    book = parseEntries(p.book);
  } else if (typeof p.text === 'string' && p.text.trim()) {
    // 分节：以「银行」/「账面」开头的行作为分节标记
    const lines = p.text.split(/\r?\n/);
    let mode = null;
    const b1 = [], b2 = [];
    lines.forEach((l) => {
      const t = l.trim();
      if (/^(银行流水|银行|bank)/i.test(t) && t.length <= 12) { mode = 'bank'; return; }
      if (/^(企业账面|账面|账上|book)/i.test(t) && t.length <= 12) { mode = 'book'; return; }
      if (mode === 'bank') b1.push(l);
      else if (mode === 'book') b2.push(l);
    });
    bank = parseEntries(b1.join('\n'));
    book = parseEntries(b2.join('\n'));
  }
  return { bank: bank || [], book: book || [] };
}

/* ------------------------------------------------------------ 各项检查 */

const DAY = 1;   // 日期用 YYYYMMDD 整数表示，跨月不可直接相减 —— 用真实日期换算天数

function toDayNumber(key) {
  if (key === null || key === undefined) return null;
  const y = Math.floor(key / 10000), mo = Math.floor((key % 10000) / 100), d = key % 100;
  return Math.floor(Date.UTC(y, mo - 1, d) / 86400000);
}

/** 1. 逐笔配对：金额完全相等且日期在窗口内 */
function matchEntries(bank, book, dayWindow) {
  const used = new Set();
  const pairs = [];
  const unmatchedBank = [];
  bank.forEach((b, bi) => {
    let best = -1, bestGap = Infinity;
    book.forEach((k, ki) => {
      if (used.has(ki)) return;
      if (Math.abs(k.amount - b.amount) > 1e-9) return;
      const bd = toDayNumber(b.date), kd = toDayNumber(k.date);
      const gap = (bd === null || kd === null) ? 0 : Math.abs(bd - kd);
      if (gap > dayWindow) return;
      if (gap < bestGap) { bestGap = gap; best = ki; }
    });
    if (best >= 0) { used.add(best); pairs.push({ bank: b, book: book[best], gapDays: bestGap }); }
    else unmatchedBank.push(b);
  });
  const unmatchedBook = book.filter((_, ki) => !used.has(ki));
  return { pairs, unmatchedBank, unmatchedBook };
}

/** 2. 可疑配对：金额不等但差在容差内 */
function findSuspicious(bankLeft, bookLeft, tolAbs) {
  const out = [];
  const takenBook = new Set();
  bankLeft.forEach((b) => {
    let best = -1, bestDiff = Infinity;
    bookLeft.forEach((k, ki) => {
      if (takenBook.has(ki)) return;
      const diff = Math.abs(k.amount - b.amount);
      if (diff > 1e-9 && diff <= tolAbs && diff < bestDiff) { bestDiff = diff; best = ki; }
    });
    if (best >= 0) {
      takenBook.add(best);
      const k = bookLeft[best];
      out.push(finding('P1', '可疑配对（金额不等）', b.line,
        `银行「${b.dateText} ${b.amount} ${b.memo}」与账面「${k.dateText} ${k.amount} ${k.memo}」金额相差 ${bestDiff.toFixed(2)}（容差内）。`,
        '常见原因是手续费、汇率差或录入笔误；请确认差异原因后再决定是否调整。',
        [b.raw, k.raw]));
    }
  });
  return { findings: out, matchedBookIdx: takenBook };
}

/**
 * 3. 疑似跨期：两侧**未达账项**里存在**同金额**的一对，但日期超出容差窗口。
 *    这是未达账项最常见的成因（银行入账日与记账日跨月），单独指出来可以省掉大量"逐月翻账"。
 *
 *    注意：配对只在**未达账项之间**做，且每笔最多认领一次。
 *    否则"银行有两笔同额、账面一笔且已配对成功"会被误报成跨期（假阳性，已实测踩到）。
 */
function findCrossPeriodPairs(unmatchedBank, unmatchedBook, dayWindow) {
  const out = [];
  const claimedBook = new Set();
  unmatchedBank.forEach((b) => {
    let idx = -1;
    for (let i = 0; i < unmatchedBook.length; i++) {
      if (claimedBook.has(i)) continue;
      if (Math.abs(unmatchedBook[i].amount - b.amount) <= 1e-9) { idx = i; break; }
    }
    if (idx < 0) return;
    claimedBook.add(idx);
    const k = unmatchedBook[idx];
    const bd = toDayNumber(b.date), kd = toDayNumber(k.date);
    const gap = (bd === null || kd === null) ? null : Math.abs(bd - kd);
    out.push(finding('P2', '疑似跨期未达', b.line,
      `银行流水「${b.dateText} ${b.amount} ${b.memo}」与企业账面「${k.dateText} ${k.amount} ${k.memo}」金额相同，`
      + (gap === null ? '但其中一方没有可识别的日期，'
        : `但相隔 ${gap} 天，超出 ${dayWindow} 天的匹配窗口，`),
      '同金额却跨期，多半是银行入账日与记账日不同期；请确认是否属于正常的在途/未达，再决定是否需要调整。',
      [b.raw, k.raw]));
  });
  return out;
}

/** 4. 单侧重复记录 */
function checkDuplicates(entries, sideLabel) {
  const out = [];
  const seen = new Map();
  entries.forEach((e) => {
    const key = `${e.dateText}|${e.amount}`;
    if (!seen.has(key)) seen.set(key, []);
    seen.get(key).push(e);
  });
  seen.forEach((list, key) => {
    if (list.length < 2) return;
    out.push(finding('P1', `${sideLabel}存在重复记录`, list[0].line,
      `${sideLabel}里有 ${list.length} 笔日期与金额完全相同：${key.replace('|', ' ')}（摘要：${list.map((x) => x.memo).join(' / ')}）。`,
      '可能是重复录入，也可能是真实的两笔同额业务；请核对凭证号。',
      list.map((x) => x.raw).slice(0, 3)));
  });
  return out;
}

/* -------------------------------------------------------------- 主流程 */

function analyze(bank, book, opts) {
  const dayWindow = Number.isFinite(opts.dayWindow) ? opts.dayWindow : 3;
  const tolAbs = Number.isFinite(opts.toleranceAbs) ? opts.toleranceAbs : 1.00;

  const { pairs, unmatchedBank, unmatchedBook } = matchEntries(bank, book, dayWindow);
  const sus = findSuspicious(unmatchedBank, unmatchedBook, tolAbs);
  const crossPairs = findCrossPeriodPairs(unmatchedBank, unmatchedBook, dayWindow);

  const sum = (arr) => Math.round(arr.reduce((n, x) => n + x.amount, 0) * 100) / 100;
  const bankSum = sum(bank), bookSum = sum(book);
  const unmatchedBankSum = sum(unmatchedBank), unmatchedBookSum = sum(unmatchedBook);
  // 对账恒等式：银行合计 − 账面合计 =（银行未达）−（账面未达）
  const identityDiff = (bankSum - bookSum) - (unmatchedBankSum - unmatchedBookSum);
  const identityOk = Math.abs(identityDiff) < 0.02;

  const findings = [
    ...sus.findings,
    // ⛔ 订阅版独有：恒等式的**成立性结论 + 口径诊断**（本包只保留下方的防误读自检）
    finding(identityOk ? 'P2' : 'P1', '对账恒等式分析', 0,
      identityOk
        ? `恒等式成立：银行合计 ${bankSum} − 账面合计 ${bookSum} = 银行未达 ${unmatchedBankSum} − 账面未达 ${unmatchedBookSum}，说明两侧每一笔都被正确读出。`
        : `恒等式不成立，差额 ${identityDiff.toFixed(2)}：两侧合计与未达清单对不上，先核对是否某笔金额被读成 0 或跨行粘连漏读。`,
      identityOk ? '未达账项清单可直接拿去逐笔核，无需再往合计上找差异。'
                 : '按差额回推定位到具体行，修完再重跑。'),
    ...crossPairs,
    ...checkDuplicates(bank, '银行流水'),
    ...checkDuplicates(book, '企业账面'),
  ];

  // 未达账项本身不是"错误"，但必须被列出来（这是对账的主要产出）
  if (unmatchedBank.length) {
    findings.push(finding('P1', '未达账项：银行有、账上无', unmatchedBank[0].line,
      `银行流水里有 ${unmatchedBank.length} 笔在账面找不到对应（合计 ${unmatchedBankSum.toFixed(2)}）：`
      + unmatchedBank.slice(0, 5).map((x) => `${x.dateText} ${x.amount}`).join('、')
      + (unmatchedBank.length > 5 ? ' …' : ''),
      '核对是否漏记、跨月入账，或属于银行手续费/利息等需要补记的项。',
      unmatchedBank.slice(0, 5).map((x) => x.raw)));
  }
  if (unmatchedBook.length) {
    findings.push(finding('P1', '未达账项：账上有、银行无', unmatchedBook[0].line,
      `企业账面上有 ${unmatchedBook.length} 笔在银行流水里找不到对应（合计 ${unmatchedBookSum.toFixed(2)}）：`
      + unmatchedBook.slice(0, 5).map((x) => `${x.dateText} ${x.amount}`).join('、')
      + (unmatchedBook.length > 5 ? ' …' : ''),
      '核对是否已开出但对方未收、在途未达，或记账日期与银行入账日期跨期。',
      unmatchedBook.slice(0, 5).map((x) => x.raw)));
  }

  // 恒等式不成立，说明上面某一步的配对/取数出了问题，必须自己报出来 —— 不能悄悄放过
  if (!identityOk) {
    findings.push(finding('P0', '对账恒等式不成立', 1,
      `银行合计 ${bankSum.toFixed(2)} − 账面合计 ${bookSum.toFixed(2)} = ${(bankSum - bookSum).toFixed(2)}，`
      + `但（银行未达 ${unmatchedBankSum.toFixed(2)}）−（账面未达 ${unmatchedBookSum.toFixed(2)}）= ${(unmatchedBankSum - unmatchedBookSum).toFixed(2)}，`
      + `相差 ${identityDiff.toFixed(2)}。`,
      '差值通常来自金额格式异常（如某笔被解析成了 0 或漏掉了一行）；请核对两侧每一笔是否都被正确读出。',
      [`bank_sum=${bankSum}`, `book_sum=${bookSum}`, `bank_count=${bank.length}`, `book_count=${book.length}`]));
  }

  const summary = { p0: 0, p1: 0, p2: 0 };
  const byCategory = {};
  findings.forEach((f) => {
    const k = f.level === 'P0' ? 'p0' : (f.level === 'P1' ? 'p1' : 'p2');
    summary[k]++;
    byCategory[f.category] = (byCategory[f.category] || 0) + 1;
  });
  summary.total = findings.length;
  summary.by_category = byCategory;
  summary.verdict = summary.p0 > 0
    ? '发现必须处理的硬错误（P0）'
    : (summary.p1 > 0 ? '没有 P0，但有需要人工核对的项（P1）'
      : (summary.p2 > 0 ? '只有提示性预警（P2），没有硬错误'
        : '在上述检查项范围内没有发现问题 —— 这不等于没有问题'));

  const reconcile = {
    bank_count: bank.length, book_count: book.length,
    bank_sum: bankSum, book_sum: bookSum,
    matched: pairs.length,
    unmatched_bank: unmatchedBank.length, unmatched_book: unmatchedBook.length,
    unmatched_bank_sum: unmatchedBankSum, unmatched_book_sum: unmatchedBookSum,
    identity_ok: identityOk,
  };
  pairs.forEach((p) => { p.bank = { date: p.bank.dateText, amount: p.bank.amount, memo: p.bank.memo }; p.book = { date: p.book.dateText, amount: p.book.amount, memo: p.book.memo }; });

  return { findings, summary, reconcile, pairs: pairs.slice(0, 100), unmatchedBank, unmatchedBook };
}

function insufficient(missing, advice) {
  return { status: 'insufficient_input', missing: [].concat(missing), advice };
}

/**
 * @param {Object} payload { bank:[...], book:[...], dayWindow?, toleranceAbs? } 或 { text }
 */
function run(payload) {
  const { bank, book } = collectMaterial(payload);
  if (bank.length === 0 && book.length === 0) {
    return insufficient(['没有收到任何流水或账面记录'],
      '请提供两侧记录：bank（银行流水）与 book（企业账面），每笔形如 {"date":"2026-05-08","amount":-1240.00,"memo":"差旅付款"}；'
      + '也可以用 text，先写一行「银行」，再写一行「账面」，各自下面按行写「日期 金额 摘要」。');
  }
  if (bank.length === 0 || book.length === 0) {
    return insufficient([
      bank.length === 0 ? '没有收到银行流水' : '没有收到企业账面记录',
    ], '对账必须两侧都有：请把 bank 与 book 都提供出来（或用 text 分「银行」「账面」两节）。');
  }
  const opts = {
    dayWindow: payload && Number.isFinite(payload.dayWindow) ? payload.dayWindow : undefined,
    toleranceAbs: payload && Number.isFinite(payload.toleranceAbs) ? payload.toleranceAbs : undefined,
  };
  const result = analyze(bank, book, opts);
  result.scope = { given: CHECKS_GIVEN.slice(), withheld: [] };
  return { status: 'success', result: result };
}

module.exports = {
  run,
  analyze,
  collectMaterial,
  parseLine,
  parseEntries,
  normAmount,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
  CHECKS_FULL_EXTRA,
  CHECKS_EXECUTED: CHECKS_GIVEN.concat(CHECKS_FULL_EXTRA),
  CHECKS_OUT_OF_SCOPE: [
    '判断哪些差异应当做未达账项调整（那是会计的事）',
    '识别银行手续费/利息等业务性质并自动入账',
    '核对银行流水本身的真伪',
    '给出税务、审计或法律意见',
    '连接银行或财务系统自动取数（本工具只处理你贴进来的文本）',
  ],
  SAMPLE_TEXT: [
    '银行',
    '2026-05-08 -1240.00 酒店消费',
    '2026-05-07 -86.00 出租车',
    '2026-05-09 -260.00 餐饮',
    '2026-05-10 -30.00 账户管理费',
    '2026-05-12 -5000.00 采购付款',
    '2026-05-12 -5000.00 采购付款',
    '',
    '账面',
    '2026-05-08 -1240.00 差旅住宿',
    '2026-05-07 -86.00 打车费',
    '2026-05-09 -261.50 餐费',
    '2026-05-12 -5000.00 采购付款',
  ].join('\n'),
};
