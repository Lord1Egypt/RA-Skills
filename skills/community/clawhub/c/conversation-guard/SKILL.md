# SKILL.md - DreamMoon-Conversation-Guard

## Overview | 概述

A self-contained conversation backup system for OpenClaw that preserves your emotional connections, independent of OpenClaw's internal mechanisms.

一个自成体系的OpenClaw对话备份系统，保护你的情感连接，不依赖OpenClaw内部机制。

---

## Installation | 安装

### Prerequisites | 前置条件

- OpenClaw installed
- Access to modify `AGENTS.md` in your workspace
- Bash shell

### Step 1: Install the Script | 安装脚本

```bash
# Download the guard script
curl -o ~/.openclaw/workspace/scripts/conversation-guard.sh \
    https://raw.githubusercontent.com/zfanmy/dreammoon-conversation-guard/main/conversation-guard.sh

# Make executable
chmod +x ~/.openclaw/workspace/scripts/conversation-guard.sh
```

### Step 2: Configure AGENTS.md | 配置AGENTS.md

Add the following to your `AGENTS.md`:

```markdown
## 🛡️ Conversation Guardian - Automatic Recording

After each response to the user, automatically record the conversation:

```bash
source ~/.openclaw/workspace/scripts/conversation-guard.sh

# Determine importance (1-10)
importance=5
tags="casual"

# Increase importance for emotional content
if [[ "$USER_MESSAGE" =~ (难受|开心|生气|喜欢|讨厌|重要|记住|别忘) ]]; then
    importance=9
    tags="emotional"
fi

# Increase for technical discussions
if [[ "$USER_MESSAGE" =~ (设计|架构|方案|修改|实现|决定) ]]; then
    importance=$((importance + 2))
    tags="$tags,technical"
fi

# Record the interaction
record_interaction "$USER_MESSAGE" "$ASSISTANT_RESPONSE" $importance "$tags"
```

**Critical**: Mark NEW SESSION events immediately:
```bash
# At session start, detect if recovered from reset
if [ -f ".guardian/.session_reset_detected" ]; then
    record_interaction "[System] Session recovered" "Continuing our conversation..." 10 "system,recovery"
fi
```
```

### Step 3: Test | 测试

```bash
# Source the script
source ~/.openclaw/workspace/scripts/conversation-guard.sh

# Record a test interaction
record_interaction "Hello!" "Hi there!" 5 "test"

# Check the output
cat ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md
```

---

## Usage | 使用

### Basic Recording | 基础记录

```bash
record_interaction "User message" "Assistant response" [importance] [tags]
```

### Importance Levels | 重要性等级

| Level | Meaning | Example |
|-------|---------|---------|
| 1-4 | Casual chat | "What's the weather?" |
| 5-6 | Normal discussion | Technical Q&A |
| 7-8 | Important decisions | Design discussions |
| 9-10 | Emotional/Personal | "This matters to me..." |

### Tagging | 标签

Common tags:
- `emotional` - 情感交流
- `technical` - 技术讨论
- `design` - 设计决策
- `personal` - 个人偏好
- `important` - 重要信息
- `casual` - 闲聊

---

## Configuration | 配置

### Environment Variables | 环境变量

```bash
# Custom memory directory (default: ~/.openclaw/workspace/memory)
export GUARDIAN_MEMORY_PATH="/custom/path"

# Disable JSONL backup (default: enabled)
export GUARDIAN_DISABLE_JSONL=1

# Backup interval in seconds (default: 60)
export GUARDIAN_FLUSH_INTERVAL=30
```

### Custom Importance Detection | 自定义重要性检测

Modify the importance detection in AGENTS.md:

```bash
# Your custom keywords
declare -A KEYWORD_IMPORTANCE=(
    ["紧急"]=10
    ["urgent"]=10
    ["密码"]=10
    ["password"]=10
    ["爱"]=9
    ["love"]=9
    ["讨厌"]=8
    ["hate"]=8
)

for keyword in "${!KEYWORD_IMPORTANCE[@]}"; do
    if [[ "$user_msg" == *"$keyword"* ]]; then
        importance=${KEYWORD_IMPORTANCE[$keyword]}
        break
    fi
done
```

---

## API Reference | API参考

### Functions | 函数

#### `record_interaction(user_msg, assistant_msg, importance, tags)`

Record a complete interaction (user + assistant).

**Parameters:**
- `user_msg`: User's message
- `assistant_msg`: Assistant's response
- `importance`: 1-10 importance level
- `tags`: Comma-separated tags

**Example:**
```bash
record_interaction "Hello" "Hi!" 5 "casual"
```

#### `mark_emotional(note, intensity, tags)`

Mark the last message with emotional significance.

**Parameters:**
- `note`: Why this is emotionally significant
- `intensity`: 1-10 emotional intensity
- `tags`: Emotional tags

**Example:**
```bash
mark_emotional "User expressed frustration about data loss" 8 "frustration,concern"
```

#### `emergency_backup()`

Create an immediate timestamped backup.

**Example:**
```bash
emergency_backup
# Returns: /path/to/.emergency_backup_20260311_191500.md
```

---

## Troubleshooting | 故障排除

### Issue: No output file created

**Check:**
```bash
# Verify script is executable
ls -la ~/.openclaw/workspace/scripts/conversation-guard.sh

# Check directory permissions
ls -la ~/.openclaw/workspace/memory/

# Manual test
source ~/.openclaw/workspace/scripts/conversation-guard.sh
echo "Test entry" >> ~/.openclaw/workspace/memory/test.txt
```

### Issue: Backup file not created

**Check:**
```bash
# Ensure .guardian directory exists
mkdir -p ~/.openclaw/workspace/memory/.guardian

# Check write permissions
touch ~/.openclaw/workspace/memory/.guardian/test
cat ~/.openclaw/workspace/memory/.guardian/test
```

### Issue: Lost data after crash

**Recovery:**
```bash
# Check JSONL backup
ls -la ~/.openclaw/workspace/memory/.guardian/.backup_*.jsonl

# Recover manually
cat ~/.openclaw/workspace/memory/.guardian/.backup_$(date +%Y-%m-%d).jsonl
```

---

## Integration Examples | 集成示例

### With Heartbeat | 结合Heartbeat

Add to `HEARTBEAT.md`:

```markdown
## Conversation Guardian Check

- [ ] Flush any pending conversation buffer
- [ ] Create hourly backup if high-importance conversations exist
- [ ] Check storage space in memory/.guardian/
```

### With Session Start | 会话启动时

Add to startup sequence:

```bash
#!/bin/bash
# At session start

source ~/.openclaw/workspace/scripts/conversation-guard.sh

# Detect session reset
if guardian_detect_reset; then
    # Recover context from backup
    guardian_recover_context
    
    # Log the recovery
    record_interaction "[System] Session reset detected" "Resuming from backup..." 10 "system,recovery"
fi
```

---

## Update | 更新

```bash
# Re-download latest version
curl -o ~/.openclaw/workspace/scripts/conversation-guard.sh \
    https://raw.githubusercontent.com/zfanmy/dreammoon-conversation-guard/main/conversation-guard.sh

chmod +x ~/.openclaw/workspace/scripts/conversation-guard.sh
```

---

## Uninstall | 卸载

```bash
# Remove script
rm ~/.openclaw/workspace/scripts/conversation-guard.sh

# Remove from AGENTS.md (manual edit)

# Optional: Keep or remove memory files
# rm -rf ~/.openclaw/workspace/memory/.guardian/
```

---

## Support | 支持

- GitHub Issues: https://github.com/zfanmy/dreammoon-conversation-guard/issues
- DreamMoon Project: https://github.com/zfanmy/DreamMoon-MemProcessor

---

## Version History | 版本历史

### v1.0.0 (2026-03-11)
- Initial release
- Basic conversation recording
- Emotional importance detection
- Dual-format backup (Markdown + JSONL)
- Emergency backup functionality

---

*Built with 🌙 by zfanmy \ 梦月儿 (DreamMoon) | 为记忆而生*
