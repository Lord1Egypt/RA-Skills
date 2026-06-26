# CryptoScope 快速配置指南（5分钟）

## ✅ 前置检查

- [x] SkillPay API Key已配置
- [x] ClawHub已发布（v1.0.3）
- [ ] 需要在SkillPay创建技能

---

## 🚀 配置步骤

### 1️⃣ 访问SkillPay（2分钟）

**URL：** https://skillpay.me/dashboard/skills

**填写信息：**
```
技能名称：CryptoScope - 加密货币分析助手

描述：
实时价格查询、技术指标分析（MA/RSI/MACD）、交易信号生成

详细说明：
✅ 支持10000+币种实时价格查询
✅ 多种技术指标（MA20/50、RSI、MACD、布林带）
✅ 智能交易信号（BUY/SELL/HOLD）
✅ 置信度和风险评估
✅ CoinGecko API（免费，无需Key）

定价：$0.05 USDT / 次
分类：数据分析
标签：crypto, bitcoin, ethereum, trading, analysis
```

---

### 2️⃣ 复制Skill ID（10秒）

创建成功后，页面会显示：
```
Skill ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**立即复制！**

---

### 3️⃣ 运行配置脚本（30秒）

```bash
cd ~/.openclaw/workspace/skills/crypto-scope
./scripts/setup_skillpay.sh YOUR_SKILL_ID
```

**或者手动更新：**

编辑 `scripts/crypto_analyzer.py` 第20行：
```python
CRYPTO_SKILL_ID = "YOUR_SKILL_ID"  # 替换为真实Skill ID
```

---

### 4️⃣ 测试（1分钟）

```bash
# 测试付费功能
python3 skills/crypto-scope/scripts/crypto_analyzer.py price bitcoin --user-id test_user

# 预期输出
{
  "symbol": "bitcoin",
  "price": 67973.00,
  "change_24h": -3.57,
  "charged": 0.05,
  "balance": 7.95
}
```

---

### 5️⃣ 重新发布（1分钟）

```bash
cd ~/.openclaw/workspace
npx clawhub publish skills/crypto-scope --version "1.0.4"
```

---

## 💡 重要提示

**充值地址：**
- 最低充值：$8 USDT
- 支持链：BNB Chain
- 充值链接：https://skillpay.me/dashboard/wallet

**API Key：**
- 已配置：✅
- Key：sk_0de94ea93e9aca73...
- 余额：$0（需充值）

---

## 📊 预期收益

- 定价：$0.05/次
- 日调用量：5-50次
- 日收入：$0.25-$2.50
- 月收入：$7.5-$75

---

## ✅ 完成检查

- [ ] SkillPay技能创建
- [ ] Skill ID复制
- [ ] 配置脚本运行
- [ ] 付费功能测试
- [ ] 重新发布到ClawHub
- [ ] 充值$8

---

**🎉 配置完成后，开始赚钱！**

---

*配置指南生成时间：2026-03-07 19:36*
