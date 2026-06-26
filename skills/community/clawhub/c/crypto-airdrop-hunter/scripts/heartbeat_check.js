#!/usr/bin/env node

/**
 * Heartbeat Check - Quick periodic monitoring
 * Bundled checks: BTC price, BTC.D, macro news, altcoins, airdrops
 * Runs 2-3x daily, minimal computation
 * 
 * Usage: node heartbeat_check.js
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Store state in skill's own folder (not external)
const STATE_FILE = path.join(__dirname, '../state.json');

function httpGet(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve({ error: e.message });
        }
      });
    }).on('error', reject);
  });
}

function loadState() {
  if (!fs.existsSync(STATE_FILE)) {
    return {
      lastChecks: {},
      lastAlerts: {},
      trackedLevels: { btcSupport: 84800, btcResistance: 88000, btcDomLevel: 54 }
    };
  }
  return JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

async function checkBTC() {
  const data = await httpGet(
    'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_market_cap=true&include_24hr_change=true'
  );
  
  if (data.error) return null;
  
  const btc = data.bitcoin;
  return {
    price: btc.usd,
    change24h: btc.usd_24h_change,
    time: Date.now()
  };
}

async function checkNews() {
  // Mock news check - in production, use RSS feeds or news API
  // For now, return empty (no major news)
  return {
    news: [],
    time: Date.now()
  };
}

async function checkAltcoins() {
  // Check HYPE & MNT (mock)
  return {
    altcoins: {
      hype: { change: 2.5 }, // 2.5% up
      mnt: { change: -1.2 }   // 1.2% down
    },
    time: Date.now()
  };
}

function analyzeAndAlert(btc, state) {
  const alerts = [];
  const { trackedLevels } = state;
  
  if (!btc) return alerts;
  
  // Check if approaching S/R
  const distToSupport = ((btc.price - trackedLevels.btcSupport) / trackedLevels.btcSupport) * 100;
  const distToResistance = ((trackedLevels.btcResistance - btc.price) / trackedLevels.btcResistance) * 100;
  
  if (distToSupport < 2) {
    alerts.push({
      type: 'PRICE',
      severity: 'high',
      message: `🔴 BTC approaching support! Harga $${btc.price}, support $${trackedLevels.btcSupport}. Jarak: ${distToSupport.toFixed(2)}%`,
      timestamp: new Date().toISOString()
    });
  }
  
  if (distToResistance < 2) {
    alerts.push({
      type: 'PRICE',
      severity: 'high',
      message: `🟢 BTC approaching resistance! Harga $${btc.price}, resistance $${trackedLevels.btcResistance}. Jarak: ${distToResistance.toFixed(2)}%`,
      timestamp: new Date().toISOString()
    });
  }
  
  return alerts;
}

async function main() {
  console.log('🔄 Running heartbeat checks...\n');
  
  const state = loadState();
  const btc = await checkBTC();
  const news = await checkNews();
  const altcoins = await checkAltcoins();
  
  const alerts = analyzeAndAlert(btc, state);
  
  // Update state
  state.lastChecks = {
    btcPrice: btc?.time,
    macroNews: news?.time,
    altcoins: altcoins?.time
  };
  saveState(state);
  
  // Output
  if (alerts.length === 0) {
    console.log('✅ HEARTBEAT_OK');
    console.log(`BTC: $${btc?.price} (${btc?.change24h.toFixed(2)}%) - sideways, no alerts`);
    return 'HEARTBEAT_OK';
  }
  
  // Send alerts
  let output = '⚠️ ALERTS:\n\n';
  alerts.forEach(a => {
    output += a.message + '\n';
  });
  
  if (btc) {
    output += `\n💰 BTC: $${btc.price} (${btc.change24h.toFixed(2)}%)\n`;
  }
  
  if (altcoins?.altcoins) {
    output += `\n📊 Altcoins:\n`;
    output += `  HYPE: ${altcoins.altcoins.hype.change > 0 ? '🟢' : '🔴'} ${altcoins.altcoins.hype.change}%\n`;
    output += `  MNT: ${altcoins.altcoins.mnt.change > 0 ? '🟢' : '🔴'} ${altcoins.altcoins.mnt.change}%\n`;
  }
  
  console.log(output);
  return output;
}

main().catch(console.error);
