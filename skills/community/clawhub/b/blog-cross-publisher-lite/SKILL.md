---
name: blog-publisher-lite
description: "Publish markdown articles to Dev.to via their REST API. Use this skill whenever the user wants to publish a blog post or article to Dev.to."
---

# Blog Publisher Lite

Publish markdown articles to **Dev.to** directly from a markdown file using their REST API.

> **Want cross-posting to Medium and Hashnode too?** Upgrade to [Blog Cross-Publisher (Full)](https://apexstack.gumroad.com/l/blog-cross-publisher)

## What You Need

A Dev.to API key. Get one at https://dev.to/settings/extensions

## Article Format

Write your article in standard markdown. The skill extracts the title from the first `# heading`, tags from the `*Tags:*` line, and everything after `---` becomes the body.

## Publishing

```bash
python scripts/publish_devto.py article.md --api-key YOUR_API_KEY --publish
```

| Flag | What It Does |
|------|-------------|
| `--publish` | Publish immediately (omit for draft) |
| `--tags "seo,webdev"` | Override tags from the file |

## API Details

POST https://dev.to/api/articles with api-key header and JSON body. Max 4 tags, lowercase.

## Troubleshooting

- **401**: API key invalid. Generate new one at dev.to/settings/extensions
- **422**: Check title present, tags <= 4, valid body_markdown
- **429**: Rate limited. Wait 30 seconds.

---

*Built by [Apex Stack](https://apexstack.gumroad.com) — tools for developers who ship.*
