---
name: context-handoff
description: 保存和恢复聊天上下文到本地文件。用于用户想在切换账号、清空 session、重新开会话、跨会话延续项目时，把当前会话级上下文或项目级摘要落盘并在之后恢复。也用于列出已有的会话上下文槽位或项目摘要，并按更新时间排序返回最近使用项。触发词包括：保存当前上下文、保存会话摘要、保存项目摘要、记下这次讨论、切号前保存、恢复上下文、恢复项目摘要、读取上次摘要、继续上次讨论、列出上下文槽位、列出已保存摘要、有哪些项目摘要、最近更新的项目摘要、按更新时间排序、session handoff, context handoff, save session context, save current context, save chat summary, save project summary, restore context, restore session context, restore project summary, continue last discussion, resume project context, list context slots, list project summaries, list saved summaries, sort by updated time, most recently updated, recently updated summaries, chat handoff, project handoff.
---

# Context Handoff

把“账号切换 / session 清理”和“项目上下文延续”拆开处理。
不要依赖聊天窗口历史天然保留；需要延续的内容必须落盘到本地文件。

## 使用目标

支持两类本地文件：

1. **会话级上下文**：绑定某个具体聊天窗口/对话用途
2. **项目级摘要**：绑定某个项目本身，与具体聊天窗口解耦

推荐目录：

- 会话级：`/root/.openclaw/workspace/handoffs/sessions/`
- 项目级：`/root/.openclaw/workspace/projects/`

## 何时使用哪一种

### 会话级上下文

当用户表达下面这些意思时，保存到：

- “保存当前对话摘要”
- “把这个会话记下来”
- “切号前保存一下上下文”
- “下次回这个聊天框继续”

会话级文件建议命名：

- `handoffs/sessions/<slot>.md`

如果拿不到系统级 session id，不要假装知道“当前聊天窗口是谁”。
让用户自己给一个 **上下文槽位名**，例如：

- `main-chat`
- `oauth-switch-chat`
- `project-a-thread`

### 项目级摘要

当用户表达下面这些意思时，保存到：

- “保存这个项目的进展”
- “记一下这个项目目前做到哪了”
- “以后恢复这个项目”
- “做个项目摘要”

项目级文件建议命名：

- `projects/<project-name>.md`

项目名由用户指定；如果没有指定，先问。

## 执行动作

### A. 列出会话级上下文槽位

当用户要求列出已有会话级上下文时：

1. 查看目录：
   - `/root/.openclaw/workspace/handoffs/sessions/`
2. 列出其中所有 `.md` 文件
3. 按文件最后修改时间倒序排序（最近更新的放前面）
4. 返回时优先给出：
   - 槽位名
   - 最后更新时间
   - 文件路径
5. 如果目录不存在或为空，明确告诉用户还没有已保存的会话级上下文

实现时优先使用能直接读到文件 mtime 的方式；不要按文件名排序来冒充“最近更新”。

### B. 保存会话级上下文

当用户要求保存会话级上下文时：

1. 如果用户没有给 `slot` 名，先问一个简短问题：
   - “要保存到哪个上下文槽位名？例如 `main-chat` / `oauth-switch-chat`”
2. 生成结构化摘要，不要直接整段复制聊天记录
3. 写入：
   - `/root/.openclaw/workspace/handoffs/sessions/<slot>.md`
4. 如果目录不存在，先创建
5. 覆盖写入为最新版本（默认不做历史堆叠，除非用户明确要求追加）

推荐内容结构：

```md
# 会话级上下文

- 槽位名：
- 保存时间：
- 当前讨论主题：
- 已完成：
- 当前决定：
- 未完成 / 下一步：
- 关键文件：
- 关键命令：
- 备注：
```

### C. 恢复会话级上下文

当用户要求恢复会话级上下文时：

1. 如果没有给 `slot` 名，先问
2. 读取：
   - `/root/.openclaw/workspace/handoffs/sessions/<slot>.md`
3. 用简洁方式把内容总结给用户
4. 不要把整份 markdown 原样全贴，除非用户要求“完整显示”

### D. 列出项目级摘要

当用户要求列出已有项目摘要时：

1. 查看目录：
   - `/root/.openclaw/workspace/projects/`
2. 列出其中 `.md` 文件
3. 排除明显不是项目摘要的全局说明文件（例如通用 README，可按上下文判断）
4. 按文件最后修改时间倒序排序（最近更新的放前面）
5. 返回时优先给出：
   - 项目名
   - 最后更新时间
   - 文件路径
6. 如果没有合适结果，明确告诉用户还没有已保存的项目摘要

实现时优先使用能直接读到文件 mtime 的方式；不要按文件名排序来冒充“最近更新”。

### E. 保存项目级摘要

当用户要求保存项目级摘要时：

1. 如果没有给项目名，先问
2. 生成结构化项目摘要
3. 写入：
   - `/root/.openclaw/workspace/projects/<project-name>.md`
4. 默认覆盖更新为“当前项目最新状态”

推荐内容结构：

```md
# <项目名>

- 更新时间：
- 项目目标：
- 当前进展：
- 已完成：
- 关键决定：
- 风险 / 注意事项：
- 关键文件：
- 关键命令：
- 下一步：
```

### F. 恢复项目级摘要

当用户要求恢复项目级摘要时：

1. 如果没有给项目名，先问
2. 读取：
   - `/root/.openclaw/workspace/projects/<project-name>.md`
3. 优先返回：
   - 当前进展
   - 已完成
   - 下一步
   - 风险 / 注意事项

## 写作要求

- 用中文写摘要
- 以“恢复工作状态”为目标，不要写成长篇会议纪要
- 重点保留决定、文件、命令、下一步
- 不要把敏感 token、密钥、cookie、完整账号凭据写进去

## 回答风格

### 保存成功时

告诉用户：

- 已保存什么类型（会话级 / 项目级）
- 保存到哪个文件
- 后续恢复该用什么关键词

例如：

- “已把当前会话上下文保存到 `handoffs/sessions/main-chat.md`。下次你说‘恢复 main-chat 上下文’就行。”
- “已把项目摘要保存到 `projects/oauth-switch.md`。下次你说‘恢复 oauth-switch 项目摘要’即可。”

### 恢复时

优先给用户一个压缩版恢复结果，例如：

- 当前在做什么
- 已完成什么
- 下一步是什么

必要时再补充文件路径和命令。

## 重要约束

- 不要假设终端脚本知道“当前聊天窗口”是谁
- 如果用户没有提供槽位名或项目名，先问
- 默认覆盖更新，不要无限追加导致文件越来越乱
- 如果文件不存在，明确告诉用户“还没有保存过这份上下文”
