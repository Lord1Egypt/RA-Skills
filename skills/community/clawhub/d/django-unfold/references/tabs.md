# Tabs Reference — All Types

> **Related files:** `references/inlines.md` (inline tab = set tab=True on inline class),
> `references/configuration.md` (TABS key lives in UNFOLD dict),
> `references/theming.md` (SIDEBAR navigation complements tab navigation)

## Tab Types Summary

| Type | Where | How configured |
|------|-------|---------------|
| Fieldset tabs | Change form — fieldsets in tabs | `classes: ["tab"]` in `fieldsets` |
| Inline tabs | Change form — inlines in tabs | `tab = True` on inline class |
| Changeform tabs | Top of change form (cross-model) | `UNFOLD["TABS"]` with `"detail": True` |
| Changelist tabs | Top of changelist | `UNFOLD["TABS"]` (default) |
| Dynamic tabs | Any — built via callback | `UNFOLD["TABS"] = "path.to.callback"` |

---

## 1. Fieldset Tabs

Group fieldsets into tabs in the change form. Fields outside `"tab"` class appear above all tabs.

```python
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    fieldsets = (
        # Always visible above tabs (no "tab" class)
        (None, {
            "fields": ["title", "slug", "author"],
        }),
        # Each tab needs a name (first arg) AND "tab" in classes
        (_("Content"), {
            "classes": ["tab"],
            "fields": ["body", "excerpt", "featured_image"],
        }),
        (_("SEO"), {
            "classes": ["tab"],
            "fields": ["meta_title", "meta_description", "canonical_url"],
        }),
        (_("Publishing"), {
            "classes": ["tab"],
            "fields": ["status", "published_at", "is_featured"],
        }),
    )
```

> A fieldset without a name (first arg is `None`) and `"tab"` class will be excluded from tab nav.

---

## 2. Inline Tabs

Group inline forms as tabs in the change form. Works independently from fieldset tabs.

```python
from unfold.admin import StackedInline, TabularInline

class AddressInline(StackedInline):
    model = Address
    tab = True       # This inline appears as a named tab
    extra = 0
    verbose_name_plural = "Addresses"   # Tab label uses this

class OrderItemInline(TabularInline):
    model = OrderItem
    tab = True
    extra = 0

class NoteInline(StackedInline):
    model = Note
    tab = True
    extra = 0

@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    inlines = [AddressInline, OrderItemInline, NoteInline]
    # fieldsets with "tab" class will merge into the same tab strip
```

> Inline tabs and fieldset tabs share the same tab navigation strip on the change form.

---

## 3. Changelist Tabs (most common)

Display tab navigation at the top of changelist views, linking to related models.

```python
# settings.py
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "TABS": [
        {
            # Which models show this tab strip (app_label.model_name lowercase)
            "models": [
                "shop.order",
                "shop.invoice",
                "shop.refund",
            ],
            "items": [
                {
                    "title": _("Orders"),
                    "link": reverse_lazy("admin:shop_order_changelist"),
                    "permission": "myapp.utils.can_see_orders",  # optional
                },
                {
                    "title": _("Invoices"),
                    "link": reverse_lazy("admin:shop_invoice_changelist"),
                },
                {
                    "title": _("Refunds"),
                    "link": reverse_lazy("admin:shop_refund_changelist"),
                },
            ],
        },
    ],
}

# myapp/utils.py
def can_see_orders(request):
    return request.user.has_perm("shop.view_order")
```

---

## 4. Changeform Tabs (detail page)

Tab navigation shown on a model's change form page, linking to related models.

```python
UNFOLD = {
    "TABS": [
        {
            "models": [
                {
                    "name": "shop.order",
                    "detail": True,   # ← this activates changeform tab mode
                },
            ],
            "items": [
                {
                    "title": _("Details"),
                    "link": reverse_lazy("admin:shop_order_changelist"),
                    "active": True,
                },
                {
                    "title": _("Shipments"),
                    "link": reverse_lazy("admin:shop_shipment_changelist"),
                    # Use "inline" key to link to an inline fragment:
                    # "inline": "shipments-inline-fragment-url",
                },
            ],
        },
    ],
}
```

---

## 5. Dynamic Tabs (Callback)

Generate tab navigation programmatically — useful for permission-conditional tabs.

```python
# settings.py
UNFOLD = {
    "TABS": "myapp.admin.tabs_callback",  # string path to function
}

# myapp/admin.py
from typing import Any
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

def tabs_callback(request: HttpRequest) -> list[dict[str, Any]]:
    tabs = []

    if request.user.has_perm("shop.view_order"):
        tabs.append({
            "page": "shop_overview",       # unique key for {% tab_list %}
            "models": ["shop.order"],
            "items": [
                {
                    "title": _("All Orders"),
                    "link": reverse_lazy("admin:shop_order_changelist"),
                    "active": True,
                },
                {
                    "title": _("Pending"),
                    "link": reverse_lazy("admin:shop_order_changelist") + "?status=pending",
                    # Dynamic active based on request:
                    "active": lambda req: req.GET.get("status") == "pending",
                },
            ],
        })

    return tabs
```

Use in custom templates:
```django
{% load unfold %}
{% tab_list "shop_overview" %}
```

---

## Key Tab Rules

- **Fieldset tab name:** The first argument of the fieldset tuple becomes the tab label — never use `None` for a tab fieldset.
- **Inline tab label:** Comes from the inline's `verbose_name_plural`.
- **`models` key:** Must use lowercase `app_label.model_name`.
- **`permission` on tab items:** String path to a function returning bool — hides the tab item.
- **Active state:** `"active": True` (static) or `"active": lambda request: bool` (dynamic).

→ For inline configuration details, see `references/inlines.md`
→ For TABS key placement in UNFOLD dict, see `references/configuration.md`
