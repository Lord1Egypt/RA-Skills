# Theming Reference — Sidebar, Colors, Tailwind

> **Related files:** `references/configuration.md` (full UNFOLD dict context),
> `references/tabs.md` (TABS key in UNFOLD, used alongside sidebar),
> `references/advanced.md` (custom pages that appear in sidebar)

## 1. Sidebar Navigation

```python
# settings.py
UNFOLD = {
    "SIDEBAR": {
        "show_search": True,            # search box at top of sidebar
        "command_search": False,        # replace sidebar search with command palette search
        "show_all_applications": True,  # "All apps" link at bottom

        "navigation": [
            {
                "title": _("Main"),
                "separator": True,       # horizontal line above group
                "collapsible": True,     # can be collapsed
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                        "badge": "myapp.utils.pending_badge",  # str path or callable
                        "badge_variant": "danger",  # info | success | warning | primary | danger
                        "badge_style": "solid",      # solid = filled background
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                ],
            },
            {
                "title": _("Commerce"),
                "items": [
                    {
                        "title": _("Orders"),
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:shop_order_changelist"),
                        "badge": lambda request: str(
                            Order.objects.filter(status="PENDING").count() or ""
                        ),
                    },
                ],
            },
        ],
    },
}
```

### Sidebar Item Keys

| Key | Type | Description |
|-----|------|-------------|
| `title` | str / lazy | Display label |
| `icon` | str | Material Symbols name (see below) |
| `link` | str / reverse_lazy | URL for the item |
| `badge` | str path or callable | Short text badge (e.g. count) — hide by returning `""` |
| `badge_variant` | str | `"info"` · `"success"` · `"warning"` · `"primary"` · `"danger"` |
| `badge_style` | str | `"solid"` for filled background |
| `permission` | str path or callable | Returns bool — hides item if False |

### Material Symbols Icons

Common icons (browse full set at https://fonts.google.com/icons):
`dashboard` · `people` · `shopping_cart` · `inventory_2` · `settings` · `bar_chart` ·
`description` · `notifications` · `lock` · `email` · `task` · `receipt` · `upload` ·
`download` · `group` · `star` · `check_circle` · `warning` · `error` · `person`

---

## 2. Colors — OKLCH Palette

Unfold uses OKLCH color space. Override the `"base"` (neutral grays) and/or `"primary"` (accent) palettes.

```python
UNFOLD = {
    "BORDER_RADIUS": "6px",  # applied everywhere

    "COLORS": {
        "base": {   # Neutral grays (50 = lightest, 950 = darkest)
            "50":  "oklch(98.5% .002 247.839)",
            "100": "oklch(96.7% .003 264.542)",
            "200": "oklch(92.8% .006 264.531)",
            "300": "oklch(87.2% .01 258.338)",
            "400": "oklch(70.7% .022 261.325)",
            "500": "oklch(55.1% .027 264.364)",
            "600": "oklch(44.6% .03 256.802)",
            "700": "oklch(37.3% .034 259.733)",
            "800": "oklch(27.8% .033 256.848)",
            "900": "oklch(21% .034 264.665)",
            "950": "oklch(13% .028 261.692)",
        },
        "primary": {  # Accent color (buttons, links, active states)
            "50":  "oklch(97.7% .014 308.299)",
            "100": "oklch(94.6% .033 307.174)",
            "200": "oklch(90.2% .063 306.703)",
            "300": "oklch(82.7% .119 306.383)",
            "400": "oklch(71.4% .203 305.504)",
            "500": "oklch(62.7% .265 303.9)",
            "600": "oklch(55.8% .288 302.321)",
            "700": "oklch(49.6% .265 301.924)",
            "800": "oklch(43.8% .218 303.724)",
            "900": "oklch(38.1% .176 304.987)",
            "950": "oklch(29.1% .149 302.717)",
        },
        "font": {
            "subtle-light":   "var(--color-base-500)",
            "subtle-dark":    "var(--color-base-400)",
            "default-light":  "var(--color-base-600)",
            "default-dark":   "var(--color-base-300)",
            "important-light":"var(--color-base-900)",
            "important-dark": "var(--color-base-100)",
        },
    },
}
```

**Quick color generation:** Use https://oklch.com or https://unfoldadmin.com/colors/ to
convert hex colors to OKLCH and generate a full palette.

---

## 3. Custom Tailwind CSS

### Unfold ≥ 0.56 (recommended: Tailwind 4 or plain CSS)

For Unfold 0.56+, the simplest approach is writing plain CSS loaded via `UNFOLD["STYLES"]`.
If you need Tailwind utility classes in custom templates:

```bash
npm i tailwindcss @tailwindcss/cli
```

```css
/* styles.css */
@import 'tailwindcss';

/* your custom rules */
.my-widget { @apply bg-primary-600 text-white rounded; }
```

```bash
npx @tailwindcss/cli -i styles.css -o myapp/static/css/admin.css --minify
```

```python
UNFOLD = {
    "STYLES": [lambda request: static("css/admin.css")],
}
```

### Unfold < 0.56 (Tailwind 3)

```js
// tailwind.config.js — extend with Unfold's CSS variables
module.exports = {
    darkMode: "class",
    content: ["./myapp/**/*.{html,py,js}"],
    theme: {
        extend: {
            colors: {
                primary: {
                    50:  "rgb(var(--color-primary-50) / <alpha-value>)",
                    // ... 100 through 950
                },
                base: {
                    50:  "rgb(var(--color-base-50) / <alpha-value>)",
                    // ... 100 through 950
                },
            },
        },
    },
};
```

```bash
npx tailwindcss -i styles.css -o myapp/static/css/admin.css --minify --watch
```

---

## 4. Environment Label

```python
UNFOLD = {
    "ENVIRONMENT": "myapp.utils.environment_callback",
}

# myapp/utils.py
def environment_callback(request):
    import os
    env = os.getenv("DJANGO_ENV", "production")
    mapping = {
        "development": ["Development", "warning"],
        "staging":     ["Staging",     "info"],
        "production":  ["Production",  "danger"],
    }
    return mapping.get(env, ["Unknown", "info"])
```

---

## 5. Login Page Customization

```python
UNFOLD = {
    "LOGIN": {
        "image": lambda request: static("img/login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),
        "form": "myapp.forms.CustomLoginForm",  # optional
    },
}

# myapp/forms.py
from unfold.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    pass  # add custom fields/validation here
```

→ For full `UNFOLD` dict and all callback signatures, see `references/configuration.md`
→ For TABS configuration alongside sidebar, see `references/tabs.md`
