function scoreResult(result) {
  let score = 0;
  if (result.mentioned) score += 35;
  if (typeof result.rank === 'number') score += Math.max(0, 30 - (result.rank - 1) * 5);
  if (result.sentiment === 'positive') score += 20;
  else if (result.sentiment === 'neutral') score += 10;
  score += Math.max(0, 15 - (result.competitors?.length || 0) * 2);
  return Math.max(0, Math.min(100, score));
}

function opportunityScore(result) {
  const meta = result.promptMeta || {};
  let score = 0;
  if (!result.mentioned) score += 40;
  if ((result.competitors?.length || 0) > 0) score += 20;

  const valueMap = { low: 5, medium: 12, high: 20 };
  const difficultyMap = { easy: 15, medium: 10, hard: 5 };
  score += valueMap[meta.commercialValue] || 0;
  score += difficultyMap[meta.difficulty] || 0;

  if (meta.intent === 'comparison' || meta.intent === 'setup' || meta.intent === 'cost') score += 10;
  if (meta.journeyStage === 'decision' || meta.journeyStage === 'consideration') score += 10;

  return Math.max(0, Math.min(100, score));
}

function buildSummary(results = []) {
  const scored = results.map((item) => ({ ...item, score: item.score ?? scoreResult(item) }));
  const opportunities = scored
    .filter((item) => !item.mentioned)
    .map((item) => ({
      prompt: item.prompt,
      engine: item.engine,
      competitors: item.competitors || [],
      promptMeta: item.promptMeta || {},
      opportunityScore: opportunityScore(item),
    }))
    .sort((a, b) => b.opportunityScore - a.opportunityScore)
    .slice(0, 20);

  return {
    overallScore: scored.length ? Math.round(scored.reduce((sum, item) => sum + item.score, 0) / scored.length) : 0,
    engineMentions: [...new Set(scored.filter((item) => item.mentioned).map((item) => item.engine))].length,
    bestRank: scored.filter((item) => typeof item.rank === 'number').map((item) => item.rank).sort((a, b) => a - b)[0] ?? null,
    competitors: [...new Set(scored.flatMap((item) => item.competitors || []))],
    sentimentBreakdown: {
      positive: scored.filter((item) => item.sentiment === 'positive').length,
      neutral: scored.filter((item) => item.sentiment === 'neutral').length,
      negative: scored.filter((item) => item.sentiment === 'negative').length,
      not_mentioned: scored.filter((item) => item.sentiment === 'not_mentioned').length,
      unknown: scored.filter((item) => item.sentiment === 'unknown').length,
    },
    topOpportunities: opportunities,
  };
}

module.exports = {
  scoreResult,
  opportunityScore,
  buildSummary,
};
