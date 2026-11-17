#!/usr/bin/env node
/**
 * Research Assistant — Knowledge builder from web/docs/files
 * 
 * Modes:
 *   --extract <url> or <file>           → Extract entities and key facts
 *   --extract --all <dir>               → Extract from all files in directory
 *   --search <query>                    → Search knowledge base
 *   --search --query <query>            → Entity-aware search
 *   --add <file>                        → Add file to knowledge base
 *   --add --url <url>                   → Add URL to knowledge base
 *   --graph                             → Show knowledge graph
 *   --summarize <query>                 → Auto-summarize on topic
 *   --status                            → Knowledge base status
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

const WORKSPACE = (() => {
  if (process.env.RESEARCH_DIR) return process.env.RESEARCH_DIR;
  let dir = __dirname;
  for (let i = 0; i < 10; i++) {
    if (fs.existsSync(path.join(dir, 'MEMORY.md'))) return dir;
    dir = path.resolve(dir, '..');
  }
  return path.resolve(__dirname, '..', '..');
})();

const DATA_DIR = path.join(WORKSPACE, 'memory', 'research');
const KB_FILE = path.join(DATA_DIR, 'knowledge-base.json');
const INDEX_FILE = path.join(DATA_DIR, 'index.json');
const RELATIONS_FILE = path.join(DATA_DIR, 'relations.json');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function loadJSON(file, fallback) {
  try {
    const data = fs.readFileSync(file, 'utf8');
    return JSON.parse(data);
  } catch { return fallback || {}; }
}

function saveJSON(file, data) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
}

function getToday() {
  return new Date().toISOString().split('T')[0];
}

function normalizeText(text) {
  return text.toLowerCase().replace(/[\s_\-]+/g, ' ').trim();
}

// ─── ENTITY EXTRACTION ─────────────────────────────────────────────────────

function extractEntities(text) {
  const entities = [];
  const relations = [];
  
  // Extract capitalized phrases (potential proper nouns)
  const capitalizedPhrases = text.match(/[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*/g) || [];
  for (const phrase of capitalizedPhrases) {
    if (phrase.length > 3 && !['This', 'That', 'These', 'Those', 'There', 'Their', 'They', 'What', 'When', 'Where', 'Which', 'Who', 'How', 'Why', 'Could', 'Would', 'Should', 'May', 'Must', 'Can', 'Will', 'Have', 'Has', 'Had', 'Are', 'Was', 'Were', 'Be', 'Being', 'Been', 'And', 'But', 'For', 'Nor', 'Or', 'So', 'Yet', 'The', 'A', 'An', 'In', 'On', 'At', 'To', 'By', 'Of', 'With', 'From', 'About', 'After', 'Before', 'During', 'Between', 'Through', 'Under', 'Over', 'Up', 'Down', 'Out', 'Off', 'Into', 'Onto', 'Upon', 'Within', 'Without', 'Against', 'Along', 'Around', 'Aside', 'Behind', 'Below', 'Beneath', 'Beside', 'Beyond', 'Below', 'Below', 'Below'].includes(phrase)) {
      entities.push({ name: phrase, type: 'proper_noun', count: 1 });
    }
  }
  
  // Extract numbers/dates
  const numbers = text.match(/\b\d{4}[-/]\d{2}[-/]\d{2}\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d+\b/g) || [];
  for (const num of numbers) {
    if (num.length >= 4) {
      entities.push({ name: num, type: 'number', count: 1 });
    }
  }
  
  // Extract URLs
  const urls = text.match(/https?:\/\/[^\s<>"{}|\\^`\[\]]+/gi) || [];
  for (const url of urls) {
    entities.push({ name: url, type: 'url', count: 1 });
  }
  
  // NOTE: Email addresses are intentionally NOT extracted to avoid PII leakage
  
  // Extract relationships (X is Y, X was Y, X became Y)
  const relationshipPatterns = [
    /([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is|was|became|serves as|works as|known as)\s+([A-Z][a-z]+)/g,
    /([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:of|at|from|in)\s+([A-Z][a-z]+)/g
  ];
  
  for (const pattern of relationshipPatterns) {
    let match;
    while ((match = pattern.exec(text)) !== null) {
      relations.push({ from: match[1], to: match[2], type: 'associated_with' });
    }
  }
  
  // Deduplicate entities
  const entityMap = new Map();
  for (const e of entities) {
    const key = e.name.toLowerCase();
    if (entityMap.has(key)) {
      entityMap.get(key).count++;
    } else {
      entityMap.set(key, { ...e });
    }
  }
  
  return {
    entities: Array.from(entityMap.values()).sort((a, b) => b.count - a.count),
    relations
  };
}

// ─── EXTRACT ───────────────────────────────────────────────────────────────

function extractFromFile(filepath) {
  const content = fs.readFileSync(filepath, 'utf8');
  const extracted = extractEntities(content);
  
  // Also extract summary (first paragraph or 200 chars)
  const summary = content.split('\n').find(line => line.trim().length > 50)?.substring(0, 200) || content.substring(0, 200);
  
  return {
    source: filepath,
    summary,
    entities: extracted.entities,
    relations: extracted.relations,
    wordCount: content.split(/\s+/).length,
    lineCount: content.split('\n').length,
    extractedAt: getToday()
  };
}

async function extractFromUrl(url) {
  return new Promise((resolve, reject) => {
    const isHttps = url.startsWith('https');
    const client = isHttps ? https : http;
    
    const req = client.get(url, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }
      
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        // Strip HTML tags
        const text = data.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
        const extracted = extractEntities(text);
        
        resolve({
          source: url,
          summary: text.substring(0, 200),
          entities: extracted.entities,
          relations: extracted.relations,
          wordCount: text.split(/\s+/).length,
          extractedAt: getToday()
        });
      });
    });
    
    req.on('error', reject);
    req.setTimeout(10000, () => { req.destroy(); reject(new Error('Timeout')); });
  });
}

// ─── KNOWLEDGE BASE ────────────────────────────────────────────────────────

function addToKB(entry) {
  const kb = loadJSON(KB_FILE, []);
  const index = loadJSON(INDEX_FILE, {});
  const relations = loadJSON(RELATIONS_FILE, []);
  
  // Add to KB
  kb.push(entry);
  if (kb.length > 1000) kb.splice(0, kb.length - 1000);
  saveJSON(KB_FILE, kb);
  
  // Update index
  for (const entity of entry.entities) {
    const key = entity.name.toLowerCase();
    if (!index[key]) index[key] = [];
    if (!index[key].find(e => e.source === entry.source)) {
      index[key].push({ source: entry.source, type: entity.type });
    }
  }
  saveJSON(INDEX_FILE, index);
  
  // Update relations
  for (const r of entry.relations) {
    if (!relations.find(rel => rel.from === r.from && rel.to === r.to)) {
      relations.push(r);
    }
  }
  saveJSON(RELATIONS_FILE, relations);
  
  console.log(`[research-assistant] Added: ${entry.source} (${entry.entities.length} entities, ${entry.relations.length} relations)`);
}

// ─── SEARCH ────────────────────────────────────────────────────────────────

function searchKB(query) {
  const kb = loadJSON(KB_FILE, []);
  const index = loadJSON(INDEX_FILE, {});
  const queryLower = normalizeText(query);
  
  // Check index first
  if (index[queryLower]) {
    const sources = index[queryLower].map(e => e.source);
    console.log(`[research-assistant] Found in index for "${query}":`);
    for (const s of sources) console.log(`  → ${s}`);
  }
  
  // Search KB
  const results = [];
  for (const entry of kb) {
    let score = 0;
    
    // Check entities
    for (const entity of entry.entities) {
      if (normalizeText(entity.name).includes(queryLower)) {
        score += entity.count * 2;
      }
    }
    
    // Check summary
    if (normalizeText(entry.summary).includes(queryLower)) {
      score += 1;
    }
    
    if (score > 0) {
      results.push({ ...entry, score });
    }
  }
  
  return results.sort((a, b) => b.score - a.score);
}

// ─── GRAPH ─────────────────────────────────────────────────────────────────

function showGraph() {
  const relations = loadJSON(RELATIONS_FILE, []);
  const kb = loadJSON(KB_FILE, []);
  
  console.log(`[research-assistant] Knowledge graph:\n`);
  console.log(`  Sources: ${kb.length}`);
  console.log(`  Relations: ${relations.length}`);
  
  // Group relations by type
  const byType = {};
  for (const r of relations) {
    if (!byType[r.type]) byType[r.type] = [];
    byType[r.type].push(r);
  }
  
  for (const [type, rels] of Object.entries(byType)) {
    console.log(`\n  ${type}: ${rels.length}`);
    for (const r of rels.slice(0, 10)) {
      console.log(`    ${r.from} → ${r.to}`);
    }
    if (rels.length > 10) console.log(`    ... and ${rels.length - 10} more`);
  }
}

// ─── SUMMARIZE ─────────────────────────────────────────────────────────────

function summarize(query) {
  const kb = loadJSON(KB_FILE, []);
  const results = searchKB(query);
  
  if (results.length === 0) {
    console.log(`[research-assistant] No results for: "${query}"`);
    return;
  }
  
  console.log(`[research-assistant] Summary for "${query}":\n`);
  
  // Collect relevant entities
  const entityMap = new Map();
  for (const r of results) {
    for (const e of r.entities) {
      if (e.count >= 2) {
        if (!entityMap.has(e.name.toLowerCase())) {
          entityMap.set(e.name.toLowerCase(), e);
        }
      }
    }
  }
  
  console.log('  Key entities:');
  for (const [, e] of entityMap) {
    console.log(`    • ${e.name} (${e.type})`);
  }
  
  console.log('\n  Sources:');
  for (const r of results.slice(0, 5)) {
    console.log(`    • ${r.source}`);
  }
  
  console.log('\n  Snippets:');
  for (const r of results.slice(0, 3)) {
    console.log(`    "${r.summary.substring(0, 100)}..."`);
  }
}

// ─── STATUS ────────────────────────────────────────────────────────────────

function showStatus() {
  const kb = loadJSON(KB_FILE, []);
  const index = loadJSON(INDEX_FILE, {});
  const relations = loadJSON(RELATIONS_FILE, []);
  
  console.log('[research-assistant] Knowledge base status:\n');
  console.log(`  Sources indexed: ${kb.length}`);
  console.log(`  Unique entities: ${Object.keys(index).length}`);
  console.log(`  Relations: ${relations.length}`);
  
  // Entity type breakdown
  const typeBreakdown = {};
  for (const entry of kb) {
    for (const e of entry.entities) {
      if (!typeBreakdown[e.type]) typeBreakdown[e.type] = 0;
      typeBreakdown[e.type] += e.count;
    }
  }
  
  console.log('\n  Entity types:');
  for (const [type, count] of Object.entries(typeBreakdown).sort((a, b) => b[1] - a[1]).slice(0, 10)) {
    console.log(`    ${type}: ${count}`);
  }
}

// ─── CLI ───────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
let mode = 'status';
let searchQuery = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--extract') mode = 'extract';
  if (args[i] === '--search') mode = 'search';
  if (args[i] === '--add') mode = 'add';
  if (args[i] === '--graph') mode = 'graph';
  if (args[i] === '--summarize') mode = 'summarize';
  if (args[i] === '--status') mode = 'status';
  if (args[i] === '--all') searchQuery = 'all';
  if (args[i] === '--query' && i + 1 < args.length) searchQuery = args[i + 1];
  if (args[i] === '--url' && i + 1 < args.length) searchQuery = args[i + 1];
  if (args[i] === '--dir' && i + 1 < args.length) process.env.RESEARCH_DIR = args[i + 1];
}

(async () => {
  switch (mode) {
    case 'extract': {
      const target = args[1];
      if (!target) {
        console.log('Usage: research-assistant.js --extract <file|url>');
      } else if (searchQuery === 'all') {
        const files = fs.readdirSync(target).filter(f => f.endsWith('.md') || f.endsWith('.txt') || f.endsWith('.json'));
        for (const f of files) {
          const entry = extractFromFile(path.join(target, f));
          addToKB(entry);
        }
        console.log(`[research-assistant] Extracted ${files.length} files from ${target}`);
      } else {
        let entry;
        if (target.startsWith('http')) {
          entry = await extractFromUrl(target);
        } else {
          entry = extractFromFile(target);
        }
        addToKB(entry);
      }
      break;
    }
    case 'search': {
      const query = searchQuery || args[1];
      if (!query) {
        console.log('Usage: research-assistant.js --search <query>');
      } else {
        const results = searchKB(query);
        console.log(`[research-assistant] Found ${results.length} results for "${query}":\n`);
        for (const r of results.slice(0, 10)) {
          console.log(`  ✅ ${r.score} — ${r.source}`);
          console.log(`     "${r.summary.substring(0, 80)}..."`);
        }
      }
      break;
    }
    case 'add': {
      const target = searchQuery || args[1];
      if (!target) {
        console.log('Usage: research-assistant.js --add <file|url>');
      } else {
        let entry;
        if (target.startsWith('http')) {
          entry = await extractFromUrl(target);
        } else {
          entry = extractFromFile(target);
        }
        addToKB(entry);
      }
      break;
    }
    case 'graph':
      showGraph();
      break;
    case 'summarize': {
      const query = searchQuery || args[2];
      if (!query) {
        console.log('Usage: research-assistant.js --summarize <query>');
      } else {
        summarize(query);
      }
      break;
    }
    default:
      showStatus();
      break;
  }
})();
