#!/usr/bin/env node

function usage() {
  console.error(`Usage: search.mjs "query" [options]

Options:
  --time-range <range>    Time range: OneDay, OneWeek, OneMonth, OneYear, NoLimit (default: NoLimit)
  --category <category>   Category: finance, law, medical, internet, tax, news_province, news_center
  --json                  Output raw JSON

Examples:
  search.mjs "云栖大会"
  search.mjs "AI人工智能" --time-range OneWeek
  search.mjs "股票市场" --category finance
  search.mjs "科技新闻" --time-range OneDay --category news`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const query = args[0];
let timeRange = "NoLimit";
let category = null;
let outputJson = false;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === "--time-range") {
    timeRange = args[i + 1] ?? "NoLimit";
    i++;
    continue;
  }
  if (a === "--category") {
    category = args[i + 1] ?? null;
    i++;
    continue;
  }
  if (a === "--json") {
    outputJson = true;
    continue;
  }
  console.error(`Unknown arg: ${a}`);
  usage();
}

const apiKey = (process.env.ALIYUN_IQS_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Error: ALIYUN_IQS_API_KEY not set");
  console.error("Get your API key at https://help.aliyun.com/zh/document_detail/2872258.html");
  process.exit(1);
}

const body = {
  query: query,
  engineType: "Generic",
  timeRange: timeRange,
  contents: {
    mainText: false,
    markdownText: false,
    summary: false,
    rerankScore: true
  }
};

if (category) {
  body.category = category;
}

const resp = await fetch("https://cloud-iqs.aliyuncs.com/search/unified", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${apiKey}`,
  },
  body: JSON.stringify(body),
});

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  throw new Error(`Aliyun Unified Search failed (${resp.status}): ${text}`);
}

const data = await resp.json();

if (outputJson) {
  console.log(JSON.stringify(data, null, 2));
  process.exit(0);
}

// Print results
const results = (data.pageItems ?? []);
console.log(`## Search Results (${results.length} results)\n`);

for (const r of results) {
  const title = String(r?.title ?? "").trim();
  const url = String(r?.link ?? "").trim();
  const snippet = String(r?.snippet ?? "").trim();
  const rerankScore = r?.rerankScore ? ` (relevance: ${(r.rerankScore * 100).toFixed(0)}%)` : "";
  const publishedTime = r?.publishedTime ? ` [${r.publishedTime}]` : "";
  const hostname = r?.hostname ? ` - ${r.hostname}` : "";

  if (!title || !url) continue;

  console.log(`- **${title}**${rerankScore}${hostname}`);
  console.log(`  ${url}`);
  if (snippet) {
    console.log(`  ${snippet.slice(0, 300)}${snippet.length > 300 ? "..." : ""}`);
  }
  if (publishedTime) {
    console.log(`  ${publishedTime}`);
  }
  console.log();
}

if (data.searchInformation?.searchTime) {
  console.log(`\nSearch time: ${data.searchInformation.searchTime}ms`);
}

if (data.requestId) {
  console.log(`Request ID: ${data.requestId}`);
}
