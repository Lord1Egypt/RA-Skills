#!/usr/bin/env node

function usage() {
  console.error(`Usage: exa-similar.mjs <url> [-n 10] [--domain example.com] [--after 2026-01-01] [--contents]`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const url = args[0];
let numResults = 10;
const includeDomains = [];
let startDate = null;
let includeContents = false;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === "-n") { numResults = parseInt(args[++i] || "10", 10); continue; }
  if (a === "--domain") { includeDomains.push(args[++i]); continue; }
  if (a === "--after") { startDate = args[++i]; continue; }
  if (a === "--contents") { includeContents = true; continue; }
  console.error(`Unknown arg: ${a}`);
  usage();
}

const apiKey = (process.env.EXA_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing EXA_API_KEY");
  process.exit(1);
}

const body = { url, numResults: Math.max(1, Math.min(numResults, 100)) };
if (includeDomains.length) body.includeDomains = includeDomains;
if (startDate) body.startPublishedDate = `${startDate}T00:00:00.000Z`;
if (includeContents) body.contents = { text: { maxCharacters: 5000, verbosity: "compact" } };

const resp = await fetch("https://api.exa.ai/findSimilar", {
  method: "POST",
  headers: { "Content-Type": "application/json", "x-api-key": apiKey },
  body: JSON.stringify(body),
});

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  console.error(`Exa findSimilar failed (${resp.status}): ${text}`);
  process.exit(1);
}

const data = await resp.json();
const results = data.results ?? [];

console.log(`## Similar to: ${url}\n`);
console.log(`Found ${results.length} similar pages:\n`);

for (const r of results) {
  const title = r.title ?? "(no title)";
  const date = r.publishedDate ? r.publishedDate.slice(0, 10) : "";
  console.log(`- **${title}** ${date ? `(${date})` : ""}`);
  console.log(`  ${r.url}`);
  if (r.text) {
    console.log(`  ${r.text.slice(0, 300)}...`);
  }
  console.log();
}
