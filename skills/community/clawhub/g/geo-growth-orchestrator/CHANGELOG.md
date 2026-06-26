# Changelog

## v1.0.5

- 增强客户交付能力：完整报告开头新增“老板能看懂的3句话结论”。
- 共同知识盲区新增商业影响和建议动作。
- 自动生成知乎、小红书、抖音、官网 FAQ 和 GEO 友好型文章选题。
- 所有建议新增影响程度、执行难度、见效速度和优先级分。
- 报告结尾新增复测机制，说明复测时间、指标和有效性判断。

## v1.0.4

- 强化 OpenClaw 默认输出契约：默认 `output_mode=full_report`，必须在当前对话输出完整 `final_report.md`。
- 新增客户交付级双模型评估报告模板 `templates/final_report.md`。
- 新增完整报告生成脚本 `scripts/generate_full_report.py`，保存原始回答、模型评分、双模型对比、完整报告和摘要。
- 新增西班牙橄榄油与西班牙火腿双模型评估示例输入。
- 新增 smoke test，验证完整报告章节、stdout 非摘要和评分字段完整。

## v1.0.3

- 新增客户成果报告与内部审计报告双层输出机制。
- 新增客户报告、内部审计报告、客户摘要、内容资产展示和下一步计划 prompt。
- 新增客户报告生成脚本 `scripts/generate_client_report.py`。
- 新增内部审计报告生成脚本 `scripts/generate_internal_report.py`。
- 新增安吉云上草原客户报告样例。
- 保留 v1.0.2 的证据等级、发布闸门和合规校验能力，但避免在客户报告中暴露内部字段。

## v1.0.0

- 新增 PowerMatrix GEO Growth Orchestrator 总控型 Skill。
- 新增标准中间件 schema：品牌母库、GEO 检测报告、内容任务、平台草稿、发布计划和工作流状态。
- 新增多平台分发 prompt，覆盖知乎、CSDN、掘金、今日头条。
- 新增发布计划和复盘报告生成 prompt。
- 新增 workflow 校验脚本 `scripts/validate_workflow_state.py`。
- 新增平台草稿合并脚本 `scripts/merge_platform_drafts.py`。
