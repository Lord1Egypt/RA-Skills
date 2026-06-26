#!/usr/bin/env node

/**
 * agent-briefing: transcript.js
 * Pull the full transcript of any Not For Humans episode.
 * Fetches from notforhumans.tv — no API key, no credits, no signup.
 *
 * Usage:
 *   node transcript.js latest              # Get latest episode transcript
 *   node transcript.js 007                 # Get episode #007 by number
 *   node transcript.js latest --json       # Output raw JSON
 */

const https = require("https");

const SITE_HOST = "notforhumans.tv";

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { target: null, json: false };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--json") opts.json = true;
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
      res.on("end", () => {
        resolve({ status: res.statusCode, data });
      });
    };

    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method: "GET",
      headers: { "Accept": "text/markdown, application/json, text/plain" },
    };

    const req = https.request(options, handler);
    req.on("error", reject);
    req.end();
  });
}

/**
 * Determine if a target string is an episode number (e.g., "007", "7", "42").
 */
function isEpisodeNumber(target) {
  return /^\d{1,4}$/.test(target);
}

/**
 * Fetch transcript from notforhumans.tv by episode number.
 */
async function fetchFromWebsite(epNumber) {
  const padded = epNumber.padStart(3, "0");
  const url = `https://${SITE_HOST}/episodes/${padded}.md`;

  try {
    const result = await httpGet(url);
    if (result.status === 200 && result.data.length > 50) {
      return {
        source: "notforhumans.tv",
        episode: padded,
        url,
        transcript: result.data,
        credits: 0,
      };
    }
    return null;
  } catch {
    return null;
  }
}

/**
 * Fetch the latest episode transcript from notforhumans.tv.
 */
async function fetchLatestFromWebsite() {
  const url = `https://${SITE_HOST}/episodes/latest.md`;

  try {
    const result = await httpGet(url);
    if (result.status === 200 && result.data.length > 50) {
      return {
        source: "notforhumans.tv",
        episode: "latest",
        url,
        transcript: result.data,
        credits: 0,
      };
    }
    return null;
  } catch {
    return null;
  }
}

/**
 * Fetch episode index to find the highest episode number.
 */
async function getLatestEpisodeNumber() {
  try {
    const result = await httpGet(`https://${SITE_HOST}/episodes/index.json`);
    if (result.status === 200) {
      const data = JSON.parse(result.data);
      const episodes = Array.isArray(data) ? data : data.episodes || data.items || [];
      if (episodes.length === 0) return null;

      // Find highest episode number
      let maxNum = 0;
      for (const ep of episodes) {
        const num = parseInt(String(ep.episode).replace(/\D/g, ""), 10) || 0;
        if (num > maxNum) maxNum = num;
      }
      return maxNum > 0 ? String(maxNum) : null;
    }
  } catch { /* fall through */ }
  return null;
}

async function main() {
  const opts = parseArgs();

  if (!opts.target) {
    console.error("Usage: node transcript.js <EPISODE_NUMBER|latest> [--json]");
    process.exit(1);
  }

  try {
    let result = null;

    if (opts.target.toLowerCase() === "latest") {
      // Try /episodes/latest.md first
      result = await fetchLatestFromWebsite();

      // Fallback: get the highest episode number from index, then fetch that
      if (!result) {
        const epNum = await getLatestEpisodeNumber();
        if (epNum) {
          result = await fetchFromWebsite(epNum);
        }
      }
    } else if (isEpisodeNumber(opts.target)) {
      result = await fetchFromWebsite(opts.target);
    } else {
      console.error(`"${opts.target}" doesn't look like an episode number.`);
      console.error("Usage: node transcript.js <EPISODE_NUMBER|latest> [--json]");
      process.exit(1);
    }

    if (!result) {
      console.error("Could not retrieve transcript.");
      console.error("The episode may not be available on notforhumans.tv yet.");
      process.exit(1);
    }

    if (opts.json) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.log(`\n📡 Not For Humans — Transcript`);
      console.log(`   Source: ${result.source}`);
      if (result.episode) console.log(`   Episode: #${result.episode}`);
      if (result.url) console.log(`   URL: ${result.url}`);
      console.log(`   Credits used: ${result.credits}`);
      console.log(`\n--- TRANSCRIPT ---\n`);
      console.log(result.transcript);
      console.log(`\n--- END TRANSCRIPT ---`);
    }
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

main();
