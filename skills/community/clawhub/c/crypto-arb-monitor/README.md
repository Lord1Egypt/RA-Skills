# Crypto Arbitrage Monitor 🔍💰

**跨交易所加密货币套利机会监控器**

## 这是什么？

一个实时监控加密货币在不同交易所之间价格差异的工具。当发现有利可图的套利机会时，自动通过飞书/Telegram发送预警。

## 支持的交易所

- Binance (币安)
- OKX (欧易)
- Bybit

## 支持的币种

- BTC/USDT
- ETH/USDT
- SOL/USDT
- XRP/USDT
- DOGE/USDT

## 安装

```bash
pip install ccxt requests python-dotenv
```

## 配置

编辑 `monitor.py` 中的 `Config` 类：

```python
class Config:
    # 设置飞书Webhook
    FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
    
    # 或设置Telegram
    TELEGRAM_BOT_TOKEN = "your_bot_token"
    TELEGRAM_CHAT_ID = "your_chat_id"
    
    # 最小价差阈值 (%)
    MIN_SPREAD_PERCENT = 0.5
```

## 运行

```bash
python monitor.py
```

## 风险提示

- 价差可能在执行过程中消失
- 需要两个交易所都有资金
- 提币/转账需要时间
- 本工具仅供监控参考，不构成投资建议
