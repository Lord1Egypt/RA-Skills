# Configuration Reference — Full UNFOLD Settings Dict

> **Related files:** `references/theming.md` (COLORS, SIDEBAR, Tailwind),
> `references/tabs.md` (TABS key), `references/advanced.md` (DASHBOARD_CALLBACK, custom pages)

## Complete UNFOLD Dictionary

```python
# settings.py
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    # ── Branding ─────────────────────────────────────────────────────
    "SITE_TITLE": "My Admin",                    # browser <title> suffix
    "SITE_HEADER": "My Application",            # sidebar top text
    "SITE_SUBHEADER": "Internal Tools",         # smaller text under header

    # Dropdown menu next to site header (links to external sites, docs, etc.)
    "SITE_DROPDOWN": [
        {
            "icon": "diamond",
            "title": _("Visit Site"),
            "link": "https://example.com",
        },
    ],

    "SITE_URL": "/",                             # link on the site header

    # Icon: shown in collapsed sidebar (32px height recommended)
    "SITE_ICON": {
        "light": lambda request: static("img/icon-light.svg"),
        "dark":  lambda request: static("img/icon-dark.svg"),
    },
    # Logo: full logo (32px height recommended)
    "SITE_LOGO": {
        "light": lambda request: static("img/logo-light.svg"),
        "dark":  lambda request: static("img/logo-dark.svg"),
    },
    "SITE_SYMBOL": "speed",  # Material Symbols icon used as fallback symbol

    # Favicons
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("img/favicon.svg"),
        },
    ],

    # ── UI toggles ────────────────────────────────────────────────────
    "SHOW_HISTORY": True,          # show/hide "History" button on changeform
    "SHOW_VIEW_ON_SITE": True,     # show/hide "View on site" button
    "SHOW_BACK_BUTTON": False,     # show/hide "Back" button on changeform header

    # ── Environment label (top-right corner) ──────────────────────────
    # Callback returns [label_text, color]
    # Colors: "info", "success", "warning", "danger"
    "ENVIRONMENT": "myapp.utils.environment_callback",
    # Optional: prefix in <title> tag per environment
    "ENVIRONMENT_TITLE_PREFIX": "myapp.utils.environment_title_prefix_callback",

    # ── Theme ─────────────────────────────────────────────────────────
    "THEME": None,  # None = user can switch; "dark" or "light" = forced

    # ── Login page ────────────────────────────────────────────────────
    "LOGIN": {
        "image": lambda request: static("img/login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),
        # Custom form (must inherit from unfold.forms.AuthenticationForm)
        "form": "myapp.forms.CustomLoginForm",
    },

    # ── Custom CSS and JS ─────────────────────────────────────────────
    "STYLES": [
        lambda request: static("css/admin-custom.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/admin-custom.js"),
    ],

    # ── Colors & radius ───────────────────────────────────────────────
    "BORDER_RADIUS": "6px",
    "COLORS": { ... },  # see references/theming.md for full OKLCH palette

    # ── Sidebar navigation ────────────────────────────────────────────
    "SIDEBAR": { ... },  # see references/theming.md

    # ── Tab navigation ────────────────────────────────────────────────
    "TABS": [ ... ],  # see references/tabs.md

    # ── Dashboard ─────────────────────────────────────────────────────
    "DASHBOARD_CALLBACK": "myapp.utils.dashboard_callback",

    # ── Extensions ────────────────────────────────────────────────────
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "es": "🇪🇸",
                "fr": "🇫🇷",
            },
        },
    },
}
```

## Callback Functions

### environment_callback

```python
def environment_callback(request):
    """Returns [label, color]. Color: info | success | warning | danger"""
    import os
    env = os.getenv("ENVIRONMENT", "production")
    return {
        "development": ["Development", "warning"],
        "staging":     ["Staging", "info"],
        "production":  ["Production", "danger"],
    }.get(env, ["Unknown", "info"])
```

### dashboard_callback

```python
def dashboard_callback(request, context):
    """
    Inject variables into templates/admin/index.html.
    context already has all standard Django admin variables — just add to it.
    """
    from myapp.models import Order, Customer
    context.update({
        "total_orders": Order.objects.count(),
        "new_customers": Customer.objects.filter(is_new=True).count(),
    })
    return context
```

### badge_callback (for sidebar items)

```python
def pending_orders_badge(request):
    """Return string to show as badge, or empty string to hide."""
    from myapp.models import Order
    count = Order.objects.filter(status="PENDING").count()
    return str(count) if count else ""
```

### permission_callback (for sidebar/tab items)

```python
def can_view_reports(request):
    return request.user.has_perm("myapp.view_report")
```

→ For COLORS and SIDEBAR full examples, see `references/theming.md`
→ For TABS full examples, see `references/tabs.md`
→ For dashboard template + components, see `references/dashboard-components.md`
