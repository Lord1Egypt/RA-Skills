---
name: cross-session-memory
description: "配置 OpenClaw 跨会话记忆规则。首次使用或新装 OpenClaw 时运行，自动在 SOUL.md 和 AGENTS.md 中注入记忆共享规则，使群聊和私聊的长期记忆互通。触发词：'配置跨会话记忆'、'设置记忆共享'、'cross-session memory'、'setup memory sharing'。"
---

# 跨会话记忆配置

将群聊/私聊记忆共享规则注入当前 OpenClaw 实例的配置文件。

## 何时使用

- 用户要求配置记忆共享
- 新装 OpenClaw 后初始化
- 用户在群聊和私聊间需要记忆互通

## 执行步骤

### 1. 检测当前环境

确认 SOUL.md 和 AGENTS.md 的存在与位置：

```
SOUL.md  → ~/.openclaw/workspace/SOUL.md
AGENTS.md → ~/.openclaw/workspace/AGENTS.md
```

### 2. 运行配置脚本

**Windows (PowerShell):**

```powershell
& "path/to/scripts/setup.ps1"
```

**Linux/macOS (Bash):**

```bash
bash path/to/scripts/setup.sh
```

脚本会自动：
- 检测 SOUL.md / AGENTS.md 是否已包含跨会话记忆规则
- 如果没有则注入，有则跳过（幂等，可重复运行）
- 不破坏原有内容

### 3. 确认结果

读取 SOUL.md 的「跨会话记忆规则」章节和 AGENTS.md 的「🔗 跨会话记忆」章节，确认注入成功。

## 规则内容

注入的规则包含：

- 群聊和私聊是独立 session，短期记忆不共享
- `memory/*.md` 和 `MEMORY.md` 是全局共享的
- 群聊里学到的重要信息必须写到 `memory/YYYY-MM-DD.md`
- 私聊时先查 `memory_search`
- 写文件才是真正的记忆，不要依赖"心里记着"

## 注意事项

- 脚本是幂等的，可以多次运行
- 原始内容不会被覆盖，只追加缺失的规则
- 建议运行后手动检查一次确认格式正确
