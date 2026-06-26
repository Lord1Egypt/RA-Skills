# 部署与平台运维预设

## domain_id

`deploy_platform_ops`

## common_jobs

- 部署到 Vercel、Netlify、Cloudflare、Render、Railway 等平台
- 执行 Docker、SSH、系统服务和环境变量操作
- 检查线上服务健康、日志、回滚和配置
- 维护 CI/CD、发布脚本和环境初始化流程
- 把本地构建产物推送到目标运行环境

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 目标平台或服务器是什么
- 当前任务是部署、回滚、诊断，还是环境初始化
- 是否已有平台 CLI、SSH 配置、CI/CD workflow 或部署日志
- 哪些操作允许自动执行，哪些必须人工确认
- 是否涉及生产环境、用户数据或付费资源
- 验收标准是本地构建通过、线上健康检查通过，还是业务回归通过
- 失败时优先回滚、暂停，还是保留现场继续诊断

## recommended_execution_planes

- `Skill + CLI`
  适合 Vercel、Netlify、Cloudflare、Docker、SSH、GitHub Actions 等命令型流程
- `Skill + API/MCP`
  适合需要读取平台状态、日志、部署记录或服务指标的流程
- `Skill + CLI + API/MCP`
  适合部署、日志诊断、健康检查和回归验证连续执行的流程

## risk_and_gates

- 生产环境操作必须先确认目标环境和影响范围
- 删除、重建、清库、回滚和密钥修改都要单独 gate
- 部署完成不等于业务已经在线生效，必须定义线上回归方式
- 涉及 SSH、密钥和环境变量时，只记录引用方式，不记录明文
- 外部平台不可用时，要保留手动操作路径和恢复建议

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.deploy_platform_ops`
- 如果涉及生产变更，补 `rollback-plan.md` 或在 `build-plan.md` 中写清回滚 gate
