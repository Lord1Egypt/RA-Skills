<div align="center">

# Context Archive

### 管理你的 AI 对话上下文

[中文](#中文) | [English](./README.md)

</div>

---

## 中文

一个 [OpenClaw](https://github.com/openclaw/openclaw) 技能，让用户主动管理对话生命周期：**归档 → 释放上下文 → 按需召回**。

### 解决什么问题

如果你用一个对话框搞定所有事情，上下文窗口会越堆越满。旧话题污染新对话，agent 注意力分散，token 白白浪费在无关的历史记录上。

### 怎么解决

Context Archive 提供三个核心动作：

| 动作 | 作用 |
|------|------|
| **归档** | 把一段对话压缩成摘要，存为 `.md` 文件 |
| **列出** | 显示所有存档的标题、日期和摘要 |
| **召回** | 把某个存档加载回当前上下文 |

### 使用示例

```
你: 归档最近关于激光投影的讨论
AI: [生成摘要] 以上是摘要。有没有遗漏的重要细节？
你: 补充一下，IMU漂移的解决方案那部分要保留
AI: 已更新。标题建议：2026-07-31-激光投影方案。确认？
你: 确认
AI: 已归档至 archives/2026-07-31-激光投影方案.md

--- 过了一会儿 ---

你: 有哪些存档
AI: 1. 2026-07-31-激光投影方案 → 激光追踪显示方案对比
    2. 2026-07-15-GitHub统计 → 仓库星数和流量分析

你: 加载第一个
AI: 已加载归档：激光投影方案。关键信息已恢复。
```

### 归档触发方式

- **按主题**: "归档关于XX的讨论"
- **相对时间**: "归档最近2小时的对话"
- **绝对时间**: "归档7/21下午3点到5点的对话"
- **整天**: "归档今天的对话"
- **最近（默认）**: "归档最近的对话"

### 细节确认

生成摘要后，agent 会主动询问是否有遗漏的重要细节。你可以指出具体是哪些对话内容，agent 会补充进归档。最多确认两轮，确保关键信息不丢失。

### 安装

```bash
clawhub install Thomaszhou22/context-archive-skill
```

或者手动把 `SKILL.md` 复制到你的 OpenClaw skills 目录。

### 归档文件格式

每个归档是一个结构化的 Markdown 文件：

```markdown
# 标题

> Archived: 2026-07-31 23:49
> Period: 23:00 — 23:49
> Messages: 15

## Summary
{叙述性摘要}

## Key Points
- {重要事实}

## User-Supplied Details
- {用户在细节确认环节补充的内容}

## Decisions
- {做出的决策}

## Files Modified
- 路径/文件名: 改了什么

## Keywords
标签1, 标签2, 标签3
```

### 环境要求

- [OpenClaw](https://github.com/openclaw/openclaw) v2.0+
- 工作目录下 `archives/` 的写入权限

### 技术栈

- 零依赖，纯技能定义文件
- 复用 OpenClaw 内置的 `memory_search`、`read`、`write` 工具

### License

MIT
