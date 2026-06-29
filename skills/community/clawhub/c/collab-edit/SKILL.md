---
name: collab-edit
version: 1.0.6
description: Enable real-time collaboration by exposing a local collaborative editing tool via aitun tunnel. Perfect for AI agents that need to co-edit code, documents, or whiteboards with users in real time.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: AITUN_SERVER
        required: false
        description: "AiTun server address (default: aitun.cc:6639)"
    install:
      - kind: pip
        package: aitun
        bins: [aitun]
      - kind: uv
        package: aitun
        bins: [aitun]
    emoji: "✏️"
    homepage: https://aitun.cc
    clawhub: https://clawhub.ai/ctz168/collab-edit
---

# Collab Edit - Real-Time Collaboration via Aitun Tunnel

## When to Use

Use this skill when:
- You need to co-edit code, a document, or a configuration file with a user in real time
- You want to set up a shared whiteboard or drawing canvas accessible via browser
- You are pair-programming with a user and need a shared code editor
- You want to collaboratively draft content (markdown, notes, specifications) with live updates
- You need to review and annotate a document together with the user

Do NOT use this skill when:
- Only one person is editing (no collaboration needed)
- The content is finalized and just needs to be shared (use sendfile instead)
- You want to share a read-only preview (use aitun-tunnel or live-preview instead)

## Instructions

### Step 1: Install aitun

```bash
pip install aitun
```

Or install via one-line script (Linux/macOS):
```bash
curl -fsSL https://aitun.cc/install.sh | bash
```

Windows (PowerShell):
```powershell
irm https://aitun.cc/install.ps1 | iex
```

Or verify it is already installed:

```bash
which aitun
```

### Step 2: Start a collaborative editing server

Choose and start a collaboration tool. Here are common options:

```bash
# Option A: Code-server (VS Code in browser) for pair programming
# Install: curl -fsSL https://code-server.dev/install.sh | sh
code-server --bind-addr 0.0.0.0:8080 --auth none &
COLLAB_PID=$!

# Option B: Hedgedoc / Etherpad-like tool for document collaboration
# (install per project instructions, then start on port 8080)

# Option C: Simple shared notepad (Python)
pip install collaborative-notepad
collaborative-notepad --port 8080 &
COLLAB_PID=$!

# Option D: Whiteboard (excalidraw self-hosted or similar)
npx excalidraw-room --port 8080 &
COLLAB_PID=$!
```

### Step 3: Create a tunnel

Expose the collaboration server to the internet:

```bash
aitun -p 8080 &
AITUN_PID=$!
sleep 3
```

The output will contain the public URL, e.g.:
- `https://aitun.cc/abc123`

### Step 4: Share the collaboration link

Send the link to the user so they can join:

```
Let's work on this together! Open the shared editor:
https://aitun.cc/abc123

I can see your changes in real time, and you can see mine.
This session is active while we're working.
```

### Step 5: Collaborate in real time

- Edit content together — both you and the user see changes instantly
- Use the chat or comment features of the collaboration tool for discussion
- Take turns editing, or work on different sections simultaneously
- Save or export the final result when collaboration is complete

### Step 6: Clean up

When the collaboration session is over, stop the servers:

```bash
kill $AITUN_PID 2>/dev/null
kill $COLLAB_PID 2>/dev/null
```

## CLI Reference

The `aitun` command (installed via `pip install aitun`, or alternatively `curl -fsSL https://aitun.cc/install.sh | bash` / `irm https://aitun.cc/install.ps1 | iex` on Windows) accepts these flags:

| Flag | Description |
|---|---|
| `-p PORT` | Local HTTP service port (optional; omit for TCP-only mode with `--tcp-ports`) |
| `-k TOKEN` | Auth token for registered subdomain (omit for free tunnel) |
| `--host HOST` | Local service address (default: localhost) |
| `--tcp-ports PORTS` | TCP forwarding ports, comma-separated (e.g., `22,3306`; requires `-k`). Use without `-p` for TCP-only mode |
| `--p2p` | Enable P2P direct connection (default: enabled) |
| `--no-p2p` | Disable P2P, force server relay mode |
| `--daemon` | Run as background daemon |
| `--stop` | Stop running daemon |

## Notes

- Free tunnels use proxy address mode (path-based URL like `aitun.cc/abc123`), NOT subdomains
- Free tunnels expire after 24 hours, auto-renewed on restart
- For a permanent collaboration endpoint, register at https://aitun.cc to get a custom subdomain
- Collaboration tools that use WebSocket work well through the tunnel
- For security, consider enabling authentication on the collaboration tool itself (most support password or token auth)
- All traffic is encrypted end-to-end
- Multiple users can open the same link simultaneously for group collaboration
- Export or save the final document before stopping the tunnel
