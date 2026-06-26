# Codex 常用命令速查

## 基础命令

```bash
# 一次性执行
codex exec "你的提示词"

# 自动批准模式
codex exec --full-auto "你的提示词"

# 无限制模式（危险）
codex exec --yolo "你的提示词"
```

## 代码审查

```bash
# 审查当前分支
codex review --base main

# 审查特定提交
codex exec "审查 commit abc123 的变更"
```

## 配置

配置文件位置：`~/.codex/config.toml`

```toml
[model]
default = "gpt-5.2-codex"

[permissions]
# 允许的模式
```

## 模型选择

- `gpt-5.2-codex` - 默认，平衡性能
- 其他模型可在 config.toml 中配置

## 常见问题

1. **不在 git 目录运行** - 创建临时 git 目录
2. **需要交互确认** - 使用 `--full-auto` 或 `--yolo`
3. **输出乱码** - 确保使用 `pty:true`
