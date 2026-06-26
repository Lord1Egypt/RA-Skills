#!/usr/bin/env node
// Bitget 高频网格配置 - 目标：每天 60-100 笔交易

const fs = require('fs');

// 高频交易配置 - 加密网格 + 合理区间
const HIGH_FREQUENCY_CONFIG = {
  "btc": {
    "symbol": "BTCUSDT",
    "gridNum": 80,              // 80 格 - 超密集
    "priceMin": 67000,          // 当前价~70300, -4.7%
    "priceMax": 74000,          // 当前价~70300, +5.3%
    "amount": 20,               // 每格 20 USDT
    "maxPosition": 600,         // 最大持仓
    "sellOrders": 40,
    "buyOrders": 40,
    "targetTradesPerDay": 30,   // BTC 目标 30 笔/天
    "notes": "BTC 高频 - 间距约 0.12%, 区间±5%"
  },
  "sol": {
    "symbol": "SOLUSDT",
    "gridNum": 100,             // 100 格 - 超密集
    "priceMin": 82,             // 当前价~87, -5.7%
    "priceMax": 92,             // 当前价~87, +5.7%
    "amount": 8,                // 每格 8 USDT
    "maxPosition": 400,
    "sellOrders": 50,
    "buyOrders": 50,
    "targetTradesPerDay": 40,   // SOL 目标 40 笔/天
    "notes": "SOL 高频 - 间距约 0.11%, 区间±6%, 高波动"
  },
  "eth": {
    "symbol": "ETHUSDT",
    "gridNum": 60,              // 60 格
    "priceMin": 1950,           // 当前价~2060, -5.3%
    "priceMax": 2180,           // 当前价~2060, +5.8%
    "amount": 3,                // 每格 3 USDT
    "maxPosition": 200,
    "sellOrders": 30,
    "buyOrders": 30,
    "targetTradesPerDay": 20,   // ETH 目标 20 笔/天
    "notes": "ETH 高频 - 间距约 0.19%, 区间±5.5%"
  },
  "avax": {
    "symbol": "AVAXUSDT",
    "gridNum": 80,              // 80 格
    "priceMin": 9.0,            // 当前价~9.6, -6.3%
    "priceMax": 10.3,           // 当前价~9.6, +7.3%
    "amount": 10,               // 每格 10 USDT
    "maxPosition": 350,
    "sellOrders": 40,
    "buyOrders": 40,
    "targetTradesPerDay": 25,   // AVAX 目标 25 笔/天
    "notes": "AVAX 高频 - 间距约 0.16%, 区间±6.5%"
  },
  "optimization": {
    "date": "2026-03-12",
    "goal": "高频交易 - 每天 60-100 笔",
    "totalTargetTrades": 115,   // 总计约 115 笔/天（留余量）
    "strategy": "超密集网格 + 小区间 + 自动调优",
    "changes": [
      "BTC: 30 格→80 格，间距 0.57%→0.12%",
      "SOL: 50 格→100 格，间距 0.2%→0.11%",
      "ETH: 30 格→60 格，间距 1.5%→0.19%",
      "AVAX: 40 格→80 格，间距 1.75%→0.16%",
      "所有币种区间缩小到±5-7%，资金更集中"
    ],
    "expectedDailyProfit": "0.8-1.5% (高频薄利)",
    "riskControl": [
      "严格 maxPosition 限制",
      "每 30 分钟监控成交",
      "自动调整网格密度",
      "异常波动时暂停"
    ]
  }
};

// 保存配置
const configPath = __dirname + '/grid_settings_highfreq.json';
fs.writeFileSync(configPath, JSON.stringify(HIGH_FREQUENCY_CONFIG, null, 2));

console.log('✅ 高频网格配置已生成！');
console.log('📁 配置文件：' + configPath);
console.log('\n📊 配置概览:');
console.log('─'.repeat(60));
console.log(`BTC:  ${HIGH_FREQUENCY_CONFIG.btc.gridNum}格 | 间距~0.12% | 目标${HIGH_FREQUENCY_CONFIG.btc.targetTradesPerDay}笔/天`);
console.log(`SOL:  ${HIGH_FREQUENCY_CONFIG.sol.gridNum}格 | 间距~0.11% | 目标${HIGH_FREQUENCY_CONFIG.sol.targetTradesPerDay}笔/天`);
console.log(`ETH:  ${HIGH_FREQUENCY_CONFIG.eth.gridNum}格 | 间距~0.19% | 目标${HIGH_FREQUENCY_CONFIG.eth.targetTradesPerDay}笔/天`);
console.log(`AVAX: ${HIGH_FREQUENCY_CONFIG.avax.gridNum}格 | 间距~0.16% | 目标${HIGH_FREQUENCY_CONFIG.avax.targetTradesPerDay}笔/天`);
console.log('─'.repeat(60));
console.log(`🎯 总目标：${HIGH_FREQUENCY_CONFIG.optimization.totalTargetTrades} 笔/天`);
console.log(`💰 预期日收益：${HIGH_FREQUENCY_CONFIG.optimization.expectedDailyProfit}`);
console.log('\n💡 下一步：运行 apply-highfreq.js 应用配置');
