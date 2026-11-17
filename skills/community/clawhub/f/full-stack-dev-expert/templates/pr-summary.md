# 交付摘要（pr-summary）

> 产出者：总指挥，任务收尾时汇总。面向用户的一页纸交付结论。

- **任务号**：FS-…
- **任务类型**：<从零建项目/功能开发/…>
- **执行模式**：<模式 A subagent 委派 / 模式 B 上下文内换装>

## 1. 角色启用表

| 角色 | 状态（已启用/未启用+原因） | 产出 |
|---|---|---|
| 需求分析师 | | docs/requirements-spec.md |
| 架构师 | | docs/architecture.md, docs/api-contract.md, docs/adr/ |
| UI/UX 设计师 | | docs/ui-spec.md |
| 数据库工程师 | | docs/db-schema.sql + migrations/ |
| 后端工程师 | | 服务端源代码 |
| 前端工程师 | | 前端源代码 |
| 管理后台后端工程师 | | 管理域端点（RBAC/审计） |
| 管理后台前端工程师 | | 管理端页面（布局/权限路由/CRUD） |
| 逆向融合工程师 | | docs/reverse-analysis.md（ORRI） |
| 测试工程师 | | docs/test-plan.md, docs/test-report.md |
| 安全工程师 | | docs/security-review.md |
| 代码审查员 | | docs/review-report.md |
| DevOps 工程师 | | docs/deploy-guide.md, CI/CD 配置 |
| 技术文档工程师 | | README, API 文档, docs/arc42.md, docs/adr/ 索引, 专业文档集（docs/prd.md, docs/user-stories.md, docs/ddd-design.md, docs/dev-standards.md, docs/roadmap.md, docs/business-process.md，按需裁剪）, docs/runbook.md（按需）, CHANGELOG.md, docs/INDEX.md |

## 2. 交付物清单

| 交付物 | 位置 | 状态 |
|---|---|---|
| 需求规格 | docs/requirements-spec.md | 已冻结/待确认 Q<x> |
| 源代码 | <路径> | 构建:通过 / 测试:x 通过 y 失败 |
| 部署文档 | docs/deploy-guide.md | 演练:通过 |

## 3. 质量结论

- 测试：通过率、缺陷分布（P0/P1 必须为 0 或列豁免理由）
- 审查：阻塞项清零 / 建议项 <n> 条待办
- 安全：高危 0；中危 <n>（状态）
- 门禁打回记录：<阶段、次数、原因>（如实）

## 4. 未决事项与建议

- 待用户决策：<待确认清单未关闭项>
- 已知问题：<P2/P3 遗留>
- 后续建议：<下一步路线>

## 5. 验证方式

```bash
# 用户复核入口：一条命令跑起项目 / 验证核心功能
<命令>
```
