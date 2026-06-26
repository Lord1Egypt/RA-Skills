---
name: conversation-analyzer
description: 智能对话分析总结，分析用户个人特征、追踪任务、检查未完成任务，并写入记忆文件
version: 1.0.0
author: opendolph
source: https://github.com/opendolph/skills/tree/main/conversation-analyzer
---

# 对话分析总结器 🧠

> 智能分析对话，总结记录结论，追踪未完成任务

---

## 核心功能

### 1. 用户个人特征分析

**分析维度：**
- **个人特征**：性格、沟通风格、决策模式
- **喜好**：技术偏好、工具选择、内容类型
- **技能**：技术栈、专业能力、熟悉领域
- **个人经历**：职业路径、项目经验、成长轨迹
- **背景**：工作环境、团队角色、行业背景
- **情绪状态**：压力水平、满意度、关注点
- **现在做的事情**：当前项目、重点任务、日常活动
- **以后想做的事情**：目标、计划、期望

**执行动作：**
- 读取 USER.md 现有记录
- 合并新分析结果
- 更新 USER.md
- 如有需要调用合适的 skill 工具

### 2. 对话任务与需求分析

**分析维度：**
- **已要求的事情**：具体任务、完成状态
- **预测后续需求**：基于模式预测下一步
- **错误记录**：理解偏差、执行错误、改进点

**执行动作：**
- 读取 MEMORY.md 中的"对话分析"记录
- 增量写入新分析结果
- 如有需要调用合适的 skill 工具

### 3. 未完成任务检查

**检查范围：**
- 对话中提到的待办事项
- 承诺但未完成的事项
- 排除 MEMORY.md 中标记"不需要完成"的任务

**执行动作：**
- 列出未完成任务
- 通过 Feishu 发送询问消息
- 如无未完成任务，发送"未发现未完成的任务"

---

## 触发条件

| 场景 | 触发方式 |
|------|----------|
| 自动触发 | 每10次对话（通过 HEARTBEAT.md 计数器） |
| 定时触发 | 每天 12:00 和 24:00（cron） |
| 手动触发 | 用户输入「分析对话」「总结」「检查任务」 |

---

## 分析工作流程

### 每10次对话

```
对话计数器 +1
    ↓
计数器 >= 10?
    ↓ 是
重置计数器
    ↓
执行3项分析任务
    ↓
更新记忆文件
```

### 每日定时分析（12:00, 24:00）

```
Cron 触发
    ↓
分析 0:00 到当前时间的所有对话
    ↓
执行3项分析任务
    ↓
更新记忆文件
    ↓
通过 Feishu 发送未完成任务通知
```

---

## 文件操作

### 输入文件
- `HEARTBEAT.md` - 对话计数器、任务追踪
- `USER.md` - 用户个人档案记录
- `MEMORY.md` - 长期记忆、对话分析历史
- `SESSION-STATE.md` - 当前会话状态
- 对话历史（通过 sessions_history 工具获取）

### 输出文件
- `USER.md` - 更新后的用户档案
- `MEMORY.md` - 追加的对话分析记录
- `HEARTBEAT.md` - 重置对话计数器
- Feishu 消息 - 任务通知

---

## 使用方法

```bash
# 手动触发分析
node skills/conversation-analyzer/scripts/analyze.js

# 仅检查未完成任务
node skills/conversation-analyzer/scripts/check-tasks.js

# 每日完整分析（0:00 到现在）
node skills/conversation-analyzer/scripts/daily-analysis.js
```

---

## Cron 配置

### 添加到 crontab

```bash
# 每天 12:00 和 24:00 执行分析
0 12,0 * * * cd ~/.openclaw/workspace && node skills/conversation-analyzer/scripts/daily-analysis.js > /dev/null 2>&1
```

### 或使用 OpenClaw cron

```bash
openclaw cron add "0 12,0 * * *" "conversation-analyzer/daily-analysis"
```

---

## 与 HEARTBEAT.md 集成

本技能读取并更新 HEARTBEAT.md：

```markdown
## 对话计数器
- 当前对话次数：0
- 上次分析时间：2026-03-24 21:00
- 分析阈值：每10次对话
```

当计数器达到10时：
1. 执行个人特征分析
2. 执行任务分析
3. 执行未完成任务检查
4. 重置计数器为0

---

## 任务状态定义

| 状态 | 含义 |
|------|------|
| Queue | 等待开始 |
| Active | 进行中 |
| Waiting | 阻塞/等待 |
| Done | 已完成 |
| Aborted | 已取消 |
| NotNeeded | 明确标记为不需要完成 |

---

*将被动响应转化为主动洞察 🎯*
