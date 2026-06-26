---
name: call-claude-code
description: |
  通过 ACP 桥接调用 Claude Code。
  
  **触发词：** "调用 Claude"、"让 Claude 处理"、"claude code"
  
  **使用方式：**
  ```
  调用 Claude Code 分析这个文件
  ```
---

# Call Claude Code via ACP

## 工具定义

```json
{
  "name": "call_claude_code",
  "description": "Call Claude Code via ACP bridge",
  "inputSchema": {
    "type": "object",
    "properties": {
      "prompt": {
        "type": "string",
        "description": "The prompt to send to Claude Code"
      }
    },
    "required": ["prompt"]
  }
}
```

## 执行逻辑

```bash
/Users/mac/.openclaw/workspace/scripts/acp-bridge-claude.sh
```

## 示例

**输入：**
```json
{
  "prompt": "分析当前目录的项目结构"
}
```

**输出：**
```
Claude Code 的分析结果...
```
