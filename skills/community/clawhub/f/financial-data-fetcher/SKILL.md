---
name: financial-data-fetcher
description: 一个基于通达信 TQ 策略接口的金融数据获取工具，提供多种API脚本用于获取股票行情、财务数据、板块信息等。
---

# TongdaXin Financial Data Fetcher

## Description

一个基于通达信 TQ 策略接口的金融数据获取工具，提供多种API脚本用于获取股票行情、财务数据、板块信息等。

## Triggers

当用户请求获取金融数据时自动触发，例如：
- "获取K线数据"
- "查询股票快照"
- "获取专业财务数据"
- "获取板块交易数据"
- "查询新股申购信息"
- 任何与股票行情、财务数据、市场信息相关的请求

## Commands

### 行情数据

```
/get_market_data --stock_list 688318.SH --period 1d --count 1
```
获取K线行情数据

```
/get_market_snapshot --stock_code 688318.SH
```
获取快照数据

```
/get_stock_info --stock_code 688318.SH --field_list Name Unit
```
获取证券基本信息

```
/get_more_info --stock_code 688318.SH
```
获取股票更多信息

```
/get_trading_dates --market SH --count 10
```
获取交易日列表

### 财务数据

```
/get_financial_data --stock_list 688318.SH --field_list FN193 FN194
```
获取专业财务数据

```
/get_financial_data_by_date --stock_list 688318.SH --field_list FN193 --year 2025
```
获取指定日期专业财务数据

```
/get_gpjy_value --stock_list 688318.SH --field_list GP1 GP2
```
获取股票交易数据

```
/get_gpjy_value_by_date --stock_list 688318.SH --field_list GP1 --year 2025
```
获取指定日期股票交易数据

```
/get_gp_one_data --stock_list 688318.SH --field_list GO1 GO2
```
获取股票的单个财务数据

### 板块数据

```
/get_stock_list --market 16
```
获取系统分类成份股

```
/get_sector_list
```
获取A股板块代码列表

```
/get_stock_list_in_sector --block_code 880081.SH
```
获取板块成份股

```
/get_bkjy_value --stock_list 880660.SH --field_list BK5 BK6
```
获取板块交易数据

```
/get_bkjy_value_by_date --stock_list 880660.SH --field_list BK9 --year 2025
```
获取指定日期板块交易数据

### 市场数据

```
/get_scjy_value --field_list SC1 SC2
```
获取市场交易数据

```
/get_scjy_value_by_date --field_list SC6 SC7 --year 2025
```
获取指定日期市场交易数据

### 新股与分红

```
/get_ipo_info --ipo_type 2 --ipo_date 1
```
获取新股申购信息

```
/get_divid_factors --stock_code 688318.SH
```
获取分红配送数据

```
/get_gb_info --stock_code 688318.SH --date_list 20250101 20250601 --count 2
```
获取股本数据

### 自定义板块

```
/get_user_sector
```
获取自定义板块列表

```
/create_sector --block_code TEST --block_name 测试板块
```
创建自定义板块

```
/delete_sector --block_code TEST
```
删除自定义板块

```
/rename_sector --block_code TEST --block_name 新名称
```
重命名自定义板块

```
/send_user_block --block_code TEST --stocks 600000.SH 600004.SH
```
添加自定义板块成份股

```
/clear_sector --block_code TEST
```
清空自定义板块成份股

### ETF与可转债

```
/get_trackzs_etf_info --zs_code 950162.CSI
```
获取跟踪指数的ETF信息

```
/get_cb_info --stock_code 123039.SZ
```
获取可转债基础信息

### 行情订阅

```
/subscribe_hq --stock_list 688318.SH
```
订阅行情

```
/unsubscribe_hq --stock_list 688318.SH
```
取消订阅更新

```
/get_subscribe_hq_stock_list
```
获取订阅列表

### 数据刷新

```
/refresh_cache --market AG --force
```
刷新行情缓存

```
/refresh_kline --stock_list 688318.SH --period 1d
```
刷新历史K线缓存

### 数据下载

```
/download_file --stock_code 688318.SH --down_time 20241231 --down_type 1
```
下载特定数据文件

## Prerequisites

使用本工具前需要满足以下条件：

### 1. 安装 Python 依赖包

```bash
pip install numpy pandas
```

### 2. 安装通达信金融终端TQ版

- 需要安装 **通达信金融终端TQ版** 并确保其正常运行
- 本工具依赖 TQ 策略接口与通达信客户端进行数据交互
- 确保 TQ 策略功能已启用

## Usage

运行脚本前需要设置 PYTHONPATH：

```bash
# Unix/Linux/Mac
export PYTHONPATH=/path/to/project

# Windows (CMD)
set PYTHONPATH=C:\path\to\project

# Windows (PowerShell)
$env:PYTHONPATH = "C:\path\to\project"

# 运行脚本
python scripts/get_market_data.py --stock_list 688318.SH --period 1d
```

或者使用 -m 方式运行：

```bash
cd /path/to/project
python -m scripts.get_market_data --stock_list 688318.SH --period 1d
```

## Enum Values

### period (周期)
- `1m` - 1分钟
- `5m` - 5分钟
- `15m` - 15分钟
- `30m` - 30分钟
- `1h` - 60分钟(1小时)
- `1d` - 1天
- `1w` - 1周
- `1mon` - 1月
- `1q` - 1季
- `1y` - 1年
- `tick` - 分笔

### dividend_type (复权类型)
- `none` - 不复权
- `front` - 前复权
- `back` - 后复权

### market (市场)
- `AG` - A股
- `HK` - 港股
- `US` - 美股
- `QH` - 国内期货
- `QQ` - 股票期权
- `NQ` - 新三板
- `ZZ` - 中证和国证指数
- `ZS` - 沪深京指数

### ipo_type
- `0` - 新股申购信息
- `1` - 新发债信息
- `2` - 新股和新发债信息

### ipo_date
- `0` - 只获取今天信息
- `1` - 获取今天及以后信息