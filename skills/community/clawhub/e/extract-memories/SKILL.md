---
name: extract-memories
version: 3.1.0
description: "对话结束时主动提炼关键记忆到 topic 文件 / 触发词：提炼记忆、提取记忆 / 命令：/extract-memories"
license: MIT
triggers:
  - 提炼记忆
  - 提取记忆
  - extract-memories
  - "/extract-memories"
---

# extract-memories v3.1.0 — 对话记忆提炼

对话结束时主动分析本轮对话，将值得持久化的信息写入 `memory/topics/` 下的独立 topic 文件，同时更新 `MEMORY.md` 索引。

---

## 线性工作流

```
用户输入："提炼记忆" 或 检测到对话结束词
         ↓
Step 1 — 确定本轮对话范围
         读取当前 session 最近消息，确定本轮对话起止
         ↓
Step 2 — 识别值得提炼的内容
         扫描消息，识别：用户决策 / 用户偏好 / 项目约束 / 外部系统指针
         ↓
Step 3 — 按四类型分类
         每个内容 → 判断类型（user/feedback/project/reference）
         feedback 必须含 Why + How to apply
         ↓
Step 4 — 检查 topics/ 是否有重复
         grep 已有 topic，确认没有重复再写
         ↓
Step 5 — 写入 topic 文件（APPEND，不覆盖）
         格式：frontmatter + 正文
         ↓
Step 6 — 更新 MEMORY.md 索引
         添加一行指针（≤150字符）
         ↓
输出："已为您提炼本轮记忆 ✅" + 提炼条数
```

---

## Step 1 — 确定本轮对话范围

读取当前 session 最近消息（不限条数，确保覆盖完整对话）。

---

## Step 2 — 识别值得提炼的内容

识别以下类型的信息：

| 类型 | 特征 | 例子 |
|------|------|------|
| 用户决策 | 用户明确做出了选择或结论 | "用这个方案" |
| 用户偏好 | 用户说了喜欢/不喜欢/习惯 | "我喜欢用 bun" |
| 项目约束 | 截止时间、冻结期、技术限制 | "周五前要上线" |
| 外部系统指针 | URL、工具、账号、路径 | "在 Linear 里有" |

**过滤**：以下不提炼——代码结构、git历史、已在 CLAUDE.md/AGENTS.md 的内容、临时状态。

---

## Step 3 — 按四类型分类

每个内容判断类型：

| 类型 | 判断标准 |
|------|---------|
| `user` | 用户角色、偏好、知识 |
| `feedback` | 用户纠正或确认的行为（含 Why + How to apply） |
| `project` | 截止、动机、约束（含 Why + How to apply） |
| `reference` | 外部系统 URL/路径 + 用途 |

---

## Step 4 — 检查重复

执行 `grep` 搜索已有 topic 文件：
- 相同段落是否已存在
- 相同 URL/路径是否已记录

若有重复，追加新内容到已有文件，不新建。

---

## Step 5 — 写入 topic 文件

**格式（frontmatter）**：

```yaml
---
name: 名称
description: 一句话描述（用于判断 relevance）
type: user / feedback / project / reference
---
正文内容

**Why:** 原因（feedback/project 必须）
**How to apply:** 何时适用（feedback/project 必须）
```

**写入模式**：APPEND，不覆盖已有内容。

---

## Step 6 — 更新 MEMORY.md 索引

在 MEMORY.md 末尾追加一行指针：

```
- [名称](topics/文件名.md) — 一句话 hook（≤150字符）
```

---

## 输出格式

> 已为您提炼本轮记忆 ✅
> 写入位置：memory/topics/
>
> **提炼结果：N条**
>
> ### user
> - [名称]: description
>   正文（一段文字即可）
>
> ### feedback
> - [名称]: description
>   正文
>   **Why:** 原因
>   **How to apply:** 何时适用
>
> ### project
> - [名称]: description
>   正文
>   **Why:** 动机
>   **How to apply:** 如何影响工作
>
> ### reference
> - [名称]: description
>   URL/路径 + 用途说明

---

## What NOT to Save（6条禁止）

1. 代码结构/文件路径（可从源码读取）
2. Git 历史（git log 是权威来源）
3. 调试方案（修复在代码里）
4. CLAUDE.md/AGENTS.md 已有的内容
5. 临时任务状态
6. PR 列表/活动摘要

---

## 触发机制

### 主会话主动触发（主要）

每次对话结束时，主 agent 会：
1. 检测结束模式：中文（`再见`/`bye`/`下次见`/`拜拜`/`结束了`/`先这样`）或英文（`bye`/`see you`/`that's all`）
2. 检测到结束模式 → 主动执行记忆提炼
3. 提炼完成后提示："已为您提炼本轮记忆 ✅"

> 建议在 AGENTS.md 中加入：
> ```
> 对话结束时，主动调用 /extract-memories 提炼关键记忆。
> ```

### Heartbeat 辅助检测

每次 heartbeat 时检查：
- 最近消息是否匹配结束模式
- 或距上次提炼是否超过 30 分钟
- 若满足条件则触发提炼

### 手动触发

- 命令：`/extract-memories`

---

## 权限要求

- `FileRead`：读取对话上下文、MEMORY.md、topics/
- `FileWrite` / `FileEdit`：写入 `memory/topics/`、`MEMORY.md`
- `sessions_history`：读取主会话消息（heartbeat 触发时）

## 触发词

- 自动：主会话主动检测结束模式
- 自动：Heartbeat 辅助检测
- 手动：`/extract-memories`

---

*本 Skill 基于 CC 记忆系统设计，适配 OpenClaw v3.1.0*
