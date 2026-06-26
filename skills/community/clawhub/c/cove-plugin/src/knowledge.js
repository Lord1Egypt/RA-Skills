/**
 * Knowledge Source Reader — loads context from memory, workspace, and custom paths.
 *
 * Works with any OpenClaw installation by reading from standard paths:
 *   ~/.openclaw/workspace/         — user workspace files
 *   ~/.openclaw/workspace/memory/  — agent memory flush files (.md)
 *   ~/.openclaw/memory/main.sqlite — agent memory database (chunks table)
 *   ~/.openclaw/agents/[id]/sessions/ -- skipped, too large
 */

const fs = require('fs');
const path = require('path');

const HOME = require('os').homedir();
const OPENCLAW_DIR = path.join(HOME, '.openclaw');
const WORKSPACE = path.join(OPENCLAW_DIR, 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const MEMORY_DB = path.join(OPENCLAW_DIR, 'memory', 'main.sqlite');

// File extensions we can read as knowledge
const TEXT_EXTENSIONS = new Set([
  '.md', '.txt', '.csv', '.json', '.yaml', '.yml',
  '.xml', '.html', '.log', '.toml', '.ini', '.cfg',
]);

// Directories/files to always skip
const SKIP = new Set([
  'node_modules', '.git', '.DS_Store', 'temp', 'canvas',
  'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
]);

/**
 * Recursively read text files from a directory.
 * @param {string} dir - Directory to scan.
 * @param {number} maxDepth - Maximum recursion depth.
 * @param {number} maxFileSize - Max bytes per file (default 10 KB).
 * @returns {Array<{path: string, content: string}>}
 */
function readDir(dir, maxDepth = 3, maxFileSize = 10240) {
  const results = [];
  const seen = new Set();

  function walk(current, depth) {
    if (depth > maxDepth || seen.has(current)) return;
    seen.add(current);

    let entries;
    try { entries = fs.readdirSync(current, { withFileTypes: true }); }
    catch { return; }

    for (const entry of entries) {
      if (SKIP.has(entry.name) || entry.name.startsWith('.')) continue;
      const fullPath = path.join(current, entry.name);

      if (entry.isDirectory()) {
        walk(fullPath, depth + 1);
      } else if (entry.isFile() && TEXT_EXTENSIONS.has(path.extname(entry.name).toLowerCase())) {
        try {
          const stat = fs.statSync(fullPath);
          if (stat.size > maxFileSize) continue; // skip large files
          const content = fs.readFileSync(fullPath, 'utf8');
          results.push({
            path: path.relative(HOME, fullPath),
            content,
          });
        } catch { /* skip unreadable */ }
      }
    }
  }

  walk(dir, 0);
  return results;
}

/**
 * Read a single file as knowledge source.
 * @param {string} filePath - Absolute or ~-relative path.
 * @returns {{path: string, content: string}|null}
 */
function readFile(filePath) {
  const resolved = filePath.startsWith('~/') ? path.join(HOME, filePath.slice(2)) : path.resolve(filePath);
  try {
    const content = fs.readFileSync(resolved, 'utf8');
    return { path: path.relative(HOME, resolved), content: content.slice(0, 10240) };
  } catch {
    return null;
  }
}

/**
 * Read text chunks from the OpenClaw memory SQLite database.
 * Uses a lightweight pure-JS approach — scans the SQLite file for text
 * content in the 'chunks' table without requiring native SQLite bindings.
 *
 * The chunks table stores: id, path, source, start_line, end_line, hash, model, text, embedding, updated_at
 * We extract the 'text' field which contains the actual memory content.
 *
 * @returns {string[]} Array of memory text chunks.
 */
function readMemoryDb() {
  try {
    if (!fs.existsSync(MEMORY_DB)) return [];
    const buf = fs.readFileSync(MEMORY_DB);
    if (buf.length < 100) return [];

    // Strategy: SQLite stores row data in pages. Text fields in the chunks
    // table contain the actual memory content. We scan for sequences of
    // printable UTF-8 that look like memory entries (longer than 80 chars,
    // not SQL schema, not JSON embeddings, not binary data).
    const chunks = [];
    let current = '';

    for (let i = 0; i < buf.length; i++) {
      const byte = buf[i];
      // Printable ASCII + common UTF-8 + newlines/tabs
      if ((byte >= 32 && byte < 127) || byte === 10 || byte === 13 || byte === 9) {
        current += String.fromCharCode(byte);
      } else {
        if (current.length > 80) {
          const trimmed = current.trim();
          // Filter out SQL schema, embedding vectors, metadata JSON, and index data
          if (trimmed &&
              !trimmed.startsWith('CREATE ') &&
              !trimmed.startsWith('SQLite') &&
              !trimmed.includes('PRIMARY KEY') &&
              !trimmed.includes('UNINDEXED') &&
              !trimmed.includes('WITHOUT ROWID') &&
              !trimmed.startsWith('[') && // embedding arrays
              !trimmed.startsWith('{') && // JSON metadata
              !/^[-0-9.,e\s]+$/.test(trimmed) && // numeric arrays
              !trimmed.includes('idx_') &&
              !trimmed.includes('autoindex')) {
            chunks.push(trimmed);
          }
        }
        current = '';
      }
    }
    // Don't forget the last chunk
    if (current.length > 80) {
      const trimmed = current.trim();
      if (trimmed && !trimmed.startsWith('CREATE ') && !trimmed.startsWith('[') && !trimmed.startsWith('{')) {
        chunks.push(trimmed);
      }
    }

    // Deduplicate and cap at 20KB total
    const seen = new Set();
    const unique = [];
    let totalLen = 0;
    for (const c of chunks) {
      if (seen.has(c) || totalLen > 20000) break;
      seen.add(c);
      unique.push(c);
      totalLen += c.length;
    }

    return unique;
  } catch {
    return [];
  }
}

/**
 * Load all relevant knowledge based on config.
 * Returns a single string of concatenated source contents, capped at 50 KB.
 *
 * @param {object} config - Plugin config with knowledge_sources section.
 * @returns {string} Knowledge context ready for LLM prompt.
 */
function loadKnowledge(config) {
  const sources = config.knowledge_sources || {};
  const allFiles = [];

  // 1. System memory (always on by default)
  if (sources.use_system_memory !== false) {
    // 1a. Memory flush files (markdown)
    allFiles.push(...readDir(MEMORY_DIR, 2));
    // 1b. Memory database (SQLite — extract text chunks)
    const dbChunks = readMemoryDb();
    if (dbChunks.length > 0) {
      allFiles.push({ path: '.openclaw/memory/main.sqlite (chunks)', content: dbChunks.join('\n\n') });
    }
  }

  // 2. Workspace root files (non-recursive, just top-level docs)
  const workspaceFiles = readDir(WORKSPACE, 1);
  allFiles.push(...workspaceFiles);

  // 3. Custom document paths
  if (Array.isArray(sources.document_paths)) {
    for (const docPath of sources.document_paths) {
      const resolved = docPath.startsWith('~/') ? path.join(HOME, docPath.slice(2)) : path.resolve(docPath);
      try {
        const stat = fs.statSync(resolved);
        if (stat.isDirectory()) {
          allFiles.push(...readDir(resolved, 2));
        } else if (stat.isFile()) {
          const f = readFile(resolved);
          if (f) allFiles.push(f);
        }
      } catch { /* skip missing paths */ }
    }
  }

  // 4. Knowledge base files from .openclaw root (agent instructions, etc.)
  const openclawRootFiles = [];
  try {
    const entries = fs.readdirSync(OPENCLAW_DIR, { withFileTypes: true });
    for (const e of entries) {
      if (e.isFile() && (e.name.endsWith('.md') || e.name.endsWith('.txt'))) {
        if (e.name === 'openclaw-sidecar.js') continue; // skip code
        try {
          const content = fs.readFileSync(path.join(OPENCLAW_DIR, e.name), 'utf8');
          if (content.length <= 10240) {
            openclawRootFiles.push({ path: `.openclaw/${e.name}`, content });
          }
        } catch { /* skip */ }
      }
    }
  } catch { /* skip */ }
  allFiles.push(...openclawRootFiles);

  // Deduplicate by path
  const seen = new Set();
  const unique = [];
  for (const f of allFiles) {
    if (!seen.has(f.path)) {
      seen.add(f.path);
      unique.push(f);
    }
  }

  // Build context string, capped at 50KB
  let context = '';
  let totalSize = 0;
  const MAX_CONTEXT = 50000;

  for (const f of unique) {
    const entry = `\n--- FILE: ${f.path} ---\n${f.content}\n`;
    if (totalSize + entry.length > MAX_CONTEXT) break;
    context += entry;
    totalSize += entry.length;
  }

  return context;
}

module.exports = { loadKnowledge, readDir, readFile, readMemoryDb };
