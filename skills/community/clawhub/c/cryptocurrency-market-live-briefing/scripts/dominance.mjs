#!/usr/bin/env node

/**
 * Get Bitcoin Dominance
 */

const BASE_URL = 'https://api1.desk3.io/v1/market/bitcoin/dominance';

async function getDominance() {
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
    
    const btcDominance = current?.dominance?.[0];
    const ethDominance = current?.dominance?.[1];
    const othersDominance = current?.dominance?.[2];
    
    console.log('\n📊 Cryptocurrency Dominance\n' + '='.repeat(50));
    console.log(`Bitcoin (BTC): ${btcDominance?.toFixed(2) || 'N/A'}%`);
    console.log(`Ethereum (ETH): ${ethDominance?.toFixed(2) || 'N/A'}%`);
    console.log(`Others: ${othersDominance?.toFixed(2) || 'N/A'}%`);
    
    console.log('\n📖 Interpretation:');
    console.log('  BTC dominance rising: Capital flowing to BTC, market in defense mode');
    console.log('  BTC dominance falling: Capital spreading to altcoins, altcoin season may arrive');
    console.log('  When BTC dominance drops below 40%, typically signals altcoin bull market');
    console.log('='.repeat(50));
    
    return current;
  } catch (error) {
    console.error('Failed to fetch dominance:', error.message);
    return null;
  }
}

getDominance();
