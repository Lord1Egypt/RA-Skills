---
name: a-share-trader
description: A股核心交易框架，整合12种选股策略的自适应量化交易系统
version: 1.0.0
author: assistant
permissions: 需要股票数据访问和交易权限
---

# A股核心交易框架

## 概述
基于用户提供的12种选股策略，结合自适应交易引擎，构建的A股量化交易系统。系统具备市场状态识别、策略动态切换、风险自适应控制等高级功能。

## 整合策略列表
1. **基本面选股策略** - 质量+增长双因子
2. **防御选股策略** - 高股息价值投资
3. **震荡选股策略** - KDJ技术指标
4. **小市值策略** - 月度切换的小市值轮动
5. **基本面加小市值** - 质量小市值混合
6. **小市值成长** - 小市值成长股精选
7. **营收利润双增** - 增长质量策略
8. **价值成长** - 价值成长平衡
9. **控盘策略** - 筹码集中度选股
10. **社保重仓** - 机构跟随策略
11. **超跌反弹** - 均值回归策略
12. **时空共振策略** - 四维度综合模型

## 核心特性
- **自适应市场感知**：识别牛熊市、震荡市等不同市场状态
- **策略动态权重**：根据不同市场环境自动调整策略权重
- **智能参数调整**：基于市场状态动态调整策略阈值
- **多维度风控**：个股、行业、组合多层风控
- **学习优化机制**：从交易绩效中持续学习优化

## 系统架构
```
A股核心交易框架/
├── core/                  # 核心引擎
│   ├── a_share_trader.py  # 主交易引擎
│   ├── adaptive_engine.py # 自适应引擎
│   └── data_interface.py  # A股数据接口
├── strategies/            # 策略模块
│   ├── __init__.py
│   ├── base_strategy.py   # 策略基类
│   ├── fundamental.py     # 基本面策略
│   ├── defensive.py       # 防御策略
│   ├── swing_trading.py   # 震荡策略
│   ├── small_cap.py       # 小市值策略
│   ├── quality_small_cap.py # 质量小市值
│   ├── small_cap_growth.py # 小市值成长
│   ├── revenue_profit.py  # 营收利润双增
│   ├── value_growth.py    # 价值成长
│   ├── chip_concentration.py # 控盘策略
│   ├── social_security.py # 社保重仓
│   ├── oversold_rebound.py # 超跌反弹
│   └── resonance.py       # 时空共振策略
├── risk_management/       # 风险管理
│   ├── core.py            # 风控核心
│   ├── position.py        # 仓位控制
│   └── stop_loss.py       # 止损策略
├── config/                # 配置
│   └── trading_config.py  # 交易配置
├── utils/                 # 工具函数
├── tests/                 # 测试
└── examples/              # 使用示例
```

## 调用方式
在智能体提示中直接请求执行此技能，例如：
> "请运行A股交易框架进行模拟交易"
> "使用A股框架分析当前市场状态"
> "执行A股策略回测"

## 数据需求
- A股实时行情数据
- 基本面数据（财务指标）
- 技术指标数据
- 市场情绪数据（可选）

## 输出示例
```json
{
  "status": "running",
  "market_state": "weak_bull",
  "state_confidence": 0.72,
  "active_strategies": 8,
  "portfolio_value": 10000000000,
  "total_return": 0.15,
  "max_drawdown": 0.08,
  "active_positions": 12
}
```

## 注意事项
1. 系统为量化交易框架，实盘交易需谨慎
2. 需要可靠的数据源支持
3. 建议先进行充分的回测和模拟交易
4. 注意市场风险，控制仓位和回撤