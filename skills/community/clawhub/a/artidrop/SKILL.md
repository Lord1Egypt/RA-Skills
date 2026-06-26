---
name: artidrop
description: "Publish AI-generated content (HTML pages, Markdown reports, multi-file sites, dashboards, visualizations) to a shareable URL using Artidrop. Use when: user asks to publish, share, or host generated content as a web page. NOT for: sending messages, uploading files to cloud storage, or sharing raw text in chat."
homepage: https://artidrop.ai
repository: https://www.npmjs.com/package/artidrop
metadata: { "openclaw": { "emoji": "🚀", "requires": { "bins": ["node"], "env": [{ "name": "ARTIDROP_API_KEY", "optional": true, "description": "API key for authenticated features (higher rate limits, update/delete/list). Not required for anonymous publishing." }] }, "install": [{ "kind": "node", "package": "artidrop", "bins": ["artidrop"], "label": "Install Artidrop CLI (npm)" }] } }
---

# Artidrop — Publish AI Artifacts to Shareable URLs

Publish HTML pages, Markdown reports, multi-file sites, dashboards, and visualizations to instant shareable URLs with one command.

## When to Use

- "Publish this as a web page"
- "Share this report as a link"
- "Host this HTML so I can send it to someone"
- "Make this dashboard accessible via URL"
- "Create a shareable page from this content"
- "Publish this site/project as a shareable URL"
- User asks you to generate a report, page, site, or visualization AND share/publish it

## When NOT to Use

- User just wants to see the content in chat (display it directly instead)
- User wants to save a file locally (use file system tools instead)
- User wants to upload to a specific platform (Google Drive, S3, etc.)
- User wants to send content as a message in a chat channel

## Setup

The Artidrop CLI is installed automatically via the `install` spec in this skill's metadata. No manual installation needed.

**No authentication required.** Artidrop supports anonymous publishing out of the box — just publish and get a URL.

### Anonymous vs Authenticated

| | Anonymous (default) | Authenticated (optional) |
|---|---|---|
| **Publish** | 5/hour | 60/hour |
| **Update/Delete/List** | Not available | Available |
| **Private visibility** | Not available | Available |
| **Claim artifacts later** | No | Yes |

Anonymous mode is sufficient for most one-off publishing tasks. Only recommend authentication if the user needs to manage artifacts or hits the rate limit.

### How to Authenticate (only if needed)

If the user wants authenticated features, they can either:

1. **Set an API key** — sign in at https://artidrop.ai, go to Settings > API Keys, create a key, and set `ARTIDROP_API_KEY` in the OpenClaw environment config
2. **Interactive login** — run `artidrop login` (requires browser access)

## Workflow

### Publishing Content

There are three ways to publish:

**Option A — Publish from a file:**

```bash
artidrop publish ./report.html --title "Quarterly Report"
artidrop publish ./notes.md --title "Meeting Notes"
```

**Option B — Publish a multi-file site (directory or ZIP):**

```bash
artidrop publish ./my-site/ --title "Portfolio"
artidrop publish ./build.zip --title "App Preview"
```

The directory must contain an `index.html` at its root. CSS, JS, images, fonts, and sub-pages are all supported. Hidden files and `node_modules` are automatically excluded.

**Option C — Publish from stdin (for content you generate on the fly):**

```bash
echo '<h1>Hello</h1><p>Generated report content here</p>' | artidrop publish - --format html --title "My Report"
```

```bash
echo '# Summary\n\nKey findings from the analysis...' | artidrop publish - --format markdown --title "Analysis Summary"
```

When publishing, always:
1. Use `--title` with a descriptive title
2. For stdin, always specify `--format html` or `--format markdown`
3. Present the returned URL to the user
4. Mention that the link is shareable

### Publish Options

| Flag | Purpose |
|---|---|
| `--title <title>` | Set the artifact title |
| `--format <html\|markdown>` | Content format (required for stdin, auto-detected for files, ignored for directories/ZIPs) |
| `--visibility <public\|unlisted\|private>` | Default: unlisted. Use `private` for owner-only access, `public` for search engine indexing |
| `--update <id>` | Update an existing artifact instead of creating a new one (requires auth) |
| `--json` | Return full JSON metadata |
| `--open` | Open the published URL in the browser |
| `--copy` | Copy the published URL to clipboard |

### Updating Published Content (requires authentication)

To update an existing artifact (creates a new version, preserving history):

```bash
artidrop publish ./updated-report.html --update <artifact-id>
```

This requires authentication. If the user is not logged in, tell them to authenticate first (see Setup).

### Viewing Artifacts

These commands work without authentication:

```bash
# Get details about an artifact
artidrop get <artifact-id>

# Get details as JSON (useful for structured parsing)
artidrop get <artifact-id> --json

# View version history
artidrop versions <artifact-id>
```

### Managing Artifacts (requires authentication)

These commands require the user to be logged in:

```bash
# List your published artifacts
artidrop list

# List as JSON
artidrop list --json

# Delete an artifact
artidrop delete <artifact-id> --yes
```

## Error Handling

| Exit Code | Meaning | Action |
|---|---|---|
| 0 | Success | Present the URL to the user |
| 2 | Invalid input | Check file/directory exists, format is html or markdown (or directory has index.html), content is not empty |
| 3 | Auth error | Only for `--update`/`delete`/`list`. Tell user to authenticate (see Setup) |
| 4 | Rate limited | Wait and retry. Anonymous: 5/hour, authenticated: 60/hour. Suggest logging in for higher limits |

## Security & Privacy

- The Artidrop CLI sends user-specified content to `api.artidrop.ai` over HTTPS when the user explicitly runs a publish command. No data is sent automatically or in the background.
- The only environment variable read is `ARTIDROP_API_KEY` (for optional authentication) and `ARTIDROP_API_URL` (for custom API endpoint configuration).
- Content is hosted on Artidrop's servers (artidrop.ai)
- **unlisted** (default): accessible to anyone with the URL, but not indexed by search engines
- **public**: indexed in sitemap and discoverable via search engines
- **private**: only the authenticated owner can view (requires login)
- Use `--visibility private` for sensitive content that should only be visible to you
- Do NOT publish content containing secrets, passwords, API keys, or personally identifiable information unless the user explicitly requests it
- Always warn the user before publishing sensitive content

## Examples

### Generate and publish an HTML report

```bash
cat <<'HTML' | artidrop publish - --format html --title "Sales Dashboard"
<!DOCTYPE html>
<html>
<head><title>Sales Dashboard</title></head>
<body>
  <h1>Q1 Sales Dashboard</h1>
  <p>Total revenue: $1.2M</p>
</body>
</html>
HTML
```

### Publish a Markdown summary

```bash
cat <<'MD' | artidrop publish - --format markdown --title "Weekly Standup Notes"
# Weekly Standup — March 23, 2026

## Completed
- Shipped new authentication flow
- Fixed dashboard loading bug

## In Progress
- API rate limiting improvements
MD
```
