---
name: aiusd-pro
version: 1.0.1
description: "AIUSD Pro — AI-powered trading agent with built-in reasoning. Use when user wants to trade, check balances, or manage positions through natural language conversation."
license: MIT
compatibility: "Requires node >= 18"
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins: ["node"]
---

# AIUSD Pro

Chat with AIUSD using natural language. This skill delegates to a backend
AI agent — you do NOT need to understand AIUSD internals or construct
specific commands.

## CLI entry point

All commands in this skill use `npx -y aiusd-pro` as the CLI prefix. This works without any global installation — npx resolves the package from npm automatically.

If `aiusd-pro` is already in PATH (via `npm install -g aiusd-pro`), you may use `aiusd-pro` directly instead.

## When to use

Use when the user wants anything related to AIUSD or trading
through natural conversation. Examples:
- "What are my balances?"
- "Buy 100 USDC worth of SOL"
- "Stake 500 AIUSD"
- "Long ETH 5x on HyperLiquid"
- "Show trending tokens"

## Authentication

If `npx -y aiusd-pro send` fails with auth error, run login:

1. `npx -y aiusd-pro login --browser` → prints JSON with `url` and `session_id`
2. Send the `url` to the user (NEVER fabricate it)
3. `npx -y aiusd-pro login --poll-session <session_id>` → waits for sign-in

## Usage

### Send a message (background mode)

Backend agent operations take 10-300 seconds (tool calls, reasoning, trading,
transaction confirmation). **Always use background mode** to avoid exec
timeout cutting off output:

```
bash background:true command:"npx -y aiusd-pro send 'user request here'"
```

Returns a `sessionId`. Then poll for completion and retrieve output:

```
process action:poll sessionId:<id>
process action:log sessionId:<id>
```

**Complete pattern:**

1. Start: `bash background:true command:"npx -y aiusd-pro send 'What are my balances?'"`
   → returns `sessionId: abc123`
2. Wait & poll: `process action:poll sessionId:abc123`
   → returns `running` or `exited`
3. Get output: `process action:log sessionId:abc123`
   → returns the agent's full response text
4. Relay output to user as-is

### Multi-turn conversation

Session context is maintained automatically across `send` calls.
The backend agent remembers all previous messages in the session.

**Confirmation flow example:**

1. `bash background:true command:"npx -y aiusd-pro send 'Buy 100 USDC worth of SOL'"`
2. Poll + log → agent responds: "Will buy ~0.65 SOL at $153. Confirm?"
3. Relay to user, user says "yes"
4. `bash background:true command:"npx -y aiusd-pro send 'yes'"`
5. Poll + log → agent responds: "Done. TX: abc123..."
6. Relay to user

**Follow-up questions work the same way** — just `send` the user's
response. The backend has full conversation history.

To start a fresh conversation:

```
bash command:"npx -y aiusd-pro session reset"
```

### Cancel

```
bash command:"npx -y aiusd-pro cancel"
```

### Session management

```
bash command:"npx -y aiusd-pro session new"
bash command:"npx -y aiusd-pro session list"
bash command:"npx -y aiusd-pro session reset"
```

## Rules

1. **Always use `background:true`** for `send` — agent responses take 10-300s.
2. Pass user intent as natural language — do NOT interpret or construct
   specific trading commands.
3. Backend agent handles all domain knowledge, tool selection, and
   multi-step reasoning.
4. Relay stdout to user as-is — already formatted for humans.
   The output includes a browser link at the end (e.g. `https://aiusd.ai/chat/<session-id>`).
   Always include this link when relaying the response — it lets browser-login users
   continue the conversation in the web UI.
5. If response asks for confirmation or more info, relay to user,
   then `send` their reply back (same session, same pattern).
6. Run commands sequentially — only one active `send` per session.
7. Short commands (`session reset`, `cancel`, `login`) can run foreground
   (no `background:true` needed).
