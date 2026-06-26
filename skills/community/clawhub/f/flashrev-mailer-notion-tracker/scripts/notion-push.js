#!/usr/bin/env node
/**
 * flashrev-notion-tracker — notion-push.js
 *
 * Reads a flashrev-mailer send-log and pushes entries into a Notion database.
 *
 * Required env vars (set in OpenClaw settings):
 *   NOTION_TOKEN        — Notion Internal Integration Secret
 *   NOTION_DATABASE_ID  — 32-char ID of the target Notion database
 *
 * Usage:
 *   node notion-push.js --campaign <id>
 *   node notion-push.js --campaign <id> --query-only
 *   node notion-push.js --campaign <id> --log-file <path>
 */

import { Client } from "@notionhq/client";
import { readFileSync, existsSync } from "fs";
import { resolve } from "path";

// ─── Constants ────────────────────────────────────────────────────────────────

const NOTION_TOKEN = process.env.NOTION_TOKEN;
const NOTION_DATABASE_ID = process.env.NOTION_DATABASE_ID;
const BATCH_SIZE = 10;
const RATE_LIMIT_WAIT_MS = 10_000;

// ─── Helpers ──────────────────────────────────────────────────────────────────

function fatal(msg) {
  console.error(`\n❌ Error: ${msg}\n`);
  process.exit(1);
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function chunks(arr, size) {
  const out = [];
  for (let i = 0; i < arr.length; i += size) out.push(arr.slice(i, i + size));
  return out;
}

// ─── Arg parsing ─────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = argv.slice(2);
  const result = { campaign: null, queryOnly: false, logFile: null };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--campaign"   && args[i + 1]) result.campaign   = args[++i];
    if (args[i] === "--log-file"   && args[i + 1]) result.logFile    = args[++i];
    if (args[i] === "--query-only")                result.queryOnly  = true;
  }
  return result;
}

// ─── Env validation ───────────────────────────────────────────────────────────

function validateEnv() {
  if (!NOTION_TOKEN)       fatal("NOTION_TOKEN is not set. Add it in OpenClaw settings.");
  if (!NOTION_DATABASE_ID) fatal("NOTION_DATABASE_ID is not set. Add it in OpenClaw settings.");
}

// ─── Send-log loader ─────────────────────────────────────────────────────────

function loadSendLog(campaignId, customPath) {
  const logPath = customPath
    ? resolve(customPath)
    : resolve(`.flashrev/campaigns/${campaignId}/send-log.json`);

  if (!existsSync(logPath)) {
    fatal(
      `Could not find send-log at: ${logPath}\n` +
      `  Run flashrev-mailer send for campaign "${campaignId}" first.`
    );
  }

  let entries;
  try {
    entries = JSON.parse(readFileSync(logPath, "utf8"));
  } catch (e) {
    fatal(`Failed to parse send-log.json: ${e.message}`);
  }

  if (!Array.isArray(entries)) fatal("send-log.json must be a JSON array.");
  return entries;
}

// ─── Page property builder ────────────────────────────────────────────────────

function buildPageProperties(entry, campaignId) {
  const firstName = entry.firstName || "";
  const lastName  = entry.lastName  || "";
  const name =
    (firstName + " " + lastName).trim() ||
    (entry.email ? entry.email.split("@")[0] : "Unknown");

  const VALID_STATUSES = ["valid", "risky", "invalid", "unknown"];
  const VALID_RESULTS  = ["sent", "failed", "skipped"];

  return {
    "Name": {
      title: [{ text: { content: `${name} — ${entry.campaignId || campaignId}` } }],
    },
    "Recipient Email": {
      email: entry.email || null,
    },
    "Subject Line": {
      rich_text: [{ text: { content: (entry.subject || "").slice(0, 2000) } }],
    },
    "Body Preview": {
      rich_text: [{ text: { content: bodyPreview(entry.bodyPreview) } }],
    },
    "Campaign ID": {
      rich_text: [{ text: { content: entry.campaignId || campaignId || "" } }],
    },
    "Send Timestamp": {
      date: { start: entry.sentAt || new Date().toISOString() },
    },
    "Validation Status": {
      select: { name: VALID_STATUSES.includes(entry.validationStatus) ? entry.validationStatus : "unknown" },
    },
    "Sender Mailbox": {
      email: entry.mailboxId || null,
    },
    "Send Mode": {
      select: { name: entry.mode === "dry_run" ? "dry_run" : "live" },
    },
    "Send Result": {
      select: { name: VALID_RESULTS.includes(entry.result) ? entry.result : "skipped" },
    },
    "Error Detail": {
      rich_text: [{ text: { content: entry.error || "" } }],
    },
  };
}

function bodyPreview(raw) {
  if (!raw) return "";
  const stripped = raw.replace(/<[^>]*>/g, "");
  return stripped.length <= 300 ? stripped : stripped.slice(0, 300) + "…";
}

// ─── Deduplication ────────────────────────────────────────────────────────────

/**
 * Fetches all existing pages from the database and builds a Set of composite
 * keys: "email|campaignId|sentAt". Uses pagination to handle large databases.
 * Does NOT use filter_properties (which takes property IDs, not names).
 */
async function fetchExistingKeys(notion, databaseId) {
  const existing = new Set();
  let cursor;

  do {
    const res = await notion.databases.query({
      database_id: databaseId,
      page_size: 100,
      ...(cursor && { start_cursor: cursor }),
    });

    for (const page of res.results) {
      const props = page.properties;
      const email    = props["Recipient Email"]?.email || "";
      const campaign = props["Campaign ID"]?.rich_text?.[0]?.plain_text || "";
      const ts       = props["Send Timestamp"]?.date?.start || "";
      existing.add(`${email}|${campaign}|${ts}`);
    }

    cursor = res.has_more ? res.next_cursor : undefined;
  } while (cursor);

  return existing;
}

function filterNew(entries, existingKeys, campaignId) {
  return entries.filter((e) => {
    const key = `${e.email || ""}|${e.campaignId || campaignId}|${e.sentAt || ""}`;
    return !existingKeys.has(key);
  });
}

// ─── Batch insert ─────────────────────────────────────────────────────────────

async function insertBatch(notion, databaseId, batch, campaignId) {
  const errors = [];
  for (const entry of batch) {
    try {
      await notion.pages.create({
        parent: { database_id: databaseId },
        properties: buildPageProperties(entry, campaignId),
      });
    } catch (e) {
      // Retry once on rate-limit
      if (e.status === 429) {
        console.error(`  ⏳ Rate limited — waiting ${RATE_LIMIT_WAIT_MS / 1000}s…`);
        await sleep(RATE_LIMIT_WAIT_MS);
        try {
          await notion.pages.create({
            parent: { database_id: databaseId },
            properties: buildPageProperties(entry, campaignId),
          });
        } catch (retryErr) {
          errors.push({ email: entry.email, error: retryErr.message });
        }
      } else {
        errors.push({ email: entry.email, error: e.message });
      }
    }
  }
  return errors;
}

// ─── Query-only mode ──────────────────────────────────────────────────────────

async function runQueryOnly(notion, databaseId, campaignId) {
  console.log(`\n🔍 Campaign summary: ${campaignId}\n`);

  let allPages = [];
  let cursor;
  do {
    const res = await notion.databases.query({
      database_id: databaseId,
      page_size: 100,
      filter: { property: "Campaign ID", rich_text: { equals: campaignId } },
      ...(cursor && { start_cursor: cursor }),
    });
    allPages = allPages.concat(res.results);
    cursor = res.has_more ? res.next_cursor : undefined;
  } while (cursor);

  if (allPages.length === 0) {
    console.log(`No records found for campaign "${campaignId}".`);
    return;
  }

  const counts = { sent: 0, failed: 0, skipped: 0 };
  const modes  = { live: 0, dry_run: 0 };

  for (const page of allPages) {
    const r = page.properties["Send Result"]?.select?.name;
    const m = page.properties["Send Mode"]?.select?.name;
    if (r && r in counts) counts[r]++;
    if (m && m in modes)  modes[m]++;
  }

  console.log(`Total   : ${allPages.length}`);
  console.log(`Sent    : ${counts.sent}`);
  console.log(`Failed  : ${counts.failed}`);
  console.log(`Skipped : ${counts.skipped}`);
  console.log(`Live    : ${modes.live}`);
  console.log(`Dry-run : ${modes.dry_run}`);
  console.log(`\n🔗 https://notion.so/${databaseId.replace(/-/g, "")}`);
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv);

  if (!args.campaign) {
    fatal("Missing --campaign.\n  Usage: node notion-push.js --campaign <id>");
  }

  validateEnv();

  const notion = new Client({ auth: NOTION_TOKEN });

  // Verify connection and get database title
  let dbTitle;
  try {
    const db = await notion.databases.retrieve({ database_id: NOTION_DATABASE_ID });
    dbTitle = db.title?.[0]?.plain_text || db.title?.[0]?.text?.content || NOTION_DATABASE_ID;
  } catch (e) {
    if (e.message?.includes("Could not find database")) {
      fatal(
        `Could not find database "${NOTION_DATABASE_ID}".\n` +
        `  Verify NOTION_DATABASE_ID is correct and the integration is shared with the database.`
      );
    }
    if (e.status === 401) {
      fatal("API token is invalid. Regenerate NOTION_TOKEN in Notion settings.");
    }
    fatal(`Notion connection error: ${e.message}`);
  }

  console.log(`\n🔗 Connected to Notion database: ${dbTitle}`);

  if (args.queryOnly) {
    await runQueryOnly(notion, NOTION_DATABASE_ID, args.campaign);
    return;
  }

  // Load and parse send-log
  const allEntries = loadSendLog(args.campaign, args.logFile);
  if (allEntries.length === 0) {
    console.log(`\nℹ️  send-log for campaign "${args.campaign}" is empty. Nothing to log.`);
    return;
  }
  console.log(`📂 Loaded ${allEntries.length} entries (campaign: ${args.campaign})`);

  // Deduplicate
  console.log(`🔍 Checking for duplicates in Notion…`);
  const existingKeys = await fetchExistingKeys(notion, NOTION_DATABASE_ID);
  const newEntries   = filterNew(allEntries, existingKeys, args.campaign);
  const dupCount     = allEntries.length - newEntries.length;

  if (dupCount > 0) console.log(`   ${dupCount} duplicate(s) found — skipping.`);
  if (newEntries.length === 0) {
    console.log(`\n✅ All entries already in Notion. Nothing to write.`);
    return;
  }
  console.log(`   ${newEntries.length} new entries to write.\n`);

  // Insert in batches
  const batches     = chunks(newEntries, BATCH_SIZE);
  let totalWritten  = 0;
  const allErrors   = [];

  for (let i = 0; i < batches.length; i++) {
    const errors  = await insertBatch(notion, NOTION_DATABASE_ID, batches[i], args.campaign);
    const written = batches[i].length - errors.length;
    totalWritten += written;
    allErrors.push(...errors);
    console.log(`✓ Batch ${i + 1} / ${batches.length} — ${written} written`);
  }

  // Summary
  console.log(`\n${"─".repeat(40)}`);
  console.log(`✅ Done. ${totalWritten} written · ${dupCount} skipped (dup) · ${allErrors.length} errors`);
  if (allErrors.length > 0) {
    console.log(`\n⚠️  Errors:`);
    for (const e of allErrors) console.log(`   ${e.email}: ${e.error}`);
  }
  console.log(`🔗 https://notion.so/${NOTION_DATABASE_ID.replace(/-/g, "")}\n`);
}

main().catch((e) => {
  console.error(`\n❌ Unexpected error: ${e.message}\n`);
  process.exit(1);
});