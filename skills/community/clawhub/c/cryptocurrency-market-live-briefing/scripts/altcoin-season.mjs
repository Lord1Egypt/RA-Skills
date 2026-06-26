#!/usr/bin/env node

/**
 * Get Altcoin Season Index
 */

const BASE_URL = 'https://mcp.desk3.io/v1/market/altcoin/season';

async function getAltcoinSeason() {
  try {
    const response = await fetch(BASE_URL, {
      headers: { 'language': 'en' }
    });
    const data = await response.json();
    
    if (data.code !== 0 || !data.data) {
      console.error('API returned error');
      return null;
    }
    
    const now = data.data.historicalValues?.now;
    const yesterday = data.data.historicalValues?.yesterday;
    const yearlyHigh = data.data.historicalValues?.yearlyHigh;
    const yearlyLow = data.data.historicalValues?.yearlyLow;
    
    console.log('\n🪙 Altcoin Season Index\n' + '='.repeat(50));
    console.log(`Current Index: ${now?.altcoinIndex || 'N/A'}`);
    console.log(`   Status: ${parseInt(now?.altcoinIndex || 0) >= 75 ? 'Altcoin Season' : 
      parseInt(now?.altcoinIndex || 0) <= 25 ? 'Bitcoin Season' : 'Neutral'}`);
    
    console.log('\nHistorical Comparison:');
    console.log(`   Yesterday: ${yesterday?.altcoinIndex || 'N/A'}`);
    console.log(`   Yearly High: ${yearlyHigh?.altcoinIndex || 'N/A'} (${yearlyHigh?.name || ''})`);
    console.log(`   Yearly Low: ${yearlyLow?.altcoinIndex || 'N/A'} (${yearlyLow?.name || ''})`);
    
    console.log('\n📖 Interpretation:');
    console.log('   0-25: Bitcoin Season - capital concentrated in Bitcoin');
    console.log('   26-74: Neutral market');
    console.log('   75-100: Altcoin Season - altcoins outperforming BTC');
    
    // Show Top Gainers
    const topCryptos = data.data.topCryptos?.slice(0, 10);
    if (topCryptos?.length > 0) {
      console.log('\n🔥 Top 10 Gainers:');
      topCryptos.forEach((coin, i) => {
        console.log(`   ${i + 1}. ${coin.symbol}: ${coin.percentChange?.toFixed(2)}%`);
      });
    }
    
    console.log('='.repeat(50));
    return now;
  } catch (error) {
    console.error('Failed to fetch altcoin season:', error.message);
    return null;
  }
}

getAltcoinSeason();
