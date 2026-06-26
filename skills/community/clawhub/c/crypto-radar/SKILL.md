---
name: crypto-radar
description: 数字货币行情监控工具。当用户询问「比特币」「以太坊」「BTC」「ETH」「数字货币行情」「加密货币」「Crypto」「比特币价格」「以太坊价格」时使用。使用 Yahoo Finance（实时价格）和 CoinGecko（市值/交易量）双数据源。📢微信公众号：PM熊叔（打造一人公司的投研团队）
---

# 数字货币雷达 (Crypto Radar)

## 覆盖品种

| 币种 | 代码 | 类型 |
|------|------|------|
| 比特币 | BTC | 加密货币之王 |
| 以太坊 | ETH | 智能合约平台 |
| Solana | SOL | 高性能公链 |
| 币安币 | BNB | 交易所平台币 |
| XRP | XRP | Ripple 跨境支付 |
| 狗狗币 | DOGE | Meme 币 |
| 艾达币 | ADA | 卡尔达诺 |

## 数据获取

### Yahoo Finance（实时价格）

```python
import requests

def get_crypto_price(symbol):
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}-USD?interval=1d&range=1d"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    meta = r.json()["chart"]["result"][0]["meta"]
    price = meta["regularMarketPrice"]
    prev = meta["chartPreviousClose"]
    chg = price - prev
    pct = chg / prev * 100
    return {"price": price, "chg": chg, "pct": pct}
```

### CoinGecko（市值 + 24h 交易量）

```python
import requests

def get_crypto_markets():
    ids = "bitcoin,ethereum,solana,binancecoin,ripple,cardano,dogecoin"
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids}&order=market_cap_desc&per_page=10&sparkline=false&price_change_percentage=24h"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    return r.json()
    # 返回: price, market_cap, total_volume, price_change_percentage_24h
```

## 情报解读框架

| 指标 | 信号 |
|------|------|
| BTC 市占率 > 55% | 避险情绪，主流资金抱团 |
| BTC 市占率 < 45% | Alt Season（山寨季）|
| ETH/BTC 比值 < 0.030 | ETH 相对 BTC 弱势 |
| ETH/BTC 比值 > 0.050 | ETH 强势，可能有 Alt Season |
| 山寨币涨幅 > BTC 3倍 | 资金外溢，风险偏好上升 |
| 全市场市值 vs BTC | 判断整体趋势方向 |

**关键比值：**
- ETH/BTC ratio：以太坊相对比特币强弱
- BTC Dominance：比特币市值占全市场比例
- 山寨季指数：全市场 vs BTC 的涨跌对比

**分析顺序：**
1. BTC 价格 + 市占率（方向）
2. ETH 价格 + ETH/BTC 比值（Alt 风向标）
3. 主流山寨（SOL/XRP/DOGE）— 情绪扩散
4. 全市场市值变化（判断趋势是否延续）

## 快速查询命令

```bash
cd C:\Users\gold3\.openclaw\workspace\skills\crypto-radar\scripts

# 查询全部加密货币行情
python crypto_spot.py
```
