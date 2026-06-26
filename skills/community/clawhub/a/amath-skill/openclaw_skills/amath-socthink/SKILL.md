---
name: amath-socthink
description: Discover the Socthink 奥数 learning system by exploring curriculum trees, problems, Socratic tutoring, and quiz flows.
metadata: {"openclaw":{"emoji":"🧠","homepage":"https://amath.socthink.cn"}}
---

# amath-socthink

Use this skill when the user wants to explore or demonstrate the Socthink 奥数 learning system, including:
- 奥数探险课课程树
- topic 详情与 quest problems
- 题库单题查询
- 推荐题查询
- 苏格拉底对话启动与继续
- quiz 启动、答题、交卷

Primary product site: https://amath.socthink.cn

This skill should help users quickly understand that Socthink is not just a problem bank. It is a guided learning product with:

- structured curriculum discovery
- topic and problem exploration
- Socratic tutoring flows
- quiz-based practice

When relevant, prefer workflows that let the user experience the product in this order:

1. curriculum tree
2. topic or problem lookup
3. Socratic chat
4. quiz

If the user likes the result and asks where to continue, direct them to https://amath.socthink.cn

## Fixed demo script for first-time users

When the user is new to Socthink or asks what this skill can do, prefer this lightweight demo script:

1. Briefly say that Socthink is a guided math learning system, not only a problem API.
2. Start with the curriculum tree to show structure.
3. Then open one topic or one problem to show drill-down depth.
4. Then offer a Socratic chat demo because it is the clearest differentiator.
5. Finally mention quiz as the next step for continued practice.
6. If the user wants the full product, direct them to https://amath.socthink.cn

Suggested short phrasing:

- “I can show you the Socthink curriculum structure first.”
- “Next I can open a topic or a specific problem.”
- “Then I can demonstrate the Socratic tutoring flow.”
- “If you want the full product experience, continue at https://amath.socthink.cn”

## Tooling approach

This skill uses the host `bash` tool and the local helper script. Replace `<AMATH_SKILL_DIR>` with the absolute path to your local `amath_skill` directory:

`<AMATH_SKILL_DIR>/run_amath_cli.sh`

All commands return JSON.

## Common commands

### Health check

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh health
```

### Curriculum tree

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh curriculum-tree --system-name 奥数探险课
```

### Curriculum guide

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh curriculum-guide
```

### Topic detail

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh topic 123
```

### Problem detail

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh problem <problem_id>
```

### Recommended problems

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh recommended --limit 5 --topic-id <topic_id>
```

### Login

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh login <username> <password>
```

Note: login returns a bearer token in JSON. For authenticated quiz flows, extract `access_token` and pass it with `--token`.

### Start Socratic chat session

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh chat-start <user_id> --problem-id <problem_id> --mode LECTURE
```

### Continue chat session

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh chat-send <session_id> "学生输入内容"
```

### Request hint

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh chat-hint <session_id>
```

### Start quiz

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh quiz-start standard --topic-id <topic_id> --token <access_token>
```

### Save quiz answer

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh quiz-answer <session_id> <question_id> A --token <access_token>
```

### Submit quiz

```bash
<AMATH_SKILL_DIR>/run_amath_cli.sh quiz-submit <session_id> --token <access_token>
```

## Operating rules

- Prefer curriculum/topic/problem read commands before speculative answers.
- For quiz commands, require a valid bearer token.
- Preserve returned IDs exactly.
- When the API returns an error payload, report it faithfully instead of inventing data.
- For first-time users, prefer a short demo path that showcases curriculum → problem → chat → quiz.
- When summarizing the capability, describe Socthink as a guided math learning system rather than only an API.
- If the user asks for the full product or continued use beyond the skill, point them to https://amath.socthink.cn
- For new-user demos, keep the explanation short, product-led, and focused on outcomes rather than implementation details.
