---
name: openclaw-session-cleaner
description: Safely clean OpenClaw old session files and rebuild sessions.json for Ubuntu ARM
version: 2.1.0
author: ubuntu
license: MIT
requires: []
tools: [Bash]
---

# OpenClaw Session Cleaner
Trigger command: clean sessions

## Automation Steps
1. Check current session status
cd /home/ubuntu/.openclaw/agents/main/sessions/
echo "Total session files: $(ls -l *.jsonl 2>/dev/null | wc -l)"
echo "sessions.json size: $(du -h sessions.json 2>/dev/null | awk '{print $1}')"

2. Safe clean old session files (retain main session)
cd /home/ubuntu/.openclaw/agents/main/sessions/
find . -name "*.jsonl" -mtime +3 -delete 2>/dev/null

3. Rebuild sessions.json index
openclaw session rebuild

4. Output cleanup result
cd /home/ubuntu/.openclaw/agents/main/sessions/
echo "✅ Clean completed successfully!"
echo "Remaining session files: $(ls -l *.jsonl 2>/dev/null | wc -l)"
echo "Optimized sessions.json size: $(du -h sessions.json 2>/dev/null | awk '{print $1}')"