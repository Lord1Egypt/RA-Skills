---
name: context-compressor
description: Intelligently compress context — conversations, code, logs. Preserve key information while reducing token usage. Auto-detects content type and applies optimal compression.
tags:
  - context
  - compression
  - productivity
  - agent
  - memory
requires:
  bins:
    - python
  env: []
---

# 上下文压缩器 / Context Compressor

在有限的上下文窗口里装下无限的对话记忆。

Fit more context in less tokens. Not truncation — intelligent compression.

## 核心理念

```
普通截断：  "这是很长的对话..." → "这是很..."           (丢了信息)
智能压缩：  "这是很长的对话..." → "讨论了XX，决定用YY"  (保留核心)
```

**不同内容，不同压缩策略：**
- 💬 对话 → 提取决策、问题、结论
- 💻 代码 → 去噪音保逻辑
- 📋 日志 → 只留错误和关键事件
- 📄 文本 → 摘要式压缩

## 命令参考

COMPRESS = python <skill_dir>/scripts/ctxcompress.py

### 压缩文本

```bash
# 从文件
$COMPRESS compress --input conversation.txt --level medium --type chat

# 从管道
echo "很长的文本..." | $COMPRESS compress --type text

# 内联文本
$COMPRESS compress --text "你的文本内容..." --level aggressive
```

**压缩级别：**
- `light` — 去掉空行和注释，保留所有内容
- `medium` — 去噪音 + 摘要 + 去重（默认）
- `aggressive` — 只保留核心信息

**内容类型（自动检测或手动指定）：**
- `chat` — 对话/聊天记录
- `code` — 代码
- `log` — 日志文件
- `text` — 普通文本

### 提取变更

比较两个文件的差异：

```bash
$COMPRESS diff --old v1.txt --new v2.txt
```

输出：新增了什么、删除了什么、修改了什么。

### 提取关键信息

从文本中提取结构化信息：

```bash
$COMPRESS extract --input chat_history.txt --type chat
```

输出 JSON：
```json
{
  "decisions": ["决定用 Flask 框架"],
  "errors_and_fixes": [{"error": "port 5000 in use", "fix": "改用 8080"}],
  "commands": ["pip install flask"],
  "urls": ["https://flask.palletsprojects.com"],
  "key_terms": ["Flask", "deploy", "gunicorn"]
}
```

### 链式压缩

把多个文件压缩成一个摘要：

```bash
$COMPRESS chain file1.py file2.log conversation.txt --level medium
```

适用于：一个任务涉及多个文件，想一次性了解全貌。

### 分析压缩潜力

```bash
$COMPRESS stats --input big_file.txt
```

显示：总行数、空行占比、注释占比、预估可压缩比例。

## Agent 使用场景

### 场景 1：对话历史压缩

当对话变长时，压缩旧消息以腾出上下文：

```bash
# 导出旧对话
cat old_messages.txt | $COMPRESS compress --type chat --level medium > compressed.txt

# 用压缩后的版本替换原文
```

压缩后保留：
- ✅ 做了什么决定
- ✅ 遇到什么问题，怎么解决的
- ✅ 关键代码片段
- ❌ 去掉了寒暄、重复讨论、中间过程

### 场景 2：错误调试压缩

20 轮试错 → 压缩成 1 段：

```bash
$COMPRESS compress --input debug_session.log --type log --level aggressive
```

输出类似：
```
📊 Log Summary: 15 errors, 3 warnings, 8 key events
ERROR: Connection refused on port 5432
ERROR: Permission denied /var/log/app.log
  (above error repeated 8x)
SUCCESS: Service started on port 8080
```

### 场景 3：跨 Session 记忆传递

把上一个 session 的精华传递给新 session：

```bash
$COMPRESS chain session1_notes.md session1_code.py session1_chat.txt --level aggressive
```

输出：一个紧凑的上下文摘要，注入新 session。

### 场景 4：代码 Review 压缩

长文件压缩后便于快速理解：

```bash
$COMPRESS compress --input big_module.py --type code --level medium
```

去掉了空行、注释、docstring，只留逻辑代码。

## 自动类型检测

根据文件扩展名和内容自动判断：

| 扩展名 | 类型 |
|--------|------|
| `.py`, `.js`, `.ts`, `.go` | code |
| `.log`, `.out`, `.err` | log |
| 包含 "User:" / "Agent:" | chat |
| 其他 | text |

## 数据输出格式

压缩结果包含元信息：

```
🗜️ Compressed: 5234 → 876 chars (83% reduction)
   Type: chat | Level: medium
────────────────────────────────────────
## 决策 / Decisions
- 决定用 PostgreSQL 而不是 MySQL

## 问题 / Issues  
- Error: port 5432 already in use
- Fix: 改用 5433

## 代码 / Code
- [342 chars of code]
```

## 目录结构

```
context-compressor/
├── SKILL.md                 # 本文件
└── scripts/
    └── ctxcompress.py       # CLI 工具
```

## 设计哲学

- **有损但保核心**：像 JPEG 压缩图片一样压缩文本
- **类型感知**：不同内容用不同压缩策略
- **可组合**：支持管道、链式压缩、提取信息
- **零依赖**：纯 Python，不需要额外库

## 局限性

- 不是语义压缩（不理解含义，只做模式匹配）
- 对话压缩依赖格式识别（如果格式不标准可能失败）
- 代码压缩可能误删重要注释（light 模式更安全）
- 没有解压功能（压缩是不可逆的有损过程）
