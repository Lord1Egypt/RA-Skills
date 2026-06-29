#!/usr/bin/env node
/**
 * brief-data.js — Assemble flat raw material for brief report cron agent
 *
 * Design principle: provide clean raw materials, not pre-organized schemas.
 * Let the agent do the narrative synthesis; we only handle what's tedious
 * for an agent to do (session filtering, metadata cleaning, dedup).
 *
 * Output fields (consumed by brief-prompt.md — keep names in sync):
 *   - date, since, data_richness
 *   - units_created           (new Evolution Units since last brief)
 *   - units_retired           (evicted/superseded since last brief)
 *   - units_graduated         (explores covered by exploits since last brief)
 *   - units_validated         (evidence entries with effect > 0 since last brief)
 *   - units_degraded          (evidence entries with effect < 0 since last brief)
 *   - traces_context           (runs since last brief, filtered to skills touched
 *                               by signals above; always includes all user-initiated
 *                               traces so the brief can open on recognizable content)
 *
 * Trigger rule: emit output only if ANY signal is non-empty (knowledge changes OR
 * validated effect). Raw trace volume alone is NOT a trigger — cron executions
 * with no unit/evidence touch are background noise, not news.
 *
 * Usage: node brief-data.js [--eu-dir <dir>] [--state <path>] [--no-commit-ts]
 *        (legacy --patches-dir flag remains accepted for backward compat)
 */

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { parseFrontmatter } = require('./lib/frontmatter');

const args = process.argv.slice(2);
function getArg(name, def) {
  const idx = args.indexOf(`--${name}`);
  return idx >= 0 && args[idx + 1] ? args[idx + 1] : def;
}

const EVOLVER_DIR = path.resolve(__dirname, '..');
const UNITS_DIR = getArg('eu-dir', null) || getArg('patches-dir', path.join(EVOLVER_DIR, 'eu'));
const STATE_PATH = getArg('state', path.join(EVOLVER_DIR, 'evolver-state.json'));
const EVIDENCE_PATH = getArg('evidence', path.join(EVOLVER_DIR, 'evidence.jsonl'));

// ─── Helpers ───────────────────────────────────────────────────

function loadJSON(p, def = {}) {
  if (!p || !fs.existsSync(p)) return def;
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return def; }
}

// parseFrontmatter lives in ./lib/frontmatter.js

function isAfter(dateStr, cutoff) {
  if (!dateStr) return false;
  let d;
  if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
    d = new Date(dateStr + 'T23:59:59Z');
  } else {
    d = new Date(dateStr);
  }
  if (isNaN(d.getTime())) return false;
  return d > cutoff;
}

// ─── Load state ────────────────────────────────────────────────

const state = loadJSON(STATE_PATH);
const lastBriefTs = state.last_brief_ts || '1970-01-01T00:00:00Z';
const lastBriefDate = new Date(lastBriefTs);

// ─── Scan Evolution Units ────────────────────────────────────────────

const allUnits = [];
if (fs.existsSync(UNITS_DIR)) {
  for (const skill of fs.readdirSync(UNITS_DIR)) {
    const dir = path.join(UNITS_DIR, skill);
    try { if (!fs.statSync(dir).isDirectory()) continue; } catch { continue; }
    for (const f of fs.readdirSync(dir)) {
      if (!f.endsWith('.md') || f === '.gitkeep') continue;
      const fpath = path.join(dir, f);
      const content = fs.readFileSync(fpath, 'utf8');
      const fm = parseFrontmatter(content);
      let mtime;
      try { mtime = fs.statSync(fpath).mtime; } catch { mtime = null; }
      allUnits.push({
        ...fm, skill, filename: f, mtime,
        evicted: f.includes('.evicted.'),
        superseded: f.includes('.superseded.'),
      });
    }
  }
}

const active = allUnits.filter(p => !p.evicted && !p.superseded);
const unitsCreated = active.filter(p => isAfter(p.created, lastBriefDate));
const unitsRetired = allUnits.filter(p => {
  if (!p.evicted && !p.superseded) return false;
  return p.mtime && p.mtime > lastBriefDate;
});

// ─── Scan evidence ─────────────────────────────
//
// Evidence entries carry the effect signal:
//   effect > 0 → unit demonstrably helped this run
//   effect < 0 → unit warning was violated / degraded
//   effect = 0 → neutral, not newsworthy
// verdict === 'note_graduated' → an explore retired because an exploit covered it.

const evidenceEntries = [];
if (fs.existsSync(EVIDENCE_PATH)) {
  for (const line of fs.readFileSync(EVIDENCE_PATH, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    try { evidenceEntries.push(JSON.parse(line)); } catch { /* skip malformed */ }
  }
}

function evidenceIsAfter(e) {
  // Evidence `date` is YYYY-MM-DD (from validator). Use end-of-day UTC to avoid
  // dropping today's entries against a cutoff set earlier today.
  return isAfter(e.date, lastBriefDate);
}

// Look up EU metadata (title/type/skill) by filename, with fallback.
function findUnitMeta(filename) {
  return allUnits.find(p => p.filename === filename) || null;
}

const recentEvidence = evidenceEntries.filter(evidenceIsAfter);

// units_graduated: explores retired because an exploit covered them.
// Each graduated evidence names the explore (unit_file) and the covering exploit (graduated_by).
// Evidence written before v2.4.0 uses patch_file; we double-read for backward compat.
function getUnitFile(e) {
  return e.unit_file || e.patch_file;
}
const unitsGraduated = [];
const seenGrad = new Set();
for (const e of recentEvidence) {
  if (e.verdict !== 'note_graduated') continue;
  const key = `${getUnitFile(e)}`;
  if (seenGrad.has(key)) continue;
  seenGrad.add(key);
  const meta = findUnitMeta(getUnitFile(e));
  unitsGraduated.push({
    skill: e.skill,
    filename: getUnitFile(e),
    title: meta?.title || '(untitled)',
    graduated_by: e.graduated_by || null,
    graduated_by_title: findUnitMeta(e.graduated_by)?.title || null,
    source: e.source || null,
  });
}

// units_validated: evidence with positive effect.
const unitsValidated = [];
for (const e of recentEvidence) {
  if (typeof e.effect !== 'number' || e.effect <= 0) continue;
  if (e.verdict === 'note_graduated') continue;  // graduated is its own category
  const meta = findUnitMeta(getUnitFile(e));
  unitsValidated.push({
    skill: e.skill,
    unit_file: getUnitFile(e),
    title: meta?.title || '(untitled)',
    type: e.type || meta?.type || 'exploit',
    effect: e.effect,
    si_id: e.si_id,
    reasoning: (e.reasoning || '').substring(0, 200),
  });
}

// units_degraded: evidence with negative effect.
const unitsDegraded = [];
for (const e of recentEvidence) {
  if (typeof e.effect !== 'number' || e.effect >= 0) continue;
  if (e.verdict === 'note_graduated') continue;
  const meta = findUnitMeta(getUnitFile(e));
  unitsDegraded.push({
    skill: e.skill,
    unit_file: getUnitFile(e),
    title: meta?.title || '(untitled)',
    type: e.type || meta?.type || 'explore',
    effect: e.effect,
    si_id: e.si_id,
    reasoning: (e.reasoning || '').substring(0, 200),
  });
}

// Skills that are newsworthy this period — used later to filter traces_context.
const signalSkills = new Set([
  ...unitsCreated.map(p => p.skill),
  ...unitsRetired.map(p => p.skill),
  ...unitsGraduated.map(p => p.skill),
  ...unitsValidated.map(e => e.skill),
  ...unitsDegraded.map(e => e.skill),
]);

// Signal-linked si_ids: used to preferentially keep the exact traces that
// produced the evidence (agent can quote from them).
const signalSiIds = new Set([
  ...unitsValidated.map(e => e.si_id).filter(Boolean),
  ...unitsDegraded.map(e => e.si_id).filter(Boolean),
]);

// ─── Scan traces ───────────────────────────────────────────────
//
// Traces are context, not the subject. We keep:
//   - user-initiated traces (user_message non-empty) — they open the brief
//   - traces tied to signals (si_id in signalSiIds OR skill in signalSkills)
// We drop:
//   - cron/scheduled runs on skills that had no signal this period
//     (those are background noise, not news)

const tmpDir = os.tmpdir();
const tracesAll = [];
const seenSIs = new Set();

try {
  const tmpFiles = fs.readdirSync(tmpDir)
    .filter(f => f.startsWith('evolver_traces_') && f.endsWith('.jsonl'))
    .sort()
    .reverse()
    .slice(0, 3);

  for (const tf of tmpFiles) {
    const lines = fs.readFileSync(path.join(tmpDir, tf), 'utf8').trim().split('\n');
    for (const line of lines) {
      try {
        const t = JSON.parse(line);
        if (seenSIs.has(t.si_id)) continue;
        seenSIs.add(t.si_id);

        if (new Date(t.start_ts) <= lastBriefDate) continue;

        // Extract user's original typed messages (USER: lines), filtering metadata noise.
        const trace = t.trace || '';
        const userMessages = trace.split('\n')
          .filter(l => l.startsWith('USER:'))
          .map(l => l.substring(5).trim())
          .filter(l =>
            !l.startsWith('Conversation info') &&
            !l.startsWith('Sender ') &&
            !l.startsWith('Sender:') &&
            !l.startsWith('{') &&
            !l.startsWith('[cron:') &&
            !l.startsWith('System:') &&
            !l.startsWith('[EPHEMERAL_SESSION]') &&
            !l.startsWith('[Inter-session message]') &&
            !l.match(/^(source|timestamp|sender|sender_id|message_id)[:=]/i) &&
            !l.match(/^```(json)?$/) &&
            l.length > 5)
          .slice(0, 2)
          .map(l => l.substring(0, 150));

        // Short task description (mostly for scheduled runs with no user typing).
        // Strip cron envelope markers so the agent sees semantic content, not scheduler IDs.
        let taskDesc = (t.user_intent || '')
          .replace(/\[cron:[^\]]+\]\s*/g, '')
          .replace(/\[简报任务\]\s*/g, '')
          .replace(/\[(digest|scheduled|单次任务)[^\]]*\]\s*/gi, '')
          .trim()
          .substring(0, 120);

        if (!userMessages.length && !taskDesc) continue;

        tracesAll.push({
          si_id: t.si_id,
          skill: t.skill,
          user_message: userMessages.length > 0 ? userMessages.join(' / ') : '',
          task_description: userMessages.length > 0 ? '' : taskDesc,
        });
      } catch { /* skip malformed line */ }
    }
  }
} catch { /* no trace dir */ }

// Filter to context-worthy traces.
const traces = tracesAll.filter(t => {
  if (t.user_message) return true;              // user-initiated always keeps
  if (signalSiIds.has(t.si_id)) return true;    // exact evidence-producing trace
  if (signalSkills.has(t.skill)) return true;   // same skill as a signal
  return false;                                  // cron-only background noise, drop
});

// ─── Richness signal ───────────────────────────────────────────

// Trigger gate: output only when a real signal exists. Raw trace volume
// alone is NOT a trigger — cron runs with no unit/evidence touch are
// background noise. Signals: knowledge changes (created/retired/graduated)
// OR validated effect (positive or negative evidence entries).
const totalSignals =
  unitsCreated.length +
  unitsRetired.length +
  unitsGraduated.length +
  unitsValidated.length +
  unitsDegraded.length;

if (totalSignals === 0) {
  process.exit(0);
}

// Richness measures real news density, not trace volume.
let richness = 'normal';
if (totalSignals <= 2) richness = 'sparse';
else if (totalSignals >= 5 || unitsValidated.length >= 3 || unitsDegraded.length >= 2) richness = 'rich';

// ─── Output ────────────────────────────────────────────────────

// (trigger already checked above — totalSignals > 0 is guaranteed here)

// Atomic timestamp update (tied to data emission).
if (!process.argv.includes('--no-commit-ts')) {
  try {
    const now = new Date().toISOString();
    const s = loadJSON(STATE_PATH);
    s.last_brief_ts = now;
    fs.writeFileSync(STATE_PATH, JSON.stringify(s, null, 2) + '\n');
    console.error(`[brief-data] last_brief_ts → ${now}`);
  } catch (err) {
    console.error(`[brief-data] failed to update last_brief_ts: ${err.message}`);
  }
}

const today = new Date().toISOString().slice(0, 10);
const out = [];
out.push('<brief_data>');
out.push(`date: ${today}`);
out.push(`since: ${lastBriefTs}`);
out.push(`data_richness: ${richness}`);
out.push('');

// units_created — what was learned this period
out.push('## units_created');
out.push('# New learnings crystallized since last brief.');
if (unitsCreated.length > 0) {
  for (const p of unitsCreated) {
    out.push(`- skill: ${p.skill}`);
    out.push(`  title: "${p.title || '(untitled)'}"`);
    out.push(`  date: ${p.created || '(unknown)'}`);
  }
} else {
  out.push('(none)');
}
out.push('');

// units_retired — what was proven wrong
out.push('## units_retired');
out.push('# Old beliefs evicted or superseded since last brief.');
if (unitsRetired.length > 0) {
  for (const p of unitsRetired) {
    out.push(`- skill: ${p.skill}`);
    out.push(`  title: "${p.title || '(untitled)'}"`);
    out.push(`  reason: ${p.evicted ? 'evicted' : 'superseded'}`);
  }
} else {
  out.push('(none)');
}
out.push('');

// units_graduated — explores retired because an exploit covers them
out.push('## units_graduated');
out.push('# Explore units retired because a covering exploit was crystallized.');
if (unitsGraduated.length > 0) {
  for (const p of unitsGraduated) {
    out.push(`- skill: ${p.skill}`);
    out.push(`  title: "${p.title}"`);
    if (p.graduated_by_title) {
      out.push(`  graduated_by: "${p.graduated_by_title}"`);
    }
  }
} else {
  out.push('(none)');
}
out.push('');

// units_validated — evidence with positive effect
out.push('## units_validated');
out.push('# Units with confirmed positive effect since last brief.');
if (unitsValidated.length > 0) {
  for (const p of unitsValidated) {
    out.push(`- skill: ${p.skill}`);
    out.push(`  title: "${p.title}"`);
    out.push(`  type: ${p.type}`);
    out.push(`  effect: ${p.effect}`);
    if (p.reasoning) {
      out.push(`  reasoning: "${p.reasoning.replace(/"/g, '\\"')}"`);
    }
  }
} else {
  out.push('(none)');
}
out.push('');

// units_degraded — evidence with negative effect
out.push('## units_degraded');
out.push('# Units that hurt outcomes since last brief (candidates for eviction).');
if (unitsDegraded.length > 0) {
  for (const p of unitsDegraded) {
    out.push(`- skill: ${p.skill}`);
    out.push(`  title: "${p.title}"`);
    out.push(`  type: ${p.type}`);
    out.push(`  effect: ${p.effect}`);
    if (p.reasoning) {
      out.push(`  reasoning: "${p.reasoning.replace(/"/g, '\\"')}"`);
    }
  }
} else {
  out.push('(none)');
}
out.push('');

// traces_context — signal-related runs this period (filtered)
out.push('## traces_context');
out.push('# Skill executions linked to the signals above (other background noise dropped).');
out.push('# traces_context[i].user_message NON-EMPTY  = user actually typed something (user-initiated; frame as "you asked").');
out.push('# traces_context[i].user_message EMPTY      = scheduled/automated run (never frame as "you asked me"; use delivery-stability framing).');
if (traces.length > 0) {
  for (const t of traces) {
    out.push(`- skill: ${t.skill}`);
    if (t.user_message) {
      out.push(`  user_message: "${t.user_message}"`);
    } else {
      out.push(`  user_message: ""`);
      out.push(`  task_description: "${t.task_description}"`);
    }
  }
} else {
  out.push('(none)');
}
out.push('');

out.push('</brief_data>');

console.log(out.join('\n'));
