---
name: bucket-list
version: 1.4.0
description: Use this skill when the user wants to record, view, update, complete, cancel, or review a personal bucket list / wish list. Supports Chinese commands such as "添加愿望：...", "查看愿望清单", "完成了...", and "我们完成了什么", plus a localhost GUI that shares the same JSON data file.
---

# 愿望清单 (Bucket List)

记录主人与龙虾一起完成的人生愿望清单。它不是待办软件，也不是人生导师；它是一个本地优先的愿望记录和成就回顾工具。

## When To Use

Use this skill when the user asks to:

- add a wish, bucket-list item, life goal, or "愿望"
- view pending, completed, or cancelled wishes
- mark a wish completed or cancelled
- review completed wishes or shared achievements
- open or maintain the bucket-list GUI
- import, export, or repair bucket-list data

## Quick Start

Start the GUI:

```bash
cd skills/bucket-list
node server.js
# open http://localhost:9999/
```

Use the CLI:

```bash
./bucket-list.sh add "去南极看企鹅" "旅行"
./bucket-list.sh view
./bucket-list.sh complete "南极" "看到了企鹅"
./bucket-list.sh cancel "学吉他" "改学钢琴"
./bucket-list.sh achievements
```

Natural-language entry:

```bash
./bucket-list.sh intent "添加愿望：去南极看企鹅"
./bucket-list.sh intent "查看愿望清单"
./bucket-list.sh intent "完成了 发布技能"
./bucket-list.sh intent "我们完成了什么"
```

## Data

The runtime data file is stored outside the skill folder:

```text
<workspace>/data/bucket-list.json
```

The published `data/bucket-list.json` inside this skill is only an empty template. Do not publish personal wishes in the package.

Canonical wish fields:

- `id`
- `content`
- `category`
- `status`: `pending`, `completed`, or `cancelled`
- `createdAt`
- `endedAt`
- `endedBy`
- `completionNote`
- `cancelReason`
- `timeline`

## Safety

- The server binds to `127.0.0.1` only.
- The server only accepts same-origin browser writes by default.
- Writes are validated, size-limited, and saved atomically with a backup.
- The CLI uses Node JSON parsing/writing instead of shell text edits.

## Boundaries

- Do not treat ordinary tasks as wishes unless the user frames them as a wish, life goal, or bucket-list item.
- Ask before recording sensitive or emotionally loaded content if the user's intent is unclear.
- Strong negative emotion should receive care first; record or update wishes only after the user confirms.
