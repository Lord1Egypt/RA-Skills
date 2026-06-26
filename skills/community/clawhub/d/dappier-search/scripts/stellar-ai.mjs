#!/usr/bin/env node

function usage() {
  console.error(`Usage: stellar-ai.mjs "residential home address"`);
  console.error(`Example: stellar-ai.mjs "1600 Amphitheatre Parkway, Mountain View, CA"`);
  console.error(`Example: stellar-ai.mjs "221B Baker Street, London"`);
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
  "https://api.dappier.com/app/aimodel/am_01hw6kehn6f0rthxsvc33s7mad",
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
  throw new Error(`Dappier Stellar AI failed (${resp.status}): ${text}`);
}

const data = await resp.json();
const message = String(data?.message ?? "").trim();

if (message) {
  console.log("## Stellar AI (Solar & Roof Analysis)\n");
  console.log(message);
  console.log();
} else {
  console.log("No results returned for this address.");
}

