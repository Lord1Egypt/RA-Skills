'use strict';
/**
 * ecom-platform-pack-full.js —— 电商与平台结算技能包（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须用它：**在电商平台卖货的商家、连锁/加盟品牌、商场联营专柜、餐饮门店、
 * 做直播与 OTA 的运营与财务岗，在每个结算周期对账之前**。
 * 要对的从来不是一张结算单，而是十几份互相关联的结算底稿：电商平台结算、退货退款与货款结算、
 * 平台账期与在途资金、直播佣金与坑位费、OTA 佣金与净结算、商场联营抽成与保底、加盟抽成与保底、
 * 连锁加盟门店结算、会员积分与储值卡核销、促销补贴与核销、采购返利与阶梯核算、
 * 整车厂返利与商务政策、寄售代销结算、餐饮门店日营业款 —— 每一份都有自己的勾稽关系，
 * **逐份手核既慢又容易漏**，而且月月重复；少算的那部分就是真金白银。
 *
 * 这个包做的事**只有一件**（不是重写任何规则）：把仓库里**已有的 14 个结算核对引擎**
 * 装进一个批量壳里，`--input <目录>`（每个子目录 = 一个客户 / 一套材料）一次跑完所有客户，
 * **每个客户一行结论**。
 *   规则来源：`scripts/engine/parts/<检查项>/`（**逐字节拷贝**自那 14 个免费包，一行都没改；
 *   本包只做"目录 → 客户 → 逐项派发"的编排与汇总）。
 *
 * 契约（与仓库其它引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *     payload.text            单客户：该客户的一套结算材料文本（每项用 `=== 检查项 ===` 分段）
 *     payload.objects[]       多客户：{name, files:[{name, text}]} —— 每个子目录 = 一个客户
 *   CHECKS_GIVEN / CHECKS_WITHHELD   本包执行 / 不执行的检查项（免费包据此如实列出未执行项）
 *   CHECKS_OUT_OF_SCOPE              本能力**根本不做**的判断（边界诚实）
 *   SAMPLE_TEXT / SAMPLE_OBJECTS     样例（免费包 --sample / --sample-batch 用它自检）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），
 * **不读环境变量**，**不写任何文件**（结果只打到 stdout）。
 * ⚠️ 材料不足**绝不给结论**：某个客户没材料就单独标"未执行"，一个客户都跑不了就整体不给结论。
 * ⚠️ 本工具**不代替审计、不出鉴证意见**，也不判断平台费率/抽成政策是否合理。
 */

const MEMBERS = [
  {
    label: '电商平台结算核对',
    id: 'platform-settlement-check',
    entry: require('./parts/platform-settlement-check/platform-settlement-check.js'),
  },
  {
    label: '退货退款与货款结算核对',
    id: 'ecommerce-refund-settlement-check',
    entry: require('./parts/ecommerce-refund-settlement-check/ecommerce-refund-settlement-check.js'),
  },
  {
    label: '平台账期与在途资金核对',
    id: 'platform-settlement-aging-check',
    entry: require('./parts/platform-settlement-aging-check/platform-settlement-aging-check.js'),
  },
  {
    label: '直播佣金与坑位费结算核对',
    id: 'live-commerce-commission-check',
    entry: require('./parts/live-commerce-commission-check/live-commerce-commission-check.js'),
  },
  {
    label: 'OTA佣金与净结算核对',
    id: 'ota-commission-check',
    entry: require('./parts/ota-commission-check/ota-commission-check.js'),
  },
  {
    label: '商场联营抽成与保底核对',
    id: 'mall-concession-check',
    entry: require('./parts/mall-concession-check/mall-concession-check.js'),
  },
  {
    label: '加盟抽成与最低保底核对',
    id: 'franchise-royalty-check',
    entry: require('./parts/franchise-royalty-check/franchise-royalty-check.js'),
  },
  {
    label: '连锁加盟门店结算核对',
    id: 'chain-store-settlement-check',
    entry: require('./parts/chain-store-settlement-check/chain-store-settlement-check.js'),
  },
  {
    label: '会员积分与储值卡核销核对',
    id: 'retail-member-points-check',
    entry: require('./parts/retail-member-points-check/retail-member-points-check.js'),
  },
  {
    label: '促销补贴与核销核对',
    id: 'promo-subsidy-check',
    entry: require('./parts/promo-subsidy-check/promo-subsidy-check.js'),
  },
  {
    label: '采购返利与阶梯核算核对',
    id: 'purchase-rebate-check',
    entry: require('./parts/purchase-rebate-check/purchase-rebate-check.js'),
  },
  {
    label: '整车厂返利与商务政策核对',
    id: 'oem-rebate-policy-check',
    entry: require('./parts/oem-rebate-policy-check/oem-rebate-policy-check.js'),
  },
  {
    label: '寄售代销结算核对',
    id: 'consignment-settlement-check',
    entry: require('./parts/consignment-settlement-check/consignment-settlement-check.js'),
  },
  {
    label: '餐饮门店日营业款核对',
    id: 'restaurant-daily-sales-check',
    entry: require('./parts/restaurant-daily-sales-check/restaurant-daily-sales-check.js'),
  },
];

/* 本包执行：14 个电商与平台结算检查项，逐个客户全跑一遍（免费层的核心产出：一次跑完所有客户） */
const CHECKS_GIVEN = MEMBERS.map((m) => m.label);

/* 订阅版追加（**多一种能力**，不是多几个数）：跨客户汇总台账 —— 单客户结果里根本不存在的东西 */
const CHECKS_WITHHELD = [
  '跨客户汇总台账（全部客户 × 全部 14 项检查合并成一张总表）',
  '结算差异风险排序清单（按 P0/P1/P2 排序，带客户名与原文文件行号）',
  '跨客户共性问题归类（同一问题命中 2 个及以上客户时合并成一条共性项）',
  '电商与平台结算台账导出（Markdown 与 CSV 文本，直接用于与平台/商场对账说明）',
];

/* 如实列出**每个成员检查包自己**没做的子检查（那 14 个免费包各自的未执行项）——
   两个档位都没实现它们，绝不能因为"买断档打开了汇总"就让买家以为这些项被跑了。 */
const SUB_CHECKS_WITHHELD = [];
for (const m of MEMBERS) {
  for (const w of (m.entry.CHECKS_WITHHELD || [])) SUB_CHECKS_WITHHELD.push(`${m.label}：${w}`);
}

const TOTAL_SUB_CHECKS = MEMBERS.reduce((n, m) => n + (m.entry.CHECKS_GIVEN || []).length, 0);

const OUT_OF_SCOPE = [
  '判断平台佣金率、商场抽成比例、返利与补贴政策定得合不合理（那是商务谈判与平台/商场规则的事）',
  '核对平台 / 商场 / 加盟商是否真的打了款（那要拿银行流水来对）',
  '核对商品是否真的发出、退货是否真实、积分与储值卡是否真的被用掉（那要拿订单、物流与消费流水比）',
  '代替审计程序，或出具鉴证意见与审计意见（只做表内/表间的算术与勾稽核对）',
  '读取平台后台 / OTA / 商场系统 / POS / 会员系统的导出文件（需要你先导出成文本，每个客户一个目录）',
  '判断积分兑换率、储值卡核销口径、加盟抽成政策、返利阶梯是否最新（本工具只核你给的表内数字与表间勾稽关系）',
];

/* 样例 = 14 个成员检查包各自的最小完整样例（各自带表头，用 `=== 检查项 ===` 分段）。
   ⚠️ 这 14 份样例**各自都是干净稿**（跑在成员引擎上 0 条发现），所以不需要"程序化修好"那一步。 */
const SAMPLE_TEXT = MEMBERS
  .map((m) => `=== ${m.label} ===\n${m.entry.SAMPLE_TEXT}`)
  .join('\n\n');

/* 有一处硬伤的样例：把「电商平台结算核对」里 SO-003 那一行的结算金额改成 460.00
   （销售额 500 − 佣金 25 − 技术服务费 5 − 运费 8 − 退款 0 = 462，与 460 不符）
   ⇒ 必须报出来，并带**原文行号**（同时合计行也会对不上 ⇒ 两条发现）。 */
const DIRTY_FROM = 'SO-003\t500.00\t25.00\t5.00\t8.00\t0.00\t462.00';
const DIRTY_TO = 'SO-003\t500.00\t25.00\t5.00\t8.00\t0.00\t460.00';
const DIRTY_TEXT = SAMPLE_TEXT.replace(DIRTY_FROM, DIRTY_TO);

/* 只覆盖 3 项的样例：用来演示"材料只覆盖了一部分"时，批量壳**明确报一条**，
   而不是把"跑了 3 项"说成"14 项都核过了"。 */
const PARTIAL_TITLES = ['电商平台结算核对', '商场联营抽成与保底核对', '餐饮门店日营业款核对'];
const PARTIAL_TEXT = SAMPLE_TEXT.split(/(?=^=== )/m)
  .filter((s) => PARTIAL_TITLES.some((t) => s.trim().indexOf(`=== ${t} ===`) === 0))
  .join('\n');

/* 批量样例：3 个客户（干净 / 有一处硬伤 / 没交材料），用来演示"一次跑完所有客户"。 */
const SAMPLE_OBJECTS = [
  { name: '豫州电商旗舰店（2026-02 结算）', files: [{ name: '电商与平台结算材料.txt', text: SAMPLE_TEXT }] },
  { name: '中岳百货联营专柜（2026-02 结算）', files: [{ name: '电商与平台结算材料.txt', text: DIRTY_TEXT }] },
  { name: '缺料客户（只登记未交材料）', files: [] },
];

/** 内置样例**不含发现**（14 份成员样例各自都是干净稿，实测 0 条发现）。
 *  这个常量是给守卫读的**显式声明**，不是放水。 */
const SAMPLE_HAS_FINDINGS = false;

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
    message: `客户「${it.client}」的材料只覆盖了 ${ran.length} / ${it.checks.length} 个电商与平台结算检查项，`
      + `未执行的是：${notRun.map((c) => c.check).join('、')} —— 这些项这次**没有核**，请补齐材料后重跑。`,
  };
}

/** 把成员引擎报的行号**落回原文文件行**（用于结论里的"原文文件与行号"）。
 *
 *  为什么不能直接 `lineNos[f.line - 1]`：成员引擎的行号口径**实测不统一**（有的把行号记成原文里的
 *  行位置、含表头，有的只算数据行），而本包的分段恰好把空行与 `=== 检查项 ===` 标题行去掉了 ⇒
 *  直接查表会**整体错位**。错行号比没有行号更糟 —— 买家按行号找回原文会看到别的记录。
 *
 *  所以落位**以原文内容为准**：成员给的 evidence 行首片段必须在原文里真的能对上。
 *    ① 用 evidence 片段按**行首**在原文里找出所有候选行；
 *    ② 候选唯一 ⇒ 直接用它；
 *    ③ 候选多行（同一片段重复出现）⇒ 取距"成员行号所对应的分段行"最近的那一行；
 *    ④ 片段缺失或对不上（对象级/汇总级结论）⇒ 如实退回该分段的首行或成员原始行号。
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
     不要按 evidence 去挑一行（那会让买家以为那行有问题）。 */
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

/* 台账层挂载点：**默认什么都不做**（本包就是这样）。
   完整档在自己的付费块里把它定义成真正的台账实现（函数声明提升，run() 里引用不会报未定义）。 */
function ledger_hook() {}

/** 订阅版判据：只认入参里的 full / credit / token 开关（不读环境变量、不靠模块级状态）。 */
function payload_is_full(p) {
  return Boolean(p && typeof p === 'object' && (p.full || p.credit || p.token));
}

/** 一个客户跑完全部 14 项；每一项的实际规则在 parts/ 里（本文件一行规则都没改）。
 *  派发方式：把该客户的每一段材料依次喂给成员引擎，**第一个跑通的段**就是这一项的表；
 *  一段都跑不通 ⇒ 这一项如实标 `not_run` 并列出还缺哪个表头，**绝不算它跑过**。 */
function runOneObject(object, it) {
  const _opt = (it && typeof it === 'object') ? it : {};
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

  const checks = [];
  const findings = [];
  const notRun = [];
  for (const m of MEMBERS) {
    let hit = null;
    let bestMissing = null;
    for (const cand of candidates) {
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
        missing: bestMissing || ['这个客户的材料里没有这一项需要的表头行'],
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
    reason: anyRan ? '' : '材料里没有任何一项能被认出的表（每个 `=== 检查项 ===` 分段的第一行要是表头行）',
  };

  /* 这一行有没有被真正核对过（有材料、且至少有一项能跑）⇒ 才够格进跨客户汇总台账。
     免费档与完整档都用它：台账只收"真跑过"的客户行，没交材料的客户不进总表。 */
  row.ledger_member = false;   // 由完整档的台账层置位；免费档恒为 false

  return row;
}

/* ===== 以下为订阅版才执行的检查 ===== */

/** 订阅版档位标记：本引擎（`*-full.js`）只装在买断包里，**有条件跑订阅版**。
 *  免费包里这一行被 strip_free_engine.py 删掉，`run.mjs` 里也不会有 `full: true` ⇒ 两档口径一致。
 *  ⚠️ 它不参与任何运行时判断（档位由"买家装了哪个包"决定），只作为档位口径的显式声明。 */
const paid = true;
/* ⚠️ 这一整块（MARKER 到 run 函数之间）免费包里**不存在**：`tools/strip_free_engine.py`
   会把它整块摘掉，并删掉因此没人引用的函数。
   所以免费引擎里既没有这些台账函数，`runOneObject` 里也没有挂台账的那一支 —— 免费档没有 ledger。 */

/** 台账的风险级别排序权重（P0 最先处理）。 */
const LEVEL_ORDER = { P0: 0, P1: 1, P2: 2 };

function levelRank(level) {
  return LEVEL_ORDER[level] === undefined ? 9 : LEVEL_ORDER[level];
}

function itemRank(f) {
  return levelRank(f.level);
}

function csvCell(v) {
  const s = (v === undefined || v === null) ? '' : String(v);
  return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

/** 跨客户汇总台账：**客户 × 检查项总表 + 结算差异风险排序清单 + 共性问题归类 + 导出**。
 *  这是订阅版在"逐客户跑 14 项"之上**多出来的那一层能力**（本包的 result 里根本没有 ledger）。
 *
 *  ⚠️ 入参是**全部客户行**（含没交材料的）：总表/风险清单/共性/处理项只收"真跑过"的行，
 *  但「没交材料的客户」必须能在台账第四节里被点名 —— 否则买家会以为台账覆盖了全部客户。
 *  同仓的 `payroll-hr-pack` 在这里只传了跑过的行 ⇒ `not_run_objects` 恒为空（台账第四节白写）。 */
function buildLedger(allRows) {
  const rows = allRows.filter((r) => r.status === 'ok');
  const matrix = rows.map((r) => ({
    object: r.object,
    verdict: r.verdict,
    status: r.status,
    total: r.total, p0: r.p0, p1: r.p1, p2: r.p2,
    checks: r.checks.map((c) => ({
      check: c.check, status: c.status, findings: c.findings || 0,
    })),
  }));

  /* 风险排序清单：按 P0 → P1 → P2，同级按客户与原文行号（可复算，不靠排序的偶然稳定性） */
  const riskQueue = [];
  for (const r of rows) {
    for (const f of r.findings) {
      riskQueue.push({
        object: f.object, level: f.level, check: f.check, category: f.category,
        source_file: f.source_file, source_line: f.source_line, evidence: f.evidence,
        message: f.message,
      });
    }
  }
  riskQueue.sort((a, b) => (levelRank(a.level) - levelRank(b.level))
    || (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)
    || (a.source_line - b.source_line)
    || String(a.category).localeCompare(String(b.category)));

  /* 跨客户共性问题归类：同一问题类别命中 2 个及以上客户 ⇒ 合并成一条共性项
     （一个客户算错是操作问题，十个客户同一类别算错是口径或模板问题 —— 只有跨客户视角才看得到） */
  const byCategory = new Map();
  for (const r of rows) {
    const seen = new Set();
    for (const f of r.findings) {
      const key = `${f.level}|${f.category}`;
      if (seen.has(key)) continue;
      seen.add(key);
      if (!byCategory.has(key)) {
        byCategory.set(key, { category: f.category, level: f.level, check: f.check, objects: [], samples: [] });
      }
      const g = byCategory.get(key);
      g.objects.push(f.object);
      if (g.samples.length < 3) g.samples.push(`${f.object}｜${f.evidence}｜${f.message}`);
    }
  }
  const commonIssues = [];
  for (const g of byCategory.values()) {
    if (g.objects.length >= 2) {
      commonIssues.push({
        category: g.category, level: g.level, check: g.check,
        objects: g.objects.slice(), count: g.objects.length, samples: g.samples.slice(),
      });
    }
  }
  commonIssues.sort((a, b) => (b.objects.length - a.objects.length)
    || (levelRank(a.level) - levelRank(b.level))
    || String(a.category).localeCompare(String(b.category)));

  /* 需要处理的客户（有材料、且有问题要处理） */
  const actionItems = [];
  for (const r of rows) {
    if (r.status !== 'ok' || !r.findings.length) continue;
    const top = r.findings.slice().sort((a, b) => itemRank(a) - itemRank(b))[0];
    actionItems.push({
      object: r.object, verdict: r.verdict, total: r.total, p0: r.p0, p1: r.p1, p2: r.p2,
      top: top ? { level: top.level, check: top.check, category: top.category, evidence: top.evidence } : null,
    });
  }

  const counts = countLevels(riskQueue);
  const notRunObjects = allRows.filter((r) => r.status !== 'ok').map((r) => r.object);
  const ledger = {
    matrix: matrix,
    risk_queue: riskQueue,
    common_issues: commonIssues,
    action_items: actionItems,
    not_run_objects: notRunObjects,
    counts: counts,
    markdown: '',
    csv: ledgerCsv(riskQueue),
  };
  ledger.markdown = ledgerMarkdown(ledger);
  return ledger;
}

function ledgerMarkdown(L) {
  const out = [];
  out.push('# 电商与平台结算技能包 · 跨客户汇总台账');
  out.push('');
  out.push(`客户数 ${L.matrix.length}｜结算差异条目 ${L.risk_queue.length} 条`
    + `（P0 ${L.counts.p0} / P1 ${L.counts.p1} / P2 ${L.counts.p2}）`
    + `｜共性问题 ${L.common_issues.length} 条｜需要处理的客户 ${L.action_items.length} 个`);
  out.push('');
  out.push('## 一、客户 × 检查项总表');
  out.push('');
  out.push('| 客户 | ' + CHECKS_GIVEN.join(' | ') + ' | 结论 | 问题数 |');
  out.push('| --- |' + CHECKS_GIVEN.map(() => ' --- |').join('') + ' --- | --- |');
  for (const m of L.matrix) {
    const cells = m.checks.map((c) => {
      if (c.status !== 'ok') return '未执行';
      return c.findings ? `有问题(${c.findings})` : '通过';
    });
    out.push(`| ${m.object} | ${cells.join(' | ')} | ${m.verdict} | ${m.total} |`);
  }
  out.push('');
  out.push('## 二、结算差异风险排序清单（P0 → P1 → P2）');
  out.push('');
  if (!L.risk_queue.length) {
    out.push('（本次没有需要处理的结算差异条目 —— 这只说明所给材料的表内勾稽对得上，'
      + '不代表平台/商场真的结了款、也不代表费率与政策合理。）');
  } else {
    out.push('| 级别 | 客户 | 检查项 | 问题类别 | 来源 | 结论 |');
    out.push('| --- | --- | --- | --- | --- | --- |');
    for (const f of L.risk_queue) {
      out.push(`| ${f.level} | ${f.object} | ${f.check} | ${f.category} | ${f.evidence || '客户级'} | ${f.message} |`);
    }
  }
  out.push('');
  out.push('## 三、跨客户共性问题归类（命中 2 个及以上客户）');
  out.push('');
  if (!L.common_issues.length) {
    out.push('（本次没有共性问题；同一类别只命中一个客户时不算共性。）');
  } else {
    for (const c of L.common_issues) {
      out.push(`- [${c.level}] ${c.category}（${c.check}）：命中 ${c.count} 个客户 —— ${c.objects.join('、')}`);
      for (const s of c.samples) out.push(`  · ${s}`);
    }
  }
  out.push('');
  out.push('## 四、未执行项（如实列出，别当成"已核"）');
  out.push('');
  out.push('本版本不包含：');
  for (const w of CHECKS_WITHHELD) out.push(`- ${w}`);
  out.push('');
  out.push('成员检查包本身未实现：');
  for (const w of SUB_CHECKS_WITHHELD) out.push(`- ${w}`);
  if (L.not_run_objects.length) {
    out.push('');
    out.push(`没交材料的客户（这次一项都没跑）：${L.not_run_objects.join('、')}`);
  }
  out.push('');
  return out.join('\n');
}

function ledgerCsv(riskQueue) {
  const head = ['客户', '级别', '检查项', '问题类别', '来源文件', '来源行', '原文行号', '结论'];
  const lines = [head.join(',')];
  for (const f of riskQueue) {
    lines.push([f.object, f.level, f.check, f.category, f.source_file, f.source_line,
      f.source_line, f.message].map(csvCell).join(','));
  }
  return lines.join('\n');
}

/* 订阅版专用：把「跨客户汇总台账」挂到本次结果上（客户 × 检查项总表、结算差异风险排序清单、
   共性问题归类、Markdown / CSV 导出）。免费包里这一整块不存在 ⇒ 那里 ledger_hook 是空函数。 */
function ledger_hook(result, findings, rows, payload) {
  if (!paid) return;
  for (const r of rows) if (r.status === 'ok') r.ledger_member = true;
  /* 传**全部行**：buildLedger 自己只把跑过的行放进总表，同时把没交材料的客户列进第四节。 */
  const ledger = buildLedger(rows);
  result.ledger = ledger;
  result.checks_executed = CHECKS_GIVEN.concat(CHECKS_WITHHELD);
  result.checks_withheld = [];
  for (const a of ledger.action_items) {
    findings.push({
      level: a.p0 > 0 ? 'P0' : 'P1',
      category: '电商与平台结算台账处理项（汇总台账）',
      line: 0,
      object: a.object,
      check: '（完整档）跨客户汇总台账',
      section: '',
      source_file: '',
      source_line: 0,
      evidence: '客户级',
      message: `客户「${a.object}」本次有 ${a.total} 条需要处理的条目（P0 ${a.p0} / P1 ${a.p1} / P2 ${a.p2}）`
        + (a.top ? `：最先处理 [${a.top.level}] ${a.top.check}｜${a.top.category}（${a.top.evidence}）。` : '。'),
    });
  }
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
      '每个客户一个子目录，目录里放该客户的一套电商与平台结算材料'
        + '（每项用 `=== 检查项 ===` 分段，Tab 分隔最稳）',
    ]);
  }

  const rows = objects.map((o) => runOneObject(o, payload));
  const usable = rows.filter((r) => r.status === 'ok');
  if (!usable.length) {
    return insufficient(
      [`全部 ${rows.length} 个客户都没有可用材料（每个客户目录里要有该客户的一套电商与平台结算材料，`
        + '且每张表要有表头行）']
        .concat(rows.map((r) => `客户「${r.object}」：没有可用材料`)),
      '把每个客户的结算材料放进各自子目录后再跑；材料不足时本工具不做任何认定、也不给任何结论。');
  }

  const findings = [];
  for (const r of rows) for (const f of r.findings) findings.push(f);
  findings.sort((a, b) => (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)
    || (a.line - b.line) || String(a.category).localeCompare(String(b.category)));

  const lv = countLevels(findings);
  const withIssues = rows.filter((r) => r.findings.length > 0).length;
  const notRunObjects = rows.filter((r) => r.status !== 'ok').length;

  const result = {
    service_type: 'ECOM_PLATFORM_SETTLEMENT_PACK',
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
    note: `本次对 ${rows.length} 个客户逐个跑了 ${CHECKS_GIVEN.length} 个电商与平台结算检查项（每个成员包内部还有 `
      + `${TOTAL_SUB_CHECKS / CHECKS_GIVEN.length} 项子检查）；未执行的检查项见 scope.checks_not_run 与 `
      + 'scope.sub_checks_not_run。',
    disclaimer: '只把各客户材料里的表内/表间算术与勾稽核一遍，结论都带**原文文件与行号**、可由第三方复算；'
      + '**不代替审计、不出具鉴证意见**，也不判断平台佣金率、商场抽成比例、返利与补贴政策是否合理。',
  };

  /* 分层：
     · 免费档（免费包里就是下面这两行 + 再下面那句 return，付费块被整块摘掉）：
       只报**实际执行**的那 14 项，未执行项如实列出（说明文本，不是实现）。
     · 完整档（本文件）：在上面那层之上再挂一层跨客户汇总台账
       （客户 × 检查项总表、结算差异风险排序清单、跨客户共性问题归类、Markdown / CSV 导出）。 */
  result.checks_executed = CHECKS_GIVEN.concat();
  result.checks_withheld = CHECKS_WITHHELD.concat();

  /* 订阅版：把跨客户汇总台账挂到本次结果上。
     ledger_hook 在免费档里是空函数（免费包付费块整块不存在）⇒ 免费档永远挂不出 ledger。 */
  ledger_hook(result, findings, rows, payload);

  /* 本包的出口：付费块被整块摘掉后直接走到这一句（订阅版在上面那一支里已经挂好台账）。 */
  return { status: 'success', result: result };
}

module.exports = {
  run, runOneObject, normalizeObjects, coerceFiles, sectionsOfFile, countLevels, checkClientCoverage,
  buildLedger, ledgerMarkdown, ledgerCsv, evidenceKey, mapMemberLine,
  CHECKS_GIVEN, CHECKS_WITHHELD, SUB_CHECKS_WITHHELD, OUT_OF_SCOPE,
  SAMPLE_TEXT, SAMPLE_OBJECTS, DIRTY_TEXT, PARTIAL_TEXT, MEMBERS, SAMPLE_HAS_FINDINGS,
};
