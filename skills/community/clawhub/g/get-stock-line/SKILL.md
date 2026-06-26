# stock-kline Skill

获取A股股票和指数历史K线数据。**支持自动切换数据源，默认使用前复权数据**。

---

## 快速开始

```python
from skills.stock_kline.kline import get_stock_history, get_today_change

# 获取股票K线 (前复权，自动切换数据源)
data = get_stock_history("600519.SH", days=100)

# 获取当天涨跌幅
result = get_today_change("600519.SH")
# 返回: {open, close, high, low, change, change_pct, volume}
```

---

## 数据源 (自动切换)

| 优先级 | 数据源 | 复权支持 | 说明 |
|--------|--------|----------|------|
| 1️⃣ | **AKShare** | ✅ 前复权/后复权 | 首选，数据准确 |
| 2️⃣ | **新浪财经API** | ❌ 不支持 | 降级备用，仅未复权 |

### 自动切换逻辑

```
get_stock_history(code, adjust="qfq")
    │
    ├─→ AKShare (前复权) ✅
    │       成功 → 返回复权数据
    │       失败 → 继续
    │
    └─→ 新浪API (未复权) ⚠️
            成功 → 返回未复权数据
            失败 → 返回空列表
```

**⚠️ 重要**: 新浪API不支持复权，除权日会有跳空。**强烈建议安装AKShare**。

---

## 安装依赖

```bash
pip install akshare pandas
```

---

## 核心功能

### 1. 获取股票K线

```python
from skills.stock_kline.kline import get_stock_history

# 前复权数据 (默认，解决除权问题)
data = get_stock_history("600519.SH", days=100)

# 后复权
data = get_stock_history("600519.SH", days=100, adjust="hfq")

# 不复权 (原始价格)
data = get_stock_history("600519.SH", days=100, adjust="")
```

### 2. 获取当天涨跌幅

```python
from skills.stock_kline.kline import get_today_change

result = get_today_change("600519.SH")
# 返回:
# {
#     "open": 1440.0,      # 开盘价
#     "close": 1453.1,     # 当前价格
#     "high": 1460.0,      # 最高
#     "low": 1430.0,       # 最低
#     "change": 13.1,      # 涨跌额
#     "change_pct": 0.91,  # 涨跌幅%
#     "volume": 1000000    # 成交量
# }
```

### 3. 计算准确涨跌幅

```python
from skills.stock_kline.kline import get_accurate_change

# 计算2026-03-13相比2026-03-12的涨幅
result = get_accurate_change("600519.SH", "2026-03-13", "2026-03-12")
# 返回: {target_price: 1413.64, prev_price: 1392.0, change_pct: 1.55}
```

### 4. 指数数据

```python
from skills.stock_kline.kline import get_index_history

# 上证指数
data = get_index_history("000001.SH", 100)

# 深证成指
data = get_index_history("399001.SZ")

# 创业板指
data = get_index_history("399006.SZ")

# 沪深300
data = get_index_history("000300.SH")
```

---

## 股票/指数代码

| 类型 | 格式 | 示例 |
|------|------|------|
| 上证股票 | 600519.SH | 贵州茅台 |
| 深证股票 | 300750.SZ | 宁德时代 |
| 创业板 | 300001.SZ | 创业板股票 |
| 上证指数 | 000001.SH | 上证指数 |
| 深证指数 | 399001.SZ | 深证成指 |

---

## 复权说明

### 什么是复权？

股票除权除息后，股价会下跌。如果不复权 Historical 价格会出现跳空。

| 复权类型 | 说明 | 适用场景 |
|----------|------|----------|
| **前复权 (qfq)** | 历史价格按最新价格调整 | ✅ **推荐用于计算涨幅** |
| 后复权 (hfq) | 最新价格按历史价格调整 | 长期持有收益计算 |
| 不复权 | 原始价格 | 不推荐，有跳空 |

**⚠️ 使用前复权数据计算涨幅可以消除除权除息导致的跳空，得到真实收益率。**

---

## 函数列表

| 函数 | 说明 | 返回格式 |
|------|------|----------|
| `get_stock_history(code, days, adjust)` | 获取股票K线 | List[Dict] |
| `get_today_change(code)` | 获取当天涨跌幅 | Dict |
| `get_accurate_change(code, date1, date2, adjust)` | 计算两日间涨幅 | Dict |
| `get_index_history(code, days)` | 获取指数K线 | List[Dict] |
| `calc_change_rate(old, new)` | 计算涨跌幅% | Float |
| `build_price_map(kline_data)` | 构建价格映射 | Dict |

---

## 完整示例

```python
from skills.stock_kline.kline import (
    get_stock_history,
    get_today_change,
    get_accurate_change,
    calc_change_rate
)

# 示例：贵州茅台

# 1. 获取实时行情
quote = get_today_change("600519.SH")
print(f"当前价格: {quote['close']}, 涨跌幅: {quote['change_pct']}%")

# 2. 获取历史K线 (前复权)
kline = get_stock_history("600519.SH", days=20)
print(f"最近20天数据: {len(kline)}条")

# 3. 计算指定日期涨幅
result = get_accurate_change("600519.SH", "2026-03-13", "2026-03-12")
print(f"涨幅: {result['change_pct']}%")

# 4. 手动计算涨幅
if len(kline) >= 2:
    today = float(kline[0]['close'])
    yesterday = float(kline[1]['close'])
    change = calc_change_rate(yesterday, today)
    print(f"今日涨幅: {change}%")
```
