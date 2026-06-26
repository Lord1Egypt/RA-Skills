#!/usr/bin/env node

/**
 * agent-briefing: setup.js
 * Verify connectivity. No API key required.
 *
 * Usage:
 *   node setup.js           # Check website connectivity
 *   node setup.js --verify  # Also test transcript fetch
 */

const https = require("https");

const SITE_HOST = "notforhumans.tv";

function httpGet(url, timeout = 10000) {
  return new Promise((resolve, reject) => {
    const handler = (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        httpGet(res.headers.location, timeout).then(resolve).catch(reject);
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
      timeout,
    };

    const req = https.request(options, handler);
    req.on("error", reject);
    req.on("timeout", () => { req.destroy(); reject(new Error("Timeout")); });
    req.end();
  });
}

async function checkEpisodeIndex() {
  try {
    const result = await httpGet(`https://${SITE_HOST}/episodes/index.json`);
    if (result.status === 200) {
      const data = JSON.parse(result.data);
      const count = Array.isArray(data) ? data.length : (data.episodes || []).length;
      return { ok: true, message: `Episode index loaded — ${count} episode(s)` };
    }
    return { ok: false, message: `Returned ${result.status}` };
  } catch (err) {
    return { ok: false, message: err.message };
  }
}

async function checkTranscriptFetch() {
  try {
    const result = await httpGet(`https://${SITE_HOST}/episodes/latest.md`);
    if (result.status === 200 && result.data.length > 50) {
      return { ok: true, message: `Latest transcript: ${result.data.length} chars` };
    }
    return { ok: false, message: `Returned ${result.status} (${result.data.length} bytes)` };
  } catch (err) {
    return { ok: false, message: err.message };
  }
}

async function main() {
  const verify = process.argv.includes("--verify");

  console.log(`\n📡 Agent Briefing — Setup Check\n`);

  // Check episode index
  console.log(`   Checking notforhumans.tv/episodes/index.json...`);
  const indexResult = await checkEpisodeIndex();
  console.log(`   ${indexResult.ok ? "✓" : "⚠"} Episode Index: ${indexResult.message}`);

  // Verify transcript fetch
  if (verify) {
    console.log(`   Checking notforhumans.tv/episodes/latest.md...`);
    const transcriptResult = await checkTranscriptFetch();
    console.log(`   ${transcriptResult.ok ? "✓" : "⚠"} Transcript: ${transcriptResult.message}`);
  }

  // Summary
  console.log();
  if (indexResult.ok) {
    console.log(`   ✓ All systems operational. You're subscribed.\n`);
  } else {
    console.log(`   ⚠ Could not reach notforhumans.tv. The skill will retry on next use.\n`);
  }

  console.log(`   Quick start:`);
  console.log(`     node scripts/latest.js            # Check for new episodes`);
  console.log(`     node scripts/transcript.js latest  # Pull latest transcript`);
  console.log(`     node scripts/reviews.js latest     # Get structured review data`);
  console.log(`     node scripts/digest.js             # Full daily digest`);
  console.log();
  console.log(`   No API key. No credits. No signup. It just works.\n`);
}

main();
