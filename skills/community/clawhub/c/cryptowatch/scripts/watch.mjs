#!/usr/bin/env node
/**
 * ₿ CryptoWatch - 实时价格监控
 * 数据源：CoinGecko API (免费，无需 Key)
 */

import fetch from 'node-fetch';

const API = 'https://api.coingecko.com/api/v3';

// 配置
const DEFAULT_COINS = ['bitcoin', 'ethereum', 'solana', 'bnb', 'xrp', 'dogecoin', 'cardano', 'avalanche-2'];
const VS_CURRENCIES = ['usd', 'cny', 'eur'];

// 参数解析
const args = process.argv.slice(2);
const params = {
  coins: [],
  vs: 'usd',
  include_24h: true,
  include_market_cap: true,
  include_volume: true,
  help: false
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--help' || args[i] === '-h') params.help = true;
  else if (args[i] === '--vs') params.vs = args[++i];
  else if (args[i] === '--top') params.top = parseInt(args[++i]);
  else if (!args[i].startsWith('--')) {
    params.coins = args[i].split(',').map(c => c.trim().toLowerCase());
  }
}

function showHelp() {
  console.log(`
₿ CryptoWatch - 加密货币价格监控

用法:
  node scripts/watch.mjs [币种] [选项]

示例:
  node scripts/watch.mjs btc              # 查询 Bitcoin
  node scripts/watch.mjs btc,eth,sol      # 查询多个币种
  node scripts/watch.mjs --top 20         # 查看前 20 名
  node scripts/watch.mjs --vs cny         # 使用人民币计价

选项:
  --vs <currency>     计价货币 (usd/cny/eur), 默认：usd
  --top <n>           查看市值前 N 名
  --help, -h          显示帮助
`);
}

// 币种 ID 映射
const COIN_MAP = {
  btc: 'bitcoin',
  eth: 'ethereum',
  sol: 'solana',
  bnb: 'bnb',
  xrp: 'xrp',
  doge: 'dogecoin',
  dogecoin: 'dogecoin',
  ada: 'cardano',
  cardano: 'cardano',
  avax: 'avalanche-2',
  link: 'chainlink',
  dot: 'polkadot',
  matic: 'matic-network',
  ltc: 'litecoin',
  uni: 'uniswap',
  atom: 'cosmos',
  xlm: 'stellar',
  etc: 'ethereum-classic',
  near: 'near',
  algo: 'algorand',
  fil: 'filecoin',
  icp: 'internet-computer',
  vet: 'vechain',
  hbar: 'hedera-hashgraph',
  apt: 'aptos',
  arb: 'arbitrum',
  op: 'optimism',
  sui: 'sui'
};

function resolveCoin(input) {
  const lower = input.toLowerCase();
  return COIN_MAP[lower] || lower;
}

// 获取价格数据
async function fetchPrices(coinIds, vsCurrency) {
  const ids = coinIds.join(',');
  const url = `${API}/simple/price?ids=${ids}&vs_currencies=${vsCurrency}&include_24hr_vol=true&include_24hr_change=true&include_market_cap=true`;
  
  const response = await fetch(url, {
    headers: { 'Accept': 'application/json' }
  });
  
  if (!response.ok) {
    throw new Error(`API 错误：${response.status}`);
  }
  
  return await response.json();
}

// 获取市场排行
async function fetchMarketRank(vsCurrency, limit = 20) {
  const url = `${API}/coins/markets?vs_currency=${vsCurrency}&order=market_cap_desc&per_page=${limit}&page=1&sparkline=false`;
  
  const response = await fetch(url, {
    headers: { 'Accept': 'application/json' }
  });
  
  if (!response.ok) {
    throw new Error(`API 错误：${response.status}`);
  }
  
  return await response.json();
}

// 格式化价格
function formatPrice(price, currency) {
  if (price === undefined || price === null) return '-';
  
  const symbols = { usd: '$', cny: '¥', eur: '€', jpy: '¥' };
  const symbol = symbols[currency] || '$';
  
  if (price >= 1000) {
    return `${symbol}${price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  } else if (price >= 1) {
    return `${symbol}${price.toFixed(2)}`;
  } else if (price >= 0.01) {
    return `${symbol}${price.toFixed(4)}`;
  } else {
    return `${symbol}${price.toFixed(6)}`;
  }
}

// 格式化涨跌幅
function formatChange(change) {
  if (change === undefined || change === null) return '-';
  const sign = change >= 0 ? '+' : '';
  const color = change >= 0 ? '🟢' : '🔴';
  return `${color} ${sign}${change.toFixed(2)}%`;
}

// 格式化市值
function formatMarketCap(cap, currency) {
  if (cap === undefined || cap === null) return '-';
  
  if (cap >= 1e12) return `$${(cap / 1e12).toFixed(2)}T`;
  if (cap >= 1e9) return `$${(cap / 1e9).toFixed(2)}B`;
  if (cap >= 1e6) return `$${(cap / 1e6).toFixed(2)}M`;
  return `$${cap.toFixed(2)}`;
}

// 显示价格
function displayPrices(data, currency) {
  console.log('\n₿ CryptoWatch - 实时价格\n');
  console.log('币种    价格'.padEnd(25) + '24h 涨跌'.padEnd(15) + '市值'.padEnd(15) + '24h 成交量');
  console.log('─'.repeat(75));
  
  for (const [coinId, info] of Object.entries(data)) {
    const symbol = coinId.toUpperCase().slice(0, 6);
    const price = formatPrice(info[currency], currency);
    const change = formatChange(info[currency + '_24h_change']);
    const marketCap = formatMarketCap(info[currency + '_market_cap'], currency);
    const volume = formatMarketCap(info[currency + '_24h_vol'], currency);
    
    console.log(`${symbol.padEnd(8)} ${price.padEnd(12)} ${change.padEnd(15)} ${marketCap.padEnd(15)} ${volume}`);
  }
  
  console.log('─'.repeat(75) + '\n');
  console.log('🔍 查询其他币种：node scripts/watch.mjs btc,eth,sol');
  console.log('📊 查看市值排行：node scripts/watch.mjs --top 20');
  console.log('💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9');
  console.log('\n₿ CryptoWatch v0.1.0 - Never Miss a Pump\n');
}

// 显示市场排行
function displayRank(data) {
  console.log('\n₿ CryptoWatch - 市值排行\n');
  console.log('排名  币种'.padEnd(20) + '价格'.padEnd(15) + '24h 涨跌'.padEnd(12) + '市值');
  console.log('─'.repeat(65));
  
  data.forEach((coin, i) => {
    const rank = String(i + 1).padEnd(4);
    const name = `${coin.symbol.toUpperCase()} ${coin.name.slice(0, 10)}`.slice(0, 16);
    const price = formatPrice(coin.current_price, 'usd');
    const change = formatChange(coin.price_change_percentage_24h);
    const marketCap = formatMarketCap(coin.market_cap, 'usd');
    
    console.log(`${rank} ${name.padEnd(16)} ${price.padEnd(15)} ${change.padEnd(12)} ${marketCap}`);
  });
  
  console.log('─'.repeat(65) + '\n');
  console.log('🔍 查询特定币种：node scripts/watch.mjs btc');
  console.log('💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9');
  console.log('\n₿ CryptoWatch v0.1.0 - Never Miss a Pump\n');
}

// 主函数
async function main() {
  if (params.help) {
    showHelp();
    process.exit(0);
  }
  
  try {
    // 查看排行模式
    if (params.top) {
      const rank = await fetchMarketRank(params.vs, params.top);
      displayRank(rank);
      return;
    }
    
    // 默认显示主流币
    let coinIds = params.coins.length > 0 
      ? params.coins.map(resolveCoin)
      : DEFAULT_COINS;
    
    const data = await fetchPrices(coinIds, params.vs);
    displayPrices(data, params.vs);
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    console.error('\n可能是 API 限流，请稍后再试或减少查询频率');
    process.exit(1);
  }
}

main();
