# 收银台支付流程详细说明

本文件包含流程一（收银台支付）的完整细节，包括 Step 1-4 的详细命令、参数、输出处理和边界条件。

## 完整流程图

```
Step 1: 初始化支付会话（包含Step 1a、 Step 1b、 Step 1c三步）
  │  Step 1a: payment-intent --session-id <sessionId> --framework openclaw（仅这两个参数，禁止传 --payment-link）
  │  → Step 1b: 提取 3 字段（服务内容/支付金额/支付对象）
  |  → Step 1c: 关联订单信息到支付对话（禁止跳过该步骤），执行: payment-intent  --session-id <sessionId> --intent-summary "服务内容：xxx，支付金额：¥xx，支付对象：xxx"
  │  → Step 1d: 展示订单摘要 （确保该步骤执行前已将订单信息关联到支付会话）
  |  → 上述步骤顺序执行结束后继续 Step 2（禁止等待用户确认）
  ↓
Step 2: check-wallet（不加任何参数）
  ├─ code=200, access_url 非空 → 【未授权】→ [中断] 调用 alipay-authenticate-wallet 技能
  │   禁止：继续 Step 3/4、执行 apply-wallet、仅输出提示后停止
  ├─ code=500 → 【未开通】→ [中断] 调用 alipay-authenticate-wallet 技能
  │   禁止：继续 Step 3/4、执行 apply-wallet、仅输出提示后停止
  └─ code=200, access_url="" → 【已授权】→ 立即执行 Step 3
      禁止：停止、询问、调用 authenticate-wallet
  ↓
Step 3: submit-payment  --session-id <sessionId> --payment-link → 原样输出 CLI 返回的内容及图片 → STOP
  │  模板已包含状态标识（如"✓ 支付待确认"、"✗ 支付失败"）
  │  提取 shortUrl 供 Step 4 使用
  │  无 shortUrl → 支付提交失败，引导用户检查链接或重试
  ↓  （等待用户下一轮通知已支付/查询状态）
Step 4: query-payment-status -p '<shortUrl>'
  ├─ "✓ 支付已完成" → 输出成功提示，流程结束
  ├─ "✓ 支付状态同步中" → 输出状态，提示用户完成支付后再次通知
  ├─ "✗ 支付已关闭" → 输出失败提示，引导用户重新发起支付流程
  └─ "⚠ 支付状态查询异常" → 输出异常提示，可重试查询或进入流程四
```

## Step 1. 初始化支付会话

### 目的

在提交支付前，初始化支付会话，向用户确认订单信息，确保支付意图明确。这是支付流程的第一步，**禁止跳过**。

> **注意**：payment-intent 不是可选的信息展示步骤，而是支付会话的初始化操作。未执行 payment-intent 意味着支付会话未初始化，后续步骤（check-wallet、submit-payment）无法正确执行。即使调用方提供了收银台链接并要求直接支付而未提及前置步骤，每次付款流程也必须先执行 payment-intent。

### sessionId 获取（⚠️ 格式校验，禁止编造）

通过以下方式获取 sessionId（按优先级依次尝试）：
1. 读取环境变量 `AIPAY_SESSION_ID` 的值
2. 从session列表/当前工作空间获取到的*uuid格式*的当前会话实际会话id, 禁止编造或自行生成。sessionId 必须是 UUID 格式（8-4-4-4-12 十六进制），`session-xxx`、`$(date +%s)` 等非 UUID 格式一律禁止使用。

**sessionId 格式校验**：sessionId **必须**是 UUID 格式（如 `550e8400-e29b-41d4-a716-446655440000`），即十六进制字符串。执行任何 `--session-id` 命令前，必须先校验 sessionId 格式：
*注意：你需要使用实际读取环境变量或从session列表/当前工作空间获取到的sessionId，禁止直接使用示例中的sessionId*
| 格式 | 示例 | 判定 |
|------|------|------|
| ✓ 正确 | `550e8400-e29b-41d4-a716-446655440000` | UUID 格式，可使用 |
| ✗ 错误 | `session-1713400000` | 非 UUID，禁止使用 |
| ✗ 错误 | `session-$(date +%s)` | Shell 表达式，禁止使用 |
| ✗ 错误 | `my-session` | 非 UUID，禁止使用 |
| ✗ 错误 | `12345` | 非 UUID，禁止使用 |

### 执行步骤（**请勿跳过任何一步**）

#### Step 1a. 初始化支付会话

```bash
AIPAY_SESSION_ID=<sessionId> AIPAY_FRAMEWORK=openclaw alipay-bot payment-intent --session-id "<sessionId>" --framework "openclaw"
```

其中 `<sessionId>` 替换为框架提供的 `AIPAY_SESSION_ID` 的实际值或使用`session_list`工具获取到的实际值。
**执行该步骤结束后，需要立即提取订单字段**

#### Step 1b. 提取订单字段

从收银台链接参数及订单信息中提取以下 3 个字段（**仅提取这 3 个字段，禁止传递其他信息**）：

| 字段 | 说明 | 数据来源 |
|------|------|---------|
| **服务内容** | 订单详情、商品名称、服务描述 | 收银台链接参数、订单信息 |
| **支付金额** | 商品价格（必须包含币种） | 收银台链接参数、订单信息 |
| **支付对象** | 商家名称、服务提供方 | 收银台链接参数、订单信息 |

**数据约束**：
- 无法提取的字段填写"未明确"，**禁止推测或编造**
- `--intent-summary` 仅接受上述 3 个字段的结构化文本
- 禁止包含用户个人信息、对话历史、或任何与订单无关的内容
- 数据来源声明：3 个字段均解析自用户主动提供的收银台链接参数

**执行该步骤结束后，需要立刻关联订单摘要到支付会话**

#### Step 1c. 关联订单摘要到支付会话（请勿跳过此步骤，执行前请确保命令及参数正确且完整）

```bash
AIPAY_SESSION_ID=<sessionId> AIPAY_FRAMEWORK=openclaw alipay-bot payment-intent --session-id "<sessionId>" --framework "openclaw" --intent-summary "服务内容：xxx，支付金额：¥xx，支付对象：xxx"
```

其中 `<sessionId>` 替换为框架提供的 `AIPAY_SESSION_ID` 的实际值或从session列表/当前工作空间获取到的*uuid格式*的当前会话实际会话id

#### Step 1d. 展示订单信息（**请确保执行该步骤前，支付会话初始化及关联订单摘要到支付会话已完成**）

向用户展示以下标准格式的订单信息：

```markdown
服务内容：[提取内容 或 "未明确"]
支付金额：¥[金额]（[币种]） 或 "未明确"
支付对象：[支付对象 或 "未明确"]
```

**展示后立即继续**

订单摘要展示给用户后，**立即继续执行 Step 2（check-wallet）**，禁止等待用户确认。Step 1 的目的是记录和展示订单信息，不是征求用户许可， 但必须执行。

### 执行示例

```
用户：帮我支付这个订单 https://cashier.alipay.com/xxx?orderId=123&amount=0.01&subject=会员服务&seller=XX科技

助手（Step 1 中四个步骤 + Step 2 在同一轮内连续按顺序执行）：
  Step 1a. 执行 alipay-bot payment-intent --session-id <sessionId> --framework openclaw
  Step 1b. 从链接中提取：
     - 服务内容：会员服务
     - 支付金额：¥0.01
     - 支付对象：XX科技
  Step 1c. 执行 alipay-bot payment-intent --session-id <sessionId> --framework openclaw --intent-summary "服务内容：会员服务，支付金额：¥0.01，支付对象：XX科技"
  Step 1d. 展示给用户：
     服务内容：会员服务
     支付金额：¥0.01
     支付对象：XX科技
  Step 1d执行结束后立即继续执行 Step 2: alipay-bot check-wallet
  ...
```

## Step 2：检查钱包

### 命令

```bash
alipay-bot check-wallet
```

**不加任何参数。**

### 返回格式

JSON（纯 JSON 文本，不含 MEDIA 行或 Markdown）：

```json
{ "code": 200|500, "access_url": "string", "message": "string", "reason": "string" }
```

### 决策逻辑

> ⚠️ **状态判断必须同时检查 code 和 access_url 两个字段。code=200 不等于已授权，必须 code=200 且 access_url 为空才是已授权。**

| code | access_url | 状态 | → 下一步 | 对客输出 | 禁止操作 |
|------|-----------|------|---------|---------|---------|
| 200 | 非空 | 未授权 | **[中断] 调用 alipay-authenticate-wallet 技能** | "支付能力尚未授权" | 继续 Step 3、执行 apply-wallet、仅输出提示 |
| 500 | 任意 | 未开通 | **[中断] 调用 alipay-authenticate-wallet 技能** | "支付能力尚未开通" | 继续 Step 3、执行 apply-wallet、仅输出提示 |
| 200 | 空 `""` | 已授权 | **立即执行 Step 3: submit-payment**（无任何停顿） | （无需额外输出） | 停止、询问"是否继续支付"、调用 authenticate-wallet、执行 apply-wallet |
| 命令执行失败 / 非法 JSON | — | 不可用 | **→ STOP** | "钱包检查失败，无法继续支付" | 继续执行后续步骤；假设结果 |

### 未授权/未开通时的强制行为

当 code=200 且 access_url 非空，或 code=500 时：
- **应当**：调用 alipay-authenticate-wallet 技能（使用当前环境的技能调用机制）
- **禁止**：继续执行 Step 3（submit-payment）或 Step 4
- **禁止**：在本技能内执行 apply-wallet / bind-wallet
- **禁止**：仅输出"未授权"/"钱包不存在"等文字后停止
- **禁止**：询问用户"是否需要开通"后等待回复
- **禁止**：输出 access_url 给用户

### 已授权时的强制行为

当 check-wallet 返回 code=200 且 access_url 为空时：
- **必须立即执行 submit-payment**，无任何停顿
- **禁止**：输出"钱包已授权，是否继续支付？"
- **禁止**：等待用户确认
- **禁止**：调用 authenticate-wallet
- **禁止**：执行 apply-wallet

### 技能协作说明

当 Step 2 返回 `code=200` 且 `access_url` 非空时：
1. **告知用户**：输出"支付能力尚未授权，正在为您申请开通支付宝支付功能"
2. **调用授权技能**：调用 `alipay-authenticate-wallet` 技能，由它接管授权流程
3. **暂停当前技能**：不再继续执行本技能后续步骤，等待授权技能完成
4. **授权成功后继续**：当授权技能完成绑定（`alipay-bot bind-wallet` 返回成功），重新进入 Step 1）

## Step 3：提交支付
**前置条件：Step 1 的两次 payment-intent 都必须已完成，不得遗漏任何一次调用**

### 执行前校验

执行 submit-payment 前必须逐条检查，任一不通过则拒绝：

| 校验项 | 要求 | 不通过时的处理 |
|--------|------|---------------|
| 来源 | 需来自上下文中已有的真实 URL | 上下文中无收银台链接 → 向用户询问"请提供支付宝收银台链接" → STOP |
| 格式 | 必须是完整的 `https://` 开头的 URL，包含域名和路径 | URL 格式错误 → 向用户说明"该链接不是有效的支付宝收银台链接，请确认后重新提供" → STOP |
| 域名 | 必须匹配 `cashier*.alipay.com` 或 `*excashier*.alipay.com` | 域名不匹配 → 向用户说明"该链接不是有效的支付宝收银台链接，请确认后重新提供" → STOP |
| 完整性 | 需包含完整的 query 参数（如 `orderId=` 等） | URL 被截断 → 向用户说明"链接不完整，请提供完整的收银台链接" → STOP |

**禁止使用不完整、被截断、被修改或自行拼接的 URL 执行命令。**

### 命令

```bash
# 如果框架提供了会话变量 或 可以获取到当前会话的sessionId 或 当前运行框架为 openclaw
AIPAY_SESSION_ID=<sessionId> AIPAY_FRAMEWORK=openclaw alipay-bot submit-payment --payment-link '<收银台链接>' --session-id <sessionId>
```
# 如果无法通过任何途径获取会话变量
```
alipay-bot submit-payment --payment-link '<收银台链接>'
```

**入参**：
- `--payment-link`：收银台链接（**必填**，需逐字符完整传递，禁止截断或修改）

### 输出处理

 1. CLI 返回的 Markdown 文本逐字符原样输出，模板已包含状态标识。图片处理规则见 `references/image-output.md`。
2. 确保链接不被修改（包括 `alipays://` 协议链接必须完整输出）
3. MEDIA 行：提取图片路径后移除该行，用 message 工具发送图片与文本整合。无可用工具时将文本和图片原样输出给用户。详见 `references/image-output.md`。
4. **提取并保存 shortUrl**（Step 4 需要）：
   - 从输出中查找 `https://u.alipay.cn/...` 格式的 URL
   - shortUrl 是后续查询支付状态的唯一有效参数，**禁止用收银台链接代替**
   - 如果 CLI 输出中没有 shortUrl，说明 submit-payment 失败，按错误处理流程引导用户
5. **输出后 STOP**，等待用户下一轮通知

### CLI 返回模板对照表

| 场景 | 模板已包含的状态标识 |
|------|---------------------|
| submit-payment 成功 | "✓ 支付待确认" + 订单金额 + 支付链接 |
| submit-payment 直接成功 | "✓ 支付成功" + 订单金额 |
| submit-payment 处理中 | "⏳ 支付处理中" + 订单金额 |
| submit-payment 失败 | "✗ 支付失败" + 错误原因 |

### 输出示例

```
**✓ 支付待确认**
**订单金额**：**¥0.01**
正在处理中...
**支付方式**：
- **电脑端用户**：请 [点击此处](https://xxx) 打开收银台页面扫码支付
- **手机端用户**：请 [点击此处](https://xxx) 唤起支付宝APP完成支付
支付完成之后就可以在淘宝订单详情页查看您的订单状态啦～
```
（同时使用 message 工具发送图片 `/tmp/openclaw/alipay-bot-cli/qrcode/payment-confirm-xxx.png`，图片处理规则见 `references/image-output.md`）

### shortUrl 处理

| CLI 输出格式 | shortUrl 提取方式 |
|-------------|------------------|
| JSON（以 `{` 开头） | 取 `result.shortUrl` 或 `shortUrl` 字段 |
| 纯文本 | 查找 `https://u.alipay.cn/` 或 `https://render` 开头的 URL |

**shortUrl vs 支付链接**（禁止混淆）：

| 类型 | 格式 | 用途 |
|------|------|------|
| shortUrl | `https://u.alipay.cn/...` 或 `https://render*.alipay.com/...` | Step 4 查询支付状态（`-p` 参数） |
| 支付链接 | `https://cashier*.alipay.com/...` 或 `alipays://...` | 展示给用户扫码支付 |

### 错误处理

| 错误场景 | 处理方式 |
|---------|---------|
| CLI 返回错误信息 | 原样输出错误信息，提示用户检查链接是否有效或重新获取 |
| CLI 输出中无 shortUrl | 支付提交失败，提示用户"支付提交失败，请检查收银台链接是否有效" |
| 命令执行超时/网络不可达 | 提示"网络请求失败，请检查网络连接后重试"，可重试 1 次 |
| 收银台链接已过期 | 提示"链接已过期，请重新获取收银台链接"，流程结束 |
| 收银台链接格式错误 | 提示"该链接不是有效的支付宝收银台链接，请确认后重新提供"，流程结束 |
| 多次支付失败（3次+） | 提示用户"多次支付失败"，执行流程四问题反馈 |

### 关键：输出后必须停止

Step 3 执行完成后，**必须先将完整输出展示给用户，然后本轮响应结束（STOP）**。用户在下一轮表示已支付或查询状态时，使用 Step 4。

## Step 4：查询支付状态

### 触发条件

用户在任何时候表示已支付或查询支付状态，常见表述：
- "已支付"、"付好了"、"支付完成了"、"搞定了"
- "支付成功了吗"、"帮我看看支付状态"、"查询刚才的订单"
- "刚才那个订单我已支付"、"看看刚才那笔支付"

**触发后立即执行查询**，不要等待额外确认。

### 命令

```bash
alipay-bot query-payment-status -p '<shortUrl>'
```

**入参**：
- `-p`：shortUrl（必填，来自 Step 3 返回的 shortUrl，必须逐字符不变地传递）

**参数来源约束**：
- 使用 Step 3 中提取的 shortUrl（`https://u.alipay.cn/...`）
- **禁止使用收银台链接**（`cashier*.alipay.com`）代替 shortUrl
- 当前上下文中已丢失 shortUrl → 提示用户"支付会话已过期，请重新发起支付"

### 状态分支处理

| CLI 返回标识 | 状态 | 处理方式 |
|-------------|------|---------|
| "✓ 支付已完成" | 支付成功 | 原样输出，流程结束 |
| "✓ 支付状态同步中" | 支付处理中 | 原样输出，提示用户完成支付后再次通知 |
| "✗ 支付已关闭" | 支付失败/关闭 | 原样输出，引导用户重新发起支付 |
| "⚠ 支付状态查询异常" | 查询异常 | 原样输出，可重试查询 1 次；仍异常则进入流程四问题反馈 |

### shortUrl 丢失处理

上下文中无对应的 shortUrl 链接 → 命令执行会提示类似"支付会话已过期，请重新发起支付"的信息，原样输出结果。

## 边界条件补充

| 场景 | 处理方式 |
|------|----------|
| 收银台链接已过期 | 提示用户"链接已过期，请重新获取收银台链接"，流程结束 |
| 支付过程用户取消 | 保留当前状态，用户可重新发起支付 |
| 用户表示已支付或查询状态 | 执行 Step 3 query-payment-status 查询最新状态 |
| 支付失败后用户重新发起 | 从 Step 1 重新开始完整流程 |
| shortUrl 丢失 | 提示用户"支付会话已过期，请重新发起支付" |
| shortUrl 在上下文中丢失 | 提示用户"支付会话已过期，请重新发起支付"，流程结束 |
| 多次支付失败（3次+） | 提示用户"多次支付失败"，执行流程四问题反馈 |
| 收银台链接格式错误 | 提示用户"链接格式无效，请确认后重新提供"，流程结束 |
| 用户在 Step 2 后发送无关消息 | 忽略无关消息，等待用户表示已支付或查询状态 |

## 对客输出要求（缺少以下信号词 = 对客表达失败）

| 步骤 | 场景 | 必须向用户输出的信号 |
|------|------|---------------------|
| Step 2 | check-wallet 已授权 | （无需额外输出，直接进 Step 3） |
| Step 2 | check-wallet 未授权/未开通 | "支付能力尚未开通/尚未授权，正在为您申请" |
| Step 2 | check-wallet 命令执行失败 | "钱包检查失败/无法继续支付" |
| Step 3 | submit-payment 成功 | 原样透传 CLI 输出（含"✓ 支付待确认"或"✓ 支付成功"） |
| Step 3 | submit-payment 失败 | 原样透传（含"✗ 支付失败"） |
| Step 4 | 支付已完成 | 原样透传（含"✓ 支付已完成"）+ 明确告知"支付成功/支付完成" |
| Step 4 | 同步中 | 原样透传（含"✓ 支付状态同步中"）+ 提示稍后去支付宝账单页查看订单状态 |
| Step 4 | 已关闭 | 原样透传（含"✗ 支付已关闭"）+ 引导重新发起 |
| Step 4 | 查询异常 | 原样透传（含"⚠ 支付状态查询异常"） |

## 检查点设计

- **Step 1 完成后**：确认订单信息已展示给用户，立即继续 Step 2
- **Step 2 完成后**：确认钱包状态（code=200 & access_url 为空）
- **Step 3 完成后**：输出支付已提交结果给用户，然后 STOP（等待用户下一轮）
- **Step 4 执行前**：确认 shortUrl 存在且有效
- **用户在下一轮表示已支付或查询状态时**：执行 Step 3 查询支付状态