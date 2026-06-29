---
name: codebytelens
description: "代码智能分析工具箱。受 Claude Code LSPTool 设计模式启发，但使用 100% 开源工具：ripgrep (搜索)、pyright (Python 类型检查)、tree-sitter (AST 解析)。不需要 LSP 服务器，开箱即用。"
metadata:
  openclaw:
    emoji: "🔬"
    requires:
      bins: [python3]
---

# OpenClaw Code Intel 🔬

> 灵感来自 Claude Code 的 LSP 代码智能架构，实现完全原创。
> 使用标准开源工具：ripgrep、pyright、AST 解析。

## 功能

| 操作 | Claude Code LSPTool | OpenClaw Code Intel |
|------|-------------------|-------------------|
| 搜索定义 | textDocument/definition | ripgrep + 正则模式匹配 |
| 查找引用 | textDocument/references | ripgrep 全局搜索 |
| 符号列表 | documentSymbol | AST 解析 (Python) |
| 类型检查 | hover (类型信息) | pyright 类型检查 |
| 调用图 | callHierarchy | 静态分析 (import/function graph) |

## 前提

```bash
# 安装依赖
pip install pyright  # Python 类型检查
```

## 使用方式

```bash
# 分析 Python 文件结构
python3 {{SKILL_DIR}}/scripts/analyze.py symbols path/to/file.py

# 搜索定义
python3 {{SKILL_DIR}}/scripts/analyze.py define "ClassName.method" path/to/

# 生成函数调用图
python3 {{SKILL_DIR}}/scripts/analyze.py calls path/to/file.py

# 代码复杂度报告
python3 {{SKILL_DIR}}/scripts/analyze.py complexity path/to/file.py
```
