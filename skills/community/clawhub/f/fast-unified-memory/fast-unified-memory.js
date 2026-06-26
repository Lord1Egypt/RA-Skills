#!/usr/bin/env node
/**
 * Unified Memory CLI
 * Integrates: OpenClaw Memory + Fast Mem0
 * Uses: Ollama nomic-embed-text (~100-120ms total)
 * 
 * Usage: unified-memory <command> [args]
 * 
 * Commands:
 *   search <query>     - Search both memory systems
 *   add <text>        - Add to Fast Mem0
 *   list              - List Fast Mem0 memories
 *   stats             - Show memory system stats
 */

const OLLAMA_URL = 'http://localhost:11434';
const FS = await import('fs');
const PATH = await import('path');

// ============== FAST MEM0 ==============
const MEM0_STORE = process.env.HOME + '/.mem0/fast-store.json';

function getMem0Store() {
  try {
    if (!FS.existsSync(MEM0_STORE)) {
      FS.writeFileSync(MEM0_STORE, JSON.stringify({ memories: [] }));
    }
    return JSON.parse(FS.readFileSync(MEM0_STORE, 'utf-8'));
  } catch {
    return { memories: [] };
  }
}

function saveMem0Store(store) {
  FS.writeFileSync(MEM0_STORE, JSON.stringify(store, null, 2));
}

function cosineSim(a, b) {
  const dot = a.reduce((sum, v, i) => sum + v * b[i], 0);
  const magA = Math.sqrt(a.reduce((s, v) => s + v * v, 0));
  const magB = Math.sqrt(b.reduce((s, v) => s + v * v, 0));
  return dot / (magA * magB);
}

// ============== OPENCLAW MEMORY ==============
const MEMORY_DIR = '/home/broedkrummen/.openclaw/workspace/memory';

// Get embedding from Ollama
async function getEmbedding(text) {
  const res = await fetch(`${OLLAMA_URL}/api/embeddings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: 'nomic-embed-text', prompt: text })
  });
  const data = await res.json();
  return data.embedding;
}

// Search OpenClaw memory files (keyword-based for speed)
async function searchOpenClaw(query) {
  const start = Date.now();
  const results = [];
  const q = query.toLowerCase();
  
  try {
    const files = FS.readdirSync(MEMORY_DIR).filter(f => f.endsWith('.md'));
    for (const file of files) {
      const content = FS.readFileSync(PATH.join(MEMORY_DIR, file), 'utf-8');
      if (content.toLowerCase().includes(q)) {
        const lines = content.split('\n').filter(l => l.toLowerCase().includes(q));
        results.push({ file, snippet: lines[0]?.substring(0, 100) });
      }
    }
  } catch {}
  
  return { results, time: Date.now() - start };
}

// Search Fast Mem0
async function searchMem0(query, limit = 5) {
  const start = Date.now();
  
  try {
    const queryEmbed = await getEmbedding(query);
    const store = getMem0Store();
    const results = store.memories
      .map(m => ({ ...m, score: cosineSim(queryEmbed, m.embedding) }))
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
    
    return { results, time: Date.now() - start };
  } catch (e) {
    return { error: e.message, time: Date.now() - start };
  }
}

// Add to Mem0
async function addMem0(text, userId = 'broedkrummen') {
  const start = Date.now();
  
  try {
    const embedding = await getEmbedding(text);
    const store = getMem0Store();
    store.memories.push({
      id: Date.now().toString(),
      memory: text,
      user_id: userId,
      embedding,
      metadata: { created_at: new Date().toISOString() }
    });
    saveMem0Store(store);
    
    return { success: true, time: Date.now() - start };
  } catch (e) {
    return { error: e.message, time: Date.now() - start };
  }
}

// List Mem0
async function listMem0(userId = 'broedkrummen') {
  const store = getMem0Store();
  return store.memories.filter(m => m.user_id === userId);
}

// ============== UNIFIED SEARCH ==============
async function searchAll(query) {
  console.log(`\n🔍 Searching: "${query}"\n`);
  
  const [mem0, openclaw] = await Promise.all([
    searchMem0(query),
    searchOpenClaw(query)
  ]);
  
  console.log('=== Fast Mem0 Results ===');
  console.log(`Time: ${mem0.time}ms`);
  if (mem0.results?.length > 0) {
    mem0.results.forEach((m, i) => {
      console.log(`  ${i + 1}. [${m.score?.toFixed(3)}] ${m.memory}`);
    });
  } else {
    console.log('  No results');
  }
  
  console.log('\n=== OpenClaw Memory ===');
  console.log(`Time: ${openclaw.time}ms`);
  if (openclaw.results?.length > 0) {
    openclaw.results.forEach((r, i) => {
      console.log(`  ${i + 1}. ${r.file}: ${r.snippet}...`);
    });
  } else {
    console.log('  No results');
  }
  
  console.log(`\n⚡ Total: ${mem0.time + openclaw.time}ms`);
}

// ============== CLI ==============
const args = process.argv.slice(2);
const cmd = args[0];

switch (cmd) {
  case 'search':
    if (!args[1]) {
      console.log('Usage: unified-memory search <query>');
      process.exit(1);
    }
    searchAll(args.slice(1).join(' '));
    break;
    
  case 'add':
    if (!args[1]) {
      console.log('Usage: unified-memory add <text>');
      process.exit(1);
    }
    addMem0(args.slice(1).join(' ')).then(r => {
      console.log(r.success ? `✅ Added in ${r.time}ms` : `❌ Error: ${r.error}`);
    });
    break;
    
  case 'list':
    listMem0().then(memories => {
      console.log(`\n📋 ${memories.length} memories:\n`);
      memories.forEach((m, i) => console.log(`${i + 1}. ${m.memory}`));
    });
    break;
    
  case 'stats':
    console.log(`
╔═══════════════════════════════════════╗
║      UNIFIED MEMORY SYSTEM            ║
╠═══════════════════════════════════════╣
║  Provider: Ollama (nomic-embed-text)║
║  Embedding: ~40ms                     ║
║  Search: ~100-120ms total             ║
╠═══════════════════════════════════════╣
║  Fast Mem0: ~/.mem0/fast-store.json   ║
║  OpenClaw: ~/.openclaw/workspace/memory/║
╚═══════════════════════════════════════╝
`);
    break;
    
  default:
    console.log(`
Unified Memory CLI

Commands:
  search <query>   - Search both memory systems
  add <text>       - Add to Fast Mem0
  list             - List Mem0 memories
  stats            - Show system stats

Speed: ~100-120ms total
Provider: Ollama (nomic-embed-text)
`);
}
