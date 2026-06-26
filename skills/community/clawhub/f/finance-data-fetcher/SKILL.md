# Finance Data Fetcher - 金融数据获取工具

## 功能说明

使用 AkShare 获取中国 A 股市场各类金融数据，包括实时行情、历史数据、财务数据和资金流向等。

## 核心功能

### 实时行情
- 实时股票报价
- 分时行情
- 分笔成交

### 历史数据
- 日 K 线数据
- 周 K 线数据
- 月 K 线数据
- 复权数据

### 财务数据
- 三大报表（资产负债表、利润表、现金流量表）
- 估值指标（PE、PB、PS）
- 盈利能力指标（ROE、ROA）
- 偿债能力指标

### 资金流向
- 主力资金流向
- 北向资金数据
- 机构持股数据

### 基本面指标
- 市盈率、市净率
- 每股收益
- 股息率
- 总市值、流通市值

## 使用示例

```python
from skill_main import fetch_stock_quote, fetch_financial_data, fetch_capital_flow, fetch_fundamental_indicators

# 获取实时报价
quote = fetch_stock_quote(stock_code="300308")

# 获取财务数据
financial = fetch_financial_data(stock_code="300308", report_type="利润表")

# 获取资金流向
capital = fetch_capital_flow(stock_code="300308")

# 获取基本面指标
indicators = fetch_fundamental_indicators(stock_code="300308")
```

## 安装依赖

```bash
pip install akshare pandas numpy requests
```

## 数据源

- AkShare (主要数据源)
- 新浪财经 API
- 东方财富 API

## 注意事项

- 实时行情有 15 分钟延迟
- 某些财务数据有季度延迟
- 建议添加缓存机制避免重复请求
- API 有频率限制，建议控制请求频率

## 导出函数

| 函数 | 说明 |
|------|------|
| `fetch_stock_quote` | 获取实时股票报价 |
| `fetch_financial_data` | 获取财务报表数据 |
| `fetch_capital_flow` | 获取资金流向数据 |
| `fetch_fundamental_indicators` | 获取基本面指标 |

## 目标代理

- AIData
- AIFundamentals
- AITechnicals