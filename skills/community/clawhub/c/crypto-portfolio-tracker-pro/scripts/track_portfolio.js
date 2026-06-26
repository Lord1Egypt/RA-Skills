#!/usr/bin/env node

/**
 * Crypto Portfolio Tracker
 * Fetches real-time portfolio data from multiple sources
 */

const https = require('https');

// Free CoinGecko API - no key required
const COINGECKO_API = 'https://api.coingecko.com/api/v3';

// Sample portfolio (users should customize)
const PORTFOLIO = {
  BTC: 0.5,
  ETH: 2.0,
  SOL: 50,
  USDT: 1000
};

function fetchPrice(coinId) {
  return new Promise((resolve, reject) => {
    const url = `${COINGECKO_API}/simple/price?ids=${coinId}&vs_currencies=usd&include_24hr_change=true`;
    
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function trackPortfolio() {
  console.log('🔍 Fetching portfolio data...\n');
  
  const coinMap = {
    BTC: 'bitcoin',
    ETH: 'ethereum',
    SOL: 'solana',
    USDT: 'tether'
  };
  
  let totalValue = 0;
  let total24hChange = 0;
  
  console.log('Symbol | Amount | Price | Value | 24h Change');
  console.log('-------|--------|-------|-------|------------');
  
  for (const [symbol, amount] of Object.entries(PORTFOLIO)) {
    const coinId = coinMap[symbol];
    try {
      const data = await fetchPrice(coinId);
      if (!data[coinId]) {
        console.log(`${symbol.padEnd(6)} | ${amount.toString().padEnd(6)} | ERROR: Data not available`);
        continue;
      }
      const price = data[coinId].usd;
      const change24h = data[coinId].usd_24h_change || 0;
      const value = amount * price;
      
      totalValue += value;
      total24hChange += value * (change24h / 100);
      
      console.log(`${symbol.padEnd(6)} | ${amount.toString().padEnd(6)} | $${price.toFixed(2).padEnd(8)} | $${value.toFixed(2).padEnd(10)} | ${change24h > 0 ? '+' : ''}${change24h.toFixed(2)}%`);
    } catch (e) {
      console.log(`${symbol.padEnd(6)} | ${amount.toString().padEnd(6)} | ERROR: ${e.message}`);
    }
  }
  
  const changePercent = (total24hChange / totalValue) * 100;
  
  console.log('\n' + '='.repeat(60));
  console.log(`💰 Total Portfolio Value: $${totalValue.toFixed(2)}`);
  console.log(`📊 24h Change: ${total24hChange > 0 ? '+' : ''}$${total24hChange.toFixed(2)} (${changePercent > 0 ? '+' : ''}${changePercent.toFixed(2)}%)`);
  console.log('='.repeat(60));
}

trackPortfolio().catch(console.error);
