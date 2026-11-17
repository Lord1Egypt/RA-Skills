# ORM — Querysets, Joins, Aggregation, Transactions

Mental model: a QuerySet is a lazily built SQL statement plus a result cache. Nothing reaches the database until you iterate, `len()`, `bool()`, `repr()`, slice with a step, or pickle it. Every surprise below is either "it evaluated when you did not expect" or "the SQL is not the shape you imagined".

## Evaluation And Caching

- Iterating one queryset twice reuses its cache; building two querysets the same way runs two statements. Assign once (`orders = list(qs)`) when the rows cross function boundaries.
- Slicing before evaluation adds `LIMIT/OFFSET` to the SQL (cheap); slicing an evaluated queryset slices the cached list (free); `qs[5]` on an unevaluated queryset issues its own `LIMIT 1 OFFSET 5`.
- `exists()` compiles to `SELECT 1 ... LIMIT 1`; `bool(qs)` fetches every row. `count()` compiles to `COUNT(*)`; `len(qs)` fetches every row. `len()` is the cheaper choice only when you were going to use the rows anyway.
- `.iterator()` streams instead of caching — necessary above a few hundred thousand rows. It bypasses the result cache, and it drops `prefetch_related` unless you pass `chunk_size` (Django >=4.1).
- `LIMIT` without `ORDER BY` returns an arbitrary page. Every `first()`, `last()`, or slice on an unordered queryset is a coin flip that stays stable in dev and flips under production concurrency.

## Fixing N+1

| Relation direction | Tool | Result |
|---|---|---|
| Forward `ForeignKey` / `OneToOneField` (`order.customer`) | `select_related("customer")` | One query, SQL JOIN |
| Reverse FK (`customer.orders`) | `prefetch_related("orders")` | Two queries, joined in Python |
| `ManyToManyField` | `prefetch_related("tags")` | Two queries (three through an explicit through model) |
| Reverse `OneToOne` (`user.profile`) | `select_related("profile")` | One query — reverse O2O is the exception that joins |
| Nested (`order.customer.company`) | `select_related("customer__company")` | Still one query |
| Filtered or ordered relation | `prefetch_related(Prefetch("orders", queryset=Order.objects.filter(paid=True)))` | Two queries, filter applied inside the prefetch |

- Calling `.filter()`, `.exclude()` or `.order_by()` on an already-prefetched manager throws the cache away and re-queries once per parent — the N+1 you thought you had fixed. Filter inside `Prefetch(queryset=...)`, or filter in Python over `obj.orders.all()`.
- `select_related()` with no arguments follows every non-null FK on the model: convenient, and a wide row you did not ask for. Name the relations.
- `only()`/`defer()` fight with `select_related`: deferring a field the join needs raises `FieldError`, and touching a deferred field later costs one query *per object*.
- `prefetch_related_objects(objs, "tags")` applies a prefetch to a list you already hold — the escape hatch when the objects did not come from a single queryset.

## Filters, Joins And Duplicates

- **Chained vs single filter on a multi-valued relation.** `Blog.objects.filter(entry__year=2026).filter(entry__author="A")` matches a blog with *some* 2026 entry and *some* entry by A — two JOINs, possibly different rows. `Blog.objects.filter(entry__year=2026, entry__author="A")` requires one entry satisfying both. Invisible in the Python, decisive in the results.
- Any JOIN across a to-many relation can multiply rows. `.distinct()` patches it, but if you also `.order_by()` a column of the joined table, that column enters the SELECT list and `DISTINCT` no longer deduplicates what you meant.
- `Q` objects compose: `filter(Q(a=1) | Q(b=2))`; positional `Q`s must precede keyword arguments. `~Q(...)` negates, with the same NULL caveat as `exclude`.
- Lookups that replace hand-written SQL: `__in` (accepts a queryset and becomes a subquery), `__range`, `__isnull`, `__date`/`__year` (on MySQL these need the timezone tables loaded), `__icontains`, `__regex`, and `__contains`/`__overlap` on `JSONField`/`ArrayField`.
- `__in` with a large Python list binds every value as a parameter and hits the backend's parameter ceiling. Pass the subquery, or batch the list.

## Aggregation

- `aggregate()` returns a dict and ends the chain; `annotate()` adds a column per row and stays chainable.
- **Two annotations over two different to-many relations inflate each other.** `annotate(Count("items"), Count("comments"))` builds a cartesian join and both counts come back multiplied. Fixes in order of preference: `Count("items", distinct=True)`, two separate queries, or `Subquery(...)` with `OuterRef`.
- `values("x").annotate(...)` groups by `x`; `annotate(...).values("x")` does not group at all. The order of those two calls *is* the `GROUP BY`.
- A model's `Meta.ordering` slips its column into that `GROUP BY` and silently changes the grouping. Clear it with a bare `.order_by()` before aggregating.
- `Sum` over an all-NULL set returns `None`, not `0` — `Coalesce(Sum("x"), 0)`. `Count` counts rows, duplicates included.
- Conditional aggregation removes most Python post-processing: `Count("id", filter=Q(status="paid"))`.
- Window functions (`Window(expression=Rank(), partition_by=..., order_by=...)`) compute running totals and per-group ranks in the database. They cannot appear inside `filter()` — wrap the annotated queryset in a subquery.

## Writing Efficiently

- `bulk_create(objs, batch_size=N)` — one `INSERT` per batch, no `save()`, no signals. Primary keys come back on backends that support `RETURNING` (PostgreSQL always). Size the batch from the backend's bind-parameter ceiling: `batch_size ≈ parameter_limit / columns_per_row`; PostgreSQL's wire protocol caps at 65535 parameters, so a 10-column model tops out near 6500 rows per statement.
- `bulk_create(..., update_conflicts=True, update_fields=[...], unique_fields=[...])` (Django >=4.1) is the ORM's upsert.
- `bulk_update(objs, ["field"], batch_size=N)` emits a `CASE` expression per field; no signals, no `auto_now`.
- `get_or_create` and `update_or_create` are two statements with a race between them. They are safe only when a unique constraint exists to lose the race against — catch `IntegrityError` and re-read.
- `Model.save(update_fields=["status"])` writes one column instead of all: fewer lost updates between concurrent writers, and a far narrower blast radius when two requests hold stale copies.
- `F()` works in filters too (`filter(sold__gt=F("stock"))`) and inside `update()` one relation level deep.

## Transactions

- `transaction.atomic()` as decorator or context manager; nested blocks are savepoints, not nested transactions.
- After an error inside the block the connection refuses further queries until rollback (SKILL.md Core Rules 7). To recover in place, isolate the risky statement in its own inner `atomic()`.
- `ATOMIC_REQUESTS = True` wraps every request in a transaction: simple and correct, but it holds a write transaction across template rendering and any outbound HTTP call in the view. Prefer explicit blocks around the writes.
- `transaction.on_commit(callback)` runs after COMMIT, and runs immediately when there is no active transaction — the same code path works in both. It never runs on rollback, which is the entire point.
- `atomic(durable=True)` (Django >=3.2) raises if it finds itself nested — the way to assert "this block really commits".
- Long transactions are the hidden cost: every touched row stays locked, and on PostgreSQL the oldest open transaction blocks cleanup database-wide. Put network calls before or after the block, never inside it.

## Locking And Concurrency

- `select_for_update()` must run inside `atomic()`; outside it raises `TransactionManagementError`. It holds the rows until commit.
- `select_for_update(skip_locked=True)` is a work queue: each worker claims rows nobody else holds. `nowait=True` fails fast instead of waiting. Backend support varies; SQLite has neither.
- Combined with `select_related()` it locks the joined tables too, unless you pass `of=("self",)`.
- The alternative is optimistic concurrency: `Model.objects.filter(pk=pk, version=old).update(version=old + 1, ...)`, treating a return value of `0` as "someone else won". No locks, no deadlocks, one extra column.
- Deadlocks come from two transactions taking the same rows in opposite orders. Impose one ordering (sort the ids before locking) rather than only adding retries.

## Raw SQL, When You Mean It

- `Model.objects.raw("SELECT ... WHERE id = %s", [pk])` returns model instances; every column you omit becomes a deferred field that costs a query on access.
- `connection.cursor()` for statements that are not row-shaped. Pass parameters as a sequence; `%s` is the placeholder on every backend, and string formatting is an injection (SKILL.md Traps).
- `QuerySet.extra()` is legacy and hard to keep safe. Reach for expressions first — `Func`, `Cast`, `Coalesce`, `Greatest`, `RawSQL` inside `annotate()` cover most of what `extra()` was used for.
- Raw writes join the surrounding transaction normally; what surprises people is that they are invisible to signals and to `on_commit` bookkeeping you may have wired to the ORM path.

## Inspection Toolkit

```python
str(qs.query)              # the SQL, parameters inlined — for reading, never for execution
qs.explain(analyze=True)   # the database's own plan (options are backend-specific)
qs.query.get_compiler("default").as_sql()   # SQL plus the real parameter tuple
from django.test.utils import CaptureQueriesContext   # count and inspect in any code path
from django.db import reset_queries                    # clear connection.queries between measurements
```
