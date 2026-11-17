# Migrations — Generating, Merging, and Changing a Live Schema

Two separate problems live here and they need different reflexes: **making Django produce the migration you meant** (a graph and autodetector problem) and **applying it without taking the site down** (a lock and volume problem). Everything below is one or the other.

## Making The Right Migration

- `makemigrations` compares your models against the *state built by replaying existing migrations*, not against the live database. That is why a hand-edited database and a healthy migration graph can disagree indefinitely.
- "No changes detected": the app is missing from `INSTALLED_APPS`, its `migrations/` package has no `__init__.py`, or the models are in a module nothing imports. `makemigrations <app>` names the app explicitly and reports the real reason more often.
- Always read the generated file before committing. The autodetector guesses; a rename it did not detect becomes `RemoveField` + `AddField`, which is a data-destroying pair that applies cleanly.
- Renames: run `makemigrations` interactively and answer the "did you rename" prompt, or write `RenameField`/`RenameModel` yourself. In a non-interactive CI run the prompt is a failure, not a question.
- `makemigrations --check --dry-run` in CI fails the build when someone changed a model without generating the migration. It is the single highest-value migration check.
- `sqlmigrate app 0007` prints the SQL a migration will emit. Read it before applying anything to a table that matters.
- A migration that keeps regenerating on every developer's machine means a non-deterministic model definition: a `choices` list built from a set, a `default` that is a lambda, or a field ordering that depends on dict iteration.

## The Graph

- Migrations form a DAG per app, linked across apps by `dependencies`. Two branches merged from git create two leaf nodes and `makemigrations --merge` writes the join. Never renumber or delete a migration that another developer has applied.
- `run_before` handles the rarer direction: "this migration must precede one in another app".
- A migration that adds a FK to another app must depend on the migration that created the target. Django usually adds it; when you write operations by hand, you must.
- `InconsistentMigrationHistory` means `django_migrations` records a migration as applied before one of its dependencies. It comes from swapping the user model late, re-pointing a FK, or restoring a database from a different branch. Repair by aligning the recorded history with the graph — deleting rows from `django_migrations` is surgery, not a fix, and needs a backup first.
- Squashing (`squashmigrations app 0001 0042`) collapses history into one file that keeps `replaces = [...]`. Every environment must have applied the full range before you delete the originals — the squash is only equivalent for a database that reached the end of the replaced span.

## Data Migrations

```python
def forwards(apps, schema_editor):
    Order = apps.get_model("shop", "Order")   # historical model, never the imported one
    for pk in Order.objects.filter(total__isnull=True).values_list("pk", flat=True).iterator():
        ...

class Migration(migrations.Migration):
    dependencies = [("shop", "0006_add_total")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
```

- `apps.get_model()` returns the model *as it existed at this point in history*. Importing the real model works today and breaks the day someone adds a field, because replaying old migrations then references a column that does not exist yet.
- Historical models carry fields and managers but **not** your custom methods, `save()` overrides, or signals. Write the logic inline.
- Always pass a reverse function; `RunPython.noop` is an explicit "this is not reversible, and I decided that".
- Keep schema operations and data operations in separate migrations. On PostgreSQL, DDL and DML in one transaction can turn a fast metadata change into a long lock; on MySQL, DDL commits implicitly and a failed data step leaves you half-migrated.
- Big backfills do not belong in a migration at all. A migration blocks the deploy: a management command that batches, commits and can resume is the right shape.

## Applying To A Live Database

The lock, not the row count, is what causes an outage: a schema change waiting for a lock queues every later query on that table behind it.

| Change | Cost |
|---|---|
| Add nullable column | Metadata-only on modern PostgreSQL and MySQL — safe |
| Add column with a constant default | Metadata-only on PostgreSQL >=11; older engines rewrite the table |
| Add column with a volatile default (`now()`, `uuid4()`) | Full table rewrite — add nullable, backfill, then set the default |
| Add NOT NULL to an existing column | Full scan under lock — add a validated check constraint first where the backend allows it |
| Add index | Blocks writes unless created concurrently; Django's `AddIndexConcurrently` (PostgreSQL) needs `atomic = False` |
| Drop column | Fast, and irreversible: it is the contract step, deployed after nothing reads the column |
| Change column type | Usually a rewrite; widening `varchar` is often metadata-only |
| Rename column | Instant in the database, breaking for any old process still running the previous code |

**Expand / backfill / contract**, the sequence that survives a rolling deploy:

1. **Expand** — add the nullable column or new table. Deploy code that writes both shapes and reads the old one.
2. **Backfill** — a batched management command with a resume key, run outside the deploy.
3. **Switch** — deploy code that reads the new shape.
4. **Contract** — a later migration adds NOT NULL and drops the old column, once no running process references it.

Renames are the same dance in disguise: add the new column, dual-write, backfill, switch reads, drop the old one. A single `RenameField` requires that no old process is still serving requests, which a rolling deploy cannot promise.

## Non-Atomic And Concurrent Operations

```python
class Migration(migrations.Migration):
    atomic = False          # required for CREATE INDEX CONCURRENTLY on PostgreSQL
    operations = [AddIndexConcurrently(model_name="order", index=...)]
```

- With `atomic = False`, a failure halfway leaves the earlier operations applied. Keep such migrations to a single operation so "did it run?" has one answer.
- MySQL has no transactional DDL at all: every migration on MySQL is effectively non-atomic, so one file per operation is the safer default there.
- A concurrent index build that fails leaves an invalid index behind on PostgreSQL; check and drop it before retrying.

## Testing And Recovering

- `migrate app 0006` migrates backwards to that number, running each reverse operation. Reverse only works if every operation is reversible — the reason `RunPython` needs its reverse argument.
- Rehearse on a restored copy of production, not on dev data. Duration scales with rows, and dev has none of them.
- `migrate --plan` shows what would run, in order, before you commit to it.
- `migrate --fake` writes a row in `django_migrations` without touching the schema. It is correct exactly once: when the schema already matches. Any other use produces a database whose recorded history is a lie, and the next developer to run `makemigrations` inherits it.
- `migrate --fake-initial` is the narrower, safer variant for adopting an existing database.
- A migration that fails halfway on PostgreSQL rolls back cleanly (transactional DDL) unless it declared `atomic = False`. On MySQL, check the schema by hand before retrying.
- Tests that run against a fresh database from migrations catch broken history; `--no-migrations` (pytest-django) or a cached test database hides it. Run the migration path at least in CI.

## Multiple Databases

- `migrate --database=analytics` runs per connection; a database router's `allow_migrate` decides which app lands where. A router that returns `None` for everything means every app migrates everywhere.
- Cross-database foreign keys do not exist. Model the relation as an id column plus explicit lookups, and expect no referential integrity from the engine.
