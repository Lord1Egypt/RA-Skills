# Audit Examples

Examples for the audit-first workflow.

## 1. Admin surface vs backend

```bash
python3 scripts/audit_contracts.py \
  --frontend /Users/imjuna/projects/dangori-admin/frontend \
  --backend /Users/imjuna/projects/dangori-admin/backend \
  --output-dir ./out/admin-audit \
  --fail-on high
```

Use when checking whether admin frontend calls still match admin backend mappings after controller or DTO changes.

## 2. Manager surface vs shared backend

```bash
python3 scripts/audit_contracts.py \
  --frontend /Users/imjuna/projects/dangori/dangori-manager \
  --backend /Users/imjuna/projects/dangori/backend \
  --output-dir ./out/manager-audit \
  --exclude coverage,.dart_tool
```

Use when validating manager web request paths, pageable queries, and request payloads against the shared backend.

## 3. Multiple frontend roots against one backend

```bash
python3 scripts/audit_contracts.py \
  --frontend /path/to/admin \
  --frontend /path/to/mobile \
  --backend /path/to/backend \
  --output-dir ./out/multi-surface-audit \
  --format md \
  --summary-only
```

Use when multiple clients share one backend and you want one combined mismatch report.

## 4. Express frontend vs Express backend

```bash
python3 scripts/audit_contracts.py \
  --frontend /path/to/react-or-next-app \
  --backend /path/to/express-api \
  --output-dir ./out/express-audit \
  --exclude dist,build,node_modules \
  --fail-on high
```

Use when the backend is Node/Express and routes are declared with `app.get/post/...`, `router.get/post/...`, or `router.route(...)` patterns.

## 5. Laravel frontend vs Laravel backend

```bash
python3 scripts/audit_contracts.py \
  --frontend /path/to/web-client \
  --backend /path/to/laravel-api \
  --output-dir ./out/laravel-audit \
  --exclude vendor,storage,bootstrap/cache \
  --fail-on high
```

Use when the backend is Laravel and routes are declared in standard `routes/*.php` files with controller actions or resource routes.

## 6. Targeted follow-up live check

Only after audit, run live helper on a narrow scenario:

```bash
python3 scripts/generate_tests.py --config config.json --read-only
```

Use this only for dev/staging follow-up verification.
