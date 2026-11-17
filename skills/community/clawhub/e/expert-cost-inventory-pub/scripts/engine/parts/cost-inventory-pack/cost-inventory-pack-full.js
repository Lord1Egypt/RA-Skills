'use strict';
/**
 * cost-inventory-pack-full.js —— 成本与存货技能包（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须用它：**制造业 / 商贸 / 生鲜 / 工程的成本会计，在每月成本结账之前**。
 * 月底要核的不是一个数，而是十几张互相关联的底稿：库存账实、出入库与加权平均成本、
 * 存货跌价准备、报废与审批、BOM 用量与损耗、材料领用与定额、材料成本差异分摊、
 * 生产投入产出与报废率、委外加工费、甲供材料、工程材料调拨、工时与人工分摊、
 * 固定资产盘点、生鲜损耗 —— 每张表都有自己的勾稽关系，**逐张手核既慢又容易漏**。
 *
 * 这个包做的事**只有一件**（不是重写任何规则）：把仓库里**已有的 14 个成本/存货检查引擎**
 * 装进一个批量壳里，`--input <目录>`（每个子目录 = 一个客户 / 一套成本存货底稿）一次跑完所有客户，
 * **每个客户一行结论**。
 *   规则来源：`scripts/engine/parts/<检查项>/`（**逐字节拷贝**自那 14 个免费包，一行都没改；
 *   本包只做"目录 → 客户 → 逐项派发"的编排与汇总）。
 *
 * 契约（与仓库其它引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *     payload.text            单客户：该客户的一套成本存货底稿文本（每张表用 `=== 检查名 ===` 分段）
 *     payload.objects[]       多客户：{name, files:[{name, text}]} —— 每个子目录 = 一个客户
 *   CHECKS_GIVEN / CHECKS_WITHHELD   本包执行 / 不执行的检查项（免费包据此如实列出未执行项）
 *   CHECKS_OUT_OF_SCOPE              本能力**根本不做**的判断（边界诚实）
 *   SAMPLE_TEXT / SAMPLE_OBJECTS     样例（免费包 --sample / --sample-batch 用它自检）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），
 * **不读环境变量**，**不写任何文件**（结果只打到 stdout）。
 * ⚠️ 材料不足**绝不给结论**：某个客户没材料就单独标"未执行"，一个客户都跑不了就整体不给结论。
 * ⚠️ 本工具**不代替成本核算制度、不判断该用哪种计价方法、不出审计意见**，也不读 ERP 导出文件。
 */

const MEMBERS = [
  {
    label: '库存账实核对',
    id: 'inventory-check',
    entry: require('./parts/inventory-check/inventory-check.js'),
  },
  {
    label: '存货出入库与加权平均成本',
    id: 'inventory-cost-flow-check',
    entry: require('./parts/inventory-cost-flow-check/inventory-cost-flow-check.js'),
  },
  {
    label: '存货跌价准备',
    id: 'inventory-provision-check',
    entry: require('./parts/inventory-provision-check/inventory-provision-check.js'),
  },
  {
    label: '存货报废与审批',
    id: 'inventory-scrap-approval-check',
    entry: require('./parts/inventory-scrap-approval-check/inventory-scrap-approval-check.js'),
  },
  {
    label: 'BOM用量与损耗差异',
    id: 'bom-consumption-variance-check',
    entry: require('./parts/bom-consumption-variance-check/bom-consumption-variance-check.js'),
  },
  {
    label: '材料领用与定额损耗',
    id: 'material-usage-loss-check',
    entry: require('./parts/material-usage-loss-check/material-usage-loss-check.js'),
  },
  {
    label: '材料成本差异分摊',
    id: 'material-cost-variance-check',
    entry: require('./parts/material-cost-variance-check/material-cost-variance-check.js'),
  },
  {
    label: '生产投入产出与报废率',
    id: 'production-yield-scrap-check',
    entry: require('./parts/production-yield-scrap-check/production-yield-scrap-check.js'),
  },
  {
    label: '委外加工费与损耗',
    id: 'outsourced-processing-fee-check',
    entry: require('./parts/outsourced-processing-fee-check/outsourced-processing-fee-check.js'),
  },
  {
    label: '甲供材料与分包领用',
    id: 'owner-supplied-material-check',
    entry: require('./parts/owner-supplied-material-check/owner-supplied-material-check.js'),
  },
  {
    label: '工程材料调拨与领用',
    id: 'project-material-transfer-check',
    entry: require('./parts/project-material-transfer-check/project-material-transfer-check.js'),
  },
  {
    label: '工时与人工成本分摊',
    id: 'labor-cost-allocation-check',
    entry: require('./parts/labor-cost-allocation-check/labor-cost-allocation-check.js'),
  },
  {
    label: '固定资产盘点账实',
    id: 'fixed-asset-count-check',
    entry: require('./parts/fixed-asset-count-check/fixed-asset-count-check.js'),
  },
  {
    label: '生鲜损耗与盘点差异',
    id: 'fresh-loss-check',
    entry: require('./parts/fresh-loss-check/fresh-loss-check.js'),
  },
];

/* 本包执行：14 个成本/存货检查项，逐个客户全跑一遍（这就是免费层的核心产出：一次跑完所有客户） */
const CHECKS_GIVEN = MEMBERS.map((m) => m.label);

/* 订阅版追加（**多一种能力**，不是多几个数）：跨客户汇总台账 —— 单客户结果里根本不存在的东西 */
const CHECKS_WITHHELD = [
  '跨客户汇总台账（全部客户 × 全部 14 项检查合并成一张总表）',
  '跨客户风险排序处理清单（按 P0/P1/P2 排序，带客户名与原文文件行号）',
  '跨客户共性问题归类（同一问题命中 2 个及以上客户时合并成一条共性项）',
  '台账导出（Markdown 与 CSV 文本，直接用于成本与存货复核说明）',
];

/* 如实列出**每个成员检查包自己**没做的检查项（那 14 个免费包各自的未执行项）——
   两个档位都没实现它们，绝不能因为"买断档打开了汇总"就让买家以为这些项被跑了。 */
const SUB_CHECKS_WITHHELD = [];
for (const m of MEMBERS) {
  for (const w of (m.entry.CHECKS_WITHHELD || [])) SUB_CHECKS_WITHHELD.push(`${m.label}：${w}`);
}

const TOTAL_SUB_CHECKS = MEMBERS.reduce((n, m) => n + (m.entry.CHECKS_GIVEN || []).length, 0);

const OUT_OF_SCOPE = [
  '判断存货该按哪种方法计价（先进先出 / 加权平均 / 个别计价），或该不该计提跌价准备（属于会计政策与判断）',
  '替企业确认成本核算制度、定额标准、损耗率是否合理（本工具只核你给的表内数字与表间勾稽关系）',
  '代替成本结账、出具审计意见或鉴证意见',
  '核对实物是否真的存在、生鲜是否真的坏了（那要人去数、去看，本工具只核你数出来、记下来的数）',
  '读取 ERP / MES / WMS / 财务软件的导出文件（需要你先导出成文本，每个客户一个目录）',
];

/* 样例 = 14 个成员检查包各自的最小完整样例（各自带表头，用 `=== 检查名 ===` 分段）。
   它是一份**干净的成本存货底稿**：跑出来 0 条发现 —— 干净样例不误报是最重要的一条。 */
const SAMPLE_TEXT = MEMBERS
  .map((m) => `=== ${m.label} ===\n${m.entry.SAMPLE_TEXT}`)
  .join('\n\n');

/* 有一处硬伤的样例：把「库存账实核对」里 A-02 水泥的差异金额从 50.00 改成 60.00
   （差异数量 2 × 单价 25.00 = 50.00，与 60.00 不符）⇒ 必须报出来，并带**原文行号**。 */
const DIRTY_FROM = 'A-02\t水泥\t200\t0\t80\t120\t118\t2\t25.00\t50.00';
const DIRTY_TO = 'A-02\t水泥\t200\t0\t80\t120\t118\t2\t25.00\t60.00';
const DIRTY_TEXT = SAMPLE_TEXT.replace(DIRTY_FROM, DIRTY_TO);

/* 只覆盖 3 项的样例：用来演示"材料只覆盖了一部分"时，批量壳**明确报一条**，
   而不是把"跑了 3 项"说成"14 项都核过了"。 */
const PARTIAL_TITLES = ['库存账实核对', '材料领用与定额损耗', '生鲜损耗与盘点差异'];
const PARTIAL_TEXT = SAMPLE_TEXT.split(/(?=^=== )/m)
  .filter((s) => PARTIAL_TITLES.some((t) => s.trim().indexOf(`=== ${t} ===`) === 0))
  .join('\n');

/* 批量样例：3 个客户（干净 / 有一处硬伤 / 没交材料），用来演示"一次跑完所有客户"。 */
const SAMPLE_OBJECTS = [
  { name: '豫州精工制造有限公司（2026-02 成本结账）', files: [{ name: '成本存货底稿.txt', text: SAMPLE_TEXT }] },
  { name: '中岳食品加工有限公司（2026-02 成本结账）', files: [{ name: '成本存货底稿.txt', text: DIRTY_TEXT }] },
  { name: '缺料客户（只登记未交材料）', files: [] },
];

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

/** 把一份材料按 `=== 检查名 ===` 分段，并**记住每一行来自哪个文件第几行**（结论要能回到原文）。
 *  每个成员引擎内部都把空行过滤掉、行号按过滤后的顺序算（本仓库 14 个引擎口径一致），
 *  所以这里也先把空行过滤掉再交给引擎，并同步保留原始行号 —— 否则回原文件时会错行。 */
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
    message: `客户「${it.client}」的材料只覆盖了 ${ran.length} / ${it.checks.length} 个成本与存货检查项，`
      + `未执行的是：${notRun.map((c) => c.check).join('、')} —— 这些项这次**没有核**，请补齐材料后重跑。`,
  };
}

/** 一个客户跑完全部 14 项；每一项的实际规则在 parts/ 里（本文件一行规则都没改）。
 *  派发方式：**优先**喂给"分段名 === 本检查项名"的那一段（`=== 检查名 ===` 就是为这件事存在的）；
 *  没对上再依次扫其余分段，**第一个跑通的段**就是这一项的表；
 *  一段都跑不通 ⇒ 这一项如实标 `not_run` 并列出还缺哪个表头，**绝不算它跑过**。 */
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

  const checks = [];
  const findings = [];
  const notRun = [];
  for (const m of MEMBERS) {
    const ordered = candidates.slice().sort((a, b) => {
      const ra = a.title === m.label ? 0 : 1;
      const rb = b.title === m.label ? 0 : 1;
      return ra - rb;
    });
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
        missing: bestMissing || ['这个客户的材料里没有这一项需要的表头行'],
      });
      continue;
    }
    const per = (hit.result.findings || []).map((f) => {
      const orig = hit.cand.lineNos[f.line - 1];
      const lineNo = orig === undefined ? hit.cand.startLine : orig;
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
    reason: anyRan ? '' : '材料里没有任何一项能被认出的表（每个 `=== 检查名 ===` 分段的第一行要是表头行）',
  };
}

/* ===== 以下为订阅版才执行的检查 ===== */

/** CSV 单元格转义（含逗号/引号/换行时加引号） */
function csvCell(v) {
  const s = String(v === undefined || v === null ? '' : v);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

/** 客户 × 检查项总表（只有跨客户汇总才有；单客户结果里不存在） */
function ledgerMatrix(rows) {
  return rows.map((r) => ({
    object: r.object,
    verdict: r.verdict,
    status: r.status,
    total: r.total, p0: r.p0, p1: r.p1, p2: r.p2,
    not_run: r.not_run.slice(),
    checks: r.checks.map((c) => ({ check: c.check, status: c.status, findings: c.findings })),
  }));
}

/** 处理清单：按风险排序（P0 → P1 → P2），同级别按客户名与原文行号 */
function ledgerRiskQueue(findings) {
  const order = { P0: 0, P1: 1, P2: 2, INFO: 3 };
  return findings.filter((f) => f.level !== 'INFO').slice().sort(
    (a, b) => (order[a.level] - order[b.level])
      || (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)
      || (a.line - b.line));
}

/** 共性问题：同一类别命中 2 个及以上客户 ⇒ 合并成一条（这是"跨客户"视角才能看到的） */
function ledgerCommonIssues(queue) {
  const map = new Map();
  for (const f of queue) {
    const key = String(f.category);
    let e = map.get(key);
    if (!e) { e = { category: key, level: f.level, count: 0, objects: [] }; map.set(key, e); }
    e.count += 1;
    if (e.objects.indexOf(f.object) < 0) e.objects.push(f.object);
  }
  return Array.from(map.values()).filter((e) => e.objects.length >= 2)
    .sort((a, b) => (b.objects.length - a.objects.length) || (b.count - a.count));
}

/** 交付层处理项：每个"有事要做"的客户一条（交给成本会计照着做） */
function ledgerActionItems(rows) {
  const out = [];
  for (const r of rows) {
    if (!r.findings.length) continue;
    out.push({
      level: 'INFO',
      category: '成本存货台账处理项（汇总台账）',
      kind: 'ledger_action',
      object: r.object,
      check: '', section: '', line: 0, source_file: '', source_line: 0,
      evidence: `客户「${r.object}」`,
      message: `客户「${r.object}」本次需处理 ${r.findings.length} 项`
        + `（P0 ${r.p0} / P1 ${r.p1} / P2 ${r.p2}`
        + `${r.not_run.length ? `；另有 ${r.not_run.length} 项未执行` : ''}）`
        + ' —— 明细见 ledger.risk_queue。',
    });
  }
  return out;
}

function ledgerMarkdown(l) {
  const out = [];
  out.push('# 成本与存货技能包 · 跨客户汇总台账');
  out.push('');
  out.push(`- 客户数：${l.matrix.length}`);
  out.push(`- 需要处理的客户：${l.action_items.length}`);
  out.push(`- 问题条目：${l.risk_queue.length}（P0 ${l.counts.p0} / P1 ${l.counts.p1} / P2 ${l.counts.p2}）`);
  out.push('');
  out.push('## 一、客户 × 检查项总表');
  out.push('');
  out.push(`| 客户 | ${CHECKS_GIVEN.join(' | ')} | 问题 | P0 | 结论 |`);
  out.push(`|${' --- |'.repeat(CHECKS_GIVEN.length + 3)}`);
  for (const m of l.matrix) {
    const cells = m.checks.map((c) => (c.status === 'ok'
      ? (c.findings ? `有问题(${c.findings})` : '通过')
      : '未执行'));
    out.push(`| ${m.object} | ${cells.join(' | ')} | ${m.total} | ${m.p0} | ${m.verdict} |`);
  }
  out.push('');
  out.push('## 二、处理清单（按风险排序）');
  out.push('');
  if (!l.risk_queue.length) out.push('（没有需要处理的问题）');
  for (const f of l.risk_queue) {
    out.push(`- [${f.level}] ${f.object}｜${f.check}｜${f.category}｜${f.evidence}：${f.message}`);
  }
  out.push('');
  out.push('## 三、跨客户共性问题');
  out.push('');
  if (!l.common_issues.length) out.push('（没有命中 2 个及以上客户的共性问题）');
  for (const c of l.common_issues) {
    out.push(`- [${c.level}] ${c.category}：命中 ${c.objects.length} 个客户`
      + `（${c.objects.join('、')}），共 ${c.count} 处 —— 优先统一口径处理。`);
  }
  out.push('');
  out.push('## 四、未执行项（如实列出，不会用默认值编造结论）');
  out.push('');
  for (const w of CHECKS_WITHHELD) out.push(`- 本版本不包含：${w}`);
  for (const w of SUB_CHECKS_WITHHELD) out.push(`- 成员检查包本身未实现：${w}`);
  if (l.not_run_objects.length) {
    out.push('');
    out.push(`没交材料的客户（这次一项都没跑）：${l.not_run_objects.join('、')}`);
  }
  return out.join('\n');
}

function ledgerCsv(queue) {
  const head = ['客户', '级别', '检查项', '问题类别', '来源文件', '来源行', '原文行号', '结论'];
  const lines = [head.join(',')];
  for (const f of queue) {
    lines.push([f.object, f.level, f.check, f.category,
      f.source_file, f.source_line, f.line, f.message].map(csvCell).join(','));
  }
  return lines.join('\n');
}

/* 跨客户汇总台账：**客户 × 检查项总表 + 风险处理清单 + 共性问题归类 + 导出**。
   台账必须能说出**哪些客户没跑**（诚实边界）⇒ 从**全部行**里筛 `not_run_objects`；
   **总表只收跑过的行**（没跑过的不能混进总表冒充"核过"）。 */
function buildLedger(result) {
  const rows = result.objects.filter((r) => r.status === 'ok');
  const matrix = ledgerMatrix(rows);
  const queue = ledgerRiskQueue(result.findings);
  const common = ledgerCommonIssues(queue);
  const actions = ledgerActionItems(rows);
  const counts = countLevels(queue);
  const notRunObjects = result.objects.filter((r) => r.status !== 'ok').map((r) => r.object);
  const ledger = {
    matrix: matrix, risk_queue: queue, common_issues: common, action_items: actions, counts: counts,
    not_run_objects: notRunObjects,
    markdown: '', csv: '',
  };
  ledger.markdown = ledgerMarkdown(ledger);
  ledger.csv = ledgerCsv(queue);
  return ledger;
}

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  if (!payload) {
    return insufficient([
      '一个客户的材料都没收到（objects[] 与 text 都是空）',
      '单客户用 {"text":"…"}；批量用 {"objects":[{"name":"客户名","files":[{"name":"底稿.txt","text":"…"}]}]}',
    ]);
  }
  const objects = normalizeObjects(payload);
  if (!objects.length) {
    return insufficient([
      '一个客户的材料都没收到（objects[] 与 text 都是空）',
      '每个客户一个子目录，目录里放该客户的一套成本存货底稿（每张表用 `=== 检查名 ===` 分段，Tab 分隔最稳）',
    ]);
  }

  const rows = objects.map(runOneObject);
  const usable = rows.filter((r) => r.status === 'ok');
  if (!usable.length) {
    return insufficient(
      [`全部 ${rows.length} 个客户都没有可用材料（每个客户目录里要有该客户的成本存货底稿，且每张表要有表头行）`]
        .concat(rows.map((r) => `客户「${r.object}」：没有可用材料`)),
      '把每个客户的成本存货底稿放进各自子目录后再跑；材料不足时本工具不做任何认定、也不给任何结论。');
  }

  const findings = [];
  for (const r of rows) for (const f of r.findings) findings.push(f);
  findings.sort((a, b) => (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)
    || (a.line - b.line) || String(a.category).localeCompare(String(b.category)));

  const lv = countLevels(findings);
  const withIssues = rows.filter((r) => r.findings.length > 0).length;
  const notRunObjects = rows.filter((r) => r.status !== 'ok').length;

  const result = {
    service_type: 'COST_INVENTORY_PACK',
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
    note: `本次对 ${rows.length} 个客户逐个跑了 ${CHECKS_GIVEN.length} 个成本与存货检查项（每个成员包内部还有 `
      + `${TOTAL_SUB_CHECKS / CHECKS_GIVEN.length} 项子检查）；未执行的检查项见 scope.checks_not_run 与 `
      + 'scope.sub_checks_not_run。',
    disclaimer: '只把各客户材料里的表内/表间算术与勾稽核一遍，结论都带**原文文件与行号**、可由第三方复算；'
      + '**不代替成本核算制度与会计判断**，也不判断某项成本该不该这样结转。',
  };

  /* 分层：订阅版多一层「跨客户汇总台账」；本包只报**实际执行**的那 14 项 */
  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  if (paid) {
    result.checks_executed = CHECKS_GIVEN.concat(CHECKS_WITHHELD);
    result.checks_withheld = [];
    result.scope.checks_not_run = [];
    result.ledger = buildLedger(result);
    for (const act of result.ledger.action_items) result.findings.push(act);
    result.summary.total = result.findings.length;
    result.summary.action_items = result.ledger.action_items.length;
    result.summary.common_issues = result.ledger.common_issues.length;
  } else {
    result.checks_executed = CHECKS_GIVEN.slice();
    result.checks_withheld = CHECKS_WITHHELD.slice();
  }

  return { status: 'success', result: result };
}

module.exports = {
  run, runOneObject, normalizeObjects, coerceFiles, sectionsOfFile, countLevels, checkClientCoverage,
  CHECKS_GIVEN, CHECKS_WITHHELD, SUB_CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, SAMPLE_OBJECTS,
  DIRTY_TEXT, PARTIAL_TEXT, MEMBERS,
};
