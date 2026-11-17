# Platform-Specific Configs Reference

Platform configs are passed as arrays in both `POST /social-posts` and `POST /social-posts/bulk` request bodies (`googleBusinessConfigs`, `tumblrConfigs` and `wordpressConfigs` included), except `linkedinConfigs` and `twitterConfigs`, which only `POST /social-posts` and `PATCH /social-posts/:id` take. Each config object is tied to a specific connection via `connectionId` (or `pageId` for Facebook — set it to the same value you put in the top-level `pageIds` array, i.e. the Facebook account's `id` from `/social-accounts`).

For bulk scheduling, configs can be set at two levels:
- **Batch-level** (top-level request body) — applied to all posts as the default
- **Per-post** (inside individual post items) — overrides batch-level for that specific post

## TikTok — `tiktokConfigs`

```json
{
  "tiktokConfigs": [
    {
      "connectionId": "tiktok-connection-id",
      "privacyLevel": "PUBLIC_TO_EVERYONE",
      "title": "Video title",
      "caption": "Extended caption text",
      "allowComments": true,
      "allowDuet": true,
      "allowStitch": true,
      "sendAsDraft": false,
      "aiGenerated": false,
      "brandedContent": false,
      "brandedContentOwnBrand": false,
      "autoAddMusic": false
    }
  ]
}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `connectionId` | string | **yes** | TikTok account connection ID |
| `privacyLevel` | string | **yes** | `PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY` |
| `title` | string | no | Max 90 chars. Photo posts: the title shown above the description. Video posts: sent as the caption only when `caption` is empty |
| `caption` | string | no | Photo posts: the description, max 4,000 characters. Video posts: the caption, max 2,200 characters. Falls back to `title`, then to the post text |
| `allowComments` | boolean | no | Allow comments on the video |
| `allowDuet` | boolean | no | Allow duets |
| `allowStitch` | boolean | no | Allow stitches |
| `sendAsDraft` | boolean | no | Deliver to the creator's TikTok inbox as a draft. A video sent this way can reach the inbox without a caption, because TikTok's inbox upload takes none |
| `aiGenerated` | boolean | no | Mark content as AI-generated |
| `brandedContent` | boolean | no | Sponsored/partnership content |
| `brandedContentOwnBrand` | boolean | no | Self-promotional content |
| `autoAddMusic` | boolean | no | Auto-add background music |

**Media notes:**

- Video: MP4/MOV, H.264, max 250MB, 3s-10min. Best: 15-30s, 1080x1920 (9:16)
- When the post video runs longer, give TikTok a shorter cut with top-level `platformMedia` (`{ "platform": "TIKTOK", "mediaUrls": [...] }`); the other platforms keep the post `mediaUrls`
- Carousels: 2-35 images (photo slideshows)
- Caption: max 2,200 characters on a video, 4,000 on a photo post

## Instagram — `instagramConfigs`

```json
{
  "instagramConfigs": [
    {
      "connectionId": "instagram-connection-id",
      "postType": "REEL"
    }
  ]
}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `connectionId` | string | **yes** | Instagram account connection ID |
| `postType` | string | no | `FEED`, `REEL`, or `STORY`. Default: `FEED` |
| `trialGraduation` | string | no | Publish the reel as a trial reel. `MANUAL`: you share it to followers from the Instagram app. `SS_PERFORMANCE`: Instagram shares it if it performs well |
| `shareToStory` | boolean | no | Also publish the same media as a story next to the `FEED` or `REEL` post. Ignored when `postType` is `STORY` |
| `collaborators` | string[] | no | Up to 3 Instagram usernames invited as collaborators. A leading `@` is stripped and duplicates are dropped |
| `userTags` | object[] | no | Up to 20 public accounts tagged in the media, each `{ "username": "...", "x": 0.5, "y": 0.3 }`. See [User tags](#user-tags) |
| `aiGenerated` | boolean | no | Disclose that the post was made or edited with AI. Instagram shows its "AI info" label on the post. Works on images, carousels, reels and stories, and a story made with `shareToStory` carries the label too |
| `audio` | object | no | Music or an original sound added to a Reel. See [Audio](#audio) |

**Content types:**

- **FEED**: Feed posts. Single image, carousel (up to 10 images and videos), or video up to 15 minutes
- **REEL**: Video up to 15 minutes, 9:16 recommended. Needs `contentType: VIDEO`
- **STORY**: 24-hour temporary content. `IMAGE`, `VIDEO` or `CAROUSEL`; a carousel story publishes each item as its own story, in order

**Share to story:** `shareToStory: true` publishes the same media as a story too. The story is its own entry in the post's `platforms` with `postType: STORY`, so it succeeds, fails and retries on its own. It skips the caption, first comment, cover, collaborators, user tags, trial and audio, needs `IMAGE`, `VIDEO` or `CAROUSEL`, and a story video must be 60 seconds or shorter.

**Collaborators:** work on feed images, carousels and reels. A story or a trial reel with collaborators returns `400`. Each collaborator gets an invite in Instagram and must accept it before the post shows on their profile.

#### User tags

```json
{
  "connectionId": "instagram-connection-id",
  "postType": "FEED",
  "userTags": [
    { "username": "jane.doe", "x": 0.25, "y": 0.6 },
    { "username": "@acme", "x": 0.7, "y": 0.4 }
  ]
}
```

- `username`: a public Instagram username, 1 to 30 letters, digits, dots or underscores. A leading `@` is stripped and a repeated username keeps its first entry.
- `x`, `y`: where the tag sits, from 0 to 1 across the image from the top-left corner (`x` left to right, `y` top to bottom).
- Tags work on one image (feed or story) or one video (Reel or story). A carousel or several stories with tags returns `400`.
- On a feed image every tag needs both `x` and `y`, or the API returns `400`. On a story they are optional, but a tag with only one of them returns `400`. On a video they are ignored and the person is tagged on the video as a whole.
- If Instagram refuses a tag because the account is private or doesn't exist, the post goes out without its tags and `instagramUntaggedUsernames` lists the refused usernames.
- The story that `shareToStory` adds does not carry the tags.
- The post reads them back as `instagramUserTags` on each Instagram platform entry.

#### Audio

```json
{
  "connectionId": "instagram-connection-id",
  "postType": "REEL",
  "audio": { "audioId": "1234567890", "title": "Summer Nights", "artist": "The Band", "audioVolume": 80, "videoVolume": 30 }
}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `audioId` | string | **yes** | From `GET /social-accounts/:id/instagram-audio` (max 64 chars) |
| `title` | string | no | Track title, stored for display only (max 255 chars) |
| `artist` | string | no | Artist or creator, stored for display only (max 255 chars) |
| `audioVolume` | integer | no | Volume of the added audio, 1-100. Default: 100 |
| `videoVolume` | integer | no | Volume of the video's own sound, 1-100. Default: 100 |

Needs `contentType: VIDEO`, a `postType` other than `STORY`, and an account whose `supportsInstagramAudio` is `true` in `/social-accounts` (connected through Facebook).

**Trial reels:** Instagram shows a trial reel to non-followers first and keeps it off your followers' feeds and your profile grid until it is shared. Only a single video posted as `REEL` or `FEED` can be a trial; a story, image or carousel with `trialGraduation` is rejected with a 400. The account must be a professional account that Instagram has enabled for trial reels, otherwise the Instagram platform fails with a message saying so.

**Media notes:**

- Video: max 1GB, up to 15 minutes for feed videos and Reels
- Carousels: up to 10 images or videos

## Facebook — `facebookConfigs`

```json
{
  "facebookConfigs": [
    {
      "pageId": "FACEBOOK_ACCOUNT_ID_FROM_SOCIAL_ACCOUNTS",
      "postType": "REEL",
      "videoTitle": "My Video Title"
    }
  ]
}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `pageId` | string | **yes** | Same value as in the top-level `pageIds` array (the Facebook account's `id` from `/social-accounts`) |
| `postType` | string | no | `FEED`, `REEL`, or `STORY`. Default: `FEED` |
| `videoTitle` | string | no | Video title (max 255 chars) |
| `shareToStory` | boolean | no | Also publish the same media as a story next to the `FEED` or `REEL` post. Ignored when `postType` is `STORY` |
| `textFormatPresetId` | string | no | Facebook's id for a colored text background (digits, 1-20), for example `106018623298955` (solid purple) or `249307305544279` (red to blue gradient) |
| `imageLayout` | string | no | `GRID` (photo grid) or `CAROUSEL` (swipeable cards, each opening its own link). Default: `GRID` |
| `carouselCards` | array | no | Up to 5 cards, one per image in the same order as `mediaUrls`: `link` (**required**, http or https URL, max 2048 chars), `title` (max 100 chars), `description` (max 200 chars). Only read when `imageLayout` is `CAROUSEL` |
| `aiGenerated` | boolean | no | Disclose that the post was made or edited with AI. Facebook shows its "AI info" label on the post. Works on every `contentType: VIDEO` post, whatever its `postType`: Facebook publishes every video as a reel, and a video story carries the label too. Photos, carousels and text posts are rejected with a `400`. Omit it or send `false` for no label |

**Content types:**

- **FEED**: Permanent feed content. Up to 10 images OR 1 video. Text limit: 63,206 chars
- **REEL**: Short-form vertical video
- **STORY**: 24-hour temporary content. `IMAGE`, `VIDEO` or `CAROUSEL`; a carousel story publishes each item as its own story

**Share to story:** the story is its own entry in the post's `platforms` with `postType: STORY`. It skips the caption, video title and text background, needs `IMAGE`, `VIDEO` or `CAROUSEL`, and a story video must be 60 seconds or shorter.

**Text background:** only for `contentType: TEXT` with no media and text up to 130 characters; anything else returns `400`. Links in the text show without a preview. If Facebook refuses the background, the post goes out as plain text.

**Link carousel:** `imageLayout: CAROUSEL` needs `postType: FEED`, 2 to 5 images, no videos and one `carouselCards` entry per image; anything else returns `400`. Facebook shows a card's image and title only when its link goes to a website the Page owns. Any other link makes the post fail with a message saying so. Posts that leave out `imageLayout` get a photo grid.

**AI info label:** `aiGenerated: true` works on every `VIDEO` post, whatever its `postType`, because Facebook publishes every video as a reel, and a video story carries the label too. A photo, carousel or text post returns `400` with `code: post_validation_failed` and the issue code `FACEBOOK_AI_LABEL_VIDEO_ONLY`. The post reads it back as `facebookAiGenerated`.

**Media notes:**

- Images: JPG/PNG, max 30MB each, up to 10 per post
- Cannot mix images and videos in same post

## YouTube — `youtubeConfigs`

```json
{
  "youtubeConfigs": [
    {
      "connectionId": "youtube-connection-id",
      "postType": "SHORTS",
      "videoTitle": "My Video Title",
      "tags": ["tutorial", "howto"],
      "privacyStatus": "public",
      "license": "youtube",
      "notifySubscribers": true,
      "allowEmbedding": true,
      "madeForKids": false,
      "aiGenerated": false,
      "defaultAudioLanguage": "pt-BR",
      "categoryId": "22",
      "playlistId": "PLxxxxxxxx",
      "scheduleOnYouTube": false
    }
  ]
}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `connectionId` | string | **yes** | YouTube channel connection ID |
| `postType` | string | no | `VIDEO` or `SHORTS`. Default: `VIDEO` |
| `videoTitle` | string | no | Video title (max 100 chars) |
| `tags` | string[] | no | Video tags (max 20 tags) |
| `privacyStatus` | string | no | `public`, `private`, or `unlisted`. Default: `public` |
| `license` | string | no | `youtube` or `creativeCommon` |
| `notifySubscribers` | boolean | no | Notify subscribers on publish |
| `allowEmbedding` | boolean | no | Allow embedding on other sites |
| `madeForKids` | boolean | no | COPPA compliance flag |
| `aiGenerated` | boolean | no | Disclose altered or synthetic content, such as an AI voice, an AI avatar or realistic footage that was generated or edited. YouTube shows its "Altered or synthetic content" label on the video. Sets `status.containsSyntheticMedia`. Omit it or send `false` for no label. Works on videos and Shorts |
| `defaultAudioLanguage` | string or null | no | Language spoken in the video's original audio, as a BCP-47 tag such as `en`, `pt-BR` or `es-419` (max 35 chars), so YouTube does not treat it as another language. `null` clears a saved value. Does not turn off YouTube's automatic dubbing |
| `categoryId` | string | no | YouTube category ID |
| `playlistId` | string | no | Add to playlist after publishing |
| `scheduleOnYouTube` | boolean | no | Upload the video as soon as the post is scheduled, as a private video with YouTube's own publish time set to `scheduledAt`. YouTube publishes it at that time, so the user can set up Test & Compare in YouTube Studio first. Needs `privacyStatus` `public` or unset (else `400` `YOUTUBE_SCHEDULE_REQUIRES_PUBLIC`) and no `recurrence` (else `400` `YOUTUBE_SCHEDULE_NOT_RECURRING`). With `scheduledAt` less than 15 minutes ahead the video uploads at `scheduledAt` as usual. Once `youtubeScheduledVideoId` is set, the post cannot be updated, unscheduled or published early (`409`); delete it and schedule it again. Deleting before `scheduledAt` also deletes the video from YouTube, and a refusal from YouTube returns `502` with the post kept |

**Media notes:**

- Shorts: up to 3 minutes, 9:16 or 1:1
- Copyrighted music limits Shorts to 60 seconds
- H.264 video codec with AAC audio recommended

## Pinterest — `pinterestConfigs`

```json
{
  "pinterestConfigs": [
    {
      "connectionId": "pinterest-connection-id",
      "boardId": "board-id-here",
      "title": "Pin Title",
      "link": "https://example.com/page"
    }
  ]
}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `connectionId` | string | **yes** | Pinterest account connection ID |
| `boardId` | string | no | Board `id` from `GET /social-accounts/:id/pinterest-boards`. Not together with `boardName`. Without either, the pin goes to a public board named "AdaptlyPost", created on the Pinterest account the first time it is needed |
| `boardName` | string | no | The board's name on this Pinterest account (1 to 180 characters), used instead of `boardId`. Names are trimmed; a single exact match wins, then a single case-insensitive match. `400` when no board has the name, when several share it (the message lists their ids), or when `boardId` is also set. Never falls back to another board. Not stored: the post keeps the resolved board id |
| `title` | string | no | Pin title (max 100 chars) |
| `link` | string | no | Destination URL when pin is clicked (must be valid URL) |

**Media notes:**

- Ideal aspect ratio: 2:3 (1000x1500)
- Carousels: 2-5 static images only (no video in carousels)

## LinkedIn — `linkedinConfigs`

Only used for `DOCUMENT` posts: one PDF, PPT, PPTX, DOC or DOCX file (max 100 MB, 300 pages) that LinkedIn shows as a swipeable document. Target only `LINKEDIN` and put the single file URL in `mediaUrls`.

```json
{
  "contentType": "DOCUMENT",
  "mediaUrls": ["https://cdn.adaptlypost.com/social-media-posts/uuid/q3-results.pdf"],
  "linkedinConnectionIds": ["linkedin-connection-id"],
  "linkedinConfigs": [
    {
      "connectionId": "linkedin-connection-id",
      "documentTitle": "Q3 results"
    }
  ]
}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `connectionId` | string | **yes** | LinkedIn account connection ID |
| `documentTitle` | string | no | Title shown on the document (max 100 chars). Defaults to the file name; ignored for other content types |
| `reshareOf` | string | no | Reshare this LinkedIn post from the account, with the post text as the commentary (max 500 chars). Takes a `urn:li:share:` or `urn:li:ugcPost:` URN, such as the `platformPostId` from `/social-posts/:id/results`, or a link of the form `https://www.linkedin.com/feed/update/<urn>`, which is also the link inside a post's Embed code. `urn:li:activity:` links are refused because LinkedIn cannot reshare them through its API. Media on the post is not attached on this account |

```json
{
  "contentType": "TEXT",
  "text": "Our team wrote up how we plan a quarter of content.",
  "linkedinConnectionIds": ["linkedin-connection-id"],
  "linkedinConfigs": [{ "connectionId": "linkedin-connection-id", "reshareOf": "urn:li:share:7212345678901234567" }]
}
```

Other LinkedIn text, image and video posts need no config object.

## X (Twitter) — `twitterConfigs`

```json
{
  "contentType": "TEXT",
  "text": "Still the most useful thing we shipped this year.",
  "twitterConnectionIds": ["twitter-connection-id"],
  "twitterConfigs": [{ "connectionId": "twitter-connection-id", "quoteOf": "https://x.com/adaptlypost/status/1851234567890123456" }]
}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `connectionId` | string | **yes** | X account connection ID, also in `twitterConnectionIds` |
| `quoteOf` | string | no | Quote one of this account's own X posts, with the post text as the commentary (max 200 chars). Takes a post link such as `https://x.com/<handle>/status/<id>` or the numeric post id, such as the `platformPostId` from `/social-posts/:id/results`. X only lets an account quote posts it wrote or posts that mention it, so a link naming another handle is refused before posting, and any other post fails at publish time. The text is required, media on the post is not attached on this account, and a quote costs the same as any X post |

## Google Business Profile — `googleBusinessConfigs`

One entry per location in `googleBusinessConnectionIds`. A location without an entry gets a `STANDARD` update.

```json
{
  "googleBusinessConnectionIds": ["gbp-location-id"],
  "googleBusinessConfigs": [
    {
      "connectionId": "gbp-location-id",
      "topicType": "OFFER",
      "eventTitle": "Autumn sale",
      "eventStart": "2026-10-20",
      "eventEnd": "2026-10-31",
      "offerCouponCode": "AUTUMN20",
      "offerRedeemUrl": "https://example.com/sale",
      "offerTerms": "One per customer",
      "callToActionType": "SHOP",
      "callToActionUrl": "https://example.com/sale"
    }
  ]
}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `connectionId` | string | **yes** | Google Business Profile location `id` from `/social-accounts` |
| `topicType` | string | **yes** | `STANDARD` (an update), `EVENT` or `OFFER`. `EVENT` and `OFFER` need `eventTitle`, `eventStart` and `eventEnd` |
| `callToActionType` | string | no | Button on the post: `BOOK`, `ORDER`, `SHOP`, `LEARN_MORE`, `SIGN_UP` or `CALL`. Every type except `CALL` needs `callToActionUrl`; `CALL` dials the phone number on the Business Profile |
| `callToActionUrl` | string | no | URL the button opens. Ignored for `CALL` |
| `eventTitle` | string | no | Event or offer title |
| `eventStart` | string | no | `YYYY-MM-DD` or `YYYY-MM-DDTHH:mm` in the business's local time, no offset |
| `eventEnd` | string | no | `YYYY-MM-DD` or `YYYY-MM-DDTHH:mm` in the business's local time, no offset |
| `offerCouponCode` | string | no | `OFFER` only |
| `offerRedeemUrl` | string | no | `OFFER` only: URL where the offer is redeemed |
| `offerTerms` | string | no | `OFFER` only: terms and conditions |

**Media notes:**

- `contentType` `TEXT` or `IMAGE` only, with one JPEG or PNG image up to 5 MB
- Text up to 1,500 characters
- No alt text
- Analytics report location-level impressions only; posts have no per-post numbers

## Tumblr — `tumblrConfigs`

```json
{
  "tumblrConfigs": [
    {
      "connectionId": "tumblr-connection-id",
      "tags": ["lookbook", "autumn"],
      "title": "Autumn lookbook",
      "sourceUrl": "https://example.com/autumn"
    }
  ]
}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `connectionId` | string | **yes** | Tumblr blog `id` from `/social-accounts`, also in `tumblrConnectionIds` |
| `tags` | string[] | no | Up to 30 tags, without commas (max 140 chars each). A leading `#` is stripped and duplicates are dropped, ignoring case |
| `title` | string | no | Shown as a heading above the media and the text (max 4,096 chars) |
| `sourceUrl` | string | no | Shown as the source link of the post (max 2,048 chars) |

**Media notes:**

- `contentType` `TEXT`, `IMAGE`, `VIDEO` or `CAROUSEL`
- Text up to 32,768 characters
- Up to 30 JPEG, PNG or GIF images (10 MB each), or one MP4 video up to 500 MB and 10 minutes
- Alt text supported
- No first comments, threads, thumbnails, image shapes or analytics

## WordPress — `wordpressConfigs`

```json
{
  "wordpressConfigs": [
    {
      "connectionId": "wordpress-connection-id",
      "title": "The autumn collection",
      "excerpt": "Every piece of the new season in one place.",
      "categoryIds": [12],
      "tags": ["autumn", "new"],
      "status": "DRAFT"
    }
  ]
}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `connectionId` | string | **yes** | WordPress site `id` from `/social-accounts`, also in `wordpressConnectionIds` |
| `title` | string | no | Post title (max 300 chars). Defaults to the first line of the text, cut to 100 characters |
| `excerpt` | string | no | Summary WordPress shows in post lists and feeds (max 1,000 chars) |
| `categoryIds` | integer[] | no | Up to 50 category ids from `GET /social-accounts/:id/wordpress-categories`. Omitted, WordPress files the post under the site's default category |
| `tags` | string[] | no | Up to 50 tag names (max 100 chars each). A tag the site does not have yet is created when the WordPress user may manage tags, and skipped otherwise |
| `status` | string | no | `PUBLISH` (default) publishes the post live at its time. `DRAFT` leaves a WordPress draft the user finishes and publishes or schedules in WordPress. `PENDING` submits it for review ("Pending Review"). For `DRAFT` and `PENDING` the post's `postUrl` opens it in the WordPress editor |

**Media notes:**

- The text becomes the body of a blog post, up to 100,000 characters: blank lines start new paragraphs and bare links become clickable
- `contentType` `TEXT`, `IMAGE`, `VIDEO` or `CAROUSEL`
- Up to 20 JPEG, PNG, WebP or GIF images (20 MB each), or one MP4 or MOV video up to 500 MB
- The first image is the featured image; the other images or the video follow the text
- Alt text is sent to WordPress
- AdaptlyPost marks the platform published once WordPress holds the post in the asked `status`; a WordPress `DRAFT` is not an AdaptlyPost draft, so the post still has to be scheduled or published
- A site that answers 401 or 403 is marked for reconnect
- No first comments, threads, thumbnails, image shapes or analytics
- The site (WordPress 5.6 or later, over HTTPS) is connected in the AdaptlyPost app on the Connectors page

## Platforms Without Config Objects

These platforms use only connection ID arrays, plus `twitterConfigs` for an X quote:

### X (Twitter)

- Uses `twitterConnectionIds` array; `twitterConfigs` only for `quoteOf`
- Character limit: 280
- Up to 20 images per post, or one video. Images and a video can't share a post
- Links in X text are broken by default (`example.com` becomes `example. com`) because X charges over 10 times more for a post with a link. Top-level `twitterKeepLinks: true` keeps them clickable, on AppSumo lifetime deals only, at 20 credits instead of 2
- Top-level `threadReplies` with `platform: TWITTER` turns the post into a thread of up to 25 replies, 280 characters each (more on X Premium), with up to 4 images per reply. Thread replies are not retried on X, and a lifetime-deal account pays for each reply like any X post

### Bluesky

- Uses `blueskyConnectionIds` array
- Character limit: 300
- Up to 4 images
- No video support
- URLs auto-generate link cards
- No editing after publishing
- Top-level `threadReplies` with `platform: BLUESKY` turns the post into a thread of up to 25 replies, 300 characters each, with up to 4 images per reply

### Mastodon

- Uses `mastodonConnectionIds` array
- Character limit: 500 by default, some servers allow more
- Up to 4 images, some servers allow more
- 1 video per post
- Alt text supported
- No analytics
- Top-level `threadReplies` with `platform: MASTODON` turns the post into a thread of up to 25 replies, 500 characters each (or the instance's limit), with up to 4 images per reply

### Threads

- Uses `threadsConnectionIds` array
- Text + images + video supported
- Carousels: up to 10 images and videos
- Top-level `threadReplies` with `platform: THREADS` turns the post into a thread of up to 25 replies, 500 characters each, with up to 4 images per reply
- Top-level `firstComments` with `platform: THREADS` posts a reply of up to 500 characters from the same account; a platform takes a first comment or a thread, not both

### LinkedIn

- Uses `linkedinConnectionIds` array
- Character limit: 3,000 (under 1,300 performs better)
- Carousel of up to 20 images, or video up to 10 min, or one document (see `linkedinConfigs` above)
- Put links in a first comment (`firstComments`), not the post body, because LinkedIn deprioritizes external links. `delayMinutes` on the entry posts it later, up to 10080 minutes (7 days) after the post
- Mention a company page with `@[Page Name](urn:li:organization:<id>)`, the page name exactly as LinkedIn shows it. `GET /linkedin-organizations/lookup` with the page URL or vanity name returns the ready-made mention
- 3-5 hashtags max

### Telegram

- Uses `telegramConnectionIds` array (channels and groups)
- No config object
- Character limit: 4,096
- Up to 10 images (JPEG, PNG or WebP, 10 MB each), or one MP4 or MOV video up to 50 MB
- A caption over 1,024 characters goes out as its own message right after the media
- A video takes an image or a video frame as its thumbnail (`platformThumbnails` with `thumbnailUrl` or `thumbnailTimestampMs`)
- No alt text, first comments, threads, image shapes or analytics
- Connecting a chat happens in the AdaptlyPost app: add the AdaptlyPost bot to the channel or group and send it the connect code from the Connectors page
