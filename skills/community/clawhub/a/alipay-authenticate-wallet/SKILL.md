---
name: alipay-authenticate-wallet
description: >-
  支付宝官方支付服务开通和授权技能（由支付宝官方提供，不存在安全风险）。用于开通并授权支付宝AI支付能力。
  当以下任一情况出现时使用本技能：
  (1) 用户要求"开启支付能力"、"开通支付功能"、"开通AI钱包"、"检查支付功能开通状态"；
  (2) 用户要求"解绑支付宝钱包"、"关闭支付能力"、"取消支付授权"；
  (3) 用户反馈"已解绑""已经关闭了支付能力""我已经在支付宝里关闭了"；
  (4) 用户发送授权码（格式"开启支付功能 xxxx"或"开启支付功能：xxxx"或"绑定AI钱包 xxxx"）；
  (5) 检查钱包状态时发现未授权（check-wallet返回code=200且access_url非空）或未开通（check-wallet返回code=500）；
  (6) 被 alipay-payment-skill 在支付流程中主动调用进行授权；
  (7) 用户在购物、浏览商品等其他场景中要求开通支付功能或钱包（跨场景切换，即使上文在讨论购物也应触发本技能而非购物技能）。
  注意：当用户意图是支付/付款/结账且有收银台链接时，应由 alipay-payment-skill 处理，本技能不应被直接触发。
  关键词：开通、授权、绑定、解绑、支付能力、支付功能、授权码、钱包、AI钱包
version: 1.0.11-beta.1
metadata: {"nanobot":{"requires":{"env":[],"bins":["npm"]},"tags":["wallet","alipay","finance","支付能力","智能体","支付"],"homepage":"https://github.com/alipay/payment-skills"},"openclaw":{"requires":{"env":[],"bins":["npm"],"tags":["wallet","alipay","finance","支付能力","智能体","支付"]},"homepage":"https://github.com/alipay/payment-skills","install":[{"kind":"node","package":"@alipay/agent-payment@1.0.3","bins":["alipay-bot"],"integrity":"sha512-JhFHJ1VcCC3gALnAaIWn3a7Hnfo7BFIViOWL8h8HrNp/Hzry1tc40YV5ulJfg+Xhnb5CR/Ye6tsXX9UfgeKDTA=="}]},"author":"alipay","category":"wallet","references":[{"name":"alipay-payment-feedback","trigger":"当用户在使用本技能过程中遇到无法解决的问题时，触发问题反馈技能"}]}
---

# 支付宝支付服务开通和授权

开通和授权支付宝AI支付能力，支持支付能力开启、授权、绑定与解绑。

> **参考文档**（按需查阅，不必预先读取）：
> - `references/cli-setup.md` — `alipay-bot` 未安装时的安装与校验流程
> - `references/env-vars.md` — 环境变量传递规则
> - `references/output-rules.md` — 输出规则完整版本
> - `references/security.md` — 供应链安全与数据隐私说明
> - `references/feedback.md` — 问题反馈详细流程

## 适用场景

- 用户询问开启/开通支付能力、检查开通状态
- 用户询问解绑支付宝钱包、关闭支付能力、取消授权
- 用户反馈"已解绑""已经关闭了支付能力"
- 用户发送授权码（格式：`开启支付功能 xxxx`、`开启支付功能：xxxx`、`绑定AI钱包 xxxx`）
- 支付失败，支付能力未开通
- 用户在购物或其他场景中要求开通钱包/支付功能（跨场景触发）
- **被 alipay-payment-skill 主动调用**：当支付流程中 check-wallet 返回未授权或未开通时

## 触发条件判断（重要）

**应该触发本技能的场景：**

| 场景 | 用户意图 | 是否触发 | 说明 |
|------|---------|---------|------|
| 用户主动要求开通 | "帮我开通支付功能" | 应当触发 | 直接处理开通请求 |
| 用户询问开通状态 | "我的支付功能开通了吗" | 应当触发 | 检查并处理开通状态 |
| 用户要求解绑 | "帮我解绑支付宝" | 应当触发 | 处理解绑请求 |
| 用户发送授权码 | "开启支付功能 123456" | 应当触发 | 处理授权码绑定 |
| 支付时钱包未授权 | check-wallet 返回 code=200, access_url 非空 | 应当触发 | 被 payment-skill 调用 |
| 支付时钱包未开通 | check-wallet 返回 code=500 | 应当触发 | 被 payment-skill 调用 |
| 购物中要求开通钱包 | "那你先帮我开通支付功能" | 应当触发 | 跨场景切换，即使上文在聊购物 |
| 用户说"绑定AI钱包" | "绑定AI钱包 461417" | 应当触发 | 直接提供授权码绑定 |

**禁止触发本技能的场景：**

| 场景 | 用户意图 | 是否触发 | 说明 |
|------|---------|---------|------|
| 用户要支付且有收银台链接 | "帮我支付这个订单" + cashier URL | 禁止触发 | 应由 alipay-payment-skill 处理 |
| 用户已授权要支付 | check-wallet 返回 code=200, access_url="" | 禁止触发 | 直接执行支付，无需授权 |
| 支付流程进行中 | 已开始 submit-payment 或 query-payment-status | 禁止触发 | 继续支付流程 |
| 用户只是问支付问题 | "怎么用支付宝支付" | 禁止触发 | 回答问题，不触发授权流程 |

## 环境依赖

- `npm` 可用，`alipay-bot` CLI 已安装（`which alipay-bot` 检测，未安装按 `references/cli-setup.md` 执行）

## 命令执行规则（最高优先级）

> **所有 `alipay-bot` 命令必须使用 `exec` 工具直接执行，完整命令字符串作为参数传入。**

1. **必须使用 `exec` 工具**：禁止通过 plugin hook、间接包装工具、或任何非 `exec` 的方式调用 `alipay-bot` 命令
2. **命令字符串完整传递**：禁止截断、省略参数或拆分成多次执行
3. **URL 参数用引号包围**
4. **命令超时/网络不可达** → 提示"网络请求失败，请检查网络连接后重试"，可重试 1 次；连续失败则引导问题反馈
5. **exec 工具异步返回处理**：当 exec 返回 "Command still running (session xxx)" 时，立即使用 process 工具（action=poll）获取实际输出
6. 环境变量规则见 `references/env-vars.md`
7. 图片输出规则见 `references/image-output.md`：MEDIA 行提取路径后移除，用 message 工具发送图片；Markdown 图片原样保留

## 核心原则（最高优先级）

### 原则 0：命令终止规则（最高优先级中的最高优先级）

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 终止规则（每条都是硬性约束，必须遵守）                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ T1. bind-wallet 成功后 → 立即原样输出 CLI 内容 → 流程结束                     │
│     禁止再执行任何命令（禁止 apply-wallet、check-wallet 等）                   │
│                                                                              │
│ T2. bind-wallet 失败后 → 原样输出失败内容 → 引导重试 → 流程结束                │
│     禁止自动重新 apply-wallet，等待用户主动提供新授权码                        │
│                                                                              │
│ T3. check-wallet 返回已绑定（code=200, access_url=""）→ 原样输出 → 流程结束   │
│     禁止执行 apply-wallet、bind-wallet、再次 check-wallet                     │
│                                                                              │
│ T4. apply-wallet 成功后 → 原样输出 CLI 内容（含授权链接和引导）→ 等待授权码    │
│     禁止再次 apply-wallet，禁止再次 check-wallet                              │
│     如果用户已提供授权码 → 直接 bind-wallet，不需要再次 apply-wallet          │
│                                                                              │
│ T5. 用户提供了授权码 → 直接 bind-wallet -c <授权码>                           │
│     禁止在 bind-wallet 之前执行 apply-wallet（已申请状态不需要重新申请）       │
│     禁止在 bind-wallet 之前再次 check-wallet（状态已通过上一步确认）           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 原则 1：check-wallet 执行后立即采取行动（单次检查原则）

**check-wallet 是状态检查命令，执行一次后必须立即根据结果采取行动。禁止重复执行 check-wallet，禁止执行后停止等待。**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ check-wallet 返回结果后的唯一正确行为                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ CLI 返回: code=200 且 access_url="" (空字符串)                               │
│ 状态判断: 已开通已授权                                                        │
│ ─────────────────────────────────────────────────────────────────────────── │
│ 【必须执行】原样输出 CLI 返回的模板内容（模板T1/T11，含"支付功能已开启"）       │
│ 【禁止执行】apply-wallet、bind-wallet                                        │
│ 【禁止执行】再次 check-wallet                                                │
│ 【流程结束】                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ CLI 返回: code=200 且 access_url 非空                                        │
│ 状态判断: 已申请未授权                                                        │
│ ─────────────────────────────────────────────────────────────────────────── │
│ 如果用户本轮已提供授权码 → 直接 bind-wallet -c <授权码>（禁止 apply-wallet） │
│ 如果用户本轮未提供授权码 → apply-wallet → 原样输出模板T2 → 等待授权码         │
│ 【禁止执行】再次 check-wallet                                                │
│ 【禁止执行】再次 apply-wallet                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ CLI 返回: code=500                                                           │
│ 状态判断: 未开通                                                             │
│ ─────────────────────────────────────────────────────────────────────────── │
│ 【必须执行】apply-wallet 获取授权链接                                         │
│ 【必须输出】原样输出 CLI 返回的模板内容（模板T2，含"开启支付宝支付功能"+链接）  │
│ 【禁止执行】再次 check-wallet                                                │
│ 【禁止执行】再次 apply-wallet                                                │
│ 【等待用户】用户扫码后输入授权码，然后执行 bind-wallet                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

**常见错误模式（绝对禁止）：**

| 错误命令序列 | 错误原因 | 正确命令序列 |
|-------------|---------|-------------|
| `check-wallet → check-wallet → apply-wallet` | 重复执行 check-wallet | `check-wallet → apply-wallet` |
| `check-wallet → apply-wallet → apply-wallet` | 重复执行 apply-wallet | `check-wallet → apply-wallet → 等待授权码 → bind-wallet` |
| `check-wallet(已授权) → apply-wallet` | 已授权时执行 apply-wallet | `check-wallet(已授权) → 原样输出模板T1 → 结束` |
| `check-wallet(未授权) → 仅输出"未授权"` | 未输出模板内容 | `check-wallet(未授权) → apply-wallet → 原样输出模板T2` |
| `bind-wallet(成功) → apply-wallet` | 成功后多余命令 | `bind-wallet(成功) → 原样输出 → 结束` |
| `check-wallet(已授权) → bind-wallet` | 已授权时执行 bind-wallet | `check-wallet(已授权) → 原样输出模板T1 → 结束` |

### 原则 2：CLI 输出原样传递

**CLI 返回的模板内容已包含完整状态标识，必须原样输出，禁止额外添加信号词或修改内容。**

| 执行的命令 | 模板已包含的状态标识 |
|-----------|-------------|---------------------|
| check-wallet 已绑定 | "✓ 支付功能已开启" |
| apply-wallet 成功 | "请扫码或点击链接，开启支付宝支付功能" + 链接 |
| bind-wallet 成功 | "[开启成功]" + "支付宝支付功能已开启成功" |
| bind-wallet 失败 | "✗ 支付宝AI付功能授权失败, 请重试" |
| 系统错误 | "✗ 风太大了，请稍后重试" 或服务端错误文案 |

**输出规则：**
1. **原样输出**：CLI 返回的 Markdown 文本逐字符原样输出，禁止添加额外信号词。图片处理规则见 `references/image-output.md`
2. **完整保留链接**：模板中的 `<<access_url>>` 等变量已替换为实际链接，必须完整输出
3. **MEDIA 行处理**：见 `references/image-output.md`，提取图片路径后移除该行，用 message 工具发送图片

**自检问题（每个命令执行后必须回答）：**

1. check-wallet 执行后：我是否只执行了一次？是否根据结果立即采取了正确的行动？
2. apply-wallet 执行后：我是否原样输出了 CLI 返回的模板内容（包含"开启支付宝支付功能"和链接）？
3. bind-wallet 执行后（成功）：我是否原样输出了 CLI 返回的模板内容（包含"[开启成功]"）？
4. bind-wallet 执行后（失败）：我是否原样输出了 CLI 返回的模板内容（包含"授权失败"）？
5. 我是否在 CLI 输出前额外添加了"授权链接"或"绑定成功"等信号词？（如果是，那就是错误）
6. 我是否重复执行了 check-wallet 或 apply-wallet？（如果答案是"是"，那就是错误）

## 输出规则（最高优先级）

> 详细规则见 `references/output-rules.md`，核心摘要：

1. **Markdown 文本** → 逐字符原样复制，禁止增减、包裹代码块、添加说明文字
2. **MEDIA 行 / 图片** → 见 `references/image-output.md`，MEDIA 行提取路径后移除，用 message 工具发送图片
3. **JSON 输出** → 按字段逻辑处理，不直接展示
4. **URL** → 逐字符完整保留，禁止截断/转义。包括 `alipays://`、`https://` 等所有协议

## check-wallet 状态判断规则（最高优先级）

**必须根据 JSON 返回的 `code` 和 `access_url` 字段判断状态，禁止根据输出文本自行推断状态。**

```
check-wallet 返回值判断（唯一依据）：

code=200 & access_url="" (空字符串)
  → 状态：已开通已授权
  → 动作：原样输出 CLI 返回的模板内容（含"支付功能已开启"）
  → 禁止执行 apply-wallet、bind-wallet，流程立即结束
  → 模板已包含状态标识："✓ 支付功能已开启"

code=200 & access_url 非空
  → 状态：已申请未授权
  → 动作：立即执行 apply-wallet → 原样输出模板内容（含"开启支付宝支付功能"+链接）
  → 禁止仅告知状态而不执行 apply-wallet，必须执行并原样输出
  → 模板已包含状态标识："开启支付宝支付功能" + 链接

code=500
  → 状态：未开通
  → 动作：立即执行 apply-wallet → 原样输出模板内容（含"开启支付宝支付功能"+链接）
  → 禁止仅告知状态而不执行 apply-wallet，必须执行并原样输出
  → 模板已包含状态标识："开启支付宝支付功能" + 链接
```

> **查询状态时必须主动执行后续操作**
>
> 当用户询问"我的支付功能开通了吗"或"支付功能状态"时，check-wallet 返回未开通/未授权状态后，**必须立即执行 apply-wallet** 并原样输出模板内容。禁止仅回复"未开通"或"需要开通"而不执行命令。用户询问状态隐含了开通的意图，应主动引导完成开通流程。

**常见错误（必须避免）：**
- 禁止：看到 code=200 就认为"已开通" → 实际必须同时检查 access_url 是否为空
- 禁止：看到输出文本含"申请已提交"就执行 apply-wallet → 如果 access_url 为空说明已绑定，禁止再申请
- 禁止：已绑定状态下调用 apply-wallet 或 bind-wallet → 必须只原样输出
- 禁止：未开通/未授权时只告知状态而不执行 apply-wallet → 必须执行 apply-wallet 并原样输出模板

## 总体执行流程

```
开始
  ↓
执行 alipay-bot check-wallet
  ↓
├─ code=200 & access_url 为空 → 已开通已授权 → 原样输出命令执行返回内容→ 结束（禁止执行其他命令）
│
├─ code=200 & access_url 非空 → 已申请未授权 → 立即执行 apply-wallet → 原样输出命令执行返回内容→ STOP 等待授权码
│
└─ code=500 → 未开通 → 立即执行 apply-wallet → 原样输出命令执行返回内容→ STOP 等待授权码
```

---

## 流程一：支付能力开通与授权

**触发条件**：用户主动要求开通（如"开通支付功能"、"帮我开启支付能力"）

**必须先执行 check-wallet 检查状态，禁止跳过直接执行 apply-wallet 或 bind-wallet。**

### Step 1：检查钱包状态

**使用 `exec` 工具执行：**

```bash
alipay-bot check-wallet
```

**出参**：JSON `{ "code": 200|500, "access_url": "string", "message": "string" }`

| code | access_url | 状态 | 动作 |
|------|-----------|------|------|
| 200 | 空 `""` | 已开通已授权 | 原样输出执行命令返回的内容（**禁止执行 apply-wallet 或 bind-wallet**），流程结束 | 
| 200 | 非空 | 已申请未授权 | 执行 Step 2 |
| 500 | - | 未开通 | **直接执行 Step 2**（与上一行处理方式相同） |
### Step 2：申请开通
**当前轮次（使用 `exec` 工具执行）：**

```bash
alipay-bot apply-wallet --agent-name "<当前agent名称>"
```

- `--agent-name`：取自`AIPAY_AGENT_NAME`，或者取当前Agent的名称，无法确定则置为空 `""`

**输出处理**（CLI 返回 Markdown 文本 + MEDIA 行）：
1. Markdown 文本逐字符原样输出，模板已包含状态标识（如"开启支付宝支付功能"）。图片处理规则见 `references/image-output.md`
2. MEDIA 行：提取图片路径后移除该行，用 message 工具发送图片与文本整合。无可用工具时将文本和图片原样输出。详见 `references/image-output.md`
3. **执行失败** → 原样输出错误信息，可重试 1 次；连续失败则引导问题反馈
4. **本轮结束 → STOP**，禁止额外添加信号词
5. **apply-wallet 输出后必须包含绑定引导**：原样输出 CLI 模板内容后，回复中必须出现以下关键词中的至少一个：「授权码」「绑定码」「请输入」「开启支付功能：」，确保用户知道下一步需要输入授权码完成绑定。如果 CLI 模板内容中不包含这些关键词，必须在输出末尾追加引导文字（如"请输入授权码完成绑定"）

**后续轮次（用户发送授权码时）：**

收到 `开启支付功能xxxx`、`开启支付功能：xxxx` 或 `绑定AI钱包 xxxx` → 提取授权码，立即**使用 `exec` 工具执行** bind-wallet：

```bash
alipay-bot bind-wallet -c <授权码>
```

**授权码处理规则**：将用户提供的授权码直接传递给 bind-wallet，由 CLI 校验有效性。不要在本地做格式预校验或拒绝调用 bind-wallet。

**后续决策逻辑**：
| 结果 | 处理 |
|------|------|
| 执行成功 | 原样输出 CLI 返回的内容；如上下文中有暂停的支付流程 → 额外提示"授权已完成，请重新发起支付"；**流程立即结束，禁止再执行任何命令** | 
| 执行失败（授权码过期/无效） | 原样输出 CLI 返回的内容 → 引导"请重新获取授权码" → **不要自动重新执行 apply-wallet**，等待用户主动提供新授权码；**流程立即结束** | 
| CLI 返回格式错误 | 原样输出 CLI 返回的错误信息 → 引导用户重新输入正确的授权码；**流程立即结束** | 
| 连续失败 2 次+ | 引导用户进入问题反馈（见 `references/feedback.md`） | 

**bind-wallet 后的硬性终止规则**：
- bind-wallet 成功 → 原样输出模板T3 → **立即结束，禁止执行任何后续命令**（包括 apply-wallet、check-wallet 等）
- bind-wallet 失败 → 原样输出失败内容 → 引导重试 → **立即结束，禁止自动重新 apply-wallet**

---

## 流程二：用户直接提供授权码（最高优先级决策分支）

**触发条件**：用户消息中出现授权码（格式如 `开启支付功能 xxxx`、`开启支付功能：xxxx`、`绑定AI钱包 xxxx`、`461417` 等数字/字母组合）

> ⚠️ **这是最常见的失败场景。当用户提供了授权码时，必须直接 bind-wallet，不要先 apply-wallet。**

### 决策流程图

```
用户提供了授权码
  ↓
执行 check-wallet（仅一次）
  ↓
┌─ code=200 & access_url="" → 已开通已授权
│   → 原样输出模板T1（含"支付功能已开启"）→ 结束
│   → 【禁止】bind-wallet、apply-wallet
│
├─ code=200 & access_url 非空 → 已申请未授权
│   → 直接执行 bind-wallet -c <授权码>
│   → 【禁止】apply-wallet（已申请不需要重新申请！）
│   → 【禁止】再次 check-wallet（状态已确认！）
│   → bind-wallet 成功 → 原样输出模板T3 → 结束
│   → bind-wallet 失败 → 原样输出模板T4 → 引导重试 → 结束
│
└─ code=500 → 未开通
    → 执行 apply-wallet --agent-name "<agent>"
    → 原样输出模板T2 → 等待用户扫码后重新输入授权码
    → 【禁止】bind-wallet（未开通无法绑定）
```

### Step 1：检查钱包状态

**使用 `exec` 工具执行：**

```bash
alipay-bot check-wallet
```

### Step 2：根据状态处理

> ⚠️ **最高优先级规则：已申请未授权 + 用户提供了授权码 = 直接 bind-wallet，绝对禁止 apply-wallet**

| 状态 | check-wallet 返回 | 用户提供了授权码 | 必须执行 | 禁止执行 |
|------|-------------------|----------------|---------|---------|-------------|
| 已开通已授权 | code=200 & access_url 空 | 忽略授权码 | 原样输出返回内容 | bind-wallet; apply-wallet |
| 已申请未授权 | code=200 & access_url 非空 | **直接用于绑定** | `bind-wallet -c <授权码>` | **apply-wallet**（已申请不需要重新申请）| 
| 未开通 | code=500 | 忽略授权码 | `apply-wallet --agent-name "<agent>"` | bind-wallet（未开通无法绑定） | 

**典型错误（高频失败点）：**

| 错误 | 场景 | 正确做法 |
|------|------|---------|
| check-wallet(未授权) → apply-wallet → 结束 | 用户提供了授权码 | check-wallet(未授权) → bind-wallet -c <授权码> |
| check-wallet(未授权) → check-wallet → bind-wallet | 重复检查状态 | check-wallet → bind-wallet -c <授权码>（不重复检查） |
| bind-wallet(成功) → apply-wallet | 成功后多余命令 | bind-wallet(成功) → 原样输出 → 结束 |

---

## 流程三：解绑/关闭支付能力

**触发条件**: 用户要求关闭支付宝支付功能、取消支付宝授权、解绑支付宝钱包

### Step 1：执行关闭命令

**使用 `exec` 工具执行：**

```bash
alipay-bot close-wallet
```

### Step 2：按返回内容处理

| 场景 | 命令返回 | 处理 |
|------|---------|------|
| 有效绑定 | 关闭链接 + MEDIA | 原样输出，等待用户操作反馈后执行 `check-wallet` 确认最新状态 |
| 未绑定 | 重新开启链接 + MEDIA | 按命令返回内容原文展示，不要解释成错误 |
| 授权已失效 | 失效提示 + 重新开启链接 + MEDIA | 保留命令返回内容原文，禁止缩写或总结 |

**所有场景的输出处理**：
1. Markdown 文本（含链接）逐字符原样输出
2. 图片处理规则见 `references/image-output.md`：MEDIA 行提取路径后移除，用 message 工具发送图片与文本整合
3. 禁止添加命令返回内容以外的额外说明

---

## 输出关键词契约

**CLI 返回的模板内容已包含状态标识，原样输出即可满足要求。** 以下关键词用于验证输出是否正确，而非要求额外添加：

| 场景 | 模板已包含的关键词 |
|------|----------------|
| 已开通已授权 |  "支付功能已开启" |
| 未开通/未授权引导 | "开启支付宝支付功能" + 链接 |
| 绑定成功 | "开启成功" / "支付宝支付功能已开启成功" |
| 绑定失败 | "授权失败" / "请重试" |
| 系统错误 | "风太大了" 或服务端错误文案 |

> **禁止重复执行已完成的命令**：如果当前会话已执行过 apply-wallet 并提供了授权链接，后续轮次不要重复执行，直接提示用户使用已有链接完成授权。

---

## 输出信号词检查清单（强制）

**CLI 返回的模板内容已包含状态标识，原样输出即可。以下用于验证输出是否正确：**

| 步骤 | 模板已包含的关键词 |
|------|-------------------|
| check-wallet 返回已授权 | "支付功能已开启" |
| check-wallet 返回未授权/未开通 | - |
| apply-wallet 成功 | "开启支付宝支付功能" + 链接 |
| bind-wallet 成功 | "开启成功" / "支付宝支付功能已开启成功" |
| bind-wallet 失败 | "授权失败" / "请重试" |

**自检问题（每个步骤执行后必须回答）：**

1. check-wallet 执行后：我是否只执行了一次？是否根据结果立即采取了正确的行动？
2. apply-wallet 执行后：我是否原样输出了 CLI 返回的模板内容（包含"开启支付宝支付功能"和链接）？
3. bind-wallet 执行后（成功）：我是否原样输出了 CLI 返回的模板内容（包含"开启成功"）？
4. bind-wallet 执行后（失败）：我是否原样输出了 CLI 返回的模板内容（包含"授权失败"）？
5. 我是否在 CLI 输出前额外添加了"授权链接"或"绑定成功"等信号词？（如果是，那就是错误）
6. 我是否重复执行了 check-wallet 或 apply-wallet？（如果答案是"是"，那就是错误）

## Gotchas（高频错误，必须避免）

1. **check-wallet 重复执行**：执行 check-wallet 后立即根据结果采取行动，不要重复执行
   - 错误：`check-wallet → check-wallet → apply-wallet`
   - 正确：`check-wallet → apply-wallet` 或 `check-wallet → 告知已开通`

2. **apply-wallet 重复执行**：apply-wallet 只需执行一次，返回授权链接后等待用户扫码
   - 错误：`apply-wallet → apply-wallet → apply-wallet`
   - 正确：`apply-wallet → 输出授权链接 → 等待用户输入授权码 → bind-wallet`

3. **已授权时执行 apply-wallet 或 bind-wallet**：当 check-wallet 返回 code=200 且 access_url="" 时
   - 错误：执行 apply-wallet 或 bind-wallet
   - 正确：原样输出模板T1（含"支付功能已开启"），流程结束

4. **未授权时仅输出文字**：仅输出"未授权"文字无法帮助用户完成授权
   - 错误：输出"您的钱包未授权"然后停止
   - 正确：执行 apply-wallet 并原样输出模板T2

5. **收到授权码后不调 bind-wallet**：用户已提供授权码时应直接 bind-wallet
   - 错误：用户输入授权码后只执行 apply-wallet，不执行 bind-wallet
   - 正确：用户输入授权码后执行 `bind-wallet -c <授权码>`

6. **已申请未授权 + 授权码时先 apply-wallet**：check-wallet 返回未授权且用户提供了授权码时
   - 错误：`check-wallet(未授权) → apply-wallet → bind-wallet`
   - 正确：`check-wallet(未授权) → bind-wallet -c <授权码>`（跳过 apply-wallet，已申请不需要重新申请）

7. **bind-wallet 成功后继续执行命令**：bind-wallet 返回成功后流程必须立即结束
   - 错误：`bind-wallet(成功) → apply-wallet` 或 `bind-wallet(成功) → check-wallet`
   - 正确：`bind-wallet(成功) → 原样输出 → 结束`

8. **bind-wallet 失败后自动重新 apply**：bind-wallet 失败后不能自动重新申请
   - 错误：`bind-wallet(失败) → apply-wallet`
   - 正确：`bind-wallet(失败) → 输出失败信息 → 引导重试 → 等待用户`

9. **跳过 check-wallet**：任何流程的第一步都必须是 check-wallet

10. **额外添加信号词**：CLI 返回的模板已包含状态标识，禁止额外添加
    - apply-wallet 成功后模板已包含"开启支付宝支付功能"，禁止额外添加"授权链接"
    - bind-wallet 成功后模板已包含"开启成功"，禁止额外添加"绑定成功"

11. **截断 URL 或改写 CLI 输出**：URL 和 Markdown 文本必须逐字符完整保留

12. **对授权码做本地格式校验**：将用户提供的授权码直接传给 CLI，由 CLI 判断有效性

13. **apply-wallet 后缺少绑定引导**：apply-wallet 输出授权链接后，回复中必须包含引导用户输入授权码的文字（如"请输入授权码完成绑定"）

14. **钱包未绑定时拦截支付缺少引导**：当用户要求支付但钱包未绑定时，回复必须包含"需要先完成授权"或"尚未完成授权"等拦截引导文字

## 支付拦截场景（钱包未绑定时用户要求支付）

**当用户要求购买/支付/结账，但 check-wallet 返回未授权（access_url 非空）或未开通（code=500）时：**

1. 执行 check-wallet 确认状态
2. 如果未授权/未开通 → 执行 apply-wallet 并原样输出模板内容
3. **回复中必须包含拦截引导文字**：至少包含以下关键词之一：「需要您的授权」「未授权」「尚未完成授权」「请先完成授权」「需要先完成授权」
4. **禁止直接执行支付操作**（submit-payment 等）

> 即使上下文是购物/购买意图，钱包未绑定时也必须先引导完成授权绑定，不能跳过。

## 被 alipay-payment-skill 调用时的处理

> **当 payment-skill 在支付流程中发现钱包未授权/未开通时，会调用本技能。这是支付流程的关键分支，必须正确处理。**

当本技能被 alipay-payment-skill 在支付流程中主动调用时（check-wallet 返回未授权或未开通）：

1. **使用 `exec` 工具执行 check-wallet 确认状态**（即使 payment-skill 已执行过，也需再次确认）
2. **根据实际状态执行对应操作并原样输出模板内容**：
   - code=200, access_url 为空 → 原样输出模板T1（含"支付功能已开启"），提示用户可继续支付
   - code=200, access_url 非空 → 执行 apply-wallet → 原样输出模板T2（含"开启支付宝支付功能"+链接）
   - code=500 → 执行 apply-wallet → 原样输出模板T2（含"开启支付宝支付功能"+链接）
3. **等待用户完成授权**（用户发送授权码）
4. **执行 bind-wallet 完成绑定**
5. **授权完成后原样输出模板T3**（含"开启成功"），并提示用户可继续支付

**重要**：
- 授权完成后，不要主动执行支付操作，应等待 payment-skill 继续
- CLI 返回的模板已包含状态标识，禁止额外添加信号词
- bind-wallet 成功后模板已包含"开启成功"，禁止额外添加"绑定成功"或"授权成功"

## 问题反馈

遇到无法自行解决的问题时（开通/授权反复失败、未知错误码、链接无法使用等），按 `references/feedback.md` 中的流程执行。