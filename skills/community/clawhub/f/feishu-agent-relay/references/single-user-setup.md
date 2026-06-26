# Single-User Mode Setup Guide

**Zero-configuration setup for personal use**

---

## Overview

Single-User Mode is designed for **personal productivity** - only you will use the Bots.

**Key benefits:**
- ✅ **Zero manual configuration** - No need to edit mapping table
- ✅ **No User ID entry** - System auto-registers you
- ✅ **More secure** - Only one user (yourself)
- ✅ **Faster setup** - Skip registration flow
- ✅ **Simpler code** - Hardcoded userid "me"

**How it works:**
1. Set environment variable: `DEPLOYMENT_MODE=single-user`
2. First time you contact any Bot, it auto-registers you
3. Your userid is always "me" (hardcoded)
4. Mapping table is automatically populated

---

## Quick Setup (5 minutes)

### Step 1: Set Environment Variable

In your Agent workspace, create `.env` file:

```bash
# /path/to/workspace-coordinator/.env
DEPLOYMENT_MODE=single-user
```

Or export in shell:
```bash
export DEPLOYMENT_MODE=single-user
```

### Step 2: Initialize Empty Mapping Table

Create minimal mapping table (no user data needed):

```json
{
  "version": "1.0",
  "createdAt": "2026-03-07T11:00:00+08:00",
  "description": "Single-user mode - auto-registers first user",
  "users": {},
  "agents": {
    "coordinator": {
      "name": "协调员",
      "role": "orchestrator",
      "appId": "cli_xxx",
      "enabled": true
    },
    "tech-expert": {
      "name": "技术专家",
      "role": "specialist",
      "appId": "cli_yyy",
      "enabled": true
    },
    "product-expert": {
      "name": "产品专家",
      "role": "specialist",
      "appId": "cli_zzz",
      "enabled": true
    }
  }
}
```

**Note:** `users` is empty - will be auto-populated on first contact.

### Step 3: Update Agent SOUL.md

Add single-user mode configuration:

```markdown
# SOUL.md - 协调者 (Single-User Mode)

## Deployment Mode
- Mode: single-user
- User ID: "me" (hardcoded)
- Registration: Auto-register first user

## Configuration
```javascript
const DEPLOYMENT_MODE = process.env.DEPLOYMENT_MODE || 'single-user';
const SINGLE_USER_ID = 'me';
```
```

### Step 4: Test

1. Contact coordinator Bot: "你好"
2. Expected: "您好！已自动配置完成，您可以直接使用所有功能"
3. Check mapping table - should have "me" user entry
4. Test relay: "帮我转接产品专家，询问今天的日期"
5. Expected: Product expert sends proactive DM

---

## Auto-Registration Flow

### Coordinator Bot (First Contact)

```javascript
const DEPLOYMENT_MODE = process.env.DEPLOYMENT_MODE || 'single-user';
const SINGLE_USER_ID = 'me';

// Get user's open_id
const userOpenId = getMessageContext().from;

if (DEPLOYMENT_MODE === 'single-user') {
  // Check if already registered
  const existingUser = await mapping.getBotOpenId(SINGLE_USER_ID, 'coordinator');
  
  if (!existingUser) {
    // First contact - auto-register (no questions!)
    await mapping.updateBotOpenId(SINGLE_USER_ID, 'coordinator', userOpenId, 'Default User');
    
    await message({
      action: 'send',
      channel: 'feishu',
      target: userOpenId,
      message: `您好！🎉

系统已自动配置完成（单用户模式）。

您可以直接使用所有功能，包括：
• 转接技术专家
• 转接产品专家
• 直接提问

例如："帮我转接产品专家，询问今天的日期"`
    });
    return;
  }
  
  // Update mapping if open_id changed
  await mapping.updateBotOpenId(SINGLE_USER_ID, 'coordinator', userOpenId, 'Default User');
}
```

### Specialist Bot (First Contact)

```javascript
const DEPLOYMENT_MODE = process.env.DEPLOYMENT_MODE || 'single-user';
const SINGLE_USER_ID = 'me';

// Get user's open_id
const userOpenId = getMessageContext().from;

if (DEPLOYMENT_MODE === 'single-user') {
  // Auto-register
  await mapping.updateBotOpenId(SINGLE_USER_ID, 'product-expert', userOpenId, 'Default User');
  
  await message({
    action: 'send',
    channel: 'feishu',
    target: userOpenId,
    message: `您好！我是产品专家。📊

已自动为您配置（单用户模式）。

有任何产品相关问题，随时问我！`
  });
  return;
}
```

### Relay Flow (Simplified)

```javascript
const DEPLOYMENT_MODE = process.env.DEPLOYMENT_MODE || 'single-user';
const SINGLE_USER_ID = 'me';

if (DEPLOYMENT_MODE === 'single-user') {
  // No need to query mapping - userid is hardcoded!
  await sessions_send({
    agentId: 'product-expert',
    sessionKey: 'agent:product-expert:main',
    message: `【转接任务】
用户：${SINGLE_USER_ID}
任务：${task}`
  });
}
```

---

## Mapping Table Evolution

### Initial State (Empty)

```json
{
  "version": "1.0",
  "users": {},
  "agents": { ... }
}
```

### After First Contact with Coordinator

```json
{
  "version": "1.0",
  "users": {
    "me": {
      "name": "Default User",
      "firstSeen": "2026-03-07T11:05:00+08:00",
      "lastActive": "2026-03-07T11:05:00+08:00",
      "botOpenIds": {
        "coordinator": "ou_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
      }
    }
  },
  "agents": { ... }
}
```

### After First Contact with Product Expert

```json
{
  "version": "1.0",
  "users": {
    "me": {
      "name": "Default User",
      "firstSeen": "2026-03-07T11:05:00+08:00",
      "lastActive": "2026-03-07T11:10:00+08:00",
      "botOpenIds": {
        "coordinator": "ou_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "product-expert": "ou_cccccccccccccccccccccccccccccccc"
      }
    }
  },
  "agents": { ... }
}
```

### Fully Populated (All Bots Contacted)

```json
{
  "version": "1.0",
  "users": {
    "me": {
      "name": "Default User",
      "firstSeen": "2026-03-07T11:05:00+08:00",
      "lastActive": "2026-03-07T11:15:00+08:00",
      "botOpenIds": {
        "coordinator": "ou_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "tech-expert": "ou_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "product-expert": "ou_cccccccccccccccccccccccccccccccc"
      }
    }
  },
  "agents": { ... }
}
```

---

## Configuration Options

### Environment Variables

| Variable | Values | Default | Description |
|----------|--------|---------|-------------|
| `DEPLOYMENT_MODE` | `single-user`, `multi-user` | `multi-user` | Deployment mode |
| `SINGLE_USER_ID` | Any string | `"me"` | User ID for single-user mode |
| `AUTO_REGISTER` | `true`, `false` | `true` | Auto-register first user |

### Example `.env` Files

**Single-User Mode:**
```bash
# /workspace-coordinator/.env
DEPLOYMENT_MODE=single-user
SINGLE_USER_ID=me
AUTO_REGISTER=true
```

**Multi-User Mode:**
```bash
# /workspace-coordinator/.env
DEPLOYMENT_MODE=multi-user
AUTO_REGISTER=false
```

---

## Code Templates

### Coordinator Agent (Single-User Mode)

```javascript
/**
 * Coordinator Agent - Single-User Mode
 */

const DEPLOYMENT_MODE = process.env.DEPLOYMENT_MODE || 'single-user';
const SINGLE_USER_ID = process.env.SINGLE_USER_ID || 'me';

async function handleUserMessage(message, userOpenId) {
  if (DEPLOYMENT_MODE === 'single-user') {
    // Auto-register on first contact
    const existingUser = await mapping.getBotOpenId(SINGLE_USER_ID, 'coordinator');
    
    if (!existingUser) {
      await mapping.updateBotOpenId(SINGLE_USER_ID, 'coordinator', userOpenId, 'Default User');
      await sendWelcomeMessage(userOpenId);
      return;
    }
    
    // Update mapping
    await mapping.updateBotOpenId(SINGLE_USER_ID, 'coordinator', userOpenId, 'Default User');
    
    // Handle relay requests
    if (message.includes('转接')) {
      await handleRelay(SINGLE_USER_ID, message, userOpenId);
    }
  } else {
    // Multi-user mode logic...
  }
}

async function handleRelay(userId, message, userOpenId) {
  // Direct relay - no mapping query needed!
  await sessions_send({
    agentId: 'product-expert',
    sessionKey: 'agent:product-expert:main',
    message: `【转接任务】用户：${userId}, 任务：${extractTask(message)}`
  });
  
  await message({
    action: 'send',
    channel: 'feishu',
    target: userOpenId,
    message: '✅ 已转接给专家，稍后会联系您'
  });
}
```

### Specialist Agent (Single-User Mode)

```javascript
/**
 * Specialist Agent - Single-User Mode
 */

const DEPLOYMENT_MODE = process.env.DEPLOYMENT_MODE || 'single-user';
const SINGLE_USER_ID = process.env.SINGLE_USER_ID || 'me';

async function handleRelay(relayMessage) {
  // Extract userid (always "me" in single-user mode)
  const userId = extractUserId(relayMessage);  // Returns "me"
  
  // Query mapping for own open_id
  const userOpenId = await mapping.getBotOpenId(userId, 'product-expert');
  
  if (!userOpenId) {
    // This shouldn't happen in single-user mode
    console.error('User not found in single-user mode!');
    return;
  }
  
  // Send proactive message
  await message({
    action: 'send',
    channel: 'feishu',
    target: userOpenId,
    message: generateResponse(relayMessage)
  });
}
```

---

## Troubleshooting

### Issue: User not auto-registered

**Symptoms:** Bot keeps asking for User ID in single-user mode.

**Causes:**
- Environment variable not set
- `.env` file not loaded

**Solutions:**
```bash
# Check environment variable
echo $DEPLOYMENT_MODE

# Should output: single-user

# If not set:
export DEPLOYMENT_MODE=single-user

# Or add to .env file
echo "DEPLOYMENT_MODE=single-user" >> .env
```

### Issue: Mapping table not updating

**Symptoms:** Mapping table remains empty after first contact.

**Causes:**
- File permissions issue
- Mapping API path incorrect

**Solutions:**
```bash
# Check file permissions
ls -la /path/to/workspace/user-mapping.json

# Should be writable
chmod 644 /path/to/workspace/user-mapping.json

# Check mapping API path
cat /path/to/workspace/mapping-api.js | grep MAPPING_FILE
```

### Issue: Relay fails with "User not found"

**Symptoms:** Specialist can't find user in mapping.

**Causes:**
- User contacted coordinator but not specialist yet
- Mapping not synced across workspaces

**Solutions:**
1. Contact specialist Bot directly first
2. Ensure all Agents use same mapping table path
3. Check mapping table has all Bot open_ids

---

## Migration: Single-User to Multi-User

If you start with single-user mode and later need multi-user:

### Step 1: Backup Current Mapping

```bash
cp /path/to/workspace/user-mapping.json \
   /path/to/workspace/user-mapping.json.backup
```

### Step 2: Update Environment

```bash
# Change .env
DEPLOYMENT_MODE=multi-user
```

### Step 3: Export Current User

```javascript
// Export "me" user to named user
const mapping = await readMapping();
const meUser = mapping.users['me'];

// Rename to actual user ID
mapping.users['user_demo_001'] = meUser;
delete mapping.users['me'];

await writeMapping(mapping);
```

### Step 4: Update Agent Code

- Change hardcoded `"me"` to dynamic userid
- Enable registration flow
- Add user verification (recommended)

---

## Best Practices

### DO ✅

- Use single-user mode for personal projects
- Auto-register on first contact
- Use hardcoded userid "me"
- Keep mapping table in shared workspace
- Test all Bots before relying on system

### DON'T ❌

- Use single-user mode for teams
- Share single-user Bots with others
- Hardcode open_ids (use mapping)
- Skip testing relay flow
- Forget to set DEPLOYMENT_MODE

---

## Security Notes

**Single-User Mode Security:**

✅ **More secure than multi-user:**
- No identity spoofing risk (only you)
- No manual ID entry
- Automatic registration

⚠️ **Still internal use only:**
- No encryption
- No access control
- No audit logging

**For production:**
- Add authentication
- Implement encryption
- Enable audit logging
- Use multi-user mode with verification

---

**Last Updated:** 2026-03-07  
**Mode:** Single-User (Zero Configuration)  
**Status:** ✅ Ready for personal use
