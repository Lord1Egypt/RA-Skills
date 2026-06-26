#!/usr/bin/env node
/**
 * Contradiction & Drift Scanner
 * 
 * Read guidance files and surface:
 *   - Contradicting directives
 *   - Stale file path references
 *   - Orphaned decisions
 *   - Model/tool name drift
 *   - Unresolved commitments
 *   - Evolution lessons not yet integrated
 * 
 * Usage: node scripts/contradiction-scanner.js [--verbose] [--json]
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.EVOLUTION_TOOLKIT_WORKSPACE
  || (process.env.HOME ? require('path').join(process.env.HOME, '.openclaw/workspace') : process.cwd());
const VERBOSE = process.argv.includes('--verbose');
const JSON_OUT = process.argv.includes('--json');

// ─── Color helpers ────────────────────────────────────────────────────────────
const c = {
  red:    s => `\x1b[31m${s}\x1b[0m`,
  yellow: s => `\x1b[33m${s}\x1b[0m`,
  green:  s => `\x1b[32m${s}\x1b[0m`,
  blue:   s => `\x1b[34m${s}\x1b[0m`,
  cyan:   s => `\x1b[36m${s}\x1b[0m`,
  gray:   s => `\x1b[90m${s}\x1b[0m`,
  bold:   s => `\x1b[1m${s}\x1b[0m`,
  dim:    s => `\x1b[2m${s}\x1b[0m`,
};

// ─── Files to scan ───────────────────────────────────────────────────────────
const GUIDANCE_FILES = [
  'AGENTS.md',
  'SOUL.md',
  'TOOLS.md',
  'MEMORY.md',
  'EVOLUTION.md',
  'HEARTBEAT.md',
  'CURRENT.md',
  'TASKS.md',
  'memory/decisions.md',
  'memory/workflows.md',
  'memory/subagents.md',
].map(f => path.join(WORKSPACE, f));

// ─── Patterns ────────────────────────────────────────────────────────────────

// Directive patterns — sentences that give instructions
const DIRECTIVE_PATTERNS = [
  /\b(always|never|must|should|don't|do not|avoid|NEVER|ALWAYS|MUST)\b.{5,80}/gi,
];

// File path references
const FILE_PATH_PATTERN = /`([^`]+\.(md|js|ts|json|sh|py|txt))`|([/~][^\s,)'"]+\.(md|js|ts|json|sh|py|txt))/g;

// Model name patterns — catch outdated model references
const MODEL_NAMES = {
  current: ['claude-sonnet-4-6', 'claude-haiku', 'gpt-5.4', 'gemini-2.5', 'gemini-3.1'],
  outdated: ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku', 'claude-2', 'gpt-4', 'gpt-3.5', 'opus 4.5', 'sonnet 4.5', 'claude-sonnet-4-5', 'claude-opus-4-5'],
};

// Tool name drift — things that have changed
const TOOL_DRIFT = [
  { old: 'QMD vsearch', current: 'memory_search (semantic)', note: 'vsearch too slow on CPU — use memory_search' },
  { old: 'openclaw gateway REST', current: 'POST /tools/invoke', note: 'documented working' },
];

// Date pattern for stale "as of" claims
const DATE_PATTERN = /(?:as of|since|updated|fixed)\s+(?:Feb|Mar|Jan|Apr|May|Jun)\s+\d{4}|2026-0[1-2]-\d{2}/gi;

// Commitment patterns — things said they'd do
const COMMITMENT_PATTERNS = [
  /\b(?:TODO|FIXME|⚠️.*will|plan to|next time|going to|should add|need to add)\b.{5,100}/gi,
  /\*\*TODO\*\*:.+/g,
];

// ─── Scanner functions ────────────────────────────────────────────────────────

function readFile(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch {
    return null;
  }
}

function extractDirectives(content, source) {
  const directives = [];
  const lines = content.split('\n');
  lines.forEach((line, idx) => {
    for (const pattern of DIRECTIVE_PATTERNS) {
      pattern.lastIndex = 0;
      const matches = line.match(pattern);
      if (matches) {
        matches.forEach(m => {
          // Dedupe — skip if this is a comment or code example
          if (line.trim().startsWith('//') || line.trim().startsWith('#!')) return;
          directives.push({ text: m.trim(), line: idx + 1, source, raw: line.trim() });
        });
      }
    }
  });
  return directives;
}

function extractFilePaths(content, source) {
  const refs = [];
  const lines = content.split('\n');
  lines.forEach((line, idx) => {
    FILE_PATH_PATTERN.lastIndex = 0;
    let match;
    while ((match = FILE_PATH_PATTERN.exec(line)) !== null) {
      const p = match[1] || match[3];
      if (p) refs.push({ path: p, line: idx + 1, source });
    }
  });
  return refs;
}

function checkFilePaths(refs) {
  const broken = [];
  const checked = new Set();
  refs.forEach(ref => {
    const key = ref.path;
    if (checked.has(key)) return;
    checked.add(key);
    
    // Try to resolve relative to workspace
    const candidates = [
      path.join(WORKSPACE, ref.path),
      path.join(WORKSPACE, 'memory', ref.path),
      ref.path, // absolute
    ];
    
    // Skip obviously non-local paths
    if (ref.path.startsWith('http') || ref.path.startsWith('~/.') || 
        ref.path.includes('node_modules') || ref.path.startsWith('/tmp')) return;
    
    const exists = candidates.some(c => {
      try { fs.accessSync(c); return true; } catch { return false; }
    });
    
    if (!exists) {
      broken.push({ ...ref, candidates });
    }
  });
  return broken;
}

function findOutdatedModels(content, source) {
  const findings = [];
  MODEL_NAMES.outdated.forEach(model => {
    const regex = new RegExp(model.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    const lines = content.split('\n');
    lines.forEach((line, idx) => {
      if (regex.test(line)) {
        findings.push({ model, line: idx + 1, source, context: line.trim() });
      }
    });
  });
  return findings;
}

function findCommitments(content, source) {
  const commitments = [];
  const lines = content.split('\n');
  lines.forEach((line, idx) => {
    for (const pattern of COMMITMENT_PATTERNS) {
      pattern.lastIndex = 0;
      if (pattern.test(line)) {
        commitments.push({ text: line.trim(), line: idx + 1, source });
      }
    }
  });
  return commitments;
}

function findDirectiveConflicts(allDirectives) {
  const conflicts = [];
  
  // Deduplicate: remove directives that are identical (same raw text, different stance detected)
  const seen = new Set();
  const dedupedDirectives = allDirectives.filter(d => {
    const key = d.raw.slice(0, 60);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  
  // Pair up directives about the same topic
  const topics = [
    { keywords: ['push', 'main', 'branch', 'git', 'merge'], label: 'Git/branch policy' },
    { keywords: ['supabase', 'management api', 'api.supabase'], label: 'Supabase API' },
    { keywords: ['memory_search', 'qmd', 'search'], label: 'Memory search tool' },
    { keywords: ['codex', 'code', 'coding'], label: 'Code delegation' },
    { keywords: ['model', 'claude', 'sonnet', 'opus', 'haiku'], label: 'Model selection' },
    { keywords: ['browser', 'profile', 'chrome', 'openclaw'], label: 'Browser profile' },
    { keywords: ['twitter', 'x.com', 'tweet'], label: 'Twitter/X access' },
    { keywords: ['cron', 'gateway', 'REST'], label: 'Cron/Gateway' },
    { keywords: ['rm', 'delete', 'trash'], label: 'File deletion' },
  ];
  
  topics.forEach(topic => {
    const relevant = dedupedDirectives.filter(d => 
      topic.keywords.some(k => d.raw.toLowerCase().includes(k))
    );
    
    if (relevant.length < 2) return;
    
    // Look for "never/always" pairs in the same topic
    const nevers = relevant.filter(d => /\bnever\b|\bdo not\b|\bdon't\b|\bavoid\b/i.test(d.text));
    const always = relevant.filter(d => /\balways\b|\bmust\b|\bshould\b/i.test(d.text));
    
    // Check if same action is both required and forbidden
    nevers.forEach(n => {
      always.forEach(a => {
        const nWords = new Set(n.text.toLowerCase().split(/\W+/).filter(w => w.length > 4));
        const aWords = new Set(a.text.toLowerCase().split(/\W+/).filter(w => w.length > 4));
        const shared = [...nWords].filter(w => aWords.has(w) && !['always', 'never', 'should', 'must', 'avoid', 'using', 'with', 'from', 'when', 'that', 'this', 'have', 'been', 'will', 'your', 'they'].includes(w));
        
        // Skip self-conflicts (same sentence contains both always/never about same thing)
        if (n.source === a.source && n.line === a.line) return;
        // Skip if they're essentially the same text
        if (n.raw === a.raw || n.text.slice(0, 40) === a.text.slice(0, 40)) return;
        
        if (shared.length >= 2) {
          conflicts.push({
            topic: topic.label,
            directive1: { ...n, stance: 'PROHIBIT' },
            directive2: { ...a, stance: 'REQUIRE' },
            sharedTerms: shared,
          });
        }
      });
    });
  });
  
  return conflicts;
}

function findEvolvedButNotIntegrated() {
  // Read EVOLUTION.md — check if recent entries (last 30 days) reference a "fix" that 
  // might not be reflected in AGENTS.md/TOOLS.md
  const evolution = readFile(path.join(WORKSPACE, 'EVOLUTION.md'));
  if (!evolution) return [];
  
  const findings = [];
  const lines = evolution.split('\n');
  const recentPattern = /2026-03-\d{2}/;
  
  lines.forEach((line, idx) => {
    if (recentPattern.test(line) && (line.includes('Fix:') || line.includes('Rule:') || line.includes('Always:') || line.includes('Never:'))) {
      // Extract the fix/rule
      const fixMatch = line.match(/(?:Fix|Rule|Always|Never):\s*(.+)/);
      if (fixMatch) {
        findings.push({
          rule: fixMatch[1].trim(),
          line: idx + 1,
          source: 'EVOLUTION.md',
          note: 'Recent lesson — verify it\'s in AGENTS.md',
        });
      }
    }
  });
  
  return findings;
}

function findStaleDateClaims(content, source) {
  const stale = [];
  const lines = content.split('\n');
  const cutoff = new Date('2026-02-01');
  
  lines.forEach((line, idx) => {
    const matches = line.match(DATE_PATTERN);
    if (!matches) return;
    
    matches.forEach(match => {
      // Try to parse the date
      const dateStr = match.match(/2026-\d{2}-\d{2}/);
      if (dateStr) {
        const d = new Date(dateStr[0]);
        const daysSince = (Date.now() - d.getTime()) / (1000 * 60 * 60 * 24);
        if (daysSince > 14) {
          stale.push({ claim: match, context: line.trim(), line: idx + 1, source, daysSince: Math.round(daysSince) });
        }
      }
    });
  });
  
  return stale;
}

function detectModelInconsistency(allContent) {
  // Check if MEMORY.md, AGENTS.md, and workflows.md agree on the current model
  const modelMentions = {};
  
  ['AGENTS.md', 'MEMORY.md', 'memory/workflows.md'].forEach(file => {
    const content = readFile(path.join(WORKSPACE, file));
    if (!content) return;
    
    MODEL_NAMES.current.forEach(model => {
      const count = (content.match(new RegExp(model, 'gi')) || []).length;
      if (count > 0) {
        if (!modelMentions[model]) modelMentions[model] = {};
        modelMentions[model][file] = count;
      }
    });
  });
  
  return modelMentions;
}

// ─── Main ─────────────────────────────────────────────────────────────────────

function main() {
  const results = {
    scannedFiles: [],
    brokenPaths: [],
    outdatedModels: [],
    conflicts: [],
    commitments: [],
    evolvedNotIntegrated: [],
    staleDateClaims: [],
    modelMap: {},
    summary: {},
  };
  
  if (!JSON_OUT) {
    console.log(c.bold('\n∴ CONTRADICTION & DRIFT SCANNER'));
    console.log(c.gray('Ergo self-knowledge tool | 2026-03-10'));
    console.log(c.gray('─'.repeat(60)));
  }
  
  // Collect all directives from all files
  let allDirectives = [];
  let allFilePaths = [];
  
  GUIDANCE_FILES.forEach(filePath => {
    const content = readFile(filePath);
    if (!content) {
      if (VERBOSE) console.log(c.gray(`  ⊘ ${path.relative(WORKSPACE, filePath)} (not found)`));
      return;
    }
    
    const relPath = path.relative(WORKSPACE, filePath);
    results.scannedFiles.push(relPath);
    
    const directives = extractDirectives(content, relPath);
    const filePaths = extractFilePaths(content, relPath);
    const outdated = findOutdatedModels(content, relPath);
    const commits = findCommitments(content, relPath);
    const stale = findStaleDateClaims(content, relPath);
    
    allDirectives = allDirectives.concat(directives);
    allFilePaths = allFilePaths.concat(filePaths);
    results.outdatedModels = results.outdatedModels.concat(outdated);
    results.commitments = results.commitments.concat(commits);
    results.staleDateClaims = results.staleDateClaims.concat(stale);
  });
  
  // Check file paths — filter out obvious template placeholders
  const templatePatterns = /YYYY-MM-DD|<name>|<feature|\/path\/to\/|\*\./;
  results.brokenPaths = checkFilePaths(allFilePaths)
    .filter(b => !templatePatterns.test(b.path));
  
  // Find directive conflicts
  results.conflicts = findDirectiveConflicts(allDirectives);
  
  // Find evolved-but-not-integrated lessons
  results.evolvedNotIntegrated = findEvolvedButNotIntegrated();
  
  // Model consistency map
  results.modelMap = detectModelInconsistency();
  
  // ─── Output ─────────────────────────────────────────────────────────────────
  
  if (JSON_OUT) {
    console.log(JSON.stringify(results, null, 2));
    return;
  }
  
  // Files scanned
  console.log(c.cyan(`\n📂 Scanned ${results.scannedFiles.length} guidance files`));
  if (VERBOSE) results.scannedFiles.forEach(f => console.log(c.gray(`   ${f}`)));
  console.log(c.gray(`   ${allDirectives.length} directives extracted | ${allFilePaths.length} file path refs found`));
  
  // ── Section 1: Broken paths
  console.log(c.bold('\n─── 📁 BROKEN FILE REFERENCES ─────────────────────────────'));
  if (results.brokenPaths.length === 0) {
    console.log(c.green('  ✓ No broken file references found'));
  } else {
    results.brokenPaths.slice(0, 20).forEach(b => {
      console.log(c.red(`  ✗ ${b.path}`));
      console.log(c.gray(`    → referenced in ${b.source} (line ${b.line})`));
    });
    if (results.brokenPaths.length > 20) {
      console.log(c.gray(`  ... and ${results.brokenPaths.length - 20} more`));
    }
  }
  
  // ── Section 2: Outdated models
  console.log(c.bold('\n─── 🤖 OUTDATED MODEL REFERENCES ──────────────────────────'));
  if (results.outdatedModels.length === 0) {
    console.log(c.green('  ✓ No outdated model references found'));
  } else {
    const byModel = {};
    results.outdatedModels.forEach(m => {
      if (!byModel[m.model]) byModel[m.model] = [];
      byModel[m.model].push(m);
    });
    Object.entries(byModel).forEach(([model, instances]) => {
      console.log(c.yellow(`  ⚠ "${model}" (${instances.length} mention${instances.length > 1 ? 's' : ''})`));
      if (VERBOSE) instances.forEach(i => 
        console.log(c.gray(`    ${i.source}:${i.line} → ${i.context.slice(0, 80)}`))
      );
    });
  }
  
  // ── Section 3: Directive conflicts
  console.log(c.bold('\n─── ⚡ POTENTIAL DIRECTIVE CONFLICTS ───────────────────────'));
  if (results.conflicts.length === 0) {
    console.log(c.green('  ✓ No obvious directive conflicts detected'));
  } else {
    results.conflicts.forEach((conflict, i) => {
      console.log(c.yellow(`\n  ${i + 1}. Topic: ${c.bold(conflict.topic)}`));
      console.log(c.red(`     PROHIBIT: "${conflict.directive1.text.slice(0, 90)}"`));
      console.log(c.gray(`       → ${conflict.directive1.source}:${conflict.directive1.line}`));
      console.log(c.cyan(`     REQUIRE:  "${conflict.directive2.text.slice(0, 90)}"`));
      console.log(c.gray(`       → ${conflict.directive2.source}:${conflict.directive2.line}`));
      console.log(c.dim(`     Shared terms: [${conflict.sharedTerms.slice(0, 5).join(', ')}]`));
    });
  }
  
  // ── Section 4: Open commitments
  console.log(c.bold('\n─── 📌 OPEN COMMITMENTS / TODOS ────────────────────────────'));
  const importantCommits = results.commitments.filter(c => 
    !c.source.includes('EVOLUTION') && c.text.length > 15
  ).slice(0, 15);
  
  if (importantCommits.length === 0) {
    console.log(c.green('  ✓ No open commitments found in guidance files'));
  } else {
    importantCommits.forEach(commit => {
      console.log(c.yellow(`  → ${commit.text.slice(0, 100)}`));
      console.log(c.gray(`    ${commit.source}:${commit.line}`));
    });
  }
  
  // ── Section 5: Recent EVOLUTION lessons
  console.log(c.bold('\n─── 🧬 RECENT EVOLUTION LESSONS TO INTEGRATE ──────────────'));
  if (results.evolvedNotIntegrated.length === 0) {
    console.log(c.green('  ✓ No recent lessons flagged'));
  } else {
    results.evolvedNotIntegrated.forEach(lesson => {
      console.log(c.cyan(`  ★ "${lesson.rule.slice(0, 100)}"`));
      console.log(c.gray(`    ${lesson.source}:${lesson.line} — ${lesson.note}`));
    });
  }
  
  // ── Section 6: Stale date claims
  console.log(c.bold('\n─── 📅 POTENTIALLY STALE DATE CLAIMS ──────────────────────'));
  const mostStale = results.staleDateClaims
    .filter(s => s.daysSince > 20)
    .sort((a, b) => b.daysSince - a.daysSince)
    .slice(0, 10);
  
  if (mostStale.length === 0) {
    console.log(c.green('  ✓ No very stale date claims found'));
  } else {
    mostStale.forEach(s => {
      console.log(c.dim(`  ⏱ ${s.claim} (${s.daysSince}d ago) — ${s.source}:${s.line}`));
      if (VERBOSE) console.log(c.gray(`    context: ${s.context.slice(0, 80)}`));
    });
  }
  
  // ── Section 7: Model consistency
  console.log(c.bold('\n─── 🗺  MODEL REFERENCE MAP ────────────────────────────────'));
  Object.entries(results.modelMap).forEach(([model, files]) => {
    const fileStr = Object.entries(files).map(([f, n]) => `${path.basename(f)}(×${n})`).join(', ');
    console.log(c.gray(`  ${model}: ${fileStr}`));
  });
  
  // ── Summary
  const totalIssues = results.brokenPaths.length + results.outdatedModels.length + 
                      results.conflicts.length + importantCommits.length + 
                      results.evolvedNotIntegrated.length;
  
  console.log(c.bold('\n─── SUMMARY ────────────────────────────────────────────────'));
  console.log(`  ${results.brokenPaths.length > 0 ? c.red('✗') : c.green('✓')} Broken file refs:      ${results.brokenPaths.length}`);
  console.log(`  ${results.outdatedModels.length > 0 ? c.yellow('⚠') : c.green('✓')} Outdated model refs:   ${results.outdatedModels.length}`);
  console.log(`  ${results.conflicts.length > 0 ? c.yellow('⚠') : c.green('✓')} Directive conflicts:   ${results.conflicts.length}`);
  console.log(`  ${importantCommits.length > 0 ? c.yellow('⚠') : c.green('✓')} Open commitments:      ${importantCommits.length}`);
  console.log(`  ${results.evolvedNotIntegrated.length > 0 ? c.cyan('★') : c.green('✓')} Evolution to integrate: ${results.evolvedNotIntegrated.length}`);
  console.log(`  ${mostStale.length > 0 ? c.dim('⏱') : c.green('✓')} Stale date claims:     ${mostStale.length}`);
  
  // Weighted scoring: conflicts are worst, stale dates are minor
  const weightedIssues = results.brokenPaths.length * 2 + 
                          results.outdatedModels.length * 3 +
                          results.conflicts.length * 4 +
                          importantCommits.length * 1 +
                          results.evolvedNotIntegrated.length * 2;
  const score = Math.max(0, 100 - weightedIssues);
  const scoreColor = score > 80 ? c.green : score > 60 ? c.yellow : c.red;
  console.log(c.bold(`\n  Coherence score: ${scoreColor(score + '/100')}`));
  
  if (totalIssues === 0) {
    console.log(c.green(c.bold('\n  ∴ System is internally consistent. Good state.\n')));
  } else {
    console.log(c.gray(`\n  Run with --verbose for full context on each issue.\n`));
  }
}

main();
