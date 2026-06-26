#!/usr/bin/env node
/**
 * Action Guard — Universal dedup for AI agent external actions.
 * Check before acting, record after. Never do the same thing twice.
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const command = args[0];

// Parse options
function getOpt(name) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : null;
}

const dataDir = getOpt('data-dir') || path.join(process.cwd(), '.action-guard');
const actionsFile = path.join(dataDir, 'actions.jsonl');

// Ensure data dir exists
function ensureDir() {
  fs.mkdirSync(dataDir, { recursive: true });
}

// Read all actions (lazy — only when needed)
function readActions() {
  if (!fs.existsSync(actionsFile)) return [];
  return fs.readFileSync(actionsFile, 'utf8')
    .split('\n')
    .filter(line => line.trim())
    .map(line => {
      try { return JSON.parse(line); }
      catch { return null; }
    })
    .filter(Boolean);
}

// Append an action
function appendAction(action) {
  ensureDir();
  fs.appendFileSync(actionsFile, JSON.stringify(action) + '\n');
}

// Check if action already taken
function check(type, target) {
  const actions = readActions();

  // Direct match — same type + same target
  const direct = actions.find(a => a.type === type && a.target === target);
  if (direct) {
    console.error(`DUPLICATE: Already performed ${type} on ${target}`);
    console.error(`  Date: ${direct.ts}`);
    if (direct.note) console.error(`  Note: ${direct.note}`);
    process.exit(1);
  }

  // Parent match — already acted on this parent (catches reply-to-same-post)
  const parentMatch = actions.find(a => a.type === type && a.parent === target);
  if (parentMatch) {
    console.error(`DUPLICATE: Already performed ${type} on parent ${target}`);
    console.error(`  Via: ${parentMatch.target}`);
    console.error(`  Date: ${parentMatch.ts}`);
    if (parentMatch.note) console.error(`  Note: ${parentMatch.note}`);
    process.exit(1);
  }

  console.log(`OK: No prior ${type} on ${target}`);
  process.exit(0);
}

// Record an action
function record(type, target) {
  const note = getOpt('note') || '';
  const parent = getOpt('parent') || undefined;

  const action = {
    type,
    target,
    ...(parent && { parent }),
    ...(note && { note }),
    ts: new Date().toISOString(),
  };

  appendAction(action);
  console.log(`RECORDED: ${type} ${target}${parent ? ' (parent: ' + parent + ')' : ''}`);
}

// Show history
function history() {
  const type = getOpt('type');
  const days = parseInt(getOpt('days') || '30');
  const cutoff = new Date(Date.now() - days * 86400000).toISOString();

  let actions = readActions().filter(a => a.ts >= cutoff);
  if (type) actions = actions.filter(a => a.type === type);

  if (actions.length === 0) {
    console.log('No actions found.');
    return;
  }

  // Show most recent first
  actions.reverse().slice(0, 50).forEach(a => {
    const date = a.ts.slice(0, 16).replace('T', ' ');
    console.log(`  [${a.type}] ${a.target} — ${date}${a.note ? ' — ' + a.note : ''}`);
  });
  console.log(`\n${actions.length} action(s) in last ${days} days`);
}

// Stats
function stats() {
  const actions = readActions();
  const counts = {};
  actions.forEach(a => {
    counts[a.type] = (counts[a.type] || 0) + 1;
  });

  if (Object.keys(counts).length === 0) {
    console.log('No actions recorded.');
    return;
  }

  console.log('Action counts:');
  Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .forEach(([type, count]) => console.log(`  ${type}: ${count}`));
  console.log(`\nTotal: ${actions.length}`);
}

// Search
function search(query) {
  const actions = readActions();
  const q = query.toLowerCase();
  const matches = actions.filter(a =>
    (a.target && a.target.toLowerCase().includes(q)) ||
    (a.note && a.note.toLowerCase().includes(q)) ||
    (a.parent && a.parent.toLowerCase().includes(q))
  );

  if (matches.length === 0) {
    console.log(`No matches for "${query}"`);
    return;
  }

  matches.reverse().forEach(a => {
    const date = a.ts.slice(0, 16).replace('T', ' ');
    console.log(`  [${a.type}] ${a.target} — ${date}${a.note ? ' — ' + a.note : ''}`);
  });
  console.log(`\n${matches.length} match(es)`);
}

// Main
switch (command) {
  case 'check':
    if (!args[1] || !args[2]) {
      console.error('Usage: guard.js check <type> <target>');
      process.exit(2);
    }
    check(args[1], args[2]);
    break;

  case 'record':
    if (!args[1] || !args[2]) {
      console.error('Usage: guard.js record <type> <target> [--note "..."] [--parent <id>]');
      process.exit(2);
    }
    record(args[1], args[2]);
    break;

  case 'history':
    history();
    break;

  case 'stats':
    stats();
    break;

  case 'search':
    if (!args[1]) {
      console.error('Usage: guard.js search <query>');
      process.exit(2);
    }
    search(args.slice(1).join(' '));
    break;

  default:
    console.log(`Action Guard — Universal dedup for AI agents

Commands:
  check <type> <target>     Check if action already taken (exit 1 = duplicate)
  record <type> <target>    Record completed action
  history                   Show recent actions
  stats                     Action counts by type
  search <query>            Search notes/targets

Options:
  --note "text"             Context note (record)
  --parent <id>             Parent ID (record, enables reply-to-same-post dedup)
  --type <type>             Filter history by type
  --days <n>                Limit history (default: 30)
  --data-dir <path>         Data directory (default: .action-guard/)`);
    break;
}
