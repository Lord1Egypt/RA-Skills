#!/usr/bin/env node
/**
 * trace-extractor.js — v2.0 Daily Mode
 * 
 * Extracts formatted traces from OpenClaw session transcripts.
 * Implements Skill Invocation (SI) detection and trace formatting.
 * 
 * Design: §11.3.1b (SI cutting) + §10.4 (trace formatting)
 * 
 * Usage:
 *   node trace-extractor.js --sessions-dir <path> [--output <path>] [--window-days 7] [--since <ISO>] [--max-si 20]
 *   node trace-extractor.js --session-file <path> [--output <path>]
 * 
 * Output: JSONL file with one SI per line:
 *   {"si_id", "skill", "session_id", "start_ts", "end_ts", "user_intent", "trace", "trace_steps", "anchor_count"}
 */

'use strict';

const fs = require('fs');
const path = require('path');

const { getAdapter } = require('./lib/platform-detect');
const { OpenClawAdapter } = require('./adapters/openclaw');
const { getBlockedSkills } = require('./lib/blocklist');

const BLOCKED_SKILLS = getBlockedSkills();

// ─── Configuration ─────────────────────────────────────────────

// Session filenames starting with these prefixes are evolver's own test/
// smoke sessions. They don't contain real user skill invocations and
// would pollute processed_sessions and trace statistics if processed.
const EVOLVER_INTERNAL_SESSION_PATTERN = /^(evolver-|test-evolver-)/;

function isEvolverInternalSession(filename) {
  return EVOLVER_INTERNAL_SESSION_PATTERN.test(filename);
}

const LOOKAHEAD = 15;           // Messages after anchor to consider as "skill related"
const MAX_READS_PER_SI = 5;     // Max SKILL.md reads before forcing new SI
const MERGE_GAP = 5;            // Merge same-skill anchors if gap ≤ N messages
const WINDOW_END_SILENT = 3;    // N consecutive non-toolCall assistant msgs = end
const WINDOW_HARD_LIMIT = 50;   // Max messages after last anchor

// toolResult dynamic limits by step count
const RESULT_LIMITS = [
  { maxSteps: 5,  limit: 800 },
  { maxSteps: 15, limit: 400 },
  { maxSteps: 30, limit: 200 },
  { maxSteps: Infinity, limit: 100 },
];

const MAX_TRACE_CHARS = 6000;

// ─── Session Parsing ───────────────────────────────────────────

/**
 * Parse a session JSONL file into structured messages.
 * Returns array of {idx, type, role, content, timestamp, toolName, isError, raw}
 */
/** Default adapter for backward compatibility */
const defaultAdapter = new OpenClawAdapter();

function parseSessionFile(filePath, adapter) {
  const a = adapter || defaultAdapter;
  const lines = fs.readFileSync(filePath, 'utf8').split('\n').filter(Boolean);
  const raw = [];
  
  for (const line of lines) {
    let entry;
    try { entry = JSON.parse(line); } catch { continue; }
    if (!a.isMessageEntry(entry)) continue;
    raw.push(entry);
  }
  
  const messages = raw.map((entry, idx) => a.normalizeEntry(entry, idx));
  return a.postProcess(messages);
}

/**
 * Parse a PB benchmark task entry (already structured, not JSONL).
 */
function parseBenchTask(task) {
  const messages = [];
  for (const entry of (task.transcript || [])) {
    if (entry.type !== 'message') continue;
    const msg = entry.message || {};
    messages.push({
      idx: messages.length,
      type: 'message',
      role: msg.role || '',
      content: msg.content || [],
      timestamp: entry.timestamp || '',
      toolName: msg.toolName || null,
      toolCallId: msg.toolCallId || null,
      isError: msg.isError || false,
      raw: msg,
    });
  }
  return messages;
}

// ─── SI Detection (§11.3.1b) ───────────────────────────────────

/**
 * Detect SKILL.md read anchors in messages.
 * Returns [{msgIdx, skill, readPath}]
 */
function detectAnchors(messages, adapter) {
  const a = adapter || defaultAdapter;
  const anchors = [];
  
  for (let i = 0; i < messages.length; i++) {
    const { detected, skillName } = a.isSkillActivation(messages[i]);
    if (detected) {
      anchors.push({ msgIdx: i, skill: skillName });
    }
  }
  
  return anchors;
}

/**
 * Group anchors into Skill Invocations.
 * Same skill consecutive anchors (gap ≤ MERGE_GAP) → merge.
 * Max MAX_READS_PER_SI reads per SI.
 */
function groupAnchorsIntoSIs(anchors, messages) {
  if (anchors.length === 0) return [];
  
  const groups = [];
  let current = { skill: anchors[0].skill, anchors: [anchors[0]] };
  
  for (let i = 1; i < anchors.length; i++) {
    const prev = current.anchors[current.anchors.length - 1];
    const curr = anchors[i];
    
    const isSameSkill = curr.skill === current.skill;
    const gap = curr.msgIdx - prev.msgIdx;
    const withinMerge = gap <= MERGE_GAP;
    const withinLimit = current.anchors.length < MAX_READS_PER_SI;
    
    if (isSameSkill && withinMerge && withinLimit) {
      current.anchors.push(curr);
    } else {
      groups.push(current);
      current = { skill: curr.skill, anchors: [curr] };
    }
  }
  groups.push(current);
  
  return groups;
}

/**
 * Define SI window [start, end] for each group.
 */
function defineWindows(groups, messages) {
  const sis = [];
  
  for (let gi = 0; gi < groups.length; gi++) {
    const group = groups[gi];
    const firstAnchor = group.anchors[0].msgIdx;
    const lastAnchor = group.anchors[group.anchors.length - 1].msgIdx;
    
    // Start: look backward for nearest user message (up to 3 messages back)
    let start = firstAnchor;
    for (let j = firstAnchor - 1; j >= Math.max(0, firstAnchor - 3); j--) {
      if (messages[j].role === 'user') {
        start = j;
        break;
      }
    }
    
    // End: earliest of:
    //   a) Next different skill's anchor
    //   b) N consecutive non-toolCall assistant messages after last anchor
    //   c) Session end
    //   d) Hard limit after last anchor
    
    let end = messages.length - 1;
    
    // (a) Next group's first anchor
    if (gi + 1 < groups.length) {
      end = Math.min(end, groups[gi + 1].anchors[0].msgIdx - 1);
    }
    
    // (d) Hard limit
    end = Math.min(end, lastAnchor + WINDOW_HARD_LIMIT);
    
    // (b) Silent assistant detection (after last anchor)
    let silentCount = 0;
    for (let j = lastAnchor + 1; j <= end; j++) {
      const msg = messages[j];
      if (msg.role === 'assistant') {
        const hasToolCall = msg.content.some(c => c.type === 'toolCall');
        if (!hasToolCall) {
          silentCount++;
          if (silentCount >= WINDOW_END_SILENT) {
            end = j;
            break;
          }
        } else {
          silentCount = 0;
        }
      }
    }
    
    // Extract user intent (first user message in window)
    let userIntent = '';
    for (let j = start; j <= Math.min(start + 3, end); j++) {
      if (messages[j].role === 'user') {
        for (const c of messages[j].content) {
          if (c.type === 'text' && c.text) {
            userIntent = c.text.substring(0, 200);
            break;
          }
        }
        if (userIntent) break;
      }
    }
    
    // Include 1-2 user messages after end for feedback signal
    let feedbackEnd = end;
    let feedbackCount = 0;
    for (let j = end + 1; j < messages.length && feedbackCount < 2; j++) {
      if (messages[j].role === 'user') {
        feedbackEnd = j;
        feedbackCount++;
      }
      // Stop if we hit another skill anchor
      if (messages[j].role === 'assistant') {
        const hasSkillRead = messages[j].content.some(c => 
          c.type === 'toolCall' && c.name === 'read' && 
          ((c.arguments || {}).path || '').includes('SKILL.md')
        );
        if (hasSkillRead) break;
      }
    }
    
    sis.push({
      skill: group.skill,
      anchors: group.anchors,
      start,
      end: feedbackEnd,
      traceEnd: end,  // actual SI end (before feedback)
      userIntent,
    });
  }
  
  return sis;
}

// ─── Trace Formatting (§10.4) ──────────────────────────────────

/**
 * Count tool call steps in a message range.
 */
function countSteps(messages, start, end) {
  let steps = 0;
  for (let i = start; i <= end && i < messages.length; i++) {
    if (messages[i].role === 'assistant') {
      if (messages[i].content.some(c => c.type === 'toolCall')) steps++;
    }
  }
  return steps;
}

/**
 * Get toolResult character limit based on step count.
 */
function getResultLimit(steps) {
  for (const r of RESULT_LIMITS) {
    if (steps <= r.maxSteps) return r.limit;
  }
  return 100;
}

/**
 * Format messages into trace text.
 */
function formatTrace(messages, start, end, skill) {
  const steps = countSteps(messages, start, end);
  const resultLimit = getResultLimit(steps);
  const lines = [];
  
  // Build set of toolCall IDs that read SKILL.md (for exact match filtering)
  const skillReadIds = new Set();
  for (let i = start; i <= end && i < messages.length; i++) {
    const msg = messages[i];
    if (msg.role !== 'assistant') continue;
    for (const c of msg.content) {
      if (c.type === 'toolCall' && (c.name === 'read' || c.name === 'Read')) {
        const p = (c.arguments || {}).path || (c.arguments || {}).file_path || '';
        if (p.match(/SKILL\.md$/i)) skillReadIds.add(c.id);
      }
    }
  }
  
  // Track if this is the last assistant text (no limit)
  let lastAssistantTextIdx = -1;
  for (let i = end; i >= start; i--) {
    if (messages[i].role === 'assistant') {
      if (messages[i].content.some(c => c.type === 'text' && c.text && c.text.trim())) {
        lastAssistantTextIdx = i;
        break;
      }
    }
  }
  
  for (let i = start; i <= end && i < messages.length; i++) {
    const msg = messages[i];
    
    for (const c of msg.content) {
      if (!c || typeof c !== 'object') continue;
      
      switch (c.type) {
        case 'text': {
          if (msg.role === 'user') {
            const text = (c.text || '').trim();
            if (text) lines.push(`USER: ${text}`);
          } else if (msg.role === 'assistant') {
            const text = (c.text || '').trim();
            if (text) lines.push(`AGENT: ${text}`);
          } else if (msg.role === 'toolResult') {
            let text = c.text || '';
            
            // Skip SKILL.md content — exact match via toolCallId
            if (msg.toolCallId && skillReadIds.has(msg.toolCallId)) {
              lines.push('RESULT: [SKILL.md content omitted]');
              continue;
            }
            
            // Dynamic limit (error gets 2x)
            const lim = msg.isError ? resultLimit * 2 : resultLimit;
            
            // Last assistant text has no limit (but it's on assistant, not toolResult)
            if (text.length > lim) {
              text = text.substring(0, lim) + `... [${text.length} chars total]`;
            }
            
            const prefix = msg.isError ? 'ERROR' : 'RESULT';
            lines.push(`${prefix}: ${text}`);
          }
          break;
        }
        
        case 'thinking':
          // Discard
          break;
          
        case 'toolCall': {
          const name = c.name || '?';
          let args = JSON.stringify(c.arguments || {}, null, 0);
          if (args.length > 300) args = args.substring(0, 300) + '...';
          lines.push(`CALL ${name}(${args})`);
          break;
        }
      }
    }
  }
  
  let trace = lines.join('\n');
  
  // Final size cap
  if (trace.length > MAX_TRACE_CHARS) {
    trace = trace.substring(0, MAX_TRACE_CHARS) + `\n... [truncated at ${MAX_TRACE_CHARS} chars]`;
  }
  
  return { trace, steps };
}

// ─── Main Pipeline ─────────────────────────────────────────────

/**
 * Extract SIs from a single session file.
 * Returns array of SI objects ready for output.
 */
function extractFromSession(sessionFile, adapter) {
  const messages = parseSessionFile(sessionFile, adapter);
  if (messages.length === 0) return [];
  
  const sessionId = path.basename(sessionFile, '.jsonl').substring(0, 12);
  const anchors = detectAnchors(messages, adapter);
  if (anchors.length === 0) return [];
  
  const groups = groupAnchorsIntoSIs(anchors, messages);
  const windows = defineWindows(groups, messages);
  
  const results = [];
  for (let i = 0; i < windows.length; i++) {
    const si = windows[i];
    const { trace, steps } = formatTrace(messages, si.start, si.end, si.skill);
    
    // Skip trivial SIs (no actual execution)
    if (steps === 0) continue;
    
    results.push({
      si_id: `si_${sessionId}_${String(i).padStart(2, '0')}`,
      skill: si.skill,
      session_id: sessionId,
      start_ts: messages[si.start].timestamp || '',
      end_ts: messages[si.end].timestamp || '',
      user_intent: si.userIntent,
      trace,
      trace_steps: steps,
      anchor_count: si.anchors.length,
    });
  }
  
  return results;
}

/**
 * Extract SIs from a PB benchmark results file.
 * Each task = 1 SI (no cutting needed).
 */
function extractFromBenchFile(benchFile) {
  const data = JSON.parse(fs.readFileSync(benchFile, 'utf8'));
  const tasks = data.tasks || [];
  const results = [];
  
  for (const task of tasks) {
    const skill = (task.frontmatter || {}).skill_target;
    if (!skill) continue;
    
    const messages = parseBenchTask(task);
    if (messages.length === 0) continue;
    
    const steps = countSteps(messages, 0, messages.length - 1);
    if (steps === 0) continue;
    
    const { trace } = formatTrace(messages, 0, messages.length - 1, skill);
    
    const score = (task.grading && task.grading.runs && task.grading.runs[0])
      ? task.grading.runs[0].score : null;
    
    // User intent: first user message
    let userIntent = '';
    for (const msg of messages) {
      if (msg.role === 'user') {
        for (const c of msg.content) {
          if (c.type === 'text') { userIntent = (c.text || '').substring(0, 200); break; }
        }
        if (userIntent) break;
      }
    }
    
    results.push({
      si_id: `si_bench_${task.task_id}`,
      skill,
      session_id: task.task_id,
      start_ts: messages[0].timestamp || '',
      end_ts: messages[messages.length - 1].timestamp || '',
      user_intent: userIntent,
      trace,
      trace_steps: steps,
      anchor_count: 0,  // bench tasks don't have explicit anchors
      score,             // bench-specific: grading score
    });
  }
  
  return results;
}

// ─── CLI ───────────────────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);
  
  let sessionsDirs = [];  // supports multiple dirs (comma-separated or repeated flag)
  let sessionFile = null;
  let benchFile = null;
  let output = null;
  let windowDays = 7;
  let sinceTs = null;   // ISO timestamp — takes priority over windowDays
  let maxSI = 0;        // 0 = unlimited
  let skipSI = 0;       // skip first N SIs (for carry-over resume)
  let countOnly = false; // --count-only: output JSON count to stdout, no trace extraction
  let filterSkill = null; // --filter-skill <name>: only keep SIs for one skill
  
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--sessions-dir': 
        // Support comma-separated and repeated flags
        (args[++i] || '').split(',').forEach(d => { if (d.trim()) sessionsDirs.push(d.trim()); });
        break;
      case '--session-file': sessionFile = args[++i]; break;
      case '--bench-file':   benchFile = args[++i]; break;
      case '--output':       output = args[++i]; break;
      case '--window-days':  windowDays = parseInt(args[++i]) || 7; break;
      case '--since':        sinceTs = args[++i]; break;
      case '--max-si':       maxSI = parseInt(args[++i]) || 0; break;
      case '--skip-si':      skipSI = parseInt(args[++i]) || 0; break;
      case '--count-only':   countOnly = true; break;
      case '--filter-skill': filterSkill = args[++i] || null; break;
    }
  }
  
  let allSIs = [];
  const adapter = getAdapter();
  console.error(`[trace-extractor] Platform: ${adapter.name}`);
  
  if (benchFile) {
    // PB benchmark mode
    allSIs = extractFromBenchFile(benchFile);
    if (filterSkill) allSIs = allSIs.filter(si => si.skill === filterSkill);
    if (BLOCKED_SKILLS.size) allSIs = allSIs.filter(si => !BLOCKED_SKILLS.has(si.skill));
    console.error(`[trace-extractor] Bench mode: ${allSIs.length} SIs from ${benchFile}${filterSkill ? ` (filter: skill=${filterSkill})` : ''}`);
    
  } else if (sessionFile) {
    // Single session file
    allSIs = extractFromSession(sessionFile, adapter);
    if (filterSkill) allSIs = allSIs.filter(si => si.skill === filterSkill);
    if (BLOCKED_SKILLS.size) allSIs = allSIs.filter(si => !BLOCKED_SKILLS.has(si.skill));
    console.error(`[trace-extractor] Single session: ${allSIs.length} SIs from ${sessionFile}${filterSkill ? ` (filter: skill=${filterSkill})` : ''}`);
    
  } else if (sessionsDirs.length > 0) {
    // Multi-session scan (incremental or windowed), supports multiple dirs
    const cutoff = sinceTs 
      ? new Date(sinceTs).getTime() 
      : Date.now() - windowDays * 24 * 3600 * 1000;
    const cutoffLabel = sinceTs ? `since ${sinceTs}` : `${windowDays}d window`;
    
    // Collect files from all session dirs
    let allFiles = [];
    for (const dir of sessionsDirs) {
      if (!fs.existsSync(dir)) {
        console.error(`[trace-extractor] Warning: sessions dir not found: ${dir}`);
        continue;
      }
      const files = fs.readdirSync(dir)
        .filter(f => f.endsWith('.jsonl'))
        .filter(f => !isEvolverInternalSession(f))
        .map(f => {
          const fullPath = path.join(dir, f);
          const stat = fs.statSync(fullPath);
          return { path: fullPath, mtime: stat.mtimeMs };
        })
        .filter(f => f.mtime >= cutoff);
      allFiles.push(...files);
    }
    allFiles.sort((a, b) => b.mtime - a.mtime);
    
    console.error(`[trace-extractor] Scanning ${allFiles.length} sessions from ${sessionsDirs.length} dir(s) (${cutoffLabel})`);
    
    for (const file of allFiles) {
      try {
        let sis = extractFromSession(file.path, adapter);
        // Apply --filter-skill before maxSI accounting so the cap counts only matching SIs.
        if (filterSkill) sis = sis.filter(si => si.skill === filterSkill);
        // Drop SIs for user-blocked skills (no new EUs generated for them).
        if (BLOCKED_SKILLS.size) sis = sis.filter(si => !BLOCKED_SKILLS.has(si.skill));
        allSIs.push(...sis);
      } catch (err) {
        console.error(`[trace-extractor] Error processing ${file.path}: ${err.message}`);
      }
      // Early exit if maxSI reached
      if (maxSI > 0 && allSIs.length >= maxSI) {
        allSIs = allSIs.slice(0, maxSI);
        console.error(`[trace-extractor] Reached maxSI limit (${maxSI}), stopping`);
        break;
      }
    }
    
    if (filterSkill) {
      console.error(`[trace-extractor] Filter: skill=${filterSkill}`);
    }
    console.error(`[trace-extractor] Total: ${allSIs.length} SIs`);
    
  } else {
    console.error('Usage: node trace-extractor.js --sessions-dir <path> | --session-file <path> | --bench-file <path>');
    process.exit(1);
  }
  
  // Apply skip-si for carry-over resume (skip already-processed SIs)
  if (skipSI > 0 && !countOnly) {
    const before = allSIs.length;
    allSIs = allSIs.slice(skipSI);
    console.error(`[trace-extractor] Skipped ${Math.min(skipSI, before)} SIs (carry-over offset), ${allSIs.length} remaining`);
  }
  
  // Output
  if (countOnly) {
    // --count-only: emit JSON summary to stdout for monitor.js consumption
    const skillCounts = {};
    for (const si of allSIs) {
      skillCounts[si.skill] = (skillCounts[si.skill] || 0) + 1;
    }
    const summary = { count: allSIs.length, skills: skillCounts };
    process.stdout.write(JSON.stringify(summary) + '\n');
    console.error(`[trace-extractor] Count-only: ${allSIs.length} SIs across ${Object.keys(skillCounts).length} skills`);
  } else {
    const jsonlLines = allSIs.map(si => JSON.stringify(si));
    const outputText = jsonlLines.join('\n') + (jsonlLines.length > 0 ? '\n' : '');
    
    if (output) {
      fs.writeFileSync(output, outputText);
      console.error(`[trace-extractor] Written ${allSIs.length} SIs to ${output}`);
    } else {
      process.stdout.write(outputText);
    }
  }
}

main();
