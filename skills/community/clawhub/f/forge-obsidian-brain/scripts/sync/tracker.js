/**
 * Sync Tracker - Manages last sync timestamps and state
 * Tracks synchronization state between OpenClaw memory and Obsidian vault
 */

const fs = require('fs');
const path = require('path');

const TRACKER_FILE = path.join(__dirname, '.sync-state.json');

/**
 * Default sync state structure
 */
const DEFAULT_STATE = {
  lastSync: {
    memoryToVault: null,    // ISO timestamp of last memory → vault sync
    vaultToMemory: null,    // ISO timestamp of last vault → memory sync
  },
  processedFiles: {
    memory: {},             // Map of memory file paths to last processed timestamps
    vault: {},              // Map of vault file paths to last processed timestamps
  },
  version: '1.0.0',
};

/**
 * Load sync state from disk
 * @returns {Object} Current sync state
 */
function loadState() {
  try {
    if (fs.existsSync(TRACKER_FILE)) {
      const data = fs.readFileSync(TRACKER_FILE, 'utf8');
      const state = JSON.parse(data);
      // Merge with defaults for any new fields
      return { ...DEFAULT_STATE, ...state };
    }
  } catch (err) {
    console.error('Error loading sync state:', err.message);
  }
  return { ...DEFAULT_STATE };
}

/**
 * Save sync state to disk
 * @param {Object} state - State to save
 */
function saveState(state) {
  try {
    fs.writeFileSync(TRACKER_FILE, JSON.stringify(state, null, 2), 'utf8');
  } catch (err) {
    console.error('Error saving sync state:', err.message);
  }
}

/**
 * Get the last sync timestamp for a direction
 * @param {string} direction - 'memoryToVault' or 'vaultToMemory'
 * @returns {Date|null} Last sync date or null
 */
function getLastSync(direction) {
  const state = loadState();
  const ts = state.lastSync[direction];
  return ts ? new Date(ts) : null;
}

/**
 * Update the last sync timestamp for a direction
 * @param {string} direction - 'memoryToVault' or 'vaultToMemory'
 */
function updateLastSync(direction) {
  const state = loadState();
  state.lastSync[direction] = new Date().toISOString();
  saveState(state);
}

/**
 * Check if a file has been processed since a given time
 * @param {string} fileType - 'memory' or 'vault'
 * @param {string} filePath - Path to the file
 * @param {Date} since - Timestamp to check against
 * @returns {boolean} True if file was processed after 'since'
 */
function isFileProcessed(fileType, filePath, since) {
  const state = loadState();
  const processedTime = state.processedFiles[fileType]?.[filePath];
  if (!processedTime || !since) return false;
  return new Date(processedTime) >= since;
}

/**
 * Mark a file as processed
 * @param {string} fileType - 'memory' or 'vault'
 * @param {string} filePath - Path to the file
 */
function markFileProcessed(fileType, filePath) {
  const state = loadState();
  if (!state.processedFiles[fileType]) {
    state.processedFiles[fileType] = {};
  }
  state.processedFiles[fileType][filePath] = new Date().toISOString();
  saveState(state);
}

/**
 * Get all tracked files for a type
 * @param {string} fileType - 'memory' or 'vault'
 * @returns {Object} Map of file paths to timestamps
 */
function getTrackedFiles(fileType) {
  const state = loadState();
  return state.processedFiles[fileType] || {};
}

/**
 * Clear all tracked files for a type (useful for full re-sync)
 * @param {string} fileType - 'memory' or 'vault'
 */
function clearTrackedFiles(fileType) {
  const state = loadState();
  state.processedFiles[fileType] = {};
  saveState(state);
}

/**
 * Reset all sync state (nuclear option)
 */
function resetAll() {
  saveState({ ...DEFAULT_STATE });
}

/**
 * Get sync statistics
 * @returns {Object} Statistics about sync state
 */
function getStats() {
  const state = loadState();
  return {
    lastMemoryToVault: state.lastSync.memoryToVault,
    lastVaultToMemory: state.lastSync.vaultToMemory,
    memoryFilesTracked: Object.keys(state.processedFiles.memory || {}).length,
    vaultFilesTracked: Object.keys(state.processedFiles.vault || {}).length,
  };
}

module.exports = {
  loadState,
  saveState,
  getLastSync,
  updateLastSync,
  isFileProcessed,
  markFileProcessed,
  getTrackedFiles,
  clearTrackedFiles,
  resetAll,
  getStats,
  TRACKER_FILE,
};
