# Binance Trader Skill

币安交易技能 - 支持现货和合约交易

## 安装

```bash
# 安装 Binance Python SDK
/usr/bin/python3.12 -m pip install python-binance ccxt

# 配置 API Key
export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_api_secret"
```

## 使用方法

### 1. 查看账户余额
```python
from binance.client import Client
import os

client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'))
account = client.get_account()
for balance in account['balances']:
    if float(balance['free']) > 0 or float(balance['locked']) > 0:
        print(f"{balance['asset']}: 可用={balance['free']}, 冻结={balance['locked']}")
```

### 2. 查看当前价格
```python
# 获取单个币种价格
price = client.get_symbol_ticker(symbol="BTCUSDT")
print(f"BTC 价格：{price['price']} USDT")

# 获取多个币种价格
prices = client.get_symbol_ticker()
for p in prices[:10]:  # 前 10 个
    print(f"{p['symbol']}: {p['price']}")
```

### 3. 下单交易
```python
# 现货买入 (市价单)
order = client.order_market_buy(
    symbol='BTCUSDT',
    quoteOrderQty=100  # 用 100 USDT 买入
)

# 现货卖出
order = client.order_market_sell(
    symbol='BTCUSDT',
    quantity=0.001  # 卖出 0.001 BTC
)

# 限价单
order = client.order_limit_buy(
    symbol='BTCUSDT',
    quantity=0.001,
    price=50000  # 在 50000 USDT 时买入
)
```

### 4. 合约交易
```python
from binance.um_futures import UMFutures

um_client = UMFutures(key=os.getenv('BINANCE_API_KEY'), secret=os.getenv('BINANCE_API_SECRET'))

# 查看合约持仓
positions = um_client.position_risk()
for pos in positions:
    if float(pos['positionAmt']) != 0:
        print(f"{pos['symbol']}: 持仓={pos['positionAmt']}, 入场价={pos['entryPrice']}, 未实现盈亏={pos['unRealizedProfit']}")

# 开多 (买入)
order = um_client.new_order(
    symbol="BTCUSDT",
    side="BUY",
    type="MARKET",
    quantity=0.001
)

# 开空 (卖出)
order = um_client.new_order(
    symbol="BTCUSDT",
    side="SELL",
    type="MARKET",
    quantity=0.001
)

# 设置止损止盈
order = um_client.new_order(
    symbol="BTCUSDT",
    side="SELL",
    type="STOP_MARKET",
    quantity=0.001,
    stopPrice=48000,  # 跌到 48000 止损
    closePosition=True
)
```

### 5. 查看 K 线数据
```python
# 获取 BTC 1 小时 K 线 (最近 100 根)
klines = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, limit=100)

for k in klines[-5:]:  # 最后 5 根
    timestamp = k[0]
    open_price = k[1]
    high = k[2]
    low = k[3]
    close = k[4]
    volume = k[5]
    print(f"时间:{timestamp}, 开:{open_price}, 高:{high}, 低:{low}, 收:{close}, 量:{volume}")
```

### 6. 查看订单历史
```python
# 现货订单历史
orders = client.get_all_orders(symbol='BTCUSDT', limit=10)
for order in orders:
    print(f"{order['symbol']}: {order['side']} {order['type']} @ {order['price']} - 状态:{order['status']}")

# 合约订单历史
orders = um_client.get_all_orders(symbol='BTCUSDT', limit=10)
```

## 安全注意事项

1. **永远不要分享 API Key**
2. **设置 IP 白名单** - 在币安后台限制 API Key 只能从特定 IP 访问
3. **限制权限** - 只开启必要的权限（交易/读取），不要开启提现权限
4. **使用子账户** - 建议创建子账户专门用于交易
5. **设置提现白名单** - 防止资金被盗转

## 常用交易对

- 现货：`BTCUSDT`, `ETHUSDT`, `BNBUSDT`, `SOLUSDT`
- 合约：`BTCUSDT`, `ETHUSDT`, `BNBUSDT` (永续合约)

## 错误处理

```python
from binance.exceptions import BinanceAPIException

try:
    order = client.order_market_buy(symbol='BTCUSDT', quoteOrderQty=100)
except BinanceAPIException as e:
    print(f"币安 API 错误：{e.status_code}, {e.message}")
except Exception as e:
    print(f"其他错误：{e}")
```
