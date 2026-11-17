# 数据采集字段清单（对应 SKILL.md §三②「一次性收数」）

> 原则：动手前先按任务类型列齐字段，**一次性问清**，缺关键字段写 `DATA_MISSING`，禁止用行业均值/经验值填补（R1）。
> 每个字段都要带「来源 + 统计区间」，例如「抖音罗盘，2026-08-01~08-31，支付买家数」。

## 一、定价 / 真实利润（→ profit_roi.py）

| 字段 | 必填 | 说明 |
|---|---|---|
| 售价（到手价/实收单价） | ✅ | 不含运费的净成交价 |
| 商品成本（含头程/采购） | ✅ | 单件到仓成本 |
| 履约物流成本 | 建议 | 单件发货+仓储 |
| 其他变动成本 | 选填 | 包装/售后耗材 |
| 平台佣金率 | ✅ | 见 commission-rates.md，按真实类目 |
| 支付通道费率 | 建议 | 通常 0.6% |
| 退货率 | 建议 | 近 30 天真实退货率 |
| 单均退货损失 | 选填 | 往返运费 + 不可售损失 |
| 单件固定成本分摊 | 选填 | 固定成本 ÷ 预计销量 |
| 单件广告费（实测） | 选填 | 投放实测值，优于预估 |
| 单件达人佣金+坑位分摊 | 选填 | 达人分销场景必填 |
| 单件商家补贴 | 选填 | 平台/店铺补贴承担部分 |
| 目标净利率 | 选填 | 默认 0 |
| 转化率（支付买家数/访客） | 选填 | 投投放测算用 |
| 点击率 | 选填 | CPM 测算用 |
| 平均点击花费 CPC | 选填 | 出价测算用 |

## 二、结算单对账（→ settlement_audit.py）

- `summary`：销售额、佣金、退款、净结算（整单合计）
- `rows[]`：order_id、gmv、commission、refund、fee_ad、fee_other、koll_fee、slot_fee、net_settlement、return_deduction、deduction_expected
- `live_deals[]`：anchor、date、gmv、commission、slot_fee
- `subsidies[]`：amount、order_date、settle_date
- `rebate`：framework_target、actual_spend、claimed_rebate_rate、tiers[{spend,rate}]

## 三、漏斗诊断（→ funnel_diagnose.py）

| 字段 | 必填 | 说明 |
|---|---|---|
| 访客数 visits | ✅ | 与支付买家数同源 |
| 支付买家数 pay_buyers | ✅ | 无则用支付订单数（须标注口径） |
| 曝光 impressions | 选填 | 算 CTR |
| 点击 clicks | 选填 | 算 CTR/CPC |
| 加购 add_cart | 选填 | 算加购率 |
| 订单 orders | 选填 | 算下单支付率 |
| GMV | 选填 | 算客单价/ROAS |
| 广告花费 ad_spend | 选填 | 算 CPC/ROAS |
| 保本 ROAS | 选填 | 来自 profit_roi，用于亏损判定 |
| prev（上期数据） | 选填 | 用于环比下滑诊断 |

## 四、选品评估（→ selection_eval.py）

- name（必填）、market_level、competition_level、gross_margin、return_rate、compliance_level、content_level（0–100 评估或真实比例）
- competitors[]（选填）：name、price、monthly_sales、edge、weak

## 五、备货计划（→ stocking_plan.py）

- avg_daily_sales、lead_time_days、unit_cost（必填）
- safety_factor（默认 1.5）、existing_stock、in_transit_stock、target_days（默认 30）
- cash_inflow_60d（红线校验用）、is_promo（大促模式）

## 六、文案合规（→ copy_compliance.py）

- 待检文案文本或文件 + 平台标识（tb/tmall/jd/pdd/douyin/xhs/ks/wx）
- 仅审核，不需要数值数据；撰写阶段按 copy-playbook.md 骨架产出
