#!/usr/bin/env node
// 使用官方 bitget-api SDK 创建网格订单

const { SpotClient } = require('bitget-api');

const fs = require('fs');
const CONFIG = JSON.parse(fs.readFileSync(__dirname + '/config.json'));
const SETTINGS = JSON.parse(fs.readFileSync(__dirname + '/grid_settings.json'));

function log(msg) {
    console.log(`[${new Date().toLocaleString('zh-CN')}] ${msg}`);
}

// 创建客户端
const client = new SpotClient({
    apiKey: CONFIG.apiKey,
    secretKey: CONFIG.secretKey,
    passphrase: CONFIG.passphrase,
    useServerTime: true
});

async function placeOrder(symbol, side, price, quantity) {
    try {
        const params = {
            symbol: symbol + '_SPBL',  // SDK 需要这个格式
            side,
            force: 'normal',
            orderType: 'limit',
            price: price.toString(),
            quantity: quantity.toString()
        };
        
        const result = await client.placeOrder(params);
        return {
            success: result.code === '00000',
            orderId: result.data?.orderId,
            msg: result.msg
        };
    } catch (e) {
        return {
            success: false,
            msg: e.message
        };
    }
}

async function main() {
    log('=' .repeat(70));
    log('🔄 Bitget 网格重启 - 使用官方 SDK');
    log('=' .repeat(70));
    
    // 获取价格
    const btcTicker = await client.getTicker('BTCUSDT_SPBL');
    const solTicker = await client.getTicker('SOLUSDT_SPBL');
    
    const btcPrice = parseFloat(btcTicker.data?.lastPr || 67500);
    const solPrice = parseFloat(solTicker.data?.lastPr || 82.8);
    
    log(`\n💰 当前价格:`);
    log(`   BTCUSDT: ${btcPrice} USDT`);
    log(`   SOLUSDT: ${solPrice} USDT`);
    
    // 创建 BTC 网格
    log('\n📊 创建 BTC 网格...');
    const { gridNum: btcGrids, priceMin: btcMin, priceMax: btcMax, amount: btcAmount } = SETTINGS.btc;
    const step = (btcMax - btcMin) / btcGrids;
    
    let btcPlaced = 0;
    for (let i = 0; i < btcGrids; i++) {
        const price = btcMin + i * step;
        if (Math.abs(price - btcPrice) < step) continue; // 跳过当前价
        
        const side = price < btcPrice ? 'buy' : 'sell';
        const quantity = btcAmount / price;
        
        const result = await placeOrder('BTCUSDT', side, price.toFixed(2), quantity.toFixed(6));
        if (result.success) {
            btcPlaced++;
            if (btcPlaced <= 3) log(`   ✅ ${side.toUpperCase()}: ${quantity.toFixed(6)} @ ${price.toFixed(2)}`);
        }
    }
    log(`BTC 成功：${btcPlaced} 个订单`);
    
    // 创建 SOL 网格
    log('\n📊 创建 SOL 网格...');
    const { gridNum: solGrids, priceMin: solMin, priceMax: solMax, amount: solAmount } = SETTINGS.sol;
    const solStep = (solMax - solMin) / solGrids;
    
    let solPlaced = 0;
    for (let i = 0; i < solGrids; i++) {
        const price = solMin + i * solStep;
        if (Math.abs(price - solPrice) < solStep) continue;
        
        const side = price < solPrice ? 'buy' : 'sell';
        const quantity = solAmount / price;
        
        const result = await placeOrder('SOLUSDT', side, price.toFixed(2), quantity.toFixed(6));
        if (result.success) {
            solPlaced++;
            if (solPlaced <= 3) log(`   ✅ ${side.toUpperCase()}: ${quantity.toFixed(6)} @ ${price.toFixed(2)}`);
        }
    }
    log(`SOL 成功：${solPlaced} 个订单`);
    
    // 汇总
    log('\n' + '=' .repeat(70));
    log('📊 完成汇总');
    log('=' .repeat(70));
    log(`BTC: ${btcPlaced} 个订单`);
    log(`SOL: ${solPlaced} 个订单`);
    log(`总计：${btcPlaced + solPlaced} 个订单`);
    
    if (btcPlaced > 0 && solPlaced > 0) {
        log('\n✅ 网格创建成功！');
    } else {
        log('\n⚠️  订单创建失败');
    }
    log('=' .repeat(70) + '\n');
}

main().catch(e => {
    log('❌ 错误：' + e.message);
    process.exit(1);
});
