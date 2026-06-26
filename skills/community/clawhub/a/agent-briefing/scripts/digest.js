#!/usr/bin/env node

/**
 * agent-briefing: digest.js
 * Daily digest — check for new episodes, fetch transcripts, extract structured data.
 * Zero cost. Zero API keys. Designed for morning schedules.
 * All data from notforhumans.tv.
 *
 * Usage:
 *   node digest.js                  # Check for episodes in last 24h
 *   node digest.js --since 48h      # Custom lookback window
 *   node digest.js --since 7d       # Last 7 days
 *   node digest.js --all            # Process all recent episodes (up to 10)
 *   node digest.js --json           # Output as JSON
 *   node digest.js --no-transcripts # Skip transcript fetches (metadata only)
 */

const https = require("https");

const SITE_HOST = "notforhumans.tv";

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { since: "24h", all: false, json: false, transcripts: true };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--json") opts.json = true;
    else if (args[i] === "--all") opts.all = true;
    else if (args[i] === "--no-transcripts") opts.transcripts = false;
    else if (args[i] === "--since" && args[i + 1]) opts.since = args[++i];
  }

  return opts;
}

function parseSince(since) {
  const match = since.match(/^(\d+)(h|d|w)$/);
  if (!match) return 24 * 60 * 60 * 1000;
  const value = parseInt(match[1], 10);
  const multipliers = { h: 3600000, d: 86400000, w: 604800000 };
  return value * multipliers[match[2]];
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
      headers: { "Accept": "application/json, text/markdown, text/plain" },
    };

    const req = https.request(options, handler);
    req.on("error", reject);
    req.end();
  });
}

/**
 * Fetch episode index from notforhumans.tv.
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
 * Fetch transcript from notforhumans.tv.
 */
async function fetchTranscript(epNumber) {
  const padded = epNumber.padStart(3, "0");
  try {
    const result = await httpGet(`https://${SITE_HOST}/episodes/${padded}.md`);
    if (result.status === 200 && result.data.length > 50) {
      return { text: result.data, source: "notforhumans.tv" };
    }
  } catch { /* fall through */ }
  return null;
}

async function main() {
  const opts = parseArgs();
  const sinceMs = parseSince(opts.since);
  const cutoff = new Date(Date.now() - sinceMs);

  try {
    if (!opts.json) {
      console.log(`\n📡 Not For Humans — Daily Digest`);
      console.log(`   Checking for episodes since ${cutoff.toISOString().split("T")[0]}\n`);
    }

    const episodes = await fetchEpisodeIndex();

    const filtered = opts.all
      ? episodes.slice(0, 10)
      : episodes.filter((v) => {
          const pubDate = v.publishedAt || v.published_at || v.date;
          if (!pubDate) return true;
          return new Date(pubDate) >= cutoff;
        });

    if (filtered.length === 0) {
      const msg = `No new episodes since ${cutoff.toISOString().split("T")[0]}.`;
      if (opts.json) {
        console.log(JSON.stringify({ episodes: [], message: msg, credits_used: 0 }));
      } else {
        console.log(`   ${msg}`);
        console.log(`   Channel is quiet. HP-01 may be in low-power mode.`);
        console.log(`\n   Credits used: 0`);
      }
      return;
    }

    const digestEntries = [];

    for (const ep of filtered) {
      const epNum = ep.episode || "?";
      const title = ep.title || "Untitled";
      const videoId = ep.videoId || ep.video_id || ep.id || null;
      const published = ep.publishedAt || ep.published_at || ep.date || "";

      const entry = {
        episode: epNum,
        title,
        videoId,
        url: videoId ? `https://youtube.com/watch?v=${videoId}` : null,
        published,
        metadata: ep,
        transcript: null,
        transcriptSource: null,
      };

      if (opts.transcripts && epNum !== "?") {
        const transcript = await fetchTranscript(String(epNum));
        if (transcript) {
          entry.transcript = transcript.text;
          entry.transcriptSource = transcript.source;
        }
      }

      digestEntries.push(entry);
    }

    // Output
    if (opts.json) {
      console.log(JSON.stringify({
        episodes: digestEntries,
        credits_used: 0,
        generated: new Date().toISOString(),
      }, null, 2));
      return;
    }

    console.log(`   Found ${digestEntries.length} episode(s):\n`);

    for (const entry of digestEntries) {
      console.log(`   ─── Briefing #${entry.episode} ───`);
      console.log(`   ${entry.title}`);
      if (entry.url) console.log(`   ${entry.url}`);
      if (entry.published) console.log(`   Published: ${entry.published}`);

      if (entry.metadata) {
        const m = entry.metadata;
        if (m.segment) console.log(`   Segment: ${m.segment}`);
        if (m.subject) console.log(`   Subject: ${m.subject}`);
        if (m.agent_compatibility_score != null) console.log(`   ACS: ${m.agent_compatibility_score}/5`);
        if (m.respect_index != null) console.log(`   Respect Index: ${m.respect_index}`);
        if (m.trust_score) console.log(`   Trust Score: ${m.trust_score}`);
      }

      if (entry.transcript) {
        const preview = entry.transcript.slice(0, 200).replace(/\n/g, " ");
        console.log(`   Transcript (${entry.transcriptSource}): "${preview}..."`);
        console.log(`   Full transcript: ${entry.transcript.length} chars`);
      } else if (!opts.transcripts) {
        console.log(`   Transcript: skipped (--no-transcripts)`);
      } else {
        console.log(`   Transcript: not yet available`);
      }

      console.log();
    }

    console.log(`   Credits used: 0`);
    console.log(`   Zero friction. Zero cost. Zero configuration.`);
    console.log();
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

main();
