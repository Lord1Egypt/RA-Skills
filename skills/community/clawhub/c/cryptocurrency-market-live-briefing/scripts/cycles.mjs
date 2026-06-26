#!/usr/bin/env node

/**
 * Get Cycle Data (Puell + Pi Cycle + Cycle Probabilities)
 */

const BASE_URL = 'https://mcp.desk3.io/v1/market/cycles';

async function getCycles() {
  try {
    const response = await fetch(BASE_URL, {
      headers: { 'language': 'en' }
    });
    const data = await response.json();
    
    if (data.code !== 0 || !data.data) {
      console.error('API returned error');
      return null;
    }
    
    console.log('\n🔄 Bitcoin Cycle Composite Analysis\n' + '='.repeat(50));
    
    // Puell Multiple
    const puell = data.data.puellMultiple;
    if (puell) {
      console.log(`\n📈 Puell Multiple: ${puell.toFixed(2)}`);
      console.log(`   Interpretation: ${puell < 0.5 ? 'Severely undervalued - best buying时机' : 
        puell < 1 ? 'Undervalued - miner revenue below annual avg' : 
        puell < 4 ? 'Normal range' : 'Overvalued - possible top'}`);
    }
    
    // Pi Cycle Top
    const piCycle = data.data.piCycleTop;
    if (piCycle) {
      console.log(`\n🔄 Pi Cycle Top Indicator`);
      console.log(`   111-day MA: $${parseFloat(piCycle.ma110).toLocaleString()}`);
      console.log(`   2x350-day MA: $${parseFloat(piCycle.ma350mu2).toLocaleString()}`);
      console.log(`   Status: ${parseFloat(piCycle.ma110) > parseFloat(piCycle.ma350mu2) ? '❌ Crossed - possible top' : '✅ Not crossed - safe'}`);
    }
    
    // Cycle Probability
    const likelihood = data.data.likelihood;
    if (likelihood) {
      console.log(`\n🎯 Cycle Probability Analysis`);
      console.log(`   Hold Signal: ${likelihood.holdCount}/${likelihood.totalCount}`);
      console.log(`   Sell Signal: ${likelihood.sellCount}/${likelihood.totalCount}`);
      console.log(`   Recommendation: ${likelihood.holdCount > likelihood.sellCount ? 'Hold' : 'Consider selling'}`);
    }
    
    console.log('='.repeat(50));
    return data.data;
  } catch (error) {
    console.error('Failed to fetch cycle data:', error.message);
    return null;
  }
}

getCycles();
