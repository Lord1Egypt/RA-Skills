---
name: ainative-vue-sdk
description: Use @ainative/vue-sdk to add AI chat to Vue 3 apps. Use when (1) Installing @ainative/vue-sdk, (2) Using the useChat composable in Vue components, (3) Providing AINative config with provideAINative, (4) Displaying reactive chat messages, (5) Building chat UI with Vue 3 Composition API. Published npm package v1.0.0.
---

# @ainative/vue-sdk

Vue 3 composables for AINative chat completions.

## Install

```bash
npm install @ainative/vue-sdk
```

## Setup: provideAINative

```typescript
// main.ts
import { createApp } from 'vue';
import { provideAINative } from '@ainative/vue-sdk';
import App from './App.vue';

const app = createApp(App);

app.provide('ainative', {
  apiKey: import.meta.env.VITE_AINATIVE_API_KEY,
  baseUrl: 'https://api.ainative.studio',
});

app.mount('#app');
```

Or provide inside a component:

```vue
<script setup>
import { provideAINative } from '@ainative/vue-sdk';
provideAINative({ apiKey: import.meta.env.VITE_AINATIVE_API_KEY });
</script>
```

## useChat Composable

```vue
<!-- ChatComponent.vue -->
<script setup lang="ts">
import { ref } from 'vue';
import { useChat } from '@ainative/vue-sdk';
import type { Message } from '@ainative/vue-sdk';

const { messages, isLoading, error, sendMessage, reset } = useChat({
  model: 'claude-3-5-sonnet-20241022',
  initialMessages: [],
});

const input = ref('');

async function send() {
  if (!input.value.trim()) return;
  const newMessages: Message[] = [
    ...messages.value,
    { role: 'user', content: input.value }
  ];
  input.value = '';
  await sendMessage(newMessages);
}
</script>

<template>
  <div>
    <div v-for="(msg, i) in messages" :key="i" :class="['message', msg.role]">
      <strong>{{ msg.role }}:</strong> {{ msg.content }}
    </div>

    <div v-if="isLoading">Thinking...</div>
    <div v-if="error" class="error">Error: {{ error.message }}</div>

    <input
      v-model="input"
      @keydown.enter="send"
      placeholder="Type a message..."
    />
    <button @click="send" :disabled="isLoading">Send</button>
    <button @click="reset">Reset</button>
  </div>
</template>
```

## useChat Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `model` | string | — | Model ID (e.g. `claude-3-5-sonnet-20241022`) |
| `initialMessages` | `Message[]` | `[]` | Seed the conversation |

## useChat Return

| Field | Type | Description |
|-------|------|-------------|
| `messages` | `Ref<Message[]>` | Reactive message list |
| `isLoading` | `Ref<boolean>` | True during request |
| `error` | `Ref<AINativeError \| null>` | Last error |
| `sendMessage` | `(msgs: Message[]) => Promise<...>` | Send next turn |
| `reset` | `() => void` | Clear conversation |

## useCredits Composable

```vue
<script setup>
import { useCredits } from '@ainative/vue-sdk';
const { balance, isLoading, error, refetch } = useCredits();
</script>

<template>
  <div v-if="!isLoading">
    Credits: {{ balance?.remaining_credits }} | Plan: {{ balance?.plan }}
    <button @click="refetch">Refresh</button>
  </div>
</template>
```

## Nuxt Integration

```typescript
// plugins/ainative.client.ts
import { provideAINative } from '@ainative/vue-sdk';
export default defineNuxtPlugin(() => {
  provideAINative({ apiKey: useRuntimeConfig().public.ainativeApiKey });
});
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    public: { ainativeApiKey: process.env.VITE_AINATIVE_API_KEY }
  }
});
```

## Exports

```typescript
import {
  useChat,
  useCredits,
  useAINative,
  provideAINative,
  type Message,
  type UseChatOptions,
  type UseChatReturn,
  type AINativeError,
} from '@ainative/vue-sdk';
```

## References

- `packages/sdks/vue/src/composables/useChat.ts` — useChat implementation
- `packages/sdks/vue/src/composables/useCredits.ts` — useCredits implementation
- `packages/sdks/vue/src/composables/useAINative.ts` — Config injection
- `packages/sdks/vue/src/index.ts` — Package exports
