---
name: a-stock-analysis
description: A股和港股股票数据分析工具，优先使用Tushare数据，Tushare不可用时自动回退到AKShare获取行情、财务指标，支持基本面分析和技术分析。
---

# A股港股股票分析

基于Tushare + AKShare双数据源的A股和港股股票基本面、技术面分析。

- **优先使用Tushare**：如果配置了Tushare Token且能正常访问，用Tushare数据
- **自动回退AKShare**：Tushare不可用、没Token或请求失败时自动切AKShare公开数据源

## 前置准备

1. **推荐配置Tushare**：访问 https://tushare.pro/ 注册并获取Token，设置环境变量 `TUSHARE_TOKEN=你的token`
2. **AKShare不需要Token**：直接可用，不需要注册

## 功能

- 获取个股基本信息
- 获取历史行情数据
- 财务指标分析（Tushare优先）
- 技术指标计算（MA、MACD、RSI等）
- 支持A股（沪/深/北）和港股

## 使用

### 安装依赖

```bash
# 需要Python 3和tushare库
pip install tushare pandas numpy
```

### 获取股票基本信息

`scripts/get_basic.py --code <股票代码>`

股票代码规则：
- A股：直接使用6位代码 (e.g., 000001 平安银行)
- 港股：使用5位代码 (e.g., 00700 腾讯控股)

### 获取历史行情

`scripts/get_historical.py --code <股票代码> --start <YYYYMMDD> --end <YYYYMMDD>`

### 基本面分析

`scripts/fundamental_analysis.py --code <股票代码>`

## 参考

- [Tushare API文档](references/tushare-api.md) - 常用API说明
