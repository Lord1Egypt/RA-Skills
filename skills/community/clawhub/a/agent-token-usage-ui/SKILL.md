---
name: agent-token-usage-ui
description: DEPRECATED — merged into `agent-token-usage` skill (v0.2.0+). Install `agent-token-usage` instead and run `bash apply-ui.sh` for the 📊 button. This package will receive no further updates.
---

# ⚠️ DEPRECATED

This skill has been merged into the main [`agent-token-usage`](https://clawhub.com/skills/agent-token-usage) skill (v0.2.0+).

## Migration

```bash
clawhub uninstall agent-token-usage-ui
clawhub install agent-token-usage
bash ~/.openclaw/workspace/skills/agent-token-usage/apply-ui.sh
```

The 📊 button, modal, and launchd refresh job are all included in the main skill now under `apply-ui.sh` / `remove-ui.sh`.
