#!/usr/bin/env node

/**
 * Get Exchange Rates
 */

const BASE_URL = 'https://mcp.desk3.io/v1/market/exchangeRate';

async function getExchangeRate() {
  try {
    const response = await fetch(BASE_URL, {
      headers: { 'language': 'en' }
    });
    const data = await response.json();
    
    if (data.code !== 0) {
      console.error('API returned error');
      return null;
    }
    
    console.log('\n💱 Exchange Rates\n' + '='.repeat(50));
    
    // Display major currency pairs
    const majorPairs = {
      'EUR/USD': data.EURUSD,
      'USD/JPY': data.USDJPY,
      'USD/CNY': data.USDCNY,
      'GBP/USD': data.GBPUSD,
      'USD/HKD': data.USDHKD,
      'AUD/USD': data.AUDUSD,
      'USD/SGD': data.USDSGD
    };
    
    for (const [pair, value] of Object.entries(majorPairs)) {
      if (value) console.log(`   ${pair}: ${value}`);
    }
    
    console.log('='.repeat(50));
    return data;
  } catch (error) {
    console.error('Failed to fetch exchange rates:', error.message);
    return null;
  }
}

getExchangeRate();
