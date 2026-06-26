---
name: generatebot-core
description: Search trending topics, generate blog posts and articles from any URL or keyword, fetch RSS feeds, and manage a content library via the GenerateBot API. Use when the user wants to find content ideas, write a blog post, create an article, generate SEO content, research trending topics, fetch news, aggregate RSS feeds, save drafts, or check their credit balance.
emoji: 🔍
homepage: https://generatebot.com
metadata:
  openclaw:
    primaryEnv: GENERATEBOT_API_KEY
    requires:
      env:
        - GENERATEBOT_API_KEY
---

## GenerateBot Core - Search, Generate & Manage Content

Base URL: `https://generatebot.com/api/v1`

Authentication: Bearer token in the Authorization header.
```
Authorization: Bearer GENERATEBOT_API_KEY
```

All request and response bodies use JSON. Set `Content-Type: application/json`.

---

### Quick Reference

| Action | Endpoint | Credits | Type |
|--------|----------|---------|------|
| Search content | POST /agents/news-aggregator | 10 | sync |
| Fetch RSS feeds | POST /rss | 0 | sync |
| Manage RSS feeds | GET/PUT/DELETE /rss | 0 | sync |
| Generate from URL | POST /pipelines (content-analyzer) | 100 | async |
| Generate from topic | POST /pipelines (topic-to-content) | 100 | async |
| Generate scripts | POST /pipelines (script-generator) | 15 | async |
| Poll status | GET /pipelines/{runId} | 0 | poll |
| List runs | GET /pipelines | 0 | sync |
| Save content | POST /content | 0 | sync |
| List content | GET /content | 0 | sync |
| Get/Update/Delete | GET/PATCH/DELETE /content/{id} | 0 | sync |
| Check credits | GET /credits | 0 | sync |
| Credit transactions | GET /credits/transactions | 0 | sync |

---

### 1. Search for Content Ideas

**POST /api/v1/agents/news-aggregator** (10 credits)

```json
{
  "topic": "sustainable architecture trends",
  "category": "technology",
  "searchConfig": {
    "resultLimit": 10,
    "countryCode": "us",
    "freshness": "pw",
    "searchBreadth": "wide",
    "preferredDomains": ["techcrunch.com", "reuters.com"],
    "excludeDomains": ["reddit.com"]
  }
}
```

- `topic` (required): What to search for
- `category` (optional): technology, finance, health, realestate, marketing, etc.
- `searchConfig` (optional):
  - `resultLimit`: number of results (default 10)
  - `countryCode`: "us", "au", "gb", etc.
  - `freshness`: "pd" (past day), "pw" (past week), "pm" (past month), "py" (past year)
  - `searchBreadth`: "narrow", "balanced", "wide"
  - `preferredDomains` / `excludeDomains`: arrays of domain strings
- Returns: array of articles with url, title, description, source, publishedAt, category
- Use the returned URLs with the pipeline endpoint below

**Tip:** RSS feeds (below) are a free alternative to the news aggregator.

---

### 2. RSS Feeds (Free Content Sourcing)

All RSS operations cost 0 credits.

**POST /api/v1/rss** - Fetch and parse feeds
```json
{
  "feedUrls": ["https://techcrunch.com/feed/", "https://blog.example.com/rss"],
  "maxItemsPerFeed": 10,
  "keywords": ["AI", "marketing"],
  "publishedAfter": "2026-04-01T00:00:00Z"
}
```
- `feedUrls` (optional): Direct RSS/Atom feed URLs (max 50)
- `urls` (optional): Website URLs to auto-discover feeds (max 20)
- `useSavedFeeds` (optional): If true, includes your saved feed URLs
- `maxItemsPerFeed`: 1-100
- `keywords`: Filter items by title + description match (max 20)
- `publishedAfter`: ISO 8601 date filter
- `feedFilter` / `feedExclude`: Include/exclude feeds by pattern
- `dedup`: Deduplicate items across runs
- `skipUnhealthyFeeds`: Skip feeds with 5+ consecutive failures
- `digest`: `{ "maxDigestItems": 20, "groupByTopic": true }` for summarized output
- Must provide at least one of `urls`, `feedUrls`, or `useSavedFeeds`
- Returns: feeds array with items (title, link, description, publishedAt, source, etc.)

**GET /api/v1/rss** - List saved feed URLs
- Returns: `{ "feedUrls": [...], "count": 3 }`

**PUT /api/v1/rss** - Save feed URLs (requires `rss:write` scope)
- Input: `{ "feedUrls": ["https://example.com/feed.xml"] }` (max 50)
- Requires an existing business profile

**DELETE /api/v1/rss** - Clear all saved feed URLs (requires `rss:write` scope)

---

### 3. Generating Content (Pipelines)

**POST /api/v1/pipelines** (async)

| Pipeline Type | Credits | Requires | Purpose |
|---------------|---------|----------|---------|
| `content-analyzer` | 100 | `url` | Generate articles, social posts, scripts, carousel from a URL |
| `full-pipeline` | 100 | `query` or `queries[]` | Generate content from a topic or question |
| `script-generator` | 15 | `query` | Generate video scripts only |

**From a URL (most common):**
```json
{ "pipelineType": "content-analyzer", "url": "https://example.com/article" }
```

**From a topic:**
```json
{ "pipelineType": "full-pipeline", "query": "How AI is transforming healthcare" }
```

Optional fields:
- `market`: "au" or "us"
- `resultLimit`: 1-100
- `businessProfile`: object with company context
- `carouselTemplate`: `{ "prompt": "...", "username": "..." }` (content-analyzer only)

Response: `{ "pipelineRunId": "uuid", "status": "running", "creditsConsumed": 100, "statusUrl": "/api/v1/pipelines/{runId}" }`

**Save the `pipelineRunId`** -- you need it later as `sourcePipelineRunId` when creating videos.

**Polling:** GET /api/v1/pipelines/{runId} every 10 seconds.
- Status values: "pending" -> "running" -> "completed" | "failed"
- Typical duration: 2-3 minutes. Keep polling up to 5 minutes.

**GET /api/v1/pipelines** - List pipeline runs
- Query params: `?status=completed&pipelineType=content-analyzer&limit=10&offset=0`

---

### 4. Completed Pipeline Response Shape

When status is `"completed"`, the response contains all generated content:

```json
{
  "status": "completed",
  "results": {
    "data": {
      "agents": {
        "aiContentGenerator": {
          "generatedContent": {
            "articles": [{ "title": "...", "introduction": "...", "sections": [{ "heading": "...", "content": "..." }], "wordCount": 1200 }],
            "linkedInPosts": [{ "intro": "...", "mainContent": "...", "callToAction": "...", "hashtags": ["#AI"] }],
            "instagramPosts": [{ "caption": "...", "hashtags": ["#AI"], "imageTextOverlay": "..." }]
          }
        },
        "scriptGenerator": {
          "scripts": [{
            "hook": "Breaking news you need to know!",
            "platform": "tiktok",
            "mainContent": [
              { "scene": 1, "voiceOver": "Here is what happened...", "textOverlay": "Key Point 1" }
            ],
            "callToAction": "Follow for more!",
            "hashtags": ["#News"]
          }]
        },
        "imageFinder": {
          "foundImages": [
            { "imageUrl": "https://cdn.example.com/img1.jpg", "altText": "...", "suggestedUse": "hero" },
            { "imageUrl": "https://cdn.example.com/img2.jpg", "altText": "...", "suggestedUse": "supporting" }
          ]
        },
        "carouselGenerator": {
          "carousel": {
            "slides": [
              { "slideNumber": 1, "text": "Key takeaway from the article" },
              { "slideNumber": 2, "text": "Supporting point with context" },
              { "slideNumber": 3, "text": "Final thought and call to action" }
            ]
          }
        }
      }
    },
    "totalImagesFound": 30,
    "totalContentItems": 5
  }
}
```

**Key paths to extract:**
- Articles: `results.data.agents.aiContentGenerator.generatedContent.articles[0]`
- Scripts: `results.data.agents.scriptGenerator.scripts[0]`
- Images: `results.data.agents.imageFinder.foundImages`
- Carousel slides: `results.data.agents.carouselGenerator.carousel.slides`

**IMPORTANT:** Pipeline results are NOT auto-saved. Save via POST /content before publishing.

---

### 5. Content Library

**POST /api/v1/content** - Save content (required before CMS/social publishing)
```json
{
  "contentType": "article",
  "title": "Article Title",
  "contentData": {
    "introduction": "Intro paragraph...",
    "sections": [{ "heading": "Section", "content": "Body text..." }],
    "metaDescription": "Short description"
  },
  "tags": ["ai", "marketing"]
}
```
- `contentType`: "article" | "linkedin" | "instagram" | "tiktok" | "script" | "reel"
- `contentData`: JSON object (max 100KB)
- `tags` (optional): max 20 strings
- `notes` (optional): max 2000 chars
- Returns: `{ "content": { "id": "uuid", ... } }` -- save the `id` as `contentId`

**GET /api/v1/content** - List content
- Query params: `?contentType=article&status=draft&limit=10&offset=0&tags=ai,marketing`
- Returns: content list with pagination (no full contentData in list view)

**GET /api/v1/content/{id}** - Get single item with full contentData

**PATCH /api/v1/content/{id}** - Update (title, contentData, tags, notes, status)

**DELETE /api/v1/content/{id}** - Delete

---

### 6. Credits

**GET /api/v1/credits** (0 credits)
Returns: `{ "total": 500, "subscription": 400, "oneTime": 100, "adminGranted": 0, "quota": 1000 }`

**GET /api/v1/credits/transactions** (0 credits) - Credit transaction history
- Query params: `?limit=20&offset=0`
- Returns: list of credit transactions with amount, type, description, and timestamps

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

- **Video Skill** (`generatebot-video`): Create video reels from pipeline data. Step-by-step tutorial for slides, image modes, captions, TTS.
- **Publish Skill** (`generatebot-publish`): Post to social media, publish to CMS, enrich articles, brand voice, AI images.
- **Templates Skill** (`generatebot-templates`): Design and render canvas-based post image templates.
- **Workflow Skill** (`generatebot-workflows`): End-to-end workflow examples, credit costs, usage patterns.