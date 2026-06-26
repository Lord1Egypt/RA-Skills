# MiniMax API Info

## Purpose
This file summarizes the currently verified official API surface used by this skill.

## Model IDs

| Modality | Verified current models | Notes |
| :--- | :--- | :--- |
| **Text** | `MiniMax-M2.7-highspeed`, `MiniMax-M2.7`, `MiniMax-M2.5-highspeed`, `M2-her` | Text models use Token Plan rolling-window logic |
| **Image** | `image-01`, `image-01-live` | `image-01-live` supports style object |
| **Video** | `MiniMax-Hailuo-2.3`, `MiniMax-Hailuo-02`, `T2V-01-Director`, `T2V-01` | Current skill mainly targets `MiniMax-Hailuo-02` |
| **Speech** | `speech-2.8-hd`, `speech-2.8-turbo`, `speech-2.6-hd`, `speech-2.6-turbo`, `speech-02-hd`, `speech-02-turbo`, `speech-01-hd`, `speech-01-turbo` | Sync and async speech are both available |
| **Music** | `music-2.5+`, `music-2.5` | `music-2.5+` still appears in official music-generation API docs |
| **Voice Clone** | `voice_clone` flow + speech model for preview | Requires file upload + clone request |
| **Voice Design** | `voice_design` | Requires `prompt` + `preview_text` |

## Verified endpoint mapping

| Capability | Official endpoint |
|---|---|
| Text-to-image | `POST /v1/image_generation` |
| Image-to-image | `POST /v1/image_generation` |
| Text-to-video | `POST /v1/video_generation` |
| Video template / Video Agent | `POST /v1/video_template_generation` |
| Sync speech | `POST /v1/t2a_v2` |
| Async speech create | `POST /v1/t2a_async_v2` |
| Async speech query | `GET /v1/query/t2a_async_query_v2` |
| Music generation | `POST /v1/music_generation` |
| Voice clone | `POST /v1/voice_clone` |
| Voice design | `POST /v1/voice_design` |
| Token Plan remains | `GET https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains` |

## Important notes

### 1. Text vs non-text quota rules
According to the latest verified Token Plan FAQ:
- **Text models**: 5-hour rolling window
- **Non-text models**: daily quota reset

### 2. remains API semantics
The remains API is now integrated into this skill, but its field semantics are treated conservatively until manually cross-checked against the official Token Plan web console.

### 3. Voice clone lifecycle
Official docs state cloned voices are deleted if they are not formally used within 7 days.

### 4. Voice clone permission risk
Official error code `2038` indicates clone permission may depend on account status / certification.

## Reference pointers
- `references/quota_mapping.json`
- `references/official-doc-sources.md`
- `references/checks/latest-check.md`
