# Huobi K线数据技能

获取火必（Huobi）实时行情和K线历史数据。

## 功能

- 获取历史K线数据（1min/5min/15min/30min/1h/1d/1w/1M）
- 获取实时行情
- 支持BTC、ETH等主流币种

## 使用方法

```bash
# 查询历史K线
node scripts/huobi-kline.js BTC 1d 30    # BTC日线最近30条
node scripts/huobi-kline.js ETH 1h 24    # ETH小时线最近24条
node scripts/huobi-kline.js SOL 15min 100 # SOL 15分钟线最近100条

# 参数说明
# 第1个参数：交易对 (btcusdt/ethusdt/solusdt等)
# 第2个参数：周期 (1min/5min/15min/30min/1h/1d/1w/1M)
# 第3个参数：数量 (默认10，最大2000)
```

## 支持的交易对

所有Huobi支持的现货交易对，如：
- btcusdt, ethusdt, solusdt, bnbusdt
- dogeusdt, xrpusdt, adausdt, dotusdt
