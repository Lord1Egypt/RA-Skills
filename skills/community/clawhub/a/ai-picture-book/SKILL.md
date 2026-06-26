---
name: baidu-wenku-ai-picture-book
description: 百度文库AI绘本是一个基于人工智能制作绘本视频的工具，支持生成静态绘本和动态绘本(URL输出)。能帮助文本内容创作者们在缺乏绘画技能的情况下，快速生成精美绘本视频，提高内容生产效率。无论是在儿童教育、亲子互动、品牌营销，还是在社交媒体内容创作等领域都能应用。
metadata: { "openclaw": { "emoji": "📔", "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# 百度文库AI绘本

## 应用场景
- 快速生成课程相关的教学绘本
- AI绘本快速实现故事可视化，缩短创作周期
- 品牌故事、产品历程或公益活动视频创作，增强传播感染力。
- 绘本形式呈现历史、科学、民俗等内容，提升大众理解度与阅读体验
- 为电子书平台、知识媒体提供视频内容素材

## 执行流程

1. **创建绘本任务**: Submit story + type → get task ID
2. **轮询任务状态**: Query every 5-10s until completion
3. **获取任务结果**: Retrieve video URLs when status = 2

## 绘本类型

| 类型 | 值  | 描述   |
|----|----|------|
| 静态 | 9  | 静态绘本 |
| 动态 | 10 | 动态绘本 |

**必选**: 用户生成绘本必须指定绘本类型 (静态/9 or 动态/10). 如果没有提供, 主动询问用户选择一种.

## 状态码说明

| 状态码     | 状态描述 | 需要的操作  |
|---------|------|--------|
| 0, 1, 3 | 进行中  | 继续轮询   |
| 2       | 完成   | 获取绘本结果 |
| Other   | 失败   | 展示异常   |

## 使用说明

### 创建任务

**Endpoint**: `POST /v2/tools/ai_picture_book/task_create`

**Parameters**:
- `method` (required): `9` for static, `10` for dynamic
- `content` (required): Story or description

**Example**:
```bash
python3 scripts/ai_picture_book_task_create.py 9 "A brave cat explores the world."
```

**Response**:
```json
{ "task_id": "uuid-string" }
```

### 查询任务

**Endpoint**: `GET /v2/tools/ai_picture_book/query`

**Parameters**:
- `task_id` (required): Task ID from create endpoint

**Example**:
```bash
python3 scripts/ai_picture_book_task_query.py --task_id="task-id-here"
```

**Response** (Completed):
```json
{
  "task_id": "uuid-string",
  "status": 2,
  "video_bos_url": "https://..."
}
```

## 循环拉取任务状态

### Option 1: Auto Polling (Recommended)
```bash
python3 scripts/ai_picture_book_poll.py --task_id="task-id-here" [--max_attempts=30] [--interval=5]
```

**Examples**:
```bash
# Default: 20 attempts, 5s intervals
python3 scripts/ai_picture_book_poll.py --task_id="task-id-here"

# Custom: 30 attempts, 10s intervals
python3 scripts/ai_picture_book_poll.py --task_id="task-id-here" --max_attempts=30 --interval=10
```

### Option 2: Manual Polling
1. Create task → store `task_id`
2. Query every 5-10s until status = 2
3. Timeout after 2-3 minutes

## 异常处理

- Invalid content: "Content cannot be empty"
- Invalid type: "Invalid type. Use 9 (static) or 10 (dynamic)"
- Processing error: "Failed to generate picture book"
- Timeout: "Task timed out. Try again later"
