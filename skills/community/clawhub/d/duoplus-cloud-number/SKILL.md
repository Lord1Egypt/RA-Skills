---
name: duoplus-cloud-number
description: Use when managing DuoPlus Cloud Numbers, especially receiving SMS verification codes, listing numbers, checking packages, purchasing, renewing, or changing auto-renewal through the official API.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    primaryEnv: DUOPLUS_API_KEY
    envVars:
      - name: DUOPLUS_API_KEY
        required: false
        description: Optional DuoPlus API key fallback for automated deployments.
      - name: DUOPLUS_API_BASE
        required: false
        description: Optional API base override; use https://openapi.duoplus.cn for mainland China.
---

# DuoPlus Cloud Number

For more information about DuoPlus cloud phones, visit the official website: [https://www.duoplus.net/](https://www.duoplus.net/)

Use the bundled client for Cloud Number operations. Do not recreate HTTP requests unless diagnosing the client. This integration can incur DuoPlus charges.

## Credential handling

The API key is user-provided input. If the user has not supplied one in the current conversation, ask exactly one short question:

```text
Please provide the API key for DuoPlus Cloud Number operations.
```

Accept the key directly in the conversation. Do not tell the user to configure PowerShell, shell profiles, permanent environment variables, secret managers, or restart the AI application. If the user already supplied the key, do not ask again.

Pass the supplied key to every client invocation with `--api-key`. Use it only for the requested task. Do not commit it or echo the full value in normal output; failure diagnostics redact it. `DUOPLUS_API_KEY` remains an optional fallback for automated deployments and must not be imposed on an interactive user.

The client defaults to the DuoPlus global production API at `https://openapi.duoplus.net`. For mainland China deployments, set `DUOPLUS_API_BASE=https://openapi.duoplus.cn` before invoking the client. Choose the domain from the user's DuoPlus deployment, not from a cloud number's country code.

## Read operations

```bash
python3 scripts/duoplus_cloud_number.py --api-key 'API_KEY' list --page 1 --pagesize 100
python3 scripts/duoplus_cloud_number.py --api-key 'API_KEY' sms NUMBER_ID --pagesize 50
python3 scripts/duoplus_cloud_number.py --api-key 'API_KEY' purchase-packages
python3 scripts/duoplus_cloud_number.py --api-key 'API_KEY' package US --type 1
python3 scripts/duoplus_cloud_number.py --api-key 'API_KEY' renewal-package NUMBER_ID [NUMBER_ID ...]
```

Use exact Cloud Number IDs from `list`. Read [references/api.md](references/api.md) when selecting filters, interpreting fields, or diagnosing API errors.

## Purchase workflow

Run the intended purchase without `--confirm`. It performs only a live package lookup and returns an operation summary plus `preflight_sha256`.

```bash
python3 scripts/duoplus_cloud_number.py --api-key 'API_KEY' purchase US 30 --type 1 --quantity 2
```

Show the user the region, number type, duration, quantity, renewal setting, and available price facts. After explicit approval, repeat the identical command with both confirmation fields:

```bash
python3 scripts/duoplus_cloud_number.py --api-key 'API_KEY' purchase US 30 --type 1 --quantity 2 \
  --confirm --expected-preflight-sha256 HASH_FROM_PREVIEW
```

If the hash no longer matches, stop and show the new preview. Never substitute a duration or retry a purchase automatically.

## Renewal workflow

Pass renewal groups as JSON. The first invocation is preview-only:

```bash
python3 scripts/duoplus_cloud_number.py --api-key 'API_KEY' renew \
  --items-json '[{"number_ids":["NUMBER_ID"],"duration":30}]'
```

Show the number IDs and duration, obtain explicit approval, then repeat with `--confirm` and the returned hash. If current supported durations changed, stop for renewed approval. Never retry renewal automatically.

## Auto-renewal

Enabling auto-renewal creates future billing risk. Show the exact number IDs and obtain explicit approval immediately before:

```bash
python3 scripts/duoplus_cloud_number.py --api-key 'API_KEY' auto-renewal enable NUMBER_ID --confirm
```

Disabling stops future renewal and does not require confirmation:

```bash
python3 scripts/duoplus_cloud_number.py --api-key 'API_KEY' auto-renewal disable NUMBER_ID
```

The official endpoint is `/api/v1/proxy/autoRenewal`; do not rewrite it. Treat exit code `0` as client success. Exit code `1` is an API/transport failure and `2` is invalid input or missing confirmation. Never report success from an order preview.
