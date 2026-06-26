# Crypto K线采集器

通过Binance API采集加密货币K线数据的工具。

## 功能

- 支持BTC、ETH等主流加密货币
- 支持多种时间周期（1m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1d, 1w）
- 自动获取完整历史数据
- 支持代理配置

## 使用方法

### Python脚本（推荐）

```bash
# 采集BTC 1小时K线数据
python3 ~/.openclaw/workspace/skills/crypto-kline/scripts/crypto-kline.py --symbol BTCUSDT --interval 1h

# 采集ETH 4小时K线数据
python3 ~/.openclaw/workspace/skills/crypto-kline/scripts/crypto-kline.py --symbol ETHUSDT --interval 4h

# 采集并保存到指定数据库
python3 ~/.openclaw/workspace/skills/crypto-kline/scripts/crypto-kline.py --symbol BTCUSDT --interval 1h --db-path /path/to/db.db
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --symbol | 交易对 (如 BTCUSDT, ETHUSDT) | BTCUSDT |
| --interval | K线周期 | 1h |
| --start-date | 开始日期 (YYYY-MM-DD) | 2024-01-01 |
| --end-date | 结束日期 (YYYY-MM-DD) | 今天 |
| --db-path | 数据库路径 | ~/.openclaw/workspace/data/{symbol}_{interval}_kline.db |
| --proxy | HTTP代理 | http://192.168.10.188:7897 |

### 支持的交易对

- BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- 以及其他Binance支持的USDT交易对

### 支持的时间周期

| 周期 | 说明 |
|------|------|
| 1m | 1分钟 |
| 5m | 5分钟 |
| 15m | 15分钟 |
| 30m | 30分钟 |
| 1h | 1小时 |
| 4h | 4小时 |
| 6h | 6小时 |
| 12h | 12小时 |
| 1d | 1天 |
| 1w | 1周 |

### Node.js脚本

```bash
# 基本用法
node ~/.openclaw/workspace/skills/crypto-kline/scripts/binance-kline.js BTCUSDT 1h 100

# 指定日期范围
node ~/.openclaw/workspace/skills/crypto-kline/scripts/binance-kline.js BTCUSDT 1h 1000 --start 2024-01-01 --end 2025-01-01
```

## 数据库表结构

```sql
CREATE TABLE {symbol}_{interval}_kline (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER,
    open_time TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    quote_volume REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_timestamp ON {symbol}_{interval}_kline(timestamp);
```

## 示例

### 采集BTC 1小时数据并重采样为6小时

```bash
# 1. 采集1小时数据
python3 ~/.openclaw/workspace/skills/crypto-kline/scripts/crypto-kline.py --symbol BTCUSDT --interval 1h

# 2. 使用resample脚本转换为6小时
python3 ~/.openclaw/workspace/scripts/resample_1h_to_6h.py --input ~/.openclaw/workspace/data/btcusdt_1h_kline.db --output ~/.openclaw/workspace/data/btcusdt_6h_kline.db
```

## 注意事项

- 需要网络访问Binance API
- 建议使用代理以提高稳定性
- 获取大量历史数据时会有请求频率限制
