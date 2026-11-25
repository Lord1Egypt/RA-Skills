# Facebook Groups API endpoint reference (SocialAPIs)

Base URL: `https://api.socialapis.io` · Auth: header `x-api-token: $SOCIALAPIS_API_KEY` · All endpoints are `GET` with query parameters.

Generated from the full reference in the `socialapis` skill. Machine-readable: https://socialapis.io/openapi.json

### `GET /facebook/groups/id`

Docs and live example: https://socialapis.io/api-sources/facebook-group-id

Resolve a Facebook group URL to its numeric group ID. Use `/facebook/groups/details` for the group's data. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook group URL |

### `GET /facebook/groups/details`

Docs and live example: https://socialapis.io/api-sources/facebook-group-details

Get a public Facebook group's profile: name, description, member count, privacy, rules and activity stats. Use `/facebook/groups/posts` for its posts. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook group URL |

### `GET /facebook/groups/posts`

Docs and live example: https://socialapis.io/api-sources/facebook-group-posts

List recent posts from a public Facebook group, with text, media, author, reactions and comment counts. Returns 3-9 posts per call plus an end_cursor for the next page; filter by date with after_time / before_time. Pricing: ceil(posts_returned / 3) credits per call, minimum 1.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook group URL |
| `limit` | no | Maximum number of posts to return. Default: 3. Minimum: 3. Maximum: 9. |
| `end_cursor` | no | Pagination cursor |
| `after_time` | no | ISO 8601 timestamp |
| `before_time` | no | ISO 8601 timestamp |
| `timezone` | no | IANA timezone for returned timestamps, e.g. UTC or America/New_York. Default: UTC. |

### `GET /facebook/groups/videos`

Docs and live example: https://socialapis.io/api-sources/facebook-group-videos

List videos posted in a public Facebook group, with video_id, title, duration, view count and thumbnail. Returns an end_cursor for the next page. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook group URL |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/groups/albums`

Docs and live example: https://socialapis.io/api-sources/facebook-group-albums

List the photo albums of a public Facebook group, with album_id, album_title, url, thumbnail_uri, photos_count and videos_count. Returns an end_cursor for the next page. Needs the numeric group ID (group_id) from `/facebook/groups/id`. To get the photos in an album, pass its album_id to `/facebook/albums/items`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `group_id` | yes | Facebook group ID, from `/facebook/groups/id` |
| `limit` | no | Maximum number of albums to return. Default: 8. Minimum: 8. Maximum: 16. |

### `GET /facebook/albums/items`

Docs and live example: https://socialapis.io/api-sources/facebook-album-items

Get the photos and videos inside a Facebook album (from a page or a group): media_id, media_type, url, thumbnail_uri and timestamp (Unix seconds). Needs an album_id from `/facebook/pages/albums` or `/facebook/groups/albums`. Returns an end_cursor for the next page. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `album_id` | yes | Album ID, from `/facebook/pages/albums` or `/facebook/groups/albums` |
| `end_cursor` | no | Pagination cursor |
