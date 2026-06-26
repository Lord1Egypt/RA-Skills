#!/usr/bin/env node
/**
 * grok_search.mjs
 *
 * Minimal xAI (Grok) search wrapper.
 * - Uses xAI Responses API (OpenAI-compatible)
 * - Lets Grok run server-side tools:
 *   - web_search (web)
 *   - x_search (X/Twitter)
 *
 * Usage:
 *   node scripts/grok_search.mjs "query" --web --json
 *   node scripts/grok_search.mjs "query" --x --days 7 --handles @clawdbot --json
 *   node scripts/grok_search.mjs "query" --x --from 2026-01-01 --to 2026-01-27 --json
 *   node scripts/grok_search.mjs "query" --x --links-only
 *   node scripts/grok_search.mjs "query" --x --raw --json
 */

import { getRuntimeConfig, readApiKeys } from "./shared.mjs";

function usage(msg) {
  if (msg) console.error(msg);
  console.error(
    "Usage: grok_search.mjs <query> (--web|--x) [--json] [--text|--links-only] [--raw] [--model <id>] [--max <n>] [--days <n>] [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--handles a,b] [--exclude a,b]"
  );
  process.exit(2);
}

function readKeyFromClawdbotConfig() {
  return readApiKeys().apiKey;
}

const runtime = getRuntimeConfig();
const args = process.argv.slice(2);
if (args.length === 0) usage();

let queryParts = [];
let mode = null; // 'web' | 'x'
let jsonOut = false;
let rawOut = false;
let format = "json"; // json|text|links
let model = runtime.model;
let maxResults = 8;

// X-search filters
let days = null; // number
let fromDate = null; // YYYY-MM-DD
let toDate = null; // YYYY-MM-DD
let handles = []; // array of handles (no @)
let excludeHandles = [];

for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "--web") mode = "web";
  else if (a === "--x") mode = "x";
  else if (a === "--json") jsonOut = true;
  else if (a === "--raw") rawOut = true;
  else if (a === "--links-only") format = "links";
  else if (a === "--text") format = "text";
  else if (a === "--model") {
    const v = args[++i];
    if (!v) usage("Missing value for --model");
    model = v;
  } else if (a === "--max") {
    const v = Number(args[++i]);
    if (!Number.isFinite(v) || v <= 0) usage("Bad value for --max");
    maxResults = Math.floor(v);
  } else if (a === "--days") {
    const v = Number(args[++i]);
    if (!Number.isFinite(v) || v <= 0) usage("Bad value for --days");
    days = Math.floor(v);
  } else if (a === "--from") {
    const v = args[++i];
    if (!v) usage("Missing value for --from");
    fromDate = v;
  } else if (a === "--to") {
    const v = args[++i];
    if (!v) usage("Missing value for --to");
    toDate = v;
  } else if (a === "--handles") {
    const v = args[++i];
    if (!v) usage("Missing value for --handles");
    handles = v
      .split(",")
      .map((h) => h.trim().replace(/^@/, ""))
      .filter(Boolean);
  } else if (a === "--exclude") {
    const v = args[++i];
    if (!v) usage("Missing value for --exclude");
    excludeHandles = v
      .split(",")
      .map((h) => h.trim().replace(/^@/, ""))
      .filter(Boolean);
  } else if (a.startsWith("-")) {
    usage(`Unknown flag: ${a}`);
  } else {
    queryParts.push(a);
  }
}

if (!jsonOut && format === "json") jsonOut = true;

const query = queryParts.join(" ").trim();
if (!query) usage("Missing <query>");
if (!mode) usage("Must specify --web or --x");

const apiKey = readKeyFromClawdbotConfig();
if (!apiKey) {
  console.error(
    "Missing CUSTOM_GROK_APIKEY/XAI_API_KEY. Set env var or add env.XAI_API_KEY in ~/.clawdbot/clawdbot.json"
  );
  process.exit(1);
}

const toolType = mode === "x" ? "x_search" : "web_search";

function isoDate(d) {
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function computeDateRange() {
  if (fromDate || toDate) {
    return {
      from_date: fromDate || undefined,
      to_date: toDate || undefined,
    };
  }
  if (days) {
    const to = new Date();
    const from = new Date();
    from.setDate(from.getDate() - days);
    return { from_date: isoDate(from), to_date: isoDate(to) };
  }
  return {};
}

const dateRange = computeDateRange();
const tools =
  mode === "x"
    ? [
        {
          type: "x_search",
          x_search: {
            ...(dateRange.from_date ? { from_date: dateRange.from_date } : {}),
            ...(dateRange.to_date ? { to_date: dateRange.to_date } : {}),
            ...(handles.length ? { allowed_x_handles: handles } : {}),
            ...(excludeHandles.length ? { excluded_x_handles: excludeHandles } : {}),
          },
        },
      ]
    : [{ type: "web_search" }];

const prompt = `Use the provided ${toolType} tool to research: ${JSON.stringify(
  query
)}

Return ONLY valid JSON (no markdown) in this schema:
{
  "query": string,
  "mode": "${mode}",
  "results": [
    {
      "title": string|null,
      "url": string|null,
      "snippet": string|null,
      "author": string|null,
      "posted_at": string|null
    }
  ],
  "citations": [string]
}

Rules:
- results length <= ${maxResults}
- citations must be unique URLs
- for mode="x":
  - urls should be x.com links to the posts whenever possible
  - title can be "@handle" and snippet should contain the tweet text
  - posted_at should be ISO date/time if you can infer it, else null
- if you cannot find anything, return empty arrays (still valid JSON).`;

const body = {
  model,
  input: [
    {
      role: "user",
      content: [{ type: "input_text", text: prompt }],
    },
  ],
  tools,
  store: false,
  temperature: 0,
};

const res = await fetch(`${runtime.baseUrl}/responses`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${apiKey}`,
    ...(runtime.userAgent ? { "User-Agent": runtime.userAgent } : {}),
  },
  body: JSON.stringify(body),
});

if (!res.ok) {
  const t = await res.text().catch(() => "");
  console.error(`xAI-compatible API error: ${res.status} ${res.statusText}`);
  console.error(t.slice(0, 4000));
  process.exit(1);
}

const data = await res.json();
const text =
  data.output_text ||
  data?.output
    ?.flatMap((o) => (Array.isArray(o?.content) ? o.content : []))
    ?.find((c) => c?.type === "output_text" && typeof c?.text === "string")
    ?.text ||
  null;

if (!text) {
  if (jsonOut) {
    console.log(JSON.stringify({ query, mode, raw: data }, null, 2));
  } else {
    console.log(JSON.stringify(data, null, 2));
  }
  process.exit(0);
}

function dedupeXCitations(urls) {
  function tweetInfo(u) {
    const m1 = u.match(/https?:\/\/(?:x\.com|twitter\.com)\/[^\/]+\/status\/(\d+)/i);
    if (m1) return { id: m1[1], kind: "status" };
    const m2 = u.match(/https?:\/\/(?:x\.com|twitter\.com)\/i\/status\/(\d+)/i);
    if (m2) return { id: m2[1], kind: "i" };
    return null;
  }

  const best = new Map();
  for (const u of urls) {
    const info = tweetInfo(u);
    if (!info) continue;
    const cur = best.get(info.id);
    if (!cur) best.set(info.id, { url: u, kind: info.kind });
    else if (cur.kind === "i" && info.kind === "status") best.set(info.id, { url: u, kind: info.kind });
  }

  const out = [];
  const seen = new Set();
  for (const u of urls) {
    const info = tweetInfo(u);
    if (info) {
      const b = best.get(info.id);
      if (b?.url === u && !seen.has(b.url)) {
        out.push(u);
        seen.add(b.url);
      }
      continue;
    }

    if (!seen.has(u)) {
      out.push(u);
      seen.add(u);
    }
  }

  return out;
}

function collectCitations(resp) {
  const out = new Set();

  if (Array.isArray(resp?.citations)) {
    for (const u of resp.citations) {
      if (typeof u === "string" && u) out.add(u);
    }
  }

  if (Array.isArray(resp?.output)) {
    for (const item of resp.output) {
      if (!item) continue;
      const content = Array.isArray(item.content) ? item.content : [];
      for (const c of content) {
        const ann = Array.isArray(c?.annotations) ? c.annotations : [];
        for (const a of ann) {
          const url = a?.url || a?.web_citation?.url;
          if (typeof url === "string" && url) out.add(url);
        }
      }
    }
  }

  if (mode === "x") {
    const xLinks = [...out].filter((u) => /https?:\/\/(x\.com|twitter\.com)\//i.test(u));
    if (xLinks.length) return dedupeXCitations(xLinks);
  }

  return [...out];
}

function normalizeParsed(parsedObj) {
  const resultsRaw = Array.isArray(parsedObj?.results) ? parsedObj.results : [];
  const results = resultsRaw.slice(0, maxResults).map((r) => {
    const obj = r && typeof r === "object" ? r : {};
    return {
      title: obj.title ?? null,
      url: obj.url ?? null,
      snippet: obj.snippet ?? null,
      author: obj.author ?? null,
      posted_at: obj.posted_at ?? null,
    };
  });

  const citationsRaw = Array.isArray(parsedObj?.citations) ? parsedObj.citations : [];
  const citationsFromResp = collectCitations(data);
  let citationsMerged = [...new Set([...citationsRaw, ...citationsFromResp].filter(Boolean))];

  const resultUrls = results.map((r) => r?.url).filter((u) => typeof u === "string" && u);

  if (mode === "x") citationsMerged = dedupeXCitations(citationsMerged);

  const citations = [];
  const seen = new Set();
  for (const u of resultUrls) {
    if (!seen.has(u)) {
      citations.push(u);
      seen.add(u);
    }
  }
  for (const u of citationsMerged) {
    if (!seen.has(u)) {
      citations.push(u);
      seen.add(u);
    }
  }

  const cap = Math.max(12, maxResults * 3);
  const capped = citations.slice(0, cap);

  return {
    query: parsedObj?.query ?? query,
    mode: parsedObj?.mode ?? mode,
    results,
    citations: capped,
  };
}

let parsed;
try {
  parsed = JSON.parse(text);
} catch {
  parsed = null;
}

if (jsonOut) {
  if (parsed) {
    console.log(JSON.stringify(normalizeParsed(parsed), null, 2));
  } else {
    console.log(text.trim());
  }
  if (rawOut) {
    console.error("\n--- RAW RESPONSE (debug) ---\n");
    console.error(JSON.stringify(data, null, 2));
  }
  process.exit(0);
}

if (!parsed) {
  console.log(text.trim());
  if (rawOut) console.error(JSON.stringify(data, null, 2));
  process.exit(0);
}

const normalized = normalizeParsed(parsed);
const citations = normalized.citations;
const results = normalized.results;

if (format === "links") {
  for (const c of citations) console.log(c);
  process.exit(0);
}

const lines = [];
lines.push(`Query: ${normalized.query}`);
lines.push(`Mode: ${normalized.mode}`);
lines.push("");

if (results.length) {
  lines.push("Results:");
  for (const r of results) {
    const title = r?.title || (r?.author ? String(r.author) : "(no title)");
    const url = r?.url || "";
    const snip = r?.snippet || "";
    const when = r?.posted_at ? `\n  ${r.posted_at}` : "";
    lines.push(`- ${title}${when}${url ? `\n  ${url}` : ""}${snip ? `\n  ${snip}` : ""}`);
  }
} else {
  lines.push("Results: (none)");
}

if (format !== "text" && citations.length) {
  lines.push("");
  lines.push("Citations:");
  for (const c of citations) lines.push(`- ${c}`);
}

console.log(lines.join("\n"));
if (rawOut) {
  console.error("\n--- RAW RESPONSE (debug) ---\n");
  console.error(JSON.stringify(data, null, 2));
}
