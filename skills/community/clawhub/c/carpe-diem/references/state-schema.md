# 本地状态协议

状态由 `scripts/carpe_diem.py` 管理。Agent 负责提炼和解释，脚本负责格式、原子写入和 revision 冲突。不要绕过脚本直接修改 JSON，除非脚本不可用且用户明确选择手工恢复。

## 个人画像

默认位置：`~/.carpe-diem/profiles/me.json`。

顶层包含 `schema_version`、`handle`、`revision`、`updated_at`，以及：`strengths`、`interests`、`recurring_frictions`、`constraints`、`project_preferences`、`working_style`、`project_history`、`consents`。

每条事实包含：

- `id`：稳定标识；
- `value`：提炼后的短结论；
- `kind`：`observed`、`inferred` 或 `explicit`；
- `confidence`：写入前为 `candidate`，确认后为 `confirmed`；
- `basis`：为什么形成这条候选；
- `confirmed_at`、`last_used_at`：时间记录。

长期画像的正确流程：

1. `state propose` 生成候选 JSON，不写文件；
2. 在主对话展示 value、kind、basis 和影响；
3. 用户确认后把提案保存为临时 JSON，再执行 `state apply`；
4. 用户要求遗忘时，确认具体 fact id 和影响，再执行 `state forget`；
5. 跨环境分享前使用 `state export`，不要复制原文件。

## 项目状态

位置：项目根目录 `.carpe-diem/project-state.json`；事件位于 `.carpe-diem/events/`。

首次由 `project init` 创建，初始阶段为 `discover`。每个确认节点使用 `project event` 记录摘要、目标阶段、下一步和 `expected-revision`。事件是本地不可变摘要，不保存源码、完整 Diff 或完整聊天。

阶段值：`discover`、`validate`、`plan`、`handoff`、`track`、`paused`、`completed`。

## 冲突

所有变更携带已读到的 revision。脚本返回 revision conflict 时，重新读取最新状态，向用户解释变化并重新生成候选；不要重试旧写入或覆盖新状态。

## 降级

脚本不可用、状态不可写或文件损坏时，保留原文件并在对话中生成一份可复制恢复摘要。不得声称状态已经保存。
