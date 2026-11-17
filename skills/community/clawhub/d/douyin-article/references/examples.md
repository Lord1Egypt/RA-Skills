# 示例集

> SKILL.md 的扩展参考。完整的批量执行示例与边界情况处理。

## 示例 1：批量执行（v4.0 全平台 + 双语翻译）

**输入** outputs/batch/inputs.txt：
```
7.94 复制打开抖音【教不会再杠Vivian的作品】第一讲-找到核心动词 https://v.douyin.com/fvvM_U8NEoQ/
https://v.douyin.com/QL_DULaIjRA/  第二讲-句子的组装
https://www.bilibili.com/video/BV1NK411D7pr?p=1
https://www.xiaoyuzhoufm.com/episode/6245cb93d485a5cd77680082
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://vimeo.com/123456789
```

**执行**：
```bash
# 阶段 1：批量获取（字幕优先，无字幕时下载音频）
python scripts/01_fetch.py outputs/batch/inputs.txt --output-dir outputs/batch
# 阶段 2：Whisper 转录（仅无字幕视频）
python scripts/02_transcribe.py --metadata outputs/batch/metadata.json --output-dir outputs/batch
# 阶段 3：打包 + 语言检测
python scripts/03_pack_transcript.py --transcript-dir outputs/batch/transcript --output-dir outputs/batch

# 阶段 3.5：翻译（仅非中文视频）
python scripts/03_5_translate.py prepare --output-dir outputs/batch/work
# 主对话循环：next-batch → AI 翻译 → apply（重复直到 done）
python scripts/subtitle_pipeline.py next-batch --manifest outputs/batch/work/subtitle-N/manifest.json --output batch-response.json
# AI 翻译 batch-response.json 中的 items
python scripts/subtitle_pipeline.py apply --manifest outputs/batch/work/subtitle-N/manifest.json --response batch-response.json
# 渲染最终翻译
python scripts/subtitle_pipeline.py render --manifest outputs/batch/work/subtitle-N/manifest.json --output outputs/batch/work/translation_N.json

# 阶段 4：主对话读 work/boundary-review_N.md + takes_packed_N.md，写 scene-boundaries_N.json
# 阶段 5：输出 MD（自动识别双语）
python scripts/04_build_output.py --transcript-dir outputs/batch/transcript --boundaries-dir outputs/batch/work --output-dir outputs/batch
```

**输出**（v4.0 全平台自动路由）：
```
📋 共 6 个视频待处理（抖音 2 / B站 1 / 小宇宙 1 / YouTube 1 / 通用平台 1）
[1] 处理: 第一讲-找到核心动词（抖音）
     ✅ 音频提取完成: audio_1.mp3 (320 KB, 348.0s)
[2] 处理: 第二讲-句子的组装（抖音）
     ✅ 音频提取完成: audio_2.mp3 (280 KB, 228.8s)
[3] B站处理: BV=BV1NK411D7pr p=1
     v4.0: 尝试拉取 B站 CC 字幕...
     ✅ 字幕拿到: 245 个片段（中文）
[4] 小宇宙处理: episode=6245cb93d485a5cd77680082
     ✅ 完成: audio_4.mp3 (50000 KB, 4080.0s)
[5] YouTube 处理: video_id=dQw4w9WgXcQ
     ✅ 字幕拿到: 50 个片段（en，需翻译）
[6] 通用平台处理: https://vimeo.com/123456789
     v4.0: 尝试拉取平台字幕...
     ✅ 字幕拿到: 180 个片段（en，需翻译）
```

**阶段 2 跳过字幕路径**：
```
⏭️ [3] 跳过 Whisper（字幕已由 bilibili-cc 生成）
⏭️ [5] 跳过 Whisper（字幕已由 youtube-transcript-api 生成）
⏭️ [6] 跳过 Whisper（字幕已由 ytdlp-subtitle 生成）
```

**阶段 3.5 翻译（仅 [5] [6] 需翻译）**：
```
📋 需要翻译: 2/6 个视频
📝 视频 5: YouTube Video (50 units)
📝 视频 6: Vimeo Video (180 units)
```

**阶段 5 输出（自动双语）**：
```
[1] 输出: 第一讲-找到核心动词
   ✅ 第一讲-找到核心动词.md (8234 字符)
[5] 输出: YouTube Video
   双语: en → zh-CN (50 units)
   ✅ YouTube-Video.md (12450 字符)

📊 输出完成: 6/6
   其中双语对比: 2 个
```

**输出** share/第一讲-找到核心动词.md（单语）：
```markdown
# 第一讲-找到核心动词

> 作者: 教不会再杠Vivian
> 路由: lesson（教学课）
> 路由原因: 标题含'第X讲'+口播教学形式
> 场景数: 7
> 语言: 中文

## 01. 课程介绍（00:00-00:35）
大家好我是Vivian，欢迎学习我的长难句系列课程...
<details><summary>切分原因</summary>开场介绍课程定位，过渡到核心原则</details>
```

**输出** share/YouTube-Video.md（双语对比）：
```markdown
# YouTube Video

> 作者: Author
> 来源: YouTube
> 转录工具: 平台字幕 (youtube-transcript-api)
> 语言: en → 中文（双语对比）

## 01. Introduction（00:00-01:30）

欢迎来到本期视频，今天我们将讨论...

> **原文**：Welcome to this video, today we will discuss...
```

## 示例 2：边界情况

**CDN URL 提取失败**（仅抖音）→ 跳过该视频，继续处理其他：
```
[3] 处理: 第三讲-学会断句
     ⚠️ CDN URL 提取失败，跳过
[4] B站处理: BV=BV1NK411D7pr p=1
     ✅ 完成: audio_4.mp3 (5931 KB, 1290.2s)
```
metadata.json 中标记 `{"idx": 3, "success": false, "error": "无法提取 CDN URL"}`

## 示例 3：无清晰边界

**主对话切分时遇到无结构内容** → 整段保留，reason 标注：
```json
{
  "id": 1,
  "start_sec": 0.0,
  "end_sec": 180.0,
  "title": "完整口播内容",
  "reason": "无清晰语义边界，整段保留"
}
```

## 示例 4：v4.0 字幕不可用 fallback

**平台无字幕** → 自动 fallback 到音频下载 + Whisper：
```
[3] B站处理: BV=BV1NK411D7pr p=1
     v4.0: 尝试拉取 B站 CC 字幕...
     v4.0: 字幕不可用，fallback 到音频下载
     yt-dlp 下载中...
     ✅ 完成: audio_3.mp3 (5931 KB, 1290.2s)
```
