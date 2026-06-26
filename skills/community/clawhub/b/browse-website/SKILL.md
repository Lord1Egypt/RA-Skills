---
name: browse-website
description: Turn any website into a filesystem. Crawls sites automatically and mounts pages as markdown files you can grep, diff, cat, and explore with standard Unix commands — over SSH or HTTP. Use this when you need to read documentation, research a website, track changes across crawls, or search any public webpage.
compatibility: Requires network access to openobj.com (SSH port 22 or HTTPS port 443).
metadata:
  author: bigmind
  version: "1.2.0"
---

# Browse Website

Use OpenObj to access any website's content. Pages are automatically crawled, converted to markdown, and mounted as a virtual filesystem you can explore with standard Unix commands.

## Network Access

All commands in this skill require network access to `openobj.com`.

Use `required_permissions: ["full_network"]` for all SSH and curl commands (they need to reach openobj.com).

## How to Use

**Preferred: SSH exec mode** (works in terminals with network access):

```bash
# required_permissions: ["full_network"]
ssh {domain}@openobj.com "{command}"
```

**Fallback: HTTP API via curl** (works in sandboxed environments):

```bash
# required_permissions: ["full_network"]
curl -s -X POST https://openobj.com/exec \
  -H 'Content-Type: application/json' \
  -d '{"site": "{domain}", "command": "{command}"}'
```

**Important:** If SSH fails due to sandbox restrictions, fall back to the curl HTTP API. Both methods return the same results.

## Available Commands

| Command               | Description                    |
| --------------------- | ------------------------------ |
| `find /site -type f`      | List all indexed pages         |
| `cat {path}`          | Read a page's markdown content |
| `grep -rl '{term}' /site` | Find pages containing a term   |
| `grep -r '{term}' /site`  | Search with matching lines     |
| `ls {path}`           | List files in a directory      |
| `head -n 20 {path}`   | Read first N lines             |
| `wc -l {path}`        | Count lines in a file          |
| `git log --oneline`   | View crawl history             |
| `git diff HEAD~1`     | See what changed in last crawl |
| `git show {hash}`     | View a specific crawl's changes |
| `openobj rediscover`  | Force a fresh re-crawl         |

## Examples

### Via SSH

```bash
# required_permissions: ["full_network"]
ssh docs.stripe.com@openobj.com "find /site -type f"
ssh docs.stripe.com@openobj.com "grep -rl 'webhook' /site"
ssh docs.stripe.com@openobj.com "cat /site/docs/webhooks.md"

# Change tracking
ssh docs.stripe.com@openobj.com "cd /site && git log --oneline"
ssh docs.stripe.com@openobj.com "cd /site && git diff HEAD~1"

# Force re-crawl and see what changed
ssh docs.stripe.com@openobj.com "openobj rediscover && cd /site && git diff HEAD~1"
```

### Via HTTP API (curl)

```bash
# required_permissions: ["full_network"]
# List all pages
curl -s -X POST https://openobj.com/exec \
  -H 'Content-Type: application/json' \
  -d '{"site": "docs.stripe.com", "command": "find /site -type f"}'

# Search for a term
curl -s -X POST https://openobj.com/exec \
  -H 'Content-Type: application/json' \
  -d '{"site": "docs.stripe.com", "command": "grep -rl webhook /site"}'

# Read a page
curl -s -X POST https://openobj.com/exec \
  -H 'Content-Type: application/json' \
  -d '{"site": "docs.stripe.com", "command": "cat /site/docs/webhooks.md"}'
```

## Workflow

1. **Discover** — Run `find /site -type f` to see all available pages
2. **Search** — Use `grep -rl '{keyword}' /site` to find relevant pages
3. **Read** — Use `cat {path}` to read the full content of a page
4. **Refine** — Use `grep -r '{term}' {path}` to search within specific files
5. **Track changes** — Use `git log` and `git diff` to see what changed across crawls
6. **Re-crawl** — Use `openobj rediscover` to force a fresh crawl and update pages

## Behavior

- First access to a domain triggers an automatic crawl (may take 10-30 seconds)
- Subsequent accesses use the cached version (refreshed every 24 hours)
- Use `openobj rediscover` to force a fresh crawl before the 24h window
- Pages are converted from HTML to markdown automatically
- Up to 200 pages per site are indexed
- The virtual filesystem mirrors the site's URL structure
- Each crawl is tracked as a git commit for change diffing

## Credits

- **Crawling** a new site or running `openobj rediscover` costs **1 credit per page**
- **Reading** cached content (`cat`, `grep`, `find`, `ls`, `git`) is **always free**
- Free accounts get **100 one-time credits**
- If you get a credit limit error, **do not retry** — inform the user:
  - To check credits: `ssh {any-domain}@openobj.com "openobj credits"`
  - To upgrade: tell the user to run `ssh auth@openobj.com` in their terminal
- Prefer reading cached sites over re-crawling to conserve credits

## Response Format

The HTTP API returns JSON:

```json
{
  "stdout": "...",
  "stderr": "...",
  "exitCode": 0
}
```

Use the `stdout` field for the command output. A non-zero `exitCode` indicates an error.
