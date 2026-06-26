# GA4 Data API → OpenClaw setup

## Best default path

Use OAuth user authorization first. It is the fastest way to get GA4 data working inside OpenClaw when the user already has a Google account with GA access.

## Preconditions

- A Google account that can log into the target GA4 property
- GA4 Property ID
- Google Analytics Data API enabled in Google Cloud
- Desktop OAuth client JSON

## One-command install

```bash
bash ~/.openclaw/workspace/skills/ga4-data-api/scripts/install_ga4_openclaw.sh <GA4_PROPERTY_ID> <PATH_TO_CLIENT_SECRET_JSON>
```

## First auth

```bash
python3 ~/.openclaw/workspace/skills/ga4-data-api/scripts/ga4_query.py \
  --metrics activeUsers,sessions \
  --dimensions date \
  --start 7daysAgo \
  --end today \
  --pretty
```

## Common pitfalls

1. Wrong Google account in browser → OAuth succeeds, but not for the intended account.
2. Testing-mode OAuth app → add the Gmail account to OAuth test users.
3. Enterprise/internal GA → verify account/permission first; do not jump straight to service account.
4. No visible “add user” button in GA → that is a permission blocker, not a UI misunderstanding.
5. Broad key-event definitions → do not treat all key events as true conversions.
