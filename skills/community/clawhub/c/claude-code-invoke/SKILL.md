---
name: claude-code-invoke
description: '通过 claude -p 命令调用 Claude Code 执行单次 Prompt 任务。当用户要求"用 Claude Code 执行 XXX"、"调用 claude -p"、"用 Claude Code 调查/分析 XXX" 时使用。前提：目标目录必须是 Git 仓库。'
metadata:
  {
    "openclaw": { "emoji": "🤖", "requires": { "anyBins": ["claude"] } },
  }
---

# Claude Code Invoke Skill

通过 `claude -p` 命令调用 Claude Code 执行单次 Prompt 任务。

## 使用场景

✅ **USE this skill when:**

- 用户要求"用 Claude Code 执行 XXX"
- 用户要求"调用 claude -p"
- 用户要求"用 Claude Code 调查/分析 XXX"
- 用户要求"用 Claude Code 查询/获取 XXX 数据"

## 核心命令格式

```bash
cd <目标Git仓库目录> && claude -p "<prompt内容>" --dangerously-skip-permissions
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `目标目录` | Claude Code 要求在 Git 仓库内运行 |
| `prompt内容` | 要执行的任务描述 |
| `--dangerously-skip-permissions` | 跳过权限确认，直接执行 |

## 执行方式

### 方式1：exec 工具（推荐，无PTY）

```bash
powershell -Command "cd '<目标目录>'; claude -p '<prompt>' --dangerously-skip-permissions"
```

### 方式2：exec 工具（标准 PowerShell）

```bash
Set-Location '<目标目录>'; claude -p '<prompt>' --dangerously-skip-permissions
```

### 方式3：背景执行

```bash
powershell -Command "cd '<目标目录>'; claude -p '<prompt>' --dangerously-skip-permissions"
# 使用 timeout 控制执行时间
```

## 常见用法示例

### 研究与分析

```bash
# 调查投资研究代码
powershell -Command "cd 'C:\Users\gold3\Code\investment-research-team'; claude -p '分析 research.ps1 的功能和使用方式' --dangerously-skip-permissions"

# 获取港股财报数据
powershell -Command "cd 'C:\Users\gold3\Code\investment-research-team'; claude -p '能否获取港股上市公司吉利的2025年的财报' --dangerously-skip-permissions"
```

### 代码审查

```bash
# 审查代码问题
powershell -Command "cd '<项目目录>'; claude -p 'Review this code for bugs: <file>' --dangerously-skip-permissions"
```

### 数据查询

```bash
# 查询数据
powershell -Command "cd '<项目目录>'; claude -p '查询A股市场今日行情数据' --dangerously-skip-permissions"
```

## 重要限制

1. **必须是 Git 仓库** — Claude Code 要求在 Git 仓库目录内运行
2. **Windows PowerShell 兼容** — 使用 `powershell -Command` 或 `Set-Location` 避免 `&&` 语法错误
3. **建议设置 timeout** — 60秒足够大多数单次任务
4. **不需要 PTY** — `claude -p` 是非交互模式，不需要 pty:true

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| `&&` 语法错误 | 使用 `powershell -Command` 或 `Set-Location ...;` |
| 不是 Git 仓库 | 先 `git init` 初始化，或切换到已有 Git 仓库 |
| 超时 | 增加 timeout 参数（建议60-120秒） |
| 无输出 | 检查 claude CLI 是否正确安装 |

## 执行示例

```bash
# 完整调用示例
powershell -Command "Set-Location 'C:\Users\gold3\Code\investment-research-team'; claude -p '能否获取港股上市公司吉利的2025年的财报' --dangerously-skip-permissions"
```
