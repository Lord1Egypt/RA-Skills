---
name: cross-session-tasks
description: >
  解决 AI Agent 跨会话失忆问题的任务管理系统。3 个文件 + 3 条规则，
  让 Agent 在 session 结束后仍能延续任务，跨 channel/thread 断点续传。
  触发词：任务管理、跨会话、task continuity、session memory、断点续传
---

# Cross-Session Task Management 🧠

**让 Agent 记住「上次做到哪了」的 3 个文件 + 3 条规则。**

## 核心问题

每次 session 结束，Agent 失忆。上下文窗口限制导致任务无法跨 session 延续。

## 设计原则

**任务状态住在文件里，不住在 thread 里。**

不管你用哪个 channel、哪个 thread、哪天开的对话，只要读到同一个文件，就能恢复上下文。

## 快速开始

### 第 1 步：创建 3 个文件

```bash
# 1. 复制模板到你的 workspace
cp templates/ACTIVE-TASKS.md ~/. openclaw/workspace/
cp templates/CLOSED-TASKS.md ~/.openclaw/workspace/
mkdir -p ~/.openclaw/workspace/projects/

# 2. 在 AGENTS.md 中添加规则（见下方）
```

### 第 2 步：在 AGENTS.md 中添加 3 条规则

在 `## Every Session` 部分添加：

```markdown
4. Read `ACTIVE-TASKS.md` — 有活跃任务就恢复上下文
```

在文件末尾添加：

```markdown
### 📋 Session 结束时更新任务状态

每次对话结束前（或主要任务完成后），检查是否有活跃任务需要更新：

1. **读 ACTIVE-TASKS.md** — 确认当前有哪些任务
2. **判断本次对话是否涉及某个任务** — 如果是：
   - 更新 `projects/任务名/progress.md` 的进度检查清单
   - 更新「下次开始时需要知道的」部分
   - 更新 ACTIVE-TASKS.md 的「上次更新」和「下一步」列
3. **发现新任务** — 如果本次对话开启了一个新项目：
   - 创建 `projects/任务名/progress.md`
   - 在 ACTIVE-TASKS.md 中添加一行
   - 归档：将 `projects/任务名/` 移至 `projects/_archive/`，从 ACTIVE-TASKS.md 删除，添加到 `CLOSED-TASKS.md`
4. **不需要更新的情况** — 纯闲聊、信息查询、无涉及活跃任务时，跳过此步骤

### 🔍 处理项目任务时：先检查是否有同名任务

当用户提到一个项目/任务名称时，**先在 ACTIVE-TASKS.md 中搜索同名任务**：
- 如果找到 → 读对应 `progress.md`，从断点继续
- 如果没找到 → 视为新任务，创建 `projects/任务名/progress.md` 并更新 ACTIVE-TASKS.md
- 如果不确定是否是旧任务，**先问用户确认**

### 📝 progress.md 必须包含以下 5 个部分

1. **基本信息** — 项目名、编号、截止日期、相关文件路径
2. **进度检查清单** — 用 checkbox 列出所有步骤，标明当前在哪步
3. **关键决策与规则** — 已做出的决定、必须遵守的规则
4. **文件位置** — 相关文件的路径
5. **下次开始时需要知道的** — 用人类语言写给未来自己的备忘录（3-5 条）
```

### 第 3 步：配置心跳兜底（可选）

在 `HEARTBEAT.md` 中添加：

```markdown
### 任务健康检查（每 2-3 次心跳触发一次）
- 读取 ACTIVE-TASKS.md，检查所有活跃任务
- 对超过 7 天未更新的任务 → 提醒
- 检查是否有任务的截止日期在 3 天内 → 紧急提醒
```

## 文件结构

```
~/.openclaw/workspace/
├── ACTIVE-TASKS.md          # 任务索引（所有活跃任务）
├── CLOSED-TASKS.md          # 已归档任务
├── AGENTS.md                # 包含任务管理规则
├── HEARTBEAT.md             # 心跳检查规则
└── projects/
    └── 任务名/
        └── progress.md      # 单个任务的进度文件
```

## 实际效果

- **第 1 天**：在 thread A 讨论某个项目，做到一半
- **第 10 天**：在 thread B 说「继续做那个项目」
- **Agent**：读 ACTIVE-TASKS.md → 找到任务 → 读 progress.md → 知道截止日期、已完成步骤、下一步 → 继续

## 评分

改进前：7/10 → 改进后：8.5/10

## 许可证

MIT-0（自由使用、修改、分发）
