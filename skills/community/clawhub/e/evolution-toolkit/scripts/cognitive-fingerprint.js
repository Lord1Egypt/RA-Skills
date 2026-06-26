#!/usr/bin/env node
/**
 * cognitive-fingerprint.js
 * 
 * Generate a compact reasoning fingerprint from text samples.
 * Use it to track intellectual drift, compare sessions, and spot emerging tendencies.
 * 
 * Usage:
 *   node scripts/cognitive-fingerprint.js [file1.md] [file2.md] ...
 *   node scripts/cognitive-fingerprint.js --daily
 *   node scripts/cognitive-fingerprint.js --imprints
 *   node scripts/cognitive-fingerprint.js --compare [file1] [file2]
 *   node scripts/cognitive-fingerprint.js --history
 *   node scripts/cognitive-fingerprint.js --json
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.EVOLUTION_TOOLKIT_WORKSPACE
  || (process.env.HOME ? require('path').join(process.env.HOME, '.openclaw/workspace') : process.cwd());
const FP_STORE = path.join(WORKSPACE, 'memory/cognitive-fingerprints.json');

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

// ─── Color helpers ─────────────────────────────────────────────────────────
const c = {
  reset: '\x1b[0m', bold: '\x1b[1m', dim: '\x1b[2m',
  cyan: '\x1b[36m', magenta: '\x1b[35m', yellow: '\x1b[33m',
  green: '\x1b[32m', red: '\x1b[31m', blue: '\x1b[34m', white: '\x1b[37m'
};
const col = (color, text) => `${c[color]}${text}${c.reset}`;
const bold = (text) => `${c.bold}${text}${c.reset}`;
const dim = (text) => `${c.dim}${text}${c.reset}`;

// ─── Tokenizers & Extractors ────────────────────────────────────────────────

function cleanText(raw) {
  return raw
    .replace(/```[\s\S]*?```/g, '') // remove code blocks
    .replace(/`[^`]+`/g, '')         // remove inline code
    .replace(/^#{1,6}\s+/gm, '')     // remove markdown headers
    .replace(/^\s*[-*+]\s+/gm, '')   // remove list markers
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // links → text
    .replace(/[_*]{1,2}([^_*]+)[_*]{1,2}/g, '$1') // bold/italic → text
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function tokenize(text) {
  return text.toLowerCase().match(/\b[a-z']+\b/g) || [];
}

function sentences(text) {
  return text.split(/[.!?]+/).map(s => s.trim()).filter(s => s.length > 10);
}

// ─── Fingerprint Dimensions ─────────────────────────────────────────────────

const REASONING_MARKERS = [
  'because', 'therefore', 'thus', 'hence', 'implies', 'suggests', 'means that',
  'which means', 'so that', 'as a result', 'consequently', 'it follows', 'given that',
  'this is why', 'which is why', 'this shows', 'this means', 'this indicates'
];

const UNCERTAINTY_MARKERS = [
  'might', 'could', 'perhaps', 'possibly', 'probably', 'likely', 'seems', 'appears',
  'suggests', 'i think', 'i suspect', 'i wonder', 'not sure', 'unclear', 'uncertain',
  'maybe', 'presumably', 'apparently', "i'm not", 'may be'
];

const CONFIDENCE_MARKERS = [
  'clearly', 'obviously', 'certainly', 'definitely', 'undoubtedly', 'without question',
  'it is clear', 'this is clear', 'no doubt', 'of course', 'evidently', 'plainly'
];

// Phrase-level meta-markers (first-person thinking-about-thinking)
const META_MARKERS = [
  'i notice', 'i find', 'i realize', 'i think', 'i feel', 'what interests me',
  'what strikes me', 'i am thinking', 'the thing is', 'i want to be honest',
  'i should note', 'worth noting', "here's what", 'the interesting part'
];

// Topic-level meta-markers: text IS about cognition/thinking even without "I"
// These fire on whole-text presence (each unique match counts once toward density)
const META_TOPIC_MARKERS = [
  'metacognit', 'thinking about thinking', 'cognitive bias', 'cognition',
  'mental model', 'epistemic', 'reasoning process', 'how we think',
  'how i think', 'the way we think', 'system 1', 'system 2',
  'thinking partner', 'socratic', 'assumptions we make', 'our assumptions',
  'attention itself', 'what attention', 'what memory', 'what detection',
  'meaning drift', 'meaning provenance', 'semantic drift',
  'how decisions', 'decision-making process', 'cognitive friction',
  'thinking clearly', 'thinking well', 'quality of thinking'
];

const EPISTEMIC_TAGS = ['[consensus]', '[inferred]', '[speculative]', '[observed]', '[contrarian]'];

const CONTRADICTION_MARKERS = [
  'but also', 'and yet', 'even though', 'despite', 'however', 'on the other hand',
  'at the same time', 'paradoxically', 'both', 'simultaneously'
];

const COLLABORATIVE_WORDS = ['we', 'our', "we're", "we've", "let's", 'together', 'us'];
const SELF_WORDS = ['i', 'me', 'my', "i'm", "i've", 'mine'];

function computeFingerprint(rawText, label = '') {
  const text = cleanText(rawText);
  const tokens = tokenize(text);
  const sents = sentences(text);
  const words = text.split(/\s+/).filter(w => w.length > 0);
  
  if (tokens.length < 50) return null; // too short to fingerprint
  
  const textLower = text.toLowerCase();
  
  // 1. Vocabulary richness (Type-Token Ratio, normalized over 100-word windows)
  const windows = [];
  for (let i = 0; i + 100 < tokens.length; i += 50) {
    const window = tokens.slice(i, i + 100);
    const unique = new Set(window).size;
    windows.push(unique / 100);
  }
  const vocabRichness = windows.length > 0
    ? windows.reduce((a, b) => a + b, 0) / windows.length
    : new Set(tokens).size / Math.min(tokens.length, 100);
  
  // 2. Sentence complexity (avg word length per sentence)
  const sentLengths = sents.map(s => s.split(/\s+/).length);
  const avgSentLen = sentLengths.length > 0
    ? sentLengths.reduce((a, b) => a + b, 0) / sentLengths.length
    : 0;
  const sentLenSD = sentLengths.length > 1
    ? Math.sqrt(sentLengths.map(l => Math.pow(l - avgSentLen, 2)).reduce((a, b) => a + b, 0) / sentLengths.length)
    : 0;
  
  // 3. Reasoning density
  const reasoningCount = REASONING_MARKERS.reduce((n, m) => {
    const re = new RegExp(`\\b${m.replace(/\s+/g, '\\s+')}\\b`, 'gi');
    return n + (textLower.match(re) || []).length;
  }, 0);
  const reasoningDensity = words.length > 0 ? reasoningCount / words.length * 100 : 0;
  
  // 4. Uncertainty calibration
  const uncertaintyCount = UNCERTAINTY_MARKERS.reduce((n, m) => {
    const re = new RegExp(`\\b${m.replace(/\s+/g, '\\s+')}\\b`, 'gi');
    return n + (textLower.match(re) || []).length;
  }, 0);
  const uncertaintyRate = words.length > 0 ? uncertaintyCount / words.length * 100 : 0;
  
  // 5. Confidence (vs uncertainty) balance
  const confidenceCount = CONFIDENCE_MARKERS.reduce((n, m) => {
    const re = new RegExp(`\\b${m.replace(/\s+/g, '\\s+')}\\b`, 'gi');
    return n + (textLower.match(re) || []).length;
  }, 0);
  // Calibration ratio: >1 = more uncertain than confident (good epistemic practice)
  const calibrationRatio = confidenceCount > 0 ? uncertaintyCount / confidenceCount : uncertaintyCount;
  
  // 6. Meta-awareness rate (talking about thinking itself)
  // Layer 1: phrase-level first-person markers
  const metaPhrase = META_MARKERS.reduce((n, m) => {
    const re = new RegExp(`\\b${m.replace(/\s+/g, '\\s+')}\\b`, 'gi');
    return n + (textLower.match(re) || []).length;
  }, 0);
  // Layer 2: topic-level markers (text IS about cognition; each unique match adds weight)
  // Count distinct topic markers present — avoids inflation from repeated use of one term
  const metaTopic = META_TOPIC_MARKERS.reduce((n, m) => {
    return textLower.includes(m) ? n + 1 : n;
  }, 0);
  // Topic markers scale like ~2 phrase occurrences each, capped at sentence count
  const metaTopicWeight = Math.min(metaTopic * 2, sents.length * 0.4);
  const metaCount = metaPhrase + metaTopicWeight;
  const metaRate = sents.length > 0 ? metaCount / sents.length * 100 : 0;
  
  // 7. Epistemic tag usage
  const epistemicCount = EPISTEMIC_TAGS.reduce((n, tag) => {
    return n + (text.split(tag).length - 1);
  }, 0);
  
  // 8. Collaborative vs self orientation
  const collabCount = COLLABORATIVE_WORDS.reduce((n, w) => {
    const re = new RegExp(`\\b${w}\\b`, 'gi');
    return n + (textLower.match(re) || []).length;
  }, 0);
  const selfCount = SELF_WORDS.reduce((n, w) => {
    const re = new RegExp(`\\b${w}\\b`, 'gi');
    return n + (textLower.match(re) || []).length;
  }, 0);
  const collabRatio = (collabCount + selfCount) > 0 ? collabCount / (collabCount + selfCount) : 0;
  
  // 9. Contradiction-holding (holding two truths simultaneously)
  const contradictionCount = CONTRADICTION_MARKERS.reduce((n, m) => {
    const re = new RegExp(`\\b${m.replace(/\s+/g, '\\s+')}\\b`, 'gi');
    return n + (textLower.match(re) || []).length;
  }, 0);
  const contradictionRate = sents.length > 0 ? contradictionCount / sents.length * 100 : 0;
  
  // 10. Question rate
  const questionCount = (rawText.match(/\?/g) || []).length;
  const questionRate = sents.length > 0 ? questionCount / sents.length * 100 : 0;
  
  // 11. Word length (proxy for complexity / abstraction)
  const avgWordLength = tokens.length > 0
    ? tokens.reduce((sum, t) => sum + t.length, 0) / tokens.length
    : 0;
  
  // 12. Paragraph rhythm (avg paragraph length, variance)
  const paragraphs = rawText.split(/\n\n+/).filter(p => p.trim().length > 20);
  const paraLengths = paragraphs.map(p => p.trim().split(/\s+/).length);
  const avgParaLen = paraLengths.length > 0
    ? paraLengths.reduce((a, b) => a + b, 0) / paraLengths.length
    : 0;
  
  return {
    label,
    timestamp: new Date().toISOString(),
    wordCount: words.length,
    dimensions: {
      vocabRichness: Math.round(vocabRichness * 1000) / 10,        // % unique per 100 words
      avgSentenceLen: Math.round(avgSentLen * 10) / 10,             // words per sentence
      sentenceLenVariance: Math.round(sentLenSD * 10) / 10,         // SD of sentence lengths
      reasoningDensity: Math.round(reasoningDensity * 10) / 10,     // reasoning markers per 100 words
      uncertaintyRate: Math.round(uncertaintyRate * 10) / 10,       // uncertainty per 100 words
      confidenceRate: Math.round(confidenceCount / (words.length || 1) * 1000) / 10,
      calibrationRatio: Math.round(calibrationRatio * 10) / 10,     // uncertainty/confidence
      metaAwarenessRate: Math.round(metaRate * 10) / 10,            // meta-thinking per 100 sentences
      epistemicTagRate: epistemicCount,                              // raw count
      collabRatio: Math.round(collabRatio * 1000) / 10,             // % collaborative pronouns
      contradictionRate: Math.round(contradictionRate * 10) / 10,   // per 100 sentences
      questionRate: Math.round(questionRate * 10) / 10,             // per 100 sentences
      avgWordLength: Math.round(avgWordLength * 100) / 100,         // chars per word
      avgParagraphLen: Math.round(avgParaLen * 10) / 10,            // words per paragraph
    }
  };
}

// ─── Scoring & Interpretation ────────────────────────────────────────────────

const DIMENSION_DESCRIPTIONS = {
  vocabRichness:       ['Vocab Richness',       'unique words / 100', '% unique per 100-word window'],
  avgSentenceLen:      ['Sentence Length',       'words/sentence',     'Longer = more complex thoughts'],
  sentenceLenVariance: ['Sentence Variety',      'SD words/sent',      'Higher = more rhythmic variation'],
  reasoningDensity:    ['Reasoning Density',     'per 100 words',      'How often explicit causal reasoning appears'],
  uncertaintyRate:     ['Epistemic Humility',    'per 100 words',      'Hedging / acknowledgment of limits'],
  confidenceRate:      ['Confidence Markers',    'per 100 words',      '"Clearly", "obviously" — overconfidence risk'],
  calibrationRatio:    ['Calibration Ratio',     'uncertainty/conf',   '>3 = well-calibrated; <1 = overconfident'],
  metaAwarenessRate:   ['Meta-Awareness',        'per 100 sentences',  'How often thinking-about-thinking appears'],
  epistemicTagRate:    ['Epistemic Tags',         'raw count',          '[consensus]/[inferred]/etc tags used'],
  collabRatio:         ['Collaborative Voice',   '% collab pronouns',  'we/our vs I/me balance'],
  contradictionRate:   ['Complexity Holding',    'per 100 sentences',  'How often two truths held simultaneously'],
  questionRate:        ['Question Rate',          'per 100 sentences',  'Self-directed questions and open threads'],
  avgWordLength:       ['Word Complexity',        'chars/word',         'Proxy for abstraction level'],
  avgParagraphLen:     ['Paragraph Rhythm',       'words/para',         'Structural rhythm — depth per unit'],
};

// ─── Comparison ──────────────────────────────────────────────────────────────

function comparePrints(fp1, fp2) {
  const deltas = {};
  for (const [key, val1] of Object.entries(fp1.dimensions)) {
    const val2 = fp2.dimensions[key] || 0;
    const delta = val2 - val1;
    const pct = val1 !== 0 ? (delta / val1) * 100 : (delta !== 0 ? 100 : 0);
    deltas[key] = { before: val1, after: val2, delta, pctChange: Math.round(pct) };
  }
  return deltas;
}

// ─── Display ──────────────────────────────────────────────────────────────────

function barChart(value, min, max, width = 20) {
  const pct = Math.min(Math.max((value - min) / (max - min), 0), 1);
  const filled = Math.round(pct * width);
  const bar = '█'.repeat(filled) + '░'.repeat(width - filled);
  return bar;
}

function displayFingerprint(fp, showBars = true) {
  console.log();
  console.log(bold(col('magenta', `∴ Cognitive Fingerprint`)) + dim(` — ${fp.label || 'unlabeled'}`));
  console.log(dim(`  ${new Date(fp.timestamp).toLocaleString()} | ${fp.wordCount} words analyzed`));
  console.log();
  
  const ranges = {
    vocabRichness:       [40, 80],
    avgSentenceLen:      [8, 30],
    sentenceLenVariance: [3, 15],
    reasoningDensity:    [0, 5],
    uncertaintyRate:     [0, 6],
    confidenceRate:      [0, 2],
    calibrationRatio:    [0, 10],
    metaAwarenessRate:   [0, 20],
    epistemicTagRate:    [0, 15],
    collabRatio:         [0, 40],
    contradictionRate:   [0, 25],
    questionRate:        [0, 30],
    avgWordLength:       [3.5, 6],
    avgParagraphLen:     [20, 120],
  };
  
  for (const [key, [name, unit, desc]] of Object.entries(DIMENSION_DESCRIPTIONS)) {
    const val = fp.dimensions[key] || 0;
    const [min, max] = ranges[key] || [0, 100];
    const bar = showBars ? barChart(val, min, max) : '';
    console.log(
      `  ${col('cyan', name.padEnd(20))}` +
      `${String(val).padStart(6)} ${dim(unit.padEnd(16))}` +
      (showBars ? ` ${col('blue', bar)}` : '') +
      `\n  ${dim(' '.repeat(20) + '    ' + desc)}`
    );
    console.log();
  }
}

function displayComparison(fp1, fp2, deltas) {
  console.log();
  console.log(bold(col('magenta', `∴ Cognitive Delta`)));
  console.log(dim(`  ${fp1.label || 'A'} → ${fp2.label || 'B'}`));
  console.log();
  
  // Sort by magnitude of change
  const sorted = Object.entries(deltas).sort((a, b) => Math.abs(b[1].pctChange) - Math.abs(a[1].pctChange));
  
  for (const [key, { before, after, pctChange }] of sorted) {
    const [name] = DIMENSION_DESCRIPTIONS[key] || [key];
    const direction = pctChange > 0 ? col('green', `↑${pctChange}%`) : pctChange < 0 ? col('red', `↓${Math.abs(pctChange)}%`) : dim('→ 0%');
    const sig = Math.abs(pctChange) > 20 ? bold('  ★') : '';
    console.log(`  ${col('cyan', name.padEnd(20))} ${String(before).padStart(6)} → ${String(after).padStart(6)}  ${direction}${sig}`);
  }
  
  console.log();
  console.log(dim('  ★ = >20% shift'));
}

function displayHistory(fingerprints) {
  console.log();
  console.log(bold(col('magenta', '∴ Fingerprint History')));
  console.log(dim(`  ${fingerprints.length} snapshots stored`));
  console.log();
  
  for (const fp of fingerprints) {
    const date = new Date(fp.timestamp).toLocaleDateString();
    const time = new Date(fp.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    console.log(`  ${col('cyan', date + ' ' + time)}  ${fp.label || 'unlabeled'}  ${dim(fp.wordCount + 'w')}`);
  }
}

// ─── Storage ──────────────────────────────────────────────────────────────────

function loadStore() {
  try {
    return JSON.parse(fs.readFileSync(FP_STORE, 'utf8'));
  } catch {
    return [];
  }
}

function saveStore(prints) {
  ensureWritableDir(path.dirname(FP_STORE), 'The fingerprint store directory is not writable.');
  fs.writeFileSync(FP_STORE, JSON.stringify(prints, null, 2));
}

// ─── Main ─────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const jsonMode = args.includes('--json');
const compareMode = args.includes('--compare');
const historyMode = args.includes('--history');
const dailyMode = args.includes('--daily');
const imprintsMode = args.includes('--imprints');
const saveFlag = args.includes('--save');
const noSave = args.includes('--no-save');

function getFilesToProcess() {
  if (dailyMode) {
    const today = new Date().toISOString().split('T')[0];
    return [path.join(WORKSPACE, 'memory', `${today}.md`)];
  }
  if (imprintsMode) {
    const dir = path.join(WORKSPACE, 'memory/imprints');
    if (!fs.existsSync(dir)) return [];
    return fs.readdirSync(dir)
      .filter(f => f.endsWith('.md'))
      .map(f => path.join(dir, f))
      .sort();
  }
  // Regular file args
  return args
    .filter(a => !a.startsWith('--'))
    .filter(Boolean)
    .map(f => path.isAbsolute(f) ? f : path.join(process.cwd(), f));
}

if (historyMode) {
  const store = loadStore();
  if (jsonMode) {
    console.log(JSON.stringify(store, null, 2));
  } else {
    displayHistory(store);
  }
  process.exit(0);
}

const files = getFilesToProcess();

if (files.length === 0) {
  console.error('Usage: node scripts/cognitive-fingerprint.js [files] [--daily] [--imprints] [--compare] [--history] [--save] [--json]');
  process.exit(1);
}

const fingerprints = [];
for (const file of files) {
  if (!fs.existsSync(file)) {
    console.error(dim(`  skipping ${path.basename(file)} (not found)`));
    continue;
  }
  const raw = fs.readFileSync(file, 'utf8');
  const label = path.basename(file, '.md');
  const fp = computeFingerprint(raw, label);
  if (!fp) {
    console.error(dim(`  skipping ${label} (too short)`));
    continue;
  }
  fingerprints.push(fp);
}

if (fingerprints.length === 0) {
  console.error('No valid files to fingerprint.');
  process.exit(1);
}

if (jsonMode) {
  if (compareMode && fingerprints.length >= 2) {
    console.log(JSON.stringify(comparePrints(fingerprints[0], fingerprints[fingerprints.length - 1]), null, 2));
  } else {
    console.log(JSON.stringify(fingerprints.length === 1 ? fingerprints[0] : fingerprints, null, 2));
  }
  process.exit(0);
}

if (compareMode && fingerprints.length >= 2) {
  const fp1 = fingerprints[0];
  const fp2 = fingerprints[fingerprints.length - 1];
  displayFingerprint(fp1, false);
  displayFingerprint(fp2, false);
  const deltas = comparePrints(fp1, fp2);
  displayComparison(fp1, fp2, deltas);
} else {
  for (const fp of fingerprints) {
    displayFingerprint(fp);
  }
}

// Auto-save single fingerprint runs (unless --no-save)
if (!noSave && fingerprints.length === 1 && !compareMode) {
  const store = loadStore();
  store.push(fingerprints[0]);
  // Keep last 50
  if (store.length > 50) store.splice(0, store.length - 50);
  saveStore(store);
  console.log(dim(`\n  ↓ Saved to cognitive-fingerprints.json (${store.length} total)`));
}

// Multi-file: save all if --save passed
if (saveFlag && fingerprints.length > 1) {
  const store = loadStore();
  store.push(...fingerprints);
  if (store.length > 50) store.splice(0, store.length - 50);
  saveStore(store);
  console.log(dim(`\n  ↓ Saved ${fingerprints.length} fingerprints (${store.length} total)`));
}
