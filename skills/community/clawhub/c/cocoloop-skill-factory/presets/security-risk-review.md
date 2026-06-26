# 安全与风险审查预设

## domain_id

`security_risk_review`

## common_jobs

- 审查 Skill、脚本、依赖和权限声明
- 检查凭据、环境变量、密钥文件和敏感数据流
- 做威胁建模、权限边界和误用风险分析
- 分析告警、日志、异常行为和访问记录
- 形成修复队列、审查报告和发布前风险说明

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 审查对象是代码、Skill、依赖、配置、日志，还是外部平台流程
- 目标是发布前检查、事故诊断、权限收敛，还是合规记录
- 是否可以读取敏感文件或日志，是否需要脱敏
- 需要按哪些风险类别检查，例如凭据泄露、越权、数据外传、命令注入
- 输出需要修复建议、阻断结论，还是可接受风险说明
- 是否需要把发现转成 Issue、PR 评论或审计记录
- 哪些操作只能分析，不能自动修复

## recommended_execution_planes

- `Skill-only`
  适合轻量威胁建模、人工审查清单和发布前风险说明
- `Skill + CLI`
  适合本地依赖、配置、脚本和仓库扫描
- `Skill + API/MCP`
  适合安全平台、日志系统、告警系统和权限系统查询
- `Skill + CLI + API/MCP`
  适合从本地证据到外部审计系统的完整链路

## risk_and_gates

- 敏感内容读取前必须确认范围，输出默认脱敏
- 不能把凭据、Token、密钥或个人信息写进最终 Skill
- 自动修复前必须确认风险等级和改动范围
- 审查结论要区分确定问题、潜在风险和需要人工确认的项
- 涉及事故或合规场景时，保留证据来源和时间范围

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.security_risk_review`
- 如果涉及真实安全事件，补 `evidence-log.md` 或在 `research-summary.md` 中写清证据边界
