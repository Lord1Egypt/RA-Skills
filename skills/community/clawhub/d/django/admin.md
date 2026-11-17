# Admin — Running It Against Real Data Volume

The admin is a generated CRUD interface tuned for a few thousand rows. Every scaling problem below has the same shape: something the admin renders per row, or a relation it resolves per row, that was free in development.

## The Volume Failures

| Symptom | Cause | Fix |
|---|---|---|
| Change page takes many seconds or times out | A `ForeignKey` renders as a `<select>` containing every row of the target table | `autocomplete_fields = ["customer"]` (needs `search_fields` on the target admin), or `raw_id_fields` |
| Changelist issues one query per row | `list_display` touches a related object | `list_select_related = ("customer",)`, or override `get_queryset()` with `select_related`/`prefetch_related` |
| Changelist itself is slow before any row renders | The pagination `COUNT(*)` over a huge table | `show_full_result_count = False`, and lower `list_per_page` (default 100) |
| A filter dropdown takes seconds to build | `list_filter` on a FK renders every distinct related row | Filter on an indexed scalar, or write a `SimpleListFilter` with fixed choices |
| Save on an inline is very slow | Inlines re-render and re-validate every child row | `max_num`, `extra = 0`, and pagination in a custom view for genuinely large children |
| `date_hierarchy` drags the page down | Aggregates over the whole table to build the drill-down | Remove it, or keep it only on tables with an index on that column |
| Search returns nothing useful, slowly | `search_fields` with a leading-wildcard `icontains` cannot use a B-tree index | Prefix search (`^field`), exact (`=field`), or a real full-text index in the database |

## Correctness Traps

- Admin bulk actions call `queryset.update()` or `queryset.delete()`: no `save()`, no signals, no `auto_now` (SKILL.md Core Rules 3). The built-in "delete selected" action *does* cascade in Python and fire signals — the two behave differently, which surprises everyone once.
- `save_model(self, request, obj, form, change)` is the hook for stamping `obj.updated_by = request.user`. `save_formset` is the equivalent for inlines, and forgetting it is why inline rows have no audit fields.
- `readonly_fields` are not rendered as inputs, so they cannot be tampered with — but a field merely excluded from the form is simply absent, and a field left editable can be posted even if the template hides it.
- `list_editable` requires the field to be in `list_display` and forbids it being the link column; the resulting page posts every visible row at once, which is a real bulk-write surface.
- `get_queryset()` on the ModelAdmin is the correct place to scope rows per user. Overriding `has_change_permission` alone still lets a user reach an object by URL if the queryset returns it.
- The admin uses the model's `_default_manager`. A soft-delete manager declared first hides rows from the admin too, which is either the feature you wanted or a mystery you will spend an afternoon on.
- `ModelAdmin.form` with `fields = "__all__"` inherits the same over-exposure problem as any ModelForm: name the fields.

## Customizing Without Fighting It

```python
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "total_display")
    list_select_related = ("customer",)
    list_filter = ("status", ("created_at", admin.DateFieldListFilter))
    search_fields = ("=id", "customer__email")
    autocomplete_fields = ("customer",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    list_per_page = 50

    @admin.display(description="Total", ordering="total")
    def total_display(self, obj):
        return f"{obj.total:,.2f}"
```

- `@admin.display(ordering=...)` makes a computed column sortable by mapping it to a real column or expression; without it the header is not clickable.
- A callable in `list_display` that returns HTML must use `format_html` — the admin does not escape what a display method returns.
- `get_readonly_fields(request, obj)` gives per-state control: editable on create, frozen after approval.
- `fieldsets` beats a long flat form for anything a human uses daily; `collapse` in the classes hides the rarely used half.
- Inlines: `TabularInline` for a few short fields, `StackedInline` when each child has many. Both fetch all children — set `max_num` and `extra = 0` on anything that could grow.
- Custom admin views hang off `get_urls()` and should be wrapped in `self.admin_site.admin_view(...)`, which applies the staff check and the never-cache headers. Forgetting the wrapper publishes an unauthenticated endpoint under `/admin/`.

## Security Posture

- The admin is a full-power interface reachable at a guessable URL. Baseline: move it off `/admin/`, require staff plus a second factor, and restrict by network where the deployment allows it.
- `is_staff` grants entry; permissions decide what is visible inside. A staff user with no permissions sees an empty index, not an error — do not read an empty admin as "access denied".
- Admin actions honor permissions per model but not per object; a delete action on a queryset the user can see deletes all of it.
- The admin logs every change into `django.contrib.admin.models.LogEntry`. That table is your audit trail for admin-made changes only — nothing the application does through normal views appears there.
- Uploads via the admin land in `MEDIA_ROOT` like any other upload and carry the same content-type risks.
- Debug pages are off with `DEBUG=False`, but a stack trace in the admin's error mail still contains request data. Filter sensitive values with `@sensitive_variables` / `@sensitive_post_parameters` on the views that touch them.

## When The Admin Is The Wrong Tool

- Non-technical users doing a defined workflow (approve, refund, reassign) are better served by a small purpose-built view: fewer fields to misuse, an audit trail you control, and validation you can test.
- Bulk operations over hundreds of thousands of rows belong in a management command with batching and a resume key.
- Reporting and analytics through the admin pushes heavy aggregates onto the same database and workers serving users. Materialize the report or read a replica.
- Keep the admin for what it is unbeatable at: inspecting and correcting individual rows during an incident.
