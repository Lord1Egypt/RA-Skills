# Discord Bot Setup Guide

## Phase 1: Discord Bot Configuration for ClawText-Ingest

This guide walks you through creating a Discord bot and granting it the minimal permissions needed for ClawText-Ingest to fetch messages from forums, channels, and threads.

---

## Step 1: Create a Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** (top right)
3. Name it: `ClawText-Ingest` (or your preference)
4. Accept Terms of Service
5. Click **Create**

---

## Step 2: Create a Bot User

1. In the left sidebar, click **Bot**
2. Click **Add Bot**
3. Under **TOKEN**, click **Copy** (keep this safe—it's like a password)
   - Store in `.env` file as: `DISCORD_TOKEN=your_token_here`

---

## Step 3: Grant Permissions

Minimal permissions for forum/channel/thread reading:

1. In the left sidebar, click **OAuth2** → **URL Generator**
2. Under **SCOPES**, select:
   - `bot`

3. Under **PERMISSIONS**, select:
   - `View Channels` (view_channel)
   - `Read Messages/View Threads` (read_message_history)

4. Copy the generated URL at the bottom

---

## Step 4: Invite Bot to Test Server

1. Paste the generated URL into your browser
2. Select your Discord server (or create a test server)
3. Click **Authorize**

**Important:** The bot can only read channels it's invited to. Grant it appropriate channel permissions.

---

## Step 5: Test the Token

```bash
# Set your token
export DISCORD_TOKEN="your_token_here"

# Run the integration test
npm run test:discord

# Or manually with Node:
node test-discord-integration.mjs
```

---

## Step 6: Configure for Production

For autonomous agent use, store the token securely:

```bash
# Option 1: Environment variable
export DISCORD_TOKEN="your_token_here"

# Option 2: .env file (add to .gitignore)
echo "DISCORD_TOKEN=your_token_here" > .env

# Option 3: OpenClaw secret vault (recommended)
# Store in your OpenClaw config secrets section
```

---

## Permissions Reference

**Required for ClawText-Ingest:**
- `view_channel` — See channels and read messages
- `read_message_history` — Fetch past messages

**Optional (not needed by default):**
- `manage_messages` — Delete messages (if you implement cleanup)
- `manage_threads` — Archive/close threads (for advanced use)

---

## Discord Intents

The ClawText-Ingest bot uses these intents:

- `Guilds` — View guild/server info
- `GuildMessages` — Read messages in channels
- `DirectMessages` — Support DM ingestion (future)
- `MessageContent` — Read message content (required since Discord.js v14)

---

## Troubleshooting

### "Invalid Token" Error
- Check that your token is correctly copied from the Developer Portal
- Never share your token or commit it to git

### "Missing Access" or "Missing Permissions" Error
- Bot must be invited to the server/channel
- Bot user role must have permission to view the channel
- Recheck step 3 (permissions) and step 4 (invitation)

### "Channel not found" Error
- Use the numeric channel ID (right-click channel → Copy Channel ID)
- Make sure the bot has `view_channel` permission on that channel

### "Forum not found" Error
- Verify it's a Discord Forum channel (not a regular channel)
- Ensure bot can access it (permissions + invitation)

---

## Next Steps

1. ✅ Token created and tested
2. → Run Phase 1 integration test (see test-discord-integration.mjs)
3. → Test with real Discord forum
4. → (Later) Create discord-ingest CLI command
5. → (Later) Agent autonomy + model selection

---

## Security Best Practices

- **Never commit tokens** to git (add `.env` to `.gitignore`)
- **Limit bot permissions** to only what's needed
- **Use read-only scopes** (we don't post/delete)
- **Rotate tokens** if compromised
- **Use separate bot for testing** vs. production

---

## Next: Integration Testing

Once your token works, run:

```bash
npm run test:discord-integration
```

This will:
1. Authenticate with Discord
2. Fetch forum structure
3. Validate message parsing
4. Test batch processing
5. Confirm ingestion compatibility

See `test-discord-integration.mjs` for details.
