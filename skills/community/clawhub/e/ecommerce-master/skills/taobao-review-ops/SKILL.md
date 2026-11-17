---
name: taobao-review-ops
description: 淘宝评价维护：traderate API 面（评价回复/列表）、差评应对策略、DSR 店铺分维护
source:
  type: external
  url: https://open.taobao.com/api.htm?spm=a219a.7386797.0.0&docType=2&docId=826
  version: "1.0.0"
  updated: 2026-10-29
metadata:
  category: 淘宝运营
  platform: API
  difficulty: 入门
---

# 淘宝评价维护（Taobao Review Ops）

> 评价是店铺分（DSR）与转化的杠杆。低量级店铺（周订单 < 50）以**模板化人工回复**为主，
> API 仅做批量查询与提醒；不追求自动生成评价内容。

## 能力

- 评价列表查询：`taobao.traderates.list.get`（按订单/时间/评分维度拉取）
- 评价回复：`taobao.traderate.add`（回评/解释）
- 差评预警：新增差评 → 提醒人工介入（不自动联系买家）
- DSR 维护策略：描述/服务/物流三项分的影响因素与日常动作

## 使用方式

```
/taobao-review-ops 拉本周差评和未回复评价
/taobao-review-ops 这条差评怎么回？给我三个版本的回复
/taobao-review-ops DSR 物流分掉了，帮我定位原因
```

## 核心 API 面（速查）

| 环节 | 接口 | 要点 |
|------|------|------|
| 评价列表 | `traderates.list.get`（`rate_type=feedback`，`fields` 选 `oid/tid/nick/content/result/created`） | 按 `created` 时间窗增量拉 |
| 回评/解释 | `traderate.add` / 差评解释通道 | 回评内容先过人工审核再提交 |
| 差评监控 | 定时任务调 `traderates.list.get` + `result=bad` 过滤 | 命中即提醒，不自动回复 |

## 回复策略（按评价类型）

| 类型 | 策略 |
|------|------|
| 好评 | 统一模板 + 变量化（商品名/买家称呼），24h 内回 |
| 中差评 | 人工介入：先查订单事实（`trade-ops` 拉详情）→ 致歉 + 归因 + 补救口径（补发/退款/补偿三选一）→ 回复公示（给后来买家看） |
| 恶意/异常评价 | 走平台申诉通道，不私下纠缠 |

## DSR 日常维护

1. **描述分**：详情页如实（问题 disclosed 制，见 `taobao-product-ops` 内容包 `detail` 字段）
2. **服务分**：响应时效；售后三选一口径提前定好，不现场博弈
3. **物流分**：发货时效承诺保守化；偏远地区提前说明

## 红线与限制

- **不刷单、不买好评、不短信骚扰改评**——平台严打，处罚力度高于普通违规
- 回评内容人工过目后提交；不自动生成承诺性表述（退款/赔偿口径必须人来定）
- API 需企业资质 + 店铺 `session`；评价接口权限与交易类同级审批
