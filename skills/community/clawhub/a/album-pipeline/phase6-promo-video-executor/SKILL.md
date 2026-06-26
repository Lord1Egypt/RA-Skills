# Phase 6.7 — Promo Video Executor Skill

> 使用 MiniMax CLI `mmx video generate` 生成专辑宣传短视频。

---

## 触发

phase6-cover-executor 完成后自动启动。

---

## 输入

| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 6 | `docs/album-overview.md` | 核心概念/叙事轴/曲目单 |
| Phase 6 | `docs/promotional-materials.md` | 宣传文档（视频脚本素材） |
| Phase 6 | `docs/cover-concept.md` | 封面概念（视觉风格参考） |
| Phase 6.4.6 | `generate/covers/album-cover-p1.png` | 最佳专辑封面（首帧参考） |
| Phase 5 | `generate/cn_320k/*.mp3` | 最终选定音频（BGM 参考） |

---

## 执行

### ⚠️ 修改范围
- **读取**：Phase 6 文档文件、封面图、音频文件
- **写入**：`docs/promo-video.mp4`、`docs/promo-video-15s.mp4`
- **禁止**：修改任何源文档或封面图文件

### 视频策略

从 `docs/promotional-materials.md` 和 `docs/album-overview.md` 提取视频脚本概念，生成两种规格的宣传视频：

| 规格 | 时长 | 用途 |
|------|------|------|
| 完整版 | 25-30 秒 | 社交媒体主视频（B站/小红书/视频号） |
| 精简版 | 15 秒 | 短视频平台（抖音/快手/Reels/Shorts） |

### 视频生成方式

#### 方式 A：纯 Text-to-Video（T2V）

不使用首帧参考，完全从文字描述生成：

```bash
# 完整版 25-30 秒
mmx video generate \
  --prompt "{专辑宣传视频完整描述：视觉风格、转场节奏、情绪氛围}" \
  --model MiniMax-Hailuo-2.3 \
  --download docs/promo-video.mp4

# 精简版 15 秒
mmx video generate \
  --prompt "{精简版视频描述：快速节奏、核心视觉冲击}" \
  --model MiniMax-Hailuo-2.3 \
  --download docs/promo-video-15s.mp4
```

#### 方式 B：首帧参考 + Text-to-Video（推荐）

使用最佳专辑封面作为首帧参考，保持视觉一致性：

```bash
# 完整版 — 以封面为首帧
mmx video generate \
  --prompt "{视频动作/转场描述：封面逐渐展开、歌词意象浮现、情绪推进}" \
  --first-frame generate/covers/album-cover-p1.png \
  --model MiniMax-Hailuo-2.3 \
  --download docs/promo-video.mp4

# 精简版 — 以封面为首帧
mmx video generate \
  --prompt "{精简版动作描述：封面快速展开 + 核心视觉元素闪现}" \
  --first-frame generate/covers/album-cover-p1.png \
  --model MiniMax-Hailuo-2.3 \
  --download docs/promo-video-15s.mp4
```

### Prompt 编写指南

从以下文档提取视频脚本素材：

| 素材来源 | 提取内容 | 视频映射 |
|---------|---------|---------|
| `docs/album-overview.md` 核心概念 | 专辑主题/悖论 | 核心视觉隐喻 |
| `docs/album-overview.md` 叙事轴线 | 情绪弧线 | 视频节奏（起→承→转→合） |
| `docs/cover-concept.md` 配色方案 | HEX 色值 | 视频色调 |
| `docs/cover-concept.md` 视觉方向 | 主视觉描述 | 视频主画面 |
| `docs/promotional-materials.md` 核心传播概念 | 一句话传播点 | 视频结尾 CTA 文字 |
| `songs/T{N}-*.md` 封面高光文案 | 每首歌一句话文案 | 中段歌词闪现文字 |
| `generate/covers/album-cover-p1.png` | 最佳封面图 | 首帧参考 |

### 视频 Prompt 结构

```
{视频类型} for music album "{专辑中文名} / {English Name}"

Opening (0-{开场秒数}s): {首帧描述，封面视觉元素}
Build ({开场秒数}-{高潮秒数}s): {情绪推进，视觉转场描述}
Climax ({高潮秒数}-{结尾秒数}s): {高潮画面，核心视觉符号}
Resolution (结尾-结束s): {收尾，专辑名/艺人名文字浮现}

Visual style: {摄影/插画/3D/抽象}
Color tone: {主色 HEX → 辅色 HEX 的渐变}
Motion: {运镜方式：推拉摇移/缩放/粒子}
Typography: {文字出现方式：淡入/手写/打字机}
Mood: {整体情绪基调}

Technical: {N} second video, {16:9 或 9:16}, cinematic quality
```

### 画面比例选择

| 平台 | 比例 | 推荐用途 |
|------|------|---------|
| 16:9 | 横版 | B站/YouTube/视频号 |
| 9:16 | 竖版 | 抖音/小红书/Reels/Shorts |
| 1:1 | 正方形 | 朋友圈/Instagram |

⚠️ **默认生成 16:9 横版**（适配最广），如需竖版/正方形可额外生成。

### CLI 参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `--prompt` | 视频描述文本 | 主描述 |
| `--model` | `MiniMax-Hailuo-2.3` | 视频生成模型 |
| `--first-frame` | 封面图路径（可选） | 首帧参考图 |
| `--download` | 输出路径 | 保存位置 |

---

## Checklist

| # | 检查项 | 打勾标准 |
|---|--------|---------|
| 1 | 完整版视频已生成 | `docs/promo-video.mp4` 存在 |
| 2 | 精简版视频已生成 | `docs/promo-video-15s.mp4` 存在 |
| 3 | 视频文件可播放 | 非损坏文件，文件大小 ≥ 1MB |
| 4 | 视频时长符合规格 | 完整版 20-30s，精简版 12-18s |
| 5 | 首帧参考（如使用）正确 | 视频开头与专辑封面视觉一致 |
| 6 | 生成日志已保存 | 记录生成耗时/模型版本/使用方式 |

全部 ✅ → 返回 Phase 6 主流程，进入 phase6-packager
