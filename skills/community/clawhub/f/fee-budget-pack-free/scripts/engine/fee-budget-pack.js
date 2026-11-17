'use strict';
/**
 * fee-budget-pack-full.js —— 费用与预算技能包（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须用它：**企业财务 / 管理会计 / 费用岗，在每月费用入账与经营分析会之前**。
 * 要核的从来不是一张表，而是十几张互相勾稽的费用底稿：预提费用与到票冲销、费用预算执行差异、
 * 部门费用预算执行、报销单合规预检、租金账单与押金、物流仓储与操作费、设备维保与备件领用、
 * 承运司机运费结算、运费对账、车队油耗与运费、物业费与滞纳金、物业公共能耗分摊、
 * 物业公共收益公示与分成、长期待摊费用摊销 —— 每张表都有自己的勾稽关系，
 * **逐张手核既慢又容易漏**，而且月月重复。
 *
 * 这个包做的事**只有一件**（不是重写任何规则）：把仓库里**已有的 14 个费用与预算检查引擎**
 * 装进一个批量壳里，`--input <目录>`（每个子目录 = 一个客户 / 一套材料）一次跑完所有客户，
 * **每个客户一行结论**。
 *   规则来源：`scripts/engine/parts/<检查项>/`（**逐字节拷贝**自那 14 个免费包，一行都没改；
 *   本包只做"目录 → 客户 → 逐项派发"的编排与汇总）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约（与仓库其它引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *     payload.text            单客户：该客户的一套费用与预算材料文本（每项用 `=== 检查项 ===` 分段）
 *     payload.objects[]       多客户：{name, files:[{name, text}]} —— 每个子目录 = 一个客户
 *   CHECKS_GIVEN / CHECKS_WITHHELD   免费档执行 / 不执行的检查项（免费包据此如实列出未执行项）
 *   CHECKS_OUT_OF_SCOPE              本能力**根本不做**的判断（边界诚实）
 *   SAMPLE_TEXT / SAMPLE_OBJECTS     样例（免费包 --sample / --sample-batch 用它自检）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），
 * **不读环境变量**，**不写任何文件**（结果只打到 stdout）。
 * ⚠️ 材料不足**绝不给结论**：某个客户没材料就单独标"未执行"，一个客户都跑不了就整体不给结论。
 * ⚠️ 本工具**不代替审计、不出鉴证意见、不判断这笔费用该不该报/该不该资本化**，
 *    也不读财务软件、费控系统、ERP 的导出文件。
 */

const MEMBERS = [
  {
    label: '预提费用与到票冲销核对',
    id: 'accrual-expense-check',
    entry: require('./parts/accrual-expense-check/accrual-expense-check.js'),
  },
  {
    label: '费用预算执行差异核对',
    id: 'budget-variance-check',
    entry: require('./parts/budget-variance-check/budget-variance-check.js'),
  },
  {
    label: '部门费用预算执行核对',
    id: 'department-budget-execution-check',
    entry: require('./parts/department-budget-execution-check/department-budget-execution-check.js'),
  },
  {
    label: '报销单合规预检',
    id: 'expense-compliance',
    entry: require('./parts/expense-compliance/expense-compliance.js'),
  },
  {
    label: '租金账单与押金结算核对',
    id: 'lease-rent-check',
    entry: require('./parts/lease-rent-check/lease-rent-check.js'),
  },
  {
    label: '物流仓储与操作费核对',
    id: 'logistics-storage-fee-check',
    entry: require('./parts/logistics-storage-fee-check/logistics-storage-fee-check.js'),
  },
  {
    label: '设备维保与备件领用费用核对',
    id: 'equipment-maintenance-cost-check',
    entry: require('./parts/equipment-maintenance-cost-check/equipment-maintenance-cost-check.js'),
  },
  {
    label: '承运司机运费结算核对',
    id: 'driver-freight-settlement-check',
    entry: require('./parts/driver-freight-settlement-check/driver-freight-settlement-check.js'),
  },
  {
    label: '运费对账',
    id: 'freight-reconciliation',
    entry: require('./parts/freight-reconciliation/freight-reconciliation.js'),
  },
  {
    label: '车队油耗与运费核对',
    id: 'fleet-fuel-cost-check',
    entry: require('./parts/fleet-fuel-cost-check/fleet-fuel-cost-check.js'),
  },
  {
    label: '物业费与滞纳金核对',
    id: 'property-fee-check',
    entry: require('./parts/property-fee-check/property-fee-check.js'),
  },
  {
    label: '物业公共能耗分摊核对',
    id: 'property-utility-apportionment-check',
    entry: require('./parts/property-utility-apportionment-check/property-utility-apportionment-check.js'),
  },
  {
    label: '物业公共收益公示与分成核对',
    id: 'property-public-income-check',
    entry: require('./parts/property-public-income-check/property-public-income-check.js'),
  },
  {
    label: '长期待摊费用摊销核对',
    id: 'long-term-amortization-check',
    entry: require('./parts/long-term-amortization-check/long-term-amortization-check.js'),
  },
];

/* 免费档执行：14 个费用与预算检查项，逐个客户全跑一遍（这就是免费层的核心产出：一次跑完所有客户） */
const CHECKS_GIVEN = MEMBERS.map((m) => m.label);

/* 完整档追加（**多一种能力**，不是多几个数）：跨客户汇总台账 —— 单客户结果里根本不存在的东西 */
const CHECKS_WITHHELD = [
  '跨客户汇总台账（全部客户 × 全部 14 项检查合并成一张总表）',
  '跨客户风险排序处理清单（按 P0/P1/P2 排序，带客户名与原文文件行号）',
  '跨客户共性问题归类（同一问题命中 2 个及以上客户时合并成一条共性项）',
  '费用台账导出（Markdown 与 CSV 文本，直接用于月度费用复核说明）',
];

/* 如实列出**每个成员检查包自己**没做的检查项（那 14 个免费包各自的未执行项）——
   两个档位都没实现它们，绝不能因为"买断档打开了汇总"就让买家以为这些项被跑了。 */
const SUB_CHECKS_WITHHELD = [];
for (const m of MEMBERS) {
  for (const w of (m.entry.CHECKS_WITHHELD || [])) SUB_CHECKS_WITHHELD.push(`${m.label}：${w}`);
}

const TOTAL_SUB_CHECKS = MEMBERS.reduce((n, m) => n + (m.entry.CHECKS_GIVEN || []).length, 0);

const OUT_OF_SCOPE = [
  '判断这笔费用该不该报、该不该资本化、预提/摊销年限是否合理（属于会计判断与公司制度，请咨询会计师或审计师）',
  '代替审计程序、代替发票真伪查验，或出具鉴证意见与审计意见（只做表内/表间的算术与勾稽核对）',
  '判断预算额度定得合不合理、超支要不要调整预算（那是预算编制与审批的事）',
  '读取财务软件 / 费控系统 / ERP 的导出文件（需要你先导出成文本，每个客户一个目录）',
  '判断费用科目、部门归属、分摊口径是否正确（本工具只核你给的表内数字与表间勾稽关系）',
];

/* 样例 = 14 个成员检查包各自的最小完整样例（各自带表头，用 `=== 检查项 ===` 分段）。
   注意：报销单合规预检那一项的样例本身是一份**同一张发票号出现两次的报销底稿**
   （重复报销线索），所以它按自身规则会报出 1 条 P0（这是该成员样例的真实结论，不是误报）；
   其余 13 项在各自样例上都是 0 条发现。 */
const SAMPLE_TEXT = MEMBERS
  .map((m) => `=== ${m.label} ===\n${m.entry.SAMPLE_TEXT}`)
  .join('\n\n');

/* 有一处硬伤的样例：把「预提费用与到票冲销核对」里 12月水电费 的期末预提余额
   从 20000.00 改成 25000.00（期初 18000 + 本期计提 20000 − 到票冲销 18000 = 20000，与 25000 不符）
   ⇒ 必须报出来，并带**原文行号**（明细行 + 合计行各一条）。 */
const DIRTY_FROM = '12月水电费\t18000.00\t20000.00\t18000.00\t20000.00';
const DIRTY_TO = '12月水电费\t18000.00\t20000.00\t18000.00\t25000.00';
const DIRTY_TEXT = SAMPLE_TEXT.replace(DIRTY_FROM, DIRTY_TO);

/* 只覆盖 3 项的样例：用来演示"材料只覆盖了一部分"时，批量壳**明确报一条**，
   而不是把"跑了 3 项"说成"14 项都核过了"。 */
const PARTIAL_TITLES = ['预提费用与到票冲销核对', '运费对账', '长期待摊费用摊销核对'];
const PARTIAL_TEXT = SAMPLE_TEXT.split(/(?=^=== )/m)
  .filter((s) => PARTIAL_TITLES.some((t) => s.trim().indexOf(`=== ${t} ===`) === 0))
  .join('\n');

/* 批量样例：3 个客户（干净 / 有一处硬伤 / 没交材料），用来演示"一次跑完所有客户"。 */
const SAMPLE_OBJECTS = [
  { name: '豫州商贸有限公司（2026-02 费用结账）', files: [{ name: '费用与预算材料.txt', text: SAMPLE_TEXT }] },
  { name: '中岳建材有限公司（2026-02 费用结账）', files: [{ name: '费用与预算材料.txt', text: DIRTY_TEXT }] },
  { name: '缺料客户（只登记未交材料）', files: [] },
];

/** 内置样例**本身带有发现**（报销单合规预检那一项的成员样例就是一份重复发票号的报销底稿）。
 *  这是**显式声明**、不是放水：`strip_free_engine` 的烟测对"样例必须是 0 发现"的包要求声明这个常量，
 *  否则会把"样例真实报出了问题"误判成"改动把包改坏了"。其余 13 项在各自样例上都是 0 发现。 */
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
 *  ⚠️ 这里**保留段内空行**（不像老版本那样先过滤掉），并且同时准备两种行号索引：
 *    · `lines` / `lineNos`        —— 段内原文（保留空行），行号与之一一对应；
 *    · `flatLines` / `flatLineNos` —— 去掉空行后的文本与行号。
 *  为什么两种都要留：实测本包成员引擎的行号口径**分成两类** ——
 *    ① 13 个表格成员按"去空行后的第几条"记行号（它们的 parseTable 内部会 filter 空行）；
 *    ② `报销单合规预检` 是**单据型**引擎，靠段内空行把「报销单 / 发票」分成多张单据
 *      （`collectMaterial` 用 `split(/\n[ \t]*\n+/)`）—— 把空行过滤掉，它就只剩一张"单据 1"，
 *      发票要素完整性那项检查会被**静默跳过**（不是报错，是悄悄少做一项）。
 *  所以段文本按**原文**交给成员引擎（表格成员自己会滤空行，行为不变），
 *  行号落位时再按口径 ① 用 `flatLineNos` 复算（见 mapMemberLine）。 */
function sectionsOfFile(f) {
  const lines = String(f.text === undefined || f.text === null ? '' : f.text).split(/\r?\n/);
  const out = [];
  let cur = { title: '', lines: [], lineNos: [] };
  const flush = () => {
    const keep = [];
    const nos = [];
    const flat = [];
    const flatNos = [];
    for (let i = 0; i < cur.lines.length; i += 1) {
      keep.push(cur.lines[i]);
      nos.push(cur.lineNos[i]);
      if (String(cur.lines[i]).trim() !== '') {
        flat.push(cur.lines[i]);
        flatNos.push(cur.lineNos[i]);
      }
    }
    if (flat.length) {
      out.push({
        title: cur.title, file: f.name,
        lines: keep, lineNos: nos, text: keep.join('\n'),
        flatLines: flat, flatLineNos: flatNos, flatText: flat.join('\n'),
        startLine: flatNos[0],
        has_inner_blank: keep.length !== flat.length,
      });
    }
  };
  for (let i = 0; i < lines.length; i += 1) {
    const m = lines[i].match(/^\s*===\s*(.+?)\s*===\s*$/);
    if (m) {
      flush();
      cur = { title: m[1].trim(), lines: [], lineNos: [] };
      continue;
    }
    cur.lines.push(lines[i]);
    cur.lineNos.push(i + 1);
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

/** 入参归一化成"客户列表"：`{text}` 是单客户，`{objects:[…]}`（或 `{clients:[…]}`）是批量。 */
function normalizeObjects(payload) {
  const raw = [];
  const list = Array.isArray(payload.objects) ? payload.objects
    : (Array.isArray(payload.clients) ? payload.clients : null);
  if (list) {
    for (const o of list) {
      if (!o) continue;
      raw.push({ name: String(o.name || o.object || o.client || '').trim(), files: coerceFiles(o) });
    }
  }
  if (payload.text !== undefined || payload.content !== undefined) {
    raw.push({
      name: String(payload.object_name || payload.object || payload.client_name || payload.client
        || payload.name || '单客户').trim(),
      files: coerceFiles(payload),
    });
  }
  const out = [];
  raw.forEach((o, i) => out.push({ name: o.name || `客户${i + 1}`, files: o.files }));
  return out;
}

/** 覆盖缺口检查：客户交了材料，但只覆盖了一部分检查项 ⇒ **明确报一条**，
 *  不能因为"跑了几项"就以为 14 项都核过了。整份材料都没交的客户不在这里报（那是客户级的"未执行"）。 */
function checkClientCoverage(it) {
  const ran = it.checks.filter((c) => c.status === 'ok');
  const notRun = it.checks.filter((c) => c.status !== 'ok');
  if (!ran.length || !notRun.length) return null;
  return {
    level: 'P2',
    category: '检查项未执行（材料只覆盖了一部分）',
    line: 1,
    message: `客户「${it.client}」的材料只覆盖了 ${ran.length} / ${it.checks.length} 个费用与预算检查项，`
      + `未执行的是：${notRun.map((c) => c.check).join('、')} —— 这些项这次**没有核**，请补齐材料后重跑。`,
  };
}

/** 把成员引擎报的行号**落回原文文件行**（用于结论里的"原文文件与行号"）。
 *
 *  为什么不能直接 `lineNos[f.line - 1]`：成员引擎的行号口径**实测不统一** ——
 *  13 个表格成员把行号记成"**去掉空行后**的第几条"（它们的 parseTable 内部先 filter 空行），
 *  而 `报销单合规预检` 与 `运费对账` 的口径又不一样（前者按分段后的单据内行号、后者按含空行的行位置）。
 *  直接查表会**整体错位**：错行号比没有行号更糟 —— 买家按行号找回原文会看到别的记录。
 *
 *  所以落位**以原文内容为准**：
 *    ① 用 evidence 片段按**行首**在原文里找出所有候选行；
 *    ② 候选唯一 ⇒ 直接用它；
 *    ③ 候选多行（同一片段重复出现）⇒ 取距"成员行号所对应的分段行"最近的那一行；
 *    ④ 片段缺失或对不上 ⇒ 按**口径 ①**用 `flatLineNos` 复算（表格成员的通行口径）；
 *      连去空行行号都越界 ⇒ 如实退回该分段的首行。
 *  这样"对得上"的成员行为完全不变，只有口径不同的成员被纠正到原文行，且绝不编造行号。 */
function evidenceKey(ev) {
  if (Array.isArray(ev)) return String(ev[0] === undefined || ev[0] === null ? '' : ev[0]).trim().slice(0, 15);
  const s = String(ev === undefined || ev === null ? '' : ev).trim();
  if (s.indexOf('\n') >= 0) return s.split('\n')[0].trim().slice(0, 15);
  return s.slice(0, 15);
}

function mapMemberLine(f, cand) {
  /* 汇总级结论（成员自己把行号记成 0）没有具体行 —— 如实指向本分段的首行，
     不要按 evidence 去挑一行（那会让买家以为那行有问题）。 */
  if (!f.line) return cand.startLine;
  const key = evidenceKey(f.evidence);
  const rows = cand.lines;
  if (key) {
    const hits = [];
    for (let i = 0; i < rows.length; i += 1) {
      if (String(rows[i]).trim().slice(0, 15) === key) hits.push(i);
    }
    if (hits.length === 1) return cand.lineNos[hits[0]];
    if (hits.length > 1) {
      let best = hits[0];
      for (const i of hits) {
        const bi = (best + 1) - f.line;
        const ii = (i + 1) - f.line;
        if (Math.abs(ii) < Math.abs(bi) || (Math.abs(ii) === Math.abs(bi) && i < best)) best = i;
      }
      return cand.lineNos[best];
    }
  }
  const flat = cand.flatLineNos[f.line - 1];
  if (flat !== undefined) return flat;
  const direct = cand.lineNos[f.line - 1];
  return direct === undefined ? cand.startLine : direct;
}

/** 让一个成员引擎认一段材料；认不出来（insufficient_input / 抛错）就返回 null，绝不编造。 */
function memberOn(m, cand) {
  let out = null;
  try { out = m.entry.run({ text: cand.text }); } catch (e) { out = null; }
  if (out && out.status === 'success' && out.result) return { result: out.result, missing: null };
  const miss = (out && out.missing) || null;
  return { result: null, missing: Array.isArray(miss) && miss.length ? miss : null };
}

/** 先把"谁认哪一段"整张矩阵算出来（派发用），再按内容落位。 */
function buildRecognition(candidates) {
  const recog = candidates.map(() => MEMBERS.map(() => null));
  for (let ci = 0; ci < candidates.length; ci += 1) {
    for (let mi = 0; mi < MEMBERS.length; mi += 1) {
      recog[ci][mi] = memberOn(MEMBERS[mi], candidates[ci]);
    }
  }
  const community = candidates.map((c, ci) => recog[ci].filter((r) => r && r.result).length);
  return { recog: recog, community: community };
}

/** 给第 mi 个成员挑出"它该读的那一段材料"。
 *
 *  为什么不能只按顺序取"第一个跑通的段"：实测本包 14 个成员里有两位是**宽松**引擎 ——
 *    · `报销单合规预检` 是单据型引擎，只要正文够长就给 success（它不看表头）；
 *    · `运费对账` 在「车队油耗与运费核对」那张表上也会 success（两张表都有"运费"列）。
 *  只取第一个成功的段 ⇒ 报销单被安到别的表上、运费对账挑错表，**结论会挂在错误的检查项下**。
 *
 *  落位规则（内容优先）：
 *    ① 分段标题 === 本成员 label ⇒ 直接用（材料按 `=== 检查项 ===` 分段时的正解）；
 *    ② 标题写着**别的成员**名字的段一律不用（那是那一位的表）；
 *    ③ 其余候选里取"**认它的成员最少**"的那一段（越小越具体：只有它认得的表最可能是它的表），
 *      同分按出现顺序升序。
 *  ③ 让"14 张表拆成 14 个文件、没有 `=== 检查项 ===` 标题"这种放法也能正确派发。 */
function pickCandidate(mi, candidates, recog, community) {
  const mine = MEMBERS[mi].label;
  const labels = MEMBERS.map((m) => m.label);
  const pool = [];
  for (let ci = 0; ci < candidates.length; ci += 1) {
    if (!recog[ci][mi] || !recog[ci][mi].result) continue;
    const t = candidates[ci].title;
    if (t && t !== mine && labels.indexOf(t) >= 0) continue;   // 标题写着别的成员的名字 ⇒ 不是我的表
    pool.push(ci);
  }
  for (const ci of pool) if (candidates[ci].title === mine) return ci;
  if (!pool.length) return -1;
  return pool.slice().sort((a, b) => (community[a] - community[b]) || (a - b))[0];
}

/** 一个客户跑完全部 14 项；每一项的实际规则在 parts/ 里（本文件一行规则都没改）。
 *  一项都认不出来 ⇒ 这一项如实标 `not_run` 并列出还缺哪个表头，**绝不算它跑过**。 */
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
      reason: '没有收到这个客户的可用材料（材料为空或只有几行）',
    };
  }

  const seen = buildRecognition(candidates);
  const recog = seen.recog;
  const checks = [];
  const findings = [];
  const notRun = [];
  for (let mi = 0; mi < MEMBERS.length; mi += 1) {
    const m = MEMBERS[mi];
    const pick = pickCandidate(mi, candidates, recog, seen.community);
    if (pick < 0) {
      notRun.push(m.label);
      let bestMissing = null;
      for (let ci = 0; ci < candidates.length; ci += 1) {
        const miss = recog[ci][mi] && recog[ci][mi].missing;
        if (miss && (!bestMissing || miss.length < bestMissing.length)) bestMissing = miss;
      }
      checks.push({
        check: m.label, status: 'not_run', findings: 0,
        missing: bestMissing || ['这个客户的材料里没有这一项需要的表头行'],
      });
      continue;
    }
    const cand = candidates[pick];
    const result = recog[pick][mi].result;
    const per = (result.findings || []).map((f) => {
      const lineNo = mapMemberLine(f, cand);
      return {
        level: f.level,
        category: f.category,
        line: f.line,
        object: object.name,
        check: m.label,
        section: cand.title,
        source_file: cand.file,
        source_line: lineNo,
        evidence: `${cand.file}:${lineNo}`,
        message: f.message,
      };
    });
    for (const f of per) findings.push(f);
    checks.push({
      check: m.label, status: 'ok', findings: per.length,
      section: cand.title || cand.file,
    });
  }

  /* 批量壳自己的检查项：材料只覆盖了一部分检查项时，明确报一条
     （别把"跑了 3 项"说成"14 项都核过了"）。 */
  const cover = checkClientCoverage({ client: object.name, checks: checks });
  if (cover) {
    findings.push(Object.assign({}, cover, {
      object: object.name, check: '（批量壳）', section: '',
      source_file: '', source_line: 0, evidence: '客户级',
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
    reason: anyRan ? '' : '材料里没有任何一项能被认出的表（每个 `=== 检查项 ===` 分段的第一行要是表头行）',
  };
}

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  if (!payload) {
    return insufficient([
      '一个客户的材料都没收到（objects[] 与 text 都是空）',
      '单客户用 {"text":"…"}；批量用 {"objects":[{"name":"客户名","files":[{"name":"材料.txt","text":"…"}]}]}',
    ]);
  }
  const objects = normalizeObjects(payload);
  if (!objects.length) {
    return insufficient([
      '一个客户的材料都没收到（objects[] 与 text 都是空）',
      '每个客户一个子目录，目录里放该客户的一套费用与预算材料（每项用 `=== 检查项 ===` 分段，Tab 分隔最稳）',
    ]);
  }

  const rows = objects.map(runOneObject);
  const usable = rows.filter((r) => r.status === 'ok');
  if (!usable.length) {
    return insufficient(
      [`全部 ${rows.length} 个客户都没有可用材料（每个客户目录里要有该客户的费用与预算材料，且每张表要有表头行）`]
        .concat(rows.map((r) => `客户「${r.object}」：没有可用材料`)),
      '把每个客户的材料放进各自子目录后再跑；材料不足时本工具不做任何认定、也不给任何结论。');
  }

  const findings = [];
  for (const r of rows) for (const f of r.findings) findings.push(f);
  findings.sort((a, b) => (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)
    || (a.line - b.line) || String(a.category).localeCompare(String(b.category)));

  const lv = countLevels(findings);
  const withIssues = rows.filter((r) => r.findings.length > 0).length;
  const notRunObjects = rows.filter((r) => r.status !== 'ok').length;

  const result = {
    service_type: 'FEE_BUDGET_PACK',
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
    note: `本次对 ${rows.length} 个客户逐个跑了 ${CHECKS_GIVEN.length} 个费用与预算检查项（每个成员包内部还有 `
      + `${TOTAL_SUB_CHECKS / CHECKS_GIVEN.length} 项子检查）；未执行的检查项见 scope.checks_not_run 与 `
      + 'scope.sub_checks_not_run。',
    disclaimer: '只把各客户材料里的表内/表间算术与勾稽核一遍，结论都带**原文文件与行号**、可由第三方复算；'
      + '**不代替审计、不出具鉴证意见**，也不判断这笔费用该不该报、该不该资本化。',
  };

  /* 分层：完整档多一层跨客户汇总台账；免费档只报**实际执行**的那 14 项 */
    result.checks_executed = CHECKS_GIVEN.slice();
    result.checks_withheld = CHECKS_WITHHELD.slice();
  

  return { status: 'success', result: result };
}

module.exports = {
  run, runOneObject, normalizeObjects, coerceFiles, sectionsOfFile, countLevels, checkClientCoverage, CHECKS_GIVEN, CHECKS_WITHHELD, SUB_CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, SAMPLE_OBJECTS, DIRTY_TEXT, PARTIAL_TEXT, MEMBERS, SAMPLE_HAS_FINDINGS,
};
