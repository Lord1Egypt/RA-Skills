---
name: confluence
description: Read and write Confluence pages, search content, manage labels and comments. Use when user mentions Confluence, wiki, documentation, pages, or knowledge base.
metadata:
  openclaw:
    emoji: "📄"
    requires:
      env: ["ATLASSIAN_URL", "ATLASSIAN_EMAIL", "ATLASSIAN_API_TOKEN"]
---

# Confluence Cloud

Read and write Confluence Cloud pages via `confluence-cli.sh`. Uses the same Atlassian credentials as Jira.

Script location: `{baseDir}/confluence-cli.sh`

## Commands

### List spaces

```bash
{baseDir}/confluence-cli.sh spaces
```

Returns: `[{ id, key, name, type, status }]`

Note: most commands use the space `id` (numeric), not the `key`.

### List pages in a space

```bash
{baseDir}/confluence-cli.sh pages 98312
{baseDir}/confluence-cli.sh pages 98312 50
```

Returns: `[{ id, title, status, parentId, authorId, created, url }]`

Default limit: 25.

### Get page content

```bash
{baseDir}/confluence-cli.sh get 12345
```

Returns: `{ id, title, status, spaceId, parentId, version, body_text, body_html, truncated, created, url }`

`body_text` is HTML-stripped plain text (first 3000 chars). `body_html` is raw storage format (first 5000 chars). If `truncated` is true, the page has more content than shown.

### Find page by title

```bash
{baseDir}/confluence-cli.sh get-by-title 98312 "Deployment Runbook"
```

Returns page content directly. Use this when you know the exact page title — avoids a separate search + get.

### List child pages

```bash
{baseDir}/confluence-cli.sh children 12345
```

Returns: `[{ id, title, status, url }]`

### Search with CQL

```bash
{baseDir}/confluence-cli.sh search "space=ENG AND type=page AND title~\"architecture\""
{baseDir}/confluence-cli.sh search "label=runbook" 20
```

Common CQL patterns:
- Pages in a space: `space=ENG AND type=page`
- By title: `title~"deployment guide"`
- By label: `label=runbook`
- Recently modified: `lastModified > now("-7d")`
- By creator: `creator=currentUser() AND type=page`

Returns: `{ total, results: [{ id, title, type, space, url }] }`

### Create page

```bash
{baseDir}/confluence-cli.sh create --space 98312 --title "Deployment Runbook" --parent 12345 --body "<h2>Steps</h2><p>1. Pull latest main...</p>"
```

Required: `--space`, `--title`. Optional: `--parent` (page ID to nest under), `--body` (HTML storage format).

Returns: `{ id, title, url }`

### Update page

```bash
{baseDir}/confluence-cli.sh update 12345 --title "Updated Title" --body "<p>New content</p>"
```

Auto-increments the version number.

Returns: `{ id, title, version, url }`

### Get page comments

```bash
{baseDir}/confluence-cli.sh comments 12345
```

Returns: `{ count, comments: [{ id, body, created, version }] }`

### Add comment to page

```bash
{baseDir}/confluence-cli.sh add-comment 12345 "This section needs updating after the API migration"
```

Returns: `{ id, pageId, created }`

### List attachments

```bash
{baseDir}/confluence-cli.sh attachments 12345
```

Returns: `[{ id, title, mediaType, fileSize, downloadUrl }]`

### Get page labels

```bash
{baseDir}/confluence-cli.sh labels 12345
```

Returns: `[{ name, prefix }]`

### Add labels

```bash
{baseDir}/confluence-cli.sh add-labels 12345 "runbook,production,v2"
```

Labels are comma-separated.

## Exploration Rules

When working with Confluence:

1. **Search first** — use `search` with CQL to find pages. Do not list all pages in a space and scan through them.
2. **Use `get-by-title`** when you know the page name — it's one call instead of search + get.
3. **Check `truncated`** — if a page is truncated, tell the user the content was too long to load fully.
4. **Use `children`** to navigate page hierarchies instead of listing the whole space.
5. **Before creating**, always search to check if a similar page already exists.

## Body Format

Confluence uses HTML "storage format":

- `<p>text</p>` — paragraph
- `<h2>text</h2>` — heading
- `<table><tbody><tr><th>Header</th></tr><tr><td>Cell</td></tr></tbody></table>` — table
- `<strong>text</strong>` — bold
- `<a href="url">text</a>` — link
- `<ac:structured-macro ac:name="jira"><ac:parameter ac:name="key">PROJ-123</ac:parameter></ac:structured-macro>` — Jira link macro

## Rules

- All output is JSON to stdout, errors to both stderr and stdout.
- Never delete pages without explicit user confirmation.
- Always search before creating to avoid duplicates.
- Results are paginated: pages (max 25), spaces (max 25), comments (max 25). Tell the user if results may be incomplete.
