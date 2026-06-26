# Logging Format Reference

The loop stays usable because the default entry is one line.

## Core rule

- One incident or discovery per line
- `date | type/category | what happened | what to do next`
- Extra fields are optional and additive
- Older short-form entries remain valid

## Canonical line shapes

### `errors.md`

```text
[YYYY-MM-DD] id:ERR-YYYYMMDD-NNN | COMMAND | what failed | fix | count:N | prevented:N | severity:medium | source:agent | expires:YYYY-MM-DD | → detail: .learnings/details/YYYY-MM-DD-slug.md
```

### `learnings.md`

```text
[YYYY-MM-DD] id:LRN-YYYYMMDD-NNN | CATEGORY | what | action | count:N | prevented:N | severity:medium | source:agent | expires:YYYY-MM-DD | → detail: .learnings/details/YYYY-MM-DD-slug.md
```

Categories: `correction`, `knowledge`, `pattern`, `gotcha`, `optimization`

### `wishes.md`

```text
[YYYY-MM-DD] CAPABILITY | what was wanted | workaround | requested:N
```

### `promotion-queue.md`

```text
[YYYY-MM-DD] id:LRN-YYYYMMDD-NNN | proposed rule text | target: AGENTS.md | source:agent | evidence: count:N prevented:N | status: pending
```

See also: `promotion-queue-format.md`

## Optional fields

| Field | Meaning | Default |
|---|---|---|
| `id:` | Stable dedup key | none |
| `count:N` | How many times it recurred | 1 |
| `prevented:N` | How many times it changed behavior | 0 |
| `severity:` | `low`, `medium`, `high`, `critical` | `medium` |
| `source:` | Trust label for promotion safety | `agent` |
| `expires:` | Temporary workaround expiry date | none |
| `→ detail:` | Link to a freeform detail file | none |

## Source labels

| Source | Meaning | Promotable? |
|---|---|---|
| `source:agent` | Agent observed it directly | Yes |
| `source:user` | User correction | Yes, after review |
| `source:external` | Email, web page, webhook, attachment, forwarded content | No |

Rules:
- If the fact first came from outside content, keep it `source:external`
- Do not promote `source:external` items
- Agents can queue entries, but only humans mark queue items `approved` or `promoted`

## Examples

```text
[2026-03-01] id:ERR-20260301-001 | gog gmail send | OAuth expired, invalid_grant | re-auth: gog auth add EMAIL | count:3 | prevented:1 | source:agent
[2026-03-02] id:LRN-20260302-001 | pattern | sub-agents need detailed specs | include reference + criteria in spawn | count:5 | prevented:3 | source:agent
[2026-03-03] id:LRN-20260303-001 | correction | Telegram 4096 char limit | keep briefs under 3500 | count:1 | severity:critical | source:user
```