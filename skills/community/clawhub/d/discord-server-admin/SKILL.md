---
name: discord-server-admin
description: Manage Discord servers with a narrow, medium-risk scope using direct Bot API calls. Use when creating, renaming, moving, or deleting channels/categories; creating, editing, deleting, or reordering roles; or assigning/removing roles from members. Not for full moderation suites, bans, kicks, webhooks, guild-wide settings, or mass actions.
---

# Discord Server Admin

Use this skill for focused Discord server administration with explicit IDs and limited write scope.

## Scope

Supported operations:
- List channels and roles
- Create, edit, and delete channels/categories
- Create, edit, delete, and reorder roles
- Assign and remove roles for members

Out of scope:
- Bans, kicks, timeouts, or other moderation actions
- Webhooks, invites, automod, templates, events, or guild settings
- Bulk/mass operations
- Fuzzy matching by names when exact IDs are available

## Quick start

Use `scripts/discord-server-admin.sh`.

Examples:

```bash
export DISCORD_BOT_TOKEN="..."

# Inspect current layout
./scripts/discord-server-admin.sh channel-list <guild_id>
./scripts/discord-server-admin.sh role-list <guild_id>

# Create a category and a text channel under it
./scripts/discord-server-admin.sh channel-create <guild_id> "CLAN HQ" --type category
./scripts/discord-server-admin.sh channel-create <guild_id> clan-chat --type text --parent-id <category_id> --topic "Main clan chat"

# Create or update a role
./scripts/discord-server-admin.sh role-create <guild_id> Member --color 3498DB --permissions 0 --mentionable false --hoist false
./scripts/discord-server-admin.sh role-edit <guild_id> <role_id> --color 2ECC71

# Assign/remove a role
./scripts/discord-server-admin.sh member-role-add <guild_id> <role_id> <user_id>
./scripts/discord-server-admin.sh member-role-remove <guild_id> <role_id> <user_id>
```

## Workflow

1. Start with `channel-list` or `role-list`.
2. Confirm exact guild/channel/role/user IDs before writes.
3. Apply one targeted change at a time.
4. If Discord returns `403`, check bot permissions and role hierarchy.
5. If a role sits above the bot role, reorder roles in Discord before retrying assignments or edits.

## Safety rules

- Treat this as a medium-risk skill because it uses a bot token and can modify server structure.
- Keep the bot token in `DISCORD_BOT_TOKEN`; do not hardcode secrets into files.
- Prefer least privilege over `Administrator` when practical.
- Avoid destructive actions unless the user clearly asked for them.
- Do not add mass-delete or bulk moderation features to this skill.
- Use exact IDs for write actions to avoid touching the wrong server object.

## Limitations

- Discord role hierarchy still applies even when the bot has strong permissions.
- `role-position` only moves the role you specify; it is not a full reorder planner.
- `channel-create` supports `text`, `voice`, and `category` only.
- Permissions must be provided as Discord integer bitfields, not named permission strings.

## Resource

- `scripts/discord-server-admin.sh` — direct HTTPS helper for channels, roles, and member role assignment.
