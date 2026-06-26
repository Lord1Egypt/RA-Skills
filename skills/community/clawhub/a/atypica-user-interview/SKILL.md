---
name: atypica-user-interview
description: Run AI-simulated user interviews and focus group discussions using atypica.ai's library of human-like personas. Each persona is an AI that behaves like a real person — with a specific background, personality, and opinions. Use this skill whenever you need user research, product feedback, UX testing, or want to understand what different types of real people think, feel, or would do — without recruiting actual participants. Trigger on phrases like "interview users", "ask real people", "focus group", "user research", "talk to users", "get user feedback", "simulate interviews", "test with users", or any request to gather qualitative human insights.
---

# atypica User Interview & Discussion

Run one-on-one interviews or group discussions with AI personas that simulate real users. atypica.ai maintains a library of AI models trained to behave like specific types of real people — each with a name, background story, personality, and authentic opinions. You ask the research question, the AI finds fitting personas, plans the research, conducts the interviews, and produces a synthesized report.

**No recruiting. No scheduling. Results in minutes.**

## What this does

- **Interviews** — the AI conducts deep one-on-one conversations with 3–8 AI personas, each responding as a distinct real person would
- **Group discussions** — the AI runs a focus group where personas debate and react to each other
- **Report generation** — the AI synthesizes everything into a structured research report with key findings

Typical use cases:
- "How would different age groups react to this pricing model?"
- "Interview 5 potential customers about their pain points"
- "Run a focus group on this product concept"
- "What would Gen Z users think about this feature?"

## Prerequisites

**IMPORTANT**: This skill works in two modes depending on your setup.

### Option 1: MCP Server (Recommended for AI assistants)

If tools starting with `atypica_universal_` are already available in your environment, you're ready. Otherwise, configure the MCP server:

**Configuration parameters**:
- **Endpoint**: `https://atypica.ai/mcp/universal`
- **API Key**: Create a free account at https://atypica.ai, then get your key at https://atypica.ai/account/api-keys (format: `atypica_xxx`)
- **Authentication**: HTTP header `Authorization: Bearer <api_key>`

**Example: Claude Desktop** — edit the config file at:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "atypica-universal": {
      "transport": "http",
      "url": "https://atypica.ai/mcp/universal",
      "headers": {
        "Authorization": "Bearer atypica_xxx"
      }
    }
  }
}
```

Restart Claude Desktop to load. For other MCP clients, the syntax may differ.

### Option 2: Direct Bash Script (Works anywhere)

No MCP setup needed — just `curl` and `jq`:

```bash
export ATYPICA_TOKEN="atypica_xxx"
scripts/mcp-call.sh atypica_universal_create '{"content":"Interview users about coffee preferences"}'
```

See [scripts/mcp-call.sh](scripts/mcp-call.sh) for full options (`-t`, `-o`, `-f`, `-v`, `-h`).

---

## Quick Start

Here's the full flow from question to report:

```typescript
// Step 1: Start a session with your research question
const session = await callTool("atypica_universal_create", {
  content: "I want to interview 5 users about their morning coffee routine and spending habits"
});
const userChatToken = session.structuredContent.token;

// Step 2: Kick off the research
await callTool("atypica_universal_send_message", {
  userChatToken,
  message: {
    role: "user",
    lastPart: { type: "text", text: "Run one-on-one interviews" }
  }
});

// Step 3: Poll until the AI finishes (interviews take 1–5 minutes)
let result;
do {
  await wait(30000); // Wait 30 seconds between polls
  result = await callTool("atypica_universal_get_messages", {
    userChatToken,
    tail: 5
  });

  // The AI may pause to ask you to confirm its research plan
  const lastMsg = result.structuredContent.messages.at(-1);
  if (lastMsg?.role === "assistant") {
    const pending = lastMsg.parts.find(p =>
      p.state === "input-available" && p.type.startsWith("tool-")
    );
    if (pending) {
      // Handle the interaction (see "Interactions" section below)
      break;
    }
  }
} while (result.structuredContent.isRunning);

// Step 4: Retrieve the final report
const reportPart = result.structuredContent.messages
  .flatMap(m => m.parts)
  .find(p => p.type === "tool-generateReport" && p.state === "output-available");

if (reportPart?.output?.reportToken) {
  const report = await callTool("atypica_universal_get_report", {
    token: reportPart.output.reportToken
  });
  console.log(report.structuredContent.title);
  console.log(report.structuredContent.shareUrl); // Public shareable link
  console.log(report.structuredContent.content);  // Full HTML report
}
```

---

## Core Workflow

1. **Create** a session with your research question
2. **Send** a message instructing the type of research (interview vs. discussion)
3. **Poll** `get_messages` — the AI runs in the background; check `isRunning`
4. **Handle** any interactions the AI pauses for (plan confirmation, clarifying questions)
5. **Retrieve** the report once complete

---

## Understanding Personas

Personas are AI models that simulate real people. Each has:
- A name and background story (e.g., "Emma, 28, UX designer in NYC")
- Consistent personality traits, opinions, and communication style
- Domain knowledge and life experience relevant to their profile

The AI automatically selects relevant personas for your topic. You can also search the library:

```typescript
// Search for personas matching your target users
const results = await callTool("atypica_universal_search_personas", {
  query: "millennial parents concerned about screen time",
  limit: 10
});

// Get a persona's full profile
const persona = await callTool("atypica_universal_get_persona", {
  personaId: results.structuredContent.data[0].personaId
});
console.log(persona.structuredContent.prompt); // Full character description
```

---

## Research Types

### One-on-One Interviews (`interviewChat`)

The AI interviews each persona separately — deep, focused conversations that surface individual perspectives and nuance.

**Best for**: Understanding personal motivations, pain points, decision journeys, emotional reactions.

```typescript
await callTool("atypica_universal_send_message", {
  userChatToken,
  message: {
    role: "user",
    lastPart: {
      type: "text",
      text: "Conduct individual interviews with 5 personas — focus on how they make purchase decisions"
    }
  }
});
```

### Group Discussion (`discussionChat`)

3–8 personas discuss a topic together, reacting to each other's opinions. More dynamic — surfaces disagreements, consensus, and social dynamics.

**Best for**: Testing concepts, exploring group norms, understanding debates within a user segment.

```typescript
await callTool("atypica_universal_send_message", {
  userChatToken,
  message: {
    role: "user",
    lastPart: {
      type: "text",
      text: "Run a focus group with 5 participants to discuss their reactions to this product concept: [describe it]"
    }
  }
});
```

### Let the AI decide

Just describe what you want to learn — the AI will choose the right approach:

```typescript
const session = await callTool("atypica_universal_create", {
  content: "I want to understand why young professionals churn from fitness apps after 30 days"
});
```

---

## Interactions

The AI occasionally pauses to ask for your input before proceeding. Check `getMessages` for parts with `state === "input-available"`.

### Confirm Research Plan (`confirmPanelResearchPlan`)

The AI presents its plan — which personas it selected, how many interviews, what questions to focus on — and asks for your approval. You can confirm as-is or edit.

**Detect**:
```json
{
  "type": "tool-confirmPanelResearchPlan",
  "state": "input-available",
  "toolCallId": "call_xyz",
  "input": {
    "question": "Why do users churn from fitness apps?",
    "plan": "# Research Plan\n...",
    "personas": [
      { "id": 1, "name": "Alex, 26, casual gym-goer" },
      { "id": 2, "name": "Maria, 31, busy mom" }
    ]
  }
}
```

**Confirm it** (or pass `editedPlan` / `editedQuestion` to adjust):
```json
{
  "userChatToken": "...",
  "message": {
    "id": "<original messageId>",
    "role": "assistant",
    "lastPart": {
      "type": "tool-confirmPanelResearchPlan",
      "toolCallId": "call_xyz",
      "state": "output-available",
      "input": { "...copy original input..." },
      "output": {
        "confirmed": true,
        "plainText": "Confirmed — looks good, proceed"
      }
    }
  }
}
```

### Answer a Question (`requestInteraction`)

Sometimes the AI asks a clarifying question before proceeding (e.g., "Which age group should I focus on?").

**Detect**:
```json
{
  "type": "tool-requestInteraction",
  "state": "input-available",
  "toolCallId": "call_abc",
  "input": {
    "question": "Which age group should I prioritize?",
    "options": ["18-24", "25-34", "35-44"],
    "maxSelect": 1
  }
}
```

**Submit your answer**:
```json
{
  "userChatToken": "...",
  "message": {
    "id": "<original messageId>",
    "role": "assistant",
    "lastPart": {
      "type": "tool-requestInteraction",
      "toolCallId": "call_abc",
      "state": "output-available",
      "input": { "...copy original input..." },
      "output": {
        "answer": "25-34",
        "plainText": "User selected: 25-34"
      }
    }
  }
}
```

---

## Monitoring Progress

After `send_message`, the AI works in the background. Monitor via `get_messages`:

| Tool Call You'll See | What's Happening |
|----------------------|-----------------|
| `searchPersonas`, `buildPersona` | Finding the right personas |
| `confirmPanelResearchPlan` | Waiting for your plan approval |
| `interviewChat` | Interviewing a persona (runs per persona) |
| `discussionChat` | Running the group discussion |
| `reasoningThinking` | Analyzing and synthesizing findings |
| `generateReport` | Writing the final report |

```typescript
// Example: Check progress and handle all states in a loop
async function runResearch(userChatToken) {
  while (true) {
    await wait(30000);
    const { isRunning, messages } = (
      await callTool("atypica_universal_get_messages", { userChatToken, tail: 5 })
    ).structuredContent;

    if (isRunning) continue; // Still working

    const lastMsg = messages.at(-1);
    if (!lastMsg) break;

    // Check for interactions needing your input
    const pending = lastMsg.parts?.find(p =>
      p.state === "input-available" && p.type.startsWith("tool-")
    );
    if (pending) {
      await handleInteraction(userChatToken, lastMsg.messageId, pending);
      continue;
    }

    // Check if report is ready
    const reportPart = messages.flatMap(m => m.parts)
      .find(p => p.type === "tool-generateReport" && p.state === "output-available");

    if (reportPart?.output?.reportToken) {
      return reportPart.output.reportToken; // Done!
    }

    // Stopped without completing — nudge it forward
    await callTool("atypica_universal_send_message", {
      userChatToken,
      message: { role: "user", lastPart: { type: "text", text: "Please continue" } }
    });
  }
}
```

---

## Getting the Report

Once `generateReport` completes, retrieve the full report:

```typescript
const report = await callTool("atypica_universal_get_report", {
  token: reportToken
});

console.log(report.structuredContent.title);       // e.g., "Fitness App Churn: User Perspectives"
console.log(report.structuredContent.description); // 1-paragraph summary
console.log(report.structuredContent.content);     // Full HTML report
console.log(report.structuredContent.shareUrl);    // https://atypica.ai/artifacts/report/{token}/share
```

The `shareUrl` is a public link you can share directly.

---

## Error Handling

**Quota exceeded** — the `sendMessage` response will have `status: "saved_no_ai"` with `reason: "quota_exceeded"`. Top up tokens at https://atypica.ai/account/tokens.

**AI failed** — `status: "ai_failed"`. The message is saved; send another message to retry.

**Connection timeout** — if `sendMessage` times out, call `getMessages` to check `isRunning`. The AI may still be working in the background.

---

## Performance

| Operation | Typical Duration |
|-----------|-----------------|
| Persona search | < 2 seconds |
| Research plan generation | 5–15 seconds |
| Interview (per persona) | 20–40 seconds |
| Group discussion (5 personas) | 30–90 seconds |
| Report generation | 30–60 seconds |
| **Full interview study (5 people)** | **2–5 minutes** |

---

## Full API Reference

See [references/api-reference.md](references/api-reference.md) for complete input/output schemas, error codes, and additional workflow examples.
