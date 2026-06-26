---
name: create-telegram-agent
description: Create a new Telegram agent in OpenClaw with proper configuration. Use when user wants to create a new Telegram bot agent, including setting up agent workspace, Telegram binding, and bot token configuration. Requires user confirmation before modifying openclaw.json.
---

# Create Telegram Agent Skill

This skill helps create a new Telegram agent with complete configuration.

## Prerequisites

Before starting, ensure you have:
1. A Telegram bot token (from @BotFather)
2. The agent's purpose/description
3. The desired agent name

## Workflow

### Step 1: Collect Required Information

Ask the user for:

1. **Agent Name** (required)
   - Must be unique
   - Use lowercase letters, digits, and hyphens
   - Examples: `healthman`, `news-bot`, `task-manager`

2. **Agent Purpose** (required)
   - What will this agent do?
   - Examples: "Personal health coach", "Daily news summarizer", "Task reminder assistant"

3. **Telegram Bot Token** (required)
   - Format: `1234567890:ABCdefGHIjklMNOpqrSTUvwxyz`
   - Get from @BotFather on Telegram

   **If user doesn't have a token, provide these steps:**

   > **How to Create a Telegram Bot Token:**
   > 1. Open Telegram and search for **@BotFather**
   > 2. Start a chat with BotFather and send `/newbot`
   > 3. Follow the prompts:
   >    - Enter a **name** for your bot (display name, e.g., "CookMaster")
   >    - Enter a **username** for your bot (must end in 'bot', e.g., "cookmaster_bot")
   > 4. BotFather will send you a message containing your **HTTP API token**
   > 5. Copy the token (format: `1234567890:ABCdefGHIjklMNOpqrSTUvwxyz`)
   >
   > **Important:** Keep your token secure. Anyone with your token can control your bot.

### Step 2: Generate Agent Configuration

Based on user input, prepare the following configurations:

#### Agent Definition
```json
{
  "id": "<agent-id>",
  "name": "<Agent Name>",
  "workspace": "/Users/<user>/.openclaw/workspace-<agent-id>",
  "agentDir": "/Users/<user>/.openclaw/agents/<agent-id>/agent"
}
```

#### Telegram Binding
```json
{
  "agentId": "<agent-id>",
  "match": {
    "channel": "telegram",
    "accountId": "<bot-id>"
  }
}
```

#### Telegram Bot Account
```json
"<bot-id>": {
  "enabled": true,
  "dmPolicy": "pairing",
  "botToken": "<full-bot-token>",
  "groupPolicy": "allowlist",
  "streamMode": "partial"
}
```

### Step 3: Present Configuration for Review

**CRITICAL: DO NOT MODIFY openclaw.json DIRECTLY**

Present the following to the user in a clear format:

---

## 📋 Configuration Summary

The following changes will be made to `openclaw.json`:

### 1. Agent Definition (add to agents.list)
```json
{
  "id": "<agent-id>",
  "name": "<Agent Name>",
  "workspace": "/Users/<user>/.openclaw/workspace-<agent-id>",
  "agentDir": "/Users/<user>/.openclaw/agents/<agent-id>/agent"
}
```

### 2. Telegram Binding (add to bindings)
```json
{
  "agentId": "<agent-id>",
  "match": {
    "channel": "telegram",
    "accountId": "<bot-id>"
  }
}
```

### 3. Telegram Bot Account (add to channels.telegram.accounts)
```json
"<bot-id>": {
  "enabled": true,
  "dmPolicy": "pairing",
  "botToken": "<full-bot-token>",
  "groupPolicy": "allowlist",
  "streamMode": "partial"
}
```

---

### 4. Agent Responsibilities (suggested for AGENTS.md)

Based on the provided purpose, generate a responsibility description covering:
- Core functions of the agent
- Working methodology
- Relationship with the user

---

**Please confirm to proceed with the modifications. Any adjustments needed?**

### Step 4: Wait for User Confirmation

Only proceed after user explicitly confirms (e.g., "confirm", "proceed", "execute", "go ahead").

### Step 5: Execute Configuration

Once confirmed:

1. **Create directories:**
   ```bash
   mkdir -p /Users/<user>/.openclaw/workspace-<agent-id>
   mkdir -p /Users/<user>/.openclaw/agents/<agent-id>/agent
   ```

2. **Update openclaw.json:**
   - Add agent to `agents.list`
   - Add binding to `bindings`
   - Add bot account to `channels.telegram.accounts`

3. **Create agent files:**
   - `AGENTS.md` - Work responsibilities and workflow
   - `SOUL.md` - Agent personality and values

4. **Report completion:**
   - Show summary of what was created
   - Remind user to restart OpenClaw gateway (if applicable)
   - Provide next steps (e.g., test the bot)

## Important Rules

1. **Never modify openclaw.json without explicit user confirmation**
2. **Always show the complete configuration changes before applying**
3. **Extract bot ID from token** (the number before the colon)
4. **Create all necessary directories** before writing files
5. **Generate appropriate AGENTS.md and SOUL.md** based on the agent's purpose
