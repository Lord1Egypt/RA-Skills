#!/usr/bin/env node

function usage() {
  console.error(
    `Usage: lifestyle-news.mjs "query" [--top_k 9] [--algorithm most_recent|semantic|most_recent_semantic|trending]`
  );
  console.error(`Example: lifestyle-news.mjs "wellness trends 2026"`);
  console.error(`Example: lifestyle-news.mjs "family routine hacks" --algorithm trending`);
  console.error(`Example: lifestyle-news.mjs "celebrity lifestyle news" --top_k 5`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const query = args[0];
let similarityTopK = 9;
let searchAlgorithm = "most_recent";

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === "--top_k") {
    similarityTopK = Number.parseInt(args[i + 1] ?? "9", 10);
    i++;
    continue;
  }
  if (a === "--algorithm") {
    searchAlgorithm = args[i + 1] ?? "most_recent";
    i++;
    continue;
  }
  console.error(`Unknown arg: ${a}`);
  usage();
}

const apiKey = (process.env.DAPPIER_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing DAPPIER_API_KEY");
  process.exit(1);
}

// Lifestyle News recommendations data model
const dataModelId = "dm_01j0q82s4bfjmsqkhs3ywm3x6y";

const resp = await fetch(
  `https://api.dappier.com/app/v2/search?data_model_id=${dataModelId}`,
  {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      similarity_top_k: similarityTopK,
      ref: "",
      num_articles_ref: 0,
      search_algorithm: searchAlgorithm,
    }),
  }
);

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  throw new Error(`Dappier Lifestyle News failed (${resp.status}): ${text}`);
}

const data = await resp.json();
const items = data?.response?.results ?? [];

if (items.length === 0) {
  console.log("No lifestyle news found for this query.");
  process.exit(0);
}

console.log("## Lifestyle News\n");

for (let i = 0; i < items.length; i++) {
  const item = items[i];
  const title = item.title || "No title";
  const author = item.author || "Unknown author";
  const pubdate = item.pubdate || "No date";
  const site = item.site || "Unknown source";
  const siteDomain = item.site_domain || "";
  const sourceUrl = item.source_url || "";
  const imageUrl = item.image_url || "";
  const summary = item.summary || "No summary available";
  const score = item.score != null ? item.score : "";

  console.log(`### ${i + 1}. ${title}\n`);
  console.log(`- **Author:** ${author}`);
  console.log(`- **Published:** ${pubdate}`);
  console.log(`- **Source:** ${site}${siteDomain ? ` (${siteDomain})` : ""}`);
  if (sourceUrl) console.log(`- **URL:** ${sourceUrl}`);
  if (imageUrl) console.log(`- **Image:** ${imageUrl}`);
  if (score) console.log(`- **Relevance:** ${score}`);
  console.log(`\n${summary}\n`);
}

