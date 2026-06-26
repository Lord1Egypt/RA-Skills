<!-- generated-by: cc-codex-collaborate -->
<!-- generated-file: true -->
<!-- template-version: 0.1.13 -->

---
description: Disable cc-codex-collaborate stop-hook automation.
argument-hint: ""
---

Disable cc-codex-collaborate loop automation.

Execute:

```bash
.claude/skills/cc-codex-collaborate/scripts/cccc-loop-stop.sh
```

This command removes cccc hook registrations from `.claude/settings.json` without deleting unrelated user hooks. It sets `docs/cccc/config.json` `automation.stop_hook_loop_enabled` to `false` and reverts `docs/cccc/config.json` mode to `supervised-auto`.

After running it, summarize what changed in the user's primary language.
