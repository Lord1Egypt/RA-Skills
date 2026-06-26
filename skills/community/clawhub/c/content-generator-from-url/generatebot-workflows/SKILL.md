---
name: generatebot-workflows
description: End-to-end content automation workflows, credit cost reference, and polling patterns for the GenerateBot API. Orchestrates multi-step pipelines from topic research to publishing. Use when the user wants to automate content creation, plan a content pipeline, estimate API costs, batch-generate content, or build a search-to-publish workflow.
emoji: ⚡
homepage: https://generatebot.com
metadata:
  openclaw:
    primaryEnv: GENERATEBOT_API_KEY
    requires:
      env:
        - GENERATEBOT_API_KEY
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