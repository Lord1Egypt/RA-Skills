#!/usr/bin/env node
/**
 * 部署卖单脚本
 * 检查持仓并基于持仓部署卖单网格
 */

const http = require('http');
const https = require('https');
const fs = require('fs');
const crypto = require('crypto');

const CONFIG = JSON.parse(fs.readFileSync(__dirname + '/config.json'));
const SETTINGS = JSON.parse(fs.readFileSync(__dirname + '/grid_settings_highfreq.json'));

function sign(message) {
  return crypto.createHmac('sha256', CONFIG.secretKey).update(message).digest('base64');
}

function request(endpoint, method = 'GET', params = {}, body = null) {
  return new Promise((resolve) => {
    const timestamp = new Date().toISOString().split('.')[0] + '.000Z';
    const fullpath = '/api/v2' + endpoint + (method === 'GET' && Object.keys(params).length ? '?' + new URLSearchParams(params) : '');
    const bodyStr = method === 'POST' && body ? JSON.stringify(body) : '';
    const signStr = timestamp + method + fullpath + bodyStr;
    const signature = sign(signStr);
    
    const proxyOptions = { hostname: '127.0.0.1', port: 7897, path: 'api.bitget.com:443', method: 'CONNECT' };
    const proxyReq = http.request(proxyOptions);
    
    proxyReq.on('connect', (res, socket) => {
      const req = https.request({
        socket, hostname: 'api.bitget.com', port: 443, path: fullpath, method,
        headers: {
          'ACCESS-KEY': CONFIG.apiKey,
          'ACCESS-SIGN': signature,
          'ACCESS-TIMESTAMP': timestamp,
          'ACCESS-PASSPHRASE': CONFIG.passphrase,
          'Content-Type': 'application/json'
        }
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => { try { resolve(JSON.parse(data)); } catch(e) { resolve({raw: data}); } });
      });
      req.on('error', e => resolve({error: e.message}));
      if (bodyStr) req.write(bodyStr);
      req.end();
    });
    proxyReq.on('error', e => resolve({error: e.message}));
    proxyReq.end();
  });
}

async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function deploySellOrders(coin) {
  const config = SETTINGS[coin];
  if (!config || !config.enabled) return;
  
  const symbol = config.symbol;
  const baseSymbol = symbol.replace('USDT', '');
  
  console.log(`\n🚀 部署 ${symbol} 卖单...`);
  
  // 获取持仓
  const assetResult = await request('/spot/account/assets', 'GET', { symbol: baseSymbol });
  const asset = assetResult.data?.find(a => a.symbol === baseSymbol);
  const available = parseFloat(asset?.available || 0);
  
  console.log(`   💰 可用持仓：${available.toFixed(4)} ${baseSymbol}`);
  
  if (available < 0.01) {
    console.log(`   ⚠️ 持仓不足，跳过`);
    return;
  }
  
  // 获取当前价格
  const tickerResult = await request('/spot/market/tickers', 'GET', { symbol });
  const currentPrice = parseFloat(tickerResult.data?.[0]?.lastPr || 0);
  
  if (!currentPrice) {
    console.log(`   ❌ 无法获取价格`);
    return;
  }
  
  console.log(`   📊 当前价格：${currentPrice} USDT`);
  
  // 计算网格
  const priceRange = config.priceMax - config.priceMin;
  const gridSpacing = priceRange / config.gridNum;
  const sellLevels = Math.ceil(config.gridNum / 2);
  
  console.log(`   📐 网格间距：${gridSpacing.toFixed(4)} (${(gridSpacing/currentPrice*100).toFixed(2)}%)`);
  console.log(`   📈 计划卖单：${sellLevels} 个`);
  
  // 计算每个卖单的金额
  const amountPerOrder = available / sellLevels;
  const minOrderValue = config.minOrderValue || 1;
  
  // 部署卖单
  let placed = 0;
  for (let i = 0; i < sellLevels; i++) {
    const price = currentPrice * (1 + (i + 1) * (gridSpacing / currentPrice));
    if (price > config.priceMax) break;
    
    // 计算数量，确保订单金额 >= 最小限制
    let size = amountPerOrder;
    const orderValue = price * size;
    
    if (orderValue < minOrderValue) {
      console.log(`   ⚠️ 订单金额不足，跳过`);
      continue;
    }
    
    const priceScale = coin === 'eth' ? 2 : 2;
    const sizeScale = coin === 'eth' ? 4 : 2;
    
    const priceStr = price.toFixed(priceScale);
    const sizeStr = size.toFixed(sizeScale);
    
    const result = await request('/spot/trade/place-order', 'POST', {}, {
      symbol: symbol,
      side: 'sell',
      orderType: 'limit',
      price: priceStr,
      size: sizeStr,
      force: 'GTC'
    });
    
    if (result.code === '00000' || result.msg === 'success') {
      placed++;
      console.log(`   ✅ 卖单 #${i+1}: ${priceStr} x ${sizeStr} ${baseSymbol} (≈${(price*size).toFixed(2)} USDT)`);
    } else {
      console.log(`   ❌ 卖单 #${i+1} 失败：${result.msg || result.error}`);
    }
    
    await sleep(300); // 避免限流
  }
  
  console.log(`\n   ✅ ${symbol} 卖单部署完成：${placed} 个`);
  return placed;
}

async function main() {
  console.log('='.repeat(60));
  console.log('🚀 Bitget 卖单部署脚本');
  console.log('='.repeat(60));
  
  try {
    await deploySellOrders('sol');
    await sleep(500);
    await deploySellOrders('eth');
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ 所有卖单部署完成！');
    console.log('='.repeat(60));
  } catch (error) {
    console.log(`\n❌ 部署异常：${error.message}`);
  }
}

main();
