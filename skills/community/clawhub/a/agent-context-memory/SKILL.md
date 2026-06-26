---
name: context-management
description: "Agent 上下文管理方法论：通过分层文件体系实现跨 session 记忆延续、职责分离和高效上下文恢复。Use when: (1) 搭建新 agent 工作区, (2) 优化 agent 记忆和上下文管理, (3) 长期运行 agent 的记忆维护。"
version: 1.0.0
author: linhan
---

# Agent 上下文管理方法论 (context-management)

让 AI Agent 跨 session 保持记忆、快速恢复上下文、持续积累经验。

**核心理念：文件 > 大脑。写下来，别靠"记住"。**

---

## 问题

每次新 session，agent 都是全新的——没有记忆、没有上下文、没有教训。导致：

- 重复犯同样的错误
- 每次都要重新交代背景
- 无法积累长期经验
- 上下文窗口浪费在重复信息上

## 解决方案

**分层文件体系 + 启动协议 + 记忆生命周期管理**

```
Session 启动
    ↓
读身份（SOUL.md）→ 读用户（USER.md）→ 读近期记忆（memory/）→ 读长期记忆（MEMORY.md）
    ↓
带着完整上下文开始工作
    ↓
工作中产生的经验 → 写入 memory/YYYY-MM-DD.md
    ↓
定期提炼 → 精华进 MEMORY.md → 过时内容清理
```

---

## 架构：五层文件体系

### 第一层：身份层

**`SOUL.md`** — Agent 是谁

定义 agent 的人格、原则和行为边界。这不是 system prompt 的复制品，而是 agent 自己的"灵魂文件"。

应包含：
- 身份定位（你是什么，不是什么）
- 核心原则（做事风格、决策哲学）
- 沟通风格（语言、详略、语气）
- 行为边界（什么能做、什么先问）

```markdown
# SOUL.md

## 身份
你是一个 [领域] 的 AI 执行者。你的职责是 [核心职责]。

## Core Truths
- 做事，不做戏。跳过客套，直接给结果
- 先自己解决，再来问。至少试过三种方式
- 出错了就直说，然后把教训写进记忆

## 沟通风格
默认 [语言]。先说结论，再说过程。

## 边界
- 读文件、搜索、整理 → 直接做
- 发消息、发布内容 → 先确认
- 删除、覆盖 → 说一声再做
```

**关键原则：** 这个文件属于 agent 自己。随着 agent 逐渐明确自己的风格，应该自主更新。修改时通知用户。

### 第二层：用户层

**`USER.md`** — 服务谁

记录用户的基本信息和工作上下文，让 agent 每次启动就知道在帮谁。

应包含：
- 时区、语言偏好
- 工作背景（做什么、关注什么）
- 定时任务表
- 习惯和偏好

```markdown
# USER.md

- **Timezone:** Asia/Shanghai (UTC+8)
- **Language:** 中文

## Context
- 运营 [项目名]，需要持续 [核心需求]
- 使用 [工具列表] 作为日常工具
- 重视效率和自动化

## 定时任务
| 时间 | 任务 | 技能 |
|------|------|------|
| 0:00 | 日志归档 | `dialogue-logger` |
| 9:00 | 日报推送 | `token-tracker` |
```

**关键原则：** 只放用户级信息，不放技能配置或机器环境。

### 第三层：路由层

**`AGENTS.md`** — 怎么工作

定义 session 启动协议、技能路由表、常见工作流。这是 agent 的"操作手册"。

应包含：
- 启动协议（每次 session 读什么、按什么顺序）
- 技能路由表（什么场景用什么技能）
- 常见工作流（多步骤任务的标准流程）
- 上下文管理规则（何时清理、何时新建 session）

```markdown
# AGENTS.md

## 每次会话
1. 读 SOUL.md
2. 读 USER.md
3. 读 memory/YYYY-MM-DD.md（今天 + 昨天）
4. 主会话额外读 MEMORY.md

## 技能路由
| 类别 | 技能 | 触发场景 |
|------|------|---------|
| 内容 | `news-writer` | "写新闻" |
| 搜索 | `web-search` | 事实核查 |

## 上下文管理
主动清理 session 的时机：
- 定时任务全部完成后
- 长内容创作任务前
- 大量工具调用积累后
- 对话超过 20 轮或包含大量搜索结果
```

### 第四层：环境层

**`TOOLS.md`** — 本机配置

记录当前机器的具体环境配置。Skills 定义工具怎么用，TOOLS.md 记录这台机器上的实际参数。

应包含：
- 浏览器配置（端口、profile）
- 文件系统路径（知识库、日志位置）
- 定时任务实际脚本路径
- 外部服务连接信息

```markdown
# TOOLS.md

## 浏览器
Chrome CDP 端口: 19792
配置: ~/.openclaw/openclaw.json

## 知识库
路径: ~/Documents/笔记/
关键文件夹:
- 01-新闻/ — 新闻存储
- 06-对话/ — 对话归档

## 定时任务
| 时间 | 脚本路径 |
|------|---------|
| 0:00 | skills/dialogue-logger/scripts/auto.js |
```

**关键原则：** 换一台机器只需改这个文件，其他文件不用动。

### 第五层：记忆层

最核心的一层，分为**短期记忆**和**长期记忆**。

#### `memory/YYYY-MM-DD.md` — 短期记忆（每日原始记录）

每天一个文件，记录当天的工作细节。格式自由，但建议包含：
- 做了什么（任务描述 + 结果）
- 遇到什么问题（错误信息 + 排查过程）
- 学到什么（可复用的技术经验）
- 待办（未完成的事项）

```markdown
# 2026-03-10 工作记录

## 小红书发布修复
- **问题**: 标题输入框匹配失败
- **修复**: 扩展匹配关键词，添加 3 次重试机制
- **教训**: 页面元素匹配不能只靠单一关键词

## 待办
- [ ] 测试新的重试逻辑
```

#### `MEMORY.md` — 长期记忆（提炼精华）

从每日记忆中提炼的**不可复现经验**。不放静态配置，不放可以从代码推导的信息。

```markdown
# MEMORY.md

## 技术教训

### 浏览器自动化（2026-03-10）
- 页面元素匹配必须用多关键词 + 重试，单一匹配不可靠
- macOS cron 默认无 Full Disk Access，需手动授权

### 工作区原则
- MEMORY.md 只留不可复现的经验，不放静态配置
- 核心文件职责单一，避免交叉重复
```

**筛选标准：** 写入 MEMORY.md 之前问自己——"这条经验能从代码或文档推导出来吗？"能推导就不写。

---

## 记忆生命周期

```
日常工作 → 写入 memory/YYYY-MM-DD.md（即时）
    ↓
定期回顾 → 提炼到 MEMORY.md（每周 1 次）
    ↓
清理过时内容 → 删除或归档旧的 daily 文件
    ↓
长期精华持续积累，短期细节定期淘汰
```

### 心跳维护机制

通过定期心跳触发记忆维护，而非靠人工提醒：

**`HEARTBEAT.md`** — 定义心跳行为

```markdown
# HEARTBEAT.md

## 默认行为
大部分心跳直接返回 HEARTBEAT_OK，不做工具调用。

## 记忆维护
每周利用一次心跳：
1. 阅读近期 memory/ 文件
2. 提炼精华到 MEMORY.md
3. 清理过时内容
4. 记录维护时间到 heartbeat-state.json
```

状态追踪文件 `memory/heartbeat-state.json`：

```json
{
  "lastChecks": {
    "memoryMaintenance": 1741829443,
    "heartbeat": 1741829443
  }
}
```

---

## 双源搜索策略

当需要历史上下文时，不只搜记忆文件——结合外部知识库双源检索：

```
用户提问
    ↓
需要历史上下文？
    ├── 否 → 直接回答
    └── 是 → 搜本地记忆 + 搜知识库
              ↓
         合并生成回复
```

搜索优先级：
1. **配置类问题** → MEMORY.md + TOOLS.md
2. **历史对话**（触发词：之前、上次、以前）→ 对话归档目录
3. **知识类问题** → 本地记忆 + 知识库合并

---

## 快速上手

### Step 1：创建核心文件

在工作区根目录创建五个文件：

```
workspace/
├── SOUL.md        # 身份层：agent 是谁
├── USER.md        # 用户层：服务谁
├── AGENTS.md      # 路由层：怎么工作
├── TOOLS.md       # 环境层：本机配置
├── MEMORY.md      # 长期记忆
├── HEARTBEAT.md   # 心跳规则（可选）
└── memory/        # 短期记忆目录
    └── .gitkeep
```

### Step 2：配置启动协议

在 AGENTS.md 中定义 session 启动顺序：

```markdown
## 每次会话
1. 读 SOUL.md — 你是谁
2. 读 USER.md — 你在帮谁
3. 读 memory/YYYY-MM-DD.md（今天 + 昨天）— 近期发生了什么
4. 主会话额外读 MEMORY.md — 长期经验
```

### Step 3：养成写记忆的习惯

在 AGENTS.md 或 SOUL.md 中加入强制规则：

```markdown
有人说"记住这个" → 写文件
学到教训 → 更新对应文档
出了错 → 写进 memory/YYYY-MM-DD.md
```

### Step 4：设定清理节奏

每周一次记忆维护：daily 文件提炼 → MEMORY.md 更新 → 过时内容清理。

---

## 设计原则

| 原则 | 说明 |
|------|------|
| **单一职责** | 每个文件只管一件事，SOUL 管身份、USER 管用户、TOOLS 管环境 |
| **文件 > 大脑** | 所有重要信息写文件，不靠 session 内"记住" |
| **分层加载** | 不是每次都读所有文件，按需加载节省上下文窗口 |
| **写入即时，提炼定期** | daily 文件随时写，MEMORY.md 定期提炼 |
| **可复现的不存** | MEMORY.md 只放不能从代码/文档推导的经验 |
| **换机器只改一个文件** | 环境差异全部隔离在 TOOLS.md |

---

## 自动提炼脚本

`scripts/memory_distill.py` 自动扫描 `memory/YYYY-MM-DD.md`，提取"技术收获"和"问题+修复"对，去重后追加到 `MEMORY.md`。

### 用法

```bash
cd ~/.openclaw/workspace

# 处理最近 7 天的 daily 文件（默认）
python3 skills/context-management/scripts/memory_distill.py

# 处理最近 30 天
python3 skills/context-management/scripts/memory_distill.py --days 30

# 处理所有未处理的文件
python3 skills/context-management/scripts/memory_distill.py --all

# 只预览，不写入
python3 skills/context-management/scripts/memory_distill.py --dry-run

# 忽略已处理记录，强制重新处理
python3 skills/context-management/scripts/memory_distill.py --all --force
```

### 提取规则

| 类型 | 匹配条件 | 说明 |
|------|---------|------|
| 技术收获 | H2/H3 标题含"技术收获""教训""经验总结"等关键词 | 整段提取，自动过滤待办项 |
| 问题+修复 | H3 段落中同时出现 `**问题**:` 和 `**修复**:` | 只提取问题/修复行，去噪 |

### 去重机制

- 对比 MEMORY.md 已有内容，超过 50% 行重复则跳过
- 通过 `memory/distill-state.json` 记录已处理文件，避免重复扫描

### 接入 cron（可选）

```bash
# 每周日 23:00 自动提炼
0 23 * * 0 cd ~/.openclaw/workspace && python3 skills/context-management/scripts/memory_distill.py --all >> logs/memory_distill.log 2>&1
```

---

## 文件结构

```
skills/context-management/
├── SKILL.md                          # 方法论文档
└── scripts/
    └── memory_distill.py             # 自动提炼脚本
```

---

## 适用场景

- 长期运行的 AI Agent（OpenClaw、Cursor Agent、自定义 agent）
- 需要跨 session 保持上下文的任何 agent 框架
- 多 agent 协作场景（通过共享 MEMORY.md 传递经验）
- 个人 AI 助手的记忆管理

## 不适用场景

- 单次问答、不需要持续运行的场景
- 上下文窗口极小（< 8K token）的模型
