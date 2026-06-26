# Content360 Integration Skill

## Status: Working ✅

The Content360 API is now fully reverse-engineered and operational. Post creation, listing, and deletion all verified working.

## What Was Built

1. **`content360_sync.py`** — Full sync script that:
   - Authenticates via email/password session (required for bearer tokens to work)
   - Reads posts from Notion Master Content Calendar
   - Creates posts in Content360 via the Inertia API
   - Marks posts as "Posted" in Notion after sync
   - Supports `--dry-run` and `--platforms` filtering

2. **`SKILL.md`** — Complete API reference with all endpoints, auth flow, and account IDs

## Setup

### 1. Set Secrets

Add to [Zo Secrets](/?t=settings&s=advanced):

| Key | Value |
|-----|-------|
| `CONTENT360_EMAIL` | `delowery@gmail.com` |
| `CONTENT360_PASSWORD` | Your password |
| `CONTENT360_API_KEY` | Bearer token from app.content360.io/os/profile/access-tokens |
| `CONTENT360_ORG_ID` | `3f3006c0-a68f-4ac6-b4ee-c14d70356cbb` |

### 2. Install Dependencies

```bash
pip install requests
```

### 3. Run Sync

```bash
# Dry run first
python3 /home/workspace/Skills/content360/scripts/content360_sync.py --dry-run

# Real sync
python3 /home/workspace/Skills/content360/scripts/content360_sync.py

# Platform filter
python3 /home/workspace/Skills/content360/scripts/content360_sync.py --platforms facebook,linkedin,youtube
```

## Key Discovery: Auth Flow

Content360 uses **Laravel Sanctum + Inertia.js**. The auth requires:

1. **Session cookie** from logging in via email/password
2. **Bearer token** (access token) in the `Authorization` header
3. **`X-Inertia-Version`** hash header (extracted from any authenticated response)
4. **`X-Requested-With: XMLHttpRequest`** on every request

The bearer tokens will NOT work without an active session cookie. The sync script handles this by:
1. Logging in via form POST to establish session
2. Extracting the Inertia version from responses
3. Making all subsequent requests with full auth headers

## API Summary

- **Base**: `https://app.content360.io/os/api/{org_uuid}/`
- **Auth**: Bearer token + session cookie + Inertia headers
- **Create Post**: POST `/posts` with `content`, `accounts[]`, `status: "draft"`, and `versions[]` array
- **List Posts**: GET `/posts`
- **Delete Post**: DELETE `/posts/{uuid}`
- **Accounts**: GET `/accounts`

## Notion Database
- Database ID: `fe775ea4-5edb-4ecd-88de-86f09ae77c5d` (Master Content Calendar)
- **Properties used**: `Posted` (checkbox), `Schedule` (date), `Platform` (select), `Caption` (rich_text), `Hook` (rich_text), `CTA` (rich_text)
