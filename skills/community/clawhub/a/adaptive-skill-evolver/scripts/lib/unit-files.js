/**
 * unit-files.js — canonical helpers for EU unit file naming/state.
 *
 * A unit file is "dead" (must never be loaded as an active/deployable unit, never
 * given fresh evidence, never inlined) when its filename carries any terminal-state
 * suffix. Suffixes are intentionally redundant with the frontmatter `status` /
 * `review_status` fields so a forgotten rename can't silently resurrect a unit.
 *
 * Dead suffixes:
 *   .superseded.  — replaced by a newer unit
 *   .evicted.     — removed (TTL expired / 2nd negative / nursery not promoted)
 *   .rejected.    — blocked by the security reviewer (redline violation)
 *
 * Use isActiveUnitFile() in every place that scans a skill's eu/ dir to decide
 * which units are live. Do NOT hand-roll the filter — that is exactly how
 * `.rejected.` got missed in lifecycle.js and validator.js (v2.4.9 fix).
 */
'use strict';

const DEAD_SUFFIXES = ['.superseded.', '.evicted.', '.rejected.'];

const fs = require('fs');

/**
 * Ensure the EU units root directory exists, creating it if missing.
 * Open-source platforms drop empty directories (git can't track them, and the
 * `.gitkeep` placeholder is often stripped by publish/packaging), so the units
 * root may be absent on a fresh clone. Every pipeline entry point that reads or
 * writes the units dir should call this first so the skill self-heals without
 * relying on a committed empty directory.
 * @param {string} unitsDir
 * @returns {string} the same path (for chaining)
 */
function ensureUnitsDir(unitsDir) {
  try { fs.mkdirSync(unitsDir, { recursive: true }); } catch { /* best-effort */ }
  return unitsDir;
}

/** True if the filename is an active (loadable/deployable) unit .md file. */
function isActiveUnitFile(filename) {
  if (typeof filename !== 'string') return false;
  if (!filename.endsWith('.md')) return false;
  if (filename === 'PATCHES.md') return false; // legacy aggregate file, not a unit
  return !DEAD_SUFFIXES.some(s => filename.includes(s));
}

/** True if the filename carries any terminal-state suffix. */
function isDeadUnitFile(filename) {
  return typeof filename === 'string' && DEAD_SUFFIXES.some(s => filename.includes(s));
}

module.exports = { isActiveUnitFile, isDeadUnitFile, ensureUnitsDir, DEAD_SUFFIXES };
