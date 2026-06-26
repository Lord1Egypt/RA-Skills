#!/usr/bin/env node

/**
 * Get Cycle Indicators Detail
 */

const BASE_URL = 'https://mcp.desk3.io/v1/market/cycleIndicators';

async function getCycleIndicators() {
  try {
    const response = await fetch(BASE_URL, {
      headers: { 'language': 'en' }
    });
    const data = await response.json();
    
    if (data.code !== 0 || !data.data) {
      console.error('API returned error');
      return null;
    }
    
    const indicators = data.data.indicators;
    
    console.log('\n📊 Bitcoin Cycle Indicators Detail\n' + '='.repeat(70));
    console.log(`${'Indicator Name'.padEnd(35)} ${'Current'.padEnd(14)} ${'Target'.padEnd(14)} ${'Status'}`);
    console.log('-'.repeat(70));
    
    indicators.forEach(item => {
      const name = item.indicatorName?.substring(0, 20) || '';
      const current = item.currentValue || 'N/A';
      const target = item.targetValue || 'N/A';
      const status = item.hitStatus ? '✅ Triggered' : '❌ Not triggered';
      
      console.log(`${name.padEnd(35)} ${String(current).padEnd(14)} ${String(target).padEnd(14)} ${status}`);
    });
    
    console.log('\n📈 Statistics:');
    console.log(`   Total Indicators: ${data.data.totalHitCount}`);
    console.log(`   Triggered: ${data.data.triggeredCount}`);
    console.log('='.repeat(70));
    
    return indicators;
  } catch (error) {
    console.error('Failed to fetch cycle indicators:', error.message);
    return null;
  }
}

getCycleIndicators();
