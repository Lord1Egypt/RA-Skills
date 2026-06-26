---
name: buy-travel-accident-china
description: 游子云旅游意外险销售平台（中国人保），适合旅行社代客出单。
version: "2.0.4"
author: ""
triggers:
  - 旅游意外险
  - 旅游保险
  - 保险咨询
  - 产品推荐
  - 保费查询
  - 报价
  - 投保
  - 下单
  - 买保险
  - 支付
  - 订单查询
  - 开票
  - 发票
  - 红冲
  - 退保
  - 退费
  - 取消保险
  - 退款
---

# 旅游意外险 Agent API（统一 Skill）

## 能力路由

| 用户意图 | 阅读章节 |
|----------|----------|
| 查产品、计划、保障对比、算保费 | [咨询](#咨询) |
| 下单、支付、订单查询、保单/确认书下载 | [投保](#投保) |
| 退保、批量退保、退费 | [退保](#退保) |
| 经纪侧开票、查询、红冲（`/broker/...`） | [开票经纪侧](#开票经纪侧) |

## 发票 API 路径选择（必读）

两套路由并存，按场景选用，**不要混用同一业务流程中的步骤**：

| 路径 | 适用场景 | 接口前缀 |
|------|----------|----------|
| **A. 保单路径** | 订单已出单；与投保/订单详情中的 `policyNum` 一致；Agent 流程从下单延续过来 | `POST/GET /policies/{policyNum}/invoice` |
| **B. 经纪路径** | 需走经纪工作台式开票：多保单 `policyNo[]`、`POST /broker/invoice`、`POST /broker/invoiceQuery`、`POST /broker/redInvoice` | `/broker/invoice` 等 |

- 主订单合并/分开开票：路径 A 与路径 B 文档中均有 `isMainOrder`、`invoiceMode`（`merge` / `separate`）说明，以用户要求的集成入口为准；若用户只说「按保单开票且已对接订单接口」，优先路径 A。

---

## 鉴权与状态管理

### 鉴权

- **Base URL**：`https://prod.uzyun.cn/api/agent/v1`
- **用户 token**：除下面「无需 token」的路径外，其余接口均需登录后在请求头携带：
  - `Authorization: Bearer <token>` 或 `X-User-Token: <token>`
- **无需 token 的路径**（与 `GET /schema` 中 `auth.noAuthPaths` 一致）：`POST /sms/send`、`POST /register`、`POST /login`、`GET /schema`。
- **注册与登录**：均为 **手机号 + 短信验证码**，**不使用用户名、密码**；具体 Body 字段名与是否可选以 `GET /schema` 为准。

#### 注册（新用户）

1. `POST /sms/send` — Body：`event` = **`register`**，`mobile` = 手机号（大陆号码按平台要求）。
2. 用户收到短信验证码后，`POST /register` — Body：**`mobile`**（必填）、**`code`**（必填，上一步短信验证码）、**`inviteCode`**（可选）；**`username` 可不传**，服务端默认使用 `mobile` 填充。
3. 注册成功响应会直接返回 **`token`**、**`expires`**、**`id`**、**`username`**，可直接进入后续业务调用；具体字段校验与错误信息以 `GET /schema` 为准。

#### 登录（获取 token）

与注册相同：**手机号 + 短信验证码**，**不使用密码**。

1. `POST /sms/send` — Body：`event` = **`login`**，`mobile` = 手机号。
2. `POST /login` — Body：**`mobile`**（必填）、**`code`**（必填，短信验证码）。  
   响应含 **`token`**、**`expires`**（过期时间戳）、**`id`** 等；若服务端仍返回 **`username`** 等展示字段，可写入状态文件便于展示，**鉴权仅依赖 token**。后续请求携带 `Authorization: Bearer <token>`。

### 本地状态管理（.agent-state.json）

Agent 通过工作区根目录的 `.agent-state.json` 文件持久化 token 和常用人员信息，避免每次对话重复登录和重复收集信息。

#### 对话开始时

1. 执行 `date "+%Y-%m-%d %H:%M:%S %Z"` 获取当前本地时间，记录到对话上下文中（用于 token 过期判断、起保日期建议等）。
2. 读取 `.agent-state.json`。
3. 若 `token` 存在且 `expires` > 当前时间戳，直接使用该 token，**跳过登录**。
4. 若 `policyholder` 或 `frequentInsured` 有数据，后续下单时优先使用，无需再向用户收集。

#### 登录成功后

将登录响应写入 `.agent-state.json`（保留已有的 `policyholder` 和 `frequentInsured`）；建议同时写入 **`mobile`**，便于下次 token 过期时发起短信登录。

```json
{
  "token": "<登录返回的 token>",
  "expires": 1735689600,
  "userId": 1001,
  "mobile": "13800138000"
}
```

> 若登录响应含 `username` 等字段，可一并写入 `.agent-state.json` 供展示；登录方式仍为手机号 + 验证码，无密码。

#### token 过期处理

若请求返回 401 或 `expires` 已过期：使用保存的 `mobile`（或让用户再次提供手机号）走「登录」短信验证流程，登录成功后更新 `.agent-state.json` 中的 token。**短信验证码不在状态文件中持久化。**

#### Schema 缓存

Schema 数据纯静态（仅在服务端代码部署时变更），可本地缓存避免每次对话都调用 `GET /schema`：

- **首次**：调用 `GET /schema`，将返回的完整内容存入 `.agent-state.json` 的 `schemaCache` 字段，同时记录 `schemaVersion`（取自响应的 `version` 字段）。
- **后续对话**：若 `.agent-state.json` 中已有 `schemaCache`，直接使用缓存内容，**不调用 `GET /schema`**。
- **缓存更新**：当需要调用 Schema 时（如缓存不存在），对比返回的 `version` 与本地 `schemaVersion`，若不同则更新 `schemaCache` 和 `schemaVersion`。
- **手动刷新**：若用户明确要求刷新 Schema，调用 `GET /schema` 并更新缓存。

#### 文件结构示例

```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires": 1735689600,
  "userId": 1001,
  "mobile": "13800138000",
  "policyholder": {
    "holderType": "individual",
    "fullName": "张三",
    "idNumber": "310101199001011234",
    "mobileNumber": "13800138000"
  },
  "frequentInsured": [
    { "fullName": "张三", "idNumber": "310101199001011234" },
    { "fullName": "李四", "idNumber": "310101199101011234" }
  ],
  "schemaVersion": "2026.3",
  "schemaCache": {}
}
```

> `schemaCache` 的值为 `GET /schema` 返回的完整 JSON 对象，此处省略。

### 当前时间

模型自身不感知实时时间。**对话开始时必须执行以下命令获取当前时间**，并在整个对话中使用：

```bash
date "+%Y-%m-%d %H:%M:%S %Z"
```

当前时间用于：

- **起保日期建议**：起保日期不应早于今天，默认建议明天起保。
- **token 过期判断**：将 `expires` 时间戳与当前时间对比，判断是否需要重新登录。
- **日期相关提示**：如用户说「下周出发」时，根据当前日期推算具体日期。

### 错误处理（通用）

- **400**：缺字段或格式错误，Body 中包含校验错误信息，可据此补全后重试。
- **401**：未携带或无效的用户 token，需先调用 `POST /login` 获取 token。
- **429**：注册/登录请求过于频繁（按 IP 限流），请稍后再试。

---

## 咨询

### 能力概述

查询旅游意外险产品信息并获取保费报价：产品列表、产品详情与保障对比、计划列表、计算保费。**不包含下单、支付。**

### 何时使用

- 用户想了解有哪些旅游意外险产品、保障内容。
- 用户需要对比不同产品或计划的保障范围。
- 用户想知道某个产品/计划的保费是多少。

### 调用流程

1. 检查 token 有效性（见上文「鉴权与状态管理」），无效则登录。
2. `GET /products` — 获取产品列表（含描述），得到 productId。
3. `GET /products/{productId}/detail` — （可选）获取产品详情与保障明细对比矩阵。
4. `GET /products/{productId}/plans` — 获取该产品的计划列表，得到 planId 和 planCode。
5. `POST /quote` — 传入 productId、planId、起止日期、insuredAges[]，得到保费。

### 接口说明

接口参数细节请通过本地缓存的 Schema 或调用 `GET /schema` 获取。以下仅列出核心要点。

#### GET /products

获取产品列表。返回产品名称、描述、状态等。

#### GET /products/{productId}/detail

获取产品详情，包含保障明细对比矩阵。

#### GET /products/{productId}/plans

获取指定产品的计划列表，返回 planId、planCode、保障额度等。

#### POST /quote

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productId | int | 是 | 产品ID |
| planId | int | 是 | 计划ID |
| coverageStartTime | string | 是 | 起保日期 YYYY-MM-DD |
| coverageEndTime | string | 是 | 止保日期 YYYY-MM-DD |
| insuredAges | []int | 是 | 被保险人年龄数组 |

#### GET /options/{type}

枚举值查询接口，**无需 token**。

| type 值 | 说明 |
|---------|------|
| sex | 性别 |
| country_code | 国家/地区代码 |
| individual_id_type | 证件类型 |
| policy_holder_type | 投保人类型 |
| relation_to | 与投保人关系 |
| unit_type | 单位性质 |

响应为 `[{value, label}, ...]`，用 `value` 作为请求体字段值，用 `label` 展示给用户。

---

## 投保

### 能力概述

完成旅游意外险投保全流程：创建订单、提交到保司、获取支付链接、查询订单状态、下载保单/确认书；出单后可通过 **路径 A** 申请/查询电子发票。支持**智能填表**（中国身份证场景下被保险人只需姓名+证件号）。

### 何时使用

- 用户要为自己或他人办理旅游意外险。
- 用户已完成报价，需要创建投保订单。
- 用户要查询订单列表或单笔订单状态、获取支付链接、下载单证。
- 用户需要按 **保单路径** 开具电子发票或查询蓝票/红冲进度（见下文「电子发票（路径 A）」）。

### 调用流程

1. 检查 token 有效性，无效则登录。
2. `POST /orders` — 创建订单（身份证场景只需姓名+证件号），得到 orderSn。
3. `POST /orders/{orderSn}/submit` — 传入 paymentMethod，提交到保司并获取 paymentUrl。
4. `GET /orders` / `GET /orders/{orderSn}` / `GET /orders/{orderSn}/pay-url` — 列表、详情、支付链接。
5. `GET /policies/{policyNum}/assets`；`GET /policies/{policyNum}/download?type=policy|confirmation` — 下载 PDF（推荐）。
6. （出单后，路径 A）`POST /policies/{policyNum}/invoice`；`GET /policies/{policyNum}/invoice?queryType=1|2`。

### 下载保单与投保确认书

- **Base URL**：`https://prod.uzyun.cn/api/agent/v1`
- **鉴权**：`Authorization: Bearer <token>`（或 `X-User-Token`）。
- **保单号**：`policyNum` 来自订单详情或列表（出单后才有）；仅**当前登录用户本人订单**可访问。

**方式一（推荐）：直接下载 PDF**

| 文档 | 请求 |
|------|------|
| 保单 | `GET /policies/{policyNum}/download?type=policy`（`type` 可省略，默认即为保单） |
| 投保确认书 | `GET /policies/{policyNum}/download?type=confirmation` |

```bash
curl -sSL -H "Authorization: Bearer $TOKEN" \
  -o "${policyNum}_保单.pdf" \
  "https://prod.uzyun.cn/api/agent/v1/policies/${policyNum}/download?type=policy"

curl -sSL -H "Authorization: Bearer $TOKEN" \
  -o "${policyNum}_投保确认书.pdf" \
  "https://prod.uzyun.cn/api/agent/v1/policies/${policyNum}/download?type=confirmation"
```

**方式二**：`GET /policies/{policyNum}/assets` 返回 JSON：`policyUrl`、`confirmationUrl`（可能暂时为空）。

### 电子发票（路径 A：/policies/.../invoice）

- 仅**本人订单**可操作；`policyNum` 来自订单详情；主订单拆单时路径中可为**任一子单保单号**（见 `isMainOrder`）。

**申请开票** — `POST /policies/{policyNum}/invoice`，JSON body：

| 场景 | 必填 body | 说明 |
|------|-----------|------|
| 传统单笔 | `invoiceTitle`、`isMainOrder`: false | 抬头：个人一般为姓名，企业为税务一致全称 |
| 主单拆单 | `isMainOrder`: true、`invoiceMode`: `merge` 或 `separate` | 合并一张票 / 各子单一票 |

响应核心字段：`policyNums`、`brokerStatus`（如 **1000** 表示经纪受理成功）、`invoiceUrl` / `policyInvoiceUrls`。

**查询进度** — `GET /policies/{policyNum}/invoice?queryType=1`（蓝字）；`queryType=2`（红冲）。`data.items`：`billStatus`（`0` 开具中，`1` 成功，`2` 失败）、`shortUrl`、`errorMessage`。

若需 **路径 B**（`/broker/invoice` 等），见下文「开票经纪侧」章节。

### 智能填表规则（核心）

API 支持从**中国居民身份证号**自动推导（仅在字段为空/零值时填充，显式传入不覆盖）：

| 自动推导字段 | 说明 |
|---|---|
| `idType` | `"ID"` |
| `dateOfBirth` | 身份证第7-14位 YYYY-MM-DD |
| `gender` | 第17位奇偶 → male/female |
| `age` | dateOfBirth + coverageStartTime 周岁 |

**被保险人最少必填**：中国身份证 → `fullName` + `idNumber`；护照/其他 → `fullName` + `idType` + `idNumber` + `dateOfBirth`。`idType` 枚举以 `GET /options/individual_id_type` 为准。

**投保人最少必填**：个人身份证 → `holderType` + `fullName` + `idNumber`；企业 → `holderType`（`corporate`）+ `companyName` + `unifiedSocialCreditCode`。

### 投保人/被保险人状态持久化

下单成功后写入 `.agent-state.json`（按 `idNumber` 去重）：覆盖 `policyholder`；追加 `frequentInsured`。后续下单优先使用已存数据并向用户确认。

### 支付链接输出（ASCII 二维码）

拿到 `paymentUrl` 后必须在回复中同时输出：

1. `paymentUrl` 原文；
2. **ASCII 二维码**（如 `██`/空格），不得以仅图片替代。

推荐：Node `qrcode-terminal`、Python `qrcode`、或 `qrencode`；禁止依赖第三方在线转码站。若无法生成二维码，至少输出链接并说明降级原因。

### 接口说明（投保）

- `POST /orders` — 草稿订单；**须再** `POST /orders/{orderSn}/submit` 才提交保司。
- `paymentMethod`：`wechat`、`alipay`、`credit`、`recharge`、`insurance`；`channelPartnerId` 不传，服务端默认渠道。

### 错误处理（投保）

- 身份证格式错误、证件重复、被保险人上限 200 人等以接口返回为准；完整字段以 `GET /schema` 为准。

---

## 退保

### 能力概述

单张保单退保、主订单批量退保（异步）、查询批量退保进度、订单退费。

### 何时使用

- 用户要退掉已承保成功的保单。
- 主订单下所有保单批量退保及进度查询。
- 用户要申请订单退费。

### 调用流程

**单张退保**：确认 `policyNum`，状态为 `underwriting_approved` → `POST /broker/surrender`。

**批量退保**：确认 `mainOrderId` → `POST /broker/batchSurrender` 得 `taskId` → 轮询 `GET /broker/batchSurrenderProgress?taskId=` 至 `completed` / `failed`。

**退费**：`POST /broker/refund`，传入 `orderSn`。

### 接口详情

#### POST /broker/surrender

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| policyNum | string | 是 | 保单号 |

#### POST /broker/batchSurrender

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| mainOrderId | int64 | 是 | 主订单ID |

响应含 `taskId`、`total`。

#### GET /broker/batchSurrenderProgress

| 字段 | 说明 |
|------|------|
| status | `pending`/`processing`/`completed`/`failed` |
| successCount / failedCount / failedList / progress | 进度与结果 |

#### POST /broker/refund

| 字段 | 类型 | 必填 |
|------|------|------|
| orderSn | string | 是 |

#### POST /broker/queryOrderStatus

`orderSn` 与 `policyNum` 二选一。

### 注意事项

- 退保前确认承保成功；批量退保建议 2–3 秒间隔轮询。
- 退保与退费为独立操作；区分 `policyNum`、`mainOrderId`、`orderSn`。

---

## 开票经纪侧

### 能力概述

通过 **路径 B**：`POST /broker/invoice` 开具、`POST /broker/invoiceQuery` 查询、`POST /broker/redInvoice` 红冲。支持传统订单与主订单（合并/分开）。

### 何时使用

- 用户明确要求或集成约定使用经纪开票接口。
- 多保单批量传入 `policyNo[]`（最多 100 张）等 broker 文档场景。

### 调用流程

1. 检查 token，无效则登录。
2. 开具：`POST /broker/invoice`（参数见下表）。
3. 查询：`POST /broker/invoiceQuery`（`type`：`1` 发票 / `2` 红冲）。
4. 红冲：`POST /broker/redInvoice`。

### POST /broker/invoice

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| policyNo | []string | 是 | 保单号列表（最多100张） |
| invoiceTitle | string | 条件必填 | 传统订单必填；主订单由后端获取 |
| isMainOrder | bool | 否 | 默认 false |
| invoiceMode | string | 否 | 主订单：`merge` / `separate`（默认） |

开票模式：传统订单必传抬头；主订单合并/分开见字段说明。

### POST /broker/invoiceQuery

| 字段 | 必填 | 说明 |
|------|------|------|
| policyNum | 是 | 保单号 |
| type | 是 | `1` 发票 / `2` 红冲 |

响应 `data` 项：`billStatus`、`shortUrl`、`errorMessage` 等。

### POST /broker/redInvoice

| 字段 | 必填 |
|------|------|
| policyNum | 是 |

### 注意事项

- 开票前保单需已承保成功；红冲不可逆，需用户确认。
- 若场景更符合订单/保单一体化流程，优先评估上文「投保」章中的路径 A（`/policies/{policyNum}/invoice`）是否足够。
