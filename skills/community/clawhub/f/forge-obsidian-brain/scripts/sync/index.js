/**
 * Sync Module - Main entry point for synchronization
 */

const { analyzeSync, CONFIG, tracker } = require('./engine');
const fs = require('fs');
const path = require('path');

/**
 * Run bidirectional sync
 * @param {Object} options
 * @param {string} options.vaultPath - Path to vault
 * @returns {Object} Sync result
 */
function runSync(options = {}) {
  try {
    const results = {
      success: true,
      memoryToVault: [],
      vaultToMemory: [],
      errors: [],
    };

    // Ensure directories exist
    if (!fs.existsSync(CONFIG.memoryDir)) {
      fs.mkdirSync(CONFIG.memoryDir, { recursive: true });
    }
    if (!fs.existsSync(CONFIG.vaultInbox)) {
      fs.mkdirSync(CONFIG.vaultInbox, { recursive: true });
    }

    // Get memory files
    const memoryFiles = fs.readdirSync(CONFIG.memoryDir)
      .filter(f => /^\d{4}-\d{2}-\d{2}\.md$/.test(f))
      .map(f => ({
        name: f,
        path: path.join(CONFIG.memoryDir, f),
        mtime: fs.statSync(path.join(CONFIG.memoryDir, f)).mtime,
      }));

    const lastSync = tracker.getLastSync('memoryToVault');

    // Sync memory files to vault inbox
    for (const file of memoryFiles) {
      if (!lastSync || file.mtime > lastSync) {
        try {
          const content = fs.readFileSync(file.path, 'utf8');
          const destPath = path.join(CONFIG.vaultInbox, file.name);

          fs.copyFileSync(file.path, destPath);

          results.memoryToVault.push({
            file: file.name,
            dest: destPath,
            status: 'copied',
          });
        } catch (err) {
          results.errors.push({ file: file.name, error: err.message });
        }
      }
    }

    // Update last sync time
    tracker.updateLastSync('memoryToVault');

    // Get vault inbox files that don't exist in memory
    if (fs.existsSync(CONFIG.vaultInbox)) {
      const vaultInboxFiles = fs.readdirSync(CONFIG.vaultInbox)
        .filter(f => f.endsWith('.md'))
        .map(f => ({
          name: f,
          path: path.join(CONFIG.vaultInbox, f),
          mtime: fs.statSync(path.join(CONFIG.vaultInbox, f)).mtime,
        }));

      const lastVaultSync = tracker.getLastSync('vaultToMemory');

      for (const file of vaultInboxFiles) {
        const memoryPath = path.join(CONFIG.memoryDir, file.name);
        if (!fs.existsSync(memoryPath) && (!lastVaultSync || file.mtime > lastVaultSync)) {
          try {
            fs.copyFileSync(file.path, memoryPath);
            results.vaultToMemory.push({
              file: file.name,
              dest: memoryPath,
              status: 'copied',
            });
          } catch (err) {
            results.errors.push({ file: file.name, error: err.message });
          }
        }
      }

      tracker.updateLastSync('vaultToMemory');
    }

    return results;
  } catch (err) {
    return {
      success: false,
      error: err.message,
      errors: [err.message],
    };
  }
}

module.exports = {
  runSync,
  analyzeSync,
  tracker,
  CONFIG,
};
