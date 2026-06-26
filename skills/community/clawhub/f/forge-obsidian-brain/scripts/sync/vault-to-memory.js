#!/usr/bin/env node
/**
 * Vault to Memory Sync - Obsidian → OpenClaw
 * Syncs vault research notes to OpenClaw memory
 */

const fs = require('fs');
const path = require('path');

const engine = require('./engine');
const tracker = require('./tracker');

/**
 * Extract research content from vault notes
 * Filters out system notes and extracts meaningful content
 * @param {string} content - Note content
 * @returns {string|null} Extracted research content or null
 */
function extractResearchContent(content) {
  // Skip if it's a template or system file
  if (content.includes('template:') || content.includes('<%')) {
    return null;
  }

  // Remove frontmatter
  content = content.replace(/^---\n[\s\S]*?\n---\n/, '');

  // Skip if empty after removing frontmatter
  if (!content.trim()) {
    return null;
  }

  // Skip sync attribution blocks (avoid circular sync)
  content = content.replace(/> 📥 \*Synced from.*?\n/g, '');
  content = content.replace(/<!-- Synced from.*? -->\n?/g, '');

  return content.trim() || null;
}

/**
 * Determine memory file path based on vault note
 * @param {string} vaultPath - Path to vault note
 * @returns {string} Target memory file path
 */
function getMemoryFilePath(vaultPath) {
  const filename = path.basename(vaultPath, '.md');
  const today = engine.getTodayString();
  
  // Check if vault note has a date pattern
  const dateMatch = filename.match(/(\d{4})-(\d{2})-(\d{2})/);
  if (dateMatch) {
    const noteDate = `${dateMatch[1]}-${dateMatch[2]}-${dateMatch[3]}`;
    // If it's a historical note, use that date
    // Otherwise use today's date for new research
    return path.join(engine.CONFIG.memoryDir, `${noteDate}.md`);
  }

  // Default to today's memory file
  return path.join(engine.CONFIG.memoryDir, `${today}.md`);
}

/**
 * Merge vault content into memory file
 * @param {string} memoryPath - Target memory file
 * @param {string} vaultContent - Content from vault
 * @param {string} sourceFile - Source vault filename
 * @returns {Object} Merge result
 */
function mergeIntoMemory(memoryPath, vaultContent, sourceFile) {
  let memoryContent = '';
  if (fs.existsSync(memoryPath)) {
    memoryContent = fs.readFileSync(memoryPath, 'utf8');
  }

  // Check for duplicates
  if (engine.isDuplicate(vaultContent, memoryContent)) {
    return { added: false, reason: 'duplicate' };
  }

  // Find existing ## sections to determine order
  const existingSections = engine.parseMemoryEntries(memoryContent);
  
  // Determine section header from source file
  const sectionHeader = `Vault Research: ${path.basename(sourceFile, '.md')}`;
  
  // Format the content
  const timestamp = new Date().toISOString();
  const formattedContent = `## ${sectionHeader}

<!-- Synced from ${sourceFile} at ${timestamp} -->

${vaultContent}
`;

  // Append to memory file
  if (memoryContent && !memoryContent.endsWith('\n')) {
    memoryContent += '\n';
  }
  if (memoryContent) {
    memoryContent += engine.CONFIG.separator;
  } else {
    // New file - add header
    memoryContent = `# ${path.basename(memoryPath, '.md')}\n\n`;
  }
  memoryContent += formattedContent;

  fs.writeFileSync(memoryPath, memoryContent, 'utf8');

  return { added: true, section: sectionHeader };
}

/**
 * Sync a single vault note to memory
 * @param {string} vaultPath - Path to vault note
 * @param {Date} since - Only sync if modified after this
 * @returns {Object} Sync result
 */
async function syncVaultNote(vaultPath, since) {
  const filename = path.basename(vaultPath);
  console.log(`📄 Processing: ${filename}`);

  // Skip if already processed
  if (tracker.isFileProcessed('vault', vaultPath, since)) {
    console.log(`   ⏭️  Skipped (already processed)`);
    return { skipped: true, reason: 'already_processed' };
  }

  // Check file modification time
  const stats = fs.statSync(vaultPath);
  if (since && stats.mtime <= since) {
    console.log(`   ⏭️  Skipped (not modified since last sync)`);
    tracker.markFileProcessed('vault', vaultPath);
    return { skipped: true, reason: 'not_modified' };
  }

  // Read and process content
  const rawContent = fs.readFileSync(vaultPath, 'utf8');
  const researchContent = extractResearchContent(rawContent);

  if (!researchContent) {
    console.log(`   ⏭️  Skipped (no research content)`);
    tracker.markFileProcessed('vault', vaultPath);
    return { skipped: true, reason: 'no_content' };
  }

  console.log(`   📝 Extracted ${researchContent.length} chars of research content`);

  // Determine target memory file
  const memoryPath = getMemoryFilePath(vaultPath);
  
  // Ensure memory directory exists
  engine.ensureDir(engine.CONFIG.memoryDir);

  // Merge into memory
  const result = mergeIntoMemory(memoryPath, researchContent, filename);

  if (result.added) {
    console.log(`   ✅ Added to ${path.basename(memoryPath)} as "${result.section}"`);
  } else {
    console.log(`   ⏭️  Already exists in memory`);
  }

  // Mark as processed
  tracker.markFileProcessed('vault', vaultPath);

  return {
    success: true,
    source: filename,
    target: path.basename(memoryPath),
    ...result,
  };
}

// Files to exclude from sync (patterns)
const EXCLUDED_PATTERNS = [
  /-memory\.md$/,           // Memory sync output files
  /^oc-/,                   // OpenClaw prefixed files (already from memory)
];

/**
 * Check if a file should be excluded from sync
 * @param {string} filename - Filename to check
 * @returns {boolean} True if should be excluded
 */
function shouldExclude(filename) {
  return EXCLUDED_PATTERNS.some(pattern => pattern.test(filename));
}

/**
 * Sync all vault notes to memory
 * @param {Object} options - Sync options
 * @returns {Object} Overall sync results
 */
async function syncAll(options = {}) {
  const results = {
    direction: 'vault-to-memory',
    started: new Date().toISOString(),
    filesProcessed: 0,
    notesSynced: 0,
    notesSkipped: 0,
    errors: [],
    details: [],
  };

  console.log('🔄 Vault → Memory Sync Started');
  console.log('='.repeat(50));

  // Get last sync time
  const since = options.force ? null : tracker.getLastSync('vaultToMemory');
  
  if (since) {
    console.log(`📅 Last sync: ${since.toISOString()}`);
  } else {
    console.log(`📅 No previous sync found (full sync)`);
  }

  // Ensure memory directory exists
  engine.ensureDir(engine.CONFIG.memoryDir);

  // Find vault notes in multiple locations
  const noteLocations = [
    engine.CONFIG.vaultInbox,
    engine.CONFIG.vaultDaily,
    path.join(process.env.HOME, 'obsidian-vault/OpenClaw/Ideas'),
  ];

  const vaultFiles = [];
  for (const location of noteLocations) {
    if (fs.existsSync(location)) {
      const files = engine.listFiles(location, /\.md$/);
      vaultFiles.push(...files);
    }
  }

  // Filter out excluded files
  const filteredFiles = vaultFiles.filter(f => !shouldExclude(f.name));
  const excludedCount = vaultFiles.length - filteredFiles.length;

  // Remove duplicates (same filename from different dirs - prefer most recent)
  const uniqueFiles = new Map();
  for (const file of filteredFiles) {
    if (!uniqueFiles.has(file.name) || uniqueFiles.get(file.name).mtime < file.mtime) {
      uniqueFiles.set(file.name, file);
    }
  }
  const dedupedFiles = Array.from(uniqueFiles.values());

  console.log(`\n🔍 Found ${dedupedFiles.length} vault notes${excludedCount > 0 ? ` (${excludedCount} excluded)` : ''}`);

  // Process each file
  for (const file of dedupedFiles) {
    try {
      const result = await syncVaultNote(file.path, since);
      results.filesProcessed++;
      results.details.push(result);

      if (result.success && result.added) {
        results.notesSynced++;
      } else {
        results.notesSkipped++;
      }
    } catch (err) {
      console.error(`   ❌ Error: ${err.message}`);
      results.errors.push({ file: file.name, error: err.message });
    }
  }

  // Update last sync timestamp
  tracker.updateLastSync('vaultToMemory');

  results.finished = new Date().toISOString();

  console.log('\n' + '='.repeat(50));
  console.log('✅ Sync Complete');
  console.log(`   Files processed: ${results.filesProcessed}`);
  console.log(`   Notes synced: ${results.notesSynced}`);
  console.log(`   Notes skipped: ${results.notesSkipped}`);

  if (results.errors.length > 0) {
    console.log(`   ⚠️  Errors: ${results.errors.length}`);
  }

  return results;
}

/**
 * Sync a specific vault note
 * @param {string} notePath - Path to vault note (can be relative to vault)
 * @returns {Object} Sync result
 */
async function syncNote(notePath) {
  // Resolve full path if relative
  let fullPath = notePath;
  if (!path.isAbsolute(notePath)) {
    fullPath = path.join(engine.CONFIG.vaultInbox, notePath);
    if (!fs.existsSync(fullPath)) {
      fullPath = path.join(process.env.HOME, 'obsidian-vault/OpenClaw', notePath);
    }
  }

  if (!fs.existsSync(fullPath)) {
    return { error: `Vault note not found: ${notePath}` };
  }

  return await syncVaultNote(fullPath, null);
}

/**
 * Run sync from command line
 */
async function main() {
  const args = process.argv.slice(2);
  const options = {
    force: args.includes('--force') || args.includes('-f'),
    note: null,
  };

  // Handle --note flag
  const noteIndex = args.findIndex(a => a === '--note' || a === '-n');
  if (noteIndex !== -1 && args[noteIndex + 1]) {
    options.note = args[noteIndex + 1];
  }

  try {
    let result;
    if (options.note) {
      result = await syncNote(options.note);
    } else {
      result = await syncAll(options);
    }

    // Output JSON if requested
    if (args.includes('--json')) {
      console.log('\n---JSON---');
      console.log(JSON.stringify(result, null, 2));
    }

    process.exit(0);
  } catch (err) {
    console.error('Sync failed:', err.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = {
  syncAll,
  syncNote,
  syncVaultNote,
  extractResearchContent,
  mergeIntoMemory,
};
