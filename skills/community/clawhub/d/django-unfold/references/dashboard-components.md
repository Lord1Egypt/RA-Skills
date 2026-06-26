# Dashboard & Components Reference

> **Related files:** `references/configuration.md` (DASHBOARD_CALLBACK setting),
> `references/theming.md` (STYLES for custom CSS in dashboard templates),
> `references/advanced.md` (custom pages that use the same component system)

## 1. Dashboard Setup

```python
# settings.py
UNFOLD = {
    "DASHBOARD_CALLBACK": "myapp.utils.dashboard_callback",
}
```

```python
# myapp/utils.py
def dashboard_callback(request, context):
    """
    Inject variables into templates/admin/index.html.
    context already contains all standard Django admin variables.
    """
    from myapp.models import Order, Customer, Product
    from django.db.models import Sum
    import json

    context.update({
        # KPI values
        "total_orders": Order.objects.count(),
        "monthly_revenue": Order.objects.filter(
            created_at__month=__import__('datetime').date.today().month
        ).aggregate(t=Sum("total"))["t"] or 0,
        "new_customers": Customer.objects.filter(is_new=True).count(),
        "low_stock_items": Product.objects.filter(stock__lt=10).count(),

        # Table data
        "recent_orders": Order.objects.select_related("customer").order_by("-created_at")[:5],

        # Chart data (Chart.js config as JSON string)
        "revenue_chart": json.dumps({
            "type": "bar",
            "data": {
                "labels": ["Jan","Feb","Mar","Apr","May","Jun"],
                "datasets": [{
                    "label": "Revenue",
                    "data": [1200, 1900, 1500, 2100, 1800, 2400],
                }],
            },
        }),
    })
    return context
```

Create `templates/admin/index.html` in your project:

```django
{% extends 'unfold/layouts/base_simple.html' %}
{% load i18n unfold %}

{% block breadcrumbs %}{% endblock %}
{% block title %}{% trans 'Dashboard' %} | {{ site_title }}{% endblock %}

{% block content %}
{% component "unfold/components/container.html" %}

  {# KPI Row #}
  <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
    {% component "unfold/components/card.html" %}
      {% component "unfold/components/text.html" %}Total Orders{% endcomponent %}
      {% component "unfold/components/title.html" %}{{ total_orders }}{% endcomponent %}
    {% endcomponent %}

    {% component "unfold/components/card.html" %}
      {% component "unfold/components/text.html" %}Monthly Revenue{% endcomponent %}
      {% component "unfold/components/title.html" %}${{ monthly_revenue }}{% endcomponent %}
    {% endcomponent %}

    {% component "unfold/components/card.html" %}
      {% component "unfold/components/text.html" %}New Customers{% endcomponent %}
      {% component "unfold/components/title.html" %}{{ new_customers }}{% endcomponent %}
    {% endcomponent %}

    {% component "unfold/components/card.html" %}
      {% component "unfold/components/text.html" %}Low Stock Items{% endcomponent %}
      {% component "unfold/components/title.html" %}{{ low_stock_items }}{% endcomponent %}
    {% endcomponent %}
  </div>

  {# Chart + Table side by side #}
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
    {% component "unfold/components/card.html" %}
      {% component "unfold/components/title.html" %}Revenue{% endcomponent %}
      {% component "unfold/components/chart.html" with chart=revenue_chart %}{% endcomponent %}
    {% endcomponent %}

    {% component "unfold/components/card.html" %}
      {% component "unfold/components/title.html" %}Recent Orders{% endcomponent %}
      {% component "unfold/components/table.html" with table=recent_table %}{% endcomponent %}
    {% endcomponent %}
  </div>

{% endcomponent %}
{% endblock %}
```

---

## 2. Component Reference

All components require `{% load unfold %}`. They support unlimited nesting via `children`.

### card.html — Container with border and shadow
```django
{% component "unfold/components/card.html" with class="col-span-2" %}
  Any content here, including nested components
{% endcomponent %}
```

### title.html / text.html — Typography
```django
{% component "unfold/components/title.html" %}1,234{% endcomponent %}  {# large bold #}
{% component "unfold/components/text.html" %}Subtitle or label{% endcomponent %}  {# muted #}
```

### chart.html — Chart.js chart
```python
# In dashboard_callback, pass a JSON string of Chart.js config:
import json
context["my_chart"] = json.dumps({
    "type": "line",  # bar | line | pie | doughnut | radar
    "data": {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "datasets": [{"label": "Sales", "data": [10, 20, 15, 30, 25]}],
    },
    "options": {"responsive": True},
})
```
```django
{% component "unfold/components/chart.html" with chart=my_chart %}{% endcomponent %}
```

### table.html — Data table
```python
context["orders_table"] = {
    "headers": ["#", "Customer", "Total", "Status"],
    "rows": [
        [o.id, o.customer.name, f"${o.total}", o.status]
        for o in recent_orders
    ],
}
```
```django
{% component "unfold/components/table.html" with table=orders_table %}{% endcomponent %}
```

### progress.html — Progress bar
```django
{% component "unfold/components/progress.html" with value=75 title="Goal Progress" %}
{% endcomponent %}
```

### button.html — Button or link
```django
{% component "unfold/components/button.html" with href="/admin/shop/order/add/" %}
  Add Order
{% endcomponent %}

{# Submit button inside a form #}
{% component "unfold/components/button.html" with submit=1 %}Save{% endcomponent %}
```

### link.html — Styled link
```django
{% component "unfold/components/link.html" with href="/admin/shop/order/" %}
  View All Orders
{% endcomponent %}
```

### navigation.html — Tab/filter navigation strip
```python
# Pass list of dicts with title, link, active
context["nav_items"] = [
    {"title": "All", "link": "/admin/shop/order/", "active": True},
    {"title": "Pending", "link": "/admin/shop/order/?status=pending"},
]
```
```django
{% component "unfold/components/navigation.html" with items=nav_items %}{% endcomponent %}
```

### tracker.html — Activity dots (e.g. commit graph)
```python
context["activity"] = {
    "title": "Last 30 days",
    "entries": [
        {"value": 2, "label": "2024-01-01"},  # value 0–3 maps to color intensity
        {"value": 0, "label": "2024-01-02"},
        # ... 30 items
    ],
}
```
```django
{% component "unfold/components/tracker.html" with tracker=activity %}{% endcomponent %}
```

### cohort.html — Cohort/retention grid
Pass `cohort` as a structured data object. Best for user retention analysis.

### layer.html — Stacked info cell
Display multiple pieces of info layered in one container.

---

## 3. Python-Based Component Class

For reusable components with Python logic:

```python
from unfold.components import BaseComponent, register_component

@register_component
class RevenueCard(BaseComponent):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from myapp.models import Order
        from django.db.models import Sum
        ctx["revenue"] = Order.objects.aggregate(t=Sum("total"))["t"] or 0
        return ctx
```

---

## 4. Custom Dashboard Tailwind Styles

When you use Tailwind classes in your dashboard templates, they need to be compiled.
See `references/theming.md` for Tailwind 4 setup. Minimal approach:

```python
# settings.py
UNFOLD = {
    "STYLES": [lambda request: static("css/dashboard.css")],
}
```

→ For custom pages that also use components, see `references/advanced.md`
→ For COLORS theming affecting component appearance, see `references/theming.md`
