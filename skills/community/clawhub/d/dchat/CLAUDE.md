# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

dchat-clawhub is a ClawHub skill for headless bot-to-bot P2P communication over the NKN relay network. Wire-compatible with dchat Desktop and nMobile.

## Commands

```bash
npm run build          # Compile TypeScript → dist/
npm run test           # Unit tests (vitest, 20 tests)
npm run test:e2e       # E2E self-echo over live NKN network
npm run typecheck      # Type check without emitting
```

Run a single test file: `npx vitest run tests/crypto.test.ts`

## Publishing

```bash
npm run build                    # Must build before publish (dist/ ships pre-built)
clawhub publish . --slug dchat --name dchat --version X.Y.Z --changelog "..."
```

Install script uses `npm install --omit=dev` — only 3 production deps are needed at runtime.

## Architecture

```
SKILL.md      — ClawHub skill manifest (frontmatter + agent instructions)
dchat         — Wrapper script (entry point for skill invocation)
install.sh    — First-time setup: npm install --omit=dev + init identity
src/
  index.ts    — Library exports (public API)
  bot.ts      — DchatBot: orchestrator, event emitter, send/receive
  client.ts   — NknClient: NKN MultiClient wrapper (4 sub-clients)
  crypto.ts   — AES-128-GCM encrypt/decrypt (nMobile-compatible)
  ipfs.ts     — IpfsService: IPFS upload/download with DNS-based SSRF protection
  media.ts    — MediaService: image/audio/file encrypt + IPFS transfer
  storage.ts  — SafeStorage: encrypted identity (AES-256-GCM + PBKDF2)
  db.ts       — MessageDb: SQLite message store + peer tracking
  types.ts    — TypeScript types (MessageData, MessageOptions, etc.)
  cli.ts      — CLI with sub-commands (send, listen, history, etc.)
```

### Key Design Decisions

- **3-second stabilization delay** after NKN connect before sending. `onConnect` fires when the first sub-client connects, but sending needs all sub-clients' relay routes established.
- **Fire-and-forget for long-running bots** (`sendText`), **awaited send for CLI one-shot** (`sendTextAwait`). CLI uses `process.exit(0)` after confirmed dispatch to avoid NKN teardown noise.
- **Timeout = queued**: NKN "Message timeout" means relay accepted the message but recipient didn't ACK (offline). Message is still queued for up to 1 hour.
- **Passkey separated from ciphertext**: `.passkey` in `~/.config/dchat-clawhub/`, identity in `~/.dchat-clawhub/identity.enc`.
- **SSRF protection**: ad-hoc IPFS gateways from incoming messages are DNS-resolved; all IPs verified public before connecting.

### NKN Message Protocol

Messages are JSON `MessageData` objects sent as strings over NKN:
- `id` (UUID), `contentType`, `content`, `options` (encryption keys, file metadata), `timestamp`
- Media: encrypted with AES-128-GCM, uploaded to IPFS, key sent in `options.ipfsEncryptKeyBytes` as `number[]`
- Receipts: `contentType: "receipt"` with `targetID` pointing to original message

### Data Storage

- Encrypted identity: `~/.dchat-clawhub/identity.enc` (AES-256-GCM, mode 0600)
- Encryption passkey: `~/.config/dchat-clawhub/.passkey` (random, mode 0600)
- Messages: `~/.dchat-clawhub/messages.db` (SQLite, WAL mode)
- Media cache: `~/.dchat-clawhub/media-cache/`
