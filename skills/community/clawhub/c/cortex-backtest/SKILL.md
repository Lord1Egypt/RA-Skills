---
name: cortex-backtest
description: Cortex 量化策略回测引擎。聚宽风格策略代码，支持日线回测，与聚宽平台完全对齐。触发场景：用户提及 Cortex 回测、策略回测、聚宽风格策略、回测引擎、量化策略开发、策略验证、Cortex 首次设置、Cortex 配置。
---

# Cortex Backtest

Cortex 是多市场量化策略回测与仿真引擎，采用**聚宽风格策略代码**，支持**日线级别回测**，与聚宽平台完全对齐。

## ⚠️ 使用前必读

**每次使用本技能前，必须先查阅经验文档！**

经验文档记录了之前使用过程中遇到的问题和解决方案，避免重复踩坑。

查阅路径：[references/cortex-experience.md](references/cortex-experience.md)

**经验分类**：
- **编号 < 100**：系统预置经验（技能自带，经过验证的常见问题）
- **编号 ≥ 100**：使用收集经验（实际使用中发现的新问题，使用后追加）

**使用后追加规则**：发现新问题时，从编号100开始递增追加到经验文档末尾。

**去重管理规则**：如果有新增系统预置经验，检查用户收集经验中是否有相同或相似的，如有则直接删除，序号可回收再用。

---

## 首次设置向导（重要！）

**使用本技能前，必须先完成场景配置！**

### 步骤 1：检查 TOOLS.md 场景配置

读取 `<WORKSPACE>/TOOLS.md`，检查是否已配置 Cortex 场景：

- **已配置场景 1/2/3** → 跳转到步骤 2
- **未配置或配置不完整** → 询问用户选择场景

### 步骤 2：验证配置文件和目录存在

根据 TOOLS.md 中登记的场景，检查对应的配置文件和目录：

| 场景 | 检查路径（绝对路径示例） |
|------|------------------------|
| 场景 1 | `/opt/cirt/etc/cortex.conf` |
| 场景 2 | `<WORKSPACE>/cortex_data/cortex_cli.conf` |
| 场景 3 | `<TENANT-WSPACE>/cortex_data/cortex_cli.conf` |

**场景 3 说明：**
- 租户目录位置由智能体（Agent）安排
- 方案 A（私域管理）：`<WORKSPACE>/user1/`（内含 `cortex_data/` 子目录）
- 方案 B（工作区统一管理）：`<WORKSPACE>/.cortex/user1/`（直接使用，不含 `cortex_data` 子目录）
- 具体路径需在 TOOLS.md 中明确登记

**占位符说明：**
- `<WORKSPACE>` - 智能体工作目录（如 `/home/allwin21/.openclaw/workspace`）
- `<TENANT-WSPACE>` - 租户工作目录（由智能体安排，可在私域中）

**检查结果处理：**
- **文件存在** → 配置完成，可正常使用
- **文件不存在** → 引导用户建立（见下方"引导建立流程"）

### 步骤 3：询问用户选择场景（如未配置）

**询问模板：**

```
检测到 Cortex 回测引擎尚未配置运行场景。

Cortex 支持三种配置场景，请根据您的使用需求选择：

【场景 1】系统配置
- 配置文件位置：/opt/cirt/etc/cortex.conf
- 适用场景：服务器部署、多智能体共享同一配置
- 特点：全局共享，配置集中管理

【场景 2】智能体独立配置  
- 配置文件位置：<WORKSPACE>/cortex_data/cortex_cli.conf
- 适用场景：单个智能体独立工作，数据隔离
- 特点：工作空间内自包含，便于迁移

【场景 3】智能体多租户配置（推荐）
- 配置文件位置：<TENANT-WSPACE>/cortex_data/cortex_cli.conf
- 适用场景：多用户/多账户，完全隔离
- 特点：每个租户独立目录，数据完全隔离
- 注意：租户目录位置由智能体安排，可在私域中管理

请回复数字 1、2 或 3 选择场景。

如选择场景 3，请指定租户目录位置（如私域路径或工作区路径）：
- 示例 1（私域）：<WORKSPACE>/user1/
- 示例 2（私域）：<WORKSPACE>/user2/
- 示例 3（工作区统一管理）：<WORKSPACE>/.cortex/user3/

占位符说明：
- <WORKSPACE> - 智能体工作目录
- <TENANT-WSPACE> - 租户工作目录（由智能体安排，可在私域中）

**注意：** 方案 B（工作区统一管理）直接使用 `<WORKSPACE>/.cortex/userN/` 作为租户目录，不再包含 `cortex_data` 子目录
```

### 步骤 4：引导建立流程（配置文件不存在时）

**根据用户选择的场景，执行以下建立流程：**

#### 场景 1 建立流程

```bash
# 1. 检查系统目录权限
ls -la /opt/cirt/etc/

# 2. 如无法写入系统目录，提示用户：
"场景 1 需要写入 /opt/cirt/etc/ 目录，当前权限不足。
建议：使用场景 2 或 3（无需系统权限），或手动创建配置文件。"

# 3. 如能写入，创建配置文件
sudo cp /opt/cirt/etc/cortex.conf.default /opt/cirt/etc/cortex.conf

# 4. 更新 TOOLS.md 登记
```

#### 场景 2 建立流程

**工作目录结构：**
```
<WORKSPACE>/cortex_data/
├── cortex_cli.conf          # 配置文件
├── strategies/              # 策略文件夹
│   └── double_ma.py
├── backtest/                # 回测输出
│   ├── index.json           # 回测索引
│   ├── double_ma-001/       # 回测结果（序号递增）
│   │   ├── strategy.py      # 策略代码副本
│   │   ├── summary.json     # 回测摘要
│   │   ├── account.csv      # 账户每日状态
│   │   ├── positions.csv    # 持仓每日明细
│   │   ├── orders.json      # 订单记录
│   │   └── run.log          # 运行日志
│   └── double_ma-002/       # 第2次回测
└── logs/                    # 日志目录
```

```bash
# 1. 创建目录结构
mkdir -p <WORKSPACE>/cortex_data/{strategies,backtest,logs}

# 2. 创建配置文件
cat > <WORKSPACE>/cortex_data/cortex_cli.conf << 'EOF'
[main]
data_dir = .
adapter = pyqdt
log_level = INFO
log_file = logs/cortex.log

[strategies]
initial_cash = 1000000
fq = post
mode = loose

[pyqdt]
data_path = /data/QuantData/pyqdt_csv
EOF

# 3. 更新 TOOLS.md 登记
```

#### 场景 3 建立流程

**说明：** 租户目录位置由智能体（Agent）安排，可在私域中管理

**工作目录结构（示例）：**
```
# 方案 A：私域管理（推荐）
<WORKSPACE>/user1/cortex_data/
<WORKSPACE>/user2/cortex_data/
<WORKSPACE>/user3/cortex_data/

# 方案 B：工作区统一管理（注意：直接使用，不含 cortex_data 子目录）
<WORKSPACE>/.cortex/user1/
<WORKSPACE>/.cortex/user2/

# 方案 A 租户目录内部结构（私域管理）
<TENANT-WSPACE>/cortex_data/
├── cortex_cli.conf          # 租户配置文件
├── strategies/              # 租户策略文件夹
│   └── my_strategy.py
├── backtest/                # 租户回测输出
│   ├── index.json
│   └── my_strategy-001/
│       ├── strategy.py      # 策略代码副本
│       ├── summary.json     # 回测摘要
│       ├── account.csv      # 账户每日状态
│       ├── positions.csv    # 持仓每日明细
│       ├── orders.json      # 订单记录
│       └── run.log          # 运行日志
└── logs/                    # 租户日志目录

# 方案 B 租户目录内部结构（工作区统一管理）
<TENANT-WSPACE>/
├── cortex_cli.conf          # 租户配置文件
├── strategies/              # 租户策略文件夹
├── backtest/                # 租户回测输出
└── logs/                    # 租户日志目录
```

```bash
# 1. 询问租户目录位置
"请指定租户目录位置（由智能体安排）："
"示例 1（私域方案 A）：<WORKSPACE>/user1"
"示例 2（私域方案 A）：<WORKSPACE>/user2"
"示例 3（工作区方案 B）：<WORKSPACE>/.cortex/user3"

# 2. 创建租户目录结构（使用绝对路径）
# 方案 A（私域管理）：
mkdir -p <TENANT-WSPACE>/cortex_data/{strategies,backtest,logs}

# 方案 B（工作区统一管理）：
mkdir -p <TENANT-WSPACE>/{strategies,backtest,logs}

# 3. 创建租户配置文件
# 方案 A（私域管理）：
cat > <TENANT-WSPACE>/cortex_data/cortex_cli.conf << 'EOF'
[main]
data_dir = .
adapter = pyqdt
log_level = INFO
log_file = logs/cortex.log

[strategies]
initial_cash = 1000000
fq = post
mode = loose

[pyqdt]
data_path = /data/QuantData/pyqdt_csv
EOF

# 方案 B（工作区统一管理）：
cat > <TENANT-WSPACE>/cortex_cli.conf << 'EOF'
[main]
data_dir = .
adapter = pyqdt
log_level = INFO
log_file = logs/cortex.log

[strategies]
initial_cash = 1000000
fq = post
mode = loose

[pyqdt]
data_path = /data/QuantData/pyqdt_csv
EOF

# 4. 更新 TOOLS.md 登记（记录实际使用的租户目录）
```

### 步骤 5：更新 TOOLS.md 登记

**配置完成后，必须在 TOOLS.md 中登记：**

```markdown
## Cortex 回测引擎

### 场景模式
**当前使用：场景 X（场景名称）**

### 安装位置
| 项目 | 路径 |
|------|------|
| CLI 工具 | `/opt/cirt/bin/cortex_cli.py` |
| Python 库 | `/opt/cirt/lib/cortex/` |

### 配置信息
[根据场景填写具体路径]

### 使用方法
[根据场景填写使用命令]
```

---

## 使用流程图

```
用户触发技能
    ↓
查阅经验文档 (references/cortex-experience.md)  ← ⚠️ 必读！
    ↓
读取 TOOLS.md 检查场景配置
    ↓
├─ 已配置场景 ──→ 检查配置文件是否存在
│                      ↓
│              ├─ 存在 ──→ 正常使用
│              └─ 不存在 ──→ 引导建立流程
│
└─ 未配置场景 ──→ 询问用户选择场景（1/2/3）
                       ↓
              用户选择场景 ──→ 执行建立流程
                       ↓
              更新 TOOLS.md 登记
                       ↓
              配置完成，正常使用
    ↓
使用完成后，发现新问题追加到经验文档
```

## 文档索引

| 文档 | 说明 | 何时使用 |
|------|------|----------|
| [references/cortex-experience.md](references/cortex-experience.md) | **⚠️ 使用经验文档** - 系统预置经验(编号<100) + 使用收集经验(编号≥100) | **每次使用前必读** |
| [references/cortex-api-reference.md](references/cortex-api-reference.md) | **策略代码 API** - 回调函数、下单函数、数据函数、与聚宽差异 | 编写策略代码或检查 API 兼容性 |
| [references/cortex-cli-usage.md](references/cortex-cli-usage.md) | **CLI 使用方法** - 命令参数、配置文件、回测输出 | 运行回测或调试 CLI |

> **重要**：经验编号<100为系统预置，编号≥100为使用收集。每次使用前先查阅，使用后发现新问题从100开始追加。

> **注意：** 首次设置向导已合并到本 SKILL.md 文档中，无需单独查阅 setup-guide.md

---

## 策略执行模式说明

Cortex CLI 支持两种策略指定方式：

### 模式 1：strategy_id 模式（推荐）

**使用条件：**
- 策略文件必须放在 `<DATA-DIR>/strategies/` 目录下
- `<DATA-DIR>` 由配置文件中的 `data_dir` 参数指定
- 策略文件名格式：`<strategy_id>.py`

**命令格式：**
```bash
python /opt/cirt/bin/cortex_cli.py backtest \
    --strategy <strategy_id> \
    --start-date 20260101 \
    --end-date 20260331 \
    --initial-cash 1000000
```

**示例：**
```bash
# 策略文件位置：<DATA-DIR>/strategies/double_ma.py
python /opt/cirt/bin/cortex_cli.py backtest \
    --strategy double_ma \
    --start-date 20260101 \
    --end-date 20260331
```

### 模式 2：绝对路径模式

**使用条件：**
- 策略文件可以放在任意位置
- 使用策略文件的绝对路径

**命令格式：**
```bash
python /opt/cirt/bin/cortex_cli.py backtest \
    --strategy /absolute/path/to/strategy.py \
    --start-date 20260101 \
    --end-date 20260331 \
    --initial-cash 1000000
```

**示例：**
```bash
python /opt/cirt/bin/cortex_cli.py backtest \
    --strategy /home/user/strategies/my_strategy.py \
    --start-date 20260101 \
    --end-date 20260331
```

### data_dir 与策略目录的关系

```
<DATA-DIR>/                    # 由 data_dir 配置指定
├── cortex_cli.conf           # 配置文件
├── strategies/               # 策略目录（strategy_id 模式必须）
│   ├── double_ma.py
│   └── ma5_strategy.py
└── backtest/                 # 回测输出目录
    └── <strategy_id>-001/
```

**重要：**
- `data_dir = .` 表示配置文件所在目录为数据目录
- 策略文件放在 `<DATA-DIR>/strategies/` 下时，可使用 strategy_id 模式
- 策略文件放在其他位置时，必须使用绝对路径模式

---

## Quick Start

```bash
# 回测示例（strategy_id 模式）
python /opt/cirt/bin/cortex_cli.py backtest \
    --config <TENANT-WSPACE>/cortex_data/cortex_cli.conf \
    --strategy ma5_strategy \
    --start-date 20250701 \
    --end-date 20260331 \
    --period daily \
    --mode loose \
    --initial-cash 1000000
```

**回测输出位置：** `<DATA-DIR>/backtest/<strategy_id>-001/`

**输出文件：**
- `account.csv` - 账户每日状态
- `positions.csv` - 持仓每日明细
- `summary.json` - 回测摘要
- `run.log` - 策略运行日志

---

## 回测结果回显报告格式

回测完成后，按以下格式回显报告：

```
📊 回测结果报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
策略名称: <strategy_id>
回测区间: <start_date> ~ <end_date>
回测频率: <period> (daily/min)
撮合模式: <mode> (loose/strict)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 收益统计
------------------------------------------------------------
初始资金:       <initial_cash>
最终市值:       <final_value>
总收益率:       <total_return>%
年化收益率:     <annual_return>%
最大回撤:       <max_drawdown>%
夏普比率:       <sharpe_ratio>
------------------------------------------------------------

📝 交易统计
------------------------------------------------------------
交易次数:       <trade_count>
盈利次数:       <win_count>
亏损次数:       <loss_count>
胜率:           <win_rate>%
平均盈利:       <avg_profit>
平均亏损:       <avg_loss>
盈亏比:         <profit_loss_ratio>
------------------------------------------------------------

📂 输出位置
------------------------------------------------------------
<DATA-DIR>/backtest/<strategy_id>-001/
  ├── account.csv      (账户每日状态)
  ├── positions.csv    (持仓每日明细)
  ├── summary.json     (回测摘要数据)
  └── run.log          (策略运行日志)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**数据来源：** `summary.json`

---

## 聚宽兼容策略格式

Cortex 策略代码采用聚宽兼容格式，支持聚宽风格的对象和方法。

> **详细 API 参考：** [references/cortex-api-reference.md](references/cortex-api-reference.md)

**支持的 API 类别：**
- 策略回调函数（initialize / handle_data / after_trading_end）
- 策略设置函数（set_benchmark / set_option / set_order_cost）
- 数据获取函数（get_price / get_bars）
- 下单函数（order_target_value / order_shares）
- Context / Portfolio / Position 对象
- 全局变量 g / log

---

## 使用引导流程

当用户发起回测请求时，遵循以下引导原则：

### 第一步：策略描述与决策点分析

**当用户提供策略描述时，按以下流程引导：**

1. **分析策略原理** - 理解用户描述的策略逻辑
2. **识别决策点** - 找出需要用户明确的关键决策
3. **逐项询问决策点** - 不假设，让用户选择

**常见决策点清单：**

| 决策点 | 问题示例 | 常见选项 |
|--------|----------|----------|
| 标的池 | 回测哪些股票？ | 全A股/沪深300/中证500/自定义股票池 |
| 信号生成 | 信号如何触发？ | 指标交叉/阈值突破/多因子组合 |
| 仓位管理 | 如何分配仓位？ | 等权/市值加权/风险平价 |
| 择时逻辑 | 是否择时？ | 满仓/择时减仓/动态调整 |
| 止损止盈 | 是否设置止损止盈？ | 有/无，具体阈值 |
| 调仓频率 | 多久调仓一次？ | 日度/周度/月度/信号触发 |
| 过滤条件 | 哪些股票不买？ | ST/停牌/涨跌停/新股 |

**引导示例：**
```
用户: "我想做一个双均线策略"

Agent: "理解您的策略思路，以下是需要明确的决策点：

1. **标的池**：回测哪些股票？
   - 全A股
   - 沪深300成分股
   - 中证500成分股
   - 其他股票池（请说明）

2. **均线参数**：使用哪两条均线？
   - MA5/MA20（短线）
   - MA10/MA60（中线）
   - 自定义参数（请说明）

3. **信号逻辑**：
   - 金叉买入、死叉卖出（标准）
   - 其他逻辑（请说明）

4. **仓位管理**：
   - 单只股票仓位：等权/按市值加权
   - 最大持仓数量：不限/固定数量（请说明）

5. **调仓频率**：
   - 每日检查信号
   - 每周调仓
   - 其他频率（请说明）

6. **过滤条件**：
   - 是否排除ST、停牌、涨跌停股票？
   - 是否排除新股（上市不足N天）？

请逐项确认或补充您的选择。"
```

### 第二步：标的域确认

| 标的域类型 | 说明 | 数据来源 |
|------------|------|----------|
| 全A股 | 沪深两市所有股票 | `get_all_securities()` |
| 沪深300 | 沪深300指数成分股 | `get_index_stocks('000300.XSHG')` |
| 中证500 | 中证500指数成分股 | `get_index_stocks('000905.XSHG')` |
| 中证1000 | 中证1000指数成分股 | `get_index_strokes('000852.XSHG')` |
| 股票池文件 | 用户自定义股票列表 | 从文件读取 |
| 基金 | 场内基金/ETF | 需确认代码范围 |
| 债券 | 可转债等 | 需确认代码范围 |

**询问示例：**
```
请确认回测标的域：
1. 全A股
2. 沪深300成分股
3. 中证500成分股
4. 中证1000成分股
5. 自定义股票池（请提供文件路径或股票列表）
```

### 第三步：聚宽兼容性确认

**询问用户：**
```
策略代码是否需要完全兼容聚宽平台？

1. **完全兼容** - 代码可直接复制到聚宽平台运行
   - 使用聚宽标准API
   - 遵守聚宽代码规范
   - 注意：Cortex与聚宽存在少量差异

2. **仅Cortex运行** - 仅在Cortex引擎运行，无需聚宽兼容
   - 可使用Cortex特有功能
   - 不考虑聚宽兼容性

请选择兼容性要求。
```

**Cortex与聚宽主要差异提醒：**
| 功能 | 聚宽 | Cortex | 影响 |
|------|------|--------|------|
| `handle_data` | 每日推送bar数据 | 不触发，需用`run_daily` | ⚠️ 代码结构需调整 |
| `context.portfolio.total_assets` | ✅ 支持 | ❌ 不支持 | 用 `total_value` 替代 |
| 分钟级回测 | ✅ 支持 | ⚠️ 效率极低 | 建议用Python版 |
| 复权默认值 | 前复权 | 后复权 | 需显式设置 |

### 第四步：必需参数检查

| 参数 | 说明 | 引导提示 |
|------|------|----------|
| `--strategy` | 策略名称或路径 | "请提供策略文件路径或策略名称" |
| `--start-date` | 开始日期 | "请提供开始日期（格式 YYYYMMDD）" |
| `--end-date` | 结束日期 | "请提供结束日期（格式 YYYYMMDD）" |
| `--period` | 回测频率 | `daily`（日线）或 `min`（分钟线） |
| `--mode` | 撮合模式 | `loose`（宽松）或 `strict`（严谨） |

### ⚠️ 引导原则

1. **询问时提供参考值** - 附带推测值或配置文件默认值，方便用户决策
2. **不要随意替用户设置参数** - 特别是资金、日期范围、策略参数
3. **缺少必需参数时，询问用户** - 提供清晰问题 + 参考值
4. **可选参数有默认值** - 从配置文件读取，无需每次询问
5. **策略代码细节不完整** - 引导用户提供策略文件或明确需求
6. **决策点必须询问** - 不假设用户的策略细节，逐项确认

### 完整引导示例

**❌ 错误做法：**
```
用户: "回测一个双均线策略"
Agent: 直接运行回测，使用默认日期和资金...  # ❌ 随意替用户决定
```

**✅ 正确做法：**
```
用户: "回测一个双均线策略"

Agent: "理解您的需求，让我逐步确认策略细节：

**第一步：策略描述分析**
双均线策略的核心逻辑是：短期均线上穿长期均线买入，下穿卖出。

需要确认的决策点：

1. **标的域**：
   - 全A股
   - 沪深300成分股
   - 中证500成分股
   - 中证1000成分股
   - 自定义股票池

2. **均线参数**：
   - MA5/MA20（短线）
   - MA10/MA60（中线）
   - 自定义（请说明）

3. **仓位管理**：
   - 单只股票仓位上限
   - 最大持仓数量
   - 是否等权分配

4. **调仓频率**：每日/每周/信号触发？

5. **过滤条件**：是否排除ST/停牌/涨跌停？

**第二步：聚宽兼容性**
策略代码是否需要完全兼容聚宽平台？
- 完全兼容（可复制到聚宽运行）
- 仅Cortex运行

**第三步：回测参数**
- 开始日期（格式：YYYYMMDD）
- 结束日期（格式：YYYYMMDD）
- 回测频率（daily 日线 | min 分钟线）
- 撮合模式（loose 宽松 | strict 严谨）
- 初始资金（参考：1000000）

请逐项确认或补充您的选择。"
```

---

## 策略代码示例

```python
def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    set_order_cost(OrderCost(
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        min_commission=5
    ), type='stock')
    
    g.stock = '000001.XSHE'
    run_daily(rebalance, time='open')

def rebalance(context):
    prices = get_price(g.stock, count=20)
    ma5 = prices['close'].tail(5).mean()
    ma20 = prices['close'].tail(20).mean()
    
    if ma5 > ma20:
        order_target_value(g.stock, context.portfolio.total_assets * 0.8)
    else:
        order_target_value(g.stock, 0)

def after_trading_end(context):
    log.info(f"总资产: {context.portfolio.total_assets:.2f}")
```

---

## ⚠️ 与聚宽差异

| 功能 | 聚宽 | Cortex | 说明 |
|------|------|--------|------|
| **驱动模式** | 数据推送 | 数据+时间双重驱动 | `handle_data` 不附带 bar 数据 |
| **默认复权** | 前复权 (pre) | 后复权 (post) | 未设置 `use_real_price` 时 |
| **撮合模式** | 宽松 | 宽松 + 严谨双模式 | 支持 strict 模式 |
| **数据源** | 聚宽内部 | pyqdt 本地数据 | 数据来源不同 |

> **详细差异说明见** [references/cortex-api-reference.md](references/cortex-api-reference.md)

---

## 配置文件位置

| 文件 | 说明 |
|------|------|
| `<CORTEX-INSTALL-DIR>/etc/cortex.conf` | 统一配置文件（推荐） |
| `<CORTEX-INSTALL-DIR>/etc/cortex_cli.conf` | CLI 专用配置（兼容） |
| `<CORTEX-INSTALL-DIR>/bin/cortex_cli.conf` | 脚本目录配置 |
| `/etc/cortex.conf` | 系统配置 |

**配置查找顺序：** `<CORTEX-INSTALL-DIR>/etc/` → `/etc/`

---

> **详细配置指南见** [首次设置向导](#首次设置向导重要) 章节