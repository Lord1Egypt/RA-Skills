#!/usr/bin/env node

/**
 * Get Core Prices - BTC/ETH/SOL prices and percentage changes
 */

const BASE_URL = 'https://api1.desk3.io/v1/market/price';

async function getPrices() {
  try {
    const response = await fetch(`${BASE_URL}?symbol=BTCUSDT,ETHUSDT,SOLUSDT`, {
      headers: {
        'language': 'en'
      }
    });
    const data = await response.json();
    
    // Get 24h change from mini 24hr endpoint
    const miniResponse = await fetch(`${BASE_URL.replace('price', 'mini/24hr')}?symbol=BTCUSDT,ETHUSDT,SOLUSDT`, {
      headers: {
        'language': 'en'
      }
    });
    const miniData = await miniResponse.json();
    
    const prices = {};
    if (data.BTCUSDT) prices.BTC = parseFloat(data.BTCUSDT);
    if (data.ETHUSDT) prices.ETH = parseFloat(data.ETHUSDT);
    if (data.SOLUSDT) prices.SOL = parseFloat(data.SOLUSDT);
    
    const changes = {};
    if (Array.isArray(miniData)) {
      miniData.forEach(item => {
        if (item.symbol === 'BTCUSDT') changes.BTC = item.priceChangePercent;
        if (item.symbol === 'ETHUSDT') changes.ETH = item.priceChangePercent;
        if (item.symbol === 'SOLUSDT') changes.SOL = item.priceChangePercent;
      });
    }
    
    console.log('\n📊 Core Prices\n' + '='.repeat(50));
    console.log(`BTC: $${prices.BTC?.toLocaleString() || 'N/A'} (${changes.BTC ? (changes.BTC >= 0 ? '+' : '') + changes.BTC.toFixed(2) + '%' : 'N/A'})`);
    console.log(`ETH: $${prices.ETH?.toLocaleString() || 'N/A'} (${changes.ETH ? (changes.ETH >= 0 ? '+' : '') + changes.ETH.toFixed(2) + '%' : 'N/A'})`);
    console.log(`SOL: $${prices.SOL?.toLocaleString() || 'N/A'} (${changes.SOL ? (changes.SOL >= 0 ? '+' : '') + changes.SOL.toFixed(2) + '%' : 'N/A'})`);
    console.log('='.repeat(50));
    
    return { prices, changes };
  } catch (error) {
    console.error('Failed to fetch prices:', error.message);
    return null;
  }
}

getPrices();
