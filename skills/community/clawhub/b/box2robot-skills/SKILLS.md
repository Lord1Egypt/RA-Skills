# Box2Robot Skills — AI Agent Reference Manual

> This document is for LLM Agents (Claude / GPT / CLAW etc.) to reference when orchestrating Box2Robot.
> Agents control the robotic arm via the `b2r.py` CLI or HTTP API.

---

## Authentication

```bash
# Login (one-time, token cached to ~/.b2r_token)
python b2r.py login <username> <password>

# Or set environment variables directly
export B2R_SERVER="https://robot.box2ai.com"
export B2R_TOKEN="<jwt_token>"
export B2R_DEVICE="B2R-XXXXXXXXXXXX"
```

Once logged in, all commands carry the token automatically — no repeated authentication needed.

---

## CLI Quick Reference

### Devices
```bash
b2r.py devices                     # List devices (* = online)
b2r.py status                      # Current servo positions and torque
```

### Servo Control
```bash
b2r.py torque on                   # Lock servos
b2r.py torque off                  # Release (allows manual dragging)
b2r.py home                        # Safe return to home position
b2r.py move <servo_id> <pos> [spd] # Move a single servo
# Position: 0-4095 (center 2048), Speed: 0-4000 (default 1000)
# 10 degrees ~ 114 counts
```

### Recording & Playback
```bash
b2r.py record start                # Start recording
b2r.py record stop [name]          # Stop recording
b2r.py record status               # Recording status
b2r.py play                        # List all trajectories
b2r.py play <traj_id>              # Play a trajectory
```

### Advanced
```bash
b2r.py exec <action> [params]      # Call any Action directly
b2r.py say "natural language"      # Natural language execution
b2r.py shell                       # Interactive shell
```

---

## Action System (79 Actions)

Invoke via `b2r.py exec <action_name>`. Parameters in JSON or key=value format.

### device (Device Management)
| Action | Description |
|--------|-------------|
| `device.list` | List devices |
| `device.status` | Device status (control mode + servos) |
| `device.bind` | Bind device (requires bind_code) |
| `device.unbind` | Unbind device |
| `device.rename` | Rename device |
| `device.wifi_add` | Add WiFi network |
| `device.wifi_clear` | Clear WiFi config |
| `device.factory_reset` | Factory reset |

### servo (Servo Control)
| Action | Parameters | Description |
|--------|------------|-------------|
| `servo.status` | device_id | Read position/load/temperature |
| `servo.move` | device_id, servo_id, position, [speed] | Move single servo |
| `servo.move_batch` | device_id, commands:[{id,position,speed}] | Batch move |
| `servo.torque` | device_id, enable:bool | Toggle torque |
| `servo.go_home` | device_id | Return to home position |
| `servo.release_control` | device_id | Release current control |
| `servo.control_mode` | device_id | Query control mode |
| `servo.set_id` | device_id, old_id, new_id | Burn servo ID |

### recording (Recording & Playback)
| Action | Parameters | Description |
|--------|------------|-------------|
| `record.start` | device_id, [mode], [camera_id] | Start recording (single/dual/phone) |
| `record.stop` | device_id, [name] | Stop recording |
| `record.status` | device_id | Recording status |
| `trajectory.list` | device_id | List trajectories |
| `trajectory.play` | device_id, trajectory_id | Play trajectory |
| `trajectory.stop` | device_id, trajectory_id | Stop playback |
| `trajectory.delete` | device_id, trajectory_id | Delete trajectory |
| `trajectory.images` | device_id, trajectory_id | Trajectory images |

### pairing (Leader-Follower Pairing)
| Action | Parameters | Description |
|--------|------------|-------------|
| `pairing.list` | — | List pairings |
| `pairing.create` | leader_id, follower_ids, [use_espnow] | Create pairing |
| `pairing.disconnect` | leader_id | Disconnect (keep record) |
| `pairing.connect` | leader_id | Reconnect |
| `pairing.delete` | leader_id | Delete pairing |
| `espnow.discover` | — | Scan nearby devices |
| `espnow.peers` | device_id | View neighbors |

### calibration (Calibration)
| Action | Parameters | Description |
|--------|------------|-------------|
| `calibrate.auto` | device_id, [servo_id=0] | Auto-calibrate (0 = all) |
| `calibrate.status` | device_id | Calibration progress |
| `calibrate.cancel` | device_id | Cancel calibration |
| `calibrate.manual` | device_id, servos:[{id,min,max,mid}] | Manual calibration |
| `calibrate.center_offset` | device_id | Write EEPROM center offset |

### camera (Camera & Voice)
| Action | Parameters | Description |
|--------|------------|-------------|
| `camera.status` | device_id | Camera status |
| `camera.snapshot` | device_id | Take photo |
| `camera.stream_mode` | device_id, mode | Stream mode (idle/preview/inference) |
| `camera.frame` | device_id | Get latest JPEG frame |
| `camera.voice_start` | device_id | Enable microphone |
| `camera.voice_stop` | device_id | Disable microphone |
| `camera.tts` | device_id, prompt | Text-to-speech |
| `camera.play_sound` | device_id, sound | Play sound effect |
| `camera.record_audio_start` | device_id | Start audio recording |
| `camera.record_audio_stop` | device_id | Stop audio recording |
| `camera.recordings` | device_id | List recordings |

### training (Training & Inference)
| Action | Parameters | Description |
|--------|------------|-------------|
| `training.submit` | name, dataset_ids, [model_type], [train_steps] | Submit training job |
| `training.list` | [page] | Job list |
| `training.status` | job_id | Training progress |
| `training.cancel` | job_id | Cancel job |
| `training.deploy` | job_id, arm_device_id, gpu_device_id | Deploy inference |
| `training.stop_inference` | job_id | Stop inference |
| `training.rate` | job_id, rating(1-5) | Rate result |

### store (Skill Store)
| Action | Parameters | Description |
|--------|------------|-------------|
| `store.list` | [search], [category] | Browse store |
| `store.execute` | task_id, device_id | Execute skill |
| `store.purchase` | task_id | Purchase |
| `store.favorite` | task_id | Favorite |
| `store.like` | task_id | Like |
| `store.rate` | task_id, rating(1-5) | Rate |

### config (Configuration & OTA)
| Action | Parameters | Description |
|--------|------------|-------------|
| `config.get` | device_id | View config |
| `config.set` | device_id, params:{key:val} | Update config |
| `config.speed` | device_id, speed(100-4000) | Set speed |
| `config.led_brightness` | device_id, brightness(0-255) | LED brightness |
| `config.volume` | device_id, volume(0-255) | Volume |
| `config.camera_resolution` | device_id, resolution | Resolution |
| `config.bluetooth` | device_id, enable:bool | Bluetooth toggle |
| `ota.check` | — | Check firmware update |
| `ota.update` | device_id | Push update |

---

## Natural Language Mapping

Via `b2r.py say "text"` or directly in the interactive shell:

| Input | Maps to |
|-------|---------|
| "go home" / "return home" | servo.go_home |
| "release torque" / "let go" | servo.torque(False) |
| "lock" / "hold" | servo.torque(True) |
| "start recording" / "teach me" | record.start |
| "stop recording" / "done recording" | record.stop |
| "take a photo" / "snapshot" | camera.snapshot |
| "open camera" | camera.stream_mode(preview) |
| "auto calibrate" | calibrate.auto |
| "louder" / "turn up volume" | config.volume(200) |
| "faster" / "speed up" | config.speed(2000) |
| "brighter" | config.led_brightness(200) |
| "move servo 1 to 2048" | servo.move(1, 2048) |
| "record 5 datasets" | workflow.batch_record(5) |
| "teach you to dance" | workflow.teach_single |

> Chinese natural language is also fully supported (e.g., "回零位", "释放力矩", "拍照").

---

## Preflight Checks

Agents must verify before executing actions:

| Step | Check | On Failure |
|------|-------|------------|
| 1 | Device online | "Device offline — check power" |
| 2 | Device type = arm | "Not a robotic arm" |
| 3 | Control mode = idle | release_control to free |
| 4 | Calibration data exists | calibrate.auto to calibrate |
| 5 | Servo count matches | Trajectory needs N axes vs device has M |
| 6 | Calibration range compatible | ratio < 0.5 = incompatible |
| 7 | Vision tasks: cam + gpu online | Report which device is missing |

---

## Typical Orchestration Scenarios

### Scenario 1: "Wave your hand"
```
1. say "wave" → search local trajectories / store
2. Found → preflight → trajectory.play or store.execute
3. Not found → suggest "You can record one: teach me to wave"
```

### Scenario 2: "Teach you to pour water, record 5 demos"
```
1. torque off                              # Release torque
2. camera.stream_mode(cam_id, "preview")   # Open camera
3. Loop 5 times:
   record.start(mode="single", camera_id)  # Record
   [user demonstrates]
   record.stop(name="pour_water_{n}")      # Save
4. training.submit(name="pour_water", dataset_ids)  # Submit training
```

### Scenario 3: Visual Inference Loop
```
1. training.deploy(job_id, arm_id, gpu_id, cam_id)
2. GPU Worker auto-loop: capture image → inference → send command → arm executes
3. training.stop_inference(job_id)  # Stop
```

---

## HTTP API Direct Access

You can also call the HTTP API directly without the CLI:

```bash
# Login
curl -X POST https://robot.box2ai.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"xxx","password":"xxx"}'
# → {"token": "eyJ..."}

# List devices
curl https://robot.box2ai.com/api/devices \
  -H "Authorization: Bearer <token>"

# Move servo
curl -X POST https://robot.box2ai.com/api/device/B2R-xxx/command \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"id":1,"position":2048,"speed":1000}'

# Go home
curl -X POST https://robot.box2ai.com/api/device/B2R-xxx/go_home \
  -H "Authorization: Bearer <token>"
```

Full endpoint list: see `box2robot_server/box2robot-cli/box2robot.md`

---

## LLM Conversational Control (chat.py)

Control the arm through natural language via Zhipu AI function calling — the LLM decides when to invoke APIs.

```bash
cd box2robot_audio

# Chat only
python chat.py

# Chat + arm control
python chat.py --robot

# First time: login required
python chat.py --robot --login <user> <password>

# Specify device
python chat.py --robot --device B2R-XXXXXXXXXXXX
```

### Available LLM Tools (9)

| Tool | Parameters | Description |
|------|------------|-------------|
| `list_devices` | — | List all devices with online status and type |
| `servo_status` | — | Current servo position/load/temp + torque state |
| `move_servo` | servo_id, position, [speed] | Move single servo (ID 1-6, pos 0-4095) |
| `go_home` | — | All servos return to calibrated center |
| `set_torque` | enable:bool | Torque on (lock) / off (release) |
| `record_start` | — | Start trajectory recording |
| `record_stop` | — | Stop recording and save |
| `list_trajectories` | — | List saved trajectories |
| `play_trajectory` | traj_id | Play trajectory by ID |
| `search_and_play` | keyword | Search by name and play (e.g., "nod", "wave") |

### API Feedback Format

Each tool returns structured feedback for the LLM to generate responses:

**Success** — prefixed with `OK:`:
```
OK: servo 1 moving to 2500 at speed 500. status=queued
OK: torque=ON, stale=False, age=353ms, 6 servos
  ID1: position=2494, load=36, temp=35
  ...
OK: Returning home in 15 steps (max_delta=342)
OK: Recording saved. id=abc123, frames=150, duration=5000ms
OK: 4 devices | active=B2R-XXXX
  White Follower | id=B2R-XXXX | type=arm | ONLINE
  Black Leader   | id=B2R-YYYY | type=arm | OFFLINE
```

**Failure** — prefixed with `ERROR:`:
```
ERROR: Device not connected              → Device offline, check power/WiFi
ERROR: No servo data (stale=True)        → Device just booted, retry in a few seconds
ERROR: Cannot disable torque while Virtual Serial is active → Close VSerial first
ERROR: Already recording                 → record_stop before starting new recording
ERROR: Not recording                     → No need to stop
ERROR: unauthorized                      → Token expired, re-login required
ERROR: No device selected                → Select a device first
ERROR: Invalid servo_id (0-253)          → Servo ID out of range
ERROR: Invalid position (0-4095)         → Position value out of range
ERROR: Trajectory not found              → Trajectory ID does not exist
ERROR: Cannot connect to server          → Network issue, check connection
ERROR: Request timeout                   → Server may be busy
```

### Multi-Device Handling

- On startup, the first online arm device is auto-selected
- If multiple arms are online, the user is prompted to choose
- Users can specify via `--device B2R-XXXX`, or say "switch to the black leader" in conversation
- `list_devices` output marks `active=` for the currently controlled device

### LLM Behavior Rules

1. **Before execution**: Confirm when user intent is ambiguous ("Which servo do you want to move?")
2. **After execution**: Generate response based on feedback (success → report result, failure → explain + suggest)
3. **Multi-step operations**: Recording requires releasing torque first (set_torque false → record_start)
4. **Safety**: Never proactively execute dangerous operations in conversation (factory_reset, calibrate, etc.)
5. **Small talk**: Conversations unrelated to the arm should not trigger any tool calls
