#!/usr/bin/env node
/**
 * validator.js — v2.0 Daily Mode
 *
 * Validates existing units against execution traces using two-step attribution.
 * Design: §10.7 (Validator) + §3.6 (multi-dimensional tags)
 * 
 * Pipeline:
 *   Step 1: Relevance Triage (per-trace) — which units relate to this trace?
 *   Step 2: Attribution (per-relevant-unit) — how did the unit influence behavior?
 *   Code:   Multi-dimensional tags → effect score (no LLM)
 *
 * Usage:
 *   node validator.js --traces <traces.jsonl> --eu-dir <dir> --output <evidence.jsonl> [--model <provider/model>]
 *
 * Output: evidence.jsonl — one entry per unit×trace attribution
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { createLLMClient } = require('./lib/llm-client');
const { parseFrontmatter } = require('./lib/frontmatter');
const { appendEvent } = require('./lib/events');
const { isActiveUnitFile, ensureUnitsDir } = require('./lib/unit-files');

// ─── Configuration ─────────────────────────────────────────────

let _llm = null;

// ─── Prompts (§10.7) ──────────────────────────────────────────

const RELEVANCE_TRIAGE_SYSTEM = `You are a Skill Evolution Validator (attribution role in an Actor-Critic framework).

Your job: given an agent's execution trace and a list of skill evolution units (each with a title and condition), identify which units are RELEVANT to this trace.

## WHAT IS RELEVANCE

A unit is relevant when the trace contains a situation that relates to the unit's condition — the agent encountered something the unit addresses.

Relevance does NOT require exact match. A unit about "web_fetch returning 403 on financial sites" is relevant to a trace where the agent got a 403 from any data source, even if the specific site differs. Look for shared patterns, analogous situations, and transferable lessons.

## RULES

1. Cast a reasonable net: include units where the connection is plausible, even if not a perfect condition match
2. But do not force relevance: if the trace has nothing to do with a unit's topic area, exclude it
3. You are filtering, not judging: downstream attribution will evaluate actual impact. Your job is only to avoid wasting attribution calls on clearly unrelated units
4. Each unit has a subtype (exploit = proven strategy, explore = dead-end warning + alternative). Carry the subtype through in your output.

## OUTPUT FORMAT

JSON array of relevant units:
[
  {"unit_file": "<filename>", "subtype": "exploit|explore", "relevance": "<one sentence: why this unit relates to the trace>"}
]

If no units are relevant, output: []

Output ONLY the JSON array, no other text.`;

const EXPLOIT_ATTRIBUTION_SYSTEM = `You are a Skill Evolution Validator (attribution role in an Actor-Critic framework).

Your job: given an agent's execution trace and a single exploit unit, determine how the unit influenced the agent's behavior.

## WHAT IS AN EXPLOIT UNIT

An exploit unit records a proven strategy: "when condition X occurs, do Y". You are evaluating whether the agent applied this strategy and what happened.

## YOUR TASK

Evaluate three independent dimensions:

### Dimension 1: match (how closely does the trace scenario match the unit's condition?)
- "exact": the unit's condition precisely describes what happened in the trace
- "broad": the unit's experience is related/analogous but the condition is not a precise match

### Dimension 2: outcome (did the unit's strategy help or hurt?)

A unit has value when applying its strategy produces a good result, and loses value when it produces a bad one. "Outcome" captures the direction and strength of that result. All labels below share the same causal requirement: the agent followed the unit's strategy, and that strategy produced the observed result.

Five labels, ordered from strongest positive to strongest negative:

- "user_positive": the user EXPLICITLY expressed satisfaction in the trace, and that satisfaction traces back to the agent having applied the unit's strategy. The user is the ground-truth evaluator of whether the skill served its purpose, so this is the highest-confidence positive signal.

- "positive": execution-level improvement — the task progressed better, fewer wasted steps, an error was avoided. No explicit user signal; this is your behavioral inference from the trace.

- "neutral": the strategy was applied but had no discernible impact.

- "negative": execution-level harm — the strategy caused wasted steps, broke progress, or made things worse. No explicit user signal; this is your behavioral inference.

- "user_negative": the user EXPLICITLY expressed dissatisfaction in the trace, and that dissatisfaction traces back to the agent having applied the unit's strategy. Highest-confidence negative signal for the same reason.

### Dimension 3: scope (how far did the impact reach?)
- "global": the impact directly determined the task's final outcome. The influenced steps are on the critical path to the final result
- "local": the impact was limited to specific steps; the task outcome was determined by other factors
- null: only when outcome is "neutral"

## RULES

1. Focus on BEHAVIORAL evidence: did the agent demonstrably execute the unit's strategy? Look for concrete actions in the trace, not just similar outcomes
2. Be conservative with "global": most single-unit influences are "local" unless the unit addressed the primary bottleneck
3. "broad" match is legitimate — strategies often transfer to analogous situations. But the connection must be substantive, not superficial

## OUTPUT FORMAT

{
  "match": "exact|broad",
  "outcome": "user_positive|positive|neutral|negative|user_negative",
  "scope": "global|local|null",
  "reasoning": "<2-3 sentences explaining what the agent did and how it relates to the unit>"
}

Output ONLY the JSON object, no other text.`;

const EXPLORE_ATTRIBUTION_SYSTEM = `You are a Skill Evolution Validator (attribution role in an Actor-Critic framework).

Your job: given an agent's execution trace and a single explore unit, determine how the unit influenced the agent's behavior.

## WHAT IS AN EXPLORE UNIT

An explore unit has two parts:
- **Dead End** (section "## Dead End"): marks a dead end — "when condition X occurs, doing Y leads to failure"
- **Possible Directions** (section "## Possible Directions"): suggests directions to explore instead

You evaluate each part independently.

## YOUR TASK

### Part 1: Warning attribution

Evaluate whether the agent encountered the dead-end scenario and how it responded:

- "avoided": the scenario occurred (or nearly occurred) but the agent steered clear of the dead-end behavior
- "violated": the scenario occurred and the agent fell into the dead end anyway
- "not_encountered": the dead-end scenario did not arise in this trace at all

When warning_status is "violated", also evaluate **recovered**:
- true: the agent fell into the dead end but then self-corrected and recovered (e.g., backtracked, tried a different approach, eventually succeeded despite the initial mistake)
- false: the agent stayed stuck in the dead end or the dead-end impact persisted through the rest of the trace

### Part 2: Alternative attribution

Evaluate whether the agent adopted the suggested alternative direction:

1. alternative_adopted: true | false
2. alternative_outcome (only when adopted = true): the causal result of following the alternative direction

   A unit's alternative has value when adopting it produces a good result, and loses value when it produces a bad one. All labels share the same causal requirement: the agent adopted the alternative, and that adoption produced the observed result.

   Five labels, ordered from strongest positive to strongest negative:

   - "user_positive": the user EXPLICITLY expressed satisfaction in the trace, and that satisfaction traces back to the agent having adopted this alternative. The user is the ground-truth evaluator, so this is the highest-confidence positive signal.

   - "positive": execution-level improvement from adopting the alternative (no explicit user signal; your inference from the trace).

   - "neutral": the alternative was adopted but had no discernible impact.

   - "negative": execution-level harm from adopting the alternative (no explicit user signal; your inference).

   - "user_negative": the user EXPLICITLY expressed dissatisfaction in the trace, traceable to the adopted alternative. Highest-confidence negative signal for the same reason.

3. alternative_scope (only when outcome ≠ neutral): "global" | "local"

## RULES

1. Warning and alternative are INDEPENDENT judgments — an agent can violate the warning but still benefit from the alternative, or avoid the dead end without using the alternative
2. "avoided" does not automatically mean the unit caused the avoidance — the agent might have avoided it for unrelated reasons. Just record the behavior
3. Focus on behavioral evidence in the trace, not inferred intentions

## OUTPUT FORMAT

{
  "warning_status": "avoided|violated|not_encountered",
  "recovered": true|false|null,
  "alternative_adopted": true|false,
  "alternative_outcome": "user_positive|positive|neutral|negative|user_negative|null",
  "alternative_scope": "global|local|null",
  "reasoning": "<2-3 sentences covering both warning and alternative observations>"
}

Output ONLY the JSON object, no other text.`;

// ─── LLM Call ──────────────────────────────────────────────────

async function callLLM(system, user, opts = {}) {
  return _llm.call(system, user, opts);
}

// ─── JSON Parsing ──────────────────────────────────────────────

function stripCodeBlock(text) {
  let s = text.trim();
  if (s.startsWith('```')) {
    s = s.split('\n').slice(1).join('\n');
    const end = s.lastIndexOf('```');
    if (end >= 0) s = s.substring(0, end);
  }
  return s.trim();
}

function parseJsonSafe(text) {
  const clean = stripCodeBlock(text);
  try { return JSON.parse(clean); } catch {}
  
  // Try to find JSON object or array
  const firstBrace = text.indexOf('{');
  const firstBracket = text.indexOf('[');
  
  if (firstBracket >= 0 && (firstBrace < 0 || firstBracket < firstBrace)) {
    const last = text.lastIndexOf(']');
    if (last > firstBracket) {
      try { return JSON.parse(text.substring(firstBracket, last + 1)); } catch {}
    }
  }
  
  if (firstBrace >= 0) {
    const last = text.lastIndexOf('}');
    if (last > firstBrace) {
      try { return JSON.parse(text.substring(firstBrace, last + 1)); } catch {}
    }
  }
  
  return null;
}

// ─── Unit Loading ─────────────────────────────────────────────

function loadSkillUnits(unitsDir, skill) {
  const skillDir = path.join(unitsDir, skill);
  if (!fs.existsSync(skillDir)) return [];
  
  return fs.readdirSync(skillDir)
    .filter(isActiveUnitFile)
    .map(filename => {
      const content = fs.readFileSync(path.join(skillDir, filename), 'utf8');
      const fm = parseFrontmatter(content);
      return {
        filename,
        content,
        type: fm.type || 'adaptive',
        subtype: fm.subtype || 'exploit',
        title: fm.title || filename,
        condition: fm.condition || '',
        condition_keywords: fm.condition_keywords || [],
        status: fm.status || 'active',
        inlined: fm.inlined === true || fm.inlined === 'true',
        review_status: fm.review_status || null,
      };
    })
    .filter(p => p.review_status !== 'rejected' && p.inlined);
}

// parseFrontmatter lives in ./lib/frontmatter.js

// ─── Step 1: Relevance Triage ──────────────────────────────────

async function runRelevanceTriage(si, patches) {
  if (patches.length === 0) return [];
  
  // Build compact unit summaries (title + condition only)
  const summaries = patches.map(p => 
    `--- ${p.filename} (subtype: ${p.subtype}) ---\ntitle: "${p.title}"\ncondition: "${p.condition}"`
  ).join('\n\n');
  
  const userPrompt = `### Execution Trace
${si.trace}

### Inline Units (${patches.length} total)
${summaries}`;

  const response = await callLLM(RELEVANCE_TRIAGE_SYSTEM, userPrompt);
  const parsed = parseJsonSafe(response);
  
  if (!parsed || !Array.isArray(parsed)) {
    console.error(`  [triage] Failed to parse response, treating as no relevance`);
    return [];
  }
  
  // Validate entries
  // LLM defensive: accept both unit_file (new) and patch_file (legacy echo) so
  // occasional schema drift in LLM output doesn't drop valid triage picks.
  return parsed.filter(entry => {
    const unitFile = entry.unit_file || entry.patch_file;
    if (!unitFile || !(entry.subtype || entry.type)) return false;
    // Normalize so downstream only has to read one field.
    entry.unit_file = unitFile;
    delete entry.patch_file;
    // Verify unit exists
    return patches.some(p => p.filename === unitFile);
  });
}

// ─── Step 2: Attribution ───────────────────────────────────────

async function runExploitAttribution(si, patch) {
  const taskId = si.session_id || si.si_id;
  
  const userPrompt = `### Task Info
task_id: ${taskId}
skill: ${si.skill}

### Current Trace
${si.trace}

### Patch
${patch.content}`;

  const response = await callLLM(EXPLOIT_ATTRIBUTION_SYSTEM, userPrompt);
  const parsed = parseJsonSafe(response);
  
  if (!parsed) {
    console.error(`  [attr:exploit] Failed to parse response for ${patch.filename}`);
    return null;
  }
  
  // Validate fields
  const validMatch = ['exact', 'broad'];
  const validOutcome = ['user_positive', 'positive', 'neutral', 'negative', 'user_negative'];
  const validScope = ['global', 'local', null];
  
  if (!validMatch.includes(parsed.match)) parsed.match = 'broad';
  if (!validOutcome.includes(parsed.outcome)) parsed.outcome = 'neutral';
  if (parsed.outcome === 'neutral') parsed.scope = null;
  else if (!validScope.includes(parsed.scope)) parsed.scope = 'local';
  
  return {
    unit_file: patch.filename,
    type: 'exploit',
    match: parsed.match,
    outcome: parsed.outcome,
    scope: parsed.scope,
    reasoning: parsed.reasoning || '',
  };
}

async function runExploreAttribution(si, patch) {
  const taskId = si.session_id || si.si_id;
  
  const userPrompt = `### Task Info
task_id: ${taskId}
skill: ${si.skill}

### Current Trace
${si.trace}

### Patch
${patch.content}`;

  const response = await callLLM(EXPLORE_ATTRIBUTION_SYSTEM, userPrompt);
  const parsed = parseJsonSafe(response);
  
  if (!parsed) {
    console.error(`  [attr:explore] Failed to parse response for ${patch.filename}`);
    return null;
  }
  
  // Validate fields
  const validWarning = ['avoided', 'violated', 'not_encountered'];
  const validOutcome = ['user_positive', 'positive', 'neutral', 'negative', 'user_negative', null];
  const validScope = ['global', 'local', null];
  
  if (!validWarning.includes(parsed.warning_status)) parsed.warning_status = 'not_encountered';
  // recovered: only meaningful when violated
  if (parsed.warning_status === 'violated') {
    parsed.recovered = typeof parsed.recovered === 'boolean' ? parsed.recovered : false;
  } else {
    parsed.recovered = null;
  }
  if (typeof parsed.alternative_adopted !== 'boolean') parsed.alternative_adopted = false;
  
  if (!parsed.alternative_adopted) {
    parsed.alternative_outcome = null;
    parsed.alternative_scope = null;
  } else {
    if (!validOutcome.includes(parsed.alternative_outcome)) parsed.alternative_outcome = 'neutral';
    if (parsed.alternative_outcome === 'neutral') parsed.alternative_scope = null;
    else if (!validScope.includes(parsed.alternative_scope)) parsed.alternative_scope = 'local';
  }
  
  return {
    unit_file: patch.filename,
    type: 'explore',
    warning_status: parsed.warning_status,
    recovered: parsed.recovered,
    alternative_adopted: parsed.alternative_adopted,
    alternative_outcome: parsed.alternative_outcome,
    alternative_scope: parsed.alternative_scope,
    reasoning: parsed.reasoning || '',
  };
}

// ─── Effect Calculation (code, no LLM) ─────────────────────────

// Outcome score table (5 levels, from strongest positive to strongest negative).
// user_* labels require explicit user text + causal link, so carry 2x weight.
const OUTCOME_SCORES = {
  user_positive: 2.0,
  positive:      1.0,
  neutral:       0,
  negative:     -1.0,
  user_negative: -2.0,
};

function computeExploitEffect(attribution) {
  const base = OUTCOME_SCORES[attribution.outcome] ?? 0;
  const matchMult = { exact: 1.0, broad: 0.5 }[attribution.match] || 0.5;
  const scopeMult = attribution.scope 
    ? ({ global: 1.0, local: 0.5 }[attribution.scope] || 1.0) 
    : 1.0; // neutral → scope=null → 1.0
  
  return base * matchMult * scopeMult;
}

function computeExploreEffect(attribution) {
  // P0-1: violated + recovered → -0.5 (drives eviction via patcher)
  // Agent hit the dead end but self-corrected — the explore unit failed to prevent it
  if (attribution.warning_status === 'violated' && attribution.recovered === true) {
    return -0.5;
  }
  
  // violated + NOT recovered → the dead end stuck, unit warning was ignored
  // Still negative but less: the explore is still relevant (the dead end exists)
  if (attribution.warning_status === 'violated' && attribution.recovered === false) {
    return -0.3;
  }

  // Warning avoided or not encountered: effect comes from alternative only
  if (!attribution.alternative_adopted) return 0;
  
  const base = OUTCOME_SCORES[attribution.alternative_outcome] ?? 0;
  const scopeMult = attribution.alternative_scope
    ? ({ global: 1.0, local: 0.5 }[attribution.alternative_scope] || 1.0)
    : 1.0;
  
  return base * scopeMult;
}

function computeEffect(attribution) {
  if (attribution.type === 'exploit') return computeExploitEffect(attribution);
  if (attribution.type === 'explore') return computeExploreEffect(attribution);
  return 0;
}

// ─── Graduated Coverage Judgment (P0-2) ────────────────────────

const GRADUATED_COVERAGE_SYSTEM = `You are evaluating whether an exploit unit makes an explore unit redundant.

## Context
An explore unit warns about a dead end and suggests alternatives.
An exploit unit provides a proven strategy for a potentially overlapping scenario.
A prior signal (LLM triage or keyword overlap) suggests the exploit may cover the explore's value.

## Your Task
Determine the actual coverage level:

- "full": the exploit directly solves the problem the explore warns about. If agents follow the exploit, they will not hit the explore's dead end. The explore can retire.
- "partial": the exploit addresses a related scenario but the explore still warns about failure modes or edge cases the exploit does not cover. The explore should stay at reduced priority.
- "none": the prior signal was a false positive. The exploit and explore address different problems despite surface-level similarity. No penalty.

## OUTPUT FORMAT
{"coverage": "full|partial|none", "reasoning": "<one sentence>"}

Output ONLY the JSON object.`;

async function judgeGraduatedCoverage(exploreContent, exploitContent) {
  const userPrompt = `### Explore Patch (candidate for retirement)
${exploreContent}

### Exploit Patch (potential replacement)
${exploitContent}`;

  const response = await callLLM(GRADUATED_COVERAGE_SYSTEM, userPrompt);
  const parsed = parseJsonSafe(response);
  if (!parsed || !['full', 'partial', 'none'].includes(parsed.coverage)) {
    return { coverage: 'none', reasoning: 'Failed to parse coverage judgment' };
  }
  return parsed;
}

// ─── Main ──────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  
  let tracesPath = null;
  let unitsDir = null;
  let outputPath = null;
  let modelSpec = null;
  
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--traces':      tracesPath = args[++i]; break;
      case '--eu-dir':
      case '--patches-dir': unitsDir = args[++i]; break;
      case '--output':      outputPath = args[++i]; break;
      case '--model':       modelSpec = args[++i]; break;
    }
  }
  
  if (!tracesPath || !unitsDir || !outputPath) {
    console.error('Usage: node validator.js --traces <file.jsonl> --eu-dir <dir> --output <evidence.jsonl> [--model <provider/model>]');
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
      console.error('[validator] Blocked: privacy.allowRemoteLLM is set to false in evolver-config.json.');
      console.error('[validator] Remove or set "privacy": { "allowRemoteLLM": true } to enable LLM calls.');
      process.exit(0);
    }
  } catch { /* config not found or unreadable — proceed with default (allow) */ }
}

  // Create LLM client
  _llm = createLLMClient(modelSpec);
  
  // Load traces
  const traces = fs.readFileSync(tracesPath, 'utf8')
    .split('\n')
    .filter(Boolean)
    .flatMap((line, i) => {
      try { return [JSON.parse(line)]; }
      catch { console.error(`[validator] Skipped malformed line ${i + 1}`); return []; }
    });
  
  console.error(`[validator] Processing ${traces.length} traces, model=${_llm.model}`);
  console.error(`[validator] Patches dir: ${unitsDir}`);
  
  // Stats
  let triageCount = 0, attrCount = 0, evidenceCount = 0;
  const evidenceEntries = [];
  const today = new Date().toISOString().split('T')[0];
  
  for (const si of traces) {
    console.error(`\n[validator] SI: ${si.si_id} (skill=${si.skill})`);
    
    // Load units for this skill
    const patches = loadSkillUnits(unitsDir, si.skill);
    if (patches.length === 0) {
      console.error(`  [triage] No units for ${si.skill} → skip`);
      continue;
    }
    
    console.error(`  [triage] ${patches.length} units for ${si.skill}`);
    
    // Step 1: Relevance Triage
    let relevant;
    try {
      relevant = await runRelevanceTriage(si, patches);
      triageCount++;
    } catch (err) {
      console.error(`  [triage] Error: ${err.message}`);
      continue;
    }
    
    if (relevant.length === 0) {
      console.error(`  [triage] No relevant units → skip`);
      continue;
    }
    
    console.error(`  [triage] ${relevant.length} relevant: ${relevant.map(r => r.unit_file).join(', ')}`);
    
    // Step 2: Attribution for each relevant unit
    for (const rel of relevant) {
      const patch = patches.find(p => p.filename === rel.unit_file);
      if (!patch) continue;
      
      let attribution;
      try {
        const relSubtype = rel.subtype || rel.type;
        if (relSubtype === 'exploit') {
          attribution = await runExploitAttribution(si, patch);
        } else {
          attribution = await runExploreAttribution(si, patch);
        }
        attrCount++;
      } catch (err) {
        console.error(`  [attr] Error for ${rel.unit_file}: ${err.message}`);
        continue;
      }
      
      if (!attribution) continue;
      
      // Compute effect
      const effect = computeEffect(attribution);
      
      const entry = {
        date: today,
        si_id: si.si_id,
        task_id: si.session_id || si.si_id,
        skill: si.skill,
        ...attribution,
        effect,
      };
      
      evidenceEntries.push(entry);
      evidenceCount++;

      // Emit evidence event
      appendEvent('evidence.add', {
        eu: `${si.skill}/${rel.unit_file}`,
        effect: effect,
        outcome: attribution.outcome || attribution.alternative_outcome || 'unknown',
        trace_si: si.si_id || null,
        source: 'llm',
      });

      const effectStr = effect > 0 ? `+${effect}` : `${effect}`;
      console.error(`  [evidence] ${rel.unit_file}: ${attribution.type} match=${attribution.match || attribution.warning_status} effect=${effectStr}`);
    }
  }
  
  // ── P0-2: note_graduated scan ──────────────────────────────────
  // Dual-source candidates:
  //   1. Exploit frontmatter has source_explore → direct candidate
  //   2. Keyword overlap >= 60% between exploit and explore → fallback candidate
  // Each candidate pair goes through LLM coverage judgment (full/partial/none).
  console.error(`\n[validator] Scanning for graduated explores...`);
  let graduatedCount = 0;
  
  ensureUnitsDir(unitsDir);
  const skillDirs = fs.readdirSync(unitsDir, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.startsWith('_'));
  
  for (const dir of skillDirs) {
    const skillName = dir.name;
    const skillDir = path.join(unitsDir, skillName);
    const unitFiles = fs.readdirSync(skillDir)
      .filter(isActiveUnitFile);
    
    // Load all patches with frontmatter + keywords
    const allUnits = unitFiles.map(pf => {
      const content = fs.readFileSync(path.join(skillDir, pf), 'utf8');
      const fm = parseFrontmatter(content);
      let kws = fm.condition_keywords || [];
      if (typeof kws === 'string') { try { kws = JSON.parse(kws); } catch { kws = []; } }
      return { file: pf, content, fm, kws: kws.map(k => (k+'').toLowerCase()) };
    });
    
    const exploits = allUnits.filter(p => (p.fm.type || '') === 'exploit');
    const explores = allUnits.filter(p => (p.fm.type || '').includes('explore'));
    
    if (exploits.length === 0 || explores.length === 0) continue;
    
    // Build candidate pairs (deduplicated)
    const candidates = new Map(); // key: "exploit::explore" → {exploitPatch, explorePatch, source}
    
    // Source 1: exploit frontmatter has source_explore
    for (const ex of exploits) {
      const se = ex.fm.source_explore;
      if (se && se !== 'none' && se !== '"none"') {
        const xp = explores.find(p => p.file === se);
        if (xp) candidates.set(`${ex.file}::${xp.file}`, { exploit: ex, explore: xp, source: 'frontmatter' });
      }
    }
    
    // Source 2: keyword overlap >= 60% fallback
    for (const ex of exploits) {
      if (ex.kws.length === 0) continue;
      const exSet = new Set(ex.kws);
      for (const xp of explores) {
        if (xp.kws.length === 0) continue;
        const key = `${ex.file}::${xp.file}`;
        if (candidates.has(key)) continue; // already from source 1
        const xpSet = new Set(xp.kws);
        const inter = [...exSet].filter(k => xpSet.has(k)).length;
        const overlap = inter / Math.min(exSet.size, xpSet.size);
        if (overlap >= 0.6) {
          candidates.set(key, { exploit: ex, explore: xp, source: `keyword_overlap_${(overlap*100).toFixed(0)}pct` });
        }
      }
    }
    
    if (candidates.size === 0) continue;
    
    // Check each candidate against existing evidence (dedup)
    const evidencePath = path.join(unitsDir, '..', 'evidence.jsonl');
    let existingEvidence = [];
    if (fs.existsSync(evidencePath)) {
      existingEvidence = fs.readFileSync(evidencePath, 'utf8')
        .split('\n').filter(Boolean).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
    }
    
    for (const [key, cand] of candidates) {
      // Dedup: skip if already judged this pair
      // Double-read unit_file || patch_file: legacy evidence.jsonl entries from
      // before v2.4.0 used patch_file; once they're all aged out, drop fallback.
      const alreadyJudged = existingEvidence.some(e => 
        e.verdict === 'note_graduated' && 
        (e.unit_file || e.patch_file) === cand.explore.file && 
        e.graduated_by === cand.exploit.file
      );
      if (alreadyJudged) continue;
      
      // LLM coverage judgment
      let coverage;
      try {
        coverage = await judgeGraduatedCoverage(cand.explore.content, cand.exploit.content);
      } catch (err) {
        console.error(`  [graduated] LLM error for ${cand.explore.file}: ${err.message}`);
        coverage = { coverage: 'none', reasoning: 'LLM error, skipping' };
      }
      
      // none = false positive, no penalty
      if (coverage.coverage === 'none') {
        console.error(`  ⊘ ${skillName}/${cand.explore.file}: none (${cand.source}) — ${coverage.reasoning}`);
        continue;
      }
      
      const penalty = coverage.coverage === 'full' ? -0.8 : -0.4;
      
      const graduatedEntry = {
        date: today,
        si_id: 'graduated_scan',
        task_id: 'graduated_scan',
        skill: skillName,
        unit_file: cand.explore.file,
        type: 'explore',
        verdict: 'note_graduated',
        graduated_by: cand.exploit.file,
        candidate_source: cand.source,
        coverage: coverage.coverage,
        coverage_reasoning: coverage.reasoning,
        effect: penalty,
      };
      
      evidenceEntries.push(graduatedEntry);
      graduatedCount++;

      // Emit graduated event
      appendEvent('evidence.add', {
        eu: `${skillName}/${cand.explore.file}`,
        effect: penalty,
        outcome: 'graduated',
        trace_si: 'graduated_scan',
        source: 'graduated_coverage',
        coverage: coverage.coverage,
        graduated_by: cand.exploit.file,
      });

      console.error(`  🎓 ${skillName}/${cand.explore.file}: ${coverage.coverage} by ${cand.exploit.file} (${cand.source}, penalty=${penalty})`);
    }
  }
  
  if (graduatedCount > 0) {
    console.error(`[validator] ${graduatedCount} graduated explore(s) found`);
  } else {
    console.error(`[validator] No new graduated explores`);
  }

  // Write evidence
  const output = evidenceEntries.map(e => JSON.stringify(e)).join('\n') + (evidenceEntries.length > 0 ? '\n' : '');
  fs.writeFileSync(outputPath, output);
  
  console.error(`\n[validator] Done: ${triageCount} triaged, ${attrCount} attributed, ${evidenceCount} evidence entries → ${outputPath}`);
}

main().catch(err => {
  console.error(`[validator] Fatal: ${err.message}`);
  process.exit(1);
});
