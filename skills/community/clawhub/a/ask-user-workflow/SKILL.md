---
name: ask-user-workflow
description: |
  Structured user consultation workflow — ask clarifying questions,
  then summarize into an actionable plan.
  Activate when the user has a complex/ambiguous task and needs help clarifying direction.
---

# Ask-User Workflow — 提问 + 总结模式

> Distilled from OpenCode's "问问题然后总结" pattern.
> Use when a task is too ambiguous to proceed directly.

---

## 核心思路

用户说"帮我做个XXX"的时候，经常连自己到底要什么都没想清楚。
这时候不要直接开干，也不要问一长串问题把用户烦死。

**正确做法：** 用结构化的 popup 一次性问完，然后自己总结成清晰的任务计划。

---

## 何时使用

- 任务目标模糊，需要澄清
- 有多个方向可选，用户没说选哪个
- 需求涉及多方（功能 + 风格 + 技术选型）
- 用户说"帮我做个XXX"但没有具体细节

**不要用 when:**
- 用户已经给了完整的需求
- 简单问题一个问句就能解决
- 用户明确说"别问了，直接做"

---

## 工作流程

### Step 1: 评估任务

拿到任务后问自己：
1. 我知道要做什么吗？
2. 知道 → 直接做
3. 不知道 → 跳到 Step 2

### Step 2: 问问题（一次性 popup）

用 `ask_user` 工具，把所有相关问题打包成**一个 multi-step popup**。

**规则：**
- 每个问题 1-4 个选项
- 每个步骤最多 4 个选项（popup 自动带"其他..."兜底）
- 问题之间有关联就串起来，无关联就分开
- label 越短越好，不要额外 description

**示例 — 用户说"帮我做个报告系统"：**

```
steps:
  - id: type
    question: "报告系统主要是做什么用途？"
    options:
      - id: notification
        label: "通知公告"
      - id: meeting
        label: "会议纪要"
      - id: weekly
        label: "周报月报"
      - id: audit
        label: "审计报告"
  - id: platform
    question: "部署在哪里？"
    options:
      - id: feishu
        label: "飞书云文档"
      - id: web
        label: "网页端"
      - id: local
        label: "本地文件"
  - id: complexity
    question: "功能要复杂到什么程度？"
    options:
      - id: simple
        label: "只读展示"
      - id: medium
        label: "支持编辑"
      - id: complex
        label: "完整 CRUD"
```

### Step 3: 收到回答，生成任务计划

用户提交 popup 后，读取 response，直接生成结构化任务：

```markdown
## 任务确认

**用途：** [用户选的用途]
**平台：** [用户选的平台]
**复杂度：** [用户选的复杂度]

### 任务分解

1. [子任务 1]
2. [子任务 2]
3. [子任务 3]

### 需要你确认的
- [待确认项 1]
- [待确认项 2]

如果没问题我就开始做了。
```

---

## 决策检查表（什么时候该问）

| 问题 | YES → 直接做 | NO → 问问题 |
|------|-------------|------------|
| 目标清晰吗？ | ✅ | ❌ 问 |
| 方向确定吗？ | ✅ | ❌ 问 |
| 技术栈明确吗？ | ✅ | ❌ 问 |
| 风格/格式有要求吗？ | ✅ | ❌ 问 |
| 涉及多方利益相关者吗？ | ❌ 问 | ✅ |

---

## 问问题的技巧

### ❌ 不要这样问
- "请问您想要 A 还是 B 还是 C 还是 D 还是 E 还是 F 还是 G？"（太多选项）
- "能告诉我更多关于这个项目的细节吗？"（太开放，用户不知道怎么答）
- 分成 10 个 popup 一个一个问（烦死用户）

### ✅ 要这样问
- 选项之间**有明确区别**，用户能直接选
- **短 label**，不要解释选项
- **2-4 个选项**最理想
- 超过 4 个就分类合并

---

## 示例：完整对话

**用户：** "帮我做个东西"
**你：** [评估] → 目标不清晰

**你：** [弹出 ask_user]

**用户选择：**
- type: "周报月报"
- platform: "飞书云文档"
- complexity: "支持编辑"

**你：**

```
## 任务确认

**用途：** 周报月报
**平台：** 飞书云文档
**复杂度：** 支持编辑

### 任务分解

1. 设计周报模板结构（标题/正文/附件）
2. 接入飞书文档 API（读取/写入）
3. 添加周期填写入口（飞书机器人 or 快捷指令？）
4. 支持导出 PDF（可选）
5. 添加提醒机制（可选）

### 确认一下
- 周报是每个人自己填，还是统一模板分发？
- 需要审批流程吗？

没问题我就开始做第 1 步了。
```

---

## 进阶：收集后做分析

如果任务涉及**调研**，可以这样组合：

1. 用 `ask_user` 问清楚调研范围和目标
2. 用 `deep-research` skill 做并行调研
3. 自己汇总成报告
4. 再问一次确认方向

---

## 注意事项

- **问之前先想清楚**：问的问题决定了后续工作的方向，要有关联性
- **不要过度询问**：2-3 个关键问题比 10 个泛泛的问题更有价值
- **给出默认倾向**：如果用户选了"其他..."，给出你的建议
- **语言匹配**：用用户的语言问问题，中文用户用中文问