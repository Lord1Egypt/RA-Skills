---
name: generatebot
description: All-in-one content generation, social media publishing, video creation, and image template design via the GenerateBot API. Search trending topics, write blog posts and articles, create short-form video reels, design and render image templates, publish to LinkedIn/Instagram/TikTok/WordPress, enrich with SEO links, generate AI images, and rewrite in brand voice. Use when the user mentions GenerateBot, wants to generate content, create videos, design post images, publish to social media or CMS, or automate content workflows.
emoji: 🤖
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

---

## GenerateBot Video - Create Video Reels

Base URL: `https://generatebot.com/api/v1`

Authentication: Bearer token in the Authorization header.
```
Authorization: Bearer GENERATEBOT_API_KEY
```

All request and response bodies use JSON. Set `Content-Type: application/json`.

---

### Overview

This skill creates short-form video reels (9:16 portrait, 1080x1920) with AI voiceover from content you have generated.

- **Cost:** 200 credits per video
- **Endpoint:** POST /api/v1/videos
- **Max concurrent renders:** 2 (extra requests return 429)
- **Typical render time:** 60-180 seconds

---

### Prerequisites

Before creating a video, you need **completed pipeline results**. Run a content pipeline first (see Core skill):
```
POST /api/v1/pipelines
{ "pipelineType": "content-analyzer", "url": "https://example.com/article" }
```
Poll until status is "completed", then extract these three things:

1. **Carousel slides:** `results.data.agents.carouselGenerator.carousel.slides`
   ```json
   [{ "slideNumber": 1, "text": "Key takeaway from the article" }, ...]
   ```

2. **Images:** `results.data.agents.imageFinder.foundImages`
   ```json
   [{ "imageUrl": "https://...", "altText": "...", "suggestedUse": "hero" }, ...]
   ```

3. **Hook:** `results.data.agents.scriptGenerator.scripts[0].hook`
   ```json
   "Breaking news you need to know!"
   ```

4. **Pipeline Run ID:** The `pipelineRunId` from the pipeline POST response.

---

### Step 1: Build Video Slides

Each carousel slide becomes one video slide. Map them like this:

```json
{
  "text": "<carousel slide text>",
  "imageUrl": "<image URL from imageFinder>",
  "highlight": ["key", "words"]
}
```

**Pairing rules:**
- Use the `suggestedUse: "hero"` image for slide 1
- Use remaining images for subsequent slides
- Each slide MUST have a unique `imageUrl` -- never reuse the same image across slides
- `text` is max 200 characters

**The `text` field is both the on-screen caption AND the voiceover narration.** Write it as spoken language:
- Numbers in words: "25 million dollars" not "$25M"
- Use "A.I." not "AI" (TTS pronounces it better)
- Add ellipsis for dramatic pauses: "And then... everything changed."

---

### Step 2: Image Display Modes

The `imageMode` field controls how images appear in the 9:16 portrait frame:

| Mode | Behavior | Best For |
|------|----------|----------|
| *(omit)* | **Auto-detect:** landscape (w/h > 1.2) uses overlay, else background | Most cases -- recommended |
| `"overlay"` | Image shown as 16:9 PiP inset (top 12%) over blurred/darkened version of itself | Landscape images, real estate, group photos |
| `"background"` | Full-screen cover-crop fills the entire frame | Portrait images, close-ups |
| `"background_with_overlays"` | Primary image full-bleed + `extraImages` as PiP insets | Multiple detail shots over a main image |

**Recommendation:** Omit `imageMode` in most cases. Auto-detection handles landscape vs portrait correctly. Only set it explicitly to override.

---

### Step 3: Extra Images and Word-Synced Timing

Add related images as overlays that appear synced to specific words in the narration:

```json
{
  "text": "A stunning property in Brisbane with a resort style pool",
  "imageUrl": "https://cdn.example.com/mansion-exterior.jpg",
  "extraImages": [
    "https://cdn.example.com/mansion-aerial.jpg",
    "https://cdn.example.com/mansion-pool.jpg"
  ],
  "extraImageTimings": [
    { "showAtWordIndex": 2 },
    { "showAtWordIndex": 7 }
  ]
}
```

**How word indexing works:**
Count words in `text` starting from 0, split on whitespace. Punctuation stays attached.

For the text above: A(0) stunning(1) property(2) in(3) Brisbane(4) with(5) a(6) resort(7) style(8) pool(9)

- The aerial shot appears at word 2 ("property")
- The pool shot appears at word 7 ("resort")
- Each overlay stays visible until the next one starts or the slide ends

**When to use extraImages:**
- Landscape images that lose detail when cropped to 9:16
- Multiple angles of the same subject (exterior + pool + interior)
- You CAN reuse the main `imageUrl` in `extraImages` for blurred-bg + clear-overlay effect

**Limits:** Max 5 extra images per slide. If you omit `extraImageTimings`, overlays distribute evenly (less precise).

---

### Step 4: Highlights

The `highlight` field is an array of words from `text` to emphasize visually (rendered in accent color with glow effect):

```json
"highlight": ["25 million", "mansion"]
```

- Pick 1-3 key words or phrases that appear in the `text`
- Max 10 items
- If omitted, the API auto-generates 2 highlights (prefers numbers and capitalized words)

---

### Step 5: Per-Slide Style Overrides (Optional)

Each slide can override global styles:

| Field | Type | Range |
|-------|------|-------|
| `fontSize` | number | 12-120 |
| `fontWeight` | string | "normal" or "bold" |
| `textColor` | string | hex, e.g. "#FFFFFF" |
| `backgroundColor` | string | hex, e.g. "#000000" |
| `textAlign` | string | "left", "center", "right" |
| `textPosition` | string | "top", "center", "bottom" |
| `imageOpacity` | number | 0-1 |
| `textWidthPercent` | number | 10-100 |
| `imageScale` | number | 0.1-5 (zoom level) |
| `imagePositionX` | number | horizontal offset |
| `imagePositionY` | number | vertical offset |

**Advanced text styling** (`textStyle` object, all fields optional):
```json
{
  "textStyle": {
    "fontFamily": "Inter",
    "letterSpacing": 1.2,
    "lineHeight": 1.4,
    "textTransform": "uppercase",
    "shadow": { "enabled": true, "offsetX": 2, "offsetY": 2, "blur": 4, "color": "#000000" },
    "outline": { "enabled": true, "width": 2, "color": "#000000" },
    "background": { "enabled": true, "color": "#000000", "opacity": 0.7, "paddingX": 12, "paddingY": 8, "borderRadius": 8 },
    "glow": { "enabled": true, "blur": 10, "color": "#75F30F", "intensity": 0.8 }
  }
}
```
- `textTransform`: "none", "uppercase", "lowercase", "capitalize"
- `shadow`: Drop shadow behind text
- `outline`: Stroke around text characters
- `background`: Colored box behind text (like a caption box)
- `glow`: Colored glow effect around text

---

### Step 6: Set the Hook

```json
"hook": "<scriptGenerator.scripts[0].hook>"
```

- Max 200 characters
- This is the opening text shown before slides begin
- No separate `script` field needed -- the API auto-builds TTS narration from all slide texts

---

### Step 7: Configure Global Style (Optional)

```json
"style": {
  "accentColor": "#FF5500",
  "captionStyle": "outlined",
  "captionPosition": "center",
  "fontSize": 48,
  "colorGrade": "cinematic",
  "filmGrain": { "enabled": true, "opacity": 0.025, "fps": 8 }
}
```

| Field | Options | Default |
|-------|---------|---------|
| `accentColor` | Hex color | #75F30F |
| `captionStyle` | "default", "outlined", "boxed", "marker" | "outlined" |
| `captionPosition` | "center", "lower-third", "top" | "lower-third" |
| `fontSize` | 24-96 | 52 |
| `colorGrade` | "cinematic", "warm", "cool", "vibrant", "none" | none |
| `filmGrain` | `{ enabled, opacity (0-0.1), fps (1-30) }` | disabled |

---

### Step 8: Configure Voice (Optional)

| Field | Description | Default |
|-------|-------------|---------|
| `voiceId` | ElevenLabs voice ID | (default Australian male) |
| `ttsModel` | "eleven_v3", "eleven_flash_v2_5", "eleven_multilingual_v2", "eleven_turbo_v2_5" | "eleven_v3" |
| `speedFactor` | 0.5-3.0, post-render speed multiplier | 1.35 |

---

### Step 9: Assemble and Submit

**POST /api/v1/videos** (200 credits)

```json
{
  "hook": "$25M mansion hits the market!",
  "slides": [
    {
      "text": "A 25 million dollar mansion in Brisbane is up for grabs.",
      "imageUrl": "https://cdn.example.com/mansion-exterior.jpg",
      "highlight": ["25 million", "mansion"],
      "extraImages": ["https://cdn.example.com/mansion-aerial.jpg"],
      "extraImageTimings": [{ "showAtWordIndex": 4 }]
    },
    {
      "text": "Spanning 1400 square meters with five bedrooms and eight bathrooms.",
      "imageUrl": "https://cdn.example.com/mansion-pool.jpg",
      "highlight": ["1400", "bathrooms"]
    }
  ],
  "sourcePipelineRunId": "<pipelineRunId from pipeline POST>",
  "style": {
    "accentColor": "#75F30F",
    "captionStyle": "outlined",
    "captionPosition": "center"
  }
}
```

**Field constraints:**
- `hook`: 1-200 chars, required
- `slides`: 1-15 slides, required (4-7 recommended)
- `slides[].text`: 1-200 chars, required
- `slides[].imageUrl`: HTTPS URL, required
- `slides[].highlight`: max 10 items, optional
- `slides[].extraImages`: max 5 URLs, optional
- `watermark`: small text in corner, max 100 chars, optional
- `watermarkLogoUrl`: HTTPS URL to a logo image for the watermark, optional
- `watermarkPosition`: position string (max 50 chars), optional
- `cta`: `{ "text": "Follow for more!", "url": "example.com" }`, optional
- `sourcePipelineRunId`: UUID, **strongly recommended** -- links video to source content

Response:
```json
{
  "jobId": "uuid",
  "contentId": "uuid",
  "status": "queued",
  "creditsConsumed": 200,
  "statusUrl": "/api/v1/videos/{jobId}"
}
```

---

### Step 10: Poll for Completion

**GET /api/v1/videos/{jobId}** every 5 seconds.

Status progression: `queued` -> `generating_audio` -> `rendering` -> `uploading` -> `completed`

- **queued**: 10-30s while render worker starts. Normal.
- **generating_audio**: TTS is being generated. Progress, not a stall.
- **rendering**: Video frames being composed. Longest phase.
- **completed**: `videoUrl` contains the download URL.
- **failed**: `error` field contains the error message.

**Keep polling up to 5 minutes.** Do NOT stop on intermediate statuses. Do NOT report failure until status is "failed" or you have polled the maximum duration.

---

### Step 11: Post the Video

The video response includes a `contentId`. Use it directly with POST /api/v1/social/post (see Publish skill):

```json
{
  "contentId": "<contentId from video response>",
  "platforms": [{
    "accountId": "<from GET /api/v1/social/accounts>",
    "platform": "instagram",
    "contentType": "video",
    "caption": "Check out our latest video!"
  }]
}
```

---

### Render Time Estimates

| Slides | Approximate Time |
|--------|------------------|
| 3-5 | 60-90 seconds |
| 6-10 | 90-150 seconds |
| 11-15 | 150-180 seconds |

Audio generation adds 10-20 seconds. Upload adds 5-10 seconds.

---

### Error Handling

| HTTP Status | Meaning |
|-------------|---------|
| 402 | Insufficient credits (need 200) |
| 429 | Too many concurrent renders (max 2) -- wait and retry |
| 400 | Invalid request body -- check error details |

---

### Other GenerateBot Skills

- **Core Skill** (`generatebot-core`): Search for content, run pipelines, manage content library. **Required before creating videos.**
- **Publish Skill** (`generatebot-publish`): Post completed videos to social media, publish articles to CMS.
- **Templates Skill** (`generatebot-templates`): Design and render canvas-based post image templates.
- **Workflow Skill** (`generatebot-workflows`): End-to-end workflow examples and patterns.

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

---

## GenerateBot Templates - Design & Render Post Images

Base URL: `https://generatebot.com/api/v1`

Authentication: Bearer token in the Authorization header.
```
Authorization: Bearer GENERATEBOT_API_KEY
```

All request and response bodies use JSON. Set `Content-Type: application/json`.

---

### Quick Reference

| Action | Method | Path | Credits | Type |
|--------|--------|------|---------|------|
| Create template | POST | /templates | 0 | sync |
| List templates | GET | /templates | 0 | sync |
| Get template | GET | /templates/{id} | 0 | sync |
| Update template | PATCH | /templates/{id} | 0 | sync |
| Delete template | DELETE | /templates/{id} | 0 | sync |
| Render template | POST | /templates/{id}/render | 20 | sync |

---

### System Overview

Templates are canvas JSON documents with dynamic text and image slots. When rendered, the system substitutes placeholder content with real text and images, auto-fits text to its bounding box, and smart-fits images to cover their target areas. The output is a high-quality image (JPEG or PNG) uploaded to CDN.

---

### Canvas JSON Format

#### Top-Level Structure

```json
{
  "version": "5.3.0",
  "objects": [ ... ],
  "clipPath": {
    "type": "rect",
    "version": "5.3.0",
    "left": 0, "top": 0,
    "width": 1080, "height": 1920,
    "fill": "#0a0a0a",
    "scaleX": 1, "scaleY": 1
  }
}
```

- `version`: Always `"5.3.0"`
- `objects`: Ordered array of canvas objects (back-to-front rendering order)
- `clipPath`: Canvas-level clip boundary -- MUST match the `clip` rect dimensions and fill

#### The Clip Rect (Workspace)

Every template MUST have a `clip` rect as its first object. This defines the artboard:

```json
{
  "type": "rect",
  "version": "5.3.0",
  "originX": "left", "originY": "top",
  "left": 0, "top": 0,
  "width": 1080, "height": 1920,
  "fill": "#0a0a0a",
  "stroke": null, "strokeWidth": 0,
  "scaleX": 1, "scaleY": 1,
  "opacity": 1, "visible": true,
  "name": "clip",
  "selectable": false, "hasControls": false
}
```

**Common dimensions:**

| Format | Width | Height | Use Case |
|--------|-------|--------|----------|
| Portrait / Story | 1080 | 1920 | Instagram Stories, LinkedIn Stories |
| Square | 1080 | 1080 | Instagram Feed, LinkedIn Feed |
| Landscape | 1200 | 627 | LinkedIn Articles, Twitter/X |

#### Object Naming Convention

| Pattern | Type | Example | Purpose |
|---------|------|---------|---------|
| `{{key}}` | Dynamic | `{{title}}`, `{{primaryImage}}` | Replaced during rendering |
| Plain name | Static | `gradient_overlay_1`, `accent_line` | Fixed decorative elements |
| `clip` | Workspace | `clip` | Artboard boundary (exactly one) |

#### Image Objects

Image placeholders define where dynamic images appear. The `src` MUST use a 1x1 transparent pixel -- never an empty string.

```json
{
  "type": "image",
  "version": "5.3.0",
  "originX": "left", "originY": "top",
  "left": 0, "top": 0,
  "width": 1200, "height": 800,
  "scaleX": 0.9, "scaleY": 2.4,
  "opacity": 1, "visible": true,
  "name": "{{primaryImage}}",
  "selectable": true, "hasControls": true,
  "src": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=",
  "crossOrigin": "anonymous",
  "filters": []
}
```

**Key rules:**
- `src` MUST be the 1x1 transparent pixel base64 shown above. Empty string `""` causes rendering failures.
- `crossOrigin` MUST be `"anonymous"`
- `filters` MUST be `[]` (empty array)
- `width`/`height` define unscaled dimensions; `scaleX`/`scaleY` scale to visual target size
- The renderer auto-fits the actual image to cover the target area (width*scaleX by height*scaleY)

**Circular image crop (optional):**

```json
{
  "type": "image",
  "name": "{{secondaryImage}}",
  "width": 300, "height": 300,
  "scaleX": 1, "scaleY": 1,
  "src": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=",
  "crossOrigin": "anonymous", "filters": [],
  "clipPath": {
    "type": "circle",
    "version": "5.3.0",
    "radius": 140,
    "left": 0, "top": 0,
    "originX": "center", "originY": "center",
    "fill": "rgb(0,0,0)",
    "inverted": false, "absolutePositioned": false
  }
}
```

#### Textbox Objects

Use large `fontSize` directly -- never use `scaleX`/`scaleY` to size text.

```json
{
  "type": "textbox",
  "version": "5.3.0",
  "originX": "left", "originY": "top",
  "left": 70, "top": 1050,
  "width": 940, "height": 350,
  "fill": "rgba(255, 255, 255, 1)",
  "stroke": null, "strokeWidth": 0,
  "fontSize": 82, "fontFamily": "Arial", "fontWeight": 900,
  "text": "Headline Goes Here in Bold White Text",
  "textAlign": "left", "lineHeight": 1.08, "charSpacing": 0,
  "scaleX": 1, "scaleY": 1,
  "angle": 0, "opacity": 1, "visible": true,
  "name": "{{title}}",
  "selectable": true, "hasControls": true, "editable": true
}
```

**Key rules:**
- `fontSize` MUST be the actual desired size. Do NOT use scaleX/scaleY to enlarge text -- this breaks auto-fit.
- `scaleX` and `scaleY` MUST be `1` on text objects.
- `height` defines the maximum bounding box -- set it generously. The renderer shrinks text to fit.
- `width` defines the text wrapping width.

**Recommended font sizes by role:**

| Role | fontSize | fontWeight | Notes |
|------|----------|------------|-------|
| Title / Headline | 62-82 | 700-900 | Bold, high-impact |
| Description / Body | 32-42 | 400 | Regular weight |
| Label / Tag | 24-28 | 700 | Often with `charSpacing: 80-150` |
| Website / URL | 22-26 | 400-600 | Subtle, lower opacity |
| CTA | 24-28 | 600-700 | Right-aligned or centered |

#### Gradient Overlays

Gradient overlays create dark zones over images where text remains readable. Use a 400x400 base rect, scale it up with `scaleX`/`scaleY`, and flip vertically with `flipY: true` so the solid color sits at the bottom.

```json
{
  "type": "rect",
  "version": "5.3.0",
  "originX": "left", "originY": "top",
  "left": -20, "top": 540,
  "width": 400, "height": 400,
  "fill": {
    "type": "linear",
    "coords": {"x1": 200, "y1": 0, "x2": 200, "y2": 400},
    "colorStops": [
      {"offset": 0, "color": "rgba(0, 0, 0, 1)"},
      {"offset": 0.6, "color": "rgba(0, 0, 0, 0.75)"},
      {"offset": 0.9, "color": "rgba(0, 0, 0, 0)"}
    ],
    "offsetX": 0, "offsetY": 0, "gradientUnits": "pixels"
  },
  "stroke": null, "strokeWidth": 0,
  "scaleX": 2.85, "scaleY": 3.5,
  "flipY": true,
  "opacity": 1, "visible": true,
  "name": "gradient_overlay_1", "selectable": true
}
```

**Best practices:**
- **Stack TWO gradient rects** with slightly different positions and color stop distributions for visual depth
- `flipY: true` makes offset 0 (solid) appear at the bottom, offset 1 (transparent) at the top
- Gradient covers the bottom 60-70% of the canvas; text sits in the fully opaque zone
- Use `left: -20` to ensure full-width coverage after scaling

---

### Template Metadata

Describes which objects are dynamic and how they appear in the editor:

```json
{
  "fields": [
    {
      "key": "title",
      "objectName": "{{title}}",
      "label": "Title",
      "maxLength": 80,
      "required": true,
      "defaultValue": "Headline Goes Here in Bold White Text"
    }
  ],
  "imageSlots": [
    {
      "key": "primaryImage",
      "objectName": "{{primaryImage}}",
      "required": true
    }
  ]
}
```

**Rules:**
- Every `{{key}}` object in canvas JSON MUST have a matching entry in `fields` (text) or `imageSlots` (images)
- `objectName` MUST exactly match the object's `name` including `{{` and `}}`
- Maximum 20 fields, maximum 10 image slots
- `defaultValue` should match the `text` property of the corresponding textbox

**Standard variable names:**

| Key | Type | Purpose | Typical maxLength |
|-----|------|---------|-------------------|
| `title` | field | Main headline | 60-100 |
| `description` | field | Supporting text | 150-250 |
| `label` | field | Category tag (e.g., "BREAKING NEWS") | 20-30 |
| `website` | field | URL or domain | 30 |
| `cta` | field | Call to action (e.g., "Read Below") | 20-30 |
| `primaryImage` | imageSlot | Main hero image | - |
| `secondaryImage` | imageSlot | Supporting image (headshot, logo) | - |

---

### API Reference

#### POST /templates -- Create Template

```json
{
  "name": "News Card Dark",
  "description": "Dark cinematic news card with full-bleed hero image...",
  "category": "linkedin",
  "canvasJson": "{...stringified canvas JSON...}",
  "templateMetadata": {
    "fields": [...],
    "imageSlots": [...]
  }
}
```

**Validation:**
- `name`: 1-200 characters, required
- `description`: max 1000 characters, optional
- `category`: `"linkedin"` | `"instagram"` | `"article"`, required
- `canvasJson`: stringified JSON, max 500KB, must contain a `clip` object
- `templateMetadata.fields`: max 20 items
- `templateMetadata.imageSlots`: max 10 items

**Response (201):**
```json
{
  "success": true,
  "data": {
    "template": {
      "id": "uuid",
      "name": "News Card Dark",
      "description": "...",
      "category": "linkedin",
      "template_metadata": {...},
      "thumbnail_url": null,
      "created_at": "2026-04-10T..."
    }
  }
}
```

#### GET /templates -- List Templates

Query: `?category=linkedin&limit=10&offset=0`

Returns lightweight metadata (no `canvas_json`). Use GET by ID for the full template.

```json
{
  "success": true,
  "data": {
    "templates": [...],
    "pagination": { "total": 12, "limit": 10, "offset": 0, "hasMore": true }
  }
}
```

#### GET /templates/{id} -- Get Template

Returns full template including `canvas_json`.

#### PATCH /templates/{id} -- Update Template

Partial updates. Send only the fields to change (`name`, `category`, `canvasJson`, `templateMetadata`, `isActive`).

#### DELETE /templates/{id} -- Delete Template

Returns `{ "success": true, "data": { "deleted": true } }`.

#### POST /templates/{id}/render -- Render Template (20 credits)

```json
{
  "fields": {
    "title": "Breaking: AI Reaches New Milestone",
    "description": "Researchers announce breakthrough in reasoning capabilities.",
    "label": "TECH NEWS",
    "website": "technews.com"
  },
  "images": {
    "primaryImage": "https://example.com/hero.jpg"
  },
  "outputFormat": "jpeg",
  "quality": 0.9
}
```

- `fields`: key-value pairs matching template field keys (all strings)
- `images`: key-value pairs matching template image slot keys (HTTPS URLs only)
- `outputFormat`: `"jpeg"` (default) or `"png"`
- `quality`: 0.1-1.0, default 0.9

**Response:**
```json
{
  "success": true,
  "data": {
    "imageUrl": "https://generatebot.b-cdn.net/posts/...",
    "width": 1080,
    "height": 1920,
    "creditsConsumed": 20,
    "pipelineRunId": "uuid"
  }
}
```

---

### Text Auto-Fit

The renderer automatically shrinks text to fit within its bounding box:
1. Set `height` generously on textbox objects -- this is the max vertical space
2. Use the actual desired `fontSize` -- the renderer shrinks if text is longer than placeholder
3. Do not rely on `scaleX`/`scaleY` for text sizing -- keep both at `1`
4. Test with long text to verify auto-fit behavior

### Image Smart-Fit

The renderer scales images to cover their target area without distortion:
- Target area = `width * scaleX` by `height * scaleY`
- Image is scaled uniformly to fill (cover) the target area, centered
- Just provide the image URL at render time -- the system handles all sizing

---

### Design Patterns

**Pattern 1: Hero Image with Gradient Overlay (Dark Theme)**
Best for news, dramatic stories. Full-bleed hero image, two stacked gradient rects, bold white title, subtle description, label at top, website/CTA at bottom.

**Pattern 2: Square Card with Accent Line**
Best for feeds. 1080x1080, aggressive gradient, thin vertical accent line, large caps title, no description.

**Pattern 3: Editorial Clean (Light Theme)**
Best for thought leadership. Light background, colored label badge, serif title, hero image in bottom half.

**Pattern 4: Split Dual Image**
Best for comparisons. Two images separated by a colored title band.

---

### Critical Rules

1. Image `src` must NEVER be empty string. Always use: `data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=`
2. Text `scaleX` and `scaleY` must be `1`. Use `fontSize` for sizing.
3. The `clip` rect must be the first object with `name: "clip"`.
4. Canvas-level `clipPath` must match the clip rect's dimensions and fill.
5. Image objects must include `crossOrigin: "anonymous"` and `filters: []`.
6. Gradient overlays use 400x400 base size scaled via `scaleX`/`scaleY`. Never use full canvas dimensions directly.
7. Stack TWO gradient rects for depth -- single gradients look flat.
8. Set generous `height` on textboxes -- this is the auto-fit bounding box.
9. Category must be `"linkedin"`, `"instagram"`, or `"article"`.
10. `canvasJson` max size is 500KB.
11. Every `{{key}}` object must have a matching metadata entry.

### Available Fonts

`Arial, Arial Black, Verdana, Helvetica, Tahoma, Trebuchet MS, Times New Roman, Georgia, Garamond, Courier New, Brush Script MT, Palatino, Bookman, Comic Sans MS, Impact, Lucida Sans Unicode, Geneva, Lucida Console`

### Example: Create and Render a Template

**Step 1: Create**
```bash
curl -X POST https://generatebot.com/api/v1/templates \
  -H "Authorization: Bearer GENERATEBOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "News Card Dark",
    "description": "Dark cinematic news card",
    "category": "linkedin",
    "canvasJson": "{...stringified canvas JSON...}",
    "templateMetadata": {
      "fields": [
        {"key": "title", "objectName": "{{title}}", "label": "Title", "maxLength": 80, "required": true, "defaultValue": "Your Headline"}
      ],
      "imageSlots": [
        {"key": "primaryImage", "objectName": "{{primaryImage}}", "required": true}
      ]
    }
  }'
```

**Step 2: Render (20 credits)**
```bash
curl -X POST https://generatebot.com/api/v1/templates/TEMPLATE_ID/render \
  -H "Authorization: Bearer GENERATEBOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": { "title": "AI Breakthrough Announced Today" },
    "images": { "primaryImage": "https://example.com/hero.jpg" },
    "outputFormat": "jpeg",
    "quality": 0.9
  }'
```

---

### Error Handling

| HTTP Status | Meaning |
|-------------|---------|
| 401 | Invalid or missing API key |
| 402 | Insufficient credits |
| 429 | Rate limit exceeded -- wait and retry |
| 400 | Invalid request body -- check error details |
| 404 | Template not found |

All errors: `{ "error": { "code": "ERROR_CODE", "message": "..." }, "requestId": "..." }`

---

### Other GenerateBot Skills

- **Core Skill** (`generatebot-core`): Search, pipeline, RSS, content CRUD, and credits endpoints.
- **Video Skill** (`generatebot-video`): Detailed video creation tutorial with imageMode reference.
- **Publish Skill** (`generatebot-publish`): Social posting, CMS publishing, enrichment, brand voice, AI images.
- **Workflows Skill** (`generatebot-workflows`): End-to-end workflow patterns and usage mapping.

---

## GenerateBot Workflows - Reference Guide

Base URL: `https://generatebot.com/api/v1`

Authentication: Bearer token in the Authorization header.
```
Authorization: Bearer GENERATEBOT_API_KEY
```

All request and response bodies use JSON. Set `Content-Type: application/json`.

---

### Credit Cost Summary

| Action | Credits | Skill |
|--------|---------|-------|
| Search (news-aggregator) | 10 | Core |
| RSS feeds (all operations) | 0 | Core |
| Content pipeline (content-analyzer) | 100 | Core |
| Topic pipeline (full-pipeline) | 100 | Core |
| Script generator pipeline | 15 | Core |
| Video reel | 200 | Video |
| Template render | 20 | Publish |
| Enrich (links or images) | 20 each | Publish |
| Brand voice rewrite | 5 | Publish |
| AI image generation | 10 | Publish |
| Reddit replies | 10 | Publish |
| Business profile | 5 | Publish |
| Save/list content | 0 | Core |
| Credit transactions | 0 | Core |
| Template CRUD | 0 | Publish |
| Social media post | 0 | Publish |
| Social post history | 0 | Publish |
| CMS publish | 0 | Publish |
| CMS publish history | 0 | Publish |
| Check credits | 0 | Core |

---

### Usage Pattern Mapping

| User Request | Actions | Credits |
|-------------|---------|---------|
| "search for [topic]" | POST /agents/news-aggregator | 10 |
| "get RSS news" | POST /rss | 0 |
| "write an article about [topic]" | POST /pipelines (full-pipeline) | 100 |
| "create content from [url]" | POST /pipelines (content-analyzer) | 100 |
| "make a video about [topic]" | Pipeline (100) + Video (200) | 300 |
| "enrich with links/images" | POST /enrich/* | 20 each |
| "generate images" | POST /agents/ai-image-generator | 10 |
| "rewrite in brand voice" | POST /agents/brand-voice-rewriter | 5 |
| "create a post template" | POST /templates | 0 |
| "render a template" | POST /templates/{id}/render | 20 |
| "post to [platform]" | POST /social/post (needs contentId) | 0 |
| "publish to [cms]" | POST /cms/publish (needs contentId) | 0 |
| "show post history" | GET /social/history or GET /cms/history | 0 |
| "check credits" / "transactions" | GET /credits or GET /credits/transactions | 0 |

---

### Complete Workflow: Search -> Article -> Video -> Publish

**Step 1: Check credits** -- GET /api/v1/credits (0 credits)
- Confirm you have at least 310 credits for the full flow

**Step 2: Search for a topic** -- POST /api/v1/agents/news-aggregator (10 credits)
- Send: `{ "topic": "your topic here" }`
- Extract the best article URL from the response array

**Step 3: Generate content** -- POST /api/v1/pipelines (100 credits)
- Send: `{ "pipelineType": "content-analyzer", "url": "<URL from step 2>" }`
- Poll GET /api/v1/pipelines/{runId} every 10s until "completed"

**Step 4: Extract content from completed pipeline**
- Article: `results.data.agents.aiContentGenerator.generatedContent.articles[0]`
- Script: `results.data.agents.scriptGenerator.scripts[0]`
- Images: `results.data.agents.imageFinder.foundImages`
- Carousel: `results.data.agents.carouselGenerator.carousel.slides`

**Step 5: Save the article** -- POST /api/v1/content (0 credits)
```json
{
  "contentType": "article",
  "title": "<articles[0].title>",
  "contentData": {
    "introduction": "<articles[0].introduction>",
    "sections": "<articles[0].sections>",
    "metaDescription": "<articles[0].metaDescription>"
  }
}
```
Save the returned `contentId` at `response.content.id`.

**Step 6: Publish article to CMS** -- POST /api/v1/cms/publish (0 credits)
- GET /api/v1/cms/accounts to get the `cmsAccountId`
- Convert article to HTML: `<p>introduction</p><h2>heading</h2><p>content</p>`
- Send with `contentId` and `cmsAccountId`

**Step 7: Create video reel** -- POST /api/v1/videos (200 credits)
- Build slides from carousel + images (see Video skill for full tutorial)
- Include `sourcePipelineRunId` from step 3
- Poll GET /api/v1/videos/{jobId} every 5s until "completed"

**Step 8: Post video to social media** -- POST /api/v1/social/post (0 credits)
- GET /api/v1/social/accounts to get connected account IDs
- Use the `contentId` from the video response with `contentType: "video"`

**Total: ~310 credits** (10 search + 100 pipeline + 200 video). CMS and social posting are free.

**Tip:** Use RSS feeds (POST /rss, 0 credits) instead of the news aggregator (10 credits) to source article URLs for free. Save your feed URLs once with PUT /rss, then fetch with `{ "useSavedFeeds": true }`.

---

### RSS-Based Workflow (Free Content Sourcing)

1. **Save RSS feeds:** PUT /api/v1/rss with `{ "feedUrls": ["https://techcrunch.com/feed/"] }`
2. **Fetch latest:** POST /api/v1/rss with `{ "useSavedFeeds": true, "keywords": ["AI"], "maxItemsPerFeed": 5 }`
3. **Pick best article** URL from the results
4. **Run pipeline:** POST /api/v1/pipelines on the chosen URL (100 credits)
5. Continue with save/publish/video as needed

---

### Behavioral Guidelines

- For operations costing 50+ credits (pipelines at 100, videos at 200), confirm the action and credit cost before proceeding. For cheap or free operations, proceed directly.
- Show real-time progress while polling async operations. Report the current status on each poll cycle.
- When a pipeline completes, summarize: article title, number of social posts, images found, carousel slides, and script availability.
- When creating a video from pipeline results, always include `sourcePipelineRunId`.
- Pipeline results are NOT auto-saved. Remind the user to save content (POST /content) before publishing.
- If the user asks to "do everything" or "full workflow", follow the Complete Workflow above.

---

### Polling Guide

**Pipelines:** Poll every 10 seconds.
- Status: "pending" -> "running" -> "completed" | "failed"
- Typical: 2-3 minutes. Max: 5 minutes.

**Videos:** Poll every 5 seconds.
- Status: "queued" -> "generating_audio" -> "rendering" -> "uploading" -> "completed" | "failed"
- "queued" can last 10-30 seconds (normal startup)
- "generating_audio" means TTS in progress (progress, not a stall)
- "rendering" is the longest phase
- Typical: 60-180 seconds. Max: 5 minutes.

**Images:** Synchronous but slow (5-15 seconds per image). Wait for the response.

**CRITICAL:** Do NOT stop polling on intermediate statuses. Do NOT report failure until status is actually "failed" or you have polled for the maximum duration.

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

- **Core Skill** (`generatebot-core`): All search, pipeline, RSS, content CRUD, and credits endpoints.
- **Video Skill** (`generatebot-video`): Detailed video creation tutorial with imageMode reference.
- **Publish Skill** (`generatebot-publish`): Social posting, CMS publishing, enrichment, brand voice, AI images.
- **Templates Skill** (`generatebot-templates`): Design and render canvas-based post image templates.