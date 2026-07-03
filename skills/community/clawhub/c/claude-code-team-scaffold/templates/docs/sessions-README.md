# Sessions

`docs/sessions/` 目录存放**会话级工作记录**（task_plan.md、findings.md、progress.md），由 `.claude/skills/planning-with-files/` skill 管理。

## 用途

- **会话恢复**：上下文压缩或重置后，`session-catchup.py` 脚本扫描此目录恢复上下文
- **跨会话记忆**：把"重要但不紧急"的内容写到磁盘而不是反复塞上下文
- **进度追踪**：每个会话一个独立子目录，清晰记录阶段性成果

## 文件命名

子目录命名建议：`YYYY-MM-DD_{topic-slug}/`

例：
- `docs/sessions/2026-06-26_user-auth-migration/`
- `docs/sessions/2026-06-20_payment-integration/`

## 模板

参考 `.claude/skills/planning-with-files/templates/`：
- `task_plan.md` — 任务阶段、进度、决策
- `findings.md` — 调研发现、文档摘要
- `progress.md` — 会话日志、测试结果

## 触发条件

何时使用 sessions：
- 多步骤复杂任务（≥5 步）
- 跨多次会话的长线工作
- 需要保留大量调研发现的任务
- 多人协作、需要交接的任务

简单任务（单次会话内可完成）不必使用。
