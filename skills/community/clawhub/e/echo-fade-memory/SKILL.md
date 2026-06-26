---
name: echo-fade-memory
version: 1.3.0
description: "Runs a thin long-term memory workflow on top of the echo-fade-memory service. Use proactively whenever an answer may depend on prior session context, durable user facts, preferences, recent personal state, past decisions, corrections, unresolved work, or previously shared images/screenshots/files. Prefer low-cost recall before answering and store durable facts or visual artifacts early."
author: hiparker
keywords: [memory, ai-agent, long-term-memory, recall, store, forget, image-memory, multimodal, screenshot, ocr, dashboard, openclaw, cursor, codex, claude-code]
metadata:
  requires:
    runtime:
      - "echo-fade-memory server on http://127.0.0.1:8080 or EFM_BASE_URL"
      - "embedding backend: Ollama or OpenAI or Gemini"
---

# Echo Fade Memory

This skill turns `echo-fade-memory` into an installed **agent memory operating layer**.

The public agent contract is intentionally thin:

- `store`
- `recall`
- `forget`

Image memory is folded into the same `store/recall/forget` contract. Dashboard and debugging routes live under `/v1/dashboard/*` and are not part of the agent-facing tool surface.

## Natural Triggers in OpenClaw

Use this skill implicitly when the conversation includes:

- remember this / 记住这个
- what did we decide before / 上次定的是什么
- user preferences, durable constraints, corrections
- project decisions worth carrying across sessions
- screenshots, diagrams, receipts, whiteboards, or UI states that may matter later
- repeated failures that reveal a reusable workaround
- elliptical continuity prompts such as 那个、这个、继续刚才的、你知道的
- time-indexed prompts such as 今天、刚刚、最近、这次、又、还、还是、依然
- continuity checks such as 你记得吗、你不是知道吗、你忘了？

Prefer over-triggering low-cost recall to under-triggering and answering as if no history exists.

If `http://127.0.0.1:8080` is unreachable in a containerized environment, set:

```bash
export EFM_BASE_URL=http://host.docker.internal:8080
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| Start of a task or session | Recall relevant context with `./scripts/recall.sh "<query>"` |
| User states a durable preference / decision / correction | Store it immediately with `./scripts/store.sh "<content>" --summary "<summary>" --type <type>` |
| User sends an image or screenshot worth keeping | Store it with `./scripts/store.sh "<file-path>" --object-type image` |
| Need old memory, image, or topic with one query | Use `./scripts/recall.sh "<query>"` |
| User asks to delete wrong or obsolete memory | Use `./scripts/forget.sh "<query-or-id>"` |
| Need debug analytics or dashboards | Open `/dashboard` or call `/v1/dashboard/*` |

## Core Workflow

### 1. Recall Before Responding

Before answering about prior decisions, preferences, goals, screenshots, or unresolved issues:

```bash
./scripts/recall.sh "database choice for this project"
```

Inspect:

- `mixed`
- `memories`
- `images`
- `entities`

If a recalled memory is fuzzy, you can still ground it with `GET /v1/memories/<id>/ground`, but keep that as an internal troubleshooting path rather than the default agent contract.

### 2. Store Durable Facts Early

When the user says something durable, store it before moving on.

Recommended minimal memory shape:

- `content`
- `summary`
- `type`

```bash
./scripts/store.sh \
  "User prefers dark mode and minimal UI" \
  --summary "dark mode preference" \
  --type preference
```

Advanced fields still exist, but only add them when you have a clear reason:

- `--importance`
- `--ref`
- `--kind`
- `--conflict-group`

Use higher `importance` only for:

- preferences
- corrections
- project decisions
- constraints
- explicit "remember this" statements

### 3. Store Images Through the Same Entry

When the conversation includes a screenshot, whiteboard, receipt, or other durable visual artifact.

Recommended minimal image shape:

- `file_path` or `url`
- optional `caption`
- optional `tags`
- optional `ocr_text`

```bash
./scripts/store.sh \
  "/absolute/path/to/meeting-whiteboard.png" \
  --object-type image \
  --caption "meeting whiteboard about rollout" \
  --tag rollout \
  --ocr-text "Deployment Checklist"
```

Advanced image flags still exist, but they are not the default mental model:

- `--session`
- `--kind`
- `--actor`
- `--memory-id`
- `--url`

Use image memory when the user is likely to ask:

- "上次那张图"
- "有猫那张图"
- "包含某句话的截图"
- "和那个决定相关的图片"

### 4. Forget Wrong or Obsolete State

If a memory or image is incorrect, unsafe, or obsolete:

```bash
./scripts/forget.sh "that obsolete deployment note"
./scripts/forget.sh "<image-id-or-query>" image
```

## Memory Taxonomy

| Situation | `memory_type` | Notes |
|-----------|---------------|-------|
| User preference | `preference` | Use high importance |
| Project decision | `project` | Add `conflict_group` for versioning |
| Goal / pending work | `goal` | Good for future follow-ups |
| Error workaround | `project` | Prefix summary with `error:` or `learning:` |
| Capability request | `goal` or `project` | Prefix summary with `feature-request:` |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/health-check.sh` | Verify the server is reachable |
| `scripts/store.sh` | Unified store wrapper for memory and image objects |
| `scripts/recall.sh` | Unified federated recall wrapper |
| `scripts/forget.sh` | Unified forget wrapper for memory or image objects |
| `scripts/activator.sh` | Hook reminder for recall/store discipline |
| `scripts/error-detector.sh` | Hook reminder when command output looks like a failure |

## Setup

### Service Availability

```bash
./scripts/health-check.sh
```

### OpenClaw Config

Recommended entry in `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "echo-fade-memory": {
        "baseUrl": "http://host.docker.internal:8080"
      }
    }
  }
}
```

Recommended precedence:

1. `EFM_BASE_URL`
2. `skills.entries.echo-fade-memory.baseUrl`
3. default `http://127.0.0.1:8080`
