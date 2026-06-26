/**
 * CENC - 中国地震台网
 */

const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

let cachedData = [];
let lastUpdate = null;

async function getCENCData() {
  // 1分钟缓存
  if (cachedData.length > 0 && lastUpdate && (Date.now() - lastUpdate) < 60000) {
    return cachedData;
  }
  
  try {
    const { stdout } = await execPromise('curl -s --max-time 10 "https://api.wolfx.jp/cenc_eqlist.json"');
    const json = JSON.parse(stdout);
    
    const data = [];
    for (let i = 1; i <= 50; i++) {
      const key = 'No' + i;
      if (json[key]) data.push(json[key]);
    }
    
    if (data.length > 0) {
      cachedData = data;
      lastUpdate = Date.now();
      return cachedData;
    }
  } catch (e) {
    console.error('[CENC] Error:', e.message);
  }
  
  return cachedData;
}

function getLatestId(data) {
  if (!data || data.length === 0) return '';
  return data[0].EventID || data[0].time || '';
}

module.exports = { getCENCData, getLatestId, getCachedData: getCENCData };
