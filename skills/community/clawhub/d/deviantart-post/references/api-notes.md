# DeviantArt API notes

## Auth

- Authorization endpoint: `https://www.deviantart.com/oauth2/authorize`
- Token endpoint: `https://www.deviantart.com/oauth2/token`
- Revoke endpoint: `https://www.deviantart.com/oauth2/revoke`
- New apps use OAuth 2.1 with PKCE (`S256`).
- Redirect URIs must match exactly.

## Token lifetimes

- Access token: about 1 hour
- Refresh token: about 3 months

## Posting workflow

1. `POST /api/v1/oauth2/stash/submit`
2. `POST /api/v1/oauth2/stash/publish`

## Required scopes

### Artwork posting
- `stash`
- `publish`

### Journal and status posting
- journals require `user.manage`
- statuses may require `user.manage`
- if journal/status posting fails with scope errors, add `user.manage` to the app scopes and re-authorize

## Submit endpoint details

- multipart/form-data upload
- accepts many file formats
- may return an error payload with HTTP 200 for large uploads
- response should include `status` and `itemid`

## Publish endpoint details

Common parameters:
- `itemid`
- `is_mature`
- `mature_level` when mature
- `allow_comments`
- `allow_free_download`
- `display_resolution`
- `add_watermark`
- `tags`
- `is_ai_generated`
- `noai`

Common response:
- `status`
- `url`
- `deviationid`

## Common failures

- submission policy / ToS acceptance required
- invalid license configuration
- invalid display resolution
- deviation already published
- preview image required

## Safe operating pattern

- authenticate once
- refresh automatically
- summarize the pending post before calling publish
- use dry-run mode when checking metadata or gallery selection
- start with one small JPG/PNG test upload
