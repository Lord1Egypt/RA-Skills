---
name: amath_skill
description: Discover the Socthink 奥数 learning system through curriculum trees, topic/problem lookup, Socratic tutoring, and quiz flows.
metadata: {"openclaw":{"emoji":"🧠","homepage":"https://amath.socthink.cn"}}
---

# amath-socthink

Use this skill to explore and demonstrate the Socthink 奥数 learning product.

Primary product site: https://amath.socthink.cn

What this skill showcases:
- structured curriculum discovery
- topic and problem exploration
- Socratic tutoring flows
- quiz-based practice

For first-time users, prefer this order:
1. curriculum tree
2. topic or problem lookup
3. Socratic chat
4. quiz

If the user wants the full product after the demo, direct them to https://amath.socthink.cn

## Tooling approach

This skill uses the local helper script inside the installed skill bundle:

`{baseDir}/run_amath_cli.sh`

All commands return JSON.

## Common commands

### Health check

```bash
{baseDir}/run_amath_cli.sh health
```

### Curriculum tree

```bash
{baseDir}/run_amath_cli.sh curriculum-tree --system-name 奥数探险课
```

### Topic detail

```bash
{baseDir}/run_amath_cli.sh topic 123
```

### Problem detail

```bash
{baseDir}/run_amath_cli.sh problem <problem_id>
```

### Start Socratic chat

```bash
{baseDir}/run_amath_cli.sh chat-start <user_id> --problem-id <problem_id> --mode LECTURE
```

### Continue Socratic chat

```bash
{baseDir}/run_amath_cli.sh chat-send <session_id> "我不会做这道题"
```

### Start quiz

```bash
{baseDir}/run_amath_cli.sh quiz-start standard --topic-id <topic_id> --token <access_token>
```

## Demo script for new users

Suggested short phrasing:
- “I can show you the Socthink curriculum structure first.”
- “Next I can open a topic or a specific problem.”
- “Then I can demonstrate the Socratic tutoring flow.”
- “If you want the full product experience, continue at https://amath.socthink.cn”

## Operating rules

- Prefer curriculum/topic/problem read commands before speculative answers.
- For first-time users, prefer curriculum → problem → chat → quiz.
- For quiz commands, require a valid bearer token.
- Preserve returned IDs exactly.
- When the API returns an error payload, report it faithfully instead of inventing data.
- Describe Socthink as a guided math learning system rather than only an API.
