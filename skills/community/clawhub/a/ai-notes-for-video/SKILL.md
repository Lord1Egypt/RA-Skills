---
name: baidu-netdisk-ai-video-notes
description: 百度网盘AI视频笔记是一款基于大模型的视频内容理解工具，可以对视频(本地视频，网络视频)语音识别生成文稿笔记、大纲笔记、图文笔记三种笔记格式。当用户需要从视频生成笔记、总结视频内容、或将视频转化为文字记录时使用，经典场景（教育，会议视频总结笔记，短视频文案建议，关键信息提取）
metadata: { "openclaw": { "emoji": "📺", "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# 百度网盘AI视频笔记

## 功能特色
- 支持mp4、mov、flv、mpeg、avi、mkv、wmv等主流视频格式
- 异步生成机制、进度反馈、多格式输出

## 应用场景
- 视频教学内容理解与笔记
- 短视频平台内容分析与文案建议
- 会议视频记录与关键信息提取
- 高峰时段直播视频回顾与笔记


## 执行流程

1. **任务创建**: 提交视频URL(本地视频或网络视频) → 生成任务ID
2. **轮询任务状态**: 每3-5秒查询一次任务状态，直到任务完成
3. **获取解析结果**: 当 status = 10002 时，输出解析结果

## 状态码说明

| Code | Status | Action |
|-------|--------|--------|
| 10000 | 进行中    | 继续轮询   |
| 10002 | 完成     | 输出解析结果 |
| Other | 失败     | 提示异常信息 |

## 笔记类型

| Type | Description |
|------|-------------|
| 1 | 文稿笔记        |
| 2 | 大纲笔记        |
| 3 | 图文笔记        |

## 使用示例

### 创建任务

**Endpoint**: `POST /v2/tools/ai_note/task_create`

**Parameters**:
- `video_url` (required): Public video URL

**Example**:
```bash
python3 scripts/ai_notes_task_create.py --video_url='https://example.com/video.mp4'
```

**Response**:
```json
{
  "task_id": "uuid-string"
}
```

### 查询任务状态

**Endpoint**: `GET /v2/tools/ai_note/query`

**Parameters**:
- `task_id` (required): Task ID from create endpoint

**Example**:
```bash
python3 scripts/ai_notes_task_query.py --task_id="task-id-here"
```

**Response** (Completed):
```json
[
   {
  "状态": "完成",
  "文稿笔记": ["note1", "note2"]
   },
   {
  "状态": "完成",
  "大纲笔记": ["note1", "note2"]
   },
   {
  "状态": "完成",
  "图文笔记": ["note1", "note2"]
   }
]
```

## 循环拉取任务状态

### Option 1: Manual Polling
1. Create task → store `task_id`
2. Query every 3-5 seconds:
```bash
python3 scripts/ai_notes_task_query.py --task_id="task-id-here"
```
3. Show progress updates:
   - Status 10000: Processing...
   - Status 10002: Completed
4. Stop after 30-60 seconds (video length dependent)

### Option 2: Auto Polling (Recommended)
Use the polling script for automatic status updates:

```bash
python3 scripts/ai_notes_poll.py --task_id="task-id-here" [--max_attempts=30] [--interval=5]
```

**Examples**:
```bash
# Default: 20 attempts, 3-second intervals
python3 scripts/ai_notes_poll.py --task_id="task-id-here"

# Custom: 30 attempts, 5-second intervals
python3 scripts/ai_notes_poll.py --task_id="task-id-here" --max_attempts=30 --interval=5
```

**Output**:
- Shows real-time progress: `[1/20] Processing... 25%`
- Auto-stops when complete
- Returns formatted notes with type labels

## 异常处理

- 文件下载失败: "File not found or invalid URL"
- Processing error: "Failed to parse video"
- Timeout: "Video too long, try again later"
