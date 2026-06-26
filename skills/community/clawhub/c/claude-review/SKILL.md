---
name: claude-review
description: "Self-review quality gate using Claude CLI. When the user says 'review your work', 'use review-work', or 'check your output', run review-work with the task summary, --context pointing to your output file/folder, and --skill pointing to the skill used (if any). You determine all arguments yourself — the user does NOT need to specify them. Requires `claude` CLI installed."
license: MIT
metadata:
  version: "3.0.0"
  tags:
    - quality
    - review
    - self-review
    - code review
    - quality gate
    - claude cli
    - learnings
  triggers:
    - "review your work"
    - "use review-work"
    - "check your output"
    - "self-review"
    - "quality check"
    - "review before finishing"
---

# claude-review — Self-Review Quality Gate

Uses Claude CLI (`claude --print`) as an independent reviewer to catch errors, missed requirements, and quality issues in your work before delivering to the user.

## How It Works

1. You complete your task and save output to file(s)
2. `review-work` sends your work to a separate Claude instance for independent review
3. If a skill was used, the reviewer checks against the skill's specific requirements
4. If LESSONS.md exists, the reviewer checks for repeat mistakes
5. Issues are returned with severity ratings (critical / major / minor) and a PASS/FAIL verdict
6. You fix issues and re-review until clean

The reviewer is a **separate Claude instance** — it has no context of your conversation, so it reviews purely on merit.

**Auto-learning:** When a review fails, critical and major issues are automatically logged to `LESSONS.md`. This file is auto-included in future reviews so the reviewer checks for repeat mistakes.

## Prerequisites

- `claude` CLI must be installed and available in PATH (`npm install -g @anthropic-ai/claude-code`)
- Valid API key configured for Claude CLI

## Command

```bash
review-work "<task_summary>" --context <file_or_folder> [--skill <file_or_folder>]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `task_summary` | Yes | What the work was supposed to accomplish |
| `--context <path>` | Yes | File or folder containing the work to review. Can also include reference material, test output, or anything relevant. |
| `--skill <path>` | No | SKILL.md or skill folder used for this task. The reviewer uses its requirements as a definition of done. |

**Auto-included (no flag needed):**
- `LESSONS.md` — if it exists, always included so the reviewer checks for repeat mistakes

All paths accept both files and folders. Claude reads all file types natively (text, images, PDFs, code).

## Workflow

When instructed to review your work:

1. **Identify** every file you created or modified
2. **Run** `review-work` with the task summary, `--context` pointing to your output, and `--skill` if a skill was used
3. **Read** the review output — look for VERDICT: PASS or FAIL
4. **Fix** any critical or major issues
5. **Re-run** `review-work` after fixing (up to 3 cycles)
6. **Report** the review summary in your final output

## Examples

Review a single file:

```bash
review-work "Write a Python email validator" --context /tmp/email.py
```

Review with skill context (reviewer verifies against skill requirements):

```bash
review-work "Write an SEO blog about class action lawsuits" --context /tmp/blog.md --skill ~/.openclaw/workspace/skills/seo-content-writer/SKILL.md
```

Review an entire project folder:

```bash
review-work "Build a todo app with React" --context /tmp/todo-app/ --skill ~/skills/fullstack/SKILL.md
```

Review with extra context (reference articles, test output, etc.):

```bash
# Put your output + reference material in one folder
review-work "Write a blog matching MoneyPilot tone" --context /tmp/blog-project/
```

## Rules

1. Review **every** file you created or modified — not just the main one
2. If a skill was used for the task, always pass `--skill`
3. If the review reports critical or major issues → fix them → re-review (up to 3 cycles)
4. Only finish after the verdict is **PASS** (zero critical/major issues)
5. Include the review summary in your final output
6. After 3 failed cycles, finish but attach the full review report

## What NOT to Do

- Do NOT ask the user for arguments — you already know what you created and which skill you used
- Do NOT say "review passed" without actually running the command
- Do NOT fabricate review results — the command produces real output
- Do NOT forget `--skill` when a skill was involved in the task

## LESSONS.md

Failed reviews are auto-logged to `LESSONS.md` (default: `~/.openclaw/workspace/LESSONS.md`). Override the path with the `LESSONS_FILE` environment variable.

This file is also auto-read on every review, so the reviewer checks: "are any past mistakes being repeated?"
