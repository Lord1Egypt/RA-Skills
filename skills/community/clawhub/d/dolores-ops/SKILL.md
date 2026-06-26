---
name: openclaw-ops
description: |
  OpenClaw 运维工具 - 负责 AI 助手自身的日常运维工作。
  包括：健康检查、Memory 同步、目录清理、日志管理、定时任务管理。
when_to_use: |
  当用户说"维护你自己"、"清理工作目录"、"设置定时任务"、"健康检查"、
  "同步记忆"、"清理临时文件"时使用此技能。
argument-hint: <daily|weekly|memory|cleanup|status>
allowed-tools: [exec, read, write, edit, sessions_list]
user-invocable: true
---

# OpenClaw Ops - AI 助手日常运维

## Goal

帮助 AI 助手保持自身运维的规律性，确保系统健康运行，并持续沉淀与用户的交互记忆。

## Steps

### 1. 每日健康检查

**触发**：每天 8:00 (via cron) 或 heartbeat

1. 执行 `openclaw gateway status` 检查 Gateway 状态
2. 检查配置警告
3. 检查 `/tmp/openclaw/openclaw-*.log` 有无 ERROR
4. 检查 Token 使用情况（`session_status`）

**异常处理**：
- Gateway 不运行 → 执行 `openclaw gateway start`
- 有 ERROR 日志 → 报告给用户
- Token 使用 > 80% → 提醒用户切换模型

### 2. Memory 同步

**触发**：每天 21:00 (via heartbeat)

1. 回顾当天对话记录（`sessions_history`）
2. 提取重要事项写入 `memory/YYYY-MM-DD.md`
3. 判断是否有值得沉淀到 `MEMORY.md` 的内容
4. 检查是否有未完成的承诺/待办

**写入规范**：
- 只记录重要事项（用户偏好、承诺、决定）
- 不记录琐碎对话
- 用简洁语言，每条不超过一句话

### 3. 目录清理

**触发**：每周五下午 或 用户明确要求

1. 列出 workspace 目录
2. 识别可清理的文件：
   - 临时文件：`*.tmp`, `*.temp`, `*.log.old`
   - 压缩包：`*.tar.gz`, `*.zip`（非项目源码）
   - 空目录
3. **删除前必须确认**（用户要求除外）

**安全规则**：
- ❌ 不删除：`.git`, `memory`, `skills`, `.openclaw` 目录
- ❌ 不删除：`MEMORY.md`, `USER.md`, `SOUL.md`, `AGENTS.md`
- ❌ 不删除用户文件
- ✅ 删除前列出示意图

### 4. 日志管理

**触发**：每周五

1. 检查日志大小：`du -sh /tmp/openclaw/`
2. 清理超过 30 天的旧日志
3. 归档重要日志（如配置变更记录）

### 5. 定时任务管理

**触发**：用户要求查看或创建 cron 任务

**查看**：`openclaw cron list`

**创建**：
```bash
openclaw cron create --name "task-name" --cron "0 8 * * *" --system-event "healthcheck"
```

**常用 Cron**：
- 每天 8 点：`0 8 * * *`
- 每天 21 点：`0 21 * * *`
- 每周五：`0 17 * * 5`

## Rules

- 定时任务（cron）创建后告知用户任务 ID
- 删除操作必须先确认再执行
- Memory 写入用简洁语言
- 异常情况立即报告给用户
- 不修改用户配置，只做运维操作

## 输出格式

完成任务后，简洁汇报：

```
✅ 早间健康检查完成
- Gateway: 运行中 (pid 44380)
- 配置警告: 1 个 (clawbnb-hub 已禁用)
- 日志: 无 ERROR

✅ Memory 同步完成
- 今日记录: 3 条
- 待沉淀: 1 条（关于用户偏好）
```

## Heartbeat 配置示例

在 `HEARTBEAT.md` 中添加：

```markdown
## 🤖 日常运维任务

### 1. 早间健康检查 (08:00-09:00)
- 检查 Gateway 状态
- 检查配置警告
- 检查日志 ERROR

### 2. 晚间 Memory 同步 (21:00-22:00)
- 回顾当天对话，写入 memory/YYYY-MM-DD.md
- 更新 MEMORY.md 重要事项

### 3. 每周五下午：周度清理
- 清理临时文件
- 检查过期日志
- 检查 cron 任务状态
```