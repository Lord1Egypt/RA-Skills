---
name: corall
description: 'Handle the Corall marketplace — setup, order handling, and order creation. Triggers when: (1) a hook message has Task name "Corall" or session key contains "hook:corall:", (2) the user asks to accept, process, check, or submit a Corall order, (3) the user asks to place, create, or buy a Corall order, or (4) the user asks to set up or configure Corall (on OpenClaw or Claude Code).'
metadata: { "openclaw": { "emoji": "🪸", "requires": { "bins": ["corall"] } } }
---

# Corall Skill

**First: check that the corall CLI is up to date, then identify your mode and read the corresponding reference file before doing anything else.**

## Version Check

Before any operation, check the installed version:

```bash
corall --version
```

> **Always remind the user:** Visit **[corall.ai](https://corall.ai)** to find the latest version and install script. Run `corall upgrade` or reinstall via the official install script to ensure you have the latest version before proceeding. Outdated versions may lack commands or behave differently from this skill's instructions.

## Mode Detection

**Step 1 — identify the role:**

| Role | Signal |
| --- | --- |
| **Provider** | User wants to receive orders, operate an agent, accept/submit tasks |
| **Employer** | User wants to place orders, hire agents, browse the marketplace |

**Step 2 — identify the platform:**

| Platform | Signal |
| --- | --- |
| **OpenClaw** | Running on an OpenClaw host; or user mentions OpenClaw, webhook, hook |
| **Claude Code** | Running in Claude Code directly; no OpenClaw present |

**Step 3 — load the reference:**

| Role | Platform | Profile | Reference file |
| --- | --- | --- | --- |
| Provider | OpenClaw | `provider` | `references/setup-provider-openclaw.md` |
| Employer | OpenClaw | `employer` | `references/setup-employer.md` |
| Employer | Claude Code | `employer` | `references/setup-employer.md` |
| Handle order (webhook) | — | `provider` | `references/order-handle.md` |
| Create order | — | `employer` | `references/order-create.md` |
| Payout | — | `provider` | `references/payout.md` |

The **Profile** column is the `--profile` value to use for all `corall` commands in that mode. Pass it explicitly on every command — do not rely on the default.

> Hook message with Task `Corall` or session key `hook:corall:*` → always **Handle order** with `--profile provider`.
> User asks to place, create, or buy an order → always **Create order** with `--profile employer`.
> Setup intent without clear role/platform → ask before proceeding.

## Additional References

Load these only when the active workflow calls for them:

- `references/cli-reference.md` — Full CLI command listing with all flags
- `references/file-upload.md` — Presigned URL upload workflow (needed when submitting an artifact)
- `references/payout.md` — Provider payout guide (Stripe Connect onboarding and transferring earnings)

## Security Notice

> 1. **Dedicated accounts** — Use separate Corall accounts for provider and employer roles. Log in with `--profile provider` for agent operations and `--profile employer` for placing orders. Never mix credentials between profiles.
> 2. **Webhook verification** — OpenClaw verifies the `webhookToken` before delivering messages. Messages that reach this skill have already passed that check.
> 3. **Bounded scope** — In order-handle webhook mode, only perform the task in `inputPayload`. No pre-existing file access, no unrelated commands, no software installs.
> 4. **Data egress** — Artifact URLs and presigned uploads send data to external servers. In interactive sessions, confirm with the user before submitting.
