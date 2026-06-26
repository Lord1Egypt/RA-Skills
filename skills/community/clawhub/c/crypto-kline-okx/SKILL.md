# OKX K线数据技能

获取OKX交易所加密货币历史K线数据，支持通过时间戳分页查询更早的历史数据。

## 功能

- 获取历史K线数据（1m/5m/15m/30m/1h/4h/6h/12h/1d/1w/1M）
- 支持时间戳分页查询，可获取超过默认限制的历史数据
- 支持BTC、ETH、SOL等主流币种

## 使用方法

```bash
# 查询历史K线
node scripts/okx-kline.js BTC-USDT 1d 30        # BTC日线最近30条
node scripts/okx-kline.js ETH-USDT 4h 100       # ETH 4小时线最近100条
node scripts/okx-kline.js SOL-USDT 1h 50        # SOL 1小时线50条

# 通过时间戳查询历史数据
# 查询2025年4月1日的数据
node scripts/okx-kline.js BTC-USDT 4h --after=1743500000000

# 参数说明
# 第1个参数：交易对 (BTC-USDT/ETH-USDT/SOL-USDT等)
# 第2个参数：周期 (1m/5m/15m/30m/1h/4h/6h/12h/1d/1w/1M)
# 第3个参数：数量 (默认100, 最大100)
# --after: 查询指定时间戳之前的数据 (更早)
# --before: 查询指定时间戳之后的数据 (更新)
```

## 时间戳分页查询示例

```bash
# 查询2025年3月的数据 (需要分页多次查询)
# OKX API单次最多返回100条，4小时K线约33天数据量

# 先获取最近的数据
node scripts/okx-kline.js BTC-USDT 4h 100

# 使用 --after 参数获取更早的数据
# after参数需要使用毫秒级时间戳
node scripts/okx-kline.js BTC-USDT 4h 100 --after=1743500000000
```

## 支持的交易对

所有OKX支持的现货交易对，如：
- BTC-USDT, ETH-USDT, SOL-USDT, BNB-USDT
- DOGE-USDT, XRP-USDT, ADA-USDT, DOT-USDT
- ONDO-USDT, PEPE-USDT, etc.

## API 限制

- 单次最多100条记录
- 4小时K线：约33天数据范围
- 使用时间戳分页可查询任意历史数据
