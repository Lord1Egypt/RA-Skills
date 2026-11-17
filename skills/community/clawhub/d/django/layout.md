# Layout — Starting A Project, Apps, Where Code Goes

Two decisions here are expensive to reverse — the app boundaries and the app *labels* — because both are baked into migration history and table names. Everything else in this file is a preference you can change on a quiet afternoon.

## Starting A Project

```
django-admin startproject config .     # the "." matters: no nested config/config/
python manage.py startapp shop apps/shop     # target dir must already exist
```

- `startproject mysite` without the trailing dot creates `mysite/mysite/`, one wrapper directory that does nothing. `startproject config .` puts `manage.py` at the repository root and the settings package in `config/`.
- Naming the settings package `config` (rather than after the product) means the project name can change without a rename that touches `DJANGO_SETTINGS_MODULE`, `wsgi.py`, `asgi.py`, and every deployment environment.
- `startapp` into a subdirectory requires that the directory exists first; it does not create intermediate paths.
- Day one, in this order, because each is cheap now and expensive later: custom user model (`AUTH_USER_MODEL` before the first `migrate`), `DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"`, settings driven by environment variables, `.gitignore` with `.env` and `db.sqlite3`, and `makemigrations --check --dry-run` plus `check --deploy` in CI.

## The Two Shapes

| Shape | Tree | Fits |
|---|---|---|
| Flat | `manage.py`, `config/`, `shop/`, `accounts/`, `billing/` | Up to roughly a handful of apps; the default `startapp` output; nothing to explain to a newcomer |
| `apps/` package | `manage.py`, `config/`, `apps/shop/`, `apps/billing/` | Enough apps that the repository root stops being readable; keeps domain code visually separate from config, infra and tooling |

- With an `apps/` package, either add `apps/` to the path or use the dotted name everywhere: `INSTALLED_APPS = ["apps.shop"]`, and `AppConfig.name = "apps.shop"`. Mixing the two forms is what produces "app isn't loaded yet" for an app you can clearly see.
- The `apps/` directory needs no `__init__.py` if you always use the dotted form; add one if anything imports `apps.something` as a package.
- Neither shape is faster or more testable. Choose on how the repository root reads, and record the choice — the cost is inconsistency, not the shape.

## What Belongs In An App

- An app is a **deployable unit of models plus the code that owns them**. If it has no models and no migrations, it is probably a package, not an app.
- Split by domain (`orders`, `catalog`, `billing`), never by layer (`models`, `views`, `serializers`). Layer-split apps make every feature a change in four apps and every import a cycle candidate.
- One app per bounded piece of the product. The test: can you describe what it owns in one sentence without "and"? If not, it is two apps or it is one app pretending to be a framework.
- Shared code with no models goes in a plain package — `core/`, `common/`, `lib/`. Keep it dependency-free in one direction: domain apps import from `core`, `core` imports from no app. That single rule prevents most import cycles.
- The reverse smell is an app that imports models from four others. That is a coordination layer; give it its own name and let it depend downward.

## App Labels And Renaming

- The app **label** is the last component of `AppConfig.name` unless `label` is set explicitly. It becomes the migration namespace and the prefix of every table name (`shop_order`).
- Two apps whose paths end in the same segment (`billing.invoices` and `sales.invoices`) collide with `ImproperlyConfigured`; set `label` on one.
- Renaming an app after tables exist is a schema change, not a rename: the tables keep their old prefix. The paths are either keeping the old names with `Meta.db_table`, or writing `AlterModelTable` operations plus migrating the `django_migrations` and `django_content_type` rows. Both are surgery.
- Therefore: **spend the extra minute on the app name at `startapp` time.** It is the only decision in this file with no cheap undo.

```python
# apps/shop/apps.py
class ShopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.shop"
    label = "shop"          # keeps table names short and stable if the path moves
```

## Inside An App

```
apps/shop/
├── __init__.py
├── apps.py                  # AppConfig; signal registration in ready(), nothing else
├── models.py                # or models/ package with explicit imports in __init__.py
├── managers.py              # custom querysets and managers, out of models.py
├── services.py              # cross-model operations, transactions, side effects
├── selectors.py             # read paths, if the team separates reads from writes
├── admin.py  forms.py  urls.py  views.py  serializers.py  tasks.py
├── migrations/              # __init__.py required, or migrations silently do not exist
├── templates/shop/          # namespaced: loaders are first-match-wins across all apps
├── static/shop/             # same reason
└── tests/                   # package with __init__.py, or a single tests.py — not both
```

- Splitting `models.py` into a `models/` package works only if `models/__init__.py` imports every model; the autodetector sees what is imported, and a model nobody imports produces "No changes detected".
- `templates/shop/index.html`, not `templates/index.html`. App template directories are searched in `INSTALLED_APPS` order and the first match wins, so an unnamespaced template silently shadows another app's.
- `apps.py` runs early. `ready()` is for connecting signals and registering checks — a query there runs during `migrate` against a schema that may not exist yet.
- Keep `views.py` free of business rules that two callers need. A view, a management command and a task all calling `services.place_order()` is the shape that keeps the admin and the API honest.

## Settings, URLs And Entry Points

```
config/
├── settings/
│   ├── base.py     dev.py     prod.py     test.py
├── urls.py          # includes each app's urls with a namespace
├── wsgi.py  asgi.py
```

- The root URLConf includes app URLConfs with `app_name` + `namespace`; app URLs never reach outside their own app. That is what keeps `{% url "shop:order-detail" %}` stable when routes move.
- `DJANGO_SETTINGS_MODULE` must be set explicitly in every non-`manage.py` entry point: the WSGI/ASGI module, the task worker, the scheduler, CI. A default that only lives in `manage.py` is how production ends up on dev settings.
- Requirements: one lockfile the build uses, and a dependency list a human edits. Whether that is `pyproject.toml`, `requirements/*.txt`, or a lock from a package manager is a preference; having exactly one source of truth is not.

## When To Split The Repository

- More apps is not more coupling — Django apps in one repository still deploy as one process and share one database. Splitting into services buys independent deploys and costs you cross-database joins, distributed transactions, and a network hop per call.
- Split when two parts have genuinely different scaling or availability needs, not when the app list gets long. Before that, an `apps/` package and a one-directional import rule get you the same clarity for free.
