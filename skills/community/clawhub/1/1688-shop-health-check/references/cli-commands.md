# CLI 命令详细字段说明

本文档包含 1688-shop-health-check 所有 CLI 命令的详细参数和字段说明。Agent 在调用具体命令前按需读取对应章节。

所有命令均通过 `python3 {baseDir}/cli.py <command> [options]` 调用，输出统一为：
```json
{"success": bool, "markdown": str, "data": {...}}
```

---

## 1. `seller_trade_code_index` — 店铺交易核心指标（总盘）

```bash
python3 {baseDir}/cli.py seller_trade_code_index [--date_type <DATE_TYPE>] [--device <DEVICE>]
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

## 2. `seller_import_abnormal_offer` — 异常商品（风险定位）

```bash
python3 {baseDir}/cli.py seller_import_abnormal_offer [--date_type <DATE_TYPE>] [--device <DEVICE>]
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

## 3. `seller_top_offer` — 优秀商品榜单（多榜单）

```bash
python3 {baseDir}/cli.py seller_top_offer [--order_by <ORDER_BY>] [--range_type <RANGE_TYPE>] [--device <DEVICE>] [--page_size <N>]
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

## 4. `seller_activity_registered_info` — 活动参与及效果

```bash
python3 {baseDir}/cli.py seller_activity_registered_info
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

## 5. `seller_customer_business_province` — 客户地域分布

```bash
python3 {baseDir}/cli.py seller_customer_business_province [--date_type <DATE_TYPE>] [--page_size <N>]
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

## 6. `seller_customer_detail` — 头部老客户明细

```bash
python3 {baseDir}/cli.py seller_customer_detail [--date_type <DATE_TYPE>] [--buyer_type <TYPE>] [--order_by <ORDER_BY>] [--page_size <N>]
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

## 7. `get_traffic_trend` — 逐日流量趋势数据

```bash
python3 {baseDir}/cli.py get_traffic_trend --query_date <QUERY_DATE> [--days <DAYS>]
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

## 8. `get_core_metrics` — 店铺核心指标同行对比及趋势数据

```bash
python3 {baseDir}/cli.py get_core_metrics [--date_type <DATE_TYPE>]
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

## 9. `configure` — 配置 AK

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
