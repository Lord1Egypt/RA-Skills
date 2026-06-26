# 云梦A股数据获取Skill

## 功能介绍

这是一个用于OpenClaw框架的A股市场数据获取技能，可以获取以下数据：

1. **个股资金流向** - 获取指定股票的资金流向数据
2. **个股新闻** - 查询指定股票的最新新闻
3. **个股筹码分布** - 获取指定股票的筹码分布数据
4. **当天龙虎榜** - 获取当日龙虎榜数据
5. **当日涨停板行情** - 获取当日涨停板股票数据
6. **昨日涨停板股池** - 获取昨日涨停板股票数据
7. **盘口异动** - 获取盘口异动数据
8. **板块异动** - 获取板块异动数据
9. **单只股票详细信息** - 获取股票的详细信息，包括换手率、成交量、盘口情况、均线情况和上升通道判断

## 安装方法

```bash
pip install -e .
```

## 依赖项

- pandas
- requests
- beautifulsoup4

## 使用方法

### 基本用法

```python
from clouddream_quant import (
    get_stock_fund_flow,
    get_stock_news,
    get_stock_chip_distribution,
    get_dragon_tiger_list,
    get_limit_up_stocks,
    get_yesterday_limit_up_stocks,
    get_market_anomalies,
    get_sector_anomalies,
    get_stock_details,
    run_all
)

# 获取个股资金流向
result = get_stock_fund_flow("000001")
print(result)

# 获取单只股票详细信息
result = get_stock_details("000001")
print(result)

# 运行所有数据获取方法
result = run_all()
print(result)
```

### 返回格式

所有方法都返回标准的OpenClaw格式：

```json
{
  "success": true,
  "data": [...],
  "message": ""
}
```

## 注意事项

1. 本技能使用东方财富和新浪财经的API获取数据，请确保网络连接正常
2. 由于API访问限制，可能会出现请求失败的情况，技能已内置重试机制
3. 数据获取速度可能会受到网络状况和API限制的影响
4. 当网络连接恢复后，技能将能够正常获取真实的A股市场数据

## 版本信息

- 版本：1.0.0
- 作者：云梦
- 描述：获取A股市场各类数据，包括行情、资金流向、龙虎榜等
