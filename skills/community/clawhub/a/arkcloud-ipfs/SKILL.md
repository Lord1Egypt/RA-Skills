---
name: arkcloud-ipfs
description: ARKCloud IPFS OpenClaw skill for file.arklink.hk. Upload, publish, list, and delete files through ARKCloud and return IPFS CID, access link, credit usage, and duplicate status. Use when the user searches or mentions arkcloud, ARKCloud, arkcloud-ipfs, ARK Cloud, IPFS, CID, file.arklink.hk, uploading a file or folder to IPFS, getting an ARKCloud file link, querying uploaded resources, deleting or unpublishing an upload, or checking ARKCloud upload API health.
version: 0.1.6
metadata:
  openclaw:
    homepage: https://github.com/djanngau/arkcloud-ipfs-skill
    primaryEnv: ARKCLOUD_UPLOAD_TOKEN
    requires:
      env:
        - ARKCLOUD_UPLOAD_TOKEN
    envVars:
      - name: ARKCLOUD_UPLOAD_TOKEN
        required: true
        description: Bearer token for the ARKCloud file upload API.
      - name: ARKCLOUD_BASE_URL
        required: false
        description: Optional ARKCloud base URL. Defaults to https://file.arklink.hk.
      - name: ARKCLOUD_CLIENT_COOKIE
        required: false
        description: Optional logged-in client session cookie for listing, folder upload, and delete helpers.
      - name: ARKCLOUD_CSRF_TOKEN
        required: false
        description: Optional CSRF token used with the client session helpers.
---

# ARKCloud IPFS

Keywords: arkcloud, ARKCloud, arkcloud-ipfs, ARK Cloud, OpenClaw skill, CowAgent skill, Claude Code skill, IPFS, CID, file.arklink.hk, decentralized storage, upload API.

Use ARKCloud's token-protected upload API. Do not call or expose the raw Kubo API or gateway API. Public uploads must go through `/api/upload`.

## Configuration

- `ARKCLOUD_BASE_URL`: optional, defaults to `https://file.arklink.hk`.
- `ARKCLOUD_UPLOAD_TOKEN`: bearer token for `POST /api/upload`.
- `ARKCLOUD_CLIENT_COOKIE`: optional browser/client session cookie for client APIs.
- `ARKCLOUD_CSRF_TOKEN`: optional CSRF token for client upload/delete APIs.

Never print, store, or commit plaintext tokens, session cookies, admin tokens, wallet private keys, seed phrases, or `.env` files. If the user asks to upload secrets, warn them and ask for confirmation before proceeding.

## Upload A File

Use the bearer-token upload helper for normal file uploads:

```bash
python <base_dir>/scripts/arkcloud_upload.py /path/to/file
```

The helper posts to `POST /api/upload` with `Authorization: Bearer <ARKCLOUD_UPLOAD_TOKEN>` and returns JSON containing:

- `cid`
- `bytes`
- `credits_charged`
- `credits_remaining`
- `filename`
- `duplicate`
- `short_url`
- `url`

If `duplicate` is true, ARKCloud returned an existing upload record and charged `0` credits.

After a successful upload, show the user these fields in this order:

- CID: use `cid`
- 文件名: use `filename`
- 大小: use `bytes`
- 链接: use `url`
- 消耗积分: use `credits_charged`
- 剩余积分: use `credits_remaining`

Prompt the user to open the link when they want to view or share the uploaded file. In user-facing copy, call it the access link, file link, or simply 链接.

## Upload A Folder

Folder upload requires a logged-in client session because it uses `POST /api/client/upload/folder` with CSRF protection.

```bash
python <base_dir>/scripts/arkcloud_upload.py /path/to/folder --folder
```

If `ARKCLOUD_CLIENT_COOKIE` or `ARKCLOUD_CSRF_TOKEN` is missing, tell the user to upload the folder from `https://file.arklink.hk/` or provide a valid client session and CSRF token. Do not attempt to bypass this through raw IPFS endpoints.

## List Uploads

Listing uploads requires a logged-in client session:

```bash
python <base_dir>/scripts/arkcloud_list.py
```

It calls `GET /api/client/uploads` and prints the upload records as JSON.

## Check Health

Use the health helper before retrying an upload when the service may be unavailable:

```bash
python <base_dir>/scripts/arkcloud_health.py
```

It calls `GET /api/health` and prints the service response as JSON.

## Delete Or Unpublish Uploads

Deleting uploads requires a logged-in client session and CSRF token:

```bash
python <base_dir>/scripts/arkcloud_delete.py <upload_id>
```

It calls `DELETE /api/client/uploads/{upload_id}`. Treat this as destructive: confirm with the user before deleting unless they explicitly asked for deletion.

## Error Handling

- Missing `ARKCLOUD_UPLOAD_TOKEN`: ask the user to configure a token from the ARKCloud wallet/client UI.
- `401` or `403`: token/session is missing, expired, inactive, or lacks CSRF.
- Insufficient credits: report `credits_required` and `credits_balance` if present.
- File too large or invalid path: report the path and avoid retrying unchanged.
- Service unavailable: check `GET /api/health` or ask whether to retry later.

## Publishing

This skill is installable from GitHub when the repo keeps this path:

```text
skills/arkcloud-ipfs/SKILL.md
```

Install examples:

```text
/skill install djanngau/arkcloud-ipfs-skill#skills/arkcloud-ipfs
cow skill install djanngau/arkcloud-ipfs-skill#skills/arkcloud-ipfs
```
