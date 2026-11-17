# Offer Snapshot v2 字段规范

> 本文使用中文维护，但 Skill 输出必须跟随用户当前使用或明确选择的语言。所有地区、币种、税费与渠道字段均可配置；本文不限定中国大陆市场。

## 1. 设计原则

Offer Snapshot 是有时间边界、可追溯、可降级的报价集合。它只描述当前样本，不代表全网或长期最低价。未知不是零，历史不等于当前，赠品净值不等于现金优惠。

## 2. 顶层结构

```json
{
  "schema_version": "2.0",
  "model": "offer_snapshot",
  "case_id": "generic-stable-id",
  "snapshot": {},
  "normalized_product": {},
  "user_requirements": {},
  "formula_policy": {},
  "evidence_grade_policy": {},
  "offers": [],
  "comparison": {},
  "decision": {},
  "evidence": []
}
```

- `case_id` 是不含姓名、账号、订单号等私人数据的稳定类型标识，不记录一次性查询结果。
- `snapshot` 必含 `captured_at`、`freshness`、`freshness_note`、`currency`、`region`。
- `normalized_product` 必含品牌、商品名、规格、版本和 `comparison_unit`。
- `offers` 至少包含两个候选项；当前、历史和线索可同时存在，但只有合格当前报价参与计算。

## 3. Offer 字段

每个 offer 至少包含：

| 字段 | 类型 | 规则 |
| --- | --- | --- |
| `offer_id` | string | 快照内唯一 |
| `period` | enum | `current` 或 `history` |
| `event_year` | integer/null | 历史报价必填 |
| `channel` | string | 渠道描述，不含用户账号 |
| `product_match` | enum | `exact`、`claimed_exact`、`mismatch` |
| `offer_type` | enum | `single`、`bundle`、`multi_pack` |
| `display_price` | number/null | 页面展示总价 |
| `confirmed_discount` | number/null | 已确认可用优惠 |
| `mandatory_cost` | number/null | 运费、税费等必要成本 |
| `cash_landed_price` | number/null | 按现金公式计算 |
| `bundle` | object/null | 套装组成与分摊信息 |
| `gift` | object | 赠品结构与净值 |
| `net_effective_cost` | number/null | 按赠品公式计算 |
| `evidence_refs` | string[] | 非空且能回链 |
| `evidence_grade` | enum | A、B、C、D |
| `price_comparison_eligible` | boolean | 是否进入现金比较 |
| `purchase_recommendation_eligible` | boolean | 是否可支持渠道推荐 |
| `exclusion_reasons` | string[] | 降级或排除原因 |

## 4. 公式与空值

### 4.1 现金到手价

```text
cash_landed_price = display_price - confirmed_discount + mandatory_cost
```

三个输入必须都是非负数。任一未知则结果为 `null`，且 `price_comparison_eligible = false`。

### 4.2 套装分摊

```text
bundle_reference_value_total = sum(component.reference_value * component.quantity)
required_item_reference_value = sum(required component.reference_value * component.quantity)
required_item_allocated_cost = cash_landed_price * required_item_reference_value / bundle_reference_value_total
```

仅当全部组成、数量和同口径参考价值可核验，且总参考价值大于零时计算。分摊用于理解成本，不把用户不需要的商品假定为可按原价变现。

### 4.3 赠品净值

```text
gift_net_value = sum(reference_value * quantity * realization_rate)
net_effective_cost = cash_landed_price - gift_net_value
```

`realization_rate` 范围为 0 到 1。赠品 SKU、数量、条件、参考价值或折算率任一未知时，`composition_known = false`，两个净值字段均为 `null`。

### 4.4 价差

```text
gap_amount = reference_cash_landed_price - candidate_cash_landed_price
gap_rate = gap_amount / reference_cash_landed_price
```

参考价必须大于零，两端必须同币种、同地区、同商品口径且均达到最低证据等级。金额建议保留两位小数，比例内部保留至少六位，展示时再格式化。

## 5. 证据结构

每条 evidence 包含：`evidence_id`、`source_type`、`grade`、`title`、`url`、`captured_at`、`supports`、`limitations`。

- A：一手商品、活动及结算条件完整。
- B：一手页面但关键条件有缺口。
- C：搜索片段、聚合页或二手内容，只作线索。
- D：历史回顾、用户内容或上下文严重缺失。

offer 的 `evidence_grade` 应取其关键主张所依赖证据中的最低等级，不能用一条高等级证据掩盖关键字段的低等级来源。

## 6. 资格规则

`price_comparison_eligible = true` 必须同时满足：

1. `period = current`；
2. `product_match = exact`；
3. `evidence_grade` 至少为 B；
4. 现金公式输入完整且结果正确；
5. 币种、地区与比较单位一致。

`purchase_recommendation_eligible = true` 还要求 A 级证据，并确认库存、主体、发票、批次、有效期、退换规则及用户约束。

历史 offer 必须有年份并退出当前比较。C/D 级线索可以展示，但不能影响排名或推荐。

## 7. 决策规则

`decision.result` 只允许：

- `建议采购`：至少一个 offer 可支持购买推荐，且用户约束满足；
- `有条件采购`：存在现金可比报价，但仍需确认关键结算或履约字段；
- `不建议采购`：无可比报价，或已知风险/约束不满足。

`recommended_offer_id` 在没有 A 级合格报价时必须为 `null`。结论必须附 `limitations` 与 `next_checks`。

## 8. 失败协议

- 时间未知：`freshness = unresolved`，禁止实时表述。
- 商品不一致：标记 `mismatch` 并排除。
- 成本未知：现金到手价为 `null` 并排除。
- 赠品未知：只比较现金价。
- 套装不可拆：只展示整套价格。
- 历史或低等级线索：保留背景，不参与当前排名。
- 证据不足：降低结论强度，不补造字段。
