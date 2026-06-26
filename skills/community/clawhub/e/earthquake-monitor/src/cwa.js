/**
 * CWA - 台湾中央气象署地震预警
 */

const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

let cachedWarning = null;
let lastUpdate = null;

async function getCWAData() {
  // 30秒缓存
  if (cachedWarning && lastUpdate && (Date.now() - lastUpdate) < 30000) {
    return cachedWarning;
  }
  
  try {
    const { stdout } = await execPromise('curl -s --max-time 10 "https://api.wolfx.jp/cwa_eew.json"');
    // 检查是否返回 HTML（被 Cloudflare 拦截）
    if (!stdout || stdout.trim().startsWith('<')) {
      console.log('[CWA] API temporarily unavailable');
      return cachedWarning;
    }
    const data = JSON.parse(stdout);
    
    if (data && data.ID) {
      cachedWarning = data;
      lastUpdate = Date.now();
      return cachedWarning;
    }
  } catch (e) {
    console.log('[CWA] Error:', e.message);
  }
  
  return cachedWarning;
}

function getLatestId(data) {
  if (!data || !data.ID) return '';
  return String(data.ID);
}

module.exports = { getCWAData, getLatestId, getCachedData: getCWAData };
