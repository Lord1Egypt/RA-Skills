# Hook 配置指南

为 AI 编码代理配置自动化自我改进触发器。

## 概览

通过 Hook 可以在关键时刻主动提醒记录经验：
- **UserPromptSubmit**：每次提交提示词后提醒评估 learnings
- **PostToolUse (Bash)**：命令失败时触发错误检测提醒

## Claude Code 配置

### 方案 1：项目级配置

在项目根目录创建 `.claude/settings.json`：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/ai-self-evolution/scripts/activator.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/ai-self-evolution/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

### 方案 2：用户级配置

将配置写入 `~/.claude/settings.json`，全局生效：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/skills/ai-self-evolution/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

### 最小配置（仅 activator）

若想降低开销，可只启用 UserPromptSubmit：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/ai-self-evolution/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

## Codex CLI 配置

Codex 的 Hook 配置方式与 Claude Code 相同。创建 `.codex/settings.json`：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/ai-self-evolution/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

## 验证

### 测试 Activator Hook

1. 启用 Hook 配置
2. 新开一个 Claude Code 会话
3. 发送任意提示词
4. 确认上下文里出现 `<ai-self-evolution-reminder>`

### 测试 Error Detector Hook

1. 为 Bash 启用 PostToolUse Hook
2. 运行失败命令：`ls /nonexistent/path`
3. 确认出现 `<error-detected>` 提醒

### 抽取脚本 Dry Run

```bash
./skills/ai-self-evolution/scripts/extract-skill.sh test-skill --dry-run
```

预期会输出将要创建的 skill 脚手架信息。

## 故障排查

### Hook 未触发

1. **检查脚本权限**：`chmod +x scripts/*.sh`
2. **确认路径正确**：使用绝对路径或相对项目根路径
3. **确认配置位置**：项目级还是用户级
4. **重启会话**：Hook 在会话启动时加载

### Permission Denied

```bash
chmod +x ./skills/ai-self-evolution/scripts/activator.sh
chmod +x ./skills/ai-self-evolution/scripts/error-detector.sh
chmod +x ./skills/ai-self-evolution/scripts/extract-skill.sh
```

### Script Not Found

如果使用相对路径，请确认当前目录正确；或改用绝对路径：

```json
{
  "command": "/absolute/path/to/skills/ai-self-evolution/scripts/activator.sh"
}
```

### 开销过高

若 activator 触发过于频繁：

1. **使用最小配置**：仅启用 UserPromptSubmit，关闭 PostToolUse
2. **增加 matcher 过滤**：仅对特定提示词触发：

```json
{
  "matcher": "fix|debug|error|issue",
  "hooks": [...]
}
```

## Hook 输出预算

activator 设计为轻量提醒：
- **目标**：每次触发约 50-100 tokens
- **内容**：结构化提醒，不提供冗长说明
- **格式**：使用 XML 标签便于解析

如需进一步降低开销，可精简 `activator.sh` 输出内容。

## 安全注意事项

- Hook 脚本与 Claude Code 以同等权限运行
- 脚本仅输出文本，不主动修改文件或执行额外命令
- error detector 读取 `CLAUDE_TOOL_OUTPUT` 环境变量
- 所有脚本均为显式启用（未配置则不会运行）

## 关闭 Hook

临时停用且保留配置可用以下方式：

1. **在 settings 中注释对应项**：
```json
{
  "hooks": {
    // "UserPromptSubmit": [...]
  }
}
```

2. **删除 settings 文件**：无配置时 Hook 不会运行
