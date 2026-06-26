# Douyin Publish Task Contract

Use this contract when another agent provides the video and edit-page metadata to this skill.

## Required JSON

```json
{
  "type": "video",
  "media": {
    "videoPath": "/absolute/path/to/video.mp4",
    "videoPaths": [],
    "cover": {
      "mode": "auto_recommended",
      "imagePath": null
    }
  },
  "metadata": {
    "title": "30 chars max preferred",
    "description": "caption text, hashtags, mentions",
    "topics": ["话题1", "话题2"],
    "mentions": [],
    "collection": null,
    "declaration": null,
    "chapters": [],
    "tags": [],
    "location": null,
    "hotspot": null
  },
  "settings": {
    "visibility": "public",
    "allowSave": true,
    "publishTime": {
      "mode": "now",
      "scheduledAt": null
    }
  }
}
```

## Fieldized Input

Upstream agents may provide this shorter field shape:

```json
{
  "tags": "#宠物险#保险",
  "封面图片": "https://example.com/cover.png",
  "标题": "养宠不焦虑的秘诀？",
  "视频地址": "https://example.com/video.mp4"
}
```

Convert and download it before publishing:

```bash
node scripts/prepare-upstream-publish-task.js --input templates/upstream-mentor-example.json --output templates/publish-task.from-upstream.json
node scripts/validate-publish-task.js --task templates/publish-task.from-upstream.json
node scripts/publish-task.js --task templates/publish-task.from-upstream.json
```

`templates/publish-task.from-upstream.json` 是由 `prepare-upstream-publish-task.js` 生成的临时文件，首次 clone/ClawHub 安装后不会预先存在。

The converter maps:

- `视频地址` -> `media.videoUrl`, downloaded to `media.videoPath`.
- `封面图片` -> `media.cover.imageUrl`, downloaded to `media.cover.imagePath`.
- `标题` -> `metadata.title`.
- `tags:#宠物险#保险` -> `metadata.topics` / `metadata.tags`. One, two, or more tags are supported.

Custom cover files are used by stable publishing when `media.cover.imagePath` exists. The publisher uploads the image, saves the Douyin cover modal, verifies cover slots received a background image, and blocks publishing if that confirmation fails. If no custom cover is provided, the publisher falls back to AI recommended cover.

## Field Meaning

- `media.videoPath`: absolute local video path. Required.
- `media.videoPaths`: optional list of absolute video paths. Stability tests rotate through this list so consecutive rounds do not reuse the same binary.
- `media.cover.mode`: use `auto_recommended`. If `imagePath` exists, stable publishing still uses that local custom cover first; `auto_recommended` is the fallback when no custom cover is provided.
- `metadata.title`: maps to the visible title input. Douyin currently shows a 30-character counter. The task is invalid above 30 characters unless it went through `prepare-upstream-publish-task.js`, which truncates to the same safe title used for publishing and verification.
- `metadata.description`: maps to the rich-text work description editor. Do not rely on plain-text hashtags when `metadata.topics/tags` is available.
- `metadata.topics`: optional topic words. The publisher clicks `#添加话题`, inputs each topic, presses Enter, and verifies real topic nodes before publishing.
- `metadata.mentions`: optional accounts. Dedicated @ picker automation is not stable yet.
- `metadata.collection`: optional collection name/id. Discovered on page; not yet automated.
- `metadata.declaration`: optional self-declaration selection. Discovered on page; not yet automated.
- `metadata.chapters`: optional video chapter data. Discovered on page; not yet automated.
- `metadata.tags`: aliases for topics in the current stable flow; all values are merged and deduplicated with `metadata.topics`.
- `metadata.location`: optional geolocation text. Discovered on page; not yet automated.
- `metadata.hotspot`: optional hot topic text. Discovered on page; not yet automated.
- `settings.visibility`: `public`, `friends`, or `private`.
- `settings.allowSave`: `true` means allow saving/downloading; `false` means disallow.
- `settings.publishTime.mode`: `now` or `scheduled`.
- `settings.publishTime.scheduledAt`: required only when `mode=scheduled`; use ISO 8601.

## Current Automation Tiers

Stable now:

- Upload video file.
- Fill title.
- Fill description.
- Upload and save custom cover from `media.cover.imagePath`; fall back to AI recommended cover when no custom cover exists.
- Wait for assistant/upload checks. Large videos may need 30-60 minutes end to end, so use the async job path instead of a short synchronous OpenClaw call.
- Click publish and handle publish SMS verification.

Discovered and ready for next implementation:

- Visibility: public/friends/private.
- Save permission: allow/disallow.
- Publish time: now/scheduled.
- Collection selector.
- Self-declaration selector.
- Location selector.
- Hotspot selector.
- Cover controls.
- Topic and @ controls.
- Chapter/tag sections.

Unsupported until explicitly implemented:

- Selecting arbitrary collections/declarations from dynamic dropdowns.
- Searching/selecting @ accounts and hotspots with ambiguity resolution.
- Scheduled publish date/time picker.

## Stability Test Template

The runnable template lives at:

`templates/publish-task.stability.json`

Validate it:

```bash
node scripts/validate-publish-task.js --task templates/publish-task.stability.json
```

Dry-run the three-round plan:

```bash
node scripts/run-publish-task-stability.js --task templates/publish-task.stability.json --rounds 3
```

Execute real publishing only when explicitly requested:

```bash
node scripts/publish-task.js --task templates/publish-task.from-upstream.json --execute
node scripts/run-publish-task-stability.js --task templates/publish-task.stability.json --rounds 3 --execute
```

Pass rule: all three rounds must publish and then be found in the Douyin works list by their unique generated titles.
