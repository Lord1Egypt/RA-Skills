#!/usr/bin/env node

/**
 * Desk3 Crypto Market Real-time Briefing
 * Includes:
 * 1. Core Prices - BTC/ETH/SOL prices and percentage changes
 * 2. Sentiment Indicators - Fear & Greed Index + explanation
 * 3. Technical Indicators - Puell, Pi Cycle, Dominance + explanations
 * 4. Geopolitical News - Top 10
 * 5. Blockchain Industry News - Top 10
 * 6. Trending - Top 10 coins real-time prices
 */

const API_BASE = 'https://api1.desk3.io/v1';

async function fetchJSON(url) {
  const res = await fetch(url, { headers: { 'language': 'en' } });
  return res.json();
}

async function getPrices() {
  try {
    const data = await fetchJSON(`${API_BASE}/market/mini/24hr?symbol=BTCUSDT,ETHUSDT,SOLUSDT`);
    if (!Array.isArray(data)) return null;
    
    const result = {};
    data.forEach(item => {
      if (item.s === 'BTCUSDT') result.BTC = { price: parseFloat(item.c), change: parseFloat(item.P) };
      if (item.s === 'ETHUSDT') result.ETH = { price: parseFloat(item.c), change: parseFloat(item.P) };
      if (item.s === 'SOLUSDT') result.SOL = { price: parseFloat(item.c), change: parseFloat(item.P) };
    });
    return result;
  } catch (e) {
    return null;
  }
}

async function getFearGreed() {
  try {
    const data = await fetchJSON(`${API_BASE}/market/fear-greed`);
    if (data.code !== 0) return null;
    // Fix: correct path is data.data.data.historicalValues.now
    return data.data?.data?.historicalValues?.now;
  } catch (e) {
    return null;
  }
}

async function getPuell() {
  try {
    const data = await fetchJSON(`${API_BASE}/market/puell-multiple`);
    if (data.code !== 0 || !data.data?.points) return null;
    const points = data.data.points;
    return { current: points[points.length - 1], prev: points[points.length - 7] };
  } catch (e) {
    return null;
  }
}

async function getDominance() {
  try {
    const data = await fetchJSON(`${API_BASE}/market/bitcoin/dominance`);
    if (data.code !== 0 || !data.data?.points) return null;
    const points = data.data.points;
    const current = points[points.length - 1];
    return {
      btc: current?.dominance?.[0],
      eth: current?.dominance?.[1],
      others: current?.dominance?.[2]
    };
  } catch (e) {
    return null;
  }
}

// News categories: 1=blockchain, 2=headlines, 3=policy, 4=flash (price moves)
// Use catid=3 for policy/macro news
async function getNews(catid, count = 10) {
  try {
    const data = await fetchJSON(`${API_BASE}/news/list?catid=${catid}&page=1&rows=${count}`);
    if (data.code !== 0) return [];
    return data.data?.list || [];
  } catch (e) {
    return [];
  }
}

async function getTrending() {
  try {
    const data = await fetchJSON(`${API_BASE}/market/mini/24hr`);
    if (!Array.isArray(data)) return [];
    return data
      .filter(item => item.q > 0)
      .sort((a, b) => b.q - a.q)
      .slice(0, 10);
  } catch (e) {
    return [];
  }
}

function formatPrice(num) {
  return '$' + num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatChange(num) {
  return (num >= 0 ? '+' : '') + num.toFixed(2) + '%';
}

async function main() {
  console.log('\n' + '🌍'.padEnd(54) + 'Desk3 Crypto Briefing'.padEnd(18) + '📊\n');
  console.log('Generated:', new Date().toLocaleString('en-US', { 
    year: 'numeric', month: 'long', day: 'numeric', 
    hour: '2-digit', minute: '2-digit', timeZone: 'Asia/Shanghai' 
  }));
  console.log('='.repeat(60));
  
  // 1. Core Prices
  console.log('\n📈 1. Core Prices\n' + '-'.repeat(40));
  const prices = await getPrices();
  if (prices) {
    console.log(`   BTC: ${formatPrice(prices.BTC?.price || 0)}  ${formatChange(prices.BTC?.change || 0)}`);
    console.log(`   ETH: ${formatPrice(prices.ETH?.price || 0)}  ${formatChange(prices.ETH?.change || 0)}`);
    console.log(`   SOL: ${formatPrice(prices.SOL?.price || 0)}  ${formatChange(prices.SOL?.change || 0)}`);
  } else {
    console.log('   Failed to fetch');
  }
  
  // 2. Sentiment Indicators
  console.log('\n😱 2. Sentiment - Fear & Greed Index\n' + '-'.repeat(40));
  const fearGreed = await getFearGreed();
  if (fearGreed) {
    console.log(`   Current: ${fearGreed.score} (${fearGreed.name})`);
    console.log(`   Interpretation: ${fearGreed.score < 25 ? 'Extreme Fear - potential buying opportunity' : 
      fearGreed.score < 50 ? 'Fear - market sentiment low' : 
      fearGreed.score < 75 ? 'Greed - market sentiment optimistic' : 'Extreme Greed - potential risk'}`);
  } else {
    console.log('   Failed to fetch');
  }
  
  // 3. Technical Indicators
  console.log('\n📊 3. Technical Indicators\n' + '-'.repeat(40));
  
  const puell = await getPuell();
  if (puell?.current) {
    console.log(`   Puell Multiple: ${puell.current.puellMultiple?.toFixed(2)}`);
    console.log(`   Interpretation: ${puell.current.puellMultiple < 0.5 ? 'Severely undervalued, historically best buying时机' : 
      puell.current.puellMultiple < 1 ? 'Undervalued, miner revenue below annual average' : 
      puell.current.puellMultiple < 4 ? 'Normal range' : 'Overvalued, possible top'}`);
  }
  
  const dominance = await getDominance();
  if (dominance) {
    console.log(`   BTC Dominance: ${dominance.btc?.toFixed(2)}%`);
    console.log(`   ETH Dominance: ${dominance.eth?.toFixed(2)}%`);
    console.log(`   Interpretation: ${dominance.btc > 60 ? 'Capital concentrated in BTC, market in defense mode' : 
      dominance.btc < 40 ? 'Altcoin season may arrive' : 'Market relatively balanced'}`);
  }
  
  console.log(`   Pi Cycle: Uses 111DMA & 2x350DMA crossover to predict cycle top`);

  // 5. Blockchain Industry News (catid=1)
  console.log('\n⛓️ 4. Blockchain Industry News - Top 10\n' + '-'.repeat(40));
  const cryptoNews = await getNews(1, 10);
  if (cryptoNews.length > 0) {
    cryptoNews.forEach((item, i) => {
      const time = new Date(item.published_at).toLocaleString('en-US', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' });
      console.log(`   ${i + 1}. ${item.title?.substring(0, 40)}...`);
      console.log(`      ${time}`);
    });
  } else {
    console.log('   No news available');
  }
  
  // 6. Trending
  console.log('\n🔥 5. Trending - Top 10 Coins\n' + '-'.repeat(40));
  console.log(`   ${'Rank'.padEnd(4)} ${'Coin'.padEnd(10)} ${'Price'.padEnd(14)} ${'24h Change'}`);
  console.log(`   ${'-'.repeat(40)}`);
  const trending = await getTrending();
  if (trending.length > 0) {
    trending.forEach((item, i) => {
      const symbol = item.s.replace('USDT', '');
      const price = parseFloat(item.c);
      const change = parseFloat(item.P);
      console.log(`   ${(i + 1).toString().padEnd(4)} ${symbol.padEnd(10)} ${formatPrice(price).padEnd(14)} ${formatChange(change)}`);
    });
  } else {
    console.log('   Failed to fetch');
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('📌 Data Source: Desk3 API | Credit: Desk3');
  console.log('');
}

main().catch(console.error);
