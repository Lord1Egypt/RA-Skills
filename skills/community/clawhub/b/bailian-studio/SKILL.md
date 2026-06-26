---
name: bailian-studio
description: Call Aliyun Bailian via DashScope; support OCR, TTS, text-to-image and image-to-image.
---

# Bailian Studio

Use DashScope for OCR、TTS、文生图、图生图。

## Requirements

- Python 3
- `dashscope` (>=1.24.0)
- `oss2`
- `requests`
- `ffmpeg`（TTS 播放依赖，使用 ffplay）

Install:
```bash
pip install -r requirements.txt
```

## Config

**API Key (priority order):**
1. `DASHSCOPE_API_KEY` env
2. `secrets/bailian.env`

**OSS (priority order):**
1. `OSS_ACCESS_KEY`, `OSS_SECRET_KEY`, `OSS_BUCKET`, `OSS_ENDPOINT`, `OSS_REGION` env
2. `secrets/bailian.env`

Example `secrets/bailian.env`:
```env
DASHSCOPE_API_KEY=sk-xxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/api/v1

# TTS 可选配置（留空走默认）
BAILIAN_TTS_MODEL=qwen3-tts-flash
BAILIAN_TTS_VOICE=
BAILIAN_TTS_SAMPLE_RATE=16000

OSS_ACCESS_KEY=ak-xxx
OSS_SECRET_KEY=sk-xxx
OSS_BUCKET=your-bucket
OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com
OSS_REGION=cn-beijing
```

**Defaults:**
- Region/base URL: Beijing (`https://dashscope.aliyuncs.com/api/v1`)
- Image model: `qwen-image-2.0-pro`
- Output dir: `tmp/bailian-studio/`
- Output format: PNG

## Usage

### TTS (speak)

```bash
python3 {baseDir}/scripts/tts_speak.py --text "你好"
```

### OCR (text)

From local image (uploads to OSS):
```bash
python3 {baseDir}/scripts/ocr_text.py --image /path/to.png
```

From URL:
```bash
python3 {baseDir}/scripts/ocr_text.py --url https://example.com/image.png
```

### Image generate (text-to-image)

```bash
python3 {baseDir}/scripts/image_generate.py \
  --prompt "一只坐在云端的橘猫" \
  --width 1024 \
  --height 1024
```

### Image generate (image-to-image)

Local image:
```bash
python3 {baseDir}/scripts/image_generate.py \
  --prompt "改成赛博朋克风格" \
  --image /path/to/reference.png \
  --width 1024 \
  --height 1024
```

URL image:
```bash
python3 {baseDir}/scripts/image_generate.py \
  --prompt "改成水彩插画风格" \
  --image https://example.com/reference.png \
  --width 1024 \
  --height 1024
```

### stdin prompt

```bash
echo "一只会发光的鲸鱼漂浮在夜空" | python3 {baseDir}/scripts/image_generate.py
```

## Behavior

- 本地参考图：先上传 OSS，再传给 DashScope
- URL 参考图：直接透传给 DashScope
- 默认一次生成 1 张图
- 成功后 stdout 打印保存路径
- 若文件名已存在，自动重命名
- 失败时输出错误信息并返回非 0 退出码
