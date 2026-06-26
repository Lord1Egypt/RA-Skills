---
name: engram-mcp-server
description: Engram MCP Server — 给 AI 注入可切换的专家记忆（谁 + 知道什么 + 怎么思考）。支持 Claude Code / Cursor / Codex 等 MCP 客户端。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["uvx"] },
      "install": [
        {
          "id": "uv",
          "kind": "shell",
          "command": "curl -LsSf https://astral.sh/uv/install.sh | sh",
          "label": "Install uv/uvx"
        }
      ]
    }
  }
---

# Engram MCP Server

把专家记忆封装成可加载资源：不仅是知识检索，还包含角色、工作流、规则与动态记忆。

## 适用场景

- 你希望 AI 在不同专家人设间快速切换
- 你需要跨会话持久化用户偏好与关键事实
- 你想在 MCP 客户端里统一管理 memory / knowledge / examples

## 快速安装（推荐）

```bash
claude mcp add --scope user engram-server -- uvx --from git+https://github.com/DazhuangJammy/Engram engram-server
```

## 常用命令

```bash
# 启动 MCP Server
engram-server serve

# 启动可视化 UI
engram-server ui
```

## 关键能力

- 零向量依赖（不强绑 chromadb/litellm）
- 索引驱动分层加载（role/workflow/rules 常驻 + knowledge/examples 按需读）
- 动态记忆、工具轨迹、记忆纠错与归档
- 支持多种 MCP 客户端集成

## 参考

- GitHub: https://github.com/DazhuangJammy/Engram
- 文档：README.md
