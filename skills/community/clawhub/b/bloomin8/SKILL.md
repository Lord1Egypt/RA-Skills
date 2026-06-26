---
name: bloomin8
description: Push images or markdown to a Bloomin8 e-ink photo frame via cloud API (async) or local BLE+LAN (instant). Scan nearby devices, check status, track delivery, change wake schedule, upload directly over WiFi.
version: 2.2.5
metadata: {"openclaw":{"homepage":"https://github.com/xander887/bloomin8-openclaw-skill","requires":{"env":["BLOOMIN8_TOKEN_*"],"bins":["python3","pip"],"pip":["bleak","aiohttp","pillow"]},"primaryEnvPrefix":"BLOOMIN8_TOKEN_","emoji":"🖼️"}}
---

## Bloomin8 E-ink Device Control

Control Bloomin8 e-ink photo frame devices. Two modes available:

- **Local BLE + LAN** (local, instant) — scan, wake, and upload directly over the local network; image displays immediately.
- **Cloud API** (remote, async) — push content via REST API; device displays on next scheduled wake.

**Image sourcing:** This skill handles delivery only. To create images, combine with any available tool — e.g. Puppeteer (HTML → screenshot), AI image generation, or scripted chart rendering — then pass the resulting file or URL to the push/upload commands below.

**Mode selection:** Prefer local mode when available, but always **confirm with the user before performing BLE scans or probing local network hosts**. Suggested flow:
1. Ask the user which mode they prefer (local or cloud), or propose one based on context.
2. If local mode: before scanning, inform the user (e.g. "I'll scan for nearby BLE devices — OK?"). Only proceed with explicit approval.
3. If you have a device IP (from prior `info`, cache, or user-provided), verify reachability (`curl http://<ip>/whistle`) before uploading. Inform the user of the IP being probed.
4. Only fall back to **cloud API** when local is impossible (no BLE hardware, device out of range, IP unreachable after BLE wake).
5. Explicit user intent overrides: "push" / "schedule" → cloud; "upload" / "display now" → local.

### Device Identity Across Modes

Both modes use the same device name as the primary identifier. When a user says a device name (e.g. "Living Room"):
- **Cloud API** → match to env var `BLOOMIN8_TOKEN_LIVING_ROOM` (uppercase, non-alphanumeric → `_`)
- **Local BLE** → match via `--name "Living Room"` (case-insensitive partial match)

The device name is set by the user in the Bloomin8 app and is consistent across BLE advertisement (`local_name`) and cloud (`device.name`). The BLE `info` command also returns the full device serial (`sn`) which matches the cloud `device_id` embedded in the API token — but in practice, name matching is sufficient and preferred.

---

## Mode 1: Cloud API (Remote, Async)

### Self-Discovery

On first use, fetch the full API documentation (no auth needed). Cache the result — it rarely changes:

```
web_fetch https://einkshot-349134901638.us-central1.run.app/open-api/help
```

This returns all endpoints, parameters, and response fields as structured JSON. If anything below conflicts with the live docs, trust the live docs.

### Authentication

Token is device-bound. Generated in the Bloomin8 app: **Devices tab → device card → ⋮ menu → API Token**.

- Env var naming: `BLOOMIN8_TOKEN_<DEVICE_NAME>` (uppercase, non-alphanumeric → `_`)
  - e.g. `BLOOMIN8_TOKEN_LIVING_ROOM`, `BLOOMIN8_TOKEN_KIDS_BEDROOM`
- When user mentions a device by name, match it to the corresponding env var
- If only one `BLOOMIN8_TOKEN_*` exists, **confirm with the user** before using it (e.g. "I found token BLOOMIN8_TOKEN_KITCHEN — shall I use it?")
- Pass as: `Authorization: Bearer $BLOOMIN8_TOKEN_<NAME>`
- Generating a new token invalidates the previous one for that device
- Token can be generated/revoked regardless of whether remote push is enabled

API base URL: `https://einkshot-349134901638.us-central1.run.app`

### Capabilities

- **GET /open-api/help** — full API docs (no auth)
- **GET /open-api/device/status** — screen dimensions, orientation, interval, pending status (includes `remote_image_on` and `pending_image.remote_image_id` when pending)
- **POST /open-api/push** — push image (URL / file upload / markdown). **Requires `remote_image_on = true`.** Last-wins: only the latest pending image will be displayed.
- **DELETE /open-api/push** — cancel the current pending image. **Requires `remote_image_on = true`.**
- **GET /open-api/push/history** — delivery history with status filter
- **PUT /open-api/device/interval** — change wake frequency (10m / 1h / 3h / 6h). **Requires `remote_image_on = true`.**

### Recommended Workflow

1. **GET /open-api/device/status** — get screen dimensions, orientation, and `estimated_push_time`. Always do this before pushing to know the target size.
2. **Prepare image** matching the device's width × height and orientation.
3. **POST /open-api/push** — push via one of the three modes (see examples below). Last-wins: only the latest push will be displayed.
4. **GET /open-api/push/history** — verify delivery. Status flow: `PENDING → PULLED → COMPLETED` (or `FAILED` / `CANCELLED`).
5. Optionally **DELETE /open-api/push** to cancel the pending image before the device wakes.
6. Optionally **PUT /open-api/device/interval** to change wake frequency. Takes effect after the **next** scheduled pull, not the upcoming one.

### Examples

**Query device status:**
```bash
curl https://einkshot-349134901638.us-central1.run.app/open-api/device/status \
  -H "Authorization: Bearer $BLOOMIN8_TOKEN_<NAME>"
```
Response: `{ "device": { "name", "width", "height", "orientation", "remote_image_interval", "has_pending", "estimated_push_time", ... } }`

**Push image via URL:**
```bash
curl -X POST https://einkshot-349134901638.us-central1.run.app/open-api/push \
  -H "Authorization: Bearer $BLOOMIN8_TOKEN_<NAME>" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/photo.jpg"}'
```
Response: `{ "remote_image_id": "ri_xyz789", "estimated_push_time": "2026-04-02T11:00:00Z" }`

**Push markdown content:**
```bash
curl -X POST https://einkshot-349134901638.us-central1.run.app/open-api/push \
  -H "Authorization: Bearer $BLOOMIN8_TOKEN_<NAME>" \
  -H "Content-Type: application/json" \
  -d '{"content_type": "markdown", "content": "# Hello World\nToday is a great day.", "theme": "minimal"}'
```
Themes: `minimal` (default), `dark`, `paper`. Server auto-renders markdown to an image matching the device screen size. **Note:** Markdown-to-image rendering is a cloud-side feature. Local BLE+LAN mode uploads raw images only — if you need to display markdown content via local mode, render it to an image yourself first (e.g. Puppeteer HTML → screenshot).

### Key Concepts

1. **Push ≠ instant display.** The e-ink device sleeps to save power and wakes on a schedule (10m / 1h / 3h / 6h). The pushed image displays on the **next wake**. The `estimated_push_time` field tells you when.
2. **Last-wins** — the device only displays the most recently pushed image. If you push multiple times before the device wakes, earlier images are skipped.
3. **Interval changes are delayed** — only affect the wake **after the next one**, since the on-device alarm is already set.
4. **Markdown rendering** — the server auto-renders markdown to an image matching the device screen size. See layout rules below to estimate content fit.

### Markdown Rendering Rules

Content that exceeds the screen is **clipped** — no scrolling or pagination. Use the formula below to estimate capacity for any screen size.

**Scaling formula:**
```
scale = min(width / 375, height / 812)
All base values below are multiplied by this scale factor.
```

**Base values (before scaling):**

| Element | Base Font | Line Height | Base Vertical Cost |
|---------|-----------|-------------|--------------------|
| Body text | 18 | ×1.7 | 30.6 + 16 margin |
| h1 | 40 (bold) | ×1.3 | 52 + 24 top + 16 bottom |
| h2 | 36 (semibold) | ×1.3 | 46.8 + 24 top + 10 bottom |
| h3 | 28 (semibold) | ×1.4 | 39.2 + 16 top + 10 bottom |
| Code block | 15 | ×1.5 | 22.5 per line + 40 padding |
| List item | 18 | ×1.6 | 28.8 + 6 gap |

**Container padding (base):** top/bottom = 50, left/right = 60

**Quick reference for common screens:**

| Screen | Scale | Content Area | Body Lines | CJK/Line | Latin/Line |
|--------|-------|-------------|------------|----------|------------|
| 480×800 | 0.985 | 362×702 | ~23 | ~18 | ~45 |
| 1200×1600 | 1.97 | 964×1403 | ~23 | ~27 | ~65 |

> Body line count is similar across sizes because font and screen scale proportionally. The main difference is characters per line.

**Capacity estimates (body text, any screen):**
- Content area: `(width - 120×scale) × (height - 100×scale)`
- Lines: `content_height / (30.6 × scale)`  → **~23 lines** for both common screens
- CJK chars/line: `content_width / (20 × scale)`
- Latin chars/line: `content_width / (8 × scale)`
- With an h1 title: subtract ~5 lines

**Practical guidelines:**
- Each heading costs 2–3 body lines of vertical space — use sparingly
- Code blocks cost extra due to padding — keep them short
- For long articles, split into multiple pushes or truncate to fit
- Supported: h1–h3, p, ul/ol, blockquote, code, table, hr, strong, em, strikethrough (GFM)
- Themes: `minimal` (white, default), `dark` (black), `paper` (cream/sepia)

### Error Handling

All errors return `{ "success": false, "error": "ERROR_CODE", "message": "..." }`.

- **401** — Missing or invalid Bearer token
- **403** — Remote push not enabled on device
- **400 invalid-argument** — Bad input: missing image, file >10MB, content >50KB, invalid interval, etc.

---

## Mode 2: Local BLE + LAN (Instant)

Control devices directly over Bluetooth and local WiFi. Images display **immediately** after upload — no waiting for the next wake cycle.

**Device image requirements:** The e-ink hardware only accepts **JPEG baseline** images whose dimensions **exactly match** the screen size (e.g. 480×800 or 1200×1600). The Bloomin8 CLI handles format conversion and resize automatically — but screen size must be known (via BLE `info`, cache, or explicit `--resize WxH`).

### Prerequisites

Requires Python 3 with BLE and HTTP libraries. Verify and install:

```bash
python3 -c "import bleak, aiohttp, PIL" 2>/dev/null || pip install bleak aiohttp pillow
```

| Package | Purpose |
|---------|---------|
| **bleak** | BLE scanning and device communication |
| **aiohttp** | HTTP image upload to device |
| **pillow** | Image resize/crop to fit screen |

> **Platform notes:**
> - **macOS** — Allow Terminal / your IDE in **System Settings → Privacy & Security → Bluetooth**
> - **Windows** — Requires Windows 10+ (native BLE support via WinRT)
> - **Linux** — Requires BlueZ 5.43+ and DBus (`sudo apt install bluez`); run with a user in the `bluetooth` group or use `sudo`

The CLI script is bundled at `scripts/bloomin8_cli.py` (the **Bloomin8 CLI**) relative to this skill file.

### Scan for Devices

Find nearby Bloomin8 devices via BLE advertisement:

```bash
python scripts/bloomin8_cli.py scan
python scripts/bloomin8_cli.py scan --timeout 15
python scripts/bloomin8_cli.py scan --json
```

Output is **deduplicated by device ID** — each device appears once with the strongest signal. Raw advertisement count is shown for reference (BLE devices broadcast repeatedly, so raw count >> actual device count).

**Battery display:** Only firmware ≥ 1.8.30 broadcasts battery level in BLE advertisements. Older devices will show "N/A". Battery is always available via the `info` command (which queries the device directly).

### Get Device Info

Query device details (IP, firmware, screen size, battery) via BLE wake + notification:

```bash
# By device name (partial match)
python scripts/bloomin8_cli.py info --name "Living Room"

# By device ID (from BLE manufacturer data)
python scripts/bloomin8_cli.py info --id "CABBF337"

# JSON output for programmatic use
python scripts/bloomin8_cli.py info --name "Living Room" --json
```

**Timing:** The `info` command takes ~20-30 seconds. It first sends a BLE wake command, waits 8 seconds for the device to boot its WiFi stack, then sends up to 5 `getInfo` requests (5s timeout each). This is normal — set user expectations accordingly.

**Caching:** Successful `info` results are cached to `~/.bloomin8/device_cache.json`. If BLE discovery or getInfo fails on a subsequent call, the CLI falls back to cached IP and screen size automatically.

Returns both BLE and HTTP device info including:
```json
{
  "sta_ip": "192.168.x.x",
  "ssid": "WiFi-Name",
  "batt": 48,
  "ver": "1.8.35",
  "w": 1200,
  "h": 1600
}
```

### Upload Image (Instant Display)

Upload an image and display it on the device immediately:

```bash
# Auto-discover device via BLE, auto-resize to screen size
python scripts/bloomin8_cli.py upload --name "Living Room" --file image.jpg

# Direct IP (skip BLE discovery entirely — fastest path)
python scripts/bloomin8_cli.py upload --ip 192.168.8.223 --file image.jpg --resize 480x800

# Name + IP combo: skip BLE, use cache for screen size auto-resize
python scripts/bloomin8_cli.py upload --name "Living Room" --ip 192.168.8.199 --file image.jpg

# Explicit screen size (required when no BLE or cache available)
python scripts/bloomin8_cli.py upload --name "Living Room" --file image.jpg --resize 480x800

# Upload without displaying
python scripts/bloomin8_cli.py upload --name "Living Room" --file image.jpg --no-show

# Resize modes: cover (default, center crop), contain (fit with white bg), stretch
python scripts/bloomin8_cli.py upload --name "Living Room" --file image.jpg --mode contain

# JSON output
python scripts/bloomin8_cli.py upload --ip 192.168.8.223 --file image.jpg --resize 480x800 --json
```

**Auto-resize behavior:**
- **Via BLE** (`--name` only): reads screen dimensions from device, auto-resizes. This is the safest path.
- **Via name + IP** (`--name` + `--ip`): skips BLE entirely, looks up cached screen size **by device name**. Best for repeated uploads after an initial `info`. **Recommended over `--ip` alone** — name is a stable device identifier, whereas IPs can change or be reused by different devices.
- **Via IP** (`--ip` only, no `--resize`): checks cache for a device matching that IP. If cached screen size is found, auto-resizes using it. If no cache hit, aborts — pass `--resize WxH` or run `info` first to populate the cache. **Note:** IP matching may be unreliable if devices change IPs (DHCP). Prefer `--name` + `--ip` for safe cache lookup.

**Workflow:** BLE scan → connect → wake → get IP + screen size → convert & resize to JPEG baseline → HTTP POST to device `/upload` endpoint. With `--ip`, the BLE steps are skipped entirely. Input can be any Pillow-supported format (JPEG, PNG, WebP, BMP, etc.) — the CLI always converts to JPEG baseline output.

### Manage Upstream Settings (Advanced)

Configure the device's cloud pull mechanism. This controls how the device fetches images from the Bloomin8 cloud server on a schedule — it's the on-device side of **Mode 1 (Cloud API)**. When upstream is enabled and a token is set, the device periodically pulls pending images pushed via the Cloud API.

**When to use:** Enabling/disabling cloud push for a device, changing the pull schedule, or pointing the device at a custom server. Most users don't need this — the Bloomin8 app manages these settings. Use this when debugging cloud delivery issues or for advanced configuration.

```bash
# View current settings
python scripts/bloomin8_cli.py upstream --ip 192.168.8.223

# Enable upstream with token
python scripts/bloomin8_cli.py upstream --ip 192.168.8.223 --on --token "your-token"

# Disable upstream
python scripts/bloomin8_cli.py upstream --ip 192.168.8.223 --off

# Set custom upstream URL and cron
python scripts/bloomin8_cli.py upstream --ip 192.168.8.223 --url "https://custom.server/api" --cron "0 */6 * * *"
```

### Local Mode Limitations

- Requires the machine running OpenClaw to have Bluetooth hardware
- Device must be within BLE range (~10m) for discovery and wake
- Device must be on the same WiFi network for HTTP upload — **same subnet is not enough**: AP isolation, VLAN separation, or different access points on the same network can block connectivity. After getting an IP via `info`, verify reachability with `curl http://<ip>/whistle` before attempting upload.
- No cloud token needed — communication is direct

### Device Cache

Successful `info` calls cache device data (name, device_id, IP, screen size) to `~/.bloomin8/device_cache.json`. This path is intentionally outside the skill directory — device data persists across skill upgrades/reinstalls and is shared by all Bloomin8 tools. This enables:
- **BLE failure fallback** — if BLE scan/getInfo times out, the CLI checks cache for a known IP
- **Fast `--ip` uploads** — use `--name "Living Room" --ip 192.168.x.x` to skip BLE and still get auto-resize from cached screen size
- Cache entries include a timestamp; IPs may change if the device reconnects to a different network

### JSON Output (`--json`)

All commands support `--json` for structured output. When enabled, human-readable emoji/text output is suppressed and a single JSON object is printed to stdout. This is the recommended mode for programmatic/agent use.

---

## Troubleshooting Decision Tree

When an operation fails, follow this diagnostic flow:

### Upload / Display Failed
```
Upload failed?
├─ Check device reachable: curl http://<ip>/whistle
│  ├─ ✅ Reachable → image format issue. Verify JPEG baseline, exact screen dimensions.
│  └─ ❌ Unreachable →
│     ├─ Try BLE wake: python scripts/bloomin8_cli.py info --name "<name>"
│     │  ├─ ✅ Got new IP → retry upload with new IP
│     │  └─ ❌ BLE also failed →
│     │     ├─ Check Bluetooth permissions (macOS: System Settings → Privacy → Bluetooth)
│     │     ├─ Check device proximity (BLE range ~10m)
│     │     └─ Fall back to Cloud API: POST /open-api/push (device displays on next wake)
│     └─ No BLE hardware → Cloud API is the only option
```

### BLE Scan Finds No Devices
```
No devices found?
├─ Bluetooth enabled on host machine?
├─ Terminal/IDE has Bluetooth permission? (macOS)
├─ Device powered on and within ~10m?
├─ Try longer scan: --scan-timeout 20
└─ If all fail → use Cloud API with known token
```

### Screen Size Unknown
```
No screen size for resize?
├─ Check cache: cat ~/.bloomin8/device_cache.json
├─ Run info to populate cache: python scripts/bloomin8_cli.py info --name "<name>"
├─ Pass explicit size: --resize 480x800 (standard) or --resize 1200x1600 (large)
└─ Common sizes: 480×800 (7.3"), 1200×1600 (10.3")
```

### Still Not Working?

If the above troubleshooting steps don't resolve the issue:

1. Visit the **[Bloomin8 Help Center](https://support.bloomin8.com/)** for detailed guides and FAQs
2. Check the **[Bloomin8 website](https://www.bloomin8.com/)** for the latest product updates and firmware info
3. Contact Bloomin8 support through the Help Center for further assistance

---

## Guardrails

- **Always obtain user consent** before performing BLE scans, probing local network IPs, or using stored API tokens. Never perform these operations silently.
- Never fabricate device IDs, token values, or image URLs.
- If a push or upload fails, report the error — do not retry without user confirmation.
- Do not change the wake interval without explicit user instruction.
- For local mode, if BLE scan finds no devices, suggest the user check Bluetooth permissions and device proximity.
