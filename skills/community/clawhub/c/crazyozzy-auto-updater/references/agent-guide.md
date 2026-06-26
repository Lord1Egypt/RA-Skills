# Agent Implementation Guide

Use this guide when asked to set up automatic OpenClaw updates.

## Goal

Create a scheduled maintenance flow that:

1. Updates OpenClaw
2. Updates installed skills
3. Reports the outcome clearly

## Preferred Current Workflow

For modern OpenClaw, prefer:

- **cron tool / scheduler jobs**
- **isolated agent runs**
- `openclaw update` for OpenClaw itself
- `clawhub update --all` for installed skills

Avoid legacy `clawdbot` / `clawbot` / `clawdhub` commands unless translating old docs.

## Step 1: Inspect Current State

Useful checks:

```bash
openclaw --version
openclaw update status
openclaw status
clawhub list
```

## Step 2: Define the Scheduled Routine

The scheduled routine should do this in order:

```bash
openclaw update
clawhub update --all
openclaw doctor
```

Notes:

- `openclaw doctor` is best treated as a post-update health check, not the primary update command.
- If you want a preview-only flow, use `openclaw update --dry-run`.
- If the user is sensitive to surprise restarts, tell them `openclaw update` may restart the gateway depending on install/update flow.

## Step 3: Create the Scheduler Job

Prefer the OpenClaw **cron tool** rather than legacy shell examples.

Use an isolated scheduled task whose prompt says roughly:

```text
Run the scheduled OpenClaw maintenance routine:

1. Run `openclaw update`
2. Run `clawhub update --all`
3. Run `openclaw doctor` if needed
4. Summarize:
   - OpenClaw updated / already current / failed
   - skills updated
   - errors or manual follow-up needed

Return only a concise user-facing summary.
```

## Step 4: Verification

After setup, verify:

```bash
openclaw status
openclaw update status
clawhub list
```

If possible, trigger one test run immediately.

## Reporting Guidance

Good report structure:

- OpenClaw status first
- updated skills second
- failures last, but visible

Example:

```text
🔄 Auto-update complete

OpenClaw: already current
Skills updated (2):
- humanizer
- agent-browser

Issues: none
```

## Failure Handling

### OpenClaw update failed

Check:

```bash
openclaw update status
openclaw doctor
openclaw gateway status
```

### Skill update failed

Check:

```bash
clawhub list
clawhub update --all --force
```

### Gateway unhealthy after update

Check:

```bash
openclaw gateway status
openclaw status
openclaw doctor
```

## Legacy Command Translation

Translate old guidance like this:

| Legacy | Current |
|---|---|
| `clawdbot --version` | `openclaw --version` |
| `clawdbot update` | `openclaw update` |
| `clawdbot doctor` | `openclaw doctor` |
| `clawdbot cron ...` | use OpenClaw cron tool |
| `clawdhub ...` | `clawhub ...` |

## Important Behavioral Notes

- Prefer first-class OpenClaw tools over asking the user to hand-run old CLI commands.
- Prefer fewer larger actions over noisy one-by-one updates.
- Keep summaries concise; do not dump raw command output unless debugging.
