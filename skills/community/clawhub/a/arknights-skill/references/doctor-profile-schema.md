# Doctor Profile Schema

`doctor-profile.json` is the local structured profile maintained by `scripts/memory.py`.
It stores only explicitly confirmed facts — never full conversations, screenshot OCR, or inferences.

Schema version: **1**

---

## File Location

Default path:

```
~/.config/arknights-skill/doctor-profile.json
```

Override with environment variable `ARKNIGHTS_MEMORY_DIR`.
Migration from the legacy `.arknights-memory/` path happens automatically on first run.

---

## Top-Level Structure

```json
{
  "schema_version": 1,
  "game": "Arknights",
  "metadata": { ... },
  "doctor": { ... },
  "account": { ... },
  "operators": { ... },
  "pending_confirmations": [ ... ]
}
```

---

## Field Reference

### `schema_version` *(integer)*

Current: `1`.  
`memory.py` will reject profiles with an unsupported version.

---

### `game` *(string)*

Always `"Arknights"`. Reserved for future multi-game support.

---

### `metadata` *(object)*

| Field | Type | Description |
|---|---|---|
| `created_at` | ISO 8601 UTC string | Profile creation timestamp. Set automatically. |
| `updated_at` | ISO 8601 UTC string | Last write timestamp. Updated on every `save`. |

Both are managed by `memory.py`; do not write manually.

---

### `doctor` *(object)*

Personal information about the Doctor.

| Field | Type | Description |
|---|---|---|
| `name` | string or null | In-game nickname / display name. |
| `server` | string or null | Server region, e.g. `"CN"`, `"US"`, `"JP"`, `"KR"`, `"EN"`. |
| `level` | integer or null | Doctor account level. |
| `uid` | string or null | Player UID. Format varies by server. |

---

### `account` *(object)*

Account state and preferences.

| Field | Type | Description |
|---|---|---|
| `progress` | object | Freeform progress map, e.g. `{"main_story": "chapter_09"}`. |
| `resources` | object | Resource stockpile, e.g. `{"lmd": 50000, "skill_book_3": 30}`. |
| `goals` | string array | Short-term or mid-term goals, e.g. `["elite2 SilverAsh", "clear OF-F4"]`. |
| `preferences` | string array | Play style or unit type preferences, e.g. `["guard mains", "low-rarity friendly"]`. |

---

### `operators` *(object)*

Keyed by operator name (use official English or CN name consistently).  
Each value:

```json
{
  "owned": true,
  "elite": 2,
  "level": 80,
  "potential": 5,
  "skill_level": 7,
  "masteries": { "1": 3, "2": 0, "3": 1 },
  "modules": { "m1": 3, "m2": 1 },
  "notes": ["top priority defender"],
  "updated_at": "2026-04-24T10:30:00Z"
}
```

| Field | Type | Valid values | Description |
|---|---|---|---|
| `owned` | boolean | `true` / `false` / `null` | Whether the Doctor owns this operator. |
| `elite` | integer or null | `0`, `1`, `2`, `null` | Elite phase. |
| `level` | integer or null | `≥ 1`, `null` | Current level within the current elite phase. |
| `potential` | integer or null | `1–6`, `null` | Potential level. |
| `skill_level` | integer or null | `1–7`, `null` | Skill rank. |
| `masteries` | object | `{ "skill_id": 0–3 }` | Per-skill mastery level. `skill_id` is `"1"`, `"2"`, or `"3"`. |
| `modules` | object | `{ "module_id": 0–3 }` | Per-module upgrade stage. `module_id` is a string identifier. |
| `notes` | string array | — | Short freeform notes. Each entry ≤ 240 chars. |
| `updated_at` | ISO 8601 UTC string | — | Last modified timestamp. Managed by `memory.py`. |

#### Merge behavior

- **Monotonic only**: `elite`, `level`, `masteries`, `potential`, `skill_level` only accept **increasing** values.
  Downgrades are rejected and written to `pending_confirmations` for manual review.
- **Boolean**: `owned` can transition `null → false → true`, but `true → false` triggers a confirmation.
- **Free text**: `notes` is deduplicated; duplicates are silently ignored.

---

### `pending_confirmations` *(array)*

Stores downgrade or conflicting-fact entries that need user confirmation before being applied.

Each item:

```json
{
  "field": "SilverAsh.elite",
  "current": 2,
  "incoming": 1,
  "reason": "incoming elite is lower",
  "observed_at": "2026-04-24T12:00:00Z"
}
```

| Field | Type | Description |
|---|---|---|
| `field` | string | Dotted path to the conflicting field. |
| `current` | any | Currently stored value. |
| `incoming` | any | Incoming value that was rejected. |
| `reason` | string | Why the write was rejected. |
| `observed_at` | ISO 8601 UTC string | When the conflict was detected. |

Use `memory.py confirm --field <field> --apply` to accept, or `memory.py dismiss --field <field>` to discard.

---

## CLI Commands Reference

| Command | Description |
|---|---|
| `path` | Print the profile file path. |
| `read` | Load or initialize the profile; print JSON to stdout, pending confirmations to stderr. |
| `update --patch-json '<json>' [--dry-run]` | Merge structured facts. With `--dry-run`, preview without saving. |
| `confirm --field <field> --apply` | Apply a pending downgrade/conflict. |
| `dismiss --field <field>` | Discard a pending entry. |
| `list [--owned] [--has-pending]` | List recorded operators. Filter by ownership or pending status. |
| `search <keyword>` | Search operators by name or notes (case-insensitive). |
| `delete-operator <name>` | Delete a recorded operator. |
| `gc [--days N] [--dry-run]` | Remove pending confirmations older than N days (default: 30). |

---

## Write Rules (What `memory.py update --patch-json` Accepts)

Only **explicitly provided facts** from the current conversation turn should be written:

| ✅ Allowed | ❌ Not written |
|---|---|
| Doctor name, server, level, UID | Full conversations |
| Account progress milestones | Raw screenshot OCR |
| Resource amounts | Long narrative logs |
| Operator owned / elite / level | Inferences not confirmed by the user |
| Mastery and module status | Guide advice |
| Short freeform notes | Strength evaluations |

See `SKILL.md` → **Core Rules §0** for the full update workflow.

---

## Example

```json
{
  "schema_version": 1,
  "game": "Arknights",
  "metadata": {
    "created_at": "2026-04-24T08:00:00Z",
    "updated_at": "2026-05-19T14:30:00Z"
  },
  "doctor": {
    "name": "Moran",
    "server": "CN",
    "level": 120,
    "uid": null
  },
  "account": {
    "progress": { "main_story": "chapter_11" },
    "resources": { "lmd": 200000, "skill_book_3": 50 },
    "goals": ["elite2 Exusiai"],
    "preferences": ["low-rarity friendly", "early game"]
  },
  "operators": {
    "Exusiai": {
      "owned": true,
      "elite": 1,
      "level": 70,
      "potential": 3,
      "skill_level": 7,
      "masteries": { "1": 3, "2": 1, "3": 0 },
      "modules": {},
      "notes": ["top priority sniper"],
      "updated_at": "2026-05-19T14:30:00Z"
    }
  },
  "pending_confirmations": []
}
```
