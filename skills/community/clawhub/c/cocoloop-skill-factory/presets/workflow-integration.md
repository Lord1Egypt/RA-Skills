# 工作流集成预设

## domain_id

`workflow_integration`

## common_jobs

- 同步 Notion、Linear、Slack、Jira、飞书、钉钉等系统
- 把会议、文档、Issue 或消息转成任务
- 汇总跨系统状态并生成更新
- 管理团队流程、审批、提醒和交接
- 把本地 Agent 输出写回外部 SaaS

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 目标系统有哪些，哪个是主系统
- 需要读取、写入，还是双向同步
- 是否已有 API、MCP、CLI、Webhook 或浏览器登录态
- 需要同步哪些对象，例如任务、文档、评论、状态、附件
- 是否允许自动写入，还是每次写入前需要人工确认
- 凭据、权限、频率限制和审计记录有什么要求
- 失败后要生成待办、重试队列，还是只返回错误报告

## recommended_execution_planes

- `Skill + API/MCP`
  适合 Notion、Linear、Slack、Jira、飞书、钉钉等有稳定接口的系统
- `Skill + CLI + API/MCP`
  适合本地文件、Git 状态和外部系统需要一起编排的流程
- `Skill + 浏览器自动化`
  只适合没有稳定接口、但页面流程明确且用户接受登录态风险的场景

## risk_and_gates

- 必须区分只读查询和真实写入
- 写入外部系统前要确认权限、范围和审计要求
- 凭据不能写进 Skill 正文或示例产物
- 批量同步需要限流、重试和幂等策略
- 涉及通知、审批或任务分配时，默认保留人工确认

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.workflow_integration`
- 如果涉及真实写入，补 `risk-review.md` 或在 `build-plan.md` 中写清写入 gate
