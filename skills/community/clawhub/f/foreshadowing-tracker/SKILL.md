---
name: foreshadowing-tracker
description: 伏笔追踪器 - 识别章节中的伏笔并追踪回收状态。当需要管理伏笔、确保前后呼应时使用，支持新增伏笔识别、待回收伏笔提醒、已回收伏笔标记。
---

# Foreshadowing Tracker - 伏笔追踪器

## Overview

自动识别章节中的伏笔（暗示、铺垫、悬念），追踪伏笔的回收状态，生成详细的伏笔追踪报告，帮助保持故事前后呼应。

**使用场景**：
- 需要识别章节中的新伏笔
- 需要追踪伏笔是否已回收
- 需要避免遗忘重要伏笔
- 需要确保故事前后呼应

## 伏笔类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **暗示** | 隐晦提示未来事件 | "他不知道，这将是最后一次见面" |
| **铺垫** | 为后续情节做准备 | "桌上放着一把古老的钥匙" |
| **悬念** | 引发读者好奇 | "门后传来奇怪的声音" |
| **flag** | 角色说出的话 | "等这件事结束，我就..." |

## CLI 使用

```bash
# 基本用法
python3 scripts/track_foreshadowing.py --book-dir projects/my-novel --chapter chapters/chapter-01.md

# 指定伏笔记录文件
python3 scripts/track_foreshadowing.py \
  --book-dir projects/my-novel \
  --chapter chapters/chapter-01.md \
  --record data/foreshadowing.json

# 输出报告到文件
python3 scripts/track_foreshadowing.py \
  --book-dir projects/my-novel \
  --chapter chapters/chapter-01.md \
  --output reports/chapter-01-foreshadowing.md

# 简写
python3 scripts/track_foreshadowing.py -d ./project -c chapter.md -o report.md
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--book-dir` / `-d` | ✅ | 小说项目目录路径 |
| `--chapter` / `-c` | ✅ | 章节文件路径 |
| `--record` / `-r` | ❌ | 伏笔记录文件（默认 data/foreshadowing.json） |
| `--output` / `-o` | ❌ | 输出报告文件路径 |

## 伏笔记录格式 (data/foreshadowing.json)

```json
{
  "foreshadowings": [
    {
      "id": "FS001",
      "chapter": 1,
      "content": "桌上放着一把古老的钥匙",
      "type": "铺垫",
      "status": "pending",
      "note": "可能是打开密室的钥匙",
      "created_at": "2026-04-04"
    },
    {
      "id": "FS002",
      "chapter": 5,
      "content": "他用那把钥匙打开了密室的门",
      "type": "回收",
      "related_to": "FS001",
      "status": "resolved",
      "note": "伏笔已回收",
      "created_at": "2026-04-05"
    }
  ]
}
```

## 输出报告格式

```markdown
# 伏笔追踪报告

**章节**: chapters/chapter-01.md
**检测时间**: 2026-04-04 23:58:00

## 检测概览

| 类型 | 数量 |
|------|------|
| 新增伏笔 | 3 |
| 待回收伏笔 | 5 |
| 已回收伏笔 | 2 |

## 新增伏笔

### FS003 (暗示)
**内容**: "他不知道，这将是最后一次见面"
**位置**: 第 3 段
**建议**: 后续需要安排再次见面的情节

### FS004 (铺垫)
**内容**: "桌上放着一把古老的钥匙"
**位置**: 第 7 段
**建议**: 后续需要说明钥匙的用途

## 待回收伏笔

| ID | 章节 | 内容 | 状态 |
|----|------|------|------|
| FS001 | 1 | 古老的钥匙 | pending |
| FS002 | 2 | 神秘电话 | pending |

## 已回收伏笔

| ID | 伏笔章节 | 回收章节 | 内容 |
|----|----------|----------|------|
| FS005 | 1 | 3 | 钥匙打开密室 |
```

## 依赖

- Python 3.8+
- rich (终端渲染)
- PyYAML (配置文件解析)

安装依赖：
```bash
pip install -r scripts/requirements.txt
```

## 与其他技能集成

### 与 novel-writer 集成

```bash
# 1. 生成章节正文
python3 ../novel-writer/scripts/write_chapter.py \
  --book-dir projects/my-novel \
  --chapter 1 \
  --output chapters/chapter-01.md

# 2. 追踪伏笔
python3 scripts/track_foreshadowing.py \
  --book-dir projects/my-novel \
  --chapter chapters/chapter-01.md \
  --output reports/chapter-01-foreshadowing.md
```

### 与 quality-checker 集成

```bash
# 1. 质量检测
python3 ../quality-checker/scripts/check_quality.py \
  --input chapters/chapter-01.md

# 2. 伏笔追踪
python3 scripts/track_foreshadowing.py \
  --book-dir projects/my-novel \
  --chapter chapters/chapter-01.md
```

## 注意事项

- 伏笔记录文件会自动创建（如不存在）
- 支持 UTF-8 和 GBK 编码
- 伏笔识别基于关键词匹配，可能需要人工审核
- 建议每章完成后立即进行伏笔追踪
