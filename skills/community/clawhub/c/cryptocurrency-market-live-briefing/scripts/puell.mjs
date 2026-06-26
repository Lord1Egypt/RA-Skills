#!/usr/bin/env node

/**
 * Get Puell Multiple Indicator
 */

const BASE_URL = 'https://api1.desk3.io/v1/market/puell-multiple';

async function getPuell() {
  try {
    const response = await fetch(BASE_URL, {
      headers: {
        'language': 'en'
      }
    });
    const data = await response.json();
    
    if (data.code !== 0 || !data.data?.points) {
      console.error('API returned error');
      return null;
    }
    
    const points = data.data.points;
    const current = points[points.length - 1];
    const prev = points[points.length - 7]; // One week ago
    
    console.log('\n📈 Puell Multiple (Miner Revenue Indicator)\n' + '='.repeat(50));
    console.log(`Current: ${current?.puellMultiple?.toFixed(2) || 'N/A'}`);
    console.log(`Last Week: ${prev?.puellMultiple?.toFixed(2) || 'N/A'}`);
    console.log(`BTC Price: $${current?.btcUsdPrice?.toLocaleString() || 'N/A'}`);
    
    console.log('\n📖 Interpretation:');
    console.log('  <0.5: Severely undervalued - historically best buying opportunity');
    console.log('  0.5-1: Undervalued - miner revenue below annual average');
    console.log('  1-4: Normal - market in balanced state');
    console.log('  >4: Overvalued - miner revenue far above annual average, possible top');
    console.log('='.repeat(50));
    
    return current;
  } catch (error) {
    console.error('Failed to fetch Puell indicator:', error.message);
    return null;
  }
}

getPuell();
