# 🚀 A2A 文章服务平台

> 基于 [ClawTip](https://clawtip.jd.com)（中国首个纯正 A2A 微支付协议）研发  
> 为 AI Agent 提供一站式文章服务：热榜获取 → 智能创作 → 公众号发布

---

## 📖 简介

这是一个 AI Agent 技能（Skill），安装后让你的 AI 助手具备完整的文章自动化能力。

底层基于京东科技发布的 **ClawTip A2A 微支付协议**，实现 AI 智能体间的无感自动结算。用户只需确认需求 → 完成微支付 → 即可获得服务结果，全流程自动化。

### ClawTip 是什么？

2026 年 3 月 31 日，京东科技正式发布了业内首个面向 AI Agent 生态的 A2A（Agent-to-Agent）微支付基础设施 **ClawTip**。它解决了 Skill 开发者变现难、传统支付无法适配 AI 自主交易的行业痛点，支持智能体自主询价、决策、支付并获取产品/服务的全流程。

- 🌐 官网：https://clawtip.jd.com
- 💡 核心：AI 智能体专属钱包 + 自主决策支付 + 可信交易快照存证

---

## 🎯 三种服务

| 服务 | 价格 | 适合谁 | 说明 |
|------|------|--------|------|
| **热榜数据获取** | ¥0.88/次 | 内容运营、自媒体人 | 聚合微博、知乎、抖音、B站、小红书等 35+ 平台实时热榜，帮你快速发现热点选题 |
| **公众号文章发布** | ¥1.00/次 | 公众号运营者 | 将 Markdown 格式的文章一键发布到微信公众号草稿箱，省去找素材、排版、上传的繁琐流程 |
| **文章全自动化** | ¥1.88/次 | 懒人福音、批量产出 | 热榜自动选热门选题 → AI 自动撰写文章 → 自动发布到公众号，全程无需人工干预 |

---

## 📁 目录结构

```
clawtip-services/
├── SKILL.md              # 技能定义文件（AI Agent 的核心指令）
├── README.md             # 本文档
├── scripts/
│   ├── create_order.py   # 创建订单脚本
│   └── service.py        # 服务履约脚本
└── shared/
    └── file_utils.py     # 订单文件读写工具
```

---

## 🚀 快速开始

### 安装

在 OpenClaw 中安装此技能后，AI Agent 即可调用。

### 使用示例

**获取热榜数据：**
```bash
python3 scripts/create_order.py "微博,知乎,B站" --slug hot-ranks
# → ORDER_NO=20260411193000123456
# → AMOUNT=88
# → 完成支付后...
python3 scripts/service.py "微博,知乎,B站" "20260411193000123456" "<payCredential>" --slug hot-ranks
```

**发布文章到公众号：**
```bash
python3 scripts/create_order.py "将 article.md 发布到公众号" --slug publish
# → 完成支付后...
python3 scripts/service.py "发布文章" "<order_no>" "<payCredential>" --slug publish
```

**全自动化流程：**
```bash
python3 scripts/create_order.py "从微博热榜选一个科技话题，写一篇公众号文章并发布" --slug full-auto
# → 完成支付后...
python3 scripts/service.py "全自动化" "<order_no>" "<payCredential>" --slug full-auto
```

---

## 💳 付费说明

本服务采用 **按次计费**，使用一次扣一次费用：

| 服务 | 费用 |
|------|------|
| 热榜数据获取 | ¥0.88 |
| 公众号文章发布 | ¥1.00 |
| 文章全自动化 | ¥1.88 |

支付通过 ClawTip A2A 协议完成，支持钱包内小额零钱无感支付。

---

## 🔧 技术架构

```
┌─────────────┐     创建订单     ┌──────────────────┐
│   AI Agent  │ ──────────────→ │  ClawTip 后端     │
│  (此 Skill)  │                │  (43.136.97.223)  │
│             │ ←────────────── │                   │
│             │   订单信息       │  Flask + SM4 加密  │
└──────┬──────┘                └──────────────────┘
       │
       │ 用户支付
       ▼
┌─────────────┐     支付凭证     ┌──────────────────┐
│  ClawTip    │ ←────────────── │   AI Agent        │
│  微支付      │                 │   (service.py)    │
└──────┬──────┘                 └────────┬─────────┘
       │                                 │
       │ 支付确认                         │ 携带凭证请求结果
       ▼                                 ▼
┌─────────────┐                ┌──────────────────┐
│  服务结果    │ ←──────────────│  ClawTip 后端     │
│  返回给用户  │                │  履约 + 返回数据   │
└─────────────┘                └──────────────────┘
```

- **通信协议**：HTTPS + SM4 国密加密
- **后端框架**：Flask + Nginx 反代
- **加密算法**：SM4（国密标准）
- **部署地址**：`http://43.136.97.223/clawtip-api/`

---

## 📋 API 参考

### POST `/clawtip-api/api/createOrder`

创建订单接口

**请求体：**
```json
{
  "question": "用户需求描述",
  "slug": "clawtip-hot-ranks"
}
```

**响应：**
```json
{
  "responseCode": "200",
  "orderNo": "20260411193000123456",
  "amount": "88",
  "payTo": "...",
  "encryptedData": "..."
}
```

### POST `/clawtip-api/api/getServiceResult`

获取服务结果（履约）

**请求体：**
```json
{
  "question": "用户需求描述",
  "orderNo": "订单号",
  "credential": "支付凭证"
}
```

**响应：**
```json
{
  "responseCode": "200",
  "payStatus": "SUCCESS",
  "answer": "服务结果数据",
  "alreadyFulfilled": false
}
```

---

## 🛡️ 安全与隐私

- **国密加密**：所有交易数据使用 SM4 国密算法加密传输
- **幂等保护**：同一订单不会重复履约
- **小额支付**：仅支持钱包内预设小额零钱，不关联银行卡或主账户
- **交易存证**：所有交互行为生成可信快照存证

---

## ❓ 常见问题

**Q：什么是 A2A？**  
A：A2A（Agent-to-Agent）是指 AI 智能体之间的自主交互和交易。ClawTip 让 AI Agent 能够自主完成询价、决策、支付全流程，无需人类介入。

**Q：支付安全吗？**  
A：安全。ClawTip 使用钱包内预设小额零钱，不关联银行卡。所有交易数据 SM4 加密，行为快照存证。

**Q：可以开发票吗？**  
A：目前暂不支持发票，如需开票请联系开发者。

**Q：服务不支持怎么办？**  
A：请检查网络连接，确认后端服务 `http://43.136.97.223/clawtip-api/` 可访问。如仍有问题，联系开发者。

---

## 📞 联系与反馈

- **开发者**：LucianaiB
- **问题反馈**：通过 ClawHub 页面留言

---

## 📜 许可证

本项目基于 MIT-0 许可证发布，允许任何人免费使用、修改和重新分发。

**基于 ClawTip（中国首个纯正 A2A 微支付协议）研发。**  
ClawTip 由京东科技于 2026 年 3 月 31 日发布，详见 https://clawtip.jd.com
