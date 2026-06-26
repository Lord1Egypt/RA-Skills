---
name: feishu-agent-relay
description: Build multi-Agent collaboration systems on Feishu (Lark). Provides complete patterns for: (1) orchestrator-specialist Agent architecture, (2) cross-Agent user identity mapping with Feishu open_id isolation, (3) Agent-to-Agent task relay via sessions_send, (4) specialist Agents proactively messaging users. Use when building multi-Bot coordination workflows where users contact one Bot but receive responses from different specialist Bots.
---

# Feishu Agent Relay

## 🚨 Installation: Choose Your Mode First!

**⚠️ BEFORE SETUP: You must choose a deployment mode!**

| Mode | For | User ID | Setup | Security |
|------|-----|---------|-------|----------|
| **Single-User** | Personal use | Auto ("me") | ✅ 5 min | ✅ High |
| **Multi-User** | Teams | Manual entry | ⚠️ 30 min | ⚠️ Low |

### Quick Decision Guide

**Choose Single-User Mode if:**
- ✅ Only YOU will use the Bots
- ✅ Personal productivity system
- ✅ Want ZERO manual configuration
- ✅ Want fastest setup (5 minutes)

📖 **Guide:** [references/single-user-setup.md](references/single-user-setup.md)

**Choose Multi-User Mode if:**
- ✅ Multiple people will use the system
- ✅ Team or organization
- ✅ Need to track different users
- ✅ Planning to add verification later

📖 **Guide:** [references/feishu-bot-setup.md](references/feishu-bot-setup.md)

---

## ⚠️ Important Limitations

**Read this before using the skill:**

### 1. Manual User ID Registration ⚠️ SECURITY LIMITATION (Multi-User Mode Only)

**Current flow requires users to manually enter their User ID:**

```
User → Bot: "你好"
Bot → User: "请告诉我您的 User ID（工号/用户名）"
User → Bot: "我的 user ID 是：user_demo_001"  ← ⚠️ MANUAL STEP - NO VERIFICATION
```

**⚠️ Risks:**
- ❌ **No identity verification** - System trusts whatever user types
- ❌ **Identity spoofing possible** - User could claim another person's ID
- ❌ **Human error** - Users may mistype their ID
- ❌ **No audit trail** - Cannot prove who actually registered
- ❌ **NOT production-ready** - **Internal/personal use ONLY**

**✅ Acceptable for:**
- Personal projects (use Single-User Mode!)
- Small team internal tools
- Testing and prototyping

**❌ NOT acceptable for:**
- Production systems
- External-facing applications
- Security-sensitive operations

**🔧 Single-User Mode avoids this:** No manual ID entry needed!

---

### 2. Multiple Feishu Bots Required 🔧 SETUP REQUIRED

This skill requires **multiple Feishu Bot applications**:

| Bot Type | Quantity | Example Names |
|----------|----------|---------------|
| **Coordinator** | 1 | 协调员 |
| **Specialists** | 2+ | 技术专家，产品专家 |

📖 **Setup Guide:** [references/feishu-bot-setup.md](references/feishu-bot-setup.md)

---

## ⚡ Single-User Mode: Zero Configuration

**Recommended for personal use!**

```bash
# 1. Set environment variable
export DEPLOYMENT_MODE=single-user

# 2. Create empty mapping table (no users needed)
cat > user-mapping.json << 'EOF'
{
  "version": "1.0",
  "users": {},
  "agents": { ... }
}
EOF

# 3. Contact any Bot - auto-registers you!
# That's it! No manual User ID entry needed.
```

**How it works:**
- First contact: Bot auto-registers you as userid "me"
- All Bots: Automatically track your open_id
- Relay: Uses hardcoded userid "me" (no queries needed)
- Security: No identity spoofing risk (only you)

📖 **Full guide:** [references/single-user-setup.md](references/single-user-setup.md)

---

## 👥 Multi-User Mode: Manual Configuration

**For teams and organizations.**

```bash
# 1. Set environment variable
export DEPLOYMENT_MODE=multi-user

# 2. Each user must register:
User → Bot: "你好"
Bot → User: "请告诉我您的 User ID"
User → Bot: "我的 user ID 是：zhangsan"
```

**⚠️ Security Warning:** Manual User ID entry has NO verification. Internal use only!

📖 **Full guide:** [references/feishu-bot-setup.md](references/feishu-bot-setup.md)

---

## Quick Start

This skill enables **multi-Agent collaboration on Feishu** where:
- Users contact a **coordinator Bot**
- Coordinator relays tasks to **specialist Bots**
- Specialists **proactively message users**

```
User → Coordinator Bot → sessions_send → Specialist Bot → User (proactive DM)
                          (userid only)    queries mapping
```

---

## 📋 Setup Checklist

### Phase 1: Feishu Bot Configuration (~30 minutes)

- [ ] Create Feishu Developer Account
- [ ] Create Coordinator Bot + Specialist Bots
- [ ] Configure Permissions
- [ ] Configure Event Subscriptions
- [ ] Test Each Bot

📖 **Guide**: [references/feishu-bot-setup.md](references/feishu-bot-setup.md)

### Phase 2: Choose Deployment Mode

- [ ] **Single-User**: Set `DEPLOYMENT_MODE=single-user`
- [ ] **Multi-User**: Set `DEPLOYMENT_MODE=multi-user`
- [ ] Initialize mapping table
- [ ] Deploy mapping API

📖 **Single-User Guide**: [references/single-user-setup.md](references/single-user-setup.md)

### Phase 3: Testing (~15 minutes)

- [ ] Test first contact (auto-register or manual)
- [ ] Test relay flow
- [ ] Test proactive message
- [ ] Verify mapping table

---

## When to Use This Skill

**Use when:**
- ✅ Multiple Feishu Bots working together
- ✅ Users contact one Bot, receive responses from different Bots
- ✅ Cross-Bot user identity management needed
- ✅ Specialist Bots proactively message users

**Don't use for:**
- ❌ Single-Bot scenarios
- ❌ Production without verification (multi-user)
- ❌ External-facing applications

---

## Architecture

```
┌─────────────────┐
│     User        │
│  (Feishu DM)    │
└────────┬────────┘
         │ 1. User contacts coordinator
         ▼
┌─────────────────┐     2. Coordinator identifies user
│  Coordinator    │        (auto or manual)
│    Agent        │
│  (orchestrator) │     3. Relay via sessions_send
└────────┬────────┘        (userid only)
         │
         ▼
┌─────────────────┐     4. Specialist queries mapping
│   Specialist    │        for own open_id
│    Agent        │
└────────┬────────┘     5. Send proactive DM
         │
         ▼
┌─────────────────────────┐
│   user-mapping.json     │
│  userid → open_id map   │
└─────────────────────────┘
```

---

## Critical Concept: Feishu open_id Isolation

**Each Bot has different open_id for the same user:**

```
Same user (userid: user_demo_001):
├─ Coordinator Bot:    ou_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
├─ Tech Expert Bot:    ou_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
└─ Product Expert Bot: ou_cccccccccccccccccccccccccccccccc
```

**You CANNOT use one Bot's open_id for another Bot!**

### Correct Relay Pattern ✅

```javascript
// 1. Coordinator queries userid
const user = await mapping.getUserByOpenId('coordinator', userOpenId);

// 2. Send relay (userid only, NO open_id)
await sessions_send({
  agentId: 'product-expert',
  sessionKey: 'agent:product-expert:main',  // ✅ Key!
  message: `【转接任务】用户 User ID: ${user.userid}`
});

// 3. Specialist queries mapping for ITS OWN open_id
const userOpenId = mapping.users[userId]?.botOpenIds?.['product-expert'];

// 4. Send message using correct open_id
await message({
  action: 'send',
  channel: 'feishu',
  target: userOpenId,  // ✅ This Bot's open_id
  message: '您好，我是产品专家...'
});
```

---

## Workflows

### Workflow 1A: Single-User - Auto Registration

```javascript
const DEPLOYMENT_MODE = process.env.DEPLOYMENT_MODE || 'single-user';
const SINGLE_USER_ID = 'me';

const userOpenId = getMessageContext().from;

// Auto-register on first contact
const existing = await mapping.getBotOpenId(SINGLE_USER_ID, 'coordinator');

if (!existing) {
  await mapping.updateBotOpenId(SINGLE_USER_ID, 'coordinator', userOpenId, 'Default User');
  
  await message({
    message: `您好！🎉 系统已自动配置完成（单用户模式）。`
  });
  return;
}
```

### Workflow 1B: Multi-User - Manual Registration

```javascript
const userOpenId = getMessageContext().from;
const user = await mapping.getUserByOpenId('coordinator', userOpenId);

if (!user) {
  // Ask for User ID
  await message({
    message: `您好！请告诉我您的 User ID（工号/用户名）。`
  });
  return;
}

await mapping.updateBotOpenId(user.userid, 'coordinator', userOpenId, user.name);
```

### Workflow 2: Coordinator Relay

```javascript
const user = await mapping.getUserByOpenId('coordinator', userOpenId);

await sessions_send({
  agentId: 'product-expert',
  sessionKey: 'agent:product-expert:main',
  message: `【转接任务】用户 User ID: ${user.userid}, 任务：${task}`
});
```

### Workflow 3: Specialist Proactive Message

```javascript
const userId = extractUserId(message);
const userOpenId = mapping.users[userId]?.botOpenIds?.['product-expert'];

if (!userOpenId) {
  await sessions_send({
    agentId: 'coordinator',
    message: `用户 ${userId} 尚未与我建立对话`
  });
  return;
}

await message({
  action: 'send',
  channel: 'feishu',
  target: userOpenId,
  message: '您好，我是产品专家...'
});
```

---

## User Mapping Table

### Single-User Mode (Auto-populated)

```json
{
  "version": "1.0",
  "users": {
    "me": {
      "name": "Default User",
      "botOpenIds": {
        "coordinator": "ou_xxx",
        "tech-expert": "ou_yyy",
        "product-expert": "ou_zzz"
      }
    }
  },
  "agents": { ... }
}
```

### Multi-User Mode (Manual registration)

```json
{
  "version": "1.0",
  "users": {
    "zhangsan": {
      "name": "张三",
      "botOpenIds": {
        "coordinator": "ou_abc...",
        "product-expert": "ou_def..."
      }
    },
    "lisi": { ... }
  },
  "agents": { ... }
}
```

---

## Configuration

### Environment Variables

| Variable | Values | Default | Description |
|----------|--------|---------|-------------|
| `DEPLOYMENT_MODE` | `single-user`, `multi-user` | `multi-user` | Deployment mode |
| `SINGLE_USER_ID` | Any string | `"me"` | User ID for single-user |

### Agent SOUL.md Template

```markdown
# SOUL.md - 协调者

## 部署模式
- Mode: single-user (或 multi-user)
- User ID: "me" (single-user) 或 dynamic (multi-user)

## 配置
- Bot App ID: cli_xxx
- 映射表：/path/to/user-mapping.json
```

---

## Error Handling

### 400 "cross app open_id"

**Cause:** Using wrong Bot's open_id.

**Fix:** Each Bot must use its own open_id from mapping.

### User not found

**Cause:** First-time user, not registered.

**Fix:** Auto-register (single-user) or ask for ID (multi-user).

---

## Testing Checklist

- [ ] Bots created and configured
- [ ] Deployment mode set
- [ ] Mapping table initialized
- [ ] First contact works
- [ ] Relay flow works
- [ ] Proactive message works
- [ ] Mapping table updated correctly

---

## Best Practices

### DO ✅

- Use `agent:xxx:main` for sessionKey
- Pass only userid in relay
- Let specialists query own open_id
- Use mapping API (not direct file access)
- **Choose appropriate deployment mode**
- **Auto-register in single-user mode**

### DON'T ❌

- Pass open_id in relay
- Use one Bot's open_id for another
- Use `feishu:direct:openid` sessionKey
- **Use multi-user for production without verification**
- **Share single-user Bots with others**

---

## Security Considerations

### Single-User Mode ✅

- No identity spoofing risk (only you)
- No manual ID entry
- Automatic registration
- **Recommended for personal use**

### Multi-User Mode ⚠️

- Manual ID entry (no verification)
- Identity spoofing possible
- **Internal use only**
- **Add verification for production**

---

## Resources

### scripts/
- `mapping-api.js` - Unified mapping API

### references/
- **`single-user-setup.md`** - Single-user mode guide (START HERE for personal use)
- **`feishu-bot-setup.md`** - Multi-user mode guide
- `mapping-schema.md` - Schema details
- `relay-examples.md` - Code examples

---

**Version:** 1.2  
**Last Updated:** 2026-03-07  
**Deployment Modes:** Single-User (zero-config) | Multi-User (manual)  
**Recommendation:** Start with Single-User for testing, switch to Multi-User for teams  
**Status:** ✅ Functional for internal/personal use | ⚠️ Not production-ready (multi-user mode)
