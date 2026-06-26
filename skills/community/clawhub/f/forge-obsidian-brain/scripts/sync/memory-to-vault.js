#!/usr/bin/env node
/**
 * Memory to Vault Sync - OpenClaw → Obsidian
 * Syncs daily memory entries to Obsidian vault notes
 */

const fs = require('fs');
const path = require('path');

const engine = require('./engine');
const tracker = require('./tracker');

/**
 * Sync a single memory file to the vault
 * @param {string} memoryPath - Path to memory file
 * @param {Date} since - Only sync entries newer than this
 * @returns {Object} Sync result
 */
async function syncMemoryFile(memoryPath, since) {
  const filename = path.basename(memoryPath);
  console.log(`📄 Processing: ${filename}`);

  // Skip if already processed
  if (tracker.isFileProcessed('memory', memoryPath, since)) {
    console.log(`   ⏭️  Skipped (already processed)`);
    return { skipped: true, reason: 'already_processed' };
  }

  // Extract entries
  const entries = engine.extractNewEntries(memoryPath, since);
  
  if (entries.length === 0) {
    console.log(`   ⏭️  No new entries`);
    tracker.markFileProcessed('memory', memoryPath);
    return { skipped: true, reason: 'no_new_entries', entries: 0 };
  }

  console.log(`   📝 Found ${entries.length} entries`);

  // Determine target vault note
  // Daily notes go to vaultDaily, others to vaultInbox
  const isDailyNote = /^\d{4}-\d{2}-\d{2}\.md$/.test(filename);
  const dateMatch = filename.match(/^(\d{4})-(\d{2})-(\d{2})/);
  
  let targetDir, targetFile;
  if (isDailyNote && dateMatch) {
    targetDir = engine.CONFIG.vaultDaily;
    targetFile = path.join(targetDir, `${dateMatch[1]}-${dateMatch[2]}-${dateMatch[3]}-memory.md`);
  } else {
    targetDir = engine.CONFIG.vaultInbox;
    targetFile = path.join(targetDir, `oc-${filename}`);
  }

  // Ensure directory exists
  engine.ensureDir(targetDir);

  // Merge entries into vault note
  const result = engine.mergeIntoFile(targetFile, entries, filename);
  
  if (result.added > 0) {
    console.log(`   ✅ Added ${result.added} entries to ${path.basename(targetFile)}`);
    if (result.skipped > 0) {
      console.log(`   ⏭️  Skipped ${result.skipped} duplicates`);
    }
  } else if (result.skipped > 0) {
    console.log(`   ⏭️  All ${result.skipped} entries already exist`);
  }

  // Mark as processed
  tracker.markFileProcessed('memory', memoryPath);

  return {
    success: true,
    source: filename,
    target: path.basename(targetFile),
    ...result,
  };
}

/**
 * Sync all memory files to vault
 * @param {Object} options - Sync options
 * @returns {Object} Overall sync results
 */
async function syncAll(options = {}) {
  const results = {
    direction: 'memory-to-vault',
    started: new Date().toISOString(),
    filesProcessed: 0,
    entriesAdded: 0,
    entriesSkipped: 0,
    errors: [],
    details: [],
  };

  console.log('🔄 Memory → Vault Sync Started');
  console.log('=' .repeat(50));

  // Get last sync time
  const since = options.force ? null : tracker.getLastSync('memoryToVault');
  
  if (since) {
    console.log(`📅 Last sync: ${since.toISOString()}`);
  } else {
    console.log(`📅 No previous sync found (full sync)`);
  }

  // Ensure directories exist
  engine.ensureDir(engine.CONFIG.vaultDaily);
  engine.ensureDir(engine.CONFIG.vaultInbox);

  // Find memory files
  const memoryFiles = engine.listFiles(engine.CONFIG.memoryDir, /^\d{4}-\d{2}-\d{2}\.md$/);
  
  console.log(`\n🔍 Found ${memoryFiles.length} memory files`);

  // Process each file
  for (const file of memoryFiles) {
    try {
      const result = await syncMemoryFile(file.path, since);
      results.filesProcessed++;
      results.details.push(result);
      
      if (result.added) {
        results.entriesAdded += result.added;
      }
      if (result.skipped) {
        results.entriesSkipped += result.skipped;
      }
    } catch (err) {
      console.error(`   ❌ Error: ${err.message}`);
      results.errors.push({ file: file.name, error: err.message });
    }
  }

  // Update last sync timestamp
  tracker.updateLastSync('memoryToVault');

  results.finished = new Date().toISOString();
  
  console.log('\n' + '='.repeat(50));
  console.log('✅ Sync Complete');
  console.log(`   Files processed: ${results.filesProcessed}`);
  console.log(`   Entries added: ${results.entriesAdded}`);
  console.log(`   Entries skipped: ${results.entriesSkipped}`);
  
  if (results.errors.length > 0) {
    console.log(`   ⚠️  Errors: ${results.errors.length}`);
  }

  return results;
}

/**
 * Sync a specific memory file by date
 * @param {string} dateStr - Date string YYYY-MM-DD
 * @returns {Object} Sync result
 */
async function syncByDate(dateStr) {
  const memoryPath = path.join(engine.CONFIG.memoryDir, `${dateStr}.md`);
  
  if (!fs.existsSync(memoryPath)) {
    return { error: `Memory file not found: ${memoryPath}` };
  }

  return await syncMemoryFile(memoryPath, null);
}

/**
 * Run sync from command line
 */
async function main() {
  const args = process.argv.slice(2);
  const options = {
    force: args.includes('--force') || args.includes('-f'),
    date: null,
  };

  // Handle --date flag
  const dateIndex = args.findIndex(a => a === '--date' || a === '-d');
  if (dateIndex !== -1 && args[dateIndex + 1]) {
    options.date = args[dateIndex + 1];
  }

  try {
    let result;
    if (options.date) {
      result = await syncByDate(options.date);
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
  syncByDate,
  syncMemoryFile,
};
