---
name: feishu-group-thread-reply
description: |
  Force openclaw-lark bot replies into message threads in Feishu group chats, preventing main chat noise.
  Patches the plugin's dispatch layer and optionally the feishu-live-card watcher.

  Use when:
  (1) Bot replies appear in the main group chat stream instead of threads
  (2) After updating openclaw-lark plugin (patches get overwritten by npm updates)
  (3) User mentions "thread reply", "群聊 thread", "回复到话题", "thread 回复"
  (4) Checking if the thread reply patch is still applied
  (5) Setting up a new OpenClaw instance with Feishu group chats
---

# Feishu Group Thread Reply

Patch openclaw-lark to reply in threads for all group chat messages.

## Quick Apply

```bash
# 1. Patch plugin
bash scripts/patch-lark-thread.sh

# 2. Patch live-card (if installed)
python3 scripts/patch-live-card.py

# 3. Restart gateway
openclaw gateway restart
```

## Check Status

```bash
bash scripts/patch-lark-thread.sh --check-only
python3 scripts/patch-live-card.py --check-only
```

## Heartbeat Auto-Check

Add to `HEARTBEAT.md` to auto-detect and re-apply after plugin updates:

```markdown
### openclaw-lark thread patch
Run: `bash <skill-dir>/scripts/patch-lark-thread.sh --check-only`
If exit code 1, re-apply: `bash <skill-dir>/scripts/patch-lark-thread.sh` then restart gateway.

### feishu-live-card watcher
Check running: `ps aux | grep watcher.py | grep -v grep`
If not running: `cd ~/.openclaw/skills/feishu-live-card && python3 watcher.py start &`
```

## How It Works

The plugin hardcodes `replyInThread: dc.isThread` which is only true when the incoming message is already in a thread. The patch changes this to `dc.isGroup || dc.isThread` so all group replies use threads.

For detailed explanation, see `references/how-it-works.md`.

## After Plugin Updates

The openclaw-lark plugin is npm-installed. Updates overwrite patched files. Re-run:

```bash
bash scripts/patch-lark-thread.sh
openclaw gateway restart
```
