# Setup — Django

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Django rewards knowing which layer owns a rule. Before proposing a fix, say which layer it lives in — database constraint, model, form or serializer, view, or infrastructure — and prefer the lowest one that can enforce it. When something is slow, count the queries before changing any code; when something is unsafe, check the queryset before checking the permission.

## How To Load Preferences

1. Read `~/Clawic/data/django/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `django_version: 5.2`, `database: postgres`, `api_layer: drf`, `settings_layout: split-by-env`, `project_layout: flat`, `task_queue: celery`, `test_runner: django`, `deploy_target: gunicorn-wsgi`, `destructive_confirm: true`.
3. Read `~/Clawic/data/django/memory.md` for prior context (their project shape, recurring pain points). Absence is fine; proceed without comment.
4. Universal values (units, locale, timezone) fall back to `~/Clawic/profile.yaml` when this skill has no key of its own.

The repository beats any stored value: `requirements`/`pyproject` name the Django version, `settings.py` names the database engine and whether DRF is installed, and `manage.py` confirms the settings module. The stored value is the fallback for when there is no project in front of you.

Work from defaults immediately. Never open with questions about their stack, their scale, or how proactive to be.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a Django version, database engine, API layer, settings layout, project layout, task queue, test runner, or deployment target → update the matching key in `~/Clawic/data/django/config.yaml`.
- User expresses a habit or stance (fat models vs services, whether migrations may be applied directly, banned packages, how much explanation they want with generated code) → record it under the relevant preference area (tooling, thresholds, conventions, platform, risk posture, output format, work order, integrations, restrictions, cadence) in `~/Clawic/data/django/memory.md`.
- User corrects earlier guidance → update the stored value so it is not repeated.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file format. Track the shape of their project (apps, scale, whether it is an API, a server-rendered site, or both), the constraints they operate under, the incidents they have hit, and how much explanation they want — but only from what they actually reveal.
