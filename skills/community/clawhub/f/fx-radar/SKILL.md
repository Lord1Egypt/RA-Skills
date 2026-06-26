---
name: fx-radar
description: 全球汇率监控工具。当用户询问「美元汇率」「人民币汇率」「港币汇率」「日元汇率」「欧元汇率」「英镑汇率」「美元兑人民币」「USD/CNY」「汇率」「外汇」「离岸人民币」「在岸人民币」「换汇」时使用。使用 Yahoo Finance 获取实时汇率数据。📢微信公众号：PM熊叔（打造一人公司的投研团队）
---

# 汇率雷达 (FX Radar)

## 覆盖品种

| 货币对 | Yahoo代码 | 说明 |
|--------|-----------|------|
| 美元/人民币 | USDCNY=X | USD/CNY |
| 美元/港元 | USDHKD=X | USD/HKD |
| 离岸人民币/港元 | CNHHKD=X | CNH/HKD |
| 美元/日元 | USDJPY=X | USD/JPY |
| 美元/瑞郎 | USDCHF=X | USD/CHF |
| 美元/加元 | USDCAD=X | USD/CAD |
| 欧元/美元 | EURUSD=X | EUR/USD |
| 英镑/美元 | GBPUSD=X | GBP/USD |
| 澳元/美元 | AUDUSD=X | AUD/USD |
| 纽元/美元 | NZDUSD=X | NZD/USD |
| 美元/离岸人民币 | USDCNH=X | USD/CNH |

## 数据获取

```python
import requests

FOREX_SYMBOLS = {
    "USDCNY=X": "USD/CNY 美元/在岸人民币",
    "USDHKD=X": "USD/HKD 美元/港元",
    "USDJPY=X": "USD/JPY 美元/日元",
    "EURUSD=X": "EUR/USD 欧元/美元",
    "GBPUSD=X": "GBP/USD 英镑/美元",
    "USDCHF=X": "USD/CHF 美元/瑞郎",
    "AUDUSD=X": "AUD/USD 澳元/美元",
    "NZDUSD=X": "NZD/USD 纽元/美元",
    "USDCNH=X": "USD/CNH 美元/离岸人民币",
}

def get_forex():
    results = {}
    for sym, name in FOREX_SYMBOLS.items():
        try:
            url = f"https://query2.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1d"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            meta = r.json()["chart"]["result"][0]["meta"]
            price = meta["regularMarketPrice"]
            prev = meta["chartPreviousClose"]
            pct = (price - prev) / prev * 100
            results[sym] = {"name": name, "price": price, "chg": price-prev, "pct": pct}
        except Exception:
            pass
    return results
```

## 情报解读框架

| 货币对 | 关键阈值 | 信号 |
|--------|----------|------|
| USD/CNY | > 7.30 | 人民币贬值压力 |
| USD/CNY | < 7.10 | 人民币偏强 |
| USD/JPY | > 150 | 日本干预风险 |
| USD/JPY | < 145 | 日本央行容忍区间 |
| EUR/USD | > 1.10 | 欧元强势 |
| EUR/USD | < 1.05 | 欧元弱势 |
| USD/CNH vs USD/CNY | CNH大幅强于CNY | 资本管制收紧信号 |

**分析顺序：**
1. 美元指数（DXY）方向 — 全球货币锚
2. USD/CNY — 人民币核心价格
3. USD/HKD — 港币联系汇率稳定
4. USD/JPY — 日本央行政策信号
5. EUR/GBP/AUD — 发达市场货币对比
6. USD/CNH vs CNY利差 — 资本流动信号

## 快速查询命令

```bash
cd C:\Users\gold3\.openclaw\workspace\skills\fx-radar\scripts

# 查询全部汇率
python fx_spot.py
```
