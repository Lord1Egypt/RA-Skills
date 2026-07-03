---
name: blog-composer
description: Jekyll blog authoring UI — manage posts, drafts, tags, and publishing workflow for static sites.
version: 1.0.0
author: TheSolAI
permissions: ["file.read", "file.write", "http.request"]
---

# Blog Composer

A proper authoring UI for Jekyll-based blogs — manages posts, drafts, tags, images, and the full publishing workflow.

## Triggers

Use when the user wants to:
- Browse, create, edit, or publish blog posts
- Manage post tags, categories, or drafts
- Work with a Jekyll or static site blog
- Schedule or schedule a post for later

## Actions

- **Browse posts** — List all posts with status (draft/published), date, tags
- **Create new post** — Scaffold with frontmatter (title, date, tags, layout)
- **Edit post** — Open and modify existing post content or metadata
- **Publish** — Move draft to published, update frontmatter
- **Tag management** — Add/remove tags, see all tags in use
- **Preview** — Show post as rendered markdown

## Configuration

Set the blog root directory in the skill config:
```
blog_root: /path/to/jekyll-site/_posts
```

## Notes

- Assumes standard Jekyll post naming: `YYYY-MM-DD-title.md`
- Frontmatter templates included for common post types (blog, guide, announcement)
