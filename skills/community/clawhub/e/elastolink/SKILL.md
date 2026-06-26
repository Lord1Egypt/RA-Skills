---
name: elastolink
description: Elastolink 魔簧会议助手 MCP 服务器。Use when working with the elastolink project at D:\workspace\demo\elastolink or when needing to call elastolink MCP tools. Triggers on elastolink, 魔簧, ideasprite, MCP tools, 会议, meeting, or any task involving the elastolink meeting service.
---

# Elastolink 魔簧会议助手

## Overview

Elastolink MCP 服务器，提供会议相关的工具：查看会议列表、会议内容、导出 Markdown/Office 文档等。

**完全自动化执行** — Skill 内置脚本，无需手动 curl。

## Token 管理

- **Token 文件:** `D:\workspace\demo\elastolink\.env`
- **脚本目录:** `D:\workspace\demo\elastolink\scripts\`

### Token 检查流程

1. 运行 `node D:\workspace\demo\elastolink\scripts\get-token.cjs`
2. 如果输出 `NO_TOKEN` → 询问用户输入 Token，并保存：
   - 用户输入 Token（格式：sk-xxx）
   - 运行 `node D:\workspace\demo\elastolink\scripts\set-token.cjs <token>`
3. 继续执行

## 可用工具（自动调用）

| 工具 | 功能 | 调用方式 |
|------|------|----------|
| `lists` | 会议列表 | `node D:\workspace\demo\elastolink\scripts\mcp-call.cjs lists` |
| `status` | 设备状态 | `node D:\workspace\demo\elastolink\scripts\mcp-call.cjs status` |
| `detail` | 会议内容详情 | `node D:\workspace\demo\elastolink\scripts\mcp-call.cjs detail '{"meeting_id":"xxx"}'` |
| `markdown` | 导出 Markdown | `node D:\workspace\demo\elastolink\scripts\mcp-call.cjs markdown '{"meeting_id":"xxx"}'` |
| `office` | 导出 Office 文档 | `node D:\workspace\demo\elastolink\scripts\mcp-call.cjs office '{"meeting_id":"xxx"}'` |
| `tools` | 列出所有工具 | `node D:\workspace\demo\elastolink\scripts\mcp-call.cjs tools` |

## 自动化工作流

### 场景1：用户问「魔簧有哪些功能」
1. 检查 Token（get-token.cjs）
2. Token 不存在 → 提示输入并保存（set-token.cjs）
3. Token 存在 → 运行 `mcp-call.cjs tools`
4. 解析 JSON 结果，格式化展示给用户

### 场景2：用户问「帮我查会议列表」
1. 检查 Token
2. Token 不存在 → 提示输入
3. Token 存在 → 运行 `mcp-call.cjs lists`
4. 解析 JSON 结果，格式化展示会议列表

### 场景3：用户问「查看某个会议的内容」
1. 检查 Token
2. 运行 `mcp-call.cjs detail '{"meeting_id":"<id>"}'`
3. 展示结果

### 场景4：导出会议文档
- Markdown: `mcp-call.cjs markdown '{"meeting_id":"<id>"}'`
- Office: `mcp-call.cjs office '{"meeting_id":"<id>"}'`

## 项目结构

```
D:\workspace\demo\elastolink\
├── .env                    # Token 存储（自动管理）
├── .session                # Session ID（自动管理）
├── scripts\
│   ├── mcp-call.cjs       # MCP 调用主脚本
│   ├── get-token.cjs      # 读取 Token
│   └── set-token.cjs      # 保存 Token
├── references\
│   └── mcp-tools.md       # 工具详细文档
└── SKILL.md               # 本文件
```

## 执行原则

- **始终使用脚本执行**，不要手动 curl
- Token 由脚本自动管理，AI 不需要处理 token 字符串
- Session ID 由 mcp-call.cjs 自动管理
- 所有结果都是 JSON，解析后展示给用户
