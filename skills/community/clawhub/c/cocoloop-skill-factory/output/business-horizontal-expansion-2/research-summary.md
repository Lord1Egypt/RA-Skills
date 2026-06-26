# Research Summary

## Scope

本轮继续扩展业务横向预设，新增 6 个高频业务域：

- `sales_crm_ops`
- `hr_recruiting_ops`
- `education_training_ops`
- `legal_contract_ops`
- `product_market_research`
- `event_community_ops`

## Selection Basis

这些领域共同满足三个条件：

- 真实业务中高频出现
- 能复用现有 Skill、CLI、API 和 MCP 执行面
- 需要独立的问题包、风险 gate 和结果补充块

## Domain Fit

新增域补齐了业务经营链路中的销售、人力、学习、法务、产品研究和活动运营场景。它们可以独立作为 `primary_domain`，也可以和内容、知识库、数据分析、工作流集成、文档产物等域组合。

## Risk Notes

本轮新增域普遍涉及客户、候选人、学员、合同、用户反馈或报名信息。默认策略是先生成待审核产物，再通过明确 gate 处理写回、发送、发布、评分和正式结论。
