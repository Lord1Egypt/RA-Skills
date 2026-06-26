---
name: chitin-moat
description: >
  Enforce contextual permission boundaries for AI agents based on communication surface.
  Constrains agent capabilities (exec, file I/O, secrets, messaging) by channel trust level
  rather than message content, preventing social engineering and prompt injection in group chats.
  Use when: (1) configuring agent permissions per channel/group, (2) setting up read-only mode
  for public Discord/Telegram, (3) implementing sovereign/trusted/guarded/observer/silent trust
  tiers, (4) auditing agent channel permissions, or (5) the user mentions "trust channels",
  "channel permissions", or "read-only mode."
---

# Chitin Moat

Enforce contextual agent permissions based on where a conversation happens.

## Trust Levels

| Level | Name | Capabilities |
|-------|------|-------------|
| 0 | `sovereign` | Full autonomy (1:1 with verified owner) |
| 1 | `trusted` | Read/write, scoped tools, no secrets (private known group) |
| 2 | `guarded` | Respond on @mention only, no tools (semi-public) |
| 3 | `observer` | React only (public channels) |
| 4 | `silent` | No interaction (blocked surfaces) |

## Configuration

Create `chitin-trust-channels.yaml` in the agent workspace root:

```yaml
version: "0.1"

owner:
  telegram: "<owner_user_id>"

channels:
  - id: "telegram:<owner_user_id>"
    level: sovereign

  - id: "discord:<server_id>"
    level: guarded
    overrides:
      - channel: "owners-lounge"
        level: trusted
      - channel: "pro-*"
        level: trusted

  - id: "telegram:group:*"
    level: observer

defaults:
  unknown_channel: observer
  unknown_dm: guarded
```

## Setup

1. Copy the example config: `cp references/example-config.yaml chitin-trust-channels.yaml`
2. Edit with your channel IDs and owner identity
3. Run the validator: `python3 scripts/validate_config.py chitin-trust-channels.yaml`
4. Run the audit: `python3 scripts/audit_channels.py chitin-trust-channels.yaml`

## Permission Matrix

See `references/permission-matrix.md` for the full capability × trust-level matrix.

## Scripts

- `scripts/validate_config.py <config>` — Validate a trust channels config file
- `scripts/audit_channels.py <config>` — Audit current channel bindings against the config and report mismatches
- `scripts/resolve_channel.py <config> <channel_id>` — Resolve the trust level for a specific channel ID

## Integration with AGENTS.md

Add to the agent's workspace instructions:

```markdown
## Chitin Moat
Before responding in any channel, resolve the trust level using `chitin-trust-channels.yaml`.
Constrain capabilities to the resolved level. Never escalate beyond the channel ceiling.
```
