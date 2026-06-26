---
name: chanjing-avatar
description: Use Chanjing Avatar API for lip-syncing and video synthesis (including cartoon avatar)
---

# Chanjing Avatar (Lip-Syncing & Video Synthesis)

## L2 Product Skill

本文件是 **L2 产品层**主手册（**Agent 执行真值**）。

- **本文件（`chanjing-avatar-SKILL.md`）**：业务逻辑、追问与异常语义；据此调度 [`scripts/cli_capabilities.py`](scripts/cli_capabilities.py) 与 [`scripts/`](scripts/) 下脚本。
- **顶层入口** [`../../SKILL.md`](../../SKILL.md)：仅负责路由到本目录，**不**承载本产品执行细则。
- **跨场景约定** [`../../orchestration/orchestration-contract.md`](../../orchestration/orchestration-contract.md)；L3 编排层说明见 [`../../orchestration/README.md`](../../orchestration/README.md)。

## When to Use This Skill

Use this skill when the user needs to:

1. **对口型（Lip-Sync）**：用户上传视频文件，驱动口型同步（仅支持非卡通素材）
2. **视频合成（Video Synthesis）**：基于平台数字人形象 ID 合成完整视频，支持背景、字幕、合规水印等（支持真人 & **卡通数字人**）

Chanjing Avatar supports:

* Text-driven or audio-driven lip-syncing
* Cartoon mode (`model=2`) is only for video synthesis with cartoon digital humans
* Multiple system voices for TTS
* Video resolution customization (1080p / 4K)
* Background image / color, subtitle configuration
* RGBA (transparent) mode for webm avatars
* AI compliance watermark
* Task status polling and callback

## How to Use This Skill

**前置条件**：凭证由顶层入口统一校验；本 Skill 不重复执行凭证校验步骤。

统一按“每步 = 脚本名 + 输入 + 输出 + 下一步”执行，不做额外追问，由 Agent 自主补齐可选默认值。

### 流程 A：对口型（Lip-Sync，非卡通素材）

| Step | 脚本名 | 输入 | 输出 | 下一步 | 失败分支 |
|------|--------|------|------|--------|----------|
| A1 | `upload_file.py` | `--service lip_sync_video` + `--file <video>` | `video_file_id` | A2 | 上传失败：检查路径/格式并重试 A1 |
| A2 | `upload_file.py`（按需） | `--service lip_sync_audio` + `--file <audio>`（仅音频驱动时） | `audio_file_id` | A3 | 上传失败：改用 TTS 驱动或重试 A2 |
| A3 | `create_task.py` | 必填：`video_file_id`；二选一：`--text + --audio-man-id` 或 `--audio-file-id`；`--model` 默认 0 | `task_id` | A4 | `10400` 回顶层鉴权；`40000` 修参重试 A3；`50000` 延迟重试 A3 |
| A4 | `poll_task.py` | `--id <task_id>` | `video_url`（远端） | A5 | 失败：返回错误详情，可回 A3 重建任务 |
| A5 | 下载动作（仅显式下载） | 用户明确要求“下载/保存到本地”时执行 | 本地文件路径 | 结束 | 下载失败：返回远端 `video_url` 与错误信息 |

### 流程 B：视频合成（Video Synthesis，支持卡通数字人）

| Step | 脚本名 | 输入 | 输出 | 下一步 | 失败分支 |
|------|--------|------|------|--------|----------|
| B1 | `create_video.py` | 必填：`person_id`、位置尺寸参数；音频二选一：TTS 或音频；`--model` 默认 0（卡通数字人用 2） | `video_id` | B2 | `10400` 回顶层鉴权；`40000` 修参重试 B1；`50000` 延迟重试 B1 |
| B2 | `poll_video.py` | `--id <video_id>` | `video_url`（远端） | B3 | 失败：返回错误详情，可回 B1 重建任务 |
| B3 | 下载动作（仅显式下载） | 用户明确要求“下载/保存到本地”时执行 | 本地文件路径 | 结束 | 下载失败：返回远端 `video_url` 与错误信息 |

API 细节与字段全量说明放在本文件后续章节，仅作参数参考；执行顺序以本节脚本流程为准。

### Workflow Output Semantics

本 Skill 输出语义对齐 [`../../orchestration/orchestration-contract.md`](../../orchestration/orchestration-contract.md)：

- `ok`：成功返回 `video_url` 或本地落盘路径
- `need_param`：必要参数缺失或校验失败（典型 `40000`）
- `auth_required`：凭据不可用（典型 `10400`）
- `upstream_error`：上游服务失败（典型 `50000`）
- `timeout`：轮询超时或长时间无结果

### `model` 参数

| 取值 | 说明 | 费用 |
|------|------|------|
| **0**（默认） | 基础版：**蝉镜 lip-sync 模型** | 1 蝉豆/秒 |
| **1** | 高质版：**蝉镜 lip-sync Pro 模型** | 2 蝉豆/秒 |
| **2** | **仅视频合成可用的卡通形象模式**：素材必须为卡通形象，否则效果与合规风险由使用方承担 | 3 蝉豆/秒 |

对口型 CLI 使用 `--model 0/1`；视频合成（卡通数字人）使用 `create_video.py ... --model 2`。

### Obtain AccessToken

从项目 `.env` 读取 `CHANJING_APP_ID` 与 `CHANJING_SECRET_KEY`，并调用：

```http
POST /open/v1/access_token
Content-Type: application/json
```

请求体（使用本地配置的 app_id、secret_key）：

```json
{
  "app_id": "<从 .env 的 CHANJING_APP_ID 读取>",
  "secret_key": "<从 .env 的 CHANJING_SECRET_KEY 读取>"
}
```

Response example:

```json
{
  "trace_id": "8ff3fcd57b33566048ef28568c6cee96",
  "code": 0,
  "msg": "success",
  "data": {
    "access_token": "1208CuZcV1Vlzj8MxqbO0kd1Wcl4yxwoHl6pYIzvAGoP3DpwmCCa73zmgR5NCrNu",
    "expire_in": 1721289220
  }
}
```

Response field description:

| First-level Field | Second-level Field | Description |
|---|---|---|
| code | | Response status code |
| msg | | Response message |
| data | | Response data |
| | access_token | Valid for one day, previous token will be invalidated |
| | expire_in | Token expiration time |

Response Status Code Description

| Code | Description |
|---|---|
| 0 | Success |
| 400 | Invalid parameter format |
| 40000 | Parameter error |
| 50000 | System internal error |

### Upload Media Files (File Management)

Before creating a lip-syncing task, you **must** upload your video (and optional audio) files using the File Management API to obtain `file_id` values.

The full documentation is here: `[File Management](https://doc.chanjing.cc/api/file/file-management.html)`.

#### Step 1: Get upload URL

```http
GET /open/v1/common/create_upload_url
access_token: {{access_token}}
```

Query params:

| Key | Example | Description |
|---|---|---|
| service | lip_sync_video / lip_sync_audio | File usage purpose. Use `lip_sync_video` for driving video, `lip_sync_audio` for audio (if audio-driven). |
| name | 1.mp4 | Original file name including extension |

You will get a response containing `sign_url`, `mime_type`, and `file_id`. Use the `sign_url` with HTTP `PUT` to upload the file, setting `Content-Type` to the returned `mime_type`. After the PUT completes, **poll the file detail API** until the file is ready (do not assume a fixed wait). Keep the returned `file_id` for `video_file_id` / `audio_file_id` below.

**Polling:** Call `GET /open/v1/common/file_detail?id={{file_id}}` with `access_token` until the response `data.status` indicates success (e.g. `status === 2`). Only then use the `file_id` for the create task API.

### Create Lip-Syncing Task

Submit a lip-syncing video creation task, which returns a video ID for polling later.

```http
POST /open/v1/video_lip_sync/create
access_token: {{access_token}}
Content-Type: application/json
```

Request body example (TTS-driven):

```json
{
  "video_file_id": "e284db4d95de4220afe78132158156b5",
  "screen_width": 1080,
  "screen_height": 1920,
  "callback": "https://example.com/openapi/callback",
  "model": 0,
  "audio_type": "tts",
  "tts_config": {
    "text": "君不见黄河之水天上来，奔流到海不复回。",
    "audio_man_id": "C-f2429d07554749839849497589199916",
    "speed": 1,
    "pitch": 1
  }
}
```

Request body example (Audio-driven):

```json
{
  "video_file_id": "e284db4d95de4220afe78132158156b5",
  "screen_width": 1080,
  "screen_height": 1920,
  "model": 0,
  "audio_type": "audio",
  "audio_file_id": "audio_file_id_from_file_management"
}
```

Request field description:

| Parameter Name | Type | Required | Description |
|---|---|---|---|
| video_file_id | string | Yes | Video file ID from File Management (`data.file_id`). Supports mp4, mov, webm |
| screen_width | int | No | Screen width, default 1080 |
| screen_height | int | No | Screen height, default 1920 |
| backway | int | No | Playback order when reaching end: 1-normal, 2-reverse. Default 1 |
| drive_mode | string | No | Drive mode: ""-normal, "random"-random frame. Default "" |
| callback | string | No | Callback URL for async notification |
| model | int | No | **0** (default): Chanjing **lip-sync** (basic). **1**: **lip-sync Pro** (high quality). **2**: **Cartoon-only** — training / driving material **must** be cartoon style. |
| audio_type | string | No | Audio type: "tts"-text driven, "audio"-audio driven. Default "tts" |
| tts_config | object | Yes (for tts) | TTS configuration when audio_type="tts" |
| tts_config.text | string | Yes (for tts) | Text to synthesize |
| tts_config.audio_man_id | string | Yes (for tts) | Voice ID |
| tts_config.speed | number | No | Speech speed: 0.5-2, default 1 |
| tts_config.pitch | number | No | Pitch, default 1 |
| audio_file_id | string | Yes (for audio) | Audio file ID from File Management (`data.file_id`) when `audio_type="audio"`. Supports mp3, m4a, wav |
| volume | int | No | Volume: 1-100, default 100 |

Response example:

```json
{
  "trace_id": "8d10659438827bd4d59eaa2696f9d391",
  "code": 0,
  "msg": "success",
  "data": "9499ed79995c4bdb95f0d66ca84419fd"
}
```

Response field description:

| Field | Description |
|---|---|
| code | Response status code |
| msg | Response message |
| data | Video ID for subsequent polling |

### Query Task List

```http
POST /open/v1/video_lip_sync/list
access_token: {{access_token}}
Content-Type: application/json
```

Request body: `{ "page": 1, "page_size": 10 }`

响应 `data.list` 数组，每项含 `id`、`status`、`progress`、`video_url`、`preview_url`、`duration`、`create_time`；`data.page_info` 含分页。

### Query Task Detail

轮询直到 status=20（成功）或 30（失败）。

```http
GET /open/v1/video_lip_sync/detail?id={{video_id}}
access_token: {{access_token}}
```

| Field | Description |
|---|---|
| status | 0=待处理、10=生成中、**20=成功**、30=失败 |
| video_url | 成功后的视频下载地址 |
| preview_url | 封面图 |
| duration | 时长（ms） |

### Callback Notification

提供 `callback` URL 时，任务完成后系统 POST 请求体与 detail 响应 `data` 结构相同。

---

## 视频合成 — Create Video（流程 B）

基于平台已有数字人形象（`person.id`）合成完整视频，支持 TTS / 音频驱动、背景、字幕、合规水印等。**卡通数字人须使用 `model=2`**。

> **与对口型（流程 A）的区别**：对口型上传用户自有视频 → 驱动口型（仅非卡通）；视频合成选择平台数字人形象 → 生成完整视频含背景与字幕（卡通数字人可用 `model=2`）。

> **状态码差异**：视频合成 status **30=成功**、10=生成中、4X=参数异常、5X=服务异常；对口型 status **20=成功**、30=失败。

### Create Video Synthesis Task

```http
POST /open/v1/create_video
access_token: {{access_token}}
Content-Type: application/json
```

Request body example (TTS-driven, cartoon avatar):

```json
{
  "person": {
    "id": "C-d1af99e0fee34978bc844d43078bf8c9",
    "x": 0,
    "y": 480,
    "width": 1080,
    "height": 1440
  },
  "audio": {
    "tts": {
      "text": ["君不见黄河之水天上来，奔流到海不复回。"],
      "speed": 1,
      "audio_man": "C-f2429d07554749839849497589199916"
    },
    "type": "tts",
    "volume": 100,
    "language": "cn"
  },
  "bg_color": "#EDEDED",
  "screen_width": 1080,
  "screen_height": 1920,
  "model": 2
}
```

核心请求参数（完整参数表见 [`references/create-video-api.md`](references/create-video-api.md)）：

| Parameter | Type | Required | Description |
|---|---|---|---|
| person.id | string | Yes | 形象 ID（公共数字人或定制数字人列表获取） |
| person.x / y / width / height | int | Yes | 数字人位置与尺寸 |
| person.figure_type | string | No | 仅公共数字人需传（`whole_body` / `sit_body`） |
| person.drive_mode | string | No | `""` 正常（默认）、`random` 随机帧 |
| person.is_rgba_mode | bool | No | 四通道 webm 输出（需 webm 定制数字人） |
| audio.type | string | Yes | `tts` 或 `audio` |
| audio.tts.text | string[] | Yes (tts) | 文本数组（单字符串，< 4000 字符） |
| audio.tts.audio_man | string | Yes (tts) | 声音 ID |
| audio.wav_url / audio.file_id | string | Yes (audio) | 音频 URL 或上传的 file_id |
| bg_color | string | No | 背景颜色 `#RRGGBB` |
| subtitle_config.show | bool | No | 是否显示字幕 |
| model | int | No | 0 基础 / 1 高质 / **2 卡通专用** |
| add_compliance_watermark | bool | No | AI 合规水印 |
| resolution_rate | int | No | 0=1080p / 1=4K |

Response: `data` 为视频 ID，用于后续查询。

### Query Video Detail（视频合成）

```http
GET /open/v1/video?id={{video_id}}
access_token: {{access_token}}
```

状态码：**10**=生成中；**30**=成功；**4X**=参数异常；**5X**=服务异常。成功后 `data.video_url` 为下载地址。

### Query Video List（视频合成）

```http
POST /open/v1/video_list
access_token: {{access_token}}
Content-Type: application/json
```

Request body: `{ "page": 1, "page_size": 10 }`。响应 `data.List` 为视频数组，`data.PageInfo` 含分页信息。

---

## Scripts

本 Skill 提供脚本（`skills/chanjing-content-creation-skill/products/chanjing-avatar/scripts/`），使用项目 `.env` 获取凭据并换取 Token。

### 对口型脚本

| 脚本 | 说明 |
|------|------|
| `get_upload_url.py` | 获取上传链接，输出 `sign_url`、`mime_type`、`file_id` |
| `upload_file.py` | 上传本地文件，轮询 file_detail 直到就绪后输出 `file_id` |
| `create_task.py` | 创建对口型任务（TTS 或音频驱动），支持 `--model`：0 基础 / 1 Pro（非卡通）；输出视频任务 id |
| `poll_task.py` | 轮询对口型任务直到完成（status=20），输出 `video_url` |

示例（普通视频 lip-sync）：

```bash
VIDEO_FILE_ID=$(python scripts/upload_file.py --service lip_sync_video --file ./my_video.mp4)
TASK_ID=$(python scripts/create_task.py \
  --video-file-id "$VIDEO_FILE_ID" \
  --text "你好世界" \
  --audio-man-id "C-f2429d07554749839849497589199916" \
  --model 1)
python scripts/poll_task.py --id "$TASK_ID"
```

音频驱动时：先上传音频得到 `audio_file_id`，再 `create_task.py --video-file-id <id> --audio-file-id <audio_file_id>`。

### 视频合成脚本

| 脚本 | 说明 |
|------|------|
| `create_video.py` | 创建视频合成任务，输出视频 ID。支持数字人形象、TTS/音频、背景、字幕、合规水印等全部参数 |
| `poll_video.py` | 轮询视频合成任务直到完成（status=30），输出 `video_url` |

示例（卡通数字人 TTS 视频合成）：

```bash
SCRIPTS=skills/chanjing-content-creation-skill/products/chanjing-avatar/scripts

VIDEO_ID=$(python $SCRIPTS/create_video \
  --person-id "C-d1af99e0fee34978bc844d43078bf8c9" \
  --person-x 0 --person-y 480 --person-width 1080 --person-height 1440 \
  --text "君不见黄河之水天上来，奔流到海不复回。" \
  --audio-man "C-f2429d07554749839849497589199916" \
  --bg-color "#EDEDED" \
  --model 2)

python $SCRIPTS/poll_video --id "$VIDEO_ID"
```

音频驱动时：`create_video --person-id <id> ... --audio-type audio --wav-url "https://example.com/audio.mp3"`
或 `--audio-file-id <file_id>`（通过 `upload_file.py` 上传获得）。

## Response Status Code Description

| Code | Description |
|---|---|
| 0 | Response successful |
| 10400 | AccessToken verification failed |
| 40000 | Parameter error |
| 40001 | Exceeds RPM/QPS limit |
| 40002 | 制作视频时长到达上限 |
| 50000 | System internal error |
| 50011 | 作品存在不合规文字内容 |

