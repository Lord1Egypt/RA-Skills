---
name: code-snippet
version: 1.0.0
description: 代码片段收藏夹。快速保存和搜索常用代码片段，支持多语言和高亮。适合开发者积累代码库。
author: 你的名字
triggers:
  - "代码片段"
  - "代码收藏"
  - "snippet"
  - "代码库"
---

# Code Snippet 📝

收藏和管理常用代码片段。

## 功能

- 💾 保存代码片段
- 🔍 快速搜索
- 🏷️ 标签分类
- 📋 一键复制

## 使用方法

### 添加片段

```bash
python3 scripts/snippet.py add "Python读取文件" --code "with open('file.txt') as f:" --lang python --tag 文件操作
```

### 搜索

```bash
python3 scripts/snippet.py search "读取文件"
```

### 列出

```bash
python3 snippets.py list --tag python
```

### 复制

```bash
python3 snippets.py get 1
```

## 示例

```bash
# 添加 Python 代码片段
python3 scripts/snippet.py add "读取JSON" --code "import json\nwith open('file.json') as f: data = json.load(f)" --lang python

# 搜索
python3 scripts/snippet.py search "JSON"

# 按标签列出
python3 scripts/snippet.py list --tag python
```
