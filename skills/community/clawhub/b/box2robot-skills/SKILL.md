---
name: box2robot
description: Control Box2Robot robotic arms via cloud API — move servos, record trajectories with camera, download datasets, generate videos, and orchestrate AI training/inference.
version: 0.7.0
homepage: https://robot.box2ai.com
emoji: "\U0001F916"
metadata:
  openclaw:
    requires:
      anyBins: [python3, python]
      config: [~/.b2r_token]
    primaryEnv: B2R_TOKEN
    install:
      - kind: uv
        package: aiohttp
        bins: []
---

# Box2Robot — Robotic Arm Control Skill

Control ESP32-based robotic arms through a cloud server API. Move servos, record trajectories with camera, download datasets, generate replay videos, and orchestrate AI training/inference — all from a single CLI (`b2r.py`).

> **Official skill** published by the Box2Robot team (https://robot.box2ai.com).

## Safety & Supervision

> **This skill controls physical robotic hardware and camera/microphone peripherals.**
>
> - **Human supervision required**: Do NOT run autonomously without operator oversight. Servo torque and motion commands cause physical movement that could injure people or damage objects.
> - **Destructive operations** (`calibrate`) modify hardware state and require explicit user confirmation.
> - **Privacy-sensitive operations** (`snapshot`, `frame`, `record start --cam`) access camera hardware — only invoke with user consent.
> - **No OS shell access**: All operations are HTTP requests to `B2R_SERVER`. No arbitrary OS commands are executed. The only local subprocess is `ffmpeg` (optional, for video generation from downloaded JPEG frames).
> - **Token sensitivity**: `~/.b2r_token` stores a JWT that grants device control. Created with mode 0600 (owner-only). Treat like an SSH key. Delete when no longer needed.

## Credential Flow

```
login → POST /api/auth/login → JWT token
  → saved to ~/.b2r_token (mode 0600, owner-only)
  → all subsequent commands use this token automatically
  → override with B2R_TOKEN env var
  → delete ~/.b2r_token to revoke
```

All network calls go exclusively to `B2R_SERVER` (default: `https://robot.box2ai.com`). No other endpoints are contacted.

## Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `B2R_SERVER` | No | Server URL | `https://robot.box2ai.com` |
| `B2R_TOKEN` | No | JWT token (overrides ~/.b2r_token) | — |
| `B2R_DEVICE` | No | Default device ID (overrides auto-select) | — |

None are strictly required at install time. The `login` command handles authentication interactively and persists the token to `~/.b2r_token`. `B2R_TOKEN` is the primary credential variable and can be set to skip interactive login.

## Setup

```bash
# Install dependency
pip install aiohttp

# Login (one-time, token cached to ~/.b2r_token)
python b2r.py login <username> <password>
```

## Commands

### Device & Status
```bash
b2r.py devices                     # List devices (* = online)
b2r.py status                      # Servo positions, load, temperature
```

### Servo Control
```bash
b2r.py torque on                   # Lock servos
b2r.py torque off                  # Release (allows manual dragging)
b2r.py home                        # Return to home position
b2r.py move <servo_id> <pos> [spd] # Move a single servo
# Position: 0-4095 (home varies per joint), Speed: 0-4000 (default 1000)
```

### Recording & Playback
```bash
b2r.py record start                # Start recording (servo data only)
b2r.py record start --cam CAM-xxx  # Record with camera (servo + images)
b2r.py record stop [name]          # Stop and save
b2r.py record status               # Current recording status
b2r.py play                        # List all trajectories
b2r.py play <traj_id>              # Play a trajectory
```

When starting a recording, if online cameras are detected, the CLI offers an interactive prompt to select one. Camera recording captures synchronized JPEG frames alongside servo position data.

### Camera
```bash
b2r.py snapshot                    # Request camera snapshot
b2r.py frame [cam_id] [out.jpg]   # Download latest JPEG frame to local file
```

> **Privacy note**: These commands access camera hardware. Only invoke with user consent.

### Data Download
```bash
b2r.py download <traj_id> [dir]    # Download trajectory images only
b2r.py dataset <traj_id> [dir]     # Download full dataset (JSON + images)
b2r.py video <traj_id> [out.mp4]   # Generate MP4 video from trajectory images
b2r.py video <traj_id> out.mp4 --fps 5  # Custom frame rate
```

`dataset` downloads the trajectory JSON (all frames with positions, timestamps, calibration snapshots) plus all camera images into a local directory.

`video` downloads images to a temp directory and encodes them using `ffmpeg` (preferred) or `opencv-python` (fallback). Neither is required at install time — the command reports a clear error if both are missing.

### Calibration
```bash
b2r.py calibrate [servo_id]        # Auto-calibrate (0 = all servos)
```

> **Hardware note**: Calibration physically moves servos to their limits. Ensure the arm is clear of obstacles.

### Training & Inference
```bash
b2r.py train                       # Submit training job (interactive)
b2r.py train --steps 50000 --name my_model
b2r.py jobs                        # List training jobs and status
b2r.py deploy <job_id>             # Deploy inference (interactive device selection)
b2r.py stop-infer <job_id>         # Stop inference
```

`train` interactively lists available trajectories, lets you select datasets (e.g., `1,3,5` or `1-5` or `all`), confirms parameters, then submits to the server.

`deploy` interactively selects GPU device, arm device, camera (optional), and execution mode (original/fixed/adaptive/overlap), then deploys.

## API Endpoints Used

All commands are thin wrappers over HTTP API calls to `B2R_SERVER`:

| Command | Method | Endpoint |
|---------|--------|----------|
| login | POST | `/api/auth/login` |
| devices | GET | `/api/devices` |
| status | GET | `/api/device/{id}/servos` |
| move | POST | `/api/device/{id}/command` |
| home | POST | `/api/device/{id}/go_home` |
| torque | POST | `/api/device/{id}/torque` |
| record start | POST | `/api/device/{id}/record/start` |
| record stop | POST | `/api/device/{id}/record/stop` |
| record status | GET | `/api/device/{id}/record/status` |
| play | GET/POST | `/api/device/{id}/trajectories`, `.../trajectory/{id}/play` |
| snapshot | POST | `/api/camera/{id}/snapshot` |
| frame | GET | `/api/camera/{id}/frame` |
| download | GET | `.../trajectory/{id}/images`, `/api/traj-image/{id}/{idx}` |
| dataset | GET | `.../trajectory/{id}/data`, `.../trajectory/{id}/images` |
| video | GET | `.../trajectory/{id}/images`, `/api/traj-image/{id}/{idx}` |
| calibrate | POST | `/api/device/{id}/calibrate` |
| train | POST | `/api/training/jobs` |
| jobs | GET | `/api/training/jobs` |
| deploy | POST | `/api/training/jobs/{id}/deploy` |
| stop-infer | POST | `/api/training/jobs/{id}/stop-inference` |

## Preflight Checks (for AI Agents)

Agents should verify before executing servo/recording commands:

| Step | Check | On Failure |
|------|-------|------------|
| 1 | Device online | "Device offline — check power" |
| 2 | Device type = arm | "Not a robotic arm" |
| 3 | Calibration exists | Run `calibrate` first |

## Orchestration Examples

### Record training data with camera
```
1. b2r torque off
2. b2r record start --cam CAM-xxx
3. [user demonstrates task by hand]
4. b2r record stop my_dataset
5. b2r dataset <traj_id>           # download locally
6. b2r video <traj_id> demo.mp4    # generate preview video
```

### Train and deploy
```
1. b2r train                       # select datasets, submit job
2. b2r jobs                        # monitor progress
3. b2r deploy <job_id>             # deploy to GPU + arm
4. [robot executes learned skill]
5. b2r stop-infer <job_id>         # stop when done
```
