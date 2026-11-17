# Blogizi CLI — command line guide

This guide walks through everyday use of the `blogizi` binary. For API details and development, see the [README](../README.md). For a file index of samples, see [EXAMPLES.md](./EXAMPLES.md).

## 1. Install

```sh
npm install -g blogizi
blogizi --version
blogizi --help
```

Requires **Node.js 20+**.

## 2. Authenticate

1. Open https://blogizi.com → **Dashboard → Account → API**
2. Copy your **account** API key
3. Run (do this in your own terminal — do not paste keys into chat logs):

```sh
blogizi auth YOUR_ACCOUNT_API_KEY
```

Config is stored at `~/.blogizi/config.json`.

### Multiple projects

```sh
blogizi use your-project-slug
# or combine:
blogizi auth YOUR_ACCOUNT_API_KEY --project your-project-slug
```

With a single project, the API picks it automatically.

## 3. Write a markdown post

Create a `.md` file with YAML frontmatter:

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

Your markdown body goes here. Do not repeat the title as an H1.
```

A ready-made example: [sample-post.md](./sample-post.md).

## 4. Save as draft

```sh
blogizi draft path/to/my-post.md
```

- Forces `status: draft` regardless of frontmatter
- Creates a new post on Blogizi (same slug already existing → conflict — use `update`)
- Prints a dashboard link to edit the draft

## 5. Update an existing post

```sh
blogizi update path/to/my-post.md
```

- Matches by `slug` and updates the existing post (`upsert: true`)
- Keeps current draft/published status unless the file sets `status` explicitly
- If no post exists for that slug, creates one

## 6. Publish live

Only when you intend the post to be public:

```sh
blogizi publish path/to/my-post.md
```

- Forces `status: published`
- Prints the public URL: `https://{projectSlug}.app.blogizi.com/{postSlug}`

## 7. Switch projects

```sh
blogizi use another-project-slug
```

Confirm the active slug in `~/.blogizi/config.json` if the wrong blog updates.

## Command cheat sheet

| Command | Effect |
| --- | --- |
| `blogizi auth <key> [--project <slug>]` | Save API key (and optional project) |
| `blogizi use <slug>` | Set active project |
| `blogizi draft <file>` | Push `.md` as **draft** (create) |
| `blogizi update <file>` | **Update** existing post by slug |
| `blogizi publish <file>` | Push `.md` as **published** (create) |

## Common workflows

### Human or AI agent wrote the file

```sh
blogizi draft ./posts/my-post.md      # review in dashboard
blogizi update ./posts/my-post.md     # after edits, same slug
blogizi publish ./posts/my-post.md    # go live when ready
```

### Scripted smoke test

```sh
./examples/basic-usage.sh
# PUBLISH=1 ./examples/basic-usage.sh   # also publish (careful)
```

### HTTP instead of CLI

See [list-projects.js](./list-projects.js) and [create-post.js](./create-post.js). Prefer the CLI for day-to-day publishing.

## Troubleshooting

| Problem | What to try |
| --- | --- |
| `Not authenticated` | `blogizi auth <key>` |
| Wrong blog / project errors | `blogizi use <slug>` |
| Duplicate slug / conflict | Change `slug` in frontmatter, or edit the existing post in the dashboard |
| Command not found | `npm install -g blogizi` and ensure Node 20+ |

## Related

- [EXAMPLES.md](./EXAMPLES.md) — sample file index
- [README.md](../README.md) — primary docs + public API
- [SKILL.md](../SKILL.md) — guidance for AI coding agents
- Site docs: https://blogizi.com/docs/cli-publishing
