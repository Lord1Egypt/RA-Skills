# 生产型工厂 — 日报 Profile

> 适用于 `经营模式 = 工厂/生产型` 的用户。

## 核心指标（按经营阶段）

| 阶段 | 核心摘要列 | 选取理由 |
|------|-----------|--------|
| 起步 | GMV、UV、询盘数、转化率 | 刚起步需被看到，关注曝光→询盘链路 |
| 成长 | GMV、订单量、询盘转化率、客单价、老客占比 | 有单了，关注转化效率和客户质量 |
| 成熟 | GMV、订单量、客单价、复购率、广告ROI | 已稳定，关注利润和投入产出 |

> 各指标对应的 API 字段名和环比计算规则详见 `capabilities.md` 及 `SKILL.md`「报告生成规范·字段映射与环比」。

## 供应链条件分支

根据供应链字段做二次细分：

| 供应周期 | 起订量 | 子类型 | 额外关注指标 |
|---------|--------|--------|------------|
| 现货直发 | 一件代发/小批试单 | 零售型工厂 | 动销率、SKU 出单率 |
| 现货直发 | 批量走货 | 批发型工厂 | 大客户询盘、复购金额 |
| 深度定制 | 任意 | 定制型工厂 | 询盘数、询盘→成交周期、客单价 |

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

### 查询 1：商品动销率

- **触发条件**：供应周期 = 现货直发
- **data_source**：`SYCM`
- **api_path**：`portal/core/overview`
- **params**：`{"dataType":"RECENT_1"}`
- **关键字段**：`pullSalesItemCnt`（动销商品数）、`itemCnt`（商品总数）、`hasVisitorItemCnt`（有访客商品数）
- **解读**：动销率 = pullSalesItemCnt / itemCnt × 100%

### 查询 2：大客户询盘概况

- **触发条件**：起订量 = 批量走货
- **data_source**：`SYCM`
- **api_path**：`customer/inquiry/coreIndex`
- **params**：`{"dateType":"RECENT_1","indexCode":"effectiveInQUsers,effectInQCnt,factoryInQUsers,factoryPerfectInQUsers"}`
- **关键字段**：`effectiveInQUsers`（有效询盘用户数）、`effectInQCnt`（有效询盘量）、`factoryInQUsers`（找工厂询盘用户数）
- **解读**：大客户询盘 ≈ 找工厂询盘，批量型工厂重点关注

### 查询 3：广告花费明细

- **触发条件**：利润来源 = 薄利多销
- **多店铺模式跳过**：✅ `get_multi_shop_report` 已返回每店 `adReport`，多店铺模式下直接使用已有数据，无需重复查询
- **data_source**：`AD`
- **api_path**：`/ad/customer`
- **params**：`{"startDate":"{yesterday_yyyyMMdd}","endDate":"{yesterday_yyyyMMdd}"}`
- **关键字段**：消耗金额/元、成交金额、点击量、曝光量、计划名称
- **解读**：ROI = 成交金额 / 消耗金额；按计划汇总输出 TOP3 消耗计划
- **注意**：startDate/endDate 需 Agent 动态计算昨日日期（格式 yyyyMMdd）

## 异常阈值调整

| 阶段 | 异常判定阈值 | 说明 |
|------|------------|------|
| 起步 | ±30% | 数据基数小、波动大属正常，放宽阈值避免频繁报警 |
| 成长 | ±15% | 标准阈值 |
| 成熟 | ±8% | 体量大时微小变化即有意义，收紧阈值 |

## 行动建议方向

| 阶段 | 核心方向 | 对应技能 |
|------|---------|---------|
| 起步 | 被看到：优化标题、主图、关键词布局、开启基础广告 | `item-title-optimizer`、`item-image-optimizer`、广告建议 |
| 成长 | 转化提效：询盘跟进质量、详情页优化、广告 ROI | `inquiry-quality`、`product-analysis`、`shop-operate` |
| 成熟 | 利润效率：大客户维护、复购管理、供应链成本 | `customer-opportunity`、`shop-freedom-query-data` |

## 经营总览话术风格

- 起步：鼓励型 — "店铺处于起步阶段，今日 UV XX，关键是提升曝光..."
- 成长：分析型 — "店铺成长期，GMV 达 XX，转化率需关注..."
- 成熟：效率型 — "店铺经营稳定，重点关注利润效率和客户维护..."
