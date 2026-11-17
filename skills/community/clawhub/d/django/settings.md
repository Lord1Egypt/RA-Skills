# Settings — Layout, Environment, Logging, Timezone

Settings are a plain Python module read once at startup. Everything confusing about them comes from that: values are frozen at import, `override_settings` cannot reach what was already read, and the module that gets imported depends on an environment variable set outside your code.

## Contents

- Layout
- Environment Variables
- Databases
- Timezone
- Logging
- Caches And Sessions
- Apps And Startup

## Layout

Three workable shapes, in increasing order of team size:

1. **Single `settings.py` driven by environment variables.** Every difference between environments is a variable. Simplest, and the model twelve-factor platforms assume.
2. **Split package** — `settings/base.py`, `settings/dev.py`, `settings/prod.py`, each importing `from .base import *`, selected with `DJANGO_SETTINGS_MODULE`. Differences are readable side by side; the risk is a dev-only value silently inherited into prod.
3. **Base plus a typed config object** (django-environ, pydantic-settings). Fails at startup on a missing or malformed variable instead of at the first request that needs it.

- `DJANGO_SETTINGS_MODULE` is what actually chooses; `manage.py` sets a default. A production process without it explicitly set is one `manage.py` edit away from running dev settings.
- Never `from .prod import *` inside dev, or vice versa: the import direction must always be base → specific.
- Reading a setting at module import in your own code freezes it: `PAGE_SIZE = settings.PAGE_SIZE` at the top of a module ignores every later `override_settings`. Read `settings.X` inside the function.
- Settings are not a config file for arbitrary application data. Anything a non-developer changes belongs in the database or a constance-style store; a settings change requires a deploy.

## Environment Variables

```python
import os
def env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and value is None:
        raise ImproperlyConfigured(f"Missing required environment variable: {name}")
    return value

SECRET_KEY = env("DJANGO_SECRET_KEY", required=True)
DEBUG = env("DJANGO_DEBUG", "0") == "1"
ALLOWED_HOSTS = [h for h in env("DJANGO_ALLOWED_HOSTS", "").split(",") if h]
```

- Environment variables are strings. `bool(os.environ.get("DEBUG"))` is `True` for the string `"0"` and for `"False"` — the classic way to ship a production site with the debug page enabled.
- Fail loudly at startup for anything required. A missing `SECRET_KEY` that defaults to `""` produces sessions nobody can validate rather than an error you can see.
- `.env` files are a development convenience. Load them explicitly and never commit one; in production the platform supplies the variables.
- Secrets do not belong in settings literals, in the repo, or in the image.

## Databases

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"), "USER": env("DB_USER"), "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"), "PORT": env("DB_PORT", "5432"),
        "CONN_MAX_AGE": 60,
        "CONN_HEALTH_CHECKS": True,      # Django >=4.1
        "OPTIONS": {"connect_timeout": 5},
    }
}
```

- `CONN_MAX_AGE` defaults to `0`: a new connection, with its authentication handshake, on every request. Any positive value reuses connections between requests within a worker.
- Persistent connections multiply: `peak_connections = instances × workers_per_instance × threads_per_worker`. Two instances of sixteen sync workers with `CONN_MAX_AGE > 0` hold 32 connections idle; against PostgreSQL's documented default `max_connections` of 100 that is a third of the server before any other client connects.
- `CONN_HEALTH_CHECKS = True` re-validates a reused connection before the request, which is what stops "server closed the connection unexpectedly" after an idle period behind a proxy or a database restart.
- Behind a transaction-pooling PgBouncer, disable server-side cursors (`"DISABLE_SERVER_SIDE_CURSORS": True`) or `.iterator()` breaks, and expect `CONN_MAX_AGE = 0` to be the correct setting because the pooler owns the connections.
- `ATOMIC_REQUESTS = True` per database wraps every request in a transaction: safe, and it holds a write transaction across template rendering.

## Timezone

- `USE_TZ = True` (the default since Django >=5.0) stores aware UTC datetimes. `TIME_ZONE` is what the ORM converts to for `__date`/`__year` lookups and what templates render by default.
- Changing `TIME_ZONE` after data exists changes interpretation of `DateField`s and of any naive datetime already stored. Aware datetimes are unaffected — one more reason for `USE_TZ = True` from day one.

## Logging

The default logging configuration writes almost nothing when `DEBUG = False`: `django.request` errors go to `mail_admins`, and that is it. A blank 500 with no trace is that default working as designed.

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"plain": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "plain"}},
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "django.db.backends": {"level": "INFO"},   # DEBUG prints every query
    },
}
```

- `disable_existing_loggers: False` — the default `True` silences every logger created before settings load, including third-party ones.
- Log to stdout in containers and let the platform collect it; a rotating file handler inside a container writes to a filesystem nobody reads.
- `propagate: False` on a logger stops it reaching the root handler; forgetting it is why messages appear twice.
- `django.db.backends` at DEBUG prints every query with its duration — the fastest ad-hoc profiler, and unusable as a permanent setting.
- `django.security.*` loggers report `DisallowedHost`, suspicious operations and CSRF failures. Route them somewhere a human sees.
- `ADMINS` plus the default `AdminEmailHandler` sends unhandled exceptions by email, including request data. An error tracker with scrubbing is the better destination.

## Caches And Sessions

- `CACHES["default"]["TIMEOUT"]` defaults to 300 seconds; `None` means never expire and `0` means never cache.
- The default `LocMemCache` is per-process: with several workers, each one has its own copy, so invalidation in one is invisible to the others. Only Redis/Memcached give a shared cache.
- `SESSION_ENGINE` decides where sessions live. The database backend requires `clearsessions` on a schedule; a pure cache backend loses every session on a restart or eviction.
- `KEY_PREFIX` and `VERSION` are how two environments share one Redis without reading each other's keys — and how you invalidate everything at once during a deploy.

## Apps And Startup

- `INSTALLED_APPS` order matters for template and static file resolution (first match wins) and for overriding built-in templates such as the admin's.
- `AppConfig.ready()` runs once per process after the registry is populated: the correct home for signal registration and system checks. It must not query the database — it runs during `migrate` and during management commands on an empty schema.
- Custom system checks (`@register(Tags.security)`) are how you make a house rule fail `manage.py check` in CI instead of in review.
- `django.setup()` is required in any standalone script before importing app code, and `DJANGO_SETTINGS_MODULE` must be set before that call — a management command is the better shape for anything recurring.
