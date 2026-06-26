---
name: context-shrink
slug: context-shrink
description: "Auto-compress session memories when context usage exceeds 85%"
type: hook
version: 1.0.2
author: Lin
license: MIT
---

# Context Shrink Hook

Auto-compresses session memories when context usage exceeds 60% threshold. Cleans up old daily logs and compresses them into MEMORY.md for long-term storage.

## Features

- **自动触发**: 当 context 使用率 ≥ 85% 时自动执行
- **智能清理**: 保留最近 3 天的详细日志
- **压缩存储**: 旧日志压缩后写入 MEMORY.md
- **Git 提交**: 自动 commit 变更记录

## Configuration

```typescript
CONTEXT_THRESHOLD = 0.85     // 85% 触发阈值
DAYS_TO_KEEP = 3           // 保留最近 N 天日志
MIN_FILES_TO_KEEP = 5      // 至少保留文件数
COMPRESSION_MODEL = 'ollama/qwen2.5:3b'
```

## Changelog

### 1.0.0
- Initial release
- Auto-compression at 60% threshold
- Git commit on cleanup
