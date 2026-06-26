---
name: generatebot-publish
description: Publish content to social media (LinkedIn, Instagram, TikTok, Facebook, X/Twitter) and CMS platforms (WordPress, Webflow, Ghost, Shopify). Also enriches articles with SEO internal links, AI-generated images, and brand voice rewriting via the GenerateBot API. Use when the user wants to post to social media, publish a blog post, schedule content, generate AI images, add internal links, rewrite in brand voice, or cross-post to multiple platforms.
emoji: 📢
homepage: https://generatebot.com
metadata:
  openclaw:
    primaryEnv: GENERATEBOT_API_KEY
    requires:
      env:
        - GENERATEBOT_API_KEY
---

## GenerateBot Publish - Social Media, CMS & Content Enhancement

Base URL: `https://generatebot.com/api/v1`

Authentication: Bearer token in the Authorization header.
```
Authorization: Bearer GENERATEBOT_API_KEY
```

All request and response bodies use JSON. Set `Content-Type: application/json`.

---

### Quick Reference

| Action | Endpoint | Credits |
|--------|----------|---------|
| List social accounts | GET /social/accounts | 0 |
| Post to social | POST /social/post | 0 |
| Social post history | GET /social/history | 0 |
| List CMS accounts | GET /cms/accounts | 0 |
| Publish to CMS | POST /cms/publish | 0 |
| CMS publish history | GET /cms/history | 0 |
| Create template | POST /templates | 0 |
| List templates | GET /templates | 0 |
| Get/Update/Delete | GET/PATCH/DELETE /templates/{id} | 0 |
| Render template | POST /templates/{id}/render | 20 |
| Enrich with links | POST /enrich/internal-links | 20 |
| Enrich with images | POST /enrich/images | 20 |
| Brand voice rewrite | POST /agents/brand-voice-rewriter | 5 |
| Generate images | POST /agents/ai-image-generator | 10 |
| Reddit replies | POST /agents/reddit-replier | 10 |
| Business profile | POST /agents/business-profile-generator | 5 |

---

### Prerequisites

Most publish actions require a `contentId`:
- **For articles:** Save via POST /content first (see Core skill). The response `id` is your `contentId`.
- **For videos:** The POST /videos response includes a `contentId` automatically (see Video skill).

---

### 1. Post to Social Media (0 credits)

**Step 1:** List connected accounts:
**GET /api/v1/social/accounts**
Returns: `[{ "id": "uuid", "platform": "instagram", "username": "@handle", "isConnected": true }]`

**Step 2:** Post content:
**POST /api/v1/social/post**
```json
{
  "contentId": "uuid-of-saved-content",
  "platforms": [
    {
      "accountId": "uuid-from-social-accounts",
      "platform": "instagram",
      "contentType": "video",
      "caption": "Check out our latest video!"
    },
    {
      "accountId": "uuid-linkedin",
      "platform": "linkedin",
      "contentType": "text",
      "text": "Great insights on AI in healthcare..."
    }
  ]
}
```

- `contentId` (required): UUID from POST /content or POST /videos
- `platforms[].accountId` (required): from GET /social/accounts
- `platforms[].platform`: "instagram", "tiktok", "threads", "linkedin", "youtube"
- `platforms[].contentType`: "text", "image", "video", "carousel", "multi-image"
- Optional: `caption` (max 5000), `text` (max 5000), `hashtags` (max 30), `mediaUrls` (max 10), `title` (max 200)

---

### 2. Publish to CMS (0 credits)

**Step 1:** List connected CMS platforms:
**GET /api/v1/cms/accounts**
Returns: `[{ "id": "uuid", "platform": "wordpress", "siteUrl": "https://myblog.com", "isConnected": true }]`

**Step 2:** Publish:
**POST /api/v1/cms/publish**
```json
{
  "contentId": "uuid-from-post-content",
  "cmsAccountId": "uuid-from-cms-accounts",
  "title": "Article Title",
  "content": "<p>Introduction paragraph...</p><h2>Section Heading</h2><p>Section content...</p>",
  "excerpt": "Short description",
  "featuredImageUrl": "https://cdn.example.com/hero.jpg",
  "status": "published"
}
```

- `contentId` (required): UUID from POST /content
- `cmsAccountId` (required): from GET /cms/accounts
- `title`: 1-500 chars
- `content`: HTML string, 1-200,000 chars
- Optional: `slug` (max 200), `excerpt` (max 1000), `featuredImageUrl`, `categories` (max 10), `tags` (max 20), `status` ("draft" | "published"), `scheduledAt` (ISO 8601)

**HTML conversion tip:** Wrap introduction in `<p>` tags, each section as `<h2>heading</h2><p>content</p>`.

---

### 3. Enrich Article with Internal Links (20 credits)

**POST /api/v1/enrich/internal-links**
```json
{
  "article": {
    "title": "Article title",
    "introduction": "Intro text...",
    "sections": [{ "heading": "Section heading", "content": "Section body..." }]
  },
  "businessProfile": {
    "sitemapUrl": "https://example.com/sitemap.xml",
    "websiteUrl": "https://example.com"
  }
}
```
Returns: enriched article with relevant internal links inserted into the content.

---

### 4. Enrich Article with Images (20 credits)

**POST /api/v1/enrich/images**
```json
{
  "article": {
    "title": "Article title",
    "sections": [{ "heading": "Section heading", "content": "Section body..." }]
  },
  "images": [
    { "imageUrl": "https://...", "altText": "Description", "suggestedUse": "hero" }
  ]
}
```
- `suggestedUse`: "hero", "supporting", "thumbnail", or "background"
- Returns: article with images matched to appropriate sections

---

### 5. Rewrite in Brand Voice (5 credits)

**POST /api/v1/agents/brand-voice-rewriter**
```json
{
  "articles": [{
    "title": "Article Title",
    "introduction": "Article intro...",
    "sections": [{ "heading": "Section heading", "content": "Section body..." }],
    "metaDescription": "Short description"
  }],
  "businessProfile": {
    "companyName": "Acme Corp",
    "brandVoice": "professional",
    "targetAudience": "enterprise CTOs",
    "industryCategory": "technology"
  }
}
```
Returns: rewritten articles matching the brand voice.

---

### 6. Generate AI Images (10 credits)

**POST /api/v1/agents/ai-image-generator**
```json
{
  "prompts": ["Modern office workspace with natural lighting, minimalist design"],
  "style": "natural",
  "size": "1024x1024"
}
```
- `prompts` (required): Array of 1-5 strings (min 10 chars each)
- `style`: "natural" or "vivid" (default: "natural")
- `size`: "1024x1024", "1536x1024", "1024x1536", "auto"
- `quality`: "low", "medium", "high"
- `useCase`: "thumbnail", "instagram", "carousel", "article" (auto-selects best size/quality)
- Returns: `{ "data": { "images": [{ "imageUrl": "https://cdn.generatebot.com/...", "prompt": "..." }] } }`
- Use the `imageUrl` values directly as slide images when creating video reels

---

### 7. Generate Reddit Replies (10 credits)

**POST /api/v1/agents/reddit-replier**
```json
{
  "redditPostUrl": "https://www.reddit.com/r/smallbusiness/comments/abc123/best_tools/"
}
```
- `redditPostUrl` (required): Full URL to a Reddit post
- Optional: `analysisConfig`: `{ "responseStyle": "professional" | "casual" | "educational" }`
- Returns: post analysis with reply suggestions and confidence scores

---

### 8. Generate Business Profile (5 credits)

**POST /api/v1/agents/business-profile-generator**
```json
{
  "websiteUrl": "https://example.com",
  "companyName": "Example Corp"
}
```
- `websiteUrl` (required): Company website to crawl
- `companyName` (required): Company name
- Optional: `userDescription`, `industryHint`, `country` (default: "Australia")
- Returns: structured profile with name, description, industry, targetAudience, keyProducts, tone

---

### 9. Post Templates (0 credits for CRUD, 20 credits to render)

Design and render social media post images using Fabric.js canvas templates.

**POST /api/v1/templates** - Create a template
```json
{
  "name": "LinkedIn Announcement",
  "description": "Clean announcement card for LinkedIn",
  "category": "linkedin",
  "canvasJson": "{...Fabric.js canvas JSON...}",
  "templateMetadata": {
    "fields": [
      { "key": "headline", "objectName": "headline-text", "label": "Headline", "maxLength": 80, "required": true },
      { "key": "body", "objectName": "body-text", "label": "Body Text", "maxLength": 200 }
    ],
    "imageSlots": [
      { "key": "logo", "objectName": "logo-image", "required": true }
    ]
  }
}
```
- `category`: "linkedin", "instagram", or "article"
- `canvasJson`: Valid Fabric.js JSON string (max 500KB). Must contain an `objects` array with a clip workspace object.
- `templateMetadata.fields`: Max 20 text fields. Each maps a `key` to a canvas `objectName`.
- `templateMetadata.imageSlots`: Max 10 image slots. Each maps a `key` to a canvas `objectName`.

**GET /api/v1/templates** - List templates
- Query params: `?category=linkedin&limit=10&offset=0`
- Returns: templates with pagination (no canvas JSON in list view)

**GET /api/v1/templates/{id}** - Get template with full canvas JSON

**PATCH /api/v1/templates/{id}** - Update (name, description, category, canvasJson, templateMetadata, isActive)

**DELETE /api/v1/templates/{id}** - Delete template

**POST /api/v1/templates/{id}/render** (20 credits) - Render template to image
```json
{
  "fields": {
    "headline": "We Just Launched!",
    "body": "Our new AI-powered content platform is live."
  },
  "images": {
    "logo": "https://cdn.example.com/logo.png"
  },
  "outputFormat": "jpeg",
  "quality": 0.9
}
```
- `fields`: Key-value map matching template field keys
- `images`: Key-value map matching template image slot keys (HTTPS URLs only)
- `outputFormat`: "jpeg" (default) or "png"
- `quality`: 0.1-1.0 (default: 0.9)
- Returns: `{ "creditsConsumed": 20, "imageUrl": "https://cdn...", "width": 1080, "height": 1080 }`

---

### 10. Social Post History (0 credits)

**GET /api/v1/social/history** - View past social media posts
- Query params: `?platform=instagram&status=published&limit=20&offset=0`
- `platform`: "instagram", "tiktok", "threads", "linkedin", "youtube"
- `status`: "pending", "uploading", "processing", "published", "failed", "expired", "cancelled"
- Returns: list of posts with platform, contentType, caption, status, platformPostId, publishedAt

---

### 11. CMS Publish History (0 credits)

**GET /api/v1/cms/history** - View past CMS publications
- Query params: `?platform=wordpress&status=published&limit=20&offset=0`
- `platform`: "wordpress", "ghost", "webflow", "wix", "shopify", "framer", "notion"
- `status`: "pending", "publishing", "published", "failed", "updated", "cancelled"
- Returns: list with platform, title, status, platformPostUrl, publishedAt, errorMessage

---

### Error Handling

| HTTP Status | Meaning |
|-------------|---------|
| 401 | Invalid or missing API key |
| 402 | Insufficient credits |
| 429 | Rate limit exceeded -- wait and retry |
| 400 | Invalid request body -- check error details |
| 404 | Resource not found |

All errors: `{ "error": { "code": "ERROR_CODE", "message": "..." }, "requestId": "..." }`

---

### Other GenerateBot Skills

- **Core Skill** (`generatebot-core`): Search for content, run pipelines, manage content library, RSS feeds.
- **Video Skill** (`generatebot-video`): Create video reels from pipeline data.
- **Templates Skill** (`generatebot-templates`): Design and render canvas-based post image templates.
- **Workflow Skill** (`generatebot-workflows`): End-to-end workflow examples and patterns.