---
name: ainative-chat-completions
description: Help agents build conversational AI with AINative's Chat Completions API. Use when (1) Building a chatbot or AI assistant, (2) Implementing streaming responses, (3) Using function/tool calling, (4) Tracking credit usage per request, (5) Choosing between streaming and non-streaming. Covers raw API, Python SDK, React SDK, and Next.js patterns. Closes #1522.
---

# AINative Chat Completions

## Endpoint

```
POST https://api.ainative.studio/v1/public/chat/completions
```

**Auth:** `X-API-Key: ak_...` or `Authorization: Bearer <jwt>`

## Basic Request

```python
import requests

response = requests.post(
    "https://api.ainative.studio/v1/public/chat/completions",
    headers={"X-API-Key": "ak_your_key"},
    json={
        "model": "claude-3-5-sonnet-20241022",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is ZeroDB?"}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }
)
data = response.json()
print(data["choices"][0]["message"]["content"])
print(f"Tokens used: {data['usage']['total_tokens']}")
```

## Streaming (SSE)

```python
import requests

with requests.post(
    "https://api.ainative.studio/v1/public/chat/completions",
    headers={"X-API-Key": "ak_your_key"},
    json={"model": "claude-3-5-sonnet-20241022",
          "messages": [{"role": "user", "content": "Count to 5"}],
          "stream": True},
    stream=True
) as resp:
    for line in resp.iter_lines():
        if line and line.startswith(b"data: "):
            chunk = line[6:]
            if chunk != b"[DONE]":
                import json
                delta = json.loads(chunk)["choices"][0]["delta"]
                print(delta.get("content", ""), end="", flush=True)
```

## React SDK — `useChat` Hook

```bash
npm install @ainative/react-sdk
```

```tsx
import { AINativeProvider, useChat } from '@ainative/react-sdk';

function App() {
  return (
    <AINativeProvider config={{ apiKey: 'ak_your_key' }}>
      <ChatComponent />
    </AINativeProvider>
  );
}

function ChatComponent() {
  const { messages, sendMessage, isLoading, error } = useChat({
    model: 'claude-3-5-sonnet-20241022',
    systemPrompt: 'You are a helpful assistant.',
  });

  const handleSend = () => sendMessage('Hello!');

  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i}><b>{msg.role}:</b> {msg.content}</div>
      ))}
      <button onClick={handleSend} disabled={isLoading}>
        {isLoading ? 'Thinking...' : 'Send'}
      </button>
      {error && <p>Error: {error.message}</p>}
    </div>
  );
}
```

## Next.js — Server Action + Streaming

```bash
npm install @ainative/next-sdk
```

```typescript
// app/api/chat/route.ts
import { createServerClient } from '@ainative/next-sdk/server';

export async function POST(request: Request) {
  const { messages } = await request.json();
  const client = createServerClient({ apiKey: process.env.AINATIVE_API_KEY! });

  const stream = await client.chat.completions.create({
    model: 'claude-3-5-sonnet-20241022',
    messages,
    stream: true,
  });

  return new Response(stream.body, {
    headers: { 'Content-Type': 'text/event-stream' }
  });
}
```

## Available Models

| Model | Context | Best For |
|-------|---------|----------|
| `claude-3-5-sonnet-20241022` | 200k | General purpose (default) |
| `claude-3-5-haiku-20241022` | 200k | Fast, low cost |
| `claude-3-opus-20240229` | 200k | Complex reasoning |
| `gpt-4o` | 128k | OpenAI fallback |

## Request Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | required | Model ID |
| `messages` | array | required | Conversation history |
| `stream` | boolean | false | Enable SSE streaming |
| `temperature` | float | 0.7 | Randomness (0-1) |
| `max_tokens` | int | 1024 | Max response length |
| `system` | string | — | System prompt (alternative) |

## Credit Costs

Credits are consumed per token. Check balance before high-volume usage:

```python
balance = requests.get(
    "https://api.ainative.studio/api/v1/public/credits/balance",
    headers={"X-API-Key": "ak_your_key"}
).json()
print(f"Remaining: {balance['remaining_credits']}")
```

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid API key | Check key format: `ak_...` |
| 402 | Insufficient credits | Top up or upgrade plan |
| 429 | Rate limit | Back off, retry with exponential delay |
| 503 | Model unavailable | Retry or use fallback model |

## References

- `docs/api/CHAT_COMPLETION_API_REFERENCE.md` (757 lines — full spec)
- `src/backend/app/api/v1/endpoints/managed_chat.py`
- `packages/sdks/react/src/hooks/useChat.ts`
- `packages/sdks/nextjs/src/`
