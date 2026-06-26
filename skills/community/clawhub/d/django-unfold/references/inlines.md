# Inlines Reference — All Types

> **Related files:** `references/tabs.md` (inline tabs — set tab=True on inline class),
> `../SKILL.md` (Rule 3: inlines must use Unfold base classes)

## Rule: Always Use Unfold Inline Classes

```python
from unfold.admin import StackedInline, TabularInline  # NOT django.contrib.admin
```

---

## 1. Basic Inline Options

```python
from unfold.admin import StackedInline, TabularInline

class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0                     # no empty extra forms
    tab = True                    # render as tab on change form
    show_change_link = True       # link to related object's change form
    hide_title = False            # hide section title
    min_num = 0
    max_num = None
    fields = ["product", "quantity", "price"]
    readonly_fields = ["total"]
```

---

## 2. Sortable Inlines

Allow drag-and-drop reordering. The model must have an integer ordering field.

```python
from unfold.admin import StackedInline

class GalleryImageInline(StackedInline):
    model = GalleryImage
    extra = 0
    ordering_field = "position"            # the ordering integer field on the model
    ordering_field_hide_input = True       # hide the raw number input

# models.py
class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="gallery/")
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]
```

---

## 3. Paginated Inlines

For large related sets, paginate the inline list.

```python
from unfold.admin import TabularInline

class OrderHistoryInline(TabularInline):
    model = OrderHistory
    extra = 0
    per_page = 10           # items per page in the inline
    readonly_fields = ["action", "timestamp", "user"]
    can_delete = False
    show_change_link = True
```

---

## 4. Nested Inlines

Display inlines within inlines (requires `unfold.contrib.inlines` in INSTALLED_APPS).

```python
from unfold.admin import ModelAdmin
from unfold.contrib.inlines.admin import UnfoldGenericStackedInline

class VariantAttributeInline(UnfoldGenericStackedInline):
    model = VariantAttribute
    extra = 0
    fields = ["name", "value"]

class ProductVariantInline(StackedInline):
    model = ProductVariant
    extra = 0
    inlines = [VariantAttributeInline]  # nested inline

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    inlines = [ProductVariantInline]
```

---

## 5. Nonrelated Inlines

Show a model that has no FK to the parent — you control the queryset manually.
**Requires:** `"unfold.contrib.inlines"` in `INSTALLED_APPS`.

```python
from unfold.contrib.inlines.admin import NonrelatedStackedInline, NonrelatedTabularInline

class CustomerOrdersInline(NonrelatedTabularInline):
    model = Order
    fields = ["order_number", "total", "status", "created_at"]
    readonly_fields = ["order_number", "total", "status", "created_at"]
    can_delete = False
    extra = 0
    verbose_name_plural = "Customer Orders"
    tab = True

    def get_form_queryset(self, obj):
        """Return queryset to display for the given parent object."""
        if obj is None:
            return self.model.objects.none()
        return self.model.objects.filter(customer=obj).order_by("-created_at")[:20]

    def save_new_instance(self, parent, instance):
        """Called when a new inline form is saved (if editable)."""
        instance.customer = parent
        instance.save()

@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    inlines = [CustomerOrdersInline]
```

---

## 6. All Inline Options Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `tab` | bool | False | Render as tab on change form |
| `extra` | int | 3 | Extra empty forms shown |
| `min_num` | int | 0 | Minimum required items |
| `max_num` | int | None | Maximum allowed items |
| `per_page` | int | — | Items per page (paginated) |
| `ordering_field` | str | — | Field for drag-drop sort |
| `ordering_field_hide_input` | bool | False | Hide ordering field input |
| `hide_title` | bool | False | Hide inline section title |
| `show_change_link` | bool | False | Link to related object |
| `can_delete` | bool | True | Show delete checkbox |
| `verbose_name_plural` | str | — | Tab label / section title |

---

## 7. Performance: Prefetch Related for Inlines

Heavy inline pages → override `get_queryset` with `prefetch_related`:

```python
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    inlines = [OrderItemInline, ShipmentInline]

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .prefetch_related("items", "items__product", "shipments")
        )
```

→ For tab display of inlines, see `references/tabs.md`
→ For nonrelated inline use cases like audit logs, see `references/forms-fields.md` (datasets vs nonrelated comparison)
