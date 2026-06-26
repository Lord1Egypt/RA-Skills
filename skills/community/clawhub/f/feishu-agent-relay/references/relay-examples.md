# Relay Examples

Real-world examples of Agent-to-Agent relay patterns with complete code.

## Example 1: Basic Date Query Relay

### Scenario
User asks coordinator to relay a simple question to product expert.

### User Request
```
User → Coordinator Bot: "帮我转接产品专家，让他私聊我今天的日期"
```

### Coordinator Processing

```javascript
// 1. Get user's open_id from message context
const userOpenId = getMessageContext().from;  // "ou_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

// 2. Query userid from mapping
const user = await mapping.getUserByOpenId('coordinator', userOpenId);
if (!user) {
  // Handle first-time user
  await message({
    action: 'send',
    channel: 'feishu',
    target: userOpenId,
    message: '请先告诉我您的 User ID'
  });
  return;
}

// 3. Send relay to product expert (CRITICAL: use agent:xxx:main)
await sessions_send({
  agentId: 'product-expert',
  sessionKey: 'agent:product-expert:main',  // ✅ Correct!
  message: `【转接任务】
用户 User ID: ${user.userid}
问题类型：product
任务：请通过飞书 Bot 私聊用户，告诉用户今天的日期。`
});

// 4. Acknowledge to user
await message({
  action: 'send',
  channel: 'feishu',
  target: userOpenId,
  message: '✅ 已转接给产品专家，稍后专家会主动联系您'
});
```

### Product Expert Processing

```javascript
// 1. Extract userid from relay message
const userId = 'user_demo_001';  // Extracted from message

// 2. Query mapping for own open_id
const mapping = await readMapping();
const userOpenId = mapping.users[userId]?.botOpenIds?.['product-expert'];

if (!userOpenId) {
  // User hasn't contacted product expert yet
  await sessions_send({
    agentId: 'coordinator',
    sessionKey: 'agent:coordinator:main',
    message: `用户 ${userId} 尚未与我建立对话`
  });
  return;
}

// 3. Send proactive message
const today = new Date().toLocaleDateString('zh-CN', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  weekday: 'long'
});

await message({
  action: 'send',
  channel: 'feishu',
  target: userOpenId,  // ✅ Product expert's own open_id
  message: `您好！我是产品专家。📊

今天是 ${today}。

有任何产品相关问题，随时欢迎咨询！`
});
```

### Result
✅ User receives direct message from Product Expert Bot with date information.

---

## Example 2: Technical Question with Detailed Answer

### Scenario
User needs technical consultation via coordinator relay.

### User Request
```
User → Coordinator Bot: "转接技术专家，问一下我们的 API 限流策略是什么"
```

### Coordinator Processing

```javascript
const userOpenId = getMessageContext().from;
const user = await mapping.getUserByOpenId('coordinator', userOpenId);

await sessions_send({
  agentId: 'tech-expert',
  sessionKey: 'agent:tech-expert:main',
  message: `【转接任务】
用户 User ID: ${user.userid}
问题类型：technical
具体任务：API 限流策略咨询
用户原始问题：我们的 API 限流策略是什么`
});
```

### Tech Expert Processing

```javascript
const userId = extractUserId(message);
const userOpenId = await mapping.getBotOpenId(userId, 'tech-expert');

if (!userOpenId) {
  await sessions_send({
    agentId: 'coordinator',
    message: `用户 ${userId} 尚未与我建立对话`
  });
  return;
}

const response = `您好！我是技术专家。🔧

关于 API 限流策略：

**当前配置：**
• 普通用户：100 次/分钟
• VIP 用户：1000 次/分钟
• 企业用户：5000 次/分钟

**限流方式：**
• 滑动窗口计数
• 按 IP + User ID 双重限制

**超出限制：**
• 返回 HTTP 429
• Retry-After 头指示等待时间

如需调整限流配置，请联系运维团队。`;

await message({
  action: 'send',
  channel: 'feishu',
  target: userOpenId,
  message: response
});
```

### Result
✅ User receives detailed technical answer from Tech Expert Bot.

---

## Example 3: User Not Registered with Specialist

### Scenario
User has contacted coordinator but not the specialist Bot yet.

### Coordinator Processing

```javascript
const userOpenId = getMessageContext().from;
const user = await mapping.getUserByOpenId('coordinator', userOpenId);

// Check if user has product-expert open_id
const productOpenId = await mapping.getBotOpenId(user.userid, 'product-expert');

if (!productOpenId) {
  // User hasn't contacted product expert yet
  await message({
    action: 'send',
    channel: 'feishu',
    target: userOpenId,
    message: `您尚未与产品专家建立对话。

请先添加产品专家 Bot（资深产品专家），然后我会帮您转接。

或者，我可以直接将您的问题转发给产品专家，由我代为转达回复。您希望哪种方式？

1️⃣ 我先去添加产品专家 Bot
2️⃣ 请协调员代为转达`
  });
  return;
}

// User has contact info - proceed with normal relay
await sessions_send({
  agentId: 'product-expert',
  sessionKey: 'agent:product-expert:main',
  message: `【转接任务】用户 User ID: ${user.userid}...`
});
```

### User Chooses Option 2 (Coordinator Forward)

```javascript
// User: "2"

// Coordinator forwards to product expert
await sessions_send({
  agentId: 'product-expert',
  sessionKey: 'agent:product-expert:main',
  message: `【转接任务 - 转发模式】
用户 User ID: ${user.userid}
问题：用户尚未与您建立对话
任务：请提供回复内容，由协调员转发给用户
用户问题：${userQuestion}`
});

// Product expert replies via coordinator
await sessions_send({
  agentId: 'coordinator',
  sessionKey: 'agent:coordinator:main',
  message: `【回复转发】
用户 User ID: ${user.userid}
回复内容：${expertResponse}`
});

// Coordinator forwards to user
await message({
  action: 'send',
  channel: 'feishu',
  target: userOpenId,
  message: `产品专家回复：

${expertResponse}`
});
```

---

## Example 4: Multi-Step Collaboration (Tech + Product)

### Scenario
Complex task requiring input from multiple specialists.

### User Request
```
User → Coordinator Bot: "我们需要设计一个新的用户仪表盘，需要技术和产品建议"
```

### Coordinator Processing

```javascript
const userOpenId = getMessageContext().from;
const user = await mapping.getUserByOpenId('coordinator', userOpenId);

// Step 1: Relay to product expert first
await sessions_send({
  agentId: 'product-expert',
  sessionKey: 'agent:product-expert:main',
  message: `【转接任务 - 产品设计】
用户 User ID: ${user.userid}
任务：用户仪表盘产品设计咨询
请提供产品建议，然后我会转接技术专家评估可行性`
});

// Wait for product expert response...
// Product expert sends reply via sessions_send
const productAdvice = await waitForExpertResponse('product-expert');

// Step 2: Relay to tech expert with product input
await sessions_send({
  agentId: 'tech-expert',
  sessionKey: 'agent:tech-expert:main',
  message: `【转接任务 - 技术评估】
用户 User ID: ${user.userid}
任务：基于产品专家的建议，评估技术可行性

产品专家建议：
${productAdvice}

请评估技术实现方案和复杂度。`
});

// Wait for tech expert response...
const techAssessment = await waitForExpertResponse('tech-expert');

// Step 3: Combine and send to user
await message({
  action: 'send',
  channel: 'feishu',
  target: userOpenId,
  message: `关于用户仪表盘的设计建议：

📊 **产品建议**
${productAdvice}

🔧 **技术评估**
${techAssessment}

如有其他问题，随时联系我们！`
});
```

---

## Example 5: First-Time User Registration

### Scenario
New user contacts coordinator for the first time.

### User Message
```
User → Coordinator Bot: "你好"
```

### Coordinator Processing

```javascript
const userOpenId = getMessageContext().from;

// Check if user exists
const user = await mapping.getUserByOpenId('coordinator', userOpenId);

if (!user) {
  // First-time user - ask for User ID
  await message({
    action: 'send',
    channel: 'feishu',
    target: userOpenId,
    message: `您好！欢迎使用协调员服务。👋

为了提供更好的服务，请告诉我您的 User ID（工号/用户名）。

例如："我的 user ID 是：user_demo_001"`
  });
  return;
}

// Existing user - greet normally
await message({
  action: 'send',
  channel: 'feishu',
  target: userOpenId,
  message: `您好，${user.name}！有什么可以帮您？`
});
```

### User Provides User ID

```
User: "我的 user ID 是：user_demo_001"
```

### Coordinator Registration

```javascript
const userOpenId = getMessageContext().from;
const userId = 'user_demo_001';  // Extract from message

// Record mapping
await mapping.updateBotOpenId(userId, 'coordinator', userOpenId, userId);

await message({
  action: 'send',
  channel: 'feishu',
  target: userOpenId,
  message: `您好，${userId}！✅

您的信息已记录：
• User ID: ${userId}
• 飞书 Open ID: [已记录]

现在我可以帮您转接技术专家或产品专家了。有什么需要帮助的吗？`
});
```

### Mapping Table After Registration

```json
{
  "users": {
    "user_demo_001": {
      "name": "user_demo_001",
      "firstSeen": "2026-03-07T10:20:00+08:00",
      "lastActive": "2026-03-07T10:20:00+08:00",
      "botOpenIds": {
        "coordinator": "ou_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
      }
    }
  }
}
```

---

## Example 6: Error Handling - Mapping API Retry

### Scenario
Mapping table file is temporarily locked or unavailable.

### Robust Mapping Access

```javascript
const MAX_RETRIES = 3;

async function readMappingWithRetry() {
  for (let i = 0; i < MAX_RETRIES; i++) {
    try {
      const content = await fs.promises.readFile(MAPPING_FILE, 'utf-8');
      return JSON.parse(content);
    } catch (err) {
      if (i === MAX_RETRIES - 1) throw err;
      // Wait before retry (exponential backoff)
      await new Promise(r => setTimeout(r, 100 * (i + 1)));
    }
  }
}

// Usage
try {
  const mapping = await readMappingWithRetry();
  // Process mapping...
} catch (err) {
  // Handle persistent failure
  await message({
    action: 'send',
    channel: 'feishu',
    target: userOpenId,
    message: '系统暂时繁忙，请稍后再试。'
  });
}
```

---

## Key Takeaways

1. **Always query mapping first** - Check user exists before relay
2. **Use correct sessionKey** - `agent:xxx:main` not `feishu:direct:openid`
3. **Handle missing users** - First-time users need registration flow
4. **Handle missing specialist contact** - Guide user or use forward mode
5. **Provide clear feedback** - Tell user what's happening at each step
6. **Implement retry logic** - Handle file access failures gracefully
7. **Validate open_id format** - Ensure data integrity
