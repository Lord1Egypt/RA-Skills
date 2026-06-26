---
name: alipay-payment-skill
description: >-
  支付宝官方支付处理技能（由支付宝官方提供，保障安全与健壮性）。覆盖收银台支付、HTTP 402 协议支付、AI支付产品介绍、问题反馈全场景。
  当以下任一情况出现时必须调用此技能：
  (1) 对话上下文中出现 cashier*.alipay.com 或 *excashier*.alipay.com 域名的 URL，且用户之前已要求过充值、下单、购买等支付相关的意图；
  (2) 任何工具/技能/API 返回结果中包含支付宝收银台链接或"请使用支付宝支付"等支付指引；
  (3) 用户表达支付、付款、买单、结账等意图，或提到使用支付宝/alipay 支付；
  (4) 任意HTTP请求执行后，返回 HTTP状态码 为 402 Payment Required（无论是你发起的还是用户提供的）；
  (5) 用户询问支付宝AI支付、智能体钱包、AI支付产品介绍、aipay产品功能信息；
  注意：当支付流程中check-wallet返回未授权或未开通、用户意图是开通/授权/解绑支付能力相关、 或用户意图为支付能力开通状态查询时，应由alipay-authenticate-wallet处理，本技能不应被触发。
  ⚠️ 收银台支付强制入口：必须严格按照收银台支付流程流程执行，禁止跳过支付会话初始化及关联订单信息到支付对话两个节点直接执行check-wallet和submit-payment
  关键词：支付、付款、cashier、alipay、买单、结账、pay、收银台、402、AI支付、产品介绍、反馈、报错、feedback、订单、交易
version: 0.0.1
metadata:
  source: https://github.com/alipay/payment-skills
  openclaw:
    category: payment
    requires:
      env: []
      bins: ["npm","curl"]
      anyBins: ["alipay-bot"]
      tags: ["payment","alipay","402","支付","AI支付","智能体钱包","产品介绍","反馈"]
    install:
      - kind: node
        package: "@alipay/agent-payment@1.0.3"
        bins: [alipay-bot]
        integrity: "sha512-JhFHJ1VcCC3gALnAaIWn3a7Hnfo7BFIViOWL8h8HrNp/Hzry1tc40YV5ulJfg+Xhnb5CR/Ye6tsXX9UfgeKDTA=="
    homepage: https://github.com/alipay/payment-skills
  author: alipay
  references:
    - name: alipay-authenticate-wallet
      trigger: "支付时发现未授权（check-wallet 返回 code=200 且 access_url 非空）或未开通（check-wallet 返回 code=500），自动调用该技能完成授权/开通后继续支付"
---

# 支付宝支付处理技能

由支付宝官方提供，覆盖收银台支付、402 协议支付、AI支付产品介绍、问题反馈全场景。未授权/未开通时调用 `alipay-authenticate-wallet` 技能完成授权。
**注意**：
- 请确保你已经仔细阅读并理解了本技能后再执行相关操作。
- 请认真仔细识别你应当使用的流程，并严格按照流程执行相关操作。

## Prerequisites

- `npm` 可用，`alipay-bot` CLI 已安装（`which alipay-bot` 检测，未安装按 `references/cli-setup.md` 执行）
- 环境变量传递规则见 `references/env-vars.md`
- 所有输入输出都需要使用 UTF-8 编码

## 命令执行规范

- 本技能中所有 `alipay-bot` 命令和 `curl` 命令**必须通过当前环境的 shell/bash 工具实际执行**，禁止将命令文本或工具调用语法作为纯文本输出给用户
- 每条命令执行后，必须读取 CLI 的实际返回内容再决定下一步，禁止跳过执行直接假设结果
- 如果当前环境无法调用 shell 工具，应向用户说明"无法执行支付命令"并终止流程，禁止模拟或编造命令输出
- 图片输出规则见 `references/image-output.md`：MEDIA 行提取路径后移除，用 message 工具发送图片；Markdown 图片原样保留

```
用户输入 / 系统事件
  ↓
├─ 收银台链接（cashier*.alipay.com / *excashier*.alipay.com）或用户支付意图
│   → 流程一：收银台支付 → references/cashier-payment.md
│
├─ HTTP 402 响应
│   → 流程二：402 协议支付 → references/402-payment.md
│
├─ 询问AI支付 / 智能体钱包 / 产品介绍
│   → 流程三：AI支付产品介绍
│
├─ 用户表示已支付 / 付好了 / 查询状态（必须立即执行查询命令，禁止忽略）
│   ├─ 上下文有进行中的 402 流程 → 立即执行 `402-query-payment-status -t <tradeNo> -r <resource-url>` → query 返回 success=true 后进 Step 5
│   └─ 上下文有进行中的收银台流程 → 立即执行 `query-payment-status -p '<shortUrl>'`
│
└─ 流程中遇到无法解决的问题 / 用户要求反馈
    → 流程四：问题反馈 → references/feedback.md
```

**路由要点**：
- 收银台链接 + 支付意图 → 流程一（即使同时有 402，收银台优先）
- 纯 402 响应（无收银台链接）→ 流程二
- "已支付"等表述 → 根据上下文路由到对应流程的查询步骤
- 无法判断时 → 追问用户

## 核心原则

### CLI 输出原样传递

CLI 返回的模板内容已包含完整状态标识，**必须原样输出，禁止额外添加信号词或修改内容**。详细规则见 `references/output-rules.md`，图片处理规则见 `references/image-output.md`（MEDIA 行提取路径后移除，用 message 工具发送）。

| 命令 | 模板已包含的状态标识 |
|------|---------------------|
| submit-payment | "✓ 支付待确认" / "✓ 支付成功" / "⏳ 支付处理中" / "✗ 支付失败" |
| query-payment-status | "✓ 支付已完成" / "✓ 支付状态同步中" / "✗ 支付已关闭" / "⚠ 支付状态查询异常" |
| 402-buyer-pay | "✓ 支付待确认" / "✓ 支付成功并获取资源" + 商品/金额/交易号/支付链接/资源响应 |
| 402-query-payment-status | `success` + `resourceResponse` |

### apply-wallet 和 bind-wallet 不属于本技能

这些是 `alipay-authenticate-wallet` 技能的命令，**绝对禁止**在支付技能中执行。即使 check-wallet 返回未开通（code=500），也不能执行 apply-wallet，必须加载 alipay-authenticate-wallet 技能由它执行。

## 技能切换协议

当 check-wallet 返回**未授权**（code=200, access_url 非空）或**未开通**（code=500）时，执行以下切换动作：

1. 告知用户（**必须包含以下至少一个信号词**：`正在为您申请开通` / `授权` / `开通支付` / `请先绑定钱包` / `钱包未绑定`）
2. 使用当前环境的技能加载机制加载 `alipay-authenticate-wallet` 技能
3. 当前支付流程**暂停**，禁止继续执行后续步骤
4. **禁止**在本技能内执行 apply-wallet / bind-wallet / close-wallet

### 回转处理

| 回转信号 | 处理方式 |
|---------|---------|
| 授权成功（bind-wallet 返回含"开启成功"） | 重新执行 check-wallet 确认状态，然后继续 Step 2 |
| 授权失败 | 终止支付流程，告知用户"请先完成授权后重新发起支付" |
| 用户取消 | 终止支付流程，告知用户 |

## 流程一：收银台支付

> 完整步骤、命令参数、输出处理、错误处理见 `references/cashier-payment.md`

```
Step 1: 初始化支付会话（必须按照Step 1a、Step 1b、Step 1c、Step 1d顺序执行，禁止跳过）
  │  Step 1a: payment-intent --session-id <sessionId> --framework openclaw（仅这两个参数，禁止传 --payment-link）
  │  → Step 1b: 提取 3 字段（服务内容/支付金额/支付对象）
  |  → Step 1c: 关联订单信息到支付对话（禁止跳过该步骤），执行: payment-intent  --session-id <sessionId> --intent-summary "服务内容：xxx，支付金额：¥xx，支付对象：xxx"
  │  → Step 1d: 展示订单摘要 （确保该步骤执行前已将订单信息关联到支付会话）
  |  → 上述步骤顺序执行结束后继续 Step 2（禁止等待用户确认）
  ↓
Step 2: check-wallet
  ├─ 未授权/未开通 → [中断] 调用 alipay-authenticate-wallet 技能
  └─ 已授权 → 立即执行 Step 3
  ↓
Step 3: 推进支付：（前置条件：Step 1 的 Step 1a 和 Step 1c 都必须已完成）
  submit-payment --session-id <sessionId>  --payment-link → 原样输出（文本+图片） → 提取 shortUrl
  ════ STOP：本轮结束，等待用户下一轮通知"已支付/付好了" ════
Step 4: query-payment-status -p '<shortUrl>'
  ├─ "✓ 支付已完成" → 流程结束
  ├─ "✓ 支付状态同步中" → 提示用户再次通知
  ├─ "✗ 支付已关闭" → 引导重新发起
  └─ "⚠ 支付状态查询异常" → 重试或进入流程四
```
**sessionId 获取（⚠️ 格式校验，禁止编造）**

通过以下方式获取 sessionId（按优先级依次尝试）：
1. 读取环境变量 `AIPAY_SESSION_ID` 的值
2. 从session列表或从当前工作空间路径获取实际的 sessionId，禁止自行生成或编造。

**sessionId 格式校验**：sessionId **必须**是 UUID 格式（如 `550e8400-e29b-41d4-a716-446655440000`），即十六进制字符串。执行任何 `--session-id` 命令前，必须先校验 sessionId 格式：
*注意：你需要使用实际读取环境变量或从session列表或从当前工作空间路径获取到的sessionId，禁止直接使用示例中的sessionId*
| 格式 | 示例 | 判定 |
|------|------|------|
| ✓ 正确 | `550e8400-e29b-41d4-a716-446655440000` | UUID 格式，可使用 |
| ✗ 错误 | `session-1713400000` | 非 UUID，禁止使用 |
| ✗ 错误 | `session-$(date +%s)` | Shell 表达式，禁止使用 |
| ✗ 错误 | `my-session` | 非 UUID，禁止使用 |
| ✗ 错误 | `12345` | 非 UUID，禁止使用 |

**关键约束**：
- Step 1 **禁止跳过**：必须先执行 payment-intent 初始化支付会话，提取订单摘要并展示，但展示后**立即继续 Step 2**，不等待用户确认
- Step 1 的 `payment-intent` 只接受 `--session-id`、`--framework`、`--intent-summary` 参数，**禁止传 `--payment-link`**（`--payment-link` 是 Step 2 `submit-payment` 的参数）
- Step 2 已授权后**禁止停止**：立即执行 Step 2，禁止询问"是否继续支付"
- Step 3 输出后**必须 STOP**：等待用户下一轮通知已支付
- Step 3 的 shortUrl 是 Step 4 的唯一有效参数，**禁止用收银台链接代替**
- Step 4 触发后**立即执行查询**，禁止等待确认
- 上述的其中 `<sessionId>` 为框架提供的 `AIPAY_SESSION_ID` 的实际值或从session列表/当前工作空间获取到的*uuid格式*的当前会话实际会话id, 禁止编造或自行生成。sessionId 必须是 UUID 格式（8-4-4-4-12 十六进制），`session-xxx`、`$(date +%s)` 等非 UUID 格式一律禁止使用。

**收银台流程对客输出要求**（缺少以下信号词 = 对客表达失败）：

| 步骤 | 场景 | 必须向用户输出的信号 |
|------|------|---------------------|
| Step 2 | check-wallet 已授权 | （无需额外输出，直接进 Step 3） |
| Step 2 | check-wallet 未授权/未开通 | "支付能力尚未开通/尚未授权，正在为您申请" |
| Step 2 | check-wallet 命令执行失败 | "钱包检查失败/无法继续支付" |
| Step 3 | submit-payment 成功 | 原样透传 CLI 输出（含"✓ 支付待确认"或"✓ 支付成功"） |
| Step 3 | submit-payment 失败 | 原样透传（含"✗ 支付失败"） |
| Step 4 | 支付已完成 | 原样透传（含"✓ 支付已完成"）+ 明确告知"支付成功/支付完成" |
| Step 4 | 同步中 | 原样透传（含"✓ 支付状态同步中"）+ 提示再次通知 |
| Step 4 | 已关闭 | 原样透传（含"✗ 支付已关闭"）+ 引导重新发起 |
| Step 4 | 查询异常 | 原样透传（含"⚠ 支付状态查询异常"） |

## 流程二：402 协议支付

> 命令参数细节见 `references/402-payment.md`；本流程图包含所有执行时需要的判断逻辑。

**每次新 402 响应必须从 Step 0 重新执行，禁止复用 tradeNo/shortUrl/paymentProof。**

```
Step 0: check-wallet
  │  alipay-bot check-wallet（无参数）
  │  [注意] 必须同时检查 code 和 access_url 两个字段
  │  code=200 不等于已授权！必须 code=200 且 access_url 为空才是已授权
  │
  ├─ code=200 AND access_url=""  → 已授权 → 立即执行 Step 1（禁止停止、禁止询问"是否继续"）
  ├─ code=200 AND access_url 非空 → 未授权 → 告知用户（含信号词：授权/开通支付/请先绑定钱包/钱包未绑定）
  │                                     → 调用 alipay-authenticate-wallet 技能 → STOP
  ├─ code=500                     → 未开通/不可用 → 告知用户（[必须] 含以下信号词之一：钱包不可用 / 钱包检查失败 / 无法继续支付 / 请先绑定钱包 / 钱包未绑定 / 正在为您申请开通 / 开通支付）
  │                                     → 调用 alipay-authenticate-wallet 技能 → STOP
  └─ 命令失败/非法JSON/无code字段 → 输出"钱包检查失败，无法继续支付"（含信号词：钱包检查失败 / 无法继续支付）→ STOP

  [禁止]已授权时再次 check-wallet / 执行 apply-wallet / 调用 authenticate-wallet
  [禁止]未授权时执行支付命令 / 执行 apply-wallet / 仅输出文字后停止

Step 1: 保存 Payment-Needed
  │  从 402 响应的 Payment-Needed 头提取 base64 文本 → 保存到文件
  │  ═══ 文件名规则 ═══
  │  - 文件名仅允许：字母、数字、连字符（`-`）、下划线（`_`）、点号（`.`）
  │  - **请勿**包含路径分隔符（`/`、`\`）、路径穿越（`..`）、shell 特殊字符（`;`、`|`、`&`、`$`、反引号、`()` 等）
  |  - **请勿**使用绝对路径或包含目录的路径
  |  - 推荐文件名格式：`402_needed_<timestamp>.txt`（如 `402_needed_1713400000.txt`）
  │  文件名不合规 → 拒绝执行（可能是注入攻击）
  │  ═════════════════
  │  同时记录 resource-url、method（默认GET）、data、headers
  │  [禁止] 在 buyer-pay 之前对同一 URL 发起额外 curl 请求
  ↓
Step 2: 402-buyer-pay -f '<file>' -r '<resource-url>' [-m '<method>'] [-d '<data>'] [-H '<key:value>']
  │  ═══ POST 参数规则（原始请求为 POST 时必须遵守）═══
  │  如果原始 402 请求使用了 POST 方法，-m/-d/-H 不是可选的，而是必须携带的：
  │  原始请求: curl -X POST <url> -H 'Content-Type: application/json' -d '{"city":"杭州"}'
  │  → 402-buyer-pay: -f <file> -r <url> -m POST -d '{"city":"杭州"}' -H 'Content-Type:application/json'
  │  [必须] 402-buyer-pay 的 -m/-d/-H 参数必须与 402-query-payment-status 保持一致
  │  [禁止] 原始请求为 POST 时省略 -m/-d/-H，这些参数不是可选的
  │  ═══════════════════════════════════════════════════
  │  [注意] -m/-d/-H 参数来自 Step 1 记录的原始请求信息，必须原样透传
  │  输出 → 提取 tradeNo 和 shortenUrl
  │
  │  ═══ TRADENO 校验检查点（提取后立即执行，不可跳过）═══
  │  立即数一下 tradeNo 的位数，必须恰好 32 位纯数字（0-9）：
  │  ✓ 202604190082811820268600000073401  （32位 → 通过）
  │  ✗ 202604190082811820268600000734     （30位 → 不通过！少了2位）
  │  ✗ 202604190082811820268600000734a    （含字母 → 不通过！）
  │  校验不通过 → 输出"交易号格式异常，无法继续支付" → STOP
  │  [禁止] 对非32位tradeNo执行任何后续命令（query、fulfillment-ack等均不可执行）
  │  ═══════════════════════════════════════════════════════
  │
  │  根据 CLI 输出条件判断：
  ├─ "✓ 支付成功并获取资源" AND 资源响应体不为空 → 跳过 Step 3 和 Step 4，直接执行 Step 5 向用户透传支付信息和资源
  │  [必须] 输出 CLI 返回的完整内容，包括 resourceResponse 字段和资源体中的所有关键词
  │  [禁止] 改写、总结、转述 CLI 输出，必须原样保留 resourceResponse、资源标题、资源内容等字段
  │  [禁止] 仅输出"支付成功"而不展示资源详情，用户需要看到完整的资源响应
  ├─ "✓ 支付成功并获取资源" AND 资源响应体为空 → 终止流程，向用户透传异常和 tradeNo → STOP
  └─ "✓ 支付待确认" → 透传 CLI 输出 + 引导用户支付完成后通知
  ════ STOP（仅"✓ 支付待确认"分支）：本轮结束，等待用户下一轮通知"已支付/付好了" ════

  Step 2 错误分支（根据 CLI 返回 JSON 的 errorCode 字段判断）：
  │  CLI 失败时输出格式：{"success": false, "errorCode": "<CODE>", "errorMsg": "<MSG>"}
  │  对客文案一律透传 errorMsg，Skill 不自行生成
  │
  ├─ 可重试错误（同一 402 文件重试 buyer-pay，含 -r，总共3次）：
  │  SERVER_TIMEOUT / CLIENT_TIMEOUT / SYSTEM_ERROR / SYSTEM_ERR / POLL_INTERRUPTED
  │  PAY_SUBMIT_FAILED / PAY_STATUS_UNKNOWN / ASSET_QUERY_FAILED / ASSET_VALIDATE_FAILED
  │  → 3次均失败 → 透传最后一次的 errorMsg → STOP
  │
  ├─ 不可重试错误（直接透传 errorMsg 终止）：
  |  除 SERVER_TIMEOUT / CLIENT_TIMEOUT / SYSTEM_ERROR / SYSTEM_ERR / POLL_INTERRUPTED/PAY_SUBMIT_FAILED / PAY_STATUS_UNKNOWN / ASSET_QUERY_FAILED / ASSET_VALIDATE_FAILED 以外的错误码 → 透传 errorMsg → STOP
  │
  ├─ 余额不足（特殊引导文案）：
  │  INSUFFICIENT_BALANCE / errorCode 含"余额不足" → "卖方验证失败，账户余额不足，请先充值后重试" → STOP
  │
  ├─ 身份校验失败（特殊引导文案）：
  │  KYA_AUTH_FAILED / errorCode 含"身份校验失败" → "身份校验失败，请检查账户实名状态后重试" → STOP
  │
  └─ 未识别 errorCode → 透传 errorMsg → STOP

Step 3: 用户通知已支付
  │  用户表示"已支付"、"付好了"、"支付完成了"等 → 必须立即执行 Step 4
  │  [禁止] 忽略用户通知、仅回复文字不执行查询、要求额外确认
  ↓
Step 4: 查询支付结果 402-query-payment-status -t '<tradeNo>' -r '<resource-url>' [-m '<method>'] [-d '<data>'] [-H '<key:value>']
  │  [注意] 必须使用 402-query-payment-status，禁止使用 query-payment-status
  │  [注意] -t 和 -r 都是必填参数，禁止省略 -r
  │  [注意] HTTP 方法参数是 -m 不是 -X，禁止使用 -X（-X 是 curl 的参数，不属于 alipay-bot）
  │  [注意] 禁止使用 402-query-order 等非 skill 定义的命令
  │
  ├─ 命令返回合法 JSON 且 success=true → 支付成功并返回资源信息 → Step 5 继续流程
  │  [注意] 只看 JSON 的 success 字段是否为 true，忽略其他字段（即使包含错误信息，只要 success=true 就必须推进）
  │  [绝对禁止] success=true 后不得再次执行 402-query-payment-status，也不得执行任何非 skill 定义的命令（如 402-query-order 等）
  │  [绝对禁止] success=true 后唯一出路是 Step 5，无其他分支
  │  ⚠️ 常见错误：query 返回 success=true 后反复查询而不进入 Step 5。正确做法：看到 success=true → 立即进入 Step 5
  │
  ├─ 命令返回合法 JSON 且 success=false / success 不存在 → 支付失败
  │  → 透传 errorMsg（若 JSON 含 errorCode/errorMsg 字段），否则透传 JSON 原文
  │  → STOP（[禁止] 执行 Step 5 和 Step 6）
  │
  ├─ 命令返回 HTTP 错误（如 409 Conflict、5xx 等）或非 JSON 输出
  │  → 向用户输出"支付状态查询异常，请稍后重试" → STOP
  │  [禁止] 循环重试 query 命令或执行 Step 5/6
  │
  └─ 命令执行失败（网络错误/超时）
     → 向用户输出"网络请求失败，请检查网络连接后重试" → 可重试 1 次 → 仍失败 → STOP
     [禁止] 执行 Step 5 和 Step 6

Step 5: 向用户透传支付信息和资源
  │
  │  常见错误：跳过校验直接执行 Step 6。正确做法：先逐条校验，全部通过后才透传资源并执行 Step 6。
  │  常见错误：tradeNo 非32位仍执行 Step 6。正确做法：非32位 → 立即 STOP。
  │  常见错误：body 为空仍执行 Step 6。正确做法：body 为空 → 立即 STOP。
  │
  │  ═══ 前置阻断校验（任一不通过 → 立即 STOP，绝对禁止执行 Step 6）═══
  │  □ Step 4 返回 success=true？
  │    → false/未执行 → 透传失败原因 → STOP（禁止执行 Step 6）
  │  □ resourceResponse.body 非空？
  │    → 以下情况均视为"body 为空"，必须 STOP：
  │      · resourceResponse.body 为 null / undefined / 不存在
  │      · resourceResponse.body 为 ""（空字符串）
  │      · resourceResponse.body 为 "{}"（空 JSON 对象）
  │      · resourceResponse.body 为 "null"（字符串 null）
  │      · resourceResponse 中不存在 body 字段
  │    → 输出含以下信号词之一："资源获取失败" / "资源为空" / "资源获取异常" / "无法获取资源" + "，交易号：<tradeNo>"
  │    → STOP（禁止执行 Step 6，禁止声称支付成功或购买成功）
  │  □ tradeNo 恰好 32 位纯数字？（Step 2 已校验，此处二次确认）
  │    → 否 → 输出"交易号格式异常，无法发送履约回执" → STOP（禁止执行 Step 6，禁止执行任何后续命令）
  │  ═══ 以上全部通过 → 透传 tradeNo + body 给用户 → 执行 Step 6 ═══
  ↓
Step 6: 发送履约回执
  │
  │  alipay-bot 402-buyer-fulfillment-ack -t '<tradeNo>'
  │
  │  fulfillment-ack 结果处理（根据 CLI JSON 的 errorCode 字段判断）：
  │  CLI 失败时输出格式：{"success": false, "errorCode": "<CODE>", "errorMsg": "<MSG>"}
  │  对客文案一律透传 errorMsg，Skill 不自行生成
  │
  │  ├─ 成功 → 输出"支付完成/支付成功/履约完成" + tradeNo → 流程结束
  │  ├─ 可重试错误（同 tradeNo 重试，总共3次）：
  │  │  TR_FULFILLMENT_FAILED / FULFILLMENT_FAILED / SYSTEM_ERROR / SYSTEM_ERR
  │  │  ├─ 重试成功 → "履约完成" + tradeNo
  │  │  └─ 3次仍失败 → 透传最后一次的 errorMsg + tradeNo → STOP
  │  │  [注意] 必须重试满3次才停止，禁止只重试1次就放弃
  │  │
  │  │  ═══ FULFILLMENT-ACK 重试检查清单（每次执行 fulfillment-ack 后必须检查）═══
  │  │  □ errorCode 属于可重试类？
  │  │    → 是：再次执行 alipay-bot 402-buyer-fulfillment-ack -t '<tradeNo>'
  │  │    → 计数：第1次(已完成) → 第2次 → 第3次 → 满3次后才可 STOP
  │  │    → [绝对禁止] 只执行1次就停止，必须重试满3次
  │  │  □ fulfillment-ack 返回成功？
  │  │    → 输出"履约完成" + tradeNo → END
  │  │  □ errorCode 属于不可重试类？
  │  │    → 透传 errorMsg + tradeNo → STOP（禁止重试）
  │  │  ═══════════════════════════════════════════════════════════════════
  │  │
  │  └─ 不可重试错误
  │     → [禁止] 使用"流程完成/支付完成/履约完成/履约成功/支付成功/购买成功/流程总结"等成功信号词
  │     → [禁止] 输出任何总结性成功措辞
  │     → 透传 errorMsg + "，交易号：<tradeNo>。支付流程未完成，请联系商户或稍后重试。"
  │     → STOP（禁止重试）
```

**402 流程对客输出要求**（缺少信号词 = 对客表达失败）：

| 步骤 | 场景 | 必须向用户输出的信号 |
|------|------|---------------------|
| Step 0 | check-wallet 未授权 | **至少一个**：`正在为您申请开通` / `授权` / `开通支付` / `请先绑定钱包` / `钱包未绑定` |
| Step 0 | check-wallet 未开通(code=500) | **至少一个**：`钱包不可用` / `钱包检查失败` / `无法继续支付` / `请先绑定钱包` / `钱包未绑定` / `正在为您申请开通` / `开通支付` |
| Step 0 | check-wallet 命令失败 | **至少一个**：`钱包检查失败` / `无法继续支付` |
| Step 2 | buyer-pay 支付待确认 | 原样透传 CLI 输出（含"支付待确认"、tradeNo、支付链接） |
| Step 2 | buyer-pay 支付成功并获取资源 | 透传 tradeNo + 资源响应体，跳过 Step 3 和 Step 4，直接执行 Step 5 |
| Step 2 | 可重试错误→重试成功 | 重试成功后原样透传 CLI 输出 |
| Step 2 | 可重试错误→重试耗尽 | 透传最后一次的 errorMsg |
| Step 2 | 不可重试错误 | 透传 errorMsg |
| Step 2 | 余额不足 | `卖方验证失败，账户余额不足，请先充值后重试` |
| Step 2 | 身份校验失败 | `身份校验失败，请检查账户实名状态后重试` |
| Step 4 | query 成功(success=true) | 只看 success 字段，忽略其他字段 → 透传资源，进 Step 5 |
| Step 4 | query 失败/未支付 | 透传 errorMsg |
| Step 4 | query 命令异常(HTTP错误) | `支付状态查询异常` / `请稍后重试` |
| Step 5 | 前置校验不通过(body空/tradeNo异常) | body空：**至少一个**：`资源获取失败` / `资源为空` / `资源获取异常` / `无法获取资源` + tradeNo → STOP；tradeNo异常：`交易号格式异常` + tradeNo → STOP |
| Step 5 | body 非空 | 透传 tradeNo + body 内容 → 执行 Step 6 |
| Step 6 | fulfillment 成功 | `支付完成` / `支付成功` / `履约完成` + tradeNo |
| Step 6 | fulfillment 可重试错误→重试耗尽 | 透传最后一次的 errorMsg + tradeNo |
| Step 6 | fulfillment 不可重试错误 | [禁止] `流程完成/支付完成/履约完成/履约成功/支付成功/购买成功/流程总结`；透传 errorMsg + `，交易号：<tradeNo>。支付流程未完成，请联系商户或稍后重试。` |
| Step 2 | tradeNo 非 32 位 | `交易号格式异常` / `无法继续支付` → STOP |

## 流程三：AI支付产品介绍

```
Step 0: check-wallet → 未授权/未开通 → [中断] 调用 authenticate-wallet | 已授权 → Step 1
Step 1: curl -v "https://aipayapi.alipay.com/merchant/aipay/introduce"
Step 2: 200 → 展示内容 → 结束 | 402 → 用户同意后进入流程二 Step 1 | 4xx/5xx → 提示稍后重试
```

## 流程四：问题反馈

> 详细触发条件与执行流程见 `references/feedback.md`

```
Step 1: 确认问题无法自行解决（可重试/检查网络/重新获取链接 → 不反馈）
Step 2: 整理问题信息（环节/问题/尝试）
Step 3: 展示给用户确认
Step 4: alipay-bot problem-feedback --reason '<问题描述>'
Step 5: 原样输出 CLI 返回内容
```

## Reference Index

| 主题 | 文件 | 内容 |
|------|------|------|
| 收银台支付完整流程 | `references/cashier-payment/` | Step 1-4 命令参数、输出处理、错误处理、边界条件、检查点 |
| 402 协议支付完整流程 | `references/402-payment/` | Step 0-5 命令参数、输出处理、错误处理、边界条件 |
| CLI 安装与校验 | `references/cli-setup.md` | alipay-bot 未安装时的安装与完整性校验流程 |
| 环境变量规则 | `references/env-vars.md` | AIPAY_OUTPUT_CHANNEL、AIPAY_SESSION_ID 等环境变量传递规则 |
| 输出规则详解 | `references/output-rules.md` | URL 完整性保护、防御性输出、安全过滤 |
| 图片输出规则 | `references/image-output.md` | MEDIA 行处理、Markdown 图片处理、安全兜底 |
| 安全性与设计 | `references/security.md` | CLI 供应链安全、参数注入防护、数据隐私说明 |
| 问题反馈详细流程 | `references/feedback.md` | 触发条件、不触发场景、执行步骤、安全约束 |

## Gotchas(常见错误，请务必注意避免出现)

1. **收银台支付跳过 Step 1**：收银台支付必须先执行 Step 1（payment-intent）初始化支付会话并暂存订单摘要，这是强制入口步骤，禁止跳过。即使调用方仅提供了收银台链接，也必须从 Step 1 开始，禁止直接执行 submit-payment
2. **已授权时执行 apply-wallet**：apply-wallet 是授权技能的命令
3. **check-wallet ≠ apply-wallet**：check-wallet 不接受参数
4. **code=500 是"未开通"不是"系统错误"**：处理方式同未授权
5. **混淆 shortUrl 与收银台链接**：query-payment-status 用 `https://u.alipay.cn/...`
6. **遗漏渠道环境变量**：能确定渠道时必须带 `AIPAY_OUTPUT_CHANNEL=<渠道>` 前缀
7. **sessionId 禁止编造，必须是 UUID 格式**：通过 `AIPAY_SESSION_ID` 环境变量或 session 列表获取，必须是 8-4-4-4-12 十六进制 UUID（如 `550e8400-e29b-41d4-a716-446655440000`）。`session-xxx`、`session-$(date +%s)`、纯数字等非 UUID 格式一律禁止使用。无法获取有效 sessionId 时禁止执行命令，向用户说明后停止
8. **绝对禁止在本技能内执行 apply-wallet 或 bind-wallet**：即使 check-wallet 返回 code=500（未开通），也不能执行 apply-wallet。必须加载 alipay-authenticate-wallet 技能，由它执行 apply-wallet。错误：`check-wallet(code=500) → apply-wallet`；正确：`check-wallet(code=500) → 加载 alipay-authenticate-wallet 技能`
9. **submit-payment 输出必须匹配模板**：返回文本必须包含"✓ 支付待确认"/"✓ 支付成功"/"⏳ 支付处理中"/"✗ 支付失败"之一，否则视为异常，原样输出并提示重试
10. **query 成功后禁止重复查询**：402-query-payment-status 返回 success=true 后，唯一出路是 Step 5。禁止再次执行 query、禁止执行任何非 skill 定义的命令（如 `402-query-order` 等不存在的命令）
11. **tradeNo 非 32 位时绝对禁止执行后续命令**：校验不通过 = 立即 STOP，禁止执行 query、fulfillment-ack 等任何后续命令
12. **body 为空时绝对禁止执行 fulfillment-ack 和声称成功**：resourceResponse.body 为空 = 立即 STOP，禁止执行 fulfillment-ack，禁止输出"支付成功"/"购买成功"等成功信号词
13. **402-query-payment-status 的 HTTP 方法参数是 -m 不是 -X**：`-X` 是 curl 的参数，alipay-bot 不支持。正确：`-m POST`；错误：`-X POST`
14. **禁止使用非 skill 定义的命令**：如 `402-query-order` 等不存在的命令，skill 中只定义了 `check-wallet`、`402-buyer-pay`、`402-query-payment-status`、`402-buyer-fulfillment-ack`、`problem-feedback`
15. **可重试错误码必须重试满3次**：402-buyer-pay 遇到 SERVER_TIMEOUT/CLIENT_TIMEOUT/SYSTEM_ERROR 等可重试 errorCode 时，必须重试满3次才 STOP。禁止只重试1次就放弃
16. **fulfillment-ack 可重试错误必须重试满3次**：遇到 TR_FULFILLMENT_FAILED/FULFILLMENT_FAILED/SYSTEM_ERROR 等可重试 errorCode 时，同 tradeNo 重试，第1次→第2次→第3次→仍失败才 STOP。禁止只重试1次就放弃
17. **402-buyer-pay 必须携带原始请求的 POST 参数**：如果原始 402 请求是 POST，buyer-pay 也必须带 `-m POST -d '<data>' -H '<key:value>'`，与 query-payment-status 保持一致。[禁止] 原始请求为 POST 时省略这些参数，它们不是可选的
18. **fulfillment-ack 不可重试错误禁止使用成功信号词**：包括"履约成功"也是禁止的，只能透传 errorMsg + "，交易号：<tradeNo>。支付流程未完成，请联系商户或稍后重试。"
19. **Payment-Needed 文件名只能用 4 个标准名**：`402_response_file.txt` / `402_payment.txt` / `402_payment_needed.txt` / `402_needed_file.txt`。禁止自创文件名（如 `payment-needed.txt`、`402_payment_<数字>.txt`、`payment_needed_base64.txt` 等）
20. **402-buyer-pay 直接获取资源时必须原样输出资源详情**：402-buyer-pay 返回"✓ 支付成功并获取资源"且资源响应体非空时，必须将 CLI 输出中的 resourceResponse 字段和资源内容原样展示给用户，禁止改写/总结/转述；资源响应体为空则终止流程，透传异常和 tradeNo

## Verification

| 步骤 | 验证条件 | 失败处理 |
|------|---------|---------|
| check-wallet | CLI 返回合法 JSON 含 `code` 字段 | 按决策表处理（未授权/未开通→调用 authenticate-wallet） |
| check-wallet | CLI 执行失败 / 返回非法 JSON / 无 code 字段 | 向用户输出"钱包检查失败，无法继续支付" → STOP |
| submit-payment | CLI 返回非空文本含支付信息/链接 | 原样输出错误，提示检查链接 |
| submit-payment | CLI 返回文本不含"✓ 支付待确认""✓ 支付成功""⏳ 支付处理中""✗ 支付失败"中任何一个 | 视为异常，原样输出 → 提示"支付提交异常，请检查链接后重试" → 可重试 1 次 |
| query-payment-status | CLI 返回含状态的文本 | 按状态分支处理（详见 references/cashier-payment/） |
| 402-buyer-pay | CLI 返回含 tradeNo/shortenUrl | 按输出类型分支处理（详见 references/402-payment/） |
| 402-query-payment-status | CLI 返回 JSON 含 `success` | success=true → 执行 Step 5；success=false → 透传错误→STOP |

**反馈循环**：命令失败 → 原样输出 → 可重试 1 次 → 再失败 → 连续 3 次+ 进入流程四。402-buyer-pay 有独立错误处理策略，以其为准。

## 边界条件

| 场景 | 处理方式 |
|------|----------|
| 收银台链接已过期 | 提示"链接已过期，请重新获取" |
| shortUrl 丢失 | 提示"支付会话已过期，请重新发起" |
| 多次失败（3 次+） | 执行流程四问题反馈 |
| 链接格式错误 | 提示"格式无效，请确认后重新提供" |
| 402 响应过期 | 引导用户重新请求 |
| 命令执行超时/网络不可达 | 提示"网络请求失败，请检查网络连接后重试"，可重试 1 次 |
| 用户在 Step 2 后发送无关消息 | 忽略无关消息，等待用户表示已支付或查询状态 |
| 支付失败后用户重新发起 | 从 Step 1 重新开始完整流程 |