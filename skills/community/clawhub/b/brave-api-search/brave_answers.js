#!/usr/bin/env node
// Brave AI Answers - uses Brave AI Grounding (chat/completions) endpoint
// Requires: BRAVE_ANSWERS_API_KEY env var
//
// IMPORTANT: Citations, entities, and research mode REQUIRE streaming mode (stream: true).
// This skill uses streaming by default for full feature coverage.

const BASE_URL = 'https://api.search.brave.com/res/v1';
const { parseArgs, fetchWithRetry } = require('./utils');

function getApiKey() {
  return process.env.BRAVE_ANSWERS_API_KEY || null;
}

// ─── HTML stripper (shared) ──────────────────────────────────────────────────

function stripHtml(text) {
  if (!text) return '';
  return text
    .replace(/<[^>]+>/g, '')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&#x27;/g, "'")
    .replace(/&#x2F;/g, '/')
    .replace(/&#39;/g, "'")
    .replace(/&quot;/g, '"')
    .trim();
}

// ─── Citation & entity parsing ────────────────────────────────────────────────

function parseCitations(text) {
  const sources = [];
  const seen = new Set();

  const citationRegex = /<citation>([\s\S]*?)<\/citation>/g;
  let match;
  while ((match = citationRegex.exec(text)) !== null) {
    try {
      const citation = JSON.parse(match[1]);
      if (citation.url && !seen.has(citation.url)) {
        seen.add(citation.url);
        sources.push({
          url: citation.url,
          title: citation.title || citation.url,
          snippet: citation.snippet || '',
          number: citation.number,
        });
      }
    } catch {
      // ignore malformed citation
    }
  }

  const cleanText = text
    .replace(/<citation>[\s\S]*?<\/citation>/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  return { cleanText, sources };
}

function parseEntities(text) {
  const entities = [];
  const entityRegex = /<enum_item>([\s\S]*?)<\/enum_item>/g;
  let match;
  while ((match = entityRegex.exec(text)) !== null) {
    try {
      const entity = JSON.parse(match[1]);
      if (entity.name) {
        entities.push({
          name: entity.name,
          href: entity.href || '',
          originalTokens: entity.original_tokens || '',
          citations: entity.citations || [],
        });
      }
    } catch {
      // ignore malformed entity
    }
  }
  return entities;
}

// ─── Streaming answer handler ──────────────────────────────────────────────────

async function streamAnswer(query, country, enableCitations, enableResearch, enableEntities) {
  const apiKey = getApiKey();
  if (!apiKey) {
    console.error('Error: BRAVE_ANSWERS_API_KEY environment variable not set.');
    console.error('Get your key at: https://api-dashboard.search.brave.com');
    process.exit(1);
  }

  const body = {
    model: 'brave',
    messages: [{ role: 'user', content: query }],
    stream: true,
    extra_body: {
      country,
      language: 'en',
      enable_citations: enableCitations,
      enable_research: enableResearch,
      enable_entities: enableEntities,
    },
  };

  const res = await fetchWithRetry(`${BASE_URL}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-Subscription-Token': apiKey,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errBody = await res.text();
    console.error(`Brave Answers API error ${res.status}: ${errBody}`);
    process.exit(1);
  }

  // Collect all chunks for final formatting
  let fullContent = '';
  let usageLine = '';
  let sources = [];
  let seenUrls = new Set();

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  process.stdout.write('**Query:** ' + query + '\n\n');

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop(); // keep incomplete line

    for (const line of lines) {
      if (!line.startsWith('data: ')) continue;
      const data = line.slice(6).trim();
      if (data === '[DONE]' || data === '') continue;

      let chunk;
      try {
        chunk = JSON.parse(data);
      } catch {
        continue;
      }

      const delta = chunk.choices?.[0]?.delta?.content || '';
      if (!delta) continue;

      // Handle special tags
      if (delta.startsWith('<citation>')) {
        const citationText = delta.replace(/<citation>/g, '').replace(/<\/citation>/g, '');
        try {
          const citation = JSON.parse(citationText);
          if (citation.url && !seenUrls.has(citation.url)) {
            seenUrls.add(citation.url);
            sources.push({
              url: citation.url,
              title: citation.title || citation.url,
              snippet: citation.snippet || '',
              number: citation.number,
            });
          }
        } catch {
          // partial citation — skip
        }
        fullContent += delta;
      } else if (delta.startsWith('<usage>')) {
        usageLine = delta;
        fullContent += delta;
      } else if (delta.startsWith('<enum_item>')) {
        // Format and stream entity item immediately
        const entityText = delta.replace('<enum_item>', '').replace('</enum_item>', '');
        try {
          const entity = JSON.parse(entityText);
          const label = entity.original_tokens || entity.name || '';
          const href = entity.href || '';
          if (label) {
            process.stdout.write(` *${label}*`);
            if (href) process.stdout.write(`(${href})`);
            process.stdout.write(' ');
          }
        } catch {
          // malformed entity tag — stream as plain text
          process.stdout.write(delta);
        }
        fullContent += delta;
      } else {
        // Plain text — stream it immediately
        process.stdout.write(delta);
        fullContent += delta;
      }
    }
  }

  process.stdout.write('\n');

  // Entities section
  const entities = parseEntities(fullContent);
  if (entities.length > 0) {
    process.stdout.write('\n**Entities mentioned:**\n');
    entities.forEach(e => {
      const citeNote = e.citations.length > 0
        ? ` (cited in ${e.citations.length} place${e.citations.length > 1 ? 's' : ''})`
        : '';
      if (e.href) {
        process.stdout.write(`- [${e.name}](${e.href})${citeNote}\n`);
      } else {
        process.stdout.write(`- ${e.name}${citeNote}\n`);
      }
    });
  }

  // Print sources at the end
  if (sources.length > 0) {
    sources.sort((a, b) => (a.number || 0) - (b.number || 0));
    process.stdout.write('\n**Sources:**\n');
    sources.forEach(s => {
      process.stdout.write(`${s.number || '?'}. [${s.title}](${s.url})\n`);
      if (s.snippet) process.stdout.write(`   > ${s.snippet}\n`);
    });
  }

  // Parse and print usage
  if (usageLine) {
    try {
      const usageJson = usageLine
        .replace('<usage>', '')
        .replace('</usage>', '');
      const usage = JSON.parse(usageJson);
      const totalTokens = (usage['X-Request-Tokens-In'] || 0) + (usage['X-Request-Tokens-Out'] || 0);
      process.stdout.write(
        `\n*Tokens: ${totalTokens} ` +
        `(in: ${usage['X-Request-Tokens-In'] || 0}, out: ${usage['X-Request-Tokens-Out'] || 0})*\n`
      );
      const totalCost = usage['X-Request-Total-Cost'];
      if (totalCost !== undefined && totalCost !== null) {
        process.stdout.write(`*Total cost: $${parseFloat(totalCost).toFixed(5)}*\n`);
      }
    } catch {
      // ignore malformed usage tag
    }
  }
}

// ─── Non-streaming fallback ───────────────────────────────────────────────────

async function getAnswer(query, country, enableCitations, enableResearch, enableEntities) {
  const apiKey = getApiKey();
  if (!apiKey) {
    console.error('Error: BRAVE_ANSWERS_API_KEY environment variable not set.');
    console.error('Get your key at: https://api-dashboard.search.brave.com');
    process.exit(1);
  }

  const body = {
    model: 'brave',
    messages: [{ role: 'user', content: query }],
    stream: false,
    extra_body: {
      country,
      language: 'en',
      enable_citations: enableCitations,
      enable_research: enableResearch,
      enable_entities: enableEntities,
    },
  };

  const res = await fetchWithRetry(`${BASE_URL}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-Subscription-Token': apiKey,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errBody = await res.text();
    console.error(`Brave Answers API error ${res.status}: ${errBody}`);
    process.exit(1);
  }

  return res.json();
}

function formatAnswer(data, query) {
  const content = data.choices?.[0]?.message?.content || '';
  if (!content) return 'No answer returned.';

  const { cleanText, sources } = parseCitations(content);
  const entities = parseEntities(content);
  const lines = [];

  lines.push(`**Query:** ${query}\n`);
  lines.push(cleanText);

  if (entities.length > 0) {
    lines.push('\n**Entities mentioned:**');
    entities.forEach(e => {
      if (e.href) {
        lines.push(`- [${e.name}](${e.href})`);
      } else {
        lines.push(`- ${e.name}`);
      }
    });
  }

  if (sources.length > 0) {
    lines.push('\n**Sources:**');
    sources.sort((a, b) => (a.number || 0) - (b.number || 0));
    sources.forEach(s => {
      lines.push(`${s.number || '?'}. [${s.title}](${s.url})`);
      if (s.snippet) lines.push(`   > ${s.snippet}`);
    });
  }

  const usage = data.usage;
  if (usage) {
    lines.push(`\n*Tokens: ${usage.total_tokens} (prompt: ${usage.prompt_tokens}, completion: ${usage.completion_tokens})*`);
  }

  return lines.join('\n');
}

// ─── Main ───────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv);

  const query = args.query;
  if (!query) {
    console.error(
      'Usage: brave_answers.js --query "your question" [--country us]\n' +
      '  [--enable-citations true] [--enable-research false] [--enable-entities false]\n' +
      '  [--stream true|false]  (default: true — required for citations/entities)'
    );
    process.exit(1);
  }

  const country = args.country || 'us';
  const enableCitations = args['enable-citations'] !== 'false';
  const enableResearch = args['enable-research'] === 'true';
  const enableEntities = args['enable-entities'] === 'true';
  const useStream = args.stream !== 'false'; // streaming ON by default

  if (useStream) {
    await streamAnswer(query, country, enableCitations, enableResearch, enableEntities);
  } else {
    const data = await getAnswer(query, country, enableCitations, enableResearch, enableEntities);
    console.log(formatAnswer(data, query));
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});