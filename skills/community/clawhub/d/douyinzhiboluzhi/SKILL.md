---
name: byted-sol-live-highlight-slicer
description: 从一段直播录屏（.webm/.mp4/.mov）中自动识别高光时刻并切割为多个短视频片段，支持音频能量、场景变化、音画混合、音画并集和 ASR 关键词五种分析方式，可输出独立片段与合并版视频。适用于“直播录屏自动剪高光”“从回放里切出主播情绪高点”“按声音峰值提取精彩片段”这类任务。
author: openclaw
---

# 直播录屏高光切片

给定本地直播录屏文件路径，使用音频能量、场景变化、音画混合、音画并集或 ASR 关键词密集度识别高光时间段，并输出多个短视频片段；可选再合并为一个高光合集视频。核心脚本为 `scripts/highlight_slicer.py`。

## 能力简介

该 Skill 用于把“本地直播录屏 -> 自动检测高光 -> 输出多个短片段 -> 可选合并”封装成单条命令执行，替代手动听完整段录屏、手动记录时间点、再逐段裁剪的重复流程。

## 适用场景

在用户已经有一段 `.webm`、`.mp4` 或 `.mov` 直播录屏，并希望：

- 自动从直播回放里找到主播情绪高点
- 根据声音能量峰值提取精彩片段
- 根据镜头/商品切换频繁区间提取高光
- 结合音量升高与画面切换提取更稳的高光
- 合并音频高光与画面高光结果，尽量避免漏掉精彩片段
- 基于已有 ASR 转写文本按电商关键词密集度提取高光
- 生成多个高光短视频片段用于二次分发
- 再额外生成一个高光合集视频

时使用本 Skill。

## 前置条件

### 环境要求

- Python 3 可执行
- 宿主环境已安装 `ffmpeg` 和 `ffprobe`
- Python 环境已安装依赖：`pydub`、`librosa`、`numpy`
- 若使用 `asr` 方法，需要准备已有转写结果文件（推荐 JSON）

### 输入文件要求

- 输入文件必须为本地绝对路径
- 支持常见直播录屏格式：`.webm`、`.mp4`、`.mov`
- 输入视频需包含可提取的音频轨道

## 输入参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--input` | 是 | 无 | 待分析直播录屏的绝对路径 |
| `--method` | 否 | `hybrid` | 分析方法：`audio` / `scene` / `hybrid` / `combined` / `asr` |
| `--threshold` | 否 | `1.5` | 音频能量阈值倍数，基于 `均值 + threshold * 标准差` 判断候选高光 |
| `--scene-threshold` | 否 | `0.1` | 场景变化阈值，越低越容易把画面切换识别为候选高光 |
| `--min-clip-duration` | 否 | `5` | 最小保留片段时长（秒） |
| `--padding` | 否 | `2` | 检测到高光后，前后额外扩展的秒数 |
| `--output-dir` | 否 | `./highlights` | 输出目录 |
| `--merge` | 否 | `true` | 是否额外输出一个合并版高光视频 |
| `--asr-file` | 否 | 无 | ASR 转写文件路径；`--method asr` 时必填 |
| `--asr-window` | 否 | `8` | ASR 关键词聚合窗口大小（秒） |
| `--top-n` | 否 | `8` | ASR 法最多保留多少个高分时间窗口 |

## 执行命令示例

### 示例 1：按默认参数提取高光并输出合并版（默认使用 `hybrid`）

```bash
python3 skill-live-highlight-slicer/scripts/highlight_slicer.py \
  --input "/absolute/path/live-recording.mp4"
```

`.mov` 输入同样支持，例如：

```bash
python3 skill-live-highlight-slicer/scripts/highlight_slicer.py \
  --input "/absolute/path/live-recording.mov"
```

### 示例 2：提高阈值，减少误检

```bash
python3 skill-live-highlight-slicer/scripts/highlight_slicer.py \
  --input "/absolute/path/live-recording.webm" \
  --threshold 2.0 \
  --min-clip-duration 6 \
  --padding 2 \
  --output-dir "./highlights"
```

### 示例 3：只输出分段，不生成合并版

```bash
python3 skill-live-highlight-slicer/scripts/highlight_slicer.py \
  --input "/absolute/path/live-recording.mp4" \
  --merge false
```

### 示例 4：使用场景变化法

```bash
python3 skill-live-highlight-slicer/scripts/highlight_slicer.py \
  --input "/absolute/path/live-recording.mp4" \
  --method scene \
  --scene-threshold 0.1
```

### 示例 5：使用 hybrid 法叠加音频和画面信号

```bash
python3 skill-live-highlight-slicer/scripts/highlight_slicer.py \
  --input "/absolute/path/live-recording.mp4" \
  --method hybrid \
  --threshold 1.5 \
  --scene-threshold 0.1
```

### 示例 6：使用已有 ASR 转写文本提取高光

```bash
python3 skill-live-highlight-slicer/scripts/highlight_slicer.py \
  --input "/absolute/path/live-recording.mp4" \
  --method asr \
  --asr-file "/absolute/path/live_asr.json" \
  --asr-window 8 \
  --top-n 6
```

### 示例 7：合并 Audio + Scene 高光结果

```bash
python3 skill-live-highlight-slicer/scripts/highlight_slicer.py \
  --input "/path/to/video.mov" \
  --method combined \
  --threshold 1.5 \
  --scene-threshold 0.15 \
  --min-clip-duration 5 \
  --padding 2 \
  --output-dir "/path/to/output" \
  --merge true
```

## 执行逻辑步骤

按以下顺序执行：

1. 校验输入参数
   - `--input` 必填，且必须为本地绝对路径
   - `--method` 允许 `audio` / `scene` / `hybrid` / `combined` / `asr`
   - `--threshold`、`--min-clip-duration`、`--padding` 必须为合法数值
   - `--merge` 解析为布尔值
2. 根据 `--method` 选择候选高光检测方式
   - `audio`：提取单声道 WAV，使用 `librosa` 计算 RMS 能量曲线
   - `scene`：执行 `ffmpeg -filter:v "select='gt(scene,阈值)',showinfo"` 提取画面切换时刻
   - `hybrid`：先跑 `audio` 和 `scene`，再取两者时间重叠区域作为优先高光
   - `combined`：先跑 `audio` 和 `scene`，再取两者候选片段并集，尽量避免漏检
   - `asr`：读取已有转写文本，按价格/行动/互动关键词密度聚合窗口分数
3. 将相邻且间隔小于 3 秒的候选高光段合并
4. 过滤掉长度小于 `--min-clip-duration` 的片段
5. 对保留片段按前后 `--padding` 秒扩展，并裁剪生成独立 `.mp4` 输出
6. 若 `--merge=true`，生成 concat 清单并调用 `ffmpeg` 合并为一个合集视频

## 输出结果

默认在 `--output-dir` 目录下输出：

- `clip_01_XXXX_YYYY.mp4` 等独立高光片段
- `segments.json`：高光片段时间信息、来源方法、分数与分析元数据；`combined` 下会保留 `audio` / `scene` / `audio+scene` 等来源标记
- `merged_highlights.mp4`：合并版高光视频（当 `--merge=true` 时）

## 退出码约定

| 退出码 | 含义 |
|--------|------|
| `0` | 成功 |
| `1` | 参数错误 |
| `2` | 音频提取失败 |
| `3` | 未检测到高光 |

## 异常处理

出现以下情况时，直接输出明确日志并按对应退出码停止：

- 输入路径为空、不是绝对路径、或文件不存在
- 输入格式不支持或输入文件不是有效视频文件
- `ffmpeg` / `ffprobe` 不可用
- 音频轨提取失败
- 场景检测命令执行失败
- `method=asr` 但缺少可解析的转写文件
- 分析后未找到满足阈值的高光片段

日志统一使用以下前缀：

- `STEP:` 当前步骤
- `OK:` 步骤成功
- `WARN:` 可继续执行的异常或兼容性提示
- `ERROR:` 终止执行的错误

## 能力边界

- `asr` 方法依赖输入转写文件结构中至少包含文本和起止时间（兼容字段如 `text/start/end`、`sentence/start_time/end_time`）
- `hybrid` 当前采用“音频高能段与场景变化段时间重叠”策略，不做更复杂的权重学习
- 不做字幕生成、封面生成、文案生成
- 不判断内容是否适合发布，仅负责高光切片
