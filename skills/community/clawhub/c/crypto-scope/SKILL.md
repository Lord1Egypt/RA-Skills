---
name: crypto-scope
version: 1.0.5
description: 加密货币数据分析助手，实时价格查询、技术指标分析、交易信号生成。使用场景：(1) 实时价格监控 (2) 技术指标分析（MA/RSI/MACD） (3) 交易信号生成 (4) 市场趋势判断。Triggers: "加密货币", "比特币", "以太坊", "价格分析", "技术指标", "交易信号", "crypto", "bitcoin", "eth"。
---

# CryptoScope - 加密货币数据分析助手

## 快速开始

### 实时价格查询

```bash
# 比特币价格
python3 scripts/crypto_analyzer.py price bitcoin

# 以太坊价格
python3 scripts/crypto_analyzer.py price ethereum

# 自定义币种
python3 scripts/crypto_analyzer.py price solana
```

### 技术指标分析

```bash
# 完整技术分析
python3 scripts/crypto_analyzer.py analyze bitcoin

# 指定指标
python3 scripts/crypto_analyzer.py analyze ethereum --indicators ma,rsi,macd
```

### 交易信号

```bash
# 生成交易信号
python3 scripts/crypto_analyzer.py signal bitcoin

# 多币种信号
python3 scripts/crypto_analyzer.py signal bitcoin,ethereum,solana
```

---

## 输出格式

### JSON格式（默认）

```json
{
  "symbol": "bitcoin",
  "name": "Bitcoin",
  "price": 42350.67,
  "change_24h": 2.35,
  "volume_24h": 28500000000,
  "market_cap": 830000000000,
  "indicators": {
    "ma_20": 42100.50,
    "rsi": 58.3,
    "macd": "bullish"
  },
  "signal": "BUY",
  "confidence": 0.75,
  "timestamp": 1709798400
}
```

### Markdown格式

```bash
python3 scripts/crypto_analyzer.py analyze bitcoin --format markdown
```

---

## 核心功能

### 1. 实时价格查询

**支持币种：**
- ✅ Bitcoin (BTC)
- ✅ Ethereum (ETH)
- ✅ BNB (BNB)
- ✅ Solana (SOL)
- ✅ Cardano (ADA)
- ✅ Polkadot (DOT)
- ✅ 10000+ 其他币种

**数据来源：**
- CoinGecko API（免费）
- 更新频率：每分钟

**示例：**

```bash
python3 scripts/crypto_analyzer.py price bitcoin

# 输出
{
  "symbol": "bitcoin",
  "name": "Bitcoin",
  "price": 42350.67,
  "change_24h": 2.35,
  "volume_24h": 28500000000
}
```

---

### 2. 技术指标分析

**支持指标：**

| 指标 | 说明 | 周期 |
|------|------|------|
| MA | 移动平均线 | 20/50/200 |
| RSI | 相对强弱指数 | 14 |
| MACD | 异同移动平均线 | 12/26/9 |
| Bollinger | 布林带 | 20,2 |
| EMA | 指数移动平均 | 12/26 |

**示例：**

```bash
# 完整分析
python3 scripts/crypto_analyzer.py analyze ethereum

# 输出
{
  "symbol": "ethereum",
  "price": 2250.45,
  "indicators": {
    "ma_20": 2200.30,
    "ma_50": 2150.80,
    "rsi": 62.5,
    "macd": {
      "value": 15.3,
      "signal": 12.1,
      "trend": "bullish"
    }
  }
}
```

---

### 3. 交易信号生成

**信号类型：**
- BUY（买入）
- SELL（卖出）
- HOLD（持有）

**信号逻辑：**
```python
# 多指标综合判断
- MA交叉
- RSI超买超卖
- MACD金叉死叉
- 趋势强度

# 置信度计算
confidence = (
    ma_signal * 0.3 +
    rsi_signal * 0.3 +
    macd_signal * 0.4
)
```

**示例：**

```bash
python3 scripts/crypto_analyzer.py signal bitcoin

# 输出
{
  "symbol": "bitcoin",
  "signal": "BUY",
  "confidence": 0.75,
  "reasons": [
    "MA20上穿MA50",
    "RSI=58（健康区间）",
    "MACD金叉确认"
  ],
  "risk_level": "medium"
}
```

---

### 4. 批量监控

**多币种监控：**

```bash
# 监控多个币种
python3 scripts/crypto_analyzer.py monitor bitcoin,ethereum,solana

# 输出
[
  {
    "symbol": "bitcoin",
    "price": 42350.67,
    "signal": "BUY",
    "confidence": 0.75
  },
  {
    "symbol": "ethereum",
    "price": 2250.45,
    "signal": "HOLD",
    "confidence": 0.60
  },
  {
    "symbol": "solana",
    "price": 105.30,
    "signal": "SELL",
    "confidence": 0.70
  }
]
```

---

## 高级用法

### 自定义周期

```bash
# 指定MA周期
python3 scripts/crypto_analyzer.py analyze bitcoin --ma-periods 10,30,60

# 指定RSI周期
python3 scripts/crypto_analyzer.py analyze ethereum --rsi-period 21
```

### 历史数据

```bash
# 获取历史价格
python3 scripts/crypto_analyzer.py history bitcoin --days 30

# 导出CSV
python3 scripts/crypto_analyzer.py history ethereum --days 90 --output csv
```

### 预警设置

```bash
# 设置价格预警
python3 scripts/crypto_analyzer.py alert bitcoin --above 45000

# RSI预警
python3 scripts/crypto_analyzer.py alert ethereum --rsi-below 30
```

---

## 技术细节

### 数据来源

**CoinGecko API：**
- 免费额度：50次/分钟
- 支持币种：10000+
- 数据更新：实时

**降级策略：**
- CoinGecko失败 → CoinCap API
- 全失败 → 返回缓存数据

---

### 指标计算

**移动平均线（MA）：**
```python
def calculate_ma(prices, period):
    return sum(prices[-period:]) / period
```

**相对强弱指数（RSI）：**
```python
def calculate_rsi(prices, period=14):
    gains = [max(prices[i] - prices[i-1], 0) for i in range(1, len(prices))]
    losses = [max(prices[i-1] - prices[i], 0) for i in range(1, len(prices))]
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))
```

**MACD：**
```python
def calculate_macd(prices):
    ema_12 = calculate_ema(prices, 12)
    ema_26 = calculate_ema(prices, 26)
    
    macd = ema_12 - ema_26
    signal = calculate_ema([macd], 9)
    
    return {
        "macd": macd,
        "signal": signal,
        "histogram": macd - signal
    }
```

---

### 信号逻辑

**买入信号：**
1. MA20上穿MA50
2. RSI < 70（未超买）
3. MACD金叉

**卖出信号：**
1. MA20下穿MA50
2. RSI > 30（未超卖）
3. MACD死叉

**持有信号：**
- 其他情况

---

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `APIError` | CoinGecko API限制 | 等待1分钟后重试 |
| `InvalidSymbol` | 币种不支持 | 检查币种名称 |
| `InsufficientData` | 数据不足 | 至少需要30天数据 |

### 日志级别

```bash
# 调试模式
python3 scripts/crypto_analyzer.py analyze bitcoin --log-level debug
```

---

## 最佳实践

### 1. 数据缓存

```python
# 启用缓存（默认5分钟）
python3 scripts/crypto_analyzer.py price bitcoin --cache 300
```

### 2. 批量请求

```bash
# 批量查询（减少API调用）
python3 scripts/crypto_analyzer.py monitor bitcoin,ethereum,solana
```

### 3. 风险管理

**⚠️ 免责声明：**
- 信号仅供参考，不构成投资建议
- 加密货币市场风险极高
- 请根据自身情况谨慎决策

---

## 使用场景

### 1. 日常监控
- 每日查看持仓币种信号
- 追踪市场趋势
- 调整投资策略

### 2. 交易决策
- 辅助判断买卖时机
- 验证交易想法
- 风险评估

### 3. 研究分析
- 对比不同币种
- 回测交易策略
- 学习技术分析

---

## 与其他技能配合

### Doc Genius（文档分析）

```bash
# 分析白皮书 → 技术分析
python3 doc-genius/scripts/doc_processor.py summarize whitepaper.pdf
python3 crypto-scope/scripts/crypto_analyzer.py analyze bitcoin
```

### Scrapling Fetch（数据抓取）

```bash
# 抓取新闻 → 情绪分析
python3 scrapling-fetch/scripts/fetch.py "https://cryptonews.com"
python3 crypto-scope/scripts/crypto_analyzer.py sentiment bitcoin
```

---

## 更新日志

### v1.0.0 (2026-03-07)
- ✅ 初始发布
- ✅ 实时价格查询
- ✅ 技术指标分析
- ✅ 交易信号生成

---

## 反馈与支持

- GitHub Issues: [待补充]
- ClawHub: https://clawhub.com/skill/crypto-scope
- Email: [待补充]

---

**CryptoScope - 让加密货币分析更智能** 📈💰

---

## 💰 付费版本

### 安装

```bash
npx clawhub install crypto-scope
```

### 使用

```bash
# 实时价格（$0.05/次）
python3 scripts/crypto_analyzer_paid.py price bitcoin --user-id user123

# 技术分析（$0.05/次）
python3 scripts/crypto_analyzer_paid.py analyze ethereum --user-id user123

# 交易信号（$0.05/次）
python3 scripts/crypto_analyzer_paid.py signal solana --user-id user123
```

### 计费说明

- **定价：** $0.05 USDT / 次
- **支付：** BNB Chain USDT
- **最低充值：** $8 USDT
- **平台费用：** 5%

**扣费流程：**
1. 检查余额
2. 获取数据
3. 自动扣费
4. 返回结果

**余额不足时：** 自动返回充值链接

---

## 🔧 配置

### SkillPay配置

**步骤：**
1. 登录 https://skillpay.me
2. 创建新技能
3. 复制Skill ID
4. 更新脚本中的 `SKILL_ID`

```python
# 在 crypto_analyzer_paid.py 中修改
SKILL_ID = 'your-skill-id-here'  # 替换为真实Skill ID
```

---

## 📊 商业化

**预期收益：**
- 日调用量：20次
- 日收入：$1.00
- 月收入：$30

**目标用户：**
- 加密货币交易者
- 区块链开发者
- Web3投资者

---
