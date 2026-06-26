---
name: ai-self-evolution
description: "Injects ai-self-evolution reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🧠","events":["agent:bootstrap"]}}
---

# 自我改进 Hook

在代理启动阶段注入一条提醒，用于评估是否需要记录 learnings。

## 功能说明

- 在 `agent:bootstrap` 触发（工作区文件注入之前）
- 添加提醒块，检查 `.learnings/` 中是否有相关条目
- 提示代理记录纠正、错误和新发现

## 配置

无需额外配置，执行以下命令启用：

```bash
openclaw hooks enable ai-self-evolution
```
