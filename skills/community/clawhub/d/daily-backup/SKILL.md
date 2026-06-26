---
name: daily-backup
version: 1.9.0
description: 每日 Git 备份。检查 agent 工作空间是否有待提交变更，由 agent 决定是否提交并 push。触发时机：cron 定时任务或手动调用。
---

# Daily Backup

每日 Git 备份辅助工具。**只备份当前 agent 自己的工作空间**（当前 session 的 `workspaceDir`）。

## 脚本说明

`scripts/pre-flight-check.sh` — 工作空间 Git 状态检查

- 输入：当前 agent 的 workspaceDir（通过环境变量 `AGENT_WORKSPACE` 传入）
- 输出：
  - `NOT_GIT_REPO` → 工作区不是 git 仓库
  - `NO_CHANGES` → 无待提交变更
  - `HAS_CHANGES` → 有待提交变更，同时输出新增/修改/删除文件数

## 核心流程

1. 运行 pre-flight-check.sh 检查当前工作空间
2. 根据结果决定是否提交（`NOT_GIT_REPO` → git init，`NO_CHANGES` → 跳过，`HAS_CHANGES` → 按内容分次提交 + push）
3. 如远程未创建，读 references/spec.md 按指引处理

## 触发时机

- cron 定时任务（建议每日）
- 用户明确要求时

## 投递（如需）

如需推送报告到飞书群，在 cron 任务里通过 `delivery` 配置指定目标（不在技能里硬编码）。

## 报告格式

```markdown
# Daily Backup 报告

**时间**: YYYY-MM-DD HH:MM

## 备份状态

| 项目 | 状态 |
|------|------|
| 提交 | ✅ / ⚠️ |
| 推送 | ✅ / ❌ / 跳过 |

## 变更统计

| 类型 | 数量 |
|------|------|
| 新增 | N |
| 修改 | N |
| 删除 | N |

## 最新提交

    <commit hash> <commit message>

