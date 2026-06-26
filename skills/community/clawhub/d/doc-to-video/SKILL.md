---
name: doc-to-video
description: 将 Markdown 技术文档自动转换成带配音旁白的专业视频。使用 edge-tts 生成自然人声、Remotion 渲染视觉场景、FFmpeg 合并音视频，输出 1920×1080 全高清视频。适用场景：项目文档视频化、教程制作、知识分享。
author: mengbin
version: "1.0.9"
homepage: https://clawhub.ai/skills/doc-to-video
keywords: [markdown, video, edge-tts, remotion, ffmpeg, tutorial, 文档视频化, 配音]
tags: [video, tutorial, automation, edge-tts, remotion, ffmpeg]
requirements:
  - python3
  - ffmpeg
  - node ≥ 18
  - pip (for edge-tts)
# v1.0.9 — add references/case-study-pattern.md (历史/安全案例复盘类内容 visual patterns: timeline/year-marker/attack-flow). 27 视频实测统计表 (L04-L30). 7-段项目 subagent 路由计数错误修复脚本. v1.0.8 后的发现 (subagent 写 JSX attribute 报错位置在 line:col, 不是整文件)
# v1.0.8 — references/batch-rendering.md 加 §9-§14 (6 个新坑): 复杂项目委派 ≤2 个、JSX 文本里 `<code>` 标签、长文压缩策略、skill 自我更新行为实测、17+ 视频磁盘管理、22 视频统计表
# v1.0.7 — references/batch-rendering.md §2 加 4 个 subagent 陷阱：600s 超时、JSX 字符串转义、`cp -R` 缺 out/、voice 系列化偏好
# v1.0.6 — add references/batch-rendering.md (subagent 委派 + 并行渲染 + 跳过第二遍 render 的 F[] 优化); Step 8 加 "skip-second-render" 快路径; 新增 ⚠️ 坑 "自动化工具偏向 non-binding helper, 不要 opinionated workflow"
# v1.0.5 — add references/second-video-pattern.md (cp -R 复用 + 4 新 visual patterns), references/syncing-to-openclaw.md (Hermes self-update 陷阱), SKILL.md Step 1.5 加"从已有项目派生"
# v1.0.4 — add templates/audio_frames.py (measure + frames 子命令)，templates/voice_test.py，Step 0 voice 试听流程，Step 4 替换为工具调用，macos-gotchas.md 加 §8.1 频谱分析辅助选 voice + §9 templates 索引
# v1.0.3 — add references/voice-swap-and-iterate.md: 换 voice / 改语速 / 改文本后的迭代工作流（含 F[] 整体缩放 vs 逐段重算、整体 atempo 误区）
# v1.0.2 — add Q8: edge-tts 48kbps MP3 硬上限 + voice 对比表 + macos-gotchas.md 对应小节
# v1.0.1 — fix ffmpeg concat path bug, add macOS Remotion Chrome gotcha, add fast-path (no atempo) when total audio already in target range, add references/ and templates/
---

# 🎬 Doc to Video：Markdown 文档转专业视频

> **Skill 名称**：doc-to-video
> **适用版本**：OpenClaw / QClaw / Hermes
> **技能类型**：文档 → 视频自动化
> **输出格式**：1920×1080 MP4，H.264 视频 + AAC 音频
|> **v1.0.6 修订**：加 `references/batch-rendering.md`（subagent 委派 + 并行渲染 + 跳过第二遍 render 的 F[] 优化）。Step 8 加"skip-second-render"快路径（如果 F[] 是从实测 audio 算的，**整遍"先 render → ffprobe → 改 F[] → 再 render"可以只跑第一步**——实测 5 个视频全部一次命中）。新加"工具设计原则"小节：non-binding helper vs opinionated workflow（用户偏好：helper 高，workflow 低）。
|> **v1.0.5 修订**：加 `references/second-video-pattern.md`（`cp -R` 复用 + 4 个新 visual patterns：CEI 时间线 / 双卡对比 / 4-file 列表 / 4-列对比表）和 `references/syncing-to-openclaw.md`（Hermes self-update 陷阱 + 可复用 sync 脚本）。SKILL.md Step 1.5 加"从已有项目派生"快路径。`voice-swap-and-iterate.md` 之外多了迭代 patterns 参考。
|> **v1.0.4 修订**：加 `templates/audio_frames.py`（measure + frames 子命令）替代手写 ffprobe 和 F[] 公式。加 `templates/voice_test.py` 把 6 voice 对比做成一行命令。Step 0 加 voice 试听流程，Step 4 用工具替代。`macos-gotchas.md` 加 §8.1 频谱分析辅助选 voice + §9 templates 索引表。配合 v1.0.3 的 `voice-swap-and-iterate.md`，换 voice 后的 F[] 重算一行命令完成。
|> **v1.0.3 修订**：加 `references/voice-swap-and-iterate.md` — 换 voice / 改语速 / 改文本后的完整迭代工作流（含 F[] 整体缩放 vs 逐段重算、整体 atempo 误区）
|> **v1.0.2 修订**：补 edge-tts 48kbps MP3 硬上限说明（Q8）—— 之前没说清楚"音听着别扭"的根因不是参数，是源端码率天花板
|> **v1.0.1 修订**：修 ffmpeg concat 路径 bug、补 macOS Remotion 渲染 gotcha、加"无需 atempo 加速"快路径、增加 references/ 和 templates/ 配套文件

将 Markdown 技术文档一键转换成带自然人声旁白的专业视频。
从内容分析、旁白编写、配音生成、视觉渲染，到音视频合并，全流程自动化。

---

## 📌 效果预览

本 Skill 已在 27 个真实项目中验证（详见末尾"Skill 开发过程记录"）：

| 视频类型 | 数量 | 场景数 / 个 | 文件大小 / 个 |
|---|---|---|---|
| Docker / Nomad 教程（原 3 个） | 3 | 9-16 | 3-6MB |
| Solidity 基础 7 个（L04-L10） | 7 | 8-9 | ~5-7MB |
| Solidity 进阶 5 个（L11-L15） | 5 | 9 | ~5-7MB |
| Solidity 安全 5 个（L16-L20） | 5 | 7-9 | ~5-7MB |
| Solidity 实战 5 个（L21-L25） | 5 | 8-9 | ~6-8MB |
| Solidity 项目 5 个（L26-L30，借贷/DAO/3 个安全案例复盘） | 5 | 7-9 | ~6-8MB |

> 27 个 TSP 系列视频实测（L04-L30）：总计 ~75 min / ~167MB，平均每个视频 2:46 / 6.2MB。
> 漂移范围 5-64ms（绝大多数 < 50ms）。
> 详细分段统计见 `references/batch-rendering.md` §14；安全案例复盘的视觉模式见 `references/case-study-pattern.md`。

> L04 详细见 `references/worked-example-tsp-solidity04.md`；同系列第二个起复用 `references/second-video-pattern.md`；批量 N 个 `references/batch-rendering.md`；换 voice / 改语速 `references/voice-swap-and-iterate.md`；Hermes ↔ OpenClaw sync `references/syncing-to-openclaw.md`；macOS 平台坑 `references/macos-gotchas.md`。

---

## 🔧 核心技术栈

```
Markdown 文档
     │
     ▼
┌─────────────────┐
│  edge-tts        │  ← 中文自然人声（Tingting/XiaoxiaoNeural）
│  Python 生成配音 │
└────────┬────────┘
         │ .m4a 音频文件
         ▼
┌─────────────────┐
│  FFmpeg atempo   │  ← 加速配音匹配目标时长
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Remotion        │  ← React 场景组件，TypeScript
│  视觉场景渲染     │     帧率 30fps，分辨率 1920×1080
└────────┬────────┘
         │ MP4 视频（无声）
         ▼
┌─────────────────┐
│  FFmpeg 合并     │  ← 去原音 + 嵌入配音
└────────┬────────┘
         │
         ▼
   带配音的 MP4 视频 ✅
```

---

## 📦 安装

### 方式一：一键安装（推荐）

```bash
skillhub install doc-to-video
```

> SkillHub 自动安装 Python 依赖（edge-tts）和 Node 依赖（Remotion）。

### 方式二：手动安装

```bash
# 1. 安装 Python 依赖
pip3 install edge-tts

# 2. 安装 FFmpeg
brew install ffmpeg        # macOS
apt install ffmpeg         # Ubuntu/Debian

# 3. 确认 Remotion 已安装在工作区
ls /Users/mac/.qclaw-oversea/workspace/node_modules/.bin/remotion
```

---

## 🚀 快速开始

### Step 0：选 voice 并试听（v1.0.4 新增）

> 选错 voice 是事后改起来最麻烦的——换 voice 会让总时长漂移几秒，触发 F[] 重算 + Remotion 重渲染，整个迭代 loop 多 4–5 分钟。**花 2 分钟在这里试听，能省后面 5 分钟。**

跑 `templates/voice_test.py` 生成 6 个候选 voice 的 9.5 秒样本：

```bash
python3 templates/voice_test.py
open /tmp  # Finder 打开，逐个点 voice_*.m4a 用 QuickTime 试听
```

> 📎 想自己改样本/候选 voice 列表？模板在 `templates/voice_test.py`（v1.0.4 加），改 SAMPLE 变量或 VOICES 列表即可。

**选 voice 时考虑：**

- 你的内容领域（技术教程 → 男声 Yunxi/Yunjian 通常更专业；知识科普 → 女声 Xiaoxiao 更亲切）
- 男女声频谱差别大：女声 centroid 3000–4000Hz 偏亮，男声 2500–3500Hz 偏温润
- 决定后记下来，下面 generate_audio.py 模板里 VOICE = "..." 就用它

### Step 1：创建工作目录

```bash
mkdir my-video-project && cd my-video-project
mkdir -p src audio out
```

### Step 1.5：从已有项目派生（v1.0.5 新增 — 第二个及之后视频）

> **如果是同系列的第二个视频**（同 voice、同作者、同代码风格），**别从头搭项目**。直接 `cp -R` 旧项目、删产物、改内容，比从 templates 重搭快 5-10 分钟。

```bash
cd ~/vscode
cp -R my-first-video-project my-second-video-project
cd my-second-video-project
rm -rf audio/* out/*.mp4 out/*.jpg node_modules package-lock.json build
npm install --no-audit --no-fund   # 3s，缓存命中
```

详见 `references/second-video-pattern.md`。

### Step 2：编写 `generate_audio.py`

```python
#!/usr/bin/env python3
"""生成各场景配音（edge-tts XiaoxiaoNeural）"""
import asyncio, edge_tts, os

SCENES = [
    ("00_title",    "欢迎观看本教程。本节介绍主要内容..."),
    ("01_chapter1", "第一章，首先介绍背景知识..."),
    ("02_chapter2", "第二章，讲解核心概念..."),
    # 更多场景...
]

VOICE = "zh-CN-XiaoxiaoNeural"
os.makedirs("audio", exist_ok=True)

async def gen(scene_id: str, text: str):
    m4a = f"audio/{scene_id}.m4a"
    if os.path.exists(m4a):
        print(f"  [skip] {scene_id}")
        return
    print(f"  → {scene_id}...")
    await edge_tts.Communicate(text, VOICE).save(m4a)
    print(f"    done")

async def main():
    await asyncio.gather(*[gen(sid, txt) for sid, txt in SCENES])
    print("\nAll done!")

asyncio.run(main())
```

### Step 3：生成配音

```bash
python3 generate_audio.py
```

### Step 4：测量各段音频时长（v1.0.4 用 audio_frames.py 替代手写 ffprobe）

> **第一次跑这个 skill 必看**：现在用 `templates/audio_frames.py` 的 `measure` 子命令，输出总时长和每段秒数。**还有保留功能**：同时输出 `F[]` 数组，可以直接粘到 `src/Scene.tsx`。

```bash
# 测各段时长 + 写到 scenes.json（供后续 frames 子命令用）
python3 templates/audio_frames.py measure --json-out scenes.json
```

输出形如：
```
📊 各段音频时长 (10 段)
  00_title     11.40s
  01_why       18.46s
  ...
  TOTAL      174.38s (2.91 min)

💾 写到 scenes.json
```

> 💡 **快路径提示**：总时长 170–185s 范围（目标 3 分钟左右）就**别用 atempo 加速**，直接拼到 Step 5 的命令。**总时长 < 165s 或 > 195s 走 atempo**（v1.0.1 加的快路径）。

### Step 5：拼接 + 加速音频

> ⚠️ **路径坑**（v1.0.1 修）：`ffmpeg -f concat` 的 demuxer 把 file_list.txt 里的路径解析为**相对列表文件所在目录**，不是 cwd。所以下面这种写法会报 "Impossible to open 'audio/audio/00_title.m4a'"：
>
> ```bash
> # ❌ 错误（路径重复 audio/）
> cat > audio/file_list.txt << 'EOF'
> file 'audio/00_title.m4a'
> file '01_chapter1.m4a'
> EOF
> ```
>
> 正确做法是切到 audio/ 下生成 list，路径用裸文件名：

```bash
# ✅ 正确：相对 audio/ 目录
cd audio
printf "file '00_title.m4a'\nfile '01_chapter1.m4a'\nfile '02_chapter2.m4a'\n" > file_list.txt
cd ..

# 必走 -c:a aac 重编码（-c copy 拼 m4a 会因 AAC bitstream 不一致失败）
ffmpeg -y -f concat -safe 0 -i audio/file_list.txt \
  -c:a aac -b:a 128k audio/combined.m4a

# 加速（示例：原始 360s → 目标 210s，加速比 1.714）
# 两级 atempo = sqrt(1.714) ≈ 1.31
ffmpeg -y -i audio/combined.m4a \
  -filter:a "atempo=1.31,atempo=1.31" \
  -c:a aac -b:a 128k audio/combined_final.m4a
```

> 💡 **快路径**（v1.0.1 新增）：如果拼接后总时长已经在 180–210s 范围内（目标 3–3.5 分钟），**跳过 atempo 加速**，零音质损失，命令直接用上面那个 `ffmpeg -y -f concat ... -c:a aac audio/combined.m4a` 即可。

### Step 6：编写 Remotion 场景组件

```tsx
// src/Scene.tsx
import React from "react";
import { useCurrentFrame } from "remotion";

function prog(t: number, s: number, d: number): number {
  return Math.min(1, Math.max(0, (t - s) / d));
}

// 精确帧边界（先渲染一次确认实际帧数后填入）
const F = [0, 266, 1096, 1780, 2730, 3545, 4093, 4610, 5215, 5715, 6130];

export const Scene: React.FC = () => {
  const f = useCurrentFrame();
  if (f < F[1])  return <CoverScene p={prog(f, 0, 40)} />;
  if (f < F[2])  return <Chapter1Scene p={prog(f, F[1], 40)} />;
  // ... 更多场景
  return <EndScene p={prog(f, F[F.length-1], 40)} />;
};
```

> 💡 **第二个视频起复用 visual patterns**：CEI 时间线 / 双卡对比 / 4-file 列表 / 4-列对比表，详见 `references/second-video-pattern.md` §"13 段视频的 4 个新 visual patterns"。

### Step 7：入口文件 `src/index.tsx`

```tsx
import React from "react";
import { Composition, registerRoot } from "remotion";
import { Scene } from "./Scene";

registerRoot(() => (
  <Composition
    id="MyVideo"
    component={Scene}
    durationInFrames={6295}   // 先填估算值，后续更正
    fps={30}
    width={1920}
    height={1080}
  />
));
```

### Step 8：渲染 + 合并

> ⚠️ **macOS 必看**（v1.0.1 新增）：Remotion 4.x 内置的 chrome-headless-shell 在 macOS 上有 sandbox/网络绑定问题。所有 `npx remotion render` 命令都必须加 `--browser-executable` 指向系统 Chrome：

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 第一次渲染：确认实际帧数
npx remotion render src/index.tsx MyVideo out/temp.mp4 \
  --browser-executable="$CHROME" --concurrency=2

# ffprobe 确认实际帧数
ffprobe -v error -select_streams v:0 \
  -show_entries stream=nb_frames -of csv=p=0 out/temp.mp4
# → 假设输出 6295，用此值更新 F[] 和 durationInFrames

# 重新渲染（用精确帧数）
npx remotion render src/index.tsx MyVideo out/final_video.mp4 \
  --browser-executable="$CHROME" --concurrency=2

# 合并音视频
ffmpeg -y -i out/final_video.mp4 -an -c:v copy /tmp/noaudio.mp4
ffmpeg -y -i /tmp/noaudio.mp4 -i audio/combined_final.m4a \
  -c:v copy -c:a aac -b:a 128k -shortest \
  out/final_with_audio.mp4

# 验证
ffprobe -v error -show_streams out/final_with_audio.mp4 \
  | grep -E "codec_type|duration"
```

Linux 上把 `--browser-executable="$CHROME"` 删掉即可。

> 🎯 **快路径（v1.0.6 新增 — 跳过第二遍渲染）**：如果你的 F[] 是用 `templates/audio_frames.py` 从**实测音频时长**算出来的（不是估算视频长度），那第一遍渲染的帧数 = 最终帧数。**整个"先 render → ffprobe → 改 F[] → 再 render"流程可以只跑第一步**。
>
> 适用条件（**两个都满足**才能跳过第二步）：
> 1. F[] 来自 `audio_frames.py frames --total N`（N = round(audio_total × 30)）
> 2. Remotion 渲染出的帧数 ≈ N（**没有**用会改变内容时长的 CSS 动画）
>
> 实测：5 个批量视频（tsp-solidity06–10）全部一次渲染命中目标，**省掉 5 次第二遍渲染 = 节省 ~25 分钟**。
>
> 不适用场景：用了 `transition: all 1s` 这类会延展内容时长的 CSS 动画——Remotion 可能渲染超过 `durationInFrames` 几帧，这种项目仍需两遍。
>
> 详见 `references/batch-rendering.md` §Step 3。

> 💡 **耗时预估**（M 系列 MacBook, concurrency=2）：
>
> | 总帧数 | 渲染时间 |
> |---|---|
> | ~4500 帧 (150s) | ~3 分钟 |
> | ~7000 帧 (235s) | ~5 分钟 |
> | ~9000 帧 (300s) | ~6-7 分钟 |
>
> 多视频批量时优先 **2-3 个 render 并行**（M 系列 64GB RAM 安全，详见 `references/batch-rendering.md` §Step 6）。

---

## 🔑 核心经验：音视频同步的坑与解法

### ❌ 错误做法（会导致不同步）

```
估算时长 → 计算帧边界 → 渲染 → 合并音频
          ↑ 用的是估算帧数，实际渲染帧数可能不同
```

Remotion 渲染的实际帧数不一定等于 `durationInFrames` 设置值！
因为 Remotion 按内容自动决定帧数，CSS 动画时长也会影响。

### ✅ 正确做法（两步确认法）

```
估算时长 → 渲染一次视频 → ffprobe 确认实际帧数
         ↓ 用实际帧数重新计算帧边界
       更新 F[] + durationInFrames → 重新渲染 → 合并
```

**帧边界计算公式：**
```
某场景开始帧 = round(该场景前累计秒数 / 音频总秒数 × 实际渲染总帧数)
```

> ⚠️ **占位 F[] 偏差实测**：第二个视频（tsp-solidity05）占位 F[] 算 7220 帧，实际需要 7100 帧（差 0.3%），但**每个场景的相对位置偏 5-10%**——t=60s 看到的不是 ThreeWays 场景而是 LowLevelScene。所以**第一遍渲染是 exploratory 的，不是浪费**，必须做。

**用 `templates/audio_frames.py` 算 F[]：**

```bash
# 拼接后用 ffprobe 拿总音频时长
TOTAL_S=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 audio/combined.m4a)

# 跑 frames 子命令算 F[]
python3 templates/audio_frames.py frames \
  --from-measure scenes.json \
  --total $(python3 -c "print(round($TOTAL_S * 30))")
# 直接复制输出的 F[] 到 src/Scene.tsx
```

### 为什么音频用 FFmpeg atempo 而不是 Remotion 内置？

Remotion 内置 `<Audio>` 组件依赖 React，在多场景场景下不稳定（报错 #130）。
FFmpeg atempo 无损加速，可精确控制时长，音质可控。

---

## 🎨 场景组件设计规范

### 布局原则

- 背景：深色渐变（`#0b1d3a → #1a3a6b`）或代码风格（`#0d1117`）
- 字体：标题 40–52px，内容 15–17px，等宽 13–14px
- 间距：水平留白 80–100px，垂直居中

### 动画原则

```tsx
// 动画进度 0→1（约 1–1.5 秒）
function prog(t: number, s: number, d: number): number {
  return Math.min(1, Math.max(0, (t - s) / d));
}
function ease(t: number) { return t * t; }

// 示例：渐入 + 上浮
<div style={{
  opacity: ease(p),                          // 0→1
  transform: `translateY(${(1-ease(p))*30}px)`, // 下→上 30px
}}>
```

### 推荐视觉组件

| 组件 | 场景 | 特点 |
|------|------|------|
| `CodeBlock` | 代码展示 | 黑色背景，蓝色文字，等宽字体 |
| `StepItem` | 步骤流程 | 彩色编号圆圈 + 文字说明 |
| `ProblemCard` | 问题排查 | 红色标题，原因+解决布局 |
| `BulletItem` | 要点列表 | 图标 + 内容 |
| `Tag` | 章节标签 | 圆角胶囊 + 光晕效果 |
| `VideoScene` | 场景容器 | 渐变背景 + 相对定位 |

### 第二个视频的 4 个新 visual patterns（v1.0.5）

详见 `references/second-video-pattern.md`：

- **CEI 时间线**（Checks-Effects-Interactions）：3 标签条 + 代码块
- **双卡对比**（delegatecall vs staticcall）：2 列并排
- **4-file 列表**（Foundry 项目结构）：2×2 grid，文件名 + 角色
- **4-列对比表**（策略选型）：每行 4 列：名称 / 安全评级 / 优点 / 风险

---

## 📂 项目结构示例

```
my-video-project/
├── generate_audio.py      # 配音生成脚本
├── src/
│   ├── index.tsx          # Remotion 入口
│   └── Scene.tsx          # 场景组件
├── audio/
│   ├── 00_title.m4a       # 各场景配音
│   ├── 01_chapter1.m4a
│   ├── ...
│   ├── combined_final.m4a # 拼接加速后完整音频
│   └── file_list.txt      # 拼接文件列表
└── out/
    ├── temp.mp4            # 首次渲染（确认帧数用）
    └── final_with_audio.mp4 # 最终输出
```

---

## ⚙️ 参数参考

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| 帧率 | 30 fps | 标准视频帧率 |
| 分辨率 | 1920×1080 | 16:9 全高清 |
| 目标时长 | 180–240 秒 | 3–4 分钟（实际取决于文章长度）|
| 加速比 | 1.3–2.0× | 过大影响音质 |
| atempo 级联 | 两级相乘≈目标加速比 | 每级不超过 2.0 |
| 每段旁白 | 100–300 字 | 对应场景内容 |
| 动画时长 | 30–40 帧 | ~1–1.3秒 |
| 音频码率 | 128k AAC | 清晰度与体积平衡 |
| 推荐 voice | zh-CN-YunxiNeural | 男声，有故事感，齿音最轻（v1.0.2 实测）|

---

## ❓ 常见问题

### Q1：音频比视频快（或慢）——最常见问题

**原因**：帧边界基于估算帧数，而非实际渲染帧数。

**解决：**
1. `ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of csv=p=0 out/video.mp4`
2. 用实际帧数重新计算所有帧边界
3. 更新 `index.tsx` 的 `durationInFrames` 和场景组件的 `F[]`
4. 重新渲染并合并

### Q2：Remotion 渲染报错 "useCurrentFrame() can only be called..."

**原因**：入口文件没有用 `Composition` API 注册。

**解决：**
```tsx
import { Composition, registerRoot } from "remotion";
registerRoot(() => (
  <Composition id="UniqueId" component={Scene}
    durationInFrames={6295} fps={30} width={1920} height={1080} />
));
```

### Q3：FFmpeg 合并后音频只有几 KB

**原因**：原视频有静音音频轨道，`-shortest` 保留了原轨道。

**解决：** 必须先用 `-an` 去掉原音：
```bash
ffmpeg -i video.mp4 -an -c:v copy noaudio.mp4
ffmpeg -i noaudio.mp4 -i audio.m4a -shortest output.mp4
```

### Q4：atempo 加速后人声变调

**原因**：单级 atempo 超过 2.0。

**解决：** 两级级联，例如 3.5x：`atempo=1.87,atempo=1.87`

### Q5：edge-tts 无网络

**备选：** macOS 系统语音 `say -v Tingting -r 175 "旁白内容"`
转 MP3：`ffmpeg -i audio.aiff -codec:a libmp3lame -qscale:a 2 audio.mp3`
（注意：音质远不如 edge-tts）

### Q6：ffmpeg concat 报 "Impossible to open 'audio/audio/00_title.m4a'"（v1.0.1 新增）

**原因**：`file_list.txt` 里写 `file 'audio/xxx.m4a'`，但 ffmpeg 的 concat demuxer 是相对**列表文件所在目录**解析路径的，不是相对当前工作目录。所以正确写法是去掉 `audio/` 前缀。详见 Step 5 里的注释。

### Q7：macOS 上 Remotion 渲染报 `spawn Unknown system error -88` 或 `Visited "http://localhost:3000/index.html" but got no response`（v1.0.1 新增）

**原因**：Remotion 4.x 自带的 chrome-headless-shell 在 macOS 上有 sandbox/网络绑定问题。

**解决**：用系统安装的 Google Chrome 替代内置 headless-shell，详见 Step 8。

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
npx remotion render src/index.tsx MyVideo out/temp.mp4 \
  --browser-executable="$CHROME"
```

### Q8：edge-tts 出来的配音"听着别扭"——女声有金属感/齿音（v1.0.2 新增）

**根因**：edge-tts 服务端**只输出 48kbps MP3 / 24kHz / mono**，无论 voice/rate/pitch 怎么设都一样。这是 Microsoft 服务的硬上限，不是配置问题。`ffprobe` 验证：

```bash
ffprobe -v error -show_streams audio/combined.m4a | grep -E "codec_name|sample_rate|bit_rate"
# codec_name=aac
# sample_rate=24000
# bit_rate=102029   # 上限就是 ~96–102k AAC，源是 48k MP3，再怎么重编码也回不去
```

**别浪费时间在以下方向**（都不会改善音质）：
- 改 rate/pitch 参数
- 把 AAC 码率从 128k 提到 192k/256k —— 源码就 48k，徒增文件大小
- `aresample=48000` 升采样 —— 0 新增信息，徒增体积

**真正能改善音质的路径**（按代价从小到大）：

1. **换 voice**（零成本，立刻可试）。Xiaoxiao 是默认最自然的，但 48k MP3 暴露齿音最明显。备选：
   - `zh-CN-YunxiNeural` — 男声，有故事感，最不像"机器女声"
   - `zh-CN-XiaoyiNeural` — 女声，柔和，齿音最轻
   - `zh-CN-YunyangNeural` — 男声，新闻播报腔，正式感强
   - `zh-CN-YunjianNeural` — 男声，活力感
   改 `generate_audio.py` 里的 `VOICE` 常量，重跑 `python3 generate_audio.py`。

2. **用 macOS 系统 `say`**（离线，零网络，音质比 edge-tts 48k MP3 略好但风格明显不同）：
   ```bash
   say -v Tingting -r 175 -o chapter01.aiff "旁白内容"
   ffmpeg -i chapter01.aiff -codec:a libmp3lame -qscale:a 2 chapter01.mp3
   ```
   见 Q5 的"备选"分支。

3. **换 TTS 引擎**（音质跃迁，但配置成本高）：
   - **Azure TTS**（付费，按字符计费）— 同源模型但提供 48k/96k/192k MP3 和 16k/24k/48k PCM，齿音明显改善
   - **CosyVoice / GPT-SoVITS**（本地开源）— 自带训练或微调能力，可克隆特定声音
   这些都需要单独接 API 或装额外服务，不在本文档覆盖范围。

**经验法则**：先试换 voice（5 分钟），不行再上 macOS `say`（半小时试出风格差异），最后才考虑换引擎。

**换 voice 后的重新同步流程**（重新生成音频 → 重渲染 Remotion → 合并），见 `references/voice-swap-and-iterate.md`。该流程中算 F[] 的 python 代码已抽到 `templates/audio_frames.py` 的 `frames` 子命令：

```bash
# 第二次渲染后用 ffprobe 拿到实际帧数，例如 4471
ACTUAL=$(ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of csv=p=0 out/final_video.mp4)

# 自动从 scenes.json 算新 F[]
python3 templates/audio_frames.py frames --from-measure scenes.json --total $ACTUAL
# 直接复制输出的 F[] 到 src/Scene.tsx，复制 DURATION_IN_FRAMES 到 src/index.tsx
```

### Q9：Remotion 报 `The character ">" is not valid inside a JSX element`（v1.0.9 新增）

**症状**：L23 Section3.tsx:40:66 渲染时 esbuild 报错，定位到某一行。错误信息里的 **line:col 是**esbuild 看到的源码位置**，比 React 编译器报的位置更准。

**根因**：subagent 在 JSX 文本节点（夹在两个标签之间的普通文字）里嵌了 JSX 标签，比如：

```tsx
<div>
  ERC1155 用一张 <code style={{color: "#f0883e"}}>(id → balance)</code> 表管理所有 token 类型。
</div>
```

JSX 解析器看到 `<code>` 试图匹配 JSX 元素，但这是**文本节点位置**，不是合法的 JSX 语法位置。`>` 被识别为标签闭合，触发 parse error。

**修复**：用全大写或反引号替代：

```tsx
<div>
  用一张映射表 (id → balance) 管理所有 token 类型。
</div>
```

**预防**（写 subagent prompt 时显式禁）：见 `references/batch-rendering.md` §10。

---

## 📂 配套 references 索引

| 文档 | 用途 |
|---|---|
| `references/worked-example-tsp-solidity04.md` | 第一个视频（10 段）端到端实例 |
| `references/second-video-pattern.md` | 第二个及之后视频的 `cp -R` 复用 + 4 个新 visual patterns |
| `references/voice-swap-and-iterate.md` | 换 voice / 改语速 / 改文本后的 F[] 重算 |
| `references/syncing-to-openclaw.md` | Hermes ↔ OpenClaw 两端 sync（self-update 陷阱） |
| `references/batch-rendering.md` | **N 个视频批量 pipeline**（v1.0.6 新增）：subagent 委派 + 并行渲染 + 跳过第二遍 render |
| `references/macos-gotchas.md` | macOS 平台专项坑（Remotion Chrome、ffmpeg 路径等）|
| `references/case-study-pattern.md` | **历史 / 安全案例复盘类**内容的 visual patterns：timeline、year-marker、attack-flow、response phases（v1.0.9 新增）|

---

## ⚠️ 工具设计原则：non-binding helper，not opinionated workflow（v1.0.6 新增）

> 这是用户的明确偏好，提炼出来避免下次跑偏。

设计新工具时，**默认做"非绑定 helper"**，**不做"opinionated workflow"**：

| 类型 | 例子 | 用户接受度 |
|---|---|---|
| ✅ **non-binding helper** | `audio_frames.py measure/frames` —— 一个 Python 工具，根据调用方式自由组合 | 高，跑了 7 个项目都好用 |
| ✅ **deterministic wrapper** | `merge.sh` —— 单一动作的固定脚本（音频合并），不试图"全流程" | 高，方便复制 |
| ⚠️ **opinionated workflow** | "批量化项目脚手架脚本" —— 一键从 0 到 mp4，假设了 npm/voice/项目结构 | **低**，用户反馈"加了之后就不通用了" |

**判断标准**：
- 工具是**回答一个问题**（"F[] 怎么算"）还是**执行一个完整流程**（"从 md 到 mp4"）？
- 前者：✅ helper
- 后者：⚠️ workflow — 需要用户**先认同**流程的所有假设才有用

**反模式**：把"npm install 自动化 + 项目结构约定 + 默认 voice + 默认 F[] 算法"打包成一个 `new-project.sh`——如果用户的下一个项目用 pnpm / 不同的 voice / 不同的场景命名，这脚本就成了阻力。

**该做的**：保持每个工具的小而专一（一个工具 = 一个职责），让用户用 `bash` / `make` / `invoke` 自由组合。

---

## 📤 发布到 SkillHub / ClawHub

### 发布前准备

1. 确保 `SKILL.md` 包含完整的 frontmatter（name, description, author, version, tags 等）
2. Skill 目录结构清晰，文件命名规范
3. 准备好封面图（可选，512×512 PNG）

### SkillHub（推荐）

访问 [https://clawhub.ai](https://clawhub.ai)：

1. **注册/登录** ClawHub 账号
2. 点击 **「Publish Skill」** 或 **「Submit」**
3. 填写信息：
   - **Skill Name**: `doc-to-video`
   - **Description**: `将 Markdown 技术文档自动转换成带配音旁白的专业视频`
   - **Category**: `Video & Media` 或 `Automation`
   - **Tags**: `markdown, video, edge-tts, remotion, ffmpeg, tutorial`
   - **Author**: 你的昵称或机构名
4. 上传文件：
   ```
   skill-doc-to-video/
   ├── SKILL.md              ← 必须
   ├── generate_audio.py     ← 推荐一起打包
   └── preview.png           ← 可选封面图
   ```
5. 点击提交，等待审核通过

### ClawHub（原生）

如果 ClawHub 支持 CLI 发布：

```bash
# 方式一：直接推送目录
npx clawhub publish ./skill-doc-to-video

# 方式二：登录后推送
clawhub login
clawhub publish --name doc-to-video --dir ./skill-doc-to-video
```

---

## 🧠 Skill 开发过程记录

本 Skill 并非一步到位，而是通过多次迭代逐步完善：

### 第一版：基础流程

**思路**：Remotion 渲染视频 → 用 FFmpeg 合并配音
**问题**：音频与视频不同步，因为帧边界计算有误

### 第二版：加入精确帧计算

**思路**：渲染一次视频，用 ffprobe 确认实际帧数，再反推边界
**问题**：确认帧数是对的，但渲染出来的帧数与预期仍有偏差

### 第三版（最终）：两步确认法 + FFmpeg 嵌入音频

**核心发现**：
- Remotion `durationInFrames` 是参考值，实际帧数由内容决定
- 必须先渲染 → ffprobe 确认 → 再算边界 → 更新代码 → 重渲染
- `<Audio>` 组件在 Remotion 中不稳定，改用 FFmpeg 直接嵌入音频

**最终流程（固化在本 Skill 中）：**
```
Markdown → 旁白 → edge-tts → 拼接加速
  → 渲染确认帧数 → ffprobe 实测 → 精确帧边界
  → 重渲染 → FFmpeg 嵌入音频 → 完成
```

**5 个原始验证项目（v1.0.0）：**
1. `docker-registry-guide-final.mp4` — 9场景，153s ✅
2. `deploy-docker-registry-final.mp4` — 16场景，207s ✅
3. `solidtidy-final.mp4` — 11场景，210s，音视频完美同步 ✅

**TSP 系列扩展（v1.0.5+）：**
4. `tsp-solidity04-final.mp4` — 10场景，178.9s，Yunxi 男声 ✅
5. `tsp-solidity05-final.mp4` — 13场景，236.7s，Yunxi 男声，13 个新 visual pattern ✅

**TSP 完整 27 视频系列（v1.0.9）**：

- L04-L25 共 22 个（v1.0.8 截止）
- L26-L30 新增 5 个：借贷 SimpleLending / DAO SimpleDAO / The DAO Hack 2016 复盘 / Parity Wallet Hack 2017 复盘 / Nomad Bridge Hack 2022 复盘
- 27 个视频总计 ~75 min / ~167MB，**漂移全部 < 70ms**
- 安全案例复盘类内容（28-30）触发了**新视觉模式**需求，沉淀到 `references/case-study-pattern.md`
- **L23 JSX 文本节点里嵌 `<code>` 标签的踩坑**（详见 batch-rendering.md §10）— 这条之前没在 SKILL.md 主文档里出现，作为 v1.0.9 的新坑点补充到主文档
- **L26/L27 7-段项目 Scene.tsx 路由计数错误**（subagent 写 8 routes for 7 audio）—— 修复脚本模板固化到 batch-rendering.md §6

**TSP 完整 22 视频系列（v1.0.8）**：

- L04-L25 全 22 个视频，全部使用 YunxiNeural 男声，10 万+ 字文档转 65 分钟视频
- 总大小 ~138MB，平均每视频 6.3MB
- 漂移全部 < 50ms（实测最大值 L14 = 64ms）
- 5 个实测 batch run (L06-10, L11-15, L16-20, L21-25) 总耗时约 1.5 小时
- **生产环境可用**：v1.0.6 之后的项目都是"一次渲染命中"，没有需要重渲染的情况

---

## 📄 许可

MIT License — 可自由使用、修改、分发。
