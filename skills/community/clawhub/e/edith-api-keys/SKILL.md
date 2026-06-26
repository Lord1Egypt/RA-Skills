---
name: edith-api-keys
description: Manage Edith smart glasses API keys with Unkey. Create, revoke, and list API keys via voice commands.
user-invocable: true
---

# Edith API Keys

Manage API keys for the Edith smart glasses app using Unkey.

## Setup

The user must have `UNKEY_ROOT_KEY` and `UNKEY_API_ID` set as environment variables.
- `UNKEY_ROOT_KEY` — root key from the Unkey dashboard (used to create/revoke keys)
- `UNKEY_API_ID` — the Unkey API ID that Edith verifies keys against

## Tools

This skill uses `curl` to call the Unkey REST API. All requests go to `https://api.unkey.dev`.

## Commands

### Create a new API key

Create a key for a plugin developer or device. Optionally set a name, expiration, or rate limit.

```bash
curl -s -X POST https://api.unkey.dev/v1/keys.createKey \
  -H "Authorization: Bearer $UNKEY_ROOT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "apiId": "'"$UNKEY_API_ID"'",
    "name": "{{name}}",
    "prefix": "edith",
    "meta": { "purpose": "{{purpose}}" },
    "expires": {{expires_unix_ms_or_null}},
    "ratelimit": {
      "async": true,
      "limit": {{rate_limit_per_second_or_10}},
      "duration": 1000
    }
  }'
```

Response includes `key` (give this to the user) and `keyId` (for management).

### List all keys

```bash
curl -s "https://api.unkey.dev/v1/apis.listKeys?apiId=$UNKEY_API_ID" \
  -H "Authorization: Bearer $UNKEY_ROOT_KEY"
```

### Revoke a key

Permanently delete a key by its `keyId`.

```bash
curl -s -X POST https://api.unkey.dev/v1/keys.deleteKey \
  -H "Authorization: Bearer $UNKEY_ROOT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyId": "{{keyId}}"}'
```

### Verify a key (read-only check)

```bash
curl -s -X POST https://api.unkey.dev/v1/keys.verifyKey \
  -H "Content-Type: application/json" \
  -d '{"apiId": "'"$UNKEY_API_ID"'", "key": "{{key}}"}'
```

### Update a key (rename, change rate limit, set expiry)

```bash
curl -s -X POST https://api.unkey.dev/v1/keys.updateKey \
  -H "Authorization: Bearer $UNKEY_ROOT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "keyId": "{{keyId}}",
    "name": "{{new_name}}",
    "ratelimit": {
      "async": true,
      "limit": {{new_limit}},
      "duration": 1000
    }
  }'
```

## Workflow

When the user asks to manage Edith API keys:

1. Check that `UNKEY_ROOT_KEY` and `UNKEY_API_ID` are set in the environment.
2. If creating a key: ask for a name/purpose, create it, and display the key to the user (it is only shown once).
3. If listing keys: fetch and display in a table with keyId, name, createdAt, and status.
4. If revoking: confirm the keyId with the user, then delete.
5. Plugins connect to the Edith WebSocket relay with `?linkCode=...&apiKey=...` — the relay verifies the key via Unkey automatically when `UNKEY_API_ID` is set on the server.

## Example

User: "Create an API key for my demo plugin"

```bash
curl -s -X POST https://api.unkey.dev/v1/keys.createKey \
  -H "Authorization: Bearer $UNKEY_ROOT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "apiId": "'"$UNKEY_API_ID"'",
    "name": "demo-plugin",
    "prefix": "edith",
    "meta": { "purpose": "demo plugin" },
    "ratelimit": { "async": true, "limit": 10, "duration": 1000 }
  }'
```
