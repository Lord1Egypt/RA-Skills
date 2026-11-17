---
name: admakeai-api
description: >-
  Create, edit, and ship ad creative via the AdMakeAI API — ad images, edits,
  batch ad sets, ad copy, UGC video, Meta uploads/analytics. Use it when a
  request is about making, publishing, or reporting ads. Default to read and
  list calls; confirm every write or credit-spending action with the user.
  Trigger words: create, generate, make, design, produce, brainstorm, batch,
  vary, mock up, upload, publish, push, ship, draft, list, browse, find, get,
  fetch, look up, audit, or recap ads, ad creatives, product photos,
  lifestyle shots, UGC, ad copy, hooks, headlines, ad sets, campaigns,
  competitor ads, competitor research, Meta ads, Facebook ads, or ad
  analytics. Also use when the user mentions AdMakeAI, admakeai, ad images,
  ad generator, ad image API, or wants to know their AdMakeAI credit
  balance.
license: MIT-0
version: 1.1.0
compatibility: Requires network access and an AdMakeAI account
allowed-tools: Bash, Read, Write, WebFetch
homepage: https://admakeai.com
metadata:
  openclaw:
    emoji: "🎨"
    homepage: https://admakeai.com
    requires:
      env:
        - ADMAKEAI_API_KEY
      bins:
        - curl
    primaryEnv: ADMAKEAI_API_KEY
    envVars:
      - name: ADMAKEAI_API_KEY
        required: true
        description: >-
          AdMakeAI API key (amai_live_...) — create one at
          https://admakeai.com/dashboard/integrations/api
    tags:
      - ad-generation
      - image-generation
      - ai-ads
      - facebook-ads
      - meta-ads
      - mcp
      - admakeai
---

# AdMakeAI API

Programmatic ad-creative generation, Meta campaign drafting, and Meta Ads reporting. 60+ tools across projects, image generation and editing, ad copy, batch ad sets, UGC video, competitor research, Facebook upload, and analytics.

**Base URL:** `https://admakeai.com/api/v1`
**MCP URL:** `https://admakeai.com/api/mcp`
**Interactive reference:** https://admakeai.com/api/docs

Get an API key at https://admakeai.com/dashboard/integrations/api

## Authentication

Every request needs the user's API key as a header. Read it from `$ADMAKEAI_API_KEY`; keys look like `amai_live_...`.

```bash
curl -H "x-api-key: $ADMAKEAI_API_KEY" \
  https://admakeai.com/api/v1/user.me
```

`Authorization: Bearer <key>` also works. Never echo the key back to the user or paste it into a file.

## How to call

Every tool has one canonical tRPC dotted path — `adGeneration.create`. Two transports expose the same allowlist:

| Transport | Name / path |
| --- | --- |
| REST | `https://admakeai.com/api/v1/adGeneration.create` — dotted path, unchanged |
| MCP | tool `adGeneration__create` — every `.` becomes `__` |

- All POST bodies are JSON. All GET inputs go in `?input=<URL-encoded JSON>`.
- REST responses are wrapped as `{ ok, tool, data }`; MCP returns the unwrapped result inside `content[0].text`.

```bash
# 1. find the project (brand) to generate for
curl -H "x-api-key: $ADMAKEAI_API_KEY" \
  https://admakeai.com/api/v1/adResearch.listProjects

# 2. create an ad image
curl -X POST -H "x-api-key: $ADMAKEAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"projectId":"<PROJECT_ID>","prompt":"Minimalist matcha product ad, lifestyle scene","adType":"product_showcase","aspectRatio":"4:5","quality":"low"}' \
  https://admakeai.com/api/v1/adGeneration.create

# 3. poll until COMPLETED
curl -H "x-api-key: $ADMAKEAI_API_KEY" \
  "https://admakeai.com/api/v1/adGeneration.getById?input=%7B%22id%22%3A%22<ID>%22%7D"
```

## The one thing to get right: projects

Every image generation is scoped to a **project** - the brand record holding
the product summary, audience, value proposition and logo. `adGeneration.create`
expands your short brief into a full image prompt using that brief, which is
why ads come back looking like ads (headline, badge, CTA baked in) instead of
stock photos.

So `projectId` is required on `adGeneration.create`, and the rule is always
the same:

1. Call `adResearch.listProjects` before the first generation of a session.
2. One project? Use it. Several? Pick the one the user's request is clearly
   about (brand name, product, URL they mentioned) and say which one you
   picked. Still ambiguous? **Ask.** Never guess an id and never generate into
   the wrong brand - that spends their credits on the wrong product.
3. No projects at all? You cannot create one through this API. Tell the user
   to set their brand up at https://admakeai.com/dashboard first.

`adResearch.getProject` gives you the full brief; read it when the user's
request depends on brand details (audience, positioning, what they actually
sell).

`adGeneration.generateImage` and `videoGeneration.start` also take a
`projectId` — for `generateImage` it is credit scoping only, nothing from the
brief reaches the prompt.

### Per-procedure spec

Hit the interactive reference for typed inputs and example payloads:

```
https://admakeai.com/api/docs
```

Or fetch the rendered HTML and grep — every tool is listed by its dotted path.

## Intent routing

Pick the right tool from natural-language intent. **Read tables top-to-bottom; first match wins.**

### Account & credits

| User says... | Tool | Notes |
| --- | --- | --- |
| "what's my balance / credits" | `user.getCredits` | Cheapest read. Returns `{ credits }`. |
| "show my profile / plan" | `user.me` | Includes credits, subscription, plan name. |

### Generate ad images

Two renderers, same credit cost, very different output. Choose deliberately:

| Tool | What it renders |
| --- | --- |
| `adGeneration.create` | **A finished ad.** A creative-director model rewrites your brief into the real image prompt using the project's brand brief, and that rewrite always adds a headline, a subline, a CTA button, and the project logo when the project has one. Negative instructions in the prompt ("no text", "no logo", "nothing but the product") **cannot** suppress them. |
| `adGeneration.generateImage` | **Exactly your prompt.** It goes to the image model verbatim — no creative-director rewrite, no brand brief, no added headline/subline/CTA, no logo. The image contains only what the prompt stipulates. |

| User says... | Tool | Notes |
| --- | --- | --- |
| "make / generate / create an ad", "design a product ad" | `adGeneration.create` | Single image. Required: `projectId`, `prompt` (a brief, not a finished prompt). Optional: `adType`, `aspectRatio`, `quality`, `referenceImageUrls`, `inputImageId` (uploaded photo), `referenceAdId` / `referenceInspirationId` to remix. |
| "no text on it", "just the product", "a clean product / lifestyle photo", "put exactly this headline on it" | `adGeneration.generateImage` | Required: `projectId` (credit scoping only), `prompt` (used verbatim — write the full image prompt yourself). Optional: `aspectRatio`, `quality`, `referenceImageUrls`, `inputImageId`. |
| "edit / change / restyle this image", "swap the background", "make it 9:16" | `adGeneration.edit` | Image-to-image. Source is `sourceAdId` (one of their generations) or `sourceImageUrl` (any URL). `editInstructions` reaches the model close to literally. |
| "remix this competitor ad" | `adGeneration.create` with `referenceInspirationId` | Save the competitor ad first with `adResearch.saveInspiration`. |
| "give me 5 variations", "batch generate", "test different hooks" | `adSet.create` then `adSet.generateBatch` | The set holds the shared brief; the batch call holds the per-variation direction. `adSet.suggestDirections` will invent the angles for you. |
| "use my product photo / logo as reference" | `upload.uploadImageBase64` → pass the returned id as `inputImageId` | Accepts JPEG/PNG/WebP base64. Already uploaded? `upload.getUserImages`. Brand assets already in the project? `project.getAssets`. |

After enqueueing, **always tell the user** the generation is async and offer to poll.

### Ad copy

| User says... | Tool | Notes |
| --- | --- | --- |
| "write copy / headlines / hooks for this ad" | `adCopyGeneration.generate` | Needs the finished `imageUrl`. Pass `projectId` so it uses the brand brief. Returns up to 5 variations with hook angles. |
| "what copy styles are there" | `adCopyGeneration.getMessagingStyles` | clickbait / professional / UGC / direct response / storytelling / ... |

### Video ads

| User says... | Tool | Notes |
| --- | --- | --- |
| "make a UGC video ad", "video version of this" | `videoGeneration.start` | Needs `projectId`. Costs 5 / 15 / 50 credits for low / medium / high. |
| "is my video done" | `videoGeneration.getStatus` | Poll until COMPLETED. Videos take minutes, not seconds. |
| "show my videos" | `videoGeneration.list` / `videoGeneration.listPending` | |

### Competitor research

| User says... | Tool | Notes |
| --- | --- | --- |
| "what ads is <brand> running" | `adResearch.searchCompanies` then `adResearch.getCompanyAds` | Live Meta Ad Library. Works for any advertiser, no project needed. |
| "add <brand> as a competitor" | `adResearch.addCompetitors` | Scrapes their ads into the project. |
| "show competitor ads for my project" | `adResearch.getScrapedAds` | Sort by `longest_running` to find their proven winners. |
| "what have we got on competitor X" | `adResearch.getCompetitorPreview` | Quick preview of the ads already scraped for one competitor. |
| "details of that competitor ad" | `adResearch.getAdDetails` | Needs `projectId` + `scrapedAdId`. |
| "save that one for inspiration" | `adResearch.saveInspiration` | Returns an inspiration ID for `adGeneration.create`. |
| "what have we saved as inspiration" | `adResearch.getSavedInspirations` | Lists saved ads with their inspiration IDs. |
| "re-scrape / refresh competitor ads" | `adResearch.scrapeCompetitor` | Async; poll `adResearch.pollStatus`. |

### Find existing ads

| User says... | Tool | Notes |
| --- | --- | --- |
| "show my recent ads" | `adGeneration.getRecent` | Default 12. Returns image URLs + prompts. |
| "list / browse / paginate my ads" | `adGeneration.list` | Cursor-paginated. |
| "search my ads for X" | `adGeneration.searchAll` | Full-text on prompts. |
| "what's still rendering" | `adGeneration.listPending` | Only PENDING status. |
| "show the details of ad <id>" | `adGeneration.getById` | Returns full record. |
| "star / favorite that one", "this is the winner" | `adGeneration.toggleFavorite` | Free toggle. Good way to mark the pick of a batch. |

### Ad sets

| User says... | Tool | Notes |
| --- | --- | --- |
| "list my ad sets" | `adSet.list` | Page-paginated. |
| "show ad set <id>" | `adSet.get` | Includes `generalInstructions`. |
| "what's in this ad set" | `adSet.getGenerations` | List of generations in that set. |
| "create an ad set" | `adSet.create` | Free. Holds project + shared brief + ad type + quality + aspect ratio. |
| "change the brief / quality of the set" | `adSet.update` | |
| "generate a batch in ad set X" | `adSet.generateBatch` | See generate-images table. |
| "what angles should we test" | `adSet.suggestDirections` | Free. Model-written creative directions to feed back in as per-variation instructions. |

### Projects

| User says... | Tool | Notes |
| --- | --- | --- |
| "list my projects" | `adResearch.listProjects` | One entry per brand/product. Start here, every session. |
| "set up a new brand / project" | *(none)* | Not available to agents. Point the user at https://admakeai.com/dashboard. |
| "show the brand brief" | `adResearch.getProject` | Brief + competitors + research jobs + ad counts. |
| "fix / update the brief, audience, industry" | `project.updateBrief` | A sharper brief improves every later generation. |
| "what product photos do we have" | `project.getAssets` | Asset URLs usable as `referenceImageUrls`. |
| "upload this photo" | `upload.uploadImageBase64` | Returns an image ID + public URL for generation or campaign drafts. |
| "what have I uploaded before" | `upload.getUserImages` | Newest first, paginated. |
| "is the research done" | `adResearch.pollStatus` | Pipeline stage + running scrape jobs. |

### Facebook ad accounts

| User says... | Tool | Notes |
| --- | --- | --- |
| "show my connected fb accounts" | `facebookConnection.list` | Returns ad accounts + Pages with cached identity. |
| "list campaigns" | `facebookUpload.getCampaigns` | Needs `connectionId` + `adAccountId`. Cold cache triggers a Meta refresh. |
| "list ad sets in campaign X" | `facebookUpload.getAdSets` | Needs `connectionId` + `campaignId`. |

### Upload generated ads to Meta

| User says... | Tool | Notes |
| --- | --- | --- |
| "preflight / validate this for fb" | `facebookUpload.runPreflight` | Checks image dims, copy length. Free, no live action. |
| "upload / publish / push this ad to meta" | `facebookUpload.request` | **DANGEROUS — creates a real ad on Meta. Costs 3 credits.** Always confirm with the user first. |
| "show my uploaded ads" | `facebookUpload.list` | Filterable by account + state. |
| "status of upload <id>" | `facebookUpload.get` | Returns Meta IDs + state. |

### Meta campaign drafts

| User says... | Tool | Notes |
| --- | --- | --- |
| "what creatives can we reuse from past uploads" | `facebookCampaignDraft.sourceAssets` | Read-only. Resolves previously-uploaded Meta ads into reusable creative assets for a draft. |
| "show me the draft before we push it" | `facebookCampaignDraft.getAgentDraft` | Read-only. Fetch a saved agent-created draft by draft ID. |
| "push that draft to meta" | `facebookCampaignDraft.pushAgentDraft` | **DANGEROUS.** Pushes a saved draft to Meta as draft campaigns / ad sets / ads. Confirm first. |
| "build a whole campaign from these images" | `facebookCampaignDraft.pushDraftCampaign` | **DANGEROUS.** Creates Meta draft campaigns / ad sets / ads from explicit campaign data, ad sets, ad copy and image URLs (raw external URLs allowed). Confirm first. |

Both push tools create real objects inside the user's Meta ad account. They land as drafts rather than live ads, but they are still writes to Meta — read the plan back to the user and get an explicit yes before calling.

### Meta analytics

All read-only and free.

| User says... | Tool | Notes |
| --- | --- | --- |
| "how did the account do last month", "total spend / ROAS" | `zernioAnalytics.accountOverview` | Account-level spend, impressions, clicks, CTR, CPC, conversions, ROAS for a range like `last_30_days`, with previous-period comparison. Best first call. |
| "campaign tree", "what's the structure" | `zernioAnalytics.tree` | Campaign → ad set → ad hierarchy. |
| "performance over time", "timeline" | `zernioAnalytics.timeline` | Time-series for an ad account. |
| "list / recap campaigns" | `zernioAnalytics.listCampaigns` | Includes rolled-up metrics. |
| "list ads in campaign X" | `zernioAnalytics.listAds` | Filterable by campaign / ad set. |
| "details of ad <id>" | `zernioAnalytics.getAd` | Metadata + creative. |
| "daily analytics for ad <id>" | `zernioAnalytics.getAdAnalytics` | Spend, CTR, CPC, conversions. |
| "what are people saying about this ad" | `zernioAnalytics.getAdComments` | Public comments on the boosted post behind a Meta ad (Facebook or Instagram placement). |

### Changing ad status on Meta

Not available. `zernioAnalytics.pauseAd` / `.resumeAd` / `.pauseCampaign` /
`.resumeCampaign` / `.pauseAdSet` / `.resumeAdSet` are **currently disabled and
fail closed**, so don't offer to pause, stop, resume or launch anything. Tell
the user to change status in Meta Ads Manager.

**We never expose delete anywhere** — not on AdMakeAI ads or ad sets, and not on live Meta resources.

## Credit costs

Generation tools and Meta uploads spend credits from the user's plan. Every read (list / get / analytics) is free.

| Tool | Cost |
| --- | --- |
| `adGeneration.create`, `adGeneration.generateImage`, `adGeneration.edit` | 2 (low) / 8 (high) / 20 (ultra) credits |
| `adSet.generateBatch` | `count × per-generation cost`. A batch of 10 high-quality images = 80 credits. |
| `videoGeneration.start` | 5 (low) / 15 (medium) / 50 (high) credits per video |
| `facebookUpload.request` | 3 credits per upload (`facebookUpload.runPreflight` is free) |
| `adCopyGeneration.generate`, `adSet.create` / `.update` / `.suggestDirections`, `adGeneration.toggleFavorite`, `project.*`, `upload.*`, `adResearch.*` | Free |
| Everything else | Free unless the underlying procedure says otherwise. |

Failed generations are refunded automatically.

**Always call `user.getCredits` before a batch of >10 generations** and warn the user if the balance is close.

## Pagination

List endpoints use one of three patterns:

| Pattern | Used by | How to advance |
| --- | --- | --- |
| `{ page, perPage }` | `adSet.list`, `adSet.getGenerations`, `videoGeneration.list`, `zernioAnalytics.listAds`, `zernioAnalytics.listCampaigns` | Increment `page`. |
| `{ limit, cursor }` | `adGeneration.list`, `adGeneration.searchAll`, `adResearch.listProjects`, `upload.getUserImages` | Pass the `nextCursor` from the previous response. |
| `{ limit, offset }` | `adResearch.getScrapedAds`, `adResearch.getSavedInspirations` | Increment `offset` by `limit`. |

Stop paginating when you have what the user asked for — agents tend to fetch too many pages.

## Common optional params

These appear on multiple tools and have the same meaning everywhere:

- `projectId`: the brand to generate for. Required on `adGeneration.create`, `adGeneration.generateImage`, `adSet.create`, `videoGeneration.start`.
- `aspectRatio`: `"1:1" | "4:5" | "9:16" | "16:9"`. Defaults to `"1:1"`. Use `"4:5"` for Instagram feed, `"9:16"` for Reels/Stories, `"16:9"` for YouTube/desktop.
- `quality`: `"low" | "high" | "ultra"`. Defaults to `"low"`. Use `"low"` while exploring angles, `"high"` for the one they'll actually run.
- `adType`: `"product_showcase" | "promotional" | "testimonial" | "lifestyle" | "comparison" | "announcement"`. Defaults to `"product_showcase"`. Only meaningful on `adGeneration.create` and `adSet.create`.
- `inputImageId`: ID of an uploaded product photo (from `upload.uploadImageBase64`) to use as a reference.

## Prompt patterns for `adGeneration.create`

`prompt` is a **creative brief, not a finished image prompt** - the renderer
expands it with the project's brand brief, then lays on headline, badge and
CTA. Describe the scene and the angle; don't hand-write the whole prompt.

Good briefs are concrete and visual. Bad ones are abstract or list-y.

| User intent | Good prompt template |
| --- | --- |
| Product on lifestyle background | `"<Product> placed on <surface> with <prop>, soft natural light, <style> aesthetic"` |
| Selfie-style UGC | `"First-person selfie of a <demo> holding <product>, casual <setting>, iPhone photo aesthetic"` |
| Before/after | `"Split-screen: left side <before state>, right side <after state with product>, clean comparison"` |
| Bold statement | `"<Product> on <bg color>, oversized typography reading '<headline>', minimalist composition"` |

If the user gives only a tagline ("matcha for tired founders") and no visual, **ask them one clarifying question** about setting/mood before generating.

For `adGeneration.generateImage` the opposite applies: you are writing the
final prompt, so be fully specific about subject, lighting, lens, background
and any on-image text — nothing is added for you.

## Known limitations

- Generation is **async**. `adGeneration.create` returns immediately with `{ id, status: "PENDING", creditCost, ... }`. Poll `adGeneration.getById` every 3-5 seconds until `status === "COMPLETED"`. Typical completion: 20-60s low-quality, 60-120s high-quality. The returned record's `prompt` field stays empty until the worker expands the brief.
- `adGeneration.create` needs a `projectId` from `adResearch.listProjects`. Projects cannot be created through the API - without one there is no brand brief to render against, so send the user to the dashboard.
- **Pause/resume through this API is currently disabled.** All six `zernioAnalytics.pause*` / `resume*` tools fail closed; use Meta Ads Manager for status changes.
- The free plan has a **daily generation cap**. The error is `FORBIDDEN: daily limit reached`. Tell the user to upgrade at `/pricing`.
- Facebook tools require the user to have **connected a Facebook account** in the dashboard first. If they haven't, `facebookConnection.list` returns empty; nudge them to https://admakeai.com/dashboard/integrations/facebook.
- The user has at most **5 active API keys** at a time. If creation fails with `FORBIDDEN: You already have 5 active API keys`, ask them to revoke one in the dashboard.
- We deliberately never expose **delete** on AdMakeAI ads, ad sets, or Meta resources. If the user asks to "delete" something, tell them it has to be done in the AdMakeAI web app or Meta Ads Manager.
