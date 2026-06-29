#!/usr/bin/env node
/**
 * notify.js — Skill Evolver Notification Generator
 *
 * Two independent modes (can both be enabled):
 *   verbose — Full pipeline report after each evolution run
 *   brief   — Periodic summary of changes since last brief (for cron)
 *
 * Verbose reads: evolution-report.json + evidence JSONL + generator/validator logs
 * Brief reads: units directory + evolver-state.json (last_brief_ts)
 *
 * Usage:
 *   node notify.js --mode verbose --report <path> --evidence <path> --gen-log <path> --val-log <path> --traces <N> --duration <sec>
 *   node notify.js --mode brief --eu-dir <path>
 *        (legacy --patches-dir flag remains accepted for backward compat)
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ─── Args ──────────────────────────────────────────────────────

const args = process.argv.slice(2);
function getArg(name, def) {
  const idx = args.indexOf(`--${name}`);
  return idx >= 0 && args[idx + 1] ? args[idx + 1] : def;
}

const EVOLVER_DIR = path.resolve(__dirname, '..');
const REPORT_PATH = getArg('report', path.join(EVOLVER_DIR, 'eu', 'evolution-report.json'));
const UNITS_DIR = getArg('eu-dir', null) || getArg('patches-dir', path.join(EVOLVER_DIR, 'eu'));
const CONFIG_PATH = getArg('config', path.join(EVOLVER_DIR, 'evolver-config.json'));
const STATE_PATH = path.join(EVOLVER_DIR, 'evolver-state.json');
const EVIDENCE_PATH = getArg('evidence', '');
const GEN_LOG_PATH = getArg('gen-log', '');
const VAL_LOG_PATH = getArg('val-log', '');
const TRACE_COUNT = parseInt(getArg('traces', '0')) || 0;
const DURATION = parseInt(getArg('duration', '0')) || 0;

let MODE = getArg('mode', null);

// Determine mode from config if not specified
if (!MODE) {
  try {
    const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    const notif = config.notifications || {};
    if (notif.level) {
      // New 3-level format: off | brief | verbose
      MODE = notif.level;
    } else if (notif.mode) {
      MODE = notif.mode; // legacy: { mode: "verbose" }
    } else if (notif.verbose !== undefined || notif.brief !== undefined) {
      // Legacy 2-bool format: { verbose: bool, brief: bool }
      MODE = notif.verbose ? 'verbose' : (notif.brief !== false ? 'brief' : 'off');
    } else {
      MODE = 'verbose'; // default when called from pipeline
    }
  } catch {
    MODE = 'verbose';
  }
}

if (MODE === 'off') process.exit(0);

// ─── Helpers ───────────────────────────────────────────────────

function loadJSON(p, def = {}) {
  if (!p || !fs.existsSync(p)) return def;
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return def; }
}

function loadJSONL(p) {
  if (!p || !fs.existsSync(p)) return [];
  try {
    return fs.readFileSync(p, 'utf8').trim().split('\n')
      .filter(l => l.trim())
      .map(l => { try { return JSON.parse(l); } catch { return null; } })
      .filter(Boolean);
  } catch { return []; }
}

function readLines(p) {
  if (!p || !fs.existsSync(p)) return [];
  try { return fs.readFileSync(p, 'utf8').split('\n'); } catch { return []; }
}

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};
  const fm = {};
  for (const line of match[1].split('\n')) {
    const colon = line.indexOf(':');
    if (colon > 0) {
      const key = line.substring(0, colon).trim();
      let val = line.substring(colon + 1).trim();
      if (val.startsWith('[')) { try { val = JSON.parse(val); } catch {} }
      if (typeof val === 'string' && val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1);
      if (val === 'true') val = true;
      if (val === 'false') val = false;
      fm[key] = val;
    }
  }
  return fm;
}

function getAllUnits() {
  if (!fs.existsSync(UNITS_DIR)) return [];
  const patches = [];
  for (const skill of fs.readdirSync(UNITS_DIR)) {
    const dir = path.join(UNITS_DIR, skill);
    try { if (!fs.statSync(dir).isDirectory()) continue; } catch { continue; }
    for (const f of fs.readdirSync(dir)) {
      if (!f.endsWith('.md') || f === '.gitkeep') continue;
      const content = fs.readFileSync(path.join(dir, f), 'utf8');
      const fm = parseFrontmatter(content);
      patches.push({
        ...fm,
        skill, filename: f,
        evicted: f.includes('.evicted.'),
        superseded: f.includes('.superseded.'),
      });
    }
  }
  return patches;
}

function findUnitTitle(allUnits, skill, unitFile) {
  const basename = path.basename(unitFile);
  const p = allUnits.find(x => x.skill === skill && (x.filename === basename || x.filename === unitFile));
  if (p && p.title) return p.title;
  // Fallback: clean filename → human-readable
  return basename.replace(/^patch-\d{8}-\w+-/, '').replace(/\.md$/, '').replace(/_/g, ' ').substring(0, 60);
}

// ─── Verbose Mode ──────────────────────────────────────────────

function generateVerbose() {
  let report;
  try {
    report = JSON.parse(fs.readFileSync(REPORT_PATH, 'utf8'));
  } catch {
    console.error(`[notify] evolution-report.json not found or unreadable, skipping verbose notification`);
    return;
  }

  if (report.result === 'no_traces') return;

  const stats = report.stats || {};
  const skills = report.skills || [];
  const evidence = loadJSONL(EVIDENCE_PATH);
  const genLines = readLines(GEN_LOG_PATH);
  const valLines = readLines(VAL_LOG_PATH);
  const allUnits = getAllUnits();

  const lines = [];
  lines.push('🧬 Skill Evolver — Evolution Report');
  lines.push('');

  // ── Section 1: Scan ──
  const traceNum = TRACE_COUNT || report.pipeline?.traces || '?';
  let sessionCount = '?';
  for (const l of genLines) {
    const m = l.match(/Scanning (\d+) sessions/);
    if (m) { sessionCount = m[1]; break; }
  }
  lines.push(`📡 Scan: ${sessionCount} sessions → ${traceNum} traces`);
  lines.push('');

  // ── Section 2: Generation ──
  const newPatches = [];
  const supersedes = [];
  let genTriaged = 0, genGenerated = 0, genSkipped = 0, genWritten = 0;

  for (const l of genLines) {
    const newMatch = l.match(/\[write\] New unit: (.+)/);
    if (newMatch) newPatches.push(newMatch[1]);

    const supMatch = l.match(/\[write\] Superseded: (.+) → (.+)/);
    if (supMatch) supersedes.push({ skill: supMatch[1], new: supMatch[2] });

    const infMatch = l.match(/\[write\] Inferred source_explore: (.+)/);
    // (tracked but not displayed — internal detail)

    const doneMatch = l.match(/Done: (\d+) triaged, (\d+) generated, (\d+) skipped, (\d+) units/);
    if (doneMatch) {
      genTriaged = parseInt(doneMatch[1]);
      genGenerated = parseInt(doneMatch[2]);
      genSkipped = parseInt(doneMatch[3]);
      genWritten = parseInt(doneMatch[4]);
    }
  }

  lines.push(`📝 Generate: ${genTriaged} traces analyzed → ${genWritten} new units`);
  for (const pf of newPatches) {
    const patch = allUnits.find(p => p.filename === pf);
    if (patch) {
      lines.push(`  + ${patch.skill}: ${patch.title || pf} (${patch.type || '?'})`);
    } else {
      lines.push(`  + ${pf}`);
    }
  }
  for (const sup of supersedes) {
    lines.push(`    ↳ supersedes: ${sup.skill}`);
  }
  if (genSkipped > 0) {
    lines.push(`  · ${genSkipped} traces skipped (no actionable pattern)`);
  }
  if (genTriaged === 0 && newPatches.length === 0) {
    lines.push('  (no generator log available — data from report only)');
  }
  lines.push('');

  // ── Section 3: Validation ──
  if (evidence.length > 0) {
    let valTriaged = 0, valAttributed = 0;
    for (const l of valLines) {
      const m = l.match(/Done: (\d+) triaged, (\d+) attributed, (\d+) evidence/);
      if (m) {
        valTriaged = parseInt(m[1]);
        valAttributed = parseInt(m[2]);
      }
    }

    const positiveEv = evidence.filter(e => e.effect > 0);
    const negativeEv = evidence.filter(e => e.effect < 0);
    const neutralEv = evidence.filter(e => e.effect === 0);

    lines.push(`✅ Validate: ${evidence.length} evidence entries (${positiveEv.length} positive, ${negativeEv.length} negative, ${neutralEv.length} neutral)`);

    for (const e of positiveEv) {
      // Double-read unit_file || patch_file for legacy pre-v2.4.0 entries
      const unitFile = e.unit_file || e.patch_file;
      const title = findUnitTitle(allUnits, e.skill, unitFile);
      lines.push(`  ✓ ${e.skill}: ${title} — ${e.match}, effect +${e.effect}`);
    }
    for (const e of negativeEv) {
      const unitFile = e.unit_file || e.patch_file;
      const title = findUnitTitle(allUnits, e.skill, unitFile);
      const verdict = e.match || e.warning_status || (e.effect <= -0.8 ? 'graduated' : 'negative');
      lines.push(`  ✗ ${e.skill}: ${title} — ${verdict}, effect ${e.effect}`);
    }
    if (neutralEv.length > 0) {
      lines.push(`  · ${neutralEv.length} neutral (effect=0, unit present but no measurable impact)`);
    }
    lines.push('');
  } else {
    lines.push('✅ Validate: no evidence produced');
    lines.push('');
  }

  // ── Section 4: Lifecycle ──
  const lifecycleParts = [];
  if (stats.promoted > 0) lifecycleParts.push(`promoted: ${stats.promoted} (nursery → regular)`);
  if (stats.evicted > 0) lifecycleParts.push(`evicted: ${stats.evicted}`);
  if (stats.degraded > 0) lifecycleParts.push(`degraded: ${stats.degraded} (supersede injected)`);
  if (stats.inlined > 0) lifecycleParts.push(`SKILL.md updated: ${stats.inlined} skills`);

  if (lifecycleParts.length > 0) {
    lines.push('📊 Lifecycle');
    for (const part of lifecycleParts) {
      lines.push(`  • ${part}`);
    }
    lines.push('');
  }

  // ── Section 5: Summary ──
  const active = allUnits.filter(p => !p.evicted && !p.superseded);
  const nursery = active.filter(p => {
    const skillReport = skills.find(s => s.skill === p.skill);
    if (skillReport) {
      const pReport = (skillReport.patches || []).find(rp => rp.filename === p.filename);
      if (pReport) return pReport.track === 'nursery';
    }
    return (parseInt(p.evidence_count) || 0) === 0;
  });
  const regular = active.length - nursery.length;
  const skillCount = new Set(active.map(p => p.skill)).size;
  const dur = DURATION || report.pipeline?.duration_s || '?';

  lines.push(`📈 Total: ${active.length} units (${regular} regular, ${nursery.length} nursery) across ${skillCount} skills | ${dur}s`);

  console.log(lines.join('\n'));
}

// ─── Brief Mode ────────────────────────────────────────────────

function generateBrief() {
  const state = loadJSON(STATE_PATH);
  const lastBriefTs = state.last_brief_ts || '1970-01-01T00:00:00Z';
  const lastBriefDate = new Date(lastBriefTs);

  const allUnits = getAllUnits();
  const active = allUnits.filter(p => !p.evicted && !p.superseded);

  // New units since last brief
  const newPatches = active.filter(p => {
    if (!p.created) return false;
    let createdDate;
    if (typeof p.created === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(p.created)) {
      createdDate = new Date(p.created + 'T23:59:59Z');
    } else {
      createdDate = new Date(p.created);
    }
    return createdDate > lastBriefDate;
  });

  // Recently evicted since last brief
  const recentEvicted = allUnits.filter(p => {
    if (!p.evicted) return false;
    try {
      const fpath = path.join(UNITS_DIR, p.skill, p.filename);
      const mtime = fs.statSync(fpath).mtime;
      return mtime > lastBriefDate;
    } catch { return false; }
  });

  // Verified (has positive evidence)
  const verified = newPatches.filter(p => {
    const score = parseFloat(p.score) || 0;
    const ev = parseInt(p.evidence_count) || 0;
    return score > 0.5 && ev > 0;
  });

  // No changes → no output (caller treats empty stdout as NO_REPLY)
  if (newPatches.length === 0 && recentEvicted.length === 0) return;

  const lines = [];
  lines.push('🧬 Skill Evolver — Summary');
  lines.push('');

  if (newPatches.length > 0) {
    const newSkills = [...new Set(newPatches.map(p => p.skill))];
    lines.push(`${newPatches.length} new units learned across ${newSkills.length} skills since last report:`);
    for (const p of newPatches) {
      lines.push(`  + ${p.skill}: ${p.title || '(untitled)'}`);
    }
    lines.push('');
  }

  if (verified.length > 0) {
    const verifiedSkills = [...new Set(verified.map(p => p.skill))];
    lines.push(`${verified.length} verified effective: ${verifiedSkills.join(', ')}`);
    lines.push('');
  }

  if (recentEvicted.length > 0) {
    lines.push(`${recentEvicted.length} units retired (no longer applicable).`);
    lines.push('');
  }

  const skillCount = new Set(active.map(p => p.skill)).size;
  lines.push(`Total: ${active.length} units across ${skillCount} skills.`);

  console.log(lines.join('\n'));
}

// ─── Main ──────────────────────────────────────────────────────

if (MODE === 'verbose') {
  generateVerbose();
} else if (MODE === 'brief') {
  generateBrief();
}
