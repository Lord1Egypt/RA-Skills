# Binance Trading Skill

币安API交易封装，支持现货和合约交易。

## 功能

### 现货交易
- `binance_spot_balance` - 获取账户余额
- `binance_spot_ticker` - 获取24小时行情
- `binance_spot_order` - 下单
- `binance_spot_orders` - 查询开放订单

### 合约交易
- `binance_futures_balance` - 获取合约账户余额
- `binance_futures_ticker` - 获取合约行情
- `binance_futures_order` - 合约下单
- `binance_futures_positions` - 查询持仓
- `binance_futures_open_orders` - 查询合约开放订单
- `binance_futures_book` - 深度数据
- `binance_futures_leverage` - 设置杠杆
- `binance_futures_close` - 平仓

### 通用
- `binance_ping` - 测试连接
- `binance_kline` - K线数据

## API配置

需要配置以下环境变量或直接在代码中修改：
- `BINANCE_API_KEY` - API Key
- `BINANCE_SECRET_KEY` - Secret Key

## 安装

```bash
# 安装依赖
npm install

# 测试连接
node index.js ping
```

## 使用示例

```javascript
const binance = require('./index.js');

// 获取余额
await binance.binance_futures_balance({});

// 获取行情
await binance.binance_futures_ticker({ symbol: "BTCUSDT" });

// 下单
await binance.binance_futures_order({
  symbol: "BTCUSDT",
  side: "BUY",
  quantity: 0.001
});

// 设置杠杆
await binance.binance_futures_leverage({
  symbol: "BTCUSDT",
  leverage: 10
});

// 平仓
await binance.binance_futures_close({
  symbol: "BTCUSDT"
});
```

## API Endpoints

| 类型 | 地址 |
|------|------|
| 现货 | https://api.binance.com |
| 合约 | https://fapi.binance.com |
