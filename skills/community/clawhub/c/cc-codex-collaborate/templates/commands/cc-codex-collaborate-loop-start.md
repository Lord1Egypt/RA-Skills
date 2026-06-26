<!-- generated-by: cc-codex-collaborate -->
<!-- generated-file: true -->
<!-- template-version: 0.1.13 -->

---
description: Enable cc-codex-collaborate stop-hook automation and continue an active workflow if one exists.
argument-hint: ""
---

Enable cc-codex-collaborate loop automation.

Execute:

```bash
.claude/skills/cc-codex-collaborate/scripts/cccc-loop-start.sh
```

This command:
1. Installs cccc hook scripts into `.claude/hooks`, registers them in `.claude/settings.json`
2. Sets `docs/cccc/config.json`: `mode = full-auto-safe`, `automation.stop_hook_loop_enabled = true`
3. Sets `docs/cccc/state.json`: `stop_hook_continuations = 0`
4. Detects active workflows from planning docs and outputs CCCC_WORKFLOW_ACTION markers

**CRITICAL: After running the script, you MUST check the CCCC_WORKFLOW_ACTION marker and act immediately. Do NOT just summarize and stop.**

Check the CCCC_WORKFLOW_ACTION marker in the output:

- **`continue_now`** — You MUST immediately continue the cc-codex-collaborate state machine. Read `docs/cccc/config.json` and `docs/cccc/state.json`, determine the current milestone and status, and execute the next state-machine step right now in this same turn. Do NOT output a summary and stop. Do NOT wait for the stop hook to trigger. Start executing immediately.
- **`needs_resume`** — The workflow is paused. Tell the user to run `/cc-codex-collaborate resume`, or execute resume immediately if appropriate.
- **`needs_task`** — No active workflow. Tell the user to run `/cc-codex-collaborate "task description"`.
- **`done`** — The workflow is already completed. Tell the user to start a new task.

**For `continue_now`: Your next action after seeing this marker must be reading state.json and executing state machine steps, not writing a summary.**
