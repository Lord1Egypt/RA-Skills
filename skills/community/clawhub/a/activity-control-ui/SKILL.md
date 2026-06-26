---
name: activity-control-ui
description: 🎨 Anime-style real-time activity dashboard with virtual avatar for OpenClaw. Displays current agent activities, session status, token usage, and ongoing tasks in a beautiful web UI. Gives your agent a visual body!
---

# Activity Control UI - 动漫风格实时控制面板

给你的 OpenClaw Agent 一个可视化身体！动漫风格渐变背景 + Q 版虚拟头像，实时显示 Agent 正在做什么。

## ✨ Features

- **🎨 Anime style UI**: Gradient starry background with floating particles, full anime aesthetic
- **👧 Virtual avatar**: Inline SVG chibi character with blinking animation and breathing glow
- **💬 Live speech bubble**: Shows what the agent is doing right now, updates in real-time
- **📊 Context meter**: Beautiful visual indicator for context window usage with color gradient
- **📜 Real-time activity feed**: Historical log of all activities
- **✅ Task tracking**: Lists current ongoing tasks with status
- **⚡ Auto-refresh**: Automatically updates status every 30 seconds
- **🎯 Quick actions**: One-click refresh / compact context

## What it does

This skill provides a local web server with:
1.  **Visual dashboard** - See at a glance what the agent is working on
2.  **Avatar with personality** - Cute chibi style that blinks and breathes
3.  **Context monitoring** - Color-coded progress bar warns you before hitting the limit
4.  **Real-time updates** - WebSocket pushes new activities instantly
5.  **Trigger maintenance** - Compact context directly from the UI

## Screenshot

![Anime-style dashboard with avatar](https://...coming-soon...)

## Usage

### Start the dashboard

```bash
cd activity-control-ui && npm install
node scripts/start-server.js [port]
```

Default port: 8080 → open http://localhost:8080

### Requirements

- Node.js with `ws` package (installed automatically with `npm install`)

## API

- `GET /api/status` - Get current session status JSON
- `WS /ws/activity` - Real-time activity stream
- Use `node scripts/broadcast.js "message" [type]` to broadcast new activities from the agent

## Author

Created with ❤️ by rudagebil11-jpg

## Resources

- `assets/control-ui.html` - Main dashboard HTML with inline SVG avatar
- `scripts/start-server.js` - HTTP + WebSocket server
- `scripts/broadcast.js` - CLI tool for broadcasting activities
