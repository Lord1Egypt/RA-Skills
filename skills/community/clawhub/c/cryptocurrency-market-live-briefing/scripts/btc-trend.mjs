#!/usr/bin/env node

/**
 * Get BTC Trend Data
 */

const BASE_URL = 'https://mcp.desk3.io/v1/market/btc/trend';

async function getBTCTrend() {
  try {
    const response = await fetch(BASE_URL, {
      headers: { 'language': 'en' }
    });
    const data = await response.json();
    
    if (data.code !== 0 || !data.data) {
      console.error('API returned error');
      return null;
    }
    
    const trends = data.data.slice(-10); // Last 10 entries
    
    console.log('\n📈 BTC Trend Data\n' + '='.repeat(60));
    console.log(`${'Date'.padEnd(10)} ${'Price'.padEnd(14)} ${'MA7'.padEnd(12)} ${'MA30'.padEnd(12)} ${'MA90'}`);
    console.log('-'.repeat(60));
    
    trends.forEach(item => {
      const date = item[0];
      const price = item[1] ? `$${parseFloat(item[1]).toLocaleString()}` : 'N/A';
      const ma7 = item[2] ? `$${parseFloat(item[2]).toLocaleString()}` : 'N/A';
      const ma30 = item[3] ? `$${parseFloat(item[3]).toLocaleString()}` : 'N/A';
      const ma90 = item[4] ? `$${parseFloat(item[4]).toLocaleString()}` : 'N/A';
      
      console.log(`${date.padEnd(10)} ${price.padEnd(14)} ${ma7.padEnd(12)} ${ma30.padEnd(12)} ${ma90}`);
    });
    
    console.log('='.repeat(50));
    return data.data;
  } catch (error) {
    console.error('Failed to fetch BTC trend:', error.message);
    return null;
  }
}

getBTCTrend();
