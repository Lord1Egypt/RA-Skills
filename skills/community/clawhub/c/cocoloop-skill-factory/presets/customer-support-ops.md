# 客户支持运营预设

## domain_id

`customer_support_ops`

## common_jobs

- 整理客服对话、工单、FAQ 和知识库答案
- 自动生成回复草稿、分流规则和升级建议
- 分析用户反馈、投诉、退款原因和满意度
- 把产品问题转成 Issue、任务或运营报告
- 维护支持话术、服务边界和风险提示

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 支持渠道是什么，例如邮件、客服系统、IM、社群或工单系统
- 目标是回复草稿、自动分类、FAQ 更新，还是反馈分析
- 是否允许自动发送，还是只生成待审核草稿
- 有哪些知识库、产品文档、SLA 或服务边界
- 是否涉及退款、投诉、隐私、未成年人或高风险内容
- 输出要写回哪里，例如 CRM、工单系统、Issue 或知识库
- 成功标准是响应速度、准确率、满意度，还是问题闭环率

## recommended_execution_planes

- `Skill-only`
  适合话术设计、FAQ 草稿、分类规则和人工审核建议
- `Skill + API/MCP`
  适合 CRM、工单系统、知识库和消息系统接入
- `Skill + CLI + API/MCP`
  适合批量导出、离线分析、回写任务和报表生成

## risk_and_gates

- 默认只生成草稿，不自动发送给客户
- 涉及退款、投诉、法律、健康或隐私问题时必须升级人工处理
- 必须引用可信知识库或明确答案来源
- 客户信息需要脱敏，不能进入示例或公开产物
- 自动分类需要保留置信度和人工复核路径

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.customer_support_ops`
- 如果涉及自动发送，必须在 `build-plan.md` 中写清发送 gate
