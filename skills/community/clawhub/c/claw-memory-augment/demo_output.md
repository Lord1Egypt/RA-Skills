# Memory Augment Demo Output

This file shows sample outputs from the memory-augment skill commands.

## Sample 1: Storing a Memory

```bash
$ clawhub memory store "User prefers Python for automation scripts" \
  --type preference --tag coding --tag python
```

**Output:**
```
✅ Memory stored with ID: a3f8d9e1-2b4c-5d6e-7f8a-9b0c1d2e3f4a
```

## Sample 2: Searching Memories

```bash
$ clawhub memory search "income decisions"
```

**Output:**
```markdown
## Found 3 memories for "income decisions"

### 1. decision (score: 0.98)
**Content:** Approved inbox-triage skill for publishing
**Tags:** income, skills, approval
**Type:** decision
**Created:** 2026-04-15T20:37:00Z

### 2. context (score: 0.72)
**Content:** Building memory-augment skill, 60% complete
**Tags:** project, development
**Type:** context
**Created:** 2026-04-15T22:47:00Z

### 3. learning (score: 0.65)
**Content:** Sub-agent spawning reduces context by ~30%
**Tags:** pattern, optimization
**Type:** learning
**Created:** 2026-04-15T21:00:00Z
```

## Sample 3: Listing Memories

```bash
$ clawhub memory list --type preference
```

**Output:**
```markdown
# Found 2 memories

- [preference] User prefers Python for automation scripts ([test, coding, python])
- [preference] User is in UTC timezone ([test, timezone, config])
```

## Sample 4: Summarizing Memories

```bash
$ clawhub memory summarize --since "7 days ago"
```

**Output:**
```markdown
# Memory Summary (Last 7 days)

**Total memories:** 12

**By type:**
- preference: 3
- decision: 2
- learning: 1
- context: 6
```

## Sample 5: JSON Output

```bash
$ clawhub memory search "skills" --format json
```

**Output:**
```json
{
  "query": "skills",
  "results": [
    {
      "id": "a3f8d9e1-2b4c-5d6e-7f8a-9b0c1d2e3f4a",
      "content": "Approved inbox-triage skill for publishing",
      "score": 0.98,
      "type": "decision",
      "tags": ["income", "skills", "approval"],
      "created": "2026-04-15T20:37:00Z"
    },
    {
      "id": "b4g9e0f2-3c5d-6e7f-8g9h-0i1j2k3l4m5n",
      "content": "Building memory-augment skill",
      "score": 0.75,
      "type": "context",
      "tags": ["project", "development"],
      "created": "2026-04-15T22:47:00Z"
    }
  ],
  "total": 2,
  "took_ms": 45
}
```

## Sample 6: Auto-Inject Context

When the user asks about "skills", the system automatically injects:

```json
{
  "context": {
    "injected_memories": [
      {
        "topic": "income",
        "content": "Approved inbox-triage skill for publishing to clawhub"
      },
      {
        "topic": "development",
        "content": "Building memory-augment skill, currently at 60% completion"
      }
    ],
    "query_analysis": {
      "keywords": ["skills"],
      "confidence": 0.92
    }
  }
}
```

## Sample 7: Search with Tag Filter

```bash
$ clawhub memory search "coding" --tag coding
```

**Output:**
```markdown
## Found 2 memories for "coding" with tag "coding"

### 1. preference (score: 0.95)
**Content:** User prefers Python for automation scripts
**Tags:** coding, python, automation
**Created:** 2026-04-15T10:00:00Z
```

---

**Demo completed at:** 2026-04-15 23:47 UTC
**Test suite:** 6/6 tests passed ✅
