#!/usr/bin/env node
/**
 * generator.js — v2.0 Daily Mode
 * 
 * Two-step pipeline: Triage → Generate
 * Reads formatted traces (from trace-extractor), generates units.
 * 
 * Design: §10.5 (Generator two-step pipeline) + §10.6 (Unit body + prompt)
 * 
 * Usage:
 *   node generator.js --traces <traces.jsonl> --patches-dir <dir> --model <model>
 *   node generator.js --mode supersede --patch <path> --traces <traces.jsonl> --patches-dir <dir> --model <model>
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { createLLMClient } = require('./lib/llm-client');
const { parseFrontmatter } = require('./lib/frontmatter');
const { reviewPatch }     = require('./reviewer');
const { appendEvent }     = require('./lib/events');
const { isActiveUnitFile, ensureUnitsDir } = require('./lib/unit-files');

// ─── Configuration ─────────────────────────────────────────────

let LLM_MODEL_SPEC = null; // null = auto-detect

// Fields owned exclusively by lifecycle.js — must never be written by generator.
// LLM may hallucinate these when generating new EUs from existing patch context.
const LIFECYCLE_MANAGED_FIELDS = ['score', 'track', 'inlined', 'evidence_count', 'last_evidence', 'status'];
let _llm = null; // LLM client instance

// ─── Prompts ───────────────────────────────────────────────────

const TRIAGE_SYSTEM = `You are a Skill Evolution Critic analyzing AI agent execution traces to extract reusable lessons.

## YOUR ROLE
You observe how an agent executed a task and identify patterns worth remembering:
- **exploit**: A strategy the agent used that WORKED (error recovery, clever workaround, effective tool usage)
- **explore**: A dead end the agent hit that FAILED with no good recovery (wasted steps, wrong approach)

## INPUT
1. Task execution trace (agent's step-by-step actions and results)
2. Skill info (name + existing units for this skill)

## WHAT TO LOOK FOR
- Error → recovery patterns (agent hit error, then found workaround → exploit)
- Repeated failures without progress (agent tried same thing multiple times → explore)
- Tool misuse or wrong tool choice (used web_search when skill has a script → explore)
- Clever fallback strategies (primary tool failed, backup worked → exploit)
- Suboptimal paths that still succeeded (agent took 10 steps when 2 would suffice)
- **User reaction patterns** (signals from USER messages in the trace):
  - User EXPLICITLY praised the agent's approach → reinforces that strategy as exploit
  - User EXPLICITLY criticized, rejected, or demanded correction → the strategy the agent just used is an explore (dead end from the user's perspective)
  - Mismatch between "execution succeeded" and "user pushed back" is the most valuable signal — execution-only analysis misses it entirely

## WHAT TO SKIP
- Normal successful execution with no interesting patterns
- Trivial observations ("agent read the skill file")
- Environment-specific issues that can't be generalized
- Patterns already covered by existing units (check the list!)
- User messages that merely continue the task (not reactions to the agent's output)
- Implicit guesses about user satisfaction (silence, topic-switching, or continuation are NOT reliable signals — only use explicit user text)

## OUTPUT FORMAT
JSON array. Each element:
{"action": "new", "subtype": "exploit|explore", "condition": "<when this applies — one sentence>", "condition_keywords": ["kw1", "kw2", ...], "reason": "<what happened and why it's worth recording>"}

Or for replacing an existing unit:
{"action": "supersede", "target": "<unit filename>", "subtype": "exploit|explore", "condition": "<updated condition>", "condition_keywords": [...], "reason": "<what's wrong with old unit + how trace shows better>"}

When generating a new exploit, check existing explore units in the list. If the exploit you are proposing would likely make an existing explore warning unnecessary (i.e., the exploit solves the problem the explore warns about), add:
  "source_explore": "<explore unit filename>"
This is a lightweight signal — you do not need to prove causation, just plausible coverage.

If nothing worth extracting: []

Output ONLY the JSON array, no other text.`;

const NEW_EXPLOIT_SYSTEM = `You are writing a skill evolution unit — a reusable lesson extracted from an agent's execution trace.

Output ONLY the unit in this exact format (no extra text):
---
schema: 2
skill: {skill_name}
type: adaptive
subtype: exploit
title: "<short descriptive title>"
condition: "{from triage}"
condition_keywords: {from triage as JSON array}
created: {date}
source_task: {task_id}
source_explore: {explore unit filename from triage, or "none" if not applicable}
status: active
---
## When to Apply
<expand the condition: when exactly this applies, when it does NOT>

## Proven Strategy
<what to do — principle-based, max 100 words, actionable>

## Evidence
<what happened in the trace that proves this works>

Rules:
- Max 100 words for Proven Strategy
- Specific enough to be actionable, general enough to transfer
- Condition must be observable from the agent's perspective
- If after reviewing the trace you cannot formulate a clear, actionable lesson (too vague, too task-specific, or already obvious), output ONLY: {"skip": true, "reason": "<why>"}`;

const NEW_EXPLORE_SYSTEM = `You are writing a skill evolution unit — a negative feedback recording a verified dead end from an agent's execution trace.

Output ONLY the unit in this exact format (no extra text):
---
schema: 2
skill: {skill_name}
type: adaptive
subtype: explore
title: "<short descriptive title>"
condition: "{from triage}"
condition_keywords: {from triage as JSON array}
created: {date}
source_task: {task_id}
status: active
---
## Condition & Boundary
<when this IS a dead end — the specific condition>
<when it might NOT be a dead end — boundary conditions, env changes, different params>

## Ineffective Behavior
<what the agent did that failed — factual description, max 100 words>

## Field Notes (unverified)
- <one-line direction to explore around the dead end, or a question>
- <optional second note>
- <optional third note, max 3>

## Failure Evidence
<error messages, status codes, failure pattern — concrete evidence from the trace>

Rules:
- Max 100 words for Ineffective Behavior
- Describe what was tried and why it failed — factual, no alternatives in this section
- Field Notes are unverified hypotheses, not proven strategies
- Boundary conditions must be complete: when IS it a dead end + when might it NOT be
- If after reviewing the trace you cannot formulate a clear, actionable warning (too vague, too task-specific, or already obvious), output ONLY: {"skip": true, "reason": "<why>"}`;

const SUPERSEDE_SYSTEM = `You are rewriting an existing skill evolution unit that has proven inadequate.
Produce a new unit that supersedes the old one, preserving valid insights while fixing issues.

Output ONLY the unit in the standard format (---frontmatter--- then sections).
Add "supersedes: {target_filename}" and "status: active" to the frontmatter.

Rules:
- Max 100 words for Strategy/Warning section
- Preserve valid insights from the old unit
- Explicitly address the degradation cause or gap
- Keep the same type (exploit/explore) unless there's a strong reason to change
- If after reviewing the trace and old unit you cannot produce a meaningfully improved version, output ONLY: {"skip": true, "reason": "<why>"}`;

// ─── LLM Call (via shared client) ──────────────────────────────

async function callLLM(system, user, opts = {}) {
  return _llm.call(system, user, opts);
}

// ─── JSON Parsing (tolerant) ───────────────────────────────────

/**
 * Normalize common wire-level artefacts: BOM, CRLF, trailing whitespace.
 * Keeps original content otherwise (no smart-quote normalization).
 */
function normalizeLLMOutput(text) {
  if (typeof text !== 'string') return '';
  return text
    .replace(/^\uFEFF/, '')    // strip BOM
    .replace(/\r\n/g, '\n')    // CRLF → LF
    .replace(/\r/g, '\n');     // lone CR → LF
}

/**
 * Extract first fenced code block. Accepts ```lang\n...\n``` or ```\n...\n```.
 * Returns inner content, or null. Handles prose prefix ("Here are: ```json ...```").
 */
function extractFencedBlock(text) {
  const m = text.match(/```[a-zA-Z0-9_-]*\n([\s\S]*?)```/);
  return m ? m[1].trim() : null;
}

function extractJsonArray(text) {
  const normalized = normalizeLLMOutput(text);

  // 1) Direct parse
  try { return JSON.parse(normalized.trim()); } catch {}

  // 2) Strip top-level wrapping ```...```
  const clean = stripCodeBlock(normalized);
  try { return JSON.parse(clean); } catch {}

  // 3) Extract first fenced block anywhere (handles "prose + ```json [...]```")
  const fenced = extractFencedBlock(normalized);
  if (fenced !== null) {
    try { return JSON.parse(fenced); } catch {}
  }

  // 4) Bare fallback: first [ to last ] in cleaned/fenced text (not raw)
  const search = fenced ?? clean;
  const first = search.indexOf('[');
  const last = search.lastIndexOf(']');
  if (first >= 0 && last > first) {
    try { return JSON.parse(search.substring(first, last + 1)); } catch {}
  }
  return null;
}

function stripCodeBlock(text) {
  let s = text.trim();
  if (s.startsWith('```')) {
    s = s.split('\n').slice(1).join('\n');
    const end = s.lastIndexOf('```');
    if (end >= 0) s = s.substring(0, end);
  }
  return s.trim();
}

// ─── Skill Context ─────────────────────────────────────────────

/**
 * Load all active units for a skill.
 * Returns [{filename, content, frontmatter}]
 */
function loadSkillUnits(unitsDir, skill) {
  const skillDir = path.join(unitsDir, skill);
  if (!fs.existsSync(skillDir)) return [];
  
  const patches = [];
  for (const f of fs.readdirSync(skillDir)) {
    if (!isActiveUnitFile(f)) continue;
    const content = fs.readFileSync(path.join(skillDir, f), 'utf8');
    const fm = parseFrontmatter(content);
    patches.push({ filename: f, content, frontmatter: fm });
  }
  return patches;
}

// parseFrontmatter lives in ./lib/frontmatter.js

/**
 * Format units for triage prompt (title + condition only).
 */
function formatUnitsForTriage(patches) {
  if (patches.length === 0) return '(no existing units)';
  return patches.map(p => {
    const fm = p.frontmatter;
    return `--- ${p.filename} (subtype: ${fm.subtype || '?'}) ---\ntitle: ${fm.title || '?'}\ncondition: ${fm.condition || '?'}`;
  }).join('\n\n');
}

/**
 * Format a single unit for generate prompt (full text).
 */
function formatUnitFull(patch) {
  return `--- ${patch.filename} ---\n${patch.content}`;
}

// ─── Step 1: Triage ────────────────────────────────────────────

async function runTriage(si, patches) {
  const unitsSummary = formatUnitsForTriage(patches);
  
  const userPrompt = `### Task Execution Trace
${si.score != null ? `Score: ${si.score}/1.0\n` : ''}
${si.trace}

### Skill: ${si.skill}
### Existing Units (${patches.length} total)
${unitsSummary}`;

  const response = await callLLM(TRIAGE_SYSTEM, userPrompt);
  const actions = extractJsonArray(response);
  
  if (!actions || !Array.isArray(actions)) {
    console.error(`  [triage] Failed to parse response for ${si.si_id}`);
    return [];
  }
  
  return actions;
}

// ─── Code-Injected Actions ─────────────────────────────────────

function loadCodeInjections(sepQueuePath) {
  if (!fs.existsSync(sepQueuePath)) return [];
  
  const lines = fs.readFileSync(sepQueuePath, 'utf8').split('\n').filter(Boolean);
  const injections = [];
  
  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      if ((entry.action === 'improve_unit' || entry.action === 'improve_patch') && !entry.processed) {
        injections.push(entry);
      }
    } catch {}
  }
  
  return injections;
}

/**
 * Mark sep-queue entries as processed by rewriting the file in place.
 * consumedKeys: Set of "{skill}::{unit_file}::{ts}" composite keys identifying
 * which improve_patch entries were actually consumed this run.
 * Double-read: legacy pre-v2.4.0 entries used patch_file; we accept either.
 */
function markInjectionsProcessed(sepQueuePath, consumedKeys) {
  if (!fs.existsSync(sepQueuePath) || consumedKeys.size === 0) return 0;
  
  const lines = fs.readFileSync(sepQueuePath, 'utf8').split('\n').filter(Boolean);
  let updated = 0;
  const rewritten = lines.map(line => {
    try {
      const entry = JSON.parse(line);
      if ((entry.action === 'improve_unit' || entry.action === 'improve_patch') && !entry.processed) {
        const key = `${entry.skill}::${entry.unit_file || entry.patch_file}::${entry.ts}`;
        if (consumedKeys.has(key)) {
          entry.processed = true;
          updated++;
          return JSON.stringify(entry);
        }
      }
      return line;
    } catch {
      return line;
    }
  });
  
  fs.writeFileSync(sepQueuePath, rewritten.join('\n') + '\n');
  return updated;
}

function mergeInjections(triageActions, injections, skill) {
  const merged = [...triageActions];
  const consumed = [];
  
  for (const inj of injections) {
    if (inj.skill !== skill) continue;
    const injFile = inj.unit_file || inj.patch_file;  // double-read legacy sep-queue
    
    // Check if triage already targets the same unit
    const exists = merged.some(a => 
      a.action === 'supersede' && a.target === injFile
    );
    
    if (!exists) {
      merged.push({
        action: 'supersede',
        target: injFile,
        type: inj.type || 'exploit',
        condition: inj.condition || '',
        condition_keywords: inj.condition_keywords || [],
        reason: `Code-injected: ${inj.reason || 'degraded evidence'}`,
        _injected: true,
      });
    }
    // Either path consumes this injection: triage already chose to
    // supersede the same target, or we just added a supersede action.
    consumed.push(inj);
  }
  
  return { merged, consumed };
}

// ─── Step 2: Generate ──────────────────────────────────────────

async function runGenerate(action, si, patches, unitsDir) {
  const today = new Date().toISOString().split('T')[0];
  const taskId = si.session_id || si.si_id;
  
  let response;
  let resultType;
  let targetInfo = {};
  
  if (action.action === 'new') {
    const actionSubtype = action.subtype || action.type;
    const system = actionSubtype === 'exploit' ? NEW_EXPLOIT_SYSTEM : NEW_EXPLORE_SYSTEM;
    const userPrompt = `### Triage Decision
action: new
subtype: ${actionSubtype}
condition: "${action.condition}"
condition_keywords: ${JSON.stringify(action.condition_keywords || [])}
reason: "${action.reason}"
source_explore: ${action.source_explore || 'none'}

### Task Trace
${si.trace}

### Context
skill: ${si.skill}
date: ${today}
source_task: ${taskId}`;

    response = await callLLM(system, userPrompt);
    resultType = 'new';
    
  } else if (action.action === 'supersede') {
    const targetPatch = patches.find(p => p.filename === action.target);
    if (!targetPatch) {
      console.error(`  [generate] Target unit not found: ${action.target}`);
      return null;
    }
    
    const userPrompt = `### Triage Decision
action: supersede
target: ${action.target}
condition: "${action.condition}"
reason: "${action.reason}"

### Target Patch (to replace)
${targetPatch.content}

### Task Trace
${si.trace}

### Context
skill: ${si.skill}
date: ${today}
source_task: ${taskId}`;

    response = await callLLM(SUPERSEDE_SYSTEM, userPrompt);
    resultType = 'supersede';
    targetInfo = { target: action.target };
  } else {
    return null;
  }
  
  // Check for skip response
  const skipCheck = detectSkip(response);
  if (skipCheck) {
    console.error(`  [generate] SKIP: ${skipCheck.reason}`);
    return null;
  }
  
  return { type: resultType, content: stripCodeBlock(normalizeLLMOutput(response)), action, ...targetInfo };
}

/**
 * Detect if LLM output is a skip signal.
 * Returns {reason} if skip, null otherwise.
 */
function detectSkip(text) {
  const clean = text.trim();
  // Direct JSON skip
  try {
    const obj = JSON.parse(stripCodeBlock(clean));
    if (obj && obj.skip === true) return { reason: obj.reason || 'no reason given' };
  } catch {}
  // Relaxed: find {"skip": true} anywhere in output
  const match = clean.match(/\{\s*"skip"\s*:\s*true\s*(?:,\s*"reason"\s*:\s*"([^"]*)")?\s*\}/);
  if (match) return { reason: match[1] || 'no reason given' };
  return null;
}

// ─── Evidence Inheritance ───────────────────────────────────────

/**
 * When a unit is superseded, copy its evidence entries to evidence.jsonl
 * with inherited_from marker, keyed to the new unit filename.
 * Patcher applies 50% weight discount on inherited evidence (§v1.4.1).
 */
function inheritEvidence(unitsDir, skill, oldFilename, newFilename) {
  const evidencePath = path.join(unitsDir, 'evidence.jsonl');
  if (!fs.existsSync(evidencePath)) return;
  
  const lines = fs.readFileSync(evidencePath, 'utf8').split('\n').filter(Boolean);
  const inherited = [];
  
  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      // Double-read unit_file || patch_file for legacy pre-v2.4.0 entries
      const entryFile = entry.unit_file || entry.patch_file;
      if (entryFile === oldFilename && entry.skill === skill) {
        inherited.push({
          ...entry,
          unit_file: newFilename,
          patch_file: undefined,   // normalize on rewrite
          inherited_from: oldFilename,
          inherited_at: new Date().toISOString(),
        });
      }
    } catch { /* skip malformed */ }
  }
  
  if (inherited.length > 0) {
    const appendData = inherited.map(e => JSON.stringify(e)).join('\n') + '\n';
    fs.appendFileSync(evidencePath, appendData);
    console.error(`  [inherit] ${inherited.length} evidence entries: ${oldFilename} → ${newFilename}`);
  }
}

// ─── Unit Writing ─────────────────────────────────────────────

function writeUnit(unitsDir, skill, generated) {
  const skillDir = path.join(unitsDir, skill);
  if (!fs.existsSync(skillDir)) fs.mkdirSync(skillDir, { recursive: true });
  
  const today = new Date().toISOString().split('T')[0].replace(/-/g, '');
  // Phase 2b+: new EU files use `eu-YYYYMMDD-slug.md` prefix.
  // Subtype (exploit|explore) is no longer encoded in the filename —
  // it lives in the frontmatter's `subtype:` field.
  const baseName = `eu-${today}-${slugify(generated.action.condition || 'unnamed')}`;
  
  // Avoid collision
  let filename = `${baseName}.md`;
  let counter = 2;
  while (fs.existsSync(path.join(skillDir, filename))) {
    filename = `${baseName}-${counter}.md`;
    counter++;
  }
  
  const filePath = path.join(skillDir, filename);
  
  // Security: validate unit content before writing
  const content = generated.content || '';
  if (content.includes('SKILL-EVOLVER:PATCHES-START') || content.includes('SKILL-EVOLVER:PATCHES-END')) {
    console.error(`  [write] REJECTED: unit contains inline marker injection — ${filename}`);
    return null;
  }
  // Validate frontmatter is parseable (tolerant to BOM/CRLF/leading whitespace)
  const fmMatch = content.match(/^\s*---\r?\n([\s\S]*?)\n---/);
  if (!fmMatch) {
    console.error(`  [write] REJECTED: unit has no valid frontmatter — ${filename}`);
    return null;
  }

  // Strip lifecycle-managed fields from frontmatter before writing.
  // LLM may hallucinate these from context — they must only be written by lifecycle.js.
  let sanitizedContent = content.replace(
    /^(\s*---\r?\n)[\s\S]*?\n---/,
    (match, open) => {
      const bodyMatch = match.match(/^\s*---\r?\n([\s\S]*?)\n---/);
      // bodyMatch cannot be null here (outer regex already matched), but guard for clarity
      if (!bodyMatch) return match;
      const stripped = [];
      const cleaned = bodyMatch[1]
        .split('\n')
        .filter(line => {
          const key = line.match(/^(\w+)\s*:/);
          if (key && LIFECYCLE_MANAGED_FIELDS.includes(key[1])) {
            stripped.push(key[1]);
            return false;
          }
          return true;
        })
        .join('\n');
      if (stripped.length > 0) {
        console.error(`  [write] Stripped lifecycle fields from frontmatter: ${stripped.join(', ')} — ${filename}`);
      }
      return `${open}${cleaned}\n---`;
    }
  );

  fs.writeFileSync(filePath, sanitizedContent);
  
  // Handle supersede: rename old unit + inherit evidence
  if (generated.type === 'supersede' && generated.target) {
    const oldPath = path.join(skillDir, generated.target);
    if (fs.existsSync(oldPath)) {
      const supersededPath = oldPath.replace('.md', '.superseded.md');
      fs.renameSync(oldPath, supersededPath);
      console.error(`  [write] Superseded: ${generated.target} → ${path.basename(supersededPath)}`);
      
      // Inherit evidence: copy old unit's evidence entries to new filename
      // Design ref: §v1.4.1 handleSupersede() — inherited_from + 50% weight discount
      inheritEvidence(unitsDir, skill, generated.target, filename);
    }
  }
  
  console.error(`  [write] New unit: ${filename}`);
  
  return filename;
}

function slugify(text) {
  return text.toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_|_$/g, '')
    .substring(0, 40);
}

// ─── Sep-Queue ─────────────────────────────────────────────────

function writeSepQueue(sepQueuePath, skill, unitFile, action) {
  const entry = {
    ts: new Date().toISOString(),
    skill,
    unit_file: unitFile,
    action: action === 'supersede' ? 'supersede_unit' : 'new_unit',
    processed: false,
  };
  fs.appendFileSync(sepQueuePath, JSON.stringify(entry) + '\n');
}

// ─── Main ──────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  
  let tracesPath = null;
  let unitsDir = null;
  let sepQueuePath = null;
  
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--traces':      tracesPath = args[++i]; break;
      case '--eu-dir':
      case '--patches-dir': unitsDir = args[++i]; break;
      case '--model':       LLM_MODEL_SPEC = args[++i]; break;
      case '--sep-queue':   sepQueuePath = args[++i]; break;
    }
  }
  
  if (!tracesPath || !unitsDir) {
    console.error('Usage: node generator.js --traces <file.jsonl> --eu-dir <dir> [--model <provider/model>]');
    console.error('Example: node generator.js --traces traces.jsonl --eu-dir ./eu --model anthropic/claude-sonnet-4.6');
    console.error('If --model is omitted, auto-detects from platform config or EVOLVER_MODEL env var');
    process.exit(1);
  }
  
// ─── Privacy Guard ────────────────────────────────────────────
// Check privacy.allowRemoteLLM in evolver-config.json.
// Default: true (allows LLM calls). Set to false to block all outbound LLM requests.
{
  const cfgPath = require('path').join(__dirname, '..', 'evolver-config.json');
  try {
    const cfg = JSON.parse(require('fs').readFileSync(cfgPath, 'utf8'));
    if (cfg.privacy?.allowRemoteLLM === false) {
      console.error('[generator] Blocked: privacy.allowRemoteLLM is set to false in evolver-config.json.');
      console.error('[generator] Remove or set "privacy": { "allowRemoteLLM": true } to enable LLM calls.');
      process.exit(0);
    }
  } catch { /* config not found or unreadable — proceed with default (allow) */ }
}

  // Create LLM client: explicit --model or auto-detect from config
  ensureUnitsDir(unitsDir);
  _llm = createLLMClient(LLM_MODEL_SPEC);
  LLM_MODEL_SPEC = _llm.model; // for logging
  
  // Load traces
  const traces = fs.readFileSync(tracesPath, 'utf8')
    .split('\n')
    .filter(Boolean)
    .flatMap((line, i) => {
      try { return [JSON.parse(line)]; }
      catch { console.error(`[generator] Skipped malformed line ${i + 1}`); return []; }
    });
  
  console.error(`[generator] Processing ${traces.length} traces, model=${LLM_MODEL_SPEC}`);
  
  // Load code injections
  const injections = sepQueuePath ? loadCodeInjections(sepQueuePath) : [];
  if (injections.length > 0) {
    console.error(`[generator] ${injections.length} code-injected actions from sep-queue`);
  }
  
  // Stats
  let triageCount = 0, generateCount = 0, unitCount = 0, skipCount = 0;
  const consumedInjectionKeys = new Set();
  
  // Process each trace
  for (const si of traces) {
    console.error(`\n[generator] SI: ${si.si_id} (skill=${si.skill}, steps=${si.trace_steps})`);
    
    // Load skill's existing units
    const patches = loadSkillUnits(unitsDir, si.skill);
    console.error(`  [triage] ${patches.length} existing units for ${si.skill}`);
    
    // Step 1: Triage
    let actions;
    try {
      actions = await runTriage(si, patches);
      triageCount++;
    } catch (err) {
      console.error(`  [triage] Error: ${err.message}`);
      continue;
    }
    
    // Merge code injections
    const { merged, consumed } = mergeInjections(actions, injections, si.skill);
    actions = merged;
    for (const inj of consumed) {
      consumedInjectionKeys.add(`${inj.skill}::${inj.unit_file || inj.patch_file}::${inj.ts}`);
    }
    
    if (actions.length === 0) {
      console.error(`  [triage] No actions → skip`);
      continue;
    }
    
    console.error(`  [triage] ${actions.length} actions: ${actions.map(a => `${a.action}/${a.type}`).join(', ')}`);
    
    // Step 2: Generate each action
    for (const action of actions) {
      try {
        const generated = await runGenerate(action, si, patches, unitsDir);
        generateCount++;
        
        if (!generated || !generated.content) {
          skipCount++;
          console.error(`  [generate] Empty/skipped for ${action.action}/${action.subtype || action.type}`);
          continue;
        }
        
        // Write unit file
        const filename = writeUnit(unitsDir, si.skill, generated);
        if (!filename) { skipCount++; continue; }
        unitCount++;

        // Emit event for successful unit creation
        if (generated.type === 'new') {
          appendEvent('unit.create', {
            eu: `${si.skill}/${filename}`,
            subtype: generated.action.subtype || generated.action.type,
            source_task: si.task_id || null,
            source_explore: generated.action.subtype === 'exploit' ? (generated.action.source_explore || null) : null,
          });
        } else if (generated.type === 'supersede') {
          appendEvent('unit.supersede', {
            eu: `${si.skill}/${filename}`,
            supersedes: `${si.skill}/${generated.target}`,
            subtype: generated.action.subtype || generated.action.type,
            source_task: si.task_id || null,
          });
        }

        // Security review — rejects rename file to .rejected.md, lifecycle won't pick it up
        const filePath = path.join(unitsDir, si.skill, filename);
        const verdict  = await reviewPatch(filePath, si.skill);
        if (verdict === 'reject') { unitCount--; skipCount++; continue; }

        // Write sep-queue entry
        if (sepQueuePath) {
          writeSepQueue(sepQueuePath, si.skill, filename, generated.type);
        }
        
      } catch (err) {
        console.error(`  [generate] Error: ${err.message}`);
      }
    }
  }
  
  console.error(`\n[generator] Done: ${triageCount} triaged, ${generateCount} generated, ${skipCount} skipped, ${unitCount} units written`);
  
  // Mark consumed injections as processed (bugfix: sep-queue was never cleaned)
  if (sepQueuePath && consumedInjectionKeys.size > 0) {
    const marked = markInjectionsProcessed(sepQueuePath, consumedInjectionKeys);
    console.error(`[generator] Marked ${marked} sep-queue entries as processed`);
  }
}

main().catch(err => {
  console.error(`[generator] Fatal: ${err.message}`);
  process.exit(1);
});
