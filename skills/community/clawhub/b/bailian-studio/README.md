# bailian-studio

Bailian Studio skill: OCR text extraction + TTS speak + image generation.

## 功能一览

1) OCR 文本识别
- 支持本地图片与 URL
- 本地图片会先上传至 OSS，再调用百炼 OCR

2) TTS 语音播报（文本 → 语音播放）
- 百炼 TTS 生成 WAV
- 使用 ffplay 播放（依赖 ffmpeg）

3) 文生图 / 图生图
- 默认模型：`qwen-image-2.0-pro`
- 默认输出目录：`tmp/bailian-studio/`
- 默认输出格式：PNG
- 本地图生图参考图会先上传 OSS；URL 参考图直接透传
- 如果目标文件已存在，会自动重命名避免覆盖

## 安装依赖

```bash
pip install -r requirements.txt
brew install ffmpeg
```

## 配置（secrets/bailian.env）

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

## 使用方法

### OCR

```bash
python3 {baseDir}/scripts/ocr_text.py --image /path/to.png
python3 {baseDir}/scripts/ocr_text.py --url https://example.com/image.png
```

### TTS

```bash
python3 {baseDir}/scripts/tts_speak.py --text "你好"
```

### 文生图

```bash
python3 {baseDir}/scripts/image_generate.py \
  --prompt "一只坐在云端的橘猫，电影感，细节丰富" \
  --width 1024 \
  --height 1024
```

### 图生图（本地图片）

```bash
python3 {baseDir}/scripts/image_generate.py \
  --prompt "把这张图改成赛博朋克夜景风格" \
  --image /path/to/reference.png \
  --width 1024 \
  --height 1024
```

### 图生图（URL）

```bash
python3 {baseDir}/scripts/image_generate.py \
  --prompt "把这张图改成吉卜力动画风格" \
  --image https://example.com/reference.png \
  --width 1024 \
  --height 1024
```

### 从 stdin 读取 prompt

```bash
echo "一只戴着宇航员头盔的柴犬" | python3 {baseDir}/scripts/image_generate.py
```

### 输出文件

- 不指定 `--output` 时，默认写入 `tmp/bailian-studio/`
- 指定 `--output /path/to/out.png` 时，保存到该文件
- 指定 `--output /path/to/dir/` 时，自动在该目录生成文件名
- 成功后 stdout 只打印最终保存路径
