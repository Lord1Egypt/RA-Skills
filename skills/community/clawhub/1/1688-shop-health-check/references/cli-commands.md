# CLI 命令详细字段说明

本文档包含 1688-shop-health-check 所有 CLI 命令的详细参数和字段说明。Agent 在调用具体命令前按需读取对应章节。

所有命令均通过 `python3 {baseDir}/cli.py <command> [options]` 调用，输出统一为：
```json
{"success": bool, "markdown": str, "data": {...}}
```

### 通用参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--NEWTON_SHOP_LOGIN_ID` | 否 | 店铺登录ID（值为 `get_bindlist` 返回的对应店铺 `loginId`），用于指定查询的店铺。Agent 单独调用单店铺命令查询非当前 AK 默认店铺时必须传入。不传时使用当前 AK 对应的默认店铺 |

---

## 1. `alibaba.1688.seller.trade.code.index` — 店铺交易核心指标（总盘）

```bash
python3 {baseDir}/cli.py alibaba.1688.seller.trade.code.index [--date_type <DATE_TYPE>] [--device <DEVICE>] [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：总盘分析**第一优先级接口**，判断店铺整体健康度、规模、效率、质量、新老客结构和下单到支付衔接情况。

**关键字段**：

| 字段 | 含义 | 用途 |
|------|------|------|
| `payAmt` | 支付金额 | 成交规模 |
| `payByrCnt` | 支付买家数 | 买家规模 |
| `payRate` | 支付转化率 | 转化效率 |
| `payMordCnt` | 支付订单数 | 订单规模 |
| `payItemCnt` | 支付商品款数 | 在售活跃款数 |
| `payItemQty` | 支付商品数量 | 件数规模 |
| `perByrAmt` | 人均支付金额 | 客单表现 |
| `payToOnRate` | 下单到支付转化效率 | 支付承接效率 |
| `payNewByrCnt` | 新支付买家数 | 拉新能力 |
| `payOldByrCnt` | 老支付买家数 | 复购能力 |
| `oldPayByrAmt` | 老买家支付金额 | 老客贡献 |
| `rfdSucAmt` | 退款成功金额 | 成交质量风险 |
| `crtOrdAmt` | 创建订单金额 | 下单规模 |
| `crtByrCnt` | 创建订单买家数 | 下单买家规模 |
| `crtOrdItmQty` | 创建订单商品数量 | 下单件数 |
| `cycleCrc` | 环比变化率 | 趋势方向（可能为负） |
| `cycleCqc` | 环比变化绝对值 | 趋势幅度 |

---

## 2. `alibaba.1688.seller.import.abnormal.offer` — 异常商品（风险定位）

```bash
python3 {baseDir}/cli.py alibaba.1688.seller.import.abnormal.offer [--date_type <DATE_TYPE>] [--device <DEVICE>] [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：风险定位**关键接口**，判断问题主要来自流量、转化还是同时恶化，识别对店铺拖累最大的异常商品。

**关键字段**：

| 字段 | 含义 |
|------|------|
| `reason` | 异常原因，如"访客下跌"/"支付下跌"/"访客下跌, 支付下跌" |
| `itemId` | 商品ID |
| `offerTitle` | 商品标题 |
| `categoryId` | 类目ID |
| `offerImageUrl` | 商品图 |
| `link` | 异常详情跳转链接 |
| `abnormalProduct` | 是否异常商品 |
| `valueMap.uv.value` | 当前访客数 |
| `valueMap.uv.cycleCrc` | 访客变化率 |
| `valueMap.uv.cycleCqc` | 访客变化值 |
| `valueMap.payAmt.value.value` | 当前支付金额 |
| `valueMap.payAmt.cycleCrc.value` | 支付金额变化率 |
| `valueMap.payAmt.cycleCqc.value` | 支付金额变化值 |

---

## 3. `alibaba.1688.seller.top.offer` — 优秀商品榜单（多榜单）

```bash
python3 {baseDir}/cli.py alibaba.1688.seller.top.offer [--order_by <ORDER_BY>] [--date_type <DATE_TYPE> | --range_type <RANGE_TYPE>] [--device <DEVICE>] [--order <desc|asc>] [--page <N>] [--page_size <N>] [--index_code <INDEX_CODE>] [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**⚠️ 重要约束**：本接口**必须按需多次调用**，单次只能拉取一种榜单。

**`order_by` 枚举**：

| 值 | 榜单类型 | 用途 |
|------|----------|------|
| `payAmt` | 支付榜（默认） | 成交主力商品 |
| `uv` | 访客榜 | 流量主力商品 |
| `payNewByrCnt` | 拉新榜 | 拉新主力商品 |
| `itemMultiByrCnt` | 复购榜 | 复购主力商品 |

**`range_type` 仅支持** `RECENT_7` / `RECENT_30`。

**关键字段**：

| 字段 | 含义 |
|------|------|
| `item.offerTitle` / `item.offerId` / `item.detailUrl` / `item.categoryID` | 商品基础信息 |
| `revealCnt` | 曝光数 |
| `uv` | 访客数 |
| `payByrCnt` | 支付买家数 |
| `payRate` | 支付转化率 |
| `payAmt` | 支付金额 |
| `payItemQty` | 支付件数 |
| `payNewByrCnt` | 新支付买家数 |
| `payOldByrCnt` | 老支付买家数 |
| `itemMultiByrCnt` | 复购买家数 |
| `itemMultiByrPayAmt` | 复购支付金额 |

---

## 4. `alibaba.1688.seller.activity.registered.info` — 活动参与及效果

```bash
python3 {baseDir}/cli.py alibaba.1688.seller.activity.registered.info [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：分析活动是否有效，是否带来流量、订单和 GMV，是否优于同行基准，是否存在"有曝光无成交"或"高产出活动可复制"。

> **⚠️ 注意**：本接口数据为**近 30 天活动**口径，不完全等同于当前分析周期，需在结论中说明。

**关键字段**：

| 字段 | 含义 |
|------|------|
| `activityName` / `activityId` | 活动信息 |
| `cateLevel1Name` | 一级类目 |
| `startTime` / `endTime` | 活动时间 |
| `activityItmVisitorUv` / `activityItmVisitorPv` | 活动商品访客 UV/PV |
| `activityItmOrderCnt` | 活动商品订单数 |
| `activityItmTakeCnt` | 活动商品领取/参与次数 |
| `activityItmGmv` | 活动商品 GMV |
| `peerActivityItmVisitorPv` | 同行活动 PV（基准） |
| `peerActivityItmGmv` | 同行活动 GMV（基准） |
| `rank` | 活动排名（可能无效） |

---

## 5. `alibaba.1688.seller.customer.business.province` — 客户地域分布

```bash
python3 {baseDir}/cli.py alibaba.1688.seller.customer.business.province [--date_type <DATE_TYPE>] [--page_size <N>] [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：分析客户地域集中度、核心区域依赖、区域覆盖面、潜在扩展区域。

**关键字段**：

| 字段 | 含义 |
|------|------|
| `attributeValue` | 地域名称（省份） |
| `payBuyerNum` | 该地域支付买家数 |
| `payBuyerNumRate` | 该地域支付买家数占比 |
| `recordCount` | 记录数 |

---

## 6. `alibaba.1688.seller.customer.detail` — 头部老客户明细

```bash
python3 {baseDir}/cli.py alibaba.1688.seller.customer.detail [--date_type <DATE_TYPE>] [--buyer_type <TYPE>] [--order_by <ORDER_BY>] [--page_size <N>] [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：分析店铺是否依赖少数头部老客户，头部老客是否持续活跃，复购盘是否稳固，是否存在高价值客户近期走弱风险。

**关键字段**：

| 字段 | 含义 |
|------|------|
| `identityName` | 客户身份/画像 |
| `companyName` | 公司名 |
| `custAreaName` | 客户地域 |
| `buyerLoginId` | 买家标识 |
| `payAmount` | **本周期**支付金额 |
| `payAmtAll` | **累计**支付金额（看历史价值） |
| `lastPayDate` | 最近支付日期（看活跃度） |
| `firstPayDate` | 首次支付日期 |
| `fstFromAd` | 是否首次来自广告（自然 vs 广告获客） |
| `buyerType` | 买家类型 |
| `payParentOrderNum` | 支付父订单数 |
| `buyerCreditLevel` | 信用等级 |
| `lstLossDate` | 最近流失日期（可能为空） |

---

## 7. `alibaba.1688.get.traffic.trend` — 逐日流量趋势数据

```bash
python3 {baseDir}/cli.py alibaba.1688.get.traffic.trend --query_date <QUERY_DATE> [--days <DAYS>] [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：获取逐日流量趋势数据，用于分析流量波动趋势、识别异常波动、判断流量健康度。

**⚠️ 重要约束**：
- `query_date` 必须传入**昨日日期**（格式：YYYY-MM-DD）
- `days` 仅支持 7 或 30，表示近 7 天或近 30 天的数据

**关键字段**（返回数组中每项包含）：

| 字段 | 含义 |
|------|------|
| `uv` | 访客数 |
| `pv` | 浏览量 |
| `UVCTR` | UV 点击率 |
| `日期` | 日期（格式：YYYYMMDD） |

---

## 8. `alibaba.1688.get.core.metrics` — 店铺核心指标同行对比及趋势数据

```bash
python3 {baseDir}/cli.py alibaba.1688.get.core.metrics [--date_type <DATE_TYPE>] [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：获取店铺核心指标的同行对比数据及趋势数据，用于判断店铺在行业中的位置、指标健康度、增长趋势。

**⚠️ 重要约束**：
- `date_type` 仅支持 `RECENT_7` 或 `RECENT_30`
- 接口返回的 `data` 是 JSON 字符串，包含 `core_metrics`（同行对比）和 `trend`（趋势数据）

**关键字段（core_metrics 数组中每项包含）**：

| 字段 | 含义 |
|------|------|
| `metric_name` | 指标名称（展现次数/访客数/浏览量/点击转化率/支付转化率/支付买家数/支付金额） |
| `metric_code` | 指标代码（impression/visitor/page_view/click_cvr/pay_cvr/buyer_count/pay_amount） |
| `my_value` | 本店数值 |
| `peer_avg` | 同行同层均值 |
| `ratio_to_peer` | 本店/同行同层均值（达标率） |
| `rating` | 评级（优秀/持平/略低/极低） |

**关键字段（trend 对象中每项包含）**：

| 字段 | 含义 |
|------|------|
| `value` | 当前值 |
| `year_on_year` | 同比变化率（本月 vs 去年同一月） |
| `week_on_week` | 环比变化率（本周 vs 上周 / 本月 vs 上月） |
| `vs_peer_avg` | 本店变化率 vs 同行平均变化率 |
| `vs_peer_good` | 本店变化率 vs 同行优秀变化率 |

**趋势字段判断提示**：
- `vs_peer_avg` > 1 表示本店变化优于同行平均
- `vs_peer_good` > 1 表示本店变化优于同行优秀

**关键字段（date_range 对象）**：

| 字段 | 含义 |
|------|------|
| `start_date` | 开始日期 |
| `end_date` | 结束日期 |

---

## 9. `shop_health_check` — 店铺健康检查（订单履约/合规扣分/买家评价）

```bash
python3 {baseDir}/cli.py shop_health_check --code <order_risk|shop_punish|feedback> [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：店铺健康检查聚合工具，单命令通过 `--code` 路由到三个模块。`order_risk`（订单履约）与 `feedback`（买家评价）服务**成交维度**，`shop_punish`（合规扣分）服务**风险维度**。仅透传后端业务数据，Agent 侧自行加工。

**参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--code` | 是 | 模块编码，枚举 `order_risk` / `shop_punish` / `feedback` |
| `--NEWTON_SHOP_LOGIN_ID` | 否 | 目标店铺 loginId，多店铺查询时传入 |

> **口径说明**：本工具返回为**实时快照**，非近 7/30 天周期口径，结论与报告中需区分标注。

### 9.1 `--code order_risk`（订单履约）

返回 `data` 结构：

| 字段 | 含义 |
|------|------|
| `overview.pending_ship_cnt` | 待发货订单数 |
| `overview.pending_payment_cnt` | 待付款订单数 |
| `overview.pending_receive_cnt` | 待收货订单数 |
| `overview.pending_custom_payment_cnt` | 待处理定制付款订单数 |
| `timeout_risk.about_to_timeout_cnt` | 即将发货超时订单数 |
| `timeout_risk.already_timeout_cnt` | 已发货超时订单数 |
| `timeout_risk.about_to_timeout_orders` | 即将超时订单 Top5（按剩余时长升序） |
| `timeout_risk.already_timeout_orders` | 已超时订单 Top5（按超时时长降序） |

每条订单明细字段：

| 字段 | 含义 |
|------|------|
| `order_id` | 订单号 |
| `product_name` | 首个商品名（截断 30 字） |
| `amount_yuan` | 订单金额（元，字符串） |
| `send_hour` | 承诺发货时长 |
| `left_time` | 距发货截止剩余时效（仅即将超时订单） |
| `overdue_time` | 已超时时长（仅已超时订单） |

### 9.2 `--code shop_punish`（合规扣分）

返回 `data` 结构：

| 字段 | 含义 |
|------|------|
| `punish_score` | 违规扣分 |
| `fake_times` | 假货次数 |
| `punish_warning.cnt` | 违规预警总数 |
| `punish_warning.new_cnt` | 新增违规数 |
| `punish_warning.deal_url` | 处理链接 |
| `punish_warning.list` | 待处理违规明细（仅 PENDING，按 `punish_time` 倒序） |
| `item_alert.cnt` | 商品预警数 |
| `item_alert.list` | 商品预警明细 |
| `legal_alert.cnt` | 司法预警数 |
| `legal_alert.admin_case` | 行政案件数 |
| `legal_alert.law_case` | 司法案件数 |
| `legal_alert.deal_url` | 处理链接 |

`punish_warning.list` 每项：`punish_id` / `rule_type`（违规规则类型） / `punish_status` / `punish_time` / `is_new` / `deal_url`。

`item_alert.list` 每项：`item_id` / `item_title` / `risk_lev1_name`（一级风险） / `risk_lev2_name`（二级风险） / `warning_left_time`（预警剩余时长） / `deal_url`。

### 9.3 `--code feedback`（买家评价）

返回 `data` 结构：

| 字段 | 含义 |
|------|------|
| `rating_overview.total_cnt` | 评价总数 |
| `rating_overview.distribution` | 1~5 分档分布，每项 `rate`（分档） / `cnt`（数量） |
| `rating_overview.low_score_cnt` | 低分（≤3 分）数量 |
| `rating_overview.low_score_ratio` | 低分占比（百分比字符串，如 `12.50%`） |
| `negative_feedback.cnt` | 负面反馈数 |
| `negative_feedback.items` | 负面反馈明细，每项 `item_name`（商品名） / `feedback`（反馈内容） |
| `positive_cnt` | 正面反馈数 |

---

## 10. `alibaba.1688.get.traffic.overview` — 全店流量概览

```bash
python3 {baseDir}/cli.py alibaba.1688.get.traffic.overview --query_date <QUERY_DATE> [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：获取全店流量概览数据（访客规模、流量总览），服务**流量维度**，与 `alibaba.1688.get.channel.traffic` 配合完成全店流量构成分析。

**参数**：`--query_date` 必填，传**昨日日期**（格式 YYYY-MM-DD）；`--NEWTON_SHOP_LOGIN_ID` 可选。

> 接口透传后端业务数据（`data`），字段结构随接口返回，Agent 侧自行解析。

---

## 11. `alibaba.1688.get.channel.traffic` — 各渠道流量

```bash
python3 {baseDir}/cli.py alibaba.1688.get.channel.traffic --query_date <QUERY_DATE> [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：获取各渠道流量数据（搜索 / 推荐 / 广告等渠道构成与占比），服务**流量维度**。根据渠道占比决定后续下钻方向。

**参数**：`--query_date` 必填，传**昨日日期**（格式 YYYY-MM-DD）；`--NEWTON_SHOP_LOGIN_ID` 可选。

> 接口透传后端业务数据（`data`），字段结构随接口返回。

---

## 12. `alibaba.1688.get.search.channel.detail` — 搜索渠道深度下钻

```bash
python3 {baseDir}/cli.py alibaba.1688.get.search.channel.detail --query_date <QUERY_DATE> [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：搜索渠道深度下钻，分析搜索流量来源与转化承接，服务**流量维度**。建议在 `alibaba.1688.get.channel.traffic` 确认搜索占比较高时下钻。

**参数**：`--query_date` 必填，传**昨日日期**（格式 YYYY-MM-DD）；`--NEWTON_SHOP_LOGIN_ID` 可选。

> 接口透传后端业务数据（`data`），字段结构随接口返回。

---

## 13. `alibaba.1688.get.recommend.channel.detail` — 推荐渠道深度下钻

```bash
python3 {baseDir}/cli.py alibaba.1688.get.recommend.channel.detail --query_date <QUERY_DATE> [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：推荐渠道深度下钻，分析推荐流量来源与承接，服务**流量维度**。建议在推荐占比较高时下钻。

**参数**：`--query_date` 必填，传**昨日日期**（格式 YYYY-MM-DD）；`--NEWTON_SHOP_LOGIN_ID` 可选。

> 接口透传后端业务数据（`data`），字段结构随接口返回。

---

## 14. `alibaba.1688.get.ad.channel.detail` — 广告渠道深度下钻

```bash
python3 {baseDir}/cli.py alibaba.1688.get.ad.channel.detail --query_date <QUERY_DATE> [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：广告渠道深度下钻，分析广告渠道流量与转化。**流量维度与广告维度共享**（两维度任一需要时均调用一次即可）。

**参数**：`--query_date` 必填，传**昨日日期**（格式 YYYY-MM-DD）；`--NEWTON_SHOP_LOGIN_ID` 可选。

> 接口透传后端业务数据（`data`），字段结构随接口返回。

---

## 15. `alibaba.1688.get.product.status` — 商品状态检查

```bash
python3 {baseDir}/cli.py alibaba.1688.get.product.status --query_date <QUERY_DATE> [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：检查商品搜索降权 / 下架等状态，服务**商品维度**。可与异常商品、优秀商品榜单交叉验证。

**参数**：`--query_date` 必填，传**昨日日期**（格式 YYYY-MM-DD）；`--NEWTON_SHOP_LOGIN_ID` 可选。

> 接口透传后端业务数据（`data`），字段结构随接口返回。

---

## 16. `alibaba.1688.get.industry.benchmark` — 行业大盘对比数据

```bash
python3 {baseDir}/cli.py alibaba.1688.get.industry.benchmark --query_date <QUERY_DATE> [--NEWTON_SHOP_LOGIN_ID <LOGIN_ID>]
```

**用途**：行业大盘对比数据查询，用于将本店表现与行业大盘对比，服务**广告维度**。

**参数**：`--query_date` 必填，传**昨日日期**（格式 YYYY-MM-DD）；`--NEWTON_SHOP_LOGIN_ID` 可选。

> 接口透传后端业务数据（`data`），字段结构随接口返回。

---

## 17. `get_bindlist` — 多店铺绑定关系列表

```bash
python3 {baseDir}/cli.py get_bindlist
```

**用途**：获取当前用户的多店铺绑定关系列表，是**多店铺批量体检的入口** —— 先取绑定列表，再对每个 `loginId` 逐店传 `--NEWTON_SHOP_LOGIN_ID` 诊断。

**参数**：无（仅需已配置 AK）。

**关键字段**（`data` 为绑定店铺数组，每项包含）：

| 字段 | 含义 |
|------|------|
| `companyName` | 店铺公司名 |
| `loginId` | 店铺登录 ID（用作其他单店铺命令的 `--NEWTON_SHOP_LOGIN_ID` 参数值） |
| `userId` | 用户 ID |
| `isOwner` | 是否为店铺负责人 |

---

## 18. `configure` — 配置 AK

```bash
python3 {baseDir}/cli.py configure [YOUR_AK]
```

**用途**：配置 1688 API 的 AccessKey，用于后续所有接口的鉴权签名。

**使用方式**：

| 命令 | 行为 |
|------|------|
| `python3 {baseDir}/cli.py configure YOUR_AK` | 写入 AK 到本地配置 |
| `python3 {baseDir}/cli.py configure` | 查看当前 AK 配置状态 |

> **注意**：首次使用前必须配置 AK，否则所有只读接口将返回 `success: false` 和 "AK 未配置" 错误。
