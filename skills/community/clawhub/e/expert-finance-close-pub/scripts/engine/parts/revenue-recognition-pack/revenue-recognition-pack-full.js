'use strict';
/**
 * revenue-recognition-pack.js —— 收入确认与结算技能包（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须用它：**软件 / 内容 / 服务型公司的收入会计与项目财务**，在**每月收入确认与结算之前**。
 * 收入侧最容易出错的不是"有没有这笔钱"，而是**该确认多少、什么时候确认**：
 * SaaS 订阅的合同金额与已确认收入、软件许可的授权期与摊销、版税与保底的分成结算、
 * 门店销售报表与收款方式合计、租金账单与免租期、分期收款的本金与利息拆分、
 * 应收催收计划的账龄与承诺回款 —— 每一项都有明确算式，但**逐项目手核既慢又容易漏**，而且月月重复。
 * 同时管着**多个项目 / 多个产品线**时，真正要做的事是"**一次跑完所有项目，每个项目一行结论**"。
 *
 * 这个包做的事**只有一件**（不是重写任何规则）：把仓库里**已有的 7 个收入确认检查引擎**
 * 装进一个批量壳里，`--input <目录>`（每个子目录 = 一家项目 / 一套材料）一次跑完所有项目，
 * **每家项目一行结论**。
 *   检查项：SaaS 订阅收入确认核对、版税与保底分成结算核对、软件许可与授权期摊销核对、门店销售报表与收款方式核对、租金账单与免租期核对、分期收款本金与利息拆分核对、应收催收计划与账龄核对。
 *   规则来源：`scripts/engine/parts/<检查项>/`（**逐字节拷贝**自那 7 个免费包，一行都没改；
 *   本包只做"目录 → 项目 → 逐项派发"的编排与汇总，外加订阅版的跨项目汇总台账）。
 * * ⚠️ 本文件在**免费壳**里是子集：付费实现会被 `strip_free_engine.py` 剥掉；
 * `CHECKS_WITHHELD` 只是"未执行的能力"的**说明文本**，不是实现。
 *
 * 契约（与仓库其它引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *     payload.text            单项目：这家项目的一套材料文本（每项用 `=== 检查项 ===` 分段）
 *     payload.objects[]       多项目：{name, files:[{name, text}]} —— 每个子目录 = 一家项目
 *   CHECKS_GIVEN / CHECKS_WITHHELD   本包执行 / 不执行的检查项（免费包据此如实列出未执行项）
 *   CHECKS_OUT_OF_SCOPE              本能力**根本不做**的判断（边界诚实）
 *   SAMPLE_TEXT / SAMPLE_OBJECTS     样例（免费包 --sample / --sample-batch 用它自检）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），
 * **不读环境变量**，**不写任何文件**（结果只打到 stdout）。
 * ⚠️ 材料不足**绝不给结论**：某家项目没材料就单独标"未执行"，一家项目都跑不了就整体不给结论。
 * ⚠️ 本工具**不代替做账/审计/纳税申报、不出鉴证意见**，也不判断业务实质该怎么定。
 */

/* 7 个成员检查项的**中文名 / base 名 / 引擎**（引擎逐字节来自各自免费包，本包一行规则都没改） */
const MEMBERS = [
  {
    label: 'SaaS 订阅收入确认核对',
    id: 'saas-revenue-recognition-check',
    entry: require('./parts/saas-revenue-recognition-check/saas-revenue-recognition-check.js'),
  },
  {
    label: '版税与保底分成结算核对',
    id: 'royalty-settlement-check',
    entry: require('./parts/royalty-settlement-check/royalty-settlement-check.js'),
  },
  {
    label: '软件许可与授权期摊销核对',
    id: 'software-license-check',
    entry: require('./parts/software-license-check/software-license-check.js'),
  },
  {
    label: '门店销售报表与收款方式核对',
    id: 'store-sales-report-check',
    entry: require('./parts/store-sales-report-check/store-sales-report-check.js'),
  },
  {
    label: '租金账单与免租期核对',
    id: 'rent-collection-check',
    entry: require('./parts/rent-collection-check/rent-collection-check.js'),
  },
  {
    label: '分期收款本金与利息拆分核对',
    id: 'installment-rate-check',
    entry: require('./parts/installment-rate-check/installment-rate-check.js'),
  },
  {
    label: '应收催收计划与账龄核对',
    id: 'receivable-collection-plan-check',
    entry: require('./parts/receivable-collection-plan-check/receivable-collection-plan-check.js'),
  },
];

/* 本包执行：7 个收入确认检查项，逐家项目全跑一遍（免费层的核心产出：一次跑完所有项目） */
const CHECKS_GIVEN = MEMBERS.map((m) => m.label);

/* 订阅版追加（**多一种能力**，不是多几个数）：跨项目汇总台账 —— 单项目结果里根本不存在的东西 */
const CHECKS_WITHHELD = [
  '跨项目汇总台账（全部项目 × 全部 7 项核对合并成一张总表）',
  '收入风险排序清单（按 P0/P1/P2 排序，带项目名与原文文件行号）',
  '跨项目共性问题归类（同一个问题命中 2 个及以上项目时合并成一条共性项）',
  '收入台账导出（Markdown 与 CSV 文本，直接用于月度收入复核说明）',
];

/* 如实列出**每个成员检查包自己**没做的子检查（那 7 个免费包各自的未执行项）——
   两个档位都没实现它们，绝不能因为"买断档打开了汇总"就让买家以为这些项被跑了。 */
const SUB_CHECKS_WITHHELD = [];
for (const m of MEMBERS) {
  for (const w of (m.entry.CHECKS_WITHHELD || [])) SUB_CHECKS_WITHHELD.push(`${m.label}：${w}`);
}

const TOTAL_SUB_CHECKS = MEMBERS.reduce((n, m) => n + (m.entry.CHECKS_GIVEN || []).length, 0);

const OUT_OF_SCOPE = [
  '判断收入该按哪个准则、在哪个时点确认（属于**会计判断**，请按公司会计政策与准则执行）',
  '代替审计或出具鉴证意见（只做表内/表间的算术与勾稽核对）',
  '核对银行回单、平台账单、合同签署的真实性，或比对业务系统 / 收款平台的逐行明细',
  '读取 CRM / 计费系统 / 收款平台的导出文件（需要你先导出成文本，每个项目一个目录）',
  '判断某项收入是否要交税、按什么税率交（属于税务判断，请咨询税务师）',
];

/* 样例 = 7 个成员检查包各自的最小完整样例（各自带表头，用 `=== 检查项 ===` 分段）。
   这 7 份样例**都是干净稿**（生成时逐项自证过 0 条发现，见 SAMPLE_HAS_FINDINGS）。 */
const SAMPLE_TEXT = MEMBERS
  .map((m) => `=== ${m.label} ===\n${m.entry.SAMPLE_TEXT}`)
  .join('\n\n');

/* 有一处硬伤的样例：把「SaaS 订阅收入确认核对」的合计行里 `180000.00` 改成 `180100.00`（各明细行相加 ≠ 合计）⇒ 必须报出来，并带**原文行号**（第 6 行）。 */
const DIRTY_FROM = '合计			180000.00				160000.00	180000.00	40000.00	300000.00		';
const DIRTY_TO = '合计			180100.00				160000.00	180000.00	40000.00	300000.00		';
const DIRTY_TEXT = SAMPLE_TEXT.replace(DIRTY_FROM, DIRTY_TO);

/* 只覆盖 3 项的样例：用来演示"材料只覆盖了一部分"时，批量壳**明确报一条**，
   而不是把"跑了 3 项"说成"7 项都核过了"。 */
const PARTIAL_TITLES = [
  'SaaS 订阅收入确认核对',
  '租金账单与免租期核对',
  '门店销售报表与收款方式核对',
];
const PARTIAL_TEXT = SAMPLE_TEXT.split(/(?=^=== )/m)
  .filter((s) => PARTIAL_TITLES.some((t) => s.trim().indexOf(`=== ${t} ===`) === 0))
  .join('\n');

/* 批量样例：3 家项目（干净 / 有一处硬伤 / 没交材料），用来演示"一次跑完所有项目"。 */
const SAMPLE_OBJECTS = [
  { name: '豫州云服务项目（2026-04 收入确认）', files: [{ name: '收入材料.txt', text: SAMPLE_TEXT }] },
  { name: '中岳内容平台项目（2026-04 收入确认）', files: [{ name: '收入材料.txt', text: DIRTY_TEXT }] },
  { name: '缺料项目（只登记未交材料）', files: [] },
];

/** 内置样例**不含发现**（7 份成员样例都是干净稿，生成时逐项自证过 0 条发现）。
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

/** 入参归一化成"项目列表"：`{text}` 是单项目，`{objects:[…]}`（或 `{orgs/clients:[…]}`）是批量。 */
function normalizeObjects(payload) {
  const raw = [];
  const list = Array.isArray(payload.objects) ? payload.objects
    : (Array.isArray(payload.orgs) ? payload.orgs
      : (Array.isArray(payload.clients) ? payload.clients : null));
  if (list) {
    for (const o of list) {
      if (!o) continue;
      raw.push({
        name: String(o.name || o.object || o.org || o.client || '').trim(),
        files: coerceFiles(o),
      });
    }
  }
  if (payload.text !== undefined || payload.content !== undefined) {
    raw.push({
      name: String(payload.object_name || payload.object || payload.org_name || payload.org
        || payload.client_name || payload.client || payload.name || '单项目').trim(),
      files: coerceFiles(payload),
    });
  }
  const out = [];
  raw.forEach((o, i) => out.push({ name: o.name || `项目${i + 1}`, files: o.files }));
  return out;
}

/** 覆盖缺口检查：项目交了材料，但只覆盖了一部分检查项 ⇒ **明确报一条**，
 *  不能因为"跑了几项"就以为 7 项都核过了。整份材料都没交的项目不在这里报（那是项目级的"未执行"）。 */
function checkClientCoverage(it) {
  const ran = it.checks.filter((c) => c.status === 'ok');
  const notRun = it.checks.filter((c) => c.status !== 'ok');
  if (!ran.length || !notRun.length) return null;
  return {
    level: 'P2',
    category: '检查项未执行（材料只覆盖了一部分）',
    line: 1,
    message: `项目「${it.client}」的材料只覆盖了 ${ran.length} / ${it.checks.length} 个收入确认检查项，`
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
 *    ④ 片段缺失或对不上（项目级/汇总级结论）⇒ 如实退回该分段的首行。
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

/** 一家项目跑完全部 7 项；每一项的实际规则在 parts/ 里（本文件一行规则都没改）。
 *  派发方式：把这家项目的每一段材料依次喂给成员引擎，**第一个跑通的段**就是这一项的表；
 *  一段都跑不通 ⇒ 这一项如实标 `not_run` 并列出还缺哪个表头，**绝不算它跑过**。 */
function runOneObject(object) {
  const live = object.files.filter((f) => String(f.text).trim() !== '');
  const candidates = [];
  for (const f of live) for (const s of sectionsOfFile(f)) candidates.push(s);
  const materialLines = live.reduce(
    (n, f) => n + String(f.text).split(/\r?\n/).filter((l) => l.trim() !== '').length, 0);

  if (!candidates.length || materialLines < 4) {
    return {
      object: object.name, status: 'insufficient_input', files: live.map((f) => f.name),
      material_lines: materialLines,
      checks: MEMBERS.map((m) => ({ check: m.label, status: 'not_run', findings: 0 })),
      findings: [], not_run: MEMBERS.map((m) => m.label),
      total: 0, p0: 0, p1: 0, p2: 0, verdict: 'NOT_RUN',
      reason: '没有收到这家项目的可用材料（材料为空或只有几行）',
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
        missing: bestMissing || ['这家项目的材料里没有这一项需要的表头行'],
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
     （别把"跑了 3 项"说成"7 项都核过了"）。 */
  const cover = checkClientCoverage({ client: object.name, checks: checks });
  if (cover) {
    findings.push(Object.assign({}, cover, {
      object: object.name, check: '（批量壳）', section: '',
      source_file: '', source_line: 0, evidence: '项目级',
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

  /* 这一行有没有被真正核对过（有材料、且至少有一项能跑）⇒ 才够格进跨项目汇总台账。
     免费档与完整档都用它：台账只收"真跑过"的项目行，没交材料的项目不进总表。 */
  row.ledger_member = false;   // 由完整档的台账层置位；免费档恒为 false

  return row;
}

/* 台账钩子（本包实现）：什么都不做。
   ⚠️ 完整档在**下面那个付费块里**重新声明同名函数 —— JS 函数声明提升 + 后定义覆盖，
      两档各只有一份生效的实现：免费包里生效的是这个空钩子，付费包里生效的是真台账。
      （`tools/strip_free_engine.py` 会整块删掉付费块，于是免费包只剩这一个空钩子。） */
function ledger_hook() { return false; }

/* ===== 以下为订阅版才执行的检查 ===== */

/** 订阅版判据用的开关名（按 key 取值，不做属性访问）。 */
const PAID_SWITCH_KEYS = ['full', 'credit', 'token'];

/** 订阅版判据：只认**入参里的开关**（不读环境变量、不靠模块级状态）。
 *  ⚠️ 判据在免费包里**整块被摘掉**（它在付费块内，run() 里也没有对它的引用），
 *     所以这里可以按 key 直取；只有 CHECKS_WITHHELD 的说明文字会留在免费包里。 */
function fullTierUnlocked(p) {
  /* ⛔ 这两句**字面量**判断不是冗余，是给仓库守卫认的"付费开关"指纹：
     `tier_channel_check.PAID_MARKERS` 与 `fix_buyout_tier.has_paid_gate` 都按
     `payload.full` / `payload.credit` 这样的**属性访问字面量**判断"这个引擎有没有付费档开关"。
     买断包的 run.mjs 会传 `full: true` —— 引擎里没有那个字面量时，守卫会判
     「引擎无付费开关却传了 full: true ⇒ 口径不一致」。所以这里按字面量写一遍，
     再用 key 列表兜住 `token`（等价语义，两边都成立）。 */
  if (p['full'] || p.full || p['credit'] || p.credit) return true;
  for (const k of PAID_SWITCH_KEYS) if (p[k]) return true;
  return false;
}


/* ------------------------------------------------------------------ *
 *  跨项目汇总台账（订阅版独有的一层能力）
 *
 *  本包把 7 项在**每一家项目内部**跑完就结束；订阅版在这些单项目结果**之上**再合一层：
 *    · matrix          项目 × 检查项总表（只收真跑过的项目，没交材料的不算"核过"）
 *    · risk_queue      收入确认风险排序清单（P0 → P1 → P2，同级按项目名 / 原文行号稳定排序）
 *    · common_issues   跨项目共性问题归类（同一问题命中 ≥2 家项目才合并成一条）
 *    · action_items    逐项目处理项（有问题的、或材料没跑全的项目各一条）
 *    · markdown / csv  台账导出文本（**只写 stdout，不落盘**）
 *  ⚠️ 这一整块会被 `tools/strip_free_engine.py --apply` 从免费包里整块摘掉，
 *     所以免费包**不存在**这些符号（守卫按实现符号核对，不看 CHECKS_WITHHELD 的说明文字）。
 * ------------------------------------------------------------------ */

/** Markdown 表格单元格转义（`|` 会截断表格）。 */
function mdCell(v) {
  return String(v === undefined || v === null ? '' : v).replace(/\|/g, '\\|').replace(/\n/g, ' ');
}

/** CSV 单元格：含逗号/引号/换行时加引号并把引号翻倍（RFC4180）。 */
function csvCell(v) {
  const s = String(v === undefined || v === null ? '' : v);
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

const LEVEL_ORDER = { P0: 0, P1: 1, P2: 2 };

/** 风险排序：级别 → 项目名 → 原文行号 → 类别（全序，结果可复现）。 */
function riskSort(a, b) {
  return (LEVEL_ORDER[a.level] === undefined ? 9 : LEVEL_ORDER[a.level])
    - (LEVEL_ORDER[b.level] === undefined ? 9 : LEVEL_ORDER[b.level])
    || (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)
    || (a.line - b.line)
    || String(a.category).localeCompare(String(b.category));
}

/** 项目 × 检查项总表：一行一家**真跑过**的项目，每行 7 个检查项的状态。 */
function ledgerMatrix(rows) {
  return rows.filter((r) => r.status === 'ok').map((r) => ({
    object: r.object,
    status: r.status,
    verdict: r.verdict,
    files: r.files.slice(),
    total: r.total,
    p0: r.p0, p1: r.p1, p2: r.p2,
    checks: r.checks.map((c) => ({
      check: c.check,
      status: c.status,
      findings: c.findings || 0,
      value: c.status === 'ok' ? (c.findings ? `有问题(${c.findings})` : '通过') : '未执行',
    })),
  }));
}

/** 跨项目共性问题：同一 category 命中 ≥2 家项目 ⇒ 合并成一条共性项（只命中 1 家不算共性）。 */
function ledgerCommonIssues(findings) {
  const byCat = {};
  for (const f of findings) {
    const k = String(f.category);
    if (!byCat[k]) byCat[k] = { category: k, level: f.level, objects: [], items: 0 };
    byCat[k].items += 1;
    if (byCat[k].objects.indexOf(f.object) < 0) byCat[k].objects.push(f.object);
    /* 同一类别里出现更严重的级别时，共性项取更严重的那一级（不掩盖 P0）。 */
    const cur = LEVEL_ORDER[byCat[k].level] === undefined ? 9 : LEVEL_ORDER[byCat[k].level];
    const nxt = LEVEL_ORDER[f.level] === undefined ? 9 : LEVEL_ORDER[f.level];
    if (nxt < cur) byCat[k].level = f.level;
  }
  return Object.keys(byCat).map((k) => byCat[k])
    .filter((c) => c.objects.length >= 2)
    .sort((a, b) => b.objects.length - a.objects.length
      || (LEVEL_ORDER[a.level] || 9) - (LEVEL_ORDER[b.level] || 9)
      || a.category.localeCompare(b.category));
}

/** 逐项目处理项：有问题的项目、或材料没跑全的项目，各给一条"接下来要做什么"。 */
function ledgerActionItems(rows) {
  const out = [];
  for (const r of rows) {
    if (r.status !== 'ok') {
      out.push({
        object: r.object, level: 'P1', kind: '材料未交齐',
        text: `项目「${r.object}」这次没有可用材料（${r.material_lines} 行），7 项一项都没跑 —— `
          + '请补齐这家项目的材料后重跑，不要按"没有问题"处理。',
      });
      continue;
    }
    const notRun = r.checks.filter((c) => c.status !== 'ok').map((c) => c.check);
    if (r.total > 0 || notRun.length) {
      out.push({
        object: r.object,
        level: r.p0 > 0 ? 'P0' : (r.total > 0 ? 'P1' : 'P2'),
        kind: r.total > 0 ? '有需要复核的发现' : '材料未覆盖全部检查项',
        text: `项目「${r.object}」本次核了 ${r.checks.length - notRun.length} / ${r.checks.length} 项，`
          + `发现 ${r.total} 条（P0 ${r.p0} / P1 ${r.p1} / P2 ${r.p2}）`
          + (notRun.length ? `；未执行的 ${notRun.length} 项：${notRun.join('、')}` : '')
          + ' —— 请按上面的风险清单逐条复核后再结账。',
      });
    }
  }
  return out;
}

/** 台账 Markdown：项目 × 检查项总表 + 风险排序清单 + 共性问题 + 逐项目处理项 + 如实列未执行项。 */
function ledgerMarkdown(result, matrix, riskQueue, commonIssues, actionItems, notRunObjects) {
  const notRun = notRunObjects || [];
  const L = [];
  L.push('# 收入确认与结算技能包 · 跨项目汇总台账');
  L.push('');
  L.push(`项目数 ${result.summary.objects}｜有问题 ${result.summary.objects_with_issues}｜`
    + `干净 ${result.summary.objects_clean}｜未执行（没交材料）${result.summary.objects_not_run}｜`
    + `发现合计 ${result.summary.total}（P0 ${result.summary.p0} / P1 ${result.summary.p1} / P2 ${result.summary.p2}）`);
  L.push('');
  L.push('## 项目 × 检查项总表');
  L.push('');
  L.push('| 项目 | 结论 | 问题数 | ' + CHECKS_GIVEN.join(' | ') + ' |');
  L.push('| --- | --- | --- | ' + CHECKS_GIVEN.map(() => '---').join(' | ') + ' |');
  for (const m of matrix) {
    L.push(`| ${mdCell(m.object)} | ${m.verdict} | ${m.total} | `
      + m.checks.map((c) => mdCell(c.value)).join(' | ') + ' |');
  }
  if (notRun.length) {
    L.push('');
    L.push('（以下项目这次没有可用材料，**不进总表**，也不当作"核过"：'
      + notRun.map(mdCell).join('、') + '）');
  }
  L.push('');
  L.push('## 收入确认风险排序清单');
  L.push('');
  if (!riskQueue.length) L.push('（本次没有发现，风险清单为空。）');
  for (const f of riskQueue) {
    L.push(`- [${f.level}] ${mdCell(f.object)}｜${mdCell(f.check)}｜${mdCell(f.evidence)}｜`
      + `${mdCell(f.category)}：${mdCell(f.message)}`);
  }
  L.push('');
  L.push('## 跨项目共性问题');
  L.push('');
  if (!commonIssues.length) L.push('（没有命中 2 家及以上项目的共性问题。）');
  for (const c of commonIssues) {
    L.push(`- [${c.level}] ${mdCell(c.category)}：命中 ${c.objects.length} 家 —— `
      + c.objects.map(mdCell).join('、'));
  }
  L.push('');
  L.push('## 逐项目处理项');
  L.push('');
  if (!actionItems.length) L.push('（本次所有项目都没有需要处理的事项。）');
  for (const a of actionItems) {
    L.push(`- [${a.level}] ${mdCell(a.object)}（${a.kind}）：${mdCell(a.text)}`);
  }
  L.push('');
  L.push('## 未执行项（如实列出）');
  L.push('');
  L.push('本版本不包含：' + (result.checks_withheld.length ? result.checks_withheld.join('；') : '（无）'));
  L.push('');
  L.push('成员检查包本身未实现：' + (result.scope.sub_checks_not_run.length
    ? result.scope.sub_checks_not_run.join('；') : '（无）'));
  L.push('');
  L.push(`口径：${result.disclaimer}`);
  return L.join('\n');
}

/** 台账 CSV：一行一条风险（项目,级别,检查项,问题类别,原文定位,说明）。 */
function ledgerCsv(riskQueue) {
  const head = '项目,级别,检查项,问题类别,原文定位,说明';
  return [head].concat(riskQueue.map((f) => [
    csvCell(f.object), csvCell(f.level), csvCell(f.check), csvCell(f.category),
    csvCell(f.evidence), csvCell(f.message),
  ].join(','))).join('\n');
}

/** 汇总台账组装：把单项目结果合并成订阅版独有的那一层。 */
function buildLedger(result, findings, rows) {
  const matrix = ledgerMatrix(rows);
  const riskQueue = findings.slice().sort(riskSort);
  const commonIssues = ledgerCommonIssues(findings);
  const actionItems = ledgerActionItems(rows);
  const notRun = rows.filter((r) => r.status !== 'ok').map((r) => r.object);
  const ledger = {
    matrix: matrix,
    risk_queue: riskQueue,
    common_issues: commonIssues,
    action_items: actionItems,
    not_run_objects: notRun,
    markdown: '',
    csv: ledgerCsv(riskQueue),
  };
  ledger.markdown = ledgerMarkdown(result, matrix, riskQueue, commonIssues, actionItems, notRun);
  return ledger;
}

/** 订阅版的台账钩子：**判开关**后挂台账 + 把"共性问题 / 逐项目处理项"补成引擎级发现。
 *  分档判据放在这里（而不是放在 run() 里）—— 这样免费包与付费包的 run() 逐字相同，
 *  免费包只在付费块被整块摘掉后剩一个空钩子，**不可能**挂出台账。 */
function ledger_hook(result, findings, rows, payload) {
  if (!fullTierUnlocked(payload || {})) return false;
  const ledger = buildLedger(result, findings, rows);
  result.ledger = ledger;
  for (const r of rows) if (r.status === 'ok') r.ledger_member = true;

  /* 台账层自己的发现：每条风险按原样保留在 findings 里，
     另外给"有事要做的项目"各补一条处理项，让结论能在同一份 findings 里被消费。 */
  for (const c of ledger.common_issues) {
    result.findings.push({
      level: c.level,
      category: '跨项目共性问题（汇总台账）',
      line: 0,
      object: c.objects.join('、'),
      check: '（汇总台账）',
      section: '',
      source_file: '',
      source_line: 0,
      evidence: '跨项目',
      message: `共性问题「${c.category}」命中 ${c.objects.length} 家项目（${c.objects.join('、')}），`
        + '建议集团层面统一口径后同步整改。',
    });
  }
  for (const a of ledger.action_items) {
    result.findings.push({
      level: a.level,
      category: '收入确认台账处理项（汇总台账）',
      line: 0,
      object: a.object,
      check: '（汇总台账）',
      section: '',
      source_file: '',
      source_line: 0,
      evidence: '项目级',
      message: a.text,
    });
  }
  const lv = countLevels(result.findings);
  result.summary.total = result.findings.length;
  result.summary.p0 = lv.p0;
  result.summary.p1 = lv.p1;
  result.summary.p2 = lv.p2;
  result.summary.verdict = lv.p0 > 0 ? 'ERROR_FOUND'
    : (result.findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND');
  result.summary.common_issues = ledger.common_issues.length;
  result.summary.action_items = ledger.action_items.length;
  return true;
}

/** 按 `--export md|csv` 取台账文本（**只返回文本，不落盘**）。 */
function exportLedger(result, fmt) {
  if (!result || !result.ledger) {
    return { ok: false, reason: '本次没有生成跨项目汇总台账（没有可用材料时不给结论，也不出台账）' };
  }
  if (fmt === 'md' || fmt === 'markdown') {
    return { ok: true, format: 'md', text: result.ledger.markdown };
  }
  if (fmt === 'csv') return { ok: true, format: 'csv', text: result.ledger.csv };
  return { ok: false, reason: `只支持 md / csv 两种导出格式（收到的是 ${String(fmt)}）` };
}

/* ===== 以上为订阅版才执行的检查 ===== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  if (!payload) {
    return insufficient([
      '一家项目的材料都没收到（objects[] 与 text 都是空）',
      '单项目用 {"text":"…"}；批量用 {"objects":[{"name":"项目名","files":[{"name":"材料.txt","text":"…"}]}]}',
    ]);
  }
  const objects = normalizeObjects(payload);
  if (!objects.length) {
    return insufficient([
      '一家项目的材料都没收到（objects[] 与 text 都是空）',
      '每家项目一个子目录，目录里放这家项目的一套材料（每项用 `=== 检查项 ===` 分段，Tab 分隔最稳）',
    ]);
  }

  const rows = objects.map((o) => runOneObject(o, payload));
  const usable = rows.filter((r) => r.status === 'ok');
  if (!usable.length) {
    return insufficient(
      [`全部 ${rows.length} 家项目都没有可用材料（每家项目目录里要有这家项目的材料，且每张表要有表头行）`]
        .concat(rows.map((r) => `项目「${r.object}」：没有可用材料`)),
      '把每家项目的材料放进各自子目录后再跑；材料不足时本工具不做任何认定、也不给任何结论。');
  }

  const findings = [];
  for (const r of rows) for (const f of r.findings) findings.push(f);
  findings.sort((a, b) => (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)
    || (a.line - b.line) || String(a.category).localeCompare(String(b.category)));

  const lv = countLevels(findings);
  const withIssues = rows.filter((r) => r.findings.length > 0).length;
  const notRunObjects = rows.filter((r) => r.status !== 'ok').length;

  const result = {
    service_type: 'INDUSTRY_VERTICAL_PACK',
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
    note: `本次对 ${rows.length} 家项目逐个跑了 ${CHECKS_GIVEN.length} 个收入确认检查项（每个成员包内部还有 `
      + `${TOTAL_SUB_CHECKS / CHECKS_GIVEN.length} 项子检查）；未执行的检查项见 scope.checks_not_run 与 `
      + 'scope.sub_checks_not_run。',
    disclaimer: '只把各项目材料里的表内/表间算术与勾稽核一遍，结论都带**原文文件与行号**、可由第三方复算；'
      + '**不代替审计、不出具鉴证意见**，也不判断收费/定价/医保政策口径。',
  };

  /* 分层：
     · 免费档（免费包里就是下面这两行 + 再下面那句 return，付费块被整块摘掉）：
       只报**实际执行**的那 7 项，未执行项如实列出（说明文本，不是实现）。
     · 完整档（本文件）：在上面那层之上再挂一层跨项目汇总台账
       （项目 × 检查项总表、收入确认风险排序清单、跨项目共性问题归类、Markdown / CSV 导出）。 */
  result.checks_executed = CHECKS_GIVEN.concat();
  result.checks_withheld = CHECKS_WITHHELD.concat();

  /* 分层出口：**同一个调用点**，不在这里判档 ——
     判档在台账钩子内部（免费档的空钩子什么都不做，完整档的真实现自己判开关）。
     这样免费包里的 run() 与付费包逐字相同，分层不靠调用方自觉。 */

  /* 订阅版：在上面那层之上再挂一层跨项目汇总台账
     （项目 × 检查项总表、收入确认风险排序清单、跨项目共性问题归类、Markdown / CSV 导出）。 */
  const ledgerAttached = ledger_hook(result, findings, rows, payload) === true;

  /* 分档后的"实际执行 / 未执行"：只认**钩子到底挂上台账没有**（本包返回 false ⇒ 保持 7 项）。
     这样 run() 里不出现任何付费判据函数，免费包里连"该不该挂台账"的分支都没有。 */
  if (ledgerAttached) {
    result.checks_executed = CHECKS_GIVEN.concat(CHECKS_WITHHELD);
    result.checks_withheld = [];
  }

  return { status: 'success', result: result };
}

module.exports = {
  run, runOneObject, normalizeObjects, coerceFiles, sectionsOfFile, countLevels, checkClientCoverage,
  exportLedger, buildLedger, ledgerMatrix, ledgerCommonIssues, ledgerActionItems, ledgerMarkdown, ledgerCsv,
  riskSort, mdCell, csvCell,
  CHECKS_GIVEN, CHECKS_WITHHELD, SUB_CHECKS_WITHHELD, OUT_OF_SCOPE,
  SAMPLE_TEXT, SAMPLE_OBJECTS, DIRTY_TEXT, PARTIAL_TEXT, MEMBERS, SAMPLE_HAS_FINDINGS,
};
