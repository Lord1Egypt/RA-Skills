#!/usr/bin/env node
/**
 * predict.js — Prediction Log CLI
 * Reduce friction around prediction logging and calibration review.
 *
 * Usage:
 *   node scripts/predict.js add
 *   node scripts/predict.js resolve
 *   node scripts/predict.js audit
 *   node scripts/predict.js stats
 *   node scripts/predict.js last [N]
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const WORKSPACE = process.env.EVOLUTION_TOOLKIT_WORKSPACE
  || (process.env.HOME ? require('path').join(process.env.HOME, '.openclaw/workspace') : process.cwd());
const LOG_PATH = path.join(WORKSPACE, 'memory', 'prediction-log.md');
const SECTION_MARKER = '## Log';
const END_MARKER = '## Calibration';

function ensureWritableDir(dirPath, label) {
  try {
    fs.mkdirSync(dirPath, { recursive: true });
    fs.accessSync(dirPath, fs.constants.W_OK);
  } catch (err) {
    console.error(`Write access required: ${label}`);
    console.error(dirPath);
    console.error('Set EVOLUTION_TOOLKIT_WORKSPACE to a writable workspace and try again.');
    process.exit(1);
  }
}

// ─── Parse predictions from markdown ────────────────────────────────────────

function parseLog() {
  const content = fs.readFileSync(LOG_PATH, 'utf8');
  const logStart = content.indexOf(SECTION_MARKER);
  const logEnd = content.indexOf(END_MARKER);
  if (logStart === -1) return { content, entries: [], before: content, after: '' };

  const before = content.slice(0, logStart + SECTION_MARKER.length + 1);
  const logSection = content.slice(logStart + SECTION_MARKER.length, logEnd !== -1 ? logEnd : undefined);
  const after = logEnd !== -1 ? content.slice(logEnd) : '';

  // Split by ### headings
  const rawEntries = logSection.split(/(?=### \d{4}-\d{2}-\d{2})/).filter(s => s.trim());

  const entries = rawEntries.map(raw => {
    const dateMatch = raw.match(/### (\d{4}-\d{2}-\d{2}) — (.+)/);
    if (!dateMatch) return null;

    const date = dateMatch[1];
    const topic = dateMatch[2].trim();
    const hasOutcome = /\*\*Outcome:\*\*/.test(raw) && !/\*\*Outcome:\*\*\s*\[fill in/.test(raw) && !/\*\*Outcome:\*\*\s*$/.test(raw);
    const hasDelta = /\*\*Delta:\*\*/.test(raw);
    const isOpen = !hasOutcome;

    // Extract confidence
    const confMatch = raw.match(/\*\*Confidence:\*\*\s*(H|M|L)/i);
    const confidence = confMatch ? confMatch[1].toUpperCase() : '?';

    // Extract epistemic basis
    const basisMatch = raw.match(/\*\*Epistemic basis:\*\*\s*(.+)/);
    const basis = basisMatch ? basisMatch[1].trim() : '?';

    return { date, topic, raw, isOpen, confidence, basis };
  }).filter(Boolean);

  return { content, entries, before, after, logSection };
}

// ─── Format a new prediction entry ──────────────────────────────────────────

function formatEntry({ date, topic, prediction, confidence, basis }) {
  return `
### ${date} — ${topic}
**Prediction:** ${prediction}
**Confidence:** ${confidence}
**Epistemic basis:** ${basis}
**Outcome:** [fill in after]
**Delta:** [what surprised me]
**Lesson:** [what to update]
`;
}

// ─── Insert after last entry in Log section ──────────────────────────────────

function insertEntry(newEntry) {
  ensureWritableDir(path.dirname(LOG_PATH), 'The prediction log directory is not writable.');
  const content = fs.readFileSync(LOG_PATH, 'utf8');
  const endMarkerIdx = content.indexOf('\n---\n\n## Calibration');
  if (endMarkerIdx === -1) {
    // Append before calibration section
    const calibIdx = content.indexOf('\n## Calibration');
    if (calibIdx === -1) {
      fs.appendFileSync(LOG_PATH, newEntry);
    } else {
      const updated = content.slice(0, calibIdx) + '\n' + newEntry + content.slice(calibIdx);
      fs.writeFileSync(LOG_PATH, updated);
    }
  } else {
    const updated = content.slice(0, endMarkerIdx) + '\n' + newEntry + content.slice(endMarkerIdx);
    fs.writeFileSync(LOG_PATH, updated);
  }
}

// ─── readline helper ─────────────────────────────────────────────────────────

function ask(rl, question) {
  return new Promise(resolve => rl.question(question, resolve));
}

// ─── Commands ────────────────────────────────────────────────────────────────

async function cmdAdd() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  
  console.log('\n📝 New Prediction\n');
  
  const today = new Date().toISOString().slice(0, 10);
  const topic = await ask(rl, `Topic (e.g. "Codex will finish within 30 min"): `);
  const prediction = await ask(rl, `Prediction (what do you expect?): `);
  
  let confidence = '';
  while (!['H', 'M', 'L'].includes(confidence.toUpperCase())) {
    confidence = await ask(rl, `Confidence [H/M/L]: `);
  }
  confidence = confidence.toUpperCase();

  console.log('\nEpistemic basis options:');
  console.log('  [observed]   — you have direct evidence');
  console.log('  [inferred]   — logical deduction, not direct evidence');
  console.log('  [consensus]  — following conventional wisdom');
  console.log('  [speculative]— educated guess, thin evidence');
  const basis = await ask(rl, `Basis: `);
  
  rl.close();
  
  const entry = formatEntry({ date: today, topic, prediction, confidence, basis });
  insertEntry(entry);
  
  console.log('\n✅ Prediction logged. Fill in Outcome/Delta/Lesson after it resolves.');
  console.log(`   Run: node scripts/predict.js resolve`);
}

function cmdAudit() {
  const { entries } = parseLog();
  const open = entries.filter(e => e.isOpen);
  
  if (open.length === 0) {
    console.log('\n✅ No open predictions. All have outcomes recorded.\n');
    return;
  }

  console.log(`\n⚠️  ${open.length} open prediction(s) awaiting outcome:\n`);
  open.forEach((e, i) => {
    const conf = e.confidence === 'H' ? '🔴' : e.confidence === 'M' ? '🟡' : '🟢';
    console.log(`  ${i + 1}. [${e.date}] ${conf} ${e.topic}`);
  });
  console.log('\n  Run `node scripts/predict.js resolve` to fill in outcomes.');
  console.log(`  Or edit memory/prediction-log.md directly.\n`);
}

function cmdStats() {
  const { entries } = parseLog();
  
  if (entries.length === 0) {
    console.log('\nNo predictions yet.\n');
    return;
  }

  const resolved = entries.filter(e => !e.isOpen);
  const open = entries.filter(e => e.isOpen);

  const confCounts = { H: 0, M: 0, L: 0, '?': 0 };
  entries.forEach(e => { confCounts[e.confidence] = (confCounts[e.confidence] || 0) + 1; });

  // Tag epistemic types
  const basisCounts = {};
  entries.forEach(e => {
    const tags = (e.basis.match(/\[(observed|inferred|consensus|speculative)\]/g) || []);
    tags.forEach(t => { basisCounts[t] = (basisCounts[t] || 0) + 1; });
    if (!tags.length) { basisCounts['[untagged]'] = (basisCounts['[untagged]'] || 0) + 1; }
  });

  console.log('\n📊 Prediction Log Stats\n');
  console.log(`  Total entries:  ${entries.length}`);
  console.log(`  Resolved:       ${resolved.length}`);
  console.log(`  Open:           ${open.length}`);
  console.log('');
  console.log('  Confidence distribution:');
  console.log(`    H (high):   ${confCounts.H || 0} entries`);
  console.log(`    M (medium): ${confCounts.M || 0} entries`);
  console.log(`    L (low):    ${confCounts.L || 0} entries`);
  console.log('');
  console.log('  Epistemic basis:');
  Object.entries(basisCounts).sort((a,b) => b[1]-a[1]).forEach(([tag, count]) => {
    console.log(`    ${tag}: ${count}`);
  });

  // Warn if too many high-confidence predictions (overconfidence signal)
  const highConf = confCounts.H || 0;
  const total = entries.length;
  const highPct = Math.round(100 * highConf / total);
  if (highPct > 50) {
    console.log(`\n  ⚠️  ${highPct}% of predictions are High confidence.`);
    console.log('     If accuracy < 80%, this indicates overconfidence bias.');
  }

  // Warn if prediction gap
  const today = new Date().toISOString().slice(0, 10);
  const lastDate = entries.length > 0 ? entries[entries.length - 1].date : null;
  if (lastDate) {
    const daysSince = Math.floor((new Date(today) - new Date(lastDate)) / (1000*60*60*24));
    if (daysSince > 3) {
      console.log(`\n  ⚠️  Last prediction: ${lastDate} (${daysSince} days ago).`);
      console.log('     Prediction gap detected. Add entries for recent significant decisions.');
    }
  }
  console.log('');
}

function cmdLast(n = 5) {
  const { entries } = parseLog();
  const last = entries.slice(-n);
  
  if (last.length === 0) {
    console.log('\nNo predictions yet.\n');
    return;
  }

  console.log(`\n📋 Last ${last.length} prediction(s):\n`);
  last.forEach(e => {
    const status = e.isOpen ? '⏳ open' : '✅ resolved';
    const conf = e.confidence === 'H' ? '🔴H' : e.confidence === 'M' ? '🟡M' : '🟢L';
    console.log(`  [${e.date}] ${conf} ${status}`);
    console.log(`    Topic: ${e.topic}\n`);
  });
}

async function cmdResolve() {
  const { entries } = parseLog();
  const open = entries.filter(e => e.isOpen);
  
  if (open.length === 0) {
    console.log('\n✅ No open predictions to resolve.\n');
    return;
  }

  console.log(`\n⏳ ${open.length} open prediction(s). Opening prediction-log.md for editing...\n`);
  open.forEach((e, i) => {
    console.log(`  ${i + 1}. [${e.date}] ${e.topic}`);
  });
  console.log('\n  📝 Edit memory/prediction-log.md directly — fill in Outcome, Delta, and Lesson for each.');
  console.log('     Tip: search for "[fill in after]" to find open entries.\n');
}

// ─── Main ────────────────────────────────────────────────────────────────────

const cmd = process.argv[2] || 'audit';
const arg = process.argv[3];

(async () => {
  switch (cmd) {
    case 'add':      await cmdAdd(); break;
    case 'audit':    cmdAudit(); break;
    case 'stats':    cmdStats(); break;
    case 'last':     cmdLast(parseInt(arg) || 5); break;
    case 'resolve':  await cmdResolve(); break;
    default:
      console.log('Usage: node scripts/predict.js [add|audit|resolve|stats|last [N]]');
  }
})();
