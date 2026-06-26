---
name: content-publisher
description: Publish content to Medium, Dev.to, and Hashnode from markdown files. Handles formatting, SEO optimization, scheduling, and cross-posting with canonical URLs. Use when asked to publish articles, blog posts, or cross-post content across platforms.
---

# Content Publisher

Publish markdown articles to Medium, Dev.to, and Hashnode. Handles SEO, formatting, and canonical URLs for cross-posting.

## Supported Platforms

| Platform | Method | Auth |
|----------|--------|------|
| Medium | Browser automation | Google login |
| Dev.to | API | API key in env `DEVTO_API_KEY` |
| Hashnode | API | API key in env `HASHNODE_TOKEN` |

## Workflow

### 1. Prepare content
Ensure article has:
- Title (H1)
- Subtitle/description
- Tags (3-5 relevant tags)
- Content body (markdown)
- Optional: cover image URL

### 2. SEO optimization checklist
Before publishing, verify:
- [ ] Title contains target keyword (under 60 chars)
- [ ] Meta description (under 155 chars)
- [ ] H2/H3 structure with keywords
- [ ] Internal/external links
- [ ] Alt text on images
- [ ] Call-to-action at end

### 3. Publish to Medium (browser)
```
1. Navigate to https://medium.com/new-story
2. Paste title and content
3. Click "Publish" → set tags → confirm
```

### 4. Publish to Dev.to (API)
```bash
curl -X POST https://dev.to/api/articles \
  -H "api-key: $DEVTO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "article": {
      "title": "TITLE",
      "body_markdown": "CONTENT",
      "published": true,
      "tags": ["ai", "productivity"],
      "canonical_url": "MEDIUM_URL"
    }
  }'
```

### 5. Publish to Hashnode (GraphQL)
```bash
curl -X POST https://gql.hashnode.com \
  -H "Authorization: $HASHNODE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { publishPost(input: { title: \"TITLE\", contentMarkdown: \"CONTENT\", publicationId: \"PUB_ID\", tags: [{slug: \"ai\"}] }) { post { url } } }"
  }'
```

## Cross-posting strategy

1. **First**: Publish on Medium (or your primary platform)
2. **Wait 24-48h**: Let search engines index the original
3. **Cross-post**: Use `canonical_url` pointing to the original
4. **Why**: Avoids duplicate content penalties in SEO

## Publication submission (Medium)

To get more reach, submit to Publications:
1. Find publication's "Write for us" page
2. Follow their submission guidelines
3. Submit via Medium's story settings → "Add to publication"

### High-traffic AI Publications
- Towards AI (AI/ML focused)
- Better Programming (dev tools)
- The Startup (business/tech)
- Geek Culture (tech general)
- Level Up Coding (programming)

## Batch publishing

For multiple articles, process sequentially with delays:
- Medium: max 2 articles per 24 hours
- Dev.to: no strict limit, but space them 1+ hours apart
- Hashnode: no strict limit
