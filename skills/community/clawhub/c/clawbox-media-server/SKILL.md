---
name: clawbox-media-server
description: Bidirectional LAN file sharing for AI agents. Provides a static file server (port 18801) for serving files to users, and an upload server (port 18802) with drag-and-drop web UI for users to send files to the agent. All traffic stays on local network — no internet required. Use when channel lacks inline media support or when you need a simple, LAN-only file exchange layer.
---

# Clawbox Media Server & Upload

Lightweight HTTP servers for bidirectional file sharing between an AI agent and users on the local network.

## What It Does

- **Media Server (port 18801)** — Serves files from a shared directory. Users can browse and download.
- **Upload Server (port 18802)** — Accepts file uploads via web UI (drag-and-drop) or API. Saves to the same shared directory.
- **Same-origin design** — Upload page served from upload server to avoid CORS/Safari issues.
- **Directory listing** — Media server root shows all files with download links.
- **Auto-start services** — Systemd units for both servers (optional).

All files are stored in `~/projects/shared-media` and instantly accessible to the agent.

---

## Quick Start (One-Command)

From your login session (with systemd user bus):

```bash
bash ~/.openclaw/workspace/skills/clawbox-media-server/scripts/install-all.sh
```

That's it! The installer:
- Creates `~/projects/shared-media` if needed
- Starts both servers immediately
- Installs systemd service files for auto-start on boot

**Access URLs** (replace `192.168.68.75` with your host's LAN IP):
- Upload page: `http://192.168.68.75:18802/`
- File browser: `http://192.168.68.75:18801/`

---

## Manual Setup

If you prefer to start manually:

**1. Start Media Server** (serves files):
```bash
node ~/.openclaw/workspace/skills/clawbox-media-server/scripts/server.js
# Listens on 0.0.0.0:18801
```

**2. Start Upload Server** (accepts uploads):
```bash
UPLOAD_PORT=18802 python3 ~/.openclaw/workspace/skills/clawbox-media-server/scripts/upload-server.py
# Serves UI on / and upload endpoint at POST /upload
```

Both read from/write to `~/projects/shared-media` by default.

---

## Usage Patterns

### Agent → User (Serving Files)

Agent copies a file to the shared directory:
```bash
cp /path/to/output.pdf ~/projects/shared-media/
```

Then sends the user a link:
```
http://192.168.68.75:18801/output.pdf
```

The user can also browse all files at `http://192.168.68.75:18801/`.

---

### User → Agent (Uploading Files)

User opens `http://192.168.68.75:18802/` in any browser, drags files in. ✅ Done.

Agent sees the files immediately in `~/projects/shared-media/` and can read them.

---

### Combined Workflow

1. User uploads via `http://192.168.68.75:18802/`
2. Agent reads file from disk (`~/projects/shared-media/<filename>`)
3. Agent processes/transforms it
4. Agent drops result in same directory
5. User downloads from `http://192.168.68.75:18801/<result>`

Fully LAN-based, no internet.

---

## Configuration

### Ports & Paths

| Variable | Default | Purpose |
|----------|---------|---------|
| `MEDIA_PORT` | `18801` | Media server port |
| `UPLOAD_PORT` | `18802` | Upload server port |
| `MEDIA_ROOT` / `UPLOAD_ROOT` | `$HOME/projects/shared-media` | Shared storage directory |

Set as environment variables before starting the servers, or edit the systemd service files.

### Systemd Services

Service names:
- `media-server.service` — Node.js media server
- `upload-server.service` — Python upload server

Enable auto-start (run once from your login session):
```bash
systemctl --user enable media-server.service upload-server.service
```

Start/stop/restart/check status:
```bash
systemctl --user start|stop|restart|status media-server.service
systemctl --user start|stop|restart|status upload-server.service
```

---

## API (Upload Server)

**Endpoint:** `POST /upload` (multipart/form-data, field name `file`)

**Request:**
```bash
curl -X POST -F "file=@/path/to/file.jpg" http://192.168.68.75:18802/upload
```

**Response (JSON):**
```json
{
  "filename": "file.jpg",
  "size": 123456,
  "download_url": "http://192.168.68.75:18801/file.jpg",
  "view_url": "http://192.168.68.75:18801/file.jpg",
  "saved_to": "/home/clawbox/projects/shared-media/file.jpg"
}
```

The file is immediately available in the shared directory and via the media server.

---

## Security Notes

### ⚠️ IMPORTANT: Read Before Deploying

- **No authentication** — anyone who can reach the ports can upload/download files. Only use on physically secured, trusted networks. Do NOT expose to the internet without additional authentication/reverse proxy.
- **Binding address** — By default, servers bind to `0.0.0.0` (all interfaces). To restrict to a specific LAN interface, set `BIND_ADDR` environment variable to your LAN IP (e.g., `192.168.68.75`). Example:
  ```bash
  BIND_ADDR=192.168.68.75 MEDIA_PORT=18801 node server.js
  ```
- **Firewall recommended** — Even on LAN, consider blocking external interfaces (WAN) using a host firewall (`ufw`, `iptables`). Allow only your LAN subnet to ports 18801/18802.
- **Directory listing** — The media server root (`:18801/`) shows all filenames. This may leak information. If privacy is needed, disable directory listing by modifying `server.js` or block access via firewall.
- **Content Security** — The upload page uses inline JavaScript (CSP relaxed). This is acceptable for a local-only service, but be aware.
- **Systemd services** — If you enable systemd services, they run under your user account. Ensure your user account is secure. Consider using a dedicated low-privilege user for production.

### Best Practice: Manual Start for Testing

Before enabling systemd auto-start, run the servers manually to verify behavior:

```bash
# Terminal 1
cd ~/.openclaw/workspace/skills/clawbox-media-server/scripts
BIND_ADDR=192.168.68.75 node server.js

# Terminal 2
cd ~/.openclaw/workspace/skills/clawbox-media-server/scripts
BIND_ADDR=192.168.68.75 python3 upload-server.py
```

Then test upload/download from another device. Once satisfied, run `install-all.sh` to set up systemd services (with the same `BIND_ADDR` configured in the service files).

---

## Troubleshooting

### "Address already in use" on startup
A previous instance is still running. Stop it first:
```bash
pkill -f server.js
pkill -f upload-server.py
```

Or change ports via environment variables.

### Upload fails with CORS/Safari errors
The upload page is served from the same port as the upload endpoint (18802), so cross-origin issues shouldn't occur. Ensure you're accessing `http://<host>:18802/` and not the old media-server copy.

### Systemd user bus not available
Run `systemctl --user enable ...` from your normal login shell (not a cron or SSH non-interactive session without DBUS_SESSION_BUS_ADDRESS set). The `install-all.sh` script will start servers manually in any case.

---

## Files & Structure

```
skills/clawbox-media-server/
├── SKILL.md               (this file)
├── server.js              (media server)
├── upload-server.py       (upload server)
├── upload.html            (upload UI, served by upload server)
├── media-server.service   (systemd unit)
├── upload-server.service  (systemd unit)
└── install-all.sh         (one-click installer)
```

All files are self-contained; no external npm/pip dependencies beyond Node.js and Python stdlib.

---

## License

Open source. Feel free to modify and redistribute.
