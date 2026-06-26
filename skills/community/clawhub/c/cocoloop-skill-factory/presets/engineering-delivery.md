# 工程交付预设

## domain_id

`engineering_delivery`

## common_jobs

- 修 PR 评论
- 修 CI
- 发布草稿 PR
- 创建或升级 Skill
- 创建或升级 MCP
- 生成工程说明文档

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 当前任务更偏代码修改、流程修复，还是构建脚手架
- 是否已有现成仓库、PR、Issue 或失败日志
- 当前目标是本地使用、团队复用，还是公开分发
- 是否需要真实提交、推分支、开 PR
- 哪些步骤必须脚本化，哪些步骤保留人工确认

## recommended_execution_planes

- `Skill + GitHub CLI/API`
  适合 PR、评论、CI、发布相关任务
- `Skill + 本地脚本`
  适合批量改写、仓库扫描、产物生成
- `Skill + MCP SDK`
  适合构建外部系统执行面

## risk_and_gates

- 必须明确仓库边界和可写范围
- 涉及 PR、CI、发布时要先确认认证状态
- 涉及自动提交、推送或发布时要保留人工 gate
- 需要区分“只分析”与“实际修改”

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，再补 `spec.yaml`
