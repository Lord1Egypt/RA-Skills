---
name: bilibili-summarizer
description: "This skill should be used when the user shares a video link (Bilibili/B站, Douyin/抖音, YouTube, Xiaohongshu/小红书) and asks to extract subtitles, summarize the video content, or evaluate its information density. Also supports local video files. Trigger phrases include 总结这个B站视频, 提取字幕, bilibili链接, BV号, 信息密度, 帮我看这个视频, 语音转字幕, 字幕管理, 字幕收藏, 抖音视频总结, 总结抖音, 总结YouTube, 总结小红书, 视频字幕, or any message containing a bilibili.com, douyin.com, youtube.com, xiaohongshu.com, or xhslink.com URL, or a video file path (.mp4/.mkv/.mov)."
---

# 视频字幕提取与总结技能（B站 + 抖音 + YouTube + 小红书 + 本地文件）

## 技能概述

从 B站、抖音、YouTube、小红书视频及本地视频文件提取字幕（支持 API 字幕 + AI 语音识别双通道），生成结构化总结与信息密度评分，并提供弹幕分析、关键帧截图、说话人分离、SRT 字幕导出等高级功能。

## 支持的平台

| 平台 | API字幕 | ASR语音识别 | 总结评分 | 弹幕分析 | 链接格式 |
|------|---------|------------|----------|----------|----------|
| **B站** | ✅ | ✅ | ✅ | ✅ | `bilibili.com/video/BVxxx` 或 `BVxxx` |
| **抖音** | ❌ | ✅ | ✅ | ❌ | `douyin.com/video/xxx` 或 `v.douyin.com/xxx` |
| **YouTube** | ❌ | ✅ | ✅ | ❌ | `youtube.com/watch?v=xxx` 或 `youtu.be/xxx` |
| **小红书** | ❌ | ✅ | ✅ | ❌ | `xiaohongshu.com/explore/xxx` 或 `xhslink.com/xxx` |
| **本地文件** | ❌ | ✅ | ✅ | ❌ | `/path/to/video.mp4` |

## v3.0 新增功能

- ✅ **一键流程** (`pipeline.py`) — 自动完成全部步骤，Agent 只需调一次
- ✅ **批量处理** — 支持多个链接同时处理
- ✅ **B站收藏夹/合集** — 自动提取收藏夹内所有视频
- ✅ **本地视频文件** — 直接拖入本地 mp4/mkv/mov 文件
- ✅ **YouTube 支持** — yt-dlp 下载音频 + ASR 识别
- ✅ **小红书支持** — yt-dlp 下载音频 + ASR 识别 + 网页信息提取
- ✅ **SRT 字幕导出** — 标准字幕格式，可导入任意播放器
- ✅ **说话人分离** — 识别多人对话（FunASR SD 模型）
- ✅ **弹幕分析** — 词频统计、密度图、高赞弹幕（仅B站）
- ✅ **关键帧截图** — 固定间隔或场景切换检测

## 脚本清单

所有脚本位于 `~/.workbuddy/skills/bilibili-summarizer/scripts/`：

| 脚本 | 功能 | 依赖 |
|------|------|------|
| **`pipeline.py`** | ⭐ 一键流程（推荐使用） | yt-dlp, ffmpeg, FunASR/Whisper |
| `video_fetcher.py` | 提取视频信息 + API 字幕（B站/抖音/YouTube/小红书） | Python 标准库 / yt-dlp |
| `video_audio.py` | 下载/提取视频音频（B站/抖音/YouTube/小红书/本地） | yt-dlp, ffmpeg |
| `speech_to_text.py` | 语音转文字（ASR + 说话人分离 + SRT导出） | FunASR 或 Whisper |
| `danmaku_analyzer.py` | B站弹幕分析（词频/密度/热评） | Python 标准库 |
| `frame_extractor.py` | 关键帧截图（间隔/场景检测） | ffmpeg |
| `subtitle_manager.py` | 字幕收藏管理 | Python 标准库 |
| `bilibili_fetcher.py` | B站专用（向后兼容） | Python 标准库 |
| `bilibili_audio.py` | B站专用（向后兼容） | yt-dlp, ffmpeg |

---

## ⭐ 推荐使用：一键流程（pipeline.py）

### 单个视频

```bash
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/pipeline.py "https://www.bilibili.com/video/BVxxxx"
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/pipeline.py "https://v.douyin.com/xxx"
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/pipeline.py "https://youtube.com/watch?v=xxx"
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/pipeline.py "https://www.xiaohongshu.com/explore/xxx"
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/pipeline.py "/path/to/local_video.mp4"
```

### 批量处理

```bash
# 多个链接空格分隔
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/pipeline.py "链接1" "链接2" "链接3"

# B站收藏夹
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/pipeline.py --collection "https://space.bilibili.com/xxx/favlist?fid=xxx"
```

### 可选功能

```bash
# 导出 SRT 字幕
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/pipeline.py "链接" --format srt

# 提取关键帧截图
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/pipeline.py "链接" --frames

# 弹幕分析（仅B站）
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/pipeline.py "链接" --danmaku

# 说话人分离
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/pipeline.py "链接" --diarize

# 全部功能
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/pipeline.py "链接" --all
```

---

## 分步使用（高级场景）

### 第一步：尝试提取 API 字幕（B站）

```bash
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/video_fetcher.py "B站链接或BV号"
```

输出 JSON，包含 `info`（视频信息）和 `subtitle`（字幕内容）。

- 若 `subtitle.status` 为「已提取」且 `subtitle.plain_text` 有内容，直接进入第四步（总结 + 评分）
- 若「无字幕」或「下载失败」，进入第二步
- **抖音/YouTube/本地文件**：直接跳到第二步

### 第二步：下载/提取音频

```bash
# 在线视频（B站/抖音/YouTube）
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/video_audio.py "视频链接"

# 本地视频文件
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/video_audio.py "/path/to/video.mp4"
```

### 第三步：语音转文字（增强版）

```bash
# 基本识别
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/speech_to_text.py "音频文件路径"

# 导出 SRT 字幕格式
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/speech_to_text.py "音频文件路径" --format srt

# 说话人分离（仅 FunASR）
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/speech_to_text.py "音频文件路径" --diarize
```

**说话人分离输出示例：**
```
[00:15][说话人0] 今天我们聊聊人工智能的发展
[00:32][说话人1] 我觉得AI最大的问题是可控性
[01:05][说话人0] 对，这个观点我同意
```

### 第四步：生成结构化总结

根据提取到的字幕（API 或 ASR）和视频信息，按以下模板输出。

**重要：** Agent 必须利用自身知识库，对视频作者和视频中提到的关键人物进行背景调查和分析，帮助用户判断视频的信息可信度和价值。

```
## 📺 视频总结

**标题：** {title}
**作者：** {owner}
**平台：** B站 / 抖音 / YouTube / 小红书 / 本地文件
**时长：** {duration}
**标签：** {tags}
**字幕来源：** API字幕 / ASR语音识别（{engine}）

---

### 👤 作者背景
（根据作者名称和视频内容，搜索/回忆该作者的背景信息：
- 身份/职业（如：某领域专家、自媒体博主、企业高管、学者等）
- 知名度和影响力（粉丝量级、行业地位）
- 擅长领域/内容方向
- 历史争议或口碑
- 可信度评估：🔴 低 / 🟡 中 / 🟢 高，并说明原因）

### 🧑 视频主人公/关键人物
（视频中重点讲述的人物，如果与作者是同一人则标注"即作者"并合并说明。
多人则分别列出，每人包含：
- 姓名/称呼
- 身份/职业
- 与视频主题的关系
- 可信度评估：🔴 低 / 🟡 中 / 🟢 高，并说明原因
- 值得关注的点（如：是否有利益相关、是否有权威背书等））

### 🎯 核心主题
（一句话概括视频核心讲了什么）

### 📋 内容大纲
（按视频时间线列出 3-7 个关键节点，格式：[MM:SS] 主题）

### 💡 核心观点 / 关键信息
（提炼 3-5 条最有价值的结论或知识点）

### 🔑 关键词
（5-10 个关键词）
```

**背景调查规则：**
- 优先利用 Agent 自身知识库中关于该作者/人物的信息
- 如果无法确认背景，明确标注"⚠️ 未能确认该作者/人物背景，建议自行搜索核实"
- 不要编造或猜测未知的背景信息
- 对涉及医疗、法律、金融等敏感领域的观点，必须额外标注可信度警告

### 第五步：信息密度评分

**信息密度** = 单位时间内传递的有效知识/信息量，满分 10 分。

评分维度：

| 维度 | 说明 | 权重 |
|------|------|------|
| 语速密度 | 字符数 / 时长（秒），值越高越密集 | 20% |
| 知识含量 | 是否包含数据、概念、方法、案例 | 30% |
| 逻辑结构 | 内容是否有清晰的论点-论据结构 | 20% |
| 冗余度 | 重复、闲聊、过渡语比例（越低越好） | 15% |
| 实用性 | 观看后能直接应用的比例 | 15% |

输出格式：

```
---

## 📊 信息密度评分

**综合评分：X.X / 10** ⭐⭐⭐⭐⭐

| 维度 | 评分 | 说明 |
|------|------|------|
| 语速密度 | X/10 | ... |
| 知识含量 | X/10 | ... |
| 逻辑结构 | X/10 | ... |
| 冗余度   | X/10 | ... |
| 实用性   | X/10 | ... |

**评分说明：** （为何得这个分，适合什么类型的观众）
**观看建议：** （正常速度 / 1.5x / 2x，或跳过某些章节）
```

### 第六步：高级分析（可选）

#### 弹幕分析（仅B站）

```bash
# 基本弹幕分析（词频 + 密度 + 热评）
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/danmaku_analyzer.py "B站链接或BV号"

# 仅高频词
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/danmaku_analyzer.py "BV号" --top-words 20

# 弹幕密度图
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/danmaku_analyzer.py "BV号" --density
```

弹幕分析可以补充到总结中：

```
### 📊 弹幕分析

**弹幕总数：** XXXX 条
**高频关键词：** 关键词1(xxx次)、关键词2(xxx次)、...
**高潮片段：** 05:30-06:00（弹幕密度最高）
**观众热评：**
- [03:45] "这个观点太精辟了"
- [08:12] "原来如此，终于明白了"
```

#### 关键帧截图

```bash
# 每30秒一张
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/frame_extractor.py "视频链接"

# 场景切换检测
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/frame_extractor.py "视频链接" --scene-detect

# 自定义间隔和数量
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/frame_extractor.py "链接" --interval 60 --max-frames 30
```

### 第七步：字幕收藏管理（可选）

用户可将字幕存入本地收藏库，后续统一管理。

```bash
# 添加字幕（从 pipeline 输出的 JSON 导入）
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/subtitle_manager.py add --json-file result.json

# 列出所有字幕
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/subtitle_manager.py list

# 导出为 Markdown / SRT
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/subtitle_manager.py export --format md --output ~/Desktop/字幕合集.md

# 搜索字幕内容
python3 ~/.workbuddy/skills/bilibili-summarizer/scripts/subtitle_manager.py search "关键词"
```

字幕数据库存储位置：`~/.workbuddy/skills/bilibili-summarizer/cache/subtitles.json`

---

## 完整处理流程图

```
用户输入（链接/本地文件/收藏夹URL）
        │
        ▼
  pipeline.py 一键流程
        │
  输入类型检测
  ╱    │    ╲    ╲    ╲
B站  抖音  YouTube 小红书 本地
  │    │    │    │
  │ video_fetcher.py
  │ 获取视频信息 + API 字幕
  │    │    │    │
  │ 有字幕？  │    │
  │ ╱    ╲   │    │
  │ 是     否  │    │
  │ │      │   │    │
  │ │ video_audio.py / extract_from_local
  │ │ 下载/提取音频
  │ │      │   │    │
  │ │ speech_to_text.py
  │ │ ASR 语音识别
  │ │ [--diarize] 说话人分离
  │ │ [--format srt] SRT导出
  │ │      │   │    │
  │ └──┬───┘───┘────┘
  │    │
  │ [--danmaku] 弹幕分析（仅B站）
  │ [--frames] 关键帧截图
  │    │
  │    ▼
  │  生成总结 + 信息密度评分
  │    │
  │    ▼
  │  subtitle_manager.py（可选）
  │  保存 / 管理 / 导出
  │
  └── 多视频批量处理循环
```

## 依赖安装

```bash
# 必须安装
brew install yt-dlp ffmpeg

# ASR 引擎（选一个）
pip install funasr modelscope torch torchaudio   # 推荐：FunASR（中文最优）
pip install openai-whisper                        # 备选：Whisper（通用）
```

## 注意事项

- B 站 API 无需 Cookie 即可访问大部分公开视频信息
- B 站 API 字幕依赖 UP 主上传或 B 站 AI 字幕
- 抖音/YouTube/小红书 **无公开字幕 API**，通过 ASR 语音识别获取字幕
- 抖音短链接（v.douyin.com）会自动解析为实际链接
- YouTube 视频信息通过 yt-dlp 获取（无需 API Key）
- 小红书短链接（xhslink.com）会自动解析为实际链接
- 小红书视频信息通过网页解析获取，部分反爬策略可能导致偶尔失败
- 说话人分离需要 FunASR SD 模型（`cam++`），首次会额外下载
- 语音识别准确率约为 95%，建议以总结为主，不要逐字引用
- 关键帧截图的在线视频需要临时下载（仅视频流，不含音频）
- 弹幕分析依赖 B 站 API，可能因反爬策略偶尔失败
- 付费/会员专属视频的音频可能无法下载
