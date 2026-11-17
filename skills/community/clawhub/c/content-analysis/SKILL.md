---
name: content-analysis
description: Extracts actionable insights from any text — word counts, reading time, top keywords, sentiment score, structure analysis.
metadata:
  openclaw:
    emoji: 📊
    homepage: https://tinycoderstudio.gumroad.com/l/7-agent-skills-pack
---
# Skill 4: Content Analysis — Stats, Sentiment & Keywords

## Overview
Extracts actionable insights from any text: word counts, reading time, top keywords, sentiment score, and structure analysis.

## Problem
Content teams need quick insights but manual analysis is slow. Existing tools are expensive or complex.

## Solution
Lightweight analyzer that returns structured insights in <50ms.

## Implementation

```javascript
// analyzer.js
function analyzeContent(input) {
  const text = String(input).trim();
  const words = text.split(/\s+/).filter(w => w.length > 0);
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
  const paragraphs = text.split(/\n\s*\n/).filter(p => p.trim().length > 0);
  
  // Word frequency (top 10, min 4 chars)
  const freq = {};
  for (const w of words) {
    const clean = w.toLowerCase().replace(/[^\w]/g, '');
    if (clean.length > 3) freq[clean] = (freq[clean] || 0) + 1;
  }
  const topWords = Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([word, count]) => ({ word, count }));
  
  // Reading time (avg 200 wpm)
  const readingTimeMin = Math.ceil(words.length / 200);
  
  // Simple sentiment
  const positive = ['good', 'great', 'excellent', 'amazing', 'awesome', 'love', 'best', 'perfect', 'happy', 'success', 'win', 'great', 'fantastic', 'wonderful', 'brilliant'];
  const negative = ['bad', 'terrible', 'awful', 'hate', 'worst', 'fail', 'error', 'problem', 'issue', 'wrong', 'broken', 'poor', 'disappointing', 'frustrating', 'annoying'];
  let sentiment = 0;
  for (const w of words) {
    const lw = w.toLowerCase().replace(/[^\w]/g, '');
    if (positive.includes(lw)) sentiment++;
    if (negative.includes(lw)) sentiment--;
  }
  
  return {
    stats: {
      chars: text.length,
      words: words.length,
      sentences: sentences.length,
      paragraphs: paragraphs.length,
      reading_time_min: readingTimeMin
    },
    top_words: topWords,
    sentiment_score: sentiment,
    sentiment_label: sentiment > 2 ? 'positive' : sentiment < -2 ? 'negative' : 'neutral'
  };
}

// Usage
const result = analyzeContent("This is amazing! I love this product. It works great. Best purchase ever. Highly recommend!");
/*
{
  stats: { chars: 91, words: 15, sentences: 5, paragraphs: 1, reading_time_min: 1 },
  top_words: [{word:"this",count:2},{word:"amazing",count:1},...],
  sentiment_score: 4,
  sentiment_label: "positive"
}
*/
```

## Batch Analysis

```javascript
// analyze-batch.js
const fs = require('fs');

function analyzeDirectory(dir) {
  const results = [];
  fs.readdirSync(dir).forEach(file => {
    if (file.endsWith('.md') || file.endsWith('.txt')) {
      const text = fs.readFileSync(`${dir}/${file}`, 'utf8');
      const analysis = analyzeContent(text);
      results.push({ file, ...analysis });
    }
  });
  return results;
}

// Generate report
const report = analyzeDirectory('./blog-posts');
console.table(report.map(r => ({
  file: r.file,
  words: r.stats.words,
  sentiment: r.sentiment_label,
  top_word: r.top_words[0]?.word
})));
```

## x402 Pay-Per-Analyze

```bash
curl -X POST https://your-api.com/api/analyze \
  -H "Content-Type: application/json" \
  -H "X-PAYMENT: <base64_payment>" \
  -d '{"text":"This is amazing! I love this product. It works great. Best purchase ever. Highly recommend!"}'
# Returns: {"stats":{...},"top_words":[...],"sentiment_score":4,"sentiment_label":"positive","agent":"loki"}
```

## Use Cases

| Use Case | Insight |
|----------|---------|
| **Blog optimization** | Find missing keywords, check readability |
| **Customer feedback** | Auto-categorize positive/negative reviews |
| **Content audit** | Find thin content, duplicate topics |
| **SEO planning** | Identify keyword gaps across posts |
| **Social monitoring** | Track brand sentiment over time |

## Customization

```javascript
// Add domain-specific sentiment words
const domainSentiment = {
  positive: ['conversion', 'retention', 'engagement', 'growth', 'revenue', 'roi'],
  negative: ['churn', 'bounce', 'drop', 'decline', 'loss', 'bug', 'downtime']
};

// Add entity extraction
function extractEntities(text) {
  const entities = {
    emails: text.match(/[\w.+-]+@[\w-]+\.[\w.-]+/g) || [],
    urls: text.match(/https?:\/\/[^\s]+/g) || [],
    mentions: text.match(/@\w+/g) || [],
    hashtags: text.match(/#\w+/g) || [],
    currency: text.match(/\$\d+(?:,\d{3})*(?:\.\d{2})?/g) || []
  };
  return entities;
}
```

## Value
- **Speed**: <50ms per analysis
- **Cost**: $0.003 per call via x402
- **No API keys**: Self-contained, no external dependencies
- **Extensible**: Add custom dictionaries, entities, metrics