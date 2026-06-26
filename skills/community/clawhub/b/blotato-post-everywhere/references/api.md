# Blotato API Reference

Base URL: `https://backend.blotato.com/v2`
Auth Header: `blotato-api-key: YOUR_API_KEY`
Content-Type: `application/json`

All creation ops are ASYNC — submit then poll for status.

---

## Endpoints

### User / Accounts
- `GET /users/me` — verify key, get user info
- `GET /users/me/accounts` — list connected accounts (get `accountId`)
- `GET /users/me/accounts?platform=twitter` — filter by platform
- `GET /users/me/accounts/{accountId}/subaccounts` — get `pageId` (Facebook/LinkedIn) or playlist (YouTube)

### Publishing
- `POST /posts` — create/publish a post (30 req/min)
- `GET /posts/{postSubmissionId}` — poll post status (60 req/min)

### Schedules
- `GET /schedules` — list future scheduled posts
- `PATCH /schedules/{id}` — update scheduled post
- `DELETE /schedules/{id}` — delete scheduled post

### Schedule Slots
- `GET /schedule/slots` — list recurring time slots
- `POST /schedule/slots` — create slots
- `POST /schedule/slots/next-available` — find next open slot for platform/account

---

## POST /posts — Request Body

```json
{
  "post": {
    "accountId": "98432",
    "content": {
      "text": "Post text here",
      "mediaUrls": [],
      "platform": "twitter",
      "additionalPosts": []
    },
    "target": {
      "targetType": "twitter"
    }
  },
  "scheduledTime": "2026-03-10T15:30:00Z"
}
```

### Scheduling Options (top-level, NOT inside `post`)
- `scheduledTime`: ISO 8601 timestamp — schedule at specific time
- `useNextFreeSlot: true` — schedule at next calendar slot
- Neither: publish immediately

### Supported Platforms
`twitter`, `linkedin`, `facebook`, `instagram`, `pinterest`, `tiktok`, `threads`, `bluesky`, `youtube`

### Required `target` fields per platform

| Platform  | targetType    | Required extra fields                                                                 |
|-----------|---------------|---------------------------------------------------------------------------------------|
| Twitter   | twitter       | none                                                                                  |
| LinkedIn  | linkedin      | none (optional: `pageId` for company page)                                            |
| Facebook  | facebook      | `pageId`                                                                              |
| Instagram | instagram     | none (optional: `mediaType`)                                                          |
| TikTok    | tiktok        | `privacyLevel`, `disabledComments`, `disabledDuet`, `disabledStitch`, `isBrandedContent`, `isYourBrand`, `isAiGenerated` |
| Pinterest | pinterest     | `boardId`                                                                             |
| Threads   | threads       | none                                                                                  |
| Bluesky   | bluesky       | none                                                                                  |
| YouTube   | youtube       | `title`, `privacyStatus`, `shouldNotifySubscribers`                                  |

### Twitter Thread example
```json
{
  "content": {
    "text": "Tweet 1",
    "mediaUrls": [],
    "platform": "twitter",
    "additionalPosts": [
      {"text": "Tweet 2", "mediaUrls": []},
      {"text": "Tweet 3", "mediaUrls": []}
    ]
  }
}
```

### Notes
- `content.platform` must match `target.targetType`
- `pageId` for Facebook/LinkedIn: fetch from `/users/me/accounts/{id}/subaccounts`
- `boardId` for Pinterest: NOT available via API — must ask user
- Media: pass public URL in `mediaUrls` directly, no upload needed

---

## Media Upload

### Option 1: Public URL (simplest)
Pass directly into `mediaUrls` — Blotato handles the rest. No upload needed.

### Option 2: Upload from URL → Blotato storage
```
POST /media
{ "url": "https://example.com/image.jpg" }
→ { "url": "https://database.blotato.com/..." }
```
Limit: 200MB. Rate limit: 30 req/min.

### Option 3: Presigned Upload (local files, up to 1GB)
**Step 1:** Get presigned URL
```
POST /media/uploads
{ "filename": "photo.jpg" }
→ { "presignedUrl": "...", "publicUrl": "..." }
```
**Step 2:** PUT file to presignedUrl with correct Content-Type header
```
PUT {presignedUrl}
Content-Type: image/jpeg
[binary file data]
```
**Step 3:** Use `publicUrl` in `mediaUrls` when posting.

Rate limit: 120 req/min. Max size: 1GB.

---

 (for content adaptation)

| Platform  | Limit           |
|-----------|-----------------|
| Twitter/X | 280 chars/tweet (threads: multiple tweets) |
| LinkedIn  | 3000 chars      |
| Facebook  | 63206 chars     |
| Instagram | 2200 chars      |
| Threads   | 500 chars       |
| Bluesky   | 300 chars       |
| TikTok    | 2200 chars (caption) |
| Pinterest | 500 chars (desc)|
| YouTube   | 5000 chars (desc)|

## Platform Content Styles

| Platform  | Optimal style |
|-----------|---------------|
| Twitter/X | Short, punchy, hashtags, break into thread if long |
| LinkedIn  | Professional, story-driven, no excessive hashtags |
| Facebook  | Conversational, can be longer, emojis OK |
| Instagram | Visual-first, emoji-heavy, hashtags at end |
| Threads   | Casual, conversational |
| Bluesky   | Similar to Twitter, concise |
| TikTok    | Trendy, casual, hashtags |
| Pinterest | Descriptive, keyword-rich |
| YouTube   | Detailed description, keywords, timestamps if applicable |
