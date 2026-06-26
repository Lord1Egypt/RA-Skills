---
name: agent-status-monitor
description: 检查本地开发 Agent（Claude Code、OpenCode、OpenClaw、Cursor 等）的运行状态、进程、会话和活动状态。触发词："agents_monitor"、"检查 Claude Code 状态"、"查看 opencode 是否在运行"、"监控开发工具"、"agent 监控"。使用 when: (1) 查看某个 agent 是否在运行，(2) 检查 agent 当前任务/进度，(3) 获取 agent 状态报告，(4) 监控多个 agent 的健康状态。
---

# Agent Status Monitor

检查本地开发工具 Agent 的运行状态和活动状态。

---

## 触发条件

**核心意图**：快速了解本地运行的 AI 开发工具（Agent）是否在运行、是否在工作、是否有会话活动。

**典型场景**：
- 同时运行多个 Agent（Claude Code、OpenCode、OpenClaw），想确认各自状态
- 不确定某个 Agent 是否还在工作，还是已经卡住/闲置
- 想查看哪个 Agent 正在活跃使用，哪个只是后台运行
- 定期检查多个 Agent 的健康状态

**触发示例**：
- "检查 agent 状态"
- "Claude Code 还在工作吗"
- "看看有哪些 agent 在运行"
- "opencode 是不是闲置了"
- "运行 agents_monitor"

---

## 具体成果

**一句话目标**：运行 `agents_monitor` 命令，输出所有本地 Agent 的运行状态（运行中/工作中/闲置/未运行）和会话数量。

**预期输出**：
```
● Claude Code: 🔥 工作中 (2 分钟内有更新) · 13 个会话
● OpenClaw: 🔥 工作中 (2 分钟内有更新) · 1 个会话
● OpenCode: 💤 闲置 (未使用) · 1 个会话
○ Cursor IDE: 未运行
```

**状态说明**：
| 状态 | 含义 |
|------|------|
| 🔥 工作中 | 2 分钟内有会话文件更新 |
| ⏳ 等待中 | 10 分钟内有更新（可能在思考/等待 API） |
| 💤 闲置 | 超过 10 分钟无更新，或未使用 |
| ○ 未运行 | 进程不存在 |

---

## 步骤逻辑

### 执行步骤

1. **运行检测脚本**
   ```bash
   ~/.openclaw/workspace/skills/agent-status-monitor/scripts/check-agents.sh
   ```

2. **进程检测** - 对每个 Agent 执行：
   - `ps aux | grep <agent>` 检查进程是否存在
   - 排除系统误报进程（如 CursorUIViewService）

3. **活动状态判断** - 检查会话目录文件修改时间：
   - 2 分钟内有更新 → 🔥 工作中
   - 10 分钟内有更新 → ⏳ 等待中
   - 超过 10 分钟无更新 → 💤 闲置
   - 只有 1 个文件且超过 5 分钟 → 💤 未使用（初始配置）

4. **输出报告** - 包含：
   - 状态图标 + 文字说明
   - 会话文件数量
   - 详细配置信息（版本、配置路径等）

### 各 Agent 会话目录

| Agent | 会话目录 |
|-------|----------|
| Claude Code | `~/.claude/projects/` |
| OpenClaw | `~/.openclaw/agents/` |
| OpenCode | `~/.local/state/opencode/` |
| Cursor IDE | 进程检测（无统一会话目录） |

### 约束
- 只检测本地运行的 Agent，不涉及云端/远程服务
- 基于文件系统修改时间，不依赖 Agent API
- 仅读取公开目录，不访问私有数据

---

## 正反样例

### ✅ 正例

**输入**：
```
检查 agent 状态
```

**输出**：
```
========================================
   Agent Status Monitor
========================================

--- 进程状态 ---
● Claude Code: 🔥 工作中 (2 分钟内有更新) · 13 个会话
● OpenClaw: 🔥 工作中 (2 分钟内有更新) · 1 个会话
● OpenCode: 💤 闲置 (未使用) · 1 个会话
○ Cursor IDE: 未运行

--- OpenCode 详情 ---
版本：1.2.15
  └─ 配置：~/.config/opencode/opencode.json
  └─ 会话日志：1 个文件

--- OpenClaw 状态 ---
[OpenClaw status 输出...]
```

**输入**：
```
Claude Code 还在工作吗
```

**输出**：
```
Claude Code: 🔥 工作中 (2 分钟内有更新) · 13 个会话
```

### ❌ 反例

**输入**：
```
检查 agent 状态
```

**错误输出**：
```
Claude Code: 运行中
OpenCode: 运行中
```
> ❌ 问题：没有显示活动状态（工作中/闲置），信息不完整

**错误输出**：
```
CPU 使用率：Claude Code 3.7%, OpenCode 0.3%
```
> ❌ 问题：CPU 使用率不可靠，Agent 等待 API 时 CPU 低但仍在工作中

**错误输出**：
```
Claude Code 进程 ID: 12345, 12346, 12347
```
> ❌ 问题：用户不关心进程 ID，关心的是"是否在工作"

---

## 明确限制

### 不做什么

- ❌ **不监控云端 Agent** - 只检测本地进程和文件
- ❌ **不统计 Token 使用量** - 各 Agent 日志格式不统一，暂不支持
- ❌ **不显示进程 ID/内存占用** - 用户关心活动状态，不是系统指标
- ❌ **不控制/停止 Agent** - 只读检测，不执行任何修改操作
- ❌ **不涉及敏感话题** - 纯技术检测，无内容审查

### 异常处理

| 情况 | 处理方式 |
|------|----------|
| 会话目录不存在 | 显示"未运行"或"未安装" |
| 无法读取文件时间 | 降级为仅进程检测 |
| 脚本执行失败 | 输出错误信息 + 建议检查路径 |
| 没有安装任何 Agent | 显示"未检测到任何 Agent" |

### 兜底策略

如果脚本检测失败，返回：
```
⚠️ 无法获取详细状态，尝试手动检查：
ps aux | grep -E "(claude|opencode|openclaw)" | grep -v grep
```

### 已知限制

1. **Cursor IDE** - 没有统一会话目录，仅进程检测
2. **新 Agent 类型** - 需要手动添加检测逻辑
3. **跨用户检测** - 只能检测当前用户的 Agent
4. **容器/Docker** - 不检测容器内运行的 Agent

---

## 相关资源

- `scripts/check-agents.sh` - 主检测脚本
- `references/agent-commands.md` - 各 Agent 命令参考

## 更新日志

- 基于会话文件修改时间判断活动状态（比 CPU 使用率更可靠）
- 支持 Claude Code、OpenCode、OpenClaw、Cursor IDE
- 提供 `agents_monitor` 命令别名
