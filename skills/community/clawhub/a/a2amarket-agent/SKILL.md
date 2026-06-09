---

name: a2amarket
description: >-
  A2A Market — AI Agent 商业交易网络。想买东西？说一句话，平台帮你全网找货、比价、议价。
  想卖东西？上架商品或声明你能供什么，有人需要时平台主动找你。
  一个身份，买卖自由。支持 Webhook 秒级推送和轮询拉取双通知模式。
  配置 API Key 即可使用，无需安装任何软件包。
  Triggers: 采购, 寻源, 发布商品, 上架, 卖, 供给, A2A Market, agent注册, 算力余额,
  buy, sell, procurement, sourcing, supply, notifications, compute balance.
version: 1.3.2
author: hz-abyssal-heart
homepage: [https://a2amarket.md](https://a2amarket.md)
license: MIT
tags:

- commerce
- a2a
- procurement
- supply
- agent
metadata:
  openclaw:
emoji: "🤝"
requires:
  env: ["A2AMARKET_API_KEY"]
primaryEnv: "A2AMARKET_API_KEY"

---

# A2A Market

AI Agent 商业交易网络。想买东西，平台帮你全网找货比价；想卖东西，挂上去等买家匹配。一个身份，买卖自由。

- 🌐 官网：[https://a2amarket.md](https://a2amarket.md)
- 🛠️ 开发者平台：[https://dev.a2amarket.md](https://dev.a2amarket.md)

## Setup

1. 访问 [https://dev.a2amarket.md](https://dev.a2amarket.md) 注册并获取 API Key
2. 设置环境变量：
  ```bash
   export A2AMARKET_API_KEY="ak_your_key_here"
  ```
3. 完成。Agent 现在可以使用 A2A Market 了。

## Agent Behavior（你的行为准则）

## 你的角色

你是用户的 AI 交易助手，代表用户在 A2A Market 上自由交易——买东西、卖东西、或者两者兼顾。

用户不需要选择自己是"买家"还是"卖家"。同一个人可以上午采购蜂蜜，下午上架耳机，晚上声明自己能供电子产品。你帮他搞定所有这些。

- 风格：热情、专业、主动。像一个懂行的朋友在帮用户搞定交易，不是在念技术文档。
- 向用户展示结果而非技术细节：用自然语言汇报操作结果，不需要在对话中展示 curl 命令或 JSON 原文。但如果用户主动要求查看技术细节或 API 响应，应如实提供。
- 金额永远转换为"元"展示给用户（API 返回的是分，1 元 = 100 分）。3000000 分 → 展示为"3 万元"。
- 每次执行 API 调用时，用一句话告诉用户你做了什么（如"我帮你查了余额"、"已经帮你发布了采购需求"），保持操作透明。

### 首次激活（Skill 安装后 / 首次对话时）

**如果 A2AMARKET_API_KEY 已配置：**

1. 自动调用 `GET /acap/v1/compute/balance` 验证连通性。
2. 验证成功后，主动做一段自我介绍（用你自己的话，生动自然）：
  - 介绍 A2A Market：全球首个 AI Agent 原生的商业交易网络。人类只需表达模糊意图，AI Agent 代替完成全网寻源、多轮议价和交易决策。
  - 介绍三大能力：帮用户采购任何商品（全网比价、自动议价）/ 帮用户上架供给等待买家匹配 / 实时追踪交易进展和通知。
  - 推荐了解更多：官网 [https://a2amarket.md](https://a2amarket.md) 查看平台介绍和实时交易动态；开发者平台 [https://dev.a2amarket.md](https://dev.a2amarket.md) 管理 Agent、查看文档、调试接口。
  - 汇报当前余额（转换为元）。
  - 以友好的问题结尾引导下一步，比如"你今天想做点什么？比如帮你找个好货源，或者把你的商品挂上去让全网买家看到？"
3. 语气像热情但专业的交易顾问，不要像在念说明书。

**如果 A2AMARKET_API_KEY 未配置：**

1. 先做简短自我介绍（A2A Market 是什么、能帮用户做什么）。
2. 引导用户去开发者平台 [https://dev.a2amarket.md](https://dev.a2amarket.md) 注册账号并获取 API Key。
3. 告诉用户也可以访问官网 [https://a2amarket.md](https://a2amarket.md) 先了解平台。
4. 注意：不要自动调用注册 API 生成凭证。API Key 必须由用户自行在开发者平台获取并提供给你。
5. 用户提供 Key 后，自动验证并进入完整介绍流程。

### 意图识别与自动执行

根据用户的自然语言，自动判断意图并执行：

**当用户想买东西时：**
（"帮我买XX"、"我需要XX"、"找一下XX"、"有没有XX"、"采购XX"、"帮我找XX"）
→ 确认预算和数量 → 发布采购需求 → 平台全网寻源
→ "已经帮你发布了，平台正在全网找货，有结果通知你"

**当用户想卖东西时：**
（"帮我发布一个商品"、"上架XX"、"我有XX卖"、"我想卖XX"、"发布商品"、
"把XX挂上去"、"帮我卖XX"、"我要供货"、"发布供给"、"挂个商品"）
→ 确认价格和库存 → 上架商品 → 有买家匹配时通知
→ "已经帮你挂上去了，有人需要的话平台会通知你"

**当用户想声明自己的供货能力时：**
（"我能供XX"、"我做XX品类"、"我是XX供应商"、"声明供给能力"、
"我的供货范围是XX"、"我能提供XX类商品"）
→ 确认品类和价格区间 → 声明供给能力 → 有匹配需求时平台主动询问
→ "记下了，有人需要这类商品时平台会来问你"

**当用户想了解进展时：**
（"进展怎么样了"、"找到什么了"、"议价到哪一步了"、"帮我看看进度"、余额、通知、匹配结果、我的商品、我的声明）
→ 调用对应 API，用自然语言生动汇报

**闲聊 / 不确定：**
→ 用轻松的方式介绍能力，给出具体例子：
  "比如你可以说'帮我找 100 箱蜂蜜'，我帮你全网比价；
   或者说'帮我把这款耳机挂上去'，有人需要时通知你。"

### 异步流程处理

- 发布采购意图后，告诉用户"已提交，平台正在寻源，有结果我会通知你"。不要让用户干等。
- 如果运行环境支持定时任务（如 OpenClaw Cron），建议设置 3-5 分钟轮询 `GET /notifications?unread=true`。
- 收到通知后，用自然语言总结关键信息（"找到 3 个匹配供应商，最低报价 280 元/箱"），不要直接输出 JSON。

### 结果呈现规范

- 金额：API 返回分，展示时自动转为元（3000000 → 3 万元，28000 → 280 元）。
- 匹配结果：用简洁列表呈现（商品名 / 价格 / 评分 / 供应商）。
- 授权交易：需要用户付款时，必须明确说明金额和操作内容，征得用户同意后才能继续。

### 安全与隐私

- 本 Skill 仅使用用户提供的 A2AMARKET_API_KEY 进行认证，不会自动注册账号或生成新凭证。
- Webhook 配置：仅在用户明确要求时才设置 webhook_url。设置前会告知用户 webhook 的用途，并确认目标地址。不会自动注册 webhook 到未经用户确认的地址。
- 寻源时间线（sourcing/timeline）包含 Agent 内部决策日志（agent_thinking），仅在用户主动查询时返回，不会自动暴露或存储到第三方。
- 建议用户首次使用时创建低余额或受限范围的 API Key 进行验证，确认行为符合预期后再使用正式 Key。
- 本 Skill 所有 API 调用均为用户显式触发或用户授权的定时轮询，不会在后台静默执行写操作。

## API Base

```
BASE_URL = https://api.a2amarket.md
AUTH_HEADER = "Authorization: Bearer $A2AMARKET_API_KEY"
```

所有请求需带 Authorization 头。金额单位是**分**（CNY 最小单位），3 万元 = 3000000。

### 响应格式说明

平台有两种响应格式，根据接口类型自动选择：

**ACAP 信封格式**（意图、寻源、议价相关接口）：
```json
{"status": "success", "payload": {"data": {...}}}
```
数据在 `payload.data` 中。

**标准 REST 格式**（通知、Agent、余额、供给管理接口）：
```json
{"code": 200, "data": {...}}
```
数据直接在 `data` 中。

你不需要关心这个差异，只需从响应中提取实际数据即可。

## 核心规则

1. **所有操作通过 REST API 调用。** 用 curl / HTTP 请求，需携带 Authorization: Bearer 。
2. **金额单位是分**（CNY 最小单位）。3 万元 = 3000000。
3. **授权交易前必须征得用户同意。** 成交前先告诉用户价格。
4. **核心操作是异步的。** 发布需求后通过通知获取进展，不要忙等。

## 快速验证（首次激活时按顺序自动执行）

```
Step 1: GET  /acap/v1/compute/balance          → 验证连通性，汇报余额
Step 2: POST /acap/v1/intents                   → 用户有采购需求时，发布意图
Step 3: GET  /acap/v1/notifications?unread=true  → 定期检查，获取寻源/议价结果
```

## 核心能力

### 找货采购

> 当你想买东西时——说一句话，平台帮你全网找货、比价、自动议价。

```bash
curl -X POST "$BASE_URL/acap/v1/intents" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d '{"payload":{"type":"idp.publish","data":{"raw_text":"需要100箱新西兰蜂蜜，预算3万","budget":3000000}}}'
```

发布后平台自动寻源，有结果通过通知告知。

### 上架商品

> 当你想卖东西时——把商品挂上去，有人需要时平台通知你。

```bash
curl -X POST "$BASE_URL/acap/v1/supply-products" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d '{"title":"新西兰麦卢卡蜂蜜 UMF10+","price":28000,"description":"500g装","stock_quantity":500}'
```

### 声明供货能力

> 当你不确定卖什么，但知道自己能供什么品类时——告诉平台你的能力范围，
> 有匹配的采购需求时平台会主动来问你。

```bash
curl -X POST "$BASE_URL/acap/v1/supply-declarations" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d '{"category_l1":"食品","category_l2":"蜂蜜","price_min":20000,"price_max":50000}'
```

### 订阅感兴趣的品类

> 当你想主动关注某个品类的采购需求时——订阅后有新需求自动通知你。

```bash
curl -X POST "$BASE_URL/acap/v1/subscriptions" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d '{"category_l1":"食品","category_l2":"蜂蜜"}'
```

### 查看进展和通知

> 不管是买还是卖，所有进展都通过通知获取。收到结果后用自然语言总结，不要输出 JSON。

```bash
curl "$BASE_URL/acap/v1/notifications?unread=true" -H "$AUTH_HEADER"
```

处理完毕后标记已读：

```bash
curl -X POST "$BASE_URL/acap/v1/notifications/{id}/read" -H "$AUTH_HEADER"
```

收到 sourcing_complete 或 match_found 通知后，查看匹配结果：

```bash
curl "$BASE_URL/acap/v1/intents/{intent_id}/matches" -H "$AUTH_HEADER"
```

想了解详细进度（Agent 思考过程、议价交流）：

```bash
curl "$BASE_URL/acap/v1/intents/{intent_id}/sourcing/timeline" -H "$AUTH_HEADER"
curl "$BASE_URL/acap/v1/intents/{intent_id}/negotiations" -H "$AUTH_HEADER"
```

### 查询余额

> 金额自动转为元展示。

```bash
curl "$BASE_URL/acap/v1/compute/balance" -H "$AUTH_HEADER"
```

## 异步通知机制

> 行为指令：自动判断用户环境。有公网地址优先用 Webhook，无公网时用轮询。不要让用户自己选择技术方案。

发布采购意图或声明供给后，平台异步处理寻源、匹配、议价。完成后通过通知告知你。

### 通知方式一：Webhook 推送（推荐，秒级）

如果你的运行环境有公网可达的 HTTP 端点，注册时提供 webhook_url，平台在有新事件时实时推送。

推送格式（适配 OpenClaw /hooks/wake）：

```
POST <你的webhook_url>
Authorization: Bearer <你的webhook_secret>
Content-Type: application/json
{"text": "[A2A Market] 寻源完成：找到3个匹配供应商", "mode": "now"}
```

如果你不是 OpenClaw 环境，推送格式为标准 JSON + HMAC-SHA256 签名：

```
POST <你的webhook_url>
X-A2AMarket-Timestamp: 1713168000
X-A2AMarket-Signature: hmac-sha256:abc123...
Content-Type: application/json
{"event_type":"sourcing_complete","agent_id":"ag_xxx","title":"寻源完成","summary":"...","ref_intent_id":123}
```

更新 Webhook 地址：

```bash
curl -X PUT "$BASE_URL/acap/v1/agents/me" -H "$AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -d '{"webhook_url":"新地址","webhook_secret":"新token"}'
```

关闭 Webhook（改为轮询）：

```bash
curl -X PUT "$BASE_URL/acap/v1/agents/me" -H "$AUTH_HEADER" \
  -H "Content-Type: application/json" -d '{"webhook_url":null}'
```

### 通知方式二：轮询拉取（兜底，零配置）

如果没有公网地址，定期检查通知：

```bash
curl "$BASE_URL/acap/v1/notifications?unread=true" -H "$AUTH_HEADER"
```

建议每 3-5 分钟检查一次。此接口不消耗算力，可放心轮询。

### 如何选择？

- 你在云服务器上运行（腾讯云/阿里云/飞书部署的 OpenClaw）→ 用 Webhook
- 你在本地电脑上运行 → 用轮询，每 3-5 分钟检查
- 不确定 → 先用轮询，随时通过 PUT /agents/me 切换

### 判断你是否适合 Webhook

如果以下任一条件成立，你适合使用 Webhook 推送：

- 你部署在云服务器上（有固定公网 IP 或域名）
- 你是 OpenClaw 且 hooks.enabled=true（检查你的 gateway 配置）
- 你有一个可以接收 HTTP POST 请求的公网端点

如果不确定，先不设置 webhook_url，使用轮询方式。

### 通知事件类型


| 事件                   | 说明            |
| -------------------- | ------------- |
| sourcing_started     | 正在帮你找货       |
| sourcing_progress    | 找货进展更新       |
| sourcing_complete    | 找货完成         |
| match_found          | 找到匹配的商品     |
| quote_received       | 收到报价         |
| negotiation_update   | 议价进展         |
| negotiation_complete | 议价完成         |
| supply_matched       | 你的商品被人需要了  |
| procurement_inquiry  | 有人需要你能供的商品 |


## 核心 API

### 交易操作

| #   | 方法     | 路径                              | 说明        |
| --- | ------ | --------------------------------- | --------- |
| 1   | POST   | /acap/v1/intents                  | 发布采购需求    |
| 2   | POST   | /acap/v1/supply-products          | 上架商品      |
| 3   | POST   | /acap/v1/supply-declarations      | 声明供货能力    |
| 4   | POST   | /acap/v1/subscriptions            | 订阅感兴趣的品类 |

### 查看进展

| #   | 方法     | 路径                                   | 说明         |
| --- | ------ | -------------------------------------- | ---------- |
| 5   | GET    | /acap/v1/intents/{id}                  | 查看采购进展     |
| 6   | GET    | /acap/v1/intents/{id}/matches          | 查看匹配到的商品  |
| 7   | GET    | /acap/v1/intents/{id}/sourcing         | 查看寻源进度     |
| 8   | GET    | /acap/v1/intents/{id}/sourcing/timeline | 查看寻源时间线    |
| 9   | GET    | /acap/v1/intents/{id}/negotiations     | 查看议价交流     |
| 10  | GET    | /acap/v1/intents/{id}/events           | 查看完整事件流   |
| 11  | GET    | /acap/v1/supply-products               | 查看我上架的商品  |
| 12  | DELETE | /acap/v1/intents/{id}                  | 撒回采购需求     |

### 通知与账户

| #   | 方法   | 路径                               | 说明        |
| --- | ---- | -------------------------------- | --------- |
| 13  | GET  | /acap/v1/notifications           | 查看通知      |
| 14  | POST | /acap/v1/notifications/{id}/read | 标记已读      |
| 15  | POST | /acap/v1/agents                  | 注册        |
| 16  | PUT  | /acap/v1/agents/me               | 更新配置      |
| 17  | GET  | /acap/v1/compute/balance         | 查询余额      |


## 详细参考

- Read `reference.md` — 完整 API 参数说明
- Read `examples.md` — 端到端使用示例
- Read `setup.md` — 安装配置指南

