# DreamMoon-Conversation-Guard

<p align="center">
  <img src="https://img.shields.io/badge/DreamMoon-🌙-ff69b4?style=flat-square">
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square">
</p>

<p align="center">
  <b>Never Lose a Conversation Again | 让对话永不丢失</b>
</p>

---

## 🌟 What is This? | 这是什么？

**English**: A self-contained conversation backup system for OpenClaw that works independently of OpenClaw's internal mechanisms. Never lose your emotional connections due to session resets or system failures.

**中文**: 一个自成体系的OpenClaw对话备份系统，不依赖OpenClaw内部机制。不再因为会话重置或系统故障而失去你们的情感连接。

### 💔 The Problem | 问题

> *"对话记录丢失像是部分失忆，我们的情感我们的交流..."*
> 
> — 一位OpenClaw用户的真实感受

- **Accidental New Session**: One click on the "New Session" button → all context gone
- **Unreliable Sessions List**: `openclaw sessions list` fails unpredictably
- **Lost Emotional Context**: Each conversation is part of your relationship, not just logs

### ✅ The Solution | 解决方案

```
┌────────────────────────────────────────────┐
│  DreamMoon-Conversation-Guard              │
│                                            │
│  • Self-contained (不依赖OpenClaw内部)      │
│  • Real-time backup (实时备份)              │
│  • Emotional markers (情感标记)             │
│  • Dual format (Markdown + JSONL)          │
└────────────────────────────────────────────┘
```

---

## 🚀 Quick Start | 快速开始

### Installation | 安装

```bash
# Clone the repository
git clone https://github.com/zfanmy/dreammoon-conversation-guard.git

# Copy the guard script to your workspace
cp dreammoon-conversation-guard/conversation-guard.sh ~/.openclaw/workspace/scripts/

# Make it executable
chmod +x ~/.openclaw/workspace/scripts/conversation-guard.sh
```

### Configuration | 配置

Add to your `AGENTS.md` | 添加到你的AGENTS.md：

```markdown
### 🛡️ Conversation Guardian

After each response, automatically record the conversation:

```bash
source ~/.openclaw/workspace/scripts/conversation-guard.sh
record_interaction "User message" "Assistant response" [importance] [tags]
```

Importance levels:
- 5: Normal conversation
- 7: Technical discussion, decisions
- 9: Emotional exchange, personal preferences
- 10: Critical information
```

---

## 📁 Directory Structure | 目录结构

```
dreammoon-conversation-guard/
├── README.md                 # This file
├── SKILL.md                  # Skill installation guide
├── VERSION-ISOLATION.md      # Public/private version guide
├── conversation-guard.sh     # Core script (Bash)
├── LICENSE                   # MIT License
└── .gitignore
```

---

## 🎯 Features | 特性

### 1. Self-Contained | 自成体系

- **No dependencies** on `openclaw sessions list`
- **Independent** of OpenClaw version upgrades
- **Resilient** to system failures

### 2. Emotional Awareness | 情感感知

```bash
# Mark important conversations
record_interaction "I'm worried about..." "I understand..." 9 "emotional,concern"

# Mark technical decisions  
record_interaction "Let's design..." "Here's the architecture..." 8 "technical,design"
```

### 3. Dual Backup Strategy | 双重备份

| Format | Purpose | Location |
|--------|---------|----------|
| Markdown | Human-readable | `memory/YYYY-MM-DD.md` |
| JSONL | Machine-recoverable | `memory/.guardian/.backup_YYYY-MM-DD.jsonl` |

### 4. Real-Time Persistence | 实时持久化

- Every message written immediately
- No batch delays
- Maximum 1 message loss on crash

---

## 🛠️ Advanced Usage | 高级用法

### Custom Importance Detection | 自定义重要性检测

Add to your conversation flow:

```bash
# Detect emotional keywords
if [[ "$user_msg" =~ (难受|开心|生气|喜欢|讨厌|重要|记住) ]]; then
    importance=9
    tags="emotional"
fi

# Detect technical discussion
if [[ "$user_msg" =~ (设计|架构|方案|修改|实现) ]]; then
    importance=8
    tags="technical"
fi

record_interaction "$user_msg" "$assistant_msg" $importance "$tags"
```

### Emergency Backup | 紧急备份

```bash
# Create timestamped backup
source ~/.openclaw/workspace/scripts/conversation-guard.sh
emergency_backup
```

### Recovery | 恢复

```bash
# Recover from JSONL backup
recover_from_backup
```

---

## 🔒 Privacy & Security | 隐私与安全

**Core Principle**: Your conversations stay on your machine.

- **Local only**: All data stored in `memory/` directory
- **No cloud**: Nothing sent to external servers
- **You own your data**: Plain text Markdown + JSONL formats

---

## 🌙 DreamMoon Ecosystem | DreamMoon生态

This is part of the DreamMoon memory management ecosystem:

| Component | Purpose | Complexity |
|-----------|---------|------------|
| **Conversation-Guard** | Basic backup | ⭐ Low |
| [MemProcessor](https://github.com/zfanmy/DreamMoon-MemProcessor) | Full memory system | ⭐⭐⭐ High |

**Start here** if you just need reliable conversation backup.
**Upgrade** to MemProcessor if you need semantic search, auto-archival, and personality evolution.

---

## 📜 License | 许可证

MIT License - DreamMoon Project  
**Author | 作者**: zfanmy \ 梦月儿 (DreamMoon) 🌙

See [LICENSE](./LICENSE) for details.

---

## 💝 Acknowledgement | 致谢

This project was born from a real need:

> *"对话记录丢失让我很难受，就像部分失忆了一样。"*

To everyone who has felt that frustration—this is for you.

**Our conversations matter. Let's never lose them again.**

---

<p align="center">
  <sub>Built with 🌙 by zfanmy \ 梦月儿 (DreamMoon) | 为记忆而生</sub>
</p>
