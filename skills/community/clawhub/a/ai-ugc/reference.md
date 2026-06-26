# RawUGC API -- Request/Response Reference

Condensed shapes for agent lookups. Base URL: `https://rawugc.com/api/v1`. Auth: `Authorization: Bearer <RAWUGC_API_KEY>`. Version: `RawUGC-Version: 2026-03-06`.

---

## Video Generation

### POST /videos/generate

**Request (application/json)**

- `model` (required): `sora-2-text-to-video` | `sora-2-image-to-video` | `kling-2.6/motion-control` | `veo3` | `veo3_fast`
- `prompt` (optional, required for text-to-video/veo3): string, 1-5000 chars
- `imageUrls` (optional, required for image-to-video/kling): string[], max 10. Veo3/veo3_fast accept up to 2.
- `videoUrls` (optional, required for kling): string[], max 1
- `aspectRatio` (optional): Sora: `portrait` | `landscape`. Veo3: `16:9` | `9:16` | `Auto`
- `nFrames` (optional, Sora only): `"10"` | `"15"`
- `selectedCharacter` (optional): string
- `characterOrientation` (optional, kling only): `image` | `video`
- `mode` (optional, kling only): `720p` | `1080p`

**Response 201**: `videoId` (vid_xxx), `model`, `status`, `creditsUsed`, `newBalance`, `estimatedCompletionTime`, `createdAt` (ms epoch)

### GET /videos/{videoId}

**Response 200**: `videoId`, `status` (`pending`|`processing`|`completed`|`failed`), `model`, `prompt`?, `creditsUsed`, `url`? (completed), `createdAt`, `completedAt`?, `failCode`?, `failMessage`?, `versions`? (MediaVersion[])

**MediaVersion**: `videoId`, `version` (int), `url`, `operation`? (`captions`|`overlay`), `createdAt`

### GET /videos

**Query**: `status`?, `limit`? (1-100, default 50), `page`? (default 1)

**Response 200**: `videos` (VideoResponse[]), `pagination` (`total`, `page`, `pageSize`, `hasMore`)

### POST /videos/captions

**Request**: `videoId` (required), `language`? (e.g. `en`)

**Response 200** (EditResponse): `videoId`, `url`, `version`, `operation`, `creditsUsed` (1)

### POST /videos/overlay

**Request**: `videoId` (required), `text` (required, 1-500), `position`? (`top`|`center`|`bottom`), `fontSize`? (8-200), `topBottomMargin`? (0-500), `strokeThickness`? (0-10)

**Response 200** (EditResponse): `videoId`, `url`, `version`, `operation`, `creditsUsed`

---

## Image Generation

### POST /images/generate

**Request**: `model` (required: `nano-banana-2` | `google/nano-banana-edit`), `prompt` (required, 1-20000), `imageUrls`? (required for edit, optional for text-to-image, max 14), `aspectRatio`? (nano-banana-2), `imageSize`? (nano-banana-edit), `resolution`? (`1K`|`2K`|`4K`), `outputFormat`? (`png`|`jpeg`|`jpg`), `googleSearch`? (boolean, nano-banana-2 only)

**Response 201**: `imageId` (img_xxx), `model`, `status`, `creditsUsed`, `newBalance`, `estimatedCompletionTime`, `createdAt`

### GET /images/{imageId}

**Response 200**: `imageId`, `status`, `model`, `prompt`, `url`? (completed), `imageSize`?, `resolution`?, `outputFormat`?, `creditsUsed`, `createdAt`, `completedAt`?, `failCode`?, `failMessage`?

### GET /images

**Query**: `status`?, `limit`? (1-100, default 20), `page`?

**Response 200**: `images` (ImageResponse[]), `pagination` (`total`, `page`, `pageSize`, `hasMore`)

---

## Music Generation

### POST /music/generate

**Request**: `prompt` (required, 1-2000), `model`? (`V3_5`|`V4`|`V4_5`|`V4_5PLUS`|`V4_5ALL`|`V5`, default V5), `instrumental`? (boolean, default true), `title`? (max 200), `style`? (max 500)

**Response 201**: `musicId` (mus_xxx), `model`, `status`, `creditsUsed` (3), `newBalance`, `estimatedCompletionTime`, `createdAt`

### GET /music/{musicId}

**Response 200**: `musicId`, `status`, `model`, `prompt`, `audioUrl`? (completed), `albumArtUrl`?, `duration`?, `title`?, `creditsUsed`, `createdAt`, `completedAt`?, `failCode`?, `failMessage`?

### GET /music

**Query**: `status`?, `limit`? (1-100, default 20), `page`?

**Response 200**: `tracks` (MusicResponse[]), `pagination` (`total`, `page`, `pageSize`, `hasMore`)

---

## Upload

### POST /upload

**Request**: `multipart/form-data`, field `file`. Accepted: `video/mp4`, `video/quicktime`, `video/webm`, `image/png`, `image/jpeg`, `image/webp`. Max 100MB.

**Response 200**: `url` (public URL for use in generation requests), `contentType`, `size` (bytes)

---

## Characters

### GET /characters

**Response 200**: `characters` (CharacterResponse[]), `count`, `adminCount`, `userCount`

### GET /characters/{characterId}

**CharacterResponse**: `_id`, `username`, `displayName`, `description`, `videoPreviewUrl`?, `type` (`admin`|`user`), `isActive`, `createdAt`, `updatedAt`

---

## Personas

### GET /personas

**Response 200**: `personas` (PersonaResponse[]), `count`

### POST /personas

**Request**: `name` (required, max 200), `description` (required, max 5000)

**Response 201**: `{ id }`

### GET /personas/{personaId}

**Response 200**: PersonaResponse

### PATCH /personas/{personaId}

**Request**: `name`?, `description`?

### DELETE /personas/{personaId}

**PersonaResponse**: `_id`, `organizationId`, `name`, `description`, `createdAt`, `updatedAt`

---

## Messaging

### GET /messaging

**Response 200**: `messages` (MessagingResponse[]), `count`

### POST /messaging

**Request**: `name` (required, max 200), `body` (required, max 5000)

**Response 201**: `{ id }`

### GET /messaging/{messageId}

### PATCH /messaging/{messageId}

**Request**: `name`?, `body`?

### DELETE /messaging/{messageId}

**MessagingResponse**: `_id`, `organizationId`, `name`, `body`, `createdAt`, `updatedAt`

---

## Products

### GET /products

**Response 200**: `products` (ProductResponse[]), `count`

### POST /products

**Request**: `name` (required, max 200), `photos` (required, URL[]), `description`? (max 1000), `messaging`? (max 5000)

**Response 201**: `{ id }`

### GET /products/{productId}

### PATCH /products/{productId}

**Request**: `name`?, `description`?, `photos`?, `messaging`?

### DELETE /products/{productId}

**ProductResponse**: `_id`, `name`, `description`, `photos`, `messaging`, `createdAt`, `updatedAt`

---

## Styles

### GET /styles

**Query**: `type`? (`video`|`image`)

**Response 200**: `styles` (StyleResponse[]), `count`

### POST /styles

**Request**: `name` (required, max 200), `description`? (max 1000), `type`? (`video`|`image`), `aspectRatio`? (`portrait`|`landscape`|`square`), `promptTemplate`? (max 5000, placeholders: `{productName}`, `{messaging}`, `{character}`)

**Response 201**: `{ id }`

### GET /styles/{styleId}

### PATCH /styles/{styleId}

**Request**: `name`?, `description`?, `aspectRatio`?, `promptTemplate`?

### DELETE /styles/{styleId}

**StyleResponse**: `_id`, `name`, `description`, `type`, `aspectRatio`, `styleId`, `promptTemplate`, `isAdmin`, `isStandard`

---

## Social Accounts

### GET /social/accounts

**Response 200**: `accounts` (SocialAccount[]), `count`

### POST /social/accounts

Sync accounts from scheduling provider. **Response 200**: `{ success }`

### DELETE /social/accounts/{accountId}

**Response 200**: `{ success }`

**SocialAccount**: `accountId`, `platform` (`tiktok`|`instagram`|`youtube`), `username`, `displayName`, `profilePicture`?, `isActive`

---

## Social Posts

### POST /social/posts

**Request**: `videoUrl` (required), `accountIds` (required, string[]), `mode` (required: `schedule`|`draft`|`now`), `scheduledFor`? (ms, required for schedule), `timezone`? (IANA, default UTC), `content`? (max 2200), `videoId`?, `publishToInbox`?, `tiktokPrivacyLevel`? (`SELF_ONLY`|`PUBLIC_TO_EVERYONE`|`MUTUAL_FOLLOW_FRIENDS`|`FOLLOWER_OF_CREATOR`), `tiktokAllowComment`?, `tiktokAllowDuet`?, `tiktokAllowStitch`?, `tiktokCommercialContentType`? (`none`|`brand_organic`|`brand_content`)

**Response 201**: SocialPost

### GET /social/posts

**Query**: `fromDate`? (ms), `toDate`? (ms), `includeDrafts`? (boolean)

**Response 200**: `posts` (SocialPost[]), `count`

### GET /social/posts/{postId}

### PATCH /social/posts/{postId}

**Request**: `content`?, `scheduledFor`?, `timezone`?, `accountIds`? (at least one field)

### DELETE /social/posts/{postId}

**Response 200**: `{ success }`

### POST /social/posts/{postId}/reschedule

**Request**: `scheduledFor` (required, ms), `timezone`?

### POST /social/posts/{postId}/publish

Immediately publish a draft.

**SocialPost**: `postId`, `platforms`, `status` (`draft`|`scheduled`|`published`|`failed`), `scheduledFor`?, `timezone`, `content`, `videoUrl`, `createdAt`, `publishedAt`?

---

## Viral Library

### GET /viral-library/videos/{videoId}

**Response 200**: ViralLibraryVideo

**ViralLibraryVideo**: `id`, `tiktokId`, `tiktokUrl`, `username`, `description`, `stats` (`views`, `likes`, `comments`, `shares`, `saves`), `hashtags`, `soundName`, `duration`, `thumbnailUrl`, `playUrl`, `analysis`? (VideoAnalysis)

**VideoAnalysis**: `hook`, `summary`, `whyItPerformed`, `attributesToCopy`, `hooksToTest`, `keyframes` (array: `timestamp`, `type`, `description`, `visual`, `audio`, `text`), `durationSeconds`, `tags`, `analyzedAt`

### GET /viral-library/search

**Query**: `q` (required, natural language), `limit`? (1-50, default 20)

**Response 200**: `results` (array of `{ video: ViralLibraryVideo, score: number }`), `query`, `total`

---

## Research

### POST /scrape-tiktok

**Request**: `query` (required, max 500), `mode`? (`keyword`|`hashtag`|`search`, default keyword), `limit`? (1-10, default 10)

**Response 200**: `scrapeId`, `count`, `videos` (array: `id`, `url`, `author`, `description`, `stats` {views, likes, comments, shares}, `duration`, `hashtags`, `thumbnail`?, `videoUrl`?)

### POST /content-plans

**Request**: `scrapeId` (required), `brief` (required, max 5000)

**Response 200**: `planId`, `scrapeId`, `brief`, `topWins`, `gapsToTest`, `blueprints` (array: `category`, `strategy`, `evidence`, `contentIdeas` [{`hook`, `openingShot`, `contentOutline`, `cta`}])

### GET /content-plans

**Response 200**: `plans` (array: `planId`, `scrapeId`, `brief`, `createdAt`), `count`

### POST /analyze-video

**Request**: `videoUrl` (required), `prompt`? (max 5000)

**Response 200**: `summary`, `hook`, `keyframes` (array: `timestamp`, `type`, `description`, `visual`, `audio`, `text`), `durationSeconds`, `tags`, `whyItPerformed`, `attributesToCopy`, `hooksToTest`

---

## Error body (ApiError)

All error responses use RFC 7807: `type`, `title`, `status`, `detail`?, `instance`?, `errors`? (Record<string, string[]>)

**Status codes**: 400 validation, 401 auth, 402 insufficient credits, 403 insufficient scope, 404 not found, 429 rate limit, 500 server error.

## Rate limit headers

All responses include: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (unix timestamp seconds).
