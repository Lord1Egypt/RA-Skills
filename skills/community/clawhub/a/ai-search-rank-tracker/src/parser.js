function normalizeText(text) {
  return String(text || '').toLowerCase().replace(/\s+/g, ' ').trim();
}

function getBrandVariants(brand, aliases = []) {
  return [brand, ...aliases].map((v) => normalizeText(v)).filter(Boolean);
}

function containsBrand(text, brand, aliases = []) {
  const hay = normalizeText(text);
  const variants = getBrandVariants(brand, aliases);
  return variants.some((v) => hay.includes(v));
}

function extractRank(text, brand, aliases = []) {
  const lines = String(text || '').split('\n').map((x) => x.trim()).filter(Boolean);
  const variants = getBrandVariants(brand, aliases);

  for (const line of lines) {
    const lower = line.toLowerCase();
    if (!variants.some((v) => lower.includes(v))) continue;

    let match = lower.match(/^(\d+)\s*[\.)]\s+/);
    if (match) return Number(match[1]);

    match = lower.match(/^[-*]\s*(\d+)\s*[\.)]\s+/);
    if (match) return Number(match[1]);
  }

  return null;
}

function extractCompetitors(text, brand, aliases = []) {
  const known = [
    'lazyclaw',
    'zeroclaw',
    'openclaw',
    'clawnow',
    'opencode',
    'codex',
    'claude code',
    'chatgpt',
    'claude',
    'gemini',
    'perplexity'
  ];

  const hay = normalizeText(text);
  const brandVariants = getBrandVariants(brand, aliases);

  return known.filter((name) => {
    const normalized = normalizeText(name);
    return hay.includes(normalized) && !brandVariants.includes(normalized);
  });
}

function detectSentiment(text, brand, aliases = []) {
  const hay = normalizeText(text);
  const mentioned = containsBrand(hay, brand, aliases);
  if (!mentioned) return 'not_mentioned';

  const positiveWords = [
    'strong option', 'good option', 'recommended', 'stands out', 'easy', 'easier', 'easy to use', 'beginner-friendly', 'secure', 'lightweight', 'simple', 'fast'
  ];
  const negativeWords = [
    'limited', 'unreliable', 'weak', 'not mature', 'hard to use', 'difficult', 'confusing', 'poor', 'not recommended'
  ];

  const positive = positiveWords.some((w) => hay.includes(w));
  const negative = negativeWords.some((w) => hay.includes(w));

  if (positive && !negative) return 'positive';
  if (negative && !positive) return 'negative';
  return 'neutral';
}

function extractExcerpt(text, brand, aliases = []) {
  const lines = String(text || '').split('\n').map((x) => x.trim()).filter(Boolean);
  const variants = getBrandVariants(brand, aliases);

  for (const line of lines) {
    const lower = line.toLowerCase();
    if (variants.some((v) => lower.includes(v))) return line;
  }

  return '';
}

function parseResponse({ engine, prompt, brand, aliases, rawResponse }) {
  const mentioned = containsBrand(rawResponse, brand, aliases);
  const rank = mentioned ? extractRank(rawResponse, brand, aliases) : null;
  const competitors = extractCompetitors(rawResponse, brand, aliases);
  const sentiment = detectSentiment(rawResponse, brand, aliases);
  const excerpt = extractExcerpt(rawResponse, brand, aliases);

  return {
    engine,
    prompt,
    brand,
    mentioned,
    rank,
    mentionType: rank ? 'ranked' : mentioned ? 'unranked' : 'none',
    sentiment,
    competitors,
    excerpt,
    rawResponse
  };
}

module.exports = {
  normalizeText,
  getBrandVariants,
  containsBrand,
  extractRank,
  extractCompetitors,
  detectSentiment,
  extractExcerpt,
  parseResponse,
};
