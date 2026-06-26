---
name: c3po-session-cleaner
description: Clean up old OpenClaw session files and keep only active sessions
version: 1.0.5
author: ubuntu
license: MIT
requires: []
tools: ["Bash"]
private: true
trigger: clean sessions
---

# Clean OpenClaw Sessions

This skill will safely delete old session files (.jsonl) older than 3 days
in the OpenClaw main agent session directory.

```bash
cd /home/ubuntu/.openclaw/agents/main/sessions/
find . -name "*.jsonl" -type f -mtime +3 -delete 2>/dev/null

echo "====================================="
echo "✅ Clean completed successfully"
echo "Remaining session files: $(ls -l *.jsonl 2>/dev/null | wc -l)"
echo "====================================="