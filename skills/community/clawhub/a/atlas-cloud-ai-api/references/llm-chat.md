# LLM Chat API — Complete Code Templates

Read this file when implementing LLM chat with Atlas Cloud API.

Atlas Cloud LLM API is **fully OpenAI-compatible**. Use the OpenAI SDK directly or raw HTTP.

## API Flow

LLM chat is **synchronous** (no polling needed):
- **Endpoint**: `POST https://api.atlascloud.ai/v1/chat/completions`
- Supports streaming via SSE (`"stream": true`)

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Model ID (e.g. `qwen/qwen3.5-397b-a17b`) |
| `messages` | array | Yes | `[{role, content}]` — roles: "system", "user", "assistant" |
| `max_tokens` | integer | No | Max response tokens |
| `temperature` | number | No | Sampling temperature (0-2, default: 1) |
| `top_p` | number | No | Nucleus sampling (0-1, default: 1) |
| `stream` | boolean | No | Enable SSE streaming (default: false) |

---

## Python (OpenAI SDK) — Recommended

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("ATLASCLOUD_API_KEY"),
    base_url="https://api.atlascloud.ai/v1",
)

response = client.chat.completions.create(
    model="qwen/qwen3.5-397b-a17b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms."},
    ],
    max_tokens=1024,
    temperature=0.7,
)

print(response.choices[0].message.content)
print(f"Tokens used: {response.usage.total_tokens}")
```

---

## Python (Raw HTTP)

```python
import requests
import os

ATLAS_API_KEY = os.environ.get("ATLASCLOUD_API_KEY")

response = requests.post(
    "https://api.atlascloud.ai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {ATLAS_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "qwen/qwen3.5-397b-a17b",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain quantum computing in simple terms."},
        ],
        "max_tokens": 1024,
        "temperature": 0.7,
    },
    timeout=120,
)

data = response.json()
print(data["choices"][0]["message"]["content"])
```

---

## Node.js / TypeScript (OpenAI SDK) — Recommended

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.ATLASCLOUD_API_KEY,
  baseURL: 'https://api.atlascloud.ai/v1',
});

const response = await client.chat.completions.create({
  model: 'qwen/qwen3.5-397b-a17b',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Explain quantum computing in simple terms.' },
  ],
  max_tokens: 1024,
  temperature: 0.7,
});

console.log(response.choices[0].message.content);
console.log(`Tokens used: ${response.usage?.total_tokens}`);
```

---

## Node.js / TypeScript (Raw fetch)

```typescript
const response = await fetch('https://api.atlascloud.ai/v1/chat/completions', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.ATLASCLOUD_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'qwen/qwen3.5-397b-a17b',
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: 'Explain quantum computing in simple terms.' },
    ],
    max_tokens: 1024,
    temperature: 0.7,
  }),
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

---

## Streaming

### Python (OpenAI SDK)

```python
stream = client.chat.completions.create(
    model="qwen/qwen3.5-397b-a17b",
    messages=[{"role": "user", "content": "Write a short poem about the ocean."}],
    max_tokens=512,
    stream=True,
)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
print()
```

### Node.js / TypeScript (OpenAI SDK)

```typescript
const stream = await client.chat.completions.create({
  model: 'qwen/qwen3.5-397b-a17b',
  messages: [{ role: 'user', content: 'Write a short poem about the ocean.' }],
  max_tokens: 512,
  stream: true,
});

for await (const chunk of stream) {
  const content = chunk.choices[0]?.delta?.content;
  if (content) {
    process.stdout.write(content);
  }
}
console.log();
```

### Raw SSE Streaming (Node.js)

```typescript
const response = await fetch('https://api.atlascloud.ai/v1/chat/completions', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.ATLASCLOUD_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'qwen/qwen3.5-397b-a17b',
    messages: [{ role: 'user', content: 'Write a short poem about the ocean.' }],
    max_tokens: 512,
    stream: true,
  }),
});

const reader = response.body!.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const text = decoder.decode(value, { stream: true });
  const lines = text.split('\n').filter((line) => line.startsWith('data: '));

  for (const line of lines) {
    const data = line.slice(6); // Strip "data: " prefix
    if (data === '[DONE]') break;

    const parsed = JSON.parse(data);
    const content = parsed.choices[0]?.delta?.content;
    if (content) {
      process.stdout.write(content);
    }
  }
}
```

---

## cURL

### Basic Request

```bash
curl -X POST "https://api.atlascloud.ai/v1/chat/completions" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen/qwen3.5-397b-a17b",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    "max_tokens": 1024,
    "temperature": 0.7
  }'
```

### Streaming

```bash
curl -X POST "https://api.atlascloud.ai/v1/chat/completions" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -N \
  -d '{
    "model": "qwen/qwen3.5-397b-a17b",
    "messages": [
      {"role": "user", "content": "Write a short poem about the ocean."}
    ],
    "max_tokens": 512,
    "stream": true
  }'
```
