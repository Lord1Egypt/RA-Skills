# Reference Skill Analysis

## Reusable Patterns

本轮新增业务域主要复用以下能力模式：

- 调研阶段使用预设问题包减少重复追问
- 设计阶段把执行面拆成 `Skill-only`、`Skill + CLI`、`Skill + API/MCP`、`Skill + CLI + API/MCP`
- 生成阶段通过 `domain_supplements` 承接域独有结果要求
- 高风险操作通过人工确认 gate 收口

## Execution Plane Notes

`sales_crm_ops`、`hr_recruiting_ops` 和 `event_community_ops` 更常依赖 CRM、ATS、HRIS、日历、邮件、表格和社群工具。

`education_training_ops` 更常依赖知识库、文档、PPT、表格、LMS 和本地批量生成脚本。

`legal_contract_ops` 更常依赖文档比对、本地文件处理、合同系统、审批系统和任务系统。

`product_market_research` 更常依赖问卷、评论、竞品页面、产品分析、知识库和文档系统。

## Gate Notes

自动触达、候选人筛选、正式评分、法律结论、合同写回、公开发布和群发提醒都需要单独确认。涉及个人信息或敏感商业信息时，需要把脱敏、权限和审计要求写入设计摘要和构建计划。
