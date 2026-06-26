# Lesson-Imprint Component

Lesson-Imprint is BMA's procedural memory component. It is included in the BMA installation path rather than treated as a separate integration.

## Purpose

Repeated agent failures should become compact behavioral safeguards. The agent should not repeatedly relearn the same tool pitfalls, validation misses, or process mistakes.

## Store Files

```text
memory/lesson-imprint/lessons.json
memory/lesson-imprint/config.json
memory/lesson-imprint/BOOTSTRAP.md
```

## Minimal Schema

```json
{
  "version": 1,
  "lessons": [
    {
      "key": "report_unverified_completion",
      "key_type": "behavior",
      "triggers": ["completion", "verification"],
      "mistake": "Reported completion before verifying the actual result.",
      "correct_action": "Before reporting completion, independently verify the actual result.",
      "count": 11
    }
  ]
}
```

Fields:

| Field | Rule |
|-------|------|
| `key` | Native error code or stable behavior key |
| `key_type` | `native_error` or `behavior` |
| `triggers` | Recall terms |
| `mistake` | One-sentence failure |
| `correct_action` | Prompt-ready safeguard |
| `count` | Repeat counter for promotion |

## Daily Distillation Extraction

Daily distillation may write the lesson store. Ad-hoc agents should not opportunistically edit it.

Extraction rules:

1. Read daily logs for `❌ FAILURE:` and `🔧 CORRECTION:` entries.
2. Ignore product bugs, third-party outages, raw logs, and non-agent-controllable issues.
3. Load existing `lessons.json` first.
4. Merge native errors by exact native key.
5. Merge behavior lessons by similarity before creating a new key.
6. Upsert lessons via `scripts/lesson_imprint.py upsert --source distillation ...`.
7. Run `scripts/lesson_imprint.py promote` once to regenerate `BOOTSTRAP.md`.

## Promotion

Only repeated lessons are promoted into `BOOTSTRAP.md`. The injected content should be the `correct_action`, not the full failure story.

Default threshold: 10.

## CLI

```bash
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py init
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py validate
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py recall --query "edit markdown" --limit 3
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py promote
```

## Protection Rule

BMA retention must never cold-archive active Lesson-Imprint state files. They are active procedural memory, not raw historical records.
