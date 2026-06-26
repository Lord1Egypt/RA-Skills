#!/usr/bin/env node
/**
 * ₿ CryptoWatch - 涨跌幅排行榜
 * 查看所有加密货币的 24h 涨跌排名
 */

import fetch from 'node-fetch';

async function getTopGainers(limit = 10) {
    try {
        console.log('📊 加载中...\n');
        
        const response = await fetch(
            'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=percent_change_24h_desc&per_page=100&page=1&sparkline=false',
            { timeout: 10000 }
        );
        
        if (!response.ok) {
            throw new Error(`API 错误：${response.status}`);
        }
        
        const data = await response.json();
        
        // 过滤交易量 > 100 万
        const filtered = data.filter(coin => coin.total_volume > 1000000);
        
        console.log(`₿ CryptoWatch - 24h 涨跌幅排行榜 (Top ${limit})\n`);
        console.log(`排名  名称              价格 (USD)      24h 涨跌    市值        24h 成交量`);
        console.log(`────────────────────────────────────────────────────────────────────────────`);
        
        filtered.slice(0, limit).forEach((coin, index) => {
            const rank = (index + 1).toString().padEnd(4);
            const name = `${coin.name} (${coin.symbol.toUpperCase()})`.padEnd(20);
            const price = `$${coin.current_price.toLocaleString('en-US', { 
                minimumFractionDigits: 2, 
                maximumFractionDigits: 6 
            })}`.padEnd(14);
            
            const change = coin.price_change_percentage_24h;
            const changeColor = change >= 10 ? '🟢🚀' : change >= 5 ? '🟢' : change >= 0 ? '🟡' : '🔴';
            const changeStr = `${changeColor} ${change >= 0 ? '+' : ''}${change.toFixed(2)}%`.padEnd(12);
            
            const marketCap = `$${(coin.market_cap / 1e9).toFixed(2)}B`.padEnd(12);
            const volume = `$${(coin.total_volume / 1e6).toFixed(0)}M`;
            
            console.log(`${rank} ${name} ${price} ${changeStr} ${marketCap} ${volume}`);
        });
        
        console.log(`\n💡 提示：node scripts/top.mjs 20 查看更多`);
        console.log(`🔗 数据来源：CoinGecko API`);
        
    } catch (error) {
        console.error('❌ 获取数据失败:', error.message);
        console.error('\n💡 CoinGecko API 可能限流，请等待 1 分钟后重试');
        process.exit(1);
    }
}

async function getTopLosers(limit = 10) {
    try {
        console.log('📊 加载中...\n');
        
        const response = await fetch(
            'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=percent_change_24h_asc&per_page=100&page=1&sparkline=false',
            { timeout: 10000 }
        );
        
        if (!response.ok) {
            throw new Error(`API 错误：${response.status}`);
        }
        
        const data = await response.json();
        
        // 过滤交易量 > 100 万
        const filtered = data.filter(coin => coin.total_volume > 1000000);
        
        console.log(`🔴 CryptoWatch - 24h 跌幅排行榜 (Bottom ${limit})\n`);
        console.log(`排名  名称              价格 (USD)      24h 涨跌    市值        24h 成交量`);
        console.log(`────────────────────────────────────────────────────────────────────────────`);
        
        filtered.slice(0, limit).forEach((coin, index) => {
            const rank = (index + 1).toString().padEnd(4);
            const name = `${coin.name} (${coin.symbol.toUpperCase()})`.padEnd(20);
            const price = `$${coin.current_price.toLocaleString('en-US', { 
                minimumFractionDigits: 2, 
                maximumFractionDigits: 6 
            })}`.padEnd(14);
            
            const change = coin.price_change_percentage_24h;
            const changeColor = change <= -10 ? '🔴📉' : change <= -5 ? '🔴' : '🟡';
            const changeStr = `${changeColor} ${change.toFixed(2)}%`.padEnd(12);
            
            const marketCap = `$${(coin.market_cap / 1e9).toFixed(2)}B`.padEnd(12);
            const volume = `$${(coin.total_volume / 1e6).toFixed(0)}M`;
            
            console.log(`${rank} ${name} ${price} ${changeStr} ${marketCap} ${volume}`);
        });
        
        console.log(`\n💡 提示：市场波动大，投资需谨慎！`);
        
    } catch (error) {
        console.error('❌ 获取数据失败:', error.message);
        process.exit(1);
    }
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
₿ CryptoWatch - 涨跌幅排行榜

用法:
  node scripts/top.mjs              # 查看涨幅榜 Top 10
  node scripts/top.mjs 20           # 查看涨幅榜 Top 20
  node scripts/top.mjs --losers     # 查看跌幅榜
  node scripts/top.mjs --losers 15  # 查看跌幅榜 Bottom 15

选项:
  --help, -h     显示帮助
  --losers       显示跌幅榜 (默认涨幅榜)
`);
    process.exit(0);
}

const limit = parseInt(args.find(a => !a.startsWith('--'))) || 10;

if (args.includes('--losers')) {
    await getTopLosers(limit);
} else {
    await getTopGainers(limit);
}
