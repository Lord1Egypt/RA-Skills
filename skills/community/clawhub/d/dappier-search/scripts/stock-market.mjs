#!/usr/bin/env node

function usage() {
  console.error(`Usage: stock-market.mjs "query with ticker symbol"`);
  console.error(`Query MUST include a stock ticker symbol (e.g. AAPL, TSLA, MSFT).`);
  console.error(`Example: stock-market.mjs "AAPL stock price today"`);
  console.error(`Example: stock-market.mjs "TSLA latest financial news"`);
  console.error(`Example: stock-market.mjs "MSFT earnings report"`);
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
  "https://api.dappier.com/app/aimodel/am_01j0rzq4tvfscrgzwac7jv1p4h",
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
  throw new Error(`Dappier Stock Market failed (${resp.status}): ${text}`);
}

const data = await resp.json();

const message = String(data?.message ?? "").trim();

if (message) {
  console.log("## Stock Market Data\n");
  console.log(message);
  console.log();
} else {
  console.log("No results returned for this query.");
}
