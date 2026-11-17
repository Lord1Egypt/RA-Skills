# Commands — The manage.py Toolkit

What each command really does, the flags that matter, and how to write one that is safe to run against production.

## Inspection Before Action

```
manage.py check                    # system checks: models, admin, urls, compatibility
manage.py check --deploy           # security audit of the CURRENT settings module
manage.py showmigrations           # applied [X] vs pending [ ], per app
manage.py showmigrations --plan    # the graph in execution order
manage.py sqlmigrate app 0007      # the SQL a migration would emit — read before applying
manage.py migrate --plan           # what would run now, in order
manage.py diffsettings             # your settings minus Django's defaults
manage.py shell -c "from django.db import connection; print(connection.settings_dict['NAME'])"
```

- `check --deploy` audits whatever settings module is active. Run it in CI against production settings, or it audits dev and reports nothing.
- `sqlmigrate` is the only way to know what a migration does to a large table before it does it.
- `diffsettings` is the fastest answer to "which environment am I actually in".

## The Ones With Sharp Edges

| Command | What it really does | Danger |
|---|---|---|
| `migrate --fake` | Writes a row in `django_migrations`, changes no schema | Correct only when the schema already matches; otherwise recorded history becomes a lie |
| `migrate --fake-initial` | Fakes only the initial migration if the tables exist | The safe variant for adopting an existing database |
| `migrate app 0006` | Migrates *backwards* to 0006 | Runs reverse operations; irreversible ones raise mid-way |
| `flush` | Deletes all data, keeps the schema, re-runs post-migrate | No confirmation with `--noinput` |
| `sqlflush` | Prints the truncation SQL | Harmless to print, catastrophic to pipe |
| `loaddata` | Loads a fixture, calling `save()` per object | Signals fire; existing rows with the same pk are overwritten |
| `dumpdata` | Serializes via `_default_manager` | A filtered default manager silently omits rows |
| `collectstatic` | Copies into `STATIC_ROOT` | `--clear` deletes the destination first; run at build time, not at boot |
| `createsuperuser` | Interactive; `--noinput` reads env vars | An automated superuser with a weak password is a permanent backdoor |
| `changepassword` | Sets a password from a prompt | The only safe way to reset one from a shell — never assign `user.password` |
| `clearsessions` | Deletes expired sessions | Not automatic; without it the session table grows forever |
| `shell` | A Python REPL with settings loaded | No transaction, no undo. A `delete()` here is production data gone |

## Writing A Management Command

```python
class Command(BaseCommand):
    help = "Backfill Order.total for rows created before the column existed."

    def add_arguments(self, parser):
        parser.add_argument("--batch-size", type=int, default=1000)
        parser.add_argument("--since-id", type=int, default=0)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        last = opts["since_id"]
        while True:
            batch = list(
                Order.objects.filter(pk__gt=last, total__isnull=True)
                .order_by("pk")[: opts["batch_size"]]
            )
            if not batch:
                break
            if not opts["dry_run"]:
                with transaction.atomic():
                    for order in batch:
                        order.total = order.compute_total()
                    Order.objects.bulk_update(batch, ["total"])
            last = batch[-1].pk
            self.stdout.write(f"through pk={last}")
```

The shape that matters, point by point:

- **Batch with a resume key.** `pk__gt=last` restarts where it stopped after a crash or a deploy; `OFFSET` re-reads everything it already skipped and drifts as rows change.
- **One transaction per batch, never one for the whole run.** A single transaction over a million rows holds locks for the duration and discards all the work if it fails at 90%.
- **`--dry-run` on anything destructive**, and make it the behavior a reviewer can check by reading the output.
- **Progress to `self.stdout`**, not `print` — the test runner and `call_command` capture it, and `--verbosity` then means something.
- **`CommandError` for user errors**; it exits with a non-zero status and no traceback, which is what a scheduler needs to see.
- **Idempotent.** Assume it will be run twice, because it will be: the filter (`total__isnull=True`) is what makes the second run cheap and harmless.
- Long backfills belong here, not in a migration — a migration blocks the deploy.
- `@transaction.atomic` on `handle` is available for short commands; for anything long-running it is the wrong default.
- Test with `call_command("backfill", batch_size=2, stdout=StringIO())` — commands are ordinary code and deserve ordinary tests.

## Scheduled Commands

- Cron or the platform scheduler invoking `manage.py <command>` is simpler than a task-queue beat process and easier to run by hand when it fails.
- Every scheduled command needs an overlap guard: the 02:00 run may still be going at 03:00. A cache key with a TTL or a database advisory lock, never a boolean column that a crash leaves set.
- Set `DJANGO_SETTINGS_MODULE` explicitly in the scheduler's environment; a cron job inherits almost nothing from an interactive shell.
- Redirect output somewhere durable and alert on non-zero exit. A silent scheduled command is a job that stopped running three weeks ago.

## Shell Discipline

- `manage.py shell` runs with no transaction. Wrap risky work explicitly:

```python
with transaction.atomic():
    qs = Order.objects.filter(...)
    print(qs.count())         # look first
    # qs.update(...)          # uncomment only after the count is what you expected
```

- Print the count before every bulk write. `filter()` with a typo matches everything, and `update()` reports the damage after doing it.
- `manage.py dbshell` opens the database client with the project's credentials — for reading. Schema changes made there are invisible to the migration graph and will fight the next `makemigrations`.
- Anything you would run twice belongs in a management command, in the repository, with a test. The shell is for looking.
