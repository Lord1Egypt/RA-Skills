## Install as a skill

```bash
npx skills add bytemindlab/blogizi-agent
```

---

# Blogizi CLI

Draft and publish markdown posts to your [Blogizi](https://blogizi.com) blog.

This README is the **primary documentation** for the CLI: install, usage, public API reference, and local development. Site docs: [blogizi.com/docs/cli-publishing](https://blogizi.com/docs/cli-publishing).

AI coding agents should write (or edit) the `.md` file themselves, then call `blogizi draft` / `blogizi update` / `blogizi publish`. See [SKILL.md](./SKILL.md).

## Claude Code plugin

This repo is a Claude Code plugin (`blogizi`). Local test:

```sh
claude --plugin-dir .
# then: /blogizi:blogizi
claude plugin validate . --strict
```

Install from this marketplace (before community listing):

```text
/plugin marketplace add bytemindlab/blogizi-agent
/plugin install blogizi@blogizi-agent
```

To submit to Anthropic’s **community** marketplace (`claude-community`), validate locally, then use [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit) (or the Team/Enterprise form on claude.ai). The curated **official** marketplace (`claude-plugins-official`) has no open application process.

## Requirements

- **Node.js 20+**
- A [Blogizi](https://blogizi.com) account and project

## Installation

```sh
npm install -g blogizi
```

From source (see [Development](#development)):

```sh
git clone https://github.com/bytemindlab/blogizi-agent.git
cd blogizi-agent
npm install
npm run build
npm link   # optional: expose `blogizi` globally from this checkout
```

Verify:

```sh
blogizi --version
blogizi --help
```

## Setup

1. Create a project at [blogizi.com](https://blogizi.com).
2. Copy your **account API key** from **Dashboard → Account → API** (also shown under project Settings → API).
3. Authenticate:

```sh
blogizi auth YOUR_ACCOUNT_API_KEY
```

4. If you have **more than one project**, select which blog to publish to:

```sh
blogizi use your-project-slug
# or in one step:
blogizi auth YOUR_ACCOUNT_API_KEY --project your-project-slug
```

With a single project, the API picks it automatically — you can skip `blogizi use`.

Credentials are stored in `~/.blogizi/config.json`:

```json
{
  "apiKey": "…",
  "apiUrl": "https://blogizi.com",
  "projectSlug": "your-project-slug"
}
```

Treat the API key like a password. Never commit it to git or paste it into chat logs.

## Usage

### Draft / update / publish a markdown file

```sh
# Save as draft in the dashboard (not live)
blogizi draft ./posts/go-chi-middleware.md

# Update an existing post by slug (keeps draft/published unless frontmatter sets status)
blogizi update ./posts/go-chi-middleware.md

# Publish live
blogizi publish ./posts/go-chi-middleware.md
```

`draft` forces `status: draft`; `publish` forces `status: published`. `update` sends `upsert: true` and only changes status when the file sets `status` explicitly — otherwise the post keeps its current visibility.

### Project switching

```sh
blogizi use another-project-slug
```

### Command reference

| Command | Description |
| --- | --- |
| `blogizi auth <apiKey> [--project <slug>]` | Save account API key (and optional project) |
| `blogizi use <projectSlug>` | Set active project for draft/update/publish |
| `blogizi draft <file>` | Save a local `.md` file as a **draft** |
| `blogizi update <file>` | **Update** an existing post by slug (`upsert`) |
| `blogizi publish <file>` | Publish a local `.md` file **live** |

### Typical agent workflow

1. Write a markdown file with Blogizi frontmatter (you / your AI agent).
2. `blogizi draft path/to/post.md` → review in the dashboard.
3. Edit and re-push with `blogizi update path/to/post.md` (same slug).
4. When ready: `blogizi publish path/to/post.md`.

## Frontmatter format

Posts are markdown with YAML frontmatter (same shape as [Write in Markdown](https://blogizi.com/docs/markdown-frontmatter)):

```yaml
---
title: "How we built our auth flow"
description: "A short meta description"
keyword: "indie app authentication"
slug: how-we-built-our-auth-flow
status: "draft"
date: "2026-08-07"
readingTime: 0
wordCount: 0
---

Your markdown content here.
```

The CLI recalculates `readingTime` / `wordCount` on parse and strips a duplicate H1 that matches `title` when present.

## Public API reference

Base URL: `https://blogizi.com`

### Authentication

Account-scoped API key (authorizes **all** projects you own):

```http
Authorization: Bearer YOUR_ACCOUNT_API_KEY
```

Optional project selector when you have multiple projects (any one of these):

```http
X-Blogizi-Project: your-project-slug
```

Or in the JSON body: `projectSlug`, `project`, or `projectId`.  
With a **single** project, the server selects it automatically.

Get or regenerate the key in the dashboard (session auth):

```http
GET  /api/account/keys
POST /api/account/keys
```

### Create a post (CLI / integrations)

```http
POST /api/posts
Content-Type: application/json
Authorization: Bearer YOUR_ACCOUNT_API_KEY
X-Blogizi-Project: your-project-slug
```

**Body**

| Field | Type | Notes |
| --- | --- | --- |
| `title` | string | Required |
| `slug` | string | Required; URL path segment |
| `description` | string | Optional meta description |
| `keyword` | string | Optional focus keyword |
| `content` | string | Markdown body (without frontmatter) |
| `frontmatter` | object | Optional; merged metadata |
| `status` | `"draft"` \| `"published"` | Visibility |
| `projectSlug` | string | Optional alternative to the header |
| `upsert` | boolean | If `true`, update an existing post with the same slug instead of failing (`blogizi update` and the [Obsidian plugin](https://blogizi.com/docs/obsidian)) |

**Success response** (simplified):

```json
{
  "data": { "slug": "how-we-built-our-auth-flow", "...": "..." },
  "project": { "id": "…", "slug": "your-project-slug" },
  "created": true
}
```

Public URL pattern: `https://{projectSlug}.app.blogizi.com/{postSlug}`

### List projects

```http
GET /api/account/projects
Authorization: Bearer YOUR_ACCOUNT_API_KEY
```

```json
{
  "data": [
    { "id": "…", "name": "My Blog", "slug": "my-blog" }
  ]
}
```

### Project-scoped posts (API key)

```http
GET  /api/projects/{projectId}/posts
POST /api/projects/{projectId}/posts
Authorization: Bearer YOUR_ACCOUNT_API_KEY
```

`POST` accepts the same create payload as `/api/posts` (project implied by the path).

Update/delete by post id is currently **dashboard session auth only**:

```http
PATCH  /api/projects/{projectId}/posts/{postId}
DELETE /api/projects/{projectId}/posts/{postId}
```

### Public blog endpoints (no auth)

```http
GET  /api/sites/{projectSlug}/posts?page=1&limit=10&tag=optional
GET  /api/sites/{projectSlug}/search?q=query
POST /api/sites/{projectSlug}/analytics
GET  /api/resolve-domain?host=blog.example.com
```

### Example: create a draft with curl

```sh
curl -sS -X POST https://blogizi.com/api/posts \
  -H "Authorization: Bearer $BLOGIZI_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Blogizi-Project: your-project-slug" \
  -d '{
    "title": "Hello from curl",
    "slug": "hello-from-curl",
    "description": "Posted via the public API",
    "keyword": "blogizi api",
    "content": "This post was created with curl.\n",
    "status": "draft"
  }'
```

Machine-oriented overview: [blogizi.com/llms.txt](https://blogizi.com/llms.txt).

## Development

### Clone and install

```sh
git clone https://github.com/bytemindlab/blogizi-agent.git
cd blogizi-agent
npm install
```

### Scripts

| Script | Description |
| --- | --- |
| `npm run build` | Compile TypeScript → `dist/` and mark the bin executable |
| `npm run dev` | Run the CLI via `tsx` without building (`tsx src/index.ts`) |
| `npm start` | Run the compiled `dist/index.js` |

Examples:

```sh
npm run build
node dist/index.js --help

npm run dev -- draft ./posts/example.md
```

## Related

- Examples: [examples/EXAMPLES.md](./examples/EXAMPLES.md) · [examples/COMMAND_LINE_GUIDE.md](./examples/COMMAND_LINE_GUIDE.md)
- AI agent guide: [SKILL.md](./SKILL.md)
- Claude plugin manifest: [`.claude-plugin/plugin.json`](./.claude-plugin/plugin.json)
- Product: [blogizi.com](https://blogizi.com)
- CLI docs: [blogizi.com/docs/cli-publishing](https://blogizi.com/docs/cli-publishing)
- Markdown frontmatter: [blogizi.com/docs/markdown-frontmatter](https://blogizi.com/docs/markdown-frontmatter)
- Obsidian plugin: [blogizi.com/docs/obsidian](https://blogizi.com/docs/obsidian) · [blogizi-obsidian](https://github.com/bytemindlab/blogizi-obsidian)
- LLM / agent brief: [blogizi.com/llms.txt](https://blogizi.com/llms.txt)

## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE) (AGPL-3.0).

Copyright (c) 2026 Blogizi.
