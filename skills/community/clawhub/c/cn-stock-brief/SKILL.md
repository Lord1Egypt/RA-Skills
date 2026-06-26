---
slug: cn-stock-brief
name: A股每日简报
version: "1.0.0"
author: 千策
---

# CN Stock Brief - A股每日简报

A股市场每日简报生成器，基于东方财富免费公开数据。

## 功能

- 📈 大盘指数：上证、深证、创业板、科创50
- 🏭 板块涨跌：TOP20 行业板块涨跌幅
- 🚀 涨幅榜：A股涨幅TOP10
- 📉 跌幅榜：A股跌幅TOP10
- 📊 多种输出格式：文本简报 / JSON

## 使用

### 每日简报（默认）
```bash
python3 ~/.qclaw/skills/cn-stock-brief/scripts/stock_brief.py
```

### JSON 格式（供程序处理）
```bash
python3 ~/.qclaw/skills/cn-stock-brief/scripts/stock_brief.py --json
```

### 仅指数数据
```bash
python3 ~/.qclaw/skills/cn-stock-brief/scripts/stock_brief.py --indices
```

### 仅板块数据
```bash
python3 ~/.qclaw/skills/cn-stock-brief/scripts/stock_brief.py --sectors
```

## 数据源

- 东方财富开放API（无需API Key，免费）
- 沪深A股实时行情
- 行业板块分类

## 依赖

- Python 3（系统自带）
- 无第三方依赖

## 注意

- ⚠️ 数据仅供参考，不构成投资建议
- 交易日才有实时数据，非交易日显示上一交易日数据

## 示例输出

```
📊 A股每日简报 | 2026-04-14 周二
========================================

📈 大盘指数
  🟢 上证指数: 3285.50 (+1.23%)
  🔴 深证成指: 10234.60 (-0.45%)
  🟢 创业板指: 2034.80 (+0.67%)
  🟢 科创50: 987.20 (+1.05%)

🏭 板块涨跌 TOP10
  1. 半导体: +3.25%
  2. 新能源: +2.18%
  ...

🚀 涨幅榜 TOP10
  1. 中芯国际(688981): 85.60 +10.02%
  ...

📉 跌幅榜 TOP10
  1. 某某股份(000001): 5.20 -8.50%
  ...

========================================
数据来源：东方财富 | 仅供参考，不构成投资建议
```

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
