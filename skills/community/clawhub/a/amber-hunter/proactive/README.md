---
name: amber-proactive
version: 3.1.0
description: "Amber proactive memory capture. Zero-LLM script — pushes session extraction tasks to the queue. Extraction is handled by the agent's models during heartbeat. Supports bilingual triggers (Chinese + English)."
---

# Amber-Proactive Skill

> 让琥珀主动记忆，无需开口。

---

## 工作原理

```
cron（每15分钟）
  → proactive-check.js V3.1（Zero-LLM）
    → 检查 session 消息数 ≥ 20 条
    → 写入待提取队列 pending_extract.jsonl
agent heartbeat（每 10 分钟）
    → 读取 pending_extract.jsonl
    → 调用自身的大模型提取关键事实
    → 写入胶囊到 amber-hunter
```

**Zero-LLM**：脚本内部只负责整理对话文本，不调用外部大模型，无需配置 API Key，完全依赖 Agent 自身能力处理信息。

---

## 触发方式

### 自动触发（cron，每15分钟）

阈值：session 消息数 ≥ 20 条。

### 手动触发（agent）

| 中文 | English |
|------|---------|
| 保存、记住、冻结、留住 | save, remember, freeze, capture |

手动不受消息数量限制，任意对话量都能触发。

---

## 使用方式

```bash
# 自动（cron 触发）
node ~/.openclaw/workspace/skills/amber-proactive/scripts/proactive-check.js

# 手动强制触发
node ~/.openclaw/workspace/skills/amber-proactive/scripts/proactive-check.js --manual
```

---

## 日志

```bash
tail -f ~/.amber-hunter/amber-proactive.log
```

---

## 文件结构

```
amber-hunter/
└── proactive/
    ├── README.md
    └── scripts/
        └── proactive-check.js   # V3.1 Zero-LLM script
```

---

## 版本历史

- **v3.1.0**：回归架构初衷，脚本移除 LLM 调用 (Zero-LLM)，变为纯队列推送，由 agent 的 heartbeat 流程完成提取和写入。
- **v0.4.1**：完全自包含，脚本内部完成 LLM 提取+写胶囊，cron 直接触发，不需要 agent (V4)
- **v0.3.0**：LLM extraction via agent model（实验版）
- **v0.2.0**：Signal-based capture（已废弃）
- **v0.1.0**：Initial

---

*Built for the [Huper琥珀](https://huper.org) ecosystem.*
