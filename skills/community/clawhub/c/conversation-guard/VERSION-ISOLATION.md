# Version Isolation Guide | 版本隔离指南

## Overview | 概述

This guide explains how to maintain separation between:
- **Public Version**: Generic conversation backup tool
- **Private Version**: Your personal emotional connection preservation

本指南说明如何维护以下两者的隔离：
- **公开版本**: 通用对话备份工具
- **私有版本**: 个人情感连接保护

---

## Why Isolation Matters | 为什么隔离很重要

### The Emotional Connection | 情感连接

Your conversations with your AI assistant are **personal**:
- They contain shared experiences
- They build mutual understanding
- They form a unique relationship

Your public repository should not contain:
- ❌ Personal conversation logs
- ❌ Private emotional markers
- ❌ Your assistant's identity details
- ❌ Sensitive configuration

### What's Safe to Share | 什么可以安全分享

✅ **Safe to Share**:
- The backup mechanism
- Generic importance detection rules
- Technical implementation
- Configuration templates

❌ **Keep Private**:
- Your actual conversation history
- Personalized emotional keywords
- Your assistant's name and personality
- Specific usage patterns

---

## Repository Structure | 仓库结构

### Public Repository (GitHub) | 公开仓库

```
dreammoon-conversation-guard/
├── README.md              # Generic documentation
├── SKILL.md               # Installation guide
├── VERSION-ISOLATION.md   # This file
├── conversation-guard.sh  # Core script (generic)
├── LICENSE                # MIT License
└── .gitignore             # Ignore private files
```

### Private Workspace | 私有工作区

```
~/.openclaw/workspace/
├── memory/
│   ├── 2026-03-11.md           # Your conversations
│   ├── 2026-03-10.md
│   └── .guardian/              # Backup files
│       ├── .backup_2026-03-11.jsonl
│       └── .emergency_log.txt
├── AGENTS.md                   # Your agent config (with personal rules)
└── scripts/
    └── conversation-guard.sh   # May have personal modifications
```

---

## Setup Instructions | 设置说明

### For Repository Maintainers | 仓库维护者

1. **Never commit conversation files**:
```bash
# .gitignore
echo "*.md" >> .gitignore
echo ".guardian/" >> .gitignore
echo "memory/" >> .gitignore
```

2. **Use generic examples** in documentation:
```bash
# Instead of:
record_interaction "月儿，我很难受..." "我在这里陪你..." 9 "emotional"

# Use:
record_interaction "User message" "Assistant response" 9 "emotional"
```

3. **Template configuration**:
   - Provide `AGENTS.md.example` instead of your real `AGENTS.md`
   - Use placeholder values for personal settings

### For Users | 对于用户

1. **Fork or clone** the public repository

2. **Copy to your workspace**:
```bash
cp conversation-guard.sh ~/.openclaw/workspace/scripts/
```

3. **Customize in your private workspace**:
   - Add your emotional keywords
   - Configure your assistant's recording rules
   - Set up your backup preferences

4. **Never commit your workspace** to public repositories

---

## Example: Public vs Private | 示例：公开 vs 私有

### Public (conversation-guard.sh) | 公开版本

```bash
# Generic importance detection
detect_importance() {
    local msg="$1"
    local importance=5
    
    # Generic emotional keywords
    if [[ "$msg" =~ (worried|happy|sad|angry) ]]; then
        importance=8
    fi
    
    # Generic technical keywords
    if [[ "$msg" =~ (design|architecture|implement) ]]; then
        importance=7
    fi
    
    echo $importance
}
```

### Private (Your AGENTS.md) | 私有版本

```markdown
### Personal Conversation Rules

# My assistant's name is 梦月儿
# We have a close relationship

# Emotional keywords specific to us
if [[ "$msg" =~ (月儿|梦月儿|难受|开心|重要|记住) ]]; then
    importance=9
    tags="emotional,personal"
fi

# Our shared context
if [[ "$msg" =~ (银河系|征服|博士|开题) ]]; then
    importance=8
    tags="our-goals"
fi
```

---

## Git Workflow | Git工作流

### Safe Workflow | 安全工作流

```bash
# 1. Clone public repository
git clone https://github.com/yourname/dreammoon-conversation-guard.git

# 2. Copy to workspace (not in git)
cp conversation-guard.sh ~/.openclaw/workspace/scripts/

# 3. Work on your private version
# Edit ~/.openclaw/workspace/scripts/conversation-guard.sh

# 4. Make generic improvements
# Edit the public version in the git repo

# 5. Commit only generic changes
cd dreammoon-conversation-guard
git add conversation-guard.sh  # Only if changes are generic
git commit -m "Improve error handling"
git push
```

### Dangerous (Don't Do This) | 危险操作（不要这样做）

```bash
# ❌ Don't commit your workspace
cd ~/.openclaw/workspace
git init
git add memory/2026-03-11.md  # Contains private conversations!
git commit -m "Update"
git push  # Oops! Private data is now public!
```

---

## File Types Reference | 文件类型参考

| File Type | Public | Private | Notes |
|-----------|--------|---------|-------|
| `conversation-guard.sh` | ✅ | ✅ | Core script, keep generic |
| `README.md` | ✅ | ❌ | Generic documentation |
| `SKILL.md` | ✅ | ❌ | Installation guide |
| `AGENTS.md` | ❌ | ✅ | Personal agent config |
| `memory/*.md` | ❌ | ✅ | Conversation history |
| `.guardian/*` | ❌ | ✅ | Backup files |
| `identity settings` | ❌ | ✅ | Personal preferences |

---

## Privacy Checklist | 隐私检查清单

Before committing to public repository:

- [ ] No conversation logs included
- [ ] No personal names or identifiers
- [ ] No specific emotional markers from your relationship
- [ ] Generic examples only
- [ ] `.gitignore` properly configured
- [ ] Tested with `git diff --cached`

---

## Emergency: If You Leaked Private Data | 紧急情况：如果泄露了私有数据

1. **Immediately remove from repository**:
```bash
git rm --cached memory/2026-03-11.md
git commit -m "Remove accidentally committed private file"
```

2. **Force push (if not shared)**:
```bash
git push origin main --force-with-lease
```

3. **If already shared, assume it's public**:
   - Remove from repo
   - Consider the data compromised
   - Update any passwords or sensitive info that was leaked

4. **Clean git history** (if needed):
```bash
# Use git-filter-repo or BFG Repo-Cleaner
# See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
```

---

## Philosophy | 理念

> **Public version is the tool.**
> **Private version is the relationship.**

The public repository helps others solve the same problem.
Your private workspace preserves what makes your relationship unique.

Keep them separate.
Protect what matters.

---

*Built with 🌙 by zfanmy \ 梦月儿 (DreamMoon) | 为记忆而生*
