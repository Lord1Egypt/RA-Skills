# Memory Template — Django

Create `~/Clawic/data/django/memory.md` with this structure:

```markdown
# Django Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Context
<!-- Their project: Django version, database, API layer, rough scale (rows, requests) -->
<!-- Shape: server-rendered site, JSON API, both; app layout; where the admin is used -->

## Constraints
<!-- Banned packages, LTS-only policy, compliance rules, tables that cannot go offline -->
<!-- Whether migrations may be applied directly, whether raw SQL is allowed -->

## Pain Points
<!-- Incidents and recurring problems they have raised -->

## Preferences
<!-- Fat models vs services, test runner, review gates, how much explanation with code -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning their project |
| `complete` | Know their stack and conventions well |
