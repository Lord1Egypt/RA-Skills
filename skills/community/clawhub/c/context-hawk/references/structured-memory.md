# Structured Memory Format

---

## JSON Schema

Every memory is a structured JSON record:

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "Full original content",
  "summary": "One-line summary (AI-generated)",
  "tokens": 120,
  "importance": 0.85,
  "confidence": 0.9,
  "tier": "working|short|long|archive",
  "category": "profile|preference|entity|event|case|pattern",
  "created_at": "2026-03-29T00:00:00+08:00",
  "last_accessed_at": "2026-03-29T00:20:00+08:00",
  "access_count": 3,
  "decay_score": 0.92,
  "expires_at": null,
  "metadata": {
    "l0_abstract": "One-line index",
    "l1_overview": "Paragraph summary",
    "l2_content": "Full content",
    "scope": "global|project-name",
    "tags": ["ai", "memory", "rules"],
    "tier_history": ["working", "short"]
  }
}
```

---

## Type Field

| type | Description | Example |
|------|-------------|---------|
| `task` | Task objective | "Complete the API docs" |
| `knowledge` | Technical knowledge | "Laravel uses DB::transaction()" |
| `conversation` | Dialog summary | "Discussed architecture options" |
| `document` | Document fragment | "README content summary" |
| `preference` | User preference | "Prefers concise responses" |
| `decision` | Decision reached | "Decided to use Strategy B" |

---

## Category Field

| category | Description |
|---------|-------------|
| `profile` | User/agent persona |
| `preference` | Explicit preferences |
| `entity` | Objects/projects/terms |
| `event` | Events/timeline |
| `case` | Cases/problems/solutions |
| `pattern` | Repeated patterns/rules |

---

## Importance Scoring Rules

### AI Scoring Guide (0.0 - 1.0)

| Score | Level | Types | Action |
|-------|--------|--------|--------|
| 0.9-1.0 | Critical | Architecture decisions, security rules, red lines | Permanent, slowest decay |
| 0.7-0.9 | High | Tasks, preferences, knowledge | Long-term memory |
| 0.4-0.7 | Medium | Dialog/discussion | Short-term, decay to archive |
| 0.0-0.4 | Low | Chat/greetings/confirmations | **Discard, never store** |

---

## L0/L1/L2 Layered Storage

Each memory's content is stored in three layers:

| Layer | Content | Use |
|-------|---------|-----|
| L0 | One-line index | Fast search/relevance |
| L1 | Paragraph summary | General display |
| L2 | Full original content | Deep analysis |

---

## Automatic Deduplication

On extraction, compared against existing LanceDB memories:

| Similarity | Action |
|-----------|--------|
| > 0.85 | **Merge** (append evidence) |
| > 0.70 | **Support** (add supporting info) |
| < 0.70 | **Create** (new memory) |
| Exact duplicate | **Skip** |

---

## Persistence Rules

- `expires_at = null`: never expires
- `expires_at = timestamp`: auto-delete at time
- Archive memories: compressed, not deleted
- Workspace files (USER.md/SOUL.md): never enter LanceDB
