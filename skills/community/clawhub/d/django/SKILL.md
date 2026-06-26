---
name: Django
slug: django
version: 1.0.1
description: Build secure Django apps avoiding ORM pitfalls, N+1 queries, and common security traps.
metadata: {"clawdbot":{"emoji":"🌿","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

## Quick Reference

| Topic | File |
|-------|------|
| QuerySet lazy eval, N+1, transactions | `orm.md` |
| Request handling, middleware, context | `views.md` |
| Validation, CSRF, file uploads | `forms.md` |
| Migrations, signals, managers | `models.md` |
| XSS, CSRF, SQL injection, auth | `security.md` |
| Async views, ORM in async, channels | `async.md` |

## Critical Rules

- QuerySets are lazy — iterating twice hits DB twice, use `list()` to cache
- `select_related` for FK/O2O, `prefetch_related` for M2M — or N+1 queries
- `update()` skips `save()` — no signals fire, no `auto_now` update
- `F()` for atomic updates — `F('count') + 1` avoids race conditions
- `get()` raises `DoesNotExist` or `MultipleObjectsReturned` — use `filter().first()` for safe
- `DEBUG=False` requires `ALLOWED_HOSTS` — 400 Bad Request without it
- Forms need `{% csrf_token %}` — or 403 Forbidden on POST
- `auto_now` can't be overridden — use `default=timezone.now` if need manual set
- `exclude(field=None)` excludes NULL — use `filter(field__isnull=True)` for NULL
- Circular imports in models — use string reference: `ForeignKey('app.Model')`
- `transaction.atomic()` doesn't catch exceptions — errors still propagate
- `sync_to_async` for ORM in async views — ORM is sync-only
