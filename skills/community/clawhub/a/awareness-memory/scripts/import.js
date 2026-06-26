#!/usr/bin/env node
// ⚠️ DO NOT EDIT — auto-generated from sdks/_shared/scripts/import.js
// Edit the source in sdks/_shared/scripts/ then run:
//   bash scripts/sync-shared-scripts.sh
// See docs/features/f-036/shared-scripts-consolidation.md

// ---------------------------------------------------------------------------
// import.js — Import existing OpenClaw Markdown memory into Awareness.
// Runs once on first install. Idempotent via marker file.
//
// Sources imported:
//   1. MEMORY.md              — long-term knowledge cards
//   2. memory/YYYY-MM-DD.md   — daily logs (last 30 days)
//   3. agents/main/sessions/  — session JSONL files (last 20)
// ---------------------------------------------------------------------------

"use strict";

const fs = require("fs");
const path = require("path");
const { loadConfig, resolveEndpoint, mcpCall, apiPost } = require("./shared");
const { resolveWorkspace } = require("./sync");

const MIGRATION_MARKER = ".awareness-openclaw-imported";
const MAX_IMPORT_DAILY_BLOCK_CHARS = 3000;
const MAX_IMPORT_SESSION_MSG_CHARS = 800;
const MAX_IMPORT_SESSIONS = 20;
const MAX_IMPORT_MESSAGES_PER_SESSION = 15;

// ---------------------------------------------------------------------------
// Marker helpers
// ---------------------------------------------------------------------------

function isImported(workspace) {
  return fs.existsSync(path.join(workspace, MIGRATION_MARKER));
}

function markImported(workspace) {
  try {
    fs.writeFileSync(
      path.join(workspace, MIGRATION_MARKER),
      `Imported at ${new Date().toISOString()}\n`,
      "utf8",
    );
  } catch { /* best-effort */ }
}

// ---------------------------------------------------------------------------
// Parsers
// ---------------------------------------------------------------------------

/**
 * Parse MEMORY.md into individual entries.
 * Supports [category] **Title**: Summary format and free-form paragraphs.
 */
function parseMemoryMd(content) {
  const entries = [];
  if (!content.trim()) return entries;
  const blocks = content.split(/\n(?:\s*\n|\s*---\s*\n)/).filter(b => b.trim().length > 20);
  for (const block of blocks) {
    const trimmed = block.trim();
    const match = trimmed.match(/^\[(\w+)\]\s*(.*)/s);
    if (match) {
      entries.push({ text: match[2].trim(), category: match[1] });
    } else {
      entries.push({ text: trimmed });
    }
  }
  return entries;
}

/**
 * Parse memory/YYYY-MM-DD.md daily logs into entries.
 */
function parseDailyMd(content, date) {
  const entries = [];
  if (!content.trim()) return entries;
  const blocks = content.split(/(?=^### |\n---\n)/m).filter(b => b.trim().length > 20);
  for (const block of blocks) {
    entries.push({ text: block.trim().slice(0, MAX_IMPORT_DAILY_BLOCK_CHARS), date });
  }
  return entries;
}

/**
 * Parse a session JSONL file into a summary string.
 */
function parseSessionJsonl(filePath) {
  try {
    const raw = fs.readFileSync(filePath, "utf8");
    const lines = raw.split("\n").filter(l => l.trim());
    const messages = [];

    for (const line of lines) {
      try {
        const obj = JSON.parse(line);
        if (obj.type !== "message") continue;
        const msg = obj.message;
        if (!msg || !msg.role) continue;
        const role = msg.role;
        if (role !== "user" && role !== "assistant") continue;

        let text = "";
        if (typeof msg.content === "string") {
          text = msg.content;
        } else if (Array.isArray(msg.content)) {
          text = msg.content
            .filter(c => c.type === "text")
            .map(c => c.text)
            .join("\n");
        }
        if (!text || text.startsWith("/")) continue;

        // Remove awareness-memory XML blocks
        text = text.replace(/<awareness-memory>[\s\S]*?<\/awareness-memory>/g, "").trim();
        if (text.length < 10) continue;

        messages.push({ role, text: text.slice(0, MAX_IMPORT_SESSION_MSG_CHARS) });
      } catch { /* skip malformed line */ }
    }

    if (messages.length === 0) return null;

    const recent = messages.slice(-MAX_IMPORT_MESSAGES_PER_SESSION);
    return recent.map(m => `${m.role}: ${m.text}`).join("\n\n");
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Main import logic
// ---------------------------------------------------------------------------

async function main() {
  const workspace = resolveWorkspace();
  if (!workspace) {
    process.stderr.write("[awareness-import] No OpenClaw workspace found\n");
    process.exit(0);
  }

  if (isImported(workspace)) {
    process.exit(0);
  }

  const config = loadConfig();
  const ep = await resolveEndpoint(config);
  if (!ep) {
    process.stderr.write("[awareness-import] No Awareness endpoint available\n");
    process.exit(0);
  }

  const batchItems = [];

  // 1. Import MEMORY.md
  const memoryMdPath = path.join(workspace, "MEMORY.md");
  if (fs.existsSync(memoryMdPath)) {
    const entries = parseMemoryMd(fs.readFileSync(memoryMdPath, "utf8"));
    for (const entry of entries) {
      batchItems.push(
        `[OpenClaw MEMORY.md${entry.category ? ` / ${entry.category}` : ""}] ${entry.text}`,
      );
    }
    process.stderr.write(`[awareness-import] Found ${entries.length} entries in MEMORY.md\n`);
  }

  // 2. Import memory/*.md daily logs (last 30 days)
  const memoryDir = path.join(workspace, "memory");
  if (fs.existsSync(memoryDir)) {
    const files = fs.readdirSync(memoryDir)
      .filter(f => f.endsWith(".md"))
      .sort()
      .slice(-30);
    for (const file of files) {
      const date = file.replace(".md", "");
      const content = (() => { try { return fs.readFileSync(path.join(memoryDir, file), "utf8"); } catch { return ""; } })();
      const entries = parseDailyMd(content, date);
      for (const entry of entries) {
        batchItems.push(`[OpenClaw daily/${date}] ${entry.text}`);
      }
    }
    process.stderr.write(`[awareness-import] Found ${files.length} daily log files\n`);
  }

  // 3. Import session JSONL files (most recent N)
  const home = process.env.HOME || "";
  const sessionsDir = path.join(home, ".openclaw", "agents", "main", "sessions");
  if (fs.existsSync(sessionsDir)) {
    const sessionFiles = fs.readdirSync(sessionsDir)
      .filter(f => f.endsWith(".jsonl"))
      .sort()
      .slice(-MAX_IMPORT_SESSIONS);
    let sessionCount = 0;
    for (const file of sessionFiles) {
      const summary = parseSessionJsonl(path.join(sessionsDir, file));
      if (summary) {
        batchItems.push(`[OpenClaw session/${file.replace(".jsonl", "")}]\n${summary}`);
        sessionCount++;
      }
    }
    process.stderr.write(`[awareness-import] Found ${sessionCount} sessions with content\n`);
  }

  // 4. Batch record to Awareness in chunks of 10
  let imported = 0;
  let skipped = 0;

  if (batchItems.length > 0) {
    for (let i = 0; i < batchItems.length; i += 10) {
      const chunk = batchItems.slice(i, i + 10);
      const content = chunk.join("\n\n---\n\n");
      try {
        if (ep.mode === "local") {
          await mcpCall(ep.localUrl, "awareness_record", {
            action: "remember",
            content,
            event_type: "openclaw_import",
          }, 15000);
        } else {
          await apiPost(ep.baseUrl, ep.apiKey, "/mcp/events", {
            memory_id: ep.memoryId,
            content,
            event_type: "openclaw_import",
            source: "openclaw-skill",
          });
        }
        imported += chunk.length;
      } catch (err) {
        skipped += chunk.length;
        process.stderr.write(`[awareness-import] Batch ${Math.floor(i / 10) + 1} failed: ${err.message}\n`);
      }
    }
  }

  markImported(workspace);
  process.stderr.write(`[awareness-import] Complete: ${imported} imported, ${skipped} skipped\n`);
}

main().catch(err => {
  process.stderr.write(`[awareness-import] Failed: ${err.message}\n`);
  process.exit(0);
});
