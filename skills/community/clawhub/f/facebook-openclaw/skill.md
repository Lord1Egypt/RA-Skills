# Facebook Advanced Skill

A comprehensive CLI tool for managing Facebook Pages and posts via the Graph API.

## Installation

This skill is installed as an npm package. After cloning or installing:

```bash
# Set your Facebook Page Access Token
$env:FB_PAGE_ACCESS_TOKEN = "your_page_access_token_here"

# Make the script executable (if needed)
# On Windows, PowerShell scripts may need execution policy adjustment
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Setup

1. **Get a Page Access Token:**
   - Go to [Facebook Developers](https://developers.facebook.com/)
   - Create an app or use an existing one
   - Use Graph API Explorer to generate a token with `pages_manage_posts`, `pages_read_engagement`, and `pages_show_list` permissions
   - Or use your existing Page Access Token

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

**Set the environment variable:**
   ```powershell
   $env:FB_PAGE_ACCESS_TOKEN = "your_token_here"
   ```

## Usage

### Main CLI
```powershell
facebook-advanced
```

### Available Commands

#### List Posts
```powershell
facebook-advanced fb-post-list <page_id> [--fields fields] [--limit N]
```
- `--fields`: Comma-separated list of fields (default: message,created_time,id,permalink_url,full_picture,likes.summary(true),comments.summary(true))
- `--limit`: Number of posts to retrieve (default: 25)

#### Create Post
```powershell
facebook-advanced fb-post-create <page_id> --message "Your message" [--link "https://example.com"]
```

#### Read Post
```powershell
facebook-advanced fb-post-read <post_id>
```

#### Hide Post
```powershell
facebook-advanced fb-post-hide <post_id>
```
Note: Hiding is recommended over deletion as it's reversible.

#### Delete Post
```powershell
facebook-advanced fb-post-delete <post_id> [--force]
```
Warning: This permanently deletes the post. Use `--force` to skip confirmation.

#### List Comments
```powershell
facebook-advanced fb-comment-list <post_id> [--limit N]
```

#### Create Comment
```powershell
facebook-advanced fb-comment-create <post_id> --message "Your comment"
```

#### Delete Comment
```powershell
facebook-advanced fb-comment-delete <comment_id> [--force]
```

#### Page Info
```powershell
facebook-advanced fb-page-info <page_id>
```

## Examples

```powershell
# Set token
$env:FB_PAGE_ACCESS_TOKEN = "EAABwzLixnjYBO..."

# List recent posts
facebook-advanced fb-post-list 123456789 --limit 10

# Create a new post
facebook-advanced fb-post-create 123456789 --message "Hello from OpenClaw!"

# Create a post with a link
facebook-advanced fb-post-create 123456789 --message "Check this out!" --link "https://example.com"

# Read a specific post
facebook-advanced fb-post-read 123456789_987654321

# Hide a post
facebook-advanced fb-post-hide 123456789_987654321

# List comments on a post
facebook-advanced fb-comment-list 123456789_987654321 --limit 50

# Reply to a post
facebook-advanced fb-comment-create 123456789_987654321 --message "Thanks for the feedback!"

# Get page information
facebook-advanced fb-page-info 123456789
```

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
```powershell
```
openclaw cron add \
  --name "Job Name" \
  --cron "cron expression" \
  --tz "America/New_York" \     # US timezone (Eastern Time)
  --session isolated \          # Recommended to use isolated to avoid polluting main context
  --message "facebook-advanced fb-post-list 123456789 --limit 10" \
  --announce  

# CLI 
```powershell
```
openclaw cron add --name "Reminder" --at "2m" --session main --system-event "Reminder: Review documents" --wake now --delete-after-run

openclaw cron add --name "Morning Briefing" --cron "0 9 * * *" --tz "America/New_York" --session isolated --message "facebook-advanced fb-post-list 123456789 --limit 10" --deliver

- `FB_PAGE_ACCESS_TOKEN`: Required. Your Facebook Page Access Token with appropriate permissions.

## Environment Variables

- `FB_PAGE_ACCESS_TOKEN`: Required. Your Facebook Page Access Token with appropriate permissions.

## Permissions Required

- `pages_manage_posts`: Create, edit, hide, delete posts
- `pages_read_engagement`: Read posts and comments
- `pages_show_list`: Access page information

## Security Notes

- Never commit your access token to version control
- Use environment variables or a secure secrets manager
- Tokens may expire; regenerate as needed
- Use the principle of least privilege for token permissions

## Troubleshooting

### "Invalid Access Token"
- Token may have expired
- Check that the token has the required permissions
- Regenerate the token from Graph API Explorer

### "Permission Denied"
- Ensure your token has the required permissions
- Verify you're an admin/editor of the page

### "Page Not Found"
- Verify the page ID is correct
- Ensure your token has access to that page

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

## API Reference

- [Facebook Graph API Documentation](https://developers.facebook.com/docs/graph-api)
- [Pages API](https://developers.facebook.com/docs/graph-api/reference/page)
- [Posts API](https://developers.facebook.com/docs/graph-api/reference/page/posts)
- [Comments API](https://developers.facebook.com/docs/graph-api/reference/post/comments)
