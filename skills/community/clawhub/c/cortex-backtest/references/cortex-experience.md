# Cortex 回测引擎使用经验文档

> 本文档记录使用过程中的经验教训，每次使用技能时务必先查阅此文档，避免重复踩坑。
> 
> **经验分类规则**：
> - **编号 < 100**：系统预置经验（技能创建时自带，经过验证的常见问题）
> - **编号 ≥ 100**：使用收集经验（实际使用过程中发现的问题，按模板追加）
> 
> **更新与维护规则**：
> 1. 每次使用后发现有新的经验教训，从编号100开始逐条追加到此文档末尾
> 2. 如果有新增系统预置经验（编号<100），检查用户收集经验（编号≥100）中是否存在相同或相似的经验，如有则移除
> 3. 移除用户经验时，直接删除记录，序号可回收再用（后续新增经验可使用已删除的序号）

---

## 📋 经验索引

### 系统预置经验（编号 < 100）

| 序号 | 问题类型 | 关键词 | 简要说明 |
|------|----------|--------|----------|
| 000 | 使用规范 | 技能执行 | 所有回测任务强制使用本技能，不能直接调用 CLI |
| 001 | 回测频率 | 日频限制 | 目前仅支持日线级别回测，分钟级别暂不支持 |
| 002 | 回调机制 | run_daily | handle_data 不触发，必须用 run_daily 注册交易逻辑 |
| 003 | 代码格式 | MIC风格 | 策略代码必须用 .XSHG/.XSHE 格式，不能用 .SH/.SZ |
| 004 | 配置文件 | 绝对路径 | 所有路径参数（配置文件内部 + CLI --config）都必须使用绝对路径 |

### 使用收集经验（编号 ≥ 100）

| 序号 | 问题类型 | 关键词 | 简要说明 |
|------|----------|--------|----------|
| 100 | 性能问题 | 效率慢 | 日线回测效率低（约1分钟/天），高频数据建议用 Python 直接处理 |
| 101 | （可用） | 序号回收 | 此序号已回收可用 |
| 102 | 数据类型 | DataFrame | account DataFrame 必须用 float 类型，否则 LossySetitemError |
| 103 | 分钟数据 | end_date | 分钟数据 end_date 需设为次日才能获取当日完整数据 |
| 104 | （可用） | 序号回收 | 此序号已回收可用（已合并至系统经验004） |
| 105 | 聚宽兼容 | 属性标准 | portfolio.total_assets是Cortex方言，聚宽用total_value |

> **追加模板**：发现新问题时，序号可回收再用（如101已删除），按模板格式追加到文档末尾。
>
> **去重示例**：如果系统新增经验覆盖用户经验100，则直接删除用户经验100，序号100可回收再用。

---

## 详细经验记录

### 000 - 强制使用本技能

**发现日期**：2026-04-26

**问题描述**：
所有回测任务必须通过 Cortex 回测引擎技能执行，不能直接调用 CLI。

**核心规则**：
- **强制使用本技能**：回测请求触发本技能后，由技能统一调度执行
- **不能绕过技能**：禁止直接调用 `/opt/cirt/bin/cortex_cli.py`

**正确做法**：
```
用户请求回测 → 触发 cortex-backtest 技能 → 技能读取经验文档 → 技能执行回测 → 技能输出报告
```

**错误做法**：
```bash
# 错误：直接调用 CLI
python /opt/cirt/bin/cortex_cli.py backtest --strategy xxx
```

**教训**：
回测任务必须通过本技能执行，确保经验文档被查阅、参数被正确引导。

---

### 001 - 仅支持日频回测

**发现日期**：2026-04-26

**问题描述**：
Cortex 回测引擎目前仅支持日线级别回测，分钟级别暂不支持。

**核心规则**：
- **仅支持日线**：period=daily 是唯一支持的频率
- **分钟级别不支持**：15分钟、30分钟、60分钟回测需用 Python 直接处理

**正确做法**：
```bash
# 日线回测：使用 Cortex
--start-date 20241101 --end-date 20260424
```

**分钟回测替代方案**：
```python
# 分钟数据：用 Python + pyqdt 直接处理
from pyqdt import QuoteData
quote = QuoteData(data_path='/data/QuantData/pyqdt_csv')
df = quote.get_price('511090.SH', period='30m', start_date='2024-11-01', end_date='2026-04-25')
```

**教训**：
日线用 Cortex，分钟用 Python。

---

### 002 - handle_data 不触发，必须用 run_daily

**发现日期**：2026-04-26

**问题描述**：
日线回测中 `handle_data(context, data)` 函数不会被自动调用，交易逻辑必须通过 `run_daily` 注册。

**核心规则**：
- **handle_data 无效**：日线回测不会触发 handle_data
- **必须用 run_daily**：交易逻辑通过 `run_daily(func, time='open')` 注册

**正确写法**：
```python
def initialize(context):
    # 正确：注册交易逻辑
    run_daily(trade_logic, time='open')
    g.stock = '511090.XSHG'

def trade_logic(context):
    # 交易逻辑在这里
    stock = g.stock
    prices = get_price(stock, count=30)
    if buy_signal:
        order_shares(stock, shares)
```

**错误写法**：
```python
def handle_data(context, data):
    # 错误：日线回测中不会触发！
    stock = g.stock
    # ...
```

**time 参数**：
| time 值 | 触发时机 |
|---------|----------|
| `'before_open'` | 9:00 开盘前 |
| `'open'` | 9:30 开盘时 |
| `'after_close'` | 15:30 收盘后 |

**教训**：
交易逻辑必须通过 run_daily 注册，handle_data 在日线回测中无效。

---

### 003 - 必须使用 MIC 代码风格

**发现日期**：2026-04-26

**问题描述**：
策略代码必须使用 MIC 代码风格（`.XSHG`/`.XSHE`），不能用 Classic 格式（`.SH`/`.SZ`）。

**核心规则**：
- **策略代码用 MIC**：`511090.XSHG`、`000001.XSHE`
- **不能用 Classic**：禁止使用 `511090.SH`、`000001.SZ`
- **自动转换**：Cortex 内部会将 MIC 转换为 Classic 格式查询数据

**正确写法**：
```python
def initialize(context):
    set_benchmark('511090.XSHG')  # MIC 格式
    g.stock = '511090.XSHG'      # MIC 格式

def trade_logic(context):
    prices = get_price('511090.XSHG', count=30)  # MIC 格式
```

**错误写法**：
```python
def initialize(context):
    g.stock = '511090.SH'  # 错误：不能用 Classic 格式！
```

**格式对比**：
| 来源 | 格式 | 示例 |
|------|------|------|
| 策略代码 | MIC | `511090.XSHG` |
| pyqdt 数据 | Classic | `511090.SH` |

**教训**：
策略代码统一使用 MIC 格式，内部自动转换。

---

### 004 - 所有路径必须使用绝对路径

**发现日期**：2026-05-01

**问题描述**：
Cortex CLI 从 `/opt/cirt/bin/` 目录运行，所有相对路径都会相对于该目录解析，而非用户期望的配置文件所在目录或当前工作目录。

**适用场景**：

| 场景 | 说明 | 错误后果 |
|------|------|----------|
| 配置文件内部参数 | `data_dir`、`log_file` 等 | 解析为 `/opt/cirt/bin/` 或 `/opt/cirt/logs/` |
| CLI `--config` 参数 | 命令行指定配置文件 | 找不到配置文件 |

**症状表现**：
- `data_dir = .` 解析为 `/opt/cirt/bin/`
- `log_file = logs/cortex.log` 解析为 `/opt/cirt/logs/cortex.log`
- `--config cortex_cli.conf` 找不到文件
- 运行时报错：`PermissionError: [Errno 13] Permission denied: '/opt/cirt/logs'`

**解决方案**：
所有路径参数必须使用**绝对路径**。

**正确用法**：

配置文件内部：
```ini
[main]
data_dir = /home/openclaw/.openclaw/workspace/cortex_data
log_file = /home/openclaw/.openclaw/workspace/cortex_data/logs/cortex.log

[pyqdt]
data_path = /data/QuantData/pyqdt_csv
```

CLI 命令行：
```bash
python3 /opt/cirt/bin/cortex_cli.py backtest \\n    --config /home/openclaw/.openclaw/workspace/cortex_data/cortex_cli.conf \\n    --strategy my_strategy
```

**错误用法**：

配置文件内部：
```ini
[main]
data_dir = .                     # 错误：解析为 /opt/cirt/bin/
log_file = logs/cortex.log      # 错误：解析为 /opt/cirt/logs/
```

CLI 命令行：
```bash
cd cortex_data
python3 /opt/cirt/bin/cortex_cli.py backtest --config cortex_cli.conf
# 错误：找不到配置文件
```

**教训**：
Cortex 的所有路径参数（配置文件内部 + CLI 参数）都必须使用**绝对路径**，相对路径会解析为 CLI 工具所在目录（`/opt/cirt/bin/`）。

---

### 105 - Portfolio属性差异（聚宽兼容性）

**发现日期**：2026-04-26

**问题描述**：
Cortex 使用 `portfolio.total_assets` 作为总资产属性，但聚宽平台使用 `portfolio.total_value`。直接在聚宽平台运行 Cortex 策略代码会报 `AttributeError`。

**错误代码**：
```python
def after_trading_end(context):
    # ❌ Cortex方言，聚宽不兼容
    total = context.portfolio.total_assets  # AttributeError!
```

**正确代码**：
```python
def after_trading_end(context):
    # ✅ 聚宽标准属性
    total = context.portfolio.total_value  # 聚宽兼容
```

**属性对照表**：
| 功能 | Cortex属性 | 聚宽属性 | 说明 |
|------|-----------|---------|------|
| 总资产 | `portfolio.total_assets` | `portfolio.total_value` | ✅ 用total_value |
| 可用现金 | `portfolio.available_cash` | `portfolio.available_cash` | ✅ 兼容 |
| 持仓数量 | `position.total_amount` | `position.total_amount` | ✅ 兼容 |
| 持仓市值 | `position.value` | `position.value` | ✅ 兼容 |

**教训**：
策略代码必须使用聚宽标准属性，避免 Cortex 方言属性。

---

### 100 - Cortex 日线回测效率极低

**发现日期**：2026-04-26

**问题描述**：
Cortex CLI 日线回测效率非常低，处理速度约 **1分钟/天**。359天的回测需要约6分钟，分钟级别数据（数千根K线）会更慢。

**症状表现**：
- 命令运行后长时间无输出
- 进程卡在 Progress: 10/359 days 等阶段
- CPU 使用率高但进度极慢

**解决方案**：
对于高频数据或大量回测需求，**建议直接用 Python 脚本使用 pyqdt 数据**，绕过 Cortex CLI。

**对比**：
| 方案 | 359天日线回测耗时 | 优势 |
|------|------------------|------|
| Cortex CLI | ~6分钟 | 聚宽风格API，标准化 |
| Python + pyqdt | <1秒 | 高效，灵活，直接数据处理 |

**建议场景**：
- **使用 Cortex**：需要聚宽风格API、标准化回测框架、策略迁移到聚宽平台
- **使用 Python**：高频数据（15分钟/30分钟/60分钟）、大规模参数优化、快速迭代测试

---

### 102 - DataFrame 类型必须为 float

**发现日期**：2026-04-26

**问题描述**：
在 Python 直接处理回测时，使用 `account.iloc[i] = [cash, position, position * close, cash + position * close]` 会报 `LossySetitemError`，因为 DataFrame 初始化时用了 int 类型，但运行时会产生 float 值。

**错误代码**：
```python
account = pd.DataFrame(index=df.index)
account['cash'] = 1000000        # int 类型
account['shares'] = 0            # int 类型
account['position_value'] = 0    # int 类型
account['total_value'] = 1000000 # int 类型

# 运行时报错：LossySetitemError
account.iloc[i] = [cash, position, position * close, cash + position * close]
```

**正确代码**：
```python
account = pd.DataFrame(index=df.index)
account['cash'] = float(1000000)        # float 类型
account['shares'] = 0.0                 # float 类型
account['position_value'] = 0.0         # float 类型
account['total_value'] = float(1000000) # float 类型

# 正常运行
account.iloc[i] = [cash, position, position * close, cash + position * close]
```

**教训**：
涉及价格计算的 DataFrame 列，初始化时必须用 `float` 类型。

---

### 103 - 分钟数据 end_date 设置

**发现日期**：2026-04-26

**问题描述**：
pyqdt 获取分钟数据时，如果 `end_date` 只有日期（无时间），实际截止到该日 `00:00:00`，**不包括当天日内数据**。

**错误用法**：
```python
# 想取 2026-04-24 的分钟数据
df = quote.get_price('511090.SH', period='30m', start_date='2026-04-24', end_date='2026-04-24')
# 返回空数据或只有开盘前数据！
```

**正确用法**：
```python
# 方法1：end_date 设为次日
df = quote.get_price('511090.SH', period='30m', start_date='2026-04-24', end_date='2026-04-25')

# 方法2：使用 count 参数
df = quote.get_price('511090.SH', period='30m', count=240, end_date='2026-04-25')
```

**教训**：
分钟数据获取时，`end_date` 必须设为**次日**才能获取当日完整数据。

---


## 📝 新增经验记录模板

发现新问题时，按以下格式追加（序号从106开始递增）：

```markdown
### 106 - 问题简要描述

**发现日期**：YYYY-MM-DD

**问题描述**：
[描述问题现象]

**症状表现**：
- [症状1]
- [症状2]

**解决方案**：
[解决方法]

**正确代码/用法**：
```python
# 正确写法
```

**错误代码/用法**：
```python
# 错误写法
```

**教训**：
[总结一句话]

---
```

---

> **文档维护**：每次使用 Cortex 回测后，如有新的经验教训，序号从106开始追加到此文档末尾。序号101、104已回收可用。