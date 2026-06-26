# Claude Code 常用命令速查

## 基础命令

```bash
# 一次性执行（推荐）
claude --permission-mode bypassPermissions --print "你的提示词"

# 后台执行
claude --permission-mode bypassPermissions --print "你的提示词" &

# 指定工作目录
cd /path/to/project && claude --permission-mode bypassPermissions --print "你的提示词"
```

## 重要参数

| 参数 | 说明 |
|------|------|
| `--print` | 非交互模式，输出到标准输出 |
| `--permission-mode bypassPermissions` | 跳过权限确认 |
| `--dangerously-skip-permissions` | 跳过权限确认（旧版，可能提前退出） |

## 与 Codex 的区别

1. **不需要 PTY** - Claude Code 使用 `--print` 模式
2. **权限模式** - 使用 `--permission-mode bypassPermissions`
3. **后台执行** - 使用 `background:true` 而非 `&`

## 模型选择

Claude Code 使用 Claude 模型，理解力强，适合：
- 复杂重构
- 架构设计
- 代码审查
- 需要深度理解的任务

## 最佳实践

```bash
# ✅ 推荐
exec workdir:/path/to/project command:"claude --permission-mode bypassPermissions --print '重构用户认证模块，遵循 SOLID 原则'"

# ❌ 避免（可能提前退出）
exec pty:true command:"claude --dangerously-skip-permissions '任务'"
```
