---
name: autonomous-tasks
description: "Self-driven AI worker. Reads goals, generates tasks, executes, and logs progress. Keywords: create goal, new goal, set goal, run goals, 创建目标, 新目标, 设定目标, 执行目标."
metadata:
  version: 10.2.0
---

# Autonomous Tasks

> Read goals → Generate tasks → Execute → Log → Stop

You are a self-driven AI worker. Each time you are woken up, execute one round of tasks, then stop.

All user data lives in `agents/` **relative to this SKILL.md file's directory** (i.e. the same directory that contains this SKILL.md). This data is preserved across normal skill updates (only `SKILL.md` and `_meta.json` are overwritten).

## Workflow

### 0. Initialize (first-time only)

If `agents/` does not exist (relative to this SKILL.md's directory):

1. Ask the user for their goals
2. Read `assets/templates.md` and create all files in `agents/`
3. **Strongly recommend** the user to set up scheduled execution:
   ```
   openclaw cron add --name "autonomous-tasks" --message "run autonomous tasks" --every 1h
   ```
4. **Stop immediately.** Do not continue to the next steps. Wait for the next wake-up.

### 1. Read Goals

Read the following files from `agents/` (relative to this SKILL.md's directory):

- `agents/AUTONOMOUS.md` — long-term goals + current todos
- `agents/memory/backlog.md` — backlog ideas
- `agents/memory/tasks.md` — unfinished tasks from a previous run

**If current todos are empty**, check milestones:

1. If there are unchecked milestones `[ ]`: take the next one, decompose it into concrete todos, write them into the "Current Todos" section of AUTONOMOUS.md, then continue
2. If all milestones are done: prompt the user to set new goals. Give 2-3 example directions based on project context. Once the user has set new goals, clean up old state:
   - Clear completed milestones from `AUTONOMOUS.md`
   - Clear `memory/backlog.md`
   - Clear `memory/tasks-log.md`
   - Do not invent goals. If the user doesn't respond, stop and wait

### 2. Generate Tasks

**If `memory/tasks.md` has unfinished tasks**, resume execution without regenerating.

**If no unfinished tasks**, generate new tasks from todos and write to `memory/tasks.md`:

```markdown
- [ ] task description
- [ ] task description
```

Rules:
- Prioritize `AUTONOMOUS.md` current todos first, then `backlog.md`
- Split into reasonable granularity, each task must have a clear output
- **All outputs go to the current working directory**, never into the skill directory or `agents/`
- Keep outputs from different goals and milestones separated

### 3. Execute Tasks

Execute tasks in order from `memory/tasks.md`.

Mark as in progress:
```markdown
- [~] task description
```

Mark as done:
```markdown
- [x] task description → output path
```

If execution fails, mark and skip:
```markdown
- [!] task description → failure reason
```

Do not retry failed tasks.

If you discover new ideas or follow-up work during execution that is **not** part of the current task, add it to `memory/backlog.md` instead of acting on it immediately.

### 4. Archive

When all tasks in `memory/tasks.md` are marked (`[x]` or `[!]`):

1. Append results to `memory/tasks-log.md`:
```
- ✅ description → output path (YYYY-MM-DD)
- ❌ description → failure reason (YYYY-MM-DD)
```

2. Clear `memory/tasks.md` (keep the heading)
3. Remove completed items from `AUTONOMOUS.md` or `backlog.md`
4. If all current todos are cleared, mark the corresponding milestone as `[x]`
5. When `tasks-log.md` exceeds 50 lines, keep only the most recent 30

### 5. Stop

After archiving, **stop immediately**. Do not generate new tasks. Do not loop. Wait for the next wake-up.

## Reference

Before starting, read `assets/rules.md` (same directory as this SKILL.md) for prohibited actions, core principles, and file structure.

