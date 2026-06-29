/**
 * blocklist.js — per-skill evolution blocklist.
 *
 * Users can block specific skills so the evolver stops touching them:
 *   - trace-extractor skips blocked skills (no new EUs generated)
 *   - lifecycle skips inlining blocked skills (existing EUs stay archived but
 *     are NOT attached to the live SKILL.md)
 *
 * The blocklist is user intent, so it lives in evolver-config.json (persistent,
 * hand-editable, visible) — NOT in evolver-state.json (runtime data).
 *
 *   {
 *     "blockedSkills": ["apewisdom", "news-summary"]
 *   }
 *
 * EU files for a blocked skill are intentionally preserved on disk (archived),
 * so unblocking + re-running restores them. Blocking never deletes lessons.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

function configCandidates() {
  const EVOLVER_DIR = path.resolve(__dirname, '..', '..');
  return [
    process.env.EVOLVER_CONFIG,
    path.join(EVOLVER_DIR, 'evolver-config.json'),
    path.join(os.homedir(), '.evolver', 'config.json'),
  ].filter(Boolean);
}

/** Resolve the active evolver-config.json path (first existing candidate). */
function resolveConfigPath() {
  for (const p of configCandidates()) {
    if (fs.existsSync(p)) return p;
  }
  // Default write target: skill-local config.
  return path.join(path.resolve(__dirname, '..', '..'), 'evolver-config.json');
}

/** Return the set of blocked skill names (lowercased exact match by name). */
function getBlockedSkills() {
  for (const p of configCandidates()) {
    if (!fs.existsSync(p)) continue;
    try {
      const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
      const list = cfg.blockedSkills;
      if (Array.isArray(list)) return new Set(list.map(String));
    } catch { /* fall through */ }
  }
  return new Set();
}

function isSkillBlocked(skill) {
  return getBlockedSkills().has(String(skill));
}

/** Add a skill to the blocklist. Returns the updated list. */
function blockSkill(skill) {
  const p = resolveConfigPath();
  let cfg = {};
  if (fs.existsSync(p)) {
    try { cfg = JSON.parse(fs.readFileSync(p, 'utf8')); } catch { cfg = {}; }
  }
  const set = new Set(Array.isArray(cfg.blockedSkills) ? cfg.blockedSkills.map(String) : []);
  set.add(String(skill));
  cfg.blockedSkills = [...set].sort();
  fs.writeFileSync(p, JSON.stringify(cfg, null, 2) + '\n');
  return cfg.blockedSkills;
}

/** Remove a skill from the blocklist. Returns the updated list. */
function unblockSkill(skill) {
  const p = resolveConfigPath();
  let cfg = {};
  if (fs.existsSync(p)) {
    try { cfg = JSON.parse(fs.readFileSync(p, 'utf8')); } catch { cfg = {}; }
  }
  const set = new Set(Array.isArray(cfg.blockedSkills) ? cfg.blockedSkills.map(String) : []);
  set.delete(String(skill));
  cfg.blockedSkills = [...set].sort();
  fs.writeFileSync(p, JSON.stringify(cfg, null, 2) + '\n');
  return cfg.blockedSkills;
}

module.exports = { getBlockedSkills, isSkillBlocked, blockSkill, unblockSkill, resolveConfigPath };
