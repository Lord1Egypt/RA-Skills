---
name: futures-radar
description: 期货与大宗商品行情监控工具。当用户询问「原油」「黄金」「白银」「天然气」「铜」「期货行情」「大宗商品」「WTI」「布伦特」「金银比」「油金比」时使用。使用 Yahoo Finance chart API 获取实时期货数据。📢微信公众号：PM熊叔（打造一人公司的投研团队）
---

# 期货雷达 (Futures Radar)

## 覆盖品种

| 类别 | 品种 | 代码 | 单位 |
|------|------|------|------|
| **能源** | WTI原油 | CL=F | 桶 |
| | 布伦特原油 | BZ=F | 桶 |
| | 天然气 | NG=F | 百万英热 |
| **贵金属** | 黄金 | GC=F | 盎司 |
| | 白银 | SI=F | 盎司 |
| | 铂金 | PL=F | 盎司 |
| | 钯金 | PA=F | 盎司 |
| **基本金属** | 铜 | HG=F | 磅 |
| **农产品** | 玉米 | ZC=F | 蒲式耳 |
| | 大豆 | ZS=F | 蒲式耳 |
| | 小麦 | ZW=F | 蒲式耳 |
| **国债期货** | 10年国债 | ZN=F | 面值100 |
| | 30年国债 | ZB=F | 面值100 |

## 数据获取

```python
import requests

def get_quote(symbol):
    """获取期货行情（Yahoo Finance chart API）"""
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    meta = r.json()["chart"]["result"][0]["meta"]
    price = meta["regularMarketPrice"]
    prev = meta["chartPreviousClose"]
    chg = price - prev
    pct = chg / prev * 100
    return {"price": price, "chg": chg, "pct": pct,
            "high": meta["regularMarketDayHigh"],
            "low": meta["regularMarketDayLow"]}
```

## 关键比价与信号

| 比价 | 公式 | 含义 |
|------|------|------|
| 金银比 | GC/F ÷ SI/F | >80 银相对便宜（均值），<50 金便宜 |
| 油金比 | CL/F ÷ (GC/F÷100) | >2.5 通胀预期强，<1.5 避险情绪 |
| 金铜比 | GC/F ÷ HG/F | 经济预期（金强→衰退/避险，铜强→复苏） |

## 情报解读框架

| 品种 | 关键信号 |
|------|----------|
| WTI原油 > 100 | 地缘风险/供应紧张，通胀压力 |
| 黄金 > 2000 | 避险情绪浓厚 |
| 白银 < 22 | 工业需求疲软 |
| 天然气 > 4 | 能源危机/冬季需求 |
| 10年国债期货 > 114 | 降息预期增强（债券涨） |
| 10年国债期货 < 110 | 利率上升预期（债券跌） |
| 钯金 > 2000 | 汽车行业需求强（芯片/电动车替代中） |

**分析顺序：**
1. 黄金 + 白银（避险/通胀主线）
2. WTI + 布伦特（地缘/供给）
3. 金银比（相对价值）
4. 国债期货（利率预期→影响所有资产）
5. 天然气 + 铜（实体经济需求）

## 快速查询命令

```bash
cd C:\Users\gold3\.openclaw\workspace\skills\futures-radar\scripts

# 查询全部期货品种
python futures_spot.py
```
