#!/usr/bin/env node

function usage() {
  console.error(`Usage: research-papers.mjs "query"`);
  console.error(`Example: research-papers.mjs "attention is all you need paper summary"`);
  console.error(`Example: research-papers.mjs "recent arXiv papers on diffusion models"`);
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
  "https://api.dappier.com/app/aimodel/am_01j0rzq4tvfscrgzwac7jv6dr2",
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
  throw new Error(`Dappier Research Papers Search failed (${resp.status}): ${text}`);
}

const data = await resp.json();
const message = String(data?.message ?? "").trim();

if (message) {
  console.log("## Research Papers Search\n");
  console.log(message);
  console.log();
} else {
  console.log("No results returned for this query.");
}

