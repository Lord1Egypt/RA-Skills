# Claude Code 配置参考

## 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API 密钥 | `sk-ant-...` |
| `ANTHROPIC_MODEL` | 默认模型 | `claude-sonnet-4-5-20250929` |
| `CLAUDE_CODE_TIMEOUT` | 超时时间 (秒) | `3600` |
| `CLAUDE_CODE_MAX_TURNS` | 最大对话轮数 | `50` |

## 配置文件位置

- **全局配置**: `~/.claude/config.json`
- **项目配置**: `<project>/.claude/settings.json`
- **日志目录**: `~/.claude/logs/`
- **工具目录**: `~/.claude/tools/`

## 项目配置示例

### 基础配置

```json
{
  "model": "claude-sonnet-4-5-20250929",
  "allowedTools": ["bash", "edit", "write", "read"],
  "maxTurns": 50,
  "permissionMode": "auto"
}
```

### 高级配置

```json
{
  "model": "claude-sonnet-4-5-20250929",
  "allowedTools": ["bash", "edit", "write", "read", "mcp"],
  "maxTurns": 100,
  "permissionMode": "auto",
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-filesystem"]
    }
  },
  "customInstructions": "始终使用 TypeScript，遵循 ESLint 规则，编写单元测试",
  "excludeTools": ["web_search"],
  "allowedDirectories": ["./src", "./tests", "./docs"],
  "readOnlyDirectories": ["./config"]
}
```

## 模型选择

### 可用模型

| 模型 | 适用场景 | 速度 | 成本 |
|------|----------|------|------|
| `claude-haiku-4-5-20250929` | 简单任务、快速响应 | 快 | 低 |
| `claude-sonnet-4-5-20250929` | 常规开发、代码审查 | 中 | 中 |
| `claude-opus-4-5-20250929` | 复杂架构、深度分析 | 慢 | 高 |

### 模型切换

```bash
# 命令行指定
claude --model claude-opus-4-5-20250929

# 配置文件指定
{
  "model": "claude-opus-4-5-20250929"
}

# 环境变量指定
export ANTHROPIC_MODEL=claude-opus-4-5-20250929
```

## MCP 服务器配置

### 文件系统 MCP

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-filesystem"],
      "env": {
        "ALLOWED_PATHS": "/home/user/projects"
      }
    }
  }
}
```

### 数据库 MCP

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost/db"
      }
    }
  }
}
```

## 权限模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `auto` | 自动允许安全操作 | 开发环境 |
| `always` | 每次操作都询问 | 生产环境 |
| `never` | 禁止所有写操作 | 审查/只读场景 |

## 自定义指令

在配置中添加 `customInstructions` 指导 Claude 行为:

```json
{
  "customInstructions": "1. 始终使用 TypeScript\n2. 遵循 Airbnb 代码规范\n3. 为新函数编写 JSDoc\n4. 编写单元测试覆盖边界情况\n5. 使用英文注释和提交信息"
}
```

## 故障排除

### 常见问题

**问题**: API 密钥无效
```bash
# 检查密钥格式
echo $ANTHROPIC_API_KEY | grep -E "^sk-ant-"

# 重新设置密钥
export ANTHROPIC_API_KEY="sk-ant-..."
```

**问题**: 模型不可用
```bash
# 检查模型名称是否正确
claude --model claude-sonnet-4-5-20250929 --version

# 查看可用模型
claude --list-models
```

**问题**: 权限被拒绝
```bash
# 检查配置文件权限
ls -la ~/.claude/config.json

# 修复权限
chmod 600 ~/.claude/config.json
```

### 日志查看

```bash
# 查看最新日志
tail -f ~/.claude/logs/latest.log

# 查看错误日志
grep -i error ~/.claude/logs/*.log
```
