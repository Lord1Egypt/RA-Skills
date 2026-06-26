---
applyTo: "**"
---
## Skills 优先级

本仓库同时使用两类 skill：

- **插件注册 skill**：通过 `contributes.chatSkills` 静态注册，Copilot 可主动调用
- **工作空间 skill**：位于 `.github/skills/`，Copilot 按需加载

当两者存在同名 skill 时，**以 `.github/skills/` 下的版本为准**。工作空间版本是经过本仓库定制的覆盖版本，优先于插件默认版本。

## 文件计划工作流（planning-with-files）

本项目使用 `docs/sessions/<task-slug>/` 下的持久化 markdown 文件作为任务工作记忆。以下规则在**所有会话**中生效。

### 会话开始时

1. 检查 `docs/sessions/` 下是否存在活跃的 `task_plan.md`
2. 如果存在：读取它以恢复上下文，运行 `git diff --stat` 了解上次的代码变更
3. 如果不存在且当前任务复杂（>5 步）：创建 `docs/sessions/<task-slug>/task_plan.md`

### 执行任务时

- **重大决策前**：重新读取 `task_plan.md` 的目标和当前阶段，确保方向一致
- **每完成一个阶段**：立即更新 `task_plan.md`（标记阶段状态 → `complete`，记录变更文件）
- **发现重要信息时**：写入 `findings.md`

### 任务结束前

- 检查 `task_plan.md` 中所有阶段是否已完成
- 如有未完成阶段：**不要标记任务完成**，继续执行或明确报告阻塞原因
- 全部完成后：更新 `progress.md` 记录最终状态
