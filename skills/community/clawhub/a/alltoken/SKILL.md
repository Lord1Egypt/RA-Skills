---
name: alltoken
description: Bootstrap a modular AllToken agent — chat, async image+video, model routing, OpenAI-compatible SDK. Works inside Hermes, OpenClaw, Claude Code, Codex CLI, OpenCode, or any runtime that loads SKILL.md.
metadata:
  version: 1.0.1
  homepage: https://alltoken.ai
  docs: https://alltoken.ai/docs/apis/overview
  license: MIT
  openclaw:
    compat: ">=0.18"
---

# Build a Modular AI Agent with AllToken

This skill helps you create a **modular AI agent** powered by [AllToken](https://alltoken.ai) — a unified, OpenAI-compatible API with access to leading language, image, and video models behind one endpoint, plus automatic provider fallbacks and cost-effective routing.

Designed to be invoked from **Hermes**, **OpenClaw**, Claude Code, Codex CLI, or any other agent runtime that consumes skills.

- **Standalone Agent Core** — runs independently, extensible via hooks
- **OpenAI SDK compatible** — change two settings and you're done
- **Multi-modal** — chat, image (async), video (async) on one key
- **Optional Ink TUI** — terminal UI cleanly separated from agent logic

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                Your Application (TS/Py)             │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Ink TUI   │  │  HTTP API   │  │   Hermes /  │  │
│  │             │  │             │  │   OpenClaw  │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │
│         │                │                │         │
│         └────────────────┼────────────────┘         │
│                          ▼                          │
│              ┌───────────────────────┐              │
│              │      Agent Core       │              │
│              │  (hooks & lifecycle)  │              │
│              └───────────┬───────────┘              │
│                          ▼                          │
│              ┌───────────────────────┐              │
│              │   AllToken REST API   │              │
│              │ api.alltoken.ai/v1    │              │
│              └───────────────────────┘              │
└─────────────────────────────────────────────────────┘
```

## Prerequisites

1. **Create an AllToken account** at [https://alltoken.ai](https://alltoken.ai).
2. **Generate an API key** in **Settings → API Keys** (the key is shown only once — copy it).
3. **Top up credits** if needed in **Settings → Billing**.

> Security: never commit your API key. Use `ALLTOKEN_API_KEY` from the environment.

## API at a glance

- **Base URL:** `https://api.alltoken.ai/v1`
- **Auth header:** `Authorization: Bearer $ALLTOKEN_API_KEY`
- **Compatibility:** OpenAI-compatible — any OpenAI SDK works by overriding `base_url`/`baseURL`.
- **Coverage:**
  - `POST /chat/completions` — chat (streaming, tool calls, thinking, web search)
  - `GET  /models` — OpenAI-compatible model list
  - `POST /images/generations/async` + `GET /images/generations/{id}` — async image generation
  - `POST /videos/generations` + `GET /videos/generations/{id}` — async video generation
  - `GET  /api-account/models` / `/{model_path}` / `/filters` — full catalog with pricing and capabilities (**public**, no auth required)
  - `GET  /api-account/providers` (+ `/{id}/stats`) — providers, health, throughput (**public**)
  - `GET  /api-account/rankings/all` — leaderboards, benchmarks, speed rankings (**public**)
  - `GET  /api-account/health/{routes,summary}` — route health & availability (**public**)
  - `GET  /api-account/user/{api-keys,usage,billing,balance}` — **web-session token only**, not callable with your `Bearer` API key (you'll get `401 auth_error / invalid_token`). Manage these in **Settings → API Keys / Billing** on https://alltoken.ai.

## Project Setup

### Step 1 — Initialize project

```bash
mkdir my-alltoken-agent && cd my-alltoken-agent
npm init -y
npm pkg set type="module"
```

### Step 2 — Install dependencies

```bash
npm install openai zod eventemitter3
npm install ink react        # optional: TUI only
npm install -D typescript @types/react tsx
```

### Step 3 — `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist"
  },
  "include": ["src"]
}
```

### Step 4 — Scripts in `package.json`

```json
{
  "scripts": {
    "start": "tsx src/cli.tsx",
    "start:headless": "tsx src/headless.ts",
    "dev": "tsx watch src/cli.tsx"
  }
}
```

### Step 5 — File layout

```bash
src/
├── client.ts       # AllToken client (OpenAI SDK with overridden baseURL)
├── agent.ts        # Standalone agent core with hooks
├── tools.ts        # Function-calling tool definitions
├── media.ts        # Async image + video helpers (poll loop)
├── cli.tsx         # Optional Ink TUI
└── headless.ts     # Headless / scriptable example
```

## Step 1 — AllToken Client

Create `src/client.ts`. AllToken is OpenAI-compatible; we just override the base URL.

```typescript
import OpenAI from 'openai';

export function createAllTokenClient(apiKey = process.env.ALLTOKEN_API_KEY): OpenAI {
  if (!apiKey) throw new Error('ALLTOKEN_API_KEY is not set');
  return new OpenAI({
    apiKey,
    baseURL: 'https://api.alltoken.ai/v1',
  });
}
```

## Step 2 — Agent Core with Hooks

Create `src/agent.ts` — the standalone agent. It streams via OpenAI's SSE protocol and emits typed events for any UI to consume.

```typescript
import OpenAI from 'openai';
import type {
  ChatCompletionMessageParam,
  ChatCompletionTool,
  ChatCompletionToolMessageParam,
} from 'openai/resources/chat/completions';
import { EventEmitter } from 'eventemitter3';
import { createAllTokenClient } from './client.js';

export interface Message {
  role: 'user' | 'assistant' | 'system' | 'tool';
  content: string;
  tool_call_id?: string;
  name?: string;
}

export interface AgentEvents {
  'message:user': (message: Message) => void;
  'message:assistant': (message: Message) => void;
  'stream:start': () => void;
  'stream:delta': (delta: string, accumulated: string) => void;
  'stream:end': (fullText: string) => void;
  'tool:call': (name: string, args: unknown, callId: string) => void;
  'tool:result': (name: string, result: unknown, callId: string) => void;
  'thinking:start': () => void;
  'thinking:end': () => void;
  'error': (error: Error) => void;
}

export interface ToolHandler {
  definition: ChatCompletionTool;
  execute: (args: any) => Promise<unknown> | unknown;
}

export interface AgentConfig {
  apiKey?: string;
  model?: string;                  // e.g. 'minimax-m2.7', 'gpt-5.4'
  instructions?: string;
  tools?: ToolHandler[];
  maxSteps?: number;               // tool-loop step limit
  temperature?: number;
  enableSearch?: boolean;          // AllToken-specific web-search toggle
}

export class Agent extends EventEmitter<AgentEvents> {
  private client: OpenAI;
  private messages: ChatCompletionMessageParam[] = [];
  private cfg: Required<Omit<AgentConfig, 'apiKey'>>;
  private toolMap: Map<string, ToolHandler>;

  constructor(config: AgentConfig = {}) {
    super();
    this.client = createAllTokenClient(config.apiKey);
    this.cfg = {
      model: config.model ?? 'minimax-m2.7',
      instructions: config.instructions ?? 'You are a helpful assistant.',
      tools: config.tools ?? [],
      maxSteps: config.maxSteps ?? 5,
      temperature: config.temperature ?? 0.7,
      enableSearch: config.enableSearch ?? false,
    };
    this.toolMap = new Map(this.cfg.tools.map((t) => [t.definition.function.name, t]));
    if (this.cfg.instructions) {
      this.messages.push({ role: 'system', content: this.cfg.instructions });
    }
  }

  getMessages(): ChatCompletionMessageParam[] { return [...this.messages]; }
  clearHistory(): void {
    this.messages = this.cfg.instructions
      ? [{ role: 'system', content: this.cfg.instructions }]
      : [];
  }
  setInstructions(text: string): void {
    this.cfg.instructions = text;
    if (this.messages[0]?.role === 'system') this.messages[0] = { role: 'system', content: text };
    else this.messages.unshift({ role: 'system', content: text });
  }
  addTool(t: ToolHandler): void {
    this.cfg.tools.push(t);
    this.toolMap.set(t.definition.function.name, t);
  }

  /** Send a user message, run the tool-loop, stream tokens. Returns the final assistant text. */
  async send(content: string): Promise<string> {
    this.messages.push({ role: 'user', content });
    this.emit('message:user', { role: 'user', content });
    this.emit('thinking:start');

    let finalText = '';

    try {
      for (let step = 0; step < this.cfg.maxSteps; step++) {
        const stream = await this.client.chat.completions.create({
          model: this.cfg.model,
          messages: this.messages,
          temperature: this.cfg.temperature,
          tools: this.cfg.tools.length ? this.cfg.tools.map((t) => t.definition) : undefined,
          stream: true,
          // AllToken extension: opt-in web search (model-dependent)
          ...(this.cfg.enableSearch ? ({ enable_search: true } as any) : {}),
        });

        this.emit('stream:start');
        let text = '';
        const toolCalls: Record<number, { id?: string; name?: string; args: string }> = {};
        let finishReason: string | undefined;

        for await (const chunk of stream) {
          const choice = chunk.choices[0];
          if (!choice) continue;
          const delta: any = choice.delta;

          if (delta?.content) {
            text += delta.content;
            this.emit('stream:delta', delta.content, text);
          }
          if (delta?.tool_calls) {
            for (const tc of delta.tool_calls) {
              const slot = toolCalls[tc.index] ?? (toolCalls[tc.index] = { args: '' });
              if (tc.id) slot.id = tc.id;
              if (tc.function?.name) slot.name = tc.function.name;
              if (tc.function?.arguments) slot.args += tc.function.arguments;
            }
          }
          if (choice.finish_reason) finishReason = choice.finish_reason;
        }

        this.emit('stream:end', text);

        // Persist the assistant turn (with tool_calls if any)
        const calls = Object.values(toolCalls).filter((c) => c.id && c.name);
        if (calls.length) {
          this.messages.push({
            role: 'assistant',
            content: text || null,
            tool_calls: calls.map((c) => ({
              id: c.id!,
              type: 'function',
              function: { name: c.name!, arguments: c.args || '{}' },
            })),
          } as any);

          // Execute tools and append results
          for (const c of calls) {
            const handler = this.toolMap.get(c.name!);
            const parsed = safeJson(c.args);
            this.emit('tool:call', c.name!, parsed, c.id!);
            const result = handler
              ? await handler.execute(parsed)
              : { error: `unknown tool: ${c.name}` };
            this.emit('tool:result', c.name!, result, c.id!);
            const toolMsg: ChatCompletionToolMessageParam = {
              role: 'tool',
              tool_call_id: c.id!,
              content: typeof result === 'string' ? result : JSON.stringify(result),
            };
            this.messages.push(toolMsg);
          }
          continue; // next loop step
        }

        // Terminal: regular completion
        this.messages.push({ role: 'assistant', content: text });
        this.emit('message:assistant', { role: 'assistant', content: text });
        finalText = text;
        break;
      }

      return finalText;
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      this.emit('error', error);
      throw error;
    } finally {
      this.emit('thinking:end');
    }
  }

  /** Non-streaming convenience method. */
  async sendSync(content: string): Promise<string> {
    this.messages.push({ role: 'user', content });
    this.emit('message:user', { role: 'user', content });
    const res = await this.client.chat.completions.create({
      model: this.cfg.model,
      messages: this.messages,
      temperature: this.cfg.temperature,
    });
    const text = res.choices[0]?.message?.content ?? '';
    this.messages.push({ role: 'assistant', content: text });
    this.emit('message:assistant', { role: 'assistant', content: text });
    return text;
  }
}

function safeJson(s: string): unknown {
  try { return JSON.parse(s || '{}'); } catch { return { _raw: s }; }
}

export function createAgent(config: AgentConfig = {}): Agent {
  return new Agent(config);
}
```

## Step 3 — Define Tools

Create `src/tools.ts`:

```typescript
import type { ToolHandler } from './agent.js';

export const timeTool: ToolHandler = {
  definition: {
    type: 'function',
    function: {
      name: 'get_current_time',
      description: 'Get the current date and time',
      parameters: {
        type: 'object',
        properties: {
          timezone: { type: 'string', description: 'IANA timezone, e.g. "UTC", "America/New_York"' },
        },
      },
    },
  },
  execute: ({ timezone }: { timezone?: string }) => ({
    time: new Date().toLocaleString('en-US', { timeZone: timezone || 'UTC' }),
    timezone: timezone || 'UTC',
  }),
};

export const calculatorTool: ToolHandler = {
  definition: {
    type: 'function',
    function: {
      name: 'calculate',
      description: 'Evaluate a basic math expression',
      parameters: {
        type: 'object',
        properties: { expression: { type: 'string' } },
        required: ['expression'],
      },
    },
  },
  execute: ({ expression }: { expression: string }) => {
    // Safe arithmetic evaluator — shunting-yard + RPN, no eval/Function.
    const tokens = expression.match(/\d+(?:\.\d+)?|[+\-*/()]/g) ?? [];
    const prec: Record<string, number> = { '+': 1, '-': 1, '*': 2, '/': 2 };
    const out: string[] = [];
    const ops: string[] = [];
    for (const t of tokens) {
      if (/^\d/.test(t)) {
        out.push(t);
      } else if (t === '(') {
        ops.push(t);
      } else if (t === ')') {
        while (ops.length && ops[ops.length - 1] !== '(') out.push(ops.pop()!);
        ops.pop();
      } else {
        while (
          ops.length &&
          ops[ops.length - 1] !== '(' &&
          (prec[ops[ops.length - 1]] ?? 0) >= prec[t]
        ) {
          out.push(ops.pop()!);
        }
        ops.push(t);
      }
    }
    while (ops.length) out.push(ops.pop()!);
    const stack: number[] = [];
    for (const t of out) {
      if (/^\d/.test(t)) {
        stack.push(parseFloat(t));
      } else {
        const b = stack.pop()!;
        const a = stack.pop()!;
        stack.push(t === '+' ? a + b : t === '-' ? a - b : t === '*' ? a * b : a / b);
      }
    }
    return { expression, result: stack[0] };
  },
};

export const defaultTools = [timeTool, calculatorTool];
```

## Step 4 — Image & Video helpers

AllToken's image and video endpoints are **asynchronous**: create a task, poll until `completed`, then read the result. Create `src/media.ts`:

```typescript
import { createAllTokenClient } from './client.js';

const BASE = 'https://api.alltoken.ai/v1';

async function authedFetch(path: string, init: RequestInit = {}) {
  const apiKey = process.env.ALLTOKEN_API_KEY;
  if (!apiKey) throw new Error('ALLTOKEN_API_KEY is not set');
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      ...(init.headers ?? {}),
    },
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`AllToken ${res.status}: ${body}`);
  }
  return res.json();
}

// ── Images ────────────────────────────────────────────────────────────────
// Result is delivered ONCE: persist `b64_json` immediately. Tasks expire in 30 min.

export interface ImageRequest {
  model?: 'gpt-image-2' | string;          // discover via GET /images/models
  prompt: string;
  size?: '1024x1024' | '1536x1024' | '1024x1536' | 'auto';
  quality?: 'low' | 'medium' | 'high' | 'auto';
  output_format?: 'png' | 'jpeg' | 'webp';
  background?: 'auto' | 'opaque';
  moderation?: 'auto' | 'low';
}

export interface ImageResult {
  id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed' | 'cancelled';
  data?: Array<{ b64_json: string; revised_prompt?: string }>;
  error?: unknown;
}

export async function generateImage(req: ImageRequest, opts: { pollMs?: number } = {}): Promise<ImageResult> {
  const created = await authedFetch('/images/generations/async', {
    method: 'POST',
    body: JSON.stringify({ model: 'gpt-image-2', ...req }),
    // Recommended: deduplicate retries with an Idempotency-Key
    headers: { 'Idempotency-Key': crypto.randomUUID() },
  });

  const id = created.id as string;
  const intervalMs = opts.pollMs ?? 2000;
  while (true) {
    const status = await authedFetch(`/images/generations/${id}`);
    if (status.status === 'completed' || status.status === 'failed' || status.status === 'cancelled') {
      return status;
    }
    await new Promise((r) => setTimeout(r, intervalMs));
  }
}

// ── Videos ────────────────────────────────────────────────────────────────

export interface VideoRequest {
  model: 'seedance-1.5-pro' | 'seedance-2.0' | string;
  prompt: string;
  duration?: number;                       // seconds; -1 = model decides
  ratio?: '16:9' | '9:16' | '4:3' | '3:4' | '21:9' | '1:1' | 'adaptive';
  resolution?: '480p' | '720p' | '1080p';
  generate_audio?: boolean;
  seed?: number;
  watermark?: boolean;
  callback_url?: string;
  // Image-to-video: pass `content` with image_url + role: 'first_frame'
  content?: Array<{
    type: 'image_url' | 'video_url' | 'audio_url' | 'draft_task';
    image_url?: { url: string };
    video_url?: { url: string };
    audio_url?: { url: string };
    role?: 'first_frame' | 'last_frame' | 'reference_image' | 'reference_video' | 'reference_audio';
  }>;
}

export async function generateVideo(req: VideoRequest, opts: { pollMs?: number } = {}) {
  const created = await authedFetch('/videos/generations', {
    method: 'POST',
    body: JSON.stringify(req),
  });
  const id = created.id as string;
  const intervalMs = opts.pollMs ?? 3000;
  while (true) {
    const status = await authedFetch(`/videos/generations/${id}`);
    if (['completed', 'failed', 'cancelled', 'expired'].includes(status.status)) return status;
    await new Promise((r) => setTimeout(r, intervalMs));
  }
}

export async function cancelVideo(id: string) {
  return authedFetch(`/videos/generations/${id}/cancel`, { method: 'POST' });
}
```

Persist `b64_json` to disk in one shot — re-polling a delivered image returns `410 image_already_retrieved` and the result is gone. The 410 envelope:

```json
{"error":{"code":"image_already_retrieved","message":"Image data was already retrieved; please submit a new generation request","request_id":"...","type":"invalid_request_error"}}
```

**Observed latencies** (use these to size your retry budget, not as SLAs):
- Image `gpt-image-2` 1024×1024 `quality=low`: ~15–25 s end-to-end (verified 20.6 s on a real submit).
- Image `quality=high` or 1536×1024: 30–60 s per docs.
- Video `seedance-1.5-pro` 5 s @ 480 p: 30–120 s typical; 1080 p can take 3–5 min.
- Recommended poll interval: 2 s for images, 3 s for videos.

**Submit-response fields** (the full shape, not just `id`):

```json
{"id":"igen_d3b8...","status":"queued","model":"gpt-image-2","created_at":"2026-05-12T13:46:09Z"}
```

After `status==completed`, the GET adds: `data: [{b64_json}]`, `usage: {input_tokens, output_tokens, total_tokens, input_tokens_details}`, `size`, `quality`, `output_format`, `completed_at`, `expires_at`. Note: `revised_prompt` is **not** present in current responses despite appearing in the docs example — treat it as optional.

## Step 5 — Headless usage

Create `src/headless.ts`:

```typescript
import { createAgent } from './agent.js';
import { defaultTools } from './tools.js';
import { generateImage } from './media.js';
import { writeFile } from 'node:fs/promises';

async function main() {
  const agent = createAgent({
    model: 'minimax-m2.7',
    instructions: 'You are a helpful assistant with tools.',
    tools: defaultTools,
    enableSearch: false,
  });

  agent.on('thinking:start', () => console.log('\n🤔 Thinking...'));
  agent.on('tool:call', (name, args) => console.log(`🔧 ${name}`, args));
  agent.on('stream:delta', (delta) => process.stdout.write(delta));
  agent.on('stream:end', () => console.log());
  agent.on('error', (e) => console.error('❌', e.message));

  // Chat
  await agent.send('What time is it in Tokyo?');

  // Image (async)
  const img = await generateImage({
    prompt: 'A clean studio product photo of a glass teapot on a walnut table',
    size: '1024x1024',
    quality: 'high',
  });
  if (img.status === 'completed' && img.data?.[0]?.b64_json) {
    await writeFile('teapot.png', Buffer.from(img.data[0].b64_json, 'base64'));
    console.log('\n💾 Saved teapot.png');
  }
}

main().catch(console.error);
```

Run: `ALLTOKEN_API_KEY=sk-... npm run start:headless`

## Step 6 — Optional Ink TUI

Create `src/cli.tsx` for a terminal chat UI. Subscribe to `stream:delta` and `tool:call` events from the agent and render them. The agent core is UI-agnostic — the same instance can power Hermes, OpenClaw, Discord, or HTTP.

```tsx
import React, { useState, useEffect, useCallback } from 'react';
import { render, Box, Text, useInput, useApp } from 'ink';
import { createAgent, type Message } from './agent.js';
import { defaultTools } from './tools.js';

const agent = createAgent({
  model: 'minimax-m2.7',
  instructions: 'You are a concise assistant.',
  tools: defaultTools,
});

function App() {
  const { exit } = useApp();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState('');
  const [loading, setLoading] = useState(false);

  useInput((ch, key) => {
    if (key.escape) exit();
    if (loading) return;
    if (key.return) {
      const text = input.trim();
      if (!text) return;
      setInput('');
      setMessages((m) => [...m, { role: 'user', content: text }]);
      agent.send(text);
    } else if (key.backspace || key.delete) setInput((v) => v.slice(0, -1));
    else if (ch && !key.ctrl && !key.meta) setInput((v) => v + ch);
  });

  useEffect(() => {
    const onStart = () => { setLoading(true); setStreaming(''); };
    const onDelta = (_d: string, acc: string) => setStreaming(acc);
    const onAssistant = (m: Message) => {
      setMessages((prev) => [...prev, m]);
      setStreaming('');
      setLoading(false);
    };
    agent.on('thinking:start', onStart);
    agent.on('stream:delta', onDelta);
    agent.on('message:assistant', onAssistant);
    return () => {
      agent.off('thinking:start', onStart);
      agent.off('stream:delta', onDelta);
      agent.off('message:assistant', onAssistant);
    };
  }, []);

  return (
    <Box flexDirection="column" padding={1}>
      <Text bold color="magenta">🤖 AllToken Agent</Text>
      {messages.map((m, i) => (
        <Box key={i} flexDirection="column" marginTop={1}>
          <Text bold color={m.role === 'user' ? 'cyan' : 'green'}>
            {m.role === 'user' ? '▶ You' : '◀ Assistant'}
          </Text>
          <Text wrap="wrap">{m.content}</Text>
        </Box>
      ))}
      {streaming && (
        <Box flexDirection="column" marginTop={1}>
          <Text bold color="green">◀ Assistant</Text>
          <Text wrap="wrap">{streaming}<Text color="gray">▌</Text></Text>
        </Box>
      )}
      <Box borderStyle="single" borderColor="gray" marginTop={1} paddingX={1}>
        <Text color="yellow">{'> '}</Text>
        <Text>{input}</Text>
        <Text color="gray">{loading ? ' ···' : '█'}</Text>
      </Box>
    </Box>
  );
}

render(<App />);
```

## Python equivalent (one-file)

For Python users — including those embedding the agent inside Hermes or OpenClaw Python tools:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["ALLTOKEN_API_KEY"],
    base_url="https://api.alltoken.ai/v1",
)

# Streaming chat
stream = client.chat.completions.create(
    model="minimax-m2.7",
    messages=[{"role": "user", "content": "Explain SSE in one sentence."}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()
```

Async image (poll loop):

```python
import os, time, base64, uuid, requests

BASE = "https://api.alltoken.ai/v1"
H = {"Authorization": f"Bearer {os.environ['ALLTOKEN_API_KEY']}", "Content-Type": "application/json"}

task = requests.post(
    f"{BASE}/images/generations/async",
    headers={**H, "Idempotency-Key": str(uuid.uuid4())},
    json={"model": "gpt-image-2", "prompt": "A cat astronaut, studio light", "size": "1024x1024", "quality": "high"},
).json()

while True:
    res = requests.get(f"{BASE}/images/generations/{task['id']}", headers=H).json()
    if res["status"] in ("completed", "failed", "cancelled"):
        break
    time.sleep(2)

if res["status"] == "completed":
    with open("cat.png", "wb") as f:
        f.write(base64.b64decode(res["data"][0]["b64_json"]))
```

## Using AllToken from inside Hermes / OpenClaw

Both Hermes and OpenClaw load skills from `SKILL.md` files and can run TypeScript or Python tools at the agent boundary. There are two integration patterns:

### Pattern A — AllToken as your agent's model provider

Point your host agent's HTTP client at AllToken. In OpenClaw / Hermes config, set:

```yaml
provider:
  base_url: https://api.alltoken.ai/v1
  api_key: ${ALLTOKEN_API_KEY}
model: minimax-m2.7
```

No code changes needed — the OpenAI-compatible endpoint accepts the same requests.

### Pattern B — AllToken as a tool inside another agent

Drop the `agent.ts` / `media.ts` modules into the host agent's tools directory and expose them as callable tools (`chat`, `generate_image`, `generate_video`). The host agent (running on any model) then delegates multimodal work to AllToken on demand.

```typescript
// host-agent-tool.ts
import { createAgent } from './agent.js';
import { generateImage, generateVideo } from './media.js';

const alltoken = createAgent({ model: 'minimax-m2.7' });

export const tools = {
  alltoken_chat: (input: { prompt: string }) => alltoken.sendSync(input.prompt),
  alltoken_image: (input: { prompt: string; size?: string }) => generateImage(input as any),
  alltoken_video: (input: { prompt: string; duration?: number }) =>
    generateVideo({ model: 'seedance-1.5-pro', ...input }),
};
```

## Discovering models

**Verified-working model IDs as of 2026-05-12** (use these for quick starts; re-confirm via `GET /v1/models` before production):

| Use case | IDs |
|----------|-----|
| Chat — cheap / fast | `gpt-5.4-nano`, `gpt-5.4-mini`, `claude-haiku-4-5`, `gemini-3-flash-preview`, `glm-4.7-flash`, `qwen3.6-flash`, `deepseek-v4-flash`, `minimax-m2.5-highspeed` |
| Chat — flagship | `gpt-5.4`, `gpt-5.4-pro`, `gpt-5.5`, `claude-opus-4-7`, `claude-sonnet-4-6`, `gemini-3.1-pro-preview`, `glm-5.1`, `deepseek-v4-pro`, `qwen3.6-max-preview`, `kimi-k2.6`, `minimax-m2.7` |
| Chat — code | `gpt-5.3-codex`, `qwen3-coder-next` |
| Image | `gpt-image-2` |
| Video — text/image to video | `seedance-1.5-pro`, `seedance-2.0`, `happyhorse-1.0-t2v`, `happyhorse-1.0-i2v` |
| Video — editing / reference | `happyhorse-1.0-video-edit`, `happyhorse-1.0-r2v` |

Available chat models on a fresh key: **38** as of this writing. Image: **1**. Video: **7**.

**Do not hardcode model IDs in production** — the catalog evolves. Use the live endpoints:

```typescript
// OpenAI-compatible list (good for SDK clients)
const list = await fetch('https://api.alltoken.ai/v1/models', {
  headers: { Authorization: `Bearer ${process.env.ALLTOKEN_API_KEY}` },
}).then((r) => r.json());

// Rich catalog with pricing, capabilities, tags (used by the website)
const catalog = await fetch('https://api.alltoken.ai/api-account/models').then((r) => r.json());

// Single model detail page
const detail = await fetch('https://api.alltoken.ai/api-account/models/gpt-5.4').then((r) => r.json());
```

Pair with the **Rankings API** (`GET /api-account/rankings/all`) for live leaderboards by usage, benchmarks, throughput, and category leaders — useful for `--auto` model selection.

## Routing & fallbacks

AllToken handles provider routing internally. Two knobs:

- **Account-level default routing** — set `routing_mode` (`code` or `manual`), `allowed_models`, and a `default_models` priority list on each API key:
  ```
  POST   /api-account/user/api-keys
  PUT    /api-account/user/api-keys/{key_id}/default-models
  ```
- **Per-request override** — pass the exact `model` ID in the request body to bypass routing for that call.

When a provider returns `502/503`, AllToken may automatically fall back to the next provider for the model.

## Web search (`enable_search`)

Pass `enable_search: true` on a chat completion to opt into AllToken's unified web-search backend. **Support is per-provider, not per-request shape** — same flag, different effective behavior across model families. Live probe on 2026-05-12 (asking "current Bitcoin price"):

| Family | Outcome | Notes |
|---|---|---|
| **DeepSeek** (`deepseek-v3.2`, `deepseek-v4-pro`) | ✅ Searches | Returns fresh prices with timestamps |
| **Qwen** (`qwen3.6-flash`, `qwen3.6-max-preview`) | ✅ Searches | Same fresh data via the unified backend |
| **Claude** (`claude-opus-4-7`, `claude-sonnet-4-6`) | ❌ Silently ignores | Model responds "I don't have web search" |
| **GLM** (`glm-5`, `glm-5.1`) | ❌ Silently ignores | Same as Claude |
| **Kimi** (`kimi-k2.6`) | ❌ Silently ignores | |
| **Minimax** (`minimax-m2.7`) | ❌ Silently ignores | |
| **Gemini** (`gemini-3.1-pro-preview`) | ⚠️ Empty / refusal | Inconsistent — re-test before relying |
| **OpenAI** (`gpt-5.4`, `gpt-5.4-nano`, `gpt-5.5`) | 🔴 HTTP 503 `all_providers_failed` | Upstream rejects the flag |

**Recommendation:** when you need search, default to a **DeepSeek** or **Qwen** model. If you're on a different family, fall back to a function-calling pattern (model emits a tool call → your tool hits a search API → you re-invoke). The `enable_search` matrix above is empirical and provider-side support may change — re-test for critical paths.

Note: AllToken does **not** include search-result citations in the response `annotations[]` field today, so detecting "did search fire" requires latency heuristics (typically +6 – 15 s vs no-search baseline) or content sniffing for fresh facts.

## Health, rate limits, errors

- **Per-key rate limits:** set `rpm_limit`, `tpm_limit`, `monthly_quota`, `credit_limit` when creating the key.
- **Status codes you should handle:** `400` invalid params · `401` bad key · `402` insufficient balance · `403` forbidden · `404` not found · `429` rate limited (respect `Retry-After`) · `5xx` upstream — already retried server-side when safe.
- **Error envelope (real wire format):**
  ```json
  {
    "error": {
      "code": "invalid_api_key",
      "message": "Invalid or revoked API key",
      "param": null,
      "type": "auth_error",
      "request_id": "d81itf8gdg1fp5ko4bjg"
    }
  }
  ```
  Note: `code` is a **string slug** (e.g. `"invalid_api_key"`, `"image_already_retrieved"`, `"all_providers_failed"`), not the numeric HTTP status. `type` groups errors (`auth_error`, `invalid_request_error`, `api_error`, …). Include `request_id` when filing support tickets.

**Python error-dispatch helper:**

```python
import json, time, urllib.request, urllib.error

def call(req):
    try:
        return urllib.request.urlopen(req, timeout=60)
    except urllib.error.HTTPError as e:
        body = e.read()
        try:
            err = json.loads(body).get("error", {})
        except Exception:
            err = {}
        retry_after = e.headers.get("Retry-After")     # integer seconds (AllToken format)
        if e.code == 429 and retry_after:
            time.sleep(int(retry_after))
            return call(req)                            # one retry
        if e.code == 401:    raise RuntimeError(f"auth: {err.get('code')} — rotate API key")
        if e.code == 402:    raise RuntimeError(f"top up credits: {err.get('message')}")
        if e.code == 410 and err.get("code") == "image_already_retrieved":
            raise RuntimeError("re-submit; image was already delivered")
        if 500 <= e.code < 600 and err.get("code") == "all_providers_failed":
            raise RuntimeError("upstream — try fallback model or retry with jitter")
        raise RuntimeError(f"{e.code} {err.get('type')}/{err.get('code')}: {err.get('message')} [req={err.get('request_id')}]")
```

`Retry-After` is sent as **integer seconds**. Always combine an explicit retry-after read with exponential backoff (+ jitter) as the fallback when the header is missing.
- **Health dashboard:** `GET /api-account/health/summary` (returns `{"data": {...}}` envelope) and `/health/routes` show live availability, p50/p95 latency, and incident routes — wire this into your runbook.

## Cost tracking & budgets

**Per-request cost:** every chat response includes a `usage` block:

```json
"usage": {
  "prompt_tokens": 13,
  "completion_tokens": 4,
  "total_tokens": 17,
  "prompt_tokens_details": { "cached_tokens": 0, "cache_creation_input_tokens": 0, "audio_tokens": 0 },
  "completion_tokens_details": { "reasoning_tokens": 0, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0 }
}
```

**Capture usage from a streaming response:** pass `stream_options: {"include_usage": true}`. The final `data:` chunk before `data: [DONE]` will have `choices: []` and the populated `usage`. Without this option, `usage` is `null` on every streamed chunk.

```python
stream = client.chat.completions.create(
    model="gpt-5.4-nano", messages=[...], stream=True,
    stream_options={"include_usage": True},
)
usage = None
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
    if chunk.usage is not None:
        usage = chunk.usage   # only present on the terminal chunk
```

**Per-request cost telemetry (vendor extension):** AllToken also emits one extra **SSE comment line** *after* `data: [DONE]` with a fiat-priced breakdown:

```
: {"cost":"0.0000188000","input_price":"0.0002000000","output_price":"0.0012500000","prompt_tokens":19,"completion_tokens":12}
```

Standard OpenAI SDKs **drop comment lines** (lines beginning with `:`), so this is invisible when using `openai`. To capture it, parse the raw SSE stream yourself and do **not** stop on `[DONE]`:

```python
# stdlib-only — captures both usage (from data: chunks) AND cost comment (post-DONE)
import urllib.request, json
req = urllib.request.Request(URL, data=BODY, method="POST", headers=H)
r = urllib.request.urlopen(req)
saw_done = False
for raw in iter(r.readline, b""):
    line = raw.decode().rstrip("\n")
    if line.startswith(":"):
        cost = json.loads(line[1:])      # {"cost": "...", ...}
    elif line.startswith("data: "):
        data = line[6:]
        if data == "[DONE]": saw_done = True; continue
        # ... parse chunk
```

**Other useful response metadata:** chat responses also carry top-level `service_tier` (e.g. `"default"`) and `x-gateway-request-id` (use this when filing support tickets).

**Account-wide totals:** `/api-account/user/{balance,billing,usage,billing/orders,...}` exist but are **not** callable with the API key — they need the web-session token. Check balance and history in **Settings → Billing** on https://alltoken.ai, or top up via the same dashboard.

## Extending the Agent

### Custom hooks

```typescript
const agent = createAgent({ model: 'minimax-m2.7' });

agent.on('message:user',      (m) => db.insert('user', m.content));
agent.on('message:assistant', (m) => db.insert('assistant', m.content));
agent.on('tool:call',         (name, args) => analytics.track('tool', { name, args }));
agent.on('error',             (err) => sentry.capture(err));
```

### HTTP server (one agent per session)

```typescript
import express from 'express';
import { createAgent, type Agent } from './agent.js';

const app = express(); app.use(express.json());
const sessions = new Map<string, Agent>();

app.post('/chat', async (req, res) => {
  const { sessionId, message } = req.body;
  let agent = sessions.get(sessionId);
  if (!agent) { agent = createAgent(); sessions.set(sessionId, agent); }
  res.json({ response: await agent.sendSync(message), history: agent.getMessages() });
});

app.listen(3000);
```

## Agent API Reference

### `createAgent(config)`

| Option         | Type          | Default                       | Description                              |
|----------------|---------------|-------------------------------|------------------------------------------|
| `apiKey`       | string        | `process.env.ALLTOKEN_API_KEY`| AllToken API key                         |
| `model`        | string        | `'minimax-m2.7'`              | Model ID (see model discovery)           |
| `instructions` | string        | `'You are a helpful assistant.'` | System prompt                         |
| `tools`        | `ToolHandler[]`| `[]`                         | Function-calling tools                   |
| `maxSteps`     | number        | `5`                           | Max tool-loop iterations                 |
| `temperature`  | number        | `0.7`                         | Sampling temperature 0–2                 |
| `enableSearch` | boolean       | `false`                       | AllToken `enable_search` extension       |

### Methods

| Method              | Returns           | Description                       |
|---------------------|-------------------|-----------------------------------|
| `send(content)`     | `Promise<string>` | Streaming send + tool loop        |
| `sendSync(content)` | `Promise<string>` | Non-streaming send                |
| `getMessages()`     | `Message[]`       | Full conversation                 |
| `clearHistory()`    | `void`            | Reset (keeps system prompt)       |
| `setInstructions()` | `void`            | Update system prompt              |
| `addTool(tool)`     | `void`            | Register tool at runtime          |

### Events

| Event              | Payload                       | Notes                              |
|--------------------|-------------------------------|------------------------------------|
| `message:user`     | `Message`                     |                                    |
| `message:assistant`| `Message`                     | Final turn (post tool loop)        |
| `stream:start`     | —                             |                                    |
| `stream:delta`     | `(delta, accumulated)`        | OpenAI-style token chunks          |
| `stream:end`       | `fullText`                    |                                    |
| `tool:call`        | `(name, args, callId)`        |                                    |
| `tool:result`      | `(name, result, callId)`      |                                    |
| `thinking:start`   | —                             |                                    |
| `thinking:end`     | —                             |                                    |
| `error`            | `Error`                       |                                    |

## Resources

**Core API**
- API overview: https://alltoken.ai/docs/apis/overview
- Chat completions: https://alltoken.ai/docs/apis/completions
- Image generation: https://alltoken.ai/docs/apis/image
- Video generation: https://alltoken.ai/docs/apis/video
- Models / Providers / Health / Rankings / Keys / Billing: https://alltoken.ai/docs/apis/{models,providers,health,rankings,keys,billing}
- Interactive API explorer: https://alltoken.ai/docs/apis/interactive

**Guides (one topic per page)**
- Quickstart: https://alltoken.ai/docs/guides/quickstart
- Authentication: https://alltoken.ai/docs/guides/authentication
- Models: https://alltoken.ai/docs/guides/models
- Multimodal: https://alltoken.ai/docs/guides/multimodal
- Streaming: https://alltoken.ai/docs/guides/streaming
- Function Calling: https://alltoken.ai/docs/guides/function-calling
- Thinking Mode: https://alltoken.ai/docs/guides/thinking-mode
- Web Search: https://alltoken.ai/docs/guides/web-search
- Video Generation: https://alltoken.ai/docs/guides/video-generation
- Model Routing: https://alltoken.ai/docs/guides/model-routing
- Model Fallbacks: https://alltoken.ai/docs/guides/model-fallbacks
- Provider Selection: https://alltoken.ai/docs/guides/provider-selection
- Rate Limits: https://alltoken.ai/docs/guides/rate-limits
- Cost Tracking: https://alltoken.ai/docs/guides/cost-tracking

**Live endpoints (callable now)**
- OpenAI-compatible model list: `GET https://api.alltoken.ai/v1/models` (Bearer)
- Public catalog (no auth): `GET https://api.alltoken.ai/api-account/models`
- Public health: `GET https://api.alltoken.ai/api-account/health/summary`

**Account management:** Settings → API Keys / Billing on https://alltoken.ai (web session required; not callable with your `Bearer` API key)

**SDKs**
- AllToken SDK overview: https://alltoken.ai/docs/sdks/overview
- OpenAI SDK (TypeScript): https://github.com/openai/openai-node
- OpenAI SDK (Python): https://github.com/openai/openai-python
- Ink (terminal UI): https://github.com/vadimdemedes/ink
