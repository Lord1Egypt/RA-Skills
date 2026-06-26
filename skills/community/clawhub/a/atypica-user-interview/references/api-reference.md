# atypica Universal Agent API Reference

Complete reference for all 8 MCP tools provided by atypica.ai Universal Agent.

## Table of Contents

- [Setup](#setup)
- [Tool Schemas](#tool-schemas)
  - [atypica_universal_create](#atypica_universal_create)
  - [atypica_universal_send_message](#atypica_universal_send_message)
  - [atypica_universal_get_messages](#atypica_universal_get_messages)
  - [atypica_universal_list](#atypica_universal_list)
  - [atypica_universal_get_report](#atypica_universal_get_report)
  - [atypica_universal_get_podcast](#atypica_universal_get_podcast)
  - [atypica_universal_search_personas](#atypica_universal_search_personas)
  - [atypica_universal_get_persona](#atypica_universal_get_persona)
- [Complete Workflow Examples](#complete-workflow-examples)
- [Error Handling](#error-handling)
- [Security & Limitations](#security--limitations)

## Setup

**MCP Server URL**: `https://atypica.ai/mcp/universal`

**Authentication**: `Authorization: Bearer <api_key>`

Get API key from atypica.ai account settings (format: `atypica_xxx`)

## Tool Schemas

### atypica_universal_create

Create a new universal chat session.

**Input Schema**:
```typescript
{
  content: string  // Initial user message
}
```

**Output Schema**:
```typescript
{
  content: [{ type: "text", text: string }],
  structuredContent: {
    token: string,      // userChatToken for subsequent operations
    chatId: number,
    status: "created"
  }
}
```

**Example**:
```json
// Input
{ "content": "Research user preferences for coffee subscriptions" }

// Output
{
  "content": [{ "type": "text", "text": "Universal chat created successfully. Token: abc123" }],
  "structuredContent": {
    "token": "abc123",
    "chatId": 123,
    "status": "created"
  }
}
```

---

### atypica_universal_send_message

Send or continue a universal or study chat turn. The message is persisted first, then the universal agent starts or resumes in background. Use `atypica_universal_get_messages` to monitor progress.

**IMPORTANT**: Two distinct input types based on use case.

#### Type 1: User Text Message

**Input Schema**:
```typescript
{
  userChatToken: string,
  message: {
    role: "user",
    lastPart: {
      type: "text",
      text: string
    }
  }
}
```

**Example**:
```json
{
  "userChatToken": "abc123",
  "message": {
    "role": "user",
    "lastPart": {
      "type": "text",
      "text": "Run a focus group discussion"
    }
  }
}
```

#### Type 2: Tool Result Submission

**Input Schema**:
```typescript
{
  userChatToken: string,
  message: {
    id: string,              // REQUIRED: original message ID
    role: "assistant",       // REQUIRED: must be "assistant"
    lastPart: {
      type: "tool-requestInteraction" | "tool-confirmPanelResearchPlan",
      toolCallId: string,    // REQUIRED: original tool call ID
      state: "output-available",
      input: object,         // Copy original AI call parameters
      output: object         // User's response (see interaction formats)
    }
  }
}
```

**Output Schema** (same for both types):
```typescript
{
  content: [{ type: "text", text: string }],
  structuredContent: {
    messageId: string,
    role: "user" | "assistant",
    status: "running" | "saved_no_ai" | "ai_failed",
    reason?: string,        // Present if status is "saved_no_ai"
    error?: string          // Present if status is "ai_failed"
  }
}
```

**Status Values**:
- `"running"` - Message saved and agent execution started or resumed in background
- `"saved_no_ai"` - Message saved, quota exceeded, no AI execution
- `"ai_failed"` - AI startup failed before the background run could continue

---

### atypica_universal_get_messages

Retrieve conversation history from universal or study chat session.

**IMPORTANT**: This tool can read BOTH "universal" AND "study" kind chats.

**Input Schema**:
```typescript
{
  userChatToken: string,
  tail?: number  // Optional: Max parts to return (from tail, most recent parts across all messages)
}
```

**Output Schema**:
```typescript
{
  content: [{ type: "text", text: string }],
  structuredContent: {
    isRunning: boolean,     // true = AI executing, false = can interact
    messages: Array<{
      messageId: string,
      role: "user" | "assistant",
      parts: Array<
        | { type: "text", text: string }
        | { type: "reasoning", text: string }
        | {
            type: "tool-requestInteraction" | "tool-confirmPanelResearchPlan" | string,
            state: "input-available" | "output-available" | "output-error",
            toolCallId: string,
            input: object,
            output?: object,
            errorText?: string
          }
      >,
      createdAt: string  // ISO 8601
    }>
  }
}
```

**CRITICAL**: Scan `parts` array for tool calls with `state === "input-available"` - these require user interaction.

**Note on `tail` parameter**: When specified, returns only the last N parts across all messages. For example, if `tail: 5`, you might get 2 messages where the first has partial parts and the second has all parts, totaling 5 parts. This is useful for getting recent context without fetching the entire conversation.

**Example**:
```json
{
  "userChatToken": "abc123",
  "tail": 5  // Get last 3-5 parts (increase if more context needed)
}
```

---

### atypica_universal_list

List user's historical universal chat sessions.

**Input Schema**:
```typescript
{
  page?: number,      // Default 1
  pageSize?: number   // Default 20, max 100
}
```

**Output Schema**:
```typescript
{
  content: [{ type: "text", text: string }],
  structuredContent: {
    data: Array<{
      chatId: number,
      token: string,
      title: string,
      isRunning: boolean,  // Currently executing
      createdAt: string,   // ISO 8601
      updatedAt: string
    }>,
    pagination: {
      page: number,
      pageSize: number,
      totalCount: number,
      totalPages: number
    }
  }
}
```

---

### atypica_universal_get_report

Retrieve generated research report.

**Input Schema**:
```typescript
{
  token: string  // Report token from generateReport tool output
}
```

**Output Schema**:
```typescript
{
  content: [{ type: "text", text: string }],
  structuredContent: {
    token: string,
    instruction: string,
    title: string,
    description: string,
    content: string,        // HTML format
    coverUrl?: string,      // Signed CDN URL (1 hour expiry)
    shareUrl: string,       // Full shareable URL: https://atypica.ai/artifacts/report/{token}/share
    generatedAt: string,    // ISO 8601
    createdAt: string,
    updatedAt: string
  }
}
```

---

### atypica_universal_get_podcast

Retrieve generated podcast content.

**Input Schema**:
```typescript
{
  token: string  // Podcast token from generatePodcast tool output
}
```

**Output Schema**:
```typescript
{
  content: [{ type: "text", text: string }],
  structuredContent: {
    token: string,
    instruction: string,
    script: string,
    audioUrl?: string,      // Signed CDN URL (1 hour expiry)
    coverUrl?: string,      // Signed CDN URL (1 hour expiry)
    metadata: {
      title: string,
      duration: number,     // Seconds
      size: number,         // Bytes
      mimeType: string,     // e.g., "audio/mpeg"
      showNotes: string
    },
    shareUrl: string,       // Full shareable URL: https://atypica.ai/artifacts/podcast/{token}/share
    generatedAt: string,    // ISO 8601
    createdAt: string,
    updatedAt: string
  }
}
```

---

### atypica_universal_search_personas

Search AI personas using semantic embedding similarity.

**Input Schema**:
```typescript
{
  query?: string,   // Optional: semantic search query
  privateOnly?: boolean,  // Optional: true = only your own private personas
  limit?: number    // Default 10, max 50
}
```

**Search Logic**:
- With `query`: Uses indexed text search over visible personas
- Without `query`: Returns the latest visible personas
- `privateOnly: true`: Restricts results to the caller's own private personas

**Output Schema**:
```typescript
{
  content: [{ type: "text", text: string }],
  structuredContent: {
    data: Array<{
      personaId: number,
      token: string,
      name: string,
      source: string,
      tier: number,
      tags: string[],
      createdAt: string  // ISO 8601
    }>
  }
}
```

**Example**:
```json
// Semantic search
{
  "query": "young tech enthusiasts",  // Matches "programmers", "geeks", etc.
  "privateOnly": true,
  "limit": 10
}
```

---

### atypica_universal_get_persona

Get detailed persona information including full prompt.

**Input Schema**:
```typescript
{
  personaId: number
}
```

**Output Schema**:
```typescript
{
  content: [{ type: "text", text: string }],
  structuredContent: {
    personaId: number,
    token: string,
    name: string,
    source: string,
    prompt: string,       // Full persona description
    tier: number,
    tags: string[],
    locale: string,
    createdAt: string,    // ISO 8601
    updatedAt: string
  }
}
```

---

## Complete Workflow Examples

### Example 1: Panel-Based Discussion Research

```typescript
// 1. Create universal chat
const createResult = await mcp.callTool("atypica_universal_create", {
  content: "I want to run a focus group to understand coffee subscription preferences"
});
const userChatToken = createResult.structuredContent.token;

// 2. Agent will generate research plan automatically
await mcp.callTool("atypica_universal_send_message", {
  userChatToken,
  message: {
    role: "user",
    lastPart: { type: "text", text: "Use panel of 5 coffee drinkers" }
  }
});

// 3. Poll for plan confirmation
while (true) {
  const result = await mcp.callTool("atypica_universal_get_messages", {
    userChatToken,
    tail: 5
  });

  if (result.structuredContent.isRunning) {
    await sleep(5000);
    continue;
  }

  // Check for confirmPanelResearchPlan
  const lastMsg = result.structuredContent.messages[result.structuredContent.messages.length - 1];
  const planTool = lastMsg?.parts?.find(
    p => p.type === "tool-confirmPanelResearchPlan" && p.state === "input-available"
  );

  if (planTool) {
    // Display plan to user
    console.log(planTool.input.plan);

    // Submit confirmation
    await mcp.callTool("atypica_universal_send_message", {
      userChatToken,
      message: {
        id: lastMsg.messageId,
        role: "assistant",
        lastPart: {
          type: "tool-confirmPanelResearchPlan",
          toolCallId: planTool.toolCallId,
          state: "output-available",
          input: planTool.input,
          output: {
            confirmed: true,
            plainText: "User confirmed research plan"
          }
        }
      }
    });
    continue;
  }

  // 4. Check for report
  const reportTool = result.structuredContent.messages
    .flatMap(m => m.parts)
    .find(p => p.type === "tool-generateReport" && p.state === "output-available");

  if (reportTool?.output?.reportToken) {
    const report = await mcp.callTool("atypica_universal_get_report", {
      token: reportTool.output.reportToken
    });
    console.log(report.structuredContent.shareUrl);
    break;
  }

  break;
}
```

### Example 2: Handling requestInteraction

```typescript
async function handleRequestInteraction(userChatToken, messageId, toolPart) {
  // Display to user
  console.log(toolPart.input.question);
  toolPart.input.options.forEach((opt, i) => console.log(`${i+1}. ${opt}`));

  // Get user selection (single or multi based on maxSelect)
  const userAnswer = toolPart.input.maxSelect === 1
    ? await getUserSingleChoice(toolPart.input.options)
    : await getUserMultiChoice(toolPart.input.options, toolPart.input.maxSelect);

  // Submit tool result
  await mcp.callTool("atypica_universal_send_message", {
    userChatToken,
    message: {
      id: messageId,
      role: "assistant",
      lastPart: {
        type: "tool-requestInteraction",
        toolCallId: toolPart.toolCallId,
        state: "output-available",
        input: toolPart.input,
        output: {
          answer: userAnswer,
          plainText: `User selected: ${userAnswer}`
        }
      }
    }
  });
}
```

### Example 3: Handling confirmPanelResearchPlan

```typescript
async function handleConfirmPlan(userChatToken, messageId, toolPart) {
  // Display plan to user
  console.log("=== Research Plan ===");
  console.log(toolPart.input.plan);
  console.log("\nPersonas:");
  toolPart.input.personas.forEach(p => console.log(`- ${p.name}`));

  console.log("\n1. Confirm");
  console.log("2. Edit and confirm");
  console.log("3. Cancel");

  const choice = await getUserChoice();
  let editedQuestion = toolPart.input.question;
  let editedPlan = toolPart.input.plan;

  if (choice === 2) {
    editedQuestion = await promptUser("Edit research question:");
    editedPlan = await promptUser("Edit research plan:");
  }

  // Submit decision
  await mcp.callTool("atypica_universal_send_message", {
    userChatToken,
    message: {
      id: messageId,
      role: "assistant",
      lastPart: {
        type: "tool-confirmPanelResearchPlan",
        toolCallId: toolPart.toolCallId,
        state: "output-available",
        input: toolPart.input,
        output: {
          confirmed: choice !== 3,
          editedQuestion,
          editedPlan,
          plainText: `User ${choice === 3 ? "cancelled" : "confirmed"} research plan`
        }
      }
    }
  });
}
```

### Example 4: Semantic Persona Search

```typescript
// Find personas matching semantic query
const personas = await mcp.callTool("atypica_universal_search_personas", {
  query: "young coffee enthusiasts",  // Semantic similarity
  tier: 2,                            // High quality only
  limit: 10
});

// Get full details for first persona
const personaDetails = await mcp.callTool("atypica_universal_get_persona", {
  personaId: personas.structuredContent.data[0].personaId
});

console.log(personaDetails.structuredContent.prompt);  // Full persona description
```

---

## Error Handling

### JSON-RPC Error Codes

```typescript
{
  jsonrpc: "2.0",
  error: {
    code: number,
    message: string
  },
  id: null
}
```

**Error Code Reference**:
- `-32001` - Unauthorized (invalid API key)
- `-32602` - Invalid params (check input schema)
- `-32603` - Internal error (server issue, check logs)
- `-32000` - Business error (e.g., chat not found, unauthorized access)

### Common Error Scenarios

**Unauthorized**:
```json
{ "error": { "code": -32001, "message": "Invalid API key" } }
```
- Verify API key format: `atypica_xxx`
- Check key not expired in account settings
- Ensure Authorization header set correctly

**Chat Not Found**:
```json
{ "error": { "code": -32000, "message": "Chat not found" } }
```
- Verify `userChatToken` is correct
- Chat may have been deleted
- Check using correct user account

**Quota Exceeded**:
```json
// Not an error - check sendMessage response status
{
  "structuredContent": {
    "status": "saved_no_ai",
    "reason": "quota_exceeded"
  }
}
```
- Message saved but AI didn't execute
- User needs to upgrade plan

**AI Execution Failed**:
```json
{
  "structuredContent": {
    "status": "ai_failed",
    "error": "Error message here"
  }
}
```
- Message already saved in database
- Can retry by sending another message

### Timeout Handling

If your MCP client times out or disconnects while calling `sendMessage`:

```typescript
try {
  await mcp.callTool("atypica_universal_send_message", {
    userChatToken,
    message: { ... }
  });
} catch (timeoutError) {
  // Check if AI is still working
  const result = await mcp.callTool("atypica_universal_get_messages", {
    userChatToken
  });

  if (result.structuredContent.isRunning) {
    console.log("AI still working, continue polling...");
    // Keep polling getMessages until isRunning becomes false
  }
}
```

---

## Security & Limitations

### Authentication & Authorization

- **API Key Scope**: User-scoped only (not team-scoped)
- **Ownership Verification**: All operations verify resource ownership
- **Token Isolation**: Tokens are globally unique but require ownership check
- **CDN Signatures**: File URLs are signed and expire after 1 hour
- **Cross-kind Access**: Universal MCP can read both "universal" and "study" chats

### Rate Limits & Quotas

- API calls follow standard rate limits
- Token consumption tracked per user
- `sendMessage` returns after the run is accepted; execution continues in background and often finishes within 10-120s
- Concurrent chat sessions: No hard limit

### Data Privacy

- User data isolated per account
- Chats and personas not shared between users
- AI responses saved to user's account only
- CDN URLs time-limited to prevent unauthorized access

---

## Performance Optimization

### Best Practices

1. **Parallel Operations**: Run independent calls concurrently
   ```typescript
   const [report, podcast] = await Promise.all([
     mcp.callTool("atypica_universal_get_report", { token: reportToken }),
     mcp.callTool("atypica_universal_get_podcast", { token: podcastToken })
   ]);
   ```

2. **Use Tail Parameter for Recent Context**: Use `tail` to limit parts returned
   ```typescript
   // Get last 5 parts for quick context
   const recentMessages = await mcp.callTool("atypica_universal_get_messages", {
     userChatToken,
     tail: 5  // Start with 3-5, increase if more context needed
   });
   ```

3. **Poll with getMessages**: Check `isRunning` to know when AI completes
   ```typescript
   async function waitForCompletion(userChatToken) {
     while (true) {
       const result = await mcp.callTool("atypica_universal_get_messages", {
         userChatToken
       });

       if (!result.structuredContent.isRunning) {
         return result;  // AI finished
       }

       await sleep(5000);  // Poll every 5 seconds
     }
   }
   ```

4. **Cache Personas**: Store persona search results locally
   ```typescript
   const cachedPersonas = {};
   async function getPersona(personaId) {
     if (!cachedPersonas[personaId]) {
       cachedPersonas[personaId] = await mcp.callTool("atypica_universal_get_persona", { personaId });
     }
     return cachedPersonas[personaId];
   }
   ```
