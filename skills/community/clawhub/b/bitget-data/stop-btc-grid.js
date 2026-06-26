#!/usr/bin/env node

const fs = require('fs');
const crypto = require('crypto');
const https = require('https');

// 加载配置
const configPath = require('path').join(__dirname, 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

class BitgetClient {
    constructor(config) {
        this.apiKey = config.apiKey;
        this.secretKey = config.secretKey;
        this.passphrase = config.passphrase;
    }

    request(endpoint, method = 'GET', params = {}) {
        return new Promise((resolve, reject) => {
            const now = new Date();
            const timestamp = now.toISOString().split('.')[0] + '.000Z';
            let pathStr = endpoint;
            let body = '';

            if (method === 'GET' && Object.keys(params).length > 0) {
                pathStr += '?' + new URLSearchParams(params).toString();
            } else if (method === 'POST') {
                body = JSON.stringify(params);
            }

            const fullpath = pathStr.startsWith('/api') ? pathStr : '/api/v2' + pathStr;
            const signStr = timestamp + method + fullpath + body;
            const signature = crypto.createHmac('sha256', this.secretKey).update(signStr).digest('base64');

            const options = {
                hostname: 'api.bitget.com',
                port: 443,
                path: fullpath,
                method: method,
                headers: {
                    'ACCESS-KEY': this.apiKey,
                    'ACCESS-SIGN': signature,
                    'ACCESS-TIMESTAMP': timestamp,
                    'ACCESS-PASSPHRASE': this.passphrase,
                    'Content-Type': 'application/json'
                }
            };

            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', (chunk) => { data += chunk; });
                res.on('end', () => {
                    try {
                        resolve(JSON.parse(data));
                    } catch (e) {
                        resolve({ data: data });
                    }
                });
            });

            req.on('error', reject);
            if (body) req.write(body);
            req.end();
        });
    }
}

async function getOpenOrders(symbol) {
    const client = new BitgetClient(config);
    const result = await client.request('/spot/v1/orders', 'GET', { symbol: symbol + 'USDT' });
    return result;
}

async function cancelOrder(symbol, orderId) {
    const client = new BitgetClient(config);
    const result = await client.request('/spot/v1/cancel-order', 'POST', {
        symbol: symbol + 'USDT',
        orderId: orderId
    });
    return result;
}

async function main() {
    console.log('========================================');
    console.log('🛑 停止 BTC 网格策略');
    console.log('========================================');
    
    // 获取 BTC 未成交订单
    console.log('\n📋 获取 BTC 未成交订单...');
    const ordersResult = await getOpenOrders('BTC');
    
    if (ordersResult.code === 0 || ordersResult.code === '0') {
        const orders = ordersResult.data;
        console.log(`   找到 ${orders.length} 个未成交订单`);
        
        if (orders.length === 0) {
            console.log('\n✅ BTC 没有未成交订单，网格已停止');
            return;
        }
        
        // 取消所有订单
        console.log('\n🔄 开始取消订单...');
        let cancelled = 0;
        let failed = 0;
        
        for (const order of orders) {
            const result = await cancelOrder('BTC', order.order_id);
            if (result.code === 0 || result.code === '0') {
                cancelled++;
                console.log(`   ✅ 已取消：${order.side} ${order.price} x ${order.size}`);
            } else {
                failed++;
                console.log(`   ❌ 失败：${order.side} ${order.price} x ${order.size} - ${result.msg}`);
            }
        }
        
        console.log('\n========================================');
        console.log(`✅ 完成：取消 ${cancelled} 个，失败 ${failed} 个`);
        console.log('========================================');
    } else {
        console.log('❌ 获取订单失败:', ordersResult);
    }
}

main().catch(console.error);
