# Facebook Page Access Token Setup

## Prerequisites

- A Facebook Page you manage
- A Meta Developer account at https://developers.facebook.com
- A Meta App (Development mode is fine for testing)

## Step 1: Get your App Secret

1. Go to https://developers.facebook.com/apps/
2. Select your app (or create one with type **Business**)
3. Go to **Settings > Basic**
4. Copy the **App Secret** — this is your `META_APP_SECRET`

## Step 2: Generate a Page Access Token

### Get a short-lived token

1. Open https://developers.facebook.com/tools/explorer/
2. Select your app
3. Click **Generate Access Token**
4. Grant permissions: `pages_manage_posts`, `pages_read_engagement`, `pages_show_list`
5. Select your Page from the **Page Access Token** dropdown
6. Copy the token (valid ~1 hour)

### Convert to long-lived token

Exchange the short-lived token:

```
GET https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={SHORT_LIVED_TOKEN}
```

This returns a long-lived **user** token. Now get the **page** token:

```
GET https://graph.facebook.com/v21.0/me/accounts?access_token={LONG_LIVED_USER_TOKEN}
```

Find your Page in the response. Its `access_token` is a long-lived Page token that does not expire under normal conditions. Its `id` is your `META_PAGE_ID`.

## Step 3: Set environment variables

Add to your shell profile or OpenClaw config:

```bash
export LONG_META_page_TOKEN="EAAxxxxxxx..."
export META_PAGE_ID="123456789012345"
export META_APP_SECRET="abcdef1234567890"
```

Or configure in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "fb-page-poster": {
        "enabled": true,
        "env": {
          "LONG_META_page_TOKEN": "EAAxxxxxxx...",
          "META_PAGE_ID": "123456789012345",
          "META_APP_SECRET": "abcdef1234567890"
        }
      }
    }
  }
}
```

## Token renewal

Long-lived Page tokens are invalidated when:
- User changes Facebook password
- User de-authorizes the app
- App permissions are revoked

If the token stops working, repeat Steps 2-3.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Invalid OAuth access token | Re-generate token (Steps 2-3) |
| Requires pages_manage_posts | Re-authorize with correct permissions |
| Application does not have permission | Add yourself as tester in App Settings or switch to Live mode |
| Empty /me/accounts response | Re-authorize with `pages_show_list` |
