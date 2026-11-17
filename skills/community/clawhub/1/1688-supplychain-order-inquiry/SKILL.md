---
name: 1688-supplychain-order-inquiry
version: 0.50.0
description: |
  跨平台供应链助手Skill，含两大能力域：①订单询盘——对指定订单/采购单发起询盘（支持单个或多个订单同问题）、查询商家回复、对话配置；②商品SKU提取——从 Shopify / AliExpress 商品链接提取全部 SKU 变体，输出含 image（原图链接）与 query（SKU 属性组合）的 JSON 数组。
  订单询盘触发词：询盘、询价、议价、帮我问商家、订单/采购单、发货时间、什么时候发货、发货了吗、催发货、物流单号、快递单号、运单号、物流跟踪、超时未发货、商家回复、询盘结果、总结商家回复。
  SKU提取触发词：提取SKU、获取SKU、提取变体、变体规格、SKU信息、Shopify商品信息、AliExpress商品信息、AE链接提取、速卖通SKU。
metadata: {"openclaw": {"requires": {"bins": ["python3"]}}, "allowed_tools": ["browser"]}
---

# 1688-supplychain-order-inquiry（订单询盘 + 商品 SKU 提取 Skill）

本 Skill 承载**两个互斥的能力域**，进入任何流程前**必须先做能力域语义路由**（见下一节），路由结果决定执行方式与输出契约：

| 能力域             | 执行方式                             | 输出形态                          |
| ------------------ | ------------------------------------ | --------------------------------- |
| A. 订单询盘域      | `python3 {baseDir}/cli.py <command>` | **纯 JSON**（无任何额外文字）      |
| B. 商品 SKU 提取域 | `browser` 工具（navigate + evaluate）| **JSON 数组**（`image` + `query`） |

订单询盘域统一入口：`python3 {baseDir}/cli.py <command> [options]`（必须使用绝对路径，`{baseDir}` 为 Skill 所在目录）

---

## 能力域语义路由（第一步 · 先判域再判命令）

按以下顺序判定，**先命中者即为最终路由**：

| 判定信号                                                                             | 路由到                                 |
| ------------------------------------------------------------------------------------ | -------------------------------------- |
| 诉求落在**已生成订单/采购单**上下文（订单号 + 面向商家提问/议价/查回复/对话配置/AK 配置） | **域 A** → 见《命令路由（判断标准）》 |
| 提供**商品链接**且诉求是拿 SKU / 变体 / 规格 / 各款式图片，链接域名含 `aliexpress.com`、`aliexpress.us` 等 | **域 B** → `sku_extract_aliexpress`   |
| 提供**商品链接**且诉求是拿 SKU / 变体 / 规格，链接为 Shopify 站点（`*.myshopify.com` 或自定义域名，路径含 `/products/<handle>`） | **域 B** → `sku_extract_shopify`      |
| 只给了 SKU 提取诉求但**没给链接**                                                    | 引导用户补商品链接，不猜平台           |
| 给了商品链接但**平台无法判定**（既非 AliExpress 也非 Shopify 特征）                  | 先按 Shopify 通用路径尝试；失败则如实说明该平台暂不支持 |
| 商品搜索、找货、选品、供应商询盘（无订单号）                                         | **不承接**，如实告知能力边界           |

### 消歧要点

- **「订单号」vs「商品链接」是最强区分信号**：出现订单/采购单号 → 域 A；出现商品详情页 URL 且无订单号 → 域 B。
- 「询价 / 要价格」在**订单上下文**里是询盘（域 A，question 走 `目标总价<金额>`）；在**商品链接上下文**里则走域 B，但注意域 B 已不再交付价格字段（只有 `image` + `query`），应向用户如实说明。
- 同一句里既有订单号又有商品链接时，以用户**动词诉求**为准：「问商家」→ 域 A；「提取 SKU」→ 域 B；两者都要则**分两步依次执行**，两个域的产物作为**两条独立消息**输出（域 A 的纯 JSON 必须单独成一条，不得与域 B 的交付内容拼接）。
- 域 B **不涉及** AK、网关、`cli.py`，不要为域 B 检查或引导配置 AK。

---

## 严格禁止 (NEVER DO)

- 不向用户透出内部工具名和技术状态
- 不编造询盘结果和 SKU 数据，所有结果必须来自工具返回
- 不凭本文件摘要拼凑参数——执行前先阅读 `references/capabilities/<command>.md`
- 域 A（订单询盘）最终回复必须是纯 JSON（首字符 `{` 或 `[`，末字符 `}` 或 `]`），不得包含任何自然语言、markdown 格式或解释文字
- 不得跨域套用输出契约：域 A 与域 B 均只能输出裸 JSON / JSON 数组（无代码块、无汇总行、无自然语言包裹），且域 B 不得夹带价格 / 库存 / 店铺字段

## 最终输出契约（HARD RULE · 入口无关 · 最高优先级）

**本条对所有调用入口无条件生效**——无论是 `POST /workflow/run` 直连本 skill 的 workflow，还是 `POST /task/create` 经由 ReAct 主 agent 把本 skill 的 workflow 当作 Workflow tool 调用，也无论未来新增任何入口：

主 agent 的**最终一条消息，必须原样等于 workflow（或 cli.py）返回的那段 JSON 字符串，逐字透传**。

- ⛔ 不得把 workflow 返回的 JSON 当作"中间结果"再总结、改写、转成表格或自然语言。
- ⛔ 不得在 JSON 前后追加任何话术、markdown 包裹、解释或 emoji。
- ⛔ 不得合并进度话术与 JSON（进度话术若有，必须是执行前的独立消息）。
- ✅ workflow 返回什么 JSON，最终就交付什么 JSON，一个字符都不改。

即 `{"success": true, "wwTaskId": "...", "message": "询盘已成功发送"}` 这类结构化 JSON 必须原封不动抵达调用方，与走哪条入口无关。

> **域 B（商品 SKU 提取）同样遵循纯 JSON 输出**：域 B 由 `browser` 工具执行，交付的是 `image` + `query` 的**纯 JSON 数组**（首字符 `[`，末字符 `]`），不得包裹代码块、不得附加汇总文字或任何自然语言，与域 A 输出契约一致。具体格式见 `references/capabilities/sku_extract_shopify.md` / `sku_extract_aliexpress.md`。

## 直连 workflow 入口（零思考直通）

当用户明确指定 workflowName（如"用 / 走 / 调用 order-inquiry-workflow 这个 workflow"），或 Harness 平台工作模板节点的 agentHints 指向本 skill 的 workflow 时，主 agent **不参与业务理解**，只做一次路由调用：

```
POST /workflow/run
{
  "workflowName": "1688-supplychain-order-inquiry-workflow",
  "instruction": "<用户原话>",        // 二选一或两者都传
  "params": { "command": "...", ... } // 结构化时传
}
```

- 结构化（零 LLM）：`{ "params": { "command": "inquiry_send", "orderIds": ["..."], "question": "目标总价<1200>" } }`
- 自然语言：`{ "instruction": "帮我问下 705123456789 那个订单什么时候能发货" }`

路由原则：用户诉求**必须落在已生成订单/采购单的上下文**里才进本 workflow——包括：向商家就订单提问（发货时间/物流单号/订单状态）、订单议价（目标总价）、查询商家询盘回复、订单对话配置、访问 AK 配置。**不承接**商品搜索、供应商询盘、找货、选品等非订单类诉求；**也不承接域 B 的商品 SKU 提取**（域 B 不走 workflow，直接用 `browser` 工具执行）。workflowName = `1688-supplychain-order-inquiry-workflow`（= SKILL name + `-workflow` 后缀，与 SKILL name 显式区分）。

⛔ 主 agent 不得：理解业务意图 / 引导用户补参数 / 改写 workflow 输出的 JSON / 用本 SKILL 下的 cli.py 绕开 workflow 直调。（其中"不得改写 workflow 输出的 JSON"由上文《最终输出契约》约束，对所有入口生效，不限本小节。）

---

## 输出两阶段（独立两条消息，严禁合并）

1. **执行前**：可单独输出进度话术（如"正在向商家发起询盘，请稍等..."）
2. **执行后**：单独输出纯 JSON，格式见各命令 reference 的"Agent 输出格式"

❌ 禁止：`正在向商家发起询盘，请稍等...{"success": true, ...}`（话术与 JSON 拼在同一条消息）

> 上述两阶段仅适用于**域 A**。域 B（SKU 提取）可先输出进度话术（如"正在打开商品页面提取 SKU，请稍等..."），最终以**纯 JSON 数组**交付（无代码块、无汇总）。

## 执行前置（MUST）

**同一会话内首次执行某命令/能力前**，MUST 完整阅读 `references/capabilities/<command>.md` 获取准确参数、输出格式和注意事项（域 B 对应 `sku_extract_shopify.md` / `sku_extract_aliexpress.md`）；本会话已读过且文件无变更则无需重读。

遇到 `success: false` 时（域 A），MUST 先阅读 `references/common/error-handling.md`，不要自行猜测错误原因。

## 能力速查

### 域 A·订单询盘（`cli.py` 命令）

| 命令             | 能力             | 示例                                                                            |
| ---------------- | ---------------- | ------------------------------------------------------------------------------- |
| `inquiry_send`   | 订单询盘（支持多订单同问题） | `cli.py inquiry_send -o "5116391244078005116,5116391244078005117" -q "什么时候能发货"` |
| `inquiry_query`  | 询盘结果查询     | `cli.py inquiry_query -t "task-uuid-xxx"`                                       |
| `inquiry_config` | 询盘对话配置     | `cli.py inquiry_config`（单轮，默认）/ `cli.py inquiry_config --multi-round`    |
| `configure`      | 配置AK           | `cli.py configure YOUR_AK`                                                      |

所有命令输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

### 域 B·商品 SKU 提取（`browser` 工具，无 CLI）

| 能力                     | 适用链接                                       | reference                                        |
| ------------------------ | ------------------------------------------ | ------------------------------------------------ |
| `sku_extract_shopify`    | Shopify 商品页（`/products/<handle>`）       | `references/capabilities/sku_extract_shopify.md`    |
| `sku_extract_aliexpress` | AliExpress / 速卖通商品页（`/item/<id>.html`） | `references/capabilities/sku_extract_aliexpress.md` |

两个能力均交付 **`image` + `query` 的 JSON 数组**，**不输出价格、库存、店铺信息**。

---

## 域 A·订单询盘触发流程

**意图识别（泛化）**：绑定了订单/采购单号 + 诉求指向商家 → 即为询盘，不限表达形态——指令式（"帮我问商家XX / 询个价 / 问下发货时间"）或正文式祈使句（"麻烦提供一下快递单号 / 麻烦尽快发货"），把用户诉求作为询盘 question 传入。

1. 确认订单 ID 和询盘问题（缺失则引导用户提供）
2. 识别可选参数意图（对话轮次 `--order-single-round`、超时 `--timeout`、附件 `--image-url` / `--image`、扩展字段 `--ext`），识别规则见 `references/capabilities/inquiry_send.md`；**用户未提及的可选参数一律不传**
3. 输出中间话术 → 执行命令 → 按 reference 的"Agent 输出格式"输出纯 JSON

## 命令路由（判断标准）

> 本小节仅在上文《能力域语义路由》已判定为**域 A** 后适用。

| 场景                                                                 | 走法                              |
| -------------------------------------------------------------------- | --------------------------------- |
| 单订单；或多订单问题相同且附件相同                                   | `inquiry_send`                    |
| ≥2 订单、问题相同、但各订单分别指定了不同附件（满足下方触发条件）    | `inquiry_send` + `--orders-detail`|
| ≥2 订单且各自问题/目标总价不同                                       | 分多次调用 `inquiry_send`（每次一个订单/一组同问题订单） |

> 本 skill 已下线 `batch_inquiry` 能力。多订单同问题直接用 `inquiry_send` 的 `-o` 传多个订单号即可；各订单问题不同的场景，请分多次调用。

### 复合意图（配置 + 发送）

当用户输入**同时包含**对话配置指令（"设置单轮询盘"/"设置超时时长"等）和面向商家的发送内容（订单号 + 发送内容/消息正文）时，**必须作为一次 `inquiry_send` 调用处理**，将配置参数（`--order-single-round`、`--timeout`）作为 `inquiry_send` 的可选参数一并传入。**严禁拆成两次调用**（一次 `inquiry_config` + 一次 `inquiry_send`）。`inquiry_send` CLI 原生支持这些配置参数，一次调用即可完成全部诉求。

仅当输入**纯粹只有配置指令、没有任何面向商家的内容**（无订单号、无发送正文）时，才走 `inquiry_config`。

### 目标总价

「目标总价」本身就是询盘问题，question 格式为 `"目标总价<金额>"`（如"目标总价17"）。各订单目标总价**相同** → 合并走 `inquiry_send`；**不同** → 分多次调用 `inquiry_send`。仅提供订单 ID 无目标总价/问题时，引导用户说明询盘目的。

### orders-detail 触发条件（必须同时满足两条）

1. **关键词**：用户输入含"分别附"/"各配"/"每个订单配"/"各自附"等按订单维度分配附件的表达
2. **格式**：用户输入逐订单列举了各自的图片/文件链接（形如"订单A：图片 xxx，文件 yyy；订单B：图片 zzz"）

不满足任一条件 → 附件走全局 `--image-url` 传入。JSON 结构与细节见 `references/capabilities/inquiry_send.md`。

## 询盘结果查询

用户说"商家回复了吗 / 总结询盘结果 / 询盘有结果了吗 / 那个订单问完没 / 商家回消息没"等 → 确认 `taskId`（= 发起询盘时返回的 `wwTaskId`，缺失则引导用户提供或从上下文提取）→ 中间话术"正在查询商家回复，请稍等..." → 执行 `inquiry_query -t <taskId>` → 按 `references/capabilities/inquiry_query.md` 的 "Agent 输出格式" 输出纯 JSON（终态透传 `status` + `summary`，非终态只返回 `status` + 固定 message）。

## 询盘对话配置

用户明确要**对询盘的对话能力本身做配置**（"设置成单轮 / 关掉 AI 自动回复 / 开启多轮对话"等，而非发起一次询盘）→ 中间话术"正在为您配置对话能力，请稍等..." → 执行 `inquiry_config`（明确要多轮加 `--multi-round`，其余默认单轮）→ 按 reference 输出纯 JSON。若用户实际是要发起询盘，走 `inquiry_send`。

**注意**：若用户输入同时包含配置指令和发送内容（订单号 + 面向商家的正文），**不要走 `inquiry_config`**，应走 `inquiry_send` 并将配置参数（`--order-single-round`、`--timeout`）一并传入。`inquiry_send` CLI 原生支持这些参数，无需分两次调用。

---

## 域 B·商品 SKU 提取流程

**意图识别**：用户给出**商品详情页链接**（无订单号）+ 诉求指向该商品的 SKU / 变体 / 规格 / 各款式图片 → 即为 SKU 提取。表达形态不限："提取一下这个链接的 SKU"、"这个商品有哪些颜色尺码"、"把各款式的图拉出来"。

**统一交付契约**：两个平台能力最终都输出同一形状的纯 JSON 数组（首字符 `[`，末字符 `]`，无代码块包裹），每项仅含两个字段：`[{"image": "<原图URL>", "query": "<SKU 属性组合>"}]`

- `query` 分隔符按平台约定：Shopify 用**英文逗号**（`"Grøn,38"`），AliExpress 用**空格**（`"Red Large"`），不要互相套用
- 两个平台均**不交付价格、库存、店铺、商品描述**；用户若明确要价格，如实说明当前能力不返回价格

1. **判平台**：按链接域名 / 路径特征选定能力
   - `aliexpress.com` / `aliexpress.us` / `zh.aliexpress.com`，路径含 `/item/<id>.html` → `sku_extract_aliexpress`
   - `*.myshopify.com` 或自定义域名且路径含 `/products/<handle>` → `sku_extract_shopify`
   - 无链接 → 引导用户补链接；平台无法判定 → 先按 Shopify 通用路径试探，失败则如实说明暂不支持该平台
2. **读 reference**：本会话首次执行该能力前，MUST 完整阅读对应的 `references/capabilities/sku_extract_*.md`，取其中的 evaluate 脚本原文，**不得凭记忆改写脚本**
3. **执行**：`browser navigate`（`wait_until=networkidle`、`timeout=60000`）→ `browser evaluate` 执行脚本
   - Shopify：单脚本三级降级（product.json → 内嵌 JSON → ShopifyAnalytics meta），一次 evaluate 完成
   - AliExpress：先跑**维度探测脚本**；仅当其返回空数组时，才降级到**逐个点击脚本**，不要两个都跑
4. **组装输出**：按 reference 的第 3 步将原始返回映射为 `image` + `query` 的纯 JSON 数组
   - Shopify：变体 title 按 ` / ` 拆分后用逗号拼接为 query；脚本额外返回的 `price` / `available` / `sku` **一律忽略**
   - AliExpress：单维度直取选项值；多维度做笛卡尔积、图片取带图维度、query 空格拼接
   - 脚本返回失败或空结果时如实说明未能提取及可能原因，**不编造 SKU、图片链接和属性组合**

多个链接 → 逐个执行并分节输出，每节标明商品标题或链接。跨平台混合链接 → 各自走对应能力。
