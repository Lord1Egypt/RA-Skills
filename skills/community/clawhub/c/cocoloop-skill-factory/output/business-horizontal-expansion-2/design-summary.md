# Design Summary

## Business Layer Update

业务横向扩展层从 6 个域扩展到 12 个域，覆盖内容、知识、数据、客服、电商、投研、销售、人力、教育、法务、产品研究和活动社群。

## Routing

新增域进入正式任务域集合。调研阶段可以直接把它们作为 `primary_domain`，也可以在跨域需求中放入 `peer_domains`。

## Preset Contract

每个新增预设都保留固定结构：

- `domain_id`
- `common_jobs`
- `default_question_pack`
- `recommended_execution_planes`
- `risk_and_gates`
- `default_outputs`

## Spec Impact

`spec-template.yaml` 已加入新增域的 `domain_supplements` 空块。PRD 文档同步更新任务域地图、路由治理、协议说明、补充块示例和 benchmark 关系。
