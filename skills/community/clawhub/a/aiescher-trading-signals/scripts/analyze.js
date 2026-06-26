#!/usr/bin/env node
const { fetchWithIndicators } = require('./lib/tradingview');
const { analyzeData } = require('./lib/indicators');
const { sendEmail, formatSignalsEmail } = require('./lib/email');
const fs = require('fs');
const path = require('path');

// Default assets
const DEFAULT_ASSETS = [
  { symbol: 'XETR:DAX', name: 'DAX', category: 'Index', timeframe: '60' },
  { symbol: 'DJ:DJI', name: 'Dow Jones', category: 'Index', timeframe: '60' },
  { symbol: 'NASDAQ:IXIC', name: 'NASDAQ 100', category: 'Index', timeframe: '60' },
  { symbol: 'SP:SPX', name: 'S&P 500', category: 'Index', timeframe: '60' },
  { symbol: 'BINANCE:BTCUSDT', name: 'Bitcoin', category: 'Crypto', timeframe: '60' },
  { symbol: 'BINANCE:ETHUSDT', name: 'Ethereum', category: 'Crypto', timeframe: '60' },
  { symbol: 'COMEX:GC1!', name: 'Gold', category: 'Commodity', timeframe: '240' },
  { symbol: 'NYMEX:CL1!', name: 'Öl (WTI)', category: 'Commodity', timeframe: '240' },
  { symbol: 'TVC:PLATINUM', name: 'Platin', category: 'Commodity', timeframe: '240' },
  { symbol: 'NYMEX:PA1!', name: 'Palladium', category: 'Commodity', timeframe: '240' },
  { symbol: 'FX:EURUSD', name: 'EUR/USD', category: 'Forex', timeframe: '60' },
];

const STATE_FILE = path.join(__dirname, '..', '.signal-state.json');

function loadConfig() {
  const configPath = process.argv.find(arg => arg.startsWith('--config='))?.split('=')[1];
  if (configPath && fs.existsSync(configPath)) {
    return JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }
  
  const defaultConfigPath = __dirname + '/../references/assets.json';
  if (fs.existsSync(defaultConfigPath)) {
    return JSON.parse(fs.readFileSync(defaultConfigPath, 'utf8'));
  }
  
  return { assets: DEFAULT_ASSETS, alerts: { email: null, minStrength: 'weak' } };
}

function loadPreviousSignals() {
  try {
    if (fs.existsSync(STATE_FILE)) {
      return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
    }
  } catch (e) {
    console.error('Fehler beim Laden des Signal-Status:', e.message);
  }
  return { signals: [], timestamp: null };
}

function saveCurrentSignals(signals) {
  try {
    fs.writeFileSync(STATE_FILE, JSON.stringify({
      signals: signals.map(s => ({ asset: s.asset, type: s.type, reason: s.reason, strength: s.strength })),
      timestamp: new Date().toISOString()
    }, null, 2));
  } catch (e) {
    console.error('Fehler beim Speichern des Signal-Status:', e.message);
  }
}

function findNewSignals(currentSignals, previousSignals) {
  const previousKeys = new Set(previousSignals.map(s => `${s.asset}|${s.type}|${s.reason}`));
  
  return currentSignals.filter(s => {
    const key = `${s.asset}|${s.type}|${s.reason}`;
    return !previousKeys.has(key);
  });
}

function filterByMinStrength(signals, minStrength) {
  const strengthOrder = { strong: 3, medium: 2, weak: 1 };
  const minLevel = strengthOrder[minStrength] || 1;
  
  return signals.filter(s => strengthOrder[s.strength] >= minLevel);
}

async function analyzeAssets(assets, config = {}) {
  console.log('\n╔════════════════════════════════════════════════════════════╗');
  console.log('║           📈 TRADING SIGNALE                              ║');
  console.log('║           ' + new Date().toLocaleString('de-DE').padEnd(47) + '║');
  console.log('╚════════════════════════════════════════════════════════════╝\n');
  
  const results = [];
  
  for (const asset of assets) {
    try {
      console.log(`Analysiere ${asset.name}...`);
      const rawData = await fetchWithIndicators(asset.symbol, asset.timeframe || '60');
      const data = analyzeData(rawData, config);
      results.push(data);
      
      // Display results
      console.log(`\n${asset.name} (${asset.symbol})`);
      console.log(`  Preis: ${data.price?.toFixed(2) || 'n/a'} (${data.change?.toFixed(2) || 0}%)`);
      console.log(`  RSI: ${data.rsi?.toFixed(1) || 'n/a'} | SMA20: ${data.sma20?.toFixed(2) || 'n/a'} | SMA50: ${data.sma50?.toFixed(2) || 'n/a'}`);
      
      if (data.signals.length > 0) {
        console.log('  🚨 SIGNALE:');
        data.signals.forEach(s => {
          const emoji = s.type === 'BUY' ? '🟢' : '🔴';
          console.log(`    ${emoji} ${s.type} - ${s.reason} (${s.strength})`);
        });
      } else {
        console.log('  ✅ Keine klaren Signale');
      }
      
    } catch (e) {
      console.log(`\n${asset.name} (${asset.symbol})`);
      console.log(`  ❌ Fehler: ${e.message}`);
    }
  }
  
  return results;
}

async function main() {
  const config = loadConfig();
  const assets = config.assets || DEFAULT_ASSETS;
  const minStrength = config.alerts?.minStrength || 'weak';
  
  // Parse command line arguments
  const symbolArg = process.argv.find(arg => arg.startsWith('--symbol='));
  const nameArg = process.argv.find(arg => arg.startsWith('--name='));
  const alwaysSend = process.argv.includes('--always-send');
  
  if (symbolArg) {
    const symbol = symbolArg.split('=')[1];
    const name = nameArg ? nameArg.split('=')[1] : symbol;
    assets.length = 0;
    assets.push({ symbol, name, category: 'Custom', timeframe: '60' });
  }
  
  const results = await analyzeAssets(assets, config.alerts);
  
  console.log('\n══════════════════════════════════════════════════════════════');
  console.log('Analyse abgeschlossen');
  console.log('══════════════════════════════════════════════════════════════\n');
  
  // Collect all current signals
  const allCurrentSignals = results.flatMap(r => 
    r.signals.map(s => ({ ...s, asset: r.name, symbol: r.symbol }))
  );
  
  // Filter by minimum strength
  const strongSignals = filterByMinStrength(allCurrentSignals, minStrength);
  
  if (allCurrentSignals.length > 0) {
    console.log('📊 SIGNAL-ÜBERSICHT:');
    const buySignals = allCurrentSignals.filter(s => s.type === 'BUY');
    const sellSignals = allCurrentSignals.filter(s => s.type === 'SELL');
    
    if (buySignals.length > 0) {
      console.log('\n🟢 KAUF-SIGNALE:');
      buySignals.forEach(s => console.log(`  • ${s.asset}: ${s.reason} (${s.strength})`));
    }
    
    if (sellSignals.length > 0) {
      console.log('\n🔴 VERKAUF-SIGNALE:');
      sellSignals.forEach(s => console.log(`  • ${s.asset}: ${s.reason} (${s.strength})`));
    }
  } else {
    console.log('📊 Keine Signale in diesem Zeitraum');
  }
  
  // Load previous signals
  const previousState = loadPreviousSignals();
  
  // Find new signals (not seen before)
  const newSignals = findNewSignals(strongSignals, previousState.signals);
  
  console.log(`\n📊 Starke Signale (${minStrength}+): ${strongSignals.length}`);
  console.log(`📊 Neue Signale: ${newSignals.length}`);
  
  // Save current signals for next run
  saveCurrentSignals(strongSignals);
  
  // Send email only if there are new strong signals or --always-send flag
  if (config.alerts?.email) {
    if (newSignals.length > 0 || alwaysSend) {
      try {
        const subject = newSignals.length > 0 
          ? `🚨 Neue Trading Signale - ${new Date().toLocaleDateString('de-DE')}`
          : `📈 Trading Signale - ${new Date().toLocaleDateString('de-DE')}`;
        
        const html = formatSignalsEmail(results, newSignals.length > 0 ? '🚨 Neue Trading Signale' : '📈 Trading Signale');
        await sendEmail(config.alerts.email, subject, html);
        
        if (newSignals.length > 0) {
          console.log('\n📧 E-Mail mit neuen Signalen gesendet an', config.alerts.email);
          newSignals.forEach(s => {
            const emoji = s.type === 'BUY' ? '🟢' : '🔴';
            console.log(`   ${emoji} ${s.asset}: ${s.reason}`);
          });
        } else {
          console.log('\n📧 E-Mail gesendet an', config.alerts.email);
        }
      } catch (e) {
        console.error('\n❌ E-Mail Fehler:', e.message);
      }
    } else {
      console.log('\n📧 Keine neuen Signale - E-Mail nicht gesendet');
    }
  }
}

main().catch(err => {
  console.error('Fehler:', err.message);
  process.exit(1);
});
