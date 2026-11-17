---
name: context-archive
version: 1.1.0
description: User-driven conversation archiving for AI agents. Archive by topic or time, free context, recall on demand.
---

# Context Archive

> Version: 1.1.0

## Purpose

Users with a single agent session accumulate context over time. Long conversations cause attention drift, irrelevant context pollution, and wasted tokens. This skill gives the user explicit control over what stays in context and what gets shelved.

## When to Use

- User says "归档", "存档", "archive", "save this conversation"
- User says "列出归档", "show archives", "有哪些存档"
- User says "加载", "召回", "load archive", "recall"
- Context is getting long (>50k tokens) and agent should suggest archiving

## Commands

### Archive (归档)

**Triggers:**
- "归档最近的对话" — archive recent conversation
- "归档最近2小时的对话" — archive by relative time
- "归档7/21下午3点到5点的对话" — archive by absolute time range
- "归档关于XX的讨论" — archive by topic
- "归档今天的对话" — archive entire day

**Time Range Parsing:**
- Relative: "最近2小时", "最近30分钟", "今天"
- Absolute: "7/21 下午3:00 到 5:00", "7月15日 到 7月20日"
- Natural language: "昨天下午", "上周三"
- Default: last 30 messages or last 2 hours, whichever is larger

**Flow:**

1. Identify the conversation segment to archive
   - For time-based: parse time range, locate messages in that window
   - For topic-based: use memory_search to locate relevant messages
   - For "recent": default window

2. Generate a structured summary of the segment
   - Key decisions made
   - Tasks completed
   - Important data/numbers
   - Action items / TODOs
   - Code or files created/modified (paths only, not content)

3. **Detail Check (关键步骤)**
   - Present the summary to the user
   - Ask: "以上是这段时间对话的摘要。有没有遗漏的重要细节？如果有，请指出是哪些具体内容，我会补充进去。"
   - If user provides additional details, incorporate them into the summary
   - If user confirms no omissions, proceed
   - Repeat at most twice to avoid infinite loop

4. Propose a title to the user
   - Format: `YYYY-MM-DD-简短描述`
   - User can override with custom name

5. Write to `archives/{title}.md`

6. Confirm to user
   - "已归档至 archives/{title}.md，包含 N 条对话的摘要"

### List Archives (列出归档)

**Triggers:**
- "列出归档", "show archives", "有哪些存档", "存档列表"

**Flow:**

1. Read `archives/` directory
2. For each .md file, extract title, date, and summary line
3. Display as a numbered list with title, date, and brief summary
4. Ask if user wants to load any

### Recall (召回/加载)

**Triggers:**
- "加载第N个归档", "加载XX归档", "recall archive", "load archive XX"

**Flow:**

1. Read the specified archive file
2. Inject summary into current context
3. Confirm to user: "已加载归档：{title}。包含以下要点：..."
4. User can now continue the conversation with that context active

### Auto-Suggest (自动建议)

**Trigger:** When session context exceeds ~50k tokens or conversation exceeds 80+ messages.

**Flow:**

1. Agent proactively suggests archiving with topic summary
2. If user agrees, run archive flow
3. If user declines, don't ask again for another 30 messages

## Archive File Template

```markdown
# {Title}

> Archived: {YYYY-MM-DD HH:mm}
> Period: {start time} — {end time}
> Messages: {count}

## Summary

{2-3 paragraph narrative summary}

## Key Points

- {bullet points of important facts/decisions}

## Decisions

- {any decisions made}

## User-Supplied Details

- {details the user specifically flagged as important during the detail check}

## Files Modified

- {path}: {what changed}

## TODOs

- [ ] {unfinished items, if any}

## Keywords

{comma-separated tags for future search}
```

## Onboarding

First-time setup when the skill is invoked for the first time:

1. Check if `archives/` directory exists and contains any .md files
2. If empty (first-time user), present this welcome message:

   > 欢迎使用 Context Archive。这个工具帮你主动管理对话上下文。
   >
   > **三个核心动作：**
   > - **归档**：把一段对话压缩成摘要文件，释放上下文空间
   > - **列出归档**：查看所有存档
   > - **加载**：把某个存档恢复到当前对话
   >
   > **你可以自己决定归档什么、归档什么时间段的：**
   > - 按主题：归档关于XX的讨论
   > - 按时间：归档最近2小时的对话、归档7/21下午3点到5点
   > - 按需求：归档今天的对话、归档最近的对话
   >
   > 归档时我会先生成摘要给你看，你确认没有遗漏再存。
   > 已为你创建 archives/ 目录。

3. Create `archives/` directory
4. Proceed with the user's intended action immediately

## Storage

- Location: `archives/` directory in workspace root
- Naming: `{YYYY-MM-DD}-{user-provided-or-auto-title}.md`
- Auto-create `archives/` if not exists

## Important Notes

- Archive summaries are NOT raw conversation dumps. They are compressed, structured summaries.
- The detail check step ensures user can flag specific content for preservation.
- Archiving does not delete messages from session history. Agent treats archived segments as low-priority.
- Multiple archives can be recalled simultaneously.
- Archives are searchable via memory_search.
- User can manually edit archive files at any time.

## Language

- Chinese-first interface
- Archive content language follows the original conversation language
- Commands work in both Chinese and English
