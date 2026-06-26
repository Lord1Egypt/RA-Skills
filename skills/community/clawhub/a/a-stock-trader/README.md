# A股模拟交易系统

## 快速开始

### 1. 获取数据
```bash
python scripts/fetch_daily.py --stock 600519 --days 250
```

### 2. 运行回测
```bash
python scripts/backtest.py --stock 600519 --strategy ma
```

### 3. 模拟交易
```bash
# 查看持仓
python scripts/simulate.py --show

# 买入
python scripts/simulate.py --buy --stock 600519 --shares 1000 --price 50.0

# 卖出
python scripts/simulate.py --sell --stock 600519 --shares 500 --price 55.0
```

## 策略说明

- `ma` - 均线策略（金叉买入，死叉卖出）
- `momentum` - 动量策略（追涨杀跌）
