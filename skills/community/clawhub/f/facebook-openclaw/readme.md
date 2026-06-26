# Facebook Advanced (fboc)

A CLI tool for managing Facebook Pages and posts via the Graph API.

## Quick Start

### 1. Configure your access token

**Option A: Using facebook-config.json (Recommended)**

Edit `facebook-config.json` in this directory:
```json
{
  "FB_PAGE_ACCESS_TOKEN": "FB_PAGE_ACCESS_TOKEN",
  "FB_APP_ID": "(OPTIONAL) YOUR_APP_ID_HERE",
  "FB_APP_SECRET": "(OPTIONAL) YOUR_APP_SECRET_HERE",
  "description": "Replace the placeholder values with your actual Facebook credentials. Never commit this file with real secrets to version control."
}
```

**Option B: Using environment variable**

```powershell
$env:FB_PAGE_ACCESS_TOKEN = "your_page_access_token_here"
```

For permanent storage with environment variable, add to your PowerShell profile:

```powershell
# Edit your profile
notepad $PROFILE

# Add this line:
$env:FB_PAGE_ACCESS_TOKEN = "your_page_access_token_here"
```

### 2. Get a Page Access Token

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create an app or use existing
3. Use Graph API Explorer to generate token with:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`

### 3. Run the CLI

```powershell
facebook-advanced --help
```

## Commands

### List Posts

```powershell
facebook-advanced fb-post-list <page_id> [--limit 25] [--fields fields]
```

Example:
```powershell
facebook-advanced fb-post-list 123456789 --limit 10
```

### Create Post

```powershell
facebook-advanced fb-post-create <page_id> --message "Your message" [--link "https://example.com"]
```

Example:
```powershell
facebook-advanced fb-post-create 123456789 --message "Hello Facebook!" --link "https://example.com"
```

### List Comments

```powershell
facebook-advanced fb-comment-list <post_id> [--limit 25]
```

### Create Comment

```powershell
facebook-advanced fb-comment-create <post_id> --message "Your comment"
```

## Options

- `--message` - Post/comment text content
- `--link` - URL to share with post
- `--picture` - Image file path for post
- `--limit` - Number of items (default: 25)
- `--fields` - Comma-separated fields to retrieve
- `--help` - Show help message

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FB_PAGE_ACCESS_TOKEN` | Yes | Your Facebook Page Access Token |
| `FB_APP_ID` | No | Your Facebook App ID |
| `FB_APP_SECRET` | No | Your Facebook App Secret |

## Cron Jobs (openclaw)
```cron
# Cron Jobs UI
- New Job
`Assistant task prompt *` 
Example:
```
facebook-advanced fb-post-list 123456789 --limit 10
```
- Add job

# Terminal

openclaw cron add \
  --name "Job Name" \
  --cron "cron expression" \
  --tz "America/New_York" \     # US timezone (Eastern Time)
  --session isolated \          # Recommended to use isolated to avoid polluting main context
  --message "facebook-advanced fb-post-list 123456789 --limit 10" \
  --announce                    # (optional) Send notification after completion

# CLI 
```powershell
```
openclaw cron add --name "Reminder" --at "2m" --session main --system-event "Reminder: Review documents" --wake now --delete-after-run

openclaw cron add --name "Morning Briefing" --cron "0 9 * * *" --tz "America/New_York" --session isolated --message "facebook-advanced fb-post-list 123456789 --limit 10" --deliver

## Troubleshooting

### "facebook-advanced: command not found"

Make sure the package is properly installed and in your PATH:

```powershell
# Check installation
npm list facebook-advanced -g

# Reinstall if needed
npm install -g facebook-advanced
```

### "FB_PAGE_ACCESS_TOKEN not set"

Set the environment variable:

```powershell
$env:FB_PAGE_ACCESS_TOKEN = "your_token_here"
```

### bin
# Create setup.ps1 in fboc directory (folder C:\Users\OS\.openclaw\workspace\skills\fboc\bin)
# Setup script for facebook-advanced CLI on Windows
# Make the bin file executable

```powershell
$binPath = Join-Path $PSScriptRoot "facebook-advanced"

# Ensure the file exists
if (Test-Path $binPath) {
    # On Windows, we don't need to chmod, but we can verify the file is readable
    Write-Host "facebook-advanced CLI is ready."
} else {
    Write-Error "facebook-advanced binary not found at $binPath"
    exit 1
}
```

### Token expired

Facebook tokens expire. Generate a new one from Graph API Explorer or extend it using the Graph API.

### Function error

PS C:\Users\OS\.openclaw\workspace\skills\fboc> facebook-advanced --help
node:internal/modules/cjs/loader:1368
  throw err;
  ^

Error: Cannot find module 'commander'
Require stack:
- C:\Users\OS\.openclaw\workspace\skills\fboc\bin\facebook-advanced
    at Function._resolveFilename (node:internal/modules/cjs/loader:1365:15)
    at defaultResolveImpl (node:internal/modules/cjs/loader:1021:19)
    at resolveForCJSWithHooks (node:internal/modules/cjs/loader:1026:22)
    at Function._load (node:internal/modules/cjs/loader:1175:37)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Module.require (node:internal/modules/cjs/loader:1445:12)
    at require (node:internal/modules/helpers:135:16)
    at Object.<anonymous> (C:\Users\OS\.openclaw\workspace\skills\fboc\bin\facebook-advanced:3:21)
    at Module._compile (node:internal/modules/cjs/loader:1688:14) {
  code: 'MODULE_NOT_FOUND',
  requireStack: [
    'C:\\Users\\OS\\.openclaw\\workspace\\skills\\fboc\\bin\\facebook-advanced'
  ]
}

=> throw them into openclaw chat, the errors will be fixed automatically

## Related to the other files

- `exec-approvals.json`: Approval list for executing commands
- `allowlist.json`: Permission list for executing fb commands
- `facebook-config.json`: Access page information
- `setup.ps1`: Setup script for facebook-advanced CLI on Windows

## License

MIT
