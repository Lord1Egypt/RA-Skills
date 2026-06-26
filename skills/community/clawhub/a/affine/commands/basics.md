# Basic Commands

Auth, workspace, and document operations.

---

## Auth Module

### login

Login with your Affine account.

```bash
affine-cli auth login [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --url | -u | No | Server URL. Default: `https://app.affine.pro` |
| --token | -t | No | API token. If not provided, interactive login |
| --workspace | -w | No | Workspace ID to use as default |
| --local | - | No | Save to local `.env` instead of global config |
| --force | -f | No | Overwrite existing config without prompts |

**Examples:**
```bash
# Login to cloud
affine-cli auth login --token your_api_token

# Login to self-hosted instance
affine-cli auth login --url https://affine.yourcompany.com --token your_token

# Save to local project
affine-cli auth login --token your_token --local
```

### logout

Remove saved credentials.

```bash
affine-cli auth logout [--local]
```

| Option | Required | Description |
|--------|----------|-------------|
| --local | No | Remove local `.env` instead of global config |

### status

Check current login status.

```bash
affine-cli auth status [--json]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --json | -j | No | Output as JSON format |

---

## Workspace Module

### list

List all accessible workspaces.

```bash
affine-cli workspace list [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --format | -f | No | Output format: `text` (default) or `json` |

---

## Document Module

### list

List documents in workspace.

```bash
affine-cli doc list [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --workspace | -w | No | Workspace ID. Uses config default if not specified |
| --count | -c | No | Number of results to return (default: 20) |
| --tag | -t | No | Filter by tag name |

### all

List all documents including deleted ones.

```bash
affine-cli doc all [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --workspace | -w | No | Workspace ID |
| --count | -c | No | Page size (default: 50) |
| --skip | -s | No | Number of documents to skip |
| --after | -a | No | Cursor for pagination |

### info

Get document details.

```bash
affine-cli doc info [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Document ID |
| --workspace | -w | No | Workspace ID |
| --content | -c | No | Content output mode: `markdown` (default), `raw`, or `hidden` |

### create

Create a new document.

```bash
affine-cli doc create [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --title | -t | **Yes** | Document title |
| --content | -c | No | Markdown content. Prefix `@` for file path (e.g., `@readme.md`) |
| --folder | -f | No | Parent folder ID |
| --tags | - | No | Comma-separated tags (e.g., `work,important`) |
| --icon | -i | No | Emoji icon (e.g., `📝`, `📁`, `💡`) |
| --workspace | -w | No | Workspace ID |

**Examples:**
```bash
# Simple document
affine-cli doc create -t "My Note" -c "# Hello\n\nThis is content"

# From file
affine-cli doc create -t "Meeting Notes" -c "@meeting.md"

# With tags and icon
affine-cli doc create -t "Project Alpha" --tags "work,project" --icon "📁"
```

### search

Search documents by keyword.

```bash
affine-cli doc search [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --query | -q | **Yes** | Search keyword |
| --workspace | -w | No | Workspace ID |
| --count | -c | No | Number of results (default: 20) |
| --match-mode | -m | No | Match mode: `substring` (default), `prefix`, `suffix`, `exact` |
| --tag | -t | No | Filter by tag name |

### delete

Delete a document.

```bash
affine-cli doc delete [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Document ID |
| --workspace | -w | No | Workspace ID |

### copy

Copy a document.

```bash
affine-cli doc copy [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Source document ID |
| --title | -t | No | New document title. Uses source title if not specified |
| --parent | -p | No | Parent document ID (to create as child) |
| --folder | -f | No | Target folder ID |
| --workspace | -w | No | Workspace ID |

### update

Update document properties.

```bash
affine-cli doc update [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Document ID |
| --title | -t | No | New title |
| --parent | -p | No | New parent document ID. Use empty to remove |
| --folder | -f | No | Target folder ID |
| --icon | -i | No | New emoji icon |
| --workspace | -w | No | Workspace ID |

### replace

Replace text in document content.

```bash
affine-cli doc replace [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Document ID |
| --search | -s | **Yes** | Text to find |
| --replace | -r | **Yes** | Replacement text |
| --workspace | -w | No | Workspace ID |
| --match-all | -a | No | Replace all occurrences (default: true) |
| --preview | -p | No | Show result without applying changes |

### append

Append content to document.

```bash
affine-cli doc append [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Document ID |
| --content | -c | **Yes** | Content to append. Prefix `@` for file path |
| --workspace | -w | No | Workspace ID |

### publish

Publish document for public access.

```bash
affine-cli doc publish [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Document ID |
| --mode | -m | No | Mode: `Page` or `Edgeless` |
| --workspace | -w | No | Workspace ID |

### unpublish

Remove public access from document.

```bash
affine-cli doc unpublish [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Document ID |
| --workspace | -w | No | Workspace ID |