#!/usr/bin/env node

/**
 * Get Fear & Greed Index
 */

const BASE_URL = 'https://mcp.desk3.io/v1/market/fear-greed';

async function getFearGreed() {
  try {
    const response = await fetch(BASE_URL, {
      headers: {
        'language': 'en'
      }
    });
    const data = await response.json();
    
    if (data.code !== 0 || !data.data) {
      console.error('API returned error');
      return null;
    }
    
    // mcp.desk3.io path: data.data.historicalValues
    const historical = data.data?.historicalValues;
    const now = historical?.now;
    
    console.log('\n😱 Fear & Greed Index\n' + '='.repeat(50));
    console.log(`Current: ${now?.score || 'N/A'} (${now?.name || 'N/A'})`);
    console.log('\nHistorical Comparison:');
    console.log(`  Yesterday: ${historical?.yesterday?.score || 'N/A'} (${historical?.yesterday?.name || 'N/A'})`);
    console.log(`  Last Week: ${historical?.lastWeek?.score || 'N/A'} (${historical?.lastWeek?.name || 'N/A'})`);
    console.log(`  Last Month: ${historical?.lastMonth?.score || 'N/A'} (${historical?.lastMonth?.name || 'N/A'})`);
    console.log(`  Yearly High: ${historical?.yearlyHigh?.score || 'N/A'} (${historical?.yearlyHigh?.name || 'N/A'})`);
    console.log(`  Yearly Low: ${historical?.yearlyLow?.score || 'N/A'} (${historical?.yearlyLow?.name || 'N/A'})`);
    
    console.log('\n📖 Interpretation:');
    console.log('  0-25: Extreme Fear - potential buying opportunity');
    console.log('  25-50: Fear - market sentiment low');
    console.log('  50-75: Greed - market sentiment optimistic');
    console.log('  75-100: Extreme Greed - potential risk');
    console.log('='.repeat(50));
    
    return now;
  } catch (error) {
    console.error('Failed to fetch Fear & Greed Index:', error.message);
    return null;
  }
}

getFearGreed();
