/**
 * Sync Engine - Core synchronization logic
 * Note-aware merging engine for OpenClaw ↔ Obsidian bidirectional sync
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Import tracker
const tracker = require('./tracker');

// Configuration
const CONFIG = {
  memoryDir: path.join(process.env.HOME, '.openclaw/workspace/memory'),
  vaultInbox: path.join(process.env.HOME, 'obsidian-vault/OpenClaw/Inbox'),
  vaultDaily: path.join(process.env.HOME, 'obsidian-vault/OpenClaw/Daily'),
  vaultArchive: path.join(process.env.HOME, 'obsidian-vault/OpenClaw/Archive'),
  attributionPrefix: '> 📥 *Synced from',
  separator: '\n\n---\n\n',
};

/**
 * Generate a hash for content to detect duplicates
 * @param {string} content - Content to hash
 * @returns {string} MD5 hash
 */
function hashContent(content) {
  return crypto.createHash('md5').update(content.trim()).digest('hex');
}

/**
 * Extract entries from a memory file
 * Memory files use ## headers as entry delimiters
 * @param {string} content - File content
 * @returns {Array<{header: string, content: string, hash: string}>} Parsed entries
 */
function parseMemoryEntries(content) {
  const entries = [];
  const lines = content.split('\n');
  let currentEntry = null;
  let currentContent = [];

  for (const line of lines) {
    // Header pattern: ## Header Name
    if (line.startsWith('## ')) {
      if (currentEntry) {
        currentEntry.content = currentContent.join('\n').trim();
        currentEntry.hash = hashContent(currentEntry.content);
        entries.push(currentEntry);
      }
      currentEntry = { header: line.replace(/^##\s*/, '').trim(), content: '', hash: '' };
      currentContent = [];
    } else if (currentEntry) {
      currentContent.push(line);
    }
  }

  // Don't forget the last entry
  if (currentEntry) {
    currentEntry.content = currentContent.join('\n').trim();
    currentEntry.hash = hashContent(currentEntry.content);
    entries.push(currentEntry);
  }

  return entries;
}

/**
 * Parse vault notes for sections
 * @param {string} content - Note content
 * @returns {Array<{header: string, content: string, hash: string}>} Parsed sections
 */
function parseVaultSections(content) {
  const entries = [];
  const lines = content.split('\n');
  let currentEntry = null;
  let currentContent = [];

  for (const line of lines) {
    // Header pattern: # Header or ## Header
    if (line.startsWith('# ') || line.startsWith('## ')) {
      if (currentEntry) {
        currentEntry.content = currentContent.join('\n').trim();
        currentEntry.hash = hashContent(currentEntry.content);
        entries.push(currentEntry);
      }
      currentEntry = { header: line.replace(/^#+\s*/, '').trim(), content: '', hash: '' };
      currentContent = [];
    } else if (currentEntry) {
      currentContent.push(line);
    }
  }

  if (currentEntry) {
    currentEntry.content = currentContent.join('\n').trim();
    currentEntry.hash = hashContent(currentEntry.content);
    entries.push(currentEntry);
  }

  return entries;
}

/**
 * Check if content already exists in target (by hash substring or similarity)
 * @param {string} content - Content to check
 * @param {string} targetContent - Target file content
 * @returns {boolean} True if likely duplicate
 */
function isDuplicate(content, targetContent) {
  const normalizedContent = content.trim().toLowerCase().replace(/\s+/g, ' ');
  const normalizedTarget = targetContent.trim().toLowerCase().replace(/\s+/g, ' ');
  
  // Check for exact match
  if (normalizedTarget.includes(normalizedContent)) return true;
  
  // Check first 200 chars for similarity (catches partial matches)
  const contentPreview = normalizedContent.slice(0, 200);
  if (contentPreview.length > 50 && normalizedTarget.includes(contentPreview)) return true;
  
  return false;
}

/**
 * Format an entry for vault insertion with attribution
 * @param {Object} entry - Entry from memory file
 * @param {string} sourceFile - Source filename
 * @returns {string} Formatted entry
 */
function formatEntryForVault(entry, sourceFile) {
  const timestamp = new Date().toISOString();
  const attribution = `${CONFIG.attributionPrefix} ${sourceFile} at ${timestamp}*\n>`;
  
  return `## ${entry.header}\n\n${attribution}\n\n${entry.content}`;
}

/**
 * Format vault content for memory with attribution
 * @param {Object} section - Section from vault note
 * @param {string} sourceFile - Source filename
 * @returns {string} Formatted section
 */
function formatSectionForMemory(section, sourceFile) {
  const timestamp = new Date().toISOString();
  const attribution = `<!-- Synced from ${sourceFile} at ${timestamp} -->`;
  
  return `## ${section.header}\n\n${attribution}\n\n${section.content}\n`;
}

/**
 * Merge entries into target file without duplicates
 * @param {string} targetPath - Target file path
 * @param {Array} entries - Entries to merge
 * @param {string} sourceFile - Source file for attribution
 * @returns {Object} Result with status and stats
 */
function mergeIntoFile(targetPath, entries, sourceFile) {
  let targetContent = '';
  if (fs.existsSync(targetPath)) {
    targetContent = fs.readFileSync(targetPath, 'utf8');
  }

  const added = [];
  const skipped = [];

  for (const entry of entries) {
    const formattedEntry = formatEntryForVault(entry, sourceFile);
    
    if (isDuplicate(entry.content, targetContent)) {
      skipped.push(entry.header);
    } else {
      // Append with separator
      if (targetContent && !targetContent.endsWith('\n')) {
        targetContent += '\n';
      }
      if (targetContent) {
        targetContent += CONFIG.separator;
      }
      targetContent += formattedEntry;
      added.push(entry.header);
    }
  }

  if (added.length > 0) {
    fs.writeFileSync(targetPath, targetContent, 'utf8');
  }

  return {
    success: true,
    added: added.length,
    skipped: skipped.length,
    addedHeaders: added,
    skippedHeaders: skipped,
  };
}

/**
 * Get today's date string for daily notes
 * @returns {string} YYYY-MM-DD
 */
function getTodayString() {
  return new Date().toISOString().split('T')[0];
}

/**
 * List files in directory matching pattern
 * @param {string} dir - Directory to scan
 * @param {RegExp} pattern - Filename pattern
 * @returns {Array<{path: string, mtime: Date}>} Matching files with modification times
 */
function listFiles(dir, pattern = /.*/) {
  if (!fs.existsSync(dir)) {
    return [];
  }

  const files = fs.readdirSync(dir)
    .filter(f => pattern.test(f))
    .map(f => {
      const fullPath = path.join(dir, f);
      const stats = fs.statSync(fullPath);
      return { path: fullPath, name: f, mtime: stats.mtime };
    });

  return files;
}

/**
 * Ensure directory exists
 * @param {string} dir - Directory path
 */
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

/**
 * Extract entries from a memory file that are newer than cutoff
 * @param {string} filePath - Path to memory file
 * @param {Date} since - Only return entries after this time
 * @returns {Array} Filtered entries
 */
function extractNewEntries(filePath, since) {
  if (!fs.existsSync(filePath)) {
    return [];
  }

  const content = fs.readFileSync(filePath, 'utf8');
  const entries = parseMemoryEntries(content);
  
  // For now, we parse all entries from the file
  // In the future, we could track entry-level timestamps
  const fileMtime = fs.statSync(filePath).mtime;
  
  if (since && fileMtime <= since) {
    return [];
  }

  return entries;
}

/**
 * Extract sections from vault notes newer than cutoff
 * @param {string} filePath - Path to vault note
 * @param {Date} since - Only return sections after this time
 * @returns {Array} Filtered sections
 */
function extractNewSections(filePath, since) {
  if (!fs.existsSync(filePath)) {
    return [];
  }

  const content = fs.readFileSync(filePath, 'utf8');
  const sections = parseVaultSections(content);
  
  const fileMtime = fs.statSync(filePath).mtime;
  
  if (since && fileMtime <= since) {
    return [];
  }

  return sections;
}

/**
 * Run full sync analysis without writing files
 * @returns {Object} Analysis of what would be synced
 */
function analyzeSync() {
  const memoryFiles = listFiles(CONFIG.memoryDir, /^\d{4}-\d{2}-\d{2}\.md$/);
  const vaultFiles = listFiles(CONFIG.vaultInbox, /\.md$/);
  
  const lastMemoryToVault = tracker.getLastSync('memoryToVault');
  const lastVaultToMemory = tracker.getLastSync('vaultToMemory');
  
  const analysis = {
    memoryToVault: {
      candidates: memoryFiles
        .filter(f => !lastMemoryToVault || f.mtime > lastMemoryToVault)
        .map(f => f.name),
    },
    vaultToMemory: {
      candidates: vaultFiles
        .filter(f => !lastVaultToMemory || f.mtime > lastVaultToMemory)
        .map(f => f.name),
    },
    trackerStats: tracker.getStats(),
  };
  
  return analysis;
}

module.exports = {
  CONFIG,
  hashContent,
  parseMemoryEntries,
  parseVaultSections,
  isDuplicate,
  formatEntryForVault,
  formatSectionForMemory,
  mergeIntoFile,
  getTodayString,
  listFiles,
  ensureDir,
  extractNewEntries,
  extractNewSections,
  analyzeSync,
  tracker,
};
