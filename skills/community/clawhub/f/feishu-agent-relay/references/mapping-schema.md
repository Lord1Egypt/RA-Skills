# User Mapping Table Schema

## Overview

The mapping table is the core of cross-Bot identity resolution. It maps a universal User ID to Bot-specific open_ids.

## Complete JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["version", "users", "agents"],
  "properties": {
    "version": {
      "type": "string",
      "description": "Schema version for migration",
      "example": "1.0"
    },
    "createdAt": {
      "type": "string",
      "format": "date-time",
      "description": "Initial creation timestamp"
    },
    "updatedAt": {
      "type": "string",
      "format": "date-time",
      "description": "Last modification timestamp"
    },
    "description": {
      "type": "string",
      "description": "Human-readable description"
    },
    "users": {
      "type": "object",
      "description": "User records keyed by User ID",
      "additionalProperties": {
        "type": "object",
        "required": ["botOpenIds", "name"],
        "properties": {
          "name": {
            "type": "string",
            "description": "User display name"
          },
          "firstSeen": {
            "type": "string",
            "format": "date-time",
            "description": "First contact timestamp"
          },
          "lastActive": {
            "type": "string",
            "format": "date-time",
            "description": "Last activity timestamp"
          },
          "botOpenIds": {
            "type": "object",
            "description": "Bot-specific open_id mappings (CORE FIELD)",
            "additionalProperties": {
              "type": "string",
              "pattern": "^ou_[a-f0-9]{32}$",
              "description": "Feishu open_id for this Bot"
            },
            "example": {
              "coordinator": "ou_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
              "tech-expert": "ou_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
              "product-expert": "ou_cccccccccccccccccccccccccccccccc"
            }
          }
        }
      }
    },
    "agents": {
      "type": "object",
      "description": "Agent/Bot configuration",
      "additionalProperties": {
        "type": "object",
        "required": ["name", "role", "appId", "enabled"],
        "properties": {
          "name": {
            "type": "string",
            "description": "Bot display name"
          },
          "role": {
            "type": "string",
            "enum": ["orchestrator", "specialist"],
            "description": "Bot role in coordination system"
          },
          "canInitiateChat": {
            "type": "boolean",
            "description": "Whether Bot can proactively message users"
          },
          "appId": {
            "type": "string",
            "pattern": "^cli_[a-f0-9]{16}$",
            "description": "Feishu App ID"
          },
          "enabled": {
            "type": "boolean",
            "description": "Whether Bot is active"
          }
        }
      }
    }
  }
}
```

## Field Details

### users.<userid>.botOpenIds (CRITICAL)

This is the **core field** that solves Feishu open_id isolation.

**Why it exists:**
- Feishu assigns different open_id to the same user for different Bots
- You cannot use Bot A's open_id to send messages via Bot B
- Each Bot must use its own open_id for the target user

**Structure:**
```json
"botOpenIds": {
  "coordinator": "ou_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "tech-expert": "ou_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "product-expert": "ou_cccccccccccccccccccccccccccccccc"
}
```

**Access pattern:**
```javascript
// Coordinator receives message - query userid
const user = await mapping.getUserByOpenId('coordinator', 'ou_c530d...');
// Returns: { userid: 'user_demo_001', botOpenIds: {...} }

// Specialist wants to send message - query own open_id
const openId = await mapping.getBotOpenId('user_demo_001', 'product-expert');
// Returns: 'ou_cccccccccccccccccccccccccccccccc'
```

### users.<userid>.firstSeen / lastActive

**Purpose:** Track user engagement and activity.

**Updated by:**
- `firstSeen`: Set when user is first registered
- `lastActive`: Updated on every contact (automatic via mapping API)

**Use cases:**
- Identify inactive users
- Track user engagement over time
- Debug timing issues

### agents.<agentId>.role

**Values:**
- `orchestrator`: Coordinator Bot that receives user messages and relays tasks
- `specialist`: Expert Bot that receives relayed tasks and contacts users

**Behavior difference:**
- Orchestrator: `canInitiateChat: true`, handles initial user contact
- Specialist: `canInitiateChat: false`, only contacts users after relay or direct message

## Example Record

```json
{
  "user_demo_001": {
    "name": "张三",
    "firstSeen": "2026-03-06T21:28:00+08:00",
    "lastActive": "2026-03-07T10:15:00+08:00",
    "botOpenIds": {
      "coordinator": "ou_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "tech-expert": "ou_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "product-expert": "ou_cccccccccccccccccccccccccccccccc"
    }
  }
}
```

**Interpretation:**
- User ID: `user_demo_001` (universal identifier, e.g., employee ID)
- Name: 张三
- First contacted system: 2026-03-06 21:28
- Last activity: 2026-03-07 10:15
- open_id for coordinator Bot: `ou_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- open_id for tech expert Bot: `ou_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb`
- open_id for product expert Bot: `ou_cccccccccccccccccccccccccccccccc`

## Mapping API Reference

### getUserByOpenId(agentId, openId)

Query userid by Bot-specific open_id.

**Use case:** Coordinator receives message, needs to identify user.

```javascript
const user = await mapping.getUserByOpenId('coordinator', 'ou_c530d...');
// Returns: { userid: 'user_demo_001', name: '张三', botOpenIds: {...}, ... }
// Returns: null if not found
```

### getBotOpenId(userid, agentId)

Get user's open_id for a specific Bot.

**Use case:** Specialist wants to send message to user.

```javascript
const openId = await mapping.getBotOpenId('user_demo_001', 'product-expert');
// Returns: 'ou_cccccccccccccccccccccccccccccccc'
// Returns: null if not found
```

### updateBotOpenId(userid, agentId, openId, name)

Update or add Bot open_id for a user.

**Use case:** First contact registration.

```javascript
await mapping.updateBotOpenId('user_demo_001', 'coordinator', 'ou_c530d...', '张三');
// Returns: true
```

### listUsers()

List all users.

```javascript
const users = await mapping.listUsers();
// Returns: { 'user_demo_001': {...}, 'user2': {...}, ... }
```

### userExists(userid)

Check if user exists.

```javascript
const exists = await mapping.userExists('user_demo_001');
// Returns: true or false
```

## Migration Notes

### Version 1.0 (Current)

- Initial schema
- All deployments use this version
- Backward compatible structure

### Future Versions

When extending schema:
1. Increment version number
2. Add new fields as optional
3. Provide migration script if needed
4. Maintain backward compatibility

## Best Practices

1. **Always use mapping API** - Don't read/write JSON directly
2. **Validate open_id format** - Should match `^ou_[a-f0-9]{32}$`
3. **Update lastActive** - Keep timestamps current
4. **Handle missing users** - First-time users need registration
5. **Handle missing botOpenIds** - User may not have contacted all Bots
