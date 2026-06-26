# A股数据获取技能包

## 功能介绍

这是一个用于OpenClaw框架的A股市场数据获取技能包，可以获取以下数据：

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

### 方法一：直接安装

```bash
pip install -e .
```

### 方法二：创建wheel包安装

```bash
python setup.py bdist_wheel
pip install dist/a_share_data_skill-1.0.0-py3-none-any.whl
```

## 使用方法

### 作为命令行工具使用

```bash
a_share_data
```

### 作为Python模块使用

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
data = get_stock_fund_flow("000001")
print(data)

# 获取单只股票详细信息
details = get_stock_details("000001")
print(details)

# 运行所有数据获取方法
results = run_all()
```

## 数据保存

所有获取的数据会保存到 `results` 目录下的CSV文件中，文件命名格式为：

- 龙虎榜：`dragon_tiger_YYYYMMDD.csv`
- 涨停板：`limit_up_YYYYMMDD.csv`
- 昨日涨停板：`yesterday_limit_up_YYYYMMDD.csv`
- 盘口异动：`market_anomalies_YYYYMMDD.csv`
- 板块异动：`sector_anomalies_YYYYMMDD.csv`

## 注意事项

1. 本技能包使用东方财富和新浪财经的API获取数据，请确保网络连接正常
2. 由于API访问限制，可能会出现请求失败的情况，技能包已内置重试机制
3. 数据获取速度可能会受到网络状况和API限制的影响

## 依赖项

- pandas
- requests
- beautifulsoup4
