# fwquant-skills

## 功能描述

FWQuant 量化分析技能包，提供专业的量化策略分析和信号生成功能，支持多标的、多时间周期的量化分析。

## 核心功能列表

| 功能名称 | 命令格式 | 功能描述 | 状态 |
|----------|----------|----------|------|
| Web服务启动 | `fwquant web run` | 启动 FWQuant Web 可视化服务，提供策略监控和信号查看界面 | 已实现 |
| 策略回测 | `fwquant backtest` | 对指定策略进行历史回测，生成回测报告 | 已实现 |
| 信号生成 | `fwquant signal` | 基于策略生成实时交易信号 | 已实现 |
| 参数优化 | `fwquant optimize` | 策略参数优化，寻找最优参数组合 | 开发中 |
| 策略训练 | `fwquant train` | 使用机器学习训练策略模型 | 开发中 |
| 实盘连接 | `fwquant connect` | 连接交易所进行实盘交易 | 开发中 |
| 风险评估 | `fwquant risk` | 策略风险评估和压力测试 | 开发中 |
| 组合分析 | `fwquant portfolio` | 多策略组合分析和优化 | 开发中 |

## 使用场景

适用于需要进行量化策略分析、信号生成、回测验证等量化交易场景。

## 输入参数

### 通用参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| action | string | analyze | 执行动作：analyze/backtest/signal/web |
| symbol | string | BTC-USDT | 交易标的 |
| timeframe | string | 1h | 时间周期 |
| strategy | string | default | 策略名称 |

### 回测参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| start_date | string | - | 回测开始日期 (YYYY-MM-DD) |
| end_date | string | - | 回测结束日期 (YYYY-MM-DD) |
| initial_capital | float | 10000 | 初始资金 |

### Web服务参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| host | string | 0.0.0.0 | 服务绑定地址 |
| port | integer | 8080 | 服务端口 |

## 输出结果

- success: 执行是否成功
- message: 执行结果消息
- data: 包含分析结果的字典
- action: 执行的动作类型

## 使用示例

```bash
# 启动 Web 服务
openclaw agent --agent main --message "@fwquant-skills action=web host=0.0.0.0 port=8080"

# 执行策略回测
openclaw agent --agent main --message "@fwquant-skills action=backtest symbol=BTC-USDT timeframe=4h strategy=momentum start_date=2024-01-01 end_date=2024-12-31"

# 生成交易信号
openclaw agent --agent main --message "@fwquant-skills action=signal symbol=ETH-USDT timeframe=1h strategy=rsi"

# 执行量化分析
openclaw agent --agent main --message "@fwquant-skills symbol=BTC-USDT timeframe=4h strategy=momentum"
```

## 扩展预留

以下功能模块预留待开发：
- [ ] 机器学习策略训练模块
- [ ] 多交易所实盘对接
- [ ] 智能风控系统
- [ ] 策略组合优化引擎
- [ ] 量化策略推荐系统