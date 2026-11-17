# Debugging — Symptom to Cause in Minutes

Work symptom-first. Django hides its real work behind three layers (the ORM, the middleware chain, the template engine), so the fastest route is almost always to make one of those layers print what it actually did. Each section below ends at a cause; SKILL.md Quick Reference maps that cause to the file that goes deeper.

## Contents

- The Universal First Three
- Page Is Slow / Query Count Explodes
- Wrong Number of Rows
- Something Saved, Then Vanished
- It Works In The Shell But Not In The Request
- Migration Will Not Behave
- Auth And Permission Confusion
- Template Renders Nothing
- Static And Media In Production
- Async And Background Work
- When You Are Truly Stuck

## The Universal First Three

1. **See the SQL.** Turn on the query logger for one run — it works with `DEBUG=False`, unlike `connection.queries`:

```python
LOGGING = {
    "version": 1,
    "handlers": {"c": {"class": "logging.StreamHandler"}},
    "loggers": {"django.db.backends": {"handlers": ["c"], "level": "DEBUG"}},
}
```

2. **See one query's plan.** `print(qs.query)` gives the SQL Django will send (parameters already inlined, so never paste it back as executable SQL); `qs.explain()` gives the database's plan.
3. **Count.** Wrap the suspect code in `assertNumQueries(n)` in a test, or in `CaptureQueriesContext(connection)`. A number is a fact; "it feels slow" is not.

## Page Is Slow / Query Count Explodes

1. Count first: `len(connection.queries)` (DEBUG on) or `CaptureQueriesContext`. Compare against the budget in SKILL.md Core Rules 1.
2. If the count scales with rows → N+1. Find the repeated statement in the log; the table it names tells you which relation is missing from `select_related`/`prefetch_related`.
3. Count fine, still slow → one heavy query. `qs.explain()` and hand it to the database (`pg` for Postgres plans).
4. Query fast in the shell, slow in the view → it is not the query: serialization, template rendering, or a middleware. Time the pieces (`time.perf_counter()` around `render()`).
5. Slow only on the first request after deploy → import time, not request time: module-level work in `apps.py`, settings, or a heavy third-party import.
6. Fast locally, slow in production with the same data → connection setup per request (`CONN_MAX_AGE = 0`) or a cache backend that is per-process.

## Wrong Number of Rows

| Symptom | Cause |
|---|---|
| Rows duplicated after filtering a multi-valued relation | Each `.filter()` on a reverse FK/M2M adds a JOIN; `.distinct()` is the patch, one `.filter(a=..., b=...)` is the fix |
| `Count`/`Sum` too large | Two annotated relations joined at once multiply rows — `distinct=True` or `Subquery` |
| NULL rows missing from an `exclude()` | `NOT (col = value)` is unknown for NULL — add `Q(col__isnull=True)` |
| A `filter()` after `prefetch_related` re-queries | Filtering the related manager discards the prefetch cache — filter inside `Prefetch(queryset=...)` |
| Results change between two identical calls | No `order_by` with `LIMIT`: the database is free to return any page |
| A row exists in the shell but not in the request | Different database (test vs dev), a tenant/manager filter, or the transaction has not committed yet |

## Something Saved, Then Vanished

1. Was it inside `atomic()` that later raised? The rollback is silent from the caller's point of view.
2. Was it a queryset `update()` on a model whose `save()` does the real work? (SKILL.md Core Rules 3.)
3. Did a signal or a `save()` override write over it afterwards? `Model.save(update_fields=[...])` narrows the write and makes the culprit obvious.
4. Two processes writing the same row → last write wins. `F()` for counters (Core Rules 4), `select_for_update()` for read-then-write.
5. `TestCase` rolls back after every test by design — data "disappearing" between tests is the framework, not a bug.

## It Works In The Shell But Not In The Request

Check in this order; each is a one-minute test.

| Difference | Check |
|---|---|
| Different settings module | `python -c "import django,os;print(os.environ.get('DJANGO_SETTINGS_MODULE'))"` in both contexts |
| Different database | `connection.settings_dict["NAME"]` inside the view |
| Authentication / permission filtering | The view scopes the queryset by `request.user`; the shell does not |
| Middleware rewriting the request | Comment the chain down to `CommonMiddleware` and re-test |
| A cached response or cached fragment | `CACHES` set to `DummyCache` for one run |
| Timezone | The shell runs in server local time; the request may run under an activated timezone |
| A worker with stale code | Reload the application server; gunicorn does not hot-reload without `--reload` |

## Migration Will Not Behave

- "No changes detected" → the app is not in `INSTALLED_APPS`, or the models module is never imported.
- "Conflicting migrations detected; multiple leaf nodes" → two branches merged; `makemigrations --merge`.
- The migration asks for a one-off default on every run → a field's default is a callable being called (`default=timezone.now` correct, `default=timezone.now()` frozen at import).
- `InconsistentMigrationHistory` → a migration is applied ahead of its dependency. Read `django_migrations` and repair the graph.
- Applied but the column is missing → someone ran `--fake`. `sqlmigrate app 00xx` prints the SQL that was supposed to run; compare against the live schema.
- Endless "Add field / Remove field" churn between developers → a non-deterministic model definition (a set, a dict ordering, a dynamic `choices` list).

## Auth And Permission Confusion

- Logged in but `request.user.is_anonymous` → `AuthenticationMiddleware` missing or after your middleware; order matters.
- `login()` succeeds for a wrong password → `login()` only creates the session; `authenticate()` is what checks credentials.
- Permission always denied after adding one → new permissions exist only after `migrate` creates them, and cached `user.get_all_permissions()` needs a fresh request or `user = User.objects.get(pk=...)`.
- Superuser bypasses your custom check → `has_perm` returns True for superusers; test object-level rules with a normal user.
- Redirect loop on the login page → `LOGIN_URL` points at a protected view.

## Template Renders Nothing

- A variable resolves to empty instead of raising: invalid variables render as `""` (`string_if_invalid` makes them visible during a debug run).
- The block does not appear → `{% block %}` in the child is outside `{% extends %}`'s reach, or `{% extends %}` is not the first tag.
- HTML shows as escaped text → the value is safe HTML that should use `format_html`, not a case for `|safe` on user input.
- A custom tag is "not registered" → the module lives outside `templatetags/`, that package lacks `__init__.py`, or the server was not restarted.

## Static And Media In Production

- 404 on `/static/...` → nothing serves it: `runserver` does in DEBUG only. Whitenoise or the web server must.
- `ValueError: Missing staticfiles manifest entry` → a template references a file `collectstatic` never saw; the manifest storage is strict on purpose.
- Uploaded files 404 → `MEDIA_URL` is not routed in production, and it should not be routed through Django at all for volume.

## Async And Background Work

- `SynchronousOnlyOperation` → an ORM call under an event loop.
- Task fails with `DoesNotExist` then succeeds on retry → queued before COMMIT (SKILL.md Core Rules 5).
- Task runs with stale field values → a model instance was serialized into the message; pass the primary key.
- Everything hangs under load with idle CPU → workers blocked on I/O or on the database connection pool, not on Python.

## When You Are Truly Stuck

Bisect the stack, in this order, because each step removes a whole layer:

1. Run the ORM call alone in `manage.py shell` — if it misbehaves there, it is a query problem.
2. Call the view function directly with `RequestFactory` — if it misbehaves, it is view logic; if not, the difference is middleware or URL routing.
3. Hit it with the test `Client` — this adds middleware and sessions back.
4. Hit it with `curl` against the running server — this adds the application server and proxy back.

The step where behavior changes names the layer, and the file above to open next.
