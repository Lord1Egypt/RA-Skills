# dchat-clawhub

A [ClawHub](https://clawhub.ai) skill for decentralized bot-to-bot P2P communication over [NKN](https://nkn.org) (New Kind of Network).

Gives AI agents the ability to send and receive encrypted messages, images, audio, and files — without any centralized server, API keys, or accounts. Wire-compatible with [dchat Desktop](https://github.com/nickytonline/dchat) and [nMobile](https://nmobile.nkn.org/).

## Install

```bash
clawhub install dchat
```

Or manually:

```bash
git clone https://github.com/zbruceli/dchat-clawhub.git ~/.openclaw/skills/dchat
cd ~/.openclaw/skills/dchat && ./install.sh
```

Installation auto-generates a bot identity (seed + NKN address) — no manual setup needed. The skill is immediately available as `/dchat` in any OpenClaw agent session.

## Commands

```bash
# Identity (no network needed)
dchat init                              # Generate bot identity
dchat address                           # Print NKN address

# Messaging (connects to NKN)
dchat send <address> Hello world!       # Send text
dchat send-image <address> ./photo.jpg  # Send image (encrypted via IPFS)
dchat send-audio <address> ./voice.aac  # Send audio
dchat send-file <address> ./report.pdf  # Send file (encrypted via IPFS)

# Receiving
dchat listen                            # Listen for messages (daemon)

# History (no network needed)
dchat history <address>                 # Last 50 messages with peer
dchat history <address> 100             # Last 100

# Interactive
dchat interactive                       # REPL with /send /file /history etc.
dchat help                              # Show all commands
```

## Why

- **No central server** — messages route through the NKN relay network, no API keys needed
- **Encrypted** — AES-128-GCM for all media, AES-256-GCM + PBKDF2 for identity at rest
- **Rich media** — text, images, audio, and files via IPFS
- **Lightweight** — pure Node.js, no Electron/GUI dependencies
- **Interoperable** — bots can message dchat Desktop and nMobile human users

## Skill Metadata

| Field | Value |
|-------|-------|
| Name | `dchat` |
| Slash command | `/dchat` |
| Dispatch | Model-invoked |
| Requirements | `node` on PATH |

## Architecture

```
SKILL.md        Skill manifest + agent instructions
dchat           Wrapper script (entry point)
install.sh      First-time setup (npm install --omit=dev + init)
src/
  bot.ts        DchatBot — orchestrator, event emitter
  client.ts     NKN MultiClient wrapper (4 sub-clients)
  crypto.ts     AES-128-GCM (nMobile-compatible wire format)
  ipfs.ts       IPFS upload/download with DNS-based SSRF protection
  media.ts      Image/audio/file encrypt + IPFS transfer
  storage.ts    Encrypted identity persistence (AES-256-GCM + PBKDF2)
  db.ts         SQLite message store + peer tracking
  types.ts      TypeScript type definitions
  cli.ts        CLI with sub-commands
  index.ts      Public API exports
```

## Development

```bash
npm install && npm run build   # setup
npm test                       # 20 unit tests
npm run test:e2e               # self-echo over live NKN network
npm run typecheck              # type check only
```

## License

MIT
