# Design Summary

## Builder Quality

新增共享协议规则模块，render 入口用抛错方式阻断不完整 spec，platform validate 用同一套规则收集错误。这样后续增加 gate 时，只需要先改共享规则，再补测试。

## Business Presets

新增三个第二层预设：

- `workflow_integration`
- `deploy_platform_ops`
- `security_risk_review`

这三个方向默认带更强的权限、凭据、写入、回滚和审计 gate，既可以作为主任务域，也可以作为跨域约束进入 `peer_domains`。

## Reference Evidence

新增 `reference-skill.py`，支持本地 Skill 复制、GitHub 浅克隆和已拉取目录分析。工具会生成 `_fetch-meta.json`、`_reference-analysis.json` 和 `_reference-analysis.md`，供设计阶段写入 `reference-skill-analysis.md`。
