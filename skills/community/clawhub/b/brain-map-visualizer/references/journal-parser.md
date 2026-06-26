---
title: "OC Brain Map — Journal Parser Script"
created: 2026-03-17
modified: 2026-04-17
tags: [brain-map, journal, parser, node-script]
status: active
---

# Journal Parser — `scripts/build-brain-map-projects.js`

Parses `memory/journal/*.md` session files, maps sessions to 13 named attention projects via keyword matching, builds per-project co-access graphs with momentum fields and edge directionality, and writes `data/brain-map-projects.json`.

Copy this script to `scripts/build-brain-map-projects.js` in your Mission Control or host app. Adjust `WORKSPACE_DIR` and `OUTPUT_PATH` via environment variables.

---

## Configuration

```bash
# Override defaults via environment variables before running
WORKSPACE_DIR=/path/to/your/vault node scripts/build-brain-map-projects.js
OUTPUT_PATH=/path/to/output/brain-map-projects.json node scripts/build-brain-map-projects.js
```

Defaults:
- `WORKSPACE_DIR` → `~/.openclaw/vault`
- `OUTPUT_PATH` → `data/brain-map-projects.json` relative to the script's directory

---

## Project Definitions

The parser maps sessions to 13 named attention categories. Each category has a label, color, and keyword list. Sessions matching keywords are attributed to that project; file co-access within those sessions builds the edges.

| ID | Label | Color |
|---|---|---|
| `memory-system` | Memory System | Gold `#c8a84b` |
| `ghost-publishing` | Ghost Publishing | Green `#22c55e` |
| `ghost-publishing-pro` | Ghost Publishing Pro Skill | Emerald `#34d399` |
| `youtube` | YouTube | Red `#ef4444` |
| `mission-control` | Mission Control | Blue `#60a5fa` |
| `brain-map-skill` | Brain Map Skill | Purple `#a78bfa` |
| `github` | GitHub | White `#f0f6ff` |
| `cron-automation` | Cron + Automation | Orange `#fb923c` |
| `model-stack` | Model Stack | Fuchsia `#e879f9` |
| `hno-business` | HNO Business | Pink `#ec4899` |
| `finances` | Finances + Bitcoin | Amber `#fbbf24` |
| `the-desk` | The Desk | Tan `#d4a373` |
| `second-brain` | Second Brain | Cyan `#67e8f9` |

Sessions not matching any category fall back to `mission-control`.

### Customizing for your agent

The `PROJECT_DEFS` array at the top of the script is the only thing you need to change to adapt the Brain Map to your vault. Replace the keyword lists with terms that reflect your actual work. The category names and colors are arbitrary — use whatever groupings make sense for your attention patterns.

If a journal entry has a `## Project` block, that label takes priority over keyword inference:

```markdown
## Project
Ghost Publishing
```

This lets you manually attribute sessions that keyword matching would misclassify.

---

## File Extraction

The parser uses a two-pass strategy to find which markdown files were accessed in each session:

**Pass 1 — `## Files Accessed` block (preferred)**

If the journal has an explicit files list under `## Files Accessed`, the parser reads it directly. This is accurate and fast.

```markdown
## Files Accessed
- MEMORY.md
- memory/recent.md
- skills/ghost-publishing-pro/SKILL.md
```

**Pass 2 — transcript regex fallback**

If the `## Files Accessed` block is absent or has fewer than 3 entries, the parser scans the full transcript text for `.md` filename references using a regex. Less precise but catches sessions without structured file lists.

The more consistently you write `## Files Accessed` blocks in your journals, the more accurate the graph becomes.

---

## Edge Computation

For each project, edges are built from file co-access within sessions:

- Any two files appearing in the same session get an edge (or increment an existing one)
- `weight` = number of sessions where both files appeared
- `recentCount` = weight for sessions in the last 30 days
- `lifetimeCount` = same as weight
- `spanDays` = days between project's first and last session

**Edge directionality** is computed from session order:

- For each session, the parser records which file appeared first in the `## Files Accessed` list
- Across all sessions, a majority vote determines `fromId` (typically accessed first) and `toId` (typically accessed later)
- `fromId`/`toId` reflect cognitive flow — what you typically open before and after each file

---

## Script

The parser exports a `buildBrainMap(options)` function so it can be called directly from API routes or other scripts without shell execution. It also runs as a standalone CLI script when invoked directly via `node`.

```javascript
#!/usr/bin/env node
/**
 * Brain Map — Project-Centric Builder
 *
 * 13 attention categories, ordered by co-access count descending.
 * Parses all journal entries, maps each session to one or more projects
 * via keyword matching. Extracts files from explicit Files Accessed blocks
 * where available; falls back to regex extraction from transcript text.
 *
 * Exports: buildBrainMap(options?) — call directly from API routes.
 * Output:  brain-map-projects.json (or options.outputPath)
 */

const fs   = require('fs');
const path = require('path');

const WORKSPACE_DIR = process.env.WORKSPACE_DIR || path.join(process.env.HOME, '.openclaw/vault');
const JOURNAL_DIR   = path.join(WORKSPACE_DIR, 'memory/journal');
const OUTPUT_PATH   = process.env.OUTPUT_PATH
  || path.join(__dirname, '../data/brain-map-projects.json');

// ── 13 attention categories ───────────────────────────────────────────────────
// Customize PROJECT_DEFS to match your vault's actual work patterns.
// Each project needs: id (machine name), label (display), color (hex), keywords (array of strings).

const PROJECT_DEFS = [
  {
    id: 'memory-system',
    label: 'Memory System',
    color: '#c8a84b',
    keywords: [
      'memory system', 'memory.md', 'recent.md', 'deep-memory', 'working.md',
      'self-memory', 'meta-memory', 'journal-writer', 'memory layers',
      'memory architecture', 'memory tier', 'vault audit', 'session log',
      'rolling log', 'memory file', 'slop creep',
    ],
  },
  {
    id: 'ghost-publishing',
    label: 'Ghost Publishing',
    color: '#22c55e',
    keywords: [
      'ghost', 'josephvoelbel.com', 'article', 'draft', 'lexical', 'ghost admin',
      'theme', 'subscribe form', 'magic link', 'continue reading',
      'feature image', 'ghost publishing', 'ghost theme', 'batch lexical',
      'member', 'subscriber', 'email newsletter', 'excerpt',
    ],
  },
  {
    id: 'ghost-publishing-pro',
    label: 'Ghost Publishing Pro Skill',
    color: '#34d399',
    keywords: [
      'ghost publishing pro', 'skill publish', 'clawhub', 'scanner',
      'virus total', 'benign', 'suspicious', 'skill security',
      'workflow 14', 'workflow 15', 'jwt', 'admin api key', 'ghost skill',
      'skill iteration', 'skill update',
    ],
  },
  {
    id: 'youtube',
    label: 'YouTube',
    color: '#ef4444',
    keywords: [
      'youtube', 'thumbnail', 'playlist', 'video description',
      'flux', 'replicate', 'pillow', 'ffmpeg', 'short', 'narration',
      'audio recording', 'whisper', 'channel description', 'watch hours',
      'ypp', 'monetization', 'thumbnail system', 'upload to youtube',
    ],
  },
  {
    id: 'mission-control',
    label: 'Mission Control',
    color: '#60a5fa',
    keywords: [
      'mission control', 'mc tab', 'ops queue', 'pipeline tab', 'analytics tab',
      'today tab', 'finances tab', 'models tab', 'sidebar',
      'hno-mission-control', 'next.js', 'activity feed', 'mc chat',
      'mc deploy', 'mc route', 'mc api',
    ],
  },
  {
    id: 'brain-map-skill',
    label: 'Brain Map Skill',
    color: '#a78bfa',
    keywords: [
      'brain map visualizer', 'oc-brain-map', 'brain map skill',
      'graph rebuild', 'force graph', 'd3', 'brain map graph', 'journal parser',
      'co-access', 'brain map tab', 'attention pocket', 'attention model',
      'reorbit', 'brainmapprojects', 'force simulation',
    ],
  },
  {
    id: 'github',
    label: 'GitHub',
    color: '#f0f6ff',
    keywords: [
      'github', 'git push', 'git commit', 'pull request', 'pr #', 'merge',
      'feature branch', 'main branch', 'hno-skills', 'ghost-theme',
      'pr open', 'pr merged', 'pat', 'personal access token',
    ],
  },
  {
    id: 'cron-automation',
    label: 'Cron + Automation',
    color: '#fb923c',
    keywords: [
      'cron', 'launchd', 'scheduled', 'second-brain-weekly', 'brain-map-weekly',
      'openclaw cron', 'heartbeat', 'filedrop', 'automation', 'dispatch',
      'cron job', 'watchdog', 'proactive',
    ],
  },
  {
    id: 'model-stack',
    label: 'Model Stack',
    color: '#e879f9',
    keywords: [
      'model routing', 'cadmus', 'maple', 'haiku', 'ollama', 'sonnet',
      'anthropic', 'openai', 'local model', 'model stack', 'model delegation',
      'tier 1', 'tier 2', 'tier 3', 'model override', 'subagent',
      'claude', 'qwen', 'gemini', 'api balance', 'topped up', 'credit',
    ],
  },
  {
    id: 'hno-business',
    label: 'HNO Business',
    color: '#ec4899',
    keywords: [
      'b2b', 'sales agent', 'client', 'hno strategy', 'consulting',
      'entrepreneur', 'product strategy', 'first client', 'pipeline card',
      'ai resume',
    ],
  },
  {
    id: 'finances',
    label: 'Finances + Bitcoin',
    color: '#fbbf24',
    keywords: [
      'bitcoin', 'btc', 'heloc', 'hysa', 'balance sheet', 'finances',
      'eth', 'sol', 'mstr', 'river', 'cold storage', 'roth', '401k',
      'mortgage', 'savings', 'net worth',
    ],
  },
  {
    id: 'the-desk',
    label: 'The Desk',
    color: '#d4a373',
    keywords: [
      'fiction', 'short story', 'literary', 'prose', 'writing', 'narrative',
      'nineteen stories', 'book layout', 'amazon print', 'published book',
    ],
  },
  {
    id: 'second-brain',
    label: 'Second Brain',
    color: '#67e8f9',
    keywords: [
      'second brain', 'second-brain', 'atom', 'slack',
      'second brain weekly', 'second brain tab', 'weekly synthesis',
      'knowledge atom', 'signal rating', 'second brain html',
    ],
  },
];

// ── Helpers ───────────────────────────────────────────────────────────────────

function extractFilesFromAccessedBlock(content) {
  const match = content.match(/## Files Accessed\n([\s\S]*?)(?:\n## |\n---|\n# |$)/);
  if (!match) return [];
  return match[1]
    .split('\n')
    .map(l => l.replace(/^[-*]\s*/, '').trim())
    .filter(l => l.endsWith('.md') && l.length > 0 && !l.includes(' '));
}

function extractFilesFromTranscript(content) {
  const found = new Set();
  const re = /(?:^|[\s"'`(,])([a-zA-Z0-9._\-/]+\.md)(?:[\s"'`),]|$)/gm;
  let m;
  while ((m = re.exec(content)) !== null) {
    const f = m[1].replace(/^\/+/, '');
    if (f.length > 3 && !f.startsWith('http') && !f.includes('node_modules')) {
      found.add(f);
    }
  }
  return [...found];
}

function matchProjects(text) {
  const lower = text.toLowerCase();
  const matched = [];
  for (const proj of PROJECT_DEFS) {
    if (proj.keywords.some(k => lower.includes(k))) matched.push(proj.id);
  }
  return matched.length > 0 ? matched : ['mission-control'];
}

function extractSummary(content) {
  const m = content.match(/## Summary\n+([\s\S]*?)(?:\n## |\n---|\n# |$)/);
  if (!m) return '';
  return m[1].replace(/\n/g, ' ').trim().slice(0, 400);
}

// ## Project block takes priority over keyword inference
function extractExplicitProject(content) {
  const m = content.match(/## Project\n+([\s\S]*?)(?:\n## |\n---|\n# |$)/);
  if (!m) return null;
  const label = m[1].replace(/\n/g, ' ').trim().toLowerCase();
  if (!label) return null;
  const matched = [];
  for (const def of PROJECT_DEFS) {
    if (label.includes(def.label.toLowerCase()) || label.includes(def.id.toLowerCase())) {
      matched.push(def.id);
    }
  }
  return matched.length > 0 ? matched : null;
}

// ── Parse journals ────────────────────────────────────────────────────────────

if (!fs.existsSync(JOURNAL_DIR)) {
  console.error('Journal dir not found:', JOURNAL_DIR);
  process.exit(1);
}

const journalFiles = fs.readdirSync(JOURNAL_DIR)
  .filter(f => f.match(/^\d{4}-\d{2}-\d{2}\.md$/))
  .sort();

process.stdout.write(`Parsing ${journalFiles.length} journal files...`);

const projectMap = {};
for (const def of PROJECT_DEFS) {
  projectMap[def.id] = { ...def, sessions: [], fileSet: new Set() };
}

let journalCount = 0;

for (const jf of journalFiles) {
  const content = fs.readFileSync(path.join(JOURNAL_DIR, jf), 'utf8');
  const date    = jf.replace('.md', '');
  const summary = extractSummary(content);
  if (!summary) continue;
  journalCount++;

  let files = extractFilesFromAccessedBlock(content);
  if (files.length < 3) {
    const extra = extractFilesFromTranscript(content);
    files = [...new Set([...files, ...extra])];
  }
  files = [...new Set(files.map(f => f.replace(/^\.?\//, '')))].filter(f => f.endsWith('.md'));

  const projIds = extractExplicitProject(content) || matchProjects(summary + ' ' + content.slice(0, 3000));
  for (const pid of projIds) {
    if (!projectMap[pid]) continue;
    projectMap[pid].sessions.push({ date, summary: summary.slice(0, 200), files });
    files.forEach(f => projectMap[pid].fileSet.add(f));
  }
}

// ── Build nodes + edges ───────────────────────────────────────────────────────

const GROUP_RULES = [
  { prefix: 'memory/',             group: 'memory' },
  { prefix: 'PublishingPipeline/', group: 'publishing' },
  { prefix: 'drafts/',             group: 'publishing' },
  { prefix: 'tools/',              group: 'infrastructure' },
  { prefix: 'workflows/',          group: 'infrastructure' },
  { prefix: 'prompts/',            group: 'infrastructure' },
  { prefix: 'scripts/',            group: 'infrastructure' },
  { prefix: 'mission-control/',    group: 'infrastructure' },
  { prefix: '.learnings/',         group: 'infrastructure' },
  { prefix: 'skills/',             group: 'skills' },
];
const CORE_FILES = new Set(['MEMORY.md','SOUL.md','USER.md','IDENTITY.md','AGENTS.md','TOOLS.md','HEARTBEAT.md','BOOTSTRAP.md']);

function classifyGroup(filePath) {
  const base = path.basename(filePath);
  if (CORE_FILES.has(base) && !filePath.includes('/')) return 'core';
  for (const r of GROUP_RULES) if (filePath.startsWith(r.prefix)) return r.group;
  return 'general';
}

const projects = [];
const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);

for (const def of PROJECT_DEFS) {
  const proj = projectMap[def.id];
  if (proj.sessions.length === 0) continue;

  const files = [...proj.fileSet];
  const nodes = files.map(f => ({
    id: f,
    group: classifyGroup(f),
    accessCount: proj.sessions.filter(s => s.files.includes(f)).length,
  }));

  const edgeMap = {};
  for (const session of proj.sessions) {
    const sf = session.files;
    for (let i = 0; i < sf.length; i++) {
      for (let j = i + 1; j < sf.length; j++) {
        const sorted = [sf[i], sf[j]].sort();
        const k = sorted.join('|||');
        if (!edgeMap[k]) {
          edgeMap[k] = {
            source: sorted[0], target: sorted[1],
            weight: 0, sessions: [],
            votes: { forward: 0, backward: 0 }
          };
        }
        edgeMap[k].weight++;
        if (!edgeMap[k].sessions.includes(session.date)) edgeMap[k].sessions.push(session.date);
        if (sf[i] === sorted[0]) { edgeMap[k].votes.forward++; }
        else                     { edgeMap[k].votes.backward++; }
      }
    }
  }

  const allDates = proj.sessions.map(s => s.date).sort();
  const spanDays = allDates.length >= 2
    ? (new Date(allDates[allDates.length-1]).getTime() - new Date(allDates[0]).getTime()) / 86400000
    : 1;

  const edges = Object.values(edgeMap).map(edge => {
    const recentCount   = edge.sessions.filter(d => d >= thirtyDaysAgo).length;
    const lifetimeCount = edge.sessions.length;
    const fromId = edge.votes.forward >= edge.votes.backward ? edge.source : edge.target;
    const toId   = edge.votes.forward >= edge.votes.backward ? edge.target : edge.source;
    return { source: edge.source, target: edge.target, fromId, toId, weight: edge.weight, recentCount, lifetimeCount, spanDays };
  });

  const coAccessScore = edges.reduce((sum, e) => sum + e.weight, 0);

  projects.push({
    id: def.id, label: def.label, color: def.color,
    sessionCount: proj.sessions.length, fileCount: nodes.length, coAccessScore,
    dateFirst: proj.sessions[0]?.date, dateLast: proj.sessions[proj.sessions.length - 1]?.date,
    sessions: proj.sessions.map(s => ({ date: s.date, summary: s.summary })),
    nodes, edges,
  });
}

projects.sort((a, b) => b.coAccessScore - a.coAccessScore);

const output = { projects, generated: new Date().toISOString(), journalCount };
fs.writeFileSync(OUTPUT_PATH, JSON.stringify(output, null, 2));

process.stdout.write(`\n✓ Written to ${OUTPUT_PATH}`);
process.stdout.write(`  ${projects.length} projects, sorted by attention:\n`);
projects.forEach((p, i) =>
  process.stdout.write(`  ${String(i+1).padStart(2)}. [${p.coAccessScore.toString().padStart(5)} co-access] ${p.label}: ${p.sessionCount} sessions, ${p.fileCount} files`)
);

// ── Exported API ──────────────────────────────────────────────────────────────
// Call buildBrainMap() directly from API routes — no shell execution needed.

function buildBrainMap(options = {}) {
  const workspaceDir = options.workspaceDir || process.env.WORKSPACE_DIR || path.join(process.env.HOME, '.openclaw/vault');
  const journalDir   = path.join(workspaceDir, 'memory/journal');
  const outputPath   = options.outputPath   || process.env.OUTPUT_PATH   || path.join(__dirname, '../data/brain-map-projects.json');

  if (!fs.existsSync(journalDir)) throw new Error('Journal dir not found: ' + journalDir);

  const journalFiles = fs.readdirSync(journalDir)
    .filter(f => f.match(/^\d{4}-\d{2}-\d{2}\.md$/))
    .sort();

  const projMap = {};
  for (const def of PROJECT_DEFS) {
    projMap[def.id] = { ...def, sessions: [], fileSet: new Set() };
  }

  let count = 0;
  for (const jf of journalFiles) {
    const content = fs.readFileSync(path.join(journalDir, jf), 'utf8');
    const date    = jf.replace('.md', '');
    const summary = extractSummary(content);
    if (!summary) continue;
    count++;

    let files = extractFilesFromAccessedBlock(content);
    if (files.length < 3) {
      const extra = extractFilesFromTranscript(content);
      files = [...new Set([...files, ...extra])];
    }
    files = [...new Set(files.map(f => f.replace(/^\.?\//,'')))].filter(f => f.endsWith('.md'));

    const projIds = extractExplicitProject(content) || matchProjects(summary + ' ' + content.slice(0, 3000));
    for (const pid of projIds) {
      if (!projMap[pid]) continue;
      projMap[pid].sessions.push({ date, summary: summary.slice(0, 200), files });
      files.forEach(f => projMap[pid].fileSet.add(f));
    }
  }

  const ago30 = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);
  const built = [];

  for (const def of PROJECT_DEFS) {
    const proj = projMap[def.id];
    if (proj.sessions.length === 0) continue;

    const files = [...proj.fileSet];
    const nodes = files.map(f => ({
      id: f, group: classifyGroup(f),
      accessCount: proj.sessions.filter(s => s.files.includes(f)).length,
    }));

    const edgeMap = {};
    for (const session of proj.sessions) {
      const sf = session.files;
      for (let i = 0; i < sf.length; i++) {
        for (let j = i + 1; j < sf.length; j++) {
          const sorted = [sf[i], sf[j]].sort();
          const k = sorted.join('|||');
          if (!edgeMap[k]) edgeMap[k] = { source: sorted[0], target: sorted[1], weight: 0, sessions: [], votes: { forward: 0, backward: 0 } };
          edgeMap[k].weight++;
          if (!edgeMap[k].sessions.includes(session.date)) edgeMap[k].sessions.push(session.date);
          if (sf[i] === sorted[0]) edgeMap[k].votes.forward++;
          else edgeMap[k].votes.backward++;
        }
      }
    }

    const allDates = proj.sessions.map(s => s.date).sort();
    const spanDays = allDates.length >= 2
      ? (new Date(allDates[allDates.length-1]).getTime() - new Date(allDates[0]).getTime()) / 86400000
      : 1;

    const edges = Object.values(edgeMap).map(edge => {
      const recentCount   = edge.sessions.filter(d => d >= ago30).length;
      const lifetimeCount = edge.sessions.length;
      const fromId = edge.votes.forward >= edge.votes.backward ? edge.source : edge.target;
      const toId   = edge.votes.forward >= edge.votes.backward ? edge.target : edge.source;
      return { source: edge.source, target: edge.target, fromId, toId, weight: edge.weight, recentCount, lifetimeCount, spanDays };
    });

    const coAccessScore = edges.reduce((sum, e) => sum + e.weight, 0);
    built.push({
      id: def.id, label: def.label, color: def.color,
      sessionCount: proj.sessions.length, fileCount: nodes.length, coAccessScore,
      dateFirst: proj.sessions[0]?.date, dateLast: proj.sessions[proj.sessions.length - 1]?.date,
      sessions: proj.sessions.map(s => ({ date: s.date, summary: s.summary })),
      nodes, edges,
    });
  }

  built.sort((a, b) => b.coAccessScore - a.coAccessScore);
  const result = { projects: built, generated: new Date().toISOString(), journalCount: count };
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));
  return result;
}

module.exports = { buildBrainMap };

// Run as CLI if called directly
if (require.main === module) {
  buildBrainMap();
}
```
