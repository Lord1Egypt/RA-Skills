# 商家友好语言规则（A4 配套）

本文档是 SKILL.md 铁律 A4「商家友好语言」的配套字段映射 + 话术模板。**首次面向商家输出前必须完整阅读**。

---

## ✅ 字段名 → 商家语言翻译表（强制使用）

| 技术词 | 商家友好说法 |
|--------|-------------|
| list_customer_cluster | 查询客群列表 |
| list_cluster_buyer_detail | 展开客群买家明细 |
| customer_reception_advice | 分析买家画像 / 获取跟进建议 |
| list_customer_details | 查询客户名单 |
| get_cluster_marketing_plan | 查询客群运营方案 |
| activate_cluster_plan | 开启客群运营计划 |
| plan_id / planId | 客群编号（一般不必展示） |
| data.list[0] | 第一个客群 / 首个客群（不出现"data"） |
| buyer_login_id | 买家账号 |
| credit_level | 信用等级 |
| if_ka | KA 标签（是 / 否） |
| procurement_mode | 采购模式（周期采购 / 老客 / 等） |
| lst_inq_time | 最近询盘时间 |
| ord_cnt_1m_level | 近 1 月下单频次（高/中/低） |
| gmv_1m_level | 近 1 月成交金额（高/中/低） |
| inq_relation | 询盘关系 |
| crowd_type | 客群类型 |
| cluster_name | 客群名称 |
| buyer_num | 买家人数 |
| --fetch-all | 全量拉取（一般不必展示） |
| --crowd-type | 客群类型筛选 |

---

## ✅ 中间步骤话术模板

| 场景 | ❌ 错误（截图所见） | ✅ 正确 |
|------|---------------------|--------|
| 准备查客群 | "Call list_customer_cluster to get all customer groups" | "正在为你查询客群…"（或直接静默执行） |
| 取第一个客群 | "Take the first one (data.list[0])" | "正在筛选最值得跟进的客群…"（或静默） |
| 拉买家明细 | "Call list_cluster_buyer_detail for that planId" | "正在拉取该客群的买家…" |
| 批量画像 | "Batch call customer_reception_advice to get buyer profiles" | "正在分析每位买家的成交机会…" |
| 排序 | "Sort by order opportunity" | "按成交机会从高到低排序…" |
| 展示交互 | "Show interaction" | "为你列出可主动跟进的买家…" |
| 场景命中 | "命中『客户机会监控』场景，立即执行第一步：调 list_customer_cluster 获取客群 planId。" | "正在为你梳理最近值得主动联系的客户…" |

---

## 应用要点

- 中间步骤话术能省则省，**优先静默执行**；必须给反馈时用 1 句中文白话
- 对商家展示买家画像时，所有字段名先按翻译表替换，再渲染（"信用等级：A5" 而非 "credit_level: A5"）
- 禁止解释「为什么要这一步」（如「按 SKILL.md A3 要求三段式输出」）
- 禁止把 SKILL.md 流程描述里的 tool/字段/路径原样复述给商家——那是给 agent 看的指令
