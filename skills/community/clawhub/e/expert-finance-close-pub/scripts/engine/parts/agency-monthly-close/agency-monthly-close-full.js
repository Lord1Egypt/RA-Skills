'use strict';
/**
 * agency-monthly-close-full.js —— 代账客户月结交付包（本包 / 订阅版共用源码）
 *
 * 谁在什么时候必须用它：**代账公司每月月结交付之前**。一家代账公司手里有几十上百个客户，
 * 每个客户每个月都要把同一批表核一遍（财务 / 人力 / 制造 / 建筑 / 电商 / 外贸 / 集团财务），
 * 现在只能一个客户一个客户地跑 —— 慢，而且**没有一张"客户 × 检查项"的总表**，
 * 交付出问题时说不清哪家客户哪一项没核。
 *
 * 这个包做的事**只有一件**（不是重写规则）：把仓库里**已有的 7 个行业月度自查引擎**装进一个
 * 批量壳里，`--input <客户目录>` 一次跑完所有客户，**每个客户一行结论**。
 *   规则来源：`scripts/engine/parts/<行业>-monthly-selfcheck/`（逐字节拷贝自那 7 个免费包，
 *   **一行都没改**；本包只做"目录 → 客户 → 结果"的编排与汇总）。
 *
 * 契约（与仓库其它引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *     payload.text            单客户：该客户的标准表文本（分段 `=== 检查名 ===`，与 7 个自查包同格式）
 *     payload.clients[]       多客户：{name, files:[{name, text}]} —— 每个子目录 = 一个客户
 *   CHECKS_GIVEN / CHECKS_WITHHELD   本包执行 / 不执行的检查项（免费包据此如实列出未执行项）
 *   CHECKS_OUT_OF_SCOPE              本能力**根本不做**的判断（边界诚实）
 *   SAMPLE_TEXT / SAMPLE_CLIENTS     样例（免费包 --sample / --sample-batch 用它自检）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * ⚠️ 材料不足**绝不给结论**：某个客户没材料就单独标"未执行"，一个客户都跑不了就整体不给结论。
 * ⚠️ 本工具**不代替做账、不出鉴证意见**，也不读 ERP/财务系统（需要你先导出成文本）。
 */

const PACKS = [
  { label: '财务月度自查包', entry: require('./parts/finance-monthly-selfcheck/finance-monthly-selfcheck.js') },
  { label: '人力资源月度自查包', entry: require('./parts/hr-monthly-selfcheck/hr-monthly-selfcheck.js') },
  { label: '制造业月度自查包', entry: require('./parts/manufacturing-monthly-selfcheck/manufacturing-monthly-selfcheck.js') },
  { label: '建筑企业月度自查包', entry: require('./parts/construction-monthly-selfcheck/construction-monthly-selfcheck.js') },
  { label: '电商财务月度自查包', entry: require('./parts/ecommerce-monthly-selfcheck/ecommerce-monthly-selfcheck.js') },
  { label: '外贸月度自查包', entry: require('./parts/export-monthly-selfcheck/export-monthly-selfcheck.js') },
  { label: '集团财务月度自查包', entry: require('./parts/group-finance-monthly-selfcheck/group-finance-monthly-selfcheck.js') },
];

/* 本包执行：7 个行业自查包，逐个客户全跑一遍（这就是免费层的核心产出：一次跑完所有客户） */
const CHECKS_GIVEN = PACKS.map((p) => p.label);

/* 订阅版追加（**多一种能力**，不是多几个数）：跨客户汇总台账 —— 单客户结果里根本不存在的东西 */
const CHECKS_WITHHELD = [
  '跨客户汇总台账（全部客户 × 全部检查项合并成一张总表）',
  '跨客户风险排序处理清单（按 P0/P1/未执行排序，带客户与原文定位）',
  '跨客户共性问题归类（同一问题命中 2 个及以上客户时合并成一条共性项）',
  '交付台账导出（Markdown 与 CSV 文本，直接用于月结交付说明）',
];

/* 如实列出**子检查包自己**没做的检查项（那 7 个免费包的 CHECKS_WITHHELD）—— 两个档位都没实现，
   绝不能因为"买断档打开了开关"就让买家以为这些项被跑了。 */
const SUB_CHECKS_WITHHELD = [];
for (const p of PACKS) {
  for (const w of (p.entry.CHECKS_WITHHELD || [])) SUB_CHECKS_WITHHELD.push(`${p.label}：${w}`);
}

const TOTAL_SUB_CHECKS = PACKS.reduce((n, p) => n + (p.entry.CHECKS_GIVEN || []).length, 0);

const OUT_OF_SCOPE = [
  '替代做账、出具鉴证意见或代客户申报（只做表内/表间的算术与勾稽核对）',
  '判断某张表的账务处理是否合规、该不该这样记账（那是会计政策与主管机关口径）',
  '读取 ERP / 财务软件 / 平台后台的导出文件（需要你先导出成文本，每个客户一个目录）',
  '代替客户沟通与催收：本工具只把"哪家客户哪一项没过"列出来',
];

/* 样例 = 7 个自查包各自的最小完整样例（含全部 `=== 检查名 ===` 分段，35 段全部唯一）。
   它是一份**干净**的月结材料：跑出来 0 条发现 —— 干净样例不误报是最重要的一条。 */
const SAMPLE_TEXT = PACKS.map((p) => p.entry.SAMPLE_TEXT).join('\n');

/* 批量样例：3 个客户（干净 / 有一处硬伤 / 没交材料），用来演示"一次跑完所有客户"。 */
const SAMPLE_CLIENTS = [
  { name: '豫州商贸有限公司', files: [{ name: '月结材料.txt', text: SAMPLE_TEXT }] },
  { name: '中岳建材有限公司', files: [{
    name: '月结材料.txt',
    text: SAMPLE_TEXT.replace(
      '合计\t545000.00\t120000.00\t\t405000.00\t405000.00',
      '合计\t645000.00\t120000.00\t\t405000.00\t405000.00'),
  }] },
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

/** 覆盖缺口检查：客户交了材料，但只覆盖了一部分自查包 ⇒ **明确报一条**，
 *  不能因为"跑了几个包"就以为 7 个包都跑过了。整份材料都没交的客户不在这里报（那是客户级的"未执行"）。 */
function checkClientCoverage(it) {
  const ran = it.packs.filter((p) => p.status === 'ok');
  const notRun = it.packs.filter((p) => p.status !== 'ok');
  if (!ran.length || !notRun.length) return null;
  return {
    level: 'P2',
    category: '检查项未执行（材料只覆盖了一部分）',
    line: 1,
    message: `客户「${it.client}」的材料只覆盖了 ${ran.length} / ${it.packs.length} 个自查包，`
      + `未执行的是：${notRun.map((p) => p.pack).join('、')} —— 这些项这次**没有核**，请补齐材料后重跑。`,
  };
}

/** 一个客户的材料合并成一份文本，并**记住每一行来自哪个文件第几行**（结论要能回到原文）。 */
function assembleClient(files) {
  const lines = [];
  const map = [];
  for (const f of files) {
    const ls = String(f.text).split(/\r?\n/);
    for (let i = 0; i < ls.length; i += 1) {
      lines.push(ls[i]);
      map.push({ file: f.name, line: i + 1 });
    }
  }
  return { text: lines.join('\n'), map };
}

function coerceFiles(c) {
  const files = [];
  if (Array.isArray(c.files)) {
    for (const f of c.files) {
      if (!f) continue;
      const t = f.text !== undefined ? f.text : f.content;
      files.push({
        name: String(f.name || f.file || '材料'),
        text: t === undefined || t === null ? '' : String(t),
      });
    }
    return files;
  }
  const t = c.text !== undefined ? c.text : c.content;
  if (t !== undefined && t !== null) {
    files.push({ name: String(c.file || c.file_name || '材料'), text: String(t) });
  }
  return files;
}

/** 入参归一化成"客户列表"：`{text}` 是单客户，`{clients:[{name,files}]}` 是批量。 */
function normalizeClients(payload) {
  const raw = [];
  if (Array.isArray(payload.clients)) {
    for (const c of payload.clients) {
      if (!c) continue;
      raw.push({ name: String(c.name || c.client || '').trim(), files: coerceFiles(c) });
    }
  }
  if (payload.text !== undefined || payload.content !== undefined) {
    raw.push({
      name: String(payload.client_name || payload.client || payload.name || '单客户').trim(),
      files: coerceFiles(payload),
    });
  }
  const out = [];
  raw.forEach((c, i) => out.push({ name: c.name || `客户${i + 1}`, files: c.files }));
  return out;
}

/** 一个客户跑完全部 7 个自查包；每个包内部的实际规则在 parts/ 里（本文件不改规则）。 */
function runOneClient(client) {
  const live = client.files.filter((f) => String(f.text).trim() !== '');
  const assembled = assembleClient(live);
  const text = assembled.text;
  const packs = [];
  const findings = [];
  const notRun = [];

  if (text.trim().length < 5) {
    for (const p of PACKS) {
      const checks = (p.entry.CHECKS_GIVEN || []).map((c) => ({ check: c, status: 'not_run', findings: 0 }));
      for (const c of checks) notRun.push(c.check);
      packs.push({
        pack: p.label, status: 'not_run', checks, findings: 0, p0: 0, p1: 0, p2: 0,
        reason: '没有收到这个客户的材料',
      });
    }
    return {
      client: client.name, status: 'insufficient_input', files: live.map((f) => f.name),
      material_lines: 0, packs, findings: [], not_run: notRun,
      total: 0, p0: 0, p1: 0, p2: 0, verdict: 'NOT_RUN',
    };
  }

  for (const p of PACKS) {
    let out = null;
    try { out = p.entry.run({ text: text }); } catch (e) { out = null; }
    if (!out || out.status !== 'success' || !out.result) {
      const checks = (p.entry.CHECKS_GIVEN || []).map((c) => ({ check: c, status: 'not_run', findings: 0 }));
      for (const c of checks) notRun.push(c.check);
      packs.push({
        pack: p.label, status: 'not_run', checks, findings: 0, p0: 0, p1: 0, p2: 0,
        reason: '这个客户的材料里没有这一套检查需要的分段/表头',
        missing: (out && out.missing) || [],
      });
      continue;
    }
    const r = out.result;
    const per = [];
    let ranChecks = 0;
    for (const c of (r.per_check || [])) {
      const st = c.status === 'ok' ? 'ok' : 'not_run';
      if (st === 'ok') ranChecks += 1; else notRun.push(c.check);
      per.push({ check: c.check, status: st, findings: c.findings || 0 });
    }
    const fs = (r.findings || []).map((f) => {
      const src = assembled.map[f.line - 1];
      return {
        level: f.level,
        category: f.category,
        line: f.line,
        client: client.name,
        pack: p.label,
        check: f.check || '',
        source_file: src ? src.file : '',
        source_line: src ? src.line : f.line,
        evidence: src && src.file ? `${src.file}:${src.line}` : `第 ${f.line} 行`,
        message: f.message,
      };
    });
    for (const f of fs) findings.push(f);
    const lv = countLevels(fs);
    packs.push({
      pack: p.label, status: ranChecks ? 'ok' : 'not_run', checks: per,
      findings: fs.length, p0: lv.p0, p1: lv.p1, p2: lv.p2,
    });
  }

  /* 批量壳自己的检查项：材料只覆盖了一部分自查包时，明确报一条（别把"跑了 1 个包"说成"全跑过了"） */
  const cover = checkClientCoverage({ client: client.name, packs: packs });
  if (cover) {
    findings.push(Object.assign({}, cover, {
      client: client.name, pack: '（批量壳）', check: '',
      source_file: '', source_line: 0, evidence: '客户级',
    }));
  }

  const lv = countLevels(findings);
  const anyRan = packs.some((p) => p.status === 'ok');
  return {
    client: client.name,
    status: 'ok',
    files: live.map((f) => f.name),
    material_lines: text.split(/\r?\n/).length,
    packs,
    findings,
    not_run: notRun,
    total: findings.length,
    p0: lv.p0, p1: lv.p1, p2: lv.p2,
    verdict: lv.p0 > 0 ? 'P0_ISSUES' : (findings.length ? 'ISSUES' : (anyRan ? 'NO_ISSUE_FOUND' : 'NOT_RUN')),
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
    client: r.client,
    verdict: r.verdict,
    status: r.status,
    total: r.total, p0: r.p0, p1: r.p1, p2: r.p2,
    not_run: r.not_run.slice(),
    packs: r.packs.map((p) => ({ pack: p.pack, status: p.status, findings: p.findings })),
  }));
}

/** 处理清单：按风险排序（P0 → P1 → P2），同级别按客户与原文行号 */
function ledgerRiskQueue(findings) {
  const order = { P0: 0, P1: 1, P2: 2, INFO: 3 };
  return findings.filter((f) => f.level !== 'INFO').slice().sort(
    (a, b) => (order[a.level] - order[b.level])
      || (a.client < b.client ? -1 : a.client > b.client ? 1 : 0)
      || (a.line - b.line));
}

/** 共性问题：同一类别命中 2 个及以上客户 ⇒ 合并成一条（这是"跨客户"视角才能看到的） */
function ledgerCommonIssues(queue) {
  const map = new Map();
  for (const f of queue) {
    const key = String(f.category);
    let e = map.get(key);
    if (!e) { e = { category: key, level: f.level, count: 0, clients: [] }; map.set(key, e); }
    e.count += 1;
    if (e.clients.indexOf(f.client) < 0) e.clients.push(f.client);
  }
  return Array.from(map.values()).filter((e) => e.clients.length >= 2)
    .sort((a, b) => (b.clients.length - a.clients.length) || (b.count - a.count));
}

/** 交付层处理项：每个"有事要做"的客户一条（交给代账会计照着做） */
function ledgerActionItems(rows) {
  const out = [];
  for (const r of rows) {
    if (!r.findings.length) continue;
    out.push({
      level: 'INFO',
      category: '月结交付处理项（汇总台账）',
      kind: 'ledger_action',
      client: r.client,
      pack: '', check: '', line: 0, source_file: '', source_line: 0,
      evidence: `客户「${r.client}」`,
      message: `客户「${r.client}」本月需处理 ${r.findings.length} 项`
        + `（P0 ${r.p0} / P1 ${r.p1} / P2 ${r.p2}`
        + `${r.not_run.length ? `；另有 ${r.not_run.length} 项未执行` : ''}）`
        + ' —— 明细见 ledger.risk_queue。',
    });
  }
  return out;
}

function ledgerMarkdown(l) {
  const out = [];
  out.push('# 代账客户月结交付台账');
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
    const cells = m.packs.map((p) => (p.status === 'ok'
      ? (p.findings ? `有问题(${p.findings})` : '通过')
      : '未执行'));
    out.push(`| ${m.client} | ${cells.join(' | ')} | ${m.total} | ${m.p0} | ${m.verdict} |`);
  }
  out.push('');
  out.push('## 二、处理清单（按风险排序）');
  out.push('');
  if (!l.risk_queue.length) out.push('（没有需要处理的问题）');
  for (const f of l.risk_queue) {
    out.push(`- [${f.level}] ${f.client}｜${f.pack}｜${f.category}｜${f.evidence}：${f.message}`);
  }
  out.push('');
  out.push('## 三、跨客户共性问题');
  out.push('');
  if (!l.common_issues.length) out.push('（没有命中 2 个及以上客户的共性问题）');
  for (const c of l.common_issues) {
    out.push(`- [${c.level}] ${c.category}：命中 ${c.clients.length} 个客户`
      + `（${c.clients.join('、')}），共 ${c.count} 处 —— 优先统一口径处理。`);
  }
  out.push('');
  out.push('## 四、未执行项（如实列出，不会用默认值编造结论）');
  out.push('');
  for (const w of CHECKS_WITHHELD) out.push(`- 本版本不包含：${w}`);
  for (const w of SUB_CHECKS_WITHHELD) out.push(`- 子检查包本身未实现：${w}`);
  if (l.not_run_objects.length) {
    out.push('');
    out.push(`没交材料的客户（这次一项都没跑）：${l.not_run_objects.join('、')}`);
  }
  return out.join('\n');
}

function ledgerCsv(queue) {
  const head = ['客户', '级别', '检查包', '问题类别', '来源文件', '来源行', '原文行号', '结论'];
  const lines = [head.join(',')];
  for (const f of queue) {
    lines.push([f.client, f.level, f.pack, f.category,
      f.source_file, f.source_line, f.line, f.message].map(csvCell).join(','));
  }
  return lines.join('\n');
}

/* 跨客户汇总台账：**客户 × 检查项总表 + 风险处理清单 + 共性问题归类 + 导出**。
   台账必须能说出**哪些客户没跑**（诚实边界）⇒ 从**全部行**里筛 `not_run_objects`；
   **总表只收跑过的行**（没跑过的不能混进总表冒充"核过"）。 */
function buildLedger(result) {
  const rows = result.clients.filter((r) => r.status === 'ok');
  const matrix = ledgerMatrix(rows);
  const queue = ledgerRiskQueue(result.findings);
  const common = ledgerCommonIssues(queue);
  const actions = ledgerActionItems(rows);
  const counts = countLevels(queue);
  const notRunObjects = result.clients.filter((r) => r.status !== 'ok').map((r) => r.client);
  const ledger = {
    matrix, risk_queue: queue, common_issues: common, action_items: actions, counts,
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
      '一个客户的材料都没收到（clients[] 与 text 都是空）',
      '单客户用 {"text":"…"}；批量用 {"clients":[{"name":"客户名","files":[{"name":"材料.txt","text":"…"}]}]}',
    ]);
  }
  const clients = normalizeClients(payload);
  if (!clients.length) {
    return insufficient([
      '一个客户的材料都没收到（clients[] 与 text 都是空）',
      '每个客户一个子目录，目录里放该客户的标准表文本（Tab 分隔最稳）',
    ]);
  }

  const rows = clients.map(runOneClient);
  const usable = rows.filter((r) => r.status === 'ok');
  if (!usable.length) {
    return insufficient(
      [`全部 ${rows.length} 个客户都没有可用材料（每个客户目录里要有该客户的标准表文本）`]
        .concat(rows.map((r) => `客户「${r.client}」：没有材料`)),
      '把每个客户的月结材料放进各自子目录后再跑；材料不足时本工具不做任何认定、也不给任何结论。');
  }

  const findings = [];
  for (const r of rows) for (const f of r.findings) findings.push(f);
  findings.sort((a, b) => (a.client < b.client ? -1 : a.client > b.client ? 1 : 0)
    || (a.line - b.line) || String(a.category).localeCompare(String(b.category)));

  const lv = countLevels(findings);
  const withIssues = rows.filter((r) => r.findings.length > 0).length;
  const notRunClients = rows.filter((r) => r.status !== 'ok').length;

  const result = {
    status: 'success',
    service_type: 'AGENCY_MONTHLY_CLOSE',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: CHECKS_WITHHELD.slice(),
      sub_checks_not_run: SUB_CHECKS_WITHHELD.slice(),
      clients: rows.length,
      clients_ran: usable.length,
      sub_checks_per_client: TOTAL_SUB_CHECKS,
      executed_locally: true,
      network_used: false,
    },
    clients: rows,
    findings,
    summary: {
      clients: rows.length,
      clients_with_issues: withIssues,
      clients_clean: usable.length - withIssues,
      clients_not_run: notRunClients,
      total: findings.length,
      p0: lv.p0, p1: lv.p1, p2: lv.p2,
      verdict: lv.p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本次对 ${rows.length} 个客户逐个跑了 ${CHECKS_GIVEN.length} 个行业月度自查包（每个包 `
      + `${TOTAL_SUB_CHECKS / CHECKS_GIVEN.length} 项子检查）；未执行的检查项见 scope.checks_not_run 与 `
      + 'scope.sub_checks_not_run。',
    disclaimer: '只把各客户材料里的表内/表间算术与勾稽核一遍，结论都带**原文文件与行号**、可由第三方复算；'
      + '**不代替做账、不出具鉴证意见**，也不判断账务处理是否合规。',
  };

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

  return { status: 'success', result };
}

module.exports = {
  run, runOneClient, normalizeClients, coerceFiles, assembleClient, countLevels, checkClientCoverage,
  CHECKS_GIVEN, CHECKS_WITHHELD, SUB_CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, SAMPLE_CLIENTS,
};
