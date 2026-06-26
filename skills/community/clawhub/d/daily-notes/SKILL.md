---
name: daily-notes
description: 日常随笔记录，收录一切想记下来的东西——奇思妙想、灵感片段、日常感想、碎碎念、发现、备忘录，支持图片附件与多图关联。Daily notes with image attachments and multi-image association support.
triggers: 记一下, 录一下, 备忘, 碎碎念, 随手记, 突然想到, 有个念头, 日记, 日常, 想法, 灵感, 创意, 发现, 拍照, 照片, 图片, note, record, memo, idea, thought
version: 1.2.0
author: Akira / Kazuya-ECNU
license: MIT
---
# daily-notes v1.1 / 日常随笔记录

## 数据文件 / Data Files（存放于 `~/.openclaw/workspace/notes-data/`）
- `~/.openclaw/workspace/notes-data/notes.json` — 随笔记录列表（含图片路径）
- `~/.openclaw/workspace/notes-data/images/` — 图片附件目录，按 `YYYY-MM-DD_描述.jpg` 命名

## 数据格式 / Data Format
```json
{
  "notes": [
    {
      "id": "uuid",
      "content": "记录内容 / Note content",
      "tags": ["想法", "技术", "生活", "碎碎念"],
      "status": "pending | in_progress | done | archived",
      "images": ["images/2026-04-06_场景描述.jpg", ...],
      "created_at": "YYYY-MM-DDTHH:mm:ss",
      "updated_at": "YYYY-MM-DDTHH:mm:ss"
    }
  ]
}
```

## 主动记录规则 / Proactive Capture Rule
用户的任何发言，**无论是否带有明确目的**，都应视为值得记录的随笔。
Any user message, regardless of whether it has a clear purpose, should be treated as worth recording.
- 没有明确任务意图的发言 → 自动记入 daily-notes
- 包含情绪、感想、碎碎念、随手想法的发言 → 自动记入 daily-notes
- 有明确任务指令的发言（如"帮我写代码"、"查询天气"）→ 正常执行任务，**不要**强制记录
- 是否记录以**是否承载了用户的想法、感受或意图**为判断标准，而非以是否有工具执行为判断标准

## 操作 / Operations
1. **记录随笔 / Record Note**：解析内容 → 提取标签 → 生成 ID → 追加到 notes.json → 反馈已记录
2. **查看列表 / List Notes**：读取 notes.json → 按时间倒序展示 → 支持按标签或状态筛选
3. **搜索记录 / Search**：按关键词搜索 content 和 tags
4. **更新状态 / Update Status**：找到对应记录 → 更新 status 和 updated_at
5. **关联图片 / Attach Images**：用户发送图片时 → 追加到对应记录的 images 数组
6. **删除记录 / Delete**：软删除（archived）或彻底删除（含图片一并删除）

## 状态说明 / Status
- `pending` — 待处理 / Pending（默认）
- `in_progress` — 进行中 / In progress
- `done` — 已完成 / Done
- `archived` — 已归档/放弃 / Archived

## 标签分类 / Tags
- `想法` / `idea` — 奇思妙想、创意点子
- `技术` / `tech` — 技术实现、代码思路
- `生活` / `life` — 日常感想、碎碎念
- `碎碎念` / `ramble` — 随手记录的心情、吐槽
- `备忘` / `memo` — 临时记录、待办提醒
- `发现` / `discovery` — 学到的新东西、有趣的观察
- `心情` / `mood` — 情绪、感受
- `健康` / `health` — 身体、锻炼、饮食
- `财务` / `finance` — 省钱，投资、理财
- 可根据内容自由添加新标签 / Free to add custom tags

## 图片处理规则 / Image Rules
- 用户发送图片时，保存到 `images/` 目录
- 文件名格式 / Filename format：`YYYY-MM-DD_场景描述.jpg`
- `images` 字段存储相对于 `notes-data/` 的相对路径列表，如 `["images/2026-04-06_xxx.jpg"]`
- 一条记录可关联多张图片（images 数组）/ Multiple images per note
- 删除记录时，关联的图片一并删除 / Images deleted with note
- 展示记录时，图片路径以相对路径形式呈现

## 注意事项 / Notes
- content 尽量完整记录原始内容，保留原汁原味
- content: write original thoughts faithfully, keep the raw voice
- tags 自动提取或用户补充 / Auto-extracted or user-provided
- 按时间倒序展示，最新的在最前面 / Newest first
- 触发词已覆盖中英文 / Triggers available in both Chinese and English
