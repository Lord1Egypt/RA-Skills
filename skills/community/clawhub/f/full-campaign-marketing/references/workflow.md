# Full-campaign pack

The plan is free: offer, audience, topics, and the line the clip will say.

## Lookup

One execute. Copy `schema_hash` from `tools.get`.

- `social.douyin.hot_search.list`
- `social.douyin.video.search`
- `social.douyin.video.comments.list`
- `social.xiaohongshu.note.search`
- `social.xiaohongshu.note.comments.list`
- `social.tiktok.video.search`

Quote a line you use. Do not invent ad-account numbers, store sales, or WeChat metrics.

## Poster, line, jingle, clip

Transform the poster from the product photo. Generate only when there is no photo, and say the product is drawn from the description. One edit restores the product if the poster lost it.

One ready voice, one spoken line under ten seconds, one instrumental jingle.

```json
{
  "image": {"type": "artifact", "artifact_id": "art_poster"},
  "driving_audio": {"type": "artifact", "artifact_id": "art_line"},
  "model": "<admits image plus driving_audio>",
  "prompt": "<the product stays; one small motion>",
  "duration": 8,
  "client_request_id": "opaque-clip"
}
```

Compose with `keep_audio` true, jingle `volume` 0.25, canvas `9:16`. Do not pass the line again as `narration`.

## Worked pack

A canned barley tea for office desks. Plan from the audience, no lookup. Poster transformed from the can photo, an eight-second line, a light jingle under the voice, one 9:16 clip.
