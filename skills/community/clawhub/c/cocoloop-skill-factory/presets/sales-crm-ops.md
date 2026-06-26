# 销售与 CRM 运营预设

## domain_id

`sales_crm_ops`

## common_jobs

- 整理线索、客户、商机、跟进记录和销售阶段
- 生成销售邮件、跟进话术、会议纪要和行动项
- 分析漏斗、转化率、客户分层和流失风险
- 把通话、邮件、表单或活动名单写入 CRM
- 生成销售周报、客户摘要和回访计划

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 目标 CRM 或客户系统是什么
- 目标是线索整理、跟进草稿、漏斗分析，还是销售报告
- 需要读取哪些对象，例如客户、联系人、商机、邮件、会议或表单
- 是否允许自动写回 CRM，还是只生成待审核内容
- 是否有销售阶段、客户分层、SLA 或跟进节奏规则
- 是否涉及个人信息、合同金额、报价或敏感客户数据
- 成功标准是转化率、响应速度、线索质量，还是销售执行效率

## recommended_execution_planes

- `Skill-only`
  适合销售话术、跟进草稿、客户摘要和人工审核建议
- `Skill + API/MCP`
  适合 CRM、邮件、日历、表单和会议系统联动
- `Skill + CLI + API/MCP`
  适合批量导出、离线分析、报告生成和系统写回

## risk_and_gates

- 默认生成草稿，不自动联系客户
- 写回 CRM 前必须确认字段、对象和影响范围
- 客户个人信息、报价和合同金额需要脱敏或权限 gate
- 销售建议要区分事实记录、推断和下一步建议
- 批量触达、邮件发送和外呼必须单独确认

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.sales_crm_ops`
- 如果涉及自动触达，必须在 `build-plan.md` 中写清触达 gate
