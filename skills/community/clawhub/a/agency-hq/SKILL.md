---
name: agency-hq
description: A pixel art office visualization for your AI agent team. Shows real-time agent status, activity feeds, and personality-driven banter. Works with OpenClaw in live mode or standalone in demo mode.
version: 1.0.0
license: MIT
author: Enjin Studio
tags: [visualization, pixel-art, dashboard, agents, monitoring]
---

# Agency HQ — AI Agent Office

A real-time pixel art visualization of your AI agent team. Agents move between rooms (office, kitchen, game room, server room) based on their actual status. Includes a live activity feed, agent spotlight cards, and personality-driven chat.

## When to Use

- You want a visual dashboard showing what your agents are doing
- You want to showcase your agent team to others (demo mode)
- You want a fun, always-on display of your OpenClaw setup

## Setup

### 1. Clone and Install

```bash
git clone https://github.com/enjinstudio/agency-hq.git
cd agency-hq
npm install
```

### 2. Configure Mode

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Set `ARENA_MODE=live` to connect to your OpenClaw instance, or leave as `demo` for simulated data.

### 3. Customize Your Agents

Edit `src/lib/agents.ts`. Each agent needs:

| Field | Description |
|-------|-------------|
| `id` | Must match your OpenClaw agent ID (e.g., `main`, `dev`, `research`) |
| `name` | Display name |
| `emoji` | Avatar emoji |
| `role` | Role label shown in spotlight |
| `model` | Model name shown in spotlight |
| `color` | Hex color for theme and pixel art |
| `desk` | Desk position: `command`, `dev`, `trading`, `research`, `design`, `security`, `content`, `strategy`, `engineering`, `pm`, `finance` |
| `accessory` | Pixel art accessory: `glasses`, `hat`, `badge`, `headphones`, `scarf`, `cap`, `bowtie`, `visor`, `antenna`, `crown`, `monocle` |

### 4. Customize Chat Lines (Optional)

Edit `src/lib/agent-chat.ts` to write personality-driven banter. Each agent has:
- `general` — random lines said to the room
- `to{AgentName}` — directed lines at specific agents (30% chance)

### 5. Run

```bash
# Development
npm run dev

# Production
npm run build && npm start
```

### 6. Deploy to Vercel (Optional)

Push to GitHub and import in Vercel. Demo mode activates automatically on Vercel.

## How Live Mode Works

In live mode, the app reads from your OpenClaw directory:

- **Agent status** — scans `~/.openclaw/agents/{id}/sessions/*.jsonl` for recent activity
- **Activity feed** — extracts user messages and tool calls from session files
- **System stats** — reads `/proc/loadavg`, runs `free -m` and `df`
- **Room assignment** — active agents → office, idle → kitchen/game room, offline → rest room

No database. No external APIs. Just reads files from disk.

## Requirements

- Node.js 20+
- OpenClaw (for live mode only)
- npm

## Notes

- The chat system generates fun flavor text — it's not real agent communication
- Demo mode works everywhere, including Vercel, with zero configuration
- The pixel art renderer uses Canvas2D — no WebGL required, works in all browsers
- Mobile responsive — stacks vertically on small screens
