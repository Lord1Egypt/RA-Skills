#!/usr/bin/env node
/**
 * collect-session.mjs
 * OpenClaw Session Collector
 *
 * Parses an OpenClaw session JSONL file and:
 *   1. Extracts stats: turns, tool calls, models, cost, duration
 *   2. Calls an LLM via LiteLLM for: session name, keywords, and summary
 *   3. Writes a rich Markdown file to <output-dir>/sessions/
 *   4. Appends a full record to <output-dir>/session-log.jsonl
 *   5. Appends a row to <output-dir>/SESSION-INDEX.md
 *
 * Requires LiteLLM to be running locally — used for cost data and LLM enrichment.
 *
 * Usage:
 *   node collect-session.mjs                          # collect most recent completed session
 *   node collect-session.mjs <session-id-or-path>    # collect specific session
 *   node collect-session.mjs --current               # collect currently active session (for /new hook)
 *   node collect-session.mjs --no-llm <id>           # skip LLM enrichment, use heuristic title
 *   node collect-session.mjs --force <id>            # re-collect even if already logged
 *   node collect-session.mjs --sweep                 # collect ALL uncollected sessions (for cron)
 *
 * Configuration (edit the CONFIG block below or set environment variables):
 *   COLLECT_SESSION_OUTPUT_DIR  — where to write session files (default: ~/workspace/memory)
 *   LITELLM_BASE_URL            — LiteLLM proxy base URL (default: http://localhost:4000)
 *   LITELLM_API_KEY             — LiteLLM virtual key to use for LLM enrichment
 *   COLLECT_SESSION_LLM_MODEL   — model to use for enrichment (default: gemini-2.0-flash)
 */

import fs from 'fs';
import path from 'path';
import readline from 'readline';
import os from 'os';

// ── CONFIG — edit these or set environment variables ─────────────────────────

// Where to write session output files (sessions/, SESSION-INDEX.md, session-log.jsonl)
// Agent: set this to your workspace memory directory, e.g. ~/clio/workspace/memory
// Or leave as null to use the default: ~/workspace/memory
const OUTPUT_DIR_DEFAULT = process.env.COLLECT_SESSION_OUTPUT_DIR
  || path.join(os.homedir(), 'workspace', 'memory');

// LiteLLM proxy URL — must be running locally
// Agent: verify this matches your LiteLLM config (check TOOLS.md or run: lsof -i :4000)
const LITELLM_BASE = process.env.LITELLM_BASE_URL || 'http://localhost:4000';

// LiteLLM virtual key — use a low-cost key (e.g. your cron or batch key)
// Agent: find your virtual keys in LiteLLM dashboard or 1Password.
// Set the LITELLM_API_KEY env var or replace the placeholder below.
const LITELLM_KEY = process.env.LITELLM_API_KEY || 'YOUR_LITELLM_VIRTUAL_KEY';

// LLM model for session naming/summarization — cheapest available is fine
// Agent: use a fast, low-cost model (e.g. gemini-2.0-flash, gpt-4o-mini, claude-haiku-3-5)
const LLM_MODEL = process.env.COLLECT_SESSION_LLM_MODEL || 'gemini-2.0-flash';

// OpenClaw sessions directory
// Agent: this is usually ~/.openclaw/agents/main/sessions — adjust if you use a custom agent name
const SESSIONS_DIR = path.join(os.homedir(), '.openclaw', 'agents', 'main', 'sessions');

// ── PRICING TABLE ($ per million tokens) ─────────────────────────────────────
// Update as model pricing changes. Sources: Anthropic, OpenAI, Google published pricing.
const MODEL_PRICING = {
  'claude-sonnet-4-6':   { input: 3.00,  output: 15.00, cacheRead: 0.30,  cacheWrite: 3.75 },
  'claude-opus-4-6':     { input: 15.00, output: 75.00, cacheRead: 1.50,  cacheWrite: 18.75 },
  'claude-haiku-3-5':    { input: 0.80,  output: 4.00,  cacheRead: 0.08,  cacheWrite: 1.00 },
  'gpt-4o':              { input: 2.50,  output: 10.00, cacheRead: 1.25,  cacheWrite: 0 },
  'gpt-4o-mini':         { input: 0.15,  output: 0.60,  cacheRead: 0.075, cacheWrite: 0 },
  'gemini-2.0-flash':    { input: 0.075, output: 0.30,  cacheRead: 0,     cacheWrite: 0 },
  'gemini-2.5-pro':      { input: 1.25,  output: 10.00, cacheRead: 0,     cacheWrite: 0 },
  // Agent: add additional models here as needed
};

// ─────────────────────────────────────────────────────────────────────────────

function deriveCost(modelId, usage) {
  if (usage.cost?.total > 0) return usage.cost.total;
  let pricing = MODEL_PRICING[modelId];
  if (!pricing) {
    const key = Object.keys(MODEL_PRICING).find(k => modelId.includes(k) || k.includes(modelId));
    pricing = key ? MODEL_PRICING[key] : null;
  }
  if (!pricing) return 0;
  const M = 1_000_000;
  return (
    ((usage.input || 0) * pricing.input / M) +
    ((usage.output || 0) * pricing.output / M) +
    ((usage.cacheRead || 0) * pricing.cacheRead / M) +
    ((usage.cacheWrite || 0) * pricing.cacheWrite / M)
  );
}

function slugify(str) {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .slice(0, 60);
}

function formatCost(n) {
  return n == null ? '$0.0000' : `$${Number(n).toFixed(4)}`;
}

function formatDuration(ms) {
  const mins = Math.round(ms / 60000);
  if (mins < 60) return `${mins}m`;
  return `${Math.floor(mins / 60)}h ${mins % 60}m`;
}

// ── Find session file ─────────────────────────────────────────────────────────

function findSessionFile(arg) {
  if (!arg) {
    const files = fs.readdirSync(SESSIONS_DIR)
      .filter(f => f.endsWith('.jsonl') && !f.includes('.reset'))
      .map(f => ({ f, mtime: fs.statSync(path.join(SESSIONS_DIR, f)).mtimeMs }))
      .sort((a, b) => b.mtime - a.mtime);
    if (!files.length) throw new Error('No session files found');
    return path.join(SESSIONS_DIR, files[0].f);
  }
  if (fs.existsSync(arg)) return arg;
  const allCandidates = fs.readdirSync(SESSIONS_DIR)
    .filter(f => f.startsWith(arg) && (f.endsWith('.jsonl') || f.includes('.reset')));
  const liveCandidates = allCandidates.filter(f => f.endsWith('.jsonl') && !f.includes('.reset'));
  if (liveCandidates.length === 1) return path.join(SESSIONS_DIR, liveCandidates[0]);
  if (liveCandidates.length > 1) throw new Error(`Ambiguous session ID: ${arg}`);
  const resetCandidates = allCandidates.filter(f => f.includes('.reset'));
  if (resetCandidates.length === 1) return path.join(SESSIONS_DIR, resetCandidates[0]);
  if (resetCandidates.length > 1) {
    resetCandidates.sort((a, b) => b.localeCompare(a));
    return path.join(SESSIONS_DIR, resetCandidates[0]);
  }
  throw new Error(`Session not found: ${arg}`);
}

// ── Parse JSONL ───────────────────────────────────────────────────────────────

async function parseSession(filePath) {
  const stats = {
    sessionId: null,
    startTime: null,
    endTime: null,
    userTurns: 0,
    assistantTurns: 0,
    toolCalls: {},
    models: {},
    totalCost: 0,
    firstUserText: null,
    userTexts: [],
  };

  const rl = readline.createInterface({
    input: fs.createReadStream(filePath),
    crlfDelay: Infinity,
  });

  for await (const line of rl) {
    if (!line.trim()) continue;
    let obj;
    try { obj = JSON.parse(line); } catch { continue; }

    const ts = obj.timestamp ? new Date(obj.timestamp).getTime() : null;
    if (ts) {
      if (!stats.startTime || ts < stats.startTime) stats.startTime = ts;
      if (!stats.endTime || ts > stats.endTime) stats.endTime = ts;
    }

    if (obj.type === 'session') {
      stats.sessionId = obj.id;
    }

    if (obj.type === 'message') {
      const msg = obj.message || {};
      const role = msg.role;
      const content = msg.content || [];

      if (role === 'user') {
        stats.userTurns++;
        if (Array.isArray(content)) {
          for (const block of content) {
            if (block?.type === 'text' && block.text) {
              const raw = block.text.trim();
              // Strip OpenClaw sender envelope if present
              let cleaned = raw;
              const timestampMatch = raw.match(/\[\w{3} \d{4}-\d{2}-\d{2} \d{2}:\d{2} \w+\] ([\s\S]+)/);
              if (timestampMatch) {
                cleaned = timestampMatch[1].trim();
              } else if (raw.startsWith('Sender (untrusted metadata)')) {
                continue;
              }
              cleaned = cleaned.slice(0, 120);
              if (!cleaned) continue;
              stats.userTexts.push(cleaned);
              if (!stats.firstUserText) stats.firstUserText = cleaned;
              break;
            }
          }
        }
      }

      if (role === 'assistant') {
        stats.assistantTurns++;
        if (Array.isArray(content)) {
          for (const block of content) {
            if (block?.type === 'toolCall' && block.name) {
              stats.toolCalls[block.name] = (stats.toolCalls[block.name] || 0) + 1;
            }
          }
        }
        if (msg.usage && msg.model) {
          const modelId = msg.model;
          if (!stats.models[modelId]) {
            stats.models[modelId] = { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, cost: 0 };
          }
          const m = stats.models[modelId];
          const u = msg.usage;
          m.input += u.input || 0;
          m.output += u.output || 0;
          m.cacheRead += u.cacheRead || 0;
          m.cacheWrite += u.cacheWrite || 0;
          const c = deriveCost(modelId, u);
          m.cost += c;
          stats.totalCost += c;
        }
      }
    }
  }

  return stats;
}

// ── LLM enrichment ────────────────────────────────────────────────────────────

function heuristicTitle(stats) {
  if (!stats.firstUserText) return 'Untitled Session';
  const txt = stats.firstUserText
    .replace(/^(hi|hey|ok|okay|so|can you|please|i want to|let's|let me|we need to)\s+/i, '')
    .replace(/\?$/, '')
    .trim();
  return txt.charAt(0).toUpperCase() + txt.slice(1);
}

async function enrichWithLLM(stats, skipLLM) {
  if (skipLLM) {
    return { name: heuristicTitle(stats), keywords: [], summary: null, llm_cost_usd: 0 };
  }

  if (LITELLM_KEY === 'YOUR_LITELLM_VIRTUAL_KEY') {
    console.warn('⚠️  LITELLM_API_KEY not configured — falling back to heuristic title. Set LITELLM_API_KEY env var or edit the CONFIG block in collect-session.mjs.');
    return { name: heuristicTitle(stats), keywords: [], summary: null, llm_cost_usd: 0 };
  }

  const durationMins = (stats.startTime && stats.endTime)
    ? Math.round((stats.endTime - stats.startTime) / 60000)
    : null;
  const toolSummary = Object.entries(stats.toolCalls)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(([name, count]) => `${name}x${count}`)
    .join(', ');
  const sampleTurns = stats.userTexts
    .slice(0, 5)
    .map(t => t.replace(/[^\x20-\x7E]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 80))
    .filter(Boolean)
    .map((t, i) => `${i + 1}. ${t}`)
    .join(' | ');

  const prompt = `Analyze this AI session and return ONLY a JSON object (no markdown, no fences, start with {, end with }).` +
    ` Duration: ${durationMins ?? '?'} min. User turns: ${stats.userTurns}. Tools: ${toolSummary || 'none'}.` +
    ` Sample messages: ${sampleTurns || '(none)'}.` +
    ` Return: {"name":"4-8 word title case title of what was done","keywords":["tag1","tag2","tag3","tag4","tag5"],"summary":"2-3 sentence past-tense factual summary of what was built or decided."}`;

  try {
    const resp = await fetch(`${LITELLM_BASE}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${LITELLM_KEY}`,
      },
      body: JSON.stringify({
        model: LLM_MODEL,
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.2,
        max_tokens: 512,
      }),
    });

    if (!resp.ok) {
      const err = await resp.text();
      console.warn(`⚠️  LLM call failed (${resp.status}): ${err.slice(0, 120)} — falling back to heuristic`);
      return { name: heuristicTitle(stats), keywords: [], summary: null, llm_cost_usd: 0 };
    }

    const data = await resp.json();
    const raw = data.choices?.[0]?.message?.content?.trim() || '';
    const usage = data.usage || {};

    const llm_cost_usd = parseFloat((
      ((usage.prompt_tokens || 0) * 0.075 / 1_000_000) +
      ((usage.completion_tokens || 0) * 0.30 / 1_000_000)
    ).toFixed(8));

    let parsed;
    try {
      const jsonMatch = raw.match(/\{[\s\S]*\}/);
      if (!jsonMatch) throw new Error('no JSON object found');
      parsed = JSON.parse(jsonMatch[0]);
    } catch (parseErr) {
      console.warn(`⚠️  LLM returned non-JSON: ${raw.slice(0, 120)} — falling back to heuristic`);
      return { name: heuristicTitle(stats), keywords: [], summary: null, llm_cost_usd };
    }

    return {
      name: parsed.name || heuristicTitle(stats),
      keywords: Array.isArray(parsed.keywords) ? parsed.keywords.slice(0, 8) : [],
      summary: parsed.summary || null,
      llm_cost_usd,
    };
  } catch (e) {
    console.warn(`⚠️  LLM enrichment error: ${e.message} — falling back to heuristic`);
    return { name: heuristicTitle(stats), keywords: [], summary: null, llm_cost_usd: 0 };
  }
}

// ── Write session MD ──────────────────────────────────────────────────────────

function writeSessionMD(stats, filePath, enrichment, outputDir) {
  const sessionsDir = path.join(outputDir, 'sessions');
  const date = stats.startTime
    ? new Date(stats.startTime).toISOString().slice(0, 10)
    : new Date().toISOString().slice(0, 10);

  const title = enrichment.name;
  const slug = slugify(title);
  const filename = `${date}-${slug}.md`;
  const outPath = path.join(sessionsDir, filename);

  const duration = (stats.startTime && stats.endTime)
    ? formatDuration(stats.endTime - stats.startTime)
    : 'unknown';
  const durationMins = (stats.startTime && stats.endTime)
    ? Math.round((stats.endTime - stats.startTime) / 60000)
    : null;

  const totalToolCalls = Object.values(stats.toolCalls).reduce((a, b) => a + b, 0);

  const toolRows = Object.entries(stats.toolCalls)
    .sort((a, b) => b[1] - a[1])
    .map(([name, count]) => {
      const pct = totalToolCalls > 0 ? ((count / totalToolCalls) * 100).toFixed(0) : 0;
      return `| \`${name}\` | ${count} | ${pct}% |`;
    }).join('\n') || '| (none) | 0 | 0% |';

  const toolList = Object.entries(stats.toolCalls)
    .sort((a, b) => b[1] - a[1])
    .map(([name, count]) => `${name} (${count})`)
    .join(', ') || 'none';

  const modelRows = Object.entries(stats.models)
    .map(([id, m]) => {
      const cacheInfo = m.cacheRead ? ` / ${m.cacheRead.toLocaleString()} cached` : '';
      return `| \`${id}\` | ${m.input.toLocaleString()} | ${m.output.toLocaleString()}${cacheInfo} | ${m.cacheWrite.toLocaleString()} | ${formatCost(m.cost)} |`;
    }).join('\n') || '| (none) | — | — | — | — |';

  const keywordLine = enrichment.keywords.length > 0
    ? enrichment.keywords.map(k => `\`${k}\``).join(' · ')
    : '*(none)*';

  const summarySection = enrichment.summary
    ? `## Summary\n\n${enrichment.summary}\n`
    : '';

  const sourceFile = path.basename(filePath);
  const collectedAt = new Date().toISOString().slice(0, 16).replace('T', ' ');

  const md = `---
session_id: ${stats.sessionId || 'unknown'}
date: ${date}
name: ${title}
keywords: [${enrichment.keywords.map(k => `"${k}"`).join(', ')}]
duration_minutes: ${durationMins ?? 'null'}
user_turns: ${stats.userTurns}
assistant_turns: ${stats.assistantTurns}
tool_calls_total: ${totalToolCalls}
total_cost_usd: ${stats.totalCost.toFixed(6)}
source_file: ${sourceFile}
source_path: ${filePath}
---

# ${title}

**Date:** ${date} · **Duration:** ${duration} · **Cost:** ${formatCost(stats.totalCost)}
**Keywords:** ${keywordLine}

${summarySection}
---

## Analytics

### Turns

| Metric | Value |
|---|---|
| User turns | ${stats.userTurns} |
| Assistant turns | ${stats.assistantTurns} |
| Total turns | ${stats.userTurns + stats.assistantTurns} |
| Total tool calls | ${totalToolCalls} |

### Tool Call Distribution

| Tool | Calls | Share |
|---|---|---|
${toolRows}

### Model Usage

| Model | Input tokens | Output tokens | Cache writes | Cost |
|---|---|---|---|---|
${modelRows}
| **Total** | | | | **${formatCost(stats.totalCost)}** |

---

*Collected by collect-session (openclaw-skill) · ${collectedAt} UTC · Source: \`${sourceFile}\`*
`;

  fs.mkdirSync(sessionsDir, { recursive: true });
  fs.writeFileSync(outPath, md);
  return { outPath, filename, date, title, slug, duration, durationMins, totalToolCalls, toolList };
}

// ── Update session index ──────────────────────────────────────────────────────

function updateIndex(stats, result, outputDir) {
  const indexFile = path.join(outputDir, 'SESSION-INDEX.md');
  const { date, title, filename, duration, totalToolCalls } = result;
  const cost = formatCost(stats.totalCost);
  const modelNames = Object.keys(stats.models).join(', ') || 'unknown';
  const sessionId = stats.sessionId || 'unknown';

  const entry = `| ${date} | [${title}](sessions/${filename}) | ${stats.userTurns} | ${totalToolCalls} | ${cost} | ${modelNames} | \`${sessionId.slice(0, 8)}\` |\n`;

  if (!fs.existsSync(indexFile)) {
    const header = `# Session Index

A running log of all collected OpenClaw sessions.
Generated by collect-session (openclaw-skill).

---

| Date | Session | Turns | Tool Calls | Cost | Models | ID |
|---|---|---|---|---|---|---|
`;
    fs.writeFileSync(indexFile, header + entry);
  } else {
    fs.appendFileSync(indexFile, entry);
  }
}

// ── Append to JSONL log ───────────────────────────────────────────────────────

function appendToLog(stats, result, enrichment, filePath, outputDir) {
  const logFile = path.join(outputDir, 'session-log.jsonl');
  const totalToolCalls = Object.values(stats.toolCalls).reduce((a, b) => a + b, 0);
  const toolDistribution = Object.fromEntries(
    Object.entries(stats.toolCalls)
      .sort((a, b) => b[1] - a[1])
      .map(([name, count]) => [name, {
        count,
        pct: totalToolCalls > 0 ? parseFloat(((count / totalToolCalls) * 100).toFixed(1)) : 0,
      }])
  );

  const record = {
    collected_at: new Date().toISOString(),
    session_id: stats.sessionId,
    source_file: path.basename(filePath),
    date: result.date,
    name: enrichment.name,
    keywords: enrichment.keywords,
    summary: enrichment.summary,
    duration_minutes: result.durationMins,
    user_turns: stats.userTurns,
    assistant_turns: stats.assistantTurns,
    total_turns: stats.userTurns + stats.assistantTurns,
    tool_calls_total: totalToolCalls,
    tool_calls_distribution: toolDistribution,
    models: Object.fromEntries(
      Object.entries(stats.models).map(([id, m]) => [id, {
        input_tokens: m.input,
        output_tokens: m.output,
        cache_read_tokens: m.cacheRead,
        cache_write_tokens: m.cacheWrite,
        cost_usd: parseFloat(m.cost.toFixed(6)),
      }])
    ),
    total_cost_usd: parseFloat(stats.totalCost.toFixed(6)),
    llm_enrichment_cost_usd: enrichment.llm_cost_usd,
    md_file: result.filename,
    source_path: filePath,
  };

  fs.appendFileSync(logFile, JSON.stringify(record) + '\n');
}

// ── Deduplication ─────────────────────────────────────────────────────────────

function loadCollectedSessionIds(outputDir) {
  const logFile = path.join(outputDir, 'session-log.jsonl');
  const ids = new Map();
  if (!fs.existsSync(logFile)) return ids;
  const lines = fs.readFileSync(logFile, 'utf-8').split('\n').filter(Boolean);
  for (const line of lines) {
    try {
      const record = JSON.parse(line);
      if (record.session_id) {
        const existing = ids.get(record.session_id);
        if (!existing || record.collected_at > existing.collected_at) {
          ids.set(record.session_id, {
            collected_at: record.collected_at,
            md_file: record.md_file,
          });
        }
      }
    } catch { /* skip malformed lines */ }
  }
  return ids;
}

function isSessionActive(filePath) {
  try {
    const stat = fs.statSync(filePath);
    return (Date.now() - stat.mtimeMs) < 60_000;
  } catch {
    return false;
  }
}

// ── Collect a single session ──────────────────────────────────────────────────

async function collectOne(filePath, { skipLLM, force, useCurrent, collected, outputDir }) {
  if (!useCurrent && isSessionActive(filePath)) {
    console.log(`⏭️  Skipping ${path.basename(filePath)} — session still active (use --current to override)`);
    return 'skipped-active';
  }

  const stats = await parseSession(filePath);

  if (!stats.sessionId) {
    console.warn(`⚠️  No session ID in ${path.basename(filePath)} — skipping`);
    return 'skipped-no-id';
  }

  if (!force && collected.get(stats.sessionId)) {
    return 'skipped-dedup';
  }

  console.log(`📂 Parsing: ${path.basename(filePath)}`);
  console.log(`🤖 Enriching with LLM${skipLLM ? ' (skipped)' : ''}...`);
  const enrichment = await enrichWithLLM(stats, skipLLM);

  const result = writeSessionMD(stats, filePath, enrichment, outputDir);
  updateIndex(stats, result, outputDir);
  appendToLog(stats, result, enrichment, filePath, outputDir);

  console.log(`✅ Session collected:`);
  console.log(`   Name:       ${enrichment.name}`);
  console.log(`   Keywords:   ${enrichment.keywords.join(', ') || '(none)'}`);
  console.log(`   Turns:      ${stats.userTurns} user / ${stats.assistantTurns} assistant`);
  console.log(`   Tool calls: ${result.totalToolCalls} — ${result.toolList}`);
  console.log(`   Cost:       ${formatCost(stats.totalCost)} session + ${formatCost(enrichment.llm_cost_usd)} LLM`);
  console.log(`   Duration:   ${result.duration}`);
  console.log(`   Output:     ${result.outPath}`);

  collected.set(stats.sessionId, { collected_at: new Date().toISOString(), md_file: result.filename });
  return 'collected';
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const skipLLM = args.includes('--no-llm');
  const useCurrent = args.includes('--current');
  const force = args.includes('--force');
  const sweep = args.includes('--sweep');
  const outputDirArg = args.find((a, i) => a === '--output-dir' && args[i + 1])
    ? args[args.indexOf('--output-dir') + 1]
    : null;

  const outputDir = outputDirArg
    ? path.resolve(outputDirArg)
    : OUTPUT_DIR_DEFAULT;

  console.log(`📁 Output dir: ${outputDir}`);

  const collected = loadCollectedSessionIds(outputDir);

  if (sweep) {
    const files = fs.readdirSync(SESSIONS_DIR)
      .filter(f => f.endsWith('.jsonl') && !f.includes('.reset'))
      .map(f => ({ f, mtime: fs.statSync(path.join(SESSIONS_DIR, f)).mtimeMs }))
      .sort((a, b) => a.mtime - b.mtime);

    if (!files.length) { console.log('No session files found.'); process.exit(0); }

    let counts = { collected: 0, skipped: 0, errors: 0 };
    for (const { f } of files) {
      try {
        const r = await collectOne(path.join(SESSIONS_DIR, f), { skipLLM, force, useCurrent: false, collected, outputDir });
        if (r === 'collected') counts.collected++; else counts.skipped++;
      } catch (e) {
        console.error(`❌ Error collecting ${f}: ${e.message}`);
        counts.errors++;
      }
    }
    console.log(`\n🧹 Sweep complete: ${counts.collected} collected, ${counts.skipped} skipped, ${counts.errors} errors`);
    process.exit(0);
  }

  const sessionArg = useCurrent ? undefined : args.find(a => !a.startsWith('--') && a !== outputDirArg);
  let filePath;
  try {
    filePath = findSessionFile(sessionArg);
  } catch (e) {
    console.error(`❌ ${e.message}`);
    process.exit(1);
  }

  const result = await collectOne(filePath, { skipLLM, force, useCurrent, collected, outputDir });
  if (result === 'skipped-active') {
    console.log(`   Use --current to force collection of the active session.`);
  } else if (result === 'skipped-dedup') {
    const sessionId = path.basename(filePath, '.jsonl');
    const existing = collected.get(sessionId) || { collected_at: 'unknown', md_file: 'unknown' };
    console.log(`⏭️  Session already collected at ${existing.collected_at}`);
    console.log(`   Output: ${existing.md_file}`);
    console.log(`   Use --force to re-collect.`);
  }
  const logFile = path.join(outputDir, 'session-log.jsonl');
  console.log(`   Log: ${logFile}`);
}

main().catch(e => { console.error(e); process.exit(1); });