# 贸易型商家 — 日报 Profile

> 适用于 `经营模式 = 贸易商/分销商` 的用户。

## 核心指标（按经营阶段）

| 阶段 | 核心摘要列 | 选取理由 |
|------|-----------|---------|
| 起步 | GMV、UV、转化率、广告ROI | 贸易商不产货，核心是流量变现效率 |
| 成长 | GMV、订单量、转化率、广告ROI、客单价 | 有稳定出单，关注投产比和客户价值 |
| 成熟 | GMV、订单量、毛利率、复购率、广告ROI | 体量大了关注利润和客户黏性 |

> 各指标对应的 API 字段名和环比计算规则详见 `report-guide.md` 「核心指标字段映射表」。

## 供应链条件分支

贸易商供应链侧重在选品和库存管理：

| 利润来源 | 子类型 | 额外关注指标 |
|---------|--------|------------|
| 薄利多销/走量赚钱 | 走量型贸易 | UV、订单量、广告获客成本、动销率 |
| 品牌溢价/高客单 | 溢价型贸易 | 客单价、转化率、老客占比、复购金额 |

## 额外数据预查询

> 以下查询通过本技能内置的 `batch_query_profile_data` 命令批量并发执行，**不走 RAG**。
> dateType 统一使用 `RECENT_1`（日报场景取昨日数据），AD 接口用动态日期。
> **多店铺场景**：使用 `batch_query_profile_data --queries '<下方查询规格数组>' --shop_login_ids '<活跃店铺ID数组>'` 一次性并发查询。

**批量调用格式**：
```bash
python3 {baseDir}/cli.py batch_query_profile_data \
    --queries '<将下方触发条件命中的查询组装为 JSON 数组>' \
    --shop_login_ids '<活跃店铺 loginId 数组>'
```
> 单店铺时也可用 `query_shop_data` 单条调用。

### 查询 1：广告花费明细

- **触发条件**：利润来源 = 薄利多销
- **多店铺模式跳过**：✅ `get_multi_shop_report` 已返回每店 `adReport`，多店铺模式下直接使用已有数据，无需重复查询
- **data_source**：`AD`
- **api_path**：`/ad/customer`
- **params**：`{"startDate":"{yesterday_yyyyMMdd}","endDate":"{yesterday_yyyyMMdd}"}`
- **关键字段**：消耗金额/元、成交金额、点击量、曝光量、计划名称
- **解读**：ROI = 成交金额 / 消耗金额；按计划汇总输出消耗 TOP3
- **注意**：startDate/endDate 需 Agent 动态计算昨日日期（格式 yyyyMMdd）

### 查询 2：客户层级分布

- **触发条件**：利润来源 = 品牌溢价
- **data_source**：`SYCM`
- **api_path**：`customer/layerAnalysis`
- **params**：`{"dateType":"RECENT_7"}`
- **关键字段**：`overallCustomerNum`（整体客户规模）、`importOldCustomerNum`（重点老客户数）、`newCustomerNum`（新客户数）、`payBuyerNum`（采购买家数）
- **解读**：高价值客户数 ≈ importOldCustomerNum；新老客占比反映客户结构健康度

### 查询 3：跨境买家占比

- **触发条件**：目标客户含跨境
- **data_source**：`SYCM`
- **api_path**：`customer/businessScenario`
- **params**：`{"dateType":"RECENT_7","buyerType":"整体客户","page":1,"pageSize":10}`
- **关键字段**：`attributeValue`（场景名，包含“跨境”）、`payBuyerNum`（该场景采购买家数）、`payBuyerNumRate`（占比）
- **解读**：找 attributeValue="跨境" 的记录，取 payBuyerNum 和 payBuyerNumRate

## 异常阈值调整

| 阶段 | 异常判定阈值 | 说明 |
|------|------------|------|
| 起步 | ±25% | 贸易商灵活度高，初期波动合理 |
| 成长 | ±12% | 略高于工厂（选品更换频繁） |
| 成熟 | ±8% | 体量稳定后收紧监控 |

## 行动建议方向

| 阶段 | 核心方向 | 对应技能 |
|------|---------|---------|
| 起步 | 选品+引流：找爆款潜力款、优化标题主图、快速起量 | `item-select`、`item-title-optimizer`、`item-image-optimizer` |
| 成长 | 投产效率：广告精细化、询盘跟进、转化率提升 | `inquiry-quality`、`product-analysis`、广告优化建议 |
| 成熟 | 客户经营：复购激活、客户分层维护、利润管理 | `customer-opportunity`、`customer-batch-upload` |

## 经营总览话术风格

- 起步：激励型 — "店铺处于引流期，今日 UV XX，广告 ROI XX，重点提升流量转化..."
- 成长：ROI导向 — "店铺增长期，GMV XX 元，广告投产比 XX，建议优化..."
- 成熟：利润导向 — "店铺经营成熟，关注毛利率和客户复购..."
