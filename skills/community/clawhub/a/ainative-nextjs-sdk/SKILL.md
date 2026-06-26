---
name: ainative-nextjs-sdk
description: Use @ainative/next-sdk to add AI chat to Next.js apps (App Router + Pages Router). Use when (1) Installing @ainative/next-sdk, (2) Setting up a streaming chat API route, (3) Protecting routes with AINative auth middleware, (4) Using the server client for API calls, (5) Building full-stack AI apps with Next.js. Published npm package v1.0.1.
---

# @ainative/next-sdk

Server-side AINative client for Next.js with App Router support, streaming chat, and auth middleware.

## Install

```bash
npm install @ainative/next-sdk
```

## Server Client — Chat Completions

```typescript
// app/api/chat/route.ts
import { createServerClient } from '@ainative/next-sdk/server';

export async function POST(request: Request) {
  const { messages } = await request.json();

  const client = createServerClient({
    apiKey: process.env.AINATIVE_API_KEY!,
  });

  // Non-streaming
  const result = await client.chat.completions.create({
    model: 'claude-3-5-sonnet-20241022',
    messages,
    max_tokens: 1024,
  });

  return Response.json(result);
}
```

## Streaming Response

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
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
    },
  });
}
```

## Auth Middleware

```typescript
// middleware.ts (repo root or src/)
import { createMiddleware } from '@ainative/next-sdk/middleware';

export const middleware = createMiddleware({
  apiKey: process.env.AINATIVE_API_KEY!,
  protectedPaths: ['/dashboard', '/api/protected'],
  loginPath: '/login',
  publicPaths: ['/', '/about', '/api/chat'],
});

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
```

## Client-Side (App Router)

```typescript
// app/components/Chat.tsx
'use client';
import { useState } from 'react';

export function Chat() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState('');

  const send = async () => {
    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');

    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: newMessages }),
    });

    const data = await res.json();
    setMessages([...newMessages, data.choices[0].message]);
  };

  return (
    <div>
      {messages.map((m, i) => <p key={i}><b>{m.role}:</b> {m.content}</p>)}
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={send}>Send</button>
    </div>
  );
}
```

## Pages Router (API route)

```typescript
// pages/api/chat.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { createServerClient } from '@ainative/next-sdk/server';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const client = createServerClient({ apiKey: process.env.AINATIVE_API_KEY! });

  const result = await client.chat.completions.create({
    model: 'claude-3-5-sonnet-20241022',
    messages: req.body.messages,
  });

  res.json(result);
}
```

## Environment Variables

```bash
# .env.local
AINATIVE_API_KEY=ak_your_key
```

Never expose `AINATIVE_API_KEY` to the client — only use it in server-side code (route handlers, Server Actions, `getServerSideProps`).

## Exports

```typescript
import { createServerClient } from '@ainative/next-sdk/server';
import { createMiddleware } from '@ainative/next-sdk/middleware';
```

## References

- `packages/sdks/nextjs/src/server/createServerClient.ts` — Server client
- `packages/sdks/nextjs/src/middleware/` — Auth middleware
- `packages/sdks/nextjs/examples/app-router/` — Example app
- `packages/sdks/nextjs/src/index.ts` — Package exports
