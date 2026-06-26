---
name: django-unfold
description: >
  Expert guidance for building advanced Django admin interfaces with django-unfold (v0.56+).
  Use this skill whenever the user mentions django-unfold, unfold admin, UnfoldModelAdmin,
  or wants to build, customize, or debug a Django admin panel with Unfold. Covers setup,
  ModelAdmin options, theming/colors, sidebar navigation, tabs (fieldset/inline/changelist/
  dynamic), inlines (sortable/paginated/nested/nonrelated), dashboard & components, actions
  (all 5 types + dropdown), filters (all types), conditional fields, sections/expandable rows,
  datasets, custom pages, crispy forms, Tailwind custom styles, @display and @action decorators,
  and all 10 third-party integrations. Always trigger this skill when the user asks to build any
  Django admin feature and django-unfold is present in the project, even if Unfold is not
  explicitly mentioned.
---

# Django Unfold Skill

Django Unfold is a modern admin theme for Django built on Tailwind CSS. It is a **drop-in
enhancement** of `django.contrib.admin` — fully compatible with all native Django admin
patterns while adding UI, components, and developer-friendly features.

**Current stable version: 0.90.x** (Django 5.0+ required from v0.90; dropped Django 4.2)

---

## ⚠️ Critical Rules — Always Apply

**Rule 1: Every ModelAdmin must inherit from `unfold.admin.ModelAdmin`**

```python
# ✅ CORRECT
from unfold.admin import ModelAdmin

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin):
    pass

# ❌ WRONG — loses all styling and Unfold features
from django.contrib.admin import ModelAdmin  # never use this base
```

**Rule 2: `INSTALLED_APPS` order — `"unfold"` must precede `"django.contrib.admin"`**

```python
INSTALLED_APPS = [
    "unfold",                           # REQUIRED FIRST
    "unfold.contrib.filters",           # optional: advanced filters
    "unfold.contrib.forms",             # optional: ArrayWidget, WysiwygWidget, crispy
    "unfold.contrib.inlines",           # optional: NonrelatedInline
    "unfold.contrib.import_export",     # optional: django-import-export
    "unfold.contrib.simple_history",    # optional: django-simple-history
    "unfold.contrib.guardian",          # optional: django-guardian
    "unfold.contrib.constance",         # optional: django-constance
    "unfold.contrib.location_field",    # optional: django-location-field
    "django.contrib.admin",             # AFTER unfold
]
```

**Rule 3: Inlines also need Unfold base classes**

```python
from unfold.admin import StackedInline, TabularInline  # not django.contrib.admin
```

**Rule 4: User & Group models need manual re-registration** — see `references/installation.md`

---

## Core ModelAdmin Options Reference

```python
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from django.db import models

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin):
    # ── Changelist layout ────────────────────────────────────────────
    list_fullwidth = False               # expand to full page width
    list_filter_sheet = True             # filters as bottom sheet (False = sidebar)
    list_filter_submit = False           # show Apply button in filter panel
    list_horizontal_scrollbar_top = False
    list_disable_select_all = False

    # ── Change form UX ────────────────────────────────────────────────
    compressed_fields = True             # compact field display
    warn_unsaved_form = True             # warn before leaving unsaved
    show_add_link = True                 # show Add button
    change_form_show_cancel_button = False

    # Custom template injection (HTML snippets, not full templates)
    change_form_before_template = "myapp/before_form.html"    # inside form, top
    change_form_after_template = "myapp/after_form.html"      # inside form, bottom
    change_form_outer_before_template = "myapp/outer_top.html"
    change_form_outer_after_template = "myapp/outer_bottom.html"

    # ── Readonly field post-processing ───────────────────────────────
    readonly_preprocess_fields = {
        "html_field": "html.unescape",
        "text_field": lambda content: content.strip(),
    }

    # ── Widget overrides ─────────────────────────────────────────────
    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
        # ArrayField: {"widget": ArrayWidget},  # for PostgreSQL ArrayField
    }

    # ── Actions (5 types) — see references/actions.md ────────────────
    actions_list = []        # above changelist (global)
    actions_row = []         # per-row in changelist table
    actions_detail = []      # top of change form header
    actions_submit_line = [] # near Save button in change form

    # ── Conditional fields — see references/forms-fields.md ──────────
    conditional_fields = {
        "field_name": "other_field == 'value'",  # Alpine.js expression
    }

    # ── Expandable row sections — see references/forms-fields.md ─────
    list_sections = []   # [SectionClass, ...]

    # ── Datasets on change form — see references/forms-fields.md ─────
    change_form_datasets = []  # [DatasetClass, ...]
```

---

## @display Decorator

**Always use `unfold.decorators.display`**, not Django's built-in.

```python
from unfold.decorators import display

class OrderAdmin(ModelAdmin):
    list_display = ["show_customer", "show_status", "show_priority"]

    # Two-line cell: main heading + subtitle
    @display(header=True)
    def show_customer(self, obj):
        return obj.full_name, obj.email   # tuple: (main, subtitle)

    # Colored status badge mapped from field values
    @display(
        description="Status",
        ordering="status",
        label={
            "PENDING":   "warning",   # orange
            "ACTIVE":    "info",      # blue
            "COMPLETED": "success",   # green
            "FAILED":    "danger",    # red
        },
    )
    def show_status(self, obj):
        return obj.status

    # Boolean label with default color
    @display(description="VIP", label=True)
    def show_priority(self, obj):
        return obj.is_vip
```

→ Full `@display` and `@action` decorator docs: **`references/decorators.md`**

---

## Reference Files — When To Read Each

Read the relevant file before implementing any feature in that area.
Each reference file contains explicit pointers to related files.

| Reference File | Read When You Need To... |
|---|---|
| `references/installation.md` | Set up from scratch, configure User/Group, run parallel admin |
| `references/configuration.md` | Understand any `UNFOLD = {...}` key: title, login, callbacks, favicons, env |
| `references/theming.md` | Change colors (OKLCH), sidebar nav, icons/badges, Tailwind custom CSS |
| `references/actions.md` | Add list/row/detail/submitline/dropdown actions, permissions, form actions |
| `references/filters.md` | Add text/date/dropdown/numeric/autocomplete/checkbox/radio/horizontal filters |
| `references/tabs.md` | Add fieldset tabs, inline tabs, changelist tabs, changeform tabs, dynamic tabs |
| `references/inlines.md` | Configure inlines: options, sortable, paginated, nested, nonrelated |
| `references/dashboard-components.md` | Build dashboards, use components (card/chart/table/progress/tracker/cohort) |
| `references/forms-fields.md` | Conditional fields, sections (expandable rows), datasets, crispy forms, JsonField |
| `references/decorators.md` | Full @display options (header, label, mapping) and @action decorator options |
| `references/integrations.md` | All 10 third-party packages: celery-beat, import-export, guardian, constance, etc. |
| `references/advanced.md` | Custom pages, custom sites, sortable changelist, command palette, multi-language |

---

## Common Pitfalls

- **Styles missing in production** → run `collectstatic`
- **Tailwind conflict on Unfold ≥ 0.56** → don't load a Tailwind 3 CSS file; use `UNFOLD["COLORS"]` or Tailwind 4
- **Custom pages not in sidebar** → add manually to `UNFOLD["SIDEBAR"]["navigation"]`
- **Third-party admin unstyled** (celery-beat, etc.) → unregister and re-register with `unfold.admin.ModelAdmin`
- **`list_filter` on Datasets** → not supported; filter via `get_queryset()` instead
- **Django 4.2** → not supported from Unfold v0.90+
