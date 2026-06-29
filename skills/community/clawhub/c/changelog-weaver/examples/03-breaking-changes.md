# Example: Breaking Change Audit & Migration Guide

## Scenario

Your API server (`api-server`) is releasing v3.0.0 — a major version bump. Between v2.9.0 and v3.0.0 there are 89 commits, including multiple breaking changes. The changelog must:

1. Clearly identify every breaking change — both explicitly marked and implicit
2. Provide a migration guide with before/after examples
3. Group related breaking changes together
4. Highlight security implications

## Step-by-Step

### 1. Collect commits

```bash
cd ~/projects/api-server
python3 ~/.openclaw/skills/changelog-weaver/scripts/weaver.py collect \
  --from v2.9.0 --to v3.0.0 \
  --version 3.0.0 \
  -o v3.0.0-commits.json
```

**Output:** `[SUMMARY] 89 commits, 12 contributors, 5 breaking changes`

### 2. AI Breaking Change Audit

> **Prompt:** "Load `v3.0.0-commits.json`. This is a major version bump (v2.9 → v3.0). I need a thorough breaking change audit:
>
> 1. Confirm all 5 explicitly marked breaking changes are correct
> 2. Scan ALL commits (including `other`, `refactor`, `chore`) for UNMARKED breaking changes — look for keywords: 'remove', 'deprecate', 'rename', 'drop support', 'change default', 'no longer', 'migrate from'
> 3. For each breaking change, write a migration note with BEFORE/AFTER examples
> 4. Flag changes that affect authentication, authorization, or data integrity as HIGH IMPACT
> 5. Generate the changelog with a `📋 Migration Guide` section at the very top
>
> The audience is API consumers who need to update their integrations."

### 3. AI Identifies Hidden Breaking Changes

The AI scans all 89 commit descriptions and finds 2 unmarked breaking changes:

| Hash | Original Commit | Why Breaking |
|------|----------------|--------------|
| `f3a2b1c0` | `refactor: normalize error response format` | Changed error response structure — clients parsing the old format will break |
| `a9b8c7d6` | `chore: update minimum Node version` | Dropped Node 16 support — CI/CD pipelines on Node 16 will fail |

### 4. AI Generates Migration Guide

> **AI Response:** "I found 7 breaking changes total (5 marked, 2 unmarked). Here are the migration notes with impact assessment..."

### 5. Generate final output

```bash
python3 scripts/weaver.py generate \
  -i v3.0.0-commits.json \
  -f changelog \
  -o CHANGELOG.md
```

## Final Output: CHANGELOG.md (excerpt)

```markdown
# Changelog

## [3.0.0] - 2026-06-15

### 📋 Migration Guide

> **v2.9 → v3.0 requires code changes.** Most integrations need 1-3 hours to migrate.

#### 🔴 HIGH IMPACT — Authentication
**Change:** Token scheme changed from `Token` to `Bearer`
```diff
- Authorization: Token abc123def456
+ Authorization: Bearer abc123def456
```
**Affected:** All API consumers. Old tokens continue to work with the new header format.

#### 🔴 HIGH IMPACT — User API Endpoint
**Change:** `/api/v1/users` removed. Use `/api/v2/users` with filter-based query params.
```diff
- GET /api/v1/users?role=admin&status=active
+ GET /api/v2/users?filter[role]=admin&filter[status]=active
```
**Affected:** Admin dashboards, user management scripts, CI/CD user provisioning.

#### 🟡 MEDIUM IMPACT — Error Response Format
**Change:** Error responses now use RFC 7807 (Problem Details) format.
```diff
- {"error": "Not Found", "code": 404}
+ {"type": "https://api.example.com/errors/not-found",
+  "title": "Resource Not Found",
+  "status": 404,
+  "detail": "User with id '99999' was not found"}
```
**Affected:** Error handling in all client applications. Old format returned a flat object; new format is a structured Problem Details object.

#### 🟡 MEDIUM IMPACT — Webhook Payloads
**Change:** `event.data` is now always an object (was sometimes a string for simple events).
```diff
- {"event": "user.created", "data": "user_12345"}
+ {"event": "user.created", "data": {"id": "user_12345"}}
```
**Affected:** Webhook handlers. Add a runtime type check: `typeof event.data === 'string' ? JSON.parse(...) : event.data`.

#### 🟢 LOW IMPACT — Node.js Version
**Change:** Node.js 16 is no longer supported. Minimum version is now Node.js 18 LTS.
**Affected:** CI/CD pipelines, Docker images, local development environments.

#### 🟢 LOW IMPACT — Rate Limit Headers
**Change:** Rate limit headers renamed for IETF draft compliance.
```diff
- X-RateLimit-Limit / X-RateLimit-Remaining / X-RateLimit-Reset
+ RateLimit-Limit / RateLimit-Remaining / RateLimit-Reset
```
**Affected:** Rate-limit-aware clients. Old headers are still sent as `X-RateLimit-*` until v3.1.0 for backwards compatibility.

#### 🟢 LOW IMPACT — Deprecated Fields
**Change:** `user.middleName` and `user.salutation` fields removed from user object.
**Affected:** Fewer than 2% of API consumers use these fields. Contact support if affected.

---

### ⚠️ Breaking Changes
- Changed authentication scheme from `Token` to `Bearer` header (#1189)
- Removed `/api/v1/users` — use `/api/v2/users` with filter-based params (#1204)
- Normalized error responses to RFC 7807 Problem Details format (#1156)
- Normalized webhook `event.data` to always be an object (#1215)
- Dropped Node.js 16 support — minimum is now Node.js 18 LTS (#1190)
- Renamed rate limit headers for IETF compliance (#1178)
- Removed deprecated `user.middleName` and `user.salutation` fields (#1167)

### ✨ Features
- Added bulk user import API with CSV validation and progress tracking (#1198)
- New webhook retry mechanism with exponential backoff (max 5 retries) (#1207)
- API key scoping — restrict keys to specific endpoints and IP ranges (#1180)
- Request ID tracking header (`X-Request-ID`) on all responses (#1201)

### 🐛 Bug Fixes
- Fixed pagination cursor drift under concurrent writes (#1195)
- Fixed 429 rate limit not resetting correctly for IPv6 clients (#1185)

### 🔒 Security
- Patched JWT key confusion vulnerability (CVE-2026-1234) (#1210)
- Added CSRF protection to OAuth callback endpoint (#1209)

### 🙏 Contributors
@alice, @bob, @charlie, @dave, @eve, @frank, @grace, @henry, @ivan, @julia, @kevin, @lisa
```

## Key Takeaways

1. **AI finds hidden breaking changes** — `refactor: normalize error responses` sounds innocent but breaks all clients
2. **Impact classification** — 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW helps consumers prioritize migration
3. **Before/After code snippets** — developers can copy-paste the migration
4. **Affected audience** — each change says who's impacted
5. **Backwards compatibility notes** — some changes have grace periods (e.g., old rate limit headers still sent until v3.1.0)
