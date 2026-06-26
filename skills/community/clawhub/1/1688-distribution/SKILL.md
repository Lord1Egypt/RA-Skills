---
name: 1688-distribution
description: 1688 分销唯一主入口。选品铺货、订单管理、知识库查询、店铺绑定，涵盖分销全链路。当用户提到铺货、选品、分销、上架、查订单、催发、旺旺、发货流程、绑店时触发。不要在用户仅询问非1688业务（如闲聊、天气、翻译等无关话题）时触发。
metadata: {"openclaw": {"emoji": "🚀", "version": "1.0.0", "requires": {"bins": ["python3"]}}}
---

# 1688 分销

统一入口：`python3 scripts/cli.py <command> [options]`

所有命令输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

**展示时直接输出 `markdown` 字段内容，禁止在后面追加任何"后续建议""操作指引""后续操作"等自创内容（无论是否含链接）。**

## ⚠️ 核心限制

**失败时直接告知用户，不编造！**

```
❌ 禁止：编造商品数据、伪造链接、臆测店铺信息、用搜索引擎补充数据、改写CLI返回结果...
✅ 仅允许：原样输出CLI工具返回的markdown，禁止擅自增加额外内容；失败时告知用户原因
```

**严格禁止（NEVER DO）：**

1. 🚫 禁止编造数据/链接 — 所有数据必须来自接口返回，不得自行构造 URL
2. 🚫 禁止未经确认执行铺货 — 铺货不可逆，必须用户明确确认商品和目标店铺
3. 🚫 禁止品牌未授权商品铺货 — `isBrandOffer=true` 且 `isBrandAuth=false` 绝对不能铺货
4. 🚫 禁止擅自添加筛选条件 / 改写用户原话 / 猜测渠道和店铺
5. 🚫 禁止向用户展示授权链接 — 浏览器授权流程中不得将 URL 展示给用户
6. 🚫 禁止使用搜索引擎、访问外部网站获取业务数据
7. 🚫 禁止失败后自行重试、补充、编造 — 直接告知用户失败原因，等待指示
8. 🚫 **禁止在任何操作完成后追加"后续建议""后续操作""操作指引"等内容** — 无论是否含链接，一律不加
9. 🚫 **禁止在未阅读 reference.md 前执行任何业务命令** — 必须**先 read_file 加载对应 reference.md → 再执行命令**。命令的动作名、参数名、参数格式必须从 reference.md 中获取，不得凭记忆或猜测拼凑

---

## AK 授权处理

AK（Access Key）用于身份认证，存储在 `{workspace}/.1688-AK/.ak_store.json`。

**授权检查**：任何业务操作前执行 `python3 scripts/capabilities/configure/cmd.py --status`，已授权则直接执行，同一会话内无需重复检查。

**未授权时自动处理（静默执行，不询问用户）：**

```
1. 执行：python3 scripts/capabilities/configure/cmd.py --get-ak
2. 命令输出 JSON（含 action: "browser_use" 和 url）
3. 必须使用 browser_use 工具打开该 url（不是展示给用户）
4. 执行 --status 确认 AK 已配置
5. 继续执行原查询
```

**禁止**：将授权链接展示给用户 / 让用户手动打开 / 向用户提及 AK、授权等细节。

**手动配置 AK**（浏览器获取失败时的兜底）：
1. 用户前往 https://clawhub.1688.com/ 登录后右上角点击🔑复制 AK
2. 执行：`python3 scripts/capabilities/configure/cmd.py <AK值>`
3. `--status` 确认

**重置 AK**：`python3 scripts/capabilities/configure/cmd.py --reset <新AK值>`，或 `--clear` 后重新授权。

---

## 意图判断

| 用户意图 | 路由到 | 触发关键词 |
|---------|--------|------------|
| 选品 + 铺货 | [选品铺货助手](#选品铺货助手) | 选品、找商品、推荐、铺货、上架、分销 |
| 订单管理 | [订单助手](#订单助手) | 查订单、退款、风险订单、催发、催揽、旺旺 |
| 知识查询 | [知识库助手](#知识库助手) | 怎么操作、教程、流程、指南、发货流程 |
| 查店铺 | [店铺查询](#店铺查询) | 查店铺、绑店、授权 |
| 重置 AK | [AK 授权处理](#ak-授权处理) | 重新设置 AK、重置 AK、更新 AK |

> 判断不清时优先询问用户意图，不要猜测。与1688分销无关的话题不触发本技能。

---

## ❗ 执行前置（最高优先级）

> ⛔ **铁律：先读文档 → 再执行命令。read_file 加载对应 reference.md 之前，禁止执行该场景的任何 CLI 命令。**

| 业务场景 | 执行前必须阅读的参考文档 |
|---------|---------------------|
| 选品（关键词/图搜） | `scripts/biz/product_search_helper/reference.md` |
| 分销参谋（商品详情） | `scripts/biz/offer_info/reference.md` |
| 铺货执行 | `scripts/biz/distribute_helper/reference.md` |
| 店铺查询 | `scripts/biz/shop_info/reference.md` |
| 订单管理 | `scripts/biz/order_helper/reference.md` |
| 知识库查询 | `scripts/biz/knowledge_helper/reference.md` |

同一会话内后续重复调用可复用已加载知识，无需重复阅读。

---

## 选品铺货助手

流程：**检查AK → 选品 → 决策分析 → 确认店铺 → 铺货 → 结果反馈 → 后续触发**

> 每步执行前须确保已阅读对应 reference.md（见[执行前置](#-执行前置最高优先级)）。

### 第一步：选品（用户已有商品 ID 时跳过）

根据用户输入自动选择模式：
- **文字描述** → 关键词选品（`distribution_select_offer`）
- **图片链接/文件** → 图搜选品（`same_img_offer_search`）

**选品数量策略** — 超量请求再精选，防止接口去重/过滤导致不足：

| 用户要求 N | 实际请求 page_size | 说明 |
|-----------|-------------------|------|
| N ≤ 25 | min(N × 2, 50) | 请求 2 倍，精选 N 个 |
| 25 < N ≤ 50 | 50 | 已达上限 |
| 未指定 | 20 | 取前 10 个候选 |

精选优先级：代发价低 > 30天分销单量高 > 服务好（包邮、一件代发、退货保障）。展示时以实际精选数量为准，禁止虚报。

### 第二步：选品决策分析（选品后自动执行）

对每个候选商品查询分销参谋数据，查询失败的静默过滤。综合分析推荐理由和风险，按推荐指数排序展示，询问用户确认。

**🚫 品牌授权检查（必须执行）**：当 `isBrandOffer=true` 且 `isBrandAuth=false` 时，该商品**不能铺货**（侵权风险），展示时标记 `🚫 不可铺货`，并给出授权链接：
> `https://air.1688.com/app/channel-fe/distribution-work/brand.html#/auth_apply?offerId={offerId}`

### 第三步：确认目标店铺

调用 `shop_and_tool_info` 查询店铺列表，过滤已过期的工具/店铺：
- **单店铺** → 直接使用
- **多店铺** → **必须列出所有可用店铺，等待用户指定，禁止自动选择**

### 第四步：执行铺货

调用铺货接口，根据 errorCode 展示结果反馈。

### 第五步：铺货后续触发（自动执行）

铺货完成后，若会话中有选品候选列表，自动检查未铺货商品，询问用户是否继续。

---

## 订单助手

流程：**检查AK → 查询订单 → 催发催揽 → 查询商家回复**

### 查询订单

根据用户意图构造查询参数（订单 ID / 时间范围 / 状态 / 退款状态），无条件时默认查当天。展示订单统计、列表、风险订单、退款订单。

### 催发催揽（有风险订单时）

从查询结果筛选风险订单，按卖家分组，为每个卖家生成催发消息并通过旺旺发送。

### 查询商家回复（用户主动触发）

催发后告知用户商家通常 5-10 分钟回复，用户要求查询时用 `task_id` 调用 `query_reply`。

---

## 知识库助手

流程：**检查AK → 解析意图 → 确认渠道/工具 → 检索知识库 → 总结输出**

识别 query（原封不动）、渠道、工具三要素，用户未明确时**必须先询问**。query 参数严禁改写，必须传递用户原话。按参考文档中的召回判断规则和展示格式输出。

---

## 店铺查询

调用 `shop_and_tool_info` 查询绑定的分销工具和店铺，自动过滤已过期项。

- **单店铺** → 直接使用
- **多店铺** → **必须列出所有可用店铺，等待用户指定目标店铺，禁止自动选择**
- **未绑定店铺（toolList 为空）** → 输出绑店引导：

> 您还没有绑定店铺到 1688 分销系统，需要先完成绑店才能铺货。
>
> ### 绑店步骤
> 1. 进入绑店页面，选择下游平台（抖音/淘宝/拼多多等）
> 2. 授权 1688 分销工具，勾选"我同意并签署协议"
> 3. 订购并授权下游工具（铺货工具 + 交易工具）
> 4. 确认显示"已授权"后，绑店完成
>
> **绑店入口：**
> - [一件代发页面](https://air.1688.com/app/channel-fe/search/index.html?#/result)
> - [AI 工作台绑店](https://air.1688.com/app/channel-fe/distribution-work/ai-assistant.html#/multi-agent-shop-binding)
>
> 遇到问题可加入官方钉钉群（群号：41361847）咨询。绑店完成后告诉我，我继续帮您铺货。

查询完成后主动询问用户是否需要铺货或其他操作。

---

## 输出格式

### 选品结果展示

> ❗ **每个商品必须包含链接**，格式：`[{offerId}](https://detail.1688.com/offer/{offerId}.html)`，嵌入到商品ID中。缺少链接 = 严重错误。

**卡片格式（≤3个商品）：**
```
### [{offerId}](https://detail.1688.com/offer/{offerId}.html) {title}
**代发价**：¥{dfPrice}（邮费 ¥{dfPost}） | **30天分销单量**：{fxOrdCnt30d}
**风险提示**：🚫 品牌未授权不可铺货 → [申请授权](https://air.1688.com/app/channel-fe/distribution-work/brand.html#/auth_apply?offerId={offerId})
```

**表格格式（>3个商品）：**
```
| 商品ID | 商品名称 | 代发价 | 邮费 | 30天分销单量 |
|--------|----------|--------|------|------------|
| [{offerId}](https://detail.1688.com/offer/{offerId}.html) | {title} | ¥{dfPrice} | ¥{dfPost} | {fxOrdCnt30d} |
```

⚠️ 输出前逐行自检"商品ID"列是否含链接，缺失则补全后再输出。品牌未授权商品在表格后单独标注风险提示。

### 铺货结果展示

铺货命令返回的 `markdown` 字段已是完整回复，**直接原样转发给用户，不得修改、不得追加任何内容**。调用时传入 `shop_name` 和 `tool_name` 参数。铺货后若有未铺商品，询问用户是否继续。**禁止追加"后续操作建议"等任何自创内容。**

### 订单列表展示

```
## 订单查询结果
**查询范围**：{时间范围} | **总计**：{totalCount} 笔
| 订单号 | 状态 | 商品 | 金额 | 卖家 |
|--------|------|------|------|------|
| {orderId} | {orderStatusText} | {productName} | ¥{fee} | {seller} |
⚠️ 风险订单：{N} 笔（需及时催发）
```

---

## Tool 总览

| 工具名 | 用途 | 调用方式 |
|--------|------|----------|
| `distribution_select_offer` | 关键词选品 | `python3 scripts/cli.py product_search_helper search --filters='[...]'` |
| `same_img_offer_search` | 图搜选品 | `python3 scripts/cli.py product_search_helper search --image_url="..."` |
| `distribution_offer_info` | 商品分销参谋 | `python3 scripts/cli.py offer_info query --offer_id="..."` |
| `shop_and_tool_info` | 店铺和工具列表 | `python3 scripts/cli.py shop_info query` |
| `distribute_offer` | 铺货到下游店铺 | `python3 scripts/cli.py distribute_helper execute --app_key="..." --shop_code="..." --channel="..." --offer_ids="..."` |
| `fx_query_order` | 查询分销订单 | `python3 scripts/cli.py order_helper query [--order_id=...] [--order_status=...]` |
| `fx_send_ww` | 旺旺催发 | `python3 scripts/cli.py order_helper send --question="..." --order_ids=...` |
| `fx_ww_reply` | 查询商家回复 | `python3 scripts/cli.py order_helper query_reply --task_id=...` |
| `distribution_knowledge_tool` | 分销知识库 | `python3 scripts/cli.py knowledge_helper query --query="..." [--channel="..."] [--business="..."]` |

---

## 异常处理

| 场景 | 处理方式 |
|------|----------|
| AK 未授权 | 自动执行 `configure --get-ak`；失败则引导用户手动配置 |
| 所有工具均已过期 | 提示用户续订分销工具 |
| `result.success` 为 false | 根据返回的 `markdown` 或 `message` 给出失败原因 |
| 接口调用异常 | 提示检查网络或联系技术支持 |
| 未绑定店铺 | 输出绑店引导话术 |
| 品牌商品未授权 | 不能铺货，引导申请品牌授权 |

**核心原则**：失败时直接告知用户，不要尝试其他方式获取或补充数据。

**全局输出规则**：所有操作（铺货、选品、订单查询、知识库等）完成后，只输出工具返回的结果，**禁止在末尾追加任何"后续操作建议""后续建议""操作指引"等自创内容（无论是否含链接）**。
