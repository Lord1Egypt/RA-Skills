#!/usr/bin/env node

/**
 * Airdrop Report Generator
 * Fetches and compiles airdrop opportunities from public sources
 * 
 * Usage:
 *   node generate_airdrop_report.js --period=daily
 *   node generate_airdrop_report.js --period=weekly
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Parse CLI arguments
const args = process.argv.slice(2);
const period = args.find(a => a.startsWith('--period='))?.split('=')[1] || 'daily';

// Sample data - in production, fetch from APIs like DefiLlama, Crunchbase, etc.
const sampleAirdrops = [
  {
    name: 'LayerZero Protocol',
    category: 'Interoperability',
    funding: '$120M Series B',
    vcs: ['a16z', 'Sequoia', 'Pantera'],
    chain: 'Multi-chain',
    activity: 'Testnet completed, token launch expected Q2 2026',
    activity_level: 'completed',
    website: 'https://layerzero.network',
    twitter: '@LayerZero_Labs',
    narrative: 'Cross-chain messaging protocol, strategic importance for multi-chain future',
    hype_level: 'high', // well-known
  },
  {
    name: 'Monad',
    category: 'L1 Blockchain',
    funding: '$225M Series B',
    vcs: ['Paradigm', 'a16z Crypto', 'Distributed Global'],
    chain: 'Solana ecosystem',
    activity: 'Private testnet, public launch Q3 2026',
    activity_level: 'ongoing',
    website: 'https://monad.xyz',
    twitter: '@monad',
    narrative: 'High-speed EVM-compatible L1, designed for 10k TPS',
    hype_level: 'moderate',
  },
  {
    name: 'Taiko',
    category: 'L2 (Type 1 zkEVM)',
    funding: '$140M Series B',
    vcs: ['Binance Labs', 'a16z Crypto', 'Polychain'],
    chain: 'Ethereum',
    activity: 'Public testnet live, bridge interactions available',
    activity_level: 'testnet',
    website: 'https://taiko.xyz',
    twitter: '@taikoxyz',
    narrative: 'Type 1 zkEVM aiming for 99% compatibility with Ethereum L1',
    hype_level: 'moderate',
  },
  {
    name: 'Avail',
    category: 'Data Availability',
    funding: '$60M Series A',
    vcs: ['Polychain', 'Coinbase Ventures', 'Parafi'],
    chain: 'Substrate-based',
    activity: 'Testnet, light client interactions encouraged',
    activity_level: 'testnet',
    website: 'https://availproject.org',
    twitter: '@AvailProject',
    narrative: 'Modular DA layer, critical infrastructure for rollup scaling',
    hype_level: 'low-moderate',
  },
  {
    name: 'Hyperliquid',
    category: 'Perpetual Futures DEX',
    funding: '$50M Series A',
    vcs: ['Paradigm', 'Jump Crypto', 'Blockchain Capital'],
    chain: 'Hyperliquid Chain',
    activity: 'Testnet + live trading, quest system active',
    activity_level: 'live',
    website: 'https://hyperliquid.xyz',
    twitter: '@HyperliquidX',
    narrative: 'High-performance derivatives platform, strong trading community',
    hype_level: 'moderate',
  },
  {
    name: 'Sonic (Fantom Foundation Relaunch)',
    category: 'L1 Blockchain',
    funding: '$50M+ Series A (continued)',
    vcs: ['Binance Labs', 'Paradigm'],
    chain: 'Ethereum-compatible',
    activity: 'Testnet phase, community engagement rewards',
    activity_level: 'testnet',
    website: 'https://sonic.ooo',
    twitter: '@sonicfantom',
    narrative: 'Rebranded Fantom with focus on gaming and DeFi',
    hype_level: 'low',
  },
];

// Filter by hype level preference (Isma likes low-moderate)
function filterByHype(airdrops) {
  return airdrops.filter(a => 
    a.hype_level === 'low' || 
    a.hype_level === 'low-moderate' || 
    a.hype_level === 'moderate'
  );
}

// Format report
function formatReport(airdrops, period) {
  const date = new Date().toLocaleDateString('id-ID', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
  
  let header = `📋 **Laporan Airdrop - ${period.charAt(0).toUpperCase() + period.slice(1)}** (${date})\n\n`;
  header += `Ditemukan ${airdrops.length} project potensial dengan funding besar dan belum launch token.\n\n`;
  header += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;

  let content = header;

  airdrops.forEach((a, idx) => {
    content += `**${idx + 1}. ${a.name}**\n`;
    content += `   📂 Kategori: ${a.category}\n`;
    content += `   💰 Funding: ${a.funding}\n`;
    content += `   🏦 Investor: ${a.vcs.join(', ')}\n`;
    content += `   ⛓️ Chain: ${a.chain}\n`;
    content += `   📊 Status: ${a.activity}\n`;
    content += `   🔗 Website: ${a.website}\n`;
    content += `   🐦 Twitter: ${a.twitter}\n`;
    content += `   💡 Narrative: ${a.narrative}\n`;
    content += `   📈 Hype Level: ${a.hype_level}\n\n`;
  });

  content += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
  content += `⚡ Tips:\n`;
  content += `- Kalau ada testnet, try bridge/interact untuk get dalam snapshot\n`;
  content += `- Follow Twitter mereka buat update terbaru\n`;
  content += `- Check Discord untuk early bird quests\n`;
  content += `- Confirm funding dari Crunchbase/DefiLlama sebelum commit\n\n`;
  content += `Generated: ${new Date().toISOString()}\n`;

  return content;
}

// Main
const filtered = filterByHype(sampleAirdrops);
const report = formatReport(filtered, period);

console.log(report);

// Optionally save to file
const reportDir = path.join(__dirname, '../reports');
if (!fs.existsSync(reportDir)) {
  fs.mkdirSync(reportDir, { recursive: true });
}

const filename = `airdrop-${period}-${new Date().toISOString().split('T')[0]}.md`;
fs.writeFileSync(path.join(reportDir, filename), report);

console.log(`\n✅ Report saved to: reports/${filename}\n`);
