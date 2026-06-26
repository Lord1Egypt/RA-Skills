
const fs = require('fs');
const newSettings = {
  "btc": {
    "symbol": "BTCUSDT",
    "gridNum": 30,
    "priceMin": 63000,
    "priceMax": 70000,
    "amount": 12,
    "maxPosition": 400,
    "notes": "2026-03-09 盈利优化：下移区间 + 加宽间距"
  },
  "sol": {
    "symbol": "SOLUSDT",
    "gridNum": 30,
    "priceMin": 75,
    "priceMax": 95,
    "amount": 15,
    "maxPosition": 400,
    "notes": "2026-03-09 盈利优化"
  },
  "eth": {
    "symbol": "ETHUSDT",
    "gridNum": 15,
    "priceMin": 1800,
    "priceMax": 2700,
    "amount": 4,
    "maxPosition": 150,
    "sellOrders": 5,
    "buyOrders": 8,
    "notes": "2026-03-09 已部署：卖单 2513-2620(5 个) | 买单 1800-2001(8 个)"
  },
  "bnb": {
    "symbol": "BNBUSDT",
    "gridNum": 10,
    "priceMin": 610,
    "priceMax": 660,
    "amount": 90,
    "maxPosition": 600,
    "sellOrders": 5,
    "buyOrders": 5,
    "notes": "2026-03-09 已调整：买单 610-625(5 个) | 卖单 640-660(5 个) | 围绕现价 630"
  },
  "optimization": {
    "date": "2026-03-09",
    "goal": "多币种分散，盈利最大化",
    "changes": [
      "新增 ETH 网格",
      "后续扩展 BNB/XRP/DOGE/AVAX"
    ]
  }
};
fs.writeFileSync('grid_settings.json', JSON.stringify(newSettings, null, 2));
console.log('✅ 网格配置已优化并保存！');
console.log('建议重启网格监控系统：node start-simple.js');
