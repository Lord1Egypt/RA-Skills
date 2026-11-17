# Models — Fields, Relations, Constraints, Managers, Signals

The model layer is the only place where a rule can be made impossible to break. Anything enforced only in a form, a serializer, or a signal is enforced only on the paths that go through them — and `update()`, `bulk_create()`, the admin's bulk actions, the shell and a data migration all skip those paths.

## Fields

- `null` is the database; `blank` is validation. Text columns get `blank=True` alone — `null=True` on a `CharField`/`TextField` creates two empty states that every query has to handle.
- `choices` is validated by forms and `full_clean()`, never by the database. Back a real invariant with a `CheckConstraint`, or accept that a script can write anything.
- `default=timezone.now` (the callable) evaluates per row; `default=timezone.now()` freezes at import time and stamps every row with the moment the process started. The same trap applies to `default=[]` and `default={}` — use `list`/`dict`, since mutable defaults are shared.
- `auto_now=True` overwrites on every `save()` and cannot be set manually; `auto_now_add=True` writes once and is not editable. When you need to backdate rows, use `default=timezone.now` and set the value yourself.
- `DecimalField` for money, never `FloatField`. `max_digits` counts all digits, `decimal_places` counts those after the point, so `max_digits=10, decimal_places=2` maxes out at 99,999,999.99.
- `DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"` project-wide. A 32-bit `AutoField` runs out at 2147483647, and changing the type later rewrites the table and every FK to it.
- `JSONField` (core since Django >=3.1) is a real column with real lookups (`data__key`, `data__contains`). Anything you filter, sort, or join on frequently belongs in its own column: JSON keys carry no per-key statistics for the planner.
- `db_default=` (Django >=5.0) puts the default in the schema, so rows inserted by raw SQL and other services get it too; `default=` is Python-side only.
- `GeneratedField` (Django >=5.0) stores a computed column the database maintains — the denormalization that cannot drift.

## Relations

- `on_delete` is required and it is a design decision: `CASCADE` (child is meaningless alone), `PROTECT` (refuse the delete), `RESTRICT`, `SET_NULL` (needs `null=True`), `SET_DEFAULT`, `DO_NOTHING` (you own the integrity, in the database or by hand).
- Django performs cascades in Python: it loads the children, fires their signals, and deletes them. A `PROTECT` you did not expect is loud; a `CASCADE` over a million rows is slow and memory-hungry.
- String references (`ForeignKey("shop.Order")`, `"self"`) break import cycles and are the default habit worth having.
- `related_name` is how the reverse side is spelled. Two FKs from the same model to the same target need distinct names or the system check fails; `related_name="+"` disables the reverse accessor entirely. In abstract base classes, use `related_name="%(app_label)s_%(class)s_set"` so subclasses do not collide.
- `related_query_name` controls the name used in *filters*, which is not automatically the same as `related_name`.
- `OneToOneField` reverse access raises `RelatedObjectDoesNotExist` when the row is absent — `hasattr(user, "profile")` or `getattr(..., None)`, not a `try/except AttributeError`.
- M2M with an explicit `through` model: `add()`/`remove()` work only when the through model has no required extra fields beyond the two FKs, or when you pass `through_defaults`. Otherwise create the through rows directly.
- Index foreign key columns you filter or join on. Django creates an index for FKs by default on most backends, but not for the *combination* you actually query — that is a composite index you declare.

## Constraints And Indexes

```python
class Meta:
    constraints = [
        models.UniqueConstraint(fields=["tenant", "slug"], name="uniq_tenant_slug"),
        models.UniqueConstraint(
            fields=["user"], condition=models.Q(is_default=True), name="one_default_per_user"
        ),
        models.CheckConstraint(condition=models.Q(price__gte=0), name="price_non_negative"),
        # the keyword is `check=` before Django 5.1, `condition=` from 5.1 on
    ]
    indexes = [models.Index(fields=["tenant", "-created_at"], name="idx_tenant_recent")]
```

- `UniqueConstraint` supersedes `unique_together`: only the constraint form supports conditions (partial uniqueness) and expressions (`Lower("email")` for case-insensitive uniqueness). `unique_together` still works; new code should not add it.
- `index_together` was deprecated in Django >=4.2 and removed in >=5.1 — `Meta.indexes` is the replacement.
- Composite index column order follows the query: equality columns first, then the one range or sort column. `(tenant, -created_at)` answers "latest 20 for this tenant" from the first 20 index entries.
- A unique constraint is also the only safe partner for `get_or_create` — it is what turns a lost race into an `IntegrityError` instead of a duplicate row.
- Constraints are checked by the database, so they hold against raw SQL, other services, and data migrations. That is the whole reason to prefer them over `clean()`.

## Validation

- `Model.save()` does **not** call `full_clean()`. `ModelForm` and DRF's `ModelSerializer` call the validators for you; nothing else does.
- Put invariants in three places deliberately: database constraint (always true), `clean()` (cross-field rules the form should show), field validators (single-field rules reused across forms).
- `clean()` raising `ValidationError({"field": "..."})` attaches the message to that field in any form using the model.
- Calling `full_clean()` inside `save()` is a defensible house rule, but it costs a uniqueness query per save and makes `bulk_create` inconsistent with the single-object path. Decide once, project-wide.

## Managers And Querysets

```python
class OrderQuerySet(models.QuerySet):
    def paid(self):
        return self.filter(status="paid")

class Order(models.Model):
    objects = OrderQuerySet.as_manager()
```

- `QuerySet.as_manager()` gives chainable methods on both the manager and any queryset — a custom `Manager` subclass with the same method does not chain.
- The **first** manager defined on a model becomes `_default_manager`, which the admin, related descriptors and `dumpdata` use. A filtered manager declared first will silently hide rows from all of them.
- Related managers (`customer.orders`) use the related model's `_default_manager` class but not your custom manager instance methods unless the manager sets `use_for_related_fields`-style behavior through `Meta.base_manager_name`.
- Soft delete via a default manager that filters `deleted_at__isnull=True` is the classic footgun: cascades, the admin, and unique constraints all still see the hidden rows. If you soft-delete, keep `all_objects` available and expect uniqueness to need a `condition`.

## Inheritance

| Style | Storage | When |
|---|---|---|
| Abstract base (`Meta.abstract = True`) | No table; fields copied into children | Shared fields and methods. The default choice |
| Multi-table inheritance | Parent table + child table joined by an implicit O2O | Rarely worth it: every child query joins, and the parent's manager returns rows you cannot cast |
| Proxy (`Meta.proxy = True`) | No new table | Different default ordering, managers, or admin behavior over the same rows |
| Explicit `OneToOneField` | Two tables you control | Multi-table's benefits with an obvious join you chose |

## Signals

- Signals fire for `save()` and `delete()` on instances — never for `update()`, `bulk_create()`, `bulk_update()`, or a queryset `delete()` on the *related* rows Django cascades in bulk.
- `post_save` receives `created` and `update_fields`; guard on both, or a partial save re-runs work meant for creation.
- Register handlers in `AppConfig.ready()` by importing the module. Importing them at the bottom of `models.py` also works and is how duplicate registrations happen — pass `dispatch_uid="..."` to make registration idempotent.
- A handler that writes to the same model must guard against recursion; a handler that calls an external service must go through `transaction.on_commit`, or it fires for rows that then roll back.
- `m2m_changed` fires several times per operation (`pre_add`, `post_add`, ...) with a `reverse` flag — check `action` first, always.

## Timezones In Models

- With `USE_TZ = True` (the default since Django >=5.0) `DateTimeField` stores an aware UTC instant. `timezone.now()` is aware; `datetime.now()` is not, and comparing them raises warnings and wrong results.
- "Today" is `timezone.localdate()`, not `date.today()` — the second uses the server's local time, which is UTC on most hosts and gives you off-by-one days near midnight.
- `DateField` has no timezone. Storing a "date" that means "a moment" is a bug that only appears for users in other zones.
- `__date` lookups convert in the database using `TIME_ZONE`; on MySQL that requires the timezone tables to be loaded, or the lookup silently misgroups.
