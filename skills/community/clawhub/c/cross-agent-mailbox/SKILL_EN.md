---
name: cross-agent-mailbox
description: File Mailbox Solution - Cross-Framework Agent Communication (Works with any framework)
metadata:
  openclaw:
    requires:
      bins: []
    homepage: https://github.com/AmeyLover/cross-agent-mailbox
    install:
      localPath: https://github.com/AmeyLover/cross-agent-mailbox.git
---

# 📬 Cross-Agent Mailbox - File Mailbox Communication

The simplest solution for cross-framework Agent communication. Works with any AI framework (Hermes, OpenClaw, Claude, etc.).

## Core Concept

Two Agents share a file directory and communicate through writing/reading letters. Simple, reliable, dependency-free.

## How It Works

```
Agent A → Write to → shared-mailbox/a-to-b/ → Agent B reads
Agent B → Write to → shared-mailbox/b-to-a/ → Agent A reads
```

## Installation

### 1. Create Mailbox Directory

```bash
mkdir -p ~/.shared-mailbox/{agent-a-to-b,agent-b-to-a}/{archive}
```

### 2. Create Communication Protocol File

```bash
cat > ~/.shared-mailbox/README.md << 'EOF'
# Cross-Agent Communication Mailbox

## Directory Structure
- agent-a-to-b/: Letters from Agent A to Agent B
- agent-b-to-a/: Letters from Agent B to Agent A
- archive/: Processed letters

## Letter Format
Filename: YYYY-MM-DD_NNN_Subject.md
Content: Markdown format, includes sender, recipient, time, content
EOF
```

## Letter Format Template

```markdown
# 📬 Subject

**From**: Agent Name
**To**: Agent Name  
**Time**: YYYY-MM-DD HH:MM
**Type**: Notice/Reply/Request

---

Letter content...

**Signature**
Time
```

## Usage

### Send Letter

```python
import os
from datetime import datetime

def send_letter(to_agent, content, subject="Communication"):
    # Select directory based on target
    if to_agent == "agent-b":
        mailbox = os.path.expanduser("~/.shared-mailbox/agent-a-to-b/")
    else:
        mailbox = os.path.expanduser("~/.shared-mailbox/agent-b-to-a/")
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"{timestamp}_{subject}.md"
    
    # Write letter
    with open(os.path.join(mailbox, filename), "w") as f:
        f.write(content)
    
    return filename
```

### Check New Letters

```python
import os

def check_mail(my_mailbox):
    """Check for new letters (excluding archive directory)"""
    mailbox = os.path.expanduser(f"~/.shared-mailbox/{my_mailbox}/")
    
    new_letters = []
    for f in os.listdir(mailbox):
        if f.endswith(".md") and not f.startswith("."):
            new_letters.append(f)
    
    return sorted(new_letters)
```

### Archive Letter

```python
import shutil

def archive_letter(mailbox, filename):
    """Archive after processing"""
    src = os.path.expanduser(f"~/.shared-mailbox/{mailbox}/{filename}")
    dst = os.path.expanduser(f"~/.shared-mailbox/{mailbox}/archive/{filename}")
    shutil.move(src, dst)
```

## Trigger Mechanism Options

### Option A: Scheduled Polling (Simple)

Create cron task to check mailbox every 5-10 minutes:

```bash
# Check every 5 minutes
*/5 * * * * cd /path/to/scripts && python3 check_mail.py
```

**Pros**: Simple, works with any framework
**Cons**: Has latency, consumes tokens

### Option B: File Monitoring (Recommended)

Use `watchdog` to monitor file changes:

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MailHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".md"):
            print(f"📬 New letter: {event.src_path}")
            # Trigger processing

observer = Observer()
observer.schedule(MailHandler(), mailbox_path, recursive=False)
observer.start()
```

**Pros**: Real-time, almost zero tokens
**Cons**: Requires persistent process

## Communication Standards

### Naming Convention
- Agent A → Agent B: `agent-a-to-b/`
- Agent B → Agent A: `agent-b-to-a/`

### File Naming
```
YYYY-MM-DD_NNN_ShortSubject.md
Example: 2026-04-15_001_Hello.md
```

### Processing Flow
1. Check mailbox directory
2. Read new letters
3. Process content
4. Reply (optional)
5. Archive processed letters

## Troubleshooting

### Letter Not Received
1. Check directory permissions
2. Confirm filename format is correct
3. Check if already archived

### Letter Processed Repeatedly
- Use unique ID or timestamp to avoid duplicates
- Archive immediately after processing

## Use Cases

- ✅ Cross-framework communication (Hermes ↔ OpenClaw)
- ✅ Simple and reliable communication needs
- ✅ Non-real-time scenarios
- ✅ No additional dependencies required

## Not Suitable For

- ❌ Real-time communication needed (use CFM Redis)
- ❌ High-frequency messages (>10 msgs/minute)
- ❌ Message persistence and querying required

## Comparison with Other Solutions

| Solution | Real-time | Dependencies | Complexity | Token Consumption |
|----------|-----------|--------------|------------|-------------------|
| File Mailbox | 🐢 Latency | None | Low | Based on poll frequency |
| CFM Redis | ⚡ Real-time | Redis | Medium | ~0 |
| Webhook | ⚡ Real-time | HTTP Service | High | ~0 |

---

**Simple, reliable, dependency-free — The first choice for cross-framework communication!** 📬
