# Agent Commands Reference

各开发工具 Agent 的状态检查命令参考。

---

## Claude Code

### 进程检查
```bash
ps aux | grep -i "claude" | grep -v grep
```

### 会话目录
```bash
# macOS/Linux
~/.claude/sessions/

# 查看最近会话
ls -lt ~/.claude/sessions/*.json | head -5
```

### 日志
```bash
# 查看日志目录
~/.claude/logs/
```

---

## OpenClaw

### 状态命令
```bash
openclaw status
openclaw status --all
openclaw sessions list
```

### 进程检查
```bash
ps aux | grep -i "openclaw" | grep -v grep
```

### 会话目录
```bash
~/.openclaw/agents/main/sessions/
```

### 日志
```bash
openclaw logs --follow
openclaw logs --tail 50
```

### Dashboard
```
http://127.0.0.1:18789
```

---

## OpenCode

### 安装位置
```bash
~/.opencode/
~/.opencode/bin/opencode
```

### 版本检查
```bash
~/.opencode/bin/opencode --version
```

### 配置目录
```bash
~/.config/opencode/opencode.json
~/.local/state/opencode/      # 会话状态
~/.local/share/opencode/      # 数据
```

### 进程检查
```bash
ps aux | grep -i "opencode" | grep -v grep
```

### 会话日志
```bash
# 查看 prompt 历史
cat ~/.local/state/opencode/prompt-history.jsonl
```

---

## Cursor

### 进程检查
```bash
ps aux | grep -i "cursor" | grep -v grep
```

### 项目历史
```bash
# Cursor 通常存储在项目本地
.cursor/
```

---

## Windsurf

### 进程检查
```bash
ps aux | grep -i "windsurf" | grep -v grep
```

---

## 通用命令

### 所有 Node.js 进程
```bash
ps aux | grep node | grep -v grep
```

### 占用端口的进程
```bash
# 查看常用 AI 工具端口
lsof -i :18789  # OpenClaw
lsof -i :8080   # 常见开发服务器
```

### 最近修改的文件
```bash
# 查找最近 1 小时内修改的日志/会话文件
find ~ -name "*.log" -o -name "sessions.json" -mmin -60 2>/dev/null
```
