---
name: facebook-page-ronnie
description: Facebook Page publishing and engagement skill for Ronnie's Page operations. Use when the user needs to: (1) publish text posts to a Facebook company Page via Graph API, (2) publish photo posts to a Facebook company Page, (3) test whether Page commenting/reply permissions are working, (4) diagnose Facebook Page token, permission, or app-live-mode issues, or (5) fall back to browser automation when Page comment/reply APIs are blocked.
metadata:
  requires:
    env: ["FACEBOOK_PAGE_ACCESS_TOKEN", "FACEBOOK_PAGE_ID"]
  emoji: "📘"
---

# Facebook Page Ronnie

Use this skill for Ronnie's Facebook Page operations, especially:
- direct Page posting via Graph API
- permission testing after Meta app changes
- diagnosing why posting works but commenting/replying fails
- switching to browser automation when engagement APIs are blocked

## Configuration
Required environment keys:
- `FACEBOOK_PAGE_ID`
- `FACEBOOK_PAGE_ACCESS_TOKEN`
- `FACEBOOK_GRAPH_VERSION` (optional, default `v22.0`)

Meaning of each config item:
- `FACEBOOK_PAGE_ID`: the numeric Facebook Page ID used in Graph API endpoints
- `FACEBOOK_PAGE_ACCESS_TOKEN`: the Page access token used to publish posts and test engagement actions
- `FACEBOOK_GRAPH_VERSION`: optional Graph API version pin, e.g. `v22.0`

Quick check:

```bash
bash "<base_dir>/scripts/check_env.sh"
```

## How to get these two required parameters

### A. Get `FACEBOOK_PAGE_ID`
Choose one of these methods:

1. **From the Facebook Page URL / About area**
   - Open the Page in browser.
   - In some Page views, the Page ID is shown in About / transparency / professional dashboard related areas.
   - Copy the numeric Page ID.

2. **Via Graph API using your Page token**
   Run:

   ```bash
   python3 - <<'PY'
   import os, json, urllib.request, ssl
   token = os.environ['FACEBOOK_PAGE_ACCESS_TOKEN']
   url = f'https://graph.facebook.com/v22.0/me?fields=id,name&access_token={token}'
   ctx = ssl.create_default_context()
   with urllib.request.urlopen(url, context=ctx, timeout=30) as r:
       print(r.read().decode())
   PY
   ```

   Expected result example:

   ```json
   {"id":"123456789012345","name":"Your Page Name"}
   ```

   The `id` value is your `FACEBOOK_PAGE_ID`.

### B. Get `FACEBOOK_PAGE_ACCESS_TOKEN`
Recommended path:

1. Log in to **Meta for Developers** and open your app.
2. Ensure the app has the permissions needed for your workflow, typically:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
   - `pages_manage_engagement`
   - `pages_read_user_content` (recommended for comment-related workflows)
3. Generate a **short-lived User Access Token** for the Facebook account that manages the Page.
4. Exchange it for a **long-lived User Access Token**.
5. Use the long-lived user token to query Page accounts and retrieve the Page access token.

Why this matters:
- if you see a token lifetime like only **1 day**, you are usually looking at a **short-lived User Access Token**, not the final long-usable Page token
- do **not** directly treat a short-lived user token as `FACEBOOK_PAGE_ACCESS_TOKEN`
- the stable workflow is: **short-lived user token → long-lived user token → Page access token**

#### Step B1. Get a short-lived User Access Token
Use Meta Graph API Explorer or your app login flow to obtain a user token for the Facebook account that manages the target Page.

#### Step B2. Exchange short-lived User Token for long-lived User Token
Call:

```bash
python3 - <<'PY'
import os, urllib.request, ssl, urllib.parse
app_id = os.environ['FACEBOOK_APP_ID']
app_secret = os.environ['FACEBOOK_APP_SECRET']
short_token = os.environ['FACEBOOK_USER_ACCESS_TOKEN']
params = urllib.parse.urlencode({
    'grant_type': 'fb_exchange_token',
    'client_id': app_id,
    'client_secret': app_secret,
    'fb_exchange_token': short_token,
})
url = f'https://graph.facebook.com/v22.0/oauth/access_token?{params}'
ctx = ssl.create_default_context()
with urllib.request.urlopen(url, context=ctx, timeout=30) as r:
    print(r.read().decode())
PY
```

Expected result example:

```json
{"access_token":"LONG_LIVED_USER_TOKEN","token_type":"bearer","expires_in":5183944}
```

Important:
- `expires_in` around 5 million seconds is roughly **60 days**
- save this returned token as your long-lived user token
- for this exchange step you need:
  - `FACEBOOK_APP_ID`
  - `FACEBOOK_APP_SECRET`
  - `FACEBOOK_USER_ACCESS_TOKEN` (short-lived user token)

#### Step B3. Use long-lived User Token to fetch the Page token
Run:

```bash
python3 - <<'PY'
import os, json, urllib.request, ssl
user_token = os.environ['FACEBOOK_USER_ACCESS_TOKEN']
url = f'https://graph.facebook.com/v22.0/me/accounts?access_token={user_token}'
ctx = ssl.create_default_context()
with urllib.request.urlopen(url, context=ctx, timeout=30) as r:
    print(r.read().decode())
PY
```

Important:
- for this step, `FACEBOOK_USER_ACCESS_TOKEN` should contain the **long-lived user token**, not the short-lived one

In the returned JSON, find the target Page entry:
- copy its `id` as `FACEBOOK_PAGE_ID`
- copy its `access_token` as `FACEBOOK_PAGE_ACCESS_TOKEN`

#### Step B4. Verify the Page token
Test whether the token can directly read the target Page:

```bash
python3 - <<'PY'
import os, urllib.request, ssl
page_id = os.environ['FACEBOOK_PAGE_ID']
token = os.environ['FACEBOOK_PAGE_ACCESS_TOKEN']
url = f'https://graph.facebook.com/v22.0/{page_id}?fields=id,name&access_token={token}'
ctx = ssl.create_default_context()
with urllib.request.urlopen(url, context=ctx, timeout=30) as r:
    print(r.read().decode())
PY
```

Expected result example:

```json
{"id":"123456789012345","name":"Your Page Name"}
```

Important reminders:
- after adding new permissions, you often need to **re-generate the token**
- if the app is still in **Development mode**, some production behaviors may stay blocked
- the acting Facebook account must actually have the necessary Page role/permissions
- long-lived user tokens are typically around **60 days**, while Page access tokens obtained through them are usually the practical token used for Page posting workflows
- even a long-usable Page token can still stop working if the user changes password, removes app authorization, loses Page role access, or the app mode/permissions change

## Default execution policy

### 1. For Page post publishing
Prefer **Graph API** first.

Use Python request execution if `curl` to `graph.facebook.com` is unstable in the current environment.

### 2. For Page comments / replies
Try **Graph API** first only when the user explicitly wants permission verification or the token is believed to include comment/reply scopes.

If API returns permission errors such as `(#200) You do not have sufficient permissions to perform this action`, explain clearly that:
- Page posting permission is working
- engagement/comment permission is still insufficient or token has not been refreshed
- browser automation is the fallback path

### 3. For browser fallback
Use browser automation when:
- user wants direct operational completion rather than permission diagnosis
- Facebook API comment/reply remains blocked
- the user is willing to log in to Facebook in browser session

## Recommended Python pattern for text Page post

```bash
python3 - <<'PY'
import os, urllib.request, urllib.parse, ssl
page_id = os.environ['FACEBOOK_PAGE_ID']
token = os.environ['FACEBOOK_PAGE_ACCESS_TOKEN']
version = os.environ.get('FACEBOOK_GRAPH_VERSION', 'v22.0')
message = 'Your post text here'
url = f'https://graph.facebook.com/{version}/{page_id}/feed'
data = urllib.parse.urlencode({
    'message': message,
    'access_token': token,
}).encode('utf-8')
req = urllib.request.Request(url, data=data, method='POST')
ctx = ssl.create_default_context()
with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
    print(r.read().decode())
PY
```

Expected success result:

```json
{"id":"PAGEID_POSTID"}
```

## Recommended Python pattern for Page comment test

```bash
python3 - <<'PY'
import os, urllib.request, urllib.parse, ssl
version = os.environ.get('FACEBOOK_GRAPH_VERSION', 'v22.0')
token = os.environ['FACEBOOK_PAGE_ACCESS_TOKEN']
post_id = 'TARGET_POST_ID'
message = 'Test comment from API'
url = f'https://graph.facebook.com/{version}/{post_id}/comments'
data = urllib.parse.urlencode({
    'message': message,
    'access_token': token,
}).encode('utf-8')
req = urllib.request.Request(url, data=data, method='POST')
ctx = ssl.create_default_context()
try:
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        print(r.read().decode())
except urllib.error.HTTPError as e:
    print(e.read().decode())
PY
```

Typical failure observed in Ronnie's setup:

```json
{"error":{"message":"(#200) You do not have sufficient permissions to perform this action"}}
```

## Permission checklist for comment / reply workflows

If the user's goal includes posting, reading comments, leaving comments, and replying to comments, recommend this permission set:

- `pages_show_list`
- `pages_read_engagement`
- `pages_manage_posts`
- `pages_manage_engagement`
- `pages_read_user_content` (recommended)

Also remind the user:
1. App should be in **Live** mode for production behavior.
2. The acting Facebook account should have strong Page role access.
3. After adding permissions, the token often must be **re-generated**.

## Troubleshooting logic

### Case A — reading Page info works, posting works, commenting fails
Conclusion:
- posting path is healthy
- engagement permission layer is still missing or token not refreshed

### Case B — `curl` fails but Python urllib works
Conclusion:
- network/SSL path for curl is unstable
- use Python request pattern as primary execution method

### Case C — user insists on direct comment/reply execution
If API still fails, switch to browser automation and ask user to log in if needed.

## Response style

Be concrete and short:
- say whether you are using API or browser path
- if comment fails, show the exact permission finding
- avoid telling the user to do Graph API Explorer manually unless explicitly needed for debugging
