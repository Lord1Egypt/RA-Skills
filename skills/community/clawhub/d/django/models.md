# Models Traps

- `makemigrations` not automatic — model changes need explicit command
- Migration conflicts on merge — rename migration file or `--merge`
- `auto_now` can't be set manually — use `default=timezone.now` instead
- `related_name` conflicts — same reverse name crashes, use unique or `'+'`
- `ForeignKey('self')` — string needed for self-reference
- Circular import in FK — use `ForeignKey('app.Model')` string form
- `signals.post_save` on update() — doesn't fire, only on `save()`
- Manager methods not on RelatedManager — `objects.custom()` won't work on `parent.children`
- `unique_together` deprecated — use `UniqueConstraint` in `Meta.constraints`
- `null=True` on CharField — use `blank=True` only, empty string not NULL
