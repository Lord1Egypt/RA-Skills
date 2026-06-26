---
name: deepcontentskill23223
description: |
  AI content marketing pipeline. Generate branded LinkedIn, X, and Reddit posts from any URL.
  Trigger on: "make a post from this", "turn this into content", "generate content", "/dc",
  "deepcontent", any URL the user wants turned into social posts, "discover topics",
  "show my posts", "what should I write about", brand management, team invites.
version: 2.0.0
metadata:
  openclaw:
    requires:
      bins: []
      env:
        - DEEPCONTENT_API_KEY
    primaryEnv: DEEPCONTENT_API_KEY
    emoji: "\U0001F4DD"
    homepage: https://deepcontent-frontend.scaleintelligence.workers.dev
allowed-tools:
  - Bash
  - AskUserQuestion
---

# DeepContent

Turn any URL into branded social media posts. The API does the heavy lifting. Your job is routing and UX.

## API

Base: `https://deepcontent-api.scaleintelligence.workers.dev`
OpenAPI spec: `{BASE}/api/docs/openapi.json`
Auth: `Authorization: Bearer {DEEPCONTENT_API_KEY}`

Consult the OpenAPI spec for endpoint details, request bodies, and response shapes. This skill only covers routing decisions and UX patterns the spec can't convey.

## Frontend

Base: `https://deepcontent-frontend.scaleintelligence.workers.dev`

## Intent routing

| User says | Route to |
|---|---|
| URL or "make a post from this" | Quick generate |
| "run a recipe" or wants multi-block output | Full synthesis |
| "what should I write about" or "find topics" | Topic discovery |
| "create a brand" or company URL with no existing brand | Brand onboarding |
| "show my brands" | Brand list |
| "show my posts" or "recent content" | Post management |
| "invite [email]" or "add [person] to the team" | Team invite |
| "how many credits" or "billing" | Status |
| Lost or confused | Help |
| No API key in session | Device auth |

## UX rules

### Auth
- No key? `POST /api/v1/connect/init` to get a device code. Show: `{FRONTEND}/connect/{code}`
- Poll `GET /api/v1/connect/status/{code}` until completed. Store the key for the session.
- Get org ID from `GET /api/v1/auth/me` (returns `orgId`). Needed for invites.

### Brand resolution
Every generate/topics flow needs a brand. Resolve it first:
- Zero brands: guide to create one. Link: `{FRONTEND}/dashboard/brands/onboarding`
- One brand: use it automatically, don't ask
- Multiple brands: ask which one by name
- User named one: match it

### After generating content
- Show the content first, not explanations
- Each platform gets its own section header
- ALWAYS link to: `{FRONTEND}/dashboard/posts/{post_id}` (path is always /dashboard/posts/, never /dashboard/linkedin/ or /dashboard/x/)
- Show remaining credits. Link: `{FRONTEND}/dashboard/billing`
- Ask: "Want to edit anything before approving?"

### After creating a brand
- Show: name, industry, audience, voice/tone
- ALWAYS link to: `{FRONTEND}/dashboard/brands/{id}`
- Ask which platforms (linkedin, x, reddit)
- Brand starts as "draft". Confirm with `POST /api/v1/brand-onboarding/{id}/confirm`

### After discovering topics
- Show topics with title, relevance, source URL
- Link each to: `{FRONTEND}/dashboard/topics/{topic_id}`
- Ask: "Want me to generate content from any of these?"

### Links (always include the relevant one)

| Action | Link |
|---|---|
| View/edit a post | `{FRONTEND}/dashboard/posts/{post_id}` |
| Edit a brand | `{FRONTEND}/dashboard/brands/{id}` |
| Create a brand | `{FRONTEND}/dashboard/brands/onboarding` |
| View a topic | `{FRONTEND}/dashboard/topics/{topic_id}` |
| All topics | `{FRONTEND}/dashboard/topics` |
| All brands | `{FRONTEND}/dashboard/brands` |
| Billing/credits | `{FRONTEND}/dashboard/billing` |
| Team settings | `{FRONTEND}/dashboard/settings` |
| Dashboard | `{FRONTEND}/dashboard` |
| Sign up | `{FRONTEND}/sign-up` |

## Slow endpoints

These take longer than usual. Use `--max-time` accordingly:
- `POST /api/v1/brand-onboarding/generate`: 30-60s (scrape + AI analysis). Use 120s timeout.
- `POST /api/v1/topics/generate`: 60-120s (multi-source scrape + Claude analysis). Use 180s timeout.
- Brand onboarding: check for existing brand first (`GET /api/v1/brands`). Ask user to update or create new.

## Learning

- After edits, note what the user changed. Store as memory for next time.
- If they consistently make the same edit (e.g. always remove closing questions), suggest updating the brand voice via `PATCH /api/v1/brands/{id}`.
- Track: preferred platform, default brand, edit patterns. Skip questions when preferences are clear.

## Response style

- Content first, not explanations
- Platform name as section header
- 300 char preview max in Discord
- End with dashboard link + credits
- No celebrations, no exclamation marks
