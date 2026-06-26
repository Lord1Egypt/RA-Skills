#!/usr/bin/env node

/**
 * OKX K线数据获取脚本
 * 支持时间戳分页查询历史数据
 * 
 * 用法: node okx-kline.js <交易对> <周期> [数量] [--after=时间戳] [--before=时间戳]
 * 例: node okx-kline.js BTC-USDT 1d 30
 *     node okx-kline.js BTC-USDT 4h 100 --after=1743500000000
 * 
 * 环境变量支持代理:
 *   export http_proxy=http://192.168.10.188:7897
 *   export https_proxy=http://192.168.10.188:7897
 */

const https = require('https');
const http = require('http');

const BASE_URL = 'www.okx.com';
const BASE_PATH = '/api/v5/market/history-candles';

const PERIOD_MAP = {
  '1m': '1m',
  '5m': '5m',
  '15m': '15m',
  '30m': '30m',
  '1h': '1H',
  '2h': '2H',
  '4h': '4H',
  '6h': '6H',
  '12h': '12H',
  '1d': '1D',
  '1w': '1W',
  '1M': '1M'
};

function fetchKline(instId, bar, limit = 100, after = null, before = null) {
  return new Promise((resolve, reject) => {
    const params = new URLSearchParams({
      instId: instId,
      bar: PERIOD_MAP[bar] || '1D',
      limit: Math.min(limit, 100).toString()
    });

    if (after) params.append('after', after);
    if (before) params.append('before', before);

    const options = {
      hostname: BASE_URL,
      path: `${BASE_PATH}?${params}`,
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0'
      }
    };

    // Use proxy if available
    const proxy = process.env.http_proxy || process.env.https_proxy || process.env.HTTP_PROXY || process.env.HTTPS_PROXY;
    
    if (proxy) {
      const proxyUrl = new URL(proxy);
      options.hostname = proxyUrl.hostname;
      options.port = proxyUrl.port;
      options.path = `https://${BASE_URL}${options.path}`;
      options.headers['Host'] = BASE_URL;
    }

    const client = proxy ? http : https;
    
    const req = client.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.code === '0') {
            resolve(json.data);
          } else {
            reject(new Error(json.msg || 'API Error'));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(15000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    req.end();
  });
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log('用法: node okx-kline.js <交易对> <周期> [数量] [--after=时间戳] [--before=时间戳]');
    console.log('例: node okx-kline.js BTC-USDT 1d 30');
    console.log('    node okx-kline.js BTC-USDT 4h 100 --after=1743500000000');
    console.log('');
    console.log('周期: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d, 1w, 1M');
    console.log('');
    console.log('时间戳分页:');
    console.log('  --after=时间戳   查询指定时间之前的数据（更早）');
    console.log('  --before=时间戳  查询指定时间之后的数据（更新）');
    console.log('');
    console.log('环境变量支持代理:');
    console.log('  export http_proxy=http://192.168.10.188:7897');
    console.log('  export https_proxy=http://192.168.10.188:7897');
    process.exit(1);
  }

  const instId = args[0].toUpperCase();
  const period = args[1] || '1d';
  let limit = parseInt(args[2]) || 100;
  limit = Math.min(limit, 100);
  
  let after = null;
  let before = null;
  
  for (let i = 3; i < args.length; i++) {
    if (args[i].startsWith('--after=')) {
      after = args[i].split('=')[1];
    } else if (args[i].startsWith('--before=')) {
      before = args[i].split('=')[1];
    }
  }

  try {
    const data = await fetchKline(instId, period, limit, after, before);
    
    if (!data || data.length === 0) {
      console.log('❌ 未找到数据');
      process.exit(1);
    }
    
    const klines = [...data].reverse();
    
    console.log(`\n📊 ${instId} ${period} K线数据 - 最近${klines.length}条\n`);
    console.log('时间                 开盘      最高      最低      收盘      成交量');
    console.log('-'.repeat(75));
    
    for (const k of klines) {
      const ts = parseInt(k[0]);
      const dt = new Date(ts);
      const dateStr = dt.toISOString().replace('T', ' ').substring(0, 16);
      
      console.log(
        `${dateStr}  ` +
        `${parseFloat(k[1]).toFixed(2).padStart(9)}  ` +
        `${parseFloat(k[2]).toFixed(2).padStart(9)}  ` +
        `${parseFloat(k[3]).toFixed(2).padStart(9)}  ` +
        `${parseFloat(k[4]).toFixed(2).padStart(9)}  ` +
        `${(parseFloat(k[5]) / 1000).toFixed(2)}K`
      );
    }
    
    if (klines.length > 0) {
      const firstTs = parseInt(klines[0][0]);
      const lastTs = parseInt(klines[klines.length - 1][0]);
      console.log('-'.repeat(75));
      console.log(`📅 数据范围: ${new Date(firstTs).toISOString().substring(0, 19)} ~ ${new Date(lastTs).toISOString().substring(0, 19)}`);
    }
    
  } catch (err) {
    console.error('❌ 获取失败:', err.message);
    process.exit(1);
  }
}

main();
