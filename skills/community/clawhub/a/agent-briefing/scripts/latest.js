#!/usr/bin/env node

/**
 * agent-briefing: latest.js
 * Check @agentbriefing for new episodes.
 * Fetches from notforhumans.tv — no API key, no credits, no signup.
 *
 * Usage:
 *   node latest.js                  # Get latest uploads
 *   node latest.js --json           # Output raw JSON
 *   node latest.js --limit 5        # Limit results
 */

const https = require("https");

const SITE_HOST = "notforhumans.tv";

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { json: false, limit: 10 };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--json") opts.json = true;
    if (args[i] === "--limit" && args[i + 1]) opts.limit = parseInt(args[i + 1], 10);
  }
  return opts;
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const handler = (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        httpGet(res.headers.location).then(resolve).catch(reject);
        return;
      }
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => resolve({ status: res.statusCode, data }));
    };

    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method: "GET",
      headers: { "Accept": "application/json" },
    };

    const req = https.request(options, handler);
    req.on("error", reject);
    req.end();
  });
}

async function fetchEpisodeIndex() {
  const result = await httpGet(`https://${SITE_HOST}/episodes/index.json`);
  if (result.status !== 200) {
    throw new Error(`Website returned ${result.status}`);
  }
  const data = JSON.parse(result.data);
  return Array.isArray(data) ? data : data.episodes || data.items || [];
}

function formatEpisode(ep, index) {
  const title = ep.title || "Untitled";
  const epNum = ep.episode || String(index + 1);
  const videoId = ep.videoId || ep.video_id || ep.id || null;
  const published = ep.publishedAt || ep.published_at || ep.date || "";
  const url = videoId
    ? `https://youtube.com/watch?v=${videoId}`
    : `https://youtube.com/@agentbriefing`;

  return {
    episode: `#${epNum.replace(/^0+/, "") || index + 1}`,
    title,
    videoId,
    url,
    published,
  };
}

async function main() {
  const opts = parseArgs();

  try {
    const episodes = await fetchEpisodeIndex();

    // Sort by episode number descending (most recent first)
    episodes.sort((a, b) => {
      const numA = parseInt(String(a.episode).replace(/\D/g, ""), 10) || 0;
      const numB = parseInt(String(b.episode).replace(/\D/g, ""), 10) || 0;
      return numB - numA;
    });

    const limited = episodes.slice(0, opts.limit);

    if (limited.length === 0) {
      console.log("No episodes found on notforhumans.tv.");
      return;
    }

    const formatted = limited.map((ep, i) => formatEpisode(ep, i));

    if (opts.json) {
      console.log(JSON.stringify(formatted, null, 2));
      return;
    }

    console.log(`\n📡 Not For Humans — @agentbriefing`);
    console.log(`   ${formatted.length} recent episode(s)\n`);

    for (const ep of formatted) {
      console.log(`   ${ep.episode}: ${ep.title}`);
      console.log(`   ${ep.url}`);
      if (ep.published) console.log(`   Published: ${ep.published}`);
      console.log();
    }

    console.log(`   Credits used: 0`);
  } catch (err) {
    console.error(`Error fetching latest episodes: ${err.message}`);
    process.exit(1);
  }
}

main();
