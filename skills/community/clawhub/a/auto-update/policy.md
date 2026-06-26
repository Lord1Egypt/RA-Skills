# Defaults and Modes - Auto-Update

The product should feel simple on day one and configurable later.

## New Skill Defaults

### All-In

Use this when the user wants new skills to behave like the rest of the fleet.

- new skills inherit auto-update by default
- the install-time question still appears so the user can override immediately
- migration risk still pauses the update until reviewed

### All-Out

Use this when the user wants strict control.

- new skills stay manual by default
- the install-time question decides whether each skill joins the auto lane
- nothing moves into auto-update silently

## OpenClaw Modes

- `auto` - let the recurring cron run apply the approved OpenClaw update path
- `notify` - let the recurring cron inspect and report, but ask before applying
- `manual` - no automatic core updates

## Recommended Fast Path

If the user says "just set it up":
- OpenClaw: `auto` on `stable`
- new skills: `all-in`
- backups: core tailoring plus per-skill folder snapshots
- migration risk: pause and ask
- summaries: standard digest after every run
