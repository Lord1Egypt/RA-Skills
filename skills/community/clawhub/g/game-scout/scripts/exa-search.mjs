#!/usr/bin/env node

function usage() {
  console.error(
    `Usage: exa-search.mjs "query" [-n 10] [--domain example.com] [--exclude bad.com] [--after 2026-01-01] [--category tweet|news] [--contents] [--summary]`
  );
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const query = args[0];
let numResults = 10;
const includeDomains = [];
const excludeDomains = [];
let startDate = null;
let category = null;
let includeContents = false;
let includeSummary = false;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === "-n") { numResults = parseInt(args[++i] || "10", 10); continue; }
  if (a === "--domain") { includeDomains.push(args[++i]); continue; }
  if (a === "--exclude") { excludeDomains.push(args[++i]); continue; }
  if (a === "--after") { startDate = args[++i]; continue; }
  if (a === "--category") { category = args[++i]; continue; }
  if (a === "--contents") { includeContents = true; continue; }
  if (a === "--summary") { includeSummary = true; continue; }
  console.error(`Unknown arg: ${a}`);
  usage();
}

const apiKey = (process.env.EXA_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing EXA_API_KEY");
  process.exit(1);
}

const body = {
  query,
  type: "auto",
  numResults: Math.max(1, Math.min(numResults, 100)),
};

if (includeDomains.length) body.includeDomains = includeDomains;
if (excludeDomains.length) body.excludeDomains = excludeDomains;
if (startDate) body.startPublishedDate = `${startDate}T00:00:00.000Z`;
if (category) body.category = category;

if (includeContents || includeSummary) {
  body.contents = {};
  if (includeContents) body.contents.text = { maxCharacters: 8000, verbosity: "compact" };
  if (includeSummary) body.contents.summary = { query };
}

const resp = await fetch("https://api.exa.ai/search", {
  method: "POST",
  headers: { "Content-Type": "application/json", "x-api-key": apiKey },
  body: JSON.stringify(body),
});

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  console.error(`Exa search failed (${resp.status}): ${text}`);
  process.exit(1);
}

const data = await resp.json();
const results = data.results ?? [];

console.log(`## Exa Search Results (${results.length})\n`);

for (const r of results) {
  const title = r.title ?? "(no title)";
  const url = r.url ?? "";
  const date = r.publishedDate ? r.publishedDate.slice(0, 10) : "unknown date";
  const author = r.author ? ` by ${r.author}` : "";

  console.log(`### ${title}`);
  console.log(`- **URL**: ${url}`);
  console.log(`- **Date**: ${date}${author}`);

  if (r.summary) {
    console.log(`- **Summary**: ${r.summary}`);
  }

  if (r.highlights && r.highlights.length) {
    console.log(`- **Highlights**:`);
    for (const h of r.highlights) {
      console.log(`  - ${h.slice(0, 500)}`);
    }
  }

  if (r.text) {
    console.log(`\n<details><summary>Content</summary>\n`);
    console.log(r.text.slice(0, 8000));
    console.log(`\n</details>`);
  }

  console.log();
}
