// Report rendering — 红点清单 + 可重跑的复查清单。
const SEV_LABEL = { high: '🔴 高', medium: '🟠 中', low: '🟡 低' };
const SEV_EN = { high: 'HIGH', medium: 'MED', low: 'LOW' };

function esc(s) { return String(s ?? '').replace(/\|/g, '\\|').replace(/\n/g, ' '); }

export function renderReport(res, opts) {
  const { findings, docs, stats, cmd } = res;
  const { limit, all, lang } = opts;
  const zh = lang !== 'en';
  const L = zh ? SEV_LABEL : SEV_EN;
  const t = zh ? ZH : EN;

  // 每条 finding 都带中英两套文案，这里按语言选一套
  const view = (f) => (zh || !f.en ? f : { ...f, ...f.en });
  const rows = findings.map(view);

  const bySev = { high: 0, medium: 0, low: 0 };
  const byType = new Map();
  for (const f of rows) {
    bySev[f.severity]++;
    byType.set(f.type, (byType.get(f.type) || 0) + 1);
  }

  const out = [];
  out.push(`# ${t.title}`, '');
  out.push(`${t.scanned}${t.c}${docs.map((d) => `\`${d.file}\``).join('、')}`);
  out.push(`${t.blocks}${t.c}${docs.reduce((n, d) => n + d.blocks.length, 0)}　|　${t.captions}${t.c}${stats.captions}　|　${t.refs}${t.c}${stats.refs}`);
  out.push('');

  if (!findings.length) {
    out.push(`## ✅ ${t.clean}`, '', t.cleanNote, '');
    out.push(...recheck(cmd, t));
    out.push(...footer(t));
    return out.join('\n');
  }

  out.push(`## ${t.summary}`, '');
  out.push(`| ${t.sev} | ${t.count} |`, '| --- | ---: |');
  for (const k of ['high', 'medium', 'low']) if (bySev[k]) out.push(`| ${L[k]} | ${bySev[k]} |`);
  out.push(`| **${t.total}** | **${findings.length}** |`, '');

  out.push(`| ${t.type} | ${t.count} |`, '| --- | ---: |');
  for (const [k, v] of [...byType.entries()].sort((a, b) => b[1] - a[1])) out.push(`| ${esc(k)} | ${v} |`);
  out.push('');

  const shown = all ? rows : rows.slice(0, limit);
  out.push(`## ${t.list}${all || rows.length <= limit ? '' : ` (${t.showing} ${shown.length} / ${rows.length}, ${t.useAll})`}`, '');
  out.push(`| # | ${t.sev} | ${t.type} | ${t.where} | ${t.what} | ${t.how} |`);
  out.push('| ---: | --- | --- | --- | --- | --- |');
  for (const f of shown) {
    out.push(`| ${f.id} | ${L[f.severity]} | ${esc(f.type)} | ${esc(f.file)} · ${esc(f.loc)} | ${esc(f.message)}${f.snippet ? `<br>\`${esc(f.snippet)}\`` : ''} | ${esc(f.fix)} |`);
  }
  out.push('');
  out.push(...recheck(cmd, t));
  out.push(...footer(t));
  return out.join('\n');
}

function recheck(cmd, t) {
  return [
    `## ${t.recheckTitle}`, '',
    t.recheckNote, '',
    '```bash',
    cmd,
    `${cmd} --fail-on high    # ${t.failOn}`,
    '```', '',
  ];
}

function footer(t) {
  return [
    '---', '',
    t.footer1, '',
    t.footer2, '',
    `<sub>${t.brand}</sub>`, '',
  ];
}

const ZH = {
  c: '：', title: '长文档一致性体检报告',
  scanned: '受检文件', blocks: '段落数', captions: '识别到的题注', refs: '识别到的引用',
  clean: '未发现问题', cleanNote: '本轮启用的所有确定性规则均已通过。注意：这不等于内容正确，只等于「文档跟自己不矛盾」。',
  summary: '汇总', sev: '严重度', count: '条数', total: '合计', type: '类型',
  list: '红点清单', showing: '显示', useAll: '加 --all 看全部',
  where: '位置', what: '问题', how: '怎么改',
  recheckTitle: '你自己能重跑的复查清单',
  recheckNote: '不用信我们说「查过了没问题」。你自己跑这条命令，看红点从 N 条降到 0：',
  failOn: '还有高危项就返回非 0，可直接写进 CI 或合同验收',
  footer1: '**本工具全程在本机运行，不联网、不上传、不调用任何模型。** 你的文档没有离开过这台机器。',
  footer2: '需要「改好的文件（原格式，不丢页眉页脚与自动编号）」、招标文件符合性矩阵、或跨全书的语义级术语归并？这几项需要人工介入：**HEFANGSHENG@gmail.com**',
  brand: 'doc-consistency · U-King　https://u-king.org　HEFANGSHENG@gmail.com',
};

const EN = {
  c: ': ', title: 'Document Consistency Report',
  scanned: 'Files', blocks: 'Blocks', captions: 'Captions found', refs: 'References found',
  clean: 'No findings', cleanNote: 'All deterministic rules passed. Note: this means the document does not contradict itself — not that its content is correct.',
  summary: 'Summary', sev: 'Severity', count: 'Count', total: 'Total', type: 'Type',
  list: 'Findings', showing: 'showing', useAll: 'pass --all for the full list',
  where: 'Where', what: 'What', how: 'Suggested fix',
  recheckTitle: 'Re-check it yourself',
  recheckNote: 'Do not take "we checked it, it is fine" for an answer. Run this yourself and watch N findings go to 0:',
  failOn: 'non-zero exit while any HIGH remains — drop it into CI or contract acceptance',
  footer1: '**Runs entirely on your machine. No network, no upload, no model calls.** Your document never leaves this computer.',
  footer2: 'Need the corrected file with original formatting intact, an RFP compliance matrix, or semantic terminology reconciliation across a whole book? Those need a human in the loop: **HEFANGSHENG@gmail.com**',
  brand: 'doc-consistency · U-King　https://u-king.org　HEFANGSHENG@gmail.com',
};
