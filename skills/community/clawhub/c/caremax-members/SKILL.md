---
name: caremax-members
description: "Manage family members in CareMax Health. Use when a user asks about family health tracking, switching between family member profiles, or viewing another family member's health data. Trigger terms: family member, member list, my family, switch member, spouse health, child health, parent health, 家人, 家庭成员."
license: MIT
---

# CareMax Family Members

> **Requires `caremax-auth` as a sibling directory** (`../caremax-auth/`). If missing, tell the user to install caremax-auth first (e.g. `npx skills add KittenYang/caremax-skills`).

List and work with family member profiles. CareMax supports tracking health data for multiple family members.

## Prerequisites — Auto-Auth (MANDATORY)

```bash
APICALL="bash ../caremax-auth/scripts/api-call.sh"
```

If `api-call.sh` returns `{"error":"no_credentials",...}` → **immediately run `bash ../caremax-auth/scripts/auth-flow.sh [base_url]`** in background (from this skill’s root). If the user specified a custom URL, pass it as the argument.

## List Members

```bash
$APICALL GET /api/skill/members
```

Response: `{"members":[{"id":"...","name":"...","gender":"...","relationship":"self","is_default":1},...]}`

## Using memberId in Other Queries

Pass `memberId` to scope queries to a specific family member:

```bash
# Indicators for a specific member
$APICALL GET "/api/skill/indicators?memberId=xxx"

# Records for a specific member
$APICALL POST /api/skill/records/query '{"memberId":"xxx"}'

# Search for a specific member
$APICALL POST /api/skill/records/search '{"query":"血常规","memberId":"xxx"}'
```

## Recommended Workflow

"show my wife's blood sugar":
```bash
# 1. Find spouse member
$APICALL GET /api/skill/members
# 2. Get indicators for that member (extract spouse's id)
$APICALL GET "/api/skill/indicators?memberId={spouse_id}"
# 3. Get trend for blood sugar indicator
$APICALL GET "/api/skill/indicators/trend?id={indicator_uuid}"
```

## Notes

- Every account has a default member (`is_default: 1` = the user themselves)
- If no `memberId` specified, queries return data for the default member
- `relationship` values: self, spouse, child, parent, sibling, other
