# Spec

## Builder Regression

- render 与 platform validate 共享同一组协议规则。
- builder 提供 `npm test` 运行单元测试。
- builder 提供 `npm run regression` 遍历 `output/**/spec.yaml` 的源 spec，并验证可 render、可 platform validate。
- 回归脚本跳过已经生成出的 Skill 目录，避免把生成结果再次当作源输入。

## Second-Layer Presets

- `workflow_integration` 覆盖 SaaS、任务、文档、消息和审批系统联动。
- `deploy_platform_ops` 覆盖部署、回滚、环境配置、日志和健康检查。
- `security_risk_review` 覆盖权限、凭据、依赖、日志和威胁建模。
- 预设必须沿用既有 preset 结构。

## Reference Skill Tooling

- `reference-skill.py fetch --source local` 复制本地候选 Skill 到证据目录。
- `reference-skill.py fetch --source github` 浅克隆 GitHub 候选仓库到证据目录。
- `reference-skill.py analyze` 分析已有候选目录。
- 工具输出 JSON 和 Markdown 两种分析结果。
- 工具只做证据固化和结构分析，设计判断仍在设计阶段完成。
