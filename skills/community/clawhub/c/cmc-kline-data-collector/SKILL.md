---
name: cmc-kline-data-collector
version: 1.0.0
description: 从 CoinMarketCap 获取加密货币 K 线历史数据，自动计算 EMA7、EMA30、RSI14 等技术指标，支持 JSON/CSV 格式输出
author: harrier
tags: crypto,coinmarketcap,eth,sol,bnb,kline,indicators,ema,rsi
repository: https://github.com/openclaw/openclaw
license: MIT
---

# CMC Kline Data Collector Skill

从 CoinMarketCap 获取 ETH/SOL/BNB 等加密货币的历史 K 线数据，自动计算 EMA7、EMA30、RSI14 等技术指标，输出标准化 JSON 格式。

---

## 使用方法

### 在对话中使用

```
获取 ETH 最近 7 天的 K 线数据
```

```
生成 ETH/SOL/BNB 的每日指标数据
```

```
输出 BTC 历史数据到 JSON 文件
```

### 编程调用

```python
from skills.crypto_data_processor import CryptoDataProcessor

# 创建处理器
processor = CryptoDataProcessor()

# 获取单个币种数据
eth_data = processor.fetch_symbol("ETH", days=30)

# 获取多个币种数据
all_data = processor.fetch_all(["ETH", "SOL", "BNB"])

# 保存为 JSON
processor.save_json(all_data, "/path/to/output.json")

# 保存为 CSV
processor.save_csv(eth_data, "eth_kline.csv")
```

---

## 输出格式

```json
{
  "ETH": [
    {"O":2027.41,"H":2040.79,"L":1930.4,"C":1982.77,"E7":1976.66,"E30":2115.05,"R14":43.71,"D":"0303"},
    {"O":1982.71,"H":2198.66,"L":1946.04,"C":2126.51,"E7":2014.12,"E30":2115.79,"R14":52.1,"D":"0304"}
  ],
  "SOL": [...],
  "BNB": [...]
}
```

**字段说明：**
- `O` - Open（开盘价）
- `H` - High（最高价）
- `L` - Low（最低价）
- `C` - Close（收盘价）
- `E7` - EMA 7（7 日指数移动平均）
- `E30` - EMA 30（30 日指数移动平均）
- `R14` - RSI 14（14 日相对强弱指数）
- `D` - Date（日期，MMDD 格式）

---

## 配置

编辑 `config.py` 修改币种和 API 设置：

```python
# 币种 ID 映射（CoinMarketCap ID）
SYMBOL_TO_ID = {
    "BTC": 1,
    "ETH": 1027,
    "BNB": 1839,
    "SOL": 5426,
    # 添加更多...
}

# 计价货币（2781=USD）
CONVERT_ID = 2781

# 输出目录
OUTPUT_DIR = "/home/admin/.openclaw/workspace/crypto-data-processor/output"
```

---

## 依赖

```bash
pip install requests
```

---

## 原项目位置

原始 `crypto-data-processor` 项目保留在：
`/home/admin/.openclaw/workspace/crypto-data-processor/`

本 Skill 名称：`cmc-kline-data-collector`

包括：
- 完整源代码
- crontab 定时任务配置
- 输出目录
- README 文档

---

## 与定时任务集成

原项目的 crontab 配置保持不变：

```bash
# 每天 9:00 自动执行
0 9 * * * cd /home/admin/.openclaw/workspace/crypto-data-processor && python scripts/daily_kline.py --output /home/admin/.openclaw/workspace/crypto-data-processor/output/daily_$(date +\%Y\%m\%d).json
```

---

## 注意事项

1. **数据需求**：需要至少 35 天历史数据来计算指标（30 天 EMA + 7 天输出）
2. **API 限制**：CMC 公开 API 无速率限制，但建议不要高频调用
3. **时区**：CMC 返回 UTC 时间，日期格式为 MMDD（如 0309=3 月 9 日）
