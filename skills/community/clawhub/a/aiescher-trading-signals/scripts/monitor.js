#!/usr/bin/env node
const { fetchWithIndicators } = require('./lib/tradingview');
const { analyzeData } = require('./lib/indicators');
const { sendEmail, formatSignalsEmail } = require('./lib/email');
const fs = require('fs');

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
];

function loadConfig() {
  const configPath = process.argv.find(arg => arg.startsWith('--config='))?.split('=')[1];
  if (configPath && fs.existsSync(configPath)) {
    return JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }
  
  const defaultConfigPath = __dirname + '/../references/assets.json';
  if (fs.existsSync(defaultConfigPath)) {
    return JSON.parse(fs.readFileSync(defaultConfigPath, 'utf8'));
  }
  
  return { assets: DEFAULT_ASSETS, alerts: { email: null, minStrength: 'medium', interval: 15 } };
}

async function checkSignals(assets, config) {
  const results = [];
  const strongSignals = [];
  
  for (const asset of assets) {
    try {
      const rawData = await fetchWithIndicators(asset.symbol, asset.timeframe || '60');
      const data = analyzeData(rawData, config.alerts);
      results.push(data);
      
      // Collect strong signals for alerts
      const minStrength = config.alerts?.minStrength || 'medium';
      const strengthOrder = { strong: 3, medium: 2, weak: 1 };
      
      data.signals.forEach(signal => {
        if (strengthOrder[signal.strength] >= strengthOrder[minStrength]) {
          strongSignals.push({ ...signal, asset: data.name, symbol: data.symbol });
        }
      });
      
    } catch (e) {
      console.error(`Fehler bei ${asset.name}:`, e.message);
    }
  }
  
  return { results, strongSignals };
}

async function main() {
  const config = loadConfig();
  const assets = config.assets || DEFAULT_ASSETS;
  const interval = config.alerts?.interval || 15;
  
  console.log(`🔍 Trading Signal Monitor gestartet`);
  console.log(`⏱️  Intervall: ${interval} Minuten`);
  console.log(`📧 E-Mail Alerts: ${config.alerts?.email || 'Deaktiviert'}`);
  console.log(`🎯 Min. Stärke: ${config.alerts?.minStrength || 'medium'}`);
  console.log('Drücke Ctrl+C zum Beenden\n');
  
  // Initial run
  console.log('Erste Analyse läuft...');
  let lastResults = await checkSignals(assets, config);
  
  if (lastResults.strongSignals.length > 0) {
    console.log('\n🚨 Starke Signale gefunden:');
    lastResults.strongSignals.forEach(s => {
      const emoji = s.type === 'BUY' ? '🟢' : '🔴';
      console.log(`  ${emoji} ${s.asset}: ${s.reason} (${s.strength})`);
    });
  }
  
  // Schedule next runs
  setInterval(async () => {
    console.log(`\n[${new Date().toLocaleTimeString('de-DE')}] Neue Analyse...`);
    
    const { results, strongSignals } = await checkSignals(assets, config);
    
    // Only notify if new strong signals appear
    const newSignals = strongSignals.filter(s => {
      return !lastResults.strongSignals.some(ls => 
        ls.asset === s.asset && ls.reason === s.reason && ls.type === s.type
      );
    });
    
    if (newSignals.length > 0) {
      console.log('\n🚨 NEUE SIGNALE:');
      newSignals.forEach(s => {
        const emoji = s.type === 'BUY' ? '🟢' : '🔴';
        console.log(`  ${emoji} ${s.asset}: ${s.reason} (${s.strength})`);
      });
      
      // Send email for new strong signals
      if (config.alerts?.email) {
        try {
          const html = formatSignalsEmail(results, '🔔 Neue Trading Signale');
          await sendEmail(config.alerts.email, `🚨 Neue Trading Signale - ${new Date().toLocaleDateString('de-DE')}`, html);
          console.log('📧 E-Mail Alert gesendet');
        } catch (e) {
          console.error('❌ E-Mail Fehler:', e.message);
        }
      }
    } else {
      console.log('✅ Keine neuen starken Signale');
    }
    
    lastResults = { results, strongSignals };
  }, interval * 60 * 1000);
}

main().catch(err => {
  console.error('Fehler:', err.message);
  process.exit(1);
});
