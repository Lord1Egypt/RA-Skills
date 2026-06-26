#!/usr/bin/env node
// ⚠️ DO NOT EDIT — auto-generated from sdks/_shared/scripts/sync.js
// Edit the source in sdks/_shared/scripts/ then run:
//   bash scripts/sync-shared-scripts.sh
// See docs/features/f-036/shared-scripts-consolidation.md

// ---------------------------------------------------------------------------
// sync.js — Bidirectional sync between Awareness memory and OpenClaw Markdown.
//
// OpenClaw's native memory is plain Markdown:
//   MEMORY.md           — long-term curated knowledge (decisions, preferences, facts)
//   memory/YYYY-MM-DD.md — daily logs (append-only)
//
// Exports:
//   syncDailyLog(content, source)        — write-back to daily log
//   syncKnowledgeCard(card)              — write-back to MEMORY.md
//   syncRecordToOpenClaw(content, insights, source) — combined write-back
// ---------------------------------------------------------------------------

"use strict";

const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const MAX_MEMORY_MD_ENTRY_CHARS = 1200; // per card summary in MEMORY.md
const MAX_DAILY_ENTRY_CHARS = 3000;     // per entry in daily log

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Resolve OpenClaw workspace directory. */
function resolveWorkspace() {
  const home = process.env.HOME || process.env.USERPROFILE || "";
  const candidates = [
    process.env.OPENCLAW_WORKSPACE,
    path.join(home, ".openclaw", "workspace"),
  ].filter(Boolean);
  for (const dir of candidates) {
    try { if (fs.existsSync(dir)) return dir; } catch { /* skip */ }
  }
  return null;
}

/** Get today's date as YYYY-MM-DD. */
function todayDate() {
  return new Date().toISOString().split("T")[0];
}

/** Get current time as HH:MM. */
function nowTime() {
  return new Date().toTimeString().slice(0, 5);
}

/** Safely append text to a file (creates parent dirs if needed). */
function appendToFile(filePath, content) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.appendFileSync(filePath, content, "utf8");
}

/** Read file content or return empty string. */
function readFileOr(filePath, fallback = "") {
  try { return fs.readFileSync(filePath, "utf8"); } catch { return fallback; }
}

// ---------------------------------------------------------------------------
// Write-back: Awareness → OpenClaw Markdown
// ---------------------------------------------------------------------------

/**
 * Append a daily log entry to memory/YYYY-MM-DD.md.
 * @param {string} content
 * @param {string} [source]
 */
function syncDailyLog(content, source = "awareness") {
  const workspace = resolveWorkspace();
  if (!workspace) return;
  try {
    const date = todayDate();
    const time = nowTime();
    const filePath = path.join(workspace, "memory", `${date}.md`);
    const truncated = content.slice(0, MAX_DAILY_ENTRY_CHARS);
    const entry = `\n### ${time} — [${source}]\n\n${truncated}\n\n---\n`;
    appendToFile(filePath, entry);
  } catch { /* best-effort */ }
}

/**
 * Append a knowledge card to MEMORY.md.
 * @param {{ category?: string, title?: string, summary?: string, tags?: string[] }} card
 */
function syncKnowledgeCard(card) {
  const workspace = resolveWorkspace();
  if (!workspace) return;
  try {
    const memoryMd = path.join(workspace, "MEMORY.md");
    const existing = readFileOr(memoryMd);

    // Deduplicate: skip if title already exists
    const title = card.title || "";
    if (title && existing.includes(title)) return;

    const category = card.category || "insight";
    const summary = (card.summary || "").slice(0, MAX_MEMORY_MD_ENTRY_CHARS);
    const tags = Array.isArray(card.tags) && card.tags.length > 0
      ? `\n_Tags: ${card.tags.join(", ")} | ${todayDate()}_`
      : `\n_${todayDate()}_`;
    const entry = `\n[${category}] **${title}**: ${summary}${tags}\n`;
    appendToFile(memoryMd, entry);
  } catch { /* best-effort */ }
}

/**
 * Sync a full record result to OpenClaw md files.
 * Handles both standard {knowledge_cards:[...]} and flat {category, decision} formats.
 * @param {string} content
 * @param {object} [insights]
 * @param {string} [source]
 */
function syncRecordToOpenClaw(content, insights, source = "awareness") {
  // 1. Always write daily log
  syncDailyLog(content, source);

  // 2. If insights contain knowledge cards, also write to MEMORY.md
  if (!insights) return;

  const cards = insights.knowledge_cards;
  if (Array.isArray(cards)) {
    // Standard format: { knowledge_cards: [{category, title, summary, tags}] }
    for (const card of cards) {
      if (card && typeof card === "object") syncKnowledgeCard(card);
    }
  } else if (insights.category || insights.title || insights.decision) {
    // Flat format from LLMs: { category: "decision", decision: "Use PostgreSQL", rationale: [...] }
    const title = String(insights.title || insights.decision || "");
    const summary = insights.rationale
      ? (Array.isArray(insights.rationale)
          ? insights.rationale.join("; ")
          : String(insights.rationale))
      : content.slice(0, MAX_MEMORY_MD_ENTRY_CHARS);
    if (title) {
      syncKnowledgeCard({
        category: String(insights.category || "insight"),
        title,
        summary,
        tags: Array.isArray(insights.tags) ? insights.tags : undefined,
      });
    }
  }
}

module.exports = { syncDailyLog, syncKnowledgeCard, syncRecordToOpenClaw, resolveWorkspace };
