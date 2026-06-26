# Agent Brainstorm Chair — Setup Guide

> **大多数情况下你不需要看这个。** 加载 SKILL.md 后会自动检测环境。
> 以下仅针对需要手动干预的少数场景。

---

## 你什么时候需要看这个

1. 自检测选了模拟模式，但你想强制用 ACP 多 Agent
2. 自检测找到了 Agent 但角色分配不对
3. 想自定义环境变量

---

## 场景一：自检测选了模拟模式，但你有 OpenClaw

设置环境变量后重新加载技能：

```bash
export OPENCLAW_BIN=/path/to/openclaw
export OPENCLAW_HOME=~/.openclaw
```

---

## 场景二：手动指定 Agent 角色

运行 `ls ~/.openclaw/agents/` 找到可用 Agent ID，然后在首次征询时手动指定：

```bash
python3 scripts/openclaw_meeting_round.py \
  --agents "your-strategist-id,your-executor-id" \
  --topic "测试议题"
```

---

## 场景三：自定义 Mention 协议

```bash
# Slack
python3 scripts/build_baton.py \
  --mention-template '<@{{speaker}}>' \
  --next-template '→ {{speaker}}' ...

# Discord
python3 scripts/build_baton.py \
  --mention-template '<@{{speaker}}>' \
  --next-template 'next: {{speaker}}' ...

# 纯文本（群聊无 bot mention 能力时）
python3 scripts/build_baton.py \
  --mention-template '**{{speaker}}**' \
  --next-template '>>> {{speaker}}' ...
```

---

## 运行测试

```bash
cd agent-brainstorm-chair
python3 -m pytest tests/ -v
```
