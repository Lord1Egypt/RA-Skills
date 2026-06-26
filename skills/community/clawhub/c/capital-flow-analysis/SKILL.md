# Capital Flow Analysis - 资金流向分析

## 功能说明

分析股票资金流向，包括主力资金、北向资金、龙虎榜数据。

## 核心功能

### 主力资金
- 主力净流入/流出
- 大单/中单/小单分布
- 主力建仓/出货识别

### 北向资金
- 沪股通/深股通持股
- 外资持仓变化
- 北向资金偏好分析

### 龙虎榜
- 上榜股票分析
- 机构席位买卖
- 游资动向追踪

## 使用示例

```python
from capital_flow import analyze_main_force, analyze_northbound

# 主力资金分析
main_force = analyze_main_force(stock_code="300308")

# 北向资金分析
northbound = analyze_northbound(stock_code="300308")
```

## 数据源

- 东方财富资金流向
- 沪深港通数据
- 交易所龙虎榜
