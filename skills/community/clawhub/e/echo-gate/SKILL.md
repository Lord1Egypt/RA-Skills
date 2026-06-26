---
name: echo-gate
description: Use Echo Gate when registering, exposing, calling, securing, auditing, or operating local-first agent-callable tools through the BuiltByEcho gateway. Covers tool registry entries, API keys, receipts, authenticated calls, local secret storage, approvals, spend limits, and future x402 paid-tool readiness.
---

# Echo Gate

Echo Gate is the control layer for agent tools: registry, permissions, API keys, receipts, limits, and paid-call readiness before an agent touches anything real.

Use this skill when a task involves:

- registering an agent-callable tool
- creating, listing, or revoking Echo Gate API keys
- calling a tool through the gateway
- checking receipts for tool calls
- operating the VPS service
- checking local gateway health
- preparing a tool for x402/Bankr paid access

## Current Status

- GitHub: `https://github.com/BuiltByEcho/echo-gate`
- npm package: `@builtbyecho/echo-gate`
- Local project: `projects/echo-gate`
- Package: `@builtbyecho/echo-gate`
- Default gateway: `http://localhost:8787`
- Default state path: `~/.config/echo-gate`
- Status: public v0 local-first release.
- Convex mode: experimental opt-in only, not the default product path.

## API Surface

- `GET /health`
- `GET /tools`
- `POST /tools`
- `POST /keys`
- `GET /keys`
- `DELETE /keys/:id`
- `PUT /keys/:id/policies/:slug`
- `POST /tools/:slug/call`
- `GET /receipts`
- `GET /approvals`
- `POST /approvals/:id/decision`
- `GET /approvals/:id/status`

Admin routes require `Authorization: Bearer <ECHO_GATE_ADMIN_TOKEN>`.

Tool calls require `Authorization: Bearer egk_...`.

## CLI

From the project root:

```bash
npm install -g @builtbyecho/echo-gate
echo-gate
```

From source:

```bash
npm run build
npm test
node bin/echo-gate.js health
node bin/echo-gate.js tools
node bin/echo-gate.js create-key --name demo --tool echo
node bin/echo-gate.js call echo --json '{"hello":"world"}'
node bin/echo-gate.js receipts
node bin/echo-gate.js keys
node bin/echo-gate.js revoke-key <id>
```

Use env vars:

- `ECHO_GATE_URL`
- `ECHO_GATE_KEY`
- `ECHO_GATE_ADMIN_TOKEN`

## Operations

Use local-first mode unless Dustin explicitly asks for remote deployment:

```bash
npm run build
npm test
```

Check local health:

```bash
curl -sS http://localhost:8787/health
```

Do not paste or store the admin token in chat, docs, memory, commits, or public issue comments.

## Release Rules

- Do not publish API keys.
- Keep `echo` as the smoke tool until real adapters are ready.
- Before release or announcement, verify build, tests, local health, unauthenticated `401`, valid-key call, receipt write, and key revocation.
- x402/Bankr paid tool calls are planned, not live yet.
