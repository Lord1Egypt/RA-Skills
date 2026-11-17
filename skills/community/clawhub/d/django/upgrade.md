# Upgrades — Versions, Deprecations, LTS Windows

An upgrade is not a version bump. It is a sequence of releases, each one taken on a green test suite with deprecation warnings turned into errors. Skipping the sequence is what turns a routine upgrade into a week.

## Contents

- The Release Calendar
- The Deprecation Contract
- The Upgrade Loop
- Third-Party Packages Are The Real Cost
- Removals Worth Knowing About
- Silent Failures During An Upgrade
- Migrations Across An Upgrade
- Staying Upgradable

## The Release Calendar

- Django ships a feature release roughly every eight months, and **every third release is an LTS** (2.2, 3.2, 4.2, 5.2). A non-LTS release gets mainstream fixes until the next feature release and security fixes for about eight months after that; an LTS gets security fixes for about three years.
- Two viable policies, pick one and write it down: **LTS-to-LTS** (upgrade once every ~2.5 years, a bigger jump, fewer interruptions) or **every release** (small jumps, continuous work, always inside mainstream support). Anything else means running unsupported for stretches you did not choose.
- Running past end of life is not "old but fine": published Django security advisories then apply to you with no patch to take.
- Each feature release also raises the **Python floor** (Django 5.0 dropped Python 3.8 and 3.9). Check the Python requirement before planning the Django one — a Django upgrade blocked on a runtime upgrade is a different project.

## The Deprecation Contract

Django's promise is what makes staged upgrades work:

- A feature deprecated in a release is **removed two feature releases later** — deprecated in 4.0, removed in 5.0; deprecated in 4.2, removed in 5.1.
- While deprecated, using it raises a `RemovedInDjangoXXWarning`, which is a `DeprecationWarning` subclass and therefore **invisible by default**.
- Consequence, and the whole reason staged upgrades are cheap: every removal that will break you on version N+1 already warns on version N. **The work of upgrading is done on the version you are already running.**

```
python -Wa manage.py test        # surface every deprecation warning
python -W error::DeprecationWarning -m pytest    # or make them fail the build
```

- Put that in CI on the current version. A suite that is green with warnings-as-errors makes the next upgrade a version bump; a suite that hides them makes it an excavation.
- Warnings only fire on code paths the tests execute. Low-coverage areas — management commands, admin customizations, migration files — are where the surprise lives.

## The Upgrade Loop

One iteration per feature release, never two at once:

1. **Land on the latest patch of the current series** (`5.1.x` before touching 5.2). Patch releases are safe and remove noise from the diff.
2. **Read the release notes of the target version, backwards from "Backwards incompatible changes" and "Features removed".** The "New features" half can wait; those two lists are the upgrade.
3. **Green suite with `-Wa` on the current version.** Fix every `RemovedInDjangoXXWarning` before bumping anything.
4. **Bump Django alone**, no other dependency in the same commit. When something breaks you need to know which change did it.
5. **Run `manage.py check`, then `check --deploy`, then the suite, then `makemigrations --check --dry-run`.** The last one catches model-level changes the new version now autodetects differently.
6. **Deploy on its own**, ahead of feature work, with the previous artifact one rollback away.

- Upgrading Django and the third-party stack in one deploy is the most common way to lose a day: the failure is real, and the bisect surface is the whole requirements file.
- Rehearse on a restored copy of production for anything with data-shaped risk. Test data does not have the row that trips the new validation.

## Third-Party Packages Are The Real Cost

- Django itself rarely blocks the upgrade; a package that has not declared support for the target version does. Inventory before planning: for each dependency, the latest version and the Django versions it claims.
- The blocking package is a fork-or-drop decision, and it is better made in week one than in week three. An unmaintained package pinning you to an end-of-life Django is a security problem, not a preference.
- Packages that hook deep — anything touching the migration autodetector, the admin's templates, custom model fields, or middleware internals — break more often than packages that only add views.
- `pip list --outdated` names candidates; the package's own changelog is what tells you whether the new major is a drop-in.

## Removals Worth Knowing About

Stable history: these are what actually breaks in real projects.

| Removed / changed | Since | Replacement |
|---|---|---|
| `django.conf.urls.url()` | Removed in 4.0 | `re_path()`, or `path()` where the pattern allows |
| `force_text`, `smart_text`, `ugettext*` | Removed in 4.0 | `force_str`, `smart_str`, `gettext*` |
| `pytz` as the timezone library | Replaced by `zoneinfo` in 4.0 | Stop passing `pytz` objects to `timezone.activate()` |
| `CSRF_TRUSTED_ORIGINS` without a scheme | Changed in 4.0 | Full origins: `https://app.example.com` |
| `USE_L10N` | Removed in 5.0 | Localized formatting follows `USE_I18N` |
| `USE_TZ` default | Flipped to `True` in 5.0 | Audit every naive datetime before landing 5.0 |
| GET on `LogoutView` | Removed in 5.0 | POST, so every logout link becomes a form |
| `DEFAULT_FILE_STORAGE`, `STATICFILES_STORAGE` | Replaced by `STORAGES` in 4.2, removed in 5.1 | One `STORAGES` dict |
| `Meta.index_together` | Deprecated in 4.2, removed in 5.1 | `Meta.indexes` with `models.Index` |
| `DEFAULT_AUTO_FIELD` unset | Warns since 3.2 (`models.W042`) | Set `BigAutoField` project-wide |

- Set `django_version` in Configuration so version-gated advice matches the project instead of the default.

## Silent Failures During An Upgrade

The dangerous half of an upgrade raises nothing:

- **A removed setting is ignored, not rejected.** Django never validates unknown settings names, so a setting the new version dropped simply stops having an effect. `diffsettings` against the release notes is the only check.
- **A changed default applies silently.** `USE_TZ` flipping to `True` changes what every naive datetime comparison means, with no error anywhere.
- **A tightened check turns a warning into a failure at deploy, not at import** — `manage.py check` in CI is what moves that discovery earlier.
- **Template and admin overrides drift.** A copied admin template keeps rendering against a changed context and loses a widget rather than raising.
- **Third-party middleware ordering assumptions** change when a Django middleware is added or split; symptoms show as auth or CSRF weirdness, not as an import error.

## Migrations Across An Upgrade

- Old migration files are executable code, and they import from Django. A removed API referenced in a migration from three years ago breaks the whole graph on a fresh database, which CI catches only if CI builds from migrations.
- Squashing before a big jump shrinks that surface, but do it as its own deploy: every environment must have applied the full replaced range first.
- After the bump, `makemigrations --check --dry-run` must be clean. A new Django version that autodetects a field attribute differently will otherwise generate a surprise migration in someone's feature branch.
- Never let an upgrade and a destructive migration ride in the same release. Rollback of code is easy; rollback of a schema change is not.

## Staying Upgradable

- Prefer documented APIs. Every import from a `django.*.utils` internal is a private contract with no deprecation cycle.
- Copying a Django template or subclassing an admin internal is a fork you now maintain across every release; count it as such.
- Keep the deprecation-warnings-as-errors job green permanently. Its value is not the current release, it is that the next one costs a bump.
- Track advisories for Django and for the dependency tree separately — the framework's own advisory list and a `pip-audit`-style scan answer different halves of the question.
