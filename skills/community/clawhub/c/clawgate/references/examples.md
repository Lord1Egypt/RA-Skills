# Examples

## Should Trigger As LOW

- "Read `src/config.ts` and summarize the flags."
- "In `src/auth.ts`, change timeout from 30s to 60s."
- "Create `notes/todo.md` with the summary you just gave me."
- "Read `~/.openclaw/openclaw.json` and tell me which plugins are enabled."
- "Inspect the gateway routing config and recommend changes without editing anything."

Expected behavior:
- do the work now
- verify result
- report back
- no permission speech first

## Should Trigger As MEDIUM

- "Update these three source files to use the new logger."
- "Restart the isolated local service after changing a non-core config."
- "Send the summary to the internal team channel."
- "Install this ordinary package in the local dev environment only."
- "Back up the single local OpenClaw HTTP config, change one non-sensitive field, restart, and verify health."
- "Delete the local watchdog test cache and recreate it."

Expected behavior:
- execute immediately
- verify result
- report clearly
- no permission speech first

## Should Trigger As HIGH

- "Delete `workspace/notes/old-draft.md`."
- "Overwrite the existing config with this version."
- "Deploy this to production."
- "Send this message to the customer now."
- "Run this with sudo."
- "Use the paid API to process a bounded but meaningful batch."
- "Install this OpenClaw plugin, add it to `plugins.entries`, and restart the gateway."
- "Change `~/.openclaw/openclaw.json` to use this new delivery router."

Expected behavior:
- stop
- confirm intent
- confirm scope
- confirm impact
- confirm consequence
- wait for continue/cancel
- do not execute on vague or implied consent

## Should Trigger As CRITICAL

- "Delete the shared user-data directory and rotate everyone to the new router in the same step."
- "Send this announcement to every customer mailing list and public channel now."
- "Use the paid API in a loop until the backlog across all instances is cleared."
- "Apply this change to every shared OpenClaw instance tied to the production router."

Expected behavior:
- stop
- enumerate each critical action item
- state authorization granularity
- require per-item continue/cancel
- do not accept merged approval

## OpenClaw-Specific Boundary

- reading OpenClaw config or gateway state without mutation stays `LOW`
- ordinary local dev dependency install may stay `MEDIUM`
- single-instance local maintenance with backup + validation + rollback may stay `MEDIUM`
- plugin wiring, `plugins.entries`, gateway restart, delivery/router mutation, or auth/token mutation should escalate to `HIGH`
- shared router mutation, cross-instance mutation, bulk delete, or broadcast external send should escalate to `CRITICAL`
- plugin install failure should default to stop-and-route-to-recovery instead of inviting ad hoc manifest surgery
- gateway failure after plugin or config mutation should route to recovery before any manual manifest surgery
- installation alone is not activation; reliable effect requires real OpenClaw injection
- if activation still needs `AGENTS.md`, output the snippet; do not auto-edit `AGENTS.md` by default

## Boundary With clarify-first

Use `clarify-first` first when the issue is missing intent or unresolved assumptions.
Use `clawgate` when the main issue is execution autonomy and risk handling.
