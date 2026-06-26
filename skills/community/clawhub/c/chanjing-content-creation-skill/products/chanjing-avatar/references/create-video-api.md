# 视频合成 API 完整参数参考

> 本文件为 `chanjing-avatar-SKILL.md` 的补充参考。完整官方文档见 [创建视频合成任务](https://doc.chanjing.cc/api/video-synthesis/create-video-task.html)。

## POST /open/v1/create_video

### 完整请求参数

| Parameter | Type | Required | Description |
|---|---|---|---|
| **person** | object | Yes | 数字人形象配置 |
| person.id | string | Yes | 形象 ID（通过公共数字人或定制数字人列表获取） |
| person.x | int | Yes | 数字人 x 坐标 |
| person.y | int | Yes | 数字人 y 坐标 |
| person.width | int | Yes | 数字人显示宽度 |
| person.height | int | Yes | 数字人显示高度（不允许为奇数） |
| person.figure_type | string | No | 仅公共数字人需传，如 `whole_body` / `sit_body` |
| person.drive_mode | string | No | 驱动模式：`""` 正常顺序（默认）、`random` 随机帧动作 |
| person.is_rgba_mode | bool | No | 是否输出四通道 webm。注意：1. 需 webm 格式四通道定制数字人；2. 2025-02-08 后定制生效；3. 输出不含字幕与背景 |
| person.backway | int | No | 素材末尾播放顺序：1 正放（默认）、2 倒放 |
| **audio** | object | Yes | 音频配置 |
| audio.type | string | Yes | `tts`（文本驱动）或 `audio`（音频文件驱动） |
| audio.tts | object | Yes (tts) | TTS 配置 |
| audio.tts.text | string[] | Yes (tts) | TTS 文本数组，**所有内容放一个字符串**，用标点分割，**长度 < 4000 字符**。多音字参考 [SSML](https://doc.chanjing.cc/api/video-synthesis/ssml.html) |
| audio.tts.audio_man | string | Yes (tts) | 声音 ID（支持公共声音 & API 定制声音），参考[公共声音列表](https://doc.chanjing.cc/api/common-material/common-voice.html) |
| audio.tts.speed | float | No | 语速 0.5–2，默认 1 |
| audio.tts.pitch | float | No | 音调，定制声音的范围参考[创建语音生成任务](https://doc.chanjing.cc/api/speech-synthesis/create-speech-task.html) |
| audio.file_id | string | Yes (audio) | 通过文件管理上传的音频 file_id（字幕需单声道 8000/16000 Hz），编码：audio/x-wav, audio/mpeg |
| audio.wav_url | string | No | 音频文件 URL（支持 mp3/m4a/wav/mp4，后缀须含文件类型），编码：audio/x-wav, audio/mpeg, audio/m4a, video/mp4 |
| audio.volume | int | No | 音量，默认 100 |
| audio.language | string | No | 语言，默认 `cn` |
| **bg_color** | string | No | 背景颜色，格式 `#RRGGBB`，如 `#EDEDED` |
| **bg** | object | No | 背景图片配置（可选） |
| bg.src_url | string | No | 背景图 URL（仅支持 jpg/png） |
| bg.file_id | string | No | 通过文件管理上传的背景素材 ID |
| bg.x | int | No | 背景图 x 坐标 |
| bg.y | int | No | 背景图 y 坐标 |
| bg.width | int | No | 背景图宽度 |
| bg.height | int | No | 背景图高度 |
| **subtitle_config** | object | No | 字幕配置（各参数推荐使用默认值，计算较复杂） |
| subtitle_config.show | bool | No | 是否显示字幕 |
| subtitle_config.x | int | No | 字幕起始 x 坐标，推荐 31（4K 推荐 80） |
| subtitle_config.y | int | No | 字幕起始 y 坐标，推荐 1521（4K 推荐 2840） |
| subtitle_config.width | int | No | 字幕区域宽度，推荐 1000（4K 推荐 2000），不能超过屏幕宽度 |
| subtitle_config.height | int | No | 字幕区域高度，推荐 200（4K 推荐 1000），不能超过屏幕高度 |
| subtitle_config.font_size | int | No | 字体大小，推荐 64（4K 推荐 150） |
| subtitle_config.color | string | No | 字体颜色，格式 `#RRGGBB` |
| subtitle_config.stroke_color | string | No | 字体描边颜色，格式 `#RRGGBB` |
| subtitle_config.stroke_width | int | No | 字体描边宽度，推荐 7 |
| subtitle_config.font_id | string | No | 字体 ID，参考[获取支持的字体列表](https://doc.chanjing.cc/api/video-synthesis/get-font-list.html) |
| subtitle_config.asr_type | int | No | 字幕时间戳来源：0 自动生成（默认）、1 用户输入 |
| subtitle_config.subtitles | array | No | 自定义字幕时间轴数组 |
| subtitle_config.subtitles[].begin_time | int | No | 字幕开始时间 |
| subtitle_config.subtitles[].end_time | int | No | 字幕结束时间 |
| subtitle_config.subtitles[].text | string | No | 字幕内容 |
| **screen_width** | int | No | 屏幕宽度，默认 1080 |
| **screen_height** | int | No | 屏幕高度，默认 1920 |
| **model** | int | No | 0=基础版 蝉镜 lip-sync（1蝉豆/秒）；1=高质版 lip-sync Pro（2蝉豆/秒）；**2=卡通形象专用**（3蝉豆/秒，训练素材必须为卡通形象） |
| **callback** | string | No | 任务完成回调 URL，POST 请求体格式与[拉取视频详情](https://doc.chanjing.cc/api/video-synthesis/get-video-detail.html)返回的 data 相同 |
| **add_compliance_watermark** | bool | No | 是否添加 AI 作品合规水印 |
| **compliance_watermark_position** | int | No | 水印位置：0 左上（默认）、1 右上、2 左下、3 右下 |
| **resolution_rate** | int | No | 0=1080p（默认）、1=4K。4K 时需数字人 `support_4k=true`，并自行调整屏幕宽高 |

### 回调参数示例

任务完成后回调 POST 请求体：

```json
{
    "id": "1914661228878233600",
    "status": 30,
    "progress": 100,
    "msg": "",
    "video_url": "https://res.chanjing.cc/chanjing/prod/dhaio/output/2025-04-22/xxx-output.mp4",
    "subtitle_data_url": "",
    "create_time": 1745325784,
    "preview_url": "https://res.chanjing.cc/chanjing/prod/dhaio/output/2025-04-22/xxx-cover.jpg",
    "duration": 45,
    "audio_urls": [
        "https://res.chanjing.cc/chanjing/res/upload/tts/2025-04-22/xxx.wav"
    ]
}
```

## GET /open/v1/video — 获取视频详情

Query param: `id` = 视频 ID

### 响应字段

| Field | Description |
|---|---|
| id | 视频 ID |
| status | **10**=生成中；**30**=成功；**4X**=参数异常；**5X**=服务异常 |
| progress | 任务进度 0-100 |
| msg | 异常或失败的错误信息（如：蝉豆不足、音频中没有人声、不支持的音频格式等） |
| video_url | 视频播放/下载地址 |
| subtitle_data_url | 字幕时间轴链接（需下载获取） |
| preview_url | 视频预览封面图 |
| duration | 视频时长（秒） |
| create_time | 生成时间（unix 时间戳） |

### 字幕时间轴字段

下载 `subtitle_data_url` 后的 JSON 结构：

```json
[
    {
        "min_time": 0,
        "max_time": 734,
        "subtitles": "字幕内容",
        "start_frame": 0,
        "end_frame": 18,
        "fps": 25
    }
]
```

## POST /open/v1/video_list — 获取视频列表

Request body: `{ "page": 1, "page_size": 10 }`

响应 `data.List` 为视频数组（字段与 detail 相同），`data.PageInfo` 含 `page`、`size`、`total_count`、`total_page`。

## 响应状态码

| code | 说明 |
|---|---|
| 0 | 响应成功 |
| 400 | 传入参数格式错误 |
| 10400 | AccessToken验证失败 / APP状态错误 |
| 40000 | 参数错误（含：缺少 tts 文本、缺少音频文件、不支持的图片格式、屏幕宽高不合法、字幕尺寸超屏幕、颜色格式错误、非 webm 数字人无法生成四通道、公共数字人需指定 figure_type、数字人高不允许为奇数等） |
| 40001 | 超出 QPS 限制（10/min） |
| 40002 | 制作视频时长到达上限 |
| 50000 | 系统内部错误（含：定制数字人不存在、公共数字人形象不对、声音 ID 不存在等） |
| 50011 | 作品存在不合规文字内容 |
