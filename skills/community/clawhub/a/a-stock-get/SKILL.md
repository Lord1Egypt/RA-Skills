---
name: a-stock-get
description: Specialized A-share stock data collector. Automatically fetch and store daily/weekly/monthly historical K-line data for all A-share stocks in SQLite database.
---

# A-Share-Get / A股数据获取工具

**English** | **中文**

---

## Overview / 概述

**English:**  
A specialized data collection tool for Chinese A-share market. Automatically fetches and stores stock list, daily, weekly, and monthly historical K-line data into a local SQLite database. Designed specifically for quantitative analysts who need a complete local copy of A-share market data.

**中文:**  
专门针对中国A股市场的数据获取工具。自动采集并存储股票列表、日线、周线、月线历史K线数据到本地SQLite数据库。专为需要完整A股本地数据副本的量化分析师设计。

---

## Features / 功能特性

**English:**  
- **Automated Stock List Management**: Fetches and updates all tradable stocks from A-share markets (60* Shanghai, 30* ChiNext, 00* Shenzhen)
- **Multi-Frequency Data Collection**: Supports parallel fetching for daily, weekly, and monthly K-line data
- **SQLite Database Storage**: Local persistent storage, easy to query for quantitative analysis
- **Automatic Filtering**: Excludes delisted and pre-IPO stocks automatically
- **Data Integrity**: Tracks last fetch timestamp for each frequency, supports incremental updates
- **Multiple Data Sources**: EastMoney/Sina/Tencent with automatic failover

**中文:**  
- **自动化股票列表管理**: 获取并更新A股市场全部可交易股票（沪市60*、创业板30*、深市00*）
- **多频率数据采集**: 支持并行获取日线、周线、月线K线数据
- **SQLite数据库存储**: 本地持久化存储，便于量化分析查询
- **自动过滤**: 自动排除退市和未上市股票
- **数据完整性**: 记录每种频率最后获取时间戳，支持增量更新
- **多数据源冗余**: 东方财富/新浪/腾讯，自动故障切换

---

## Database Schema / 数据库架构

### Stock List Table (stocks)
| Column / 字段 | Type / 类型 | Description / 说明 |
|---------------|-------------|-------------------|
| code | TEXT | Stock code (e.g., 600519) / 股票代码 |
| name | TEXT | Stock name (e.g., 贵州茅台) / 股票名称 |
| market | TEXT | Market type (60/30/00) / 市场类型 |
| day_get | TIMESTAMP | Last daily data fetch time / 最后日线数据获取时间 |
| week_get | TIMESTAMP | Last weekly data fetch time / 最后周线数据获取时间 |
| month_get | TIMESTAMP | Last monthly data fetch time / 最后月线数据获取时间 |
| status | TEXT | Stock status (active/delisted) / 股票状态 |
| created_at | TIMESTAMP | Record creation time / 记录创建时间 |

---

## Installation & Setup / 安装与设置

### Step 1: Database Initialization / 第一步：数据库初始化

**English:**  
Run the initialization script to create the database and tables:

```bash
python scripts/init_db.py
```

**中文:**  
运行初始化脚本创建数据库和表：

```bash
python scripts/init_db.py
```

### Step 2: Fetch Stock List / 第二步：获取股票列表

**English:**  
Fetch all tradable stocks from A-share markets:

```bash
python scripts/fetch_stocks.py
```

**中文:**  
从A股市场获取所有可交易股票列表：

```bash
python scripts/fetch_stocks.py
```

### Step 3: Start Data Collection / 第三步：启动数据收集

**English:**  
```bash
# Enhanced data fetching with external events
python scripts/day.py get all --limit 10
python scripts/week.py get all --limit 10
python scripts/month.py get all --limit 10

# Traditional usage (fetch all active stocks)
python scripts/day.py
python scripts/week.py
python scripts/month.py

# Database reset and fetch tool
python scripts/db_reset.py reset status
python scripts/db_reset.py fetch day 000001

# Parallel fetching for large batches
python scripts/day_parallel.py
python scripts/week_parallel.py
python scripts/month_parallel.py
```

**中文:**  
```bash
# 增强版数据获取（支持外部事件）
python scripts/day.py get all --limit 10
python scripts/week.py get all --limit 10
python scripts/month.py get all --limit 10

# 传统用法（获取所有活跃股票）
python scripts/day.py
python scripts/week.py
python scripts/month.py

# 数据库重置与获取工具
python scripts/db_reset.py reset status
python scripts/db_reset.py fetch day 000001

# 并行获取大量数据
python scripts/day_parallel.py
python scripts/week_parallel.py
python scripts/month_parallel.py
```

---

## File Structure / 文件结构

```
a-stock-get/
├── SKILL.md                  # This documentation
├── scripts/
│   ├── init_db.py               # Database initialization
│   ├── fetch_stocks.py          # Fetch stock list from API
│   ├── day.py                  # Enhanced daily data fetch with external events
│   ├── day_original.py         # Original daily data fetch (backup)
│   ├── day_parallel.py         # Parallel daily data fetch
│   ├── db_reset.py             # Database reset and fetch tool
│   ├── week.py                 # Enhanced weekly data fetch with external events
│   ├── week_original.py        # Original weekly data fetch (backup)
│   ├── week_parallel.py        # Parallel weekly data fetch
│   ├── month.py                # Enhanced monthly data fetch with external events
│   ├── month_original.py       # Original monthly data fetch (backup)
│   ├── month_parallel.py       # Parallel monthly data fetch
│   ├── data_validation.py      # Data validation and integrity check
│   ├── data_repair.py          # Data repair tool
│   ├── schedule_config.py      # OpenClaw cron job configuration
│   └── README.md               # Detailed usage documentation
├── references/
│   └── data_sources.md        # Data source documentation
└── D:\xistock\                # Data directory (external)
    └── stock.db             # SQLite database
```

---

## Data Sources / 数据来源

**English:**  
- **East Money API**: Real-time stock quotes and listing information
- **Sina Finance**: Historical data for technical analysis
- **Tencent Finance**: Alternative data source for redundancy

**中文:**  
- **东方财富API**: 实时股票行情和上市信息
- **新浪财经**: 技术分析历史数据
- **腾讯财经**: 冗余备用数据源

---

## Requirements / 依赖要求

```bash
pip install requests
pip install sqlite3
pip install pandas
pip install akshare  # Chinese stock data library
```

---

## Notes / 注意事项

**English:**  
- Database file is stored at `D:\xistock\stock.db` for data persistence
- Stock list should be updated regularly (e.g., weekly) to capture new listings and delistings
- API rate limits apply when fetching data; parallel mode improves speed
- This system is for research and educational purposes; comply with local regulations for actual trading

**中文:**  
- 数据库文件存储在 `D:\xistock\stock.db` 确保数据持久化
- 股票列表应定期更新（如每周）以捕捉新股上市和退市变化
- 获取数据受API速率限制，并行模式提升速度
- 本系统仅用于研究和教育目的；实际交易请遵守当地法规



## Todo / 待办事项

- [x] Add incremental update mode (only fetch stocks not updated today)
- [x] Add external event control to day.py, week.py, and month.py
- [x] Create database reset and fetch tool (db_reset.py)
- [x] Add data validation and integrity checks (data_validation.py)
- [x] Add data repair tool (data_repair.py)
- [x] Add OpenClaw cron job configuration (schedule_config.py)
- [ ] Integrate with OpenClaw heartbeat for scheduled automatic updates
- [ ] Add advanced analytics and reporting features

---

## References / 参考资料

- [AkShare Documentation](https://akshare.readthedocs.io/) - Chinese financial data library
- [SQLite Python Tutorial](https://docs.python.org/3/library/sqlite3.html)

---

**Version**: 1.0.0  
**Last Updated**: 2026-03-13  
**Author**: jakey
**Email**: zhuxi0906@gmail.com
**Wechat**: jakeycis
