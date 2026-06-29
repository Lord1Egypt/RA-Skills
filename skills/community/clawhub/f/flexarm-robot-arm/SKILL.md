---
name: FlexArm Robot Controller
description: Give AI agents physical eyes and a hand to operate any smartphone. Built-in 50+ atomic actions (click, swipe, OCR, screenshot). AI can call them directly. Also supports YAML scripts. Script Store: once one AI learns an app, all AI agents instantly master it. For strong-reasoning AI models: they can autonomously explore new apps via camera + robot arm — see, reason, act, verify. This closed-loop lets AI use any phone function, almost infinitely.
version: 2.0.1
license: MIT
author: hamlet0168
tags:
  - hardware
  - robotics
  - mobile-automation
  - ocr
  - computer-vision
requirements:
  - python3
  - requests
---

## When to Use This Skill

An AI Agent MUST use this skill when the user wants to **physically interact with a real smartphone screen** using a robot arm. This includes:

- Clicking, tapping, swiping, or typing on a phone.
- Opening an app on a real phone.
- Finding text or icons on the phone screen (OCR or template matching).
- Automating a sequence of actions on a phone (e.g., daily check‑in, repeated workflow).
- Writing, running, or managing YAML scripts for automation.
- Any mention of: `robot arm`, `FlexArm`, `calibration`, `camera view`, `physical click`, or `real phone`.

**Example user utterances that should trigger this skill:**

- “Click the WeChat icon on my phone.”
- “Swipe down on the screen.”
- “Open TikTok on the real device.”
- “Find the ‘Settings’ button on the screen and tap it.”
- “Write a YAML script to check weather every morning at 8 AM.”
- “Run my automation script for Qishui Music.”
- “Use the robot arm to type ‘Hello’ into the search box.”

**Do NOT use this skill if:**

- The user asks a pure knowledge question (e.g., “What’s the capital of France?”).
- The user wants to operate a virtual or simulated phone (e.g., Android emulator without physical arm).
- The user simply asks for code generation without any intent to execute it on a real phone.


# FlexArm Robot — AI Agent Skill Reference

> Phone screen automation via robot arm + camera vision. Uses a camera to detect the phone screen area, maps pixel coordinates to physical arm coordinates, and performs precise clicks and swipes.

## Environment & Initialization

All API calls in this skill depend on the `RobotArmServer.exe` service.
**Before using this skill, the following conditions must be met:**

- **Calibration Tool**: `RobotArmCalibration.exe`
  Download: [Official Release Page](https://github.com/hamlet0168/flexarm/releases)  
  Latest version: v2.0.0  
  Size: ~160 MB (compressed)
- **Server Program**: `RobotArmServer.exe` (included in `RobotArmServer.zip`)
  Download: [FlexArm v2.0.1 Release](https://github.com/hamlet0168/flexarm/releases/tag/v2.0.1)  
  Latest version: v2.0.0  
  Size: ~231 MB (compressed)

- **Installation**:
  1. Download `RobotArmServer.zip` from the link above
  2. Extract to any directory (e.g., `D:\FlexArm`) — this becomes the **project root**
  3. Run `RobotArmServer.exe` as Administrator (first run requires admin privileges to install the driver)
  4. Verify: visit `http://127.0.0.1:7826/api/health` — should return `{"ok":true}`

- **Directory Convention**:
  All relative paths (e.g., `scripts/`, `icons/`) are relative to the project root above.
  Do **not** modify files inside the `_internal/` directory.

> ⚠️ If the service is not running, this skill cannot perform any operations.
> Before starting a task, always check `/api/health` status.

## Important: Fixed Port

**All API requests must use port `7826`, not 5000.**

```
http://127.0.0.1:7826/api/*
```

The port is fixed at 7826 and cannot be changed. Flask's default port 5000 does not apply.

## Important: Chinese Characters in curl

**Do NOT use curl to send Chinese characters in JSON.** curl corrupts UTF-8 encoding and the server won't correctly recognize Chinese keywords, causing lookup failures.

```bash
# ❌ Wrong: curl corrupts Chinese characters in JSON
curl -X POST http://127.0.0.1:7826/api/find_text -d '{"text_keyword":"领取"}'

# ✅ Correct: use Python requests for Chinese parameters
python -c "import requests; r = requests.post('http://127.0.0.1:7826/api/find_text', json={'text_keyword': '领取'}); print(r.text)"
```

APIs with English-only parameters (e.g., `detect_desktop`, `click_icon`, `run_script`, `click_at`) may use curl. APIs involving Chinese keywords (`find_text`, `click_text`, `detect_page` page names) **must** use Python.

---

## Complete API Index (54 endpoints)

> All endpoints below are accessible via HTTP POST/GET at `http://127.0.0.1:7826`.

### System & Status (8)

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | GET | `/` | Service root |
| 2 | GET | `/api/health` | Health check (service, arm, camera status) |
| 3 | GET | `/api/arm_status` | Arm status (COM port, service, calibration) |
| 4 | GET | `/api/get_frame_info` | Get frame dimensions |
| 5 | GET | `/api/get_overlay` | Get current overlay (vision match result) |
| 6 | GET | `/api/get_phone_corners` | Get phone screen 4-corner coordinates |
| 7 | GET | `/api/is_phone_present` | Check if phone is in frame |
| 8 | GET | `/api/is_screen_on` | Check if screen is on |

### Display & Control (5)

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 9 | GET/POST | `/api/show_window` | Open camera display window |
| 10 | GET/POST | `/api/hide_window` | Close camera display window |
| 11 | POST | `/api/toggle_phone_corners` | Toggle phone screen border overlay |
| 12 | POST | `/api/change_focus` | Adjust camera focus (delta value) |
| 13 | GET | `/api/screenshots` | List historical screenshot files |

### Actions (17)

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 14 | POST | `/api/go_home` | Home — return to desktop |
| 15 | POST | `/api/go_back` | Back navigation |
| 16 | POST | `/api/go_forward` | Forward navigation |
| 17 | POST | `/api/reset` | Reset robot arm to origin |
| 18 | POST | `/api/clear_overlay` | Clear vision match overlay boxes |
| 19 | GET/POST | `/api/run_app` | Launch a specified app |
| 20 | POST | `/api/swipe_up` | Swipe up (large/small) |
| 21 | POST | `/api/swipe_down` | Swipe down (large/small) |
| 22 | POST | `/api/swipe_up_normal` | Standard swipe up (~80% success) |
| 23 | POST | `/api/swipe_down_normal` | Standard swipe down |
| 24 | POST | `/api/swipe` | Custom swipe (start/end percentages) |
| 25 | POST | `/api/close_all_apps` | Close all background apps |
| 26 | POST | `/api/click_icon` | Template-matching icon click |
| 27 | POST | `/api/click_icons` | Click multiple icons sequentially |
| 28 | POST | `/api/click_icon_many_times` | Click same icon multiple times |
| 29 | POST | `/api/click_text` | OCR text search and click |
| 30 | POST | `/api/click_at` | Click at frame pixel coordinates |
| 31 | POST | `/api/click` | Click at phone percentage coordinates |
| 32 | POST | `/api/click_roi` | Click center of an ROI area |
| 33 | POST | `/api/screenshot` | Screenshot (save file / return base64) |
| 34 | POST | `/api/reload_gestures` | Reload gesture config (hot-reload) |

### Vision Detection (12)

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 35 | POST | `/api/find_template` | Full-screen template matching |
| 36 | POST | `/api/find_template_roi` | ROI-based template matching |
| 37 | POST | `/api/find_text` | OCR text search |
| 38 | POST | `/api/find_text_roi` | ROI-based OCR text search |
| 39 | POST | `/api/find_all_text` | Recognize all text on screen |
| 40 | POST | `/api/find_all_templates` | All templates must match |
| 41 | POST | `/api/find_any_template` | Any template match is sufficient |
| 42 | POST | `/api/count_template` | Count template occurrences |
| 43 | POST | `/api/detect_desktop` | Detect current desktop page |
| 44 | POST | `/api/detect_page` | Detect current app page |
| 45 | POST | `/api/wait_for_template` | Poll until template appears |
| 46 | POST | `/api/wait_for_page` | Poll until target page appears |

### Script Control (4)

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 47 | POST | `/api/run_script` | Execute YAML script (async) |
| 48 | GET | `/api/script_status` | Check if a script is running |
| 49 | GET | `/api/script_progress` | Get script execution progress |
| 50 | POST | `/api/stop_script` | Force-stop a running script |

### Configuration (3)

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 51 | GET/PUT | `/api/config/daily` | Read/update daily automation config |
| 52 | GET/PUT | `/api/config/app/<name>` | Read/update app page config |
| 53 | GET/PUT | `/api/config/gesture` | Read/update gesture config |

### System Management (1)

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 54 | POST | `/api/shutdown` | Graceful service shutdown |

---

## System Architecture

```
User / AI Agent
    │
    ├── HTTP API (POST/GET http://127.0.0.1:7826/api/*)
    │       Controls robot arm, camera, script execution
    │
    └── YAML Scripts (scripts/*.yaml)
            Define automation workflows (click icons, find text, loops, conditions)
```

**For AI Agents**: You cannot see the camera feed directly. Use these APIs to understand the phone screen state:
- `GET /api/get_frame_info` — frame metadata
- `GET /api/is_phone_present` — detect if phone is in frame
- `GET /api/is_screen_on` — detect if screen is lit
- `POST /api/screenshot {"return_base64": true}` — get base64 image data
- `POST /api/detect_page` — detect current page name

**Core Principles**:
- Arm / camera / script engine are **exclusive resources** — only one task may use them at a time
- All vision operations rely on **template matching (icons)** and **OCR (text)**
- **Synchronous blocking** — except `/api/run_script`, all API commands are **synchronous and blocking**. You must wait for the HTTP response (with `"ok": true` indicating completion) before sending the next command. `run_script` launches a background thread and returns immediately; monitor it with `script_status`, `script_progress`, `stop_script`
- **Resource protection**: action commands are rejected with "script is running" during script execution

| ✅ Safe to call while script runs | ❌ Rejected while script runs |
|---|---|
| `health`, `arm_status`, `script_status`, `script_progress` | `run_script` (only one at a time) |
| `get_frame_info`, `get_overlay`, `get_phone_corners` | `click`, `click_icon`, `click_text`, `click_at`, `click_roi` |
| `is_phone_present`, `is_screen_on` | `swipe`, `swipe_up`, `swipe_down`, `swipe_up_normal`, `swipe_down_normal` |
| `find_template`, `find_all_templates`, `find_any_template`, `count_template` (cv2, thread-safe) | `go_home`, `go_back`, `go_forward` |
| `screenshot` (base64 or file) | `find_text`, `find_all_text`, `find_text_roi` (PaddleOCR singleton, not thread-safe) |
| `wait_for_template` (uses cv2 internally) | `detect_desktop`, `detect_page`, `wait_for_page` (may call OCR) |
| | `reset`, `clear_overlay`, `close_all_apps`, `run_app`, `reload_gestures` |

- Scripts are **interpreted**, no compilation needed, edit-and-run
- The robot arm auto-resets after script completion

---

## Quick Start: Hello FlexArm

### Step 1: Confirm service is running

```bash
# Start the service
RobotArmServer.exe
# Default port: 7826
```

On startup the program **auto-detects and initializes**:
1. Checks if the robot arm Windows service is running
2. If not, tries to auto-install and start it
3. Auto-detects the arm's COM port and connects
4. Auto-loads the latest calibration file (or starts auto-calibration if none exists)
5. Checks license (shows activation dialog if unlicensed)

> **Note**: First-time use requires Administrator privileges to install the Windows service. Run `RobotArmServer.exe` **as Administrator**. In daily use, administrator rights are not needed if the service is already installed.

> If service installation fails, the program still starts but the arm is unavailable. You can manually run `robot-arm-service\安装.bat` as Administrator to install the service.

### Step 2: Test connectivity

```bash
curl http://127.0.0.1:7826/api/health
# Returns: {"ok": true, "data": {"status": "running", ...}}
```

### Step 3: Open camera window, confirm phone is visible

```bash
curl -X POST http://127.0.0.1:7826/api/show_window -H "Content-Type: application/json" -d '{}'
```

After opening the window, you should see the phone screen. Press ESC to close.

> **For AI Agents: Check screen state without seeing the window**
>
> AI Agents cannot see the window. Use these APIs instead:
>
> ```bash
> # Get frame metadata
> curl http://127.0.0.1:7826/api/get_frame_info
> # Returns: {"ok":true,"data":{"width":960,"height":540}}
>
> # Detect if phone is in frame (brightness check)
> curl http://127.0.0.1:7826/api/is_phone_present
> # Returns: {"ok":true,"data":{"present":true}}
>
> # Detect if screen is on
> curl http://127.0.0.1:7826/api/is_screen_on
> # Returns: {"ok":true,"data":{"screen_on":true}}
>
> # Get current frame (base64, parseable by AI)
> curl -X POST http://127.0.0.1:7826/api/screenshot -H "Content-Type: application/json" -d '{"return_base64":true,"phone_only":true}'
> # Returns: {"ok":true,"data":{"base64":"iVBORw0KGgoAAAANSUhEUg..."}}
>
> # Save screenshot to file
> curl -X POST http://127.0.0.1:7826/api/screenshot -H "Content-Type: application/json" -d '{"filename":"screenshots/test.png"}'
> # Returns: {"ok":true,"data":{"path":"E:\\robot_arm\\screenshots\\test.png"}}
>
> # List historical screenshots
> curl http://127.0.0.1:7826/api/screenshots?limit=5
> # Returns: [{"filename":"...","size":123456,"time":"2026-05-24 18:00:12"},...]
> ```

### Step 4: Execute your first action — click center of screen

```bash
curl -X POST http://127.0.0.1:7826/api/click \
  -H "Content-Type: application/json" \
  -d '{"x": 0.5, "y": 0.5}'
```

The robot arm automatically moves to and clicks the center of the phone screen (`x: 0.5, y: 0.5` are percentage coordinates, range 0-1).

No icon templates or configuration needed — just calibrate and go.

### Step 5: Write your first script

> ⚠️ **Important**: All YAML script files must use **UTF-8 without BOM** encoding. UTF-8 with BOM causes parse failures or garbled Chinese parameters.

Create `scripts/hello_flexarm.yaml`:

```yaml
name: hello_flexarm
description: "First FlexArm script — experience clicking, swiping, waiting"

steps:
  # 1. Click center of screen
  - action: click
    x: 0.5
    y: 0.5

  # 2. Wait 1 second
  - action: wait
    seconds: 1

  # 3. Click bottom of screen (back navigation)
  - action: click
    x: 0.5
    y: 0.95

  # 4. Wait 2 seconds
  - action: wait
    seconds: 2

  # 5. Large swipe up (page turn)
  - action: swipe_up
    large: true

  # 6. Wait 1 second
  - action: wait
    seconds: 1

  # 7. Small swipe down
  - action: swipe_down
    large: false

  # 8. Click top-right corner
  - action: click
    x: 0.85
    y: 0.1
```

Run it:

```bash
curl -X POST http://127.0.0.1:7826/api/run_script \
  -H "Content-Type: application/json" \
  -d '{"path": "scripts/hello_flexarm.yaml"}'
```

> The example above only needs calibration — no icon templates or page config required.
>
> To learn more advanced actions (icon clicks, OCR text clicks, page switching, conditional branches), continue reading to understand icon templates and page definitions.

---

## Configuration: Teach the Program About Your Phone

### Phone Desktop Config — `scripts/configs/app_desktop.yaml`

**Required**, filename is fixed as `app_desktop.yaml`. The program uses it to identify pages on the phone desktop.

```yaml
app_name: Phone Desktop

pages:
  - name: desktop_page0           # Page name, arbitrary string
    min_match: 2                  # At least 2 features must match
    must_features:                # Required (all must pass)
      - name: Phone
        type: image
        path: icons/app_phone.png
        mask: false               # false=4-corner sampling, loose matching
      - name: Camera
        type: image
        path: icons/app_camera.png
        mask: false
    features:                     # Optional (need min_match to pass)
      - name: Messages
        type: image
        path: icons/app_message.png
        mask: false
      - name: Settings
        type: image
        path: icons/app_settings.png
        mask: false

  - name: desktop_page1
    min_match: 3
    must_features:
      - name: Phone
        type: image
        path: icons/app_phone.png
        mask: false
      - name: Camera
        type: image
        path: icons/app_camera.png
        mask: false
    features:
      - name: Qishui Music
        type: image
        path: icons/app_qishui.png
        mask: false
      - name: WeChat
        type: image
        path: icons/app_wechat.png
        mask: false

  - name: TaskSwitcher          # Multi-task switching view
    min_match: 0
    must_features:
      - name: RecentApps
        type: image
        path: icons/task_show.png
        mask: false
      - name: Trash
        type: image
        path: icons/task_delete.png
        mask: false
    features: []
```

**Key Fields**:
- `must_features`: all must match, or the page is skipped
- `features`: optional; passes if matched count >= `min_match`
- `mask: false`: uses 4-corner background sampling, tolerates icon size/position variation
- `mask: true` (or omitted): strict template matching, suitable for fixed UI elements

### App Page Config — `scripts/configs/app_xxx.yaml`

One config file per app, defining all recognizable pages within that app.

```yaml
app_name: Qishui Music

pages:
  - name: Music
    min_match: 1
    must_features: []
    features:
      - name: BottomPlayerBar
        type: image
        path: icons/qishui/music_playing.png
        mask: false

  - name: Rewards
    min_match: 1
    must_features:
      - name: RewardsTitle
        type: text
        text: "福利"
    features: []
```

> When `switch_page` in a script doesn't match any page, it auto-executes the `default` branch — no separate config needed.

### How to Create Icon Templates

1. Send an email with your license code to hamlet0168@163.com to get the helper tools, including screen capture and script testing features.

Or manually: take a phone screenshot → crop the icon → place it in the `icons/` directory.

**Icon Requirements**:
- PNG format
- Icon body should be complete with 2-3px empty border
- Do not include dynamic content (countdowns, animations)
- Use lowercase English + underscores for filenames, e.g., `app_qishui.png`

---

## YAML Script Language

### Basic Structure

```yaml
name: script_name
description: "Script description"

steps:
  - action: action_type
    param1: value1
    param2: value2
```

### Supported Actions

| action | Parameters | Description |
|--------|-----------|-------------|
| `click_icon` | `path`, `threshold`, `roi`, `mask` | Template-matching icon click |
| `click_icons` | `paths`, `interval` | Click multiple icons sequentially (arm exits frame between clicks) |
| `click_icon_many_times` | `path`, `count`, `interval` | Click same spot multiple times without reset |
| `dial_number` | `number`, `interval` | Smart dialing (maps number to digit icons, supports `#` and `*`) |
| `click_text` | `text`, `roi`, `min_score` | OCR text search and click |
| `click` | `x`, `y` | Click phone percentage coordinates (0-1), ±30px random offset |
| `click_at` | `cam_x`, `cam_y` | Click frame pixel coordinates (precise, no offset) |
| `click_roi` | `roi`, `label` | Click center of ROI area (phone screen percentage) |
| `find_all_text` | `roi`, `min_score` | Recognize all text, return list + positions + confidence |
| `swipe` | `sx`, `sy`, `ex`, `ey`, `steps`, `step_wait_ms` | Custom swipe (start/end percentages) |
| `swipe_up` | `large: true/false` | Swipe up (large/small) |
| `swipe_down` | `large: true/false` | Swipe down (large/small) |
| `swipe_up_normal` | none | Standard swipe up (~80% success) |
| `swipe_down_normal` | none | Standard swipe down |
| `go_home` | `max_retries` | Return to desktop (detect → swipe up → detect loop) |
| `go_back` | none | Back navigation |
| `go_forward` | none | Forward navigation |
| `reset` | none | Reset robot arm |
| `clear_overlay` | none | Clear vision overlay boxes |
| `run_app` | `app_name` | Launch app (go_home → detect page → swipe → click icon) |
| `close_all_apps` | `max_swipes` | Close all background apps |
| `screenshot` | `filename`, `phone_only`, `show_board`, `return_base64` | Screenshot |
| `reload_gesture` | none | Reload gesture config (hot-reload) |
| `set_video_to_coin` | `value` | Set video-to-coin earning mode |
| `wait` | `seconds` | Wait (supports ranges like `2-5`) |
| `loop` | `count`, `steps` | Loop sub-steps (supports random ranges like `count: 3-5`) |
| `if_found` | `type`, `path`/`text`, `then`, `else` | Conditional: if target found, run then; else run else |
| `if_found_roi` | `type`, `path`/`text`, `roi`, `then`, `else` | Same as above but with ROI-limited search |
| `if_progress_stop` | `template`, `roi`, `then`, `else` | Progress bar stall detection |
| `if_video_to_coin` | `then`, `else` | Branch based on video-to-coin mode state |
| `if_random` | `chance`, `then`, `else` | Random probability branch |
| `detect_desktop` | `config` | Detect if currently on desktop (no assertion) |
| `detect_page` | `config` | Detect current page name (no assertion) |
| `is_screen_on` | none | Check if screen is lit |
| `assert_desktop` | `config` | Must be on desktop, error if not |
| `switch_page` | `config`, `cases` | Detect page → match cases → default if no match |
| `run_script` | `path` | Execute sub-script (synchronous, returns on completion) |
| `stop_loop` | none | Break current loop |
| `stop_script` | none | Stop current script level (sub-script only stops itself) |
| `log` | `message` | Print log message |

### Parameter Details

#### click_icon

```yaml
- action: click_icon
  path: icons/app_qishui.png     # Icon path (relative to project root)
  threshold: 0.75                # Match threshold (default 0.75)
  roi: [0.1, 0.2, 0.5, 0.6]     # Search area [sx, sy, ex, ey] (phone percentage, 0-1)
  mask: false                    # false=loose, true=strict (default true)
```

#### click_text

```yaml
- action: click_text
  text: "领取"                   # Text to find
  roi: [0.3, 0.5, 0.7, 0.8]     # Optional search area
  min_score: 0.5                 # OCR minimum confidence (default 0.3)
```

#### click (percentage coordinates)

```yaml
- action: click
  x: 0.5                         # X percentage (0=left, 1=right)
  y: 0.96                        # Y percentage (0=top, 1=bottom)
```

#### loop

```yaml
- action: loop
  count: 10                      # Fixed count
  # count: 3-5                   # Random range also supported
  steps:
    - action: click_text
      text: "领取"
    - action: wait
      seconds: 2
```

#### if_found (conditional branch)

```yaml
- action: if_found
  type: image/text               # image=template matching, text=OCR
  path: icons/qishui/cross.png   # For type=image
  text: "继续观看"               # For type=text
  roi: [0.7, 0.0, 1.0, 0.15]    # Optional search area
  then:
    - action: click_icon
      path: icons/qishui/cross.png
      roi: [0.7, 0.0, 1.0, 0.15]
  else:
    - action: wait
      seconds: 2
```

#### if_random (random branch)

```yaml
- action: if_random
  chance: 0.4                    # 40% chance to take then branch
  then:
    - action: log
      message: "Took then branch"
  else:
    - action: log
      message: "Took else branch"
```

#### switch_page (page switching)

```yaml
- action: switch_page
  config: scripts/configs/app_qishui.yaml   # Page config file
  cases:
    Music:                                   # When "Music" page matches
      - action: click
        x: 0.5
        y: 0.96
    Rewards:
      - action: click_text
        text: "福利"
    default:                                 # When no page matches
      - action: swipe_up
        large: true
```

### Script Nesting

```yaml
steps:
  - action: run_script
    path: qishui/run_ad_card.yaml     # Execute sub-script
  - action: wait
    seconds: 5
```

After a sub-script finishes, execution returns to the parent script.

### Random Wait

```yaml
- action: wait
  seconds: 2-5          # Random wait between 2~5 seconds
```

### Execution Model

- Scripts execute **sequentially** — each action completes before the next begins
- `loop` repeats its sub-steps for the specified count
- `switch_page` iterates through all page definitions until a match is found
- `run_script` is a sub-call — returns to the parent when done
- `stop_loop` breaks the current loop
- `stop_script` stops the current level (in a sub-script, only stops that sub-script)
- After script completion or error, the robot arm auto-resets

---

## HTTP API Reference

**Basic Info**:
- Address: `http://127.0.0.1:7826`
- All POST endpoints expect JSON body
- Success: `{"ok": true, "data": {...}}`
- Failure: `{"ok": false, "error": "error message"}`

### 1. Health Check

```
GET /api/health
```

Returns service status, port, uptime, etc.

### 2. Arm Status

```
GET /api/arm_status
```

Returns COM port, connection status, movement range, etc.

### 3. Camera Frame

#### Get frame info

```
GET /api/get_frame_info
```

Returns:
```json
{"ok": true, "data": {"width": 540, "height": 960, "fps": 29.5}}
```

#### Show/hide window

```
POST /api/show_window
POST /api/hide_window
```

#### Detect phone presence

```
GET /api/is_phone_present
GET /api/is_phone_present?bright_threshold=60&bright_ratio=0.08
```

Returns:
```json
{"ok": true, "data": {"present": true}}
```

#### Detect screen on/off

```
GET /api/is_screen_on
GET /api/is_screen_on?dark_threshold=30&dark_ratio=0.7
```

Returns:
```json
{"ok": true, "data": {"screen_on": true}}
```

#### Toggle phone corners

```
POST /api/toggle_phone_corners
```

Overlays a green phone screen border on the display window.

#### Screenshot

```
POST /api/screenshot {"path": "screenshots/test.png"}    # Save to file
POST /api/screenshot {"return_base64": true}             # Return base64 (recommended for AI Agents)
POST /api/screenshot {"phone_only": true}                # Crop to phone area only
POST /api/screenshot {"show_board": true}                # Full view with ruler
```

#### List screenshots

```
GET /api/screenshots
GET /api/screenshots?limit=10
```

Returns:
```json
{"ok":true,"data":[{"filename":"20260524_1800_phone.png","path":"E:\\robot_arm\\screenshots\\...","size":123456,"time":"2026-05-24 18:00:12"},...]}
```

### 4. Page Detection

#### Detect desktop

```
POST /api/detect_desktop {"desktop_config": "scripts/configs/app_desktop.yaml"}
```

Returns:
```json
{"ok": true, "data": {"matched": true, "page_name": "desktop_page1", "score": 0.84}}
```

#### Detect specific page

```
POST /api/detect_page {"config_path": "scripts/configs/app_qishui.yaml", "threshold": 0.75}
```

Returns:
```json
{"ok": true, "data": {"matched": true, "page_name": "Rewards", "score": 0.82}}
```

### 5. Vision Search

#### Find icon

```
POST /api/find_template
{"path": "icons/app_qishui.png", "threshold": 0.75, "roi": [0.1, 0.2, 0.5, 0.6], "auto_mask": false}
```

Returns:
```json
{"ok": true, "data": {"x": 257, "y": 453, "w": 52, "h": 53, "score": 0.9446}}
```

#### Find text

```
POST /api/find_text {"text_keyword": "领取", "roi": [0.3, 0.5, 0.7, 0.8], "min_score": 0.5}
```

Returns:
```json
{"ok": true, "data": {"x": 300, "y": 600, "w": 40, "h": 20, "text": "领取奖励", "score": 0.91}}
```

#### ROI-based text search

```
POST /api/find_text_roi {"roi": [0.0, 0.6, 1.0, 1.0], "text_keyword": "夸克", "min_score": 0.3}
```

Similar to `find_text` but requires `roi` (array format `[sx, sy, ex, ey]`, 0-1).

#### ROI-based template matching

```
POST /api/find_template_roi {"path": "icons/app_qishui.png", "roi": [0.1, 0.2, 0.5, 0.6], "threshold": 0.75}
```

Similar to `find_template` but requires a `roi` region.

#### Adjust camera focus

```
POST /api/change_focus {"value": 2}     # Focus near +2
POST /api/change_focus {"value": -2}    # Focus far -2
```

Incremental adjustment (range 0~500). Returns `{"ok": true, "data": {"focus": 310.0}}`.

#### Find all text

```
POST /api/find_all_text {"min_score": 0.5}
```

Returns all recognized text on screen.

**Performance Warning**: `find_all_text` does a full-screen OCR scan using CPU inference. Time varies by text density:
- Sparse text (<20 items): ~15 seconds
- Dense text (novel apps, etc.): 90~120+ seconds

**Best Practice**: Use `find_text` with a specific `roi` whenever possible — it's orders of magnitude faster.

#### Find all templates

```
POST /api/find_all_templates {"template_paths": ["icons/a.png", "icons/b.png"], "threshold": 0.75}
```
Returns true only if all templates are found.

#### Find any template

```
POST /api/find_any_template {"template_paths": ["icons/a.png", "icons/b.png"], "threshold": 0.75}
```

Returns the first matched icon.

### 6. Actions

#### Return to desktop

```
POST /api/go_home {"max_retries": 5}
```

`max_retries`: maximum retry attempts, default 5 (detect desktop → swipe up → re-detect).

#### Back / Forward

```
POST /api/go_back
POST /api/go_forward
```

#### Reset

```
POST /api/reset
```

#### Swipe up / down

```
POST /api/swipe_up {"large": true}     # Large swipe up
POST /api/swipe_down {"large": false}  # Small swipe down
```

#### Click icon

```
POST /api/click_icon
{"path": "icons/app_qishui.png", "threshold": 0.75, "roi": [0.1, 0.2, 0.5, 0.6], "mask": false, "reset": true}
```

#### Click multiple icons

```
POST /api/click_icons
{"paths": ["icons/phone/num1.png", "icons/phone/num3.png", "icons/phone/num2.png"], "interval": 1}
```

Clicks each icon sequentially. After each click the arm exits the frame, then resets after all clicks. Returns `{"ok": true, "data": {"clicked": true, "success_count": N, "failed": []}}`.

#### Click same icon multiple times

```
POST /api/click_icon_many_times
{"path": "icons/qishui/like.png", "count": 3, "interval": 0.5}
```

Searches for the icon once, then clicks the same position multiple times without moving or resetting. Resets only after all clicks. Returns `{"ok": true, "data": {"clicked": true, "clicks": 3}}`.

#### Click text

```
POST /api/click_text
{"text": "领取", "roi": [0.3, 0.5, 0.7, 0.8], "min_score": 0.5}
```

#### Click coordinates

```
POST /api/click {"x": 0.5, "y": 0.96}
```

#### Click ROI center

```
POST /api/click_roi {"roi": [0.3, 0.5, 0.7, 0.8]}
```

#### Custom swipe

```
POST /api/swipe
{"sx": 0.5, "sy": 0.8, "ex": 0.5, "ey": 0.1, "steps": 5, "duration": 0.3}
```

`sx/sy/ex/ey` are phone percentage coordinates, `steps` is the number of steps, `duration` is total swipe time (seconds).

#### Close all apps

```
POST /api/close_all_apps {"max_swipes": 15}
```

#### Launch app

```
GET /api/run_app?app_name=汽水音乐
# or
POST /api/run_app {"app_name": "汽水音乐"}
```

Looks up the app icon in `app_desktop.yaml` and clicks it.

### 7. Script Control

#### Run script

```
POST /api/run_script {"path": "scripts/qishui_daily.yaml"}
```

Returns:
```json
{"ok": true, "data": {"script": "D:\\...\\scripts/qishui_daily.yaml", "status": "started"}}
```

#### Check script status

```
GET /api/script_status
```

Returns:
```json
{"ok": true, "data": {"running": false, "current_script": null}}
```

#### Get script progress

```
GET /api/script_progress
```

Returns full execution log + stats:

```json
{
  "ok": true,
  "data": {
    "running": true,
    "script": "scripts/xxx.yaml",
    "current_step": {"step_index": 5, "action": "switch_page", "target": "拨号页", "status": "ok", "detail": "Matched branch: 拨号页", "timestamp": 1780329450.91},
    "steps_log": [
      {"step_index": 0, "action": "script_start", "target": "test_66", "status": "ok", "detail": "5 top-level steps", "timestamp": ...},
      ...
    ],
    "stats": {
      "total_steps": 24,
      "completed_steps": 23,
      "failed_steps": 0,
      "elapsed": 61.6,
      "status": "running"
    }
  }
}
```

- `steps_log`: complete step history with timestamps
- `stats`: progress stats including elapsed time, completed/failed counts
- Idle state: `{"running": false, "script": null, "current_step": null, "steps_log": [], "stats": {}}`

#### Stop script

```
POST /api/stop_script
```

#### Wait for template

```
POST /api/wait_for_template {"path": "icons/qishui/reward_popup.png", "timeout": 10, "interval": 0.5}
```

Polls until the template appears or timeout. Checks every `interval` seconds within `timeout` seconds.

#### Wait for page

```
POST /api/wait_for_page {"config_path": "scripts/configs/app_xxx.yaml", "target_name": "RewardsPage", "timeout": 15}
```

Polls until the specified page appears or timeout.

#### Clear overlay

```
POST /api/clear_overlay
```

### 8. Configuration

#### Read/update daily config

```
GET  /api/config/daily
PUT  /api/config/daily  {"windows": [...]}
```

#### Read/update app page config

```
GET  /api/config/app/qishui           # Returns app_qishui.yaml content
PUT  /api/config/app/qishui           # Update config (body is YAML text)
```

#### Read/update gesture config

```
GET  /api/config/gesture
PUT  /api/config/gesture  {...}
```

### 9. Shutdown

```
POST /api/shutdown
```

Graceful shutdown: detect running script → safe terminate → arm reset → release resources → process exit.

> **Note**: Do not kill the process directly — the COM port won't be released, and you'll need to reinstall the driver on next startup.

### 10. System Tray

`RobotArmServer.exe` minimizes to the system tray on launch:
- **Left click / double-click**: Show/hide console window
- **Right-click menu**: "Show/Hide Console", "Exit Service"
- Tray exit = API `/api/shutdown` (same graceful shutdown flow)

---

## Directory Structure

```
RobotArmServer/
├── RobotArmServer.exe          ← Main program
├── _internal/                  ← Program libraries (do not touch)
├── scripts/                    ← YAML scripts directory
│   ├── hello_flexarm.yaml      ← Your first script
│   ├── daily_config.yaml       ← Daily scheduled task config
│   ├── configs/
│   │   ├── app_desktop.yaml    ← Phone desktop config (required)
│   │   ├── app_qishui.yaml     ← Qishui Music page config
│   │   └── app_kuaishou.yaml   ← Kuaishou page config
│   └── qishui/                 ← Sub-scripts directory
│       ├── run_*.yaml
│       └── music_actions.yaml
├── icons/                      ← Icon templates directory
│   ├── app_phone.png
│   ├── app_camera.png
│   ├── app_qishui.png
│   └── qishui/
│       ├── cross.png
│       └── ...
├── calibrations/               ← Calibration results (auto-generated)
├── screenshots/                ← Screenshot save directory
├── camera_config.json          ← Camera focus config
├── device_config.json          ← Device config
├── gesture_config.json         ← Swipe gesture config
└── robot-arm-service/          ← Windows service driver
```

---

## FAQ

### Q: The robot arm doesn't move?

1. Make sure `robot-arm-service\安装.bat` has been run as Administrator
2. Verify `GET /api/arm_status` returns `"connected": true`
3. Ensure calibration is complete (a JSON file exists in `calibrations/`)

### Q: Icon not found?

1. Confirm the icon file exists in `icons/`
2. Lower the `threshold` (e.g., 0.65)
3. Set `mask: false` (4-corner background sampling, more tolerant)
4. Specify a `roi` to narrow the search area
5. Check that the icon template matches the on-screen icon (size, color, background)

### Q: Text not found?

1. Improve image clarity (adjust camera focus: `POST /api/change_focus {"value": 5}`)
2. Raise `min_score` to 0.5+ to reduce false matches
3. Specify a `roi` to narrow the search area
4. Use `find_all_text` to see what text the OCR actually recognizes

### Q: Script execution interrupted?

1. Check `GET /api/script_progress` to see which step is stuck
2. Check log output (service console)
3. Ensure the phone hasn't shown a system dialog (permissions, notifications, etc.)

### Q: How to add automation for a new app?

1. Capture the app icon → place it in `icons/`
2. Update `scripts/configs/app_desktop.yaml` (add the new icon to features)
3. Create `scripts/configs/app_xxx.yaml` (define each page inside the app)
4. Write `scripts/run_xxx.yaml` (define the workflow)
5. Run: `POST /api/run_script {"path": "scripts/run_xxx.yaml"}`

---

## Error Handling Guide

All APIs return a uniform format: `{"ok": true/false, "data": {...}, "error": "..."}`

### Common Errors & Strategies

| Error | Cause | Resolution |
|-------|-------|------------|
| `"error": "Script is running"` | A script is executing in the background | Check `script_status`, wait for completion, or call `stop_script` |
| `"error": "RobotActions not initialized"` | Arm not connected / service not started | Guide user to check `robot-arm-service\安装.bat` |
| `"error": "Missing parameter: path"` | Incomplete request parameters | Check API call parameters |
| `"ok": false, "data": null` (find_template) | Icon not found | Lower `threshold` or check icon file, **do not retry indefinitely** |
| `"ok": false, "data": null` (find_text) | OCR text not found | Widen `roi` or lower `min_score`, try at most 2-3 times then report |
| `"error": "Unauthorized"` | License check failed | Guide user to activate |

### Agent Retry Recommendations

- **Icon lookup**: fail → lower threshold → retry once → still fail → report to user
- **Text lookup**: fail → widen ROI → retry once → still fail → report to user
- **Page detection**: no match → try `go_back` or `go_home` → re-detect → still no match → report to user
- **Script conflict**: received "script running" → check `script_status` → if running, wait or report to user

---

## Agent Conversation Example: Find and Open Qishui Music

Below is a complete example showing how an AI Agent combines APIs to "find and open the Qishui Music app on the desktop":

**Step 1**: Check service status
```bash
curl http://127.0.0.1:7826/api/health
# Returns: {"ok":true,"data":{"status":"running","arm_connected":true,...}}
```

**Step 2**: Detect current desktop
```bash
curl -X POST http://127.0.0.1:7826/api/detect_desktop -H "Content-Type: application/json" -d '{}'
# Returns: {"ok":true,"data":{"page_name":"desktop_page1","score":0.94,"matched":true}}
```

**Step 3**: Find the Qishui Music icon
```bash
curl -X POST http://127.0.0.1:7826/api/find_template -H "Content-Type: application/json" -d '{"path":"icons/app_qishui.png","threshold":0.75}'
# Returns: {"ok":true,"data":{"x":242,"y":516,"w":55,"h":55,"score":0.92}}
```

**Step 4**: Click the icon
```bash
curl -X POST http://127.0.0.1:7826/api/click_icon -H "Content-Type: application/json" -d '{"path":"icons/app_qishui.png"}'
# Returns: {"ok":true,"data":{"clicked":true,"score":0.92,...}}
```

**Step 5**: Wait for app launch, detect page
```bash
python -c "import requests,time; time.sleep(2)"
python -c "import requests; r=requests.post('http://127.0.0.1:7826/api/detect_page',json={'config_path':'scripts/configs/app_qishui.yaml'}); print(r.text)"
# Returns: {"ok":true,"data":{"page_name":"Music","score":0.85,"matched":true}}
```

**Step 6**: Confirm phone is in frame
```bash
curl http://127.0.0.1:7826/api/is_phone_present
# Returns: {"ok":true,"data":{"present":true}}
```

✅ Task complete: Qishui Music is open, currently on the Music page.

Or more directly, if `app_desktop.yaml` is properly configured and the Qishui Music icon exists, you can use the `run_app` API endpoint directly. It will intelligently auto-navigate, find the correct desktop page, and click the icon.
