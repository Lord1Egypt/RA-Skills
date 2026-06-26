# Actions Reference — All Types

> **Related files:** `references/decorators.md` (full @action decorator options),
> `references/forms-fields.md` (action with intermediate form pattern),
> `../SKILL.md` (ModelAdmin attributes: actions_list, actions_row, etc.)

## Action Types Overview

| Attribute | Location | Receives |
|-----------|----------|----------|
| `actions_list` | Above changelist (global) | `request` only |
| `actions_row` | Per-row button in changelist | `request, object_id` |
| `actions_detail` | Top of change form | `request, object_id` |
| `actions_submit_line` | Near Save button | `request, obj` (after save) |
| Standard `actions` | Dropdown on changelist | `request, queryset` |

All use `unfold.decorators.action`. All require `@action(description=...)`.

---

## 1. Changelist Global Action (actions_list)

Fires from the changelist header; no selection needed.

```python
from unfold.decorators import action
from unfold.enums import ActionVariant

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    actions_list = ["import_orders"]
    actions_list_hide_default = True  # hide Django's built-in list actions

    @action(
        description="Import Orders",
        icon="upload",
        variant=ActionVariant.PRIMARY,
    )
    def import_orders(self, request):
        # redirect to import page or process directly
        from django.shortcuts import redirect
        return redirect("/admin/import/orders/")
```

---

## 2. Changelist Row Action (actions_row)

Appears as a button on each row.

```python
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    actions_row = ["view_receipt"]

    @action(
        description="View Receipt",
        icon="receipt_long",
        url_path="view-receipt",          # optional: custom URL segment
        attrs={"target": "_blank"},        # optional: HTML attrs on <a>
    )
    def view_receipt(self, request, object_id: int):
        from django.shortcuts import redirect
        return redirect(f"/receipts/{object_id}/")
```

---

## 3. Change Form Action (actions_detail)

Appears in the change form header area.

```python
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    actions_detail = ["send_confirmation", "mark_shipped"]
    actions_detail_hide_default = True

    @action(
        description="Send Confirmation",
        icon="email",
        variant=ActionVariant.SUCCESS,
        permissions=["send_confirmation"],  # calls has_send_confirmation_permission()
    )
    def send_confirmation(self, request, object_id: int):
        order = Order.objects.get(pk=object_id)
        send_email(order)
        self.message_user(request, "Confirmation sent.")

    def has_send_confirmation_permission(self, request, obj=None):
        return request.user.has_perm("orders.send_confirmation")

    @action(description="Mark Shipped", icon="local_shipping")
    def mark_shipped(self, request, object_id: int):
        Order.objects.filter(pk=object_id).update(status="SHIPPED")
```

---

## 4. Submit Line Action (actions_submit_line)

Fires **after** the form is already saved. Handler receives the already-saved instance.

```python
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    actions_submit_line = ["save_and_activate", "save_and_notify"]

    @action(description="Save & Activate")
    def save_and_activate(self, request, obj):
        obj.status = "ACTIVE"
        obj.save()  # must re-save since this runs after the main save

    @action(description="Save & Notify", variant=ActionVariant.INFO)
    def save_and_notify(self, request, obj):
        obj.notify_customer()
        # no redirect needed — stays on same page
```

---

## 5. Dropdown Actions

Group actions into a dropdown button (any location):

```python
from unfold.decorators import action

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    actions_list = ["bulk_actions_dropdown"]

    @action(description="Bulk Actions", icon="more_horiz")
    def bulk_actions_dropdown(self, request):
        pass  # dropdown container — define children separately

    # Children are defined as methods too; grouped via template or custom logic
```

Actually, dropdown grouping is configured via returning a list from the action:
```python
# Dropdown action groups actions_row items visually — use variant grouping
# and icons to differentiate; Unfold renders them in a dropdown automatically
# when multiple actions_row items share the same area
```

---

## 6. Action Variants

```python
from unfold.enums import ActionVariant

# Available variants:
ActionVariant.DEFAULT  # default gray
ActionVariant.PRIMARY  # blue (primary color)
ActionVariant.SUCCESS  # green
ActionVariant.INFO     # light blue
ActionVariant.WARNING  # orange
ActionVariant.DANGER   # red
```

---

## 7. Action with Intermediate Form

When an action needs user input before executing, render a form:

```python
from django import forms
from django.shortcuts import render
from unfold.widgets import UnfoldAdminTextInputWidget

class RefundForm(forms.Form):
    reason = forms.CharField(widget=UnfoldAdminTextInputWidget, label="Reason")
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    actions_detail = ["process_refund"]

    @action(description="Process Refund", icon="payments")
    def process_refund(self, request, object_id: int):
        if request.method == "POST":
            form = RefundForm(request.POST)
            if form.is_valid():
                # process the refund
                from django.shortcuts import redirect
                return redirect(f"/admin/orders/order/{object_id}/change/")
        else:
            form = RefundForm()

        return render(
            request,
            "admin/orders/refund_form.html",
            {"form": form, "object_id": object_id},
        )
```

Template `admin/orders/refund_form.html`:
```django
{% extends "admin/base_site.html" %}
{% load i18n unfold %}

{% block content %}
<form action="" method="post" novalidate>
  {% csrf_token %}
  <div class="border border-base-200 mb-8 rounded-default pt-3 px-3 shadow-sm dark:border-base-800">
    {% for field in form %}
      {% include "unfold/helpers/field.html" with field=field %}
    {% endfor %}
  </div>
  <div class="flex justify-end gap-2">
    {% component "unfold/components/button.html" with submit=1 %}{% trans "Submit" %}{% endcomponent %}
  </div>
</form>
{% endblock %}
```

---

## 8. Permissions on Actions

Two permission approaches can be combined:

```python
@action(
    description="Approve",
    permissions=["approve_order"],           # method-based
    # OR:
    permissions=["orders.approve_order"],    # Django permission string
)
def approve_order(self, request, object_id):
    pass

# Method-based: define has_{permission_name}_permission
def has_approve_order_permission(self, request, obj=None):
    return request.user.is_superuser or request.user.has_perm("orders.approve_order")
```

→ For `@action` decorator full options, see `references/decorators.md`
→ For action with form UI, see also `references/forms-fields.md` (crispy forms integration)
