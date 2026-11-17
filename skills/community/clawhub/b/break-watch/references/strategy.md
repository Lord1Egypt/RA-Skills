# Break Watch 选股策略详解

## 策略概述

Break Watch 是盘中实时选股工具，筛选同时满足"放量 + 上涨 + 收阳线"三个条件的 A 股股票。
三项条件必须同时满足，任意一项不满足都不视为命中。

## 三大筛选条件

### 1. 收阳线

盘中没有最终收盘价，因此将"收阳线"定义为：

- 当前价 `price > 今日开盘价 open`

即当前日线暂时为阳线。

### 2. 上涨

- 当前价达到最低涨幅要求
- `price >= last_close * (1 + min_rise_pct / 100)`
- 默认最低涨幅 `1.0%`

### 3. 放量

放量使用两个指标双重判断：

#### 历史同进度量比

- 取最近 N 个交易日（默认 20 日）的平均成交量作为前期基准
- 根据当前交易进度折算预期成交量
- `expected_volume = avg_volume * trading_progress`
- `volume_ratio = current_volume / expected_volume`
- 要求 `volume_ratio >= volume_ratio_threshold`（默认 2.0）

#### 盘中新增量突增

- 从第二轮扫描开始，记录每只股票本轮新增成交量
- `interval_volume = current_volume - previous_volume`
- 使用最近 M 个扫描周期（默认 5 轮）的平均新增量作为盘中短期基准
- `interval_spike_ratio = interval_volume / avg_recent_interval_volume`
- 样本充足时（至少 3 轮）要求 `interval_spike_ratio >= interval_spike_threshold`（默认 2.0）
- 首轮或样本不足时，仅按历史同进度放量判断

## 交易进度计算

按 A 股常规交易时段：

| 时段 | 时间 | 分钟数 |
|------|------|--------|
| 上午 | 09:30 - 11:30 | 120 |
| 下午 | 13:00 - 15:00 | 120 |
| 全天 | - | 240 |

示例：当前 10:30，已交易 60 分钟，进度 = 60 / 240 = 25%。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `volume_ratio_threshold` | 2.0 | 历史同进度量比阈值 |
| `interval_spike_threshold` | 2.0 | 盘中新增量突增阈值 |
| `interval_spike_window` | 5 | 突增参考窗口（扫描轮数） |
| `interval_spike_min_samples` | 3 | 最少样本轮数 |
| `min_rise_pct` | 1.0 | 最低涨幅（%） |
| `history_days` | 20 | 历史基准天数 |
| `scan_interval_seconds` | 30 | 扫描间隔（秒） |

## 股票范围规则

### 支持的 A 股代码段

| 市场 | 代码前缀 | 板块 |
|------|----------|------|
| 上海 | 600xxx, 601xxx, 603xxx, 605xxx | 沪市主板 |
| 深圳 | 000xxx, 001xxx, 002xxx, 003xxx | 深市主板 |
| 深圳 | 300xxx, 301xxx | 创业板 |

### 默认剔除

- 科创板：688xxx, 689xxx
- 北交所：8xxxxx, 4xxxxx, 920xxx

### 扫描模式

- `all`：全市场扫描，从通达信服务器拉取证券列表
- `watchlist`：只扫描指定股票，支持 `600000`、`sh600000`、`sz000001` 等写法

## 数据源

使用 pytdx 连接通达信行情服务器，默认服务器列表：

- 119.6.200.40:7709
- 182.140.139.191:7709
- 218.200.222.134:7709
- 182.150.28.166:7709

支持服务器自动故障切换：当前服务器连接失败或请求失败时，按顺序尝试下一个。

## 输出文件

| 文件 | 说明 |
|------|------|
| `output/signals_YYYYMMDD.csv` | 命中结果 CSV |
| `output/signals_YYYYMMDD.html` | 命中结果 HTML 页面 |
| `output/ths_codes_YYYYMMDD.txt` | 同花顺导入用股票代码（一行一个） |
| `logs/break_watch_YYYYMMDD.log` | 运行日志 |

## 注意事项

- 非交易时间运行时，通达信返回上一交易日收盘数据
- 首轮扫描没有前一轮成交量对比，盘中新增量突增倍数标记为不可用（null）
- 同一只股票默认每日只提示一次（`repeat_alert = false`）
- 评分仅供行情整理与复盘参考，不构成投资建议
