#!/usr/bin/env node

/**
 * Huobi K线数据获取脚本
 * 用法: node huobi-kline.js <交易对> <周期> <数量>
 * 例: node huobi-kline.js btcusdt 1d 30
 */

const https = require('https');

const BASE_URL = 'api.huobi.pro';
const BASE_PATH = '/market/history/kline';

const PERIOD_MAP = {
  '1min': '1min',
  '5min': '5min',
  '15min': '15min',
  '30min': '30min',
  '1h': '60min',
  '1d': '1day',
  '1w': '1week',
  '1M': '1mon'
};

function fetchKline(symbol, period, size = 10) {
  return new Promise((resolve, reject) => {
    const params = new URLSearchParams({
      symbol: symbol.toLowerCase(),
      period: PERIOD_MAP[period] || '1day',
      size: Math.min(size, 2000)
    });

    const options = {
      hostname: BASE_URL,
      path: `${BASE_PATH}?${params}`,
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.status === 'ok') {
            resolve(json.data);
          } else {
            reject(new Error(json['err-msg'] || 'API Error'));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    req.end();
  });
}

function formatTimestamp(ts) {
  return new Date(ts).toISOString().replace('T', ' ').substring(0, 19);
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log('用法: node huobi-kline.js <交易对> [周期] [数量]');
    console.log('例: node huobi-kline.js btcusdt 1d 30');
    console.log('');
    console.log('周期: 1min, 5min, 15min, 30min, 1h, 1d, 1w, 1M');
    process.exit(1);
  }

  const symbol = args[0].toLowerCase();
  const period = args[1] || '1d';
  const size = parseInt(args[2]) || 10;

  try {
    const data = await fetchKline(symbol, period, size);
    
    // 倒序显示（最新在前）
    const sorted = [...data].reverse();
    
    console.log(`\n📊 ${symbol.toUpperCase()} K线数据 (${period}) - 最近${sorted.length}条\n`);
    console.log('时间                 开盘      最高      最低      收盘      成交量');
    console.log('-'.repeat(75));
    
    for (const k of sorted) {
      console.log(
        `${formatTimestamp(k.id * 1000)}  ` +
        `${k.open.toFixed(2).padStart(9)}  ` +
        `${k.high.toFixed(2).padStart(9)}  ` +
        `${k.low.toFixed(2).padStart(9)}  ` +
        `${k.close.toFixed(2).padStart(9)}  ` +
        `${(k.vol / 1000).toFixed(2)}K`
      );
    }
    
    // 显示最新和最早的收盘价
    if (sorted.length > 1) {
      const latest = sorted[sorted.length - 1];
      const oldest = sorted[0];
      const change = ((latest.close - oldest.close) / oldest.close * 100).toFixed(2);
      console.log('-'.repeat(75));
      console.log(`📈 期间涨幅: ${change > 0 ? '+' : ''}${change}%`);
    }
    
  } catch (err) {
    console.error('❌ 获取失败:', err.message);
    process.exit(1);
  }
}

main();
