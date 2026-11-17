# douyin-article · 视频批量转录为结构化逐字稿

批量把抖音 / B 站 / 小宇宙 / YouTube / Vimeo / TikTok 等任意平台音视频转录为带语义切分的 Markdown 逐字稿（每视频一个独立 .md）。

特色：
- **5+0.5 阶段管线**：fetch → transcribe（仅无字幕时）→ pack + 语言检测 → 3.5 translate（仅非中文时）→ boundaries → build
- **全平台支持**：抖音 / B站 / 小宇宙 / YouTube + yt-dlp 1700+ 平台（Vimeo / TikTok / Twitter / X / Twitch / TED 等）
- **三层字幕探测（v4.1）**：B站公共 API → yt-dlp → Whisper，平台有字幕时跳过 Whisper（节省 95% 能耗）
- **双语对比翻译**：用户使用「双语转录」触发词时，非中文内容翻译为中文，输出「中文译文 + 英文原文 blockquote」段落对比格式
- **6 路由模型**：lesson / explainer / conversation / demo / narrative / bulletin
- **Light-plus 原则**：保留推理 / 例子 / 数字 / 限定条件，非摘要
- **按语义边界切分**，不机械每 60/90 秒切一段
- **错字自动修正**（faster-whisper 在中文上的常见同音错字）

## 用户须知

- **本地副作用**：脚本会下载视频/音频流到 `outputs/` 目录，调用 ffmpeg/yt-dlp/agent-browser 等外部进程
- **网络访问**：B站公共 API、抖音 CDN、YouTube transcript API；YouTube 走 `HTTPS_PROXY` 代理
- **资源占用**：Whisper 转录会占用 GPU/CPU 资源（字幕可用时自动跳过）
- **清理方式**：删除 `outputs/` 目录可清理全部中间产物

## 安装

```bash
pip install faster-whisper opencc-python-reimplemented youtube-transcript-api
pip install -U yt-dlp
winget install Gyan.FFmpeg
npm install -g agent-browser
```

## 使用

把链接写到 `inputs.txt`，每行一条（支持抖音分享文本、抖音 URL、B 站 URL 含 p=N 参数）：

```
7.94 复制打开抖音【教不会再杠Vivian的作品】第一讲-找到核心动词 https://v.douyin.com/xxx/
https://www.bilibili.com/video/BV1NK411D7pr?p=1
```

然后依次执行：

```bash
# 阶段 1：批量获取（字幕优先，无字幕时下载音频）
python scripts/01_fetch.py inputs.txt --output-dir outputs/batch
# 阶段 2：Whisper 转录（仅无字幕视频）
python scripts/02_transcribe.py --metadata outputs/batch/metadata.json --output-dir outputs/batch
# 阶段 3：打包 + 语言检测
python scripts/03_pack_transcript.py --transcript-dir outputs/batch/transcript --output-dir outputs/batch

# 阶段 3.5：翻译（仅非中文视频）
python scripts/03_5_translate.py prepare --output-dir outputs/batch/work
# 主对话循环：next-batch → AI 翻译 → apply（重复直到 done）

# 阶段 4：主对话读 work/boundary-review_N.md + takes_packed_N.md，写 scene-boundaries_N.json
# 阶段 5：输出 MD（自动识别双语）
python scripts/04_build_output.py --transcript-dir outputs/batch/transcript --boundaries-dir outputs/batch/work --output-dir outputs/batch
```

最终输出在 `outputs/batch/share/*.md`。非中文视频在「双语转录」触发词下输出双语对比格式。

## 文档

- [SKILL.md](SKILL.md) — 主入口
- [references/pipeline-details.md](references/pipeline-details.md) — 5+0.5 阶段管线 + 平台支持矩阵
- [references/route-rules.md](references/route-rules.md) — 6 路由模型
- [references/examples.md](references/examples.md) — 完整示例集
- [references/troubleshooting.md](references/troubleshooting.md) — 故障排查 + 首次使用配置

## License

MIT-0

---

# douyin-article · Batch Video Transcription to Structured Transcript

Batch transcribe Douyin / Bilibili / Xiaoyuzhou / YouTube / Vimeo / TikTok and other platform audio/video into semantically segmented Markdown transcripts (one .md per video).

Highlights:
- 5+0.5 stage pipeline: fetch → transcribe (only when no subtitles) → pack + language detection → 3.5 translate (only for non-Chinese) → boundaries → build
- Full platform support: Douyin / Bilibili / Xiaoyuzhou / YouTube + yt-dlp 1700+ platforms (Vimeo / TikTok / Twitter / X / Twitch / TED, etc.)
- Three-layer subtitle detection (v4.1): Bilibili public API → yt-dlp → Whisper; skip Whisper when platform subtitles available (saves 95% energy)
- Bilingual contrast translation: when user triggers with "双语转录" (bilingual transcribe), non-Chinese content is translated to Chinese, output as "Chinese translation + English original blockquote" paragraph contrast format
- 6-route model: lesson / explainer / conversation / demo / narrative / bulletin
- Light-plus principle: keep reasoning / examples / numbers / qualifiers, not a summary
- Semantic boundary segmentation, not mechanical 60/90s cuts
- Auto error correction (common faster-whisper homophone errors in Chinese)

## User Notices

- **Local side effects**: Scripts download video/audio streams to `outputs/` directory, invoke ffmpeg/yt-dlp/agent-browser external processes
- **Network access**: Bilibili public API, Douyin CDN, YouTube transcript API; YouTube uses `HTTPS_PROXY`
- **Resource usage**: Whisper transcription consumes GPU/CPU resources (auto-skipped when subtitles available)
- **Cleanup**: Delete the `outputs/` directory to clean all intermediate artifacts

## Install

```bash
pip install faster-whisper opencc-python-reimplemented youtube-transcript-api
pip install -U yt-dlp
winget install Gyan.FFmpeg
npm install -g agent-browser
```

## Usage

Write links to `inputs.txt`, one per line (supports Douyin share text, Douyin URLs, Bilibili URLs with p=N parameter):

```
https://www.bilibili.com/video/BV1NK411D7pr?p=1
https://www.youtube.com/watch?v=xxxxx
```

Then run:

```bash
# Stage 1: Batch fetch (subtitle-first, fallback to audio download)
python scripts/01_fetch.py inputs.txt --output-dir outputs/batch
# Stage 2: Whisper transcription (only for videos without subtitles)
python scripts/02_transcribe.py --metadata outputs/batch/metadata.json --output-dir outputs/batch
# Stage 3: Pack + language detection
python scripts/03_pack_transcript.py --transcript-dir outputs/batch/transcript --output-dir outputs/batch

# Stage 3.5: Translation (only for non-Chinese videos)
python scripts/03_5_translate.py prepare --output-dir outputs/batch/work
# Main conversation loop: next-batch → AI translate → apply (repeat until done)

# Stage 4: Main conversation reads work/boundary-review_N.md + takes_packed_N.md, writes scene-boundaries_N.json
# Stage 5: Output MD (auto-detect bilingual)
python scripts/04_build_output.py --transcript-dir outputs/batch/transcript --boundaries-dir outputs/batch/work --output-dir outputs/batch
```

Final output in `outputs/batch/share/*.md`. Non-Chinese videos output bilingual contrast format under the "双语转录" (bilingual transcribe) trigger.

## Docs

- [SKILL.md](SKILL.md) — Main entry
- [references/pipeline-details.md](references/pipeline-details.md) — 5+0.5 stage pipeline + platform matrix
- [references/route-rules.md](references/route-rules.md) — 6-route model
- [references/examples.md](references/examples.md) — Full example set
- [references/troubleshooting.md](references/troubleshooting.md) — Troubleshooting + first-use config

## License

MIT-0
