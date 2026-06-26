#!/usr/bin/env node

/**
 * agent-briefing: reviews.js
 * Fetch structured review data and search episodes from notforhumans.tv.
 * No API key, no credits, no signup.
 *
 * Usage:
 *   node reviews.js latest                    # Get review data from latest episode
 *   node reviews.js 006                       # Get review data for episode #006
 *   node reviews.js --search "OpenClaw"       # Search episodes by keyword
 *   node reviews.js --search "smart speaker" --json
 */

const https = require("https");

const SITE_HOST = "notforhumans.tv";

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { target: null, search: null, json: false };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--json") opts.json = true;
    else if (args[i] === "--search" && args[i + 1]) opts.search = args[++i];
    else if (!args[i].startsWith("--")) opts.target = args[i];
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
      headers: { "Accept": "application/json, text/plain" },
    };

    const req = https.request(options, handler);
    req.on("error", reject);
    req.end();
  });
}

/**
 * Fetch the master episode index from notforhumans.tv.
 */
async function fetchEpisodeIndex() {
  const result = await httpGet(`https://${SITE_HOST}/episodes/index.json`);
  if (result.status === 200) {
    const data = JSON.parse(result.data);
    return Array.isArray(data) ? data : data.episodes || data.items || [];
  }
  throw new Error(`Website returned ${result.status}`);
}

/**
 * Fetch a specific product review from notforhumans.tv.
 */
async function fetchProductReview(slug) {
  try {
    const result = await httpGet(`https://${SITE_HOST}/reviews/${slug}.json`);
    if (result.status === 200) {
      return JSON.parse(result.data);
    }
    return null;
  } catch {
    return null;
  }
}

function isEpisodeNumber(target) {
  return /^\d{1,4}$/.test(target);
}

/**
 * Search episodes by keyword. Checks title, subject, and segment fields.
 */
function searchIndex(episodes, query) {
  const q = query.toLowerCase();
  return episodes.filter((ep) => {
    const fields = [
      ep.title,
      ep.subject,
      ep.segment,
      ep.episode,
    ].filter(Boolean).map((f) => String(f).toLowerCase());

    return fields.some((f) => f.includes(q));
  });
}

function printEpisode(ep) {
  console.log(`   Briefing #${ep.episode}: ${ep.title || ""}`);
  if (ep.videoId) console.log(`   https://youtube.com/watch?v=${ep.videoId}`);
  if (ep.segment) console.log(`   Segment: ${ep.segment}`);
  if (ep.subject) console.log(`   Subject: ${ep.subject}`);
  if (ep.agent_compatibility_score != null) console.log(`   Agent Compatibility Score: ${ep.agent_compatibility_score}/5`);
  if (ep.respect_index != null) console.log(`   Respect Index: ${ep.respect_index}`);
  if (ep.trust_score) console.log(`   Trust Score: ${ep.trust_score}`);
  console.log();
}

async function main() {
  const opts = parseArgs();

  try {
    const episodes = await fetchEpisodeIndex();

    // --- SEARCH MODE ---
    if (opts.search) {
      const results = searchIndex(episodes, opts.search);

      if (opts.json) {
        console.log(JSON.stringify(results, null, 2));
        return;
      }

      console.log(`\n📡 Not For Humans — Search: "${opts.search}"\n`);

      if (results.length === 0) {
        console.log(`   No matching episodes found.`);
      } else {
        for (const r of results) printEpisode(r);

        for (const r of results) {
          if (r.subject) {
            const slug = r.subject.toLowerCase().replace(/\s+/g, "-");
            const review = await fetchProductReview(slug);
            if (review) {
              console.log(`   ─── Full Review: ${r.subject} ───`);
              console.log(JSON.stringify(review, null, 2));
              console.log();
            }
          }
        }
      }

      console.log(`   Credits used: 0`);
      return;
    }

    // --- SINGLE EPISODE / LATEST ---
    if (!opts.target) {
      console.error("Usage: node reviews.js <EPISODE_NUMBER|latest> [--json]");
      console.error("       node reviews.js --search <query> [--json]");
      process.exit(1);
    }

    let ep = null;

    if (opts.target.toLowerCase() === "latest") {
      // Sort by episode number descending, pick first
      const sorted = [...episodes].sort((a, b) => {
        const numA = parseInt(String(a.episode).replace(/\D/g, ""), 10) || 0;
        const numB = parseInt(String(b.episode).replace(/\D/g, ""), 10) || 0;
        return numB - numA;
      });
      ep = sorted[0] || null;
    } else if (isEpisodeNumber(opts.target)) {
      const padded = opts.target.padStart(3, "0");
      ep = episodes.find((e) => e.episode === padded || e.episode === opts.target);
    }

    if (!ep) {
      console.error("Episode not found.");
      process.exit(1);
    }

    // Try fetching full product review if available
    let fullReview = null;
    if (ep.subject) {
      const slug = ep.subject.toLowerCase().replace(/\s+/g, "-");
      fullReview = await fetchProductReview(slug);
    }

    if (opts.json) {
      console.log(JSON.stringify({ episode: ep, review: fullReview }, null, 2));
      return;
    }

    console.log(`\n📡 Not For Humans — Review Data\n`);
    printEpisode(ep);

    if (fullReview) {
      console.log(`   ─── Full Product Review ───`);
      console.log(JSON.stringify(fullReview, null, 2));
      console.log();
    }

    console.log(`   Credits used: 0`);
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

main();
