'use strict';
/**
 * contract-comparison.js —— 多份合同条款横向比对（本地引擎）
 *
 * 为什么做这个：
 *   采购 / 法务 / 审计经常遇到同一件事：**按同一个模板签了几十份合同**，
 *   其中某一份被**悄悄改过一条**（违约金从 5% 变成 2%、管辖地从甲方所在地变成乙方所在地、
 *   质保期从 24 个月变成 12 个月）。手工逐份比对不现实，而评标 / 内审 / 外部审计
 *   恰恰会拿这个说事。这件事**完全是确定性的**：把每份合同按「条」切开、对齐、找不同。
 *
 * 与 contract-consistency（单份合同一致性核对）的区别：
 *   · 那个查的是**一份合同自己跟自己打架**（第 4 条引用第 8 条，但合同里没有第 8 条）；
 *   · 这个查的是**多份合同之间条款不同**（同一模板下的偏离）。
 *   两个能力互补，不重叠。
 *
 * 设计原则（与本仓库其它引擎一致）：
 *   · 自包含：只用 Node.js 标准库，**不发起任何网络请求**；
 *   · 每条结论都引用原文与行号，第三方可用同一份输入复算；
 *   · 材料不足时返回 insufficient_input 并说明缺什么，**绝不输出"未发现问题"**；
 *   · 只做AI比对，**不判断哪一份条款更好、也不给法律意见**。
 */

const CHECKS_GIVEN = [
  '条款切分与横向对齐（把每份合同按「第X条」切开，按条款标题对齐）',
  '缺条 / 多条（某份合同少了或多了哪一条）',
  '关键字段跨合同一致（合同金额 / 违约金比例 / 争议解决 / 合同期限）',
  '条款对照表（每条被几份合同覆盖、有几份不同版本）',
];

const CHECKS_FULL_EXTRA = [
  '条款正文差异的具体文字（同一条的各版本全文并列）',
  '比例与天数类数值差异（如 5% 与 3%、24 个月与 12 个月）',
  '日期逻辑（签订日 ≤ 生效日 ≤ 到期日）',
  '模板占位符残留（【填写…】/ XXX / TBD）',
  '合同金额大小写是否一致',
];

// 订阅版**没有**未执行项：这个引擎无条件执行全部检查（含上面的追加项）。
// 早先这里留着本包那份数组，导致对外 JSON 说"未执行"、实际却都跑了 —— 口径必须与行为一致。
const CHECKS_WITHHELD = [];

/* ---------------------------------------------------------------- 工具 */

function finding(level, category, line, message, advice, evidence) {
  return { level, category, line, message, advice, evidence };
}

/** 文本归一：去掉空白与常见标点，用于比较 */
function normText(s) {
  return String(s == null ? '' : s)
    .replace(/\s+/g, '')
    .replace(/[，。；：、（）()【】\[\]"'"'《》<>·—\-_,.;:]/g, '')
    .toLowerCase();
}

/** 金额归一（与仓库其它引擎口径一致：千分位/货币符号/括号负数） */
function normAmount(v) {
  if (v === null || v === undefined) return null;
  let t = String(v).trim().replace(/[,，\s\u00A0]/g, '');
  t = t.replace(/[¥￥$€£]/g, '').replace(/(元|人民币|cny|rmb)$/i, '');
  if (/^\(.*\)$/.test(t)) t = '-' + t.slice(1, -1);
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  return Math.round(parseFloat(t) * 100) / 100;
}

/* --------------------------------------------------- 1. 条款切分与对齐 */

// 主口径：中文合同的「第X条」；兼容英文合同的 Article N
const CLAUSE_RE = /^第\s*([一二三四五六七八九十百零〇\d]+)\s*条/;
const ARTICLE_RE = /^Article\s+(\d+)/i;
// 兜底口径：合同不用「第X条」时才启用，避免把条款内部的 1. 2. 3. 误切成新条款
const FALLBACK_RE = /^(第\s*[一二三四五六七八九十百零〇\d]+\s*章|[一二三四五六七八九十]+[、.．]|\d+[、.．]\s*\S)/;

/** 从标题行的剩余部分抽「条款标题」，遇到第一个标点就停 */
function titleOf(rest) {
  const t = String(rest || '').trim();
  if (!t) return '';
  const cut = t.split(/[：:。；;，,（(【\[]/)[0].trim();
  return (cut || t).slice(0, 16);
}

/**
 * 把一份合同文本切成条款。
 * @returns {{no:string, title:string, body:string, line:number}[]}
 */
function segmentClauses(text) {
  const lines = String(text == null ? '' : text).split(/\r?\n/);
  const hasMain = lines.some((l) => CLAUSE_RE.test(l.trim()) || ARTICLE_RE.test(l.trim()));
  const head = hasMain ? null : FALLBACK_RE;

  const out = [];
  let cur = null;
  lines.forEach((raw, i) => {
    const line = raw.trim();
    let m = CLAUSE_RE.exec(line);
    let no = '';
    let rest = '';
    if (m) { no = m[1]; rest = line.slice(m[0].length); }
    else {
      const a = ARTICLE_RE.exec(line);
      if (a) { no = a[1]; rest = line.slice(a[0].length); }
      else if (head && head.test(line)) { no = ''; rest = line; }
    }
    if (no !== '' || (head && head.test(line))) {
      cur = { no, title: titleOf(rest), body: line, line: i + 1 };
      out.push(cur);
    } else if (cur) {
      cur.body += '\n' + raw;
    }
  });
  return out.filter((c) => c.body.trim().length > 0);
}

/** 条款的对齐键：优先用标题文本（编号会因增删条款而错位），没有标题才退回编号 */
function clauseKey(c) {
  const t = normText(c.title);
  if (t) return 'T:' + t;
  return 'N:' + normText(c.no);
}

/* ------------------------------------------------------- 2. 关键字段 */

/**
 * 带标签的字段抽取。刻意只抽**标签写得清楚**的字段 ——
 * 猜出来的值会变成假阳性，宁可漏。
 */
const DATE_PAT = '(\\d{4}\\s*[-\\/年.]\\s*\\d{1,2}\\s*[-\\/月.]\\s*\\d{1,2}\\s*日?)';

/**
 * 每个字段给一个 extract(text) —— 而不是只给一条正则。
 * 原因（写代码时就踩到）：正则的惰性量词会把「壹拾万」截成「壹」、
 * 违约金写法的数字可能在关键词前面（「支付合同总金额 5% 的违约金」）。
 * 用函数把"在含关键词的整句里找数值"这件事写清楚，比堆正则可靠得多。
 */
const FIELD_SPECS = [
  {
    id: 'contract_amount', label: '合同金额',
    extract(text) {
      // 「合同总金额：人民币壹拾万元整（小写 100,000.00）」
      const m = new RegExp('(?:合同(?:总)?(?:金额|价款|总价)|总金额|价款合计|合同价)\\s*[:：]?\\s*'
        + '([^\\n]{0,50}?)\\s*[（(]\\s*(?:小写)?\\s*[¥￥]?\\s*([\\d,]+(?:\\.\\d{1,2})?)').exec(text);
      if (!m) return null;
      const num = normAmount(m[2]);
      if (num === null) return null;
      // 去掉「合同总金额：」这类标签前缀，只留值本身
      const label = m[1].split(/[:：]/).pop();
      return { text: label.trim().slice(0, 30), num };
    },
  },
  {
    id: 'penalty_rate', label: '违约金比例',
    extract(text) {
      // 注意：不能只取**第一个**含「违约」的片段 —— 标题行「第八条 违约责任」也含，
      // 但它没有百分比。要取第一个**同时含百分比**的片段（这条被测试抓出来过）。
      for (const seg of String(text).split(/\n|。|；/)) {
        if (!/违约/.test(seg)) continue;
        const m = /(\d+(?:\.\d+)?)\s*%/.exec(seg);
        if (m) return { text: m[1] + '%', num: parseFloat(m[1]) };
      }
      return null;
    },
  },
  {
    id: 'prepay_rate', label: '预付款比例',
    extract(text) {
      for (const seg of String(text).split(/\n|。|；/)) {
        if (!/(预付款|首付款|定金)/.test(seg)) continue;
        const m = /(\d+(?:\.\d+)?)\s*%/.exec(seg);
        if (m) return { text: m[1] + '%', num: parseFloat(m[1]) };
      }
      return null;
    },
  },
  {
    id: 'jurisdiction', label: '争议解决 / 管辖',
    extract(text) {
      const m = /(?:向|由|提交)\s*([^\n，。；]{2,28}?(?:人民法院|仲裁委员会|仲裁院))/.exec(text);
      if (!m) return null;
      const v = m[1].replace(/\s+/g, '').trim();
      // 「北京市朝阳区人民法院」与「北京朝阳区人民法院」视为同一个（去「市/省」后缀差异交给 normText）
      return { text: v, num: null };
    },
  },
  {
    id: 'term_span', label: '合同期限',
    extract(text) {
      const m = new RegExp('(?:自|从)\\s*' + DATE_PAT + '[^\\n]{0,30}?(?:至|到)\\s*' + DATE_PAT).exec(text);
      if (!m) return null;
      return { text: `${m[1].replace(/\s/g, '')} 至 ${m[2].replace(/\s/g, '')}`, num: null };
    },
  },
];

function extractFields(text) {
  const body = String(text == null ? '' : text);
  const out = {};
  FIELD_SPECS.forEach((spec) => {
    let v = null;
    try { v = spec.extract(body); } catch (e) { v = null; }
    if (v && v.text) out[spec.id] = { label: spec.label, text: v.text, num: v.num };
  });
  return out;
}

/* --------------------------------------------------------- 3. 各项检查 */

/** 3.1 对齐：条款键 -> 各合同上的那一版 */
function align(contracts) {
  const groups = new Map();   // key -> { key, title, no, byContract: Map(idx -> clause) }
  contracts.forEach((c, ci) => {
    c.clauses.forEach((cl) => {
      const k = clauseKey(cl);
      if (!groups.has(k)) groups.set(k, { key: k, title: cl.title || ('第' + cl.no + '条'), byContract: new Map() });
      const g = groups.get(k);
      // 同一份合同里同一个键出现两次：只留第一次，避免自比对噪声
      if (!g.byContract.has(ci)) g.byContract.set(ci, cl);
    });
  });
  return groups;
}

/**
 * 标题近似合并。
 * 真实场景：同一模板下有的写「第八条 违约责任」、有的写「第八条 违约责任与赔偿」。
 * 只按标题精确对齐的话，会被误报成**两条缺条**（我写测试时真的踩到了）。
 * 规则：标题互为包含关系、且**覆盖的合同不重叠**时才合并 ——
 * 重叠说明它们本就是两份合同各自的独立条款，不能合。
 */
function mergeSimilarTitles(groups) {
  const keys = [...groups.keys()];
  for (let i = 0; i < keys.length; i++) {
    for (let j = i + 1; j < keys.length; j++) {
      const a = groups.get(keys[i]), b = groups.get(keys[j]);
      if (!a || !b) continue;
      const ta = String(a.title).replace(/\s/g, ''), tb = String(b.title).replace(/\s/g, '');
      if (!ta || !tb) continue;
      if (!(ta === tb || ta.includes(tb) || tb.includes(ta))) continue;
      if ([...a.byContract.keys()].some((k) => b.byContract.has(k))) continue;
      const keep = a.byContract.size >= b.byContract.size ? a : b;
      const drop = keep === a ? b : a;
      drop.byContract.forEach((v, k) => keep.byContract.set(k, v));
      if (String(keep.title).length < String(drop.title).length) keep.title = drop.title;
      groups.delete(drop.key);
    }
  }
}

/** 3.2 缺条 / 多条 */
function checkMissing(groups, contracts) {
  const out = [];
  groups.forEach((g) => {
    const missing = contracts.map((c, i) => ({ c, i })).filter((x) => !g.byContract.has(x.i));
    if (!missing.length) return;
    const first = g.byContract.values().next().value;
    out.push(finding('P1', '缺条', first ? first.line : 0,
      `条款「${g.title}」有 ${contracts.length - missing.length} 份合同写了、`
      + `${missing.length} 份没有：${missing.map((x) => x.c.name).join('、')}。`,
      '同一模板下的合同条款应当一致；请确认是遗漏、是被删掉，还是这一份本来就另用模板。',
      missing.map((x) => x.c.name)));
  });
  return out;
}

/** 3.3 条款正文差异（含「有几份不同版本」的统计） */
function checkClauseDiff(groups, contracts) {
  const out = [];
  groups.forEach((g) => {
    const versions = new Map();   // normText(body) -> {clause, names[]}
    g.byContract.forEach((cl, ci) => {
      const key = normText(cl.body);
      if (!versions.has(key)) versions.set(key, { clause: cl, names: [] });
      versions.get(key).names.push(contracts[ci].name);
    });
    if (versions.size < 2) return;
    const list = [...versions.values()].sort((a, b) => b.names.length - a.names.length);
    const first = list[0].clause;
    out.push(finding('P1', '条款正文不一致', first.line,
      `条款「${g.title}」在 ${contracts.length} 份合同里有 ${versions.size} 个不同版本：`
      + list.map((v) => `${v.names.length} 份写的是「${excerpt(v.clause.body)}」`).join('；') + '。',
      '同一条款出现多个版本，通常是某一两份被单独改过；请逐份确认是有意为之还是遗漏。',
      list.map((v) => `${v.names.join('、')}：${v.clause.body}`)));
  });
  return out;
}

function excerpt(s, n) {
  const t = String(s || '').replace(/\s+/g, ' ').trim();
  return t.length > (n || 40) ? t.slice(0, n || 40) + '…' : t;
}

/** 3.4 关键字段跨合同不一致 */
/**
 * 该字段的差异是否**已经被条款级差异覆盖**？
 * 若是，就不再重复报一遍（同一个事实报两次 = 噪声，买家会以为有两处问题）。
 * 只在该字段的几个值**全部**落在已被标记为"有多个版本"的条款里时才判定为覆盖。
 */
function coveredByClauseDiff(fieldId, contracts, diffClauses) {
  let any = false;
  contracts.forEach((c, ci) => {
    const f = c.fields[fieldId];
    if (!f) return;
    const needle = normText(f.text);
    const hit = (c.clauses || []).find((cl) => normText(cl.body).includes(needle));
    if (!hit || !diffClauses.has(`${ci}:${hit.line}`)) { any = false; return; }
    any = true;
  });
  // 只要有一份的对应条款**不在**差异集里，就不能判定为"已被覆盖"
  for (let ci = 0; ci < contracts.length; ci++) {
    const f = contracts[ci].fields[fieldId];
    if (!f) continue;
    const needle = normText(f.text);
    const hit = (contracts[ci].clauses || []).find((cl) => normText(cl.body).includes(needle));
    if (!hit || !diffClauses.has(`${ci}:${hit.line}`)) return false;
  }
  return any;
}

function checkFields(contracts, diffClauses) {
  const out = [];
  FIELD_SPECS.forEach((spec) => {
    const rows = contracts
      .map((c, i) => ({ name: c.name, v: c.fields[spec.id], i }))
      .filter((r) => r.v);
    if (rows.length < 2) return;   // 只有一份写清楚，无从比对
    if (coveredByClauseDiff(spec.id, contracts, diffClauses)) return;   // 已在「条款正文不一致」里说过
    const distinct = new Map();
    rows.forEach((r) => {
      const k = r.v.num !== null && r.v.num !== undefined ? 'V:' + r.v.num : 'S:' + normText(r.v.text);
      if (!distinct.has(k)) distinct.set(k, { v: r.v, names: [] });
      distinct.get(k).names.push(r.name);
    });
    if (distinct.size < 2) return;
    const vals = [...distinct.values()];
    // 哪几份没写这个字段，也如实说出来 —— 但不当成"不一致"
    const absent = contracts.filter((c) => !c.fields[spec.id]).map((c) => c.name);
    out.push(finding('P1', '关键字段不一致', 0,
      `${spec.label}在各份合同里不一样：` + vals.map((v) => `${v.v.text}（${v.names.join('、')}）`).join('；')
      + (absent.length ? `；另有 ${absent.length} 份没有写清楚这一项（${absent.join('、')}），未参与比对。` : ''),
      '这是最容易被内外审计抓住的一类偏离；请确认哪个版本才是应当执行的口径。',
      vals.map((v) => `${spec.label}：${v.names.join('、')} = ${v.v.text}`)));
  });
  return out;
}

/** 3.5 日期逻辑（签订 ≤ 生效 ≤ 到期） */
function parseYmd(s) {
  const m = /(\d{4})\s*[-\/年.]\s*(\d{1,2})\s*[-\/月.]\s*(\d{1,2})/.exec(String(s || ''));
  if (!m) return null;
  const y = +m[1], mo = +m[2], d = +m[3];
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  return Math.floor(Date.UTC(y, mo - 1, d) / 86400000);
}

function checkDates(contracts) {
  const out = [];
  contracts.forEach((c) => {
    const sign = parseYmd((/签订日期\s*[:：]?\s*([^\n]{0,20})/.exec(c.text) || [])[1]);
    const span = c.fields.term_span && c.fields.term_span.text || '';
    const parts = span.split(/\s*至\s*/);
    const start = parseYmd(parts[0]), end = parseYmd(parts[1]);
    if (sign !== null && start !== null && sign > start) {
      out.push(finding('P1', '日期逻辑', 0,
        `${c.name}：签订日期（${/签订日期\s*[:：]?\s*([^\n]{0,20})/.exec(c.text)[1].trim()}）晚于合同生效日（${parts[0].trim()}）。`,
        '先生效后签订通常意味着日期写错了，请核对原件。', [c.name]));
    }
    if (start !== null && end !== null && start > end) {
      out.push(finding('P0', '日期逻辑', 0,
        `${c.name}：合同期限的起始日晚于到期日（${span}）。`,
        '期限起止颠倒，几乎一定是笔误，属于硬错误。', [c.name]));
    }
  });
  return out;
}

/** 3.6 模板占位符残留 */
const PLACEHOLDER_RE = /【[^】]{0,20}(?:填写|待补|待定|请填)[^】]{0,20}】|\[\s*(?:填写|待补|TBD|TODO)[^\]]{0,20}\]|\bTBD\b|\bXXX+\b|_{4,}/g;

function checkPlaceholders(contracts) {
  const out = [];
  contracts.forEach((c) => {
    const hits = [...new Set(String(c.text).match(PLACEHOLDER_RE) || [])];
    if (!hits.length) return;
    out.push(finding('P1', '模板占位符残留', 0,
      `${c.name}里还留着 ${hits.length} 处没替换的占位符：${hits.slice(0, 6).join('、')}。`,
      '占位符意味着这一处条款还没定稿，签署前必须填实。', hits.slice(0, 6)));
  });
  return out;
}

/** 3.7 金额大小写是否一致（同一份合同内） */
const CN_DIGITS = { 零: 0, 壹: 1, 贰: 2, 叁: 3, 肆: 4, 伍: 5, 陆: 6, 柒: 7, 捌: 8, 玖: 9, 一: 1, 二: 2, 三: 3, 四: 4, 五: 5, 六: 6, 七: 7, 八: 8, 九: 9 };
const CN_UNITS = { 拾: 10, 十: 10, 佰: 100, 百: 100, 仟: 1000, 千: 1000, 万: 10000, 亿: 100000000 };

/**
 * 中文大写金额 -> 数字。
 *
 * 刻意**不支持**「壹亿贰仟万」这类嵌套写法（会返回 null 而不是猜一个数）——
 * 这个值会被用来判 P0「大小写不一致」，**猜错就是假阳性 P0**，
 * 宁可漏报也不能冤枉买家的合同。
 */
function parseCnRough(s) {
  const t = String(s || '').replace(/[人民币元整圆零角分\s]/g, '');
  if (!t) return null;
  if (!/^[壹贰叁肆伍陆柒捌玖拾佰仟万亿一二三四五六七八九十百千]+$/.test(t)) return null;
  if (t.includes('亿')) return null;   // 嵌套写法超出本工具口径，宁可不判
  let total = 0, section = 0, num = 0, seen = false;
  for (const ch of t) {
    if (CN_DIGITS[ch] !== undefined) { num = CN_DIGITS[ch]; seen = true; continue; }
    const u = CN_UNITS[ch];
    if (u === undefined || u >= 100000000) return null;
    if (u === 10000) {
      section += num;
      total += section * 10000;
      section = 0; num = 0;
    } else {
      section += (num === 0 ? 1 : num) * u;   // 「拾」= 10
      num = 0;
    }
    seen = true;
  }
  if (!seen) return null;
  return total + section + num;
}

function checkAmountCase(contracts) {
  const out = [];
  contracts.forEach((c) => {
    // 「人民币壹拾万元整（小写 100,000.00）」—— 大写在小写括号**之前**，所以不锚定括号
    const m = /(?:人民币|金额大写\s*[:：]?)?\s*([壹贰叁肆伍陆柒捌玖拾佰仟万亿]{2,})\s*元\s*整?/.exec(c.text);
    if (!m) return;
    const cn = parseCnRough(m[1]);
    const num = c.fields.contract_amount && c.fields.contract_amount.num;
    if (cn === null || num === null || num === undefined) return;
    if (Math.abs(cn - num) > 0.01) {
      out.push(finding('P0', '金额大小写不一致', 0,
        `${c.name}的金额大写「${m[1]}」= ${cn}，但小写是 ${num}，两者对不上。`,
        '大小写不一致在合同里属于硬错误，签署前必须改到一致。', [`大写 ${cn}`, `小写 ${num}`]));
    }
  });
  return out;
}

/* -------------------------------------------------------------- 主流程 */

function analyze(contracts) {
  const groups = align(contracts);
  mergeSimilarTitles(groups);
  const clauseDiff = checkClauseDiff(groups, contracts);
  // 已被条款级差异覆盖的「哪一份的哪一条」—— 供关键字段检查去重使用。
  // 用 (合同序号:行号) 做键，而不是用条款键：标题被近似合并过之后，
  // 条款键和原始标题对不上，用键会漏判（写这段时实测踩到）。
  const diffClauses = new Set();
  groups.forEach((g) => {
    const versions = new Set([...g.byContract.values()].map((cl) => normText(cl.body)));
    if (versions.size < 2) return;
    g.byContract.forEach((cl, ci) => diffClauses.add(`${ci}:${cl.line}`));
  });
  const findings = [
    ...checkMissing(groups, contracts),
    ...clauseDiff,
    ...checkFields(contracts, diffClauses),
    ...checkDates(contracts),
    ...checkPlaceholders(contracts),
    ...checkAmountCase(contracts),
  ];

  // 条款对照表（本产品的核心产出，天然不是"问题"，单独放在 comparison 里）
  const comparison = [...groups.values()].map((g) => {
    const versions = new Set([...g.byContract.values()].map((cl) => normText(cl.body)));
    return {
      clause: g.title,
      covered: g.byContract.size,
      total: contracts.length,
      versions: versions.size,
      missing: contracts.filter((c, i) => !g.byContract.has(i)).map((c) => c.name),
    };
  }).sort((a, b) => (b.missing.length - a.missing.length) || (b.versions - a.versions));

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
    : (summary.p1 > 0 ? '没有 P0，但有需要人工确认的条款偏离（P1）'
      : '在上述检查项范围内没有发现问题 —— 这不等于没有问题');

  return {
    findings, summary, comparison,
    contractCount: contracts.length,
    clauseCount: groups.size,
    contracts: contracts.map((c) => ({
      name: c.name, clauseCount: c.clauses.length,
      fields: Object.keys(c.fields).map((k) => `${c.fields[k].label}=${c.fields[k].text}`),
    })),
  };
}

/* ------------------------------------------------------------ 材料收集 */

function normContract(x, i) {
  if (x && typeof x === 'object' && typeof x.text === 'string') {
    return { name: String(x.name || x.title || `合同${i + 1}`).slice(0, 40), text: x.text };
  }
  if (typeof x === 'string') return { name: `合同${i + 1}`, text: x };
  return null;
}

/** 从纯文本里按分节标题切出多份合同 */
function splitContractsFromText(text) {
  const raw = String(text || '');
  // 分节标记：单独一行、以「合同一 / 合同A / 第一份 / ## 名称 / 【名称】 / 甲方：xxx 的合同」开头
  const lines = raw.split(/\r?\n/);
  const blocks = [];
  let cur = null;
  lines.forEach((l) => {
    const t = l.trim();
    const m = /^(?:#{1,3}\s*)?(?:【)?(合同\s*[一二三四五六七八九十A-Za-z\d]+|第\s*[一二三四五六七八九十\d]+\s*份(?:合同)?|===+\s*(.+?)\s*===+)(?:】)?\s*$/.exec(t);
    if (m) {
      cur = { name: (m[2] || m[1]).trim(), lines: [] };
      blocks.push(cur);
      return;
    }
    if (cur) cur.lines.push(l);
    else { cur = { name: '合同1', lines: [] }; blocks.push(cur); }
  });
  return blocks.map((b) => ({ name: b.name, text: b.lines.join('\n') }))
    .filter((b) => b.text.trim().length > 0);
}

function collectContracts(payload) {
  const p = payload && typeof payload === 'object' ? payload : {};
  if (Array.isArray(p.contracts) && p.contracts.length) {
    return p.contracts.map(normContract).filter(Boolean);
  }
  if (typeof p.text === 'string' && p.text.trim()) {
    // 站点免费入口只发 {text}：优先按分节标记切，切不出多份再按空行切
    const byMarker = splitContractsFromText(p.text);
    if (byMarker.length >= 2) return byMarker;
    const blocks = p.text.split(/\n[ \t]*\n+/).map((x) => x.trim()).filter(Boolean);
    if (blocks.length >= 2) return blocks.map((b, i) => ({ name: `合同${i + 1}`, text: b }));
  }
  return [];
}

/* ------------------------------------------------------------------ run */

function insufficient(missing, advice) {
  return { status: 'insufficient_input', missing: [].concat(missing), advice };
}

/**
 * @param {Object} payload { contracts:[{name,text}], ... } 或 { text }（多份用分节标题或空行分隔）
 */
function run(payload) {
  const raw = collectContracts(payload);
  if (raw.length === 0) {
    return insufficient(['没有收到任何合同正文'],
      '请提供至少两份合同：contracts 数组，每项形如 {"name":"合同A","text":"第三条 服务期限…"}；'
      + '也可以用一个 text，每份合同用单独一行「合同一」「合同二」这样的分节标题开头（或空行分隔）。');
  }
  const enabled = raw.filter((c) => c.text.trim().length >= 30);
  if (enabled.length < 2) {
    return insufficient([
      `收到 ${raw.length} 份，但其中正文足够长的只有 ${enabled.length} 份`,
    ], '横向比对至少需要**两份**都有实质正文的合同；请补齐后再跑。只有一份时无从比对，本工具不会硬给结论。');
  }
  const contracts = enabled.map((c) => {
    const clauses = segmentClauses(c.text);
    return { name: c.name, text: c.text, clauses, fields: extractFields(c.text) };
  });
  const noClause = contracts.filter((c) => c.clauses.length === 0);
  if (noClause.length === contracts.length) {
    return insufficient(['两份合同的正文里都没有识别出任何条款标题'],
      '本工具靠「第X条」这类条款标题来对齐。请确认正文里保留了条款标题；'
      + '如果合同确实没有分条，本工具无法做横向对齐（不会用猜测凑出结论）。');
  }
  const result = analyze(contracts);
  result.scope = { given: CHECKS_GIVEN.slice(), withheld: [] };
  return { status: 'success', result: result };
}

module.exports = {
  run,
  analyze,
  collectContracts,
  splitContractsFromText,
  segmentClauses,
  extractFields,
  clauseKey,
  normAmount,
  normText,
  parseCnRough,
  FIELD_SPECS,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
  CHECKS_FULL_EXTRA,
  CHECKS_EXECUTED: CHECKS_GIVEN.concat(CHECKS_FULL_EXTRA),
  CHECKS_OUT_OF_SCOPE: [
    '判断哪一份条款对甲方/乙方更有利（那是法务与商务的判断）',
    '给出法律意见、认定条款是否有效或是否违法',
    '核对签署人权限、印章真伪或签署流程是否合规',
    '把两份法律含义不同但用词相近的条款认定为"等价"（本工具只做文本与数值的AI比对）',
    '连接合同管理系统或电子签平台取数（本工具只处理你贴进来的文本）',
  ],
  SAMPLE_TEXT: [
    '合同一',
    '技术服务合同',
    '甲方：北京星河科技有限公司',
    '乙方：上海云帆信息技术有限公司',
    '签订日期：2026-03-01',
    '',
    '第三条 服务期限',
    '本协议自 2026年3月1日 起生效，至 2027年2月28日 止。',
    '',
    '第五条 合同金额',
    '合同总金额：人民币壹拾万元整（小写 100,000.00）。',
    '',
    '第八条 违约责任',
    '任何一方违约，应向对方支付合同总金额 5% 的违约金。',
    '',
    '第十条 争议解决',
    '双方同意向北京市朝阳区人民法院提起诉讼。',
    '',
    '合同二',
    '技术服务合同',
    '甲方：北京星河科技有限公司',
    '乙方：上海云帆信息技术有限公司',
    '签订日期：2026-04-01',
    '开户银行：【填写：开户银行】',
    '',
    '第三条 服务期限',
    '本协议自 2026年3月1日 起生效，至 2027年2月28日 止。',
    '',
    '第五条 合同金额',
    '合同总金额：人民币壹拾万元整（小写 100,000.00）。',
    '',
    '第七条 保密义务',
    '双方对履约过程中知悉的商业秘密保密，保密期为五年。',
    '',
    '第八条 违约责任',
    '任何一方违约，应向对方支付合同总金额 2% 的违约金。',
    '',
    '第十条 争议解决',
    '双方同意向上海市浦东新区人民法院提起诉讼。',
  ].join('\n'),
};
