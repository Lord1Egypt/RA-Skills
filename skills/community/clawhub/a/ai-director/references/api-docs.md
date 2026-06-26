# AIDirector API Reference

Base URL: `https://giggle.pro`

## Authentication

Add header: `x-auth: <api_key>`

## Endpoints

### Project

#### Create Project

```
POST /api/v1/project/create
{
  "name": "项目名称",
  "type": "director",
  "aspect": "16:9"
}
```

#### Get My Assets

```
GET /api/v1/project/my_assets
```

### Script

#### Generate Script

```
POST /api/v1/script/storyExpansion
{
  "project_id": "proj_xxx",
  "diy_story": "故事创意",
  "video_duration": "60",
  "language": "zh-CN",
  "aspect": "16:9"
}
```

Returns `task_id`, poll for completion.

#### Check Script Status

```
GET /api/v1/script/getExpandedStory?task_id=<task_id>
```

#### Get Script Detail

```
GET /api/v1/script/detail?project_id=<project_id>
```

#### Update Script

```
POST /api/v1/script/update
{
  "project_id": "proj_xxx",
  "diy_script": "原创意",
  "ai_script": "完整剧本"
}
```

### Character

#### Auto Generate Characters

```
POST /api/v1/character/generate
{
  "project_id": "proj_xxx"
}
```

#### List Characters

```
GET /api/v1/character/list?project_id=<project_id>
```

#### Update Character

```
POST /api/v1/character/update
{
  "id": 1,
  "name": "角色名",
  "gender": "male|female",
  "prompt": "角色描述",
  "used": true,
  "voice_id": "voice_xxx",
  "use_asset_id": "asset_xxx"
}
```

#### Manual Character Generation

```
POST /api/v1/character/generate_by_detail
{
  "project_id": "proj_xxx",
  "name": "角色名",
  "gender": "female",
  "prompt": "详细描述",
  "image_model": "flux-pro",
  "generating_count": 4,
  "parent_id": "0"
}
```

### Storyboard

#### Auto Generate Storyboard

```
POST /api/v1/storyboard-shots/auto-generate
{
  "project_id": "proj_xxx"
}
```

#### List Storyboard

```
GET /api/v1/storyboard-shots/list?project_id=<project_id>
```

Response includes `shot_list` with:

- `id`, `shot_id`
- `prompt` - shot description
- `generating_status` - image status
- `video_generating_status` - video status
- `characters` - character list with dialogues

#### Get Shot Detail

```
GET /api/v1/storyboard-shots/detail?project_id=<project_id>&parent_id=<shot_id>
```

#### Update Shot

```
POST /api/v1/storyboard-shots/update
{
  "project_id": "proj_xxx",
  "id": 1,
  "used": true,
  "use_asset_id": "asset_xxx"
}
```

### Image Generation

#### Auto Generate All Images

```
POST /api/v1/storyboard-shots/auto-generate-image
{
  "project_id": "proj_xxx"
}
```

#### Generate Single Image

```
POST /api/v1/storyboard-shots/generate-image
{
  "project_id": "proj_xxx",
  "parent_id": 1,
  "generate_type": "auto",
  "prompt": "图片描述",
  "model": "flux-pro",
  "generating_count": 4
}
```

### Video Generation

#### Auto Generate All Videos

```
POST /api/v1/storyboard-shots/auto-generate-video
{
  "project_id": "proj_xxx",
  "model": "wan25",
  "duration": 5,
  "generate_audio": true,
  "second_model": "kling25"
}
```

**Models:** `wan25` (default), `kling25`, `kling26`, `minimax`, `minimax23`, `sora2`, `sora2-pro`, `sora2-fast`, `veo31`, `seedance15-pro`, `grok`, `grok-fast`

**Note:** `model` is the primary video generator, `second_model` is used as fallback if primary fails.

#### Generate Single Video

```
POST /api/v1/storyboard-shots/generate-video
{
  "project_id": "proj_xxx",
  "shot_id": 1,
  "model": "wan25",
  "prompt": "视频动作描述",
  "duration": 5,
  "generating_count": 2,
  "generate_audio": true,
  "second_model": "kling25"
}
```

#### Get Video Detail

```
GET /api/v1/storyboard-shots/video-detail?project_id=<project_id>&parent_id=<shot_id>
```

#### Select Video

```
POST /api/v1/storyboard-shots/use-video
{
  "project_id": "proj_xxx",
  "parent_id": 1,
  "video_id": 1,
  "asset_id": "asset_xxx"
}
```

#### Generate Voice

```
POST /api/v1/storyboard-shots/generate-voice
{
  "project_id": "proj_xxx",
  "shot_id": 1
}
```

### Export

#### Export Full Video

```
POST /api/v1/video-edit/export-entire-film
{
  "project_id": "proj_xxx",
  "bgm_asset_id": "asset_bgm_xxx",
  "bgm_volume": 0.3,
  "subtitle_enabled": true
}
```

#### Export All Clips

```
POST /api/v1/video-edit/export-all-clips
{
  "project_id": "proj_xxx"
}
```

## Status Values

### Generation Status

- `pending` - queued
- `generating` / `processing` - in progress
- `completed` - done
- `failed` - error (check `err_msg`)

### Project Status

- `creating` - being created
- `exporting` - export in progress
- `completed` - ready

## Timing Estimates

| Task             | Duration |
| ---------------- | -------- |
| Script           | 10-30s   |
| Character (each) | 30-60s   |
| Image (each)     | 10-30s   |
| Video (each)     | 2-5 min  |
| Export           | 5-15 min |
