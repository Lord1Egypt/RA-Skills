# Forms — Validation, ModelForms, Formsets, Uploads

The validation pipeline, in order: `is_valid()` → `full_clean()` → `to_python()` per field → field validators → `clean_<field>()` per field → `clean()` on the form → (for `ModelForm`) `instance.full_clean()` minus the exclusions. Knowing where you are in that sequence answers most form questions.

## The Validation Pipeline

- `cleaned_data` exists only after `is_valid()` (or `full_clean()`). Reading it before is a `KeyError` or an `AttributeError`, depending on how far the form got.
- A `clean_<field>()` method must **return** the value. Returning `None` implicitly is the most common silent data loss in Django forms.
- If a field fails, its key is absent from `cleaned_data` when `clean()` runs. Cross-field checks must use `cleaned_data.get("x")`, never `cleaned_data["x"]`.
- Errors: `self.add_error("field", "message")` attaches to a field and removes it from `cleaned_data`; `raise ValidationError(...)` inside `clean()` lands in `NON_FIELD_ERRORS`.
- `ValidationError` with `code=` and `params=` produces translatable, testable errors — assert on `code`, not on the English string.
- `form.has_changed()` and `form.changed_data` compare against `initial`. They are how you avoid writing rows nothing changed, and how formsets decide which forms to save.
- Overriding `__init__`: call `super().__init__(*args, **kwargs)` **first**, then touch `self.fields`. Before that call the fields do not exist. Pop your custom kwargs before the super call.
- A `required=False` field still fails validation if its value is invalid; `disabled=True` makes the widget read-only *and* ignores whatever the browser posts, which is the only way to make a rendered field tamper-proof.

## ModelForms

- `fields` explicitly, always. `fields = "__all__"` and `exclude = [...]` both grow the attack surface silently: the next field someone adds to the model becomes user-writable.
- Fields with `editable=False` (including `auto_now`/`auto_now_add`) are never in a `ModelForm`. Set them in `save()` or on the model.
- `form.save(commit=False)` returns an unsaved instance so you can set `request.user` or a tenant. After you save it, call `form.save_m2m()` or every many-to-many selection is lost — `commit=False` defers both the insert and the M2M write.
- `ModelForm` validation runs `instance.full_clean(exclude=<fields not on the form>)`, so a `unique_together` involving a field you excluded is *not* checked by the form — the database raises `IntegrityError` at save time instead. Catch it, or include the field.
- `instance=obj` edits; `initial={...}` only pre-fills the widget and is discarded on save. Passing `initial` where you meant `instance` produces a form that always creates new rows.
- Uniqueness validation costs a query per unique field per submission. It is also racy: two simultaneous submissions both pass and one gets an `IntegrityError`. The constraint in the database is the real enforcement.
- Limiting a related field's choices per user belongs in `__init__`: `self.fields["project"].queryset = Project.objects.filter(owner=user)`. A form that renders every row is both slow and an authorization leak.

## Formsets

```python
OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, fields=["sku", "qty"], extra=1, can_delete=True, max_num=20
)
```

- The management form (`TOTAL_FORMS`, `INITIAL_FORMS`, ...) must be rendered — `{{ formset.management_form }}` — or you get `ManagementFormDataMissing` on POST. JavaScript that clones a form must bump `TOTAL_FORMS`.
- `max_num` defaults to 1000 and `absolute_max` defaults to `max_num + 1000`: a crafted POST can make Django instantiate that many forms before validation. Set `max_num` to a real number.
- `DATA_UPLOAD_MAX_NUMBER_FIELDS` (default 1000) caps the whole POST. A formset posts `forms × fields_per_form + 4` inputs, so ~200 forms of 5 fields is the ceiling before `TooManyFieldsSent` (SKILL.md Settings Defaults That Bite).
- Cross-form validation goes in `BaseFormSet.clean()`, and it must start by checking `if any(self.errors): return` — individual form errors leave `cleaned_data` incomplete.
- `can_delete` adds a `DELETE` checkbox; `formset.save()` honors it, but a manual loop over `formset.forms` will happily re-save rows the user asked to delete.
- Each form in a formset validates independently, so a uniqueness rule across the set (two line items with the same SKU) has to be written in the formset's `clean()`.

## File Uploads

- `enctype="multipart/form-data"` on the `<form>` and `request.FILES` in the view. Without the enctype, `request.FILES` is empty and no error is raised anywhere.
- The form must receive both: `MyForm(request.POST, request.FILES)`.
- `FILE_UPLOAD_MAX_MEMORY_SIZE` (default 2621440 bytes) decides the object you get: below it, an in-memory upload with no `temporary_file_path()`; above it, a temp file on disk. Code that assumes one shape crashes on the other, and small test files never cross the boundary.
- `DATA_UPLOAD_MAX_MEMORY_SIZE` limits the *non-file* part of the body; a big JSON or textarea POST raises `RequestDataTooBig` before your view runs.
- Validate the file, not its name: extension and `content_type` are both attacker-controlled. Check the size, sniff the real type, and for images let Pillow open it (`ImageField` does this) before trusting anything.
- `upload_to` may be a callable `(instance, filename)`; sanitize or discard the client filename. Building a path from raw input triggers `SuspiciousFileOperation` at best and writes outside the storage root at worst.
- Deleting a model row does not delete its file — Django removed that behavior deliberately, because a rolled-back transaction would have left a missing file. Clean up in a scheduled task, not in a signal.
- Never serve user uploads from the application's own domain without forcing `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`: an uploaded HTML file is stored XSS on your origin.

## Widgets And Rendering

- `widget=forms.Textarea(attrs={"rows": 3})` on the field; `Meta.widgets` on a `ModelForm`. Changing a widget never changes validation — the field type decides that.
- Rendering: `{{ form }}` is fine for prototypes, `{{ form.as_div }}` (Django >=4.1) is the modern default, and a loop over `{% for field in form %}` with `{{ field.errors }}` is what real templates use.
- `{% csrf_token %}` in every POST form, or 403. It is not needed for GET forms and must not be placed outside the `<form>` tag.
- Custom rendering of a field's error state reads `field.errors` (a list) and `form.non_field_errors()` — they are separate, and forgetting the second hides whole-form failures from the user.
- Multi-value inputs (`MultipleChoiceField`, checkbox groups) come from `data.getlist(name)`; a custom widget's `value_from_datadict` is where that mapping lives.

## Where Form Logic Belongs

| Rule | Home | Why |
|---|---|---|
| Single-field format (regex, range) | Field validator | Reusable across every form on that field |
| Cross-field within one submission | Form `clean()` | Needs both values, still a UI-level message |
| Invariant that must always hold | Database constraint | Survives shell, scripts, bulk writes, other services |
| Authorization ("may this user pick this?") | The queryset in `__init__` **and** the view | A form is not an access-control layer |
| Side effect (email, task, webhook) | The view, inside `transaction.on_commit` | Forms should not fire effects during validation |
