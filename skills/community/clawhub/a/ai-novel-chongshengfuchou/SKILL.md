---
name: novel-video-pipeline
description: >
  全自动"重生爽文"短视频流水线。给定题材，依次完成：
  AI生成小说 → TTS语音合成 → FFmpeg竖屏视频合成。
  触发关键词：生成爽文、生成小说视频、重生爽文流水线、
  novel pipeline、tts 合成视频、爽文视频。
---

# 重生爽文全自动流水线 SKILL

## 概述

本 SKILL 封装三条独立流水线，可单独调用，也可顺序串联：

| 步骤 | 函数入口 | 输入 | 输出 |
|------|----------|------|------|
| 1. 生成小说 | `run_novel(theme, cfg)` | 题材字符串 | `output.txt` |
| 2. 生成语音 | `run_audio(cfg)` | `output.txt` | `audio/*.mp3` |
| 3. 生成视频 | `run_video(cfg)` | `audio/` + `video/` + `bgm.mp3` | `output.mp4` |

---

## 目录结构要求

```
工作目录/
├── pipeline.py        # 本 SKILL 的执行脚本
├── video/             # 竖屏或横屏 .mp4 素材（至少 1 个）
├── bgm.mp3            # 背景音乐
├── output.txt         # 步骤1生成，步骤2读取（自动创建）
├── audio/             # 步骤2生成，步骤3读取（自动创建/清空）
└── output.mp4         # 最终输出（自动创建）
```

---

## 素材准备（首次使用必读）

步骤3（生成视频）需要用户自行准备以下两个素材，**缺失时脚本会打印详细提示并终止**，不会静默失败。

### video/ — 视频背景素材

- 在脚本同级目录新建 `video/` 文件夹
- 放入至少 **1 个 `.mp4` 文件**（多个会随机拼接）
- 推荐使用**竖屏（9:16）无版权**背景视频，横屏也可自动居中裁剪成 1080×1920
- 免费素材推荐：
  - [Pexels Videos](https://www.pexels.com/videos/) — 搜索 "nature loop" / "abstract"
  - [Pixabay](https://pixabay.com/videos/) — 完全免版税

### bgm.mp3 — 背景音乐

- 将背景音乐文件**重命名为 `bgm.mp3`**，放在脚本同级目录
- 建议时长 **> 3 分钟**（脚本会循环播放，太短会有卡顿感）
- 默认混音：bgm 音量 `0.08`，人声音量 `1.8`（可通过 cfg 或 CLI 参数调整）
- 免费素材推荐：
  - [Free Music Archive](https://freemusicarchive.org/)
  - [YouTube 音频库](https://www.youtube.com/audiolibrary)（需登录）

### FFmpeg

系统需安装 FFmpeg（含 ffprobe），缺失时脚本会打印安装指引：

```bash
# macOS
brew install ffmpeg
# Ubuntu / Debian
sudo apt install ffmpeg
# Windows：下载后将 bin/ 加入系统 PATH
# https://ffmpeg.org/download.html
```

---



## 配置说明（cfg 字典）

```python
cfg = {
    # ── LLM ──────────────────────────────────
    "api_key":   "YOUR_OPENAI_COMPATIBLE_API_KEY",
    "base_url":  "https://api.example.com/v1",   # OpenAI 兼容端点
    "model":     "gpt-4o",

    # ── Prompt（可选，有内置默认值）──────────
    "premise_prompt": "...",   # 脑洞生成 system prompt
    "story_prompt":   "...",   # 正文写作 system prompt

    # ── TTS ──────────────────────────────────
    "tts_delay":  10,          # 每段请求间隔秒数，防限流

    # ── 视频合成 ─────────────────────────────
    "bgm_vol":    0.08,        # 背景音乐音量（建议 0.05~0.15）
    "voice_vol":  1.8,         # 朗读人声音量（建议 1.5~2.5）
}
```

---

## 调用方式

### 方式一：直接命令行

```bash
# 全流程（题材随机）
python pipeline.py --all

# 指定题材
python pipeline.py --all --theme 末日

# 单步执行
python pipeline.py --novel --theme 职场
python pipeline.py --audio
python pipeline.py --video
```

环境变量传入 API 信息（推荐）：

```bash
export OPENAI_API_KEY="sk-xxx"
export OPENAI_BASE_URL="https://api.example.com/v1"
export OPENAI_MODEL="gpt-4o"
python pipeline.py --all --theme 修仙
```

### 方式二：Python 代码调用

```python
from pipeline import run_novel, run_audio, run_video

cfg = {
    "api_key":  "sk-xxx",
    "base_url": "https://api.example.com/v1",
    "model":    "gpt-4o",
}

# 顺序执行全流程
run_novel("末日", cfg)
run_audio(cfg)
run_video(cfg)
```

---

## AI 使用本 SKILL 的指令

当用户请求生成爽文视频时，Claude 应：

1. **读取本 SKILL.md**，了解参数结构
2. **询问或推断**以下信息：
   - 题材（theme）：用户指定或随机
   - API 配置：优先读环境变量 `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `OPENAI_MODEL`
3. **调用** `bash_tool` 执行：
   ```bash
   python pipeline.py --all --theme <题材>
   ```
4. **实时输出**日志，三步完成后告知用户 `output.mp4` 已生成

### 常见用户指令映射

| 用户说 | Claude 执行 |
|--------|-------------|
| "帮我生成一个末日题材的爽文视频" | `--all --theme 末日` |
| "只生成小说，题材职场" | `--novel --theme 职场` |
| "小说已经有了，帮我转语音" | `--audio` |
| "音频有了，合成视频" | `--video` |
| "重新生成视频，背景音乐小一点" | 修改 `BGM_VOL` 环境变量后 `--video` |

---

## 输出格式说明

- `output.txt` 结构：
  ```
  【AI生成的绝妙脑洞】
  <一句话核心设定>

  【爽文正文】
  <连贯正文，无标题无分章>
  ```
- `output.mp4`：竖屏 **1080×1920**（9:16），适配抖音/视频号/小红书
