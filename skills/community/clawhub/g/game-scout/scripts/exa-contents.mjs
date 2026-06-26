#!/usr/bin/env node

function usage() {
  console.error(`Usage: exa-contents.mjs <url> [<url2> ...] [--summary "question"]`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const urls = [];
let summaryQuery = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--summary") {
    summaryQuery = args[++i];
    continue;
  }
  urls.push(args[i]);
}

if (urls.length === 0) usage();

const apiKey = (process.env.EXA_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing EXA_API_KEY");
  process.exit(1);
}

const body = {
  urls,
  text: { maxCharacters: 12000, verbosity: "standard" },
  highlights: { maxCharacters: 4000 },
};

if (summaryQuery) {
  body.summary = { query: summaryQuery };
}

const resp = await fetch("https://api.exa.ai/contents", {
  method: "POST",
  headers: { "Content-Type": "application/json", "x-api-key": apiKey },
  body: JSON.stringify(body),
});

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  console.error(`Exa contents failed (${resp.status}): ${text}`);
  process.exit(1);
}

const data = await resp.json();
const results = data.results ?? [];

for (const r of results) {
  console.log(`## ${r.title ?? "(no title)"}`);
  console.log(`**URL**: ${r.url ?? ""}`);

  if (r.summary) {
    console.log(`\n**Summary**: ${r.summary}`);
  }

  if (r.highlights && r.highlights.length) {
    console.log(`\n**Highlights**:`);
    for (const h of r.highlights) {
      console.log(`- ${h.slice(0, 500)}`);
    }
  }

  if (r.text) {
    console.log(`\n### Content\n`);
    console.log(r.text);
  }

  console.log("\n---\n");
}
