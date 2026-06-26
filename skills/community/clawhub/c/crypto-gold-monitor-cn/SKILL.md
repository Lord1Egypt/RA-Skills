---
name: crypto-gold-monitor
description: "加密货币与贵金属价格监控 / Crypto & Precious Metals Price Monitor - 监控BTC/ETH实时价格、黄金/白银国内外价格，免费无需Key"
---

# 加密货币与贵金属价格监控 / Crypto & Precious Metals Price Monitor

实时监控比特币、以太坊、黄金、白银价格走势，支持国内外价格对比。

Real-time monitoring of Bitcoin, Ethereum, Gold, and Silver prices with domestic vs international comparison.

## 功能特性 / Features

- ₿ **比特币 / Bitcoin** - 实时价格 (USD/CNY)、24h涨跌
  - Real-time price (USD/CNY), 24h change

- Ξ **以太坊 / Ethereum** - 实时价格 (USD/CNY)、24h涨跌
  - Real-time price (USD/CNY), 24h change

- 🥇 **黄金 / Gold** - 国内金价 + 国际金价
  - Domestic Gold (CNY/gram) + International Gold (USD/oz)

- 🥈 **白银 / Silver** - 国内银价 + 国际银价
  - Domestic Silver (CNY/gram) + International Silver (USD/oz)

- 💱 **汇率显示 / Exchange Rate** - 实时USD/CNY汇率
  - Real-time USD/CNY exchange rate

- 🔄 **自动缓存 / Auto Cache** - 5分钟缓存，避免频繁请求
  - 5-minute cache to avoid excessive requests

## 使用方法 / Usage

### 1. 查看所有价格 / View All Prices
```bash
crypto-monitor all
```

### 2. 强制刷新 / Force Refresh
```bash
crypto-monitor refresh
```

### 3. 查看帮助 / View Help
```bash
crypto-monitor help
```

## 数据来源 / Data Sources

### 加密货币 / Crypto
- **CoinGecko API** (免费，无需API Key)
- 无请求限制 / No rate limits

### 贵金属 / Precious Metals
- **张良珠宝 API** - 国内实时报价
  - 国内金价 (元/克)
  - 国际金价 (伦敦金，美元/盎司)
  - 国内银价 (元/克)
  - 国际银价 (伦敦银，美元/盎司)

### 汇率 / Exchange Rate
- **exchangerate-api.com** - 实时 USD/CNY

## 价格说明 / Price Notes

| 品种 | 国内价格 | 国际价格 |
|------|---------|---------|
| 黄金 | 元/克 (约 ¥1,115/克) | 美元/盎司 (约 $5,020/oz) |
| 白银 | 元/克 (约 ¥19.7/克) | 美元/盎司 (约 $79/oz) |

⚠️ 投资有风险，数据仅供参考
⚠️ Investment involves risk, data for reference only

## 常见问题 / FAQ

**Q: 需要API Key吗？**
A: 不需要，全部免费API。

**Q: 数据多久更新一次？**
A: 默认缓存5分钟，可用 `refresh` 强制刷新。

**Q: 国内金价和国际金价有什么区别？**
A: 国内金价包含税费和加工费，通常比国际金价贵。张良珠宝数据来自国内珠宝商报价。