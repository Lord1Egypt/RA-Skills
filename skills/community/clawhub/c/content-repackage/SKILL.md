---
name: content-repackage
description: Convert markdown content into multiple formats instantly. Transform one article into Twitter threads, email digests, and HTML landing pages. Zero dependencies, works offline.
version: 1.0.0
tags:
  - content
  - marketing
  - automation
  - twitter
  - email
  - landing-page
---

# Content Repackage

Convert markdown to Twitter threads, emails, and HTML landing pages in one click.

## Usage

```bash
node content-repackage.js <input.md> [output-dir]
```

## Input
Any markdown file with optional frontmatter.

## Output

### Twitter Thread
- Auto-splits into 280-char tweets
- Preserves sentence boundaries
- Adds thread numbers

### Email Digest
- Clean subject line from title
- Proper formatting

### HTML Landing Page
- Mobile-responsive design
- Dark theme
- No external dependencies

## Use Cases
- Content creators
- Newsletter authors
- Developers documenting projects
- Marketers creating campaign materials
