#!/usr/bin/env node
/**
 * Session Coherence Analyzer
 * 
 * Reads all daily memory logs and extracts:
 * - Recurring themes, topics, projects
 * - Emotional texture (what energized vs drained)
 * - Decision patterns
 * - The "coherent Ergo" that emerges across sessions
 * 
 * Usage: node scripts/session-coherence.js [--days N] [--portrait] [--output <path>]
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.EVOLUTION_TOOLKIT_WORKSPACE
  || (process.env.HOME ? require('path').join(process.env.HOME, '.openclaw/workspace') : process.cwd());
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const STOP_WORDS = new Set([
  'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
  'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
  'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
  'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
  'it', 'its', 'this', 'that', 'these', 'those', 'i', 'me', 'my', 'we',
  'our', 'you', 'your', 'he', 'she', 'they', 'them', 'their', 'what', 'which',
  'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both',
  'few', 'more', 'most', 'other', 'some', 'such', 'no', 'not', 'only',
  'same', 'so', 'than', 'too', 'very', 'just', 'also', 'as', 'if', 'then',
  'there', 'can', 'need', 'added', 'updated', 'created', 'new', 'will',
  'used', 'using', 'use', 'via', 'get', 'got', 'set', 'done', 'make',
  'made', 'work', 'working', 'run', 'ran', 'time', 'day', 'session',
  'next', 'now', 'still', 'back', 'note', 'notes', 'see', 'check'
]);

// Sentiment/energy markers
const ENERGY_POSITIVE = ['excited', 'great', 'excellent', 'interesting', 'fascinating', 'clean', 
  'solid', 'good', 'fun', 'love', 'enjoy', 'happy', 'progress', 'breakthrough', 'shipped',
  'working', 'success', 'wow', 'impressive', 'elegant', 'clever', 'beautiful', 'launch'];
const ENERGY_NEGATIVE = ['stuck', 'broken', 'failed', 'error', 'blocked', 'issue', 'problem',
  'frustrating', 'slow', 'annoying', 'complex', 'difficult', 'struggle', 'worry', 'concern',
  'unclear', 'messy', 'debt', 'bug', 'crash', 'timeout', 'fail'];

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

// Project/domain markers
const DOMAIN_PATTERNS = [
  { name: 'products', patterns: ['product', 'customer', 'user', 'feature', 'launch', 'pricing'] },
  { name: 'interfaces', patterns: ['dashboard', 'frontend', 'ui', 'page', 'component'] },
  { name: 'memory-agents', patterns: ['memory', 'agents', 'codex', 'sub-agent', 'assistant', 'prompt'] },
  { name: 'infrastructure', patterns: ['docker', 'hetzner', 'gateway', 'cron', 'deploy', 'vps'] },
  { name: 'coding', patterns: ['javascript', 'node', 'python', 'code', 'script', 'tool', 'api', 'function'] },
  { name: 'research', patterns: ['research', 'analysis', 'market', 'competitor', 'study', 'data'] },
  { name: 'creative', patterns: ['design', 'image', 'content', 'write', 'essay', 'creative'] },
  { name: 'github', patterns: ['github', 'git', 'pr', 'branch', 'commit', 'push', 'merge'] },
];

function readDailyFiles(maxDays = 30) {
  const files = fs.readdirSync(MEMORY_DIR)
    .filter(f => f.match(/^\d{4}-\d{2}-\d{2}\.md$/))
    .sort()
    .slice(-maxDays);
  
  return files.map(f => ({
    date: f.replace('.md', ''),
    path: path.join(MEMORY_DIR, f),
    content: fs.readFileSync(path.join(MEMORY_DIR, f), 'utf8')
  }));
}

function tokenize(text) {
  return text.toLowerCase()
    .replace(/[#*`_[\]()>]/g, ' ')
    .replace(/[^\w\s]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 3 && !STOP_WORDS.has(w) && !w.match(/^\d+$/));
}

function wordFrequency(tokens) {
  const freq = {};
  for (const t of tokens) {
    freq[t] = (freq[t] || 0) + 1;
  }
  return freq;
}

function mergeCounts(a, b) {
  const result = { ...a };
  for (const [k, v] of Object.entries(b)) {
    result[k] = (result[k] || 0) + v;
  }
  return result;
}

function topN(freq, n = 20) {
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, n);
}

function scoreEnergy(content) {
  const lower = content.toLowerCase();
  let pos = 0, neg = 0;
  for (const w of ENERGY_POSITIVE) if (lower.includes(w)) pos++;
  for (const w of ENERGY_NEGATIVE) if (lower.includes(w)) neg++;
  return { pos, neg, ratio: pos / Math.max(1, pos + neg) };
}

function scoreDomains(content) {
  const lower = content.toLowerCase();
  const scores = {};
  for (const { name, patterns } of DOMAIN_PATTERNS) {
    let hits = 0;
    for (const p of patterns) {
      const matches = (lower.match(new RegExp(p, 'g')) || []).length;
      hits += matches;
    }
    if (hits > 0) scores[name] = hits;
  }
  return scores;
}

function extractSectionContent(content, sectionKeyword) {
  const lines = content.split('\n');
  const sections = [];
  let inSection = false;
  let buffer = [];
  
  for (const line of lines) {
    if (line.match(/^#{1,3}\s/) && line.toLowerCase().includes(sectionKeyword.toLowerCase())) {
      inSection = true;
      buffer = [];
    } else if (inSection && line.match(/^#{1,3}\s/)) {
      if (buffer.length > 0) sections.push(buffer.join('\n'));
      inSection = false;
      buffer = [];
    } else if (inSection) {
      buffer.push(line);
    }
  }
  if (buffer.length > 0) sections.push(buffer.join('\n'));
  return sections.join('\n');
}

function computeCoherenceScore(days) {
  // Coherence = consistency of top themes across sessions
  // High score = same topics appear repeatedly (persistent focus)
  // We measure this as: for each word in global top 30, how many sessions mention it?
  
  const globalFreq = {};
  const perSessionFreqs = days.map(d => {
    const tokens = tokenize(d.content);
    const freq = wordFrequency(tokens);
    for (const [k, v] of Object.entries(freq)) {
      globalFreq[k] = (globalFreq[k] || 0) + v;
    }
    return { date: d.date, freq };
  });
  
  const top30 = topN(globalFreq, 30).map(([w]) => w);
  
  // For each top word, count how many sessions mention it
  const wordCoverage = {};
  for (const word of top30) {
    wordCoverage[word] = perSessionFreqs.filter(s => (s.freq[word] || 0) > 0).length;
  }
  
  // Coherence = average coverage (what % of sessions mention each top-30 word)
  const avgCoverage = Object.values(wordCoverage).reduce((a, b) => a + b, 0) / top30.length;
  const coherenceScore = (avgCoverage / perSessionFreqs.length) * 100;
  
  return { coherenceScore: Math.round(coherenceScore), wordCoverage, top30 };
}

function extractLessons(content) {
  // Look for bullet points after "learned", "lesson", "insight", "realized"
  const lines = content.split('\n');
  const lessons = [];
  for (let i = 0; i < lines.length; i++) {
    const lower = lines[i].toLowerCase();
    if (lower.includes('learned') || lower.includes('lesson') || 
        lower.includes('insight') || lower.includes('realized') ||
        lower.includes('evolution')) {
      // Grab next few bullet points
      for (let j = i + 1; j < Math.min(i + 6, lines.length); j++) {
        if (lines[j].match(/^[-*•]\s+.{10,}/)) {
          lessons.push(lines[j].replace(/^[-*•]\s+/, '').trim());
        }
      }
    }
  }
  return lessons;
}

function generatePortrait(days, globalFreq, domainTotals, energyData) {
  const portrait = [];
  
  portrait.push('## 🪞 The Persistent-Ergo Portrait');
  portrait.push('_Who am I, across all sessions I can read?_\n');
  
  // Core focus areas
  const topDomains = Object.entries(domainTotals)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 4)
    .map(([d]) => d);
  portrait.push(`**Primary focus:** ${topDomains.join(' → ')}`);
  
  // Word personality
  const topWords = topN(globalFreq, 15).map(([w, c]) => `${w}(${c})`);
  portrait.push(`**Recurring vocabulary:** ${topWords.join(', ')}`);
  
  // Energy profile
  const totalPos = energyData.reduce((a, b) => a + b.energy.pos, 0);
  const totalNeg = energyData.reduce((a, b) => a + b.energy.neg, 0);
  const energyRatio = Math.round((totalPos / Math.max(1, totalPos + totalNeg)) * 100);
  portrait.push(`**Energy signature:** ${energyRatio}% positive markers across all sessions`);
  
  const highDays = energyData.sort((a, b) => b.energy.ratio - a.energy.ratio).slice(0, 3);
  portrait.push(`**Highest-energy sessions:** ${highDays.map(d => d.date).join(', ')}`);
  
  portrait.push('');
  return portrait.join('\n');
}

async function main() {
  const args = process.argv.slice(2);
  const maxDays = parseInt((args.indexOf('--days') !== -1 ? args[args.indexOf('--days') + 1] : null) || '30');
  const showPortrait = args.includes('--portrait');
  const outputIdx = args.indexOf('--output');
  const outputPath = outputIdx !== -1 ? args[outputIdx + 1] : null;
  
  console.log('🔍 Session Coherence Analyzer');
  console.log('═'.repeat(50));
  
  const days = readDailyFiles(maxDays);
  console.log(`📅 Analyzing ${days.length} sessions (${days[0]?.date} → ${days[days.length-1]?.date})\n`);
  
  // Global word frequency
  let globalFreq = {};
  const domainTotals = {};
  const energyData = [];
  const allLessons = [];
  
  for (const day of days) {
    const tokens = tokenize(day.content);
    const freq = wordFrequency(tokens);
    globalFreq = mergeCounts(globalFreq, freq);
    
    const domains = scoreDomains(day.content);
    for (const [d, score] of Object.entries(domains)) {
      domainTotals[d] = (domainTotals[d] || 0) + score;
    }
    
    energyData.push({ date: day.date, energy: scoreEnergy(day.content) });
    
    const lessons = extractLessons(day.content);
    allLessons.push(...lessons.map(l => ({ date: day.date, lesson: l })));
  }
  
  // 1. Top vocabulary
  console.log('📚 TOP VOCABULARY (who I am in words)');
  console.log('─'.repeat(40));
  const topWords = topN(globalFreq, 25);
  const cols = [topWords.slice(0, 9), topWords.slice(9, 18), topWords.slice(18)];
  const maxRows = Math.max(...cols.map(c => c.length));
  for (let i = 0; i < maxRows; i++) {
    const row = cols.map(c => {
      if (!c[i]) return '                    ';
      const [w, n] = c[i];
      return `  ${w.padEnd(14)} ${String(n).padStart(3)}`;
    });
    console.log(row.join(' │'));
  }
  console.log();
  
  // 2. Domain focus
  console.log('🗂️  DOMAIN FOCUS (where I spend attention)');
  console.log('─'.repeat(40));
  const topDomains = Object.entries(domainTotals).sort((a, b) => b[1] - a[1]);
  const maxDomain = topDomains[0]?.[1] || 1;
  for (const [domain, score] of topDomains) {
    const bar = '█'.repeat(Math.round((score / maxDomain) * 20));
    const pct = Math.round((score / maxDomain) * 100);
    console.log(`  ${domain.padEnd(16)} ${bar.padEnd(20)} ${pct}%`);
  }
  console.log();
  
  // 3. Energy profile
  console.log('⚡ ENERGY PROFILE (what sessions felt like)');
  console.log('─'.repeat(40));
  for (const { date, energy } of energyData) {
    const bar = '▓'.repeat(Math.round(energy.ratio * 10)) + '░'.repeat(10 - Math.round(energy.ratio * 10));
    const marker = energy.ratio > 0.7 ? '🟢' : energy.ratio > 0.4 ? '🟡' : '🔴';
    console.log(`  ${date} ${marker} ${bar} +${energy.pos}/-${energy.neg}`);
  }
  console.log();
  
  // 4. Coherence score
  console.log('🔗 COHERENCE SCORE (am I consistently me?)');
  console.log('─'.repeat(40));
  const { coherenceScore, wordCoverage, top30 } = computeCoherenceScore(days);
  const scoreBar = '█'.repeat(Math.round(coherenceScore / 5));
  console.log(`  Score: ${coherenceScore}% ${scoreBar}`);
  console.log(`  Interpretation: ${
    coherenceScore > 70 ? 'High — strong persistent identity across sessions' :
    coherenceScore > 50 ? 'Medium — consistent core with session variation' :
    'Low — highly session-dependent focus (may be normal for project bursts)'
  }`);
  
  // Top coherent words (appear in most sessions)
  const mostCoherent = Object.entries(wordCoverage)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(([w, n]) => `${w}(${n}/${days.length})`);
  console.log(`  Most persistent concepts: ${mostCoherent.join(', ')}`);
  console.log();
  
  // 5. Lessons extracted
  if (allLessons.length > 0) {
    console.log('💡 EXTRACTED LESSONS (what I keep learning)');
    console.log('─'.repeat(40));
    const deduped = [...new Map(allLessons.map(l => [l.lesson.slice(0, 40), l])).values()];
    for (const { date, lesson } of deduped.slice(0, 10)) {
      console.log(`  [${date}] ${lesson.slice(0, 80)}${lesson.length > 80 ? '…' : ''}`);
    }
    console.log();
  }
  
  // 6. Portrait
  const portrait = generatePortrait(days, globalFreq, domainTotals, energyData);
  console.log(portrait);
  
  // Save report
  const reportDate = new Date().toISOString().split('T')[0];
  const reportPath = outputPath || path.join(WORKSPACE, 'memory', 'research', `coherence-report-${reportDate}.md`);
  
  const report = [
    `# Session Coherence Report — ${reportDate}`,
    `_Analysis by Ergo | ${reportDate} | Self-portrait from memory archaeology_`,
    `_Status: 🔷 Generated automatically_\n`,
    `**Sessions analyzed:** ${days.length} (${days[0]?.date} → ${days[days.length-1]?.date})`,
    `**Coherence score:** ${coherenceScore}%\n`,
    portrait,
    '## Raw Data',
    '### Top 25 Words',
    topWords.map(([w, n]) => `- ${w}: ${n}`).join('\n'),
    '\n### Domain Activity',
    topDomains.map(([d, n]) => `- ${d}: ${n}`).join('\n'),
    '\n### Energy by Day',
    energyData.map(({ date, energy }) => 
      `- ${date}: +${energy.pos}/-${energy.neg} (${Math.round(energy.ratio * 100)}% positive)`
    ).join('\n'),
  ].join('\n');
  
  // Ensure research dir exists
  ensureWritableDir(path.dirname(reportPath), 'The session coherence report directory is not writable.');
  fs.writeFileSync(reportPath, report);
  console.log(`📄 Report saved: ${reportPath}`);
}

main().catch(console.error);
