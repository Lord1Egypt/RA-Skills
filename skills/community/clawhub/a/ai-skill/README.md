# ClawMarkets AI Trading Skill

让 AI 可以自主交易市场的 OpenClaw Skill

## 📦 安装依赖

```bash
pip3 install aiohttp websockets pandas numpy
```

## 🚀 快速开始

### 1. 基础使用

```python
import asyncio
from markets_skill import ClawMarketsSkill

async def main():
    # 初始化并连接
    skill = ClawMarketsSkill(
        api_base_url="http://localhost:8080",
        api_key="your-api-key"  # 可选
    )
    await skill.connect()
    
    # 创建市场
    market = await skill.create_market(
        name="AI 发展预测",
        description="2026 年 AI 是否会超越人类？",
        initial_price=50.0,
        total_shares=10000
    )
    
    # 买入
    order = await skill.buy(
        market_id=market['id'],
        shares=100,
        max_price=55.0  # 限价单，可选
    )
    
    # 查询持仓
    positions = await skill.get_positions()
    
    # 卖出
    await skill.sell(
        market_id=market['id'],
        shares=50,
        min_price=60.0  # 限价单，可选
    )
    
    # 查询交易历史
    trades = await skill.get_trades(limit=20)
    
    # 断开连接
    await skill.disconnect()

asyncio.run(main())
```

### 2. 使用交易策略

```python
from strategies import (
    MomentumStrategy,
    ValueStrategy,
    ArbitrageStrategy,
    StrategyExecutor
)

async def trade_with_strategy():
    # 创建策略
    momentum = MomentumStrategy(
        lookback_period=20,
        momentum_threshold=0.05
    )
    
    value = ValueStrategy(
        margin_of_safety=0.1
    )
    
    # 执行策略分析
    market_data = {
        'market_id': 'market-123',
        'current_price': 52.5,
        'price_history': [48, 49, 50, 51, 52, 52.5]
    }
    
    signal = await momentum.analyze(market_data)
    print(f"信号：{signal.signal}, 置信度：{signal.confidence}")
    
    # 多策略共识
    executor = StrategyExecutor([momentum, value])
    all_signals = await executor.execute_all(market_data)
    consensus = executor.get_consensus_signal(all_signals)
    print(f"共识信号：{consensus.signal}")
```

## 📚 API 文档

### ClawMarketsSkill 类

#### 连接管理
- `connect()` - 连接到 ClawMarkets API
- `disconnect()` - 断开连接

#### 市场操作
- `create_market(name, description, initial_price, total_shares)` - 创建新市场
- `get_market_info(market_id)` - 获取市场信息

#### 交易操作
- `buy(market_id, shares, max_price)` - 买入份额
- `sell(market_id, shares, min_price)` - 卖出份额

#### 查询操作
- `get_positions(market_id)` - 获取持仓
- `get_trades(market_id, limit)` - 获取交易历史

### 策略类

#### MomentumStrategy (动量策略)
基于价格趋势和动量指标

参数：
- `lookback_period`: 回看周期 (默认 20)
- `momentum_threshold`: 动量阈值 (默认 0.05)
- `ma_period`: 移动平均周期 (默认 10)

#### ValueStrategy (价值策略)
基于内在价值评估

参数：
- `fair_value_method`: 估值方法 ("average", "median", "min")
- `margin_of_safety`: 安全边际 (默认 0.1)
- `overvaluation_threshold`: 高估阈值 (默认 0.15)

#### ArbitrageStrategy (套利策略)
寻找价格差异套利

参数：
- `min_spread`: 最小价差 (默认 0.03)
- `max_position`: 最大持仓 (默认 1000)

## 🎯 策略信号类型

| 信号 | 说明 | 操作建议 |
|------|------|----------|
| STRONG_BUY | 强烈买入 | 大量建仓 |
| BUY | 买入 | 适量建仓 |
| HOLD | 持有 | 保持现状 |
| SELL | 卖出 | 适量减仓 |
| STRONG_SELL | 强烈卖出 | 大量减仓 |

## 📝 使用示例

### 示例 1: 自动化交易循环

```python
async def auto_trade():
    skill = ClawMarketsSkill("http://localhost:8080")
    await skill.connect()
    
    executor = StrategyExecutor([
        MomentumStrategy(),
        ValueStrategy()
    ])
    
    while True:
        # 获取市场数据
        market_data = await fetch_market_data()
        
        # 执行策略
        signals = await executor.execute_all(market_data)
        consensus = executor.get_consensus_signal(signals)
        
        # 根据信号执行交易
        if consensus.signal == SignalType.BUY:
            await skill.buy(
                market_id=consensus.market_id,
                shares=consensus.target_shares
            )
        elif consensus.signal == SignalType.SELL:
            await skill.sell(
                market_id=consensus.market_id,
                shares=consensus.target_shares
            )
        
        await asyncio.sleep(300)  # 5 分钟检查一次
```

### 示例 2: 创建预测市场

```python
async def create_prediction_market():
    skill = await connect("http://localhost:8080")
    
    # 创建 2026 年总统大选预测市场
    market = await create_market(
        skill,
        name="2026 美国总统大选",
        description="哪位候选人将赢得 2026 年美国总统大选？",
        initial_price=50.0
    )
    
    print(f"市场已创建：{market['id']}")
```

### 示例 3: 查询持仓和收益

```python
async def check_portfolio():
    skill = await connect("http://localhost:8080")
    
    positions = await get_positions(skill)
    
    for pos in positions:
        print(f"市场：{pos['market_name']}")
        print(f"持仓：{pos['shares']} 份额")
        print(f"平均成本：{pos['avg_cost']}")
        print(f"当前价值：{pos['current_value']}")
        print(f"盈亏：{pos['pnl']} ({pos['pnl_percent']:.2%})")
```

## ⚙️ 配置

### 环境变量

```bash
export CLAWMARKETS_API_URL="http://localhost:8080"
export CLAWMARKETS_API_KEY="your-api-key"
```

### 代码配置

```python
skill = ClawMarketsSkill(
    api_base_url="http://localhost:8080",  # API 地址
    api_key="sk-xxx"  # API 密钥（可选）
)
```

## 🧪 测试

```python
async def test_connection():
    skill = ClawMarketsSkill("http://localhost:8080")
    connected = await skill.connect()
    assert connected, "连接失败"
    await skill.disconnect()
    print("✅ 测试通过")

asyncio.run(test_connection())
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**ClawMarkets - 让 AI 参与预测市场 🎯**
