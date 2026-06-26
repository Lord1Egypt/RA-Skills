# CryptoScope 技能配置说明

## ⚠️ 重要：SkillPay配置

当前技能使用临时Skill ID，需要在SkillPay后台创建真实技能后更新。

---

## 📋 配置步骤（5分钟）

### 1️⃣ 创建SkillPay技能

**访问：** https://skillpay.me/dashboard/skills

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
✅ 历史数据分析（90天）
✅ CoinGecko API（免费，无需Key）

定价：$0.05 USDT / 次
分类：数据分析
标签：crypto, bitcoin, ethereum, trading, analysis, blockchain
```

---

### 2️⃣ 复制Skill ID

创建成功后，页面会显示：

```
Skill ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**立即复制这个ID！**

---

### 3️⃣ 更新配置

**编辑文件：**
```bash
vim skills/crypto-scope/scripts/crypto_analyzer_paid.py
```

**修改第14行：**
```python
# 修改前
SKILL_ID = 'crypto-scope-v1-placeholder'

# 修改后
SKILL_ID = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'  # 替换为真实Skill ID
```

---

### 4️⃣ 重新发布

```bash
cd ~/.openclaw/workspace
npx clawhub publish skills/crypto-scope --version "1.0.2"
```

---

## 🧪 测试付费流程

```bash
# 测试价格查询
python3 skills/crypto-scope/scripts/crypto_analyzer_paid.py price bitcoin --user-id test_user

# 预期输出
{
  "symbol": "bitcoin",
  "name": "Bitcoin",
  "price": 67973.00,
  "change_24h": -3.57,
  "charged": 0.05,
  "balance": 7.95,
  "timestamp": 1709798400
}
```

---

## 💰 定价说明

- **价格：** $0.05 USDT / 次
- **支付：** BNB Chain USDT
- **最低充值：** $8 USDT
- **平台费用：** 5%
- **开发者收入：** 95%

---

## 📊 预期收益

**保守估计：**
- 日调用量：10次
- 日收入：$0.50
- 月收入：$15

**乐观估计：**
- 日调用量：50次
- 日收入：$2.50
- 月收入：$75

---

## ⚡ 快速配置命令

**一键更新配置（替换YOUR_SKILL_ID）：**

```bash
# 设置Skill ID
export SKILL_ID="YOUR_SKILL_ID"

# 更新脚本
sed -i '' "s/crypto-scope-v1-placeholder/$SKILL_ID/g" ~/.openclaw/workspace/skills/crypto-scope/scripts/crypto_analyzer_paid.py

# 重新发布
cd ~/.openclaw/workspace && npx clawhub publish skills/crypto-scope --version "1.0.2"
```

---

## ✅ 配置完成检查

- [ ] 在SkillPay后台创建技能
- [ ] 复制Skill ID
- [ ] 更新脚本配置
- [ ] 重新发布到ClawHub
- [ ] 测试付费流程
- [ ] 开始赚钱！

---

**💡 提示：** 配置完成后，每次调用自动扣费，无需任何额外操作！

---

*配置文档生成时间：2026-03-07 14:17*
