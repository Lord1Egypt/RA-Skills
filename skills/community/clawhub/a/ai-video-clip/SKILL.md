---
name: ai-video-clip
description: AI 智能视频剪辑助手。支持 ASR 语音转文字、词级时间戳剪切、LLM 驱动剪辑决策（EDL）、视频渲染、自检循环、多平台导出。当用户需要：自动剪辑视频、AI 理解视频内容并剪切、生成字幕并烧录、提取高光片段、导出短视频、多平台视频格式适配时使用此技能。

---

# Video Clip Assistant v2

AI 智能视频剪辑助手。基于 video-use 架构改进，本地 Whisper 替代付费 API，在 WorkBuddy 环境下实现完整 AI Agent 驱动剪辑闭环。

> **核心理念**：用户只需描述剪辑意图，AI Agent 自动完成转录 → 分析 → 编辑决策 → 渲染 → 自检全流程。无需手动操作时间轴。

## 架构概述

```
素材文件夹 → Layer 1 转录层 → Layer 2 AI决策层 → Layer 3 渲染层 → Layer 4 自检层 → 成品
                  ↓                    ↓                ↓              ↓
            Whisper/ASR        LLM 分析生成 EDL    FFmpeg 渲染    质量检查循环
```

## 快速开始

### 一键智能剪辑（AI Agent 工作流）

```bash
# 1. 转录视频
python3 scripts/transcribe.py --input my_video.mp4 --output transcript.json --format json

# 2. 预览 LLM prompt
python3 scripts/generate_edl.py --transcript transcript.json --strategy remove_fillers --dry-run

# 3. 在 WorkBuddy 对话中粘贴 prompt，获取 EDL JSON，保存为 edl.json

# 4. 预览 EDL
python3 scripts/render_edl.py --edl edl.json --dry-run

# 5. 渲染视频
python3 scripts/render_edl.py --edl edl.json --output edit/final.mp4

# 6. 自检质量
python3 scripts/self_eval.py --video edit/final.mp4 --edl edl.json --output quality_report.json
```

### 简短模式（交互式对话）

直接在对话中说：

> "帮我剪辑 `~/Videos/meeting.mp4`，去掉所有口癖和长停顿"
> "从 `~/Videos/live.mp4` 提取 5 个最精彩的高光片段"

Agent 会自动识别意图 → 选择策略 → 生成 EDL → 请求确认 → 渲染 → 自检 → 交付。

## 核心脚本

### `scripts/transcribe.py` — ASR 转录层 (新增)

高精度语音转文字，输出结构化 packed transcript。

```bash
python3 scripts/transcribe.py \
  --input <视频/音频文件> \
  --engine <whisper|faster-whisper|funclip> \
  --model <tiny|base|small|medium|large> \
  --language <zh|en|auto> \
  --diarize \
  --format <json|packed> \
  --output <输出文件>
```

| 引擎 | 特点 | 推荐场景 |
|------|------|---------|
| `whisper` | OpenAI 标准，词级时间戳 | 英文/多语言 |
| `faster-whisper` | CTranslate2 加速，显存更少 | 本地部署 |
| `funclip` | 阿里 DAMO，中文最优 | 中文视频 |

### `scripts/generate_edl.py` — AI 决策层 (新增)

基于 transcript 和剪辑策略生成 Edit Decision List。

```bash
python3 scripts/generate_edl.py \
  --transcript <transcript.json> \
  --strategy <remove_fillers|extract_highlights|condense|topic_splits|social_clip|custom> \
  --output <edl.json>
```

**内置策略** (详见 `templates/clip_strategies.yaml`):

| 策略 | 说明 |
|------|------|
| `remove_fillers` | 去口癖/um/uh/那个/然后 + 静音裁剪 |
| `extract_highlights` | 提取 N 个最精彩高光片段 |
| `condense` | 精简到目标时长 |
| `topic_splits` | 按主题自动分片 |
| `social_clip` | 社交平台适配剪辑 |
| `custom` | 自定义要求 |

### `scripts/render_edl.py` — 渲染执行层 (新增)

按 EDL 指令调用 FFmpeg 渲染最终视频。

```bash
python3 scripts/render_edl.py \
  --edl <edl.json> \
  --output <edit/final.mp4> \
  [--segments] \
  [--dry-run]
```

**渲染特性**:
- 自动 30ms 音频 crossfade at cut points
- 支持色彩校正 (warm/cool/cinematic/vivid)
- 字幕烧录
- Concat 拼接

### `scripts/self_eval.py` — 自检循环 (新增)

渲染后自动检查视频质量。

```bash
python3 scripts/self_eval.py \
  --video <edit/final.mp4> \
  --edl <edl.json> \
  --output <quality_report.json>
```

**检查项**:
- 时长与 EDL 预期对比
- 黑帧检测
- 音频爆音
- 过长静音
- 切点边界完整性

### `scripts/generate_subtitles.py` — 字幕生成 (新增)

基于 Whisper 词级时间戳生成 SRT 字幕。

```bash
python3 scripts/generate_subtitles.py \
  --input <视频文件> \
  --output <subs.srt> \
  --mode <sentence|standard|word_chunk> \
  --style <default|netflix|douyin|bilibili|youtube|minimal>
```

**字幕模式**:
| 模式 | 说明 |
|------|------|
| `sentence` | 智能断句（基于标点和停顿） |
| `standard` | 标准按长度分割（max 25字/行） |
| `word_chunk` | 两词一组 UPPERCASE（快节奏风格） |

字幕风格预设：`templates/subtitle_styles.json`。

### 保留脚本 (增强)

#### `scripts/cut_video.py`
按时间轴剪切视频（支持 EDL JSON 输入）。
```bash
# 传统模式
python3 scripts/cut_video.py --input video.mp4 --start 10 --duration 30 --output clip.mp4
python3 scripts/cut_video.py --input video.mp4 --segments "0-30,60-90,120-150" --output ./clips/

# EDL 模式 (新增)
python3 scripts/cut_video.py --input video.mp4 --edl edl.json --output ./clips/
```

#### `scripts/extract_highlights.py`
双重维度高光提取：音频能量 + 场景检测。
```bash
python3 scripts/extract_highlights.py \
  --input <视频> \
  --num-clips <数量> \
  --min-duration <秒> \
  --output <目录> \
  [--transcript transcript.json]  # 新增：结合语义增强
```

#### `scripts/burn_subtitles.py`
可配置字幕风格烧录。
```bash
python3 scripts/burn_subtitles.py \
  --input <视频> \
  --srt <字幕.srt> \
  --output <输出.mp4> \
  [--style <风格预设>]          # 新增
  [--style-file styles.json]    # 新增
```

#### `scripts/export_social.py`
多平台短视频格式导出（保留）。
```bash
python3 scripts/export_social.py \
  --input <视频> \
  --format <vertical|square|horizontal> \
  --duration <秒> \
  --output <目录>
```

## 典型工作流

### 工作流 1: 从长视频/直播回放提取精华

```bash
# 1. 转录
python3 scripts/transcribe.py --input raw_video.mp4 --output transcript.json

# 2. 生成高光 EDL
python3 scripts/generate_edl.py \
  --transcript transcript.json \
  --strategy extract_highlights \
  --num-clips 5 \
  --output highlights_edl.json

# 3. 渲染
python3 scripts/render_edl.py \
  --edl highlights_edl.json \
  --output edit/highlights.mp4

# 4. 导出多平台版本
python3 scripts/export_social.py \
  --input edit/highlights.mp4 \
  --format vertical \
  --duration 60 \
  --output shorts/
```

### 工作流 2: 去口癖精修口播视频

```bash
# 1. 转录 (词级时间戳)
python3 scripts/transcribe.py \
  --input talking_head.mp4 \
  --output transcript.json

# 2. 生成去冗余 EDL
python3 scripts/generate_edl.py \
  --transcript transcript.json \
  --strategy remove_fillers \
  --output clean_edl.json

# 3. 生成字幕
python3 scripts/generate_subtitles.py \
  --input talking_head.mp4 \
  --output subs.srt \
  --mode sentence \
  --style netflix

# 4. 渲染 (带色彩校正 + 字幕)
python3 scripts/render_edl.py \
  --edl clean_edl.json \
  --output edit/final.mp4

# 5. 烧录字幕
python3 scripts/burn_subtitles.py \
  --input edit/final.mp4 \
  --srt subs.srt \
  --style netflix \
  --output edit/final_subtitled.mp4

# 6. 质量检查
python3 scripts/self_eval.py \
  --video edit/final_subtitled.mp4 \
  --edl clean_edl.json
```

### 工作流 3: 批量制作社交平台短视频

直接把需求告诉 AI Agent：

> "帮我把 `~/Videos/tutorial.mp4` 拆成 5 个 60 秒的抖音竖版短视频，每个视频有 hook 和 CTA，加字幕"

Agent 会自动：
1. 转录视频
2. 使用 `social_clip` 策略生成 EDL
3. 渲染每个片段
4. 横转竖裁切 + 字幕
5. 自检每个输出

## 环境要求

- **必须**: FFmpeg (`ffmpeg` / `ffprobe`)
- **转录**: openai-whisper 或 faster-whisper（`pip install openai-whisper`）
- **中文增强**: FunClip / funasr（`pip install funasr funclip`，可选）
- **说话人分离**: pyannote-audio（`pip install pyannote.audio`，可选，需 HuggingFace token）
- **Python 3.9+**

```bash
# 最小安装
pip install openai-whisper pyyaml

# 推荐安装 (全功能)
pip install openai-whisper faster-whisper pyyaml

# 中文增强
pip install funasr funclip

# 说话人分离 (可选)
pip install pyannote.audio
```

## 技术架构

### 双通道感知（借鉴 video-use）

```
Layer 1 — 结构化转译文本 (always loaded)
  词级时间戳 + 说话人 ID + confidence
  ~12KB per source → LLM 主要阅读窗口

Layer 2 — 按需视觉采样 (on demand)
  仅在决策点采样：模糊停顿、复拍对比、切点健康检查
  避免暴力逐帧 (30,000 frames → 45M tokens)
```

### EDL 标准化 (借鉴 video-use)

EDL (Edit Decision List) 将编辑决策与渲染执行隔离:
- **可审计**: 每次编辑有 start/end/reason/confidence
- **可回溯**: 保存 edl.json，下次可重放
- **可干预**: 用户审核后修改再渲染

Schema: `templates/edl_schema.json`

### 自检循环 (借鉴 video-use)

渲染后自动检查质量，发现问题自动修复（max 3 轮）。

## 模板目录

| 文件 | 说明 |
|------|------|
| `templates/edl_schema.json` | EDL 标准 Schema 定义 |
| `templates/clip_strategies.yaml` | 6 种预置剪辑策略 + 决策规则 |
| `templates/subtitle_styles.json` | 6 种字幕风格预设 |
| `references/ffmpeg_cheatsheet.md` | FFmpeg 常用命令速查 |

## 与 video-use 的对比改进

| 维度 | video-use | 本 Skill |
|------|-----------|---------|
| ASR | ElevenLabs 付费 API | 本地 Whisper + FunClip 免费 |
| 平台绑定 | Claude Code 专属 | WorkBuddy 通用 |
| 中文支持 | 基础 | 深度优化 (FunClip + 中文策略) |
| 自检 | 内置 | 独立可配置 |
| 多平台导出 | 无 | 9:16/16:9/1:1 |
| 策略模板 | 无 | 6 种预置 + 自定义 |
| EDL Schema | 无标准 | JSON Schema 定义 |
