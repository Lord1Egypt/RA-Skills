#!/usr/bin/env node

function usage() {
  console.error(`Usage: bright-twitter.mjs <url> [<url2> ...] [--timeout 30]`);
  console.error(`\nExamples:`);
  console.error(`  bright-twitter.mjs "https://x.com/user/status/123456"`);
  console.error(`  bright-twitter.mjs "https://x.com/u1/status/111" "https://x.com/u2/status/222"`);
  console.error(`  bright-twitter.mjs "https://x.com/user/status/123456" --timeout 60`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const urls = [];
let timeoutSec = 30;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--timeout") { timeoutSec = parseInt(args[++i] || "30", 10); continue; }
  urls.push(args[i]);
}

if (urls.length === 0) usage();

const apiKey = (process.env.BRIGHTDATA_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing BRIGHTDATA_API_KEY");
  process.exit(1);
}

const datasetId = "gd_lwxkxvnf1cynvib9co"; // X Posts - collect by URL
const headers = {
  "Content-Type": "application/json",
  Authorization: `Bearer ${apiKey}`,
};

// Step 1: Trigger async collection
const triggerResp = await fetch(
  `https://api.brightdata.com/datasets/v3/trigger?dataset_id=${datasetId}&notify=false&include_errors=true`,
  {
    method: "POST",
    headers,
    body: JSON.stringify({ input: urls.map((url) => ({ url })) }),
  }
);

if (!triggerResp.ok) {
  const text = await triggerResp.text().catch(() => "");
  console.error(`Trigger failed (${triggerResp.status}): ${text.slice(0, 300)}`);
  process.exit(1);
}

const { snapshot_id } = await triggerResp.json();
if (!snapshot_id) {
  console.error("No snapshot_id returned");
  process.exit(1);
}

// Step 2: Poll until ready
const deadline = Date.now() + timeoutSec * 1000;
let status = "running";

while (Date.now() < deadline) {
  const logResp = await fetch(
    `https://api.brightdata.com/datasets/v3/log/${snapshot_id}`,
    { headers: { Authorization: `Bearer ${apiKey}` } }
  );
  if (logResp.ok) {
    const log = await logResp.json();
    status = log.status;
    if (status === "ready") break;
    if (status === "failed") {
      console.error("Scrape failed.");
      process.exit(1);
    }
  }
  await new Promise((r) => setTimeout(r, 2000));
}

if (status !== "ready") {
  console.error(`Timed out after ${timeoutSec}s. Snapshot: ${snapshot_id}`);
  console.error(`Check later: curl -H "Authorization: Bearer $BRIGHTDATA_API_KEY" "https://api.brightdata.com/datasets/v3/snapshot/${snapshot_id}?format=json"`);
  process.exit(1);
}

// Step 3: Fetch results
const dataResp = await fetch(
  `https://api.brightdata.com/datasets/v3/snapshot/${snapshot_id}?format=json`,
  { headers: { Authorization: `Bearer ${apiKey}` } }
);

if (!dataResp.ok) {
  const text = await dataResp.text().catch(() => "");
  console.error(`Failed to fetch results (${dataResp.status}): ${text.slice(0, 300)}`);
  process.exit(1);
}

const posts = await dataResp.json();

if (!Array.isArray(posts) || posts.length === 0) {
  console.log("No posts found (tweets may be deleted or accounts private).");
  process.exit(0);
}

console.log(`## Twitter/X Posts (${posts.length})\n`);

for (const p of posts) {
  const user = p.user_posted ?? p.name ?? "unknown";
  const date = p.date_posted ? new Date(p.date_posted).toISOString().slice(0, 10) : "unknown";
  const text = p.description ?? "(no text)";
  const likes = p.likes ?? 0;
  const reposts = p.reposts ?? 0;
  const replies = p.replies ?? 0;
  const views = p.views ?? 0;
  const verified = p.is_verified ? " [verified]" : "";

  console.log(`### @${user}${verified} — ${date}`);
  console.log(text);
  console.log(`\n> Likes: ${likes} | Reposts: ${reposts} | Replies: ${replies} | Views: ${views}`);

  if (p.hashtags && p.hashtags.length) {
    console.log(`> Tags: ${p.hashtags.join(", ")}`);
  }
  if (p.external_url) {
    console.log(`> Link: ${p.external_url}`);
  }
  if (p.url) {
    console.log(`> Tweet: ${p.url}`);
  }
  console.log();
}
