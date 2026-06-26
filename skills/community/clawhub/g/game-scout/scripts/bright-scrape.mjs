#!/usr/bin/env node

function usage() {
  console.error(`Usage: bright-scrape.mjs <url> [<url2> ...] [--country us]`);
  console.error(`Scrapes URLs to markdown using Bright Data Web Unlocker.`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const urls = [];
let country = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--country") { country = args[++i]; continue; }
  urls.push(args[i]);
}

if (urls.length === 0) usage();

const apiKey = (process.env.BRIGHTDATA_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing BRIGHTDATA_API_KEY");
  process.exit(1);
}

const zone = (process.env.BRIGHTDATA_ZONE ?? "").trim();
if (!zone) {
  console.error("Missing BRIGHTDATA_ZONE (create a Web Unlocker zone in your Bright Data dashboard)");
  process.exit(1);
}

async function scrapeUrl(url) {
  const body = {
    zone,
    url,
    format: "raw",
    data_format: "markdown",
  };
  if (country) body.country = country;

  const resp = await fetch("https://api.brightdata.com/request", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify(body),
  });

  const text = await resp.text().catch(() => "");

  if (!resp.ok) {
    return { url, error: `HTTP ${resp.status}: ${text.slice(0, 200)}` };
  }

  // Try parsing as JSON — Web Unlocker may return {body: "markdown"}
  try {
    const data = JSON.parse(text);
    if (data.body) return { url, content: data.body };
    return { url, content: JSON.stringify(data, null, 2) };
  } catch {
    // Response is plain text/markdown directly
    return { url, content: text };
  }
}

const results = await Promise.all(urls.map(scrapeUrl));

for (const r of results) {
  console.log(`## Source: ${r.url}\n`);
  if (r.error) {
    console.log(`**Error**: ${r.error}\n`);
  } else {
    console.log(r.content);
  }
  console.log("\n---\n");
}
