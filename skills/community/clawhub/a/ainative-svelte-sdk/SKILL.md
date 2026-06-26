---
name: ainative-svelte-sdk
description: Use @ainative/svelte-sdk to add AI chat to Svelte/SvelteKit apps. Use when (1) Installing @ainative/svelte-sdk, (2) Using Svelte stores for chat state, (3) Configuring AINative in a Svelte app, (4) Displaying chat messages reactively, (5) Handling loading and error states with Svelte stores. Published npm package v1.0.0.
---

# @ainative/svelte-sdk

Svelte stores and utilities for AINative chat completions.

## Install

```bash
npm install @ainative/svelte-sdk
```

## Configure

```typescript
// src/lib/ainative.ts
import { setAINativeConfig } from '@ainative/svelte-sdk';

setAINativeConfig({
  apiKey: import.meta.env.VITE_AINATIVE_API_KEY,
  baseUrl: 'https://api.ainative.studio',
});
```

Call this once in your app root (`+layout.svelte` or `App.svelte`).

## createChatStore

```svelte
<!-- src/lib/Chat.svelte -->
<script lang="ts">
  import { createChatStore } from '@ainative/svelte-sdk';

  const chat = createChatStore({
    model: 'claude-3-5-sonnet-20241022',
  });

  let input = '';

  async function send() {
    if (!input.trim()) return;
    const userMsg = { role: 'user' as const, content: input };
    input = '';
    await chat.sendMessage([...$chat.messages, userMsg]);
  }
</script>

{#each $chat.messages as msg}
  <div class="message {msg.role}">
    <strong>{msg.role}:</strong> {msg.content}
  </div>
{/each}

{#if $chat.isLoading}
  <p>Thinking...</p>
{/if}

{#if $chat.error}
  <p class="error">Error: {$chat.error.message}</p>
{/if}

<input bind:value={input} on:keydown={(e) => e.key === 'Enter' && send()} />
<button on:click={send} disabled={$chat.isLoading}>Send</button>
```

## Store Shape

`$chat` is a reactive store with this shape:

| Field | Type | Description |
|-------|------|-------------|
| `messages` | `Message[]` | Full conversation history |
| `isLoading` | `boolean` | True while request in flight |
| `error` | `AINativeError \| null` | Last error |

## createChatStore Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `model` | string | — | Model ID |
| `initialMessages` | `Message[]` | `[]` | Seed conversation |

## SvelteKit — Server Route

For server-side calls, use the raw API directly (no browser auth exposure):

```typescript
// src/routes/api/chat/+server.ts
import { AINATIVE_API_KEY } from '$env/static/private';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
  const { messages } = await request.json();

  const resp = await fetch('https://api.ainative.studio/v1/public/chat/completions', {
    method: 'POST',
    headers: {
      'X-API-Key': AINATIVE_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'claude-3-5-sonnet-20241022',
      messages,
    }),
  });

  return new Response(resp.body, {
    headers: { 'Content-Type': 'application/json' },
  });
};
```

## Environment Variables

```bash
# .env
VITE_AINATIVE_API_KEY=ak_your_key         # Client-safe (public key only)
AINATIVE_API_KEY=ak_your_key              # Server-side (SvelteKit $env/static/private)
```

> Use server routes for production — never expose API keys in client bundles.

## Exports

```typescript
import {
  createChatStore,
  setAINativeConfig,
  ainativeConfig,
  type Message,
  type ChatState,
  type AINativeError,
} from '@ainative/svelte-sdk';
```

## References

- `packages/sdks/svelte/src/stores/chat.ts` — Chat store implementation
- `packages/sdks/svelte/src/stores/config.ts` — Config store
- `packages/sdks/svelte/src/index.ts` — Package exports
