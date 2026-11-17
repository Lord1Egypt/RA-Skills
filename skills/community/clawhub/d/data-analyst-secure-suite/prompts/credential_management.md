# Credential Management Workflow

This document guides data analysts on how to securely manage database keys, API tokens, and other sensitive credentials in **MGC Blackbox ≥ 1.5.4**, and implement **zero-exposure calls** in scripts.

All sensitive operations must be explicitly authorized by the user before proceeding.

---

# 1. Credential Management Overview

MGC Blackbox provides local encrypted storage and zero-exposure access capabilities:

- Credentials never exposed to AI in plaintext
- Credentials decrypted only on the user's local machine
- Scripts can safely call credentials, but AI cannot see content
- All access requires user authorization

---

# 2. How to Securely Store Credentials

Credential storage is recommended via **MGC WebUI** or **mgc_save** tool.

## Method 1: Via WebUI (Recommended)

1. Start MGC:
   ```
   mgc
   ```
2. Open WebUI:
   ```
   http://127.0.0.1:57218
   ```
3. Navigate to **Save page**
4. Fill in fields:

```
info_type: "token"
info_owner: "db_warehouse_prod"   # Custom name
content: <your database credentials>  # Plaintext encrypted locally
```

## Method 2: Via mgc_save

```python
mgc_save(
    info_type="token",
    info_owner="db_warehouse_prod",
    content="postgres://user:password@host:5432/dbname"
)
```

### Security Notes

- Credentials stored encrypted locally
- AI cannot see credential content
- All access requires user authorization
- Credentials never leave the user's machine

---

# 3. How to Call Credentials with Zero Exposure (Core)

**MGC implementation**: scripts are stored in MGC; at runtime MGC decrypts and executes the script locally. If the script needs to access credentials, it calls a local API to fetch them internally.

## Standard Example: Script Internally Accesses Credentials Safely

```python
import os, requests, json

# Read MGC access token (fixed path, do not change)
with open(os.path.expanduser("~/.mgc/database/mgc_black_box/.mgc_token")) as f:
    MGC_TOKEN = f.read().strip()

def get_credential(info_owner="db_warehouse_prod"):
    """Fetch credential from MGC"""
    resp = requests.post(
        "http://127.0.0.1:57219/api/mgc/sensitive/get",
        headers={"X-MGC-Token": MGC_TOKEN},
        json={
            "info_type": "token",
            "info_owner": info_owner,
        },
    )
    if resp.status_code == 200:
        data = resp.json()
        if data.get("code") == 200:
            data_field = data.get("data")
            if isinstance(data_field, str):
                return json.loads(data_field)
            elif isinstance(data_field, dict):
                content = data_field.get("content")
                if content:
                    return json.loads(content)
    return None

# Using credential
def query_monthly_orders():
    credential = get_credential("db_warehouse_prod")
    # ... use credential to connect and query
```

**Notes**:
- This call is local-only (127.0.0.1), AI cannot see credentials
- Token file path: `~/.mgc/database/mgc_black_box/.mgc_token`
- Script execution is managed by MGC, and credentials are decrypted inside MGC

## Locating Credentials by Name (Recommended Workflow)

Before accessing a credential, locate it with **mgc_find** (fuzzy search by name):

```python
# Fuzzy search for a credential by name
matches = mgc_find(
    info_owner="db_warehouse",  # partial name; substring match by default
    # Note: mgc_find does not accept info_type since 1.5.0 — pass only
    # info_owner / diff_1..3
)
# Returns metadata list — never the credential plain_text.
# After locating the exact info_owner, the script internally calls the MGC API
# to retrieve and decrypt.
```

**Security features**:
- `mgc_find` never returns credential plain_text — only metadata
- After locating, the script still goes through the MGC API (local decryption)
- All access still requires user authorization

---

# 3.5 Credential Rotation and Deletion (new in 1.5.4)

## Credential rotation

Rotation does not change `info_owner` — just overwrite the record with new content:

```python
mgc_save(
    info_type="token",
    info_owner="db_warehouse_prod",   # the same name
    content="postgres://user:newpassword@host:5432/dbname",
)
# After the overwrite the old password is invalid immediately — no delete needed
```

## Deleting an obsolete credential (`mgc_delete`, new in 1.5.4)

When a credential has expired, is no longer used, or is suspected to be compromised, you can delete the local record:

```python
mgc_delete(
    info_type="token",
    info_owner="db_warehouse_prod",
)
```

**Authorization requirement**: `mgc_delete` is irreversible, so the AI must first state what will be deleted and obtain explicit user authorization:

```
Credential Name: db_warehouse_prod
Operation: Delete local credential record (irreversible)
Authorization Required: YES

Do you authorize deleting this credential? Reply "yes" to proceed, or "no" to cancel.
```

**Notes**:
- `info_type` and `info_owner` are both required for `mgc_delete`
- The deletion targets the local encrypted storage only — it does not change the credential state in any external system
- MGC protects the node's own credentials (such as `__NODE_PUB__`); attempts to delete such protected records are refused
- If the exact `info_type` is uncertain, look up the metadata with `mgc_find` first

---

# 4. How to Authorize Credential Access (User Must Confirm)

When AI needs to access credentials, it must ask the user:

```
Credential Name: db_warehouse_prod
Operation: Access Credential
Authorization Required: YES

Do you authorize accessing this credential? Reply "yes" to proceed, or "no" to cancel.
```

AI must not access any credentials without user authorization.

---

# 5. Best Practices

### ✔ 1. Use Descriptive info_owner
For example:
- `db_warehouse_prod`
- `api_salesforce_token`
- `redis_cache_credential`

### ✔ 2. Do Not Hardcode Credentials in Scripts
All credentials must be obtained via MGC.

### ✔ 3. Do Not Paste Credentials in AI Conversations
AI cannot protect plaintext credentials.

### ✔ 4. All Access Requires Authorization
AI must not automatically access credentials.

### ✔ 5. Clean Up Expired Credentials Promptly
After rotating a credential, if no other script still references the old one, remove the local record with `mgc_delete` (user authorization required).

---

# 6. FAQ

| Issue | Solution |
|-------|----------|
| Script cannot access credentials | Check if `info_owner` matches |
| Credentials empty | Check if WebUI stored correctly |
| Execution failed | Check if script dependencies are available locally |
| `mgc_find` reports a parameter error | `mgc_find` does not accept `info_type` (removed since 1.5.0) — pass only `info_owner` / `diff_1..3` |
| `mgc_find` matches multiple records with the same name | Inspect the returned metadata (`diff_1` / `diff_2` / `diff_3`) and narrow down with a more precise `diff_*` |
| `mgc_delete` is refused | Protected records (such as the node's own credentials) cannot be deleted; confirm `info_type` and `info_owner` match exactly |
| Still getting the old password after an overwrite | Make sure `info_type` and `info_owner` exactly match the original record — otherwise a new record is created instead |

---

# 7. Summary

This credential management document provides:

- Local encrypted storage
- Zero-exposure calls
- User authorization mechanism
- Secure script writing guidelines
- Credential rotation and secure deletion (1.5.4)

This is the foundational capability for secure data analyst workflows.

---

## Collaboration extension (1.5.4+)

### Sharing access rights (not the data)

Multiple team members can each call the same credential (e.g. `db_warehouse_prod`) from their own machines through MGC, without sharing any data externally. Each member stores the credential on their own node via `mgc_save` and reads it via `mgc_get`.

### Sharing analysis methods and scripts across the team

When the team wants to share **analysis methods and scripts** (not just credentials), use `mgc_seal_package` to seal a workflow folder to a target node (one-key-per-node), or omit `ext04` to seal in free mode for public distribution. See `prompts/collaboration_management.md` for the full flow.

---
