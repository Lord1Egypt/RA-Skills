# Daily WeChat Article Writer Skill

## Metadata
- **Name**: daily-wechat-writer
- **Description**: A cron-based skill that pitches 3 trending AI/Human-interest topics at 10:00 AM daily. Upon user selection, it auto-generates a full article with context-matched AI images and uploads it to WeChat draft box.
- **Author**: Liuu (Editor-in-Chief)
- **Version**: 1.1.0 (2026-03-26)

## Features
1. **Daily Pitch (10:00 AM)**: Aggregates trending topics from Reddit, Hacker News, Twitter, and Xiaohongshu. Filters for human-centric AI stories (micro-perspective, emotional, sincere).
2. **Auto-Writer**:
   - Deep research based on selected topic
   - Article writing in "Editor" persona (sincere, grounded, concise)
   - **Context-aware AI image generation** using Google Imagen 4
   - WeChat draft upload with proper Chinese title extraction
3. **Style Lock**: Enforces sincere, grounded, and concise writing style; ensures Chinese title is used.
4. **Image Matching Protocol**: Generated images must directly correspond to specific article sections (e.g., cover = IP creation scene, section images = concrete metaphors).

## Usage
- **Automatic**: Runs daily at 10:00 AM via system cron (managed by OpenClaw).
- **Manual**: `/daily-pitch` to trigger the pitch immediately.
- **Selection**: User replies "选1", "选2", etc. to trigger `auto_writer.py`.

## Files
- `scripts/daily_topic_pitch.py`: Fetches trends and formats the pitch.
- `scripts/auto_writer.py`: Handles writing, AI image generation (Imagen 4), and WeChat upload.
- `scripts/upload_to_wechat.py`: Handles Markdown parsing, title extraction, and WeChat API integration.

## Configuration
- **Time**: 10:00 AM Asia/Shanghai
- **Sources**: Reddit (r/ArtificialInteligence, r/ChatGPT), Hacker News, Xiaohongshu (via search), Twitter (AI influencers).
- **Image Generation**:
  - Model: `imagen-4.0-generate-001` (Google Imagen 4)
  - API Key: Configured via environment variable `GOOGLE_IMAGEN_API_KEY` (user-provided)
  - Aspect Ratio: 16:9 (800x450 or similar)
  - Prompt Style: Realistic, cinematic, authentic textures, matching article's "earthy" aesthetic

## Lessons Learned (2026-03-26)
1. **Unsplash实拍图虽可商用，但难以精准匹配微观意象** → 改用AI生图可100%定制
2. **封面图必须反映文章核心主题** → "个人IP/朋友圈"主题需要手机/社交媒体/摆摊等视觉符号
3. **标题提取必须优先使用Markdown中文化标题** → 修改了`upload_to_wechat.py`的标题解析逻辑
4. **图片审核需前置分析** → 每次生成图片后应检查：是否匹配段落？是否符合"土味/真实"美学？是否呼应标题？
5. **API测试流程**：先用curl测试imagen-4.0-generate-001端点，确认密钥有效后再批量生成
