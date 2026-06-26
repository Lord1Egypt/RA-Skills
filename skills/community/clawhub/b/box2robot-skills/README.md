# Box2Robot Skills CLI

Standalone single-file CLI for controlling Box2Robot robotic arms. Talks directly to the server HTTP API — no monorepo dependency required.

## Install

### Via ClawHub (recommended for AI agents)
```bash
claw install box2robot
```

### Manual
```bash
pip install aiohttp
```

## Quick Start

```bash
# Login (token saved to ~/.b2r_token)
python b2r.py login <username> <password>

# List devices
python b2r.py devices

# Control
python b2r.py home                    # Go to home position
python b2r.py move 1 2048             # Move servo #1 to position 2048
python b2r.py move 1 2048 500         # With speed
python b2r.py torque off              # Release torque
python b2r.py status                  # Servo positions/load/temp
python b2r.py snapshot                # Camera snapshot
python b2r.py calibrate               # Auto-calibrate all servos
```

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `login [user] [pass]` | Login and save token | `b2r.py login user pass` |
| `devices` | List all devices | `b2r.py devices` |
| `status [device_id]` | Servo status | `b2r.py status` |
| `move <id> <pos> [speed]` | Move a servo | `b2r.py move 1 2048 500` |
| `home` | Go to home position | `b2r.py home` |
| `torque on/off` | Toggle torque | `b2r.py torque off` |
| `record start/stop [name]` | Recording control | `b2r.py record start` |
| `play [traj_id]` | Play trajectory (no args = list) | `b2r.py play` |
| `snapshot [cam_id]` | Camera snapshot | `b2r.py snapshot` |
| `calibrate [servo_id]` | Auto-calibrate (0 = all) | `b2r.py calibrate` |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `B2R_SERVER` | Server URL | `https://robot.box2ai.com` |
| `B2R_TOKEN` | JWT token (overrides ~/.b2r_token) | — |
| `B2R_DEVICE` | Default device ID (overrides auto-select) | — |

## Authentication & Credential Storage

```
login → POST /api/auth/login → JWT token → ~/.b2r_token (JSON)
```

- **`~/.b2r_token`** stores `{ "token": "...", "server": "...", "device": "..." }`.
- Created with owner-only permissions (0600).
- Subsequent commands read this file automatically — no repeated login.
- Override with `B2R_TOKEN` env var. Delete file to revoke.

> **Security note:** The token grants device control access. Treat it like an SSH key.

## API Endpoints Used

| Command | Method | Endpoint |
|---------|--------|----------|
| login | POST | `/api/auth/login` |
| devices | GET | `/api/devices` |
| status | GET | `/api/device/{id}/servos` |
| move | POST | `/api/device/{id}/command` |
| home | POST | `/api/device/{id}/go_home` |
| torque | POST | `/api/device/{id}/torque` |
| record | POST/GET | `/api/device/{id}/record/start\|stop\|status` |
| play | GET/POST | `/api/device/{id}/trajectories`, `.../trajectory/{id}/play` |
| snapshot | POST | `/api/camera/{id}/snapshot` |
| calibrate | POST | `/api/device/{id}/calibrate` |

## Documentation

- `SKILLS.md` — AI Agent reference manual (for Claude / GPT / other LLMs)
