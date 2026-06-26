---
name: claude-statusline
version: 1.0.0
description: |
  Claude Code 状态栏 - 显示Git分支、模型、Context用量、输出Token、花费、时长、代码改动行数
  
  功能：实时显示Claude Code会话状态
tags:
  - claude-code
  - statusline
  - productivity
---

# Claude Code 状态栏

显示 Claude Code 会话的状态信息。

## 功能

- Git分支显示
- 当前使用模型
- Context用量
- 输出Token数量
- 会话时长
- 代码改动行数

## 安装

### 第一步：配置 settings.json

在 `~/.claude/settings.json` 中添加：

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline-command.sh"
  }
}
```

### 第二步：创建脚本

将以下脚本保存到 `~/.claude/statusline-command.sh`：

```bash
#!/bin/bash
# Claude Code Status Line Script

get_git_branch() {
    if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        git_branch=$(git branch --show-current 2>/dev/null | tr -d '\n')
        [ -z "$git_branch" ] && git_branch=$(git symbolic-ref --short HEAD 2>/dev/null | tr -d '\n')
    fi
    [ -z "$git_branch" ] && git_branch="no-git"
}

get_model() {
    model_name=$(grep -o '"model": *"[^"]*"' ~/.claude/settings.json 2>/dev/null | cut -d'"' -f4 | tr -d '\n')
    [ -z "$model_name" ] && model_name="unknown"
}

get_changed_lines() {
    if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        changed=$(git diff --stat 2>/dev/null | tail -1 | awk '{print $1"+"$4}' | tr -d '\n')
        [ -z "$changed" ] || [ "$changed" = "+" ] && changed="0+0"
        changed_lines="$changed"
    else
        changed_lines="no-git"
    fi
}

main() {
    get_git_branch
    get_model
    get_changed_lines
    echo "${git_branch} | ${model_name} | N/A | N/A | N/A | N/A | ${changed_lines}"
}

main
```

### 第三步：添加执行权限

```bash
chmod +x ~/.claude/statusline-command.sh
```

## 效果

重新启动 Claude Code 后，状态栏将显示：

```
git_branch | model_name | N/A | N/A | N/A | N/A | 10+5
```

## 前提条件

- 需要 `jq`（用于解析 JSON）：`brew install jq`
- 需要在 Git 仓库中（否则显示 no-git）

## 自定义

可根据需要修改脚本，例如：
- 添加 Context 用量检测
- 添加 Token 统计
- 添加花费计算
- 添加会话时长

---

MIT License
