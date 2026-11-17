# 5 阶段管线详细执行步骤

> SKILL.md 的扩展参考。当需要了解每个阶段的具体执行细节时阅读本文件。

## 阶段 1：批量获取（脚本执行）

```bash
cd "<skill目录>"
python scripts/01_fetch.py outputs/{batch-name}/inputs.txt --output-dir outputs/{batch-name}
```

**抖音实战补丁**（脚本已内置，无需手动处理）：
- agent-browser open（不 close 上一个，避免 close 挂起）
- 等待 40 秒让 blob URL 变成直接 CDN URL
- eval 直接参数模式 + network requests `__vid` 匹配 fallback
- CLIXML 噪声正则清理
- curl 下载 + MD5 去重检测
- ffmpeg 提取 16kHz 单声道 MP3

输出：
- `outputs/{batch-name}/audio/audio_N.mp3`
- `outputs/{batch-name}/metadata.json`

## 阶段 2：转录（脚本执行）

```bash
python scripts/02_transcribe.py --metadata outputs/{batch-name}/metadata.json --output-dir outputs/{batch-name}
```

**核心**：保留 segments 的 start/end/text（时间戳是阶段 4 语义切分的基础）。

转录后自动执行：
- opencc t2s 繁简转换（Whisper small 默认输出繁体）
- 错字修正字典（同音错字，如"长男句"→"长难句"）

输出：
- `outputs/{batch-name}/transcript/transcript_N.json`

**transcript_N.json 结构**：
```json
{
  "video_id": "1",
  "title": "第一讲-找到核心动词",
  "author": "教不会再杠Vivian",
  "source_url": "https://v.douyin.com/...",
  "duration_sec": 723.5,
  "segments": [
    {"start": 0.0, "end": 3.2, "text": "大家好我是Vivian"},
    {"start": 3.2, "end": 8.5, "text": "欢迎学习我的长难句系列课程"}
  ]
}
```

## 阶段 3：打包 + 工作表（脚本执行）

```bash
python scripts/03_pack_transcript.py --transcript-dir outputs/{batch-name}/transcript --output-dir outputs/{batch-name}
```

**本阶段不切分！** 只生成两个产物供阶段 4 使用：

1. **`takes_packed_N.md`** —— 按 90 秒窗口预打包的可读转录稿（带时间戳）
2. **`boundary-review_N.md`** —— 切分工作表，包含：
   - 视频信息（标题/时长/segments 数）
   - 路由建议（基于标题启发式判断）
   - 6 路由规则表
   - 你的任务说明
   - 输出格式约束

## 阶段 4：路由 + 切分（★ TRAE 主对话执行，非脚本）

这是整个管线的核心。**主对话读 boundary-review_N.md 后，写 scene-boundaries_N.json**。

### 4.1 读取工作表

```
read: outputs/{batch-name}/work/boundary-review_1.md
read: outputs/{batch-name}/work/takes_packed_1.md
```

### 4.2 判断路由

工作表已基于标题给出路由建议，主对话可调整。6 路由规则详见 [`route-rules.md`](route-rules.md)。

### 4.3 提议边界点

**核心原则**：
- ❌ **不要按固定时长机械切分**（这是反模式）
- ✅ **按语义完成处切分**：知识点结束、论点完成、问答闭合、操作步骤完成
- ✅ **保留完整内容**：推理、例子、数字、限定条件都不要删
- ✅ **保持时间顺序**：不重排内容

### 4.4 写 scene-boundaries_N.json

```
write: outputs/{batch-name}/work/scene-boundaries_1.json
```

格式：
```json
{
  "video_id": "1",
  "title": "第一讲-找到核心动词",
  "route": "lesson",
  "route_reason": "标题含'第X讲'+口播教学形式",
  "scenes": [
    {
      "id": 1,
      "start_sec": 0.0,
      "end_sec": 45.3,
      "title": "课程介绍",
      "reason": "开场介绍本系列课程定位和本节目标，过渡到核心原则"
    },
    {
      "id": 2,
      "start_sec": 45.3,
      "end_sec": 150.8,
      "title": "核心原则：一个句子只有一个核心动词",
      "reason": "完整讲解核心原则+例句论证，清晰过渡到第二原则"
    }
  ]
}
```

**约束**：
- 第一个场景 start_sec = 0.0
- 最后一个场景 end_sec >= transcript 最后一个 segment 的 end
- 场景之间不能重叠或空隙
- 每个场景有简短 title 和具体 reason

## 阶段 5：输出（脚本执行）

```bash
python scripts/04_build_output.py --transcript-dir outputs/{batch-name}/transcript --boundaries-dir outputs/{batch-name}/work --output-dir outputs/{batch-name}
```

按 scene-boundaries.json + transcript.json 生成结构化 MD：
- 每场景一个 `## 02. 标题（时间区间）` 标题
- 保留该时间范围内的完整 segment 文本
- 每场景底部有 `<details>` 折叠的切分原因

输出：
- `outputs/{batch-name}/share/{标题}.md`

## 批量执行示例（8 个视频）

```bash
# 假设输入文件 outputs/batch-2026-07-14/inputs.txt 已准备好

# 阶段 1
python scripts/01_fetch.py outputs/batch-2026-07-14/inputs.txt --output-dir outputs/batch-2026-07-14

# 阶段 2
python scripts/02_transcribe.py --metadata outputs/batch-2026-07-14/metadata.json --output-dir outputs/batch-2026-07-14

# 阶段 3
python scripts/03_pack_transcript.py --transcript-dir outputs/batch-2026-07-14/transcript --output-dir outputs/batch-2026-07-14

# 阶段 4（主对话逐个读 boundary-review_N.md + takes_packed_N.md，写 scene-boundaries_N.json）
# 这一步由主对话执行，不是脚本命令

# 阶段 5
python scripts/04_build_output.py --transcript-dir outputs/batch-2026-07-14/transcript --boundaries-dir outputs/batch-2026-07-14/work --output-dir outputs/batch-2026-07-14
```

## 平台支持矩阵（v4.0）

| 平台 | 获取方式 | 转录方式 | 字幕优先 | 双语翻译 | 代理支持 |
|------|---------|---------|---------|---------|---------|
| 抖音 | agent-browser + curl | Whisper | 不适用 | 不适用（中文） | 不需要 |
| B站 | yt-dlp | yt-dlp 字幕优先；无字幕时 Whisper | ✅ v4.0 | ✅ | 不需要 |
| 小宇宙 | curl 抓 HTML 提取 audio 直链 | Whisper | 不适用 | ✅ | 不需要 |
| YouTube | youtube-transcript-api + yt-dlp 字幕 | 字幕（跳过Whisper）/ Whisper | ✅ | ✅ | HTTPS_PROXY 环境变量 |
| 通用平台 (v4.0) | yt-dlp 1700+ extractor | yt-dlp 字幕优先；无字幕时 Whisper | ✅ v4.0 | ✅ | 视平台而定 |

**v4.0 通用平台支持列表**（部分示例，完整列表见 yt-dlp 文档）：
- Vimeo / TikTok / Twitch / Dailymotion
- Twitter / X / Instagram / Facebook
- Reddit / SoundCloud / Pinterest / LinkedIn
- Streamable / VEVO / TED / Loom
- Udemy / Coursera / Skillshare / Wikipedia
