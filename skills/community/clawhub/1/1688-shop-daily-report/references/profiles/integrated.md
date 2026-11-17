# 工贸一体 — 日报 Profile（默认）

> 适用于 `经营模式 = 工贸一体` 或经营模式未知时的默认模板。
> 工贸一体兼具生产和销售，指标兼顾供应链效率和销售转化。

## 核心指标（按经营阶段）

| 阶段 | 核心摘要列 | 选取理由 |
|------|-----------|---------|
| 起步 | GMV、UV、询盘数、转化率 | 兼顾曝光和询盘，验证产品市场匹配 |
| 成长 | GMV、订单量、UV、转化率、客单价 | 产销两端并重，关注规模和效率 |
| 成熟 | GMV、订单量、客单价、广告ROI、老客占比 | 利润优先，兼顾增长和复购 |

> 各指标对应的 API 字段名和环比计算规则详见 `capabilities.md` 及 `SKILL.md`「报告生成规范·字段映射与环比」。

## 供应链条件分支

工贸一体按利润来源和供应周期做二次适配：

| 利润来源 | 供应周期 | 子类型 | 额外关注指标 |
|---------|---------|--------|------------|
| 薄利多销 | 现货直发 | 快周转型 | 动销率、订单量、物流时效 |
| 薄利多销 | 快速生产 | 敏捷型 | 订单量、产能利用率、交期 |
| 品牌溢价 | 任意 | 品牌型 | 客单价、复购率、品牌搜索量 |

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

### 查询 1：广告获客成本

- **触发条件**：利润来源 = 薄利多销
- **多店铺模式跳过**：✅ `get_multi_shop_report` 已返回每店 `adReport`，多店铺模式下直接使用已有数据，无需重复查询
- **data_source**：`AD`
- **api_path**：`/ad/customer`
- **params**：`{"startDate":"{yesterday_yyyyMMdd}","endDate":"{yesterday_yyyyMMdd}"}`
- **关键字段**：消耗金额/元、成交金额、点击量、广告访客数去重
- **解读**：获客成本 = 消耗金额 / 广告访客数去重；ROI = 成交金额 / 消耗金额
- **注意**：startDate/endDate 需 Agent 动态计算昨日日期（格式 yyyyMMdd）

### 查询 2：各渠道流量趋势

- **触发条件**：利润来源 = 薄利多销（与查询 1 同时触发）
- **data_source**：`SYCM`
- **api_path**：`portal/flowBoard/getFlowSourceTopV2`
- **params**：`{"dataType":"RECENT_1","device":"ALL","indexCode":"uv,crtByrCnt"}`
- **关键字段**：每条记录含 `outerId`（渠道ID）、`outerName`（渠道名）、`uv`（访客数）、`crtByrCnt`（下单买家数）
- **解读**：按 uv 降序输出 TOP5 流量渠道，含环比变化

### 查询 3：商品动销率

- **触发条件**：供应周期 = 现货直发
- **data_source**：`SYCM`
- **api_path**：`portal/core/overview`
- **params**：`{"dataType":"RECENT_1"}`
- **关键字段**：`pullSalesItemCnt`（动销商品数）、`itemCnt`（商品总数）
- **解读**：动销率 = pullSalesItemCnt / itemCnt × 100%

### 查询 4：跨境买家占比

- **触发条件**：目标客户含跨境
- **data_source**：`SYCM`
- **api_path**：`customer/businessScenario`
- **params**：`{"dateType":"RECENT_7","buyerType":"整体客户","page":1,"pageSize":10}`
- **关键字段**：`attributeValue`（场景名，包含“跨境”）、`payBuyerNum`（采购买家数）、`payBuyerNumRate`（占比）
- **解读**：找 attributeValue="跨境" 的记录，取占比和买家数

### 查询 5：大客户询盘概况

- **触发条件**：起订量 = 批量走货
- **data_source**：`SYCM`
- **api_path**：`customer/inquiry/coreIndex`
- **params**：`{"dateType":"RECENT_1","indexCode":"effectiveInQUsers,effectInQCnt,factoryInQUsers,factoryPerfectInQUsers"}`
- **关键字段**：`effectiveInQUsers`（有效询盘用户数）、`effectInQCnt`（有效询盘量）、`factoryInQUsers`（找工厂询盘用户数）
- **解读**：大客户询盘 ≈ 找工厂询盘，批量型商家重点关注

## 异常阈值调整

| 阶段 | 异常判定阈值 | 说明 |
|------|------------|------|
| 起步 | ±25% | 初期波动较大，放宽阈值 |
| 成长 | ±12% | 标准阈值 |
| 成熟 | ±8% | 体量稳定后收紧 |

## 行动建议方向

| 阶段 | 核心方向 | 对应技能 |
|------|---------|---------|
| 起步 | 产品力+曝光：标题主图优化、商品分析、基础广告 | `item-title-optimizer`、`item-image-optimizer`、`product-analysis` |
| 成长 | 转化+客户：询盘质量、客户跟进、广告精细化 | `inquiry-quality`、`customer-opportunity`、`shop-operate` |
| 成熟 | 效率+复购：客户维护、数据深度分析、供应链优化 | `customer-opportunity`、`shop-freedom-query-data` |

## 经营总览话术风格

- 起步：引导型 — "店铺起步中，今日 UV XX，询盘 XX 条，关键是提升产品曝光和详情转化..."
- 成长：均衡型 — "店铺稳步增长，GMV XX 元，订单 XX 单，产销两端运转正常..."
- 成熟：结果型 — "店铺经营稳健，GMV XX 元，重点关注利润效率和客户复购..."
