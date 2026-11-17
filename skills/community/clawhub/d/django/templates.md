# Templates — Escaping, Context, Tags, Performance

The Django Template Language is deliberately weak: no arbitrary expressions, no calls with arguments, silent failure on missing names. Fighting that weakness in the template is the mistake; the answer is almost always to compute in the view or in a custom tag.

## Silent Failure

- An unknown variable renders as the empty string. An attribute that raises `AttributeError`, `IndexError` or `KeyError` also renders empty. A wrong variable name and a `None` look identical.
- To see them during a debug run, set `OPTIONS["string_if_invalid"] = "!!MISSING %s!!"` on the template engine. Do not leave it on: some third-party templates rely on empty resolution.
- `{{ obj.method }}` calls the method with no arguments. If it raises, the exception is swallowed unless the callable sets `do_not_call_in_templates = True` or the error is not one of the silenced types.
- `{{ dict.key }}` tries dictionary lookup, then attribute, then list index — in that order. A dict key named `items` resolves to the *method*, not your value.
- `{% if %}` supports comparisons, `in`, `not`, `and`/`or` — but no arithmetic beyond `add`. If the template needs a calculation, the view owes it a context variable.

## Escaping And XSS

- Autoescaping is on: every `{{ value }}` is HTML-escaped. That protection ends the moment you write `|safe`, `mark_safe()`, or `{% autoescape off %}`.
- `format_html("<b>{}</b>", user_input)` escapes the arguments while keeping your markup — the correct tool whenever code builds HTML. `mark_safe(f"<b>{user_input}</b>")` is the same line with the vulnerability added.
- HTML escaping is not JavaScript escaping. Interpolating a value inside a `<script>` block is XSS even when escaped. Use `{{ data|json_script:"config" }}`, which emits a `<script type="application/json">` element, and read it with `JSON.parse(document.getElementById("config").textContent)`.
- Attribute context needs quotes: `<a href="{{ url }}">` is safe; `<a href={{ url }}>` is not, escaped or otherwise. A `javascript:` URL in `href` also survives HTML escaping — validate the scheme in Python.
- `|safe` applied to a value that came from a database column is still user input if a user ever wrote that column. Rich text needs a sanitizer (bleach-style allowlist) at write time, not `|safe` at read time.

## Inheritance And Includes

- `{% extends %}` must be the first template tag in the file. Blocks defined outside the child's own `{% block %}` tags are ignored, which is why "my content does not appear".
- `{{ block.super }}` renders the parent's block content inside the child's override.
- `{% include %}` renders another template with the current context; `{% include "x.html" with a=1 only %}` restricts it to exactly what you pass, which is the version that does not break when a parent renames a variable.
- Includes inside a loop re-parse nothing (templates are cached) but do re-render. A heavy include inside a 500-row loop is 500 renders — inline it or restructure.
- `{% block %}` names must be unique within a template. Duplicates raise at parse time.

## Custom Tags And Filters

```
myapp/
└── templatetags/
    ├── __init__.py        # required, and the usual reason a tag is "not registered"
    └── shop_tags.py
```

```python
from django import template
register = template.Library()

@register.filter
def money(value):                     # filters take one argument plus an optional parameter
    return f"{value:,.2f}"

@register.simple_tag(takes_context=True)
def price_for(context, product):      # tags take anything, including keyword arguments
    return product.price_for(context["request"].user)

@register.inclusion_tag("shop/_badge.html")
def badge(order):
    return {"order": order}
```

- `{% load shop_tags %}` in every template that uses them; loading is per file, not inherited from a parent template.
- Adding a new module under `templatetags/` requires a server restart — the library registry is built at import.
- A `simple_tag` returning HTML must build it with `format_html`, or mark the whole tag with `@register.simple_tag(...)` and `mark_safe` on content you fully control. Returning raw user data from a tag bypasses autoescaping.
- `inclusion_tag` renders a template per call: convenient, and a hidden loop cost when used inside a large `{% for %}`.

## Performance

- Template rendering is rarely the bottleneck; the queries the template *triggers* are. Every `{{ order.customer.name }}` on an unprefetched queryset is a query (SKILL.md Core Rules 1-2).
- `{% for %}` over a queryset evaluates it once and caches; over a *manager* (`{% for x in obj.items %}` without `.all`) the DTL calls it for you — but a filtered relation inside the loop re-queries per row.
- The cached template loader is enabled automatically when `DEBUG=False` and `OPTIONS["loaders"]` is unset. If you set `loaders` by hand, you have opted out and must add `django.template.loaders.cached.Loader` yourself.
- `{% cache 600 fragment_name request.user.id %}` caches a fragment; every variable the fragment depends on must be in the key, or users see each other's content. That is the most common cache-poisoning bug in Django apps.
- `{% with total=order.compute_total %}` evaluates once instead of per use — the fix for an expensive property referenced three times.

## Static, Media And URLs In Templates

- `{% load static %}` then `{% static "shop/app.css" %}`. Hard-coded `/static/...` paths break the moment the storage adds content hashes.
- With `ManifestStaticFilesStorage`, `{% static %}` raises for a file `collectstatic` never saw. That strictness is the feature: it catches a typo at deploy time instead of a 404 in production.
- `{% url "shop:order-detail" pk=order.pk %}` — never build URLs by string concatenation, or a URL change becomes a site-wide search-and-replace.
- Media files (user uploads) use `{{ obj.image.url }}`, which comes from the storage backend, not from `{% static %}`.
