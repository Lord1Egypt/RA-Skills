#!/usr/bin/env node

/**
 * Get Pi Cycle Top Indicator
 */

const BASE_URL = 'https://api1.desk3.io/v1/market/pi-cycle-top';

async function getPiCycle() {
  try {
    const response = await fetch(BASE_URL, {
      headers: {
        'language': 'en'
      }
    });
    const data = await response.json();
    
    if (data.code !== 0) {
      console.error('API returned error');
      return null;
    }
    
    console.log('\n🔄 Pi Cycle Top Indicator\n' + '='.repeat(50));
    
    if (data.data) {
      // Try to parse different data formats
      const jsonStr = JSON.stringify(data.data);
      
      // Find key metrics
      if (jsonStr.includes('111DMA') || jsonStr.includes('350DMA')) {
        console.log('Pi Cycle Top uses 111-day MA and 2x350-day MA');
        console.log('When 111DMA crosses above 2x350DMA, may signal Bitcoin top');
      }
      
      // Output raw data for debugging
      console.log('\nData:', jsonStr.substring(0, 500));
    } else {
      console.log('Current data: None');
    }
    
    console.log('\n📖 Interpretation:');
    console.log('  This indicator uses 111-day simple moving average (111DMA)');
    console.log('  and 2x the 350-day moving average (2x350DMA)');
    console.log('  When 111DMA crosses above 2x350DMA, it typically signals Bitcoin cycle top');
    console.log('  Historically accurate - famous Bitcoin top prediction indicator');
    console.log('='.repeat(50));
    
    return data.data;
  } catch (error) {
    console.error('Failed to fetch Pi Cycle indicator:', error.message);
    return null;
  }
}

getPiCycle();
