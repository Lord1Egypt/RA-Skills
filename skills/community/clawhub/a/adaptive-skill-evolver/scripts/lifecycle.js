#!/usr/bin/env node
/**
 * lifecycle.js — v2.0 Daily Mode
 *
 * Unit lifecycle management: scoring, nursery, promotion, eviction.
 * Design: §10.8 (Lifecycle) + §3.5 (dual-track + Nursery)
 *
 * Pure code — no LLM calls. Reads evidence.jsonl + units dir, manages lifecycle.
 *
 * Pipeline:
 *   1. EVICT: remove degraded units (2nd negative → archive)
 *   2. SCORE: compute coverage + effect + efficiency for each unit
 *   3. SELECT: fill regular slots (3 exploit + 3 explore) + nursery (2 slots)
 *   4. DEGRADE: first negative → write sep-queue for generator supersede
 *   5. WRITE-BACK: update unit frontmatter + inline active units into SKILL.md
 *
 * Usage:
 *   node lifecycle.js --eu-dir <dir> --evidence <evidence.jsonl> --traces <traces.jsonl> [--sep-queue <path>] [--window-days 14]
 *
 * Output: updated units dir (promotions, evictions), sep-queue entries
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { parseFrontmatter, CURRENT_SCHEMA_VERSION } = require('./lib/frontmatter');
const { appendEvent } = require('./lib/events');
const { isActiveUnitFile, ensureUnitsDir } = require('./lib/unit-files');
const { getBlockedSkills } = require('./lib/blocklist');

function isDir(p) { try { return fs.statSync(p).isDirectory(); } catch { return false; } }

// ─── Configuration ─────────────────────────────────────────────

const REGULAR_EXPLOIT_SLOTS = 3;
const REGULAR_EXPLORE_SLOTS = 3;
const NURSERY_SLOTS = 2;
// Score governs deployment eligibility. score = coverage[0,0.3] + effect[-1,1] + efficiency.
// Two distinct cutoffs:
//   - PROMOTE_SCORE_FLOOR (> 0): a unit must prove net-positive value to be promoted
//     into a deployed regular slot.
//   - HARMFUL_SCORE_CEIL (< 0): a unit with net-negative aggregate evidence is proven
//     harmful; it must never be inlined (not even as an "under evaluation" nursery unit)
//     and is dropped to the waiting queue so DEGRADE/supersede can act on it.
// score == 0 means "unproven" (brand-new, no evidence) and still earns a nursery trial.
const PROMOTE_SCORE_FLOOR = 0;
const HARMFUL_SCORE_CEIL  = 0;
const NURSERY_TTL_DAYS = 14;      // daily mode: 14 days
const EFFICIENCY_HISTORY_DAYS = 30;
const MIN_EFFICIENCY_SAMPLES = 3;

// ─── Unit Loading ─────────────────────────────────────────────

// parseFrontmatter lives in ./lib/frontmatter.js

function loadAllPatches(unitsDir) {
  if (!fs.existsSync(unitsDir)) return [];

  const patches = [];
  for (const skill of fs.readdirSync(unitsDir)) {
    const skillDir = path.join(unitsDir, skill);
    if (!isDir(skillDir)) continue;

    for (const filename of fs.readdirSync(skillDir)) {
      if (!isActiveUnitFile(filename)) continue;

      const content = fs.readFileSync(path.join(skillDir, filename), 'utf8');
      const fm = parseFrontmatter(content);

      // Belt-and-suspenders: a unit may carry review_status:rejected in frontmatter
      // even if the .rejected.md rename failed. Never load/render rejected units.
      if (fm.review_status === 'rejected') continue;

      patches.push({
        skill,
        filename,
        content,
        type: fm.type || 'adaptive',
        subtype: fm.subtype || 'exploit',
        title: fm.title || filename,
        condition: fm.condition || '',
        condition_keywords: Array.isArray(fm.condition_keywords) ? fm.condition_keywords : [],
        created: fm.created || '',
        source_task: fm.source_task || '',
        supersedes: fm.supersedes || null,
        pinned: fm.pinned === true || fm.pinned === 'true',
        _status: fm.status || 'active',
        _inlined: fm.inlined === true || fm.inlined === 'true',
        // State tracking (will be computed)
        evidence: [],
        score: 0,
        track: 'pending', // 'regular', 'nursery', 'waiting', 'pending'
      });
    }
  }

  return patches;
}

// ─── Evidence Loading ──────────────────────────────────────────

function loadEvidence(evidencePath) {
  if (!fs.existsSync(evidencePath)) return [];

  return fs.readFileSync(evidencePath, 'utf8')
    .split('\n')
    .filter(Boolean)
    .map(line => {
      try { return JSON.parse(line); } catch { return null; }
    })
    .filter(Boolean);
}

// ─── Trace Loading (for keyword coverage) ──────────────────────

function loadTraces(tracesPath) {
  if (!fs.existsSync(tracesPath)) return [];

  return fs.readFileSync(tracesPath, 'utf8')
    .split('\n')
    .filter(Boolean)
    .map(line => {
      try { return JSON.parse(line); } catch { return null; }
    })
    .filter(Boolean);
}

// ─── Scoring ───────────────────────────────────────────────────

/**
 * Keyword coverage: fraction of skill traces containing any condition keyword.
 * Returns [0, 1] (raw), caller applies × 0.3 for nursery.
 */
function computeKeywordCoverage(patch, skillTraces) {
  if (skillTraces.length === 0 || patch.condition_keywords.length === 0) return 0;

  const keywords = patch.condition_keywords.map(k =>
    typeof k === 'string' ? k.toLowerCase() : ''
  ).filter(Boolean);

  if (keywords.length === 0) return 0;

  let hits = 0;
  for (const trace of skillTraces) {
    const text = (trace.trace || '').toLowerCase();
    if (keywords.some(kw => text.includes(kw))) {
      hits++;
    }
  }

  return hits / skillTraces.length;
}

/**
 * Evidence-based effect: mean of all evidence effect values.
 * Inherited evidence (from superseded patches) gets 50% weight discount (§v1.4.1).
 */
function computeMeanEffect(evidenceEntries) {
  if (evidenceEntries.length === 0) return 0;
  let weightedSum = 0;
  let totalWeight = 0;
  for (const e of evidenceEntries) {
    const weight = e.inherited_from ? 0.5 : 1.0;
    weightedSum += (e.effect || 0) * weight;
    totalWeight += weight;
  }
  return totalWeight > 0 ? weightedSum / totalWeight : 0;
}

/**
 * Efficiency: step delta vs historical median (daily mode).
 * Returns [-0.25, +0.25] (already × 0.5).
 */
function computeEfficiency(patch, allTraces) {
  // Get step-count samples for this skill (current + historical merged in main()).
  const skillTraces = allTraces.filter(t => t.skill === patch.skill);
  if (skillTraces.length < MIN_EFFICIENCY_SAMPLES) return 0;

  const steps = skillTraces.map(t => t.trace_steps || 0).sort((a, b) => a - b);
  const median = steps[Math.floor(steps.length / 2)];

  // Get steps from traces where this patch had evidence
  const unitTraceIds = new Set(patch.evidence.map(e => e.si_id || e.task_id));
  const unitTraces = skillTraces.filter(t => unitTraceIds.has(t.si_id));

  if (unitTraces.length === 0) return 0;

  const unitSteps = unitTraces.map(t => t.trace_steps || 0);
  const avgPatchSteps = unitSteps.reduce((s, v) => s + v, 0) / unitSteps.length;

  const raw = (median - avgPatchSteps) / Math.max(median, 1);
  return clamp(raw, -0.5, 0.5) * 0.5;
}

function clamp(val, min, max) {
  return Math.min(Math.max(val, min), max);
}

/**
 * Compute unified score (daily mode).
 * score = coverage + effect + efficiency × 0.5
 *
 * Coverage: keyword_coverage × 0.3 for ALL tracks (daily mode).
 * Daily has no bench-style trigger_rate — keyword soft-matching only.
 * Coverage value range: [0, 0.3], so effect [-1, 1] is the dominant dimension.
 *
 * The difference between regular and nursery is evidence:
 *   Nursery (no evidence): score ≈ keyword_coverage × 0.3 (max 0.3)
 *   Regular (has evidence): score ≈ keyword_coverage × 0.3 + effect (effect dominates)
 */
function computeScore(patch, skillTraces, allTraces) {
  const coverage = computeKeywordCoverage(patch, skillTraces) * 0.3;

  const effect = computeMeanEffect(patch.evidence);
  const efficiency = computeEfficiency(patch, allTraces);

  patch._coverage = coverage;
  patch._effect = effect;
  patch._efficiency = efficiency;

  return coverage + effect + efficiency;
}

// ─── Nursery TTL ───────────────────────────────────────────────

function isNurseryExpired(patch, windowDays) {
  if (!patch.created) return false;
  const created = new Date(patch.created);
  const now = new Date();
  const diffDays = (now - created) / (1000 * 60 * 60 * 24);
  return diffDays > windowDays;
}

// ─── Eviction ──────────────────────────────────────────────────

function countNegativeEvidence(patch) {
  // Count ALL negative evidence (including inherited) for eviction.
  // Rationale: if an ancestor patch was degraded and this supersede still
  // hits negative, give up — the condition has had its shot at improvement.
  // Ancestors can have at most 1 negative (2nd would evict directly, not supersede),
  // so a fresh supersede patch starts with negCount=1 and dies on its first native negative.
  // Score still discounts inherited via computeMeanEffect (50% weight in L165).
  return patch.evidence.filter(e => (e.effect || 0) < 0).length;
}

// ─── Sep-Queue ─────────────────────────────────────────────────

function writeSepQueueEntry(sepQueuePath, entry) {
  fs.appendFileSync(sepQueuePath, JSON.stringify(entry) + '\n');
}

// ─── File Operations ───────────────────────────────────────────

function evictPatch(unitsDir, skill, filename, reason) {
  const src = path.join(unitsDir, skill, filename);
  const dest = src.replace('.md', '.evicted.md');
  if (fs.existsSync(src)) {
    // Update status in frontmatter before renaming
    let fc = fs.readFileSync(src, 'utf8');
    if (fc.match(/^status:.*$/m)) {
      fc = fc.replace(/^status:.*$/m, 'status: evicted');
    } else {
      fc = fc.replace(/\n---\n/, '\nstatus: evicted\n---\n');
    }
    fs.writeFileSync(src, fc, 'utf8');
    fs.renameSync(src, dest);
    console.error(`  [evict] ${filename} → evicted (${reason})`);

    return true;
  }
  return false;
}

// ─── Frontmatter Write-back ────────────────────────────────────

/**
 * Update patch file frontmatter with computed metadata.
 * Only writes if something actually changed.
 */
function writeFrontmatter(unitsDir, patch) {
  const filePath = path.join(unitsDir, patch.skill, patch.filename);
  if (!fs.existsSync(filePath)) return;

  let content = fs.readFileSync(filePath, 'utf8');
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) return;

  const track = patch.pinned ? 'pinned' : (patch.track === 'regular' ? 'regular' : (patch._isNursery ? 'nursery' : 'regular'));
  const inheritedCount = patch.evidence.filter(e => e.inherited_from).length;
  const updates = {
    schema: CURRENT_SCHEMA_VERSION,
    score: parseFloat(patch.score.toFixed(4)),
    track,
    status: patch._status || 'active',
    inlined: patch._inlined || false,
    evidence_count: patch.evidence.length,
    inherited_evidence: inheritedCount > 0 ? inheritedCount : undefined,
    last_evidence: patch.evidence.length > 0
      ? patch.evidence[patch.evidence.length - 1].date || ''
      : '',
  };

  let fmBlock = fmMatch[1];
  let changed = false;

  for (const [key, val] of Object.entries(updates)) {
    if (val === '' || val === undefined) continue;
    const lineRe = new RegExp(`^${key}:.*$`, 'm');
    const newLine = `${key}: ${typeof val === 'string' ? `"${val}"` : val}`;

    if (lineRe.test(fmBlock)) {
      const oldLine = fmBlock.match(lineRe)[0];
      if (oldLine !== newLine) {
        fmBlock = fmBlock.replace(lineRe, newLine);
        changed = true;
      }
    } else {
      fmBlock += '\n' + newLine;
      changed = true;
    }
  }

  if (changed) {
    content = content.replace(/^---\n[\s\S]*?\n---/, `---\n${fmBlock}\n---`);
    fs.writeFileSync(filePath, content, 'utf8');
  }
}

// ─── SKILL.md Inline ───────────────────────────────────────────

const INLINE_START = '<!-- SKILL-EVOLVER:PATCHES-START -->';
const INLINE_END = '<!-- SKILL-EVOLVER:PATCHES-END -->';

// Dynamically resolve OpenClaw installation root (works across nvm versions and install methods)
function resolveOpenClawRoot() {
  try {
    // Method 1: find `openclaw` in PATH (pure JS, no child_process)
    const dirs = (process.env.PATH || '').split(path.delimiter);
    for (const dir of dirs) {
      const full = path.join(dir, 'openclaw');
      try { fs.accessSync(full, fs.constants.X_OK); } catch { continue; }
      const real = fs.realpathSync(full);
      const parts = real.split(path.sep);
      const nmIdx = parts.lastIndexOf('node_modules');
      if (nmIdx >= 0) return parts.slice(0, nmIdx + 2).join(path.sep);
    }
  } catch { /* fallback */ }
  try {
    // Method 2: derive from process.execPath (node binary → global node_modules)
    const candidate = path.resolve(path.dirname(process.execPath), '..', 'lib', 'node_modules', 'openclaw');
    if (fs.existsSync(candidate)) return candidate;
  } catch { /* fallback */ }
  return null;
}

const _ocRoot = resolveOpenClawRoot();

const SKILL_SEARCH_PATHS_STATIC = [
  // Primary: derive from lifecycle's own location (scripts/ → skill-evolver/ → skills/)
  path.resolve(__dirname, '..', '..'),
  path.join(process.env.HOME || '/root', '.openclaw', 'skills'),
  // Bundled skills from OpenClaw install
  ...(_ocRoot ? [
    path.join(_ocRoot, 'skills'),
    path.join(_ocRoot, 'skills', 'others'),
    path.join(_ocRoot, 'skills', 'tencent'),
  ] : []),
].filter(p => fs.existsSync(p));

// Auto-discover skill directories under extensions (covers wecom-openclaw-plugin, acpx, diffs, etc.)
function discoverExtensionSkillPaths() {
  const extRoot = _ocRoot ? path.join(_ocRoot, 'extensions') : null;
  if (!extRoot) return [];
  const paths = [];
  try {
    if (!fs.existsSync(extRoot)) return paths;
    const walk = (dir, depth) => {
      if (depth > 3) return; // Don't go too deep
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        if (!entry.isDirectory()) continue;
        if (entry.name === 'node_modules') continue;
        const full = path.join(dir, entry.name);
        if (entry.name === 'skills') {
          paths.push(full);
        } else {
          walk(full, depth + 1);
        }
      }
    };
    walk(extRoot, 0);
  } catch { /* ignore permission errors */ }
  return paths;
}

let _cachedSearchPaths = null;
function getSkillSearchPaths() {
  if (_cachedSearchPaths) return _cachedSearchPaths;
  // Cross-platform: use adapter's skill search paths if available
  try {
    const { getAdapter } = require('./lib/platform-detect');
    const adapter = getAdapter();
    if (typeof adapter.getSkillSearchPaths === 'function') {
      const adapterPaths = adapter.getSkillSearchPaths().filter(p => fs.existsSync(p));
      if (adapterPaths.length > 0) {
        _cachedSearchPaths = [...adapterPaths, ...SKILL_SEARCH_PATHS_STATIC.filter(p => !adapterPaths.includes(p)), ...discoverExtensionSkillPaths()];
        return _cachedSearchPaths;
      }
    }
  } catch { /* fallback to static */ }
  _cachedSearchPaths = [...SKILL_SEARCH_PATHS_STATIC, ...discoverExtensionSkillPaths()];
  return _cachedSearchPaths;
}

function findSkillMds(skillName) {
  const results = [];
  for (const base of getSkillSearchPaths()) {
    const p = path.join(base, skillName, 'SKILL.md');
    if (fs.existsSync(p)) results.push(p);
  }
  return results;
}

/**
 * Render inline block from active patches for a skill.
 */
function renderInlineBlock(patches) {
  if (patches.length === 0) return null;

  const lines = [
    INLINE_START,
    '',
    '## Experience Patches (auto-generated by skill-evolver)',
    '',
    '> Experience from past executions — passively triggered references, not an execution plan.',
    '> - **EXPLOIT (proven strategy)**: When you encounter the condition during execution, apply this strategy. If you do not encounter the condition, ignore it.',
    '> - **EXPLORE (ineffective path)**: Marks a known dead end. When you find yourself heading toward this path, stop immediately and change direction.',
    '',
  ];

  // Pinned first, then regular, then nursery
  const pinned = patches.filter(p => p.pinned);
  const regular = patches.filter(p => !p.pinned && (p.track === 'regular' || !p._isNursery));
  const nursery = patches.filter(p => !p.pinned && p._isNursery && p.track !== 'regular');

  for (const p of [...pinned, ...regular, ...nursery]) {
    const icon = p.subtype === 'exploit' ? 'EXPLOIT' : 'EXPLORE';
    const isNursery = !p.pinned && p._isNursery && p.track !== 'regular';
    const isPinned = p.pinned;

    let label, scoreLine;
    if (isPinned) {
      label = `📌 ${p.title}`;
      scoreLine = `(pinned by user)`;
    } else if (isNursery) {
      label = `🆕 [NURSERY] ${p.title}`;
      scoreLine = `(prior: ${p.score.toFixed(2)})`;
    } else {
      label = p.title;
      scoreLine = `(score: ${p.score.toFixed(2)})`;
    }

    lines.push(`### [${icon}] ${label} ${scoreLine}`);

    if (isPinned) {
      lines.push(`> 📌 PINNED by user · ${p.evidence.length} evidence`);
    } else if (isNursery) {
      lines.push(`> NEW — under evaluation`);
    } else {
      const typeLabel = p.subtype === 'exploit' ? 'proven strategy' : 'ineffective path';
      lines.push(`> ${p.subtype.toUpperCase()} (${typeLabel}) · verified ${p.evidence.length}×`);
    }
    lines.push('');

    // Extract sections from patch content (skip frontmatter)
    const body = p.content.replace(/^---\n[\s\S]*?\n---\n*/, '').trim();
    // Demote ## to #### for inline context
    const demoted = body.replace(/^## /gm, '#### ');
    lines.push(demoted);
    lines.push('');
  }

  lines.push(INLINE_END);
  return lines.join('\n');
}

/**
 * Write inline block into SKILL.md. Idempotent — no write if unchanged.
 * Returns 'inlined' | 'unchanged' | 'appended'
 */
function inlineIntoSkillMd(skillMdPath, inlineBlock) {
  // Security: validate path targets a SKILL.md file and doesn't traverse outside skill dirs
  const resolved = path.resolve(skillMdPath);
  if (!resolved.endsWith(path.sep + 'SKILL.md')) {
    throw new Error(`Path boundary violation: ${resolved} is not a SKILL.md file`);
  }
  // Block path traversal attempts (e.g., skill named "../../etc")
  const dirName = path.basename(path.dirname(resolved));
  if (dirName.includes('..') || dirName.startsWith('.')) {
    throw new Error(`Path boundary violation: suspicious skill dir name "${dirName}"`);
  }

  let content = fs.readFileSync(skillMdPath, 'utf8');

  if (content.includes(INLINE_START)) {
    // Replace existing block
    const re = new RegExp(
      INLINE_START.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') +
      '[\\s\\S]*?' +
      INLINE_END.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'),
      'm'
    );
    const newContent = content.replace(re, inlineBlock);
    if (newContent === content) return 'unchanged';

    // Post-write line count check
    const lineCount = newContent.split('\n').length;
    if (lineCount > 500) {
      console.error(`  [inline] ⚠️  ${skillMdPath}: ${lineCount} lines (>500) — may impact agent context window`);
    }

    fs.writeFileSync(skillMdPath, newContent, 'utf8');
    return 'inlined';
  } else {
    // Append — protect frontmatter by inserting after it
    if (!content.endsWith('\n')) content += '\n';

    // Detect and preserve frontmatter (--- ... ---)
    // Insert inline block at the END of file, never inside frontmatter
    const fmMatch = content.match(/^---\n[\\s\\S]*?\n---\n/);
    if (fmMatch && fmMatch.index === 0) {
      // Frontmatter exists — append after entire content (safe)
      content += '\n---\n\n' + inlineBlock + '\n';
    } else {
      // No frontmatter — append normally
      content += '\n---\n\n' + inlineBlock + '\n';
    }

    // Post-write line count check
    const lineCount = content.split('\n').length;
    if (lineCount > 500) {
      console.error(`  [inline] ⚠️  ${skillMdPath}: ${lineCount} lines (>500) — may impact agent context window`);
    }

    fs.writeFileSync(skillMdPath, content, 'utf8');
    return 'appended';
  }
}

/**
 * Remove inline block from SKILL.md (when all patches evicted).
 * Returns 'removed' | 'not_found'
 */
function removeInlineFromSkillMd(skillMdPath) {
  // Security: same boundary check as inlineIntoSkillMd
  const resolved = path.resolve(skillMdPath);
  if (!resolved.endsWith(path.sep + 'SKILL.md')) {
    throw new Error(`Path boundary violation: ${resolved} is not a SKILL.md file`);
  }
  let content = fs.readFileSync(skillMdPath, 'utf8');
  if (!content.includes(INLINE_START)) return 'not_found';

  const re = new RegExp(
    '\n*---\n*\n*' +
    INLINE_START.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') +
    '[\\s\\S]*?' +
    INLINE_END.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') +
    '\n*',
    'm'
  );
  const newContent = content.replace(re, '\n');
  if (newContent === content) return 'not_found';
  fs.writeFileSync(skillMdPath, newContent, 'utf8');
  return 'removed';
}

// ─── Main ──────────────────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);

  let unitsDir = null;
  let evidencePath = null;
  let tracesPath = null;
  let tracesHistoryPath = null;
  let sepQueuePath = null;
  let windowDays = NURSERY_TTL_DAYS;

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--eu-dir':
      case '--patches-dir':    unitsDir = args[++i]; break;
      case '--evidence':       evidencePath = args[++i]; break;
      case '--traces':         tracesPath = args[++i]; break;
      case '--traces-history': tracesHistoryPath = args[++i]; break;
      case '--sep-queue':      sepQueuePath = args[++i]; break;
      case '--window-days':    windowDays = parseInt(args[++i]); break;
    }
  }

  if (!unitsDir || !evidencePath) {
    console.error('Usage: node lifecycle.js --eu-dir <dir> --evidence <evidence.jsonl> --traces <traces.jsonl> [--traces-history <path>] [--sep-queue <path>] [--window-days 14]');
    process.exit(1);
  }

  // Units root may be absent on a fresh clone (open-source platforms drop empty
  // dirs); ensure it exists before any read/write-back.
  ensureUnitsDir(unitsDir);

  // Load data
  const allUnits = loadAllPatches(unitsDir);
  const evidence = loadEvidence(evidencePath);
  const currentTraces = tracesPath ? loadTraces(tracesPath) : [];
  const historicalTraces = tracesHistoryPath ? loadTraces(tracesHistoryPath) : [];
  // Current traces carry full fields (used for keyword coverage).
  // Historical traces are lightweight (si_id/skill/trace_steps/ts) for efficiency stats.
  // De-dup by si_id so the same SI doesn't count twice.
  const seenIds = new Set(currentTraces.map(t => t.si_id));
  const allTraces = [...currentTraces, ...historicalTraces.filter(t => !seenIds.has(t.si_id))];

  // Reset all inlined flags (inlined is a per-run snapshot, not persistent)
  for (const patch of allUnits) {
    patch._inlined = false;
  }

  console.error(`[lifecycle] ${allUnits.length} patches, ${evidence.length} evidence entries, ${currentTraces.length} current + ${allTraces.length - currentTraces.length} history traces`);

  // Assign evidence to patches
  // Double-read unit_file || patch_file: legacy evidence.jsonl entries from
  // before v2.4.0 used patch_file.
  for (const entry of evidence) {
    const entryFile = entry.unit_file || entry.patch_file;
    const patch = allUnits.find(p =>
      p.filename === entryFile && p.skill === entry.skill
    );
    if (patch) {
      patch.evidence.push(entry);
    }
  }

  // Group patches by skill
  const skills = [...new Set(allUnits.map(p => p.skill))];

  // Stats
  let evictCount = 0, promoteCount = 0, degradeCount = 0;
  const report = [];
  const selectedBySkill = new Map(); // skill → Set<filename> of patches selected for SKILL.md

  for (const skill of skills) {
    console.error(`\n[lifecycle] Skill: ${skill}`);

    let skillPatches = allUnits.filter(p => p.skill === skill);
    const skillTraces = allTraces.filter(t => t.skill === skill);

    // ─── Step 1: EVICT ───────────────────────────

    const toEvict = [];
    for (const patch of skillPatches) {
      if (patch.pinned) continue; // Pinned patches are never evicted

      // User explicit rejection → immediate eviction (strongest signal).
      // A single user_negative evidence evicts the patch: the user themselves
      // has rejected what the patch prescribes.
      // Exclude inherited: user_negative is bound to a specific patch's wording
      // (what the user actually saw and rejected), not to the condition itself.
      // A supersede rewrites the patch — the new wording deserves its own chance.
      // This differs from native negatives (countNegativeEvidence), which track
      // condition-level failure and DO carry across supersede.
      const hasUserNegative = (patch.evidence || []).some(e =>
        !e.inherited_from && (
          e.attribution?.outcome === 'user_negative' ||
          e.attribution?.alternative_outcome === 'user_negative'
        )
      );
      if (hasUserNegative) {
        toEvict.push({ patch, reason: 'user explicitly rejected' });
        continue;
      }

      const negCount = countNegativeEvidence(patch);

      // 2nd negative → evict
      // Note: superseded patches are renamed to *.superseded.md and filtered out by
      // loadAllPatches (see L72), so they never appear in skillPatches here.
      // No separate "superseded + negative" branch needed.
      if (negCount >= 2) {
        toEvict.push({ patch, reason: `${negCount} negative evidence` });
      }

      // Nursery TTL expired
      if (patch.evidence.length === 0 && isNurseryExpired(patch, windowDays)) {
        toEvict.push({ patch, reason: `nursery TTL expired (${windowDays}d)` });
      }
    }

    for (const { patch, reason } of toEvict) {
      if (evictPatch(unitsDir, skill, patch.filename, reason)) {
        evictCount++;
        // Emit eviction event with full patch context
        appendEvent('unit.evict', {
          eu: `${skill}/${patch.filename}`,
          reason,
          track: patch.track || (patch._isNursery ? 'nursery' : 'regular'),
          evidence_count: patch.evidence ? patch.evidence.length : 0,
          score: typeof patch.score === 'number' ? patch.score : null,
        });
        skillPatches = skillPatches.filter(p => p !== patch);
      }
    }

    // ─── Step 2: SCORE ───────────────────────────

    for (const patch of skillPatches) {
      const hasPositiveEvidence = patch.evidence.some(e => (e.effect || 0) > 0);
      const isNursery = !hasPositiveEvidence; // no positive evidence → nursery
      patch.score = computeScore(patch, skillTraces, allTraces);
      patch._isNursery = isNursery;
    }

    // ─── Step 3: SELECT (fill slots) ─────────────

    // Pinned patches: always active, don't compete for slots
    const pinnedPatches = skillPatches.filter(p => p.pinned);
    const unpinnedPatches = skillPatches.filter(p => !p.pinned);

    const exploits = unpinnedPatches.filter(p => p.subtype === 'exploit').sort((a, b) => b.score - a.score);
    const explores = unpinnedPatches.filter(p => p.subtype === 'explore').sort((a, b) => b.score - a.score);

    // Regular slots: top N with positive evidence AND net-positive score.
    // Score floor guards the case where a unit has *some* positive evidence
    // (so !_isNursery) but its aggregate score went net-negative (effect/efficiency
    // drag). Such a unit must not occupy a deployed slot — it falls back to nursery
    // so the DEGRADE/supersede machinery can act on it instead of being inlined.
    for (const p of [...exploits, ...explores]) {
      if (!p._isNursery && p.score < HARMFUL_SCORE_CEIL) {
        p._isNursery = true;
        console.error(`  [demote] ${p.filename} (${p.score.toFixed(3)}) < ${HARMFUL_SCORE_CEIL} — net-negative, removed from regular track`);
      }
    }
    const regularExploits = exploits.filter(p => !p._isNursery).slice(0, REGULAR_EXPLOIT_SLOTS);
    const regularExplores = explores.filter(p => !p._isNursery).slice(0, REGULAR_EXPLORE_SLOTS);

    // Nursery slots: top K from remaining unpinned. Proven-harmful units (score < ceil)
    // are excluded entirely — they drop to the waiting queue and are NOT inlined, since a
    // negative-score unit is not "unproven", it is demonstrated net-harmful.
    const nurseryPool = unpinnedPatches
      .filter(p => p._isNursery && p.score >= HARMFUL_SCORE_CEIL)
      .sort((a, b) => b.score - a.score);
    const harmfulWaiting = unpinnedPatches.filter(p => p._isNursery && p.score < HARMFUL_SCORE_CEIL);
    if (harmfulWaiting.length) {
      for (const p of harmfulWaiting) console.error(`  [suppress] ${p.filename} (${p.score.toFixed(3)}) < ${HARMFUL_SCORE_CEIL} — net-harmful, not inlined`);
    }
    const nurseryPatches = nurseryPool.slice(0, NURSERY_SLOTS);
    const waitingQueue = nurseryPool.slice(NURSERY_SLOTS);

    // Check promotions: nursery patch with evidence score ≥ regular min
    for (const np of [...nurseryPatches]) {
      if (np.evidence.length === 0) continue; // no evidence yet, can't promote
      // Score floor: never promote a net-negative unit onto the deployed track,
      // even into an open slot. Negative score = net-harmful aggregate evidence.
      if (np.score <= PROMOTE_SCORE_FLOOR) {
        console.error(`  [promote-skip] ${np.filename} (${np.score.toFixed(3)}) ≤ floor ${PROMOTE_SCORE_FLOOR} — net-negative, kept in nursery`);
        continue;
      }

      const sameTypeRegular = np.subtype === 'exploit' ? regularExploits : regularExplores;
      const maxSlots = np.subtype === 'exploit' ? REGULAR_EXPLOIT_SLOTS : REGULAR_EXPLORE_SLOTS;

      if (sameTypeRegular.length < maxSlots) {
        // Open slot → promote directly
        sameTypeRegular.push(np);
        np.track = 'regular';
        np._isNursery = false;
        promoteCount++;
        console.error(`  [promote] ${np.filename} → regular (open slot)`);

        // Emit promotion event
        appendEvent('unit.promote', {
          eu: `${skill}/${np.filename}`,
          from_track: 'nursery',
          to_track: 'regular',
          score: np.score,
          evidence_count: np.evidence.length,
        });
      } else {
        const minRegular = sameTypeRegular[sameTypeRegular.length - 1];
        if (np.score > minRegular.score) {
          // Promote: swap nursery patch in, demote regular min
          sameTypeRegular.pop();
          sameTypeRegular.push(np);
          sameTypeRegular.sort((a, b) => b.score - a.score);
          np.track = 'regular';
          np._isNursery = false;
          promoteCount++;
          console.error(`  [promote] ${np.filename} (${np.score.toFixed(3)}) replaces ${minRegular.filename} (${minRegular.score.toFixed(3)})`);

          // Emit promotion event
          appendEvent('unit.promote', {
            eu: `${skill}/${np.filename}`,
            from_track: 'nursery',
            to_track: 'regular',
            score: np.score,
            evidence_count: np.evidence.length,
          });
        }
      }
    }

    // Nursery early-stop: if nursery score < waiting queue top prior score
    for (const np of [...nurseryPatches]) {
      if (np.track === 'regular') continue; // already promoted
      if (waitingQueue.length > 0 && np.score < waitingQueue[0].score) {
        console.error(`  [early-stop] ${np.filename} (${np.score.toFixed(3)}) < waiting top (${waitingQueue[0].score.toFixed(3)})`);
        if (evictPatch(unitsDir, skill, np.filename, 'early-stop')) {
          evictCount++;
          appendEvent('unit.evict', {
            eu: `${skill}/${np.filename}`,
            reason: 'early-stop',
            track: 'nursery',
            evidence_count: np.evidence ? np.evidence.length : 0,
            score: typeof np.score === 'number' ? np.score : null,
          });
        }
      }
    }

    // ─── Step 4: DEGRADE (first negative → inject supersede) ───

    for (const patch of skillPatches) {
      if (patch.pinned) continue; // Pinned patches don't get degraded
      if (patch._status === 'degraded') continue; // Already degraded, waiting for supersede
      const negCount = countNegativeEvidence(patch);
      // 1st negative → code-inject supersede for next generator run.
      // Note: no need to check "already superseded" — superseded patches are
      // renamed to *.superseded.md and filtered out by loadAllPatches (L72),
      // so they never reach this loop.
      if (negCount === 1) {
        // First negative → code-inject supersede for next generator run
        if (sepQueuePath) {
          writeSepQueueEntry(sepQueuePath, {
            ts: new Date().toISOString(),
            action: 'improve_unit',
            skill: patch.skill,
            unit_file: patch.filename,
            type: patch.type,
            condition: patch.condition,
            condition_keywords: patch.condition_keywords,
            reason: `degraded: ${patch.evidence.filter(e => e.effect < 0).map(e => e.reasoning).join('; ').substring(0, 200)}`,
            processed: false,
          });
          degradeCount++;
          patch._status = 'degraded';
          console.error(`  [degrade] ${patch.filename} → sep-queue (1st negative, pending supersede)`);

          // Emit degrade event
          appendEvent('lifecycle.degrade', {
            eu: `${skill}/${patch.filename}`,
            negative_count: 1,
          });
        }
      }
    }

    // Report for this skill
    const allSelected = [...pinnedPatches, ...regularExploits, ...regularExplores, ...nurseryPatches.filter(p => p.track !== 'regular')];
    selectedBySkill.set(skill, new Set(allSelected.map(p => p.filename)));
    report.push({
      skill,
      pinned: pinnedPatches.length,
      regular_exploit: regularExploits.length,
      regular_explore: regularExplores.length,
      nursery: nurseryPatches.filter(p => p.track !== 'regular').length,
      waiting: waitingQueue.length,
      patches: allSelected.map(p => ({
        filename: p.filename,
        title: p.title,
        type: p.type,
        track: p.pinned ? 'pinned' : (p.track === 'regular' ? 'regular' : (p._isNursery ? 'nursery' : 'regular')),
        score: parseFloat(p.score.toFixed(4)),
        coverage: parseFloat((p._coverage || 0).toFixed(4)),
        effect: parseFloat((p._effect || 0).toFixed(4)),
        efficiency: parseFloat((p._efficiency || 0).toFixed(4)),
        evidence_count: p.evidence.length,
      })),
    });

    console.error(`  [slots] pinned: ${pinnedPatches.length}, regular: ${regularExploits.length}E/${regularExplores.length}X, nursery: ${nurseryPatches.filter(p => p.track !== 'regular').length}, waiting: ${waitingQueue.length}`);
  }

  // ─── Step 5: WRITE-BACK (frontmatter + SKILL.md inline) ───

  const skipInline = args.includes('--skip-inline');
  let inlineCount = 0;
  const blockedSkills = getBlockedSkills();

  for (const skill of skills) {
    // Blocked skill: ensure it is un-inlined and never re-attached. EU files on
    // disk are preserved (archived) — blocking suppresses deployment, not history.
    if (blockedSkills.has(skill)) {
      if (!skipInline) {
        for (const smdPath of findSkillMds(skill)) {
          if (smdPath.includes('/extensions/')) continue;
          const result = removeInlineFromSkillMd(smdPath);
          if (result === 'removed') {
            inlineCount++;
            console.error(`  [inline] ${smdPath} → removed (skill blocked)`);
          }
        }
      }
      continue;
    }

    const activePatches = allUnits.filter(p => p.skill === skill);

    // Write-back frontmatter for all active patches
    // Only mark inlined for patches actually selected for SKILL.md
    const selected = selectedBySkill.get(skill) || new Set();
    for (const patch of activePatches) {
      if (!skipInline && selected.has(patch.filename)) patch._inlined = true;
      writeFrontmatter(unitsDir, patch);
    }

    if (skipInline) continue;

    // Find SKILL.md files for this skill
    const skillMds = findSkillMds(skill);

    if (activePatches.length === 0) {
      // All patches evicted — remove inline block
      for (const smdPath of skillMds) {
        if (smdPath.includes('/extensions/')) continue;
        const result = removeInlineFromSkillMd(smdPath);
        if (result === 'removed') {
          console.error(`  [inline] ${smdPath} → removed (no active patches)`);
        }
      }
      continue;
    }

    // Render and write inline block — only selected patches (respects slot limits)
    const selectedPatches = activePatches.filter(p => selected.has(p.filename));

    // Defensive: active patches exist but none selected → clear stale inline block
    if (selectedPatches.length === 0) {
      for (const smdPath of skillMds) {
        if (smdPath.includes('/extensions/')) continue;
        const result = removeInlineFromSkillMd(smdPath);
        if (result === 'removed') {
          console.error(`  [inline] ${smdPath} → removed (no selected patches)`);
        }
      }
      continue;
    }

    const inlineBlock = renderInlineBlock(selectedPatches);
    if (!inlineBlock) continue;

    for (const smdPath of skillMds) {
      // Skip bundled extensions/ SKILL.md — Gateway auto-restores these files.
      // Lifecycle should only inline into local (workspace) SKILL.md copies.
      if (smdPath.includes('/extensions/')) {
        console.error(`  [inline] ${smdPath} → skipped (bundled extension, auto-restored by Gateway)`);
        continue;
      }
      try {
        const result = inlineIntoSkillMd(smdPath, inlineBlock);
        if (result !== 'unchanged') {
          inlineCount++;
          console.error(`  [inline] ${smdPath} → ${result}`);
        }
      } catch (e) {
        console.error(`  [inline] ERROR ${smdPath}: ${e.message}`);
      }
    }
  }

  // Output summary to stdout (JSON)
  const summary = {
    timestamp: new Date().toISOString(),
    stats: {
      patches: allUnits.length,
      evidence: evidence.length,
      evicted: evictCount,
      promoted: promoteCount,
      degraded: degradeCount,
      inlined: inlineCount,
    },
    skills: report,
  };
  console.log(JSON.stringify(summary, null, 2));

  console.error(`\n[lifecycle] Done: ${evictCount} evicted, ${promoteCount} promoted, ${degradeCount} degraded, ${inlineCount} SKILL.md inlined`);
}

main();