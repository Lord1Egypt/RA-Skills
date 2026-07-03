---
name: ai-short-video-factory
display_name: "AI 短视频工厂"
version: "1.2.0"
category: "video"
platforms: ["macOS", "Linux"]
tags: ["AI短视频工厂", "视频制作", "HTML视频", "GSAP动画", "短视频", "AI视频", "HyperFrames", "数据可视化", "产品发布", "科技资讯"]
author: "raelzhang"
agent_created: true
description: "AI Short Video Factory creates MP4 videos from HTML using HyperFrames. Use for captioned talking-head edits, product launches, data visualizations, code walkthroughs, social clips, GSAP animations, transitions, audio muxing, and deterministic rendering."
description_zh: "AI 短视频工厂是一个基于 HyperFrames 的 AI 视频生成 Skill，可将文字创意、结构化脚本或内容大纲自动转化为 HTML + CSS + GSAP 动画视频，并渲染为 MP4。支持产品发布、科技资讯、数据可视化、代码讲解、口播字幕等多种视频类型。AI 全流程自动化：项目初始化 → HTML 编写 → 动画编排 → 渲染交付。内置布局自检、中文适配、音频合成等完整管线。"
---

# AI 短视频工厂｜HTML-to-Video Studio

## 概述

AI 短视频工厂是一个基于 HyperFrames 的 AI 视频生成 Skill，可将文字创意、结构化脚本或内容大纲自动转化为 HTML + CSS + GSAP 动画视频，并通过 Headless Chrome + FFmpeg 确定性渲染为 MP4。无需 React，无按次收费，专为 AI Agent 设计。

**核心能力：**
- 🎬 从文字描述一键生成完整视频（15s ~ 3min）
- 🎨 完全自定义：布局、配色、动画、字体均由 HTML/CSS 控制
- 🔄 AI 全流程自动化：初始化 → 编写 → 动画 → 渲染 → 交付
- 🎵 支持字幕同步、原片音频保留、按需 BGM 合成与音量调校
- ✅ 自检管线确保视觉完整性和技术正确性

## 快速开始

**一句话生成视频：**
> "帮我做一个 30 秒的科技资讯短视频，主题是 AI 编程工具的发展趋势"

AI 会自动完成全流程：
1. 初始化项目 → `npx hyperframes init`
2. 编写 HTML 视频内容（场景规划 + 动画编排）
3. 渲染为 MP4 → `npx hyperframes render`
4. 按需处理音频 → 保留原片音频，或在用户要求时 FFmpeg 后置混音
5. 执行自检管线 → 确保质量达标后交付

**最小示例：**
```bash
# 创建项目
npx hyperframes init my-video --non-interactive
# 编辑 index.html（AI 自动生成内容）
# 渲染
npx hyperframes render --non-interactive
```

## 适用场景

| 视频类型 | 典型时长 | 示例 |
|----------|---------|------|
| 科技资讯 / 行业速报 | 30-60s | AI 编程工具趋势、技术周报 |
| 产品发布 / 功能介绍 | 15-45s | 新功能 demo、产品亮点 |
| 数据可视化 | 20-40s | 市场规模、增长趋势、对比分析 |
| 教程 / 代码讲解 | 30-120s | 技术方案讲解、代码 walkthrough |
| 社交媒体短视频 | 15-30s | 抖音/小红书风格竖版视频 |
| 口播 + 字幕 | 任意 | 带背景去除、字幕同步的 talking-head |
| 品牌宣传 / 活动预热 | 15-45s | 会议宣传、品牌介绍 |

---

## Overview (English)

HyperFrames is an open-source (Apache 2.0) HTML-native video rendering framework by HeyGen. Write video as HTML + CSS + seekable animations, then render deterministically to MP4 via headless Chrome + FFmpeg. No React required, no per-render fees, designed for AI agents.

## Prerequisites Check & Installation

Before any operation, run the environment diagnostic:

```bash
npx hyperframes doctor
```

This reports all dependencies and their status. **If any check fails, STOP and resolve before proceeding.**

### Required Tools (ALL mandatory)

| Tool | Minimum version | Purpose | Install command |
|------|----------------|---------|----------------|
| **Node.js** | 22+ | HyperFrames CLI runtime | WorkBuddy 自动管理；或 `nvm install 22` / 官网安装 |
| **FFmpeg** | 5.0+ | Video encoding, audio muxing, frame extraction | macOS: `brew install ffmpeg`; Linux: `apt install ffmpeg` |
| **FFprobe** | (bundled with FFmpeg) | Media inspection, duration/format checks | Installed with FFmpeg |
| **Chrome Headless Shell** | Auto-managed | Frame-by-frame rendering engine | `npx hyperframes browser ensure` (auto-downloads) |
| **HyperFrames CLI** | 0.6.90+ | Composition management & rendering | `npx hyperframes@latest` (auto via npx) |

### Optional Tools (for advanced workflows)

| Tool | Purpose | Install command |
|------|---------|----------------|
| **Docker** | Containerized rendering (CI/CD, remote) | `brew install --cask docker` / Docker Desktop |
| **Python 3.9+** | Optional audio analysis / BGM synthesis helpers | WorkBuddy 自动管理；或系统 Python 3.9+ |

### First-Time Setup Sequence

For a brand new environment, execute these steps in order:

```bash
# 1. Verify Node.js (should be pre-installed by WorkBuddy)
node --version  # must be >= 22.0.0

# 2. Install FFmpeg if missing
which ffmpeg || brew install ffmpeg
ffmpeg -version  # confirm installation

# 3. Download Chrome Headless Shell (auto-cached at ~/.cache/hyperframes/chrome/)
npx hyperframes browser ensure

# 4. Run full diagnostic — all checks must pass
npx hyperframes doctor
```

### Troubleshooting Common Setup Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `doctor` shows ✗ FFmpeg | FFmpeg not installed | `brew install ffmpeg` |
| `doctor` shows ✗ Chrome | First run, no cached browser | `npx hyperframes browser ensure` |
| Render hangs indefinitely | Chrome sandbox conflict in WorkBuddy | Use `dangerouslyDisableSandbox: true` on Bash tool |
| `EACCES` permission error | npx cache permission issue | `sudo chown -R $(whoami) ~/.npm` |
| Render produces 0-byte MP4 | FFmpeg encoder issue | Check `ffmpeg -encoders` has `libx264` and `aac` |
| `npx hyperframes` not found | Node/npx not in PATH | 确保 Node.js 22+ 在 PATH 中；WorkBuddy 环境下使用托管 Node |

### Pre-Flight Check (AI Must Execute Before Every Project)

```bash
# Quick 3-command pre-flight (run at start of every video task)
npx hyperframes doctor          # full diagnostic
which ffmpeg && ffmpeg -version  # confirm FFmpeg accessible
echo "Pre-flight OK"
```

If `doctor` reports any failure, resolve it BEFORE writing any HTML. Do NOT proceed with a broken environment — it will waste render time and produce invalid output.

## Workflow Decision Tree

1. **从零生成视频** → Step 1 (Init) → Step 2 (Compose) → Step 3 (Animate) → Step 4 (Lint) → Step 5 (Render)
2. **口播后期加工（加字幕/特效/换背景）** → 详见「口播后期处理管线」章节完整流程
3. **已有口播 + 去背景 + 换场景** → Remove background → Write composition with layers → Add captions → Add music → Render
4. **修改已有 composition** → Read files → Modify → Lint → Render
5. **数据可视化视频** → Plan data scenes → Compose with animated charts → Render
6. **多段素材拼接** → FFmpeg concat → HyperFrames 加统一字幕/特效/转场 → Render

## Step 1: Initialize Project

```bash
npx hyperframes init <project-name> --non-interactive
npx hyperframes init my-video --example blank
npx hyperframes init my-video --video clip.mp4        # with existing video
npx hyperframes init my-video --audio track.mp3       # with audio
npx hyperframes init my-video --tailwind              # Tailwind v4 support
```

Available templates: `blank`, `warm-grain`, `play-mode`, `swiss-grid`, `vignelli`, `decision-tree`, `kinetic-type`, `product-promo`, `nyt-graph`

## CRITICAL: Rendering Requirements

These rules are MANDATORY — violating them causes the compile phase to hang indefinitely:

1. **GSAP: Keep CDN URL** — Always use `<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>`. The Compiler automatically inlines CDN scripts. **NEVER use a local `lib/gsap.min.js`** — file serving breaks during render.
2. **Fonts: DO NOT use @import** — Never write `@import url('https://fonts.googleapis.com/...')`. Instead, just declare `font-family: "Inter", sans-serif` in CSS. The Compiler auto-resolves common Google Fonts and caches them to `~/.cache/hyperframes/fonts/`. Supported fonts include: Inter, JetBrains Mono, Roboto, etc. **Noto Sans SC is NOT auto-resolved** — avoid it.
3. **WorkBuddy sandbox** — `npx hyperframes render` requires `dangerouslyDisableSandbox: true` because it launches Headless Chrome (Puppeteer).
4. **Always use `--non-interactive`** — Required for WorkBuddy automation.

## CRITICAL: Prompt Priority & Creative Freedom Protocol

### Priority Rule (MOST IMPORTANT — Governs Everything Below)

```
用户提示词的明确意图 > 硬约束（技术安全）> 软默认（参考建议）
```

**Two modes of operation:**

| 提示词类型 | AI 行为 |
|-----------|--------|
| **详细提示词**（明确指定布局、配色、风格、动画等） | 严格按提示词执行，只保留硬约束，软默认全部让位。AI 的任务是实现用户的视觉创意，不是把视频拉回模板。 |
| **简单提示词**（只给主题/关键词，未指定视觉细节） | AI 自由发挥创意，参考软默认值作为起点，鼓励创新布局和视觉表达。 |

**Creative License（创意许可）：** 当用户的提示词包含具体的视觉描述、风格要求、布局指示、动效要求时，视为创意许可——AI 应优先实现用户的视觉意图，所有软默认规则自动退让。AI 不应将每个视频拉回同一个标准模板。

**无论哪种模式，AI 必须在最终输出前执行 §9 AI自检管线，确保技术安全。**

---

### Rule Classification: Hard Constraints vs Soft Defaults

#### 🔴 硬约束（HARD CONSTRAINTS — 永远生效，即使用户提示词冲突也不可违反）

这些是技术限制，违反会导致渲染崩溃、输出错误或不可预期行为：

| # | 硬约束 | 原因 |
|---|--------|------|
| H1 | 禁止 `Math.random()`/`Date.now()`/`new Date()`/`performance.now()` | 非确定性渲染导致帧不一致 |
| H2 | 字体仅限白名单: Inter, JetBrains Mono, Roboto, sans-serif | 其他字体 lint 报错或渲染失败 |
| H3 | 禁止 `@import url()` 引入字体 | Compiler 不支持，渲染卡死 |
| H4 | GSAP CDN 必须使用 jsdelivr URL | 本地文件路径在渲染环境中不可用 |
| H5 | `window.__timelines` 必须同步注册 | 异步注册导致空帧 |
| H6 | 内容不可超出画布边界（任何像素） | 超出部分被裁切，用户看到残缺内容 |
| H7 | 禁止 inline `style="top:XX%"` 覆盖内容定位 | 百分比定位跨场景不一致，导致溢出 |
| H8 | GSAP repeat 使用 `Math.floor` 而非 `Math.ceil` | ceil 可能超出 composition 时长 |
| H9 | 音频必须 FFmpeg 后置合成（≥30s视频） | HyperFrames 内置音频 ~32s 截断 bug |

#### 🟢 软默认（SOFT DEFAULTS — 仅当用户提示词未指定时生效，一旦用户有明确意图即让位）

这些是经过验证的良好实践，但不是唯一正确答案：

| # | 软默认 | 默认值 | 用户可覆盖场景 |
|---|--------|--------|--------------|
| S1 | 标题区位置 | top: 50px | 用户要全屏标题、底部标题等 |
| S2 | 内容起始位置 | top: 240px | 用户要居中布局、沉浸式设计等 |
| S3 | 卡片间距 | 28-36px | 用户要紧凑/宽松排版 |
| S4 | 内容底部边界 | 980px | 用户明确要底部内容 |
| S5 | 左右安全边距 | 120px | 用户要全出血设计 |
| S6 | 字号范围 | 见参考表 | 用户指定特定字号风格 |
| S7 | 卡片宽度 | 320-520px | 用户要大卡片/小卡片 |
| S8 | 场景过渡方式 | 0.6s opacity fade | 用户指定滑动/缩放/3D等过渡 |
| S9 | 背景风格 | 暗色渐变 + 网格 + 模糊光球 | 用户指定任何其他背景 |
| S10 | 粒子数量 | 40 个, mulberry32 seed=42 | 用户不要粒子或要更多 |
| S11 | 骨架结构 | scene-wrapper 标准骨架 | 用户描述了不同的布局需求 |
| S12 | 配色方案 | 无预设（等用户指定）| 用户未指定时用中性深色/浅色 |

---

### 1. Prompt Compliance Checklist

Before writing HTML, create a compact production checklist with:
- Topic/title and target audience
- Required scenes or content points
- Required visual style and forbidden styles
- **Required color palette — ALWAYS follow the user's prompt specification; never substitute or override**
- Required BGM style, whether it must cover the whole video, and target volume
- Duration target and final scene end time
- Any requested font/card/icon scale preferences
- **Creative direction signal**: 用户是否给了详细视觉指示？(YES → 严格执行，软默认让位; NO → AI自由发挥，参考软默认)

After rendering, check the output against this list. If the user asked for a specific BGM style, do not replace it with a different style unless explicitly approved. If the user specified a color palette, do not swap it for a "safer" or "more generic" scheme.

### 2. Color Palette Rule

**User's prompt is the ONLY source of truth for color decisions.** The Skill provides NO default theme colors. When the user provides a color scheme (e.g., "霓虹青绿玫红橙紫"), implement it exactly. When the prompt omits color requirements, AI may freely choose a palette that best serves the content and mood — no need to ask unless the user is unsatisfied.

### 3. Safe Typography Scale for 1920x1080 (Soft Default — 参考范围)

These are **reference ranges** for when the user hasn't specified typography preferences. If the user describes a specific visual style (e.g., "极简大字报风格", "数据密集仪表盘"), AI should adapt freely while ensuring readability.

| Element | Reference range | Hard max (H6: 不可超出画布) |
|---------|----------------|---------------------------|
| Cover mega title | 96-120px | 132px |
| Scene title | 64-84px | 92px |
| Subtitle | 38-56px | 64px |
| Body text | 28-42px | 48px |
| Card title | 32-44px | 48px |
| Data number | 72-104px | 112px |
| Icon/emoji | 56-96px | 112px |
| Code text | 26-36px | 42px |

**Note:** Hard max 仅为防溢出，不是风格限制。如果用户明确要超大标题效果且布局容得下，AI 应实现。

### 4. Layout Safe Zones (Soft Default — 标准布局参考)

以下是 1920x1080 的**标准布局参考**。当用户提示词未指定布局时使用；当用户描述了不同的布局需求（如全屏沉浸式、非规则排列、斜切设计、居中对称等），AI 应自由设计，仅确保不违反硬约束 H6（内容不超出画布）和 H7（禁止 inline top%）。

```
┌──────────────────────────────────────────────┐
│ Title Safe Zone: top 50px, height ≤ 150px    │ ← 标准参考
├──────────────────────────────────────────────┤
│ Content Safe Zone: top 240px ~ bottom 980px  │ ← 标准参考
├──────────────────────────────────────────────┤
│ Bottom Safe Margin: bottom 100px             │ ← 建议保留
└──────────────────────────────────────────────┘
```

**硬约束（始终生效）：**
- H6: 所有可见内容必须在 0~1920px (水平) 和 0~1080px (垂直) 范围内
- H7: 禁止 inline `style="top:XX%"` — 必须使用 CSS class 或固定 px 值

**软默认（未指定时使用）：**
- 标题区: `top: 50px`, 居中, height ≤ 150px
- 内容区: `top: 240px`, 底部不超过 980px
- 左右边距: ≥ 120px
- 标题与内容间距: ≥ 40px

**Content height budget (标准布局下的参考计算):**
```text
available_height = 980px - 240px = 740px
max_card_height = (available_height - (rows-1) × gap) / rows

Example: 3 rows, gap=24px → max per row = (740 - 48) / 3 = 230px ✓
Example: 6 cards 2×3, gap=28px → max per row = (740 - 28) / 2 = 356px ✓
Example: 4 vertical items, gap=18px → max per item = (740 - 54) / 4 = 171px ✓
```

**If content_height > available_height (overflow risk), apply fixes:**
1. Reduce card padding (28px → 20px)
2. Reduce gap (36px → 24px → 18px)
3. Reduce icon/text size within cards
4. Split into two consecutive scenes

**Card layout dimension reference (soft defaults):**

| Layout type | Card width | Max gap | Container width |
|-------------|-----------|---------|-----------------|
| 3 horizontal | 360-480px | 36px | 90% (1728px) |
| 4 horizontal | 280-380px | 30px | 90% |
| 2×3 grid | 320-520px | 28px | 1600px |
| 2 large horizontal | 680-780px | 36px | 90% |
| Vertical list (3-4 items) | 90% width | 20-24px | 90% |
| Timeline (3 items) | 90% width | 20px | 90% |

### 5. Font White List — HARD CONSTRAINT (H2)

Only use fonts that HyperFrames Compiler can auto-resolve:

```css
/* ALLOWED */
font-family: "Inter", sans-serif;
font-family: "JetBrains Mono", monospace;  /* for code blocks */
font-family: "Roboto", sans-serif;

/* PROHIBITED — cause lint errors or render failures */
font-family: "PingFang SC";        /* macOS only, not bundled */
font-family: "Microsoft YaHei";    /* Windows only */
font-family: "Noto Sans SC";       /* not auto-resolved */
font-family: "Source Han Sans";    /* not auto-resolved */
```

Chinese text rendering: rely on `sans-serif` fallback (renders correctly in Chrome). The visual difference is negligible for video output.

### 6. Deterministic Rendering — HARD CONSTRAINT (H1, H8)

HyperFrames requires frame-level determinism for multi-pass rendering:

```javascript
// ❌ PROHIBITED — non-deterministic (H1)
Math.random()
Date.now()
new Date()
performance.now()  // for positioning

// ✅ REQUIRED — use seeded PRNG
function mulberry32(seed) {
  return function() {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  }
}
const rand = mulberry32(42);  // fixed seed
```

Also for GSAP `repeat` calculations (H8):
```javascript
// ❌ May overshoot composition duration
repeat: Math.ceil(duration / cycle) - 1

// ✅ Guaranteed to stay within bounds
repeat: Math.floor(duration / cycle) - 1
```

### 7. Scene Duration and Root Duration

The root composition duration must equal the last scene end time:

```text
root_duration = max(scene.data_start + scene.data_duration)
```

Never leave `data-duration` shorter than the final scene. This causes unreliable render behavior and confusing QA results.

### 8. BGM Must Match Prompt and Cover Full Video

For videos longer than 30s, do not rely on short audio loops inside HyperFrames. Use this reliable workflow:

1. Generate or prepare a full-length WAV whose duration is at least `root_duration + 3s`.
2. Render the visual video with HyperFrames (audio `data-duration` can match video, but DO NOT trust the rendered audio).
3. Replace/mux final audio with FFmpeg from the WAV source:

```bash
ffmpeg -y -i rendered.mp4 -i bgm_full.wav -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 192k -t <root_duration+0.02> \
  -movflags +faststart final.mp4
```

4. Verify the final MP4 by extracting the audio stream and checking real decoded duration and per-second RMS:

```bash
ffmpeg -y -i final.mp4 -vn -ac 1 -ar 44100 extracted_audio.wav
ffprobe -v quiet -show_entries format=duration -show_entries stream=codec_type,duration -of default=noprint_wrappers=1 final.mp4
ffmpeg -ss <root_duration-12> -t 12 -i final.mp4 -af volumedetect -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume"
```

Bundled helper option:

```bash
python scripts/verify_audio.py final.mp4 --min-duration <root_duration> --tail-seconds 12
```

A successful BGM check must prove:
- Extracted audio duration >= video duration - 0.1s
- No silent seconds in the final 12 seconds (RMS > -30dB per second)
- The BGM style matches the user's requested or previously approved style
- Volume is audible but not overpowering (RMS mean between -15dB ~ -20dB)

**BGM generation fallback:** Only generate BGM when the user explicitly requests new music or when the source material has no audio to preserve. If numpy is unavailable, use Python standard library `struct` + `wave` + `math` to synthesize. A 130BPM electronic track can include: kick (4-on-floor), hi-hat (8th notes), bass (sub oscillator), pad (chord progression), lead melody, and arpeggio layers. For existing edited videos with original audio, preserve and post-mux the original audio instead of synthesizing replacement music.

Bundled helper option for generated BGM projects:

```bash
python scripts/gen_bgm.py bgm.wav --duration <root_duration+3> --bpm 110 --volume 0.25
```

### 9. AI Self-Check Pipeline (Mandatory Before Delivery — 两种模式通用)

**无论用户提示词是详细还是简单，最终交付前都必须执行此管线。** 此管线验证的是**技术安全和视觉完整性**，不是风格是否符合某个模板。

Execute ALL checks in this exact order. Do NOT skip any step.

#### Phase A: Pre-Write Validation (before writing HTML)

| # | Check | 详细提示词模式 | 简单提示词模式 |
|---|-------|---------------|---------------|
| A1 | Scene count × avg duration = total duration? | 按提示词场景规划 | AI 自行规划 |
| A2 | Content density reasonable for scene duration? | 按提示词内容量 | 参考中文密度表 |
| A3 | Colors match user specification? | 严格匹配提示词配色 | AI 自由选择 |
| A4 | Font family only uses whitelist? (H2) | **始终检查** | **始终检查** |
| A5 | 是否存在 Hard Constraint 冲突? | **始终检查** | **始终检查** |

#### Phase B: Post-Write / Pre-Render Validation

```bash
# B1: Lint must pass with 0 errors (HARD — always)
npx hyperframes lint

# B2: Check for prohibited patterns in HTML (HARD — H1, H2)
grep -n "Math.random\|Date.now\|PingFang\|Microsoft YaHei\|Noto Sans" index.html
# → must return empty

# B3: Check for inline top% overrides (HARD — H7)
grep -n 'style=.*top:.*%' index.html
# → If found: REMOVE immediately (use CSS class or fixed px)

# B4: Check root data-duration matches expected
grep 'data-composition-id.*data-duration\|data-start.*data-duration' index.html
# → Verify last scene end = root duration
```

#### Phase C: Post-Render Validation

| # | Check | Command | Pass criteria |
|---|-------|---------|---------------|
| C1 | Video duration | `ffprobe -show_format` | ≥ target - 0.1s |
| C2 | Resolution | `ffprobe -show_streams` | 匹配用户要求的分辨率 |
| C3 | Frame rate | `ffprobe -show_streams` | 30fps (除非用户要求 60fps) |
| C4 | Audio duration after mux | Extract WAV, check length | ≥ video duration |
| C5 | Last 12s no silence | Per-second RMS check | All seconds > -30dB |
| C6 | Audio mean volume | `volumedetect` | -15dB ~ -20dB |

#### Phase D: Layout & Visual Integrity Check (关键步骤)

For **every video**, extract key frames and verify visual integrity:

```bash
# Extract key frames at scene midpoints
ffmpeg -ss <mid_time> -i final.mp4 -frames:v 1 -q:v 2 check_scene_N.jpg
```

**通用视觉检查（两种模式都执行）：**
- ✅ 所有文字和内容在画布范围内（H6）— 无裁切
- ✅ 无文字互相重叠导致不可读
- ✅ 卡片/元素间距均匀，无挤压变形
- ✅ 关键信息可读（字号足够，对比度足够）
- ✅ 动画过渡流畅，无跳切（除非用户要求跳切风格）

**额外检查（仅标准布局模式——使用软默认时）：**
- 标题在顶部可见，不与内容重叠
- 所有卡片在安全区范围内

If ANY check in Phases B-D fails → fix → re-render → re-verify. Maximum 2 retry cycles; if still failing after 2 retries, report the specific issue to the user.

### 10. Auto-Completion Defaults (Soft — 仅简单提示词模式)

当用户的提示词**未指定**以下细节时，AI 可参考这些经过验证的默认值作为**起点**，但鼓励在此基础上发挥创意：

| Missing item | Default reference | AI 可自由替换？ |
|-------------|------------------|----------------|
| Layout strategy | Title top:50px + Content top:240px | ✅ 可用任何不违反 H6/H7 的布局 |
| Font | `Inter, sans-serif` | ❌ 硬约束 H2，只能用白名单字体 |
| Audio strategy | FFmpeg post-mux from full-length WAV | ❌ 硬约束 H9（≥30s 视频） |
| Content container | `.content-area` / `.content-col` | ✅ 可用任何语义化 CSS 结构 |
| Card gap | 28-36px (horizontal), 20-24px (vertical) | ✅ |
| Particle generation | 40 particles, mulberry32 seed=42 | ✅ 数量自由，但 PRNG 必须用 mulberry32 (H1) |
| Background | Dark gradient + grid + blur orb | ✅ 完全自由 |
| Transition style | 0.6s opacity fade | ✅ 可用滑动、缩放、模糊等 |
| Grid background animation | 20s infinite translate loop | ✅ |
| Verification pipeline | Full Phase A-D self-check | ❌ 始终必须执行 |

**Key principle:** 默认值是灵感参考，不是束缚。AI 应根据视频主题和内容自然选择最佳表达方式。

### 11. Common Pitfalls Registry (Quick Reference)

| Pitfall | Root cause | Type | Prevention |
|---------|-----------|------|------------|
| Content overflows bottom | `top:XX%` inline style | 🔴 H7 | 禁止 inline top%，用 CSS class 固定 px |
| Audio cuts at ~32s | HyperFrames built-in audio bug | 🔴 H9 | Always FFmpeg post-mux |
| Non-deterministic frames | `Math.random()` | 🔴 H1 | Replace with mulberry32 PRNG |
| Lint error: unresolved font | Using PingFang SC etc. | 🔴 H2 | Font whitelist only |
| GSAP overruns composition | `Math.ceil` for repeat count | 🔴 H8 | Use `Math.floor` instead |
| Empty/black frames | `window.__timelines` not registered | 🔴 H5 | Ensure synchronous registration |
| Cards overlap title | `transform:translate(-50%,-50%)` centering | ⚠️ 自检 | Phase D frame spot-check 发现即修 |
| 2×3 grid uneven spacing | Card width too small for container | ⚠️ 自检 | Phase D 视觉检查 |
| Scene jump cuts | Missing exit transitions | ⚠️ 自检 | 除非用户要求跳切风格 |

## Step 2: Write HTML Composition

A composition is an HTML file. The root container defines the video canvas.

### Simple Single-Scene Example

```html
<!doctype html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
</head>
<body>
  <div data-composition-id="main" data-start="0" data-width="1920" data-height="1080">

    <!-- Video clip: track 0, starts at 0s, plays for 10s -->
    <video id="bg-video" data-start="0" data-duration="10" data-track-index="0"
           src="background.mp4" muted playsinline></video>

    <!-- Title overlay: track 1, appears at 1s for 4s -->
    <h1 id="title" class="clip" data-start="1" data-duration="4" data-track-index="1">
      Product Launch
    </h1>

    <!-- Audio: track 2, from 0s for 10s, volume 50% -->
    <audio data-start="0" data-duration="10" data-track-index="2"
           data-volume="0.5" src="music.wav"></audio>
  </div>

  <style>
    body { margin: 0; overflow: hidden; }
    [data-composition-id="main"] {
      width: 1920px; height: 1080px;
      position: relative; background: #000;
    }
    #title {
      position: absolute; top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      font-size: 96px; color: white; font-family: sans-serif;
    }
  </style>

  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#title", { opacity: 0, y: 60, duration: 0.8, ease: "power3.out" }, 1);
    tl.to("#title", { opacity: 0, y: -40, duration: 0.5, ease: "power2.in" }, 4);
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
```

### Multi-Scene Standard Skeleton (Soft Default — Reference Starting Point)

For videos with 3+ scenes when the user hasn't specified a custom layout, this skeleton provides a proven starting point. **If the user's prompt describes a different visual structure (e.g., full-screen transitions, split-screen, non-linear navigation, cinematic parallax), AI should design freely — only the Hard Constraints (H1-H9) remain in effect.**

```html
<!doctype html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
</head>
<body>
<div data-composition-id="main" data-start="0" data-duration="TOTAL_SECONDS"
     data-width="1920" data-height="1080">

  <!-- ===== BACKGROUND LAYER (persists entire video) ===== -->
  <div id="bg-layer" style="position:absolute;inset:0;z-index:0;">
    <!-- Grid background, particles, orbs — shared across scenes -->
    <div id="grid-bg"></div>
    <div id="particles-container"></div>
  </div>

  <!-- ===== SCENE 1: Opening ===== -->
  <div id="scene-1" class="scene-wrapper" data-start="0" data-duration="4" data-track-index="1">
    <div class="scene-title" id="s1-title">
      <!-- Main title content -->
    </div>
    <div class="content-area" id="s1-content">
      <!-- Scene content: cards, text, data -->
    </div>
  </div>

  <!-- ===== SCENE 2 ===== -->
  <div id="scene-2" class="scene-wrapper" data-start="4" data-duration="4" data-track-index="1">
    <div class="scene-title" id="s2-title">
      <h2>场景标题</h2>
      <p class="subtitle">副标题说明</p>
    </div>
    <div class="content-area" id="s2-cards">
      <!-- Horizontal card layout -->
    </div>
  </div>

  <!-- ===== SCENE N: (repeat pattern) ===== -->
  <!-- ... -->

  <!-- ===== AUDIO ===== -->
  <audio data-start="0" data-duration="TOTAL_SECONDS" data-track-index="2"
         data-volume="0.5" src="bgm.wav"></audio>
</div>

<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { margin: 0; overflow: hidden; background: #0a0a0f; font-family: "Inter", sans-serif; color: #fff; }
  [data-composition-id="main"] { width: 1920px; height: 1080px; position: relative; overflow: hidden; }

  /* ===== SCENE WRAPPER ===== */
  .scene-wrapper { position: absolute; inset: 0; opacity: 0; }

  /* ===== TITLE ZONE: fixed top 50px ===== */
  .scene-title {
    position: absolute;
    top: 50px;
    left: 0;
    width: 100%;
    text-align: center;
    z-index: 10;
  }
  .scene-title h2 { font-size: 76px; font-weight: 700; margin: 0; }
  .scene-title .subtitle { font-size: 38px; opacity: 0.7; margin-top: 8px; }

  /* ===== CONTENT ZONE: fixed top 240px ===== */
  .content-area {
    position: absolute;
    top: 240px;
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 36px;
    flex-wrap: wrap;
  }
  .content-col {
    position: absolute;
    top: 240px;
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
  }

  /* ===== CARD STYLES ===== */
  .glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 28px 24px;
    backdrop-filter: blur(12px);
  }
</style>

<script>
  // ===== Seeded PRNG (mulberry32) =====
  function mulberry32(seed) {
    return function() {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    }
  }
  const rand = mulberry32(42);

  // ===== GSAP Timeline =====
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });
  const TOTAL = TOTAL_SECONDS;

  // --- Scene 1: 0-4s ---
  tl.to("#scene-1", { opacity: 1, duration: 0.01 }, 0);
  tl.from("#s1-title", { scale: 0.5, opacity: 0, duration: 0.8, ease: "back.out(1.4)" }, 0.1);
  tl.from("#s1-content", { y: 40, opacity: 0, duration: 0.6 }, 0.5);
  tl.to("#scene-1", { opacity: 0, duration: 0.5 }, 3.4);  // exit at scene_end - 0.6

  // --- Scene 2: 4-8s ---
  tl.to("#scene-2", { opacity: 1, duration: 0.01 }, 4);
  tl.from("#s2-title", { x: -60, opacity: 0, duration: 0.6, ease: "power2.out" }, 4.1);
  tl.from("#s2-cards .glass-card", { scale: 0.6, opacity: 0, duration: 0.5, stagger: 0.15 }, 4.4);
  tl.to("#scene-2", { opacity: 0, duration: 0.5 }, 7.4);

  // --- Scene N: (repeat pattern) ---
  // ...

  window.__timelines["main"] = tl;
</script>
</body>
</html>
```

**Skeleton naming conventions (recommended for consistency, not mandatory):**
- Scene wrappers: `#scene-1`, `#scene-2`, ... `#scene-N`
- Scene titles: `#s1-title`, `#s2-title`, ... `#sN-title`
- Content containers: `#s1-content`, `#s2-cards`, `#s3-items`, ... (descriptive suffix)
- Card elements: `.glass-card`, `.data-card`, `.app-card` (semantic naming)
- Background: `#bg-layer`, `#grid-bg`, `#particles-container`

**Scene wrapper pattern (recommended, AI may use alternative transition approaches if user requests):**
```javascript
// Scene entry (instant opacity on)
tl.to("#scene-N", { opacity: 1, duration: 0.01 }, SCENE_START);
// Scene content animations
tl.from("#sN-title", { /* entrance */ }, SCENE_START + 0.1);
tl.from("#sN-content ...", { /* entrance */ }, SCENE_START + 0.3);
// Scene exit (0.6s before end) — EXCEPT final scene
tl.to("#scene-N", { opacity: 0, duration: 0.5 }, SCENE_END - 0.6);
```

### Data Attributes Reference

| Attribute | Required | Purpose |
|-----------|----------|---------|
| `data-composition-id` | Yes | Unique ID for the composition |
| `data-start` | Yes | Start time in seconds (or clip ID ref: `"el-1 + 2"`) |
| `data-duration` | Yes for img/div | Duration in seconds (video/audio auto-detect) |
| `data-track-index` | Yes | Track layer (same-track clips cannot overlap) |
| `data-width` / `data-height` | Yes (root) | Canvas dimensions (1920x1080 or 1080x1920) |
| `data-volume` | No | Audio volume 0-1 (default 1) |
| `data-media-start` | No | Trim offset into source media |
| `data-composition-src` | No | Path to external sub-composition HTML |

### Video and Audio Rules

- Video MUST be `muted playsinline` — audio is always a separate `<audio>` element
- Never call `video.play()`/`audio.play()` — the framework owns playback
- Never nest video inside a timed div — use a non-timed wrapper
- **Long BGM warning**: HyperFrames' built-in audio processing may truncate long background music around ~32s even when the source audio and `data-duration` are longer. Always verify the rendered MP4 by extracting its audio stream and checking the decoded audio duration/RMS; `volumedetect -ss 30 -t 12` can be misleading because it only analyzes available samples.
- **Reliable long-BGM workflow**: render the visual video first, then replace/mux the audio with FFmpeg from a full-length WAV source: `ffmpeg -i rendered.mp4 -i bgm_full.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -t <composition_duration> -movflags +faststart final.mp4`. Verify by extracting `final.mp4` audio to WAV and checking per-second RMS through the end.

## Step 3: Animate with GSAP

### Non-Negotiable Rules

1. All timelines MUST start `{ paused: true }` — player controls playback
2. Register every timeline: `window.__timelines["<composition-id>"] = tl`
3. Duration comes from `data-duration`, NOT from GSAP timeline length
4. **No `repeat: -1`** — calculate exact repeats: `repeat: Math.ceil(duration / cycleDuration) - 1`
5. **No `Math.random()`, `Date.now()`** — use seeded PRNG if needed
6. **No async timeline construction** — no `setTimeout`, `await`, Promises
7. Only animate visual properties: `opacity`, `x`, `y`, `scale`, `rotation`, `color`, `backgroundColor`
8. Never animate `visibility`, `display`
9. Offset first animation 0.1–0.3s from t=0

### Scene Transitions (multi-scene compositions)

1. ALWAYS use transitions between scenes — no jump cuts
2. ALWAYS use entrance animations (`gsap.from()`) on every element
3. NEVER use exit animations except on the final scene — the transition IS the exit
4. Final scene only may fade elements out

### Layout Before Animation

Build the end-state first as static CSS, then add motion:
1. Position elements at their **most visible moment**
2. Add entrances with `gsap.from()` — animate FROM offscreen TO CSS position
3. Add exits with `gsap.to()` — only on final scene

## Step 4: Lint & Inspect

```bash
npx hyperframes lint              # Structure/code check (fast)
npx hyperframes lint --json       # Machine-readable
npx hyperframes inspect           # Visual layout check (launches Chrome)
npx hyperframes inspect --json    # Agent-readable findings
```

Fix all errors before rendering. Warnings should be addressed.

## Step 5: Render

```bash
npx hyperframes render                          # Standard MP4
npx hyperframes render --quality draft          # Fast iteration (~3x faster)
npx hyperframes render --quality high --fps 60  # Final delivery
npx hyperframes render --output final.mp4       # Custom filename
npx hyperframes render --format webm            # Transparent WebM
npx hyperframes render --docker                 # Byte-level consistency
```

| Flag | Options | Default | Notes |
|------|---------|---------|-------|
| `--output` | path | `renders/name_timestamp.mp4` | Output path |
| `--fps` | 24, 30, 60 | 30 | 60fps doubles render time |
| `--quality` | draft, standard, high | standard | draft for iteration |
| `--format` | mp4, webm | mp4 | WebM supports transparency |
| `--workers` | 1-8 or auto | auto | Each worker spawns a Chrome |
| `--docker` | flag | off | Reproducible output |
| `--variables` | JSON | — | Override composition variables |

Deliver the rendered MP4 to user via `deliver_attachments`.

## Media Processing

### Text-to-Speech (TTS)

Local inference with Kokoro-82M. No API key needed.

```bash
npx hyperframes tts "Your script here" --voice af_heart --output narration.wav
npx hyperframes tts script.txt --voice bf_emma --output narration.wav
npx hyperframes tts --list                      # List all 54 voices
```

Voice selection:
| Content Type | Voice | Reason |
|-------------|-------|--------|
| Product demo | `af_heart` / `af_nova` | Warm, professional |
| Tutorial | `am_adam` / `bf_emma` | Neutral, easy to follow |
| Marketing | `af_sky` / `am_michael` | Energetic or authoritative |
| Casual/social | `af_heart` / `af_sky` | Friendly, natural |

Chinese voices use `z` prefix: e.g., `zf_xiaobei`, `zm_yunjian`.

Requirements: Python 3.8+, `pip install kokoro-onnx soundfile`. Non-English needs `espeak-ng`.

### Transcription (for captions)

Local Whisper inference. No API key needed.

```bash
npx hyperframes transcribe audio.mp3                      # → transcript.json
npx hyperframes transcribe video.mp4 --model small        # Default model
npx hyperframes transcribe video.mp4 --model medium       # Better accuracy
npx hyperframes transcribe subtitles.srt                  # Import existing
```

Output: `transcript.json` with word-level timestamps:
```json
[{"id": "w0", "text": "Hello", "start": 0.0, "end": 0.5}, ...]
```

**CRITICAL**: Never use `.en` models unless audio is confirmed English. `.en` models TRANSLATE instead of transcribe.

### Background Removal

Local u2net_human_seg model. No API key.

```bash
npx hyperframes remove-background talking-head.mp4 -o transparent.webm
npx hyperframes remove-background subject.mp4 -o subject.webm --background-output plate.webm
npx hyperframes remove-background portrait.jpg -o cutout.png
```

Output formats:
- `.webm` (VP9 + alpha) — for direct use in `<video>` composition
- `.mov` (ProRes 4444) — for editing in external tools
- `.png` — single image cutout

## Common Video Recipes

### Recipe 1: Talking-Head + Captions + Background Music

```bash
# 1. Remove background from talking-head video
npx hyperframes remove-background talking-head.mp4 -o transparent.webm

# 2. Transcribe for captions
npx hyperframes transcribe talking-head.mp4 --model small

# 3. Init project and compose
npx hyperframes init captioned-video --non-interactive
```

Composition structure:
- Track 0: Background (gradient, image, or video)
- Track 1: Transparent talking-head (`transparent.webm`)
- Track 2: Animated captions (driven by `transcript.json`)
- Track 3: Background music (`<audio>` with `data-volume="0.3"`)

### Recipe 2: Product Launch Video

```bash
npx hyperframes init product-launch --example product-promo --non-interactive
```

Typical structure: 3-5 scenes with title → features → demo → CTA.

### Recipe 3: Code Walkthrough

Structure: Terminal/editor mockup background + animated code highlights + voiceover captions.

### Recipe 4: Data Visualization

Structure: Animated charts (CSS/GSAP driven), counters, stat reveals with staggered entrances.

### Recipe 5: Social Media Short (Vertical 1080x1920)

Set `data-width="1080" data-height="1920"` on root. Refer to **"Vertical Video Safe Zones (P1)"** section for complete layout rules, typography scale, and safe margins. Key points: title at top 160px, content zone 400-1600px, bottom 320px reserved for platform UI, fast pacing (2-3s per scene), bold colors, single-column card layout preferred.

---

## 口播后期处理管线（Post-Production Pipeline for Talking-Head Videos）

本章节覆盖 **对已有视频素材进行后期处理** 的完整流程——加字幕、叠特效、换背景、混音 BGM、画中画等。

### 适用场景

| 场景 | 输入 | 输出 |
|------|------|------|
| 口播 + 字幕 | 一段录好的口播 MP4 | 带字幕动效的成品 MP4 |
| 口播 + 字幕 + 特效 | 口播 MP4 | 带字幕 + 粒子/光效叠加的成品 |
| 口播 + 换背景 | 口播 MP4（纯色/杂背景） | 去背景 + 新背景的成品 |
| 多段素材拼接 | 多个 MP4 片段 | 合并 + 转场 + 统一字幕的成品 |
| 画中画 | 主视频 + 辅助画面 | PiP 布局的成品 |

### 关键经验：口播视频修改防错清单（必须执行）

以下经验来自一次 86 秒口播视频连续迭代中反复出现的问题。处理已有口播视频时必须优先执行这些规则，避免重复踩坑。

#### 0. 触发与能力边界：精细口播后期必须启用本 Skill

1. **用户要求“更精准时间对齐 / 更炫字幕动效 / 转场特效 / 完整口播后期处理管线”时，必须立即启用 AI 短视频工厂 Skill。** 不得只用纯 FFmpeg + ASS 字幕做简单烧录后交付，因为那只能完成基础字幕，不等于完整口播后期。
2. **不得在未启用 HyperFrames 的情况下承诺“精准匹配字幕位置和特效”。** 如果只是 FFmpeg 静态字幕，必须明确说明能力有限；若用户明确要求完整效果，进入 HyperFrames 管线。
3. **完整口播后期标准管线必须包含：** 素材预检 → 音频提取 → Whisper/whisper.cpp 转写或时间戳分析 → 用户原文校对 → HTML Composition 编排 → GSAP 字幕/特效/转场 → HyperFrames lint → HyperFrames render → FFmpeg 后置音频合成 → 交付前验证。
4. **第一次交付就应采用正确管线。** 不要先交一个“简单字幕版”再等用户指出“没有启用 HyperFrames”。如果用户一开始已经提出“自动匹配位置、加字幕和特效”，默认就是 HyperFrames 任务。
5. **若先前已经用非 HyperFrames 方案做错，必须在复盘中记录为：触发识别失败，而不是单纯“效果不好”。** 后续遇到类似请求时，先加载本 Skill，再执行完整管线。

#### A. 源素材与音频：不要凭听感或渲染结果臆断

1. **始终先确认用户指定的原视频就是唯一音频真源。** 用户说“原视频里有背景音乐”时，不得擅自判断为没有 BGM，也不得自行合成替代音乐。
2. **必须用 FFmpeg 验证尾段音频是否存在。** 对用户指出的时间段（例如 1:16 后）执行：

```bash
ffmpeg -ss 76 -t 10 -i input.mov -af volumedetect -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume"
```

如果 `mean_volume`/`max_volume` 有有效值，说明该段确实有声音，后续成品必须保留。

3. **已有原片音频时，采用“视觉渲染 + FFmpeg 后置合成原音频”的可靠流程。** 不要依赖 HyperFrames 从 `.mov` 或长音频中直接 mux 完整音频；不要在 `<audio>` 中直接引用 `.mov` 作为音频源来保留长尾 BGM。正确做法：

```bash
# 1. 从原视频提取完整音频
ffmpeg -y -i input.mov -vn -acodec pcm_s16le -ar 44100 -ac 1 original_audio.wav

# 2. HyperFrames 渲染视觉版（可以不放 <audio>，允许 silent visual output）
npx hyperframes render --output visual.mp4

# 3. 后置合成完整原音频
ffmpeg -y -i visual.mp4 -i original_audio.wav \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k \
  -t <video_duration> -movflags +faststart final.mp4
```

4. **最终必须验证音频完整性。** 不仅检查 `ffprobe` 时长，还要检查用户指出的尾段：

```bash
ffprobe -v quiet -show_entries format=duration -show_entries stream=codec_type,duration -of default=noprint_wrappers=1 final.mp4
ffmpeg -ss 76 -t 10 -i final.mp4 -af volumedetect -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume"
```

#### B. 字幕与文案：用户给的精确文案优先级最高

1. **用户明确指定某段字幕时，必须逐字使用用户原文。** 不要根据 ASR、记忆或模型理解自行“纠错”产品名。例如用户指定“Codex自动化剪辑视频”，不得改成 “QDesk”“QClaw” 或其它更合理的词。
2. **每次修改字幕后必须定位对应 `cap-*`，只改目标时间段，不顺手改其它字幕。** 对 3s-7s 这类精确时间段，先在 `index.html` 中找到 `data-start`/`data-duration` 覆盖该区间的字幕节点，再替换文本。
3. **避免交付前只报“已改”。** 对字幕修正必须在最终回答中列出改动后的准确文本，便于用户核对。

#### C. 视觉迭代：严格按用户约束，不额外加效果

1. **用户要求“不要增强光效/不要粒子/不要某类动效”时，必须删除对应 CSS、DOM、GSAP tween。** 不要仅设为透明或保留隐藏元素，避免后续误启用或 lint 干扰。
2. **用户要求位置变化时，按方向显式调整坐标。** 例如“整体往左一点”应从 `right: ...` 改为明确 `left: ...` 或减少 `right` 值，并在交付说明中标注实际坐标变化。
3. **用户要求字体颜色不要为白色时，检查所有相关文本层。** 数据图表要同时检查 value、label、legend，不只改一个元素。

#### D. 交付门禁：未验证关键问题不得交付

在每次渲染交付前，至少完成以下验证：

- 字幕关键片段：目标 `cap-*` 文本与用户要求完全一致。
- 音频关键片段：用户指出的尾段存在有效音量。
- 成品时长：视频流和音频流时长接近，误差 ≤ 0.1s。
- 用户本轮要求：逐项勾选，不遗漏“颜色/位置/去除效果/音频”等小项。

### 完整 Step-by-Step 流程

```text
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: 素材预处理                                          │
│   ① 检查素材格式 → ② FFmpeg 标准化 → ③ 提取音频             │
├─────────────────────────────────────────────────────────────┤
│ Phase 2: 分析与转写                                          │
│   ④ 语音转写 → ⑤ 字幕分组 → ⑥ 时间轴确认                   │
├─────────────────────────────────────────────────────────────┤
│ Phase 3: 合成编排                                            │
│   ⑦ 初始化项目 → ⑧ 编写 Composition HTML → ⑨ 渲染           │
├─────────────────────────────────────────────────────────────┤
│ Phase 4: 后期混音                                            │
│   ⑩ BGM 合成 → ⑪ 音量平衡 → ⑫ 交付                        │
└─────────────────────────────────────────────────────────────┘
```

### Phase 1: 素材预处理

#### 素材预检清单

```bash
# 检查视频信息
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# 确认关键参数
# - 分辨率：1920x1080 或 1080x1920（竖版）
# - 帧率：25/30fps
# - 编码：H.264/H.265
# - 音频：AAC，采样率 44100/48000
```

#### 常见预处理操作

```bash
# 分辨率不是 1080p → 缩放
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:a copy normalized.mp4

# 竖版视频标准化
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:a copy normalized_v.mp4

# 帧率标准化为 30fps
ffmpeg -i input.mp4 -r 30 -c:a copy fps30.mp4

# 提取纯音频（用于转写和混音）
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio_for_transcribe.wav
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 audio_original.wav

# 获取视频时长（秒）
ffprobe -v error -show_entries format=duration -of csv=p=0 input.mp4
```

#### 多段素材拼接预处理

```bash
# 方式 1: FFmpeg concat demuxer（推荐，无重编码）
# 创建 filelist.txt:
# file 'clip1.mp4'
# file 'clip2.mp4'
# file 'clip3.mp4'
ffmpeg -f concat -safe 0 -i filelist.txt -c copy merged.mp4

# 方式 2: 需要重编码（分辨率/编码不同时）
ffmpeg -f concat -safe 0 -i filelist.txt -vf "scale=1920:1080" -c:v libx264 -c:a aac merged.mp4

# 方式 3: 在 HyperFrames 中用多个 <video> 元素分段播放（带转场）
# → 见后续 Composition 模板
```

### Phase 2: 语音转写与字幕生成

```bash
# 转写中文口播（推荐 medium 模型，中文识别更准）
npx hyperframes transcribe input.mp4 --model medium

# 如果已有 SRT/VTT 字幕文件
npx hyperframes transcribe existing.srt
```

**中文字幕分组规则：**

| 规则 | 说明 |
|------|------|
| 每行最大字数 | 14-16 个中文字符 |
| 每组最大行数 | 2 行 |
| 按语义断句 | 在标点符号（，。！？）处断开 |
| 最短停留时间 | ≥ 1.2 秒（给观众阅读时间） |
| 最长停留时间 | ≤ 5 秒（避免字幕"粘"太久） |

### Phase 3: Composition 编排

#### 核心 HTML 模板：口播 + 字幕 + 特效

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    /* === 字幕层样式 === */
    .caption {
      position: absolute;
      bottom: 100px;
      left: 50%;
      transform: translateX(-50%);
      font-family: "Inter", sans-serif;
      font-size: 42px;
      font-weight: 700;
      color: #ffffff;
      text-align: center;
      max-width: 75%;
      padding: 12px 24px;
      border-radius: 8px;
      background: rgba(0, 0, 0, 0.6);
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
      /* 中文适配 */
      line-height: 1.5;
      letter-spacing: 0.02em;
    }

    /* === 特效层样式 === */
    .effect-layer {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 10;
    }

    .particle {
      position: absolute;
      width: 4px;
      height: 4px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.6);
    }
  </style>
</head>
<body>
  <!-- Root composition -->
  <div data-composition-id="post-production"
       data-width="1920" data-height="1080" data-fps="30"
       data-duration="VIDEO_DURATION">

    <!-- Track 0: 原始视频（或去背景后的视频 + 新背景） -->
    <video id="main-video"
           data-start="0" data-duration="VIDEO_DURATION" data-track-index="0"
           src="input.mp4"
           style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">
    </video>

    <!-- Track 1: 字幕层 -->
    <div id="cap-1" class="caption" data-start="0.5" data-duration="2.3" data-track-index="1">
      大家好，欢迎来到今天的分享
    </div>
    <div id="cap-2" class="caption" data-start="2.8" data-duration="2.0" data-track-index="1">
      今天我们聊一聊 AI 编程
    </div>
    <!-- ... 更多字幕 ... -->

    <!-- Track 2: 特效叠加层 -->
    <div id="effects" class="effect-layer"
         data-start="0" data-duration="VIDEO_DURATION" data-track-index="2">
      <!-- 粒子/光效/图标等 -->
    </div>

    <!-- Track 3: BGM -->
    <audio data-start="0" data-duration="VIDEO_DURATION" data-track-index="3"
           src="bgm.wav" data-volume="0.25"></audio>

  </div>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    // 字幕入场动画
    const captionTl = gsap.timeline({ paused: true });
    document.querySelectorAll('.caption').forEach(cap => {
      const start = parseFloat(cap.dataset.start);
      captionTl.fromTo(cap,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.3 },
        start
      );
      captionTl.to(cap,
        { opacity: 0, duration: 0.2 },
        start + parseFloat(cap.dataset.duration) - 0.2
      );
    });

    window.__timelines = window.__timelines || {};
    window.__timelines["post-production"] = captionTl;
  </script>
</body>
</html>
```

#### 去背景 + 换背景模板

```html
<!-- Track 0: 新背景 -->
<div id="new-bg" data-start="0" data-duration="VIDEO_DURATION" data-track-index="0"
     style="position:absolute;inset:0;background:linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);">
  <!-- 可放动态网格、粒子等背景动画 -->
</div>

<!-- Track 1: 去背景后的人物 -->
<video id="person" data-start="0" data-duration="VIDEO_DURATION" data-track-index="1"
       src="transparent.webm"
       style="position:absolute;bottom:0;left:50%;transform:translateX(-50%);height:90%;object-fit:contain;">
</video>

<!-- Track 2: 字幕 -->
<!-- ... -->
```

#### 画中画 (PiP) 模板

```html
<!-- Track 0: 主画面（全屏） -->
<video id="main" data-start="0" data-duration="VIDEO_DURATION" data-track-index="0"
       src="main-content.mp4"
       style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">
</video>

<!-- Track 1: 画中画（右下角小窗） -->
<video id="pip" data-start="0" data-duration="VIDEO_DURATION" data-track-index="1"
       src="talking-head.mp4"
       style="position:absolute;bottom:40px;right:40px;width:360px;height:360px;
              border-radius:50%;object-fit:cover;border:3px solid rgba(255,255,255,0.8);
              box-shadow:0 4px 20px rgba(0,0,0,0.3);">
</video>

<!-- PiP 变体：左下角矩形 -->
<!--
<video id="pip-rect" ...
       style="position:absolute;bottom:40px;left:40px;width:480px;height:270px;
              border-radius:12px;object-fit:cover;border:2px solid rgba(255,255,255,0.5);">
</video>
-->
```

#### 分屏布局模板

```html
<!-- 左右分屏 50/50 -->
<video id="left" data-start="0" data-duration="VIDEO_DURATION" data-track-index="0"
       src="screen-recording.mp4"
       style="position:absolute;left:0;top:0;width:50%;height:100%;object-fit:cover;">
</video>
<video id="right" data-start="0" data-duration="VIDEO_DURATION" data-track-index="0"
       src="talking-head.mp4"
       style="position:absolute;right:0;top:0;width:50%;height:100%;object-fit:cover;">
</video>
<!-- 中间分割线 -->
<div data-start="0" data-duration="VIDEO_DURATION" data-track-index="1"
     style="position:absolute;left:50%;top:0;width:2px;height:100%;background:rgba(255,255,255,0.3);transform:translateX(-50%);">
</div>
```

### Phase 4: 音频混音策略

#### 基本混音（BGM + 原声）

```bash
# 1. 渲染视频（无音频）
npx hyperframes render --non-interactive

# 2. 提取原始口播音频
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 voice.wav

# 3. 混合：原声为主，BGM 为辅
ffmpeg -i voice.wav -i bgm.wav -filter_complex \
  "[0:a]volume=1.0[voice];[1:a]volume=0.25[bgm];[voice][bgm]amix=inputs=2:duration=first" \
  -ac 2 -ar 44100 mixed_audio.wav

# 4. 合并视频 + 混音
ffmpeg -i rendered_video.mp4 -i mixed_audio.wav -c:v copy -c:a aac -shortest final.mp4
```

#### 高级：BGM 自动避让（Ducking）

当人声出现时 BGM 自动降低音量，人声停顿时 BGM 恢复：

```bash
# 使用 sidechaincompress 实现 ducking
ffmpeg -i voice.wav -i bgm.wav -filter_complex \
  "[1:a]volume=0.35[bgm_vol];\
   [bgm_vol][0:a]sidechaincompress=threshold=0.02:ratio=4:attack=200:release=1000[bgm_ducked];\
   [0:a][bgm_ducked]amix=inputs=2:duration=first[out]" \
  -map "[out]" -ac 2 -ar 44100 mixed_ducked.wav
```

**参数说明：**
- `threshold=0.02`: 人声信号强度阈值（越低越敏感）
- `ratio=4`: 压缩比（4:1 表示 BGM 降到原来 1/4）
- `attack=200`: 压缩启动时间 200ms（避免突然降低）
- `release=1000`: 释放时间 1000ms（人声停后 1 秒 BGM 恢复）

#### 音量标准化

```bash
# 测量当前音量
ffmpeg -i mixed_audio.wav -af "volumedetect" -f null /dev/null

# 标准化到 -16 LUFS（适合社交媒体）
ffmpeg -i mixed_audio.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" normalized.wav
```

### 特效叠加模板库

#### 1. 粒子飘落效果

```html
<div id="particles" class="effect-layer" data-start="0" data-duration="VIDEO_DURATION" data-track-index="2">
  <!-- 粒子由 JS 生成 -->
</div>

<script>
function mulberry32(seed) {
  return function() {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  }
}
const rand = mulberry32(42);

// 生成粒子
const container = document.getElementById('particles');
for (let i = 0; i < 30; i++) {
  const p = document.createElement('div');
  p.className = 'particle';
  p.style.cssText = `
    left: ${rand() * 100}%;
    top: -10px;
    width: ${3 + rand() * 4}px;
    height: ${3 + rand() * 4}px;
    opacity: ${0.3 + rand() * 0.5};
    background: hsl(${200 + rand() * 60}, 80%, 70%);
  `;
  container.appendChild(p);
}

// 粒子下落动画
const particleTl = gsap.timeline({ paused: true });
container.querySelectorAll('.particle').forEach((p, i) => {
  particleTl.to(p, {
    y: 1200,
    x: `+=${(rand() - 0.5) * 200}`,
    duration: 4 + rand() * 3,
    repeat: Math.floor(VIDEO_DURATION / 6),
    ease: "none",
    delay: rand() * 3
  }, 0);
});
// 注意：将 particleTl 加入 window.__timelines
</script>
```

#### 2. 底部动态信息条（Lower Third）

```html
<div id="lower-third" class="effect-layer" data-start="2" data-duration="8" data-track-index="2">
  <div style="position:absolute;bottom:60px;left:60px;display:flex;align-items:center;gap:16px;">
    <div style="width:4px;height:48px;background:linear-gradient(180deg,#00d4ff,#7b2ff7);border-radius:2px;"></div>
    <div>
      <div style="font-family:'Inter',sans-serif;font-size:28px;font-weight:700;color:#fff;">张三</div>
      <div style="font-family:'Inter',sans-serif;font-size:20px;color:rgba(255,255,255,0.7);margin-top:4px;">高级产品经理 · 某科技公司</div>
    </div>
  </div>
</div>

<script>
const ltTl = gsap.timeline({ paused: true });
const lt = document.querySelector('#lower-third > div');
ltTl.fromTo(lt, { x: -300, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: "power2.out" }, 2);
ltTl.to(lt, { x: -300, opacity: 0, duration: 0.4, ease: "power2.in" }, 9.5);
// 加入 window.__timelines
</script>
```

#### 3. 光效扫描（Light Sweep）

```html
<div id="light-sweep" class="effect-layer" data-start="0" data-duration="VIDEO_DURATION" data-track-index="2">
  <div class="sweep-bar" style="
    position:absolute;
    top:0;left:-200px;
    width:200px;height:100%;
    background:linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    transform:skewX(-15deg);
  "></div>
</div>

<script>
const sweepTl = gsap.timeline({ paused: true });
sweepTl.to('.sweep-bar', {
  x: 2200,
  duration: 3,
  repeat: Math.floor(VIDEO_DURATION / 5),
  repeatDelay: 2,
  ease: "power1.inOut"
}, 0);
</script>
```

#### 4. 关键词高亮弹出

```html
<!-- 在特定时间点弹出关键信息 -->
<div id="keyword-pop" data-start="5" data-duration="3" data-track-index="2"
     style="position:absolute;top:50%;right:80px;transform:translateY(-50%);
            font-family:'Inter',sans-serif;font-size:56px;font-weight:900;
            color:#00d4ff;text-shadow:0 0 20px rgba(0,212,255,0.5);">
  效率提升 300%
</div>

<script>
const kwTl = gsap.timeline({ paused: true });
kwTl.fromTo('#keyword-pop',
  { scale: 0, opacity: 0, rotation: -5 },
  { scale: 1, opacity: 1, rotation: 0, duration: 0.4, ease: "back.out(1.7)" },
  5
);
kwTl.to('#keyword-pop', { opacity: 0, y: -30, duration: 0.3 }, 7.5);
</script>
```

### 字幕动效选项

AI 根据视频风格自动选择最合适的字幕动效：

| 动效类型 | 适用场景 | CSS/GSAP 实现 |
|----------|---------|--------------|
| **淡入淡出** | 正式/商务口播 | `opacity: 0→1→0` |
| **底部弹出** | 活泼/教程 | `y: 20→0`, `opacity: 0→1` |
| **逐字打字机** | 科技/极客风 | 每字 stagger 0.05s |
| **卡拉OK高亮** | 重点强调 | word-level 颜色切换 |
| **缩放弹入** | 短视频/抖音风 | `scale: 0.5→1`, `ease: back.out` |

#### 卡拉OK高亮实现

```html
<div id="cap-karaoke" class="caption" data-start="3" data-duration="2.5" data-track-index="1">
  <span class="word" data-word-start="3.0" data-word-end="3.4">今天</span>
  <span class="word" data-word-start="3.4" data-word-end="3.7">我们</span>
  <span class="word" data-word-start="3.7" data-word-end="4.1">来聊</span>
  <span class="word" data-word-start="4.1" data-word-end="4.5">AI</span>
  <span class="word" data-word-start="4.5" data-word-end="5.0">编程</span>
</div>

<style>
.word { color: rgba(255,255,255,0.5); transition: color 0.1s; }
.word.active { color: #00d4ff; text-shadow: 0 0 10px rgba(0,212,255,0.5); }
</style>

<script>
const karaokeTl = gsap.timeline({ paused: true });
document.querySelectorAll('#cap-karaoke .word').forEach(w => {
  const start = parseFloat(w.dataset.wordStart);
  karaokeTl.to(w, { className: "+=active", duration: 0.01 }, start);
});
</script>
```

#### 逐字打字机实现

```javascript
const typeTl = gsap.timeline({ paused: true });
const capEl = document.getElementById('cap-type');
const chars = capEl.textContent.split('');
capEl.textContent = '';
chars.forEach(ch => {
  const span = document.createElement('span');
  span.textContent = ch;
  span.style.opacity = '0';
  capEl.appendChild(span);
});
typeTl.to(capEl.querySelectorAll('span'), {
  opacity: 1,
  stagger: 0.05,
  duration: 0.01
}, parseFloat(capEl.dataset.start));
```

### 快速口播加工模式

当用户只说 **"帮我这段口播加字幕和特效"** 时，AI 自动执行以下完整流程：

```text
用户提供 MP4 → 
  ① ffprobe 检查素材参数
  ② 标准化为 1080p 30fps（如需）
  ③ hyperframes transcribe --model medium
  ④ 自动字幕分组（中文 14字/行，按标点断句）
  ⑤ 选择字幕动效（默认：底部弹出 + 半透明底板）
  ⑥ 选择特效层（默认：轻微粒子 + 底部信息条）
  ⑦ 编写 Composition HTML
  ⑧ hyperframes render
  ⑨ 音频处理（默认保留原片完整音频；仅在用户要求时混入 BGM）
  ⑩ 自检管线 Phase B-D
  ⑪ 交付 final.mp4
```

**AI 默认选择（用户未指定时）：**
- 字幕样式：底部居中，42px，白字 + 半透明黑底
- 字幕动效：淡入淡出
- 特效层：轻微光效扫描（不抢视觉焦点）
- BGM：无（除非用户要求）
- 画面处理：保持原始画面不去背景

**用户可随时覆盖任何默认选择。**

### 口播后期自检追加项

在标准 Phase A-D 自检管线之外，口播后期处理需额外检查：

| # | 检查项 | Pass 标准 |
|---|--------|-----------|
| P1 | 字幕与语音同步 | 字幕出现时间 ≤ 语音开始后 0.2s |
| P2 | 字幕无遮挡关键画面 | 字幕区域（bottom 100px）无人脸/关键信息 |
| P3 | 原视频音画同步 | 渲染后口型与音频匹配 |
| P4 | 特效层不干扰主内容 | 特效透明度 ≤ 0.3，不遮挡人物/字幕 |
| P5 | BGM ducking 生效 | 人声段 BGM 降到 -20dB 以下 |
| P6 | 视频时长完整 | output duration ≥ input duration - 0.1s |

---

## Sub-Compositions

For complex videos, split into separate HTML files:

```html
<!-- In index.html -->
<div id="scene-1" data-composition-id="intro"
     data-composition-src="compositions/intro.html"
     data-start="0" data-duration="5" data-track-index="1"></div>
```

Sub-composition files use `<template>` wrapper (main index.html does NOT):

```html
<template id="intro-template">
  <div data-composition-id="intro" data-width="1920" data-height="1080">
    <!-- content, style, script -->
  </div>
</template>
```

## Variables (Parametrized Compositions)

Declare on `<html>` root, read with `window.__hyperframes.getVariables()`:

```html
<html data-composition-variables='[
  {"id":"title","type":"string","label":"Title","default":"Hello"},
  {"id":"accent","type":"color","label":"Accent Color","default":"#ff6b35"}
]'>
```

Override at render: `npx hyperframes render --variables '{"title":"Q4 Report"}'`

## Iterative Fix Decision Tree

When the user requests modifications after initial delivery, follow this decision tree to minimize re-work:

### Fix Classification

| Change type | Scope | Actions required |
|------------|-------|-----------------|
| **Text/data change** | Single scene content | Edit HTML → Lint → Re-render → Re-mux audio → Verify |
| **Layout/position fix** | CSS class or inline style | Edit CSS → Lint → Re-render → Re-mux audio → Verify |
| **Color/style change** | CSS variables or colors | Edit CSS → Lint → Re-render → Re-mux audio → Verify |
| **Animation timing** | GSAP parameters | Edit JS → Lint → Re-render → Re-mux audio → Verify |
| **Add/remove scene** | Structure change | Edit HTML+JS → Recalculate all timings → Lint → Re-render → Re-mux → Verify |
| **BGM style change** | Audio only | Only when user requested BGM change: regenerate/replace BGM → Re-mux only (skip re-render) → Verify audio |
| **Duration change** | Everything | Full rebuild required |

### Quick-Fix Workflow (for text/layout/color/animation changes)

```text
1. Identify affected scene(s) — read current HTML
2. Make targeted edit(s) — ONLY touch affected parts
3. npx hyperframes lint — must pass
4. npx hyperframes render --quality draft — fast preview check
5. If draft looks good → render --quality standard
6. Re-mux the approved audio source (original_audio.wav for existing videos, bgm.wav only for generated-BGM projects)
7. Verify final MP4 (Phase C+D checks)
8. Deliver
```

**Key optimization: DO NOT regenerate or replace audio** unless the user requests a music style change or duration change. For existing source videos, reuse the extracted `original_audio.wav`; for generated-BGM projects, reuse the existing approved `bgm.wav` across layout/content fixes.

### When to Use `--quality draft` First

ALWAYS render draft quality first when:
- Fixing layout issues (verify position before full render)
- User reported visual problems (confirm fix before spending 10+ minutes)
- Making multiple iterative adjustments (draft → confirm → standard)

Draft renders at ~3x speed. Only proceed to `standard` after visual confirmation.

### Batch Fix Strategy

When user reports multiple issues at once:
1. Collect ALL reported issues
2. Fix ALL issues in a single pass (edit HTML once)
3. Lint once
4. Render once (not once per fix)
5. Verify all fixes in the rendered output

NEVER render between each individual fix — that wastes 10+ minutes per cycle.

---

## Chinese Content Adaptation (Soft Default — 中文适配参考)

以下规则是中文视频的**经验参考**，帮助 AI 在用户未给出详细排版指示时做出合理的中文布局决策。**当用户的提示词有明确的排版/密度/风格要求时，以用户要求为准。**

### Text Density Reference

| Scene duration | 建议中文字数 (同时在屏) | 建议内容项数 |
|---------------|-------------------------|-------------|
| 3 seconds | 60-80 字 | 3-4 items |
| 4 seconds | 80-120 字 | 4-6 items |
| 5+ seconds | 120-160 字 | 6-8 items |

**自检关注点**: 如果某场景文字过密导致不可读（字号 ≤ 28px 且停留 ≤ 3s），AI 应自动拆分——这是可读性问题，不是风格限制。

### Chinese Typography CSS (推荐实践)

```css
/* Line breaking — keep Chinese words together */
.content-area, .content-col, .glass-card {
  word-break: keep-all;        /* prevent mid-word breaks */
  overflow-wrap: break-word;   /* break only at natural points */
  line-break: strict;          /* no punctuation at line start */
}

/* Chinese line height — wider than English */
p, span, .card-desc { line-height: 1.6; }   /* body text */
h2, h3 { line-height: 1.3; }                /* titles */

/* Mixed CJK + Latin spacing */
.mixed-text { text-spacing-trim: space-all; } /* if supported */
/* Fallback: manually add thin space between Chinese and numbers/English */
```

### Chinese-English Mixed Content Conventions

| Pattern | Example | Rule |
|---------|---------|------|
| Number + Chinese unit | `128亿美元` | No space between number and Chinese |
| English brand + Chinese | `GitHub Copilot 工具` | Space between English and Chinese |
| Percentage | `156%` or `156％` | Use half-width `%` (more compact) |
| Punctuation | `，、。；` | Use full-width Chinese punctuation in body text |
| Data labels | `市场规模：` | Use full-width colon `：` in Chinese context |
| Card titles | `核心技术突破` | No trailing punctuation on card titles |

### Chinese Layout Adjustments (参考)

Chinese characters are wider than Latin characters. 当 AI 自行规划布局时可参考：

| Element | English width | Chinese adjustment |
|---------|--------------|-------------------|
| Card title | 40-44px | 38-42px (reduce 2px) |
| Body text | 34-38px | 32-36px (reduce 2px) |
| Card width | 360px | 380-400px (increase 20-40px) |
| Line chars | ~40 chars/line | ~18-22 中文字/行 |

### Scene Content Text Templates (灵感参考，非必须)

```text
数据展示场景:
  主数据: "128亿" (数字 88-96px + 单位 42px)
  标签: "市场规模" (38px, opacity 0.7)

卡片场景:
  图标: 64-72px emoji/SVG
  卡片标题: "核心技术突破" (40px, bold)
  描述文字: "一句话说明功能或数据" (32-34px, opacity 0.8)
  底部标注: "具体数据或来源" (28px, opacity 0.6)

列表场景:
  序号: "01" (56px, accent color)
  内容: "一行描述，不超过25字" (36px)

NOTE: 以上仅为参考模板。AI 完全可以使用不同的信息层级、卡片结构或数据展示方式。
```

---

## Vertical Video Safe Zones (P1 — 1080×1920)

### Layout System for 9:16 Vertical Videos

```
┌───────────────────────┐
│ Top Safe: 120px       │ ← Platform UI (status bar)
├───────────────────────┤
│ Title Zone:           │
│ top 160px, h ≤ 200px  │
├───────────────────────┤
│                       │
│ Content Zone:         │
│ top 400px ~ bot 1600px│ ← Available: 1200px
│                       │
├───────────────────────┤
│ Bottom Safe: 320px    │ ← Platform UI (controls, comments)
└───────────────────────┘
```

### Vertical Video Typography Scale

| Element | Safe range | Hard max |
|---------|-----------|----------|
| Cover mega title | 120-160px | 180px |
| Scene title | 80-100px | 120px |
| Subtitle | 48-64px | 72px |
| Body text | 36-48px | 56px |
| Card title | 40-52px | 56px |
| Data number | 96-128px | 140px |
| Icon/emoji | 72-108px | 128px |

### Vertical Content Rules

- Max 2 cards horizontally (full width), prefer single-column stacking
- Card width: 90% container (≈ 972px)
- Scene transitions: faster pacing (2-3s per scene typical for Reels/TikTok)
- Bottom 320px always clear (platform overlays on mobile)
- Horizontal safe margin: ≥ 60px (narrower than landscape)

---

## Icon & Emoji Strategy (P1)

### Recommended Approach Priority

1. **Unicode Emoji** (first choice for most cases)
   - ✅ Renders consistently in Chrome Headless
   - ✅ No external dependencies
   - ✅ Supports all common categories
   - ⚠️ Style varies slightly across platforms (but video rendering uses Chrome's Noto Emoji)

2. **Inline SVG** (when custom icons needed)
   - ✅ Pixel-perfect control
   - ✅ Animatable with GSAP
   - ✅ Color matches theme exactly
   - ⚠️ Increases HTML file size

3. **CSS-drawn shapes** (for simple geometric icons)
   - ✅ No external resources
   - ✅ Fully animatable
   - ⚠️ Limited to simple shapes

### PROHIBITED approaches
- ❌ Font Awesome / Material Icons CDN (render environment may not load)
- ❌ External image URLs (network dependency = unreliable)
- ❌ Icon font `@import` (same issue as Google Fonts)

### Common Tech Video Icon Set (copy-paste ready)

```text
Categories:
💻 编程/开发   🚀 发布/增长   📊 数据/图表   🔧 工具/设置
🎯 目标/聚焦   ⚡ 性能/速度   🔒 安全/隐私   🌐 网络/全球
📱 移动端      🤖 AI/机器人   🎮 游戏        🏗️ 架构/构建
💡 创新/灵感   📈 增长/趋势   🛡️ 防护/安全   ⏱️ 时间/效率

Specific use cases:
Web开发: 🌐    移动应用: 📱    AI/ML: 🤖    游戏: 🎮
网络安全: 🔒   数据科学: 📊    代码: 💻     部署: 🚀
效率: ⚡       质量: ✅        风险: ⚠️     趋势: 📈
```

### Icon Sizing Rules

```css
/* Standard icon in card */
.card-icon { font-size: 64px; line-height: 1; }

/* Small inline icon */
.inline-icon { font-size: 48px; vertical-align: middle; }

/* Feature highlight icon */
.feature-icon { font-size: 72px; }

/* NEVER exceed these for icons: */
/* Horizontal video: 96px max */
/* Vertical video: 128px max */
```

### Custom SVG Icon Template

```html
<!-- Reusable SVG icon pattern for tech videos -->
<svg width="64" height="64" viewBox="0 0 64 64" fill="none">
  <circle cx="32" cy="32" r="28" stroke="currentColor" stroke-width="2" opacity="0.3"/>
  <path d="M20 32 L28 40 L44 24" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
</svg>
```

---

## Render Time Estimation (P1)

### Estimated Render Duration by Quality

| Quality | Speed ratio | 10s video | 30s video | 42s video | 60s video |
|---------|------------|-----------|-----------|-----------|-----------|
| `draft` | ~6fps | ~2 min | ~5 min | ~7 min | ~10 min |
| `standard` | ~3fps | ~3 min | ~10 min | ~14 min | ~20 min |
| `high` | ~1.5fps | ~7 min | ~20 min | ~28 min | ~40 min |

*Times are approximate. Complex scenes (many particles, gradients, blur filters) render slower.*

### Factors That Increase Render Time

| Factor | Impact | Mitigation |
|--------|--------|-----------|
| `backdrop-filter: blur()` | +30-50% | Limit to 3-4 elements max |
| > 50 particles | +20% | Cap at 40, reduce size |
| Multiple box-shadows | +15% | Use single subtle shadow |
| 60fps (vs 30fps) | +100% | Use 30fps unless requested |
| Large video backgrounds | +40% | Use gradient/CSS backgrounds instead |

### User Communication Template

Before starting a render, inform the user:

```text
"开始渲染 [质量] 品质视频（[时长]秒），预计需要 [X-Y] 分钟。
渲染期间我会持续检查进度，完成后立即进行音频合成和质量验证。"
```

### Render Strategy Decision

```text
用户要求"快速看一下效果" → --quality draft
用户要求"正式版/最终版"  → --quality standard
用户明确说"最高画质"     → --quality high --fps 60
修复布局问题验证        → --quality draft (先确认再正式渲染)
```

---

## Performance Optimization (P2)

### DOM Element Limits

| Complexity level | Max DOM elements | Max particles | Max cards | Render impact |
|-----------------|-----------------|---------------|-----------|---------------|
| Light | < 200 | 20 | 3-4 | Normal speed |
| Medium | 200-500 | 40 | 6-8 | +20% time |
| Heavy | 500-1000 | 60 | 10-12 | +50% time |
| Danger zone | > 1000 | > 80 | > 15 | May crash Chrome |

### Optimization Techniques

```css
/* Use will-change for animated elements (Chrome optimization) */
.scene-wrapper, .glass-card, .particle {
  will-change: transform, opacity;
}

/* Reduce paint complexity */
.particle {
  border-radius: 50%;
  /* Use background-color, NOT box-shadow for particles */
  background: currentColor;
}

/* GPU-accelerated properties only */
/* PREFER: transform, opacity */
/* AVOID: width, height, top, left, margin, padding, box-shadow (triggers layout) */
```

### When Chrome Crashes During Render

1. Reduce `--workers` to 1: `npx hyperframes render --workers 1`
2. Remove excessive particles (cap at 30)
3. Replace `backdrop-filter: blur()` with pre-blurred gradient backgrounds
4. Remove multiple `box-shadow` layers
5. If still crashing: split into shorter sub-compositions, render separately, concatenate with FFmpeg

### Render Timeout Handling

If render exceeds 20 minutes for a ≤ 60s video:
1. Check if Chrome process is still alive (`ps aux | grep chrome`)
2. If frozen: kill and retry with `--workers 1 --quality draft`
3. If draft succeeds: the standard render had a resource issue → simplify complex scenes
4. Report specific scene if identifiable (check last rendered frame number in output)

---

## Multi-Resolution Adaptation (P2)

### Supported Canvas Sizes

| Aspect ratio | Resolution | Use case | Init config |
|-------------|-----------|----------|-------------|
| 16:9 横版 | 1920×1080 | YouTube, 公众号, B站 | `data-width="1920" data-height="1080"` |
| 9:16 竖版 | 1080×1920 | 抖音, Reels, 视频号 | `data-width="1080" data-height="1920"` |
| 1:1 正方形 | 1080×1080 | Instagram Feed, 小红书 | `data-width="1080" data-height="1080"` |
| 4:5 竖版 | 1080×1350 | Instagram Feed (推荐) | `data-width="1080" data-height="1350"` |
| 4:3 标准 | 1440×1080 | 演示文稿风格 | `data-width="1440" data-height="1080"` |

### Per-Resolution Safe Zone Quick Reference

| Resolution | Title top | Content top | Content bottom | Side margin |
|-----------|-----------|-------------|----------------|-------------|
| 1920×1080 | 50px | 240px | 980px | 120px |
| 1080×1920 | 160px | 400px | 1600px | 60px |
| 1080×1080 | 50px | 200px | 980px | 80px |
| 1080×1350 | 80px | 260px | 1200px | 80px |

### Resolution-Specific Typography Scale

| Element | 1920×1080 | 1080×1920 | 1080×1080 |
|---------|-----------|-----------|-----------|
| Mega title | 96-120px | 120-160px | 80-100px |
| Scene title | 64-84px | 80-100px | 56-72px |
| Body text | 28-42px | 36-48px | 28-38px |
| Card title | 32-44px | 40-52px | 30-40px |
| Icon | 56-96px | 72-108px | 48-80px |

### Cross-Resolution Card Layouts

```text
1920×1080 (横版):
  3 horizontal cards: 480px each + 36px gap
  2×3 grid: 520px × 300px cards
  
1080×1920 (竖版):
  2 horizontal cards: 480px each + 24px gap
  1-column stack: 920px wide cards
  
1080×1080 (正方形):
  2 horizontal cards: 460px each + 24px gap
  2×2 grid: 460px × 340px cards
```

---

## Delivery & File Management (P2)

### File Naming Convention

```text
{project_name}_{version}_{quality}.mp4

Examples:
  ai_coding_video_v1_standard.mp4      ← first delivery
  ai_coding_video_v2_standard.mp4      ← after layout fix
  ai_coding_video_v3_standard.mp4      ← after content update
  ai_coding_video_final_standard.mp4   ← user-approved final
```

### Intermediate File Cleanup

After user approves a final version:
```bash
# Keep: final approved MP4, source HTML, bgm.wav
# Remove: intermediate renders
rm -f render_v1.mp4 render_v2.mp4 render_v3.mp4
rm -f final_ai_coding_v1.mp4 final_ai_coding_v2.mp4
# Keep: final_ai_coding_v3.mp4 (or rename to _final)
```

**Rule**: Never auto-delete intermediate files without user confirmation. Ask: "是否清理中间渲染文件？只保留最终版本。"

### Delivery Checklist

Before calling `deliver_attachments`:
1. ✅ File is the post-mux version (not raw render)
2. ✅ Audio verified (Phase C checks passed)
3. ✅ File size reasonable (1080p 42s ≈ 5-15MB for standard quality)
4. ✅ Filename clearly indicates version

### What to Preserve for Future Edits

Always keep in project directory:
- `index.html` — source composition (for re-editing)
- `original_audio.wav` — extracted original audio for existing-video edits, when source audio must be preserved
- `bgm.wav` — approved BGM audio only when the project uses generated or external BGM
- Customized copies of bundled helper scripts only if they were modified for this project (`scripts/verify_audio.py`, `scripts/gen_bgm.py` remain available in the Skill package)
- Final approved `.mp4` — the delivered product

## Quality Checklist (Final Gate — 交付前必过)

Before delivering any video, execute the full **AI Self-Check Pipeline** (Section 9). The checklist adapts to prompt mode:

### 硬约束检查（两种模式都必须通过）

1. **Lint pass**: `npx hyperframes lint` → 0 errors. (H-all)
2. **No prohibited code**: No `Math.random`, no banned fonts, no inline `top:%` overrides. (H1, H2, H7)
3. **Deterministic rendering**: No non-deterministic APIs, GSAP repeat uses `Math.floor`. (H1, H8)
4. **Root duration alignment**: `data-duration` on root = last scene end time.
5. **Audio full coverage** (≥30s video): FFmpeg post-mux → verify duration ≥ video, no silence in last 12s, RMS -15~-20dB. (H9)
6. **Visual integrity**: All content within canvas bounds, no clipping, no unreadable overlaps. (H6)
7. **Final delivery**: Only deliver the verified post-mux MP4. Never send intermediate renders.

### 视觉质量检查（两种模式都必须通过）

8. **Frame spot-check**: Extract mid-scene screenshots → verify no overlap/overflow/clipping.
9. **Readability**: 关键文字可读（字号 + 对比度 + 停留时间足够）.
10. **Transitions**: 场景之间有过渡，无未经用户要求的跳切.

### 提示词合规检查（详细提示词模式）

11. **Prompt compliance**: Content points, visual style, **color palette (user-specified, never overridden)**, BGM style, duration all match original prompt.

### 布局参考检查（仅使用软默认布局时）

12. **Standard layout zone**: Content ≥ 240px, ≤ 980px; Title zone not overlapped.
13. **Card density**: Compute `content_height` vs `available_height`. If overflow → reduce/split.
14. **Typography scale**: Text/icon sizes within reference range hard max.

**Note**: Items 12-14 仅在 AI 使用了标准布局骨架时检查。如果 AI 根据用户提示词或创意判断使用了自定义布局，这些项被替换为 Item 8 (frame spot-check) 的通过即可。

## 已知限制

| # | 限制 | 影响 | 应对方式 |
|---|------|------|---------|
| 1 | HyperFrames 内置音频 ≥32s 截断 | 长视频音频不完整 | FFmpeg 后置合成完整音频 (H9) |
| 2 | 仅支持 Inter/JetBrains Mono/Roboto 字体 | 中文字体无法自定义 | 依赖 sans-serif 系统回退 |
| 3 | 不支持 `@import url()` 引入字体 | 自定义 Google Fonts 不可用 | 仅用 Compiler 自动解析的字体 |
| 4 | 渲染需 Headless Chrome + FFmpeg | 无法在纯容器环境直接运行 | 需安装完整依赖或使用 Docker |
| 5 | 非确定性 API 会导致帧不一致 | `Math.random()` 等使渲染结果不可复现 | 使用 mulberry32 seeded PRNG |
| 6 | 单次渲染 DOM 复杂度上限 ~500 节点 | 超出可能导致 Chrome crash | 拆分场景或简化 DOM |
| 7 | 竖版视频 (1080×1920) 为实验性支持 | 部分动画比例需手动调整 | 使用竖版安全区参考表 |
| 8 | 渲染速度受机器性能影响 | 42s 视频约需 3-8 分钟渲染 | 开发阶段用 draft 模式预览 |

---

## Troubleshooting

```bash
npx hyperframes doctor         # Check environment
npx hyperframes browser        # Manage bundled Chrome
npx hyperframes info           # Version details
```

Common issues:
- "FFmpeg not found" → `brew install ffmpeg`
- "Chrome not found" → `npx hyperframes browser` to download
- Render hangs → Check for `repeat: -1` in timelines
- Empty frames → Ensure `window.__timelines` is registered synchronously

## References

- [references/composition-rules.md](references/composition-rules.md) — Full data-attribute spec, track rules, sub-composition format
- [references/animation-guide.md](references/animation-guide.md) — GSAP patterns, easing reference, transition catalog
- [references/caption-patterns.md](references/caption-patterns.md) — Caption styling, word-level sync, karaoke effects
