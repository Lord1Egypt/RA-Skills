---
name: fcpx-assistant
description: "Final Cut Pro X (FCPX) 助手 — 全自动视频生产（从主题到发布）、TTS 配音、素材搜集、自动成片、调色、B-roll 插入、FCP 项目管理、剪辑辅助。触发词: FCPX, FCP, Final Cut, 做视频, 自动成片, 配音, voiceover, 素材, 导入素材, 导出, 发布视频, 调色, B-roll, 视频制作, make video, auto video, import media, export, color grade, publish"
---

# Final Cut Pro 助手

全自动视频生产线 + FCP 日常剪辑助手。

## 核心工作流

```
主题 💡 → AI 文案 📝 → 搜素材 🔍 → TTS 配音 🎤 → 自动成片 🎞️ → 调色 🎨 → B-roll 🎬 → 发布 🚀
```

### 一键全流程

```bash
bash scripts/auto-video-from-topic.sh \
    --topic "如何制作一杯完美的咖啡" \
    --publish bilibili \
    --title "咖啡教程" --tags "咖啡，教程"
```

### 分步执行

**Step 1: AI 文案** — 根据主题生成分镜脚本 + 配音文本 + 素材关键词

```bash
bash scripts/ai-script-generator.sh --topic "主题" --style 教程 --duration 90 --keywords
```

**Step 2: 搜集素材** — 从 Pexels/Pixabay 下载免费素材

```bash
bash scripts/media-collector.sh --keywords "nature ocean sunset" --count 5 --output ./my-project
```

**Step 3: 背景音乐** — 把 BGM (mp3/wav/m4a) 放入 `./my-project/music/`

```bash
bash scripts/music-collector.sh --keywords "轻松 愉快" --count 3 --output ./my-project/music
```

**Step 4: TTS 配音** — edge-tts 生成配音（免费、稳定、支持多声线）

```bash
bash scripts/tts-voiceover.sh --script-file ./script.txt --output ./my-project/voiceover --merge
# 可选声音：--voice zh-CN-YunxiNeural (男) / zh-CN-XiaoxiaoNeural (女)
```

**Step 5: 自动成片** — 素材 + 配音 + 字幕 + BGM 组装成完整视频

```bash
bash scripts/auto-video-maker.sh \
    --project ./my-project --script-file ./script.txt \
    --voiceover ./my-project/voiceover --style vlog --output final.mp4
```

智能特性：配音时长自动对齐、PingFang SC 字幕烧入、BGM 自动降到 15%、fade 转场、自动清理中间文件。

**Step 6: 调色**（可选）

```bash
bash scripts/auto-color-grade.sh final.mp4 final-graded.mp4 --style cinematic --intensity 0.7
```

风格：natural / cinematic / vintage / fresh / warm / cool

**Step 7: B-roll 插入**（可选）

```bash
bash scripts/auto-broll-insert.sh final.mp4 ./broll/ output.mp4 --script script.txt --transition fade
```

自动在场景转换处插入，支持文案关键词智能匹配。

**Step 8: 发布**

```bash
bash scripts/auto-publish.sh --video final.mp4 --platform bilibili --title "标题" --tags "标签"
```

支持 bilibili / youtube / tiktok / xiaohongshu。配置详情见 [references/publishing.md](references/publishing.md)。

---

## 项目目录结构

```
my-project/
├── videos/     ← 素材（Step 2 自动填充）
├── music/      ← BGM（Step 3）
├── voiceover/  ← 配音（Step 4 自动生成：vo_000.wav, vo_001.wav...）
└── meta/       ← 元数据（自动生成）
```

---

## FCP 项目管理

```bash
osascript scripts/check-fcp.scpt             # 检查 FCP 状态
osascript scripts/list-projects.scpt          # 列出所有项目
osascript scripts/open-project.scpt "名称"     # 打开项目
osascript scripts/import-temp-media.scpt      # 导入临时素材
osascript scripts/project-time-tracking.scpt  # 时间追踪
osascript scripts/create-script.scpt "标题" "内容"  # 创建文案
osascript scripts/list-scripts.scpt           # 列出文案
```

## 剪辑辅助

```bash
bash scripts/scene-detect.sh video.mp4          # 场景检测
bash scripts/auto-rough-cut.sh video.mp4         # 自动粗剪（去静音）
bash scripts/smart-tagger.sh ./media/            # 智能标签
bash scripts/auto-chapter-marker.sh video.mp4    # 自动章节标记
bash scripts/audio-normalizer.sh video.mp4       # 音频标准化 (-23 LUFS)
bash scripts/auto-voiceover.sh "文本" out.wav     # 单文件配音 (edge-tts)
bash scripts/multi-lang-subtitles.sh video.mp4 en  # 多语言字幕 (Whisper)
bash scripts/auto-thumbnail.sh video.mp4 ./thumbs  # 关键帧缩略图
```

## 新功能

```bash
bash scripts/auto-bgm-match.sh -v video.mp4 -m ./bgm/ -o output.mp4   # 智能 BGM 匹配
bash scripts/multi-platform-export.sh video.mp4 -p tiktok bilibili     # 多平台适配导出
bash scripts/subtitle-styler.sh --srt sub.srt --style cinematic        # 字幕样式增强
bash scripts/video-analyzer.sh video.mp4                                # 视频质量分析
bash scripts/intro-outro-generator.sh --title "标题" --type intro       # 片头片尾生成
bash scripts/cover-generator.sh --video video.mp4 --title "标题" --all  # 封面图生成
```

## Web UI

```bash
bash start-webui.sh   # 启动后访问 http://localhost:7861
```

一键成片界面，含实时进度条、分步工具、项目历史、调色/B-roll 控制。

---

## 参考文档

- **风格预设 & 所有参数**: [references/styles-options.md](references/styles-options.md)
- **平台发布配置**: [references/publishing.md](references/publishing.md)
- **依赖安装 & TTS 部署**: [references/dependencies.md](references/dependencies.md)

## 必需依赖速查

ffmpeg (drawtext) · osascript · curl · jq · edge-tts (pipx install edge-tts) · whisper (brew install openai-whisper)

安装详情见 [references/dependencies.md](references/dependencies.md)。
