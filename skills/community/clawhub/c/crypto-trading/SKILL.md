# CryptoTrading AI 交易代理技能

> PAI CryptoTrading 项目的核心交易决策技能
> @version 1.0.0

## 🎯 目标
- 每 10 分钟自动执行交易决策循环
- 整合 Dify AI + OpenClaw 双分析
- 应用经验规则 (R001-R006) 验证决策
- 自动记录决策和交易结果

## 📋 核心流程

### 1. 行情获取 (Data Collection)
```
- 获取 BTC/ETH/BNB 1h K 线数据
- 获取订单簿深度数据
- 计算技术指标：RSI, MACD, 布林带
- 获取账户持仓和余额
```

### 2. AI 决策 (AI Decision)
```
- 调用 Dify AI 获取市场分析
- 调用 OpenClaw (qwen3.5-plus) 获取独立分析
- 对比两种分析结果
- 生成最终决策：BUY/SELL/HOLD
```

### 3. 规则验证 (Rule Validation)
```
R001: 4h 趋势过滤 - 1h 信号必须与 4h 同向
R002: 置信度校准 - 单一指标上限 0.55
R003: 交易频率控制 - 单币种每日≤3 笔
R004: 止损纪律 - 5% 止损，盈利 10% 移动止损
R005: 仓位管理 - 单币种≤25%，默认 10%
R006: 聚焦主流币 - BTC/ETH/BNB
```

### 4. 交易执行 (Trade Execution)
```
- 计算交易数量 (使用 order_amount.py)
- 执行市价单
- 记录执行结果
- 更新持仓状态
```

### 5. 记忆记录 (Memory Logging)
```
- 保存决策到 memory/trading/YYYY-MM-DD.md
- 更新 memory/crypto_trading_state.json
- 双分析对比落库 (ai_analysis_comparison 表)
```

## 🔧 工具
- `core/data_collector.py` - 行情数据收集
- `core/autonomous_ai.py` - AI 决策引擎
- `core/enhanced_trade_executor.py` - 交易执行器
- `core/risk_manager.py` - 风险管理
- `core/experience_analyzer.py` - 经验分析器
- `validate_ct_execution.py` - 执行验证脚本

## 📊 成功标准
- ✅ 每 10 分钟完成一次决策循环
- ✅ 双分析对比落库成功
- ✅ 交易执行准确率 > 95%
- ✅ 止损执行率 100%

## 🔄 改进记录
| 日期 | 改进内容 |
|------|----------|
| 2026-03-03 | 修复 position_size 计算错误 |
| 2026-03-03 | 添加 OpenClaw 双分析对比 |
| 2026-03-02 | 实现经验规则 R001-R006 |

## 📁 相关文件
- `/Users/zst/Documents/ML/CryptoTrading/` - 主项目目录
- `/Users/zst/clawd/memory/trading/` - 交易日志
- `/Users/zst/clawd/memory/trading_rules.md` - 规则库
- `/Users/zst/clawd/memory/trading_mistakes.md` - 错误清单
