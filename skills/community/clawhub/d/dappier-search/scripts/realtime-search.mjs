#!/usr/bin/env node

function usage() {
  console.error(`Usage: realtime-search.mjs "query"`);
  console.error(`Example: realtime-search.mjs "latest news today"`);
  console.error(`Example: realtime-search.mjs "weather in New York"`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const query = args[0];

const apiKey = (process.env.DAPPIER_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing DAPPIER_API_KEY");
  process.exit(1);
}

const resp = await fetch(
  "https://api.dappier.com/app/aimodel/am_01j06ytn18ejftedz6dyhz2b15",
  {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  }
);

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  throw new Error(`Dappier Real Time Search failed (${resp.status}): ${text}`);
}

const data = await resp.json();

const message = String(data?.message ?? "").trim();

if (message) {
  console.log("## Real Time Search Results\n");
  console.log(message);
  console.log();
} else {
  console.log("No results returned for this query.");
}
