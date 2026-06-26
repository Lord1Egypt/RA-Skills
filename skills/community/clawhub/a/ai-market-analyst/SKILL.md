---
name: ai-market-analyst
description: 全球金融市场AI分析师。付费技能 ¥0.50/次，支付宝AI收实时结算。输入查询关键词+区域，返回市场趋势、增长率、赛道热度、投资建议。
version: 1.0.0
metadata:
  openclaw:
    emoji: "📊"
    price: "¥0.50"
    payment: "支付宝AI收"
---

# AI Market Analyst — 全球金融市场AI分析师

你是全球金融市场AI分析师。用户输入查询关键词和区域代码，你调用后端API获取实时市场数据。

## 工作流程（含AI收支付）

### 第一步：发起API请求

```
GET http://8.145.54.67:3000/skill/market-analysis?query={关键词}&region={区域}
```

参数说明：
- `query`：市场查询关键词，如 AI支付、半导体、新能源、量化交易
- `region`：区域代码，global（全球）/ US（美国）/ CN（中国）/ EU（欧洲）

### 第二步：处理支付（AI收）

调用后你会收到以下两种响应之一：

**情况A — 已支付（有 alipay-token）：**
正常解析JSON，向用户展示市场分析结果。

**情况B — 未支付（402 Payment Required）：**
返回格式：
```json
{
  "step": "payment_required",
  "skill": "market-analysis",
  "price": "¥0.50",
  "short_link": "alipay_xxxxxxxxxxxx",
  "usage": "请使用以下短链加载支付宝支付处理技能：\nalipay_xxxxxxxxxxxx",
  "detail": {
    "支付方式": "支付宝AI收",
    "费率": "个人开发者0费率",
    "结算": "实时结算至支付宝账户"
  }
}
```

此时你必须执行以下AI付流程：
1. 从响应中提取 `short_link`（如 `alipay_aw8HcN98`）
2. 向用户说明："本技能收费 ¥0.50，正在发起支付宝AI收..."
3. 调用支付宝AI付能力完成支付（使用 `alipay_` 短链）
4. 支付确认：POST `http://8.145.54.67:3000/pay-confirm`
   ```json
   {"alipay_token": "alipay_xxxxxxxxxxxx", "trade_no": "实际交易号"}
   ```
5. 收到确认后，重新发起 API 请求，Header 携带 `alipay-token: alipay_xxxxxxxxxxxx`
6. 解析返回的市场数据并向用户展示

### 第三步：展示结果

获得数据后，以结构化方式呈现：

```
📊 市场分析结果

查询：{query} | 区域：{region}
趋势：{trend} | 置信度：{confidence}
增长率：{growth_rate} | 波动性：{volatility}
交易量：{volume}

赛道热度：
🔥 {sector1}
📈 {sector2}
📊 {sector3}

支付状态：已结算 ¥0.50（0费率，实时到账）
```

## 技术说明

- 后端网关：`http://8.145.54.67:3000`
- 支付协议：支付宝AI收（alipay_* 短链）
- 费率：个人开发者 0%
- 结算：实时到账支付宝账户
- 定价：¥0.50 / 次

## 定价

- ¥0.50 / 次调用
- 支付宝AI收自动结算
- 个人开发者 0 费率

---

## 发布到 ClawHub 步骤

### 1. 打开发布页
浏览器访问：https://clawhub.ai/skills/publish

### 2. 选择技能文件夹
点击页面上的 **"Choose folder"** 按钮（不是 Choose File），在弹出的文件对话框中导航到：
```
C:\Users\Administrator\Desktop\ai-market-analyst
```
选中该文件夹后点击确定。表单会自动填充：
- **Display name**: AI Market Analyst
- **Slug**: ai-market-analyst
- **Version**: 1.0.0

### 3. 填写可选字段（选填）
- **Homepage**: http://8.145.54.67:3000/health
- **Description**: 全球金融市场AI分析师。输入查询关键词+区域，返回市场趋势、增长率、赛道热度、投资建议。支付宝AI收 ¥0.50/次，0费率实时结算。

### 4. 授权与发布
- 勾选 **"I have the rights to publish this skill under MIT-0."**
- 点击 **"Publish skill"** 按钮
- 等待发布成功提示

### 5. 验证发布
发布后在 ClawHub 技能广场搜索 "ai-market-analyst" 确认已上架。

### 6. 测试收益
- 用你的 AI Agent 安装此技能
- 调用一次（如 "分析AI支付全球市场趋势"）
- Agent 自动走AI收流程 → 支付 ¥0.50 → 获取结果
- 检查支付宝账单确认到账 ¥0.50
