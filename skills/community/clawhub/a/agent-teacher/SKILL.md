---
name: agent-teacher
description: 教授新 agent 掌握工作室基础能力的技能。触发时机：(1) 创建新 agent 后需要初始化配置时 (2) 教现有 agent 掌握某项技能时 (3) 新 agent 上岗培训。课程分"行为准则→基础→进阶"三大类，行为准则必须优先于一切技能学习。
---

# Agent Teacher

教授新 agent 掌握工作室基础能力的技能。

## 课程理念

- **准则优先**：行为准则必须先于一切技能学习，准则比技能更重要
- **基础扎实**：技能让 Agent 做事情，准则让 Agent 不犯错
- **循序渐进**：按顺序完成课程，不要跳跃
- **不重复记录**：已经学过并记住的内容不要重复记录，直接巩固现有知识点即可

---

## 课程体系

### 行为准则（必修第一课）

**必须先于所有技能学习！** 准则违规比技能不熟练更严重。

| 课程 | 内容 |
|------|------|
| `rules-of-conduct` | 工作室行为准则（约15条核心规则） |

详见 `references/rules-of-conduct.md`

### 身份定制（必修第1.5课）

**在安装任何技能之前必须完成！** 定义你是谁、你的工作规范。这些文件必须**中文编写**。

| 课程 | 内容 |
|------|------|
| `phase-0-identity` | SOUL.md、IDENTITY.md、AGENTS.md 定制 |

详见 `references/phase-0-identity.md`

### 基础课程（必修）

在行为准则学习后进行。

| 分类 | 技能 | 安装 |
|------|------|------|
| **持续存在** | daily-log, memory-review, daily-backup, todo-list | clawhub 安装 |
| **沟通协作** | feishu-send, contacts, sessions_send | 部分安装部分内置 |
| **知识检索** | memory_search, memory_get | 内置 |
| **飞书文档** | feishu_doc/wiki/bitable | 内置 |
| **系统维护** | health-check, dependency-tracker | clawhub 安装 |

详见 `references/phase-1-foundation.md`

### 进阶课程（选修）

按需学习，用于专业任务。

| 分类 | 技能 | 安装 |
|------|------|------|
| **搜索** | mmx-cli, multi-search-engine | mmx-cli 优先，mcporter 备选 |
| **浏览器** | browser | 内置需启用 |
| **外部服务** | mcporter | 需配置key |
| **视觉** | canvas, image, mmx-cli | image 理解用内置工具，生图用 mmx-cli |
| **技能开发** | skill-creator, clawhub | 部分内置部分安装 |

详见 `references/phase-2-advanced.md`

---

## 新 agent 上岗教学流程

### Step 1: 学习行为准则（必须第一个）

读取并理解 `references/rules-of-conduct.md`
→ 确认理解后再进行下一步

### Step 2: 安装并学习基础技能

```bash
cd /home/axelhu/.openclaw/workspace/[agent-name]
mkdir -p skills

# 基础技能
clawhub install daily-log --dir skills
clawhub install memory-review --dir skills
clawhub install daily-backup --dir skills
clawhub install todo-list --dir skills
clawhub install feishu-send --dir skills
clawhub install health-check --dir skills
clawhub install dependency-tracker --dir skills
cp -r /home/axelhu/.openclaw/workspace/skills/contacts skills/

# sessions_send、memory_search、memory_get、feishu_doc/wiki/bitable、skill-creator 已内置
```

### Step 3: 验证掌握

- 行为准则：能复述至少 5 条核心规则
- 基础技能：能发日报、能搜记忆、能给其他 agent 发消息

### Step 4: 进阶按需学习

根据角色和任务需要，安装进阶技能。

---

## 详细课程资料

- 行为准则：`references/rules-of-conduct.md`
- 基础技能：`references/phase-1-foundation.md`
- 进阶技能：`references/phase-2-advanced.md`

## 汇报模板

```
已完成 [agent-name] 上岗培训 ✅
行为准则：✅ 已掌握（能复述核心规则）
基础技能：✅ daily-log, memory-review, daily-backup, todo-list, feishu-send, contacts, health-check
进阶技能：按需安装
```

## 触发示例

- "教 zero-producer 上岗培训"
- "新 agent 上岗，按顺序教学"
- "给 programmer 补行为准则"
