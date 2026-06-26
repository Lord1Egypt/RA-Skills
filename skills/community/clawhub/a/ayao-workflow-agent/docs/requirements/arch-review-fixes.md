# 需求文档：ARCH-REVIEW H1–H5 修复

> 创建时间：2026-03-20
> 来源：cc-review ARCH-REVIEW 全面审查结果
> 档位：C（需求来自 review 报告，已明确；设计需 cc-plan 探索代码后输出）

## 背景

对 coding-swarm-agent skill 做了一次整体架构 + 代码 review，发现 5 个 High 问题，
核心问题集中在监控层失效、安全风险、文档误导三类。

## 需要修复的问题

### H1 — update-task-status.sh：flock race guard 被 set -e 破坏

**问题：** flock 块内用 `set -e` 的隐式退出码传播，某些中间步骤失败时会跳出 flock
块而不触发 race guard（CAS 检查），竞态保护形同虚设。

**期望：** flock 块内的状态 CAS 检查需要显式捕获退出码（`if cmd; then ... fi` 模式），
确保无论哪步失败都能正确触发 race guard 并返回正确的 exit code。

---

### H2 — health-check.sh：stuck 检测读取的 tmux 字段从未被写入

**问题：** health-check 读 `active-tasks.json` 里 task 的 `tmux` 字段来判断 agent session，
但 dispatch.sh 的 `update-task-status.sh` 调用从来没有写入这个字段——stuck 检测永远 miss。

**期望：** dispatch.sh 在 mark running 时，通过 `update-task-status.sh` 同时写入 `tmux` 字段，
让 health-check.sh 能正确找到对应的 tmux session。

---

### H3 — health-check.sh vs heartbeat：两个时间戳来源不一致，heartbeat 无效

**问题：** dispatch.sh 的 heartbeat 每 5 分钟更新 `agent-pool.json` 里 agent 的 `last_seen`，
但 health-check.sh 判断 stuck 读的是 `active-tasks.json` 里 task 的 `updated_at`——
两者来源不同，heartbeat 更新的字段 health-check 根本不读，heartbeat 形同虚设。

**期望：** 统一时间戳来源：heartbeat 更新 `active-tasks.json` 里对应 running task 的
`updated_at`（通过 `update-task-status.sh heartbeat` 子命令或类似机制），
让 health-check 的 stuck 检测能感知到 agent 仍在活跃。

---

### H4 — dispatch.sh force-commit：git add -A 有安全风险

**问题：** agent 忘记 commit 时，runner script 执行 `git add -A`，
会把 `.env`、`config/secrets.json` 等未被 .gitignore 覆盖的敏感文件一起推送到远端 repo。

**期望：** 改为 `git add -u`（只 stage 已跟踪文件的修改，不添加新文件），
避免意外推送敏感文件。force-commit 的 commit message 里注明这是 fallback。

---

### H5 — SKILL.md 对自动化程度描述严重误导

**问题：** SKILL.md Phase 5 描述 on-complete.sh 会 `POST /hooks/agent` 触发自动 dispatch，
实际 on-complete.sh 只发 `openclaw system event`，review 派发和 next-task dispatch
都依赖 AI orchestrator 被事件唤醒后**手动**执行。文档严重高估了自动化程度。

**期望：** 更新 SKILL.md 相关描述，明确说明：
- on-complete.sh 发 `openclaw system event` 唤醒 orchestrator
- orchestrator（AI）被唤醒后负责 verify scope、dispatch review（full 级别）、dispatch next pending task
- "自动" = "AI 被事件驱动，无需人类介入"，不是"脚本自驱无 AI"

---

## 超出范围

以下 Low/Suggestion 问题本次不修，留待下次：
- L1–L6（/tmp 清理、L3 eval、L4 重复计算等）
- S1–S5（建议类优化）
