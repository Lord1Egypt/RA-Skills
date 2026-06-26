#!/usr/bin/env node

/**
 * Fetch Fear & Greed Index and Global Metrics from CoinMarketCap
 * Cache for 24 hours (daily data, no need to hit API every heartbeat)
 */

require('dotenv').config({ path: require('path').join(__dirname, '../../../.env') });
const https = require('https');
const fs = require('fs');
const path = require('path');

const CMC_API_KEY = process.env.CMC_API_KEY;
const CMC_BASE = 'pro-api.coinmarketcap.com';
const CACHE_FILE = path.join(__dirname, '../../../memory/cmc-cache.json');
const CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

// Helper: fetch JSON with CMC headers
function fetchCMC(url) {
  return new Promise((resolve, reject) => {
    const headers = {
      'X-CMC_PRO_API_KEY': CMC_API_KEY,
      'Accept': 'application/json',
      'User-Agent': 'defi-scout/1.0'
    };
    
    const urlObj = new URL(url);
    const opts = {
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      headers
    };
    
    https.get(opts, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.status.error_code !== 0) {
            reject(new Error(`CMC API error: ${json.status.error_message}`));
          } else {
            resolve(json);
          }
        } catch (e) {
          reject(new Error(`JSON parse error: ${e.message}`));
        }
      });
    }).on('error', reject);
  });
}

// Read from cache
function readCache() {
  try {
    if (!fs.existsSync(CACHE_FILE)) return null;
    
    const raw = fs.readFileSync(CACHE_FILE, 'utf8');
    const cache = JSON.parse(raw);
    
    if (Date.now() - cache.fetchedAt < CACHE_TTL_MS) {
      console.log(`[cmc-sentiment] Cache hit (${Math.round((Date.now() - cache.fetchedAt) / 3600000)}h old)`);
      return cache.data;
    }
  } catch (err) {
    // Cache invalid or doesn't exist
  }
  return null;
}

// Write to cache
function writeCache(data) {
  try {
    const memoryDir = path.join(__dirname, '../../../memory');
    if (!fs.existsSync(memoryDir)) {
      fs.mkdirSync(memoryDir, { recursive: true });
    }
    
    fs.writeFileSync(CACHE_FILE, JSON.stringify({
      fetchedAt: Date.now(),
      data
    }, null, 2));
  } catch (err) {
    console.error('[cmc-sentiment] Cache write error:', err.message);
  }
}

// Get Fear & Greed Index (latest value)
async function getFearAndGreed() {
  try {
    const url = `https://${CMC_BASE}/v3/fear-and-greed/historical?limit=1`;
    const json = await fetchCMC(url);
    
    if (!json.data || !json.data.length) {
      throw new Error('No F&G data returned');
    }
    
    const latest = json.data[0];
    const value = latest.value;
    const timestamp = latest.timestamp;
    
    // Categorize
    let category = 'Neutral';
    if (value >= 80) category = 'Extreme Greed';
    else if (value >= 60) category = 'Greed';
    else if (value >= 40) category = 'Neutral';
    else if (value >= 20) category = 'Fear';
    else category = 'Extreme Fear';
    
    return { value, category, timestamp };
    
  } catch (error) {
    console.error('[cmc-sentiment] F&G fetch failed:', error.message);
    return null;
  }
}

// Get Global Metrics (BTC/ETH dominance)
async function getGlobalMetrics() {
  try {
    const url = `https://${CMC_BASE}/v1/global-metrics/quotes/latest`;
    const json = await fetchCMC(url);
    
    const data = json.data;
    return {
      btcDominance: data.btc_dominance,
      ethDominance: data.eth_dominance,
      totalMarketCap: data.total_market_cap,
      totalVolume24h: data.total_volume_24h,
      activeCryptos: data.active_cryptocurrencies,
      timestamp: data.last_updated
    };
    
  } catch (error) {
    console.error('[cmc-sentiment] Global metrics fetch failed:', error.message);
    return null;
  }
}

// Main function
async function getSentimentData() {
  // Check cache first
  const cached = readCache();
  if (cached) {
    return cached;
  }
  
  // No valid cache, fetch fresh
  console.log('[cmc-sentiment] Cache miss, fetching fresh from CMC');
  
  try {
    const [fng, metrics] = await Promise.all([
      getFearAndGreed(),
      getGlobalMetrics()
    ]);
    
    const result = {
      fng,
      metrics,
      fetchedAt: new Date().toISOString()
    };
    
    // Write to cache
    writeCache(result);
    
    return result;
    
  } catch (error) {
    console.error('[cmc-sentiment] Failed to fetch CMC data:', error.message);
    
    // Return null if both failed
    return null;
  }
}

// CLI mode
if (require.main === module) {
  getSentimentData()
    .then(data => {
      if (!data) {
        console.log('No CMC sentiment data available');
        process.exit(1);
      }
      
      // Format for DeFi brief
      const fng = data.fng;
      const metrics = data.metrics;
      
      if (fng && metrics) {
        console.log(`Sentiment: F&G ${fng.value} (${fng.category}) | BTC dom: ${metrics.btcDominance.toFixed(1)}% | ETH dom: ${metrics.ethDominance.toFixed(1)}%`);
      } else if (fng) {
        console.log(`Sentiment: F&G ${fng.value} (${fng.category}) | BTC/ETH dom: N/A`);
      } else if (metrics) {
        console.log(`Sentiment: F&G N/A | BTC dom: ${metrics.btcDominance.toFixed(1)}% | ETH dom: ${metrics.ethDominance.toFixed(1)}%`);
      } else {
        console.log('Sentiment: No data');
      }
    })
    .catch(error => {
      console.error('Error:', error.message);
      process.exit(1);
    });
}

module.exports = { getSentimentData };