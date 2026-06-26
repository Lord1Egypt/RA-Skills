---
name: context-memory-manager
description: >
  Agent 上下文记忆管理。每次被唤醒时自动检查 session 上下文使用率，
  超过阈值时保存完整对话并提炼记忆。支持每日定时复盘已有记忆、
  合并冗余、防止遗忘。
  使用场景：(1) 自动监控上下文使用率 (2) 超阈值保存完整对话并压缩记忆 (3)
  每日定时复盘已有记忆 (4) 查询当前 session 状态。
  触发词："监控上下文"、"压缩记忆"、"复盘记忆"、"memory review"、"context monitor"、
  "记忆管理"、"上下文太长"、"清理记忆"、"每日复盘"、"安装 context-memory-manager"。
---

# Context Memory Manager

Agent 上下文感知记忆管理：自动保存完整对话 → 提炼结构化记忆 → 防止遗忘。

## 架构设计

```
┌─────────────────────────────────────────────────────┐
│  Compress（每次被唤醒时 — 核心机制）                    │
│  session_status → 检查上下文使用率                      │
│  → 超 70%：保存完整上下文 → 提炼记忆 → 更新 MEMORY.md    │
├─────────────────────────────────────────────────────┤
│  Review（每天凌晨 3 点 — cron 触发）                    │
│  增量扫描 memory 文件 → 输出 JSON 报告                  │
│  → Agent 被唤醒时检查报告 → 提炼/合并 → 更新 MEMORY.md  │
└─────────────────────────────────────────────────────┘
```

> **核心原则**：上下文检测只有 Agent 自己能做（`session_status`），
> cron 脚本仅辅助磁盘文件扫描和复盘报告产出。

## 记忆分类

| 类型 | 路径 | 定位 |
|------|------|------|
| 聊天日志 | `memory/chat/YYYY-MM-DD.md` | 完整对话原始记录 |
| 项目日志 | `memory/projects/<项目名>/YYYY-MM-DD.md` | 结构化沉淀 |
| 核心记忆 | `MEMORY.md` | 全局索引 + 用户偏好 + 待办 |
| 归档文件 | `memory/archive/` | 超过 30 天的旧日志 |

**数据流向**：
```
会话 → session_status 检测 → 超阈值
  ↓
① 保存完整上下文 → memory/chat/YYYY-MM-DD.md（原始对话，不裁剪）
  ↓
② 从对话提炼 → memory/projects/<项目名>/（结构化项目记忆）
  ↓
③ 更新 MEMORY.md（全局索引、用户偏好、待办事项）
  ↓
cron 每日扫描 → 增量对比 → 复盘提炼 → 合并冗余
```

## ⚡ 首次安装引导（必须执行）

> 当用户安装此 skill 后首次触发时，按以下流程操作：

### Step 1：检查现有状态

```bash
ls -d <workspace>/memory/chat 2>/dev/null && echo "OK" || echo "MISSING"
ls -d <workspace>/memory/projects 2>/dev/null && echo "OK" || echo "MISSING"
test -f <workspace>/MEMORY.md && echo "OK" || echo "MISSING"
```

### Step 2：提示用户

```
📦 context-memory-manager 已安装！需要初始化以下配置：
- [ ] memory/chat/ 目录（聊天日志）
- [ ] memory/projects/ 目录（项目日志）
- [ ] MEMORY.md 核心记忆文件
- [ ] crontab 每日复盘任务（每天凌晨 3 点）

是否一键初始化？
```

### Step 3：执行初始化

1. **创建目录**：`mkdir -p <workspace>/memory/{chat,projects}`
2. **创建 MEMORY.md**（如不存在）
3. **写入 .last_review**：`date -Iseconds > <workspace>/.last_review`
4. **设置 crontab**（追加模式，不覆盖已有内容）：
   ```
   0 3 * * * python3 <skill_dir>/scripts/daily_review.py --workspace <workspace> --days 7 --update-timestamp --archive-days 30 > /tmp/cmm_review.log 2>&1
   ```

### Step 4：确认完成

输出初始化报告，告知用户下次被唤醒时自动开始监控上下文。

---

## 工作流程

### 1. 上下文压缩（每次被唤醒时自动触发）

**Step 1：检查上下文使用率**
```
调用 session_status 获取当前 session 的 token 使用量
```

**Step 2：判断是否需要压缩**

| 使用率 | 动作 |
|--------|------|
| < 70% | 无需操作 |
| ≥ 70% | 执行压缩流程 |
| ≥ 85% | 紧急压缩（优先处理） |

**Step 3：保存完整上下文（必须第一步）**

调用 `sessions_history(sessionKey, limit=尽可能大)` 获取完整对话历史，
将原始对话保存为 `memory/chat/YYYY-MM-DD.md`。
**不要裁剪对话内容，保留完整记录。**

**Step 4：提炼记忆**

从保存的完整对话中提炼：
- **项目进展**：做了什么、改了哪些文件、遇到什么问题
- **用户偏好**：新的偏好、习惯、决策
- **待办事项**：新增/完成的待办
- **关键决策**：技术方案选择、方向调整

写入：
- `memory/projects/<项目名>/YYYY-MM-DD.md`（项目记忆）
- `MEMORY.md`（全局更新）

**Step 5：输出摘要**

告知用户本次压缩保存了多少行对话、提炼了多少条记忆。

### 2. 每日记忆复盘（cron 每天凌晨 3 点）

**cron 脚本产出报告**：
```bash
python3 scripts/daily_review.py --workspace <workspace> \
    --days 7 --update-timestamp --archive-days 30
```

脚本输出 JSON 报告并写入 `/tmp/cmm_review_report.json`，包含：
- 新增/变更的文件列表（增量扫描）
- token 估算
- agent 执行指令

**Agent 被唤醒时处理报告**：
1. 检查 `/tmp/cmm_review_report.json` 是否存在
2. 如存在 → 按报告中的 `agent_instructions` 执行
3. 处理完后**删除该文件**，避免重复处理

### 3. 自动归档

超过 30 天的聊天日志（`memory/chat/`）自动移动到 `memory/archive/`。
归档不删除文件，需要时仍可查阅。

## ⚡ Agent 被唤醒时的自动检查

> 每次被用户消息唤醒时，按以下顺序执行：

1. **session_status 检查**：调用 `session_status` 获取上下文使用率
   - ≥ 70% → 执行完整压缩流程（保存 → 提炼 → 更新 MEMORY.md）

2. **复盘报告检查**：检查 `/tmp/cmm_review_report.json`
   - 存在 → 读取报告，执行复盘提炼
   - 处理完后删除文件

3. **如果两者都不需要** → 正常响应用户请求

## 注意事项

- 压缩时必须**先保存完整对话**，再提炼，不允许直接裁剪丢弃
- 聊天日志保留原始对话轨迹，不精简
- 项目日志按项目分目录，结构化沉淀
- `.last_review` 文件记录复盘时间戳，用于增量扫描
- 首次复盘无 `.last_review` 文件时，全量扫描
- Token 估算为粗略值（字节数 / 2.5），实际因模型而异
