#!/usr/bin/env node
/**
 * evolver-cli.js — Skill Evolver v2.0 Query & Control Interface
 * 
 * Agent-facing CLI for querying status, managing units, and controlling evolution.
 * Query commands read from local files only (no LLM calls, no network).
 * Control commands (pin, unpin, block, unblock, evict, pause, resume, clear, feedback)
 * write to local state/unit files — no LLM calls, no external network.
 * 
 * Commands:
 *   status                    Overall status summary
 *   units [skill]             List units for a skill (or all)
 *   patches                   (deprecated alias for 'units')
 *   history [--limit N]       Recent evolution runs
 *   explain <unit-file>       Full detail for a specific unit
 *   pin <unit-file>           Protect unit from eviction
 *   unpin <unit-file>         Remove protection
 *   evict <unit-file>         Manually evict a unit
 *   feedback <unit> good|bad  Add user evidence
 *   pause                     Pause automatic evolution
 *   resume                    Resume automatic evolution
 *   config [key] [value]      View or set config
 *   check                     Environment check (LLM, sessions, units)
 *   clear <skill>|--all       Detach (un-inline) a skill's EUs from SKILL.md (archived, not deleted)
 *   block <skill>             Exclude a skill from future evolution + detach now
 *   unblock <skill>           Allow a skill to evolve again
 *   blocklist                 Show blocked skills
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { parseFrontmatter } = require('./lib/frontmatter');
const { appendEvent } = require('./lib/events');
const { getBlockedSkills, blockSkill, unblockSkill } = require('./lib/blocklist');
const { isActiveUnitFile } = require('./lib/unit-files');

function isDir(p) { try { return fs.statSync(p).isDirectory(); } catch { return false; } }

const EVOLVER_DIR = path.resolve(__dirname, '..');
const UNITS_DIR = path.join(EVOLVER_DIR, 'eu');
const STATE_PATH = path.join(EVOLVER_DIR, 'evolver-state.json');
const CONFIG_PATH = path.join(EVOLVER_DIR, 'evolver-config.json');
const REPORT_PATH = path.join(UNITS_DIR, 'evolution-report.json');

// ─── Helpers ───────────────────────────────────────────────────

function loadJSON(p, def = {}) {
  if (!fs.existsSync(p)) return def;
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return def; }
}

function saveJSON(p, data) {
  fs.writeFileSync(p, JSON.stringify(data, null, 2) + '\n');
}

// parseFrontmatter lives in ./lib/frontmatter.js

function getAllUnits() {
  if (!fs.existsSync(UNITS_DIR)) return [];
  const patches = [];
  for (const skill of fs.readdirSync(UNITS_DIR)) {
    const dir = path.join(UNITS_DIR, skill);
    if (!isDir(dir)) continue;
    for (const f of fs.readdirSync(dir)) {
      if (!f.endsWith('.md') || f === '.gitkeep') continue;
      const content = fs.readFileSync(path.join(dir, f), 'utf8');
      const fm = parseFrontmatter(content);
      patches.push({
        skill, filename: f, content, ...fm,
        evicted: f.includes('.evicted.'),
        superseded: f.includes('.superseded.'),
      });
    }
  }
  return patches;
}

function findUnit(query) {
  const all = getAllUnits().filter(p => !p.evicted && !p.superseded);
  // Exact filename match
  let match = all.find(p => p.filename === query);
  if (match) return match;
  // Partial filename match
  match = all.find(p => p.filename.includes(query));
  if (match) return match;
  // Title match
  match = all.find(p => p.title && p.title.toLowerCase().includes(query.toLowerCase()));
  return match || null;
}

function timeAgo(isoStr) {
  if (!isoStr) return 'never';
  const ms = Date.now() - new Date(isoStr).getTime();
  const h = Math.floor(ms / 3600000);
  if (h < 1) return `${Math.floor(ms / 60000)}m ago`;
  if (h < 24) return `${h}h ago`;
  return `${Math.floor(h / 24)}d ago`;
}

function detectSessionsDir() {
  const ocRoot = path.resolve(__dirname, '..', '..', '..');
  const candidates = [
    path.join(ocRoot, 'agents/main/sessions'),
    path.join(process.env.HOME || '/root', '.openclaw/agents/main/sessions'),
  ];
  for (const d of candidates) { if (fs.existsSync(d)) return d; }
  return null;
}

// ─── Commands ──────────────────────────────────────────────────

function cmdStatus() {
  const state = loadJSON(STATE_PATH);
  const config = loadJSON(CONFIG_PATH);
  const patches = getAllUnits();
  
  const active = patches.filter(p => !p.evicted && !p.superseded);
  const pinned = active.filter(p => p.pinned);
  const evicted = patches.filter(p => p.evicted);
  const exploits = active.filter(p => p.subtype === 'exploit' && !p.pinned);
  const explores = active.filter(p => p.subtype === 'explore' && !p.pinned);
  
  const skills = [...new Set(active.map(p => p.skill))];
  
  const out = {
    mode: config.mode || 'not configured',
    paused: state.paused || false,
    initialized: state.initialized || false,
    active_units: active.length,
    breakdown: {
      pinned: pinned.length,
      exploit: exploits.length,
      explore: explores.length,
    },
    evicted_total: evicted.length,
    skills: skills.length,
    skill_list: skills,
    last_evolution: state.last_evolution_ts || null,
    last_evolution_ago: timeAgo(state.last_evolution_ts),
    last_monitor: state.last_monitor_ts || null,
    pending_si: state.pending_si_count || 0,
    total_evolutions: state.total_evolutions || 0,
    total_si_processed: state.total_si_processed || 0,
    notifications: config.notifications?.mode || 'off',
    model: config.budget?.model || 'auto',
  };
  
  console.log(JSON.stringify(out, null, 2));
}

function cmdUnits(skillFilter) {
  const units = getAllUnits().filter(p => !p.evicted && !p.superseded);
  const filtered = skillFilter ? units.filter(p => p.skill === skillFilter) : units;
  
  if (filtered.length === 0) {
    console.log(JSON.stringify({ units: [], message: skillFilter ? `No active units for ${skillFilter}` : 'No active units' }));
    return;
  }
  
  const out = filtered.map(p => ({
    skill: p.skill,
    filename: p.filename,
    type: p.type,
    subtype: p.subtype,
    title: p.title || '',
    condition: p.condition || '',
    score: p.score || 0,
    track: p.pinned ? 'pinned' : (p.track || 'unknown'),
    evidence_count: p.evidence_count || 0,
    created: p.created || '',
  }));
  
  console.log(JSON.stringify({ units: out }, null, 2));
}

function cmdHistory(limit = 5) {
  // Read evolution-report.json (current) + any archived reports
  const reports = [];
  if (fs.existsSync(REPORT_PATH)) {
    try { reports.push(JSON.parse(fs.readFileSync(REPORT_PATH, 'utf8'))); } catch {}
  }
  
  // Check for archived reports
  const archiveDir = path.join(UNITS_DIR, '.reports');
  if (fs.existsSync(archiveDir)) {
    for (const f of fs.readdirSync(archiveDir).sort().reverse().slice(0, limit)) {
      try { reports.push(JSON.parse(fs.readFileSync(path.join(archiveDir, f), 'utf8'))); } catch {}
    }
  }
  
  console.log(JSON.stringify({ history: reports.slice(0, limit) }, null, 2));
}

function cmdExplain(query) {
  const patch = findUnit(query);
  if (!patch) {
    console.log(JSON.stringify({ error: `Unit not found: ${query}` }));
    process.exit(1);
  }
  
  // Load evidence
  const evidencePath = path.join(UNITS_DIR, patch.skill, patch.filename.replace('.md', '.evidence.jsonl'));
  let evidence = [];
  if (fs.existsSync(evidencePath)) {
    evidence = fs.readFileSync(evidencePath, 'utf8').split('\n').filter(Boolean).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  }
  
  console.log(JSON.stringify({
    filename: patch.filename,
    skill: patch.skill,
    type: patch.type,
    title: patch.title,
    condition: patch.condition,
    score: patch.score,
    track: patch.pinned ? 'pinned' : patch.track,
    created: patch.created,
    source_task: patch.source_task,
    evidence_count: evidence.length,
    evidence,
    content: patch.content,
  }, null, 2));
}

function cmdPin(query) {
  const patch = findUnit(query);
  if (!patch) { console.log(JSON.stringify({ error: `Unit not found: ${query}` })); process.exit(1); }
  
  const filePath = path.join(UNITS_DIR, patch.skill, patch.filename);
  let content = fs.readFileSync(filePath, 'utf8');
  
  if (content.includes('pinned: true')) {
    console.log(JSON.stringify({ result: 'already_pinned', patch: patch.filename }));
    return;
  }
  
  // Add pinned: true to frontmatter
  content = content.replace(/^---\n/, '---\npinned: true\n');
  fs.writeFileSync(filePath, content);
  
  // Write user evidence
  const unitDir = path.dirname(filePath);
  const evidencePath = path.join(unitDir, patch.filename.replace(/\.md$/, '.evidence.jsonl'));
  const entry = { date: new Date().toISOString().slice(0, 10), type: patch.type, verdict: 'user_pin', effect: 1.0, source: 'user', reasoning: 'User pinned this unit' };
  fs.appendFileSync(evidencePath, JSON.stringify(entry) + '\n');
  
  console.log(JSON.stringify({ result: 'pinned', patch: patch.filename, skill: patch.skill }));

  // Emit user pin event
  appendEvent('user.pin', { eu: `${patch.skill}/${patch.filename}` });

  // Emit evidence event for the pin
  appendEvent('evidence.add', {
    eu: `${patch.skill}/${patch.filename}`,
    effect: 1.0,
    outcome: 'user_pin',
    trace_si: null,
    source: 'user',
  });
}

function cmdUnpin(query) {
  const patch = findUnit(query);
  if (!patch) { console.log(JSON.stringify({ error: `Unit not found: ${query}` })); process.exit(1); }
  
  const filePath = path.join(UNITS_DIR, patch.skill, patch.filename);
  let content = fs.readFileSync(filePath, 'utf8');
  content = content.replace(/^pinned: true\n/m, '');
  fs.writeFileSync(filePath, content);
  
  console.log(JSON.stringify({ result: 'unpinned', patch: patch.filename }));

  // Emit user unpin event
  appendEvent('user.unpin', { eu: `${patch.skill}/${patch.filename}` });
}

function cmdEvict(query) {
  const patch = findUnit(query);
  if (!patch) { console.log(JSON.stringify({ error: `Unit not found: ${query}` })); process.exit(1); }
  
  const src = path.join(UNITS_DIR, patch.skill, patch.filename);
  const dest = src.replace('.md', '.evicted.md');
  fs.renameSync(src, dest);
  
  // Write user evidence
  const evidencePath = path.join(UNITS_DIR, patch.skill, patch.filename.replace(/\.md$/, '.evidence.jsonl'));
  const entry = { date: new Date().toISOString().slice(0, 10), type: patch.type, verdict: 'user_evict', effect: -2.0, source: 'user', reasoning: 'User manually evicted' };
  try { fs.appendFileSync(evidencePath, JSON.stringify(entry) + '\n'); } catch {}
  
  console.log(JSON.stringify({ result: 'evicted', patch: patch.filename, skill: patch.skill }));

  // Emit user evict event
  appendEvent('user.evict', { eu: `${patch.skill}/${patch.filename}` });

  // Emit unit.evict event (evolver will also emit this on next run)
  appendEvent('unit.evict', {
    eu: `${patch.skill}/${patch.filename}`,
    reason: 'user_evict',
    track: patch.pinned ? 'pinned' : (patch.track || 'unknown'),
    evidence_count: typeof patch.evidence_count === 'number' ? patch.evidence_count : 0,
    score: typeof patch.score === 'number' ? patch.score : null,
  });
}

function cmdFeedback(query, sentiment) {
  if (!['good', 'bad'].includes(sentiment)) {
    console.log(JSON.stringify({ error: 'Sentiment must be "good" or "bad"' }));
    process.exit(1);
  }
  
  const patch = findUnit(query);
  if (!patch) { console.log(JSON.stringify({ error: `Unit not found: ${query}` })); process.exit(1); }
  
  const unitDir = path.join(UNITS_DIR, patch.skill);
  if (!fs.existsSync(unitDir)) fs.mkdirSync(unitDir, { recursive: true });
  const evidencePath = path.join(unitDir, patch.filename.replace(/\.md$/, '.evidence.jsonl'));
  const effect = sentiment === 'good' ? 1.0 : -1.0;
  const entry = { date: new Date().toISOString().slice(0, 10), type: patch.type, verdict: `user_${sentiment === 'good' ? 'positive' : 'negative'}`, effect, source: 'user', reasoning: `User feedback: ${sentiment}` };
  fs.appendFileSync(evidencePath, JSON.stringify(entry) + '\n');
  
  console.log(JSON.stringify({ result: 'feedback_recorded', patch: patch.filename, sentiment, effect }));

  // Emit user feedback event
  appendEvent('user.feedback', {
    eu: `${patch.skill}/${patch.filename}`,
    sentiment: sentiment,
  });

  // Emit evidence event for the feedback
  appendEvent('evidence.add', {
    eu: `${patch.skill}/${patch.filename}`,
    effect: effect,
    outcome: sentiment === 'good' ? 'user_feedback_positive' : 'user_negative',
    trace_si: null,
    source: 'user',
  });
}

function cmdPause() {
  const state = loadJSON(STATE_PATH);
  state.paused = true;
  saveJSON(STATE_PATH, state);
  console.log(JSON.stringify({ result: 'paused' }));
}

function cmdResume() {
  const state = loadJSON(STATE_PATH);
  state.paused = false;
  saveJSON(STATE_PATH, state);
  console.log(JSON.stringify({ result: 'resumed' }));
}

function cmdConfig(key, value) {
  const config = loadJSON(CONFIG_PATH);
  
  if (!key) {
    console.log(JSON.stringify(config, null, 2));
    return;
  }
  
  if (!value) {
    // Read a specific key (dot-path)
    const parts = key.split('.');
    let obj = config;
    for (const p of parts) { obj = obj?.[p]; }
    console.log(JSON.stringify({ key, value: obj }));
    return;
  }
  
  // Set a value (dot-path)
  const parts = key.split('.');
  let obj = config;
  for (let i = 0; i < parts.length - 1; i++) {
    if (!obj[parts[i]]) obj[parts[i]] = {};
    obj = obj[parts[i]];
  }
  // Auto-parse numbers and booleans
  if (value === 'true') value = true;
  else if (value === 'false') value = false;
  else if (/^\d+$/.test(value)) value = parseInt(value);
  
  obj[parts[parts.length - 1]] = value;
  saveJSON(CONFIG_PATH, config);
  console.log(JSON.stringify({ result: 'updated', key, value }));
}

function cmdReviews(args) {
  const REVIEW_LOG = path.join(EVOLVER_DIR, 'logs', 'review-log.jsonl');
  if (!fs.existsSync(REVIEW_LOG)) {
    console.error('No review log found (no rejections recorded yet).');
    return;
  }

  // Parse flags
  const skillIdx = args.indexOf('--skill');
  const filterSkill = skillIdx >= 0 ? args[skillIdx + 1] : null;
  const limitIdx = args.indexOf('--limit');
  const limit = limitIdx >= 0 ? (parseInt(args[limitIdx + 1]) || 20) : 20;

  const lines = fs.readFileSync(REVIEW_LOG, 'utf8')
    .split('\n').filter(Boolean)
    .map(l => { try { return JSON.parse(l); } catch { return null; } })
    .filter(Boolean)
    .filter(e => !filterSkill || e.skill === filterSkill)
    .reverse()   // newest first
    .slice(0, limit);

  if (lines.length === 0) {
    console.error(filterSkill ? `No rejections for skill: ${filterSkill}` : 'No rejections recorded.');
    return;
  }

  console.error(`\nReview rejections (newest first, showing ${lines.length}):`);
  for (const e of lines) {
    const date = e.ts ? e.ts.slice(0, 10) : '?';
    console.error(`\n  ${date}  [${e.skill}]  ${e.patch}`);
    console.error(`    REJECTED: ${e.reason}`);
  }
  console.error('');
}

function cmdCheck() {
  const result = { llm: {}, sessions: {}, units: {} };
  
  // LLM check
  try {
    const { createLLMClient } = require('./lib/llm-client');
    const llm = createLLMClient();
    result.llm = { mode: llm.mode, model: llm.model, available: true };
  } catch (e) {
    result.llm = { available: false, error: e.message };
  }
  
  // Sessions check
  const sessDir = detectSessionsDir();
  if (sessDir) {
    const files = fs.readdirSync(sessDir).filter(f => f.endsWith('.jsonl'));
    result.sessions = { dir: sessDir, count: files.length, available: true };
  } else {
    result.sessions = { available: false };
  }
  
  // Units check
  result.units = {
    dir: UNITS_DIR,
    writable: (() => { try { fs.accessSync(UNITS_DIR, fs.constants.W_OK); return true; } catch { return false; } })(),
    active: getAllUnits().filter(p => !p.evicted && !p.superseded).length,
  };
  
  console.log(JSON.stringify(result, null, 2));
}

// ─── Clear / Block (user control over EU deployment) ───────────────

const INLINE_START = '<!-- SKILL-EVOLVER:PATCHES-START -->';
const INLINE_END   = '<!-- SKILL-EVOLVER:PATCHES-END -->';

/** Reject skill names that could traverse outside the skills root. */
function isSafeSkillName(skill) {
  return typeof skill === 'string'
    && skill.length > 0
    && !skill.includes('..')
    && !skill.includes('/')
    && !skill.includes('\\')
    && !skill.startsWith('.');
}

/** Resolve SKILL.md path(s) for a skill via the platform adapter's search paths. */
function findSkillMdPaths(skill) {
  const out = [];
  if (!isSafeSkillName(skill)) return out; // boundary guard (path traversal)
  try {
    const { getAdapter } = require('./lib/platform-detect');
    const adapter = getAdapter();
    const bases = (typeof adapter.getSkillSearchPaths === 'function' ? adapter.getSkillSearchPaths() : []) || [];
    for (const base of bases) {
      const p = path.join(base, skill, 'SKILL.md');
      if (fs.existsSync(p)) out.push(p);
    }
  } catch { /* fall through */ }
  return out;
}

/** Strip the evolver PATCHES block from a SKILL.md. Returns 'removed' | 'absent'. */
function stripInlineBlock(smdPath) {
  let content = fs.readFileSync(smdPath, 'utf8');
  if (!content.includes(INLINE_START)) return 'absent';
  const re = new RegExp(
    INLINE_START.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '[\\s\\S]*?' +
    INLINE_END.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\n?',
    'm'
  );
  const next = content.replace(re, '').replace(/\n{3,}/g, '\n\n');
  if (next === content) return 'absent';
  fs.writeFileSync(smdPath, next, 'utf8');
  return 'removed';
}

/**
 * clear <skill> | --all
 * Detach (un-inline) a skill's EUs from its live SKILL.md WITHOUT deleting them.
 * EU files stay archived on disk; this only removes the attached block.
 * Note: a plain clear is re-attached on the next evolution run unless the skill
 * is also blocked. Use `clear <skill> --block` (or `block <skill>`) to keep it off.
 */
function cmdClear(args) {
  const all = args.includes('--all');
  const alsoBlock = args.includes('--block');
  const targets = [];

  if (all) {
    if (fs.existsSync(UNITS_DIR)) {
      for (const s of fs.readdirSync(UNITS_DIR)) {
        if (isDir(path.join(UNITS_DIR, s))) targets.push(s);
      }
    }
  } else {
    const skill = args.find(a => !a.startsWith('--'));
    if (!skill) { console.log(JSON.stringify({ error: 'Usage: clear <skill> [--block] | clear --all [--block]' })); process.exit(1); }
    targets.push(skill);
  }

  const cleared = [];
  for (const skill of targets) {
    const mds = findSkillMdPaths(skill);
    let removedAny = false;
    for (const smd of mds) {
      if (smd.includes('/extensions/')) continue; // bundled, auto-restored
      if (stripInlineBlock(smd) === 'removed') removedAny = true;
    }
    if (removedAny) {
      cleared.push(skill);
      appendEvent('user.clear', { skill, archived: true });
    }
    if (alsoBlock) blockSkill(skill);
  }

  console.log(JSON.stringify({
    result: 'cleared',
    skills: cleared,
    note: 'EUs archived (not deleted). ' + (alsoBlock
      ? 'Skills also blocked from future evolution.'
      : 'Run `block <skill>` to prevent re-attachment on the next evolution.'),
    blocked: alsoBlock ? targets : [],
  }, null, 2));
}

/** block <skill> — exclude a skill from future evolution + detach existing EUs. */
function cmdBlock(skill) {
  if (!skill) { console.log(JSON.stringify({ error: 'Usage: block <skill>' })); process.exit(1); }
  if (!isSafeSkillName(skill)) { console.log(JSON.stringify({ error: `Invalid skill name: ${skill}` })); process.exit(1); }
  const list = blockSkill(skill);
  // Also detach now so the effect is immediate (don't wait for next run).
  for (const smd of findSkillMdPaths(skill)) {
    if (smd.includes('/extensions/')) continue;
    stripInlineBlock(smd);
  }
  appendEvent('user.block', { skill });
  console.log(JSON.stringify({ result: 'blocked', skill, blockedSkills: list }, null, 2));
}

/** unblock <skill> — allow a skill to evolve again (re-attached on next run). */
function cmdUnblock(skill) {
  if (!skill) { console.log(JSON.stringify({ error: 'Usage: unblock <skill>' })); process.exit(1); }
  if (!isSafeSkillName(skill)) { console.log(JSON.stringify({ error: `Invalid skill name: ${skill}` })); process.exit(1); }
  const list = unblockSkill(skill);
  appendEvent('user.unblock', { skill });
  console.log(JSON.stringify({
    result: 'unblocked', skill, blockedSkills: list,
    note: 'Archived EUs will be re-evaluated and re-attached on the next evolution run.',
  }, null, 2));
}

/** blocklist — show currently blocked skills. */
function cmdBlocklist() {
  console.log(JSON.stringify({ blockedSkills: [...getBlockedSkills()].sort() }, null, 2));
}

// ─── Main ──────────────────────────────────────────────────────

const [cmd, ...rest] = process.argv.slice(2);

switch (cmd) {
  case 'status':   cmdStatus(); break;
  case 'units':    cmdUnits(rest[0]); break;
  case 'patches':  cmdUnits(rest[0]); break;  // deprecated alias (v2.4.0) — keep one cycle
  case 'history':  cmdHistory(rest.includes('--limit') ? parseInt(rest[rest.indexOf('--limit') + 1]) : 5); break;
  case 'explain':  cmdExplain(rest[0]); break;
  case 'pin':      cmdPin(rest[0]); break;
  case 'unpin':    cmdUnpin(rest[0]); break;
  case 'evict':    cmdEvict(rest[0]); break;
  case 'feedback': cmdFeedback(rest[0], rest[1]); break;
  case 'pause':    cmdPause(); break;
  case 'resume':   cmdResume(); break;
  case 'config':   cmdConfig(rest[0], rest[1]); break;
  case 'check':    cmdCheck(); break;
  case 'reviews':  cmdReviews(rest); break;
  case 'clear':    cmdClear(rest); break;
  case 'block':    cmdBlock(rest[0]); break;
  case 'unblock':  cmdUnblock(rest[0]); break;
  case 'blocklist': cmdBlocklist(); break;
  default:
    console.error(`Usage: node evolver-cli.js <command> [args]
Commands: status, units [skill], patches (deprecated), history, explain <unit>, pin <unit>,
          unpin <unit>, evict <unit>, feedback <unit> good|bad,
          pause, resume, config [key] [value], check,
          reviews [--skill <name>] [--limit N],
          clear <skill>|--all [--block], block <skill>, unblock <skill>, blocklist`);
    process.exit(1);
}
