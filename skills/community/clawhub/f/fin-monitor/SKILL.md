---
name: finance-monitor
description: 从 CNBC 抓取 18 个金融指标数据（宏观经济、指数ETF、美股个股），写入本地 SQLite 数据库。纯 stdlib，无需任何 API Key。
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Finance Monitor

定期抓取金融指标数据，写入本地 SQLite 数据库。

## ⚠️ 安全声明

**API Key 是敏感信息**，请勿将真实 API Key 直接写入 skill 或任何公开可访问的文件。

获取 Finnhub API Key（免费注册）：https://finnhub.io/register

### Key 安全传递方式

| 方式 | 安全性 | 说明 |
|---|---|---|
| `FINNHUB_API_KEY` 环境变量 | ✅ 推荐 | 不暴露在进程列表/日志中 |
| `--finnhub-key` 参数 | ⚠️ 备用 | 会暴露在进程列表，仅测试用 |

---

## 数据源

| 指标 | 代码 | 数据源 | 说明 |
|---|---|---|---|
| 美国10年期TIPS | US10YTIP | CNBC | 实时报价 |
| 美国10年期国债 | US10Y | CNBC | 实时报价 |
| 黄金 COMEX | GC | CNBC | 实时报价 |
| WTI 原油 | CL | CNBC | 实时报价 |
| 标普500 ETF | SPY | CNBC | 实时报价 |
| 标普500指数 | SPX | CNBC | 实时报价 |
| 纳斯达克100 ETF | QQQ | CNBC | 实时报价 |
| 纳斯达克100指数 | NDX | CNBC | 实时报价 |
| 美元指数 DXY | DXY | CNBC | 实时报价 |
| 恐慌指数 VIX | VIX | CNBC | 实时报价 |
| **苹果** | AAPL | CNBC | 实时报价 |
| **微软** | MSFT | CNBC | 实时报价 |
| **英伟达** | NVDA | CNBC | 实时报价 |
| **亚马逊** | AMZN | CNBC | 实时报价 |
| **Meta** | META | CNBC | 实时报价 |
| **联合健康** | UNH | CNBC | 实时报价 |
| **可口可乐** | KO | CNBC | 实时报价 |
| **伯克希尔哈撒韦** | BRK.B | CNBC | 实时报价 |

> **注意**：Finnhub 免费版不支持 SPX、NDX、黄金、VIX、国债收益率。如需这些指标，推荐使用 Finnhub Pro 或其他数据源。

---

## 参数

| 参数 | 说明 | 默认值 |
|---|---|---|
| `db_path` | SQLite 数据库路径（**必填**） | 无 |
| `log_path` | 日志文件路径 | `db_path所在目录/fetch.log` |
| `FINNHUB_API_KEY` | Finnhub API Key（**环境变量，推荐**） | 无 |
| `--finnhub-key` | Finnhub API Key（命令行，备用） | 无 |

---

## 安装依赖

### Python 3

```bash
python3 --version
```

---

## 使用方式

用户说以下内容时触发：
- "抓取金融数据"
- "更新指标数据"
- "刷新 finance 数据库"

### 推荐方式

```bash
export FINNHUB_API_KEY=你的key
python3 scripts/fetch_data.py --db-path ~/finance/finance.db
```

### 备用方式（仅测试用）

```bash
python3 scripts/fetch_data.py \
  --db-path ~/finance/finance.db \
  --finnhub-key 你的key
```

---

## 数据库表结构

```sql
CREATE TABLE indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fetch_date TEXT NOT NULL,
    fetch_time TEXT NOT NULL,
    name_cn TEXT NOT NULL,
    code TEXT NOT NULL,
    prev_close REAL,
    current_price REAL,
    after_hours REAL,
    change_pct REAL,
    week52_high REAL,
    dist_from_high_pct REAL,
    week52_low REAL,
    dist_from_low_pct REAL,
    source TEXT DEFAULT 'nasdaq',
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE fetch_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fetch_date TEXT NOT NULL,
    fetch_time TEXT NOT NULL,
    source TEXT NOT NULL,
    indicators_count INTEGER,
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);
```

---

## 返回格式

```
✅ Data fetched | 2026-03-23 18:00
📂 DB: ~/finance/finance.db

Indicator          Code   Price        Change
------------------------------------------------
标普500 ETF          SPY      648.57      -1.70%
纳斯达克100 ETF        QQQ      582.06      -1.85%
WTI 原油            CL        85.12       +0.81%
美元指数            DX        12.39        -0.23%
```

---

## 定时任务

### macOS / Linux

```bash
# 编辑 crontab
crontab -e

# 添加（每小时整点执行）
0 * * * * cd ~/finance && FINNHUB_API_KEY=你的key /usr/bin/python3 fetch_data.py --db-path ~/finance/finance.db >> ~/finance/fetch.log 2>&1
```

### Windows 任务计划程序

1. 创建基本任务，触发器：每小时
2. 操作：启动程序 → `py`
3. 参数：`fetch_data.py --db-path C:\Users\你\finance\finance.db`
4. 在用户环境变量中设置 `FINNHUB_API_KEY=你的key`

### OpenClaw cron

```json
{
  "cron": "0 * * * *",
  "command": "python3",
  "args": ["fetch_data.py", "--db-path", "~/finance/finance.db"],
  "env": { "FINNHUB_API_KEY": "你的key" },
  "workdir": "~/finance"
}
```
