---
name: discord-admin
description: Full Discord server administration suite for OpenClaw — roles, moderation, channels, invites, webhooks, audit log, and member management.
metadata: { "openclaw": { "primaryEnv": "DISCORD_TOKEN", "requires": { "bins": ["node"], "network": true } } }
---

# Discord Admin Plugin

Full Discord server administration suite for OpenClaw. Manage roles, moderate users, configure channels, handle invites and webhooks, and query audit logs — all through a single unified tool.

## What it does

Registers a `discord_admin` tool that exposes 22 administrative actions for Discord servers. The plugin connects its own Discord.js client using your bot token and provides structured JSON responses for every operation.

## Features

- **Role Management** — Create, edit, and delete roles with color, hoist, mentionable, and permission options
- **Moderation** — Kick, ban, unban, timeout, untimeout, and warn users (warnings sent via DM embed)
- **Channel Admin** — Lock, unlock, clone, set slowmode, and make channels private with role-based access
- **Bulk Delete** — Purge up to 100 messages from a channel
- **Invites** — Create, list, and delete server invites with max age/uses/temporary options
- **Webhooks** — Create, list, and delete webhooks by channel or guild
- **Server Info** — Fetch guild metadata including member count, boost level, channel/role counts
- **Audit Log** — Query audit log entries with optional action type filter
- **Member List** — List members with optional role filter
- **Nickname Management** — Set or clear member nicknames

## Setup

1. Install the plugin and its dependencies:
   ```
   clawhub install discord-admin-plugin
   cd ~/.openclaw/skills/discord-admin-plugin && npm install
   ```

2. Configure your Discord bot token in your OpenClaw config (this is the only credential required — it is read from `channels.discord.token` and never sent anywhere except the Discord gateway):
   ```json
   {
     "channels": {
       "discord": {
         "token": "YOUR_BOT_TOKEN"
       }
     }
   }
   ```

3. Ensure your bot has the required gateway intents enabled in the Discord Developer Portal:
   - Guilds
   - Guild Members (privileged)
   - Guild Moderation
   - Guild Messages
   - Guild Invites
   - Guild Webhooks

4. Restart your gateway: `openclaw gateway restart`

## Credentials & Permissions

This plugin requires a **Discord bot token** (`channels.discord.token` in OpenClaw config). The token is used exclusively to connect to the Discord gateway — it is never transmitted to any other endpoint.

**Required bot permissions:** Manage Roles, Kick Members, Ban Members, Moderate Members, Manage Channels, Manage Messages, Create Instant Invite, Manage Webhooks, View Audit Log, Manage Nicknames.

**Required privileged intents:** Guild Members (for member listing, kicks, timeouts, nickname changes).

Use a bot token with the minimum permissions your use case needs. Avoid using a full-admin token if you only need a subset of actions.

## Actions

| Action | Description |
|--------|-------------|
| `role-create` | Create a new role |
| `role-edit` | Edit an existing role |
| `role-delete` | Delete a role |
| `kick` | Kick a member |
| `ban` | Ban a user |
| `unban` | Unban a user |
| `timeout` | Timeout a member (up to 28 days) |
| `untimeout` | Remove a timeout |
| `warn` | Send a warning DM embed |
| `bulk-delete` | Purge 2-100 messages |
| `channel-clone` | Clone a channel |
| `channel-lock` | Deny SendMessages for @everyone |
| `channel-unlock` | Reset SendMessages for @everyone |
| `channel-slowmode` | Set slowmode (0-21600s) |
| `channel-private` | Hide channel, grant to specific roles |
| `invite-create` | Create an invite |
| `invite-list` | List server invites |
| `invite-delete` | Delete an invite |
| `webhook-create` | Create a webhook |
| `webhook-list` | List webhooks |
| `webhook-delete` | Delete a webhook |
| `server-info` | Get server metadata |
| `audit-log` | Query audit log |
| `member-list` | List members |
| `nickname-set` | Set a member's nickname |
