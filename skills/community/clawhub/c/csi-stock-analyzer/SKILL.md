---
name: csi-stock-analyzer
description: |
  专业A股投资分析工具，支持实时行情获取、技术指标分析（MACD/KDJ/RSI/EMA）、
  智能数据缓存、新闻舆情分析。适用于中证2000成分股及全市场股票分析。
  
  使用场景：
  1. 需要分析某只股票的买入/卖出时机
  2. 需要获取股票的技术指标信号（金叉/死叉/超买/超卖）
  3. 需要批量分析中证2000成分股
  4. 需要监控股票的舆情和消息面
  5. 需要缓存股票历史数据避免重复获取
---

# CSI 股票分析器

专业A股投资分析工具，提供实时行情、技术分析、智能缓存和舆情监控。

## 核心功能

- **实时行情获取**: 全A股实时数据
- **技术分析**: MACD、KDJ、RSI、EMA四大指标
- **智能缓存**: SQLite本地缓存，增量更新
- **交易信号**: 自动识别金叉/死叉/超买/超卖
- **舆情分析**: 新闻监控和情感分析

## 快速开始

```python
from core.stock_analyzer import AdvancedStockAnalyzer

analyzer = AdvancedStockAnalyzer()
result = analyzer.comprehensive_analysis('000977', days=120)

print(f"评级: {result['recommendation']['overall']}")
print(f"建议: {result['recommendation']['action']}")
```

## 技术指标说明

### MACD
- **金叉买入**: DIF上穿DEA，MACD柱由负转正
- **死叉卖出**: DIF下穿DEA，MACD柱由正转负

### KDJ
- **超卖买入**: J值<0且回升，或K线上穿D线
- **超买卖出**: J值>100且回落，或K线下穿D线

### RSI
- **超卖买入**: RSI<30且回升
- **超买卖出**: RSI>70且回落

### EMA
- **多头排列**: 价格>EMA20>EMA60
- **空头排列**: 价格<EMA20<EMA60

## 项目结构

```
csi2000_analyzer/
├── core/
│   ├── data_fetcher.py
│   ├── data_cache.py
│   ├── stock_analyzer.py
│   ├── news_analyzer.py
│   └── database.py
├── data/cache/
├── config.yaml
└── main.py
```

## 免责声明

本工具提供的所有数据和分析结果仅供参考，不构成任何投资建议。投资者应独立判断，自负盈亏。