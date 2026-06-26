#!/usr/bin/env node
// ⚠️ DO NOT EDIT — auto-generated from sdks/_shared/scripts/capture.js
// Edit the source in sdks/_shared/scripts/ then run:
//   bash scripts/sync-shared-scripts.sh
// See docs/features/f-036/shared-scripts-consolidation.md

// ---------------------------------------------------------------------------
// Stop hook — DISABLED
//
// Session checkpoints were low-value noise: truncated 200-char snippets of
// Claude's responses, lacking structure or insight. They polluted both local
// storage and cloud sync with "Session checkpoint: ..." entries that diluted
// recall quality.
//
// Meaningful content is already captured via:
//   1. awareness_record (record-rule in CLAUDE.md) — structured decisions,
//      solutions, pitfalls with knowledge cards
//   2. save-memory.js — fire-and-forget auto-save after significant work
//
// This script is kept as a no-op to avoid breaking the SKILL.md hook
// registration. It exits immediately with no side effects.
// ---------------------------------------------------------------------------

process.exit(0);
