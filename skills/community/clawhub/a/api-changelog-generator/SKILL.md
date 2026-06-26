---
name: api-changelog-generator
description: Generate and maintain API changelogs from OpenAPI/Swagger specs — track endpoints added, removed, deprecated, or modified between versions. Detect breaking changes, generate migration guides, and produce consumer-facing release notes.
---

# API Changelog Generator

Track API changes across versions automatically. Compare OpenAPI specs to detect what changed, classify changes as breaking/non-breaking, and generate professional changelogs and migration guides for API consumers.

Use when: "generate API changelog", "what changed in the API", "API release notes", "breaking changes since v1", "API migration guide", "track API changes", or maintaining public API documentation.

## Commands

### 1. `diff` — Compare Two API Versions

Compare two OpenAPI/Swagger spec files and produce a structured diff.

```bash
OLD_SPEC="${1:?Usage: diff <old-spec> <new-spec>}"
NEW_SPEC="${2:?Usage: diff <old-spec> <new-spec>}"

python3 -c "
import json, sys, os

def load_spec(path):
    with open(path) as f:
        if path.endswith(('.yml', '.yaml')):
            try:
                import yaml
                return yaml.safe_load(f)
            except ImportError:
                print(f'Warning: PyYAML not installed, trying JSON parse')
                return json.load(f)
        return json.load(f)

old = load_spec('$OLD_SPEC')
new = load_spec('$NEW_SPEC')

# Extract paths (endpoints)
old_paths = set()
new_paths = set()
for path, methods in old.get('paths', {}).items():
    for method in methods:
        if method in ('get','post','put','patch','delete','options','head'):
            old_paths.add(f'{method.upper()} {path}')
for path, methods in new.get('paths', {}).items():
    for method in methods:
        if method in ('get','post','put','patch','delete','options','head'):
            new_paths.add(f'{method.upper()} {path}')

added = sorted(new_paths - old_paths)
removed = sorted(old_paths - new_paths)
common = sorted(old_paths & new_paths)

print('=== Endpoint Changes ===')
print(f'Added: {len(added)}, Removed: {len(removed)}, Modified: (checking...)')
print()

if added:
    print('🟢 New Endpoints:')
    for ep in added:
        print(f'  + {ep}')
    print()

if removed:
    print('🔴 Removed Endpoints (BREAKING):')
    for ep in removed:
        print(f'  - {ep}')
    print()

# Check for parameter changes in common endpoints
print('🟡 Modified Endpoints:')
for ep in common:
    method, path = ep.split(' ', 1)
    old_op = old['paths'].get(path, {}).get(method.lower(), {})
    new_op = new['paths'].get(path, {}).get(method.lower(), {})

    changes = []

    # Parameter changes
    old_params = {p.get('name',''): p for p in old_op.get('parameters', [])}
    new_params = {p.get('name',''): p for p in new_op.get('parameters', [])}

    for name in set(new_params) - set(old_params):
        req = new_params[name].get('required', False)
        changes.append(f'  + param: {name} ({\"required\" if req else \"optional\"}){\" (BREAKING)\" if req else \"\"}')
    for name in set(old_params) - set(new_params):
        changes.append(f'  - param: {name} (removed, BREAKING)')
    for name in set(old_params) & set(new_params):
        if old_params[name].get('required') != new_params[name].get('required'):
            if new_params[name].get('required'):
                changes.append(f'  ~ param: {name} now required (BREAKING)')
            else:
                changes.append(f'  ~ param: {name} now optional')

    # Response changes
    old_resps = set(old_op.get('responses', {}).keys())
    new_resps = set(new_op.get('responses', {}).keys())
    for code in new_resps - old_resps:
        changes.append(f'  + response: {code}')
    for code in old_resps - new_resps:
        changes.append(f'  - response: {code} (removed)')

    # Deprecation
    if new_op.get('deprecated') and not old_op.get('deprecated'):
        changes.append(f'  ⚠️  DEPRECATED')

    if changes:
        print(f'  {ep}:')
        for c in changes:
            print(f'    {c}')

# Schema changes
print()
print('=== Schema Changes ===')
old_schemas = old.get('components', old.get('definitions', {})).get('schemas', {})
new_schemas = new.get('components', new.get('definitions', {})).get('schemas', {})

for name in sorted(set(new_schemas) - set(old_schemas)):
    print(f'  + New schema: {name}')
for name in sorted(set(old_schemas) - set(new_schemas)):
    print(f'  - Removed schema: {name} (BREAKING if referenced)')
for name in sorted(set(old_schemas) & set(new_schemas)):
    old_props = set(old_schemas[name].get('properties', {}).keys())
    new_props = set(new_schemas[name].get('properties', {}).keys())
    old_req = set(old_schemas[name].get('required', []))
    new_req = set(new_schemas[name].get('required', []))

    added_props = new_props - old_props
    removed_props = old_props - new_props
    new_required = new_req - old_req

    if added_props or removed_props or new_required:
        print(f'  ~ {name}:')
        for p in sorted(added_props):
            brk = ' (BREAKING)' if p in new_req else ''
            print(f'      + property: {p}{brk}')
        for p in sorted(removed_props):
            print(f'      - property: {p} (BREAKING)')
        for p in sorted(new_required - added_props):
            print(f'      ~ property: {p} now required (BREAKING)')
" 2>/dev/null
```

### 2. `changelog` — Generate Formatted Changelog

Produce a consumer-facing changelog from the diff:

```markdown
# API Changelog

## v2.1.0 (2026-04-28)

### New Endpoints
- `POST /api/v2/webhooks` — Register webhook subscriptions
- `GET /api/v2/webhooks/{id}` — Get webhook details

### Breaking Changes
- `DELETE /api/v1/legacy-auth` — Removed (use `/api/v2/auth` instead)
- `POST /api/v2/users` — `email` parameter is now required
- Schema `UserResponse` — removed `legacy_id` property

### Deprecated
- `GET /api/v2/users/search` — Use `GET /api/v2/users?q=` instead (removal in v3.0)

### Non-Breaking Changes
- `GET /api/v2/users/{id}` — Added optional `include` parameter
- Schema `UserResponse` — Added `avatar_url` property
- `POST /api/v2/orders` — New response code `429` for rate limiting

### Migration Guide
1. Replace calls to `/api/v1/legacy-auth` with `/api/v2/auth`
2. Ensure `email` is included in `POST /api/v2/users` requests
3. Update response parsing to handle missing `legacy_id` in `UserResponse`
```

### 3. `breaking` — Breaking Changes Only

Filter the diff to show only breaking changes:
- Removed endpoints
- Removed parameters or schema properties
- Parameters changed from optional to required
- Response schema type changes
- Changed authentication requirements

Categorize severity:
- **Critical**: Endpoint removed, auth changed
- **High**: Required parameter added, response property removed
- **Medium**: Parameter type changed, new validation rules
- **Low**: Deprecation warnings

### 4. `migration` — Generate Migration Guide

For each breaking change, generate specific consumer migration instructions:

```markdown
## Migration Guide: v2.0 → v2.1

### 1. Removed: POST /api/v1/legacy-auth
**Impact:** All clients using v1 auth will get 404
**Action:**
- Replace `POST /api/v1/legacy-auth` with `POST /api/v2/auth`
- Update request body: `{username, password}` → `{email, password}`
- Response format changed: `{token}` → `{access_token, refresh_token, expires_in}`

### 2. Required param: POST /api/v2/users — email
**Impact:** Requests without `email` will get 422
**Action:**
- Add `email` field to all user creation requests
- Validate email format client-side before sending
```

### 5. `track` — Maintain Changelog History

Append new diff results to a running `API-CHANGELOG.md` file:

```bash
CHANGELOG="${1:-API-CHANGELOG.md}"

# If changelog exists, prepend new entry
if [ -f "$CHANGELOG" ]; then
  echo "Prepending to existing changelog: $CHANGELOG"
else
  echo "Creating new changelog: $CHANGELOG"
fi
```

Format: newest version at the top, Keep a Changelog compatible.

### 6. `consumers` — Estimate Consumer Impact

Scan the codebase for API calls that would be affected by breaking changes:

```bash
echo "=== Consumer Impact Analysis ==="

# Find API calls in the codebase
rg -n "(fetch|axios|http|request)\(['\"].*(/api/|/v[0-9])" \
  -g '*.{ts,js,py,go,java}' -g '!node_modules' -g '!vendor' 2>/dev/null | head -30

# For each breaking change endpoint, find matching calls
# (Use the removed/changed endpoints from diff output)
```

## Output Formats

- **text** (default): Human-readable changelog
- **json**: `{version, date, breaking: [], deprecated: [], added: [], modified: [], migration: []}`
- **markdown**: Consumer-facing changelog document
- **rss**: RSS/Atom feed format for API changelog subscriptions

## Notes

- Supports OpenAPI 3.x and Swagger 2.0 specifications
- YAML specs require PyYAML (falls back to JSON parsing)
- Breaking change classification follows semantic versioning conventions
- Schema diff handles nested objects and $ref resolution
- For best results, version your API specs in git and compare between tags
- Works alongside api-diff skill (which focuses on spec comparison; this focuses on changelog generation and consumer communication)
