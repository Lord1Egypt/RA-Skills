# OpenClaw

OpenClaw 是一个基于 Tushare 的黄金动态定投 skill 原型，当前默认使用黄金 ETF `518880.SH` 作为主执行标的。

## 初始设计

- 数据源：Tushare
- 主标的：`518880.SH`
- 节奏：日收盘后评估，默认推荐按周执行，也可由用户自定义
- 输出：一个有上下限的动态定投倍率和建议金额

## 数据方案

- 主执行标的：`518880.SH`
- 主数据接口：Tushare `fund_daily`
- 可选参考锚：上海黄金交易所 `Au99.99`
- `Au99.99` 参考数据接口：Tushare `sge_daily`

策略应优先根据 ETF 自身的数据生成信号，因为实际执行的就是这个标的。如果以后加入 `Au99.99`，它更适合作为辅助校验，而不是替代 ETF 主信号。

## 长期背景参考

黄金长期历史回报常被概括为“约 8% 左右”，这类数据可以作为为什么长期配置黄金的背景依据，但不应直接放进日常动态定投公式。

更稳妥的理解方式是：

- 它属于长期配置层的背景参考
- 它不属于日度或周度的交易触发信号
- 它可以帮助设定长期预期，但不能直接决定本期该投 `1.2x` 还是 `0.7x`

因此在 OpenClaw 中，这类长期统计只作为说明信息存在，不参与核心倍率、布林修正或 MACD 确认逻辑。

## 建议模型

当前使用一个三层规则模型：

- 核心状态：由 `MA20`、`MA60`、`RSI14` 和 60 日回撤决定
- 布林修正：根据价格在布林通道中的相对位置进行加减
- MACD 确认：只在极端状态下做确认，不单独主导决策

初始核心倍率如下：

- `oversold`：`1.6`
- `weak`：`1.2`
- `neutral`：`1.0`
- `hot`：`0.7`

然后继续叠加：

- 布林修正：`+0.2`、`+0.1`、`0`、`-0.1`、`-0.2`
- MACD 修正：`+0.1`、`0`、`-0.1`
- 最终倍率裁剪区间：`0.6 ~ 1.8`

## 当前原型

仓库中的 [scripts/openclaw.py](/C:/Users/EgonHomePC/Documents/GitHub/AUsub/scripts/openclaw.py) 目前可以：

- 读取本地 JSON 配置
- 使用 Tushare 获取最近日线
- 计算 `MA20`、`MA60`、`RSI14`、布林线、`MACD` 和 60 日回撤
- 输出一个受限范围内的动态定投建议 JSON
- 在输出中明确区分：
  - 基于场内黄金 ETF `518880.SH` 的主行情指标表
  - 基于上海黄金交易所 `Au99.99` 的参考行情区块

## 使用方式

## 环境变量

- `TUSHARE_TOKEN`：必填。用于访问 Tushare 行情数据。
- `OPENCLAW_CONFIG`：可选。自定义策略配置文件路径。
- `OPENCLAW_USER_ID`：可选。用户定投方案 ID，对应 `memory/users/<id>.json`。
- `OPENCLAW_HISTORY_PATH`：可选。回测历史数据 CSV 路径。
- `OPENCLAW_SYMBOL`：可选。主执行标的，默认 `518880.SH`。

说明：

- 安装其他 Tushare 相关 skill，并不等于当前项目会自动获得可用的 `TUSHARE_TOKEN`。
- 只有当当前运行环境已经正确设置并可访问 `TUSHARE_TOKEN` 时，OpenClaw 才能正常调用 Tushare。

安装依赖：

```bash
pip install tushare
```

设置 Token：

```bash
set TUSHARE_TOKEN=your_token_here
```

运行原型：

```bash
python scripts/openclaw.py
```

如果你要结合某个用户的定投方案一起生成建议：

```bash
set OPENCLAW_USER_ID=demo_user
python scripts/openclaw.py
```

如果你想指定自定义配置文件：

```bash
set OPENCLAW_CONFIG=C:\path\to\your-config.json
python scripts/openclaw.py
```

## 用户记忆配置

如果后续要把不同用户的定投方案分开管理，建议采用“每个用户一份记忆配置”的方式管理。

推荐目录：

```text
memory/
|---- users/
|     |---- template.json
|     |---- demo_user.json
```

建议记忆配置分成几部分：

- 用户基础信息
- 定投方案
- 场内 / 场外执行偏好
- 风险边界
- 方案来源说明

这样做的好处是：

- 公共策略和个人账户状态解耦
- 后续可以支持多个用户
- 不需要每次维护持仓快照
- 方便以后做日报、周报和自动化

## 默认方案与自定义

当前项目中的这些设置：

- `weekly_thursday_if_trading`
- 基础金额 `1000`

都应被理解为默认推荐方案，而不是必须固定使用的唯一方案。

用户可以直接自定义：

- 定投节奏
- 基础金额
- 是否优先场内 ETF
- 是否允许场外先积累再转入场内
- 场外转场内阈值

如果用户还没有方案，也可以先把这些信息告诉 openclaw：

- 可用于投资的预算范围
- 计划中的其他投资
- 对黄金的配置想法

然后由模型先给一个建议方案，待用户确认后，再写入用户配置文件。

说明：

- 不建议把收入、支出、存款等敏感财务信息持久化写入用户配置文件。
- 如果用户希望模型参考这类信息，更适合在一次性对话中临时提供，再由用户确认最终方案参数。

## 下一步建议

建议继续做这几件事：

1. 根据日期切换普通日报和周三执行前日报
2. 结合本地历史数据优化回测指标和执行日规则
3. 加入日报或周报自动化

## 回测说明

当前仓库已提供一个最小回测结构：

- [scripts/fetch_history.py](/C:/Users/EgonHomePC/Documents/GitHub/AUsub/scripts/fetch_history.py)
- [scripts/backtest.py](/C:/Users/EgonHomePC/Documents/GitHub/AUsub/scripts/backtest.py)

推荐流程：

1. 先从 Tushare 拉取 `518880.SH` 历史日线并保存到本地
```bash
set TUSHARE_TOKEN=your_token_here
python scripts/fetch_history.py
```

2. 再基于本地 CSV 做回测，不重复消耗 Tushare 次数
```bash
python scripts/backtest.py
```

这个最小回测会把动态定投和固定定投做一个基础对比，用来帮助判断：

- 当前阈值是否过于敏感
- 动态倍率区间是否合理
- 相比固定定投是否有明显差异

## 风险说明

这个项目应该被视为一个纪律化执行辅助工具，而不是主观择时或收益保证工具。
