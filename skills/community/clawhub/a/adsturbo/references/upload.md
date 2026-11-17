# Upload

Script: `scripts/upload.py`

## Why you must upload first, every time

All of AdsTurbo's generation endpoints accept asset parameters only as **publicly accessible URLs** — they do not accept local file paths or base64. If the user provides a local file, it must go through this step to become a URL first.

This is the most common pitfall: passing `./photo.jpg` directly into `--image-url` will always fail.

## Three commands

```bash
python3 scripts/upload.py image ./portrait.jpg     # image
python3 scripts/upload.py audio ./voice.mp3        # audio, no transcoding
python3 scripts/upload.py file  ./clip.mp4         # video and any other file
```

The response body contains the uploaded URL — use it directly as the asset parameter for the next command.

| Command | Purpose | Typical downstream use |
|---|---|---|
| `image` | Portraits, product photos, reference images, first/last frames, masks | `--photo-url` `--image-url` `--start-frame` `--reference-images` `--mask-url` |
| `audio` | Voiceovers, voice-cloning samples | `--audio-url` `--voice-audio-url` `--said-url` |
| `file` | Video assets | `--video-url` `--reference-videos` |

Use `audio` rather than `file` for audio — `audio` stores the file as-is without transcoding, preserving the audio quality needed for voice cloning.

## If it's already a URL, don't upload it

If the asset the user provides is already a public URL (e.g., a product page image or a CDN-hosted video), use it directly — don't download it and upload it again.

## Typical chaining

```bash
# Local photo + local recording -> a custom digital human voiceover
PHOTO=$(python3 scripts/upload.py image ./me.jpg)
VOICE=$(python3 scripts/upload.py audio ./sample.mp3)
# Extract the url field from the returned JSON and pass it into the next step
python3 scripts/digital_human.py persona-create --photo-url <url> --voice-audio-url <url>
```

## Limitations

- Uses `multipart/form-data`; authentication is the same as other endpoints (`Authorization: Bearer <API Key>`)
- Large file uploads are slow; set the client timeout to 300 seconds
- A missing file errors out immediately, without sending an invalid request

---

# 素材上传 / Upload

脚本：`scripts/upload.py`

## 为什么每次都要先上传

AdsTurbo 的所有生成接口，素材参数收的都是**公网可访问的 URL**，不接受本地文件路径，也不接受 base64。用户给的如果是本地文件，必须先过这一步换成 URL。

这是最容易踩的坑：直接把 `./photo.jpg` 填进 `--image-url` 一定失败。

## 三个命令

```bash
python3 scripts/upload.py image ./portrait.jpg     # 图片
python3 scripts/upload.py audio ./voice.mp3        # 音频，不转码
python3 scripts/upload.py file  ./clip.mp4         # 视频及其他任意文件
```

返回体里带上传后的 URL，直接拿去填下一个命令的素材参数。

| 命令 | 用途 | 典型下游 |
|---|---|---|
| `image` | 人像、商品图、参考图、首尾帧、mask | `--photo-url` `--image-url` `--start-frame` `--reference-images` `--mask-url` |
| `audio` | 配音、声音克隆样本 | `--audio-url` `--voice-audio-url` `--said-url` |
| `file` | 视频素材 | `--video-url` `--reference-videos` |

音频走 `audio` 而不是 `file`——`audio` 这条是原样存储不转码，能保住声音克隆需要的音质。

## 已经是 URL 就别上传

用户给的素材如果本来就是公网链接（比如商品详情页的图、CDN 上的视频），直接用，不用下载下来再传一遍。

## 典型串联

```bash
# 本地照片 + 本地录音 → 专属数字人口播
PHOTO=$(python3 scripts/upload.py image ./me.jpg)
VOICE=$(python3 scripts/upload.py audio ./sample.mp3)
# 从返回 JSON 里取出 url 字段，填进下一步
python3 scripts/digital_human.py persona-create --photo-url <url> --voice-audio-url <url>
```

## 限制

- 走 `multipart/form-data`，鉴权与其他接口一致（`Authorization: Bearer <API Key>`）
- 大文件上传较慢，客户端超时设为 300 秒
- 文件不存在会直接报错，不会发出无效请求
