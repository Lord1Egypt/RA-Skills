---
name: video-editing
description: AI 视频编辑与后期，覆盖剪辑拼接、转场、字幕、配乐与批量格式处理，衔接 AI 生成片段与成品交付
source:
  type: derived
  repo: prime-skills/runcomfy-agent-skills
  path: video-edit/SKILL.md
  version: 1.0.0
  updated: 2026-05-15
  url: https://skills.sh/prime-skills/runcomfy-agent-skills/video-edit
metadata:
  category: 视频编辑
  platform: 通用
  difficulty: 进阶
tags:
  - video-editing
  - ffmpeg
  - concat
  - subtitle
  - post-production
---

# Video Editing — AI 视频编辑与后期

> 把 AI 变成剪辑助理：把生成片段拼接成成品，加转场、字幕、配乐，批量转格式。基于 skills.sh 全生态最高安装量（408.9K）的 runcomfy-agent-skills video-edit 改编，补充 ffmpeg 确定性命令。

## 能力

- **片段拼接（concat）**：同参数 AI 片段无缝拼接，不同参数片段加转场
- **转场与节奏**：硬切 / 淡入淡出 / 变速，匹配 BGM 节奏
- **字幕与配乐**：烧录字幕、BGM 混音、音量归一
- **批量格式处理**：MP4/WebM/GIF 互转、分辨率缩放、抽帧、裁剪
- **交付规范**：横竖屏、码率、H.264 编码统一（短视频平台兼容）

## 使用方式

在 Claude Code 中使用 `/video-editing` 调用。

```
/video-editing 把 output/ 下 5 段生成片段拼成一个 20 秒视频，加转场
/video-editing 给这段视频烧录中文字幕（srt 文件已有）
/video-editing 把这段 4K 视频压成抖音竖屏 1080p
```

## 工作流

1. **清点素材** — 确认片段参数一致（分辨率/fps），不一致先统一
2. **拼接** — 同参数用 ffmpeg concat（无损），不同参数用转场方案
3. **后期** — 字幕（srt 烧录）、BGM 混音、音量归一
4. **转码交付** — 目标平台规格（抖音 1080p 竖屏 / B 站 4K 横屏）；H.264 兼容性优先
5. **成片质检** — 全片抽查首/中/尾，音画同步确认

常用命令（详见脚本 [scripts/media_batch.py](../../scripts/media_batch.py) 与 ffmpeg 手册）：

```bash
# 同参数无损拼接
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4
# 烧录字幕
ffmpeg -i in.mp4 -vf subtitles=sub.srt -c:a copy out.mp4
# 压缩到抖音竖屏 1080p
ffmpeg -i in.mp4 -vf "scale=-2:1920" -c:v libx264 -crf 23 out.mp4
```

## 适用场景

- AI 视频生成后的人工后处理（拼接/字幕/配乐）
- 批量素材格式统一（转码、缩放、抽帧）
- 短视频平台交付（规格适配）
- 简单剪辑需求（不引入专业剪辑软件）

## 限制

- 不做精细剪辑（多轨/关键帧/调色），复杂需求请用专业软件
- 不做 AI 生成（见 `video-generation`）
- 音画同步问题依赖素材质量，无法靠后处理完全修复
- 字幕/配乐需自行准备素材，不提供生成能力

## 相关参考（Playbook）

- [references/video-generation-playbook.md](../../references/video-generation-playbook.md) — 第 4 节后处理与交付链路（片段质检 → 拼接 →
  配乐/字幕）、第 6 节交付清单；生成端参数与比例约定见第 3 节
