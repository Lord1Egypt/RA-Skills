/**
 * Download history management
 * @module utils/history
 */

const fs = require('fs');
const path = require('path');

/**
 * Get history file path
 * @returns {string}
 */
function getHistoryFilePath() {
  const homeDir = process.env.HOME || process.env.USERPROFILE;
  const configDir = path.join(homeDir, '.bilibit');
  
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  
  return path.join(configDir, 'history.json');
}

/**
 * Load history from file
 * @returns {Array}
 */
function loadHistory() {
  const filePath = getHistoryFilePath();
  
  try {
    if (fs.existsSync(filePath)) {
      const data = fs.readFileSync(filePath, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('Failed to load history:', error.message);
  }
  
  return [];
}

/**
 * Save history to file
 * @param {Array} history - History array
 * @returns {boolean}
 */
function saveHistory(history) {
  const filePath = getHistoryFilePath();
  
  try {
    fs.writeFileSync(filePath, JSON.stringify(history, null, 2), 'utf8');
    return true;
  } catch (error) {
    console.error('Failed to save history:', error.message);
    return false;
  }
}

/**
 * Add a download record to history
 * @param {Object} record - Download record
 * @param {string} record.videoId - Video ID (BV/AV)
 * @param {string} record.url - Video URL
 * @param {string} record.title - Video title
 * @param {string} record.author - Video author
 * @param {string} record.downloadPath - Downloaded file path
 * @param {string} record.quality - Video quality
 * @param {boolean} record.danmaku - Whether danmaku was downloaded
 * @returns {boolean}
 */
function addRecord(record) {
  const history = loadHistory();
  
  const newRecord = {
    ...record,
    timestamp: Date.now(),
    date: new Date().toISOString()
  };
  
  // Add to beginning of array
  history.unshift(newRecord);
  
  // Keep only last 100 records
  if (history.length > 100) {
    history.splice(100);
  }
  
  return saveHistory(history);
}

/**
 * Get recent history
 * @param {number} limit - Number of records to return
 * @returns {Array}
 */
function getRecent(limit = 10) {
  const history = loadHistory();
  return history.slice(0, limit);
}

/**
 * Search history by keyword
 * @param {string} keyword - Search keyword
 * @returns {Array}
 */
function searchHistory(keyword) {
  const history = loadHistory();
  const lowerKeyword = keyword.toLowerCase();
  
  return history.filter(record => 
    record.title.toLowerCase().includes(lowerKeyword) ||
    record.author.toLowerCase().includes(lowerKeyword) ||
    record.videoId.toLowerCase().includes(lowerKeyword)
  );
}

/**
 * Clear all history
 * @returns {boolean}
 */
function clearHistory() {
  return saveHistory([]);
}

/**
 * Format history record for display
 * @param {Object} record - History record
 * @returns {string}
 */
function formatRecord(record) {
  const date = new Date(record.timestamp).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
  
  const danmaku = record.danmaku ? '🎬' : '';
  const quality = record.quality ? `[${record.quality}]` : '';
  
  return `${date} ${danmaku} ${quality} ${record.title} - ${record.author}`;
}

/**
 * Print history to console
 * @param {number} limit - Number of records to show
 */
function printHistory(limit = 10) {
  const history = getRecent(limit);
  
  if (history.length === 0) {
    console.log('📭 No download history yet');
    return;
  }
  
  console.log(`\n📊 Download History (Last ${Math.min(limit, history.length)} records):\n`);
  
  history.forEach((record, index) => {
    console.log(`${(index + 1).toString().padStart(2)}. ${formatRecord(record)}`);
  });
  
  console.log('');
}

module.exports = {
  getHistoryFilePath,
  loadHistory,
  saveHistory,
  addRecord,
  getRecent,
  searchHistory,
  clearHistory,
  formatRecord,
  printHistory
};
