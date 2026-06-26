---
name: ainative-react-sdk
description: Use @ainative/react-sdk to add AI chat and credits to React apps. Use when (1) Installing @ainative/react-sdk, (2) Using the useChat hook for chat completions, (3) Displaying credit balance with useCredits, (4) Setting up AINativeProvider, (5) Handling loading/error states in chat UI. Published npm package v1.0.1.
---

# @ainative/react-sdk

React hooks and components for AINative — chat completions, credit tracking, and managed sessions.

## Install

```bash
npm install @ainative/react-sdk
```

## Setup: AINativeProvider

Wrap your app (or a subtree) with the provider:

```tsx
import { AINativeProvider } from '@ainative/react-sdk';

function App() {
  return (
    <AINativeProvider config={{ apiKey: 'ak_your_key' }}>
      <YourApp />
    </AINativeProvider>
  );
}
```

## useChat Hook

```tsx
import { useChat } from '@ainative/react-sdk';
import type { Message } from '@ainative/react-sdk';

function ChatUI() {
  const { messages, isLoading, error, sendMessage } = useChat({
    model: 'claude-3-5-sonnet-20241022',
    temperature: 0.7,
    max_tokens: 1024,
  });

  const handleSend = async (input: string) => {
    await sendMessage([
      ...messages,
      { role: 'user', content: input }
    ]);
  };

  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i} className={`message ${msg.role}`}>
          <strong>{msg.role}:</strong> {msg.content}
        </div>
      ))}
      {isLoading && <div>Thinking...</div>}
      {error && <div className="error">Error: {error.message}</div>}
      <input
        onKeyDown={(e) => e.key === 'Enter' && handleSend(e.currentTarget.value)}
        placeholder="Type a message..."
      />
    </div>
  );
}
```

### useChat Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `model` | string | — | Model ID (e.g. `claude-3-5-sonnet-20241022`) |
| `temperature` | number | 0.7 | Randomness (0–1) |
| `max_tokens` | number | 1024 | Max response tokens |

### useChat Return

| Field | Type | Description |
|-------|------|-------------|
| `messages` | `Message[]` | Full conversation history |
| `isLoading` | `boolean` | True while request in flight |
| `error` | `AINativeError \| null` | Last error, if any |
| `sendMessage` | `(msgs: Message[]) => Promise<...>` | Send next message |

## useCredits Hook

```tsx
import { useCredits } from '@ainative/react-sdk';

function CreditsBar() {
  const { balance, isLoading, error, refetch } = useCredits();

  if (isLoading) return <div>Loading credits...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <span>{balance?.remaining_credits} credits remaining</span>
      <span> | Plan: {balance?.plan}</span>
      <button onClick={refetch}>Refresh</button>
    </div>
  );
}
```

### useCredits Return

| Field | Type | Description |
|-------|------|-------------|
| `balance` | `CreditBalance \| null` | Balance data |
| `isLoading` | `boolean` | Fetching state |
| `error` | `AINativeError \| null` | Error state |
| `refetch` | `() => void` | Manually refresh |

`CreditBalance` shape: `{ remaining_credits: number, plan: string, ... }`

## Exports

```typescript
import {
  AINativeProvider,
  useChat,
  useCredits,
  useAINativeContext,  // access raw config/baseUrl
  type Message,
  type ChatCompletionResponse,
  type CreditBalance,
  type AINativeError,
  type UseChatOptions,
} from '@ainative/react-sdk';
```

## Environment Variable (CRA / Vite)

```bash
REACT_APP_AINATIVE_API_KEY=ak_your_key   # CRA
VITE_AINATIVE_API_KEY=ak_your_key        # Vite
```

```tsx
<AINativeProvider config={{ apiKey: process.env.REACT_APP_AINATIVE_API_KEY! }}>
```

## References

- `packages/sdks/react/src/hooks/useChat.ts` — Hook implementation
- `packages/sdks/react/src/hooks/useCredits.ts` — Credits hook
- `packages/sdks/react/src/AINativeProvider.tsx` — Provider context
- `packages/sdks/react/src/index.ts` — Package exports
