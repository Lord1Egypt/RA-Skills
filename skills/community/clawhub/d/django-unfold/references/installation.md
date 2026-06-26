# Installation & Setup Reference

> **Related files:** `../SKILL.md` (global rules), `references/configuration.md` (full UNFOLD dict),
> `references/theming.md` (sidebar/colors after setup)

## 1. Install the Package

```bash
pip install django-unfold
# or
uv add django-unfold
# or
poetry add django-unfold
```

## 2. INSTALLED_APPS (order critical)

```python
INSTALLED_APPS = [
    "unfold",                           # MUST BE FIRST
    "unfold.contrib.filters",           # optional: advanced filter types
    "unfold.contrib.forms",             # optional: WYSIWYG, Array widgets, crispy
    "unfold.contrib.inlines",           # optional: nonrelated inlines
    "unfold.contrib.import_export",     # optional: django-import-export
    "unfold.contrib.simple_history",    # optional: django-simple-history
    "unfold.contrib.guardian",          # optional: django-guardian
    "unfold.contrib.constance",         # optional: django-constance
    "unfold.contrib.location_field",    # optional: django-location-field
    "django.contrib.admin",             # AFTER unfold
    "django.contrib.auth",
    "django.contrib.contenttypes",
    # ... your apps
]
```

## 3. URLs — no changes needed

```python
# urls.py — default Django admin URLs work unchanged
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]
```

## 4. User & Group Re-registration (Required)

Django's built-in User and Group models won't have Unfold styling unless re-registered:

```python
# admin.py (in any app, e.g. your main app)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
```

> **Note:** The MRO (Method Resolution Order) matters: `BaseUserAdmin` must come before `ModelAdmin`.

## 5. Minimal ModelAdmin

```python
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin):
    pass  # Already styled — add options as needed
```

## 6. Parallel Admin (Run Default + Unfold Side by Side)

Useful for gradual migration from standard Django admin:

```python
# admin_default.py — separate file for default admin
from django.contrib.admin import AdminSite

default_admin = AdminSite(name="default_admin")

# urls.py
from django.contrib import admin  # Unfold-powered
from .admin_default import default_admin

urlpatterns = [
    path("admin/", admin.site.urls),            # Unfold admin
    path("django-admin/", default_admin.urls),  # Original admin
]
```

## 7. Collectstatic (Production)

```bash
python manage.py collectstatic
```

Forgetting this is the most common cause of missing styles in production.

## 8. Django Version Requirements

- Unfold ≥ 0.90: requires **Django 5.0+** (Django 4.2 support dropped)
- Unfold < 0.90: supports Django 4.2+

→ Next steps: configure `UNFOLD` dict in `references/configuration.md`
→ Set up sidebar navigation and colors in `references/theming.md`
