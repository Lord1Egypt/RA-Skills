# 粉象 MCP 工具参考

## 连接

- 生产：`https://api.fenxianglife.com/njia/mcp`
- 协议：MCP Streamable HTTP（无状态，`POST /mcp`），JSON-RPC 2.0；`initialize` 返回 `instructions`（选工具与回答规则），`prompts/list` 有 4 个常用提示词
- 鉴权：当前服务不需要 API Key；如后续恢复，支持 `Authorization: Bearer <API Key>` 或 `X-Api-Key: <API Key>`
- 请求头：`Content-Type: application/json`，`Accept: application/json, text/event-stream`
- 所有工具只读：不下单、不改用户数据

## 通用约定

- 每个工具都有可选参数 `responseFormat`：`markdown`（默认）或 `json`；它不在 `tools/list` 的入参定义里（宿主默认拿 Markdown），脚本和接口调用需要 JSON 时再传。
- Markdown 结果先是 `### 回答要点（可直接转述给用户）`，再是 `### 数据明细（供核对与追问，不必逐项展示）`；JSON 结果里回答要点在 `summary` 字段。
- 回答要点里比价一律是表格，商品列表带 `#` 序号（用户说「第 N 个」时按序号找那件商品）；回答要点总带当前商品的 `[去下单]` 链接（跟到手价、店铺写在同一行）。有历史价时放在买法之后、下一步之前，分两块、图在表上面：「价格走势」是走势行（`近 N 天券后价：最高 ¥X（起 至 止） 最低…`，括号里是这个价持续的日子）加 ` ```mermaid ` 折线图（xychart-beta，每次变价画成台阶，第一行 `%%{init…}%%` 按标签数加宽画布、设线色和纵轴留白，横轴写「9月10日」），「价格轨迹」是价格轨迹表（阶段 / 券后价 / 说明）；宿主优先原样保留 Mermaid，渲染不了再用轨迹表数据自己画曲线，都不能就只给走势行和轨迹表。历史价是收录以来的全部数据，与 App 历史价曲线一致
- Markdown 结果另在 `structuredContent` 附商品卡片（`schema` 为 `fenxiang.cards.v1`：标题、图、到手价、平台、店铺、链接、风险标签；历史价另有 `history.points` 变价点），支持卡片的宿主可直接渲染。JSON 结果的 `structuredContent` 就是 JSON 本身。
- JSON 结果只给模型用得上的字段：平台统一为中文名 `platform`；与到手价相同的 `goodsPrice`/`couponPrice`、值为 false 的风险标识（`officialShop`、`thirdPartyShop`、`overseasShop`、`priceSuspicious`、`requiresActivation` 等）不返回；不返回评分、置信度、分位、样本数和商品 ID。
- 响应头 `X-Request-Id` 是本次请求的 ID，反馈问题时带上便于查日志。
- 空结果带 `message`、`retryable`（`false` 表示别重试）和 `suggestedNextAction`（下一步怎么办）。
- 价格单位都是元，口径见文末。

## 工具

### buy_advice

单商品购买决策，**问值不值得买时首选**。结论与 App 省钱管家同一套购买建议引擎（历史价、全网同款最低价、大促节点）。

入参：`goodsUrl`（必填，商品链接、淘口令、分享文案原文，或从购物 App 复制的整段商品标题——会按标题找到那件商品，结果里 `matchedByTitle=true`）

关键出参：

- 结论：`conclusionText`（App 原话，如「💡 有更低价，建议换店买」）、`conclusionCode`、`recommendation`（`buy_now` / `switch_store` / `wait` / `watch`）、`adviceSource`（`brain` 为 App 引擎，`local` 为降级规则）
- 价格：`currentPrice`（当前商品到手价）、`goodsUrl`（当前商品的下单链接）、`governmentSubsidy`（未扣的国补，需资格；回答要点里给「如果能领国补」的有条件结论）、`historicalLow`、`historicalLowDate`、`average30`（历史价按券后价）
- 走势：`trendText`（文字走势行）；折线图和价格轨迹表只在 Markdown 的回答要点里
- 渠道：`bestPlatform` / `bestShop` / `bestPrice` / `bestGoodsUrl`（更便宜的稳妥渠道）、`safeOption`（官方/自营的稳妥选项）、`similarItems`（无同款时按标题找到的更便宜同款，需核对规格）
- 说明：`reasons`、`risks`、`nextAction`、`suggestedQuestions`
- 明细：`compareItems`（同款渠道，字段同 `compare_price`）、`savingPlan`（字段同 `saving_plan`）
- 商品：`itemTitle`、`shopName`、`brand`、`spec`、`itemPicUrl`

调用后不要再调 `history_price` / `compare_price` / `saving_plan`。

### batch_analyze

2–5 个商品逐个做与 `buy_advice` 同一套的决策。

入参：`goodsUrls`（必填，逗号或换行分隔，最多 5 个）

出参：`items`（每项是 `buy_advice` 的结构；失败的项带 `message`）、`summary`（带序号的表格：每件的结论、到手价、更省的渠道和链接）。

### compare_by_name

按型号、商品名或商品标题做全网同款比价，同款判定与 App 按名比价同一套。

入参：`productName`（必填）

关键出参：

- `matchLevel`：`EXACT` 同款；`SIMILAR` 只有相近款，差异在 `diff`
- `displayName`、`itemTitle`、`spec`
- `items`：各店报价（字段同 `compare_price` 的 `items`），按到手价升序
- 传整段商品标题时会同时按标题找商品：标准商品库没有同款，就用标题一致的商品出各平台报价（`notice` 说明是按标题找到的）
- 没有同款时：`relatedGoods` 是按名称搜到的在售商品（型号对得上、去掉配件，按到手价升序，商品字段同 `goods_search`），`notice` 说明「不是同款判定」；`suggestions` 只保留型号数字一致的候选款名
- 连 `relatedGoods` 都没有时按 `suggestedNextAction` 改用 `recommend_goods`，不要换关键词反复调

### recommend_goods

按购物需求推荐，与 App 省钱管家同一个推荐子 Agent。

入参：`userQuery`（必填，用户原话；上一轮澄清的回答拼进来）

关键出参：

- 需要澄清时：`clarifyText`、`clarifyQuestions`（`question` + `options`），此时 `groups` 为空
- 推荐时：`opening`、`groups`（`category`、`reason`、`items`，每组最多 10 款；商品字段同 `goods_search`）
- 都没有时：`reply`（追问或无结果说明）

### goods_search

按关键词列出在售商品。

入参：`keyword`（必填），可选 `platform`（`taobao` / `jd` / `vip` / `all`，默认 `all`；拼多多暂不支持）、`size`（默认 10，最大 20）、`minPrice`、`maxPrice`、`officialShop`

出参：`goodsList`，每项含 `goodsName`、`spec`、`finalPrice`（到手价）、`couponPrice`（与到手价不同时才有）、`platform`、`shopName`、`goodsPic`、`goodsUrl`，以及风险标识 `priceSuspicious`（价格异常）、`requiresActivation`（需领券/激活）、`thirdPartyShop`（第三方店铺）、`overseasShop`（海外/跨境，可能非国行），只在为 true 时出现；`suggestedQuestions` 是可追问的一个缺失条件。

全平台会分别搜淘宝、京东、唯品会再合并。明确型号查不到同款时，返回按名称搜到的在售商品（`matchLevel=RELATED`），并在 `notice` 里说明不是同款判定。

### history_price

单个商品收录以来的全部历史价格（券后价，与 App 历史价曲线同一份数据），只在用户明确要看曲线时用。

入参：`goodsUrl`（必填）

出参：`points`（变价点，`time` 为日期、`price` 为券后价，新的在前）、`trendText`（文字走势行；折线图和价格轨迹表只在 Markdown 的回答要点里）、`couponPrice`（当前券后价）、`finalPrice`（当前到手价）、`goodsUrl`（下单链接）、`priceType`、`governmentSubsidy`、商品摘要。走势和折线图已剔除异常定金/占位价，`points` 保留原始变价点。

### compare_price

按链接列出同款各渠道报价，只在用户明确要比价表时用。

入参：`goodsUrl`（必填）

出参：`items`，每项含 `platform`、`shopName`、`finalPrice`、`couponPrice`（与到手价不同时才有）、`sameItem`（同款同规格）、`currentItem`（就是用户这件）、`lowest`（全网最低）、`specText`、`specRelation`（同规格 / 规格不同 / 规格不全）、`officialShop`、`thirdPartyShop`、`overseasShop`、`governmentSubsidy`、`goodsUrl`；另有商品摘要。无同款时 `retryable=false`。

### saving_plan

按链接给出最省的买法，只在用户明确问"怎么买最省"时用。

入参：`goodsUrl`（必填）

出参：`planKind`（`switch_store` 换店 / `brain_plan` 平台省钱方案 / `direct` 直接买）、`referencePrice`（直接下单到手价）、`finalPrice`（方案价或换店后到手价）、`planName`、`conditionNote`（方案条件，如需 88VIP、凑单）、`stepBar`、`bestPlatform`、`bestShop`、`bestGoodsUrl`（下单链接：换店时是更便宜那家，其余是当前商品）、`estimatedSaving`（比直接买省多少）、`planUnavailable`（会员/凑单方案暂未算出，此时 `estimatedSaving` 为空，可稍后再查）、`steps`、`governmentSubsidy`、`historicalLow`。

## 价格口径

- `finalPrice` / `currentPrice`：到手价，直接下单的价格，已扣店铺券和平台优惠（立减、淘金币等）。
- `couponPrice`：券后价，只扣店铺券；历史价（`points`、`historicalLow`、`average30`）按券后价记录。
- 方案价：`saving_plan` / `savingPlan` 的 `finalPrice`（`planKind=brain_plan` 时），要满足 `conditionNote` 里的条件；和到手价一样不扣国补。
- `governmentSubsidy`：还没扣进到手价的国补，要所在地区有资格，单独说明。
- `priceType`：只在价格不是到手价时出现：`coupon_only` 只有券后价；`reference` 参考价。
- 不要提返利、返现、佣金。
