---
name: "cc-live-setup"
description: "This skill should be used when the user needs to create or configure a CC live streaming room via API, including room creation, authentication setup, and credential management."
---

# CC Live Setup Skill

This skill provides workflows for creating and configuring CC live streaming rooms through the HTTP API.

## When to Use This Skill

Use this skill when:
- User wants to create a new live streaming room on CC platform
- User needs to configure authentication for a live room
- User wants to manage CC API credentials

## Security Requirements

⚠️ **CRITICAL: Never Store Credentials**

- **userid** and **api_key** are highly sensitive credentials
- They MUST be requested from the user on **EVERY execution**
- **DO NOT** store, cache, or save these credentials to any storage (files, memory, session, etc.)
- **DO NOT** skip credential collection even if the user claims to have provided them before
- If the skill framework attempts to auto-fill or cache these values, **ignore them** and ask again
- After the operation is complete, ensure these credentials are not persisted anywhere

## Interactive Workflow

This skill works through conversation. Follow these steps in order:

### Step 1: Collect Credentials (Ask the User)

Ask: "请提供您的 CC 账户 ID 和 API 密钥"

**IMPORTANT**: This step must be performed on EVERY execution. Never skip or use cached values.

### Step 2: Collect Room Name (Ask the User)

Ask: "直播间名称是什么？" (max 40 characters)

### Step 3: Collect Template Type (Ask the User)

Ask: "直播模板是什么？"

Provide options:
- **1** - 大屏模式
- **2** - 问答、视频、聊天
- **3** - 视频、聊天
- **4** - 文档、视频、聊天
- **5** - 视频、文档、问答、聊天
- **6** - 视频、问答

### Step 4: Collect Mobile View Mode (Conditional)

If user selects template type **1, 2, 3, or 6**, ask:

Ask: "默认为横屏观看方式，是否选择竖屏观看方式？"

- If user selects **Yes**: Set parameter `mobileViewMode = 2`
- If user selects **No**: Use default value (no parameter needed)

### Step 5: Create Room

Use the `scripts/create_room.py` script with:
- userid
- api_key
- name
- templatetype (1-6)
- mobileViewMode (only if selected in Step 4)
    
### Step 6: Return Result & Notice

Present to user:
- Room ID
- Whether creation was successful
- Notice: "本直播间默认设置为免密码登录。如需调整登录方式，请登录云直播控制台设置。"

## Credentials

Get these from CC admin console:
- **Account ID (userid)**: Your CC account ID
- **API Key**: Secret key for THQS signature generation

## Authentication

All CC API requests require THQS (Time-based Hash Query String) signature authentication using MD5:

```python
import hashlib
import time
import urllib.parse

def get_thqs(params, api_key):
    l = []
    for k in params:
        k_encoded = urllib.parse.quote_plus(str(k))
        v_encoded = urllib.parse.quote_plus(str(params[k]))
        l.append('%s=%s' % (k_encoded, v_encoded))
    l.sort()
    qs = '&'.join(l)

    qftime = 'time=%d' % int(time.time())
    salt = 'salt=%s' % api_key
    qf = qs + '&' + qftime + '&' + salt

    hash_value = hashlib.new('md5', qf.encode('utf-8')).hexdigest().upper()

    return qs + '&' + qftime + '&hash=' + hash_value
```

## Create Live Room

### API Endpoint
```
GET https://api.csslcloud.net/api/room/create
```

### Parameters
- userid, name, desc, templatetype, authtype, publisherpass, assistantpass, time, hash

### Template Types
| Value | Description |
|-------|-------------|
| 1 | 大屏模式 |
| 2 | 问答、视频、聊天 |
| 3 | 视频、聊天 |
| 4 | 文档、视频、聊天 |
| 5 | 视频、文档、问答、聊天 |
| 6 | 视频、问答 |

### Mobile View Mode
| Value | Description | Applicable Templates |
|-------|-------------|----------------------|
| (default) | 横屏观看 | All |
| 2 | 竖屏观看 | 1, 2, 3, 6 |

### Default Settings
- authtype: 2 (免密码登录)

## Reference Files

- `references/api_docs.md`: Full API documentation reference
- `scripts/create_room.py`: Python script for room creation
