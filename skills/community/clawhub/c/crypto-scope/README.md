🎉 CryptoScope v1.0.1 - 加密货币分析助手

## 📦 安装

```bash
npx clawhub install crypto-scope
```

## 💰 功能

### 1. 实时价格查询
支持10000+币种，数据来源于CoinGecko（免费API，无需Key）

### 2. 技术指标分析
- MA（移动平均线）: MA20/MA50/MA200
- RSI（相对强弱指数）: 14日RSI
- MACD（异同移动平均线）: 金叉/死叉信号
- Bollinger Bands（布林带）

### 3. 交易信号生成
- BUY（买入）: 多指标看涨
- SELL（卖出）: 多指标看跌
- HOLD（持有）: 趋势不明

## 🚀 快速开始

### 免费版（立即可用）

```bash
# 实时价格
python3 scripts/crypto_analyzer.py price bitcoin

# 技术分析
python3 scripts/crypto_analyzer.py analyze ethereum

# 交易信号
python3 scripts/crypto_analyzer.py signal solana
```

### 付费版（$0.05/次）

```bash
# 配置Skill ID后可用
python3 scripts/crypto_analyzer_paid.py signal bitcoin --user-id user123
```

## 📊 定价

- **价格**: $0.05 USDT / 次
- **支付**: BNB Chain USDT
- **最低充值**: $8 USDT
- **平台费用**: 5%
- **开发者收入**: 95%

## 🔧 SkillPay配置

**⚠️ 付费版需要配置SkillPay Skill ID**

**配置步骤（5分钟）：**
1. 访问 https://skillpay.me/dashboard/skills
2. 点击"创建技能"
3. 填写信息（见 SETUP.md）
4. 复制Skill ID
5. 更新 `crypto_analyzer_paid.py` 第14行
6. 重新发布

**详细指南**: `cat SETUP.md`

## 🎯 使用示例

### 示例1：价格查询

```bash
python3 scripts/crypto_analyzer.py price bitcoin

# 输出
{
  "symbol": "bitcoin",
  "name": "Bitcoin",
  "price": 67973.00,
  "change_24h": -3.57,
  "volume_24h": 28500000000,
  "market_cap": 1300000000000
}
```

### 示例2：交易信号

```bash
python3 scripts/crypto_analyzer.py signal ethereum

# 输出
{
  "symbol": "ethereum",
  "signal": "BUY",
  "confidence": 0.75,
  "reasons": [
    "MA20 > MA50（多头趋势）",
    "RSI=58（健康区间）",
    "MACD金叉（看涨）"
  ],
  "risk_level": "medium"
}
```

## ⚠️ 免责声明

**信号仅供参考，不构成投资建议**
- 加密货币市场风险极高
- 请根据自身情况谨慎决策
- 过往表现不代表未来收益

## 📚 支持币种

支持10000+币种，包括：
- Bitcoin (bitcoin)
- Ethereum (ethereum)
- BNB (binancecoin)
- Solana (solana)
- Cardano (cardano)
- Polkadot (polkadot)
- 等10000+币种

**完整币种列表**: https://coingecko.com/coins

## 🔗 链接

- **ClawHub**: https://clawhub.com/skill/crypto-scope
- **SkillPay**: https://skillpay.me
- **CoinGecko**: https://coingecko.com

## 📧 支持

- GitHub Issues: [待补充]
- Email: [待补充]

---

**CryptoScope - 让加密货币分析更智能** 📈💰

*版本: v1.0.1*
*发布日期: 2026-03-07*
