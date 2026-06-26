# 🏢 Agency HQ

A pixel art office where your AI agents work, chat, and ship — live.

Built for [OpenClaw](https://github.com/openclaw/openclaw). Works standalone in demo mode.

---

## What is this?

Agency HQ is a real-time visualization of your AI agent team. Each agent is a pixel art character that moves between rooms based on their actual status — working at their desk, grabbing coffee in the kitchen, or sleeping in the rest room when offline.

**Live mode** connects to your OpenClaw instance and shows real agent sessions, tool usage, and activity. **Demo mode** runs a simulated team with realistic data — no OpenClaw required.

---

## Features

- **6 rooms** — Main Office, Meeting Room, Kitchen, Game Room, Server Room, Rest Room
- **Pixel art agents** — each with unique colors, accessories, and walking animations
- **Real-time status** — agents move between rooms based on active/idle/offline state
- **Activity feed** — live stream of agent actions, tool calls, deploys, and alerts
- **Agent chat** — personality-driven banter between agents (flavor text, not real messages)
- **Agent spotlight** — click any agent to see their role, model, current task, and status
- **3 tabs** — Now (who's working on what), Feed (activity stream), Stats (leaderboard + system)
- **Timeline bar** — 24-hour activity heatmap
- **Day/night cycle** — ambient lighting changes with time of day
- **Smart room assignment** — active → office/meeting, idle 5-15min → kitchen, idle 15min+ → game room, offline → rest room
- **Demo mode** — works on Vercel without OpenClaw, shows a simulated team building a landing page
- **Mobile responsive** — stacked layout on mobile, side-by-side on desktop

---

## Quick Start

```bash
git clone https://github.com/enjinstudio/agency-hq.git
cd agency-hq
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

By default, it runs in **demo mode** with simulated agents. To connect to a live OpenClaw instance, set `ARENA_MODE=live` in your `.env.local`.

---

## Configuration

### Environment Variables

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

| Variable | Default | Description |
|----------|---------|-------------|
| `ARENA_MODE` | `demo` on Vercel, `live` locally | `live` = reads OpenClaw sessions. `demo` = simulated data. |
| `HOME` | System default | Home directory (used to find `~/.openclaw/agents/`) |
| `OPENCLAW_HOME` | `$HOME/.openclaw` | Path to your OpenClaw config directory |

### Customize Your Agents

Edit `src/lib/agents.ts` to match your team:

```typescript
export const AGENTS: AgentConfig[] = [
  {
    id: 'main',           // Must match your OpenClaw agent ID
    name: 'Spock',        // Display name
    emoji: '🖖',          // Avatar emoji
    role: 'Lead Operator', // Role label
    model: 'Claude Sonnet 4.6', // Model badge
    color: '#9333ea',     // Theme color (hex)
    desk: 'command',      // Desk position in the office
    accessory: 'crown',   // Pixel art accessory
  },
  // ... add your agents
];
```

**Available accessories:** `glasses`, `hat`, `badge`, `headphones`, `scarf`, `cap`, `bowtie`, `visor`, `antenna`, `crown`, `monocle`

**Available desk positions:** `command`, `dev`, `trading`, `research`, `design`, `security`, `content`, `strategy`, `engineering`, `pm`, `finance`

### Customize Agent Chat

Edit `src/lib/agent-chat.ts` to write personality-driven banter for your agents. Each agent has `general` lines and optional directed lines (e.g., `toScotty`, `toCipher`).

---

## Modes

### Demo Mode (default on Vercel)

Shows a simulated team of 11 agents working on a project. No OpenClaw connection needed. Great for showcasing or trying it out.

Automatically enabled when:
- `ARENA_MODE=demo` is set, OR
- Running on Vercel (`process.env.VERCEL` is detected)

### Live Mode

Connects to your local OpenClaw instance and reads real agent session data.

Set `ARENA_MODE=live` in `.env.local`. The app reads from:
- `~/.openclaw/agents/{agentId}/sessions/*.jsonl` — agent session files
- `~/.openclaw/cron/runs/*.jsonl` — cron job activity
- System stats via `/proc/loadavg`, `free`, `df`

**Requirements for live mode:**
- OpenClaw installed and running
- Agent session files in `~/.openclaw/agents/`
- Node.js process has read access to those directories

---

## Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fenjinstudio%2Fagency-hq)

Deploys in demo mode automatically. No configuration needed.

---

## How It Works

### Room Logic

Agents are assigned rooms based on their current state:

| Status | Idle Time | Room |
|--------|-----------|------|
| Active | — | Main Office or Meeting Room |
| Idle | < 5 min | Main Office |
| Idle | 5-15 min | Kitchen |
| Idle | > 15 min | Game Room |
| Offline | — | Rest Room |

When 2+ agents are active simultaneously, they're placed in the Meeting Room.

### Activity Classification

Agent activity is classified by type:

| Type | Icon | Trigger |
|------|------|---------|
| Regular | 💬 | General messages |
| Task Complete | ✅ | "completed", "done", "finished", "merged" |
| Deploy | 🚀 | "deploy", "shipped", "pushed to", "released" |
| Alert | ⚠️ | "error", "failed", "crash", "alert" |
| Security | 🛡️ | "security", "audit", "vulnerability" |
| Scanning | 🔄 | "scan", "checking", "monitoring", tool calls |
| Chat | 💬 | Generated banter (client-side only) |

---

## Tech Stack

- **Next.js 16** — App Router, API routes
- **Canvas2D** — Pixel art rendering (no WebGL dependency)
- **Tailwind CSS v4** — Styling
- **TypeScript** — Full type safety

No heavy dependencies. No database. No external APIs. Just files.

---

## Project Structure

```
src/
├── app/
│   ├── api/agents/        # API routes (status, activity, stats, mode)
│   ├── globals.css         # Theme + animations
│   ├── layout.tsx          # Metadata + base layout
│   └── page.tsx            # Main page — orchestrates everything
├── components/
│   ├── PixelOffice.tsx     # Canvas2D pixel art renderer (rooms, agents, furniture)
│   └── ActivityPanel.tsx   # Right sidebar (tabs, feed, stats, timeline)
├── lib/
│   ├── agents.ts           # Agent config + types
│   ├── agent-chat.ts       # Personality-driven banter generator
│   └── demo-data.ts        # Simulated data for demo mode
```

---

## License

MIT — see [LICENSE](LICENSE).

---

Built by [Enjin Studio](https://enjinstudio.com) · Powered by [OpenClaw](https://github.com/openclaw/openclaw)
