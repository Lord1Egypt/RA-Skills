---
name: Django
slug: django
version: 1.0.3
description: >-
  Builds, debugs, and hardens Django apps: models, the ORM, views, templates, forms, the admin, DRF APIs, and deployment.
  Use when a page fires one query per row (N+1, select_related, prefetch_related, annotate double-counting); when
  makemigrations conflicts, a migration locks a live table, or InconsistentMigrationHistory blocks a deploy; on 403 CSRF
  verification failed, DEBUG=False turning every request into 400 DisallowedHost or a blank 500, or SECURE_SSL_REDIRECT
  looping behind a proxy; on SynchronousOnlyOperation, AppRegistryNotReady, or NoReverseMatch; when a background task runs
  before its transaction commits, signals fire on rows that roll back, or update() skips auto_now; when the admin times
  out on a big table, collectstatic breaks static files, or workers exhaust database connections; when writing
  serializers, formsets, a custom user model, permissions, or assertNumQueries tests; or upgrading Django across a
  deprecation. Not for plain Python, FastAPI or Flask services, or engine-level SQL tuning.
homepage: https://clawic.com/skills/django
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🌿
    requires:
      bins:
      - python3
    os:
    - linux
    - darwin
    - win32
    displayName: Django
    configPaths:
    - ~/Clawic/data/django/
---

User preferences and memory live in `~/Clawic/data/django/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/django/` or `~/clawic/django/`), move it to `~/Clawic/data/django/`.

## When To Use

- Writing or reviewing Django models, migrations, views, forms, templates, admin classes, or DRF serializers
- A page is slow or the query count grows with the number of rows on screen
- A migration will not generate, will not apply, conflicts after a merge, or would lock a production table
- An exception that is Django's and not Python's: `SynchronousOnlyOperation`, `TransactionManagementError`, `AppRegistryNotReady`, `NoReverseMatch`, `DisallowedHost`, `ImproperlyConfigured`
- Hardening a project for production: settings split, `check --deploy`, static and media, sessions, permissions, upload limits
- Background jobs, async views, Channels, caching, or a test suite that is slow or order-dependent
- Not for plain Python semantics, packaging, or asyncio internals, and not for engine-level SQL tuning (see Related Skills)

## Quick Reference

| Situation | Play |
|---|---|
| Query count grows with rows on the page | `select_related` for forward FK/O2O, `prefetch_related` for reverse FK/M2M (Core Rules 1-2, → `orm.md`) |
| `Sum`/`Count` inflated after `annotate` | Two joins multiply rows — `Count("x", distinct=True)` or a `Subquery` (→ `orm.md`) |
| Rows come back duplicated after filtering on a related model | Chained `.filter().filter()` joins twice; one `.filter(a=..., b=...)` requires the same related row (→ `orm.md`) |
| `makemigrations` reports "No changes detected" | App missing from `INSTALLED_APPS`, or models defined outside an imported module (→ `migrations.md`) |
| Two migration leaves after a merge | `makemigrations --merge`; never renumber files by hand (→ `migrations.md`) |
| The migration must run on a live table | Expand → backfill in batches → contract, each in its own migration (Core Rules 6, → `migrations.md`) |
| 403 "CSRF verification failed" | Missing `{% csrf_token %}`, or `CSRF_TRUSTED_ORIGINS` entries without a scheme behind a proxy (→ `security.md`) |
| 400 on every request once `DEBUG=False` | `ALLOWED_HOSTS` (→ `settings.md`) |
| 500 with an empty response and nothing in the logs | `DEBUG` off with no `LOGGING` config — the exception exists, nothing writes it down (→ `settings.md`) |
| Redirect loop behind a load balancer | `SECURE_SSL_REDIRECT` without `SECURE_PROXY_SSL_HEADER` (→ `deployment.md`) |
| `SynchronousOnlyOperation` | ORM touched from an async context — `sync_to_async` or the `a`-prefixed ORM methods (→ `async.md`) |
| Task fails with `DoesNotExist`, then succeeds on retry | Queued inside `atomic()` and picked up before COMMIT — `transaction.on_commit` (Core Rules 5, → `tasks.md`) |
| Admin change page hangs or times out | A ForeignKey rendered as a `<select>` of every row — `autocomplete_fields`, `list_select_related` (→ `admin.md`) |
| Static files 404, or the manifest raises after deploy | `collectstatic`, `STATIC_ROOT`, and hashed-name references (→ `deployment.md`) |
| Tests pass alone and fail as a suite | Mutated `setUpTestData` objects, or a setting read at import time (→ `testing.md`) |
| A DRF endpoint issues N+1 or leaks a field | `SerializerMethodField` touching a relation; `fields = "__all__"` (→ `drf.md`) |
| Login, permissions, or a custom user model | `auth.md` — and set `AUTH_USER_MODEL` before the first `migrate` (Core Rules 8) |
| Starting a project, or deciding where a new app goes | `startproject config .`, domain-shaped apps, and a label chosen once — it is baked into every table name (→ `layout.md`) |
| Bumping the Django version, or `RemovedInDjangoXXWarning` in the test output | Clear deprecations on the current version with `python -Wa manage.py test`, then move one feature release at a time (→ `upgrade.md`) |
| Text must render in the user's language, or dates in their format | `gettext_lazy` at import time, `{% blocktranslate %}` in templates, and `compilemessages` — Django reads `.mo`, never `.po` (→ `i18n.md`) |
| Anything else | Reproduce in `manage.py shell`, switch the `django.db.backends` logger to DEBUG, and read the SQL Django actually emitted before changing any code (→ `debug.md`) |

Depth on demand, by phase:

- **Start** — `layout.md` project skeleton, app boundaries, labels, where non-app code goes
- **Diagnose** — `debug.md` symptom to cause in minutes · `commands.md` the `manage.py` toolkit and what each command really does
- **Model the data** — `models.md` fields, relations, constraints, managers, signals · `migrations.md` generating, merging, squashing, online schema change · `orm.md` querysets, joins, aggregation, transactions, locking
- **Serve requests** — `views.md` view classes, URLs, middleware, requests and responses · `forms.md` validation, formsets, file uploads · `templates.md` escaping, context, custom tags · `auth.md` users, sessions, permissions, password flows · `admin.md` the admin at real data volume · `drf.md` serializers, viewsets, permissions, pagination · `i18n.md` translation, locale switching, formats, timezones
- **Make it fast** — `performance.md` query budgets, caching layers, profiling · `async.md` async views, ASGI, Channels · `tasks.md` background jobs, on_commit, retries, email
- **Ship it** — `settings.md` settings layout, env config, logging, timezone · `deployment.md` WSGI/ASGI, workers, static and media, release sequence · `security.md` the Django-specific attack surface · `testing.md` fast, isolated, honest tests · `upgrade.md` release cadence, deprecations, LTS windows

## Core Rules

1. **Give every list view a query budget and assert it.** Budget = 1 query for the page + 1 per `prefetch_related` + 0 for `select_related` (it joins into the page query) + 1 for the count if you paginate. A paginated 50-row page of orders with `select_related("customer")` and `prefetch_related("items")` is 1 + 1 + 0 + 1 = 3 queries; the unoptimized version of the same page is 1 + 50 + 50 + 1 = 102. Check it with `assertNumQueries(3)` in a test, not by eye — the regression arrives inside someone else's template change.
2. **`select_related` joins, `prefetch_related` runs a second query.** Forward `ForeignKey`/`OneToOneField` → `select_related` (SQL JOIN, one query). Reverse FK and `ManyToManyField` → `prefetch_related` (one extra query, joined in Python). Passing an M2M to `select_related` raises `FieldError`; passing a forward FK to `prefetch_related` works but buys an extra round trip for nothing.
3. **Queryset-level writes bypass the model.** `update()`, `delete()`, `bulk_create()`, `bulk_update()` never call `Model.save()`, never fire `pre_save`/`post_save`, never touch `auto_now`, and never run validators. That is exactly why they are fast. When you use them, set the timestamp yourself: `.update(status="done", updated_at=timezone.now())`.
4. **Counters use `F()`, not read-modify-write.** `obj.n += 1; obj.save()` reads a stale value and loses every concurrent increment; `Model.objects.filter(pk=pk).update(n=F("n") + 1)` is a single atomic `UPDATE ... SET n = n + 1`. After an `F()` write the in-memory attribute holds an expression object, not a number — `refresh_from_db()` before reading it.
5. **Side effects belong in `transaction.on_commit`.** Anything outside the database — a queued task, an email, a webhook, a cache invalidation — fires only after COMMIT. Queued inside `atomic()`, a worker can pick the job up before the row is visible: the symptom is a task failing with `DoesNotExist` for an object you just created, and passing on retry.
6. **A schema change on a live table is three deploys, not one.** Expand (add the nullable column or new table, ship code that tolerates both shapes) → backfill in batches with a resume key → contract (set NOT NULL, drop the old column) once nothing reads the old shape. One migration that adds a NOT NULL column to a large table rewrites it under a lock, and every request queues behind that lock.
7. **Catch database errors outside the `atomic()` block.** After any statement raises inside a transaction, the connection is poisoned: every later query raises `TransactionManagementError` until rollback. To continue after an expected `IntegrityError`, wrap just the risky statement in its own nested `with transaction.atomic():` — the nesting is a savepoint, and only the savepoint rolls back.
8. **Set `AUTH_USER_MODEL` before the first `migrate`.** Start every project with `class User(AbstractUser): pass` even if it stays empty. Swapping the user model after tables exist means rewriting every FK to `auth.User` and, in practice, rebuilding migration history — Django offers no supported path for it.
9. **Reference models by string; never import them at module import time.** `ForeignKey("shop.Order")` and `settings.AUTH_USER_MODEL` break import cycles. `get_user_model()` or a queryset at module level raises `AppRegistryNotReady`; put it inside the function, or in `AppConfig.ready()` for signal registration only.

## Exception To Cause

Django raises its own exception types before Python's. The type names the subsystem.

| Exception | What it actually means | First move |
|---|---|---|
| `SynchronousOnlyOperation` | An ORM call reached an async context | Wrap in `sync_to_async(...)`, or use `aget`/`acreate`/`async for` (Django >=4.1) (→ `async.md`) |
| `TransactionManagementError` | A query ran after an error inside `atomic()`, or `select_for_update()` ran outside a transaction | Rule 7; for locking, open an `atomic()` block first |
| `AppRegistryNotReady` | Models or `get_user_model()` touched during import | Rule 9 — move it into a function or `AppConfig.ready()` |
| `ImproperlyConfigured` | Settings used before `django.setup()`, or a required setting missing or empty | The message tail names the setting; standalone scripts need `django.setup()` before importing any app code |
| `DisallowedHost` | The `Host` header is not in `ALLOWED_HOSTS` | Add the host; behind a proxy also check `USE_X_FORWARDED_HOST` (→ `settings.md`) |
| `NoReverseMatch` | A `{% url %}`/`reverse()` name, namespace, or argument count is wrong | Check `app_name` plus the pattern's converters — a `<int:pk>` route rejects a string silently (→ `views.md`) |
| `TemplateDoesNotExist` | Loader order, not a missing file, most of the time | The debug page lists every path tried; check `APP_DIRS` and `DIRS` (→ `templates.md`) |
| `FieldError` | An invalid lookup, or `only()`/`defer()` conflicting with `select_related` | The message lists the valid choices; re-read the `__` lookup chain |
| `RelatedObjectDoesNotExist` | A nullable FK that is NULL, or a reverse OneToOne with no row | `getattr(obj, "profile", None)`; the class also catches as `Model.DoesNotExist` |
| `MultipleObjectsReturned` | `get()` matched more than one row — a uniqueness constraint is missing | Add the `UniqueConstraint`, then decide whether the caller wanted `filter().first()` |
| `SuspiciousFileOperation` | A generated path escaped the storage root | Never build `upload_to` or a storage name from raw user input (→ `security.md`) |
| `InconsistentMigrationHistory` | A migration is recorded as applied before a dependency it needs | Usually a late user-model swap or a re-pointed FK; repair the graph, do not `--fake` blindly (→ `migrations.md`) |
| `OperationalError: database is locked` | SQLite with concurrent writers | SQLite serializes writes; raise `timeout` in `DATABASES["default"]["OPTIONS"]`, or move to Postgres for anything concurrent |

## HTTP Symptoms

| Response | Usual cause |
|---|---|
| 400 on everything after `DEBUG=False` | `ALLOWED_HOSTS` empty or missing this host |
| 403 "CSRF verification failed" | No `{% csrf_token %}`; a cross-origin POST needing `CSRF_TRUSTED_ORIGINS` entries with the scheme (`https://app.example.com`, required since Django >=4.0); or `CSRF_COOKIE_SECURE` on a plain-HTTP origin |
| 404 on a URL that exists | Trailing-slash mismatch, `include()` ordering, or a path converter rejecting the value |
| 301 loop | `SECURE_SSL_REDIRECT` behind a TLS-terminating proxy with no `SECURE_PROXY_SSL_HEADER` |
| 302 to `/accounts/login/` from an API client | `LoginRequiredMixin` on an endpoint that should answer 401/403 — use DRF permissions instead (→ `drf.md`) |
| A POST arrives as a GET with no data | `APPEND_SLASH`: Django answers a slash-less POST with a 301 and the body is dropped. Post to the exact URL |
| 500, blank body, nothing logged | `DEBUG=False` with default logging — Django mails `ADMINS` and writes nothing else (→ `settings.md`) |
| 502/504 under load, fine when idle | Worker saturation, or a request longer than the proxy timeout (→ `deployment.md`) |
| Users randomly logged out | `SECRET_KEY` differs between instances, or was rotated without `SECRET_KEY_FALLBACKS` (Django >=4.1) |

## Settings Defaults That Bite

Exact Django defaults that produce confusing failures. All are overridable in settings.

| Setting | Default | What the default costs you |
|---|---|---|
| `DATA_UPLOAD_MAX_MEMORY_SIZE` | 2621440 bytes (2.5 MB) | A non-file POST body above it raises `RequestDataTooBig` — hits large JSON payloads and long text fields |
| `DATA_UPLOAD_MAX_NUMBER_FIELDS` | 1000 | `TooManyFieldsSent` on large formsets. A formset posts `forms × fields_per_form + 4` management inputs, so 1000 caps you near 200 forms of 5 fields |
| `FILE_UPLOAD_MAX_MEMORY_SIZE` | 2621440 bytes (2.5 MB) | Below it an upload is an in-memory object with no `temporary_file_path()`; above it, a temp file on disk. Code that assumes one shape breaks on the other |
| `CONN_MAX_AGE` | 0 | A fresh TCP connect plus auth handshake on every single request |
| `CACHES["default"]["TIMEOUT"]` | 300 seconds | Anything cached without an explicit timeout expires in five minutes |
| `LocMemCache` `MAX_ENTRIES` | 300, with `CULL_FREQUENCY` 3 | At 300 keys it evicts one third at random — and each worker process holds its own copy, which is why hit rates look impossible (→ `performance.md`) |
| `SESSION_COOKIE_AGE` | 1209600 seconds (14 days) | Sessions live two weeks and the `django_session` table grows forever unless `clearsessions` runs on a schedule |
| `PASSWORD_RESET_TIMEOUT` | 259200 seconds (3 days) | Reset links stay valid for three days |
| Formset `max_num` | 1000, with `absolute_max` = `max_num + 1000` | A crafted POST can force Django to build up to `absolute_max` forms before validation runs |
| `DEFAULT_AUTO_FIELD` | unset → `models.W042` | Every app gets a 32-bit `AutoField` and the system check nags; set `BigAutoField` project-wide |
| `DEBUG` | `False` | Right for production, and the one default people expect backwards: with `DEBUG=True` Django appends every query to `connection.queries` forever, so a long-running dev process grows without bound |

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/django/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| django_version | number (4.2-6.x) | 5.2 | Which `Django >=X.Y` gated advice applies when the project's version is unknown, and which deprecations to flag |
| database | postgres \| mysql \| sqlite \| oracle | postgres | Switches ORM and migration advice: `select_for_update` options, server-side cursors, JSON lookups, whether `__date` needs loaded timezone tables |
| api_layer | none \| drf \| ninja \| plain-json | drf | Which request/response idiom generated endpoints use, and whether `drf.md` guidance applies at all |
| settings_layout | single \| split-by-env \| env-vars | split-by-env | Where a new setting is written and how secrets are read (→ `settings.md`) |
| project_layout | flat \| apps-package | flat | Where a new app is created and which dotted names appear in `INSTALLED_APPS` and `AppConfig.name` (→ `layout.md`) |
| task_queue | none \| celery \| rq \| django-tasks | celery | Shape of background-job examples; with `none`, work is inlined behind `transaction.on_commit` instead (→ `tasks.md`) |
| test_runner | django \| pytest-django | django | Whether tests are emitted as `TestCase` classes or pytest functions with fixtures (→ `testing.md`) |
| deploy_target | gunicorn-wsgi \| uvicorn-asgi \| paas \| serverless | gunicorn-wsgi | Worker-count formula, static-file strategy, and whether long-lived database connections are safe (→ `deployment.md`) |
| destructive_confirm | bool | true | `migrate --fake`, `flush`, `sqlflush`, reverse migrations and drop-column operations are emitted for review instead of run |

Preference areas — customizable dimensions; a stated preference is recorded in `config.yaml` and applied from then on:

- **Tooling** — dependency manager and venv layout, debug toolbar vs profiler, `django-filter`/`factory_boy`/`allauth` and friends, migration linting in CI
- **Thresholds** — query budget per view, default page size, cache TTLs, backfill batch size, the slow-request threshold worth reporting
- **Conventions** — fat models vs a service layer, URL and view naming, `related_name` style, serializer naming, app naming style
- **Platform** — database engine and version, cache and broker backends, media storage backend, hosting target, Python version floor
- **Risk posture** — whether migrations may be applied directly, whether raw SQL is allowed, how hard to push back on `fields = "__all__"` and `@csrf_exempt`
- **Output format** — whole files vs diffs, how much explanation ships with generated code, type hints and docstrings
- **Work order** — test-first vs code-first, whether a migration review gate precedes merge, when `check --deploy` runs
- **Integrations** — auth provider and SSO, email and payment providers, error tracking, broker choice, object storage
- **Restrictions** — banned packages, LTS-only policy, PII fields that must never be logged, compliance regimes requiring audit trails
- **Cadence** — dependency and security upgrade rhythm, LTS upgrade window, session and log cleanup schedules

## Output Gates

Before emitting models, a migration, a view, or a serializer:

- Does every view that lists related data declare its query budget, with `select_related`/`prefetch_related` to match (Rule 1)?
- Does the migration touch a live table, and if so, is it split expand → backfill → contract (Rule 6)?
- Is every external side effect wrapped in `transaction.on_commit` (Rule 5)?
- Do new foreign keys and frequently filtered columns get an index in the same migration?
- Are `ModelForm` and `ModelSerializer` field lists explicit, never `"__all__"`?
- Does every object fetched by an ID from the request also filter on ownership or permission (→ `security.md`)?
- Are user-supplied strings rendered without `|safe`/`mark_safe`, and JSON handed to scripts through `{{ data|json_script:"id" }}`?
- Timestamps via `timezone.now()` / `timezone.localdate()`, never `datetime.now()` / `date.today()`?

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Assuming `Model.save()` validates | `save()` never calls `full_clean()`: `choices`, validators and most `max_length` checks are form-layer only | Enforce in the database with `Meta.constraints`, or call `full_clean()` explicitly |
| `null=True` on a text field | Two empty states (`""` and `NULL`) that every query then has to handle | `blank=True` alone; keep `null=True` for non-text columns |
| `Meta.ordering` on a busy model | Every query inherits the sort — and in `values().annotate()` the ordering column silently joins the `GROUP BY`, changing your aggregate | Order at the queryset; `.order_by()` with no arguments clears an inherited sort |
| `exclude(field=None)` to find NULLs | Compiles to `NOT (field = NULL)`, which drops NULL rows instead of selecting them | `filter(field__isnull=True)` |
| `queryset.delete()` over millions of rows | Django loads the objects to cascade and fire signals in Python | Delete in primary-key batches, or move the cascade into the database and own it there |
| `get_object_or_404(Order, pk=pk)` in a user-facing view | Any authenticated user can read any ID | Scope the lookup: `get_object_or_404(Order, pk=pk, user=request.user)` |
| `fields = "__all__"` on a ModelForm or ModelSerializer | Every future field becomes exposed and writable the day it is added | List fields explicitly and let that list be the review surface |
| `@login_required` on a class-based view | The decorator wraps the class object, not the request handler | `LoginRequiredMixin` first in the bases, or `method_decorator` on `dispatch` |
| Signals carrying business logic | They fire from anywhere, are invisible at the call site, and never run for `update()`/`bulk_create()` | An explicit service function; keep signals for cross-app decoupling you actually need |
| `datetime.now()` in models or views | Naive local time; with `USE_TZ=True` (the default in Django >=5.0) you get a `RuntimeWarning` and drifted comparisons | `timezone.now()`, and `timezone.localdate()` for "today" |
| `.raw()` or `.extra()` built with f-strings | String interpolation is SQL injection regardless of the ORM around it | Bind parameters: `.raw("... WHERE id = %s", [pk])` |
| Reading `request.body` twice | The stream is consumed; the second read returns `b""` | Read once into a local, or use `request.POST` for form encodings |
| Leaving sessions to grow | The `django_session` table has no automatic cleanup | `manage.py clearsessions` on a schedule, or a cache-backed session engine |

## Where Experts Disagree

- **Fat models vs a service layer.** Model methods keep behavior next to the data and make the shell powerful; a service layer keeps transactions, side effects and orchestration in one readable place. The testable boundary: anything that spans two aggregates or touches the outside world (payments, email, tasks) belongs in a service, because that is precisely what has to be wrapped in `atomic()` and `on_commit`.
- **Signals.** One camp bans them as action at a distance; the other keeps them for genuine cross-app decoupling. Both agree they are the wrong tool inside a single app, and both concede they never fire for queryset-level writes — so a signal can never be the only enforcement of an invariant.
- **DRF vs plain views for JSON.** DRF earns its weight when you need content negotiation, browsable docs, permissions and pagination as policy; for a handful of endpoints it is a large surface to reason about. Boundary: a public API or more than a few endpoints → DRF or Ninja; three internal endpoints → `JsonResponse` with explicit validation.
- **Async Django.** Async views pay off for I/O fan-out (several outbound HTTP calls per request); they buy little where the request time is ORM queries, since that path still crosses a thread. Adopt per view, not per project (→ `async.md`).
- **UUID vs bigint primary keys.** UUIDs stop enumeration and let clients mint IDs offline; random v4 fragments the index and widens every foreign key. Common ground: exposing a sequential ID is only a problem when authorization is missing — the check protects the row, not the shape of the key.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/django (install if the user confirms):

- `py` — Python itself: imports, packaging, typing, asyncio internals, pytest mechanics
- `pg` — PostgreSQL underneath the ORM: EXPLAIN plans, index design, vacuum, locks, connection pooling
- `rest-api` — API design decisions above the framework: versioning, contracts, error shapes
- `fastapi` — when the service is async-first and needs no ORM, admin, or templates
- `auth` — protocol-level identity: OAuth flows, SSO, MFA, passwordless

## Feedback

- If useful, star it: https://clawic.com/skills/django
- Latest version: https://clawic.com/skills/django

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/django.
