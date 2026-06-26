---
name: ainative-sdk-quickstart
description: Get started with AINative SDKs in under 5 minutes. Use when (1) Setting up AINative for the first time, (2) Choosing between React/Next.js/Svelte/Vue SDKs, (3) Installing and configuring any AINative SDK, (4) Getting an API key and project ID, (5) Making the first API call. Covers all four framework SDKs and the zerodb-cli init command. Closes #1517.
---

# AINative SDK Quick Start

## 1. Get an API Key (30 seconds)

```bash
# Auto-creates a project + API key, configures your IDE's MCP server
npx zerodb init
```

This outputs:
```
API Key: ak_...
Project ID: proj_...
MCP config written to .claude/mcp.json (or cursor/mcp.json)
```

Or create manually at `https://app.ainative.studio` → Settings → API Keys.

## 2. Choose Your SDK

| Framework | Package | Hook/API |
|-----------|---------|----------|
| React | `@ainative/react-sdk` | `useChat`, `useCredits` |
| Next.js | `@ainative/next-sdk` | Server client + middleware |
| Svelte | `@ainative/svelte-sdk` | Svelte stores |
| Vue | `@ainative/vue-sdk` | Composables |
| Raw API | `requests` / `fetch` | REST directly |

## 3. React

```bash
npm install @ainative/react-sdk
```

```tsx
import { AINativeProvider, useChat } from '@ainative/react-sdk';

function App() {
  return (
    <AINativeProvider config={{ apiKey: 'ak_your_key' }}>
      <Chat />
    </AINativeProvider>
  );
}

function Chat() {
  const { messages, sendMessage, isLoading } = useChat({
    model: 'claude-3-5-sonnet-20241022',
  });

  return (
    <div>
      {messages.map((m, i) => <div key={i}>{m.role}: {m.content}</div>)}
      <button onClick={() => sendMessage([...messages, { role: 'user', content: 'Hello' }])}
              disabled={isLoading}>
        Send
      </button>
    </div>
  );
}
```

## 4. Next.js

```bash
npm install @ainative/next-sdk
```

```typescript
// app/api/chat/route.ts
import { createServerClient } from '@ainative/next-sdk/server';

export async function POST(request: Request) {
  const { messages } = await request.json();
  const client = createServerClient({ apiKey: process.env.AINATIVE_API_KEY! });

  const result = await client.chat.completions.create({
    model: 'claude-3-5-sonnet-20241022',
    messages,
    stream: true,
  });

  return new Response(result.body, {
    headers: { 'Content-Type': 'text/event-stream' },
  });
}
```

## 5. Svelte

```bash
npm install @ainative/svelte-sdk
```

```svelte
<script>
  import { createChatStore, setAINativeConfig } from '@ainative/svelte-sdk';

  setAINativeConfig({ apiKey: 'ak_your_key' });
  const chat = createChatStore({ model: 'claude-3-5-sonnet-20241022' });
</script>

{#each $chat.messages as msg}
  <p><b>{msg.role}:</b> {msg.content}</p>
{/each}
<button on:click={() => chat.sendMessage([...$chat.messages, { role: 'user', content: 'Hi' }])}>
  Send
</button>
```

## 6. Vue

```bash
npm install @ainative/vue-sdk
```

```vue
<script setup>
import { useChat } from '@ainative/vue-sdk';
import { provideAINative } from '@ainative/vue-sdk';

provideAINative({ apiKey: 'ak_your_key' });
const { messages, sendMessage, isLoading } = useChat({ model: 'claude-3-5-sonnet-20241022' });
</script>

<template>
  <div v-for="(msg, i) in messages" :key="i">{{ msg.role }}: {{ msg.content }}</div>
  <button @click="sendMessage([...messages, { role: 'user', content: 'Hi' }])" :disabled="isLoading">
    Send
  </button>
</template>
```

## 7. Environment Variables

```bash
# .env
AINATIVE_API_KEY=ak_your_key
NEXT_PUBLIC_AINATIVE_API_KEY=ak_your_key  # Next.js client-side
```

## References

- `packages/sdks/react/` — React SDK source
- `packages/sdks/nextjs/` — Next.js SDK source
- `packages/sdks/svelte/` — Svelte SDK source
- `packages/sdks/vue/` — Vue SDK source
- `packages/zerodb-cli/` — zerodb init source
