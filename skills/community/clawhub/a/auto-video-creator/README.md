# Auto Video Creator - AI Video Generation from Text & Images

**Generate professional videos in seconds using XLXAI Sora2 API**

[English](#english) | [中文](#中文) | [日本語](#日本語) | [한국어](#한국어)

---

## English

### What is Auto Video Creator?

Auto Video Creator is an AI-powered video generation skill that creates short videos from text prompts or images using the XLXAI Sora2 API. It returns the raw task/result JSON (including video_url when generation completes). The skill focuses on video generation only—it does not upload or publish videos to social platforms.

---

## 中文

### 什么是视频自动生成器？

视频自动生成器是一个基于 XLXAI Sora2 API 的 AI 视频生成技能，可以从文字提示或图片生成短视频。返回 API 的 task/result JSON（完成时包含 video_url）。该技能仅负责视频生成，不负责上传或发布到社交平台。

---

## 日本語

### Auto Video Creator とは？

Auto Video Creator は、XLXAI Sora2 API を使用してテキストプロンプトまたは画像から短いビデオを生成する AI 駆動のビデオ生成スキルです。API が返すタスク/結果 JSON を返します（生成完了時にvideo_urlを含む）。このスキルはビデオ生成のみに焦点を当てており、ソーシャルプラットフォームへのアップロードまたは公開は行いません。

---

## 한국어

### Auto Video Creator란?

Auto Video Creator는 XLXAI Sora2 API를 사용하여 텍스트 프롬프트 또는 이미지에서 짧은 비디오를 생성하는 AI 기반 비디오 생성 스킬입니다. API가 반환하는 작업/결과 JSON을 반환합니다(생성 완료 시 video_url 포함). 이 스킬은 비디오 생성에만 중점을 두며 소셜 플랫폼으로의 업로드 또는 게시는 수행하지 않습니다.

---

## Key Features

- ✅ **Text-to-Video**: Generate videos from text prompts
- ✅ **Image-to-Video**: Create videos from images with motion
- ✅ **Multiple Formats**: Portrait & landscape orientations
- ✅ **Flexible Duration**: 4s, 8s, or 12s video lengths
- ✅ **Async Support**: Non-blocking task creation with polling
- ✅ **Simple CLI**: Easy-to-use Python script interface

## 主な機能

- ✅ **テキスト-ビデオ**: テキストプロンプトからビデオを生成
- ✅ **画像-ビデオ**: 画像からモーション付きビデオを作成
- ✅ **複数フォーマット**: ポートレートとランドスケープの向き
- ✅ **柔軟な期間**: 4秒、8秒、または12秒のビデオ長
- ✅ **非同期サポート**: ノンブロッキングタスク作成とポーリング
- ✅ **シンプルCLI**: 使いやすいPythonスクリプトインターフェース

## 주요 기능

- ✅ **텍스트-비디오**: 텍스트 프롬프트에서 비디오 생성
- ✅ **이미지-비디오**: 이미지에서 모션이 있는 비디오 생성
- ✅ **다양한 형식**: 세로 및 가로 방향
- ✅ **유연한 기간**: 4초, 8초 또는 12초 비디오 길이
- ✅ **비동기 지원**: 논블로킹 작업 생성 및 폴링
- ✅ **간단한 CLI**: 사용하기 쉬운 Python 스크립트 인터페이스

## Use Cases

- 📱 **TikTok**: Create viral short videos with text prompts
- 📺 **YouTube Shorts**: Generate quick video content for YouTube
- 📸 **Instagram Reels**: Produce engaging reels from images
- 🎬 **Content Creation**: Automate video production for creators
- 📢 **Marketing**: Generate promotional videos quickly
- 🎨 **Social Media**: Create consistent content across platforms

## 使用场景

- 📱 **TikTok**: 用文字提示创建病毒式短视频
- 📺 **YouTube Shorts**: 为YouTube生成快速视频内容
- 📸 **Instagram Reels**: 从图片生成吸引人的短视频
- 🎬 **内容创作**: 自动化视频制作流程
- 📢 **营销推广**: 快速生成宣传视频
- 🎨 **社交媒体**: 跨平台创建一致的内容

## ユースケース

- 📱 **TikTok**: テキストプロンプトからバイラル短編ビデオを作成
- 📺 **YouTube Shorts**: YouTubeの高速ビデオコンテンツを生成
- 📸 **Instagram Reels**: 画像から魅力的なリールを作成
- 🎬 **コンテンツ作成**: ビデオ制作を自動化
- 📢 **マーケティング**: プロモーションビデオを迅速に生成
- 🎨 **ソーシャルメディア**: プラットフォーム全体で一貫したコンテンツを作成

## 사용 사례

- 📱 **TikTok**: 텍스트 프롬프트에서 바이럴 숏폼 비디오 생성
- 📺 **YouTube Shorts**: YouTube용 빠른 비디오 콘텐츠 생성
- 📸 **Instagram Reels**: 이미지에서 매력적인 릴 생성
- 🎬 **콘텐츠 제작**: 비디오 제작 자동화
- 📢 **마케팅**: 프로모션 비디오 빠르게 생성
- 🎨 **소셜 미디어**: 플랫폼 전체에서 일관된 콘텐츠 생성

---

### Setup

```bash
cp skills/xlxai-video/.env.example skills/xlxai-video/.env
# Edit .env and set XLXAI_API_KEY
export XLXAI_API_KEY="sk-..."
```

### Generate Video (Blocking)

```bash
python3 skills/xlxai-video/scripts/generate_video.py "Your prompt here" --model sora2-portrait-4s
```

### Generate Video (Non-blocking)

```bash
python3 skills/xlxai-video/scripts/generate_video.py "Your prompt" --no-wait
```

### Image-to-Video

```bash
python3 skills/xlxai-video/scripts/generate_video.py "Describe scene" --image /path/to/image.jpg
```

## Example Output

```json
{
  "task_id": "task_XXXX",
  "status": "completed",
  "video_url": "https://.../xxx.mp4",
  "progress": 100,
  "duration": 38,
  "message": "Generation complete"
}
```

## Available Models

| Model | Orientation | Duration |
|-------|-------------|----------|
| sora2-portrait-4s | Portrait | 4 seconds |
| sora2-portrait-8s | Portrait | 8 seconds |
| sora2-portrait-12s | Portrait | 12 seconds |
| sora2-landscape-4s | Landscape | 4 seconds |
| sora2-landscape-8s | Landscape | 8 seconds |
| sora2-landscape-12s | Landscape | 12 seconds |

## Important Notes

- **Video URL**: May point to provider's CDN. Download and self-host if needed.
- **Copyright & Rights**: Verify copyright and portrait rights before publishing generated content.
- **API Key Security**: Keep your API key secret. Use environment variables or CI secrets in production.
- **Rate Limits**: Check XLXAI API documentation for rate limiting details.

## Support

- **Email**: yefl2064@gmail.com
- **Telegram**: [@kuajintontu](https://t.me/kuajintontu)

## サポート

- **メール**: yefl2064@gmail.com
- **Telegram**: [@kuajintontu](https://t.me/kuajintontu)

## 지원

- **이메일**: yefl2064@gmail.com
- **Telegram**: [@kuajintontu](https://t.me/kuajintontu)

## Changelog

**v1.0.0** — Initial release with text-to-video & image-to-video support
