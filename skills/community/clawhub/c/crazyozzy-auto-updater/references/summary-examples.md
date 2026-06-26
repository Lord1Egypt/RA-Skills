# Update Summary Examples

Reference examples for formatting update reports.

## Full Update

```text
🔄 Auto-update complete

OpenClaw: updated to a newer version

Skills updated (3):
- prd
- browser
- humanizer

Issues: none
```

## No Updates Available

```text
🔄 Auto-update check

OpenClaw: already current
Skills: all installed skills are current

Nothing to update today.
```

## Partial Update (Skills Only)

```text
🔄 Auto-update complete

OpenClaw: already current

Skills updated (2):
- himalaya
- 1password

Issues: none
```

## Update With Errors

```text
🔄 Auto-update complete (with issues)

OpenClaw: updated successfully

Skills updated (1):
- prd

Issues:
- nano-banana-pro failed to update
- Recommendation: run `clawhub update nano-banana-pro` manually
```

## First Run / Setup Confirmation

```text
🔄 Auto-updater configured

Scheduled updates are enabled.

What will be maintained:
- OpenClaw core
- installed skills via ClawHub

You’ll receive a short summary after each run.
```

## Formatting Guidelines

1. Keep the header short
2. Put OpenClaw status first
3. Group updated skills together
4. Surface failures clearly
5. Avoid walls of text and raw logs
6. Include versions when they are easy to obtain, but don’t block on them
