---
name: deviantart-post
description: Post artwork, journals, and status updates to a user's DeviantArt account through the official DeviantArt API using OAuth 2.1 Authorization Code with PKCE, Sta.sh upload, and Sta.sh publish. Use when the user wants to authenticate a local DeviantArt app, upload or publish a local file to DeviantArt, create a DeviantArt journal, or post a DeviantArt status update.
---

# DeviantArt Post

Use the official API, not browser automation.

## Workflow

1. Ensure a local DeviantArt app exists and the user has a `client_id` and redirect URI.
2. Create an app credentials file at `~/.openclaw/deviantart-app-credentials.json`, or override the path with `DEVIANTART_APP_CREDENTIALS`.
3. If no token exists or refresh fails, run `scripts/deviantart_auth.py`.
4. Before any external post, summarize what will be published and get explicit confirmation.
5. Run the relevant script for artwork, journals, or statuses.
6. Return the final URL or deviation ID.

## Local files

Default paths:

- App credentials: `~/.openclaw/deviantart-app-credentials.json`
- Token file: `~/.openclaw/deviantart-token.json`

Optional overrides:

- `DEVIANTART_APP_CREDENTIALS`
- `DEVIANTART_TOKEN_PATH`

Credentials file shape:

```json
{
  "client_id": "12345",
  "redirect_uri": "http://127.0.0.1:8765/callback",
  "scopes": ["stash", "publish"]
}
```

Add `user.manage` when journals or statuses are needed.

## Commands

Authenticate:

```powershell
python .\skills\deviantart-post\scripts\deviantart_auth.py
```

Post artwork:

```powershell
python .\skills\deviantart-post\scripts\deviantart_post_art.py --file "C:\path\to\image.png" --title "My title" --tags tag_one tag_two --artist-comments "Optional description" --is-mature false
```

Or use the PowerShell wrapper:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\deviantart-post\scripts\deviantart_post.ps1 -File "C:\path\to\image.png" -Title "My title" -Tags tag_one,tag_two -IsMature false
```

Create a journal:

```powershell
python .\skills\deviantart-post\scripts\deviantart_post_journal.py --title "My journal" --body "Body text" --is-mature false
```

Or use the PowerShell wrapper:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\deviantart-post\scripts\deviantart_post_journal.ps1 -Title "My journal" -Body "Body text" -IsMature false
```

Post a status:

```powershell
python .\skills\deviantart-post\scripts\deviantart_post_status.py --body "Hello from OpenClaw"
```

Or use the PowerShell wrapper:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\deviantart-post\scripts\deviantart_post_status.ps1 -Body "Hello from OpenClaw"
```

## Notes

- `stash/submit` may return an error body even with HTTP 200. Always inspect the JSON body.
- New DeviantArt apps use PKCE. Keep the auth flow local and desktop-friendly.
- Access tokens expire quickly; refresh automatically before posting.
- Omit empty optional publish fields; DeviantArt validates them aggressively.
- Use `--dry-run` when the user wants a preview before uploading.
- Gallery folder names can be resolved through `--gallery-name`; if multiple folders have the same name, require a UUID instead.
- Ask before publishing because this is an external write action.

## If auth fails

Read `references/api-notes.md` and check:
- redirect URI exact match
- client_id correctness
- local callback port availability
- whether the user needs to re-authorize the app
- whether requested scopes match the action being attempted
