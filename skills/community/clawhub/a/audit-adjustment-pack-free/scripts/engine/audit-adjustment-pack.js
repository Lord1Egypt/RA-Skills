'use strict';
/**
 * audit-adjustment-pack-full.js —— 审计与账务调整技能包（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须用它：**会计师事务所的审计助理 / 项目经理、企业财务的报表编制与复核岗，
 * 在年度审计与专项审计的"调整分录汇总、报表项目复核"这些固定节点上**。要核的从来不是一张表，
 * 而是一整套互相关联的审计与账务调整底稿：试算平衡、审计调整分录、资产减值准备、资产处置损益、
 * 固定资产折旧、无形资产摊销、模具摊销、坏账准备、预提费用、预付款核销、长期待摊费用摊销、
 * 存货跌价准备、现金盘点长短款、罚款与违约金结算 —— 每张表都有自己的勾稽关系，
 * **逐张手核既慢又容易漏**，而且每个被审计单位、每一期都要重复一遍；
 * 调整分录借贷不平、减值或折旧算错、盘亏挂账不处理，后果都比多花半小时严重得多。
 *
 * 这个包做的事**只有一件**（不是重写任何规则）：把仓库里**已有的 14 个审计与账务调整检查引擎**
 * 装进一个批量壳里，`--input <目录>`（每个子目录 = 一个被审计单位 / 一套底稿）一次跑完所有单位，
 * **每个被审计单位一行结论**。
 *   规则来源：`scripts/engine/parts/<检查项>/`（**逐字节拷贝**自那 14 个免费包，一行都没改；
 *   本包只做"目录 → 被审计单位 → 逐项派发"的编排与汇总）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约（与仓库其它引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *     payload.text            单单位：该单位的一套审计调整底稿文本（每项用 `=== 检查项 ===` 分段）
 *     payload.objects[]       多单位：{name, files:[{name, text}]} —— 每个子目录 = 一个被审计单位
 *   CHECKS_GIVEN / CHECKS_WITHHELD   免费档执行 / 不执行的检查项（免费包据此如实列出未执行项）
 *   CHECKS_OUT_OF_SCOPE              本能力**根本不做**的判断（边界诚实）
 *   SAMPLE_TEXT / SAMPLE_OBJECTS     样例（免费包 --sample / --sample-batch 用它自检）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），
 * **不读环境变量**，**不写任何文件**（结果只打到 stdout）。
 * ⚠️ 材料不足**绝不给结论**：某个单位没材料就单独标"未执行"，一个单位都跑不了就整体不给结论。
 * ⚠️ 本工具**不代替审计、不出鉴证意见**，也不判断某项调整分录该不该做、金额该不该审定。
 */

const MEMBERS = [
  {
    label: '试算平衡与科目余额核对',
    id: 'trial-balance-check',
    entry: require('./parts/trial-balance-check/trial-balance-check.js'),
  },
  {
    label: '审计调整分录核对',
    id: 'audit-adjustment-check',
    entry: require('./parts/audit-adjustment-check/audit-adjustment-check.js'),
  },
  {
    label: '资产减值准备核对',
    id: 'asset-impairment-check',
    entry: require('./parts/asset-impairment-check/asset-impairment-check.js'),
  },
  {
    label: '资产处置损益核对',
    id: 'asset-disposal-check',
    entry: require('./parts/asset-disposal-check/asset-disposal-check.js'),
  },
  {
    label: '固定资产折旧核对',
    id: 'depreciation-check',
    entry: require('./parts/depreciation-check/depreciation-check.js'),
  },
  {
    label: '无形资产摊销核对',
    id: 'intangible-amortization-check',
    entry: require('./parts/intangible-amortization-check/intangible-amortization-check.js'),
  },
  {
    label: '模具摊销核对',
    id: 'mold-amortization-check',
    entry: require('./parts/mold-amortization-check/mold-amortization-check.js'),
  },
  {
    label: '坏账准备计提核对',
    id: 'bad-debt-provision-check',
    entry: require('./parts/bad-debt-provision-check/bad-debt-provision-check.js'),
  },
  {
    label: '预提费用核对',
    id: 'accrual-expense-check',
    entry: require('./parts/accrual-expense-check/accrual-expense-check.js'),
  },
  {
    label: '预付款与预付账款核销核对',
    id: 'prepayment-offset-check',
    entry: require('./parts/prepayment-offset-check/prepayment-offset-check.js'),
  },
  {
    label: '长期待摊费用摊销核对',
    id: 'long-term-amortization-check',
    entry: require('./parts/long-term-amortization-check/long-term-amortization-check.js'),
  },
  {
    label: '存货跌价准备核对',
    id: 'inventory-provision-check',
    entry: require('./parts/inventory-provision-check/inventory-provision-check.js'),
  },
  {
    label: '现金盘点与长短款核对',
    id: 'cash-count-check',
    entry: require('./parts/cash-count-check/cash-count-check.js'),
  },
  {
    label: '罚款与违约金结算核对',
    id: 'penalty-settlement-check',
    entry: require('./parts/penalty-settlement-check/penalty-settlement-check.js'),
  },
];

/* 免费档执行：14 个审计与账务调整检查项，逐个被审计单位全跑一遍（免费层的核心产出：一次跑完所有单位） */
const CHECKS_GIVEN = MEMBERS.map((m) => m.label);

/* 完整档追加（**多一种能力**，不是多几个数）：跨被审计单位汇总台账 —— 单单位结果里根本不存在的东西 */
const CHECKS_WITHHELD = [
  '跨被审计单位汇总台账（全部单位 × 全部 14 项检查合并成一张总表）',
  '账务调整风险排序清单（按 P0/P1/P2 排序，带被审计单位名与原文文件行号）',
  '跨单位共性问题归类（同一问题命中 2 个及以上被审计单位时合并成一条共性项）',
  '审计调整台账导出（Markdown 与 CSV 文本，直接用于调整分录汇总与复核说明附件）',
];

/* 如实列出**每个成员检查包自己**没做的子检查（那 14 个免费包各自的未执行项）——
   两个档位都没实现它们，绝不能因为"买断档打开了汇总"就让使用者以为这些项被跑了。 */
const SUB_CHECKS_WITHHELD = [];
for (const m of MEMBERS) {
  for (const w of (m.entry.CHECKS_WITHHELD || [])) SUB_CHECKS_WITHHELD.push(`${m.label}：${w}`);
}

const TOTAL_SUB_CHECKS = MEMBERS.reduce((n, m) => n + (m.entry.CHECKS_GIVEN || []).length, 0);

const OUT_OF_SCOPE = [
  '判断某项审计调整分录该不该做、调整金额是否恰当（属于会计判断，请按企业会计准则、审计准则与项目复核意见执行）',
  '判断被审计单位的会计政策与会计估计变更是否合理（本工具只核你给的表内数字与表间勾稽关系）',
  '代替审计程序、出具审计意见或鉴证报告（只做表内/表间的算术与勾稽核对，不获取也不评价审计证据）',
  '判断重要性水平、调整门槛与未更正错报的汇总口径（请按审计计划确定的重要性水平执行）',
  '核对原始凭证、合同、发票、银行回单、盘点记录的真伪，或比对财务系统/审计软件的逐行明细',
  '读取财务系统 / ERP / 审计软件的导出文件（需要你先导出成文本，每个被审计单位一个目录）',
];

/* 逐字节拷贝进来的 14 个成员引擎，各自在自己的样例上必须**0 条发现**。
   这里在加载时实测一遍并把"样例自带发现"的成员如实记下来（不是放水，是声明）：
   真出现了这种成员，`SAMPLE_HAS_FINDINGS` 会变成 true，测试会当场把名字打出来。 */
const MEMBER_SAMPLE_FINDINGS = [];
for (const m of MEMBERS) {
  let bad = false;
  try {
    const o = m.entry.run({ text: m.entry.SAMPLE_TEXT });
    bad = !(o && o.status === 'success')
      || (((o.result || {}).findings) || []).length > 0;
  } catch (e) {
    bad = true;
  }
  if (bad) MEMBER_SAMPLE_FINDINGS.push(m.id);
}

/* 样例 = 14 个成员检查包各自的最小完整样例（各自带表头，用 `=== 检查项 ===` 分段）。 */
const SAMPLE_TEXT = MEMBERS
  .map((m) => `=== ${m.label} ===\n${m.entry.SAMPLE_TEXT}`)
  .join('\n\n');

/* 有一处硬伤的样例：把「试算平衡与科目余额核对」里 1001 库存现金那一行的**期末余额**从 25000.00
   改成 24000.00（期初 20000.00 + 本期借方 20000.00 − 本期贷方 15000.00 = 25000.00，与 24000 不符，
   连带期末余额合计也不再为 0）⇒ 必须报出来，并带**原文行号**。 */
const DIRTY_FROM = '1001\t库存现金\t资产\t20000.00\t20000.00\t15000.00\t25000.00';
const DIRTY_TO = '1001\t库存现金\t资产\t20000.00\t20000.00\t15000.00\t24000.00';
const DIRTY_TEXT = SAMPLE_TEXT.replace(DIRTY_FROM, DIRTY_TO);

/* 只覆盖 3 项的样例：用来演示"材料只覆盖了一部分"时，批量壳**明确报一条**，
   而不是把"跑了 3 项"说成"14 项都核过了"。 */
const PARTIAL_TITLES = ['试算平衡与科目余额核对', '固定资产折旧核对', '坏账准备计提核对'];
const PARTIAL_TEXT = SAMPLE_TEXT.split(/(?=^=== )/m)
  .filter((s) => PARTIAL_TITLES.some((t) => s.trim().indexOf(`=== ${t} ===`) === 0))
  .join('\n');

/* 批量样例：3 个被审计单位（干净 / 有一处硬伤 / 没交材料），用来演示"一次跑完所有单位"。 */
const SAMPLE_OBJECTS = [
  { name: '豫州制造有限公司（2026 年度审计调整）', files: [{ name: '审计调整底稿.txt', text: SAMPLE_TEXT }] },
  { name: '中岳建设有限公司（2026 年度审计调整）', files: [{ name: '审计调整底稿.txt', text: DIRTY_TEXT }] },
  { name: '缺料单位（只登记未交底稿）', files: [] },
];

/** 内置样例**不含发现**（每个成员引擎都已在自己的样例上自证 0 条发现）。
 *  这个常量是给守卫读的**显式声明**，不是放水。 */
const SAMPLE_HAS_FINDINGS = MEMBER_SAMPLE_FINDINGS.length > 0;

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

/** 把一份底稿按 `=== 检查项 ===` 分段，并**记住每一行来自哪个文件第几行**（结论要能回到原文）。
 *  成员引擎内部都把空行过滤掉、行号按过滤后的顺序算，所以这里也先过滤空行再交给引擎，
 *  并同步保留原始行号 —— 否则回原文件时会错行。 */
function sectionsOfFile(f) {
  const lines = String(f.text === undefined || f.text === null ? '' : f.text).split(/\r?\n/);
  const out = [];
  let cur = { title: '', lines: [], lineNos: [] };
  const flush = () => {
    const keep = [];
    const nos = [];
    for (let i = 0; i < cur.lines.length; i += 1) {
      if (String(cur.lines[i]).trim() !== '') {
        keep.push(cur.lines[i]);
        nos.push(cur.lineNos[i]);
      }
    }
    if (keep.length) {
      out.push({
        title: cur.title, file: f.name, text: keep.join('\n'),
        lineNos: nos, startLine: nos[0],
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

/** 入参归一化成"被审计单位列表"：`{text}` 是单单位，`{objects:[…]}`（或 `{clients:[…]}`）是批量。 */
function normalizeObjects(payload) {
  const raw = [];
  const list = Array.isArray(payload.objects) ? payload.objects
    : (Array.isArray(payload.clients) ? payload.clients
      : (Array.isArray(payload.projects) ? payload.projects : null));
  if (list) {
    for (const o of list) {
      if (!o) continue;
      raw.push({ name: String(o.name || o.object || o.client || '').trim(), files: coerceFiles(o) });
    }
  }
  if (payload.text !== undefined || payload.content !== undefined) {
    raw.push({
      name: String(payload.object_name || payload.object || payload.client_name || payload.client
        || payload.name || '单单位').trim(),
      files: coerceFiles(payload),
    });
  }
  const out = [];
  raw.forEach((o, i) => out.push({ name: o.name || `单位${i + 1}`, files: o.files }));
  return out;
}

/** 覆盖缺口检查：单位交了底稿，但只覆盖了一部分检查项 ⇒ **明确报一条**，
 *  不能因为"跑了几项"就以为 14 项都核过了。整份底稿都没交的单位不在这里报（那是单位级的"未执行"）。 */
function checkClientCoverage(it) {
  const ran = it.checks.filter((c) => c.status === 'ok');
  const notRun = it.checks.filter((c) => c.status !== 'ok');
  if (!ran.length || !notRun.length) return null;
  return {
    level: 'P2',
    category: '检查项未执行（材料只覆盖了一部分）',
    line: 1,
    message: `被审计单位「${it.client}」的底稿只覆盖了 ${ran.length} / ${it.checks.length} 个审计与账务调整检查项，`
      + `未执行的是：${notRun.map((c) => c.check).join('、')} —— 这些项这次**没有核**，请补齐材料后重跑。`,
  };
}

/** 把成员引擎报的行号**落回原文文件行**（用于结论里的"原文文件与行号"）。
 *
 *  为什么不能直接 `lineNos[f.line - 1]`：成员引擎的行号口径**实测不统一**（有的把行号记成原文里的
 *  行位置、含表头，有的只算数据行），而本包的分段恰好把空行与 `=== 检查项 ===` 标题行去掉了 ⇒
 *  直接查表会**整体错位**。错行号比没有行号更糟 —— 使用者按行号找回原文会看到别的记录。
 *
 *  所以落位**以原文内容为准**：成员给的 evidence 行首片段必须在原文里真的能对上。
 *    ① 用 evidence 片段按**行首**在原文里找出所有候选行；
 *    ② 候选唯一 ⇒ 直接用它；
 *    ③ 候选多行（同一片段重复出现）⇒ 取距"成员行号所对应的分段行"最近的那一行；
 *    ④ 片段缺失或对不上（单位级/汇总级结论）⇒ 如实退回该分段的首行。
 *  这样"对得上"的成员行为完全不变，只有口径不同的成员被纠正到原文行，且绝不编造行号。 */
function evidenceKey(ev) {
  if (Array.isArray(ev)) return String(ev[0] === undefined || ev[0] === null ? '' : ev[0]).trim().slice(0, 15);
  const s = String(ev === undefined || ev === null ? '' : ev).trim();
  if (s.indexOf('\n') >= 0) return s.split('\n')[0].trim().slice(0, 15);
  return s.slice(0, 15);
}

function mapMemberLine(f, cand) {
  const direct = cand.lineNos[f.line - 1];
  const key = evidenceKey(f.evidence);
  const rows = String(cand.text).split('\n');       // 与 lineNos 一一对应（sectionsOfFile 已过滤空行）
  /* 汇总级结论（成员自己把行号记成 0）没有具体行 —— 如实指向本分段的首行，
     不要按 evidence 去挑一行（那会让使用者以为那行有问题）。 */
  if (!f.line) return cand.startLine;
  if (!key) return direct === undefined ? cand.startLine : direct;
  const hits = [];
  for (let i = 0; i < rows.length; i += 1) {
    if (String(rows[i]).trim().slice(0, 15) === key) hits.push(i);
  }
  if (!hits.length) return direct === undefined ? cand.startLine : direct;
  if (hits.length === 1) return cand.lineNos[hits[0]];
  let best = hits[0];
  for (const i of hits) {
    const bi = (best + 1) - f.line;
    const ii = (i + 1) - f.line;
    if (Math.abs(ii) < Math.abs(bi) || (Math.abs(ii) === Math.abs(bi) && i < best)) best = i;
  }
  return cand.lineNos[best];
}

/* 台账层挂载点：**默认什么都不做**（免费档就是这样）。
   完整档在自己的付费块里把它定义成真正的台账实现（函数声明提升，run() 里引用不会报未定义）。 */
function ledger_hook() {}

/** 一个单位跑完全部 14 项；每一项的实际规则在 parts/ 里（本文件一行规则都没改）。
 *  派发方式（**先认段名、再认内容**）：
 *    ① 优先喂给**分段名等于本检查项名**的那一段（`=== 固定资产折旧核对 ===`）；
 *    ② 没有同名段、或同名段跑不通时，再按文件顺序依次试其它段，**第一个跑通的段**才是这一项的表；
 *    ③ 一段都跑不通 ⇒ 这一项如实标 `not_run` 并列出还缺哪个表头，**绝不算它跑过**。
 *  为什么要有①（实测撞出来的真缺陷）：好几张审计底稿的列名会互相"认得上"
 *  （处置损益表里也有「原值 / 累计折旧 / 账面净值」，折旧引擎会把它当成自己的表），
 *  纯按内容顺序派发会让某项跑在**别人的表**上 ⇒ 分段名与检查项名对不上，结论张冠李戴。
 *  先同名、再兜底，既不改任何成员规则，也不许"跑不通也硬算跑过"。 */
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
      reason: '没有收到这个单位的可用底稿（材料为空或只有几行）',
    };
  }

  const checks = [];
  const findings = [];
  const notRun = [];
  for (const m of MEMBERS) {
    /* ① 先试同名段（标题逐字等于本检查项名）；② 再按文件顺序兜底试其余段。 */
    const ordered = candidates.filter((c) => c.title === m.label)
      .concat(candidates.filter((c) => c.title !== m.label));
    let hit = null;
    let bestMissing = null;
    for (const cand of ordered) {
      let out = null;
      try { out = m.entry.run({ text: cand.text }); } catch (e) { out = null; }
      if (out && out.status === 'success' && out.result) { hit = { cand: cand, result: out.result }; break; }
      const miss = (out && out.missing) || [];
      if (Array.isArray(miss) && miss.length && (!bestMissing || miss.length < bestMissing.length)) {
        bestMissing = miss;
      }
    }
    if (!hit) {
      notRun.push(m.label);
      checks.push({
        check: m.label, status: 'not_run', findings: 0,
        missing: bestMissing || ['这个单位的底稿里没有这一项需要的表头行'],
      });
      continue;
    }
    const per = (hit.result.findings || []).map((f) => {
      const lineNo = mapMemberLine(f, hit.cand);
      return {
        level: f.level,
        category: f.category,
        line: f.line,
        object: object.name,
        check: m.label,
        section: hit.cand.title,
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
    });
  }

  /* 批量壳自己的检查项：底稿只覆盖了一部分检查项时，明确报一条
     （别把"跑了 3 项"说成"14 项都核过了"）。 */
  const cover = checkClientCoverage({ client: object.name, checks: checks });
  if (cover) {
    findings.push(Object.assign({}, cover, {
      object: object.name, check: '（批量壳）', section: '',
      source_file: '', source_line: 0, evidence: '单位级',
    }));
  }

  const lv = countLevels(findings);
  const anyRan = checks.some((c) => c.status === 'ok');
  const row = {
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
    reason: anyRan ? '' : '底稿里没有任何一项能被认出的表（每个 `=== 检查项 ===` 分段的第一行要是表头行）',
  };

  /* 这一行有没有被真正核对过（有底稿、且至少有一项能跑）⇒ 才够格进跨单位汇总台账。
     免费档与完整档都用它：台账只收"真跑过"的单位行，没交材料的单位不进总表。 */
  row.ledger_member = false;   // 由完整档的台账层置位；免费档恒为 false

  return row;
}

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  if (!payload) {
    return insufficient([
      '一个被审计单位的底稿都没收到（objects[] 与 text 都是空）',
      '单单位用 {"text":"…"}；批量用 {"objects":[{"name":"单位名","files":[{"name":"底稿.txt","text":"…"}]}]}',
    ]);
  }
  const objects = normalizeObjects(payload);
  if (!objects.length) {
    return insufficient([
      '一个被审计单位的底稿都没收到（objects[] 与 text 都是空）',
      '每个被审计单位一个子目录，目录里放该单位的一套审计调整底稿（每项用 `=== 检查项 ===` 分段，Tab 分隔最稳）',
    ]);
  }

  const rows = objects.map((o) => runOneObject(o));
  const usable = rows.filter((r) => r.status === 'ok');
  if (!usable.length) {
    return insufficient(
      [`全部 ${rows.length} 个被审计单位都没有可用底稿（每个单位目录里要有该单位的审计调整底稿，且每张表要有表头行）`]
        .concat(rows.map((r) => `被审计单位「${r.object}」：没有可用底稿`)),
      '把每个单位的审计调整底稿放进各自子目录后再跑；材料不足时本工具不做任何认定、也不给任何结论。');
  }

  const findings = [];
  for (const r of rows) for (const f of r.findings) findings.push(f);
  findings.sort((a, b) => (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)
    || (a.line - b.line) || String(a.category).localeCompare(String(b.category)));

  const lv = countLevels(findings);
  const withIssues = rows.filter((r) => r.findings.length > 0).length;
  const notRunObjects = rows.filter((r) => r.status !== 'ok').length;   // run() 里的 rows 就是全部单位

  const result = {
    service_type: 'AUDIT_ADJUSTMENT_PACK',
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
    note: `本次对 ${rows.length} 个被审计单位逐个跑了 ${CHECKS_GIVEN.length} 个审计与账务调整检查项（每个成员包内部还有 `
      + `${TOTAL_SUB_CHECKS} 项子检查）；未执行的检查项见 scope.checks_not_run 与 `
      + 'scope.sub_checks_not_run。',
    disclaimer: '只把各单位底稿里的表内/表间算术与勾稽核一遍，结论都带**原文文件与行号**、可由第三方复算；'
      + '**不代替审计、不出具审计意见或鉴证报告**，也不判断某项调整分录该不该做、金额该不该审定。',
  };

  /* 分层：
     · 免费档（免费包里就是下面这两行 + 再下面那句 return，付费块被整块摘掉）：
       只报**实际执行**的那 14 项，未执行项如实列出（说明文本，不是实现）。
     · 完整档（本文件）：在上面那层之上再挂一层跨被审计单位汇总台账
       （被审计单位 × 检查项总表、账务调整风险排序清单、共性问题归类、Markdown / CSV 导出）。 */
  result.checks_executed = CHECKS_GIVEN.concat();
  result.checks_withheld = CHECKS_WITHHELD.concat();

  /* 完整档：把跨被审计单位汇总台账挂到本次结果上。
     ledger_hook 在免费档里是空函数（免费包付费块整块不存在）⇒ 免费档永远挂不出 ledger。 */
  ledger_hook(result, findings, rows, payload);

  /* 免费档的出口：付费块被整块摘掉后直接走到这一句（完整档在上面那一支里已经挂好台账）。 */
  return { status: 'success', result: result };
}

module.exports = {
  run, runOneObject, normalizeObjects, coerceFiles, sectionsOfFile, countLevels, checkClientCoverage, CHECKS_GIVEN, CHECKS_WITHHELD, SUB_CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, SAMPLE_OBJECTS, DIRTY_TEXT, PARTIAL_TEXT, MEMBERS, SAMPLE_HAS_FINDINGS, MEMBER_SAMPLE_FINDINGS,
};
