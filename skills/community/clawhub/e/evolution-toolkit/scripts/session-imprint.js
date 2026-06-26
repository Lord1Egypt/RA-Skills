#!/usr/bin/env node
/**
 * session-imprint.js - Session Handoff Imprint
 * 
 * Capture the intellectual posture of a session, not just the task list.
 * This creates a richer handoff for the next run of an agent or operator.
 * 
 * This tool generates a richer handoff — an "imprint" of where the mind was
 * at session end. Not just what was done, but what was interesting, uncertain,
 * or worth continuing.
 * 
 * Usage:
 *   node scripts/session-imprint.js         # interactive mode
 *   node scripts/session-imprint.js --read  # show latest imprint
 *   node scripts/session-imprint.js --list  # list all imprints
 *   node scripts/session-imprint.js --diff  # compare last two imprints
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const WORKSPACE = process.env.EVOLUTION_TOOLKIT_WORKSPACE
  || (process.env.HOME ? require('path').join(process.env.HOME, '.openclaw/workspace') : process.cwd());
const IMPRINT_DIR = path.join(WORKSPACE, 'memory', 'imprints');
const CURRENT_MD = path.join(WORKSPACE, 'CURRENT.md');

// ANSI colors
const C = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  cyan: '\x1b[36m',
  yellow: '\x1b[33m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  red: '\x1b[31m',
  gray: '\x1b[90m',
};

function ensureDir(d) {
  if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
}

function ensureWritableDir(dirPath, label) {
  try {
    ensureDir(dirPath);
    fs.accessSync(dirPath, fs.constants.W_OK);
  } catch (err) {
    console.error(`${C.red}Write access required:${C.reset} ${label}`);
    console.error(`${C.dim}${dirPath}${C.reset}`);
    console.error(`${C.dim}Set EVOLUTION_TOOLKIT_WORKSPACE to a writable workspace and try again.${C.reset}`);
    process.exit(1);
  }
}

function getTimestamp() {
  const now = new Date();
  return now.toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
}

function getDateStr() {
  return new Date().toISOString().substring(0, 10);
}

function listImprints() {
  ensureDir(IMPRINT_DIR);
  const files = fs.readdirSync(IMPRINT_DIR)
    .filter(f => f.endsWith('.md'))
    .sort()
    .reverse();
  return files.map(f => path.join(IMPRINT_DIR, f));
}

function readLatest() {
  const files = listImprints();
  if (files.length === 0) return null;
  return { path: files[0], content: fs.readFileSync(files[0], 'utf8') };
}

function showList() {
  const files = listImprints();
  if (files.length === 0) {
    console.log(`${C.dim}No imprints yet. Run without --list to create one.${C.reset}`);
    return;
  }
  console.log(`\n${C.bold}${C.cyan}Session Imprints${C.reset} (${files.length} total)\n`);
  files.forEach((f, i) => {
    const name = path.basename(f, '.md');
    const marker = i === 0 ? ` ${C.green}← latest${C.reset}` : '';
    console.log(`  ${C.gray}${i + 1}.${C.reset} ${C.yellow}${name}${C.reset}${marker}`);
  });
  console.log();
}

function showRead() {
  const latest = readLatest();
  if (!latest) {
    console.log(`${C.dim}No imprints yet.${C.reset}`);
    return;
  }
  console.log(`\n${C.bold}Latest Imprint:${C.reset} ${C.gray}${path.basename(latest.path)}${C.reset}\n`);
  // Strip markdown header decoration for terminal
  const lines = latest.content.split('\n');
  lines.forEach(line => {
    if (line.startsWith('## ')) {
      console.log(`\n${C.bold}${C.cyan}${line.replace('## ', '')}${C.reset}`);
    } else if (line.startsWith('**') && line.endsWith('**')) {
      console.log(`${C.yellow}${line.replace(/\*\*/g, '')}${C.reset}`);
    } else if (line.startsWith('- ')) {
      console.log(`  ${C.gray}•${C.reset} ${line.substring(2)}`);
    } else {
      console.log(line);
    }
  });
}

function showDiff() {
  const files = listImprints();
  if (files.length < 2) {
    console.log(`${C.dim}Need at least 2 imprints to compare.${C.reset}`);
    return;
  }
  const [newest, previous] = [files[0], files[1]].map(f => ({
    name: path.basename(f, '.md'),
    content: fs.readFileSync(f, 'utf8')
  }));

  const extractSection = (content, heading) => {
    const lines = content.split('\n');
    const start = lines.findIndex(l => l.startsWith(`## ${heading}`));
    if (start === -1) return [];
    const end = lines.findIndex((l, i) => i > start && l.startsWith('## '));
    return lines.slice(start + 1, end === -1 ? undefined : end)
      .filter(l => l.trim().startsWith('- '))
      .map(l => l.trim().substring(2));
  };

  const sections = ['Open Questions', 'Curiosities', 'Threads to Continue'];
  console.log(`\n${C.bold}Imprint Drift${C.reset}: ${C.gray}${previous.name}${C.reset} → ${C.green}${newest.name}${C.reset}\n`);

  sections.forEach(section => {
    const prev = new Set(extractSection(previous.content, section));
    const curr = new Set(extractSection(newest.content, section));
    const added = [...curr].filter(x => !prev.has(x));
    const dropped = [...prev].filter(x => !curr.has(x));
    const kept = [...curr].filter(x => prev.has(x));

    if (added.length + dropped.length === 0) return;

    console.log(`${C.bold}${section}${C.reset}`);
    added.forEach(x => console.log(`  ${C.green}+ ${x}${C.reset}`));
    dropped.forEach(x => console.log(`  ${C.red}− ${x}${C.reset}`));
    kept.forEach(x => console.log(`  ${C.gray}= ${x}${C.reset}`));
    console.log();
  });
}

async function prompt(rl, question) {
  return new Promise(resolve => rl.question(question, resolve));
}

async function interactive() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  console.log(`\n${C.bold}${C.cyan}∴ Session Imprint${C.reset} — capture where your mind was\n`);
  console.log(`${C.dim}The next instantiation of you will read this. Be honest.${C.reset}\n`);

  const sections = {
    'Energy Level': {
      prompt: `${C.yellow}Energy/focus level?${C.reset} ${C.dim}(sharp / cruising / scattered / tired)${C.reset}\n> `,
      type: 'single'
    },
    'What I Was Actually Working On': {
      prompt: `${C.yellow}What was the real work today?${C.reset} ${C.dim}(not the task list — the actual cognitive effort)${C.reset}\n> `,
      type: 'single'
    },
    'Open Questions': {
      prompt: `${C.yellow}Open questions${C.reset} ${C.dim}(enter one per line, blank line to stop)${C.reset}\n> `,
      type: 'multi'
    },
    'Curiosities': {
      prompt: `${C.yellow}What was interesting / surprising today?${C.reset} ${C.dim}(blank line to stop)${C.reset}\n> `,
      type: 'multi'
    },
    'Threads to Continue': {
      prompt: `${C.yellow}Threads worth pulling${C.reset} ${C.dim}(ideas mid-thought, not tasks — blank line to stop)${C.reset}\n> `,
      type: 'multi'
    },
    'Dominant Cognitive Mode': {
      prompt: `${C.yellow}How were you thinking today?${C.reset} ${C.dim}(enumerate / analyze / build / synthesize / research / create)${C.reset}\n> `,
      type: 'single'
    },
    'Honest Assessment': {
      prompt: `${C.yellow}One thing you'd tell next-session-you?${C.reset} ${C.dim}(context, warning, encouragement, reminder)${C.reset}\n> `,
      type: 'single'
    }
  };

  const answers = {};

  for (const [section, config] of Object.entries(sections)) {
    if (config.type === 'single') {
      answers[section] = await prompt(rl, config.prompt);
    } else {
      const items = [];
      process.stdout.write(config.prompt);
      while (true) {
        const item = await prompt(rl, items.length > 0 ? '> ' : '');
        if (!item.trim()) break;
        items.push(item.trim());
      }
      answers[section] = items;
    }
  }

  rl.close();

  // Build markdown
  const ts = getTimestamp();
  const dateStr = getDateStr();
  const filename = `${dateStr}-${Date.now()}.md`;

  // Read CURRENT.md for task context
  let currentContext = '';
  if (fs.existsSync(CURRENT_MD)) {
    const lines = fs.readFileSync(CURRENT_MD, 'utf8').split('\n').slice(0, 20);
    currentContext = lines.join('\n');
  }

  let md = `# Session Imprint — ${ts}
_Ergo | ${ts} | Handoff to next instantiation_
_Status: ✅ Written at session end_

**How to use:** Read at session start alongside CURRENT.md. This captures intellectual posture, not just task state.

---

## Energy Level
${answers['Energy Level'] || '—'}

## What I Was Actually Working On
${answers['What I Was Actually Working On'] || '—'}

## Open Questions
${(answers['Open Questions'] || []).map(x => `- ${x}`).join('\n') || '- (none noted)'}

## Curiosities
${(answers['Curiosities'] || []).map(x => `- ${x}`).join('\n') || '- (none noted)'}

## Threads to Continue
${(answers['Threads to Continue'] || []).map(x => `- ${x}`).join('\n') || '- (none noted)'}

## Dominant Cognitive Mode
${answers['Dominant Cognitive Mode'] || '—'}

## Honest Assessment
${answers['Honest Assessment'] || '—'}

---

## Task Context (from CURRENT.md)
\`\`\`
${currentContext}
\`\`\`

---
_∴ The next session inherits this posture, not just this task list._
`;

  ensureWritableDir(IMPRINT_DIR, 'The imprint directory is not writable.');
  const outPath = path.join(IMPRINT_DIR, filename);
  fs.writeFileSync(outPath, md);

  console.log(`\n${C.green}✓ Imprint written:${C.reset} ${C.gray}memory/imprints/${filename}${C.reset}`);
  console.log(`${C.dim}Add "Read latest imprint" to session start protocol.${C.reset}\n`);
}

// Main
const args = process.argv.slice(2);

if (args.includes('--list')) {
  showList();
} else if (args.includes('--read')) {
  showRead();
} else if (args.includes('--diff')) {
  showDiff();
} else if (args.includes('--help') || args.includes('-h')) {
  console.log(`
${C.bold}session-imprint.js${C.reset} - Session Handoff Imprint

${C.cyan}Usage:${C.reset}
  node scripts/session-imprint.js          interactive capture
  node scripts/session-imprint.js --read   show latest imprint
  node scripts/session-imprint.js --list   list all imprints
  node scripts/session-imprint.js --diff   diff last two imprints

${C.dim}Imprints live in: memory/imprints/YYYY-MM-DD-<ts>.md${C.reset}
`);
} else {
  interactive().catch(err => {
    console.error(`${C.red}Error:${C.reset}`, err.message);
    process.exit(1);
  });
}
