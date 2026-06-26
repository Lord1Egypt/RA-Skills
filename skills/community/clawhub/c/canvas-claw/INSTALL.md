# Canvas Claw 安装指南

Canvas Claw 是一个新的 OpenClaw skill 包，底层通过 AI-video-agent API 提供图片和视频生成能力。

## 必需环境变量

```bash
export AI_VIDEO_AGENT_BASE_URL="http://localhost:8000"
export AI_VIDEO_AGENT_TOKEN="your_token"
export AI_VIDEO_AGENT_SITE_ID="10000"
```

## 登录辅助

```bash
python3 ./scripts/login.py \
  --base-url "http://localhost:8000" \
  --site-id 10000 \
  --username "demo" \
  --password "secret"
```

## 使用示例

```bash
python3 ./scripts/generate_image.py --prompt "cinematic portrait"
python3 ./scripts/generate_image.py --prompt "same character in snow" --reference-image "/tmp/ref.png"
python3 ./scripts/generate_video.py --prompt "a rainy city street at night"
python3 ./scripts/generate_video.py --prompt "the character turns and smiles" --first-frame "/tmp/frame.png"
python3 ./scripts/image_models.py
python3 ./scripts/video_models.py
```
