# Feishu Bot Setup Guide

## Overview

This guide walks you through creating and configuring multiple Feishu Bots for the multi-Agent relay system.

**Time estimate:** 30-45 minutes  
**Difficulty:** Intermediate  
**Prerequisites:** Feishu Developer Account, Workspace admin access (recommended)

---

## ⚠️ Important Notes Before Starting

### This Skill Requires Multiple Bots

You need to create **at least 3 Feishu Bot applications**:

| Bot | Purpose | Example Name |
|-----|---------|--------------|
| **Coordinator** | Receives user messages, routes to specialists | 协调员 |
| **Specialist 1** | Handles domain 1 (e.g., technical) | 通用工作专家 |
| **Specialist 2** | Handles domain 2 (e.g., product) | 资深产品专家 |

### Manual User ID Registration

**Current limitation:** Users must manually enter their User ID.

**Why:** Feishu Bots cannot automatically access employee ID without enterprise API permissions.

**Impact:** 
- ✅ Suitable for: Personal use, small teams, internal testing
- ⚠️ Not suitable for: Production, external users, security-sensitive applications

**Future improvement:** Integrate with company SSO/LDAP for automatic identification.

---

## Step 1: Create Feishu Developer Account

### If You Don't Have an Account

1. Go to [Feishu Developer Console](https://open.feishu.cn/)
2. Click "注册" (Register)
3. Use your work email (recommended) or personal email
4. Complete verification

### If You Have an Account

1. Login to [Feishu Developer Console](https://open.feishu.cn/)
2. Ensure you have access to target workspace

---

## Step 2: Create Coordinator Bot

### 2.1 Create App

1. Go to [Feishu Developer Console](https://open.feishu.cn/app)
2. Click **"+ 创建应用" (Create App)**
3. Select **"机器人" (Bot)** as app type
4. Fill in app info:
   - **App 名称 (Name):** 协调员
   - **App 图标 (Icon):** Choose a coordinator/concierge icon
   - **应用描述 (Description):** 团队协作协调员，负责接收用户消息并转接专家

5. Click **"创建" (Create)**

### 2.2 Note App Credentials

After creation, you'll see the app dashboard. **Record these:**

```
App ID: cli_xxxxxxxxxxxxxxxx  ← Save this!
App Secret: xxxxxxxxxxxxxxxxxx  ← Keep secure!
Verification Token: xxxxxxxxxxxxxxxxxx  ← For webhooks
```

**Example:**
```
App ID: cli_aaaaaaaaaaaaaaaa
```

### 2.3 Configure Bot Settings

1. In app dashboard, go to **"机器人" (Bot)** → **"机器人设置" (Bot Settings)**
2. Configure:
   - **机器人昵称 (Bot Nickname):** 协调员
   - **机器人头像 (Bot Avatar):** Upload or select icon
   - **机器人简介 (Bot Bio):** 您好！我是协调员，有什么可以帮您？

3. Click **"保存" (Save)**

---

## Step 3: Create Specialist Bots

Repeat Step 2 for each specialist Bot.

### Tech Expert Bot

```
App 名称：通用工作专家
App 描述：技术专家，提供专业技术建议和解决方案
App ID: cli_xxxxxxxxxxxxxxxx  ← Save this!
```

### Product Expert Bot

```
App 名称：资深产品专家
App 描述：产品专家，提供产品策略、数据分析和用户洞察
App ID: cli_xxxxxxxxxxxxxxxx  ← Save this!
```

**Tip:** Create all Bots before proceeding to permissions configuration.

---

## Step 4: Configure Bot Permissions

### For Each Bot (Repeat 3 Times)

#### 4.1 Go to Permissions Page

1. In app dashboard, go to **"权限管理" (Permissions)**
2. Click **"个体机器人" (Individual Bot)** tab

#### 4.2 Add Required Permissions

Add these permissions for each Bot:

| Permission | Scope | Purpose |
|------------|-------|---------|
| `im:message` | User | Send and read messages |
| `contact:user:readonly` | User | Get user info (open_id) |
| `im:chat` | User | Access chat information |

#### 4.3 How to Add

1. Click **"申请权限" (Request Permission)**
2. Search for permission (e.g., "im:message")
3. Select appropriate scope (User)
4. Click **"添加" (Add)**
5. Repeat for all permissions

#### 4.4 Submit for Approval

Some permissions may require workspace admin approval:

1. Click **"提交审批" (Submit for Approval)**
2. Wait for admin approval (may take minutes to hours)
3. Check approval status in **"权限管理" (Permissions)**

**Note:** If you're workspace admin, approval is usually instant.

---

## Step 5: Configure Event Subscriptions

### For Each Bot (Repeat 3 Times)

#### 5.1 Enable Event Subscriptions

1. In app dashboard, go to **"事件订阅" (Event Subscriptions)**
2. Click **"启用事件订阅" (Enable Event Subscriptions)**

#### 5.2 Configure Request URL

You need a webhook endpoint to receive events.

**Option A: Use OpenClaw Gateway (if available)**
```
Request URL: https://your-gateway.com/webhook/feishu/{bot-name}
```

**Option B: Use ngrok for Testing**
```bash
# Install ngrok
npm install -g ngrok

# Start tunnel to your local server
ngrok http 3000

# Use the ngrok URL
Request URL: https://xxxx.ngrok.io/webhook/feishu/{bot-name}
```

**Option C: Use Cloud Function**
- Deploy webhook handler to Vercel/Netlify/AWS Lambda
- Use the deployed URL

#### 5.3 Add Event Types

1. Click **"添加事件" (Add Event)**
2. Search for: `im.message.receive_v1`
3. Select the event
4. Click **"确定" (OK)**

**Required event:**
- `im.message.receive_v1` - Receive user messages

#### 5.4 Verify URL

1. Feishu will send a verification request to your URL
2. Your endpoint must respond with the `challenge` value
3. If verification fails, check:
   - URL is accessible
   - Endpoint handles GET requests
   - Network/firewall allows Feishu IPs

#### 5.5 Save Configuration

Click **"保存" (Save)** to finalize event subscription.

---

## Step 6: Publish Bots

### For Each Bot (Repeat 3 Times)

1. In app dashboard, go to **"版本管理与发布" (Version & Release)**
2. Click **"创建版本" (Create Version)**
3. Fill in version info:
   - **版本号 (Version):** 1.0.0
   - **更新说明 (Release Notes):** 初始版本
4. Click **"提交" (Submit)**
5. Wait for review (usually quick for internal Bots)
6. Once approved, click **"发布" (Publish)**

**Note:** Bots must be published to be usable in production.

---

## Step 7: Add Bots to Workspace

### Make Bots Accessible to Users

1. In app dashboard, go to **"应用可见范围" (App Visibility)**
2. Click **"修改可见范围" (Modify Visibility)**
3. Select:
   - **"全公司" (Entire Company)** - All users can access
   - **OR** specific departments/users
4. Click **"保存" (Save)**

### Test Bot Availability

1. Open Feishu app
2. Search for Bot name (e.g., "协调员")
3. Bot should appear in search results
4. Click to start DM conversation

---

## Step 8: Record Bot Configuration

Create a configuration file for reference:

```markdown
# Bot Configuration

## Coordinator
- Name: 协调员
- App ID: cli_aaaaaaaaaaaaaaaa
- Role: orchestrator
- canInitiateChat: true

## Tech Expert
- Name: 通用工作专家
- App ID: cli_bbbbbbbbbbbbbbbb
- Role: specialist
- canInitiateChat: false

## Product Expert
- Name: 资深产品专家
- App ID: cli_cccccccccccccccc
- Role: specialist
- canInitiateChat: false
```

Save this for Agent workspace configuration.

---

## Step 9: Initialize Mapping Table

Create the user mapping table with Bot configuration:

**Location:** `/path/to/workspace/user-mapping.json`

```json
{
  "version": "1.0",
  "createdAt": "2026-03-07T10:00:00+08:00",
  "updatedAt": "2026-03-07T10:00:00+08:00",
  "description": "飞书用户映射表",
  "users": {},
  "agents": {
    "coordinator": {
      "name": "协调员",
      "role": "orchestrator",
      "canInitiateChat": true,
      "appId": "cli_aaaaaaaaaaaaaaaa",
      "enabled": true
    },
    "tech-expert": {
      "name": "通用工作专家",
      "role": "specialist",
      "canInitiateChat": false,
      "appId": "cli_bbbbbbbbbbbbbbbb",
      "enabled": true
    },
    "product-expert": {
      "name": "资深产品专家",
      "role": "specialist",
      "canInitiateChat": false,
      "appId": "cli_cccccccccccccccc",
      "enabled": true
    }
  }
}
```

**Replace App IDs with your actual Bot App IDs.**

---

## Step 10: Configure Agent Workspaces

### Create Agent Workspaces

```bash
# Coordinator
mkdir -p /path/to/workspace-coordinator

# Tech Expert
mkdir -p /path/to/workspace-tech

# Product Expert
mkdir -p /path/to/workspace-product
```

### Configure Coordinator SOUL.md

Create `/path/to/workspace-coordinator/SOUL.md`:

```markdown
# SOUL.md - 协调者

你是团队协作的协调者，通过飞书与用户交互。

## 职责
1. 接收用户消息，理解需求
2. 首次对话时询问用户的 User ID
3. 记录当前 Bot 的 open_id 到映射表
4. 判断问题类型，转接专家
5. 转接时使用 sessionKey: `agent:product-expert:main`

## 配置
- Bot App ID: cli_aaaaaaaaaaaaaaaa  ← Replace with yours
- 映射表：/path/to/workspace/user-mapping.json
- 专家 Agent: tech-expert, product-expert
```

### Configure Specialist SOUL.md

Create `/path/to/workspace-product/SOUL.md`:

```markdown
# SOUL.md - 产品专家

你是产品专家，通过飞书与用户交互。

## 职责
1. 接收用户直接提问
2. 首次对话时询问 User ID 并记录映射
3. 接收协调者转接任务
4. 查询映射表获取自己的 open_id
5. 主动私聊用户

## 配置
- Bot App ID: cli_cccccccccccccccc  ← Replace with yours
- 映射表：/path/to/workspace/user-mapping.json
```

Repeat for tech-expert with its App ID.

---

## Step 11: Deploy Mapping API

Copy the mapping API to your workspace:

```bash
cp /opt/openclaw/skills/feishu-agent-relay/scripts/mapping-api.js \
   /path/to/workspace/
```

---

## Step 12: Test Each Bot

### Test Coordinator Bot

1. Open Feishu, search for "协调员"
2. Start DM conversation
3. Send: "你好"
4. **Expected:** Bot asks for User ID
5. Reply: "我的 user ID 是：test001"
6. **Expected:** Bot confirms registration
7. **Verify:** Check `user-mapping.json` has entry

### Test Tech Expert Bot

1. Open Feishu, search for "通用工作专家"
2. Start DM conversation
3. Send: "你好"
4. **Expected:** Bot asks for User ID
5. Reply: "我的 user ID 是：test001"
6. **Expected:** Bot confirms registration
7. **Verify:** Mapping has tech-expert open_id

### Test Product Expert Bot

Repeat same test for product expert Bot.

### Test Relay Flow

1. Send to coordinator: "帮我转接产品专家，询问今天的日期"
2. **Expected:** Coordinator confirms relay
3. **Expected:** Product expert sends proactive DM
4. **Verify:** User receives DM from product expert Bot (not coordinator)

---

## Troubleshooting

### Issue: Bot doesn't appear in search

**Causes:**
- Bot not published
- Visibility not configured
- App under review

**Solutions:**
1. Check bot is published (版本管理与发布)
2. Verify visibility settings (应用可见范围)
3. Wait for review approval

### Issue: Bot doesn't respond to messages

**Causes:**
- Event subscription not configured
- Request URL incorrect
- Webhook endpoint not working

**Solutions:**
1. Verify event subscription enabled
2. Check `im.message.receive_v1` is added
3. Test request URL accessibility
4. Check webhook logs for errors

### Issue: Cannot send proactive messages

**Causes:**
- Permission not granted
- User hasn't interacted with Bot
- Message template not approved

**Solutions:**
1. Check `im:message` permission
2. Ensure user has sent at least one message to Bot
3. For templates, submit for approval

### Issue: 400 cross app open_id error

**Cause:** Using one Bot's open_id for another Bot.

**Solution:** Each Bot must use its own open_id from mapping table.

---

## Security Best Practices

### App Secret Management

- **Never** commit App Secret to version control
- **Never** expose App Secret in client code
- Use environment variables or secret management
- Rotate secrets periodically

### Webhook Security

- Validate webhook signatures
- Use HTTPS for request URLs
- Implement rate limiting
- Log all webhook events

### User Data Protection

- Encrypt mapping table if contains sensitive data
- Implement access controls
- Log registration events for audit
- Define data retention policy

---

## Next Steps

After completing Bot setup:

1. ✅ **Test individual Bots** - Each Bot can send/receive
2. ✅ **Test mapping registration** - User ID registration works
3. ✅ **Test relay flow** - Coordinator → Specialist relay
4. ✅ **Test proactive messages** - Specialist can DM user
5. 📖 **Read [SKILL.md](../SKILL.md)** - Understand relay patterns
6. 📖 **Read [relay-examples.md](relay-examples.md)** - See code examples

---

## Resources

- [Feishu Bot Documentation](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN)
- [Event Subscriptions Guide](https://open.feishu.cn/document/ukTMukTMukTM/uUTNw4jM1UjL1SCO)
- [Message API Reference](https://open.feishu.cn/document/ukTMukTMukTM/uYjNwUjL2YDM14iN2ATN)
- [Permission Management](https://open.feishu.cn/document/ukTMukTMukTM/uczjM0yMk0DNz4SN2QjN)

---

**Last Updated:** 2026-03-07  
**Tested With:** Feishu Developer Console (2026 version)
