# Filters Reference — All Types

> **Related files:** `../SKILL.md` (list_filter_sheet, list_filter_submit ModelAdmin options),
> `references/configuration.md` (global UNFOLD settings),
> `references/tabs.md` (TABS + filters can appear together on same changelist)

**Prerequisite:** Add `"unfold.contrib.filters"` to `INSTALLED_APPS`.

---

## 1. Filter Display Mode

```python
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_filter_sheet = True    # bottom sheet panel (default)
    # list_filter_sheet = False  # sidebar mode
    list_filter_submit = True   # show Apply button (useful for expensive filters)
```

---

## 2. Text Filter

Filter by typing text. Applies a case-insensitive `__icontains` lookup.

```python
from unfold.contrib.filters.admin import FieldTextFilter

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_filter = [
        ("customer_name", FieldTextFilter),
        ("email", FieldTextFilter),
    ]
```

---

## 3. Datetime / Date Range Filter

```python
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_filter = [
        ("created_at", RangeDateTimeFilter),   # datetime picker (from/to)
        ("due_date",   RangeDateFilter),        # date picker (from/to)
    ]
```

---

## 4. Dropdown Filters

```python
from unfold.contrib.filters.admin import (
    DropdownFilter,
    ChoiceDropdownFilter,      # for CharField with choices
    RelatedDropdownFilter,     # for ForeignKey / ManyToManyField
)

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_filter = [
        ("status",   ChoiceDropdownFilter),    # uses field's choices
        ("customer", RelatedDropdownFilter),   # FK — shows related model items
        ("tags",     RelatedDropdownFilter),   # M2M
    ]
```

Custom dropdown filter with your own queryset:

```python
from unfold.contrib.filters.admin import DropdownFilter

class RegionFilter(DropdownFilter):
    title = "Region"
    parameter_name = "region"

    def lookups(self, request, model_admin):
        return [
            ("north", "North"),
            ("south", "South"),
            ("east",  "East"),
            ("west",  "West"),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(region=self.value())
        return queryset
```

---

## 5. Autocomplete Filter

For ForeignKey fields where the related model has too many items for a dropdown.
The related model's admin must define `search_fields`.

```python
from unfold.contrib.filters.admin import AutocompleteFilter

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_filter = [
        ("customer", AutocompleteFilter),
    ]

# Required: related admin must have search_fields
@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    search_fields = ["name", "email"]
```

---

## 6. Numeric Filters

```python
from unfold.contrib.filters.admin import (
    RangeNumericListFilter,   # two inputs: min and max
    SingleNumericFilter,      # single number (exact or gt/lt)
    SliderNumericFilter,      # slider UI
)

# Range filter — subclass it
class PriceRangeFilter(RangeNumericListFilter):
    parameter_name = "price"
    title = "Price Range"

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_filter = [PriceRangeFilter]
```

---

## 7. Horizontal Layout Filter

Display filter inputs horizontally instead of vertically:

```python
from unfold.contrib.filters.admin import (
    RangeNumericListFilter,
    RangeDateFilter,
)

@admin.register(Report)
class ReportAdmin(ModelAdmin):
    list_filter_sheet = False  # sidebar mode — required for horizontal layout
    list_filter = [
        ("amount",     RangeNumericListFilter),
        ("created_at", RangeDateFilter),
    ]
```

---

## 8. Checkbox and Radio Filters

```python
from unfold.contrib.filters.admin import (
    CheckboxFilter,    # multi-select checkboxes
    RadioFilter,       # single-select radio buttons
)

class StatusCheckboxFilter(CheckboxFilter):
    title = "Status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ("active",   "Active"),
            ("inactive", "Inactive"),
            ("pending",  "Pending"),
        ]

    def queryset(self, request, queryset):
        values = self.value()  # returns list for checkbox, single for radio
        if values:
            return queryset.filter(status__in=values)
        return queryset
```

---

## 9. Combining Multiple Filter Types

```python
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_filter_sheet = True
    list_filter_submit = True

    list_filter = [
        ("status",       ChoiceDropdownFilter),
        ("customer",     AutocompleteFilter),
        ("created_at",   RangeDateTimeFilter),
        ("total",        RangeNumericListFilter),
        ("customer_name",FieldTextFilter),
        ("is_paid",      CheckboxFilter),
    ]
```

→ For `list_filter_sheet` and `list_filter_submit` ModelAdmin options, see `../SKILL.md`
→ For changelist tabs alongside filters, see `references/tabs.md`
