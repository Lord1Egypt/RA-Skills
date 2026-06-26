# Claude Code CLI 配置参考

## 配置文件位置

- `~/.claude/settings.json` - 主配置文件
- `~/.claude/settings.local.json` - 本地覆盖（不共享）
- `~/.claude/sessions/<uuid>.json` - 会话持久化

## API 认证配置

### Bailian API (百炼)

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-bailian-api-key",
    "ANTHROPIC_BASE_URL": "https://coding.dashscope.aliyuncs.com"
  }
}
```

### 其他兼容 API

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-token",
    "ANTHROPIC_BASE_URL": "https://your-api-endpoint"
  }
}
```

**注意：** Claude Code CLI 使用 Anthropic-compatible 格式，但官方 Claude.ai OAuth 认证无法用于 API Key 场景。

## 模型配置

### 设置默认模型

```json
{
  "model": "claude-sonnet-4-20250514"
}
```

### Bailian 模型映射

| Bailian Model ID | Claude Equivalent |
|------------------|-------------------|
| bailian/qwen3.5-plus | Sonnet-class |
| bailian/glm-5 | Claude-class |
| bailian/kimi-k2.5 | Claude-class |

## 会话持久化

### 会话文件结构

`~/.claude/sessions/<uuid>.json`:
```json
{
  "sessionId": "uuid",
  "cwd": "/path/to/project",
  "model": "model-id",
  "messages": [...],
  "toolCalls": [...],
  "createdAt": "ISO-timestamp",
  "updatedAt": "ISO-timestamp"
}
```

### 恢复会话

命令行方式：
```bash
claude --resume <session-id>
```

OpenClaw 方式：
```json
{
  "runtime": "acp",
  "resumeSessionId": "<uuid>",
  "agentId": "claude-code"
}
```

## Channels 限制说明

**重要：** Claude Code Channels 功能需要 claude.ai OAuth 认证，无法使用 API Key。

官方文档明确：
> "Channels require claude.ai authentication (not API keys)"

### 替代方案

使用 OpenClaw 作为桥接：
- OpenClaw 接收用户消息（Telegram/WebChat）
- 通过 PTY 转发到 Claude Code CLI
- Claude Code 输出返回给用户

## 性能优化配置

### Token 缓存

```json
{
  "enableTokenCache": true
}
```

### 并发限制

```json
{
  "maxConcurrentToolCalls": 5
}
```

### 思考模式

```json
{
  "thinking": "high"
}
```

或通过命令：
```
/thinking high
```

## 工具权限配置

### 允许特定工具

```json
{
  "allowedTools": ["Read", "Write", "Edit", "Bash"]
}
```

### 禁止危险操作

```json
{
  "disallowedTools": ["Bash(rm *)", "Bash(sudo *)"]
}
```

## MCP 服务器配置

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["--root", "/path/to/project"]
    }
  }
}
```

## 常用命令

| 命令 | 用途 |
|------|------|
| `/help` | 显示帮助 |
| `/status` | 会话状态 |
| `/clear` | 清除历史 |
| `/compact` | 压缩历史 |
| `/cost` | Token 使用量 |
| `/model` | 切换模型 |
| `/thinking` | 切换思考模式 |
| `/cd` | 切换目录 |

## 故障排除

### API 连接失败
检查：
1. `ANTHROPIC_BASE_URL` 是否正确
2. API Key 是否有效
3. 网络是否可达

### 会话恢复失败
检查：
1. 会话文件是否存在
2. Session ID 是否正确
3. 工作目录是否可访问

### PTY 卡住
解决：
1. 发送空消息唤醒
2. 重启会话
3. 检查终端环境