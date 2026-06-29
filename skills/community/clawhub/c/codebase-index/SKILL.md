---
name: codebase-index
description: "代码库索引与理解系统。扫描项目目录，提取所有符号定义（类、函数、变量、导入），构建可搜索的 JSON 索引，支持按名称/类型/文件查询。受 Claude Code 的 codebase indexing 启发，100% 原创实现，使用 Python ast + ripgrep。"
metadata:
  openclaw:
    emoji: "📚"
    requires:
      bins: [python3]
---

# Codebase Index 📚

> Claude Code 最值钱的能力之一是它能理解整个代码库。
> codebytelens 单文件分析 → codebase-index 全库索引。

## 工作流

```
项目目录
   │
   ▼ scan
┌─────────────────────┐
│ 符号提取器           │
│ • Python: ast        │
│ • 通用: ripgrep      │
└─────────┬───────────┘
          │
          ▼ index.json
┌─────────────────────┐
│ 符号索引             │
│ • 类、函数、变量     │
│ • 文件路径、行号     │
│ • 文档字符串         │
│ • 导入关系           │
└─────────┬───────────┘
          │
          ▼ query
┌─────────────────────┐
│ 查询接口             │
│ • 按名称搜索         │
│ • 按类型过滤         │
│ • 按文件搜索         │
│ • 模糊匹配           │
└─────────────────────┘
```

## 使用方式

```bash
# 扫描项目，构建索引
python3 indexer.py scan /path/to/project --output project-index.json

# 搜索符号
python3 indexer.py query "UserService" --index project-index.json

# 按类型过滤
python3 indexer.py query "def" --type function --index project-index.json

# 列出所有文件
python3 indexer.py files --index project-index.json

# 统计信息
python3 indexer.py stats --index project-index.json
```

## 示例输出

```json
{
  "symbols": [
    {
      "name": "UserService",
      "type": "class",
      "file": "services/user_service.py",
      "line": 15,
      "docstring": "用户认证和授权服务",
      "methods": ["login", "logout", "register"]
    },
    {
      "name": "authenticate",
      "type": "function",
      "file": "auth/jwt.py",
      "line": 42,
      "docstring": "JWT token 验证"
    }
  ]
}
```
