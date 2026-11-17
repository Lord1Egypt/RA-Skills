# Cortex CLI 使用方法

> 回测命令行工具完整使用指南

---

## 基本命令

```bash
python bin/cortex_cli.py backtest \
    --strategy <策略名称或路径> \
    --start-date <YYYYMMDD> \
    --end-date <YYYYMMDD>
```

---

## 参数说明

### 必需参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--strategy` `-s` | 策略名称或策略文件路径(.py) | `double_ma` 或 `/path/to/strategy.py` |
| `--start-date` | 开始日期 (YYYYMMDD) | `20260101` |
| `--end-date` | 结束日期 (YYYYMMDD) | `20260331` |

### 可选参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--initial-cash` | 初始资金 | 配置文件 `initial_cash` |
| `--fq` | 复权模式: `pre`(前复权) 或 `post`(后复权) | 配置文件 `fq` |
| `--mode` | 撮合模式: `loose`(宽松) 或 `strict`(严谨) | 配置文件 `mode` |
| `--report-dir` `-r` | 回测报告输出目录（路径模式） | 策略文件目录的 `backtest/` |
| `--config` `-c` | 配置文件路径 | 自动查找 |
| `--version` `-v` | 显示版本 | - |

---

## 策略模式

### 名称模式

策略文件位于固定目录 `<DATA-DIR>/strategies/<name>.py`：

```bash
python bin/cortex_cli.py backtest \
    --strategy double_ma \
    --start-date 20260101 \
    --end-date 20260331
```

**输出位置：** `<DATA-DIR>/backtest/<strategy_id>-001/`（序号递增）

### 路径模式

直接指定策略文件路径，适合独立开发：

```bash
python bin/cortex_cli.py backtest \
    --strategy /home/user/my_strategies/test_strategy.py \
    --start-date 20260101 \
    --end-date 20260331
```

**输出位置：** 策略文件所在目录的 `backtest/test_strategy-001/`

**自定义输出目录：**
```bash
python bin/cortex_cli.py backtest \
    --strategy /path/to/strategy.py \
    --start-date 20260101 \
    --end-date 20260331 \
    --report-dir /home/user/backtest_results
```

---

## 配置文件

### 配置文件查找顺序

1. `<CORTEX-INSTALL-DIR>/etc/cortex.conf` （推荐）
2. `<CORTEX-INSTALL-DIR>/etc/cortex_cli.conf`
3. `<CORTEX-INSTALL-DIR>/bin/cortex_cli.conf`
4. `/etc/cortex.conf` （系统配置）

### 配置文件结构

```ini
[log]
level = INFO
file = <DATA-DIR>/logs/cortex_cli.log
rotate_size = 10M
rotate_num = 5

[main]
data_dir = <DATA-DIR>
adapter = pyqdt

[strategies]
# 税费设置（聚宽默认值）
open_commission = 0.0003
close_commission = 0.0003
stamp_tax = 0.001
min_commission = 5

# 滑点设置（聚宽默认值）
slippage_type = price_related
slippage_value = 0.00246

# 复权方式（回测默认后复权）
fq = post

# 撮合模式（严谨）
mode = strict

# 初始资金
initial_cash = 1000000

[pyqdt]
data_path = <PYQDT-DATA-PATH>
```

### CLI 参数覆盖配置文件

```bash
# 覆盖复权模式为前复权
python bin/cortex_cli.py backtest \
    --strategy double_ma \
    --start-date 20260101 \
    --end-date 20260331 \
    --fq pre

# 覆盖撮合模式为宽松（对照聚宽）
python bin/cortex_cli.py backtest \
    --strategy double_ma \
    --start-date 20260101 \
    --end-date 20260331 \
    --mode loose

# 覆盖初始资金
python bin/cortex_cli.py backtest \
    --strategy double_ma \
    --start-date 20260101 \
    --end-date 20260331 \
    --initial-cash 500000
```

---

## 回测输出

### 输出目录结构

**名称模式：** `<DATA-DIR>/backtest/<strategy_id>-<seq>/`
```
<DATA-DIR>/backtest/
├── index.json               # 回测索引文件
├── double_ma-001/           # 第1次回测
│   ├── strategy.py          # 策略代码副本
│   ├── summary.json         # 回测摘要
│   ├── account.csv          # 账户每日状态
│   ├── positions.csv        # 持仓每日明细
│   ├── orders.json          # 订单记录
│   └── run.log              # 策略运行日志
├── double_ma-002/           # 第2次回测
│   └── ...
```

**路径模式：** 策略文件目录的 `backtest/<strategy_id>-<seq>/`
```
<策略文件目录>/backtest/
├── index.json
├── my_strategy-001/
│   └── ...
```

### account.csv 格式

| 列名 | 说明 |
|------|------|
| date | 日期（回测时间） |
| available_cash | 可用资金 |
| market_value | 持仓市值 |
| total_assets | 总资产 |

### positions.csv 格式

| 列名 | 说明 |
|------|------|
| date | 日期 |
| type | 品种 (stock) |
| code | 标的代码 |
| side | 多空 (long/short) |
| amount | 持仓数量 |
| available | 可卖数量（T+1） |
| last_price | 最新价 |
| market_value | 市值 |
| profit | 盈亏 |
| open_cost | 开仓均价 |
| today | 今日买入数量 |
| today_profit | 今日收益 |
| profit_pct | 盈亏占比 |
| position_pct | 仓位占比 |

### summary.json 格式

```json
{
  "initial_cash": 1000000.00,
  "final_value": 985502.70,
  "total_return": -1.45,
  "trade_count": 5
}
```

---

## 复权模式说明

| 模式 | 参数 | 说明 | 适用场景 |
|------|------|------|----------|
| 后复权 | `--fq post` | Cortex 默认 | 一般回测 |
| 前复权 | `--fq pre` | 聚宽默认 | 对照聚宽 |
| 动态复权 | 策略中 `set_option('use_real_price', True)` | 基准日=current_dt | 精确回测 |

**注意：** 策略代码中使用 `use_real_price=True` 会启用动态复权，CLI 参数无效。

---

## 撮合模式说明

| 模式 | 参数 | 说明 | 适用场景 |
|------|------|------|----------|
| 严谨 | `--mode strict` | 严格资金限制，拟真交易 | 实盘仿真 |
| 宽松 | `--mode loose` | 允许资金超限 | 策略研发、对照聚宽 |

**宽松模式特点：**
- cash 可能为负（允许超限买入）
- 税费先加总再四舍五入（聚宽风格）

**严谨模式特点：**
- 严格检查可用资金
- 买入超限会拒绝下单
- 税费每步分别四舍五入

---

## 常用命令示例

### 快速回测

```bash
python bin/cortex_cli.py backtest \
    --strategy double_ma \
    --start-date 20260101 \
    --end-date 20260331
```

### 前复权对照聚宽

```bash
python bin/cortex_cli.py backtest \
    --strategy double_ma \
    --start-date 20260101 \
    --end-date 20260331 \
    --fq pre \
    --mode loose
```

### 小资金测试

```bash
python bin/cortex_cli.py backtest \
    --strategy my_strategy.py \
    --start-date 20260101 \
    --end-date 20260131 \
    --initial-cash 100000
```

### 指定输出目录

```bash
python bin/cortex_cli.py backtest \
    --strategy /path/to/strategy.py \
    --start-date 20260101 \
    --end-date 20260331 \
    --report-dir /home/user/backtest_results
```

---

## 常见问题

### Q: 日期格式错误

**错误：** `日期格式错误: 2026-01-01,应为 YYYYMMDD 格式`

**解决：** 使用 `YYYYMMDD` 格式：
```bash
--start-date 20260101  # 正确
--start-date 2026-01-01  # 错误
```

### Q: 配置文件缺失必要项

**错误：** `配置文件缺少必要项: [pyqdt] data_path`

**解决：** 编辑配置文件添加缺失项：
```ini
[pyqdt]
data_path = <PYQDT-DATA-PATH>
```

### Q: 策略文件找不到

**名称模式：** 策略文件必须在 `<DATA-DIR>/strategies/<name>.py`

**路径模式：** 检查文件路径是否正确

---

## 运行日志

回测时日志输出示例：

```
2026-04-23 09:00:00 - cortex_cli - INFO - Cortex CLI v1.0.0
2026-04-23 09:00:00 - cortex_cli - INFO - 配置文件: /path/to/cortex.conf
2026-04-23 09:00:00 - cortex_cli - INFO - 策略模式: 名称模式
2026-04-23 09:00:00 - cortex_cli - INFO - 策略名称: double_ma
2026-04-23 09:00:00 - cortex_cli - INFO - 时间区间: 2026-01-01 ~ 2026-03-31
2026-04-23 09:00:00 - cortex_cli - INFO - 复权模式 (fq): post
2026-04-23 09:00:00 - cortex_cli - INFO - 撮合模式 (mode): strict
2026-04-23 09:00:00 - cortex_cli - INFO - 初始化回测引擎...
2026-04-23 09:00:00 - cortex_cli - INFO - 开始回测...
2026-04-23 09:00:05 - cortex_cli - INFO - 回测完成
2026-04-23 09:00:05 - cortex_cli - INFO - ============================================================
2026-04-23 09:00:05 - cortex_cli - INFO - 回测摘要:
2026-04-23 09:00:05 - cortex_cli - INFO -   初始资金: 1000000.00
2026-04-23 09:00:05 - cortex_cli - INFO -   最终市值: 985502.70
2026-04-23 09:00:05 - cortex_cli - INFO -   总收益率: -1.45%
2026-04-23 09:00:05 - cortex_cli - INFO -   交易次数: 5
2026-04-23 09:00:05 - cortex_cli - INFO - ============================================================
```

---

## 版本信息

- CLI 版本：v1.0.0
- 支持周期：day（日线）
- 数据源：pyqdt