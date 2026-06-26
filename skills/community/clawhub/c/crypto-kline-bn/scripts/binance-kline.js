#!/usr/bin/env node
/**
 * Binance K线获取脚本 (支持代理)
 * 用法: node binance-kline.js <交易对> <周期> [数量] [代理]
 * 例: node binance-kline.js BTCUSDT 1h 100
 *     node binance-kline.js BTCUSDT 1h 100 http://192.168.10.188:7897
 */

const http = require('http');
const https = require('https');

function formatTime(ts) {
  const date = new Date(ts);
  return date.toISOString().replace('T', ' ').substring(0, 19);
}

function fetchKlines(symbol, interval, limit = 100, proxy = null) {
  return new Promise((resolve, reject) => {
    const url = `https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=${limit}`;
    
    const options = {
      timeout: 30000
    };

    // 使用代理
    if (proxy) {
      const urlObj = new URL(proxy);
      options.hostname = urlObj.hostname;
      options.port = urlObj.port;
      options.path = url;
      options.method = 'GET';
      options.headers = {
        'Host': 'api.binance.com'
      };
    }

    const client = proxy ? http : https;
    
    const req = client.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const klines = JSON.parse(data);
          resolve(klines);
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => req.destroy());
    req.end();
  });
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('用法: node binance-kline.js <交易对> <周期> [数量] [代理]');
    console.log('例: node binance-kline.js BTCUSDT 1h 100');
    console.log('    node binance-kline.js BTCUSDT 1h 100 http://192.168.10.188:7897');
    console.log('');
    console.log('周期: 1m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1d, 1w, 1M');
    process.exit(1);
  }

  const symbol = args[0].toUpperCase();
  const interval = args[1];
  const limit = parseInt(args[2]) || 100;
  const proxy = args[3] || process.env.HTTPS_PROXY || process.env.http_proxy;

  console.log(`📊 获取 ${symbol} ${interval} K线 (${limit}条)...\n`);
  if (proxy) console.log(`   代理: ${proxy}\n`);

  try {
    const klines = await fetchKlines(symbol, interval, limit, proxy);
    
    console.log(`${'时间'.padEnd(20)} ${'开盘'.padEnd(12)} ${'最高'.padEnd(12)} ${'最低'.padEnd(12)} ${'收盘'.padEnd(12)} ${'成交量'.padEnd(14)}`);
    console.log('-'.repeat(90));

    klines.forEach(k => {
      const [ts, open, high, low, close, vol] = [k[0], k[1], k[2], k[3], k[4], k[5]];
      console.log(`${formatTime(ts)} ${open.padStart(11)} ${high.padStart(11)} ${low.padStart(11)} ${close.padStart(11)} ${(parseFloat(vol)/1000).toFixed(2)}K`.padEnd(90));
    });

    console.log(`\n共 ${klines.length} 条`);

  } catch (e) {
    console.error('❌ 获取失败:', e.message);
    process.exit(1);
  }
}

main();
