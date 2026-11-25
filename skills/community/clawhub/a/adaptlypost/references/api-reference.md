# AdaptlyPost API Reference

Base URL: `https://post.adaptlypost.com/post/api/v1`
Auth: `Authorization: Bearer <api-token>` header. Tokens start with the `adaptly_` prefix.

The same header also accepts a WorkOS OAuth token, which is how the hosted MCP server authenticates. For a skill, use an `adaptly_` token.

## Roles and permissions

Every key carries the workspace role chosen when it was created. Its permissions are that role's set intersected with the current permissions of the member who created it, so a key never does more than its creator: demoting the creator shrinks the key on the next request, and removing the creator from the workspace revokes it. An OAuth token reaches every workspace its member belongs to: `GET /workspaces` lists them, the `X-Workspace-Id` header picks one per request, and each workspace applies the member's own role there. An API key belongs to one workspace, so a skill using an `adaptly_` key never sends that header.

| Role | Permissions |
| --- | --- |
| `admin` | every permission below |
| `editor` | `workspace.read`, `posts.read`, `posts.draft`, `posts.others`, `posts.schedule`, `posts.publish`, `posts.delete`, `media.upload`, `accounts.read`, `analytics.read`, `analytics.sync`, `ai.generate`, `members.read`, `tokens.own`, `webhooks.read`, `webhooks.manage`, `signature.manage`, `inbox.read`, `inbox.reply` |
| `contributor` | `workspace.read`, `posts.read`, `posts.draft`, `media.upload`, `accounts.read`, `analytics.read`, `ai.generate`, `members.read`, `tokens.own`, `inbox.read` |
| `viewer` | `workspace.read`, `posts.read`, `accounts.read`, `analytics.read`, `members.read`, `webhooks.read`, `inbox.read` |

Which permission each endpoint needs:

| Endpoint | Permission | Roles |
| --- | --- | --- |
| `GET /social-posts`, `GET /social-posts/:id`, `GET /social-posts/:id/results`, `GET /recurring-posts`, `GET /recurring-posts/:id` | `posts.read` | all |
| `POST /social-posts` with `saveAsDraft: true`; `PATCH /social-posts/:id` and `DELETE /social-posts/:id` on a `DRAFT`; `POST /social-posts/:id/unschedule` on a dated `DRAFT` | `posts.draft` | admin, editor, contributor |
| `POST /social-posts` and `POST /social-posts/:id/publish` with a future `scheduledAt` (so every `POST /social-posts` with `recurrence`); `POST /social-posts/:id/publish` without `scheduledAt` or `publishNow` on a draft whose planned date is in the future; `PATCH /social-posts/:id` and `POST /social-posts/:id/unschedule` on a post that is not a `DRAFT`; `POST /social-posts/bulk`; `POST /recurring-posts/:id/pause`, `POST /recurring-posts/:id/resume` | `posts.schedule` | admin, editor |
| `POST /social-posts` without `scheduledAt` or with a past one; `POST /social-posts/:id/publish` with a past `scheduledAt`, with `publishNow: true`, or without either on a post that has no future planned date; `POST /social-posts/:id/retry`; `POST /social-posts/bulk` with any item due now or earlier | `posts.publish` | admin, editor |
| `DELETE /social-posts/:id` on a post that is not a `DRAFT`; `DELETE /recurring-posts/:id` | `posts.delete` | admin, editor |
| Any write on a post or recurring post another member created | the row above, plus `posts.others` | admin, editor |
| `POST /upload-urls` | `media.upload` | admin, editor, contributor |
| `GET /social-accounts`, `GET /linkedin-organizations/lookup` | `accounts.read` | all |
| `GET /social-accounts/:id/instagram-audio`, `GET /social-accounts/:id/pinterest-boards`, `GET /social-accounts/:id/youtube-playlists`, `GET /social-accounts/:id/wordpress-categories`, `POST /social-posts/validate`, `POST /social-posts/bulk/validate` | `posts.draft` | admin, editor, contributor |
| `POST /social-accounts/:id/check`, `DELETE /social-accounts/:id`, `POST /connect-links`, `DELETE /connect-links/:token` | `accounts.manage` | admin |
| `GET /workspaces` | none, any valid key | all |
| `POST /workspaces`, `DELETE /workspaces/:id` | `workspace.manage`, and the key's creator must be an organization owner or admin | admin |
| `GET /members` | `members.read` | all |
| `DELETE /members/:userId`, `GET /invitations`, `POST /invitations`, `DELETE /invitations/:id` | `members.manage` | admin |
| `DELETE /organization/members/:userId` | `members.manage`, and the key's creator must be an organization owner or admin | admin |
| `GET /webhooks`, `GET /webhooks/:id` | `webhooks.read` | admin, editor, viewer |
| `POST /webhooks`, `PATCH /webhooks/:id`, `DELETE /webhooks/:id`, `POST /webhooks/:id/test` | `webhooks.manage` | admin, editor |
| `GET /analytics/*` | `analytics.read` | all |
| `POST /analytics/sync` | `analytics.sync` | admin, editor |
| `POST /ai/*`, `GET /ai/images/:jobId` | `ai.generate` | admin, editor, contributor |
| `GET /inbox/*`, `POST /inbox/refresh` | `inbox.read` | all |
| Every other `POST`, `PUT` and `DELETE` under `/inbox` (replies, messages, review replies, hide, unhide, like, unlike, delete, status changes) | `inbox.reply`, plus an active plan | admin, editor |

The permission is also written into each operation's description in `GET /openapi.json`.

## Endpoints

### GET /social-accounts

List all connected social media accounts for the account group tied to this API token.

**Response:**

```json
{
  "accounts": [
    {
      "id": "cmlxmnxn20006hzpzvo291ckg",
      "platform": "INSTAGRAM",
      "displayName": "John Doe",
      "username": "johndoe",
      "avatarUrl": "https://...",
      "status": "active"
    },
    {
      "id": "cmlxmnxn20006hzpzvo291abc",
      "platform": "FACEBOOK",
      "displayName": "My Business Page",
      "username": "",
      "avatarUrl": "",
      "status": "unauthorized",
      "unauthorizedReason": "The session has been invalidated because the user changed their password.",
      "pageId": "123456789012345"
    }
  ]
}
```

Platform values: `TIKTOK`, `INSTAGRAM`, `FACEBOOK`, `TWITTER`, `YOUTUBE`, `LINKEDIN`, `THREADS`, `BLUESKY`, `MASTODON`, `PINTEREST`, `GOOGLE_BUSINESS`, `TELEGRAM`, `TUMBLR`, `WORDPRESS`

**Notes:**

- Facebook accounts represent pages, not personal profiles
- For Facebook, pass the `id` field in `pageIds` when creating posts. The extra `pageId` field is the page's public ID on facebook.com (shown since pages have no `username`); `pageIds` and `POST /social-accounts/:id/check` accept it as well
- LinkedIn and YouTube accounts may have empty `username`
- Bluesky `username` is the handle (e.g., `user.bsky.social`)
- Mastodon `username` is the full handle with the server (e.g., `user@mastodon.social`)
- Google Business Profile accounts (`GOOGLE_BUSINESS`) are business locations: `displayName` is the location title and `username` is empty. Pass the `id` in `googleBusinessConnectionIds`
- Instagram accounts carry `supportsInstagramAudio`: `true` when the account was connected through Facebook, which adding Instagram audio to Reels needs
- Telegram accounts (`TELEGRAM`) are channels and groups: `displayName` is the chat title, `username` is the public @username without the `@` (empty for a private chat) and `avatarUrl` is empty. Pass the `id` in `telegramConnectionIds`. The API cannot connect a Telegram chat; the user adds the AdaptlyPost bot to the chat and sends it the connect code from the Connectors page in the app
- Tumblr accounts (`TUMBLR`) are blogs; pass the `id` in `tumblrConnectionIds`
- WordPress accounts (`WORDPRESS`) are self-hosted WordPress sites (5.6 or later, over HTTPS); pass the `id` in `wordpressConnectionIds`. The API cannot connect a Tumblr blog or a WordPress site; the user connects them on the Connectors page in the app
- `status` is `active` or `unauthorized`. An unauthorized account stays listed but the platform rejected its token (a locked Facebook profile, a security checkpoint, a page the user lost access to). `POST /social-posts` refuses it with a 400 until the user reconnects it in the dashboard, so skip it when scheduling and tell the user to reconnect. `unauthorizedReason` is the platform's own message. Registered webhooks receive `account.unauthorized` the moment this happens

### POST /social-accounts/:id/check

Asks Facebook whether the page token still works, right now. Pages are also checked automatically twice a day. `:id` is the account `id` from `/social-accounts` or the Facebook `pageId`. Facebook pages only; other platforms return 400.

**Response:**

```json
{
  "id": "cmlxmnxn20006hzpzvo291abc",
  "platform": "FACEBOOK",
  "displayName": "My Business Page",
  "pageId": "123456789012345",
  "status": "unauthorized",
  "unauthorizedReason": "The session has been invalidated because the user changed their password.",
  "checkedAt": "2026-09-13T09:10:00.000Z"
}
```

A rejected token marks the page `unauthorized` and fires `account.unauthorized`; a working token clears an earlier mark. Use it before a scheduling run when the user has just reconnected, or when a post failed with a token error and you want to confirm the page is back.

### DELETE /social-accounts/:id

Disconnects the account from the workspace, the same as removing it on the Connectors page: the stored login is deleted, the account comes off every pending and recurring post, and it stops counting toward the plan. It works on any `status`, so an `unauthorized` account can be cleaned up without reconnecting it. `:id` is the account `id` from `/social-accounts` or the Facebook `pageId`; for Facebook only that page goes, and other pages from the same login stay connected. A removed Telegram chat stops getting posts, but the bot stays in the chat until someone removes it in Telegram. Returns 404 when the workspace does not hold the account. It cannot be undone, so confirm with the user first.

**Response:**

```json
{
  "id": "cmlxmnxn20006hzpzvo291abc",
  "platform": "FACEBOOK",
  "displayName": "My Business Page",
  "pageId": "123456789012345",
  "removed": true
}
```

### GET /social-accounts/:id/instagram-audio

Search Instagram music and original sounds to add to a Reel. `:id` is the Instagram account `id` from `/social-accounts`, and the account needs `supportsInstagramAudio: true`.

**Query parameters:**

- `audioType` (string, required): `music` or `original_sound`
- `searchQuery` (string, optional): Keyword filter, max 100 characters. Leave it out for trending audio

**Response:**

```json
{
  "audio": [
    {
      "audioId": "1234567890",
      "audioType": "music",
      "title": "Summer Nights",
      "displayArtist": "The Band",
      "durationMs": 184000,
      "coverArtworkUrl": "https://...",
      "previewUrl": "https://...",
      "instagramUrl": "https://www.instagram.com/reels/audio/1234567890/",
      "isAdsEligible": true
    }
  ]
}
```

`displayArtist` is set for music and `igUsername` for original sounds; original sounds also carry `profilePictureUrl`. `previewUrl` expires after about 1.5 days. Only audio Meta cleared for third-party publishing comes back, which can differ from what the Instagram app shows. Pass the chosen `audioId` in `instagramConfigs[].audio` (see [platform-configs.md](platform-configs.md#instagram--instagramconfigs)).

Returns `400` when the account is not connected through Facebook or Instagram rejects the search, and `404` for an unknown account.

### GET /social-accounts/:id/pinterest-boards

List the boards a Pinterest account can pin to, secret boards included. `:id` is the Pinterest account `id` from `/social-accounts`.

**Response:**

```json
{
  "boards": [
    {
      "id": "549755885175",
      "name": "Recipes",
      "description": "Weeknight dinners",
      "privacy": "PUBLIC",
      "pinCount": 42
    }
  ]
}
```

`id` and `name` are always set; `description`, `privacy` and `pinCount` are optional. `privacy` is `PUBLIC`, `PROTECTED` or `SECRET`. A board belongs to one Pinterest account, so list the boards of each Pinterest account you post to. Pass the chosen `id` as `pinterestConfigs[].boardId`, or skip this call and pass the name the user gave as `pinterestConfigs[].boardName` (see [platform-configs.md](platform-configs.md#pinterest--pinterestconfigs)).

Returns `404` when the account is not found or is not a Pinterest account in this workspace, and `400` when Pinterest refuses the request, usually because the account must be reconnected.

### GET /social-accounts/:id/youtube-playlists

List the playlists of a YouTube channel, private and unlisted ones included. `:id` is the YouTube account `id` from `/social-accounts`.

**Response:**

```json
{
  "playlists": [
    {
      "id": "PLxxxxxxxx",
      "title": "Tutorials",
      "privacyStatus": "public",
      "itemCount": 12
    }
  ]
}
```

`id` and `title` are always set; `privacyStatus` and `itemCount` are optional. `privacyStatus` is `public`, `unlisted` or `private`. A playlist belongs to one channel, so list the playlists of each channel you post to. Pass the chosen `id` as `youtubeConfigs[].playlistId` to add the uploaded video to that playlist (see [platform-configs.md](platform-configs.md#youtube--youtubeconfigs)).

Returns `404` when the account is not found or is not a YouTube account in this workspace, and `400` when YouTube refuses the request, usually because the account must be reconnected.

### GET /linkedin-organizations/lookup

Look up a LinkedIn company page so a LinkedIn post can mention it. Needs `accounts.read`. Read-only.

**Query parameters:**

- `query` (string, required, 1 to 300 characters): the company page URL (`https://www.linkedin.com/company/acme/`), its vanity name (`acme`, the part after `linkedin.com/company/`) or `@acme`

**Response:**

```json
{
  "organization": {
    "id": "2414183",
    "name": "Devtestco",
    "vanityName": "devtestco",
    "urn": "urn:li:organization:2414183",
    "mention": "@[Devtestco](urn:li:organization:2414183)"
  }
}
```

`vanityName` is `null` when the page has none. Paste `mention` into the LinkedIn text as it is. When the post also goes to other platforms, put it in `platformTexts` for `LINKEDIN`, since other platforms show the syntax as raw text.

LinkedIn matches the exact vanity name only, so this is not a search: `acm` or a company name with spaces finds nothing, and the answer is `{ "organization": null }`. Ask the user for the page URL when the vanity name is unknown.

Errors carry a `code` in the body:

- `400` `linkedin_organization_query_invalid`: the query is neither a page URL nor a vanity name
- `400` `linkedin_organization_lookup_unavailable`: no LinkedIn account of the workspace could run the lookup. Tell the user to connect or reconnect a LinkedIn account, ideally a company page they administer

### GET /social-accounts/:id/wordpress-categories

List the categories of a WordPress site, sorted by name. `:id` is the WordPress account `id` from `/social-accounts`. Needs `posts.draft`.

**Response:**

```json
{
  "categories": [
    { "id": 12, "name": "News", "parentId": null },
    { "id": 15, "name": "Releases", "parentId": 12 }
  ]
}
```

`parentId` is `null` for a top-level category. Pass the chosen ids as `wordpressConfigs[].categoryIds` (see [platform-configs.md](platform-configs.md#wordpress--wordpressconfigs)). Without `categoryIds` WordPress files the post under the site's default category.

Returns `404` when the account is not found or is not a WordPress account in this workspace, and an error with the reason when the site refuses the request or cannot be reached.

### POST /social-posts

Create or schedule a post to one or more social media platforms.

A draft (`saveAsDraft: true`) needs `posts.draft`, with or without a planned date. A future `scheduledAt` also needs `posts.schedule`, and a post that publishes now also needs `posts.publish`; without it the call answers `403 permission_denied`.

**Request:**

```json
{
  "platforms": ["TWITTER", "INSTAGRAM"],
  "contentType": "IMAGE",
  "text": "Post text with #hashtags",
  "platformTexts": [{ "platform": "TWITTER", "text": "Short version for X" }],
  "mediaUrls": ["https://cdn.adaptlypost.com/social-media-posts/uuid/photo.jpg"],
  "mediaAltTexts": ["A red bicycle leaning on a brick wall"],
  "thumbnailUrl": "https://cdn.adaptlypost.com/social-media-posts/uuid/thumb.jpg",
  "scheduledAt": "2026-06-15T10:00:00.000Z",
  "timezone": "America/New_York",
  "saveAsDraft": false,
  "twitterConnectionIds": ["connection-id-1"],
  "instagramConnectionIds": ["connection-id-2"],
  "instagramConfigs": [
    {
      "connectionId": "connection-id-2",
      "postType": "FEED"
    }
  ]
}
```

**Required fields:**

- `platforms` (string[]): At least one platform, unless `accountIds` is sent. Values: `FACEBOOK`, `INSTAGRAM`, `THREADS`, `TIKTOK`, `TWITTER`, `BLUESKY`, `MASTODON`, `LINKEDIN`, `PINTEREST`, `YOUTUBE`, `GOOGLE_BUSINESS`, `TELEGRAM`, `TUMBLR`, `WORDPRESS`
- `contentType` (string): `TEXT`, `IMAGE`, `VIDEO`, `CAROUSEL`, or `DOCUMENT`. `CAROUSEL` takes 2 or more items in `mediaUrls`, up to 4 on `TWITTER`, `BLUESKY` and `MASTODON`, 5 on `PINTEREST`, 10 on `INSTAGRAM`, `FACEBOOK`, `THREADS` and `TELEGRAM`, 20 on `LINKEDIN` and `WORDPRESS`, 30 on `TUMBLR` and 35 on `TIKTOK` (JPEG or WebP only). `INSTAGRAM` and `THREADS` mix images and videos in one carousel; the others take images only, and `YOUTUBE` has no carousel. `DOCUMENT` is LinkedIn only: exactly one PDF, PPT, PPTX, DOC or DOCX URL in `mediaUrls` (max 100 MB, 300 pages). `GOOGLE_BUSINESS` takes `TEXT` or `IMAGE` only
- `timezone` (string): IANA timezone string (e.g., `America/New_York`, `Europe/London`). Stored with the post for display; it does not shift `scheduledAt`

**Optional fields:**

- `accountIds` (string[]): Account `id`s (or Facebook `pageId`s) from `/social-accounts`. AdaptlyPost adds each account's platform to `platforms` and its id to the matching connection id list, so you can send these instead of `platforms` and the per-platform lists, or alongside them. An id that is not connected to the workspace returns `400`. `POST /social-posts` only
- `text` (string): Default post text for all platforms. On LinkedIn, mention a company page with `@[Page Name](urn:li:organization:<id>)`, using the page name exactly as LinkedIn shows it; `GET /linkedin-organizations/lookup` returns the ready-made mention
- `platformTexts` (array): Per-platform text overrides. Each: `{ "platform": "TWITTER", "text": "..." }`. The LinkedIn mention syntax works here too
- `mediaUrls` (string[]): Public URLs of uploaded media files
- `mediaAltTexts` (string[]): Alt text for each image, in the same order as `mediaUrls` (max 1000 characters each; use `""` to skip an image). Sent to X, Bluesky, Mastodon, Tumblr, WordPress, LinkedIn, Facebook, Instagram and Threads. Pinterest uses the first one, cut to 500 characters. TikTok, YouTube, Google Business Profile, Telegram and videos ignore it
- `thumbnailUrl` (string): Video thumbnail as an https URL or an image data URI, used on every platform that takes one unless `platformThumbnails` overrides it
- `thumbnailTimestampMs` (number): Video frame (ms) to use as the thumbnail on every platform that takes one: `YOUTUBE`, `FACEBOOK`, `INSTAGRAM`, `LINKEDIN`, `PINTEREST`, `TELEGRAM` and `TIKTOK`. A `thumbnailUrl` sent with it wins everywhere except `TIKTOK`, and `platformThumbnails` overrides both
- `platformThumbnails` (array): A different thumbnail per platform. See [Platform thumbnails](#platform-thumbnails)
- `platformMedia` (array): Different media for one platform. See [Platform media](#platform-media)
- `platformAspectRatios` (array): Reframe images to one shape per platform. See [Image shape per platform](#image-shape-per-platform)
- `firstComments` (array): A comment posted shortly after the post goes out. See [First comments](#first-comments)
- `threadReplies` (array): Replies that turn the post into a thread on X, Threads, Bluesky or Mastodon. See [Thread replies](#thread-replies)
- `twitterKeepLinks` (boolean): Keep links in the X text clickable. See [Links on X](#links-on-x)
- `scheduledAt` (string): ISO 8601 UTC datetime. A future value schedules the post; omitted or in the past publishes immediately. With `saveAsDraft: true` it is the draft's planned date: the post stays a `DRAFT`, and `POST /social-posts/:id/publish` without `scheduledAt` schedules it for that date
- `saveAsDraft` (boolean): Save as `DRAFT` instead of scheduling/publishing; validation is deferred to `POST /social-posts/:id/publish`
- `recurrence` (object): Repeats the post. See [Recurrence](#recurrence) below
- `pageIds` (string[]): Facebook page account `id` values from `/social-accounts` (the account's `pageId` value is accepted too)
- `tiktokConnectionIds` (string[]): TikTok account connection IDs
- `threadsConnectionIds` (string[]): Threads account connection IDs
- `instagramConnectionIds` (string[]): Instagram account connection IDs
- `twitterConnectionIds` (string[]): X/Twitter account connection IDs
- `blueskyConnectionIds` (string[]): Bluesky account connection IDs
- `mastodonConnectionIds` (string[]): Mastodon account connection IDs
- `linkedinConnectionIds` (string[]): LinkedIn account connection IDs
- `pinterestConnectionIds` (string[]): Pinterest account connection IDs
- `youtubeConnectionIds` (string[]): YouTube account connection IDs
- `googleBusinessConnectionIds` (string[]): Google Business Profile location `id` values from `/social-accounts`. A location without a `googleBusinessConfigs` entry gets a `STANDARD` update
- `telegramConnectionIds` (string[]): Telegram channel and group `id` values from `/social-accounts`. Text up to 4096 characters, up to 10 images (JPEG, PNG or WebP, 10 MB each) or one MP4 or MOV video (50 MB). A caption over 1024 characters goes out as its own message after the media
- `tumblrConnectionIds` (string[]): Tumblr blog `id` values from `/social-accounts`. Text up to 32768 characters, up to 30 JPEG, PNG or GIF images (10 MB each) or one MP4 video (500 MB, up to 10 minutes)
- `wordpressConnectionIds` (string[]): WordPress site `id` values from `/social-accounts`. The text becomes the body of a blog post (up to 100,000 characters; blank lines start new paragraphs and bare links become clickable). Up to 20 JPEG, PNG, WebP or GIF images (20 MB each) or one MP4 or MOV video (500 MB); the first image is the featured image and the other images or the video follow the text. A site without a `wordpressConfigs` entry uses the first line of the text as the title
- `pinterestConfigs` (array): Pinterest-specific settings per connection. Pick the board with `boardId` or `boardName` (the board's name on that account, resolved when the request is handled; `400` when no board or several boards have it), never both. With neither, the pin goes to a public board named "AdaptlyPost". `aiGenerated: true` discloses that the Pin was made or modified with AI: Pinterest gets the `AI_MODIFIED` disclosure and shows an "AI modified" label on image, video and carousel Pins
- `tiktokConfigs` (array): TikTok-specific settings per connection
- `instagramConfigs` (array): Instagram-specific settings per connection
- `facebookConfigs` (array): Facebook-specific settings per page
- `youtubeConfigs` (array): YouTube-specific settings per connection. `scheduleOnYouTube: true` uploads the video as soon as the post is scheduled, as a private video that YouTube publishes itself at `scheduledAt`, so the user can set up Test & Compare in YouTube Studio first. It needs `privacyStatus` `public` or unset (`400` `YOUTUBE_SCHEDULE_REQUIRES_PUBLIC`) and no `recurrence` (`400` `YOUTUBE_SCHEDULE_NOT_RECURRING`). With `scheduledAt` less than 15 minutes ahead the video uploads at `scheduledAt` as usual
- `linkedinConfigs` (array): LinkedIn-specific settings per connection (`documentTitle` for `DOCUMENT` posts, `reshareOf` to reshare a LinkedIn post)
- `twitterConfigs` (array): X settings per account, items `{ connectionId, quoteOf?, aiGenerated? }`: `quoteOf` quotes one of the account's own X posts; `aiGenerated: true` discloses that the post contains AI-generated media, which sets `made_with_ai` on the X post, and X labels it
- `threadsConfigs` (array): Threads settings per account, items `{ connectionId, aiGenerated? }`. `connectionId` must match an entry in `threadsConnectionIds`. `aiGenerated: true` discloses AI-generated content: Threads shows its "AI info" label on the post. Works on text, image, video and carousel posts; on a carousel the label covers the whole post. Thread replies do not carry it
- `googleBusinessConfigs` (array): Google Business Profile settings per location: topic (update, event or offer), button, event and offer details
- `tumblrConfigs` (array): Tumblr settings per blog: tags, a title and a source link
- `wordpressConfigs` (array): WordPress settings per site: title, excerpt, category ids, tags and `status` (`PUBLISH`, the default, publishes the post live; `DRAFT` leaves a WordPress draft; `PENDING` submits it for review). See [platform-configs.md](platform-configs.md#wordpress--wordpressconfigs)

See [platform-configs.md](platform-configs.md) for detailed config schemas.

#### First comments

`firstComments` posts a comment from the same account shortly after the post goes out, one entry per platform:

```json
{ "firstComments": [{ "platform": "LINKEDIN", "text": "Read the full report at example.com/report", "delayMinutes": 60 }] }
```

Each entry takes `platform`, `text` and an optional `delayMinutes`: an integer from 0 to 10080 (7 days), how many minutes after the platform publishes to post the comment. Omitted or 0 means no delay. The comment goes out within about a minute of that time; without a delay, within about a minute of the post (about two minutes on YouTube). Once the post is published the delay cannot be changed; deleting the post cancels a comment that has not gone out yet. An out-of-range value returns `400`.

| Platform | Posted as | Max characters |
| --- | --- | --- |
| `LINKEDIN` | comment | 1250 |
| `TWITTER` | reply | 280 |
| `THREADS` | reply | 500 |
| `BLUESKY` | reply | 300 |
| `MASTODON` | reply | 500 |
| `YOUTUBE` | comment | 10000 |
| `FACEBOOK` | comment | 8000 |
| `INSTAGRAM` | comment | 2200 |

Any other platform returns `400`, as does a platform the post does not go to, an empty or too long text, a second entry for one platform, a platform that also has `threadReplies`, a private or made for kids YouTube video, and Facebook or Instagram stories. The comment goes out within about a minute of the platform publishing (about two minutes on YouTube), or within about a minute of `delayMinutes` after it, and is retried up to 3 times. On X it is not retried, and on a lifetime-deal account it costs credits like any X post. A failed comment never fails the post: read `firstCommentStatus` and `firstCommentError` on the platform entry. A Facebook Page or Instagram account connected before Facebook and Instagram got first comments needs one reconnect from Connectors; until then its comment fails and `firstCommentError` says to reconnect. On `PATCH`, sending the array replaces every first comment and leaving it out keeps the stored ones.

#### Thread replies

`threadReplies` turns the post into a thread, one entry per platform. The post opens the thread, and each text goes out from the same account as a reply to the one before:

```json
{
  "threadReplies": [
    {
      "platform": "TWITTER",
      "texts": ["2/ Here is what changed", "", "4/ Read more at example.com"],
      "mediaUrls": [[], ["https://cdn.adaptlypost.com/social-media-posts/uuid/before.png", "https://cdn.adaptlypost.com/social-media-posts/uuid/after.png"], []]
    }
  ]
}
```

- `platform` (string, required): `TWITTER`, `THREADS`, `BLUESKY` or `MASTODON`
- `texts` (string[], required): The replies in order, each trimmed, up to 25. Each is held to the platform limit below and never more than 25000 characters
- `mediaUrls` (string[][]): Optional and parallel to `texts`: up to 4 JPEG, PNG, GIF or WEBP image URLs per reply, uploaded through [POST /upload-urls](#post-upload-urls) like the post's own `mediaUrls`, and `[]` for a reply without images. A reply with images may have an empty text

| Platform | Max characters per reply |
| --- | --- |
| `TWITTER` | 280 (more on X Premium) |
| `THREADS` | 500 |
| `BLUESKY` | 300 |
| `MASTODON` | 500 (or the instance's limit) |

Any other platform returns `400`, as does a platform the post does not go to, a reply with neither text nor images, a reply over the limit, more than 25 replies, more than 4 images or a video on a reply, a second entry for one platform, and a platform that also has a first comment. Replies start about 10 seconds after the platform publishes, 2 seconds apart. A failed run is retried up to 3 times and resumes after the last reply that went out. On X it is not retried, and a lifetime-deal account pays for each reply like any X post. A failed thread never fails the post: read `threadStatus`, `threadReplyIds` and `threadError` on the platform entry. On `PATCH`, sending the array replaces every stored thread, an entry with `"texts": []` removes that platform's thread, and leaving the array out keeps the stored threads.

#### Platform thumbnails

`platformThumbnails` gives one platform of a `VIDEO` post its own thumbnail, one entry per platform: `{ "platform", "thumbnailUrl", "thumbnailTimestampMs" }`. `thumbnailUrl` is an https URL or an image data URI; `thumbnailTimestampMs` is a video frame in ms (integer, 0 or more).

- `YOUTUBE`, `FACEBOOK`, `INSTAGRAM`, `LINKEDIN`, `PINTEREST`, `TELEGRAM`: image or frame; the image wins when both are sent
- `TIKTOK`: frame only

A platform without an entry uses the post-level `thumbnailUrl` and `thumbnailTimestampMs`, which work on every platform above. Other platforms, posts that are not videos, Facebook and Instagram stories, a second entry for one platform and an entry the platform cannot use return `400`. On `PATCH`, sending the array replaces every override and leaving it out keeps the stored ones.

#### Platform media

`platformMedia` gives one platform its own media, for when the post media does not fit it: a video too long for TikTok, a carousel with more images than X takes. One entry per platform: `{ "platform": "TIKTOK", "mediaUrls": ["https://cdn.adaptlypost.com/social-media-posts/uuid/short-cut.mp4"], "mediaAltTexts": [] }`.

- `platform` (string, required): A platform the post goes to
- `mediaUrls` (string[], required): Not empty. Public URLs from [POST /upload-urls](#post-upload-urls), like the post's own `mediaUrls`; no data URIs
- `mediaAltTexts` (string[]): Alt text per item, in the same order as this entry's `mediaUrls` (max 1000 characters each; use `""` to skip one)

The entry must match the post `contentType`: one video for `VIDEO`, one image for `IMAGE`, one document for `DOCUMENT`, two or more items for `CAROUSEL`. `TEXT` posts take none. Each entry is checked against its own platform's limits only, and the post `mediaUrls` is no longer checked against that platform. A platform without an entry uses the post `mediaUrls`. An overridden platform does not use the post-level `thumbnailUrl` or `thumbnailTimestampMs`; give it its own through [`platformThumbnails`](#platform-thumbnails).

A platform the post does not go to, an empty `mediaUrls`, a data URI, a second entry for one platform and media of another type return `400`. On `PATCH`, sending the array replaces every override, `[]` clears them all, and leaving it out keeps the stored ones. It takes effect without `platforms`.

#### Image shape per platform

`platformAspectRatios` reframes every image of an `IMAGE` or `CAROUSEL` post to one shape on a platform, one entry per platform: `{ "platform": "INSTAGRAM", "aspectRatio": "PORTRAIT", "fit": "CROP" }`.

- `aspectRatio`: `SQUARE` (1:1), `PORTRAIT` (4:5), `VERTICAL` (9:16), `LANDSCAPE` (1.91:1). `INSTAGRAM` takes `SQUARE`, `PORTRAIT` and `LANDSCAPE`; `TIKTOK` takes all four
- `fit`: `CROP` (default) cuts the image from the center; `PAD` keeps the whole image and fills the rest with a blurred copy

Other platforms, video posts, Instagram stories and a second entry for one platform return `400`. Leave a platform out to keep its images as uploaded. On `PATCH` it applies to the `mediaUrls` sent in the same request.

#### Links on X

X charges over 10 times more for a post with a link, so by default every link in X text is broken (`example.com` becomes `example. com`). `twitterKeepLinks: true` keeps them clickable. Only AppSumo lifetime deals can turn it on, and a kept link costs 20 credits instead of 2; `true` on any other plan returns `400`. It is ignored when the X text has no link. `POST /social-posts` and `PATCH` take it; bulk does not.

#### Recurrence

`recurrence` repeats the post. The future `scheduledAt` is the first post and sets the time of day, and `timezone` decides which local day and time that is for every later post.

```json
{
  "scheduledAt": "2026-10-05T07:00:00.000Z",
  "timezone": "Europe/Berlin",
  "recurrence": { "frequency": "WEEKLY", "weekdays": ["MONDAY", "FRIDAY"], "endsOn": "2026-12-31" }
}
```

- `frequency` (string, required): `DAILY`, `WEEKLY`, `MONTHLY` or `YEARLY`. `YEARLY` comes back on the same date every year at the same local time; a series started on February 29 posts on February 28 in other years
- `interval` (integer): Repeat every N days, weeks, months or years. Range: 1-30. Default: 1
- `weekdays` (Weekday[]): `WEEKLY` only. The weekday of `scheduledAt` is always included
- `endsOn` (string): `YYYY-MM-DD`, the last day an occurrence may go out on (inclusive). Must be on or after the day of the first post
- `maxOccurrences` (integer): Total number of posts the series publishes. Range: 2-365

`endsOn` and `maxOccurrences` cannot be combined; with neither the post repeats until it is paused or deleted. Each rule below returns `400` with the message shown:

- no `frequency`: `Choose how often the post repeats`
- `saveAsDraft: true`: `A recurring post cannot be saved as a draft. Schedule it instead`
- no future `scheduledAt`: `Pick a future date and time for the first post of a recurring series`
- both `endsOn` and `maxOccurrences`: `Choose either an end date or a number of posts, not both`
- `endsOn` before the first post: `The end date must be on or after the first post`
- a TikTok account: `TIKTOK posts cannot repeat. Remove the account or turn off repeat`

Only `POST /social-posts` takes `recurrence`. `PATCH /social-posts/:id`, bulk items and `POST /social-posts/:id/publish` do not. See [Recurring posts](#recurring-posts) for how the series runs.

**Response:**

```json
{
  "postId": "cmm0z0k3q0000i0r5mxn0hfhs",
  "queuedPlatforms": ["TWITTER", "INSTAGRAM"],
  "skippedPlatforms": [
    {
      "platform": "FACEBOOK",
      "reason": "No valid connection found"
    }
  ],
  "isScheduled": true,
  "scheduledAt": "2026-06-15T10:00:00.000Z",
  "recurringPostId": "cmr1a2b3c0000i0r5rcp0abcd"
}
```

`recurringPostId` is only present when the request carried `recurrence`; `postId` is then the first post of the series.

`queuedPlatforms` confirms that publishing jobs were queued, not that they succeeded: each platform publishes asynchronously and on its own, so read `GET /social-posts/:id/results` for the outcome. A future `scheduledAt` returns `isScheduled: true` with status `SCHEDULED`; a missing or past `scheduledAt` publishes immediately with status `PENDING`; `saveAsDraft: true` stores a `DRAFT`, with `scheduledAt` as its planned date when one was sent.

### GET /social-posts

List every post in the authenticated account group, any status, with pagination. Newest first by default.

**Query parameters:**

- `limit` (integer, optional): Number of posts to return. Range: 1-100. Default: 20
- `offset` (integer, optional): Number of posts to skip. Min: 0. Default: 0
- `sortOrder` (string, optional): `NEWEST` or `OLDEST`. Default: `NEWEST`
- `statuses` (PostStatus[], optional): Filter by one or more post statuses. Repeat the key per value. Any query parameter outside this list returns `400`.
- `platforms` (PlatformType[], optional): Filter by one or more platforms. Repeat the key per value.
- `startDate` (string, optional): Lower bound on `scheduledAt`, or on `createdAt` for posts that were never scheduled (ISO 8601, e.g. `2026-07-20`).
- `endDate` (string, optional): Upper bound on `scheduledAt`, or on `createdAt` for posts that were never scheduled (ISO 8601, e.g. `2026-07-22`).

Array filters (`statuses`, `platforms`) are sent as repeated keys, e.g. `platforms=FACEBOOK&platforms=TIKTOK`.

**Example:**

```
GET /social-posts?limit=10&offset=0&statuses=SCHEDULED&statuses=PUBLISHING&platforms=FACEBOOK
```

**Response:**

```json
{
  "posts": [
    {
      "id": "cmm0z0k3q0000i0r5mxn0hfhs",
      "createdAt": "2026-02-24T19:00:34.114Z",
      "updatedAt": "2026-02-24T19:00:34.114Z",
      "userId": "user_01KH48SNHMPJNFYPJWZVJAKXDS",
      "contentType": "TEXT",
      "text": "Hello from API!",
      "scheduledAt": "2026-06-15T10:00:00.000Z",
      "timezone": "America/New_York",
      "status": "DRAFT",
      "recurringPostId": null,
      "occurrenceAt": null,
      "platforms": [
        {
          "id": "cmm0z0k3u0001i0r5dlbfa440",
          "createdAt": "2026-02-24T19:00:34.114Z",
          "updatedAt": "2026-02-24T19:00:34.114Z",
          "platform": "TWITTER",
          "status": "PENDING",
          "connectionId": "cmlxly42t0004hzq1bh9kqpwl",
          "mediaUrls": [],
          "previewUrls": [],
          "youtubeTags": []
        }
      ]
    }
  ],
  "total": 1,
  "hasMore": false
}
```

**Post status values:** `DRAFT`, `SCHEDULED`, `PENDING`, `PUBLISHING`, `COMPLETED`, `PARTIAL_FAILURE`, `FAILED`
**Platform status values:** `PENDING`, `PUBLISHING`, `PUBLISHED`, `FAILED`

The post carries its `mediaUrls` at the top level as well as on each platform entry. Once a platform entry is published, `platformPostId` and a clickable `postUrl` are set on every platform. Instagram and Facebook stories expire after 24 hours, so their `postUrl` links to the profile or page. `previewUrls` holds one permanent preview image per media item (WebP, up to 720px, a still frame for videos), filled in shortly after publishing starts; an empty string means that item could not be rendered. After publishing, `mediaUrls` may be replaced by the platform's own CDN links, which expire within days, and the uploaded source files are removed, so display `previewUrls`.

`recurringPostId` names the recurring post this post is an occurrence of, and `occurrenceAt` is the series slot it fills, which stays the same when the post is rescheduled. Both are `null` on posts that are not part of a series.

Platform entry fields set by the newer request fields (absent when not used):

- First comment: `firstComment`, `firstCommentStatus` (`PENDING`, `PUBLISHED` or `FAILED`), `firstCommentId`, `firstCommentError`, `firstCommentPublishedAt`, `firstCommentDelayMinutes` (integer, absent when the comment posts right away), `firstCommentDueAt` (ISO date-time, set once the platform publishes; a comment with `firstCommentStatus` `PENDING` goes out within about a minute of that time)
- Thread: `threadReplies` (the reply texts in order, empty when the platform has no thread), `threadReplyMediaUrls` (string[][], parallel to `threadReplies`, `[]` for a reply without images), `threadStatus` (`PENDING` until every reply is posted, `PUBLISHED` once they are, `FAILED` when one could not be), `threadReplyIds` (the platform's ids of the replies published so far, in order, AT URIs on Bluesky; fewer ids than replies means the rest did not go out), `threadError`, `threadPublishedAt`
- Thumbnail override: `thumbnailUrl`, `thumbnailTimestampMs`
- Media override: `mediaOverrideUrls`, `mediaOverrideAltTexts` (empty when the platform uses the post media). The entry's `mediaUrls` is what that platform publishes
- Image shape: `mediaAspectRatio`, `mediaAspectRatioFit`
- Instagram: `instagramCollaborators`, `instagramUserTags` (each `{ username, x, y }`), `instagramAiGenerated` (the post carries the AI info label), `instagramUsername` (the handle it published from), `instagramAudioId`, `instagramAudioTitle`, `instagramAudioArtist`, `instagramAudioVolume`, `instagramVideoVolume`
- Facebook: `facebookTextFormatPresetId`, `facebookImageLayout` (`GRID` or `CAROUSEL`), `facebookCarouselCards` (each with `link`, `title`, `description`), `facebookAiGenerated` (the post carries the AI info label; see `facebookConfigs[].aiGenerated`)
- YouTube: `youtubeAiGenerated` (the video carries the altered or synthetic content label; see `youtubeConfigs[].aiGenerated`), `youtubeDefaultAudioLanguage`, `youtubeScheduleOnYouTube`, `youtubeScheduledVideoId` (the YouTube video uploaded ahead of `scheduledAt`; while it is set and the entry is not published, the post cannot be updated, unscheduled or published early)
- X: `twitterKeepLinks`, `twitterQuoteOf` (the id of the X post this account quotes), `twitterAiGenerated` (the post carries the made-with-AI label; see `twitterConfigs[].aiGenerated`)
- Threads: `threadsAiGenerated` (the post carries the AI info label; see `threadsConfigs[].aiGenerated`)
- Pinterest: `pinterestAiGenerated` (the Pin carries the AI modified label; see `pinterestConfigs[].aiGenerated`)
- LinkedIn: `linkedinDocumentTitle`, `linkedinReshareOf` (the LinkedIn post URN this account reshares)
- TikTok: `tiktokDraftFallback` (TikTok's daily cap was hit, so the content went to the creator's TikTok inbox as a draft instead of being published)
- Google Business Profile: `googleBusinessTopicType`, `googleBusinessCallToActionType`, `googleBusinessCallToActionUrl`, `googleBusinessEventTitle`, `googleBusinessEventStart`, `googleBusinessEventEnd`, `googleBusinessOfferCouponCode`, `googleBusinessOfferRedeemUrl`, `googleBusinessOfferTerms`
- Tumblr: `tumblrTags`, `tumblrTitle`, `tumblrSourceUrl`
- WordPress: `wordpressTitle`, `wordpressExcerpt`, `wordpressCategoryIds`, `wordpressTags`, `wordpressStatus` (`PUBLISH`, `DRAFT` or `PENDING`)

A story shared next to a feed post or reel (`shareToStory`) is its own platform entry with `instagramPostType` or `facebookPostType` set to `STORY`.

### GET /social-posts/:id

Get a single post by ID. Returns 404 if not found or not in the account group.

**Response:**
Same structure as individual post in the list endpoint.

**Error response (404):**

```json
{
  "message": "Post not found or access denied",
  "error": "Not Found",
  "statusCode": 404
}
```

### POST /social-posts/bulk

Schedule up to 100 posts at once. Each post can have its own content, media, and scheduled time.

**Request:**

```json
{
  "platforms": ["YOUTUBE", "PINTEREST"],
  "timezone": "America/New_York",
  "youtubeConnectionIds": ["conn_yt123"],
  "pinterestConnectionIds": ["conn_pin456"],
  "youtubeConfigs": [{ "connectionId": "conn_yt123", "postType": "SHORTS", "privacyStatus": "public" }],
  "pinterestConfigs": [{ "connectionId": "conn_pin456", "boardId": "board_abc", "title": "Default title" }],
  "posts": [
    {
      "contentType": "VIDEO",
      "text": "First video",
      "mediaUrls": ["https://cdn.adaptlypost.com/uploads/video1.mp4"],
      "scheduledAt": "2026-03-15T10:00:00Z"
    },
    {
      "contentType": "VIDEO",
      "text": "Second video with custom YouTube config",
      "mediaUrls": ["https://cdn.adaptlypost.com/uploads/video2.mp4"],
      "scheduledAt": "2026-03-15T14:00:00Z",
      "youtubeConfigs": [{ "connectionId": "conn_yt123", "postType": "VIDEO", "videoTitle": "Full tutorial", "privacyStatus": "unlisted" }]
    }
  ]
}
```

**Required fields:**

- `platforms` (string[]): At least one platform
- `timezone` (string): IANA timezone string
- `posts` (array): 1-100 post items

**Optional fields (batch-level):**

- Connection ID arrays: `twitterConnectionIds`, `linkedinConnectionIds`, `instagramConnectionIds`, `tiktokConnectionIds`, `youtubeConnectionIds`, `pinterestConnectionIds`, `blueskyConnectionIds`, `mastodonConnectionIds`, `threadsConnectionIds`, `googleBusinessConnectionIds`, `telegramConnectionIds`, `tumblrConnectionIds`, `wordpressConnectionIds`, `pageIds`
- Platform configs (applied to all posts as default): `pinterestConfigs`, `threadsConfigs`, `twitterConfigs`, `tiktokConfigs`, `instagramConfigs`, `facebookConfigs`, `youtubeConfigs`, `googleBusinessConfigs`, `tumblrConfigs`, `wordpressConfigs`

`firstComments`, `threadReplies`, `platformThumbnails`, `platformMedia` and `platformAspectRatios` go on each post item, not the batch. Bulk does not take `twitterKeepLinks`, `linkedinConfigs` or `accountIds`.

See [platform-configs.md](platform-configs.md) for config schemas.

**Post item fields:**

- `contentType` (string, required): `TEXT`, `IMAGE`, `VIDEO`, or `CAROUSEL`. `DOCUMENT` posts cannot be bulk scheduled; create them one at a time
- `scheduledAt` (string, required): ISO 8601 UTC datetime
- `text` (string): Post text
- `platformTexts` (array): Per-platform text overrides
- `mediaUrls` (string[]): Media file URLs
- `mediaAltTexts` (string[]): Alt text for each image, in the same order as `mediaUrls` (max 1000 characters each; use `""` to skip an image). Sent to X, Bluesky, Mastodon, Tumblr, WordPress, LinkedIn, Facebook, Instagram and Threads. Pinterest uses the first one, cut to 500 characters. TikTok, YouTube, Google Business Profile, Telegram and videos ignore it
- `thumbnailUrl` (string): Thumbnail URL for video posts
- `thumbnailTimestampMs` (number): Thumbnail position in video (ms)
- `firstComments`, `threadReplies`, `platformThumbnails`, `platformMedia`, `platformAspectRatios` (arrays): Same as on [POST /social-posts](#first-comments)
- Platform config overrides (per-post): `pinterestConfigs`, `threadsConfigs`, `twitterConfigs`, `tiktokConfigs`, `instagramConfigs`, `facebookConfigs`, `youtubeConfigs`, `googleBusinessConfigs`, `tumblrConfigs`, `wordpressConfigs` — when set on a post item, these override the batch-level configs for that specific post

A Pinterest `boardName`, at the batch level or on an item, is resolved per item. An item whose name matches no board, or several, fails alone with `success: false` and the reason in `errorMessage`; the other items are still scheduled.

**Response:**

```json
{
  "totalScheduled": 2,
  "totalFailed": 0,
  "results": [
    { "postId": "post_abc001", "success": true, "isScheduled": true, "scheduledAt": "2026-03-15T10:00:00Z", "errorMessage": null },
    { "postId": "post_abc002", "success": true, "isScheduled": true, "scheduledAt": "2026-03-15T14:00:00Z", "errorMessage": null }
  ]
}
```

**Notes:**

- Maximum 100 posts per request
- Each post is processed independently — if one fails, others still schedule
- Only one account per platform allowed (platform ToS compliance)
- Per-post platform configs completely replace batch-level configs (no merging)

### POST /social-posts/validate

Dry-runs a post. Takes the same body as [POST /social-posts](#post-social-posts) and runs every check that call runs, plus the ones that usually fail only at publish time (TikTok creator limits and video length, the YouTube upload quota for channels without a backup upload, expired Instagram and Threads tokens, Mastodon attachments past the server's limit, Pinterest board ids, X credits on lifetime deals). It creates, uploads and records nothing. Needs `posts.draft` and no active plan.

Content problems answer `200` with the report. `400` means a malformed body, `401` and `403` the usual auth answers.

**Response:**

```json
{
  "valid": false,
  "outcome": "SCHEDULED",
  "scheduledAt": "2026-03-15T10:00:00.000Z",
  "requiredPermissions": ["posts.schedule"],
  "issues": [],
  "accounts": [
    { "platform": "TWITTER", "connectionId": "conn_tw1", "accountName": "Acme", "status": "BLOCKED",
      "issues": [{ "code": "TEXT_TOO_LONG", "severity": "ERROR", "message": "Text exceeds maximum length for X. Maximum is 280 characters", "platform": "TWITTER", "connectionId": "conn_tw1" }] },
    { "platform": "LINKEDIN", "connectionId": "conn_li1", "accountName": "Acme Inc", "status": "READY", "issues": [] }
  ],
  "notChecked": [
    { "code": "PLATFORM_PROCESSING", "message": "The platform processes media after upload and can still reject it then" }
  ]
}
```

- `valid` (boolean): `false` when any issue has severity `ERROR`
- `outcome`: `PUBLISH_NOW`, `SCHEDULED` or `DRAFT`, what creating the post would do; `scheduledAt` is set when `SCHEDULED`
- `requiredPermissions` (string[]): the permissions creating it needs. A missing one is reported as a `PERMISSION_DENIED` issue
- `issues`: problems not tied to one selected account
- `accounts`: one entry per selected account with `platform`, `connectionId`, `accountName` (may be missing), `status` (`READY`, `WARNING` or `BLOCKED`) and its `issues`
- `notChecked`: what only the platform can decide at publish time, each `{ code, message }` with `code` one of `PLATFORM_PROCESSING`, `DUPLICATE_CONTENT`, `PLATFORM_RATE_LIMITS`, `LIVE_ACCOUNT_ACCESS`, `VIDEO_DURATION`

An issue is `{ code, severity, message, platform?, connectionId? }`. `severity` is `ERROR` (blocks the post) or `WARNING` (the post goes through). `message` is translated into the request's language; show it as is. Codes include the media and text checks (`TEXT_TOO_LONG`, `VIDEO_TOO_LARGE`, ...) and `ACCOUNT_NOT_FOUND`, `ACCOUNT_DISCONNECTED`, `ACCOUNT_TOKEN_EXPIRED`, `MEDIA_NOT_UPLOADED`, `TIKTOK_POSTING_BLOCKED`, `TIKTOK_VIDEO_TOO_LONG`, `TIKTOK_MEDIA_DOMAIN`, `YOUTUBE_UPLOAD_QUOTA_EXHAUSTED`, `MASTODON_MEDIA_DROPPED`, `PINTEREST_BOARD_NOT_FOUND`, `X_CREDITS_INSUFFICIENT`, `PERMISSION_DENIED`, `SUBSCRIPTION_REQUIRED` and `CHECK_UNAVAILABLE`. The list grows; treat an unknown code as opaque and show its `message`.

### POST /social-posts/bulk/validate

Takes the same body as [POST /social-posts/bulk](#post-social-postsbulk) and returns one report per item, in request order. Needs `posts.draft`.

```json
{
  "valid": false,
  "totalValid": 1,
  "totalInvalid": 1,
  "results": [
    { "index": 0, "report": { "valid": true, "outcome": "SCHEDULED", "...": "..." } },
    { "index": 1, "report": { "valid": false, "outcome": "SCHEDULED", "...": "..." } }
  ]
}
```

`index` is the item's 0-based position in `posts`, and each `report` has the shape above.

### POST /upload-urls

Get presigned upload URLs for media files. Upload 1-20 files per request.

**Request:**

```json
{
  "files": [
    { "fileName": "photo.jpg", "mimeType": "image/jpeg" },
    { "fileName": "video.mp4", "mimeType": "video/mp4" }
  ]
}
```

**Supported MIME types:**

- `image/jpeg` — JPEG images
- `image/png` — PNG images
- `image/webp` — WebP images
- `image/gif` — GIF images. They post to Facebook, X, Bluesky, Mastodon, LinkedIn and Tumblr; every other platform refuses them when the post is created
- `video/mp4` — MP4 video
- `video/quicktime` — MOV video
- `application/pdf` — PDF document (LinkedIn `DOCUMENT` posts)
- `application/vnd.ms-powerpoint` — PowerPoint 97-2003 document (LinkedIn `DOCUMENT` posts)
- `application/vnd.openxmlformats-officedocument.presentationml.presentation` — PowerPoint document (LinkedIn `DOCUMENT` posts)
- `application/msword` — Word 97-2003 document (LinkedIn `DOCUMENT` posts)
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document` — Word document (LinkedIn `DOCUMENT` posts)

Keep the file extension in `fileName`: a post reads the file type from it.

**Response:**

```json
{
  "urls": [
    {
      "fileName": "photo.jpg",
      "uploadUrl": "https://...presigned-s3-url...",
      "publicUrl": "https://cdn.adaptlypost.com/social-media-posts/uuid/photo.jpg",
      "key": "social-media-posts/uuid/photo.jpg",
      "expiresAt": "2026-02-24T20:00:00.000Z"
    }
  ]
}
```

**Upload flow:**

1. Call this endpoint to get `uploadUrl` and `publicUrl` (this only mints a URL — it does not store a file)
2. PUT the raw file binary to `uploadUrl` with matching `Content-Type` header, and confirm a `2xx` response
3. Use the `publicUrl` in `mediaUrls` when creating a post

> **The file must be uploaded (step 2) before you reference its `publicUrl`.** `POST /social-posts` and `POST /social-posts/bulk` verify every `publicUrl` exists in storage. A URL whose PUT never completed (or whose upload URL expired after 1 hour) is rejected with `400 Bad Request` and `Media file(s) not found in storage: <url>`. In bulk requests this is reported per-post; the remaining posts are still scheduled.

One `publicUrl` may be reused across any number of posts, bulk items included; the file is kept until the last post referencing it has published. Reuse the `publicUrl` you uploaded, not a `mediaUrls` value read back from a published post, since those may be the platform's own expiring links.

### GET /social-posts/:id/results

Per-platform publishing outcome for one post. Each platform reports on its own, so read this per row rather than treating the post as one pass or fail. Publishing is asynchronous, so poll until no row is `PENDING` or `PUBLISHING`.

**Response:**

```json
{
  "postId": "cmm0z0k3q0000i0r5mxn0hfhs",
  "status": "PARTIAL_FAILURE",
  "results": [
    { "platformId": "pp_abc001", "platform": "TWITTER", "accountName": "johndoe", "status": "PUBLISHED", "platformPostId": "1234567890", "errorMessage": null, "publishedAt": "2026-06-15T10:00:12.000Z" },
    { "platformId": "pp_abc002", "platform": "TIKTOK", "accountName": "johndoe", "status": "FAILED", "platformPostId": null, "errorMessage": "Spam risk: too many posts in a short window", "publishedAt": null }
  ]
}
```

Take `platformId` from `FAILED` rows when calling `POST /social-posts/:id/retry`. Use `GET /social-posts/:id` instead when you also need the content and schedule.

### PATCH /social-posts/:id

Update a `DRAFT` or `SCHEDULED` post, or a post that `FAILED` on every platform. A failed post becomes a `DRAFT` again with its platforms back to `PENDING`; publish or schedule it with `POST /social-posts/:id/publish`. A post that published on some platforms and failed on others (`PARTIAL_FAILURE`) cannot be edited, and neither can any other status: they answer `400` `Cannot edit post in current state` rather than being partially applied.

Moving a `SCHEDULED` post's `scheduledAt` more than a minute into the past returns `400` `The new scheduled time is in the past. Choose a time in the future`. Resending the time the post already has is accepted even after it passed. To publish now, use `POST /social-posts/:id/publish` without `scheduledAt`. `scheduledAt: null` takes the planned date off a `DRAFT` or a failed post, which then leaves the calendar; on a `SCHEDULED` post it returns `400`, so use `POST /social-posts/:id/unschedule` there. Leaving `scheduledAt` out keeps the current date.

A post with a YouTube entry whose `youtubeScheduledVideoId` is set and not yet published returns `409`, because the video already waits on YouTube for its publish time. Delete the post and schedule it again to change it.

Accepts the same body as `POST /social-posts`, minus `saveAsDraft`, `recurrence` and `accountIds`. Updates are partial: `text`, `contentType`, `scheduledAt`, `timezone`, `thumbnailUrl`, `thumbnailTimestampMs`, `firstComments`, `threadReplies`, `platformThumbnails` and `platformMedia` you omit keep their values. Sending `firstComments`, `threadReplies`, `platformThumbnails` or `platformMedia` replaces every stored entry, `[]` clears them, and a `threadReplies` entry with `"texts": []` removes that platform's thread. `platforms` is the exception: sending it rebuilds the post's targets from that request alone, so resend every `*ConnectionIds` array and platform config you want to keep. `mediaUrls` only take effect together with `platforms`, and on a `SCHEDULED` post they are verified in storage the same way as on create. Omitting `platforms` leaves accounts, configs, and media untouched. `platformMedia` takes effect with or without `platforms`.

**Response:** the updated post, in the same shape as `GET /social-posts/:id`.

### POST /social-posts/:id/unschedule

Take a post off the calendar without deleting it. Accepts a `SCHEDULED` post, or a `DRAFT` that still has a date, and turns it into an undated `DRAFT` with `scheduledAt: null`. Content, media and accounts are kept, and nothing publishes until the post is scheduled again with `POST /social-posts/:id/publish`. No request body.

Any other status returns `400` `Cannot edit post in current state`. An id outside the workspace returns `404` `Post not found or access denied`. A post whose YouTube video already waits on YouTube (`youtubeScheduledVideoId` set, not yet published) returns `409`.

**Response:** the post as an undated draft, in the same shape as `GET /social-posts/:id`.

### DELETE /social-posts/:id

Delete a post record. Use it to cancel a `DRAFT` or `SCHEDULED` post; a deleted scheduled post will not publish. A post that is `PUBLISHING` right now is refused with `409` `Post is being published and cannot be deleted`; wait for it to finish. Other statuses are accepted, but deleting a `COMPLETED` or `PARTIAL_FAILURE` post only drops AdaptlyPost's record: the content already exists on each network, and removing it there is a manual step. Prefer `PATCH` over delete-and-recreate. Irreversible.

Deleting a post before `scheduledAt` while its YouTube video waits on YouTube (`youtubeScheduledVideoId` set) also deletes that video from YouTube. If YouTube refuses, the call returns `502` and the post stays; try again, after reconnecting the channel if it was disconnected.

**Response:** `{ "deleted": true }`

### POST /social-posts/:id/publish

Publish a draft, either immediately or on a schedule. Accepts a `DRAFT`, and also a `SCHEDULED` post to reschedule it or push it live; any other status returns `400` `Post is not a draft`.

**Request:**

```json
{ "scheduledAt": "2026-03-15T10:00:00Z", "timezone": "UTC" }
```

- `scheduledAt` (string, optional): schedules the post for that time instead of the draft's planned date. A past time publishes now.
- `timezone` (string, required)
- `publishNow` (boolean, optional): publishes now even when the draft has a planned date. Sending it with `scheduledAt` returns `400` `Send either scheduledAt or publishNow, not both`.

Without `scheduledAt`, a draft whose planned date is in the future is scheduled for that date, and any other post publishes now. Scheduling needs `posts.schedule` and publishing now needs `posts.publish`, so a key that holds only `posts.draft` gets `403 permission_denied`. Publishing now moves the post to `PENDING`, clears its stored `scheduledAt`, queues a publishing job per platform, and `queuedPlatforms` lists them. This is irreversible from the agent's side once it returns. Scheduling sets `SCHEDULED` and returns an empty `queuedPlatforms`. `timezone` is required (use `UTC` if unknown); it is stored for display and does not shift `scheduledAt`. Fails with `400` if an account on the draft was disconnected (`Connection not found for <platform>`) or a TikTok entry has no `privacyLevel` (`Privacy level is required for TikTok posts`); fix those with `PATCH` first. A post whose YouTube video already waits on YouTube (`youtubeScheduledVideoId` set, not yet published) returns `409`.

**Response:** `{ "postId", "queuedPlatforms", "isScheduled", "scheduledAt" }`. Read `GET /social-posts/:id/results` afterwards for the per-platform outcome.

### POST /social-posts/:id/retry

Retry the platforms that failed on a post. `platformIds` takes PostPlatform ids from the results endpoint, platform names such as `BLUESKY` (every failed entry of that platform), or can be omitted to retry every failed entry. Only rows whose status is `FAILED` are reset to `PENDING` and re-queued with the same content. A value that matches neither an entry id nor a platform of the post returns `400` `Unknown retry target: ...`; if nothing matched has failed the API returns `400` `No failed platforms to retry`. The post moves to `PUBLISHING` and the retry is asynchronous, so read the results endpoint again afterwards.

**Request:**

```json
{ "platformIds": ["pp_abc002", "BLUESKY"] }
```

**Response:** `{ "postId", "queuedPlatforms", "isScheduled": false }`

Get `platformIds` from `GET /social-posts/:id/results`, or name the platform. Retry only after the cause is fixed. A platform restriction is that network's decision about the account and a retry will not clear it, while a refreshed token or replaced media will.

### POST /connect-links

Mint a link that lets someone connect social accounts to this account group without an AdaptlyPost login of their own. Built for agencies onboarding a client, and for agents that need an account connected but must never handle the credentials.

Every field is optional. With no body the link offers every platform, shows the client every account in the group, has no cap and expires after 7 days. An agent always sends a body: `PRIVATE`, the platforms asked for, `maxAccounts` and a short `expiresAt`, and widens a field only when the user asks.

| Field | Type | Meaning |
| --- | --- | --- |
| `name` | string, up to 80 characters | Label in the dashboard list of links |
| `visibility` | `PUBLIC` or `PRIVATE` | `PRIVATE` shows the client only the accounts they connected through this link |
| `allowedPlatforms` | array of platform types | Platforms the client can pick. Omit or send `[]` for every platform |
| `maxAccounts` | integer, 1 or more | The link stops working once that many accounts are connected through it |
| `expiresAt` | ISO 8601 date-time with `Z` or an offset | When the link stops working, at least 1 hour and at most 365 days away |
| `neverExpires` | boolean | `true` keeps the link working until it is revoked. Don't send it with `expiresAt` |
| `returnUrl` | URL, up to 2048 characters | Where the client goes after connecting, picking pages or channels, or being refused, instead of staying on the link page. Must be https (http only for localhost) with no credentials. Your own query parameters are kept |

**Request:**

```json
{
  "name": "Acme onboarding",
  "visibility": "PRIVATE",
  "allowedPlatforms": ["INSTAGRAM", "TIKTOK"],
  "maxAccounts": 3,
  "expiresAt": "2026-03-30T18:00:00Z"
}
```

**Response:**

```json
{
  "url": "https://adaptlypost.com/connect/abc123",
  "token": "abc123",
  "expiresAt": "2026-03-30T18:00:00.000Z",
  "name": "Acme onboarding",
  "visibility": "PRIVATE",
  "allowedPlatforms": ["INSTAGRAM", "TIKTOK"],
  "maxAccounts": 3,
  "returnUrl": null,
  "startUrls": [
    { "platform": "INSTAGRAM", "url": "https://..." },
    { "platform": "TIKTOK", "url": "https://..." }
  ]
}
```

`expiresAt` is `null` for a link made with `neverExpires: true`, and `returnUrl` is `null` when not set. An expiry outside the range, a `returnUrl` that is not https, or both `expiresAt` and `neverExpires`, answers `400`.

`startUrls` has one entry per platform the link offers that connects through the network's own consent screen, for an app that shows its own connect buttons. Bluesky and Telegram are left out because they connect on the link page. Add `server=` to the Mastodon URL, `site=` to the WordPress URL, and `via=facebook` to the Instagram URL to connect through a Facebook Page.

After a connect, a page or channel pick, or a refused start or consent, the client lands on `returnUrl` with these query parameters added: `status` (`connected` or `error`), `platform` (when known), one `accountId` per account connected (the same `id` that `GET /social-accounts` lists), and on an error `error` (a code) and `message`. A wrong Bluesky or WordPress password keeps the client on the link page.

Send the `url` to the person who owns the account. Anyone holding it can attach an account to your group, so treat it as a secret and revoke it once used.

### DELETE /connect-links/:token

Revoke a connect link before it is used or after it expires.

**Response:** `{ "success": true }`

Returns `404` when the token does not exist or belongs to another account group.

## Team

Workspaces, members and invitations. Every call acts in the key's own workspace. A key whose role lacks the permission, or whose creator is not an organization owner or admin where that is required, gets `403 permission_denied`. A plan without room for another workspace, or without a team seat for an invitation, gets `403 subscription_required` with `limitKey`, `limit` and `currentUsage` (see [Error Responses](#error-responses)). Every change here needs the user's "yes" first, with what it removes or grants shown (Safety rule 12 in SKILL.md).

### GET /workspaces

Lists the workspaces the caller can act in. An API key reaches only its own, so this returns one entry. Open to every valid key.

```json
{
  "workspaces": [
    {
      "id": "cmws0001",
      "name": "Acme",
      "organization": { "id": "org_01", "name": "Acme Agency" },
      "role": { "key": "admin", "name": "Admin" },
      "permissions": ["workspace.read", "workspace.manage", "members.read", "members.manage"],
      "isDefault": true,
      "current": true,
      "can": { "draft": true, "schedule": true, "publish": true }
    }
  ]
}
```

`permissions` is shortened here; it lists every permission the key holds.

### POST /workspaces

Creates a workspace in the caller's organization. Every organization owner and admin becomes its admin; nobody else is added. Needs `workspace.manage`, and the key's creator must be an organization owner or admin when the call is made.

| Field | Type | Meaning |
| --- | --- | --- |
| `name` | string, 1 to 100 characters, required | Unique within the organization. No `<` or `>` |
| `description` | string, up to 500 characters | No `<` or `>` |
| `connectionLimit` | integer, 0 to 10000 | Most social accounts the workspace may connect. Leave it out for no limit |

**Response (201):**

```json
{
  "id": "cmws0002",
  "name": "Acme client",
  "description": null,
  "organizationId": "org_01",
  "isDefault": false,
  "connectionLimit": 5,
  "createdAt": "2026-11-18T10:00:00.000Z"
}
```

`400` for an invalid body or a name the organization already uses. `403 subscription_required` when the plan has no room under `max_workspaces`.

### DELETE /workspaces/:id

Deletes a workspace of the caller's organization with everything it holds: posts, recurring posts, RSS feeds, inbox items, API keys and connect links. Needs `workspace.manage`, and the key's creator must be an organization owner or admin. Deleting the key's own workspace also ends the key.

**Response:** `{ "success": true }`

`400` for the default workspace, the organization's last workspace, and a workspace that still has connected social accounts. `404` when the workspace is not in this organization.

### GET /members

Lists the members of the key's workspace. Needs `members.read`.

```json
{
  "members": [
    {
      "userId": "user_01",
      "email": "jane@acme.com",
      "firstName": "Jane",
      "lastName": "Doe",
      "role": "editor",
      "organizationRoles": ["org-member"],
      "joinedAt": "2026-10-02T09:30:00.000Z"
    }
  ]
}
```

`role` is `admin`, `editor`, `contributor` or `viewer`; `organizationRoles` holds `org-owner`, `org-admin` or `org-member`. `firstName` and `lastName` may be `null`.

### DELETE /members/:userId

Removes a member from the key's workspace and revokes their API keys and connect links there. They stay in the organization and in their other workspaces. Needs `members.manage`.

**Response:** `{ "success": true }`

`400` for the caller's own account and for a member's last workspace; remove them from the organization instead. `404` when they are not a member of this workspace.

### DELETE /organization/members/:userId

Removes someone from the organization and every workspace in it, and revokes all their API keys and connect links. Needs `members.manage`, and the key's creator must be an organization owner or admin. The owner cannot be removed, and only the owner can remove an organization admin.

**Response:** `{ "success": true }`

### GET /invitations

Lists the invitations that include the key's workspace, newest first. Needs `members.manage`. Query: `limit` (1 to 100, default 20) and `offset` (default 0); page while `hasMore` is true.

```json
{
  "invitations": [
    {
      "id": "inv_01",
      "email": "sam@acme.com",
      "organizationId": "org_01",
      "organizationRole": "org-member",
      "status": "pending",
      "workspaces": [{ "workspaceId": "cmws0001", "workspaceName": "Acme", "role": "contributor" }],
      "expiresAt": "2026-11-25T10:00:00.000Z",
      "createdAt": "2026-11-18T10:00:00.000Z"
    }
  ],
  "total": 1,
  "hasMore": false
}
```

`status` is `pending`, `accepted`, `expired` or `revoked`. `workspaceName` is `null` for a workspace that no longer exists.

### POST /invitations

Emails an invitation to the organization that lasts 7 days. On accepting, the person joins the organization with `organizationRole` and each listed workspace with its role. Needs `members.manage`.

| Field | Type | Meaning |
| --- | --- | --- |
| `email` | email address, required | Who to invite |
| `organizationRole` | `org-member` (default) or `org-admin` | Only the organization owner may invite an `org-admin` |
| `workspaces` | array of `{ "workspaceId", "role" }`, at least one, required | `role` is `admin`, `editor`, `contributor` or `viewer` |
| `creditAllowance` | `{ "mode": "MONTHLY", "monthlyAmount": 1 to 100000 }` or `{ "mode": "FIXED", "balance": 0 to 100000 }` | How many of the plan owner's AI credits the person may spend. `MONTHLY` resets every plan cycle, `FIXED` moves only when spent or changed. Only an organization owner or admin may set it |

A key whose creator is not an organization admin may only invite `org-member`, only to workspaces where that creator holds `members.manage`, and only with a role no higher than their own there.

**Request:**

```json
{
  "email": "sam@acme.com",
  "workspaces": [{ "workspaceId": "cmws0001", "role": "contributor" }]
}
```

**Response (201):** the invitation, in the shape of a `GET /invitations` entry.

`400` for an invalid body, an unknown workspace, someone already invited, or someone already a member. `403 subscription_required` when the plan has no team seat left.

### DELETE /invitations/:id

Revokes a pending invitation that includes the key's workspace. Needs `members.manage`. Only the owner may revoke an invitation for an organization admin.

**Response:** the invitation with `status: "revoked"`.

`400` when the invitation is no longer pending. `404` when no such invitation includes this workspace.

## Recurring posts

A recurring post is a series created by passing `recurrence` to `POST /social-posts`. Only the next occurrence of an `ACTIVE` series exists, as a `SCHEDULED` post created about 24 hours ahead with `recurringPostId` and `occurrenceAt` set. Deleting that one post skips that date and the series continues. Occurrences missed while the series is paused are skipped, never published late.

X and LinkedIn reject a post whose text matches an earlier one. Put spintax such as `{Hi|Hello}` in the text so each occurrence differs.

Editing a series and skipping one date are only possible in the AdaptlyPost app.

Reading needs `posts.read`. A series counts as a scheduled post, so pause and resume need `posts.schedule` and delete needs `posts.delete` (admin, editor), plus `posts.others` on a series another member created. A Contributor key gets `403 permission_denied`.

### GET /recurring-posts

List the recurring posts in the account group.

**Query parameters:**

- `limit` (integer, optional): Range: 1-100. Default: 20
- `offset` (integer, optional): Min: 0. Default: 0
- `statuses` (RecurringPostStatus[], optional): Filter by status. Repeat the key per value. Any query parameter outside this list returns `400`.

**Example:**

```
GET /recurring-posts?limit=20&statuses=ACTIVE&statuses=PAUSED
```

**Response:**

```json
{
  "recurringPosts": [
    {
      "id": "cmr1a2b3c0000i0r5rcp0abcd",
      "userId": "user_01KH48SNHMPJNFYPJWZVJAKXDS",
      "status": "ACTIVE",
      "frequency": "WEEKLY",
      "interval": 1,
      "weekdays": ["MONDAY", "FRIDAY"],
      "startsAt": "2026-10-05T07:00:00.000Z",
      "timezone": "Europe/Berlin",
      "endsOn": "2026-12-31T00:00:00.000Z",
      "nextOccurrenceAt": "2026-10-09T07:00:00.000Z",
      "occurrenceCount": 1,
      "contentType": "TEXT",
      "text": "{Hi|Hello} everyone, here is the tip of the week",
      "mediaUrls": [],
      "platformTypes": ["LINKEDIN"],
      "platforms": [
        {
          "id": "cmr1a2b3c0000i0r5rcp0abcd-0",
          "platform": "LINKEDIN",
          "status": "PENDING",
          "connectionId": "cmlxly42t0004hzq1bh9kqpwl",
          "accountName": "Jane Doe"
        }
      ],
      "createdAt": "2026-09-26T12:00:00.000Z",
      "updatedAt": "2026-09-26T12:00:00.000Z"
    }
  ],
  "total": 1,
  "hasMore": false
}
```

**Fields:**

- `status`: `ACTIVE`, `PAUSED` or `ENDED`
- `pauseReason`: Set when `PAUSED`. `USER`, `CONSECUTIVE_FAILURES`, `SUBSCRIPTION_INACTIVE`, `ACCESS_LOST`, `CONNECTION_REMOVED` or `INVALID_CONTENT`
- `lastError`: The error that paused the series, when there was one
- `frequency`, `interval`, `weekdays`, `endsOn`, `maxOccurrences`: The rule from `recurrence`
- `startsAt`: The first post's time; `timezone` is the series timezone
- `nextOccurrenceAt`: The next slot that does not exist as a post yet. Absent once the series has ended
- `occurrenceCount`: Posts the series has created so far
- `contentType`, `text`, `mediaUrls`, `mediaAltTexts`, `thumbnailUrl`, `platformTypes`, `platforms`: The content and targets every occurrence copies

A series pauses itself after 3 failed posts in a row (`CONSECUTIVE_FAILURES`), when the subscription lapses (`SUBSCRIPTION_INACTIVE`), when its creator loses workspace access (`ACCESS_LOST`), when one of its accounts is disconnected (`CONNECTION_REMOVED`), or when a platform rejects the content (`INVALID_CONTENT`). Fix the cause before resuming it.

### GET /recurring-posts/:id

One recurring post, in the same shape as a list entry. An id outside the account group returns `404` `Recurring post not found`.

### POST /recurring-posts/:id/pause

Stops creating occurrences and deletes the upcoming scheduled post. No request body.

**Response:** the recurring post with `status: "PAUSED"` and `pauseReason: "USER"`.

### POST /recurring-posts/:id/resume

Continues from the next occurrence after now. Occurrences missed while paused are not published. A series whose end has already passed comes back as `ENDED`. No request body.

**Response:** the recurring post with its new `status` and `nextOccurrenceAt`.

### DELETE /recurring-posts/:id

Stops the series and deletes its upcoming scheduled post. Posts that already went out are kept. Irreversible.

**Response:** `{ "deleted": true }`

## Inbox

The inbox holds what people send the connected accounts: comments on the workspace's posts, mentions, direct messages (conversations) and Google Business Profile reviews.

| Channel | Platforms |
| --- | --- |
| comments | `FACEBOOK`, `INSTAGRAM`, `THREADS`, `YOUTUBE`, `BLUESKY`, `MASTODON`, `LINKEDIN` |
| mentions | `FACEBOOK`, `INSTAGRAM`, `THREADS`, `BLUESKY`, `MASTODON` |
| messages | `FACEBOOK`, `INSTAGRAM`, `BLUESKY`, `MASTODON` |
| reviews | `GOOGLE_BUSINESS` |

`TIKTOK` and `TWITTER` have no inbox. Every channel is exposed, including those that depend on platform permissions still in review (Messenger and Instagram messages, Threads mentions). A connection without the permission shows `RECONNECT_REQUIRED` for that channel in the summary, and a write on it answers `403` `inbox_reconnect_required`.

Reads need `inbox.read`, which every role holds. Writes, status changes and likes included, need `inbox.reply` (admin, editor) and an active AdaptlyPost plan. `POST /inbox/refresh` is a read.

Each connection syncs about every 10 minutes, so a new item can take up to 10 minutes to show up. The first sync of a connection, and of each channel, imports its history.

| Method | Path | Permission | Body / query | Answer |
| --- | --- | --- | --- | --- |
| GET | `/inbox/summary` | `inbox.read` | none | `InboxSummary` |
| POST | `/inbox/refresh` | `inbox.read` | none | `202` `{ "queued": true }` |
| GET | `/inbox/comments` | `inbox.read` | list query, `postId`, `platformPostId` | `{ comments, total, hasMore, nextCursor }` |
| GET | `/inbox/comments/:id` | `inbox.read` | none | `{ comment, parent, replies }` |
| POST | `/inbox/comments/:id/reply` | `inbox.reply` | `{ "text" }` | `201` `InboxComment` (the new reply) |
| POST | `/inbox/comments/:id/hide` | `inbox.reply` | none | `InboxComment` |
| POST | `/inbox/comments/:id/unhide` | `inbox.reply` | none | `InboxComment` |
| POST | `/inbox/comments/:id/like` | `inbox.reply` | none | `InboxComment` |
| DELETE | `/inbox/comments/:id/like` | `inbox.reply` | none | `InboxComment` |
| DELETE | `/inbox/comments/:id` | `inbox.reply` | none | `{ "deleted": true }` |
| POST | `/inbox/comments/status` | `inbox.reply` | `{ "ids", "status" }` | `{ comments, unreadCount }` |
| GET | `/inbox/mentions` | `inbox.read` | list query | `{ mentions, total, hasMore, nextCursor }` |
| POST | `/inbox/mentions/:id/reply` | `inbox.reply` | `{ "text" }` | `201` `InboxMention` |
| POST | `/inbox/mentions/status` | `inbox.reply` | `{ "ids", "status" }` | `{ mentions, unreadCount }` |
| GET | `/inbox/conversations` | `inbox.read` | list query | `{ conversations, total, hasMore, nextCursor }` |
| GET | `/inbox/conversations/:id` | `inbox.read` | none | `{ conversation, messages }` |
| POST | `/inbox/conversations/:id/messages` | `inbox.reply` | `{ "text" }` | `201` `{ conversation, message }` |
| POST | `/inbox/conversations/status` | `inbox.reply` | `{ "ids", "status" }` | `{ conversations, unreadCount }` |
| GET | `/inbox/reviews` | `inbox.read` | list query, `ratings`, `replied` | `{ reviews, total, hasMore, nextCursor }` |
| PUT | `/inbox/reviews/:id/reply` | `inbox.reply` | `{ "text" }` | `InboxReview` |
| DELETE | `/inbox/reviews/:id/reply` | `inbox.reply` | none | `InboxReview` |
| POST | `/inbox/reviews/status` | `inbox.reply` | `{ "ids", "status" }` | `{ reviews, unreadCount }` |

An unknown id, or one from another workspace, answers `404` `inbox_item_not_found`.

### List query

Every parameter is optional, on all four lists:

- `accountIds`: account `id`s from `/social-accounts`, repeated or comma separated, at most 50
- `platforms`: `PlatformType` values, repeated or comma separated
- `statuses`: `UNREAD`, `READ` or `DONE`, repeated or comma separated
- `since`: ISO 8601 date-time; only items created on the platform at or after it
- `search`: free text
- `limit`: 1-100, default 25
- `cursor`: the previous page's `nextCursor`, which is `null` on the last page

Lists are newest first: by `createdAt` for comments, mentions and reviews, by `lastMessageAt` for conversations. Comments also take `postId` (an AdaptlyPost post id from `/social-posts`) and `platformPostId` (the platform's own post id). Reviews also take `ratings` (1-5, repeated or comma separated) and `replied` (`true` or `false`).

```bash
curl -s -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  "https://post.adaptlypost.com/post/api/v1/inbox/comments?statuses=UNREAD&platforms=INSTAGRAM&platforms=FACEBOOK&limit=25"
```

### Status updates

`POST /inbox/{comments|mentions|conversations|reviews}/status` takes `{ "ids": ["..."], "status": "DONE" }` with 1-100 ids and one of `UNREAD`, `READ`, `DONE`. It changes AdaptlyPost's inbox only; nothing reaches the platform. The answer carries the updated items and the channel's new `unreadCount`.

### Reply limits

| Write | Limit |
| --- | --- |
| Comment and mention replies | The platform's comment limit: `LINKEDIN` 1250, `THREADS` 500, `BLUESKY` 300, `MASTODON` 500, `YOUTUBE` 10000, `FACEBOOK` 8000, `INSTAGRAM` 2200 characters |
| Review replies | 4096 bytes of UTF-8 (`maxReplyLength` on the review) |
| Messages | `maxMessageLength` on the conversation |

Empty or too long text answers `400` `inbox_reply_invalid`, and the message names the limit. Google allows one reply per review, so `PUT /inbox/reviews/:id/reply` puts the reply or replaces the one already there.

### Delete and like, per platform

| Platform | Delete | Like / unlike |
| --- | --- | --- |
| `FACEBOOK` | any comment on the Page's posts | yes |
| `INSTAGRAM` | any comment on the account's media | no |
| `YOUTUBE` | the channel's own comments only | no |
| `THREADS` | the account's own replies only | no |
| `BLUESKY` | the account's own replies only | yes |
| `MASTODON` | the account's own replies only | yes (favourite) |
| `LINKEDIN` | any comment on the organization's posts | yes |

`capabilities` on each comment says which actions apply to it: `canReply`, `canHide`, `canDelete`, `canLike`. An action it does not allow answers `400` `inbox_action_unsupported`. Deleting a comment removes it on the platform and in AdaptlyPost.

### Messaging window

Facebook and Instagram take a reply only within 24 hours of the person's last message. `replyWindowEndsAt` on the conversation says when that ends (`null` on other platforms), and a message after it answers `400` `inbox_messaging_window_closed`.

### Shapes

Dates are ISO 8601 UTC.

`InboxComment`:

```json
{
  "id": "ic_01",
  "accountId": "cmlxmnxn20006hzpzvo291ckg",
  "platform": "INSTAGRAM",
  "accountName": "adaptlypost",
  "postId": "cmm0z0k3q0000i0r5mxn0hfhs",
  "platformPostId": "17912345678901234",
  "postText": "Plan a week of posts in one sitting",
  "postPermalink": "https://www.instagram.com/p/…",
  "platformCommentId": "17998765432109876",
  "parentPlatformCommentId": null,
  "isReply": false,
  "author": { "id": "1784…", "name": "Jane Doe", "username": "jane.doe", "avatarUrl": "https://…" },
  "text": "Does this work with Reels?",
  "permalink": "https://www.instagram.com/p/…",
  "likeCount": 2,
  "createdAt": "2026-11-08T09:12:00.000Z",
  "status": "UNREAD",
  "isHidden": false,
  "isOwn": false,
  "replied": false,
  "repliedAt": null,
  "likedByAccount": false,
  "capabilities": { "canReply": true, "canHide": true, "canDelete": true, "canLike": false }
}
```

`postId` is `null` when the post was not published through AdaptlyPost. `parentPlatformCommentId` is `null` on a top-level comment. `replied` is true when the account has a reply under the comment, sent from AdaptlyPost or from the platform's own app. `author.id`, `author.username`, `author.avatarUrl`, `permalink`, `likeCount` and `repliedAt` can be `null`.

`InboxMention`: `id`, `accountId`, `platform`, `accountName`, `platformMentionId`, `author { id, name, username, avatarUrl }`, `text`, `permalink`, `thumbnailUrl`, `createdAt`, `status`, `replied`, `repliedAt`, `capabilities { canReply }`, `replies: [{ id, text, permalink, createdAt }]`.

`InboxConversation`: `id`, `accountId`, `platform`, `accountName`, `participant { id, name, username, avatarUrl }`, `lastMessageText`, `lastMessageAt`, `lastMessageIsOwn`, `status`, `repliedAt`, `replyWindowEndsAt`, `maxMessageLength`, `capabilities { canReply }`.

`InboxMessage`: `id`, `isOwn`, `text`, `hasAttachments`, `createdAt`.

`InboxReview`: `id`, `accountId`, `platform` (`GOOGLE_BUSINESS`), `accountName`, `platformReviewId`, `reviewer { name, avatarUrl, isAnonymous }`, `rating` (1-5), `text`, `reply` (`{ text, updatedAt }` or `null`), `createdAt`, `updatedAt`, `status`, `repliedAt`, `maxReplyLength`, `capabilities { canReply }`.

`InboxSummary`:

```json
{
  "unread": { "comments": 12, "mentions": 3, "conversations": 2, "reviews": 1 },
  "accounts": [
    {
      "accountId": "cmlxmnxn20006hzpzvo291ckg",
      "platform": "INSTAGRAM",
      "accountName": "adaptlypost",
      "avatarUrl": "https://…",
      "needsReconnect": false,
      "lastSyncedAt": "2026-11-08T09:20:00.000Z",
      "lastErrorCode": null,
      "comments": "AVAILABLE",
      "mentions": "AVAILABLE",
      "messages": "RECONNECT_REQUIRED",
      "reviews": "UNSUPPORTED"
    }
  ]
}
```

Each channel field is `AVAILABLE`, `RECONNECT_REQUIRED` (the connection lacks the permission or its token expired; the user reconnects the account in AdaptlyPost) or `UNSUPPORTED` (the platform has no such channel).

### Refusals

Inbox refusals use the usual body `{ "statusCode", "error", "code", "message" }`:

| `code` | Status | When | What to do |
| --- | --- | --- | --- |
| `inbox_item_not_found` | 404 | Unknown id, or another workspace's | Stop |
| `inbox_action_unsupported` | 400 | A hide, delete or like the platform or this comment does not allow (see `capabilities`) | Stop |
| `inbox_reconnect_required` | 403 | The connection lacks the permission for this channel or action (channels still in platform review included), or its token expired | Ask the user to reconnect the account in AdaptlyPost; do not retry |
| `inbox_reply_invalid` | 400 | Empty text, or over the limit (the message names it) | Fix the text |
| `inbox_messaging_window_closed` | 400 | The Facebook or Instagram 24-hour window passed | Stop |
| `inbox_rate_limited` | 429 | The platform rate limited AdaptlyPost | Retry after a while |
| `inbox_platform_error` | 503 | The platform failed | Retry later |

## Webhooks

Rather than polling `GET /social-posts` to find out whether something published, register a URL and let AdaptlyPost call you.

### Events

| event | fires when |
| --- | --- |
| `post.scheduled` | A post is accepted onto the schedule |
| `post.published` | Every targeted platform published |
| `post.partially_failed` | Some platforms published and some failed |
| `post.failed` | Every platform failed |
| `account.unauthorized` | A platform rejected a connected account's token; `data.account` carries the account `id`, `platform`, `displayName`, `pageId` (Facebook), `status: "unauthorized"` and the platform's `reason`. The account stays on `/social-accounts` with `status: "unauthorized"` until reconnected |
| `image.completed` | An AI image job finished; `data.image` carries `jobId`, `sessionId`, `prompt`, `imageUrl` and `imageId` |
| `image.failed` | An AI image job failed; `data.image` carries `jobId`, `sessionId`, `prompt` and `error` |
| `comment.created` | The inbox sync found a new comment from someone else; `data.comment` is an [`InboxComment`](#shapes) |
| `comment.replied` | The account replied to a comment, from AdaptlyPost (dashboard or API) or from the platform's own app; `data.comment` is the reply and `data.parentCommentId` the comment it answers |
| `mention.created` | A new mention; `data.mention` is an `InboxMention` |
| `message.received` | A new inbound direct message; `data.conversation` and `data.message` |
| `review.created` | A new Google review; `data.review` is an `InboxReview` |

A webhook's `events` decides what it receives. Omitted or empty, it gets the seven post, account and image events above, for every post and account of the workspace, until it is deleted; webhooks created before `events` existed keep exactly that. Inbox events reach only a webhook whose `events` names them, and a non-empty `events` means only the listed events. Inbox events fire for items the sync finds after the first sync of a connection and channel, which imports history without firing anything, and arrive within about 10 minutes, not in real time. Register a webhook only for a URL the user gave and after they agree to what it will receive; to follow one post, poll `GET /social-posts/:id`. Post events carry `data.post`, account events `data.account`, image events `data.image`. `data.post` has the same shape as `GET /social-posts/:id`, so it carries every platform entry field, first comments and Google Business Profile settings included.

### POST /api/v1/webhooks

**Request:** `{ "url": "https://example.com/hooks/adaptlypost", "events": ["post.published", "post.failed"] }`

`events` (string[], optional): the event names this webhook receives, from the table above. Omit it or send `[]` for the seven post, account and image events.

**Response:**

```json
{
  "id": "wh_abc123",
  "url": "https://example.com/hooks/adaptlypost",
  "active": true,
  "secret": "whsec_..."
}
```

> The signing secret is returned **only here, only once**. It is not in `GET /webhooks` or `GET /webhooks/:id`. Store it when you create the webhook or delete it and make a new one.

Maximum 10 webhooks per account group. The URL must reach a public host: deliveries to a private or internal address are refused and the delivery records an error.

### GET /api/v1/webhooks

Returns `{ "webhooks": [...] }` without secrets.

### GET /api/v1/webhooks/:id

One webhook, without its secret.

### PATCH /api/v1/webhooks/:id

Body accepts `url`, `active` and `events`. Set `active: false` to pause deliveries without losing the registration and its secret. `events` replaces the list; `[]` goes back to the seven post, account and image events.

### DELETE /api/v1/webhooks/:id

**Response:** `{ "deleted": true }`

### POST /api/v1/webhooks/:id/test

Sends a `webhook.test` event to the registered URL so you can verify signature checking before a real post depends on it.

### Verifying a delivery

Each request carries four headers:

| header | contents |
| --- | --- |
| `x-adaptly-signature` | `sha256=<hex>` |
| `x-adaptly-timestamp` | Unix timestamp used in the signature |
| `x-adaptly-event` | Event name, for example `post.published` |
| `x-adaptly-webhook-id` | Which registration produced this delivery |

The signature is `HMAC-SHA256(secret, "<timestamp>.<raw body>")`, hex encoded and prefixed with `sha256=`. Sign the **raw** body, before any JSON parsing, or the bytes will not match.

```js
const expected =
  "sha256=" +
  crypto.createHmac("sha256", secret).update(`${timestamp}.${rawBody}`).digest("hex");
crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(received));
```

Compare with a timing-safe function, and reject timestamps that are far from now so an old capture cannot be replayed.

### Delivery behaviour

AdaptlyPost retries a failing endpoint 5 times with a 10 second timeout per attempt. After 20 consecutive failures the webhook is deactivated, which is why a receiver that has been down for a while goes quiet and stays quiet: reactivate it with `PATCH /webhooks/:id`.

## Analytics

Post performance for the connected accounts. Covered platforms: `FACEBOOK`, `INSTAGRAM`, `THREADS`, `TIKTOK`, `PINTEREST`, `BLUESKY`, `YOUTUBE`, `TWITTER`, `LINKEDIN`, `GOOGLE_BUSINESS`. `GOOGLE_BUSINESS` reports only location-level impressions (how often the location was seen); its posts are listed with every per-post metric `null`. `MASTODON`, `TELEGRAM`, `TUMBLR` and `WORDPRESS` have no analytics and are ignored by every filter.

Connecting an account imports its posts from the last 180 days, and less for accounts whose platform exposes less; `historyHorizonAt` on the sync status says how far. Analytics are kept from then on while the account stays connected, so any date range in that history can be queried. A post keeps refreshing for 180 days after it is published, then holds its last numbers. Weekly buckets and day boundaries follow the workspace defaults.

Every window endpoint takes:

- `from` (string, required): ISO 8601 start of the window
- `to` (string, required): ISO 8601 end of the window, not earlier than `from`
- `platforms` (PlatformType[], optional): repeat the key per value; omit for every covered platform. `/analytics/platform-breakdown` does not take it
- `connectionIds` (string[], optional): account `id`s from `/social-accounts`, repeat the key per value; omit for every account

Metrics count posts published inside the window. Every comparison uses the window of the same length immediately before `from`. Accounts listed in `accountActivityConnectionIds` (LinkedIn personal profiles, Google Business Profile locations) are the exception: they count their account-wide activity on each day of the window, every post whenever published, instead of the lifetime totals of posts published in it, and they have no rows in `/analytics/posts`.

### GET /analytics/overview

```json
{
  "views": { "value": 48210, "previousValue": 39100, "deltaPercent": 23.3 },
  "likes": { "value": 2210, "previousValue": 1980, "deltaPercent": 11.6 },
  "comments": { "value": 340, "previousValue": 410, "deltaPercent": -17.1 },
  "shares": { "value": 128, "previousValue": null, "deltaPercent": null },
  "followers": { "value": 12980, "previousValue": 12410, "deltaPercent": 4.6 },
  "postsCount": { "value": 42, "previousValue": 37, "deltaPercent": 13.5 },
  "avgViewsPerPost": { "value": 1147.9, "previousValue": 1056.8, "deltaPercent": 8.6 },
  "engagementRate": { "value": 5.55, "previousValue": 6.11, "deltaPercent": -9.2 },
  "partialMetrics": ["shares"],
  "accountActivityConnectionIds": ["cmlxmnxn20006hzpzvo291ckh"],
  "lastSyncedAt": "2026-09-08T06:12:41.000Z"
}
```

`followers` is the latest count as of `to`, compared with the count as of the end of the previous window. `engagementRate` is likes + comments + shares over views, as a percentage. `partialMetrics` lists metrics at least one selected platform cannot report, so their totals cover only the platforms that can; a metric no selected platform reports is `null`. `deltaPercent` is `null` when the previous value is 0 or unknown. `accountActivityConnectionIds` lists the accounts counted by daily account-wide activity, as described above.

### GET /analytics/timeseries

Extra parameter: `granularity` (`DAILY`, the default, `WEEKLY` or `MONTHLY`).

```json
{
  "points": [
    { "date": "2026-08-01T00:00:00.000Z", "views": 1820, "likes": 90, "comments": 12, "shares": 4, "followers": 12420, "postsCount": 2, "engagementRate": 5.8 }
  ]
}
```

`date` is the start of the bucket in UTC. `followers` is the latest known count at the end of the bucket; the other counters sum posts published inside it.

### GET /analytics/platform-breakdown

Takes `from`, `to` and `connectionIds`.

```json
{
  "platforms": [
    {
      "platform": "INSTAGRAM",
      "followers": { "value": 8210, "previousValue": 7990, "deltaPercent": 2.8 },
      "views": { "value": 30100, "previousValue": 24800, "deltaPercent": 21.4 },
      "likes": { "value": 1500, "previousValue": 1310, "deltaPercent": 14.5 },
      "comments": { "value": 210, "previousValue": 260, "deltaPercent": -19.2 },
      "shares": { "value": 128, "previousValue": 90, "deltaPercent": 42.2 },
      "postsCount": { "value": 20, "previousValue": 18, "deltaPercent": 11.1 },
      "avgViewsPerPost": { "value": 1505, "previousValue": 1377.8, "deltaPercent": 9.2 },
      "engagementRate": { "value": 6.1, "previousValue": 6.7, "deltaPercent": -9 },
      "supportedMetrics": ["followers", "views", "likes", "comments", "shares", "saves", "reach", "impressions"],
      "accountActivityConnectionIds": []
    }
  ]
}
```

One row per platform with data in the workspace. Compare two platforms only on metrics both list in `supportedMetrics`. `accountActivityConnectionIds` names the platform's accounts counted by daily account-wide activity.

### GET /analytics/posts

Extra parameters: `sortBy` (`VIEWS`, `LIKES`, `COMMENTS`, `SHARES`, `SAVES`, `CLICKS`, `IMPRESSIONS`, `ENGAGEMENT_RATE`, or `PUBLISHED_AT`, the default), `page` (from 1), `limit` (1-100, default 20).

```json
{
  "posts": [
    {
      "id": "ap_01j9x…",
      "postId": "cmm0z0k3q0000i0r5mxn0hfhs",
      "postPlatformId": "cmm0z0k3u0001i0r5dlbfa440",
      "platform": "INSTAGRAM",
      "publishedAt": "2026-08-14T10:00:12.000Z",
      "title": "Plan a week of posts in one sitting",
      "thumbnailUrl": "https://…",
      "permalink": "https://www.instagram.com/p/…",
      "connectionId": "cmlxmnxn20006hzpzvo291ckg",
      "accountName": "adaptlypost",
      "metrics": { "views": 9120, "likes": 410, "comments": 38, "shares": 22, "saves": 61, "clicks": null, "impressions": 10230, "reach": 8540, "engagementRate": 5.15 }
    }
  ],
  "total": 42,
  "page": 1,
  "limit": 20,
  "hasMore": true
}
```

Includes posts published through AdaptlyPost and posts discovered on the accounts; discovered posts have `postId` and `postPlatformId` set to `null`. `postId` is the id for `GET /social-posts/:id`, `postPlatformId` is the `platformId` from `/social-posts/:id/results`, and `connectionId` is the account `id` from `/social-accounts`. A metric the platform does not report is `null`. YouTube videos also carry `engagedViews` (views that played past the first frame), `averageViewDurationSeconds` and `averageViewPercentage` in `metrics`, `null` until YouTube Analytics reports the video, which lags a few days.

### GET /analytics/top-posts

Same rows as `/analytics/posts` without pagination: the top `limit` (1-50, default 10) ordered by `sortBy` (default `VIEWS`). Returns `{ "posts": [...] }`.

### GET /analytics/discovered-posts

Posts found on the connected accounts that AdaptlyPost did not publish, for a read-only calendar. Extra parameter: `limit` (1-1000, default 200).

```json
{
  "posts": [
    { "id": "ap_01j9x…", "platform": "TIKTOK", "publishedAt": "2026-08-20T17:30:00.000Z", "text": "…", "thumbnailUrl": "https://…", "permalink": "https://www.tiktok.com/@…", "accountName": "adaptlypost" }
  ]
}
```

### GET /analytics/sync-status

No parameters.

```json
{
  "accountGroupId": "ag_…",
  "syncInProgress": false,
  "lastSyncedAt": "2026-09-08T06:12:41.000Z",
  "historyHorizonAt": "2026-03-12T00:00:00.000Z",
  "platforms": [
    {
      "platform": "INSTAGRAM",
      "connectionId": "cmlxmnxn20006hzpzvo291ckg",
      "accountName": "adaptlypost",
      "status": "IDLE",
      "lastSyncedAt": "2026-09-08T06:12:41.000Z",
      "lastErrorMessage": null,
      "historyHorizonAt": "2026-03-12T00:00:00.000Z",
      "lastDiscoveryAt": "2026-09-08T06:10:03.000Z",
      "needsAnalyticsReconnect": false
    }
  ]
}
```

`status` is `IDLE`, `QUEUED`, `SYNCING` or `FAILED`. `connectionId` is the account `id` from `/social-accounts`. Accounts on platforms without analytics are not listed. `needsAnalyticsReconnect: true` means the account was connected before the analytics permissions existed; it stays parked, with no syncs and no errors, until the user reconnects it (a connect link works) and approves the extra permissions.

### POST /analytics/sync

No body. Queues a sync for every covered account and re-reads the last 7 days. Analytics refresh on their own every few hours, so this is for "I just published" moments. One run per workspace every 15 minutes. A YouTube channel read in the last 12 hours is skipped.

```json
{ "queued": false, "message": "Analytics were synced recently. Please try again in 412 seconds", "cooldownSecondsRemaining": 412 }
```

Inside the cooldown, or when no connected account supports analytics, the response is still `200` with `queued: false`; inside the cooldown `cooldownSecondsRemaining` says how long to wait. When queued, `cooldownSecondsRemaining` is `null`. The run is asynchronous: poll `GET /analytics/sync-status` until `syncInProgress` is `false`, then read the metrics again.

## Rate limits

600 requests per minute per API token, counted on a hash of the token rather than on IP.

Every response carries the RFC 9331 headers:

```
RateLimit-Policy: "adaptlypost-api";q=600;w=60
RateLimit-Limit: 600
RateLimit-Remaining: 587
RateLimit-Reset: 43
```

A `429` adds `Retry-After` in seconds. Wait it out rather than retrying immediately, since a retry inside the window just burns the next allowance.

## GET /openapi.json

The full OpenAPI 3 spec, and the one endpoint that needs no authentication, so Make, n8n and Zapier can import it without a token.

## Enums

**PlatformType:**
`FACEBOOK`, `INSTAGRAM`, `THREADS`, `TIKTOK`, `TWITTER`, `BLUESKY`, `MASTODON`, `LINKEDIN`, `PINTEREST`, `YOUTUBE`, `GOOGLE_BUSINESS`, `TELEGRAM`, `TUMBLR`, `WORDPRESS`

**ContentType:**
`TEXT`, `IMAGE`, `VIDEO`, `CAROUSEL`, `DOCUMENT`

**TikTokPrivacyLevel:**
`PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY`

**MetaVideoPostType (Instagram & Facebook):**
`FEED`, `REEL`, `STORY`

**GoogleBusinessTopicType:**
`STANDARD`, `EVENT`, `OFFER`

**GoogleBusinessCallToActionType:**
`BOOK`, `ORDER`, `SHOP`, `LEARN_MORE`, `SIGN_UP`, `CALL`

**MediaAspectRatio:**
`SQUARE`, `PORTRAIT`, `VERTICAL`, `LANDSCAPE`

**MediaAspectRatioFit:**
`CROP`, `PAD`

**FirstCommentStatus:**
`PENDING`, `PUBLISHED`, `FAILED`

**InstagramAudioType:**
`music`, `original_sound`

**YouTubePostType:**
`VIDEO`, `SHORTS`

**YouTubePrivacyStatus:**
`public`, `private`, `unlisted`

**YouTubeLicense:**
`youtube`, `creativeCommon`

**RecurrenceFrequency:**
`DAILY`, `WEEKLY`, `MONTHLY`, `YEARLY`

**Weekday:**
`MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`

**RecurringPostStatus:**
`ACTIVE`, `PAUSED`, `ENDED`

**RecurringPostPauseReason:**
`USER`, `CONSECUTIVE_FAILURES`, `SUBSCRIPTION_INACTIVE`, `ACCESS_LOST`, `CONNECTION_REMOVED`, `INVALID_CONTENT`

**AnalyticsGranularity:**
`DAILY`, `WEEKLY`, `MONTHLY`

**AnalyticsSortMetric:**
`VIEWS`, `LIKES`, `COMMENTS`, `SHARES`, `SAVES`, `CLICKS`, `IMPRESSIONS`, `ENGAGEMENT_RATE`, `PUBLISHED_AT`

**AnalyticsSyncJobStatus:**
`IDLE`, `QUEUED`, `SYNCING`, `FAILED`

**InboxStatus:**
`UNREAD`, `READ`, `DONE`

**InboxChannelAccess:**
`AVAILABLE`, `RECONNECT_REQUIRED`, `UNSUPPORTED`

**WebhookEventName:**
`post.scheduled`, `post.published`, `post.partially_failed`, `post.failed`, `account.unauthorized`, `image.completed`, `image.failed`, `comment.created`, `comment.replied`, `mention.created`, `message.received`, `review.created`

## Error Responses

- `400` — Bad request (missing fields, invalid data, validation errors)
- `401` — Invalid, expired, revoked or missing API token. `code: token_issuer_lost_access` means the member who created the key lost access to the workspace, so the key was revoked; a new key from a current member is the only fix
- `403` — The key's role lacks the permission (`code: permission_denied`), or the workspace plan is not active or has no room for what was asked (`code: subscription_required`). On the inbox, `code: inbox_reconnect_required` means the account must be reconnected in AdaptlyPost
- `404` — Resource not found or access denied (`code: inbox_item_not_found` on the inbox)
- `429` — Rate limit exceeded; see `Retry-After`. On the inbox, `code: inbox_rate_limited` means the platform, not AdaptlyPost, rate limited the call
- `503` — `code: inbox_platform_error`: the platform failed; retry later

The inbox codes and what to do about each are in [Inbox refusals](#refusals).

**Example error:**

```json
{
  "message": ["timezone must be a string", "timezone should not be empty"],
  "error": "Bad Request",
  "statusCode": 400
}
```

**Post refused for its content (400):**

```json
{
  "statusCode": 400,
  "error": "Bad Request",
  "code": "post_validation_failed",
  "message": "Text exceeds maximum length for X. Maximum is 280 characters",
  "issues": [
    { "code": "TEXT_TOO_LONG", "severity": "ERROR", "message": "Text exceeds maximum length for X. Maximum is 280 characters", "platform": "TWITTER", "connectionId": "conn_tw1" }
  ]
}
```

`POST /social-posts` answers this way when a check refuses the post. `message` is one string for one issue and an array of strings for several. `issues` has the same shape as in [POST /social-posts/validate](#post-social-postsvalidate). Fix what they name before sending again.

**Permission denied (403):**

```json
{
  "statusCode": 403,
  "error": "Forbidden",
  "code": "permission_denied",
  "requiredPermission": "posts.publish",
  "role": "contributor",
  "keyRole": "contributor",
  "issuerRole": "editor",
  "tokenType": "api_token",
  "message": "The Contributor role cannot publish posts. Send the post with saveAsDraft: true and ask a workspace member to publish it."
}
```

`requiredPermission` is the permission the operation needs (see [Roles and permissions](#roles-and-permissions)), `role` is the role actually in force, which is the issuer's role when the member who created the key has since been demoted below the key's role; `keyRole` is the role recorded on the key, `issuerRole` the creator's current role, and `tokenType` is `api_token` or `oauth`. `message` says what the role cannot do and what to do instead, in the request's language. Stop on this error: a retry or another key of the same role gets the same answer.

**Plan limit reached (403):**

```json
{
  "statusCode": 403,
  "error": "Forbidden",
  "code": "subscription_required",
  "errorCode": "LIMIT_EXCEEDED",
  "message": "Workspace limit reached for your plan",
  "limitKey": "max_workspaces",
  "limit": 3,
  "currentUsage": 3
}
```

`POST /workspaces` answers this way when the plan has no room for another workspace, and `POST /invitations` when it has no team seat left. Tell the user to upgrade; a retry gets the same answer.

**Key revoked because its creator left (401):**

```json
{
  "statusCode": 401,
  "error": "Unauthorized",
  "code": "token_issuer_lost_access",
  "message": "This API key no longer works: the member who created it lost access to the workspace. Ask a workspace admin for a new key."
}
```
