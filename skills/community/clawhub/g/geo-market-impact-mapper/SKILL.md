# geo-market-impact-mapper

市场影响映射技能。负责获取和分析原油、黄金等大宗商品价格数据，为地缘事件提供市场联动分析。

## 功能

- **实时价格获取**: 通过 Yahoo Finance API 获取原油 (CL=F)、黄金 (GC=F) 期货价格
- **涨跌幅计算**: 计算日内涨跌幅百分比
- **双阈值检测**: 
  - 高优先级：原油±3%、黄金±2%
  - 观察池：原油±1.2%、黄金±0.8%
- **15 分钟脉冲**: 检测短期价格异动
- **市场联动分析**: 将商品价格波动与地缘事件关联

## 数据源

| 商品 | 代码 | 说明 |
|:---|:---|:---|
| 原油 | `CL=F` | WTI 原油期货 |
| 黄金 | `GC=F` | 黄金期货 |

## 阈值配置

```python
# 高优先级阈值
OIL_HIGH_THRESHOLD = 3.0    # 原油 ±3%
GOLD_HIGH_THRESHOLD = 2.0   # 黄金 ±2%

# 观察池阈值
OIL_WATCH_THRESHOLD = 1.2   # 原油 ±1.2%
GOLD_WATCH_THRESHOLD = 0.8  # 黄金 ±0.8%
```

## 使用方法

### Python API

```python
from geo_market_impact_mapper import (
    get_market_data,
    MarketImpact,
    is_high_priority,
    is_watch_level,
)

# 获取市场数据
market = get_market_data()
print(f"原油：{market.oil_pct:+.2f}%")
print(f"黄金：{market.gold_pct:+.2f}%")

# 检查是否达到高优先级
if market.is_high_priority():
    print("⚠️ 市场异动达到高优先级阈值")

# 检查是否达到观察池
if market.is_watch_level():
    print("👁️ 市场异动进入观察范围")

# 生成市场影响描述
description = market.get_impact_description()
# → "原油大涨 2.5%，利多石油石化板块，利空航空运输"
```

### MarketImpact 数据结构

```python
@dataclass
class MarketImpact:
    oil_pct: float = 0.0      # 原油涨跌幅
    gold_pct: float = 0.0     # 黄金涨跌幅
    oil_pulse: float = 0.0    # 15 分钟脉冲
    gold_pulse: float = 0.0   # 15 分钟脉冲
```

## 影响路径映射

| 事件类型 | 影响路径 | 受益板块 | 受损板块 |
|:---|:---|:---|:---|
| 地缘冲突 | 原油供应扰动 → 油价上涨 | 石油石化、油运 | 航空、物流 |
| 避险升温 | 黄金需求增加 → 金价上涨 | 有色金属（黄金） | - |
| 央行加息 | 美元走强 → 商品承压 | 银行 | 成长股、有色 |

## 依赖

- `requests`: HTTP 请求库
- Yahoo Finance API (免费，无需 API Key)

## 相关文件

- 主模块：`geo_market_impact_mapper.py`

## 版本

- **v1.0.0**: 初始版本，从 smart-geo-push.py v2.0 拆分
