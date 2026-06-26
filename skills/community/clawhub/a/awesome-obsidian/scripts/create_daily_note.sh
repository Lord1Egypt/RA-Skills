#!/bin/bash
# 创建每日笔记

VAULT_PATH="${OBSIDIAN_VAULT:-/home/sandbox/.openclaw/workspace/repo/obsidian-vault}"
JOURNAL_DIR="$VAULT_PATH/journal"
DATE=$(date +%Y-%m-%d)
NOTE_FILE="$JOURNAL_DIR/$DATE.md"

# 检查是否已存在
if [ -f "$NOTE_FILE" ]; then
    echo "📝 今日笔记已存在: $NOTE_FILE"
    exit 0
fi

# 创建笔记
cat > "$NOTE_FILE" << EOF
---
title: $DATE
date: $DATE
tags: [daily]
---

# $DATE $(date +%A)

## Timeline

- $(date +%H:%M) —

## Tasks

- [ ]

## Notes

## Gratitude

1.
2.
3.
EOF

echo "✅ 创建今日笔记: $NOTE_FILE"
