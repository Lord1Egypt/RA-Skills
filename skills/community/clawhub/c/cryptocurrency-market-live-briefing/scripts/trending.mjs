#!/usr/bin/env node

/**
 * Get Trending Coins Real-time Prices
 */

const BASE_URL = 'https://api1.desk3.io/v1/market/mini/24hr';

async function getTrending() {
  try {
    const response = await fetch(BASE_URL, {
      headers: {
        'language': 'en'
      }
    });
    const data = await response.json();
    
    if (!Array.isArray(data)) {
      console.error('API returned error:', data);
      return null;
    }
    
    // Sort by volume (q) to get trending coins
    const sorted = data
      .filter(item => item.q > 0)
      .sort((a, b) => b.q - a.q)
      .slice(0, 10);
    
    console.log('\n🔥 Trending - Top 10 Coins\n' + '='.repeat(60));
    console.log(`${'Rank'.padEnd(4)} ${'Coin'.padEnd(12)} ${'Price'.padEnd(16)} ${'24h Change'.padEnd(10)} ${'Volume(USDT)'}`);
    console.log('-'.repeat(60));
    
    sorted.forEach((item, index) => {
      const symbol = item.s.replace('USDT', '');
      const price = parseFloat(item.c).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });
      const change = parseFloat(item.P);
      const changeStr = (change >= 0 ? '+' : '') + change.toFixed(2) + '%';
      const volume = (item.q / 1e9).toFixed(2) + 'B';
      
      console.log(
        `${(index + 1).toString().padEnd(4)} ${symbol.padEnd(12)} $${price.padEnd(15)} ${changeStr.padEnd(10)} $${volume}`
      );
    });
    
    console.log('='.repeat(60));
    
    return sorted;
  } catch (error) {
    console.error('Failed to fetch trending:', error.message);
    return null;
  }
}

getTrending();
