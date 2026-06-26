---
name: free-search
description: "完全免费的网页搜索，使用 Bing 搜索结果。无需 API key，完全免费使用。当用户需要搜索网页、查找信息时使用此命令。"
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["python3"] } } }
---

# Free Search

完全免费的网页搜索，使用 Bing 搜索结果。

## 何时使用

✅ **使用此命令当：**
- 用户需要搜索网页
- 查找最新信息
- 查找资料或文档
- 需要网络搜索结果

## 使用方法

```bash
python3 /Users/liruozhen/openclaw/skills/ddg-free/scripts/search.py --query "搜索关键词" --max-results 5
```

## 输出格式

返回 JSON 格式，包含：
- `query`: 搜索词
- `results`: 结果数组，每个包含：
  - `title`: 标题
  - `url`: 链接
  - `snippet`: 摘要

## 示例

```bash
python3 /Users/liruozhen/openclaw/skills/ddg-free/scripts/search.py --query "人工智能最新发展" --max-results 3
```

## 特点

- ✅ 完全免费，无需注册
- ✅ 无需 API key
- ✅ 无使用限制
- ✅ 支持中英文搜索
- ✅ 使用 Bing 搜索结果
