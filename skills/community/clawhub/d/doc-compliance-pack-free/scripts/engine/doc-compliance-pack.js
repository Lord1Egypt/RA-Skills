'use strict';
/**
 * doc-compliance-pack-full.js —— 发票与单据合规技能包（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须用它：**采购 / 应付 / 财务会计 / 内控 / 代账，在"别人把材料交上来、我要签字或付款"之前**。
 * 要审的从来不是一张单据：发票领用存台账、作废与红冲发票、农产品收购发票与进项抵扣、应付暂估与发票未到、
 * 合同全文一致性、多份合同条款差异、中标结果与合同一致性、投标报价明细、广告文案合规、广告文案违规体检、
 * 出口退税单证一致性、报销单合规、采购三单匹配、外贸单证单单一致 —— **一份材料往往要同时过好几把尺子**，
 * 逐把尺子手审既慢又容易漏，而且每次来料都要重来一遍。
 *
 * 这个包做的事**只有一件**（不是重写任何规则）：把仓库里**已有的 14 个单据/材料合规检查引擎**
 * 装进一个批量壳里，`--input <目录>`（每个子目录 = 一份材料 / 一个供应商）一次跑完所有材料，
 * **每份材料一行结论**。
 *   规则来源：`scripts/engine/parts/<检查项>/`（**逐字节拷贝**自那 14 个免费包，一行都没改；
 *   本包只做"目录 → 材料 → 逐项派发"的编排与汇总）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 *
 * 契约（与仓库其它引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *     payload.text            单份材料：把这份材料的各张单据按 `=== 检查项 ===` 分段拼成文本
 *     payload.objects[]       多份材料：{name, files:[{name, text}]} —— 每个子目录 = 一份材料
 *   CHECKS_GIVEN / CHECKS_WITHHELD   免费档执行 / 不执行的检查项
 *   CHECKS_OUT_OF_SCOPE              本能力**根本不做**的判断（边界诚实）
 *   SAMPLE_TEXT / SAMPLE_OBJECTS     样例（免费包 --sample / --sample-batch 用它自检）
 *
 * 行号口径（**这一条是本包存在的技术理由之一**）：14 个成员引擎的**行号字段并不统一** ——
 * 多数写成 `line`（正文字符串里的行号），「投标报价明细」写 `row`，「广告文案合规」写 `index`（字符位置）。
 * 本包在**批量壳层**把它们统一换算成"**原文文件里的行号**"，并且落位**以原文内容为准**
 * （见 `resolveSourceLine`）：先按结论里的原文片段去找那一行，找不到才退回成员给的行号。
 * 成员引擎一行都没改，口径差异只在这一个函数里被吸收。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），
 * **不读环境变量**，**不写任何文件**（结果只打到 stdout）。
 * ⚠️ 材料不足**绝不给结论**：某份材料没交就单独标"未执行"，一份都跑不了就整体不给结论。
 * ⚠️ 本工具**不代替法务/审计/税务鉴证**，不出具鉴证意见，也不判断某份单据是否真实合法。
 */

const MEMBERS = [
  {
    label: '发票领用存与开票数据',
    id: 'invoice-usage-stock-check',
    line_field: 'line',
    entry: require('./parts/invoice-usage-stock-check/invoice-usage-stock-check.js'),
  },
  {
    label: '发票作废与红冲',
    id: 'tax-invoice-void-check',
    line_field: 'line',
    entry: require('./parts/tax-invoice-void-check/tax-invoice-void-check.js'),
  },
  {
    label: '农产品收购发票与进项抵扣',
    id: 'agri-purchase-invoice-deduction-check',
    line_field: 'line',
    entry: require('./parts/agri-purchase-invoice-deduction-check/agri-purchase-invoice-deduction-check.js'),
  },
  {
    label: '应付暂估与发票未到',
    id: 'ap-provisional-check',
    line_field: 'line',
    entry: require('./parts/ap-provisional-check/ap-provisional-check.js'),
  },
  {
    label: '合同一致性',
    id: 'contract-consistency-check',
    line_field: 'line',
    entry: require('./parts/contract-consistency-check/contract-consistency.js'),
  },
  {
    label: '多份合同条款差异',
    id: 'contract-comparison',
    line_field: 'line',
    entry: require('./parts/contract-comparison/contract-comparison.js'),
  },
  {
    label: '中标结果与合同一致性',
    id: 'award-contract-consistency-check',
    line_field: 'line',
    entry: require('./parts/award-contract-consistency-check/award-contract-consistency-check.js'),
  },
  {
    label: '投标报价明细',
    id: 'bidguard-quote-audit',
    line_field: 'row',
    entry: require('./parts/bidguard-quote-audit/quote-audit.js'),
  },
  {
    label: '广告文案合规',
    id: 'adcheckup-content-compliance',
    line_field: 'index',
    entry: require('./parts/adcheckup-content-compliance/ad-compliance.js'),
  },
  {
    label: '广告文案违规体检',
    id: 'ad-copy-rewrite',
    line_field: 'line',
    entry: require('./parts/ad-copy-rewrite/ad-copy-rewrite.js'),
  },
  {
    label: '出口退税单证一致性',
    id: 'export-rebate-doc-consistency-check',
    line_field: 'line',
    entry: require('./parts/export-rebate-doc-consistency-check/export-rebate-doc-consistency-check.js'),
  },
  {
    label: '报销单合规',
    id: 'expense-compliance',
    line_field: 'line',
    entry: require('./parts/expense-compliance/expense-compliance.js'),
  },
  {
    label: '采购三单匹配',
    id: 'three-way-match',
    line_field: 'line',
    entry: require('./parts/three-way-match/three-way-match.js'),
  },
  {
    label: '外贸单证单单一致',
    id: 'trade-doc-consistency',
    line_field: 'line',
    entry: require('./parts/trade-doc-consistency/trade-doc-consistency.js'),
  },
];

/* 免费档执行：14 项材料合规检查，逐份材料全跑一遍（这就是免费层的核心产出：一次跑完所有材料） */
const CHECKS_GIVEN = MEMBERS.map((m) => m.label);

/* 完整档追加（**多一种能力**，不是多几个数）：跨材料体检台账 + 能不能签/能不能付 ——
   单份材料的结果里根本不存在这些东西。 */
const CHECKS_WITHHELD = [
  '跨材料体检台账（全部材料 × 全部 14 项检查合并成一张总表）',
  '按风险排序的「能不能签 / 能不能付」处置清单（带材料名与原文文件行号）',
  '跨材料共性问题归类（同一类问题命中 2 份及以上材料时合并成一条共性项）',
  '体检报告导出（Markdown 与 CSV 文本，直接交给签字/付款复核环节）',
];

/* 如实列出**每个成员检查包自己**没做的检查项（那 14 个免费包各自的未执行项）——
   两个档位都没实现它们，绝不能因为"买断档打开了体检台账"就让买家以为这些项被跑了。 */
const SUB_CHECKS_WITHHELD = [];
for (const m of MEMBERS) {
  for (const w of (m.entry.CHECKS_WITHHELD || [])) SUB_CHECKS_WITHHELD.push(`${m.label}：${w}`);
}

const TOTAL_SUB_CHECKS = MEMBERS.reduce((n, m) => n + (m.entry.CHECKS_GIVEN || []).length, 0);

const OUT_OF_SCOPE = [
  '判断某份发票/合同/单据是否真实、是否伪造、是否具备法律效力（属于法务/税务/审计的判断，请咨询专业人士）',
  '代替审计程序、代替函证、代替税务鉴证，或出具鉴证意见与法律意见（只做单证内的算术与单证间的字段一致性核对）',
  '核验发票真伪（不查全国增值税发票查验平台、不比对税局数据），也不判断某笔支出能否税前扣除',
  '读取财务软件 / 票税系统 / 合同管理系统的导出文件（需要你先导出成文本，一份材料一个目录）',
  '判断合同条款是否公平、是否对我方有利，也不评价报价是否合理、是否低于成本（只核你给的内容是否自洽）',
];

/* 有两个成员引擎**没有导出 SAMPLE_TEXT**（它们在仓库里本来就把样例放在自己的 `templates/sample.json`）。
   本包不从它们"猜"样例：这里原样内联那两份上游样例，测试里会与上游文件**逐字节比对**，
   一旦上游改了样例，比对会失败而不是悄悄漂移。 */
const SAMPLE_FALLBACK = {
  'bidguard-quote-audit': '序号\t项目名称\t数量\t单价\t合价\n1\t土方开挖\t100\t25\t2500\n'
    + '2\t混凝土浇筑\t50\t400\t19000\n3\t钢筋制安\t\t3800\t76000',
  'adcheckup-content-compliance': '本品牌全国销量第一，效果最好，100%有效。最后一步点击提交即可，我们提供一站式服务。',
};

/** 成员自己的样例（引擎导出了 SAMPLE_TEXT 就用它；没导出就用同包 templates/sample.json 的原样文本） */
function memberSample(m) {
  if (typeof m.entry.SAMPLE_TEXT === 'string' && m.entry.SAMPLE_TEXT !== '') return m.entry.SAMPLE_TEXT;
  return SAMPLE_FALLBACK[m.id] || '';
}

/* 样例 = 14 个成员检查包各自的最小完整样例（各自带表头，用 `=== 检查项 ===` 分段）。
   注意：其中 7 项的**样例本身**就是有问题的材料 ——「合同一致性」（合同主体不一致、条款交叉引用失效、
   金额与日期矛盾）、「多份合同条款差异」（条款缺条与正文不一致）、「投标报价明细」（分项算术不平、
   缺漏项）、「广告文案合规」（绝对化用语）、「报销单合规」（重复发票号）、「采购三单匹配」
   （三单字段不一致）、「外贸单证单单一致」（单单不一致）—— 所以它们会按自身规则报出发现，
   那是这些成员样例的真实结论，不是误报；其余 7 项在各自样例上是 0 条发现。 */
const SAMPLE_TEXT = MEMBERS
  .map((m) => `=== ${m.label} ===\n${memberSample(m)}`)
  .join('\n\n');

/* 有一处硬伤的样例：把「发票领用存与开票数据」里 2026-01 的期末库存从 27 改成 30
   （期初 50 + 领用 100 − 开出 120 − 作废 2 − 红冲 1 = 27，与 30 不符）
   ⇒ 必须报出来，并带**原文文件里的行号**。 */
const DIRTY_FROM = '2026-01\t50\t100\t120\t2\t1\t27';
const DIRTY_TO = '2026-01\t50\t100\t120\t2\t1\t30';
const DIRTY_TEXT = SAMPLE_TEXT.replace(DIRTY_FROM, DIRTY_TO);

/* 只覆盖 3 项的样例：用来演示"材料只交了一部分单据"时，批量壳**明确报一条**，
   而不是把"跑了 3 项"说成"14 项都核过了"。 */
const PARTIAL_TITLES = ['发票领用存与开票数据', '合同一致性', '报销单合规'];
const PARTIAL_TEXT = SAMPLE_TEXT.split(/(?=^=== )/m)
  .filter((s) => PARTIAL_TITLES.some((t) => s.trim().indexOf(`=== ${t} ===`) === 0))
  .join('\n');

/* 批量样例：3 份材料（干净 / 有一处硬伤 / 没交材料），用来演示"一次跑完所有材料"。 */
const SAMPLE_OBJECTS = [
  { name: '豫州新材料有限公司（2026-03 付款前体检）', files: [{ name: '报送材料.txt', text: SAMPLE_TEXT }] },
  { name: '中岳机电设备有限公司（2026-03 付款前体检）', files: [{ name: '报送材料.txt', text: DIRTY_TEXT }] },
  { name: '缺料供应商（只登记未交材料）', files: [] },
];

/** 内置样例**本身带有发现**（6 个成员的样例就是有问题的材料）。
 *  这是**显式声明**、不是放水：`strip_free_engine` 的烟测对"样例必须是 0 发现"的包要求声明这个常量，
 *  否则会把"样例真实报出了问题"误判成"改动把包改坏了"。 */
const SAMPLE_HAS_FINDINGS = true;

function insufficient(missing, advice) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: advice
      || '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值（认不出表头就不出结论）。',
  };
}

function countLevels(list) {
  const out = { p0: 0, p1: 0, p2: 0 };
  for (const f of list) {
    if (f.level === 'P0') out.p0 += 1;
    else if (f.level === 'P1') out.p1 += 1;
    else if (f.level === 'P2') out.p2 += 1;
  }
  return out;
}

/** 把一份材料按 `=== 检查项 ===` 分段，并**记住每一行来自哪个文件第几行**（结论要能回到原文）。
 *
 *  ⛔ 这里**绝不删空行**（与"先过滤空行再交给成员"的写法相比，这是本包实测出来的硬要求）：
 *     本仓库有成员引擎**用空行分隔多张单据** —— `three-way-match` 用 `split(/\n[ \t]*\n+/)`
 *     把一段文本切成"采购订单 / 入库单"两张单据，`trade-doc-consistency` 同理。
 *     实测：把它们自己的样例先过滤空行再喂进去，三单匹配的 2 条发现、外贸单证的 1 条发现
 *     **全部消失**（Engine 把两张单据看成了一张，跨单据字段比对自然无从谈起）；
 *     `contract-consistency` 也会从 12 条掉到 10 条。删空行 = 悄悄改掉成员的输入语义。
 *     所以本包原样保留材料（只摘掉 `=== 检查项 ===` 标题行本身），并且**行号按原样记**。 */
function sectionsOfFile(f) {
  const lines = String(f.text === undefined || f.text === null ? '' : f.text).split(/\r?\n/);
  if (lines.length > 1 && lines[lines.length - 1] === '') lines.pop();   // 末尾换行不算一行
  const out = [];
  let cur = { title: '', texts: [], nos: [], keptNos: [] };
  const flush = () => {
    if (!cur.texts.length || !cur.keptNos.length) return;               // 只有空行的段不算一段
    out.push({
      title: cur.title, file: f.name, text: cur.texts.join('\n'),
      lineNos: cur.nos.slice(), keptLineNos: cur.keptNos.slice(), startLine: cur.keptNos[0],
    });
  };
  for (let i = 0; i < lines.length; i += 1) {
    const m = lines[i].match(/^\s*===\s*(.+?)\s*===\s*$/);
    if (m) {
      flush();
      cur = { title: m[1].trim(), texts: [], nos: [], keptNos: [] };
      continue;
    }
    cur.texts.push(lines[i]);
    cur.nos.push(i + 1);
    if (String(lines[i]).trim() !== '') cur.keptNos.push(i + 1);
  }
  flush();
  return out;
}

function coerceFiles(o) {
  const files = [];
  if (Array.isArray(o.files)) {
    for (const f of o.files) {
      if (!f) continue;
      const t = f.text !== undefined ? f.text : f.content;
      files.push({
        name: String(f.name || f.file || '材料'),
        text: t === undefined || t === null ? '' : String(t),
      });
    }
    return files;
  }
  const t = o.text !== undefined ? o.text : o.content;
  if (t !== undefined && t !== null) {
    files.push({ name: String(o.file || o.file_name || '材料'), text: String(t) });
  }
  return files;
}

/** 入参归一化成"材料列表"：`{text}` 是单份材料，`{objects:[…]}`（或 `{clients:[…]}`）是批量。 */
function normalizeObjects(payload) {
  const raw = [];
  const list = Array.isArray(payload.objects) ? payload.objects
    : (Array.isArray(payload.clients) ? payload.clients : null);
  if (list) {
    for (const o of list) {
      if (!o) continue;
      raw.push({
        name: String(o.name || o.object || o.client || o.material || '').trim(),
        files: coerceFiles(o),
      });
    }
  }
  if (payload.text !== undefined || payload.content !== undefined) {
    raw.push({
      name: String(payload.object_name || payload.object || payload.client_name || payload.client
        || payload.material_name || payload.name || '单份材料').trim(),
      files: coerceFiles(payload),
    });
  }
  const out = [];
  raw.forEach((o, i) => out.push({ name: o.name || `材料${i + 1}`, files: o.files }));
  return out;
}

/** 覆盖缺口检查：材料交了，但只覆盖了一部分检查项 ⇒ **明确报一条**，
 *  不能因为"跑了几项"就以为 14 项都核过了。整份材料都没交的不在这里报（那是材料级的"未执行"）。 */
function checkMaterialCoverage(it) {
  const ran = it.checks.filter((c) => c.status === 'ok');
  const notRun = it.checks.filter((c) => c.status !== 'ok');
  if (!ran.length || !notRun.length) return null;
  return {
    level: 'P2',
    category: '检查项未执行（材料只覆盖了一部分）',
    line: 1,
    message: `材料「${it.material}」的来料只覆盖了 ${ran.length} / ${it.checks.length} 个单据合规检查项，`
      + `未执行的是：${notRun.map((c) => c.check).join('、')} —— 这些项这次**没有核**，请补齐材料后重跑。`,
  };
}

/** 分段对齐检查：材料是多段的（多个文件 / 多张单据），却**没有任何一段**用
 *  `=== 检查项 ===` 分段标题 ⇒ 各项是按"第一个能认出的段"派发的，可能错位。
 *  这时如实报一条，而不是让买家以为"每一项都精确地跑在自己那段材料上"。 */
function checkSectionAlignment(it) {
  if (it.titled_sections || it.candidates < 2) return null;
  const ran = it.checks.filter((c) => c.status === 'ok').map((c) => c.check);
  if (!ran.length) return null;
  return {
    level: 'P2',
    category: '材料没有分段标题（派发可能错位）',
    line: 1,
    message: `材料「${it.material}」有 ${it.candidates} 段内容，但没有一段用 \`=== 检查项 ===\` 分段标题：`
      + `本次是按"第一个能认出的段"逐项派发的（已执行：${ran.join('、')}），`
      + '可能落到别的单据上 —— 请把每张单据前加上 `=== 检查项名 ===` 一行后重跑。',
  };
}

/** 取"用来在原文里定位那一行"的候选片段（**按可靠性排序**，逐个去原文里找，第一个找得到的就用）。
 *  ① evidence / name / term 里**引号括起来的具体值**最可靠（"甲方：北京星河科技有限公司" 里的那个名字）；
 *  ② 其次是每条 evidence 行的**冒号后面的值**（"合同一：第八条 违约责任" → "第八条 违约责任"）；
 *  ③ 最后才是整行本身。
 *  ⚠️ 这些都只是**线索**，最终一定要在原文里真的找得到才用（找不到就如实退回行号/分段首行，绝不编造）。 */
function evidenceKeys(f) {
  const out = [];
  const add = (s) => {
    const t = String(s === undefined || s === null ? '' : s).trim();
    if (t.length >= 2 && t.length <= 60 && out.indexOf(t) < 0) out.push(t);
  };
  const sources = [];
  const ev = f && f.evidence;
  if (Array.isArray(ev)) {
    for (const x of ev) sources.push(String(x === undefined || x === null ? '' : x));
  } else if (ev !== undefined && ev !== null) {
    sources.push(String(ev));
  }
  if (f && f.name) sources.push(String(f.name));
  if (f && f.term) sources.push(String(f.term));
  for (const raw of sources) {
    const q = raw.match(/[\u300c\u300e"\u201c]([^\u300d\u300f"\u201d]{2,40})[\u300d\u300f"\u201d]/);
    if (q) add(q[1]);
  }
  for (const raw of sources) {
    for (const line of raw.split('\n')) {
      const t = line.trim();
      if (!t) continue;
      const i = Math.max(t.lastIndexOf('\uff1a'), t.lastIndexOf(':'));
      if (i > 0 && i < t.length - 1) add(t.slice(i + 1));
      add(t.length > 30 ? t.slice(0, 30) : t);
    }
  }
  return out;
}

/** 成员引擎的行号口径归一 → "它自己那份正文字符串里的行号"。
 *  成员引擎一行都没改：多数写 `line`，「投标报价明细」写 `row`，「广告文案合规」写 `index`（字符位置）。 */
function memberRow(f, cand, lineField) {
  if (lineField === 'index') {
    const idx = Number.isInteger(f.index) ? f.index : -1;
    if (idx < 0) return 0;
    const upto = String(cand.text).slice(0, idx);
    return 1 + (upto.match(/\n/g) || []).length;
  }
  for (const k of [lineField, 'line', 'row']) {
    if (Number.isInteger(f[k]) && f[k] > 0) return f[k];
  }
  return 0;
}

/** 把成员引擎报的行号**落回原文文件行**（用于结论里的"原文文件与行号"）。
 *
 *  成员引擎的行号口径各包不同（`line` / `row` / `index`），而且**成员内部是否过滤空行也不一致**
 *  （本包把材料原样交给成员，成员自己怎么算行号是它的事），直接 `lineNos[row - 1]` 可能整体错位。
 *  错行号比没有行号更糟 —— 买家按行号找回原文会看到别的记录。
 *
 *  所以落位**以原文内容为准**，并且保证结果一定落在原文里**真实存在的非空行**上：
 *    ① 按 `evidenceKeys` 的顺序拿线索，在原文里找出所有"包含该片段"的行；
 *    ② 唯一命中 ⇒ 直接用；
 *    ③ 多行命中 ⇒ 取**不超过成员行号的最后一个命中**（同一片段重复出现时，成员报的行号通常就在其后不远处）；
 *    ④ 一条线索都找不到 ⇒ 退回成员行号对应的原文行；那一行是空行时，再试"按非空行计数"的解释；
 *    ⑤ 仍不行 ⇒ 如实退回**分段首行**。成员没给行号（汇总级/跨单据结论）⇒ 分段首行。
 *  这样"对得上"的成员行为完全不变，只有口径不同的成员被纠正到原文行，且绝不编造行号。 */
function resolveSourceLine(f, cand, lineField) {
  const row = memberRow(f, cand, lineField);
  /* 汇总级/跨单据结论（成员自己把行号记成 0）没有具体行 —— 如实指向本分段的首行，
     不按线索去挑一行（那会让买家以为那行有问题）。 */
  if (!row) return cand.startLine;
  const rows = String(cand.text).split('\n');       // 与 lineNos 一一对应（本包原样保留空行）
  const first = cand.lineNos[0];
  const rowText = (no) => String(rows[no - first] === undefined ? '' : rows[no - first]);
  const real = (no) => Number.isInteger(no) && rowText(no).trim() !== '';
  for (const key of evidenceKeys(f)) {
    const hits = [];
    for (let i = 0; i < rows.length; i += 1) {
      if (String(rows[i]).indexOf(key) >= 0) hits.push(i + 1);
    }
    if (!hits.length) continue;
    if (hits.length === 1) return cand.lineNos[hits[0] - 1];
    let below = null;
    for (const h of hits) { if (h <= row) below = h; }
    return cand.lineNos[(below === null ? hits[0] : below) - 1];
  }
  const direct = cand.lineNos[row - 1];
  if (real(direct)) return direct;
  const kept = cand.keptLineNos[row - 1];           // 成员按"非空行"计数时的另一种解释
  if (real(kept)) return kept;
  return cand.startLine;                            // 都不行 ⇒ 如实退回分段首行（绝不给一个空行号）
}


/** 一份材料跑完全部 14 项；每一项的实际规则在 parts/ 里（本文件一行规则都没改）。
 *
 *  派发规则（**比"第一个跑通的段"更严**，因为本包的成员里有几个是"什么文本都能跑"的自由文本检查）：
 *    · 材料**有分段标题**时：只认标题与本项名字**完全相同**的那一段；
 *      没有同名段 ⇒ 这一项如实标 `not_run`（缺什么写清楚），**绝不拿别的单据顶替**。
 *    · 材料**完全没有分段标题**时（单份材料直接贴、或一堆没有标题的文件）：
 *      按顺序把每一段喂给成员引擎，**第一个跑通的段**就是这一项的表（此时段就是整份材料本身）。
 */
function runOneObject(object) {
  const live = object.files.filter((f) => String(f.text).trim() !== '');
  const candidates = [];
  for (const f of live) for (const s of sectionsOfFile(f)) candidates.push(s);
  const materialLines = live.reduce(
    (n, f) => n + String(f.text).split(/\r?\n/).filter((l) => l.trim() !== '').length, 0);

  if (!candidates.length || materialLines < 5) {
    return {
      object: object.name, status: 'insufficient_input', files: live.map((f) => f.name),
      material_lines: materialLines,
      checks: MEMBERS.map((m) => ({ check: m.label, status: 'not_run', findings: 0 })),
      findings: [], not_run: MEMBERS.map((m) => m.label),
      total: 0, p0: 0, p1: 0, p2: 0, verdict: 'NOT_RUN',
      reason: '没有收到这份材料的可用内容（材料为空或只有几行）',
    };
  }

  const titledSections = candidates.some((c) => c.title !== '');
  const checks = [];
  const findings = [];
  const notRun = [];
  for (const m of MEMBERS) {
    const named = candidates.filter((c) => c.title === m.label);
    const order = named.length ? named : (titledSections ? [] : candidates);
    let hit = null;
    let bestMissing = null;
    for (const cand of order) {
      let out = null;
      try { out = m.entry.run({ text: cand.text }); } catch (e) { out = null; }
      if (out && out.status === 'success' && out.result) {
        hit = { cand: cand, result: out.result, matched: cand.title === m.label };
        break;
      }
      const miss = (out && out.missing) || [];
      if (Array.isArray(miss) && miss.length && (!bestMissing || miss.length < bestMissing.length)) {
        bestMissing = miss;
      }
    }
    if (!hit) {
      notRun.push(m.label);
      checks.push({
        check: m.label, status: 'not_run', findings: 0,
        missing: bestMissing || (titledSections
          ? [`材料里没有 \`=== ${m.label} ===\` 这一段（或那一段里认不出这一项需要的表头）`]
          : ['这份材料里没有这一项需要的表头行']),
      });
      continue;
    }
    const per = (hit.result.findings || []).map((f) => {
      const lineNo = resolveSourceLine(f, hit.cand, m.line_field);
      return {
        level: f.level,
        category: f.category,
        line: memberRow(f, hit.cand, m.line_field),
        object: object.name,
        check: m.label,
        section: hit.cand.title || hit.cand.file,
        section_matched: hit.matched,
        source_file: hit.cand.file,
        source_line: lineNo,
        evidence: `${hit.cand.file}:${lineNo}`,
        message: f.message,
      };
    });
    for (const f of per) findings.push(f);
    checks.push({
      check: m.label, status: 'ok', findings: per.length,
      section: hit.cand.title || hit.cand.file,
      section_matched: hit.matched,
    });
  }

  /* 批量壳自己的两项检查：材料只覆盖了一部分、以及"多段却没有分段标题"（派发可能错位）。 */
  const cover = checkMaterialCoverage({ material: object.name, checks: checks });
  if (cover) {
    findings.push(Object.assign({}, cover, {
      object: object.name, check: '（批量壳）', section: '', section_matched: false,
      source_file: '', source_line: 0, evidence: '材料级',
    }));
  }
  const align = checkSectionAlignment({
    material: object.name, checks: checks,
    candidates: candidates.length, titled_sections: titledSections,
  });
  if (align) {
    findings.push(Object.assign({}, align, {
      object: object.name, check: '（批量壳）', section: '', section_matched: false,
      source_file: '', source_line: 0, evidence: '材料级',
    }));
  }

  const lv = countLevels(findings);
  const anyRan = checks.some((c) => c.status === 'ok');
  return {
    object: object.name,
    status: anyRan ? 'ok' : 'insufficient_input',
    files: live.map((f) => f.name),
    material_lines: materialLines,
    checks: checks,
    findings: findings,
    not_run: notRun,
    total: findings.length,
    p0: lv.p0, p1: lv.p1, p2: lv.p2,
    verdict: lv.p0 > 0 ? 'P0_ISSUES' : (findings.length ? 'ISSUES' : (anyRan ? 'NO_ISSUE_FOUND' : 'NOT_RUN')),
    reason: anyRan ? '' : '材料里没有任何一项能被认出的单据（每一项要有表头行，或用 `=== 检查项名 ===` 分段）',
  };
}

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  if (!payload) {
    return insufficient([
      '一份材料都没收到（objects[] 与 text 都是空）',
      '单份材料用 {"text":"…"}；批量用 {"objects":[{"name":"材料名","files":[{"name":"材料.txt","text":"…"}]}]}',
    ]);
  }
  const objects = normalizeObjects(payload);
  if (!objects.length) {
    return insufficient([
      '一份材料都没收到（objects[] 与 text 都是空）',
      '每份材料一个子目录，目录里放这份材料的一套单据（每项用 `=== 检查项 ===` 分段，Tab 分隔最稳）',
    ]);
  }

  const rows = objects.map(runOneObject);
  const usable = rows.filter((r) => r.status === 'ok');
  if (!usable.length) {
    return insufficient(
      [`全部 ${rows.length} 份材料都没有可用内容（每个子目录里要有这份材料的单据，且每张单据要有表头行）`]
        .concat(rows.map((r) => `材料「${r.object}」：没有可用内容`)),
      '把每份材料放进各自子目录后再跑；材料不足时本工具不做任何认定、也不给任何结论。');
  }

  const findings = [];
  for (const r of rows) for (const f of r.findings) findings.push(f);
  findings.sort((a, b) => (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)
    || (a.line - b.line) || String(a.category).localeCompare(String(b.category)));

  const lv = countLevels(findings);
  const withIssues = rows.filter((r) => r.findings.length > 0).length;
  const notRunObjects = rows.filter((r) => r.status !== 'ok').length;

  const result = {
    service_type: 'DOC_COMPLIANCE_PACK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: CHECKS_WITHHELD.slice(),
      sub_checks_not_run: SUB_CHECKS_WITHHELD.slice(),
      objects: rows.length,
      objects_ran: usable.length,
      sub_checks_per_object: TOTAL_SUB_CHECKS,
      executed_locally: true,
      network_used: false,
      wrote_files: false,
    },
    objects: rows,
    findings: findings,
    summary: {
      objects: rows.length,
      objects_with_issues: withIssues,
      objects_clean: usable.length - withIssues,
      objects_not_run: notRunObjects,
      total: findings.length,
      p0: lv.p0, p1: lv.p1, p2: lv.p2,
      verdict: lv.p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本次对 ${rows.length} 份材料逐份跑了 ${CHECKS_GIVEN.length} 个单据合规检查项（每个成员包内部还有 `
      + `${TOTAL_SUB_CHECKS / CHECKS_GIVEN.length} 项子检查）；未执行的检查项见 scope.checks_not_run 与 `
      + 'scope.sub_checks_not_run。',
    disclaimer: '只把各份材料里的表内/表间算术与单证间字段一致性核一遍，结论都带**原文文件与行号**、'
      + '可由第三方复算；**不代替法务、审计与税务鉴证**，也不判断单据的真实性与合法性。',
  };

  /* 分层：完整档多一层「跨材料体检台账 + 能不能签/能不能付」；免费档只报**实际执行**的那 14 项 */
    result.checks_executed = CHECKS_GIVEN.slice();
    result.checks_withheld = CHECKS_WITHHELD.slice();
  

  return { status: 'success', result: result };
}

module.exports = {
  run, runOneObject, normalizeObjects, coerceFiles, sectionsOfFile, countLevels, checkMaterialCoverage, checkSectionAlignment, resolveSourceLine, memberRow, evidenceKeys, CHECKS_GIVEN, CHECKS_WITHHELD, SUB_CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, SAMPLE_OBJECTS, SAMPLE_FALLBACK, DIRTY_TEXT, PARTIAL_TEXT, MEMBERS, SAMPLE_HAS_FINDINGS,
};
