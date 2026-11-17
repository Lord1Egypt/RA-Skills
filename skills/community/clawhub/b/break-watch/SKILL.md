---
name: break-watch
description: "盘中放量上涨阳线股票扫描器。当用户询问盘中选股、放量突破、放量上涨、阳线筛选、盘中扫描、量比选股、突破选股、Break Watch，或提到'放量'、'上涨'、'阳线'、'盘中选股'、'量比'、'突增'等术语时触发此技能。通过通达信 pytdx 获取实时行情，筛选同时满足放量、上涨、收阳线三个条件的 A 股股票，输出结构化信号列表。"
agent_created: true
---

# Break Watch - 盘中放量上涨阳线扫描器

## Overview

盘中实时扫描 A 股市场，筛选同时满足"放量 + 上涨 + 收阳线"三个条件的股票。通过 pytdx 连接通达信行情服务器获取实时行情数据，使用历史同进度量比和盘中新增量突增双重指标判断放量，输出结构化信号列表。

## Prerequisites

首次使用前，需在 managed Python venv 中安装 pytdx：

```bash
C:\Users\xfb\.workbuddy\binaries\python\versions\3.13.12\python.exe -m venv C:\Users\xfb\.workbuddy\binaries\python\envs\default
C:\Users\xfb\.workbuddy\binaries\python\envs\default\Scripts\pip install pytdx
```

若 venv 已存在则跳过创建，直接执行 pip install。

## Core Workflow

### Step 1: 执行扫描

使用 managed Python 运行 `scripts/scan_breakout.py`，默认输出 JSON 到 stdout：

```bash
C:\Users\xfb\.workbuddy\binaries\python\envs\default\Scripts\python.exe <skill_dir>/scripts/scan_breakout.py
```

常用参数：

```bash
# 全市场扫描，使用默认参数
python scripts/scan_breakout.py

# 指定自选股扫描
python scripts/scan_breakout.py --mode watchlist --watchlist 600000,000001,300750

# 调整阈值
python scripts/scan_breakout.py --min-rise-pct 2.0 --volume-ratio-threshold 3.0

# 非交易时间强制扫描
python scripts/scan_breakout.py --force-scan

# 同时输出 CSV/HTML/TXT 文件
python scripts/scan_breakout.py --output both --result-dir ./output

# 使用自定义配置文件
python scripts/scan_breakout.py --config /path/to/config.toml
```

参数说明：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--mode all\|watchlist` | 扫描模式 | all |
| `--watchlist CODES` | 逗号分隔的股票代码 | - |
| `--min-rise-pct N` | 最低涨幅阈值 | 1.0 |
| `--volume-ratio-threshold N` | 历史量比阈值 | 2.0 |
| `--interval-spike-threshold N` | 盘中突增阈值 | 2.0 |
| `--history-days N` | 历史基准天数 | 20 |
| `--force-scan` | 非交易时间也扫描 | false |
| `--output json\|files\|both` | 输出格式 | json |
| `--result-dir PATH` | 输出文件目录 | output/ |
| `--config PATH` | 配置文件路径 | config.toml |

脚本输出 JSON 到 stdout，进度信息输出到 stderr。使用 `json.loads()` 解析输出。

### Step 2: 解读扫描结果

JSON 输出结构：

```json
{
  "scan_time": "2026-07-07T14:00:00",
  "server": "119.6.200.40:7709",
  "is_trading_hours": true,
  "trading_progress": 0.25,
  "universe_size": 3500,
  "scannable_count": 3200,
  "signal_count": 3,
  "signals": [
    {
      "code": "600000",
      "name": "浦发银行",
      "market": "SH",
      "timestamp": "2026-07-07 14:00:00",
      "price": 10.50,
      "last_close": 10.30,
      "open": 10.35,
      "change_pct": 1.94,
      "current_volume": 500000,
      "avg_volume": 1000000,
      "expected_volume": 250000,
      "volume_ratio": 2.0,
      "interval_volume": 50000,
      "interval_spike_ratio": 2.5,
      "server": "119.6.200.40:7709"
    }
  ],
  "config": {
    "mode": "all",
    "min_rise_pct": 1.0,
    "volume_ratio_threshold": 2.0,
    "interval_spike_threshold": 2.0,
    "history_days": 20
  },
  "errors": []
}
```

关键字段说明：

| 字段 | 说明 |
|------|------|
| `is_trading_hours` | 是否在交易时段内 |
| `trading_progress` | 当日交易进度 (0-1) |
| `universe_size` | 股票池总数 |
| `scannable_count` | 有足够历史数据可扫描的数量 |
| `signal_count` | 命中信号数 |
| `signals` | 命中信号列表 |
| `volume_ratio` | 历史同进度量比 |
| `interval_spike_ratio` | 盘中新增量突增倍数（首轮为 null） |

### Step 3: 向用户呈现结果

扫描完成后，按以下方式呈现：

1. **扫描概要**：扫描时间、交易进度、股票池规模、命中数量
2. **命中信号表**：用 Markdown 表格展示命中股票

| 代码 | 名称 | 当前价 | 涨幅% | 量比 | 突增倍数 | 命中时间 |
|------|------|--------|-------|------|----------|----------|
| 600000 | 浦发银行 | 10.50 | +1.94% | 2.00 | 2.50 | 14:00:00 |

3. **策略说明**：简要说明命中条件（放量+上涨+收阳线）
4. **风险提示**：每次结果末尾附加免责声明

可使用 `show_widget` 工具生成可视化图表辅助说明，如量比分布图、涨幅排名图等。

## 策略详解

命中股票必须同时满足三个条件，详见 `references/strategy.md`：

1. **收阳线**：当前价 > 今日开盘价
2. **上涨**：涨幅 >= 最低涨幅阈值（默认 1%）
3. **放量**：历史同进度量比 >= 阈值（默认 2.0）且盘中新增量突增倍数 >= 阈值（默认 2.0）

## 注意事项

- A 股涨跌颜色：涨为红色，跌为绿色（中国市场惯例）
- 非交易时间扫描时，通达信返回上一交易日收盘数据，`is_trading_hours` 为 false
- 首轮扫描没有前一轮对比，`interval_spike_ratio` 为 null，仅按历史量比判断
- 科创板（688/689）和北交所默认剔除，创业板（300/301）保留
- 评分仅供行情整理与复盘参考，不构成投资建议

## Script Reference

核心扫描脚本：`scripts/scan_breakout.py`

该脚本导入 `src/break_watch/` 包，封装为单次扫描 + JSON 输出的入口。底层扫描引擎（tdx_client、scanner、universe、output 等模块）保持不变，可通过 `config.toml` 或 CLI 参数配置。

项目原始入口 `run.py` 仍可用于持续循环扫描和 exe 打包场景。
