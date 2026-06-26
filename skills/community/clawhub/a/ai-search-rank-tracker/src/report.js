const { toCsvRow } = require('./utils');

function renderMarkdownReport(output) {
  const { brand, prompts, engines, summary, results, generatedAt, promptPack } = output;
  const lines = [];
  lines.push('# AI Search Rank Tracker Report');
  lines.push('');
  lines.push(`- **Brand:** ${brand}`);
  lines.push(`- **Prompts:** ${prompts.length}`);
  if (promptPack) lines.push(`- **Prompt pack:** ${Array.isArray(promptPack) ? promptPack.join(', ') : promptPack}`);
  lines.push(`- **Engines:** ${engines.join(', ')}`);
  lines.push(`- **Overall score:** ${summary.overallScore}/100`);
  lines.push(`- **Generated at:** ${generatedAt}`);
  lines.push('');
  lines.push('## Summary');
  lines.push('');
  lines.push(`- Engines mentioning brand: ${summary.engineMentions}`);
  lines.push(`- Best rank: ${summary.bestRank ?? 'not found'}`);
  lines.push(`- Competitors seen: ${summary.competitors.length ? summary.competitors.join(', ') : 'none detected'}`);
  lines.push(`- Sentiment mix: ${JSON.stringify(summary.sentimentBreakdown)}`);
  lines.push('');

  if (summary.topOpportunities?.length) {
    lines.push('## Top GEO opportunities');
    lines.push('');
    for (const item of summary.topOpportunities.slice(0, 10)) {
      lines.push(`- **${item.prompt}** (${item.engine}) — score ${item.opportunityScore}/100`);
      lines.push(`  - Competitors: ${item.competitors.length ? item.competitors.join(', ') : 'none detected'}`);
      if (item.promptMeta?.intent) lines.push(`  - Intent: ${item.promptMeta.intent}`);
      if (item.promptMeta?.commercialValue) lines.push(`  - Commercial value: ${item.promptMeta.commercialValue}`);
    }
    lines.push('');
  }

  lines.push('## Results');
  lines.push('');
  for (const item of results) {
    lines.push(`### ${item.engine} — ${item.prompt}`);
    lines.push(`- Mentioned: ${item.mentioned ? 'yes' : 'no'}`);
    lines.push(`- Rank: ${item.rank ?? 'not found'}`);
    lines.push(`- Mention type: ${item.mentionType}`);
    lines.push(`- Sentiment: ${item.sentiment}`);
    lines.push(`- Competitors: ${item.competitors.length ? item.competitors.join(', ') : 'none detected'}`);
    lines.push(`- Excerpt: ${item.excerpt || 'n/a'}`);
    lines.push(`- Score: ${item.score ?? 'n/a'}`);
    if (item.promptMeta?.category) lines.push(`- Category: ${item.promptMeta.category}`);
    if (item.promptMeta?.intent) lines.push(`- Intent: ${item.promptMeta.intent}`);
    if (item.error) lines.push(`- Error: ${item.error}`);
    lines.push('');
  }
  return lines.join('\n');
}

function renderCsvReport(output) {
  const header = [
    'engine','prompt','brand','mentioned','rank','mentionType','sentiment','competitors','excerpt','score','category','subcategory','intent','journeyStage','difficulty','commercialValue','error','startedAt','finishedAt'
  ];
  const rows = output.results.map((item) => toCsvRow([
    item.engine,
    item.prompt,
    item.brand,
    item.mentioned,
    item.rank ?? '',
    item.mentionType,
    item.sentiment,
    (item.competitors || []).join('|'),
    item.excerpt || '',
    item.score ?? '',
    item.promptMeta?.category || '',
    item.promptMeta?.subcategory || '',
    item.promptMeta?.intent || '',
    item.promptMeta?.journeyStage || '',
    item.promptMeta?.difficulty || '',
    item.promptMeta?.commercialValue || '',
    item.error || '',
    item.startedAt || '',
    item.finishedAt || ''
  ]));
  return [toCsvRow(header), ...rows].join('\n');
}

module.exports = {
  renderMarkdownReport,
  renderCsvReport,
};
