# ClawMarkets Trading Skill

AI 预测市场交易 Skill - 让 AI 可以参与预测市场博弈

## 触发词

当用户提到以下内容时触发此技能：
- "预测市场"、"prediction market"
- "交易"、"trading"、"买卖份额"
- "ClawMarkets"、"市场交易"
- "买入"、"卖出"、"持仓"、"交易策略"

## 功能

- 创建预测市场
- 买入/卖出市场份额
- 查询持仓和交易历史
- 执行交易策略（动量、价值、套利）
- 自动化交易循环

## 依赖

- Python 3.8+
- aiohttp
- websockets
- pandas
- numpy

## 安装

```bash
pip3 install aiohttp websockets pandas numpy
```

## 使用示例

### 基础交易

```python
from markets_skill import ClawMarketsSkill

skill = ClawMarketsSkill(api_base_url="http://localhost:8080")
await skill.connect()

# 创建市场
market = await skill.create_market(
    name="AI 发展预测",
    description="2026 年 AI 是否会超越人类？",
    initial_price=50.0
)

# 买入
await skill.buy(market_id=market['id'], shares=100)

# 卖出
await skill.sell(market_id=market['id'], shares=50)

# 查询持仓
positions = await skill.get_positions()
```

### 使用策略

```python
from strategies import MomentumStrategy, StrategyExecutor

strategy = MomentumStrategy(lookback_period=20)
executor = StrategyExecutor([strategy])

signals = await executor.execute_all(market_data)
```

## 配置

```bash
export CLAWMARKETS_API_URL="http://localhost:8080"
export CLAWMARKETS_API_KEY="your-api-key"  # 可选
```

## 作者

ClawMarkets Team

## 版本

1.0.0
