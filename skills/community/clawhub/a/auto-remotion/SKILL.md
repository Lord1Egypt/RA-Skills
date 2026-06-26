---
name: auto-remotion
description: |
  从已有录屏/产品演示视频生成官网宣传片的工作流。

  当用户提到以下场景时触发：
  - "把录屏转成宣传片"、"用录屏做产品视频"
  - "把演示视频做成官网介绍"
  - "Remotion 切片"、"视频分镜"
  - "产品宣传视频生成"、"screen recording to promo video"
  - "多个视频合并成宣传片"、"产品视频剪辑"
  - 用户想用 Remotion 把长视频切成短片段做宣传片

  本技能覆盖从原始录屏素材到完整 Remotion 宣传片的完整流程：
  环境准备 → 目标确认 → 素材识别（人工/自动）→ 分镜策划 → 结构化规格 → Remotion 实现
  → 字幕轨 → 中文配音（edge-tts）→ BGM → 渲染出片

  每个阶段都有具体检查清单、常见问题和决策框架。

  **本 skill 不适用的情况**（见"不适用场景"章节）：
  - 从技术文档/幻灯片生成视频（无源视频素材）
  - 需要 AI 生成视频画面本身（仅处理已有素材的剪辑组合）
---

## 云端链接

- **GitHub**: https://github.com/16Miku/auto-remotion
- **ClawHub**: https://clawhub.ai/16miku/auto-remotion

---

## 核心理念

这条工作流的核心不是"让 AI 替代人工"，而是：

> **把人工判断和自动化工具各自放在最合适的位置。**
> 人工判断哪些画面有价值，工具负责把价值组合成视频。

**执行顺序很重要**：
1. 先锁定素材区间
2. 再锁定段落结构
3. 再锁定总时间线
4. 最后才叠加字幕、配音、BGM、包装

违反这个顺序，会导致大量返工。

---

## 快速启动（3 分钟理解全局）

**对于 AI Agent / 自动化脚本，使用非交互式创建**：

```bash
npx create-video --yes --blank --no-tailwind my-video
```

**对于手动操作**：
```bash
npx create-video@latest
# 交互式选择 Blank 模板
```

**典型对话节奏**：
- 用户：录屏 20 分钟 → 宣传片 60 秒
- 执行顺序：先看素材定结构，再动手写代码

---

## 阶段零：环境准备

### 0.1 创建 Remotion 项目

**交互式创建**（手动操作时）：
```bash
npx create-video@latest
# 选择模板：Blank（空白模板）
```

**非交互式创建**（AI Agent / 脚本时）：
```bash
npx create-video --yes --blank --no-tailwind my-video
```

可用模板 flags：
| Flag | 模板 |
|------|------|
| `--blank` | 空白画布（推荐） |
| `--hello-world` | Hello World 动画 |
| `--javascript` | 纯 JavaScript 版 |
| `--recorder` | 录屏工具 |
| `--still` | 静态图片模板 |
| `--overlay` | 视频叠加层 |
| `--audiogram` | 音频可视化 |
| `--prompt-to-video` | AI 文字生视频 |

**重要 flags**：
- `--yes` / `-y`：跳过所有交互提示（AI Agent 必须）
- `--no-tailwind`：不安装 TailwindCSS
- `--tmp`：在临时目录创建

### 0.2 安装依赖

```bash
cd my-video
npm install
```

### 0.3 启动开发服务器

```bash
npm run dev
```

同时在另一个终端启动 Claude Code：

```bash
cd my-video
claude
```

### 0.4 安装 ClawHub CLI（可选）

如需发布技能或管理注册表认证，可安装独立 clawhub CLI：

```bash
npm i -g clawhub
# 或
pnpm add -g clawhub
```

### 0.5 安装 remotion-video-toolkit skill（可选）

**本 skill（auto-remotion）与 remotion-video-toolkit 是不同的 skill：**

- **auto-remotion**：本 skill，专注"从录屏到宣传片"的完整剪辑工作流，覆盖需求确认→素材识别→Remotion 实现→配音字幕→BGM→渲染出片
- **remotion-video-toolkit**：ClawHub 上的另一个 skill，29 条规则，专注 Remotion API 使用、动画特效、渲染管道等技术细节

两者可互补使用。如果需要 remotion-video-toolkit 辅助开发：

**方式一：使用 openclaw 原生命令（推荐）**

```bash
openclaw skills install remotion-video-toolkit
```

**方式二：使用 clawhub CLI**

```bash
npx clawhub@latest install remotion-video-toolkit --force
```

该 skill 包含 29 条规则，覆盖：
- 动画、时序、渲染（CLI/Node.js/Lambda/Cloud Run）
- 字幕、3D、图表、文字特效、转场、媒体处理

**注意**：`npx skills add remotion-dev/skills` 是安装 **remotion-best-practices** skill 的方式，与 remotion-video-toolkit 是完全不同的 skill。

**方式三：从本地路径安装（安装 **remotion-best-practices**）**

```bash
npx skills add remotion-dev/skills
```

安装时选择：
- Agent 类型：Claude Code 或当前使用的 Agent
- 安装范围：全局安装（global）

**注意**：`npx skills add remotion-dev/skills` 安装的是 **remotion-best-practices**，与 auto-remotion 和 remotion-video-toolkit 都是完全不同的 skill。

### 0.6 环境检查清单

| 检查项 | 命令 | 预期结果 |
|--------|------|---------|
| Node.js | `node --version` | ≥ 18 |
| npm | `npm --version` | ≥ 9 |
| Remotion CLI | `npx remotion --version` | 显示版本号 |
| 开发服务器 | `npm run dev` | localhost:3000 可访问 |

---

## 阶段一：明确目标与约束

在动手之前，先对齐：

1. **输入是什么**：录屏、直播录屏、剪辑素材包，还是多段演示视频？
2. **输出是什么**：官网宣传片、产品介绍、销售演示，还是社媒短视频？
3. **时长目标**：严格 60 秒、可浮动到 70 秒，还是优先完整表达？
4. **核心价值**：产品能力、用户体验、结果展示，还是品牌感？
5. **哪些后置**：字幕、配音、BGM 放到第二阶段？

如果约束不先说清楚，后面会在"要不要保留完整结果""能不能接受更长"这类问题上反复拉扯。

---

## 阶段二：建立结构化中间产物

不要直接写代码。先建立以下文件：

### 2.1 剪辑执行稿（`.md`）

按 Segment 分解，每段包含：
- 目标 / 画面描述 / 屏幕文案 / 旁白 / Remotion 对接建议
- 这是讨论和审阅的基础

### 2.2 分镜表（`storyboard.json`）

```json
{
  "compositionId": "MyPromoV1",
  "fps": 30,
  "durationInFrames": 1800,
  "canvas": "1920x1080",
  "segments": [
    {
      "segmentId": "SegmentIntro",
      "segmentIndex": 0,
      "startFrame": 0,
      "durationFrames": 150,
      "goal": "片头引入，30字内概括价值",
      "text": { "eyebrow": "", "title": "", "body": "" },
      "narration": "产品名，让 AI 完成真实任务。",
      "clip": null,
      "overlay": "top-bar"
    }
  ]
}
```

### 2.3 编辑规格（`edit-spec.json`）

帧级时间线，包含真实素材区间和速度：

**单视频源**：
```json
{
  "compositionId": "MyPromoV1",
  "fps": 30,
  "durationInFrames": 1800,
  "sourceVideo": { "path": "./public/source.mp4" },
  "segments": [
    {
      "segmentId": "SegmentIntro",
      "startFrame": 0,
      "durationFrames": 150,
      "clips": []
    }
  ]
}
```

**多视频源**（`clips[]` 中指定 `src`）：
```json
{
  "compositionId": "MyPromoV1",
  "fps": 30,
  "durationInFrames": 1800,
  "sourceVideos": [
    { "id": "video-a", "path": "./public/product-demo.mp4" },
    { "id": "video-b", "path": "./public/user-review.mp4" }
  ],
  "segments": [
    {
      "segmentId": "SegmentIntro",
      "startFrame": 0,
      "durationFrames": 150,
      "clips": [
        { "src": "video-a", "start": 10.5, "end": 15.2, "playbackRate": 1 }
      ]
    },
    {
      "segmentId": "SegmentFeature",
      "startFrame": 150,
      "durationFrames": 300,
      "clips": [
        { "src": "video-b", "start": 0, "end": 8.5, "playbackRate": 1 }
      ]
    }
  ]
}
```

---

## 阶段三：识别母视频时间点

这一步是整个链路的核心桥梁。

**不要跳过**。即使有 AI 视频理解能力，在 MVP 阶段人工识别仍然最快。

推荐做法：
1. 用户（或你引导用户）观看原视频，给出粗粒度内容分区
2. 在粗粒度分区中细化为可剪辑时间点
3. 区分"价值展示片段"和"过程等待片段"
4. 用结构化表格记录所有时间点

**关键原则**：
- 对话类片段要确保"输入→发送→回复出现"的因果链完整
- 长任务演示不要只靠整体快进，要拆成"发起/执行/结果/成果展示"多个叙事节点
- 真实切片时间点以**分**为单位记录（`4:16` 而不是 `4.267`）

---

## 阶段三补充：自动视频理解（可选）

> 本章节借鉴 [video-use](https://github.com/browser-use/video-use) 项目。如需实现 Agent 自动化剪辑，建议启用本流程。

### 3.1 核心思想：让 LLM 读视频，而不是看视频

传统方式（纯人工）：
```
人工看视频 10-20min → 人工标记时间点 → 人工判断价值 → 人工规划分镜
```

自动化方式（基于转录）：
```
视频 → 转录文本（1-2min）→ LLM 阅读转录（10s）→ 自动识别有价值片段 → 自动生成分镜
```

**关键洞察**：用转录文本把视频"文本化"，LLM 擅长处理文本，就能自动化原本需要人工判断的决策。

---

### 3.2 两段式视频理解架构

| 层 | 方式 | 代价 |
|----|------|------|
| **音频转录层** | ElevenLabs Scribe 词级时间戳 | ~12KB/小时视频 |
| **视觉合成层** | 按需生成 filmstrip + waveform PNG | 仅在决策点生成 |

LLM 从不直接处理视频帧，而是读取"文本化的视频信息"。这样把 ~45M tokens（逐帧 dump）压缩到 ~12KB + 少量 PNG。

---

### 3.3 转录管道

**依赖安装**：

```bash
pip install -e video-use/helpers
# 或独立安装
pip install requests librosa matplotlib pillow numpy
```

**核心脚本**：

| 脚本 | 功能 |
|------|------|
| `transcribe.py` | ElevenLabs Scribe 转录，输出词级时间戳 JSON |
| `pack_transcripts.py` | 把 JSON 打包成 `takes_packed.md`（phrase 级） |
| `timeline_view.py` | 按需生成 filmstrip + waveform PNG |

**转录命令**：

```bash
# 单文件
python helpers/transcribe.py <video_path>

# 批量（4 并行）
python helpers/transcribe_batch.py <videos_dir>

# 打包成 takes_packed.md
python helpers/pack_transcripts.py --edit-dir <edit_dir>
```

---

### 3.4 takes_packed.md 格式

这是 LLM 阅读视频内容的主要 artifact。格式示例：

```markdown
# Packed transcripts

## C0103  (duration: 43.0s, 8 phrases)
  [002.52-005.36] S0 Ninety percent of what a web agent does is completely wasted.
  [006.08-006.74] S0 We fixed this.
```

**生成规则**：
- 按静音 ≥ 0.5s 或说话人切换切分 phrase
- 每个 phrase 带有 `[start-end]` 时间戳
- 包含音频事件标记：`(laughs)`、`(sighs)`、`(applause)`

---

### 3.5 LLM 自动分镜

给定 `takes_packed.md`，LLM 可直接生成分镜：

```json
[
  {"source": "C0103", "start": 2.42, "end": 6.85,
   "beat": "HOOK", "quote": "Ninety percent...", "reason": "Cleanest delivery"},
  {"source": "C0103", "start": 14.30, "end": 28.90,
   "beat": "SOLUTION", "quote": "We fixed this", "reason": "Only take without false start"}
]
```

**Editor sub-agent prompt 要点**：
- 输入：takes_packed.md + 用户上下文 + 目标时长
- 输出：JSON 数组，带 source/start/end/beat/quote/reason
- 规则：切点必须在词边界、30-200ms pad、优先 ≥400ms 静音

---

### 3.6 timeline_view：按需可视化

在 LLM 判断模糊时，生成可视化确认：

```bash
python helpers/timeline_view.py <video> <start> <end> -o out.png
```

输出：filmstrip + waveform + word labels PNG

**使用原则**：只在决策点使用，不是全程扫描工具。

---

## 阶段四：Remotion 骨架搭建

### 4.1 项目结构约定

```
remotion-app/
├── public/              ← 所有源素材放这里（视频、音频、图片）
│   ├── source.mp4      ← 源视频（单视频场景）
│   ├── video-a.mp4     ← 多视频场景：来源视频 A
│   ├── video-b.mp4     ← 多视频场景：来源视频 B
│   ├── voiceover.mp3   ← 配音
│   └── bgm.mp3         ← BGM
├── src/
│   ├── Composition.tsx  ← 主 composition（含所有 Segment 组件）
│   └── Root.tsx        ← composition 注册
└── package.json
```

**所有源素材必须放 `public/`，用 `staticFile("文件名")` 引用。**

### 4.2 视频切片工具函数

**单视频源**（默认）：

```tsx
type ClipSpec = {
  trimBeforeFrames: number;
  trimAfterFrames: number;
  playbackRate: number;
};

const clip = (
  startSeconds: number,
  endSeconds: number,
  playbackRate = 1
): ClipSpec => ({
  trimBeforeFrames: Math.round(startSeconds * 30),
  trimAfterFrames: Math.round(endSeconds * 30),
  playbackRate,
});

// 高倍速片段务必 muted
<Video
  src={videoSrc}
  muted                      // ← 超过 10x 强烈建议 muted
  trimBefore={trimBeforeFrames}
  trimAfter={trimAfterFrames}
  playbackRate={playbackRate}
  style={{ width: "100%", height: "100%", objectFit: "cover" }}
/>
```

**多视频源**：传入视频文件标识符：

```tsx
type ClipSpec = {
  trimBeforeFrames: number;
  trimAfterFrames: number;
  playbackRate: number;
  src?: string;  // ← 可选：指定来源视频（默认为主视频）
};

// 不同 Segment 使用不同来源视频
const clipA = clip(10, 15, 1);           // 来自 source-a.mp4
const clipB = clip(5, 12, 1, "source-b.mp4"); // 来自 source-b.mp4

<Video
  src={staticFile(clipA.src || "source-a.mp4")}
  muted
  trimBefore={clipA.trimBeforeFrames}
  trimAfter={clipA.trimAfterFrames}
  playbackRate={clipA.playbackRate}
  style={{ width: "100%", height: "100%", objectFit: "cover" }}
/>
```

### 4.3 Sequence 嵌套与时长管理

**父子 Sequence 时长是关键原则**：

> 外层 Sequence 的 `durationInFrames` 必须足够容纳所有子片段的总时长。

如果子片段时长总和超过父级，会发生截断（子片段被砍掉尾部）。

```tsx
// 正确示例
<Sequence from={840} durationInFrames={606}>  {/* ← 必须 ≥ 所有子片段之和 */}
  <SegmentModules />
</Sequence>
```

### 4.4 TypeScript 踩坑清单

| 错误写法 | 正确写法 |
|---------|---------|
| `<AbsoluteFill pointerEvents="none">` | `<AbsoluteFill style={{ pointerEvents: "none" }}>` |
| `<Video style={{ objectFit: "cover" }}>` | `<Video objectFit="cover">` |
| `playbackRate={0}` | 不支持，改为纯色背景 |
| `import JSON from "./data.json"` | 内联为 TypeScript 常量数组 |

---

## 阶段五：字幕轨接入

### 5.1 字幕数据结构

字幕 cue 用**左闭右开**区间 `[startFrame, endFrame)`：

```tsx
type SubtitleCue = {
  cueId: string;
  segmentId: string;
  startFrame: number;  // 包含
  endFrame: number;    // 不包含
  text: string;
};

const activeCue = subtitleCues.find(
  (cue) => frame >= cue.startFrame && frame < cue.endFrame
);
```

### 5.2 渲染组件

```tsx
const SubtitleTrack: React.FC = () => {
  const frame = useCurrentFrame();
  const activeCue = subtitleCues.find(
    (cue) => frame >= cue.startFrame && frame < cue.endFrame
  );
  if (!activeCue) return null;

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{
        position: "absolute", left: 140, right: 140, bottom: 42,
        display: "flex", justifyContent: "center",
      }}>
        <div style={{
          maxWidth: 1080, padding: "16px 24px", borderRadius: 22,
          background: "rgba(5, 8, 22, 0.72)", color: "white",
          fontSize: 28, textAlign: "center",
        }}>
          {activeCue.text}
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

---

## 阶段六：中文配音（edge-tts）

### 6.1 流程

```
voiceover-script.json（结构化旁白文本）
    → edge-tts 生成各段 MP3
    → ffmpeg 合并（每段后加静音填充对齐目标帧时长）
    → 放入 public/
    → <Audio src={staticFile("voiceover.mp3")} /> 接入 Composition
```

### 6.2 静音填充是关键

**不能假设配音自然时长等于目标帧时长。**

edge-tts 按自然语速生成，每句实际时长和目标帧时长必然有偏差（可能 ±0.5-2 秒）。直接合并会导致：
- 配音总时长比视频短
- 后半段 Segment 没有配音
- 字幕和配音完全错位

**正确做法**：每段配音后测量实际时长，用 `anullsrc` 生成静音填充到目标秒数：

```bash
# 生成静音
ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t 2.5 -q:a 9 silence.mp3
# 合并
ffmpeg -f concat -safe 0 -i concat_list.txt -acodec libmp3lame output.mp3
```

### 6.3 配音生成脚本示例

实际项目中使用的 Python 脚本结构（`generate_voiceover_v2.py`）：

```python
import asyncio
import edge_tts
import subprocess
import json
import os

FFMPEG = "A:/study/AI/LLM/browser-use-cli-test/remotion-app/node_modules/@remux/compositor-win32-x64-msvc/ffmpeg.exe"

async def generate_segment(seg: dict, output_dir: str):
    """生成单段配音 + 静音填充"""
    target_sec = seg["targetSec"]
    output_path = os.path.join(output_dir, f"vo_{seg['id']}.mp3")

    # 1. 生成配音
    communicate = edge_tts.Communicate(seg["text"], "zh-CN-XiaoxiaoNeural")
    seg_path = os.path.join(output_dir, f"seg_{seg['id']}.mp3")
    await communicate.save(seg_path)

    # 2. 测量实际时长
    probe = subprocess.run([
        FFMPEG, "-i", seg_path, "-hide_banner"
    ], capture_output=True, text=True)
    # 解析输出获取时长，或使用 ffprobe 精确测量
    actual_dur = measure_duration(seg_path)  # 自定义函数

    # 3. 计算静音填充
    silence_sec = target_sec - actual_dur
    if silence_sec > 0.05:
        silence_path = os.path.join(output_dir, f"silence_{seg['id']}.mp3")
        subprocess.run([
            FFMPEG, "-f", "lavfi",
            "-i", f"anullsrc=r=24000:cl=mono",
            "-t", str(silence_sec),
            "-q:a", "9",
            silence_path
        ])
        # 4. 合并配音 + 静音
        concat_file = os.path.join(output_dir, f"concat_{seg['id']}.txt")
        with open(concat_file, "w") as f:
            f.write(f"file '{seg_path}'\n")
            f.write(f"file '{silence_path}'\n")
        subprocess.run([
            FFMPEG, "-f", "concat", "-safe", "0",
            "-i", concat_file, "-acodec", "libmp3lame", output_path
        ])
    else:
        os.rename(seg_path, output_path)

async def main():
    with open("voiceover-script.json") as f:
        segments = json.load(f)
    for seg in segments:
        await generate_segment(seg, "output_dir")
    # 最后用 ffmpeg concat 合并所有段
    subprocess.run([FFMPEG, "-f", "concat", "-safe", "0",
                    "-i", "final_concat.txt", "-acodec", "libmp3lame",
                    "remotion-app/public/voiceover.mp3"])

asyncio.run(main())
```

### 6.4 中文语音选项

| Voice | 特点 | 适用场景 |
|-------|---|---|
| `zh-CN-XiaoxiaoNeural` | 专业女声，清晰流畅 | 产品介绍（本次选用） |
| `zh-CN-YunxiNeural` | 年轻男声，有点活泼 | 科技产品演示 |
| `zh-CN-YunjianNeural` | 阳刚男声 | 强技术感，专业工具 |

### 6.5 配音与时间线匹配策略

微调顺序：
1. 先调文字内容长度
2. 次调语速（`rate` 参数）
3. 最后才改 Segment 时长（因为改时长会影响所有子片段基准）

---

## 阶段七：BGM 接入

### 7.1 来源

Pixabay Music（商用免费，无需署名）
关键词：`"light technology"`、`"corporate tech"`

### 7.2 动态音量接入

```tsx
<Audio
  src={staticFile("bgm.mp3")}
  volume={(frame) => {
    const t = frame / 30;
    if (t < 3) return (t / 3) * 0.4;           // 淡入
    if (t > 63.2) return ((66.2 - t) / 3) * 0.4; // 淡出
    return 0.2;                                      // 配音密集段
  }}
/>
```

### 7.3 音量原则

**配音清晰度优先**：BGM 必须作为背景，不能盖过人声。

- 配音密集段：0.15-0.25
- 无配音段（片头/片尾）：0.3-0.5
- 本次实践最终值：峰值 0.4，正常段 0.2

---

## 阶段八：渲染出片

### 8.1 渲染命令

```bash
npx remotion render MyCompositionV1 --fps=30 --frames=0-{N-1} --output="output.mp4"
```

**帧范围是左闭右开 `[0, N)`**，总帧数 N 意味着最后一帧是 N-1。

### 8.2 磁盘空间要求

Remotion 渲染需要：
- webpack bundle 缓存（~400MB）
- Chromium headless（~100MB）
- 临时帧文件

渲染前确保 **C 盘有 5-10GB 可用空间**。`%TEMP%` 中的 `remotion-webpack-bundle-*` 可提前清理。

### 8.3 Studio 预览 ≠ 最终渲染

- Studio 预览受浏览器解码限制，高倍速（>10x）可能卡顿
- 最终渲染用 ffmpeg 硬解码，流畅得多
- **Studio 只做节奏判断，最终质量以渲染出片为准**

---

## 关键设计决策框架

### Hard Rules（生产正确性铁律）

> 以下规则来自 [video-use](https://github.com/browser-use/video-use) 项目的生产验证。违反这些规则会导致静默失败或输出损坏，务必遵守。

| # | 规则 | 说明 |
|---|------|------|
| 1 | **字幕 LAST** | 字幕必须在滤镜链最后应用，否则叠加层会遮住字幕 |
| 2 | **分段提取 → 无损 concat** | 有叠加时用 `-c copy` concat，避免双重编码 |
| 3 | **30ms 音频淡入淡出** | 每个分段边界加 `afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03`，否则有 pop 音 |
| 4 | **叠加层 PTS 偏移** | 用 `setpts=PTS-STARTPTS+T/TB` 偏移叠加层帧 0，否则动画窗口显示错误帧 |
| 5 | **Master SRT 用输出时间线偏移** | `output_time = word.start - segment_start + segment_offset`，否则 concat 后字幕错位 |
| 6 | **不在词中间切割** | 所有切边必须对齐到转录词的边界 |
| 7 | **切割边缘留 pad** | 工作窗口 30-200ms，Scribe 时间戳漂移 50-100ms，pad 吸收漂移 |
| 8 | **词级 verbatim ASR** | 不用 SRT/phrase 模式（丢失亚秒级间隙数据） |
| 9 | **按源缓存转录** | 不重新转录，除非源文件本身变了 |
| 10 | **多动画并行子代理** | 用 `Agent` 工具并行生成，总耗时 ≈ 最慢那个 |
| 11 | **执行前确认策略** | 在用户确认计划前不进行任何切割 |
| 12 | **输出到 `<videos_dir>/edit/`** | 不在 skill 目录写任何输出 |

### Option A vs Option B 决策

当某个 Segment 时长问题无法通过调速解决时：

| 选项 | 做法 | 适用条件 |
|-----|------|---------|
| Option A（压缩） | 强制缩短时长，裁剪内容 | 甲方严格卡时长 |
| Option B（接受更长） | 让叙事完整，接受更长总时长 | 优先内容完整 |

**决策原则**：官网宣传片的核心目标是"把产品价值讲清楚"，而非"严格卡 N 秒"。压缩到不完整，反而失去意义。

### 冻结帧实现

不要用 `Img src="video.mp4#t=1.0"`（依赖 HTTP 服务器）或 `playbackRate={0}`（不支持）。改用纯色背景或预渲染图片。

---

## 不适用场景（重要）

本 skill **不适用**于以下场景，识别到时请明确告知用户：

| 场景 | 原因 | 建议 |
|-----|------|------|
| **技术文档/幻灯片 → 视频** | 本 skill 需要已有录屏视频作为输入，没有源视频无法切片 | 先用 Screen Studio/OBS/Keynote 录制幻灯片演示，再走本工作流 |
| **AI 生成视频画面** | 本 skill 仅处理已有素材的剪辑组合，不生成新画面 | 需要 Text-to-Video / AI 视频生成工具（如 Sora、Pika） |
| **从零构建动画视频** | 本 skill 假设有现成素材，只是剪辑重组 | 需要纯动画/图形动画工具（如 After Effects、Canva） |

**回归路径**：如果用户有技术文档但没有录屏 → 引导用户先录制幻灯片演示（Screen Studio/OBS）→ 再回到本工作流。

---

## 决策树

用户描述任务时，按以下顺序判断：

```
用户描述任务
    │
    ├─ 有录屏/产品演示视频（.mp4）？
    │       ├─ 是 → 走完整工作流（本 skill）
    │       └─ 否 → 跳转到"不适用场景"处理
    │
    └─ 目标是官网宣传片/产品介绍？
            ├─ 是 → 本 skill 适用
            └─ 否 → 说明本 skill 专注场景，建议其他方案
```

---

## 项目结构总览

```
project/
├── work/                          ← 工作流与资产层
│   └── projects/{project-id}/
│       ├── edit-script.md          ← 剪辑执行稿
│       ├── storyboard.json         ← 分镜表
│       ├── edit-spec.json         ← 编辑规格（帧级时间线，支持多视频源）
│       ├── subtitle-track.json      ← 字幕时间轴
│       ├── voiceover-script.json   ← 配音脚本
│       ├── generate_voiceover.py  ← 配音生成脚本
│       ├── process_bgm.py         ← BGM 混合脚本
│       ├── takes_packed.md         ← 自动视频理解：打包转录文本
│       ├── transcripts/             ← 自动视频理解：原始转录 JSON
│       │   └── <video_stem>.json
│       ├── timeline_view/          ← 自动视频理解：可视化确认 PNG
│       └── animations/            ← 动画叠加层（如有）
└── remotion-app/                  ← Remotion 实现层
    ├── public/
    │   ├── source.mp4            ← 源视频（单视频场景）
    │   ├── video-a.mp4            ← 多视频场景：来源视频 A
    │   ├── video-b.mp4            ← 多视频场景：来源视频 B
    │   ├── voiceover.mp3         ← 配音
    │   └── bgm.mp3               ← BGM
    └── src/
        ├── Composition.tsx        ← 主 composition
        └── Root.tsx              ← 注册
```

---

## 常见问题速查

| 问题 | 原因 | 解决方案 |
|-----|------|---------|
| 子片段被截断 | 父级 Sequence durationInFrames 不够 | 检查并扩大父级时长 |
| Studio 预览高倍速片段卡顿 | 浏览器解码压力大 | 设置 `muted: true`，Studio 只判断节奏 |
| 配音和字幕错位 | 配音总时长 ≠ 视频时长 | 每段后加静音填充对齐 |
| 渲染报 ENOSPC | C 盘空间不足 | 清理 %TEMP%，确保 5-10GB 可用 |
| 渲染时 FreezeFrame 报错 | `#t=` 或 `playbackRate=0` 不支持 | 改用纯色背景 |
| 渲染报错 "frame range 0-N is not inbetween..." | 帧范围写错（应为左闭右开） | 改为 `--frames=0-{N-1}` |
| 某 Segment 时长不够 | 素材本身内容少 + 加速已到极限 | Option B：接受更长；或压缩其他 Segment |
| BGM 盖过人声 | BGM 音量过大 | 降低 BGM 音量至 0.15-0.25，配音段更低 |
| edge-tts 生成失败 | 网络或认证问题 | 检查 `edge-tts --list-voices` 是否正常 |
