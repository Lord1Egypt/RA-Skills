# Conversation Analyzer 🧠

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

An intelligent conversation analysis skill for OpenClaw that analyzes user personality, tracks tasks, checks incomplete tasks, and writes conclusions to memory files.

### Features

- 🧠 **User Personality Analysis** - Analyze personality, preferences, skills, experience, background, emotional state
- 📋 **Task Tracking** - Track requested tasks, predict future needs, record errors
- ✅ **Incomplete Task Check** - Detect todos, send Feishu notifications
- 🔄 **Auto-trigger** - Every 10 conversations or daily via cron
- 💾 **Memory Integration** - Writes to USER.md and MEMORY.md

### Installation

```bash
npx skills add opendolph/conversation-analyzer
```

### Quick Start

```bash
# Manual trigger full analysis
cd ~/.openclaw/workspace
node skills/conversation-analyzer/scripts/analyze.js

# Check incomplete tasks only
node skills/conversation-analyzer/scripts/check-tasks.js

# Daily analysis (0:00 to now)
node skills/conversation-analyzer/scripts/daily-analysis.js
```

### Setup Cron Jobs

#### Option 1: System crontab

```bash
# Edit crontab
crontab -e

# Add these lines
# Daily analysis at 12:00 and 24:00
0 12,0 * * * cd ~/.openclaw/workspace && node skills/conversation-analyzer/scripts/daily-analysis.js > /dev/null 2>&1
```

#### Option 2: OpenClaw cron

```bash
openclaw cron add "0 12,0 * * *" "conversation-analyzer/daily-analysis"
```

### HEARTBEAT.md Integration

Add to your HEARTBEAT.md:

```markdown
## Conversation Counter
- Current count: 0
- Last analysis: not executed
- Threshold: 10 conversations

## Analysis Tasks (Auto-trigger every 10 conversations)

### 1. User Personality Analysis
Analyze: personality, preferences, skills, experience, background, emotional state, current activities, future goals
→ Update USER.md

### 2. Conversation Task Analysis
Analyze: requested tasks, predicted needs, error records
→ Append to MEMORY.md "Conversation Analysis" section

### 3. Incomplete Task Check
Check: todos in conversation, promised but incomplete items
→ Send Feishu notification
```

### Analysis Dimensions

#### User Personality
| Dimension | Description |
|-----------|-------------|
| Personal Traits | Personality, communication style, decision patterns |
| Preferences | Tech preferences, tool choices, content types |
| Skills | Tech stack, professional capabilities |
| Experience | Career path, project experience |
| Background | Work environment, team role, industry |
| Emotional State | Stress level, satisfaction, focus |
| Current Activities | Current projects, key tasks |
| Future Goals | Goals, plans, expectations |

#### Task Status
| Status | Meaning |
|--------|---------|
| Queue | Waiting to start |
| Active | In progress |
| Waiting | Blocked/Waiting |
| Done | Completed |
| Aborted | Cancelled |
| NotNeeded | Explicitly not required |

---

<a name="中文"></a>
## 中文

OpenClaw 智能对话分析技能，分析用户个人特征、追踪任务、检查未完成任务，并将结论写入记忆文件。

### 功能特点

- 🧠 **用户个人特征分析** - 分析性格、喜好、技能、经历、背景、情绪状态
- 📋 **任务追踪** - 追踪要求的任务、预测后续需求、记录错误
- ✅ **未完成任务检查** - 检测待办事项，发送飞书通知
- 🔄 **自动触发** - 每10次对话或通过 cron 每日执行
- 💾 **记忆集成** - 写入 USER.md 和 MEMORY.md

### 安装

```bash
npx skills add opendolph/conversation-analyzer
```

### 快速开始

```bash
# 手动触发完整分析
cd ~/.openclaw/workspace
node skills/conversation-analyzer/scripts/analyze.js

# 仅检查未完成任务
node skills/conversation-analyzer/scripts/check-tasks.js

# 每日分析（0:00 到现在）
node skills/conversation-analyzer/scripts/daily-analysis.js
```

### 配置 Cron 任务

#### 方式一：系统 crontab

```bash
# 编辑 crontab
crontab -e

# 添加以下行
# 每天 12:00 和 24:00 执行分析
0 12,0 * * * cd ~/.openclaw/workspace && node skills/conversation-analyzer/scripts/daily-analysis.js > /dev/null 2>&1
```

#### 方式二：OpenClaw cron

```bash
openclaw cron add "0 12,0 * * *" "conversation-analyzer/daily-analysis"
```

### HEARTBEAT.md 集成

添加到你的 HEARTBEAT.md：

```markdown
## 对话计数器
- 当前对话次数：0
- 上次分析时间：未执行
- 分析阈值：每10次对话

## 分析任务（每10次对话自动触发）

### 1. 用户个人特征分析
分析：性格、喜好、技能、经历、背景、情绪状态、当前活动、未来目标
→ 更新 USER.md

### 2. 对话任务分析
分析：要求的任务、预测的需求、错误记录
→ 追加到 MEMORY.md "对话分析" 部分

### 3. 未完成任务检查
检查：对话中的待办、承诺但未完成的事项
→ 发送飞书通知
```

### 分析维度

#### 用户个人特征
| 维度 | 说明 |
|------|------|
| 个人特征 | 性格、沟通风格、决策模式 |
| 喜好 | 技术偏好、工具选择、内容类型 |
| 技能 | 技术栈、专业能力 |
| 经历 | 职业路径、项目经验 |
| 背景 | 工作环境、团队角色、行业 |
| 情绪状态 | 压力水平、满意度、关注点 |
| 当前活动 | 当前项目、重点任务 |
| 未来目标 | 目标、计划、期望 |

#### 任务状态
| 状态 | 含义 |
|------|------|
| Queue | 等待开始 |
| Active | 进行中 |
| Waiting | 阻塞/等待 |
| Done | 已完成 |
| Aborted | 已取消 |
| NotNeeded | 明确不需要完成 |

---

## License

MIT © opendolph
