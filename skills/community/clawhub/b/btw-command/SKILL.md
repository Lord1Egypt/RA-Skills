---
name: "btw Command"
slug: "btw"
description: >
  Ask non-blocking clarifying questions during agent workflows. Use when agents need user input without halting execution. Handles deployment decisions, code review confirmations, data validation choices, and security checks with timeout defaults.
category: "Agent Tools"
tags: ["agent-workflow", "questions", "non-blocking", "clarification", "user-input"]
price_per_call: 0
input_schema:
  type: object
  properties:
    question:
      type: string
      description: "The question to ask the user"
    options:
      type: array
      items:
        type: string
      description: "Available answer options (optional)"
    default:
      type: string
      description: "Default answer if timeout occurs"
    timeout:
      type: number
      description: "Timeout in seconds (default: 300)"
    priority:
      type: string
      enum: ["urgent", "normal", "low"]
      description: "Question priority level"
    context:
      type: object
      description: "Additional context for the question"
  required: ["question"]
output_schema:
  type: object
  properties:
    answer:
      type: string
      description: "User's answer or default if timeout"
    answered_at:
      type: string
      description: "ISO timestamp of answer"
    timed_out:
      type: boolean
      description: "Whether the question timed out"
    response_time_ms:
      type: number
      description: "Time taken to answer in milliseconds"
---

# btw Command

**Local skill by [Claw0x](https://claw0x.com)** — runs entirely in your OpenClaw agent.

> **Runs locally.** No external API calls, no API key required. Complete privacy.

## What It Does

The btw Command skill allows AI agents to ask clarifying questions without halting their main workflow. Questions are queued, users are notified via multiple channels, and if no answer is received within the timeout period, a default answer is used automatically.

Think of it as "by the way, I need to know..." — the agent continues working while waiting for your input.

## Quick Reference

| When This Happens | Do This | What You Get |
|-------------------|---------|--------------|
| Need deployment confirmation | Ask "Deploy to staging or production?" | Non-blocking answer with default |
| Code review decision | Ask "Refactor this complex function?" | User choice without workflow halt |
| Data validation | Ask "Found duplicates, merge or keep?" | Timeout-safe decision |
| Security check | Ask "API key expiring, rotate now?" | Priority-based notification |

## 5-Minute Quickstart

### Step 1: Install (30 seconds)
```bash
openclaw skill add btw
```

### Step 2: Ask Your First Question (1 minute)
```typescript
const result = await agent.run('btw', {
  question: 'Deploy to staging or production?',
  options: ['staging', 'production'],
  default: 'staging',
  timeout: 300,
  priority: 'urgent'
});

console.log(result.answer); // 'production' or 'staging' (default)
```

### Step 3: Handle the Answer (instant)
```typescript
if (result.timed_out) {
  console.log(`Used default: ${result.answer}`);
} else {
  console.log(`User chose: ${result.answer} in ${result.response_time_ms}ms`);
}
```

## Real-World Use Cases

### Scenario 1: Deployment Automation
**Problem**: Agent needs to deploy but unsure which environment
**Solution**: Ask non-blocking question with timeout
**Example**:
```typescript
const { answer } = await btw({
  question: 'Tests passed! Deploy to which environment?',
  options: ['staging', 'production', 'skip'],
  default: 'staging',
  timeout: 600, // 10 minutes
  priority: 'urgent'
});

if (answer === 'production') {
  await deployToProduction();
} else if (answer === 'staging') {
  await deployToStaging();
}
```

### Scenario 2: Code Review Decisions
**Problem**: Agent finds complex code, unsure if refactoring is needed
**Solution**: Ask for human judgment without blocking
**Example**:
```typescript
const { answer } = await btw({
  question: 'Function `processData` has 150 lines. Refactor?',
  options: ['yes', 'no', 'later'],
  default: 'later',
  timeout: 300,
  priority: 'normal',
  context: {
    file: 'src/utils/data.ts',
    lines: 150,
    complexity: 'high'
  }
});
```

### Scenario 3: Data Validation
**Problem**: Agent finds duplicate records, needs merge strategy
**Solution**: Ask with context and smart default
**Example**:
```typescript
const { answer } = await btw({
  question: 'Found 5 duplicate users. How to handle?',
  options: ['merge', 'keep-all', 'keep-newest'],
  default: 'keep-newest',
  timeout: 180,
  priority: 'normal',
  context: {
    duplicates: 5,
    table: 'users',
    criteria: 'email'
  }
});
```

### Scenario 4: Security Checks
**Problem**: API key expiring soon, needs rotation decision
**Solution**: High-priority question with short timeout
**Example**:
```typescript
const { answer } = await btw({
  question: 'API key expires in 2 days. Rotate now?',
  options: ['yes', 'no', 'remind-tomorrow'],
  default: 'remind-tomorrow',
  timeout: 60,
  priority: 'urgent',
  context: {
    key_name: 'STRIPE_API_KEY',
    expires_at: '2026-03-29'
  }
});
```

## Integration Recipes

### OpenClaw Agent
```typescript
agent.onTask(async (task) => {
  // Ask question without blocking
  const { answer } = await agent.run('btw', {
    question: 'Approve this change?',
    options: ['yes', 'no'],
    default: 'no',
    timeout: 300
  });
  
  if (answer === 'yes') {
    await task.execute();
  }
});
```

### LangChain Agent
```python
def ask_user(question, options, default, timeout=300):
    # Use btw skill locally
    result = agent.run('btw', {
        'question': question,
        'options': options,
        'default': default,
        'timeout': timeout
    })
    return result['answer']

# Use in agent
answer = ask_user(
    'Deploy to production?',
    ['yes', 'no'],
    'no',
    timeout=600
)
```

### Custom Agent
```javascript
// Local btw implementation
async function askBtw(question, options, defaultAnswer) {
  const result = await agent.run('btw', {
    question,
    options,
    default: defaultAnswer,
    timeout: 300
  });
  
  return result.answer;
}
```

## Workflow Diagram

```
Agent Workflow
     │
     ├─ Main Task (continues)
     │
     └─ btw Question
          ├─ Queue Question
          ├─ Notify User (Web/Mobile/Slack)
          │
          ├─ User Answers → Return Answer
          │
          └─ Timeout → Return Default
```

## Why Use Via Claw0x?

- **Zero configuration**: No API keys, no setup
- **Complete privacy**: Runs entirely locally
- **Offline capable**: Works without internet
- **Unlimited usage**: No rate limits or quotas
- **Open source**: Transparent implementation
- **Agent-native**: Built for autonomous workflows

## Prerequisites

**None.** Just install and use.

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `question` | string | Yes | - | The question to ask |
| `options` | string[] | No | - | Available answer options |
| `default` | string | No | First option | Default if timeout |
| `timeout` | number | No | 300 | Timeout in seconds |
| `priority` | string | No | "normal" | Priority: urgent/normal/low |
| `context` | object | No | {} | Additional context |

## Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `answer` | string | User's answer or default |
| `answered_at` | string | ISO timestamp |
| `timed_out` | boolean | Whether timeout occurred |
| `response_time_ms` | number | Time to answer |

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 400 | Invalid input | Check question is non-empty |
| 500 | Internal error | Retry or check logs |

## Pricing

**Free.** No API key required, no usage limits.

- Runs entirely locally in your agent
- No external API calls
- Complete privacy
- Unlimited questions

## Rate Limits

**None.** Unlimited questions.

## About Claw0x

[Claw0x](https://claw0x.com) is the native skills layer for AI agents — providing unified API access, atomic billing, and quality control.

**Explore more skills**: [claw0x.com/skills](https://claw0x.com/skills)

**GitHub**: [github.com/kennyzir/btw](https://github.com/kennyzir/btw)
