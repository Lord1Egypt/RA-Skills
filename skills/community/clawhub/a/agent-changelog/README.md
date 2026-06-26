# agent-changelog

A versioning skill for OpenClaw that keeps a clear history of workspace changes with sender attribution.

Use it to answer questions like:

- Who changed this file?
- What changed between two points in time?
- Can I roll back to a known good state?

## What you get

- Automatic capture of tracked file changes between turns
- Batched git commits every 10 minutes with per-sender attribution
- Chat/CLI commands for status, log, diff, rollback, and restore
- Optional external sync after each batched commit (GitHub push or PromptLayer version)

## Quick start

Requirements: `git`, `jq`, Node.js

1. Install the skill into your OpenClaw workspace:

```bash
npx agent-changelog
```
Defaults to `~/.openclaw/workspace` (or `OPENCLAW_WORKSPACE` if set).

2. In your terminal, restart the gateway so the skill is picked up:

```bash
openclaw gateway restart
```

3. In chat, run:

```bash
/agent-changelog setup
```
![Setup command flow in chat](images/setup.gif)

4. Restart the gateway again to activate the installed hooks:

```bash
openclaw gateway restart
```

5. Verify:

```bash
/agent-changelog status
```
![Status command output example](images/status.gif)

**Optional — connect to external sync:**
After setup, the agent can walk you through linking the workspace to one external provider. GitHub handles git identity, auth (SSH or HTTPS), remote configuration, and the initial push. PromptLayer handles API key setup, collection creation or connection, and the initial snapshot sync.

_PromptLayer pulls require `unzip` (macOS/Linux) or PowerShell `Expand-Archive` (Windows)._

_Pick one external provider per workspace: GitHub or PromptLayer._

## Example usages

Check the latest commit and pending changes:
```text
/agent-changelog show me the recent changes
```

Browse specific recent history:
```text
/agent-changelog show me the last 10 changes made to the SOUL file
```

See what is pending before the next batch commit:
```text
/agent-changelog what are the uncommitted changes?
```

## Configuration

After setup, `.agent-changelog.json` is created (if missing) and defaults to tracking the entire workspace:

```json
{
  "tracked": [
    "."
  ]
}
```

Edit this file to narrow or expand what gets tracked.

External sync settings (provider choice and PromptLayer collection info) are stored in your OpenClaw config at `~/.openclaw/openclaw.json` (or `OPENCLAW_CONFIG`). The PromptLayer API key is stored in that OpenClaw config (outside the workspace).

## A note on secrets

By default, agent-changelog tracks your entire workspace. Setup creates a `.gitignore` that excludes common secret patterns — `.env` files, API keys, tokens, credentials, cloud config directories, and more.

A few things to be careful about:

- **If your workspace already has a `.gitignore`**, setup leaves it untouched. Make sure it excludes anything sensitive before enabling tracking.
- **If you're pushing to a remote**, audit your workspace for hardcoded secrets in tracked files (SOUL.md, AGENTS.md, etc.) before the first push.
- **Narrow your tracking** if you're unsure. Edit `.agent-changelog.json` to list only the specific files you want versioned instead of `.`.

## In one minute: how it behaves

- On `message:received`, sender details are captured.
- On `message:sent`, tracked file changes are staged and queued with attribution.
- Every 10 minutes, queued entries are committed together with grouped attribution.

This gives you low-noise, attributable history without manual git bookkeeping every turn.

## FAQ

**Does this work without OpenClaw?**
No. The hooks rely on OpenClaw's event system (`message:received` / `message:sent`), and setup uses the `openclaw` CLI to register crons and enable hooks. It's built specifically for OpenClaw and won't run on another platform without significant rework.

**Which external systems can I connect?**
GitHub or PromptLayer. Pick one per workspace. Auto-sync works with either provider: GitHub pushes to your remote when configured, and PromptLayer publishes a version after each batch commit. Provider configuration details are stored in your OpenClaw config (not in the workspace).

**How does push/pull work with PromptLayer?**
Push always creates a new version in PromptLayer; existing versions are never modified or deleted, so you can always pull an older one back. Pull is diff-based: only files that differ from the pulled version are updated locally. Any local files that don't exist in the PromptLayer version are left untouched, so nothing is deleted from your workspace during a pull.

**How do you handle secrets and sensitive data?**
PromptLayer API keys are stored only in your local OpenClaw config and are never written to `.agent-changelog.json` or tracked files. Setup creates a `.gitignore` with common secret patterns, but you should still review your workspace and tracked files before syncing to any external system.

## Workspace files

| File                        | Purpose                                                                       |
| --------------------------- | ----------------------------------------------------------------------------- |
| `.agent-changelog.json` | Your tracked-files configuration                                              |
| `.version-context`          | Temporary sender handoff between hooks (not committed)                        |
| `pending_commits.jsonl`     | Pending attribution entries waiting for the next batch commit (not committed) |
