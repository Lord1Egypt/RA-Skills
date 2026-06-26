---
name: "ble-device-control"
description: "Control BLE devices via airctl CLI. MUST invoke when user mentions Bluetooth, BLE, device scan, connect, read, write, or notify. ALWAYS read this skill BEFORE running any airctl command."
---

# BLE Device Control Skill

> **IMPORTANT: Read this document before executing any airctl command.**
>
> **Guidelines:**
> 1. **Consult the Command Reference below first.** All common airctl commands and their syntax are documented here.
> 2. **Follow the Decision Tree** to determine which workflow to execute. Do not skip steps.
> 3. **If a command is not found in this document**, verify it with `airctl --help` before using it.
> 4. **Check prerequisites first** before any BLE operation.
> 5. **Validate all user-provided inputs** before passing them to airctl commands. See Input Validation below.

## Input Validation

All user-provided inputs must be validated before being used in airctl commands to prevent shell injection. Apply these validation rules:

**Device Address** — Must match MAC address format: `XX:XX:XX:XX:XX:XX` where each `XX` is a hexadecimal pair.
- Valid regex: `^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$`
- Example valid: `AA:BB:CC:DD:EE:FF`
- If invalid: reject the input and ask the user to provide a valid address.

**Device Alias** — Must contain only alphanumeric characters and underscores. No hyphens, spaces, or special characters.
- Valid regex: `^[A-Za-z0-9_]+$`
- Example valid: `my_sensor`, `heart_rate`
- If invalid: replace hyphens with underscores, remove spaces and special characters, then confirm with the user.

**UUID** — Must match standard BLE UUID format: 4-digit short or 8-4-4-4-12 full format.
- Valid regex: `^[0-9A-Fa-f]{4}$` or `^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$`
- Example valid: `2A19`, `00002A19-0000-1000-8000-00805F9B34FB`
- Both short and full UUID formats are supported in all commands.
- If invalid: reject the input and ask the user to provide a valid UUID.

**Handle** — Must be a positive integer.
- Valid regex: `^[1-9][0-9]*$`
- Example valid: `10`, `74`
- If invalid: reject the input.

**Write Data** — Must use one of the documented data format prefixes with only allowed characters.
- `hex:` prefix: followed by hexadecimal characters only (`0-9A-Fa-f`). Valid regex: `^hex:[0-9A-Fa-f]+$`
- `text:` prefix: followed by printable ASCII characters. Valid regex: `^text:[\x20-\x7E]+$`
- `base64:` prefix: followed by Base64 characters. Valid regex: `^base64:[A-Za-z0-9+/=]+$`
- No prefix: treated as hex, same rules as `hex:`.
- If invalid: reject the input and ask the user to provide properly formatted data.

**Device Name** (for scan filter) — Must contain only printable characters. No shell metacharacters.
- Disallowed characters: `` ` $ | ; & < > ( ) { } [ ] \ ! # ``
- If disallowed characters found: reject the input and ask the user to provide a clean device name.

## Prerequisites

This skill requires the `airctl` CLI tool.

**Provenance:**

| Field | Value |
|-------|-------|
| Source Code | https://github.com/skinapi2025/AirCtl |
| License | MIT |
| Author | skinapi2025 |

**Verify airctl is installed:**

```bash
airctl --version
```

If airctl is not installed, **ask the user** to install it before proceeding. Provide the following installation command for the user to review and execute:

```bash
pip install git+https://github.com/skinapi2025/AirCtl.git
```

> **Note:** Do NOT automatically run `pip install` without user confirmation. The user should verify the package source and approve the installation.

After installation, verify the package origin:

```bash
pip show airctl
```

Confirm that the output shows `Home-page: https://github.com/skinapi2025/AirCtl` or `Author: skinapi2025`.

## Decision Tree

**Follow this decision tree to determine which workflow to execute. Start from the top and follow the FIRST matching path:**

```
User mentions Bluetooth/BLE device operation?
│
├─ YES → What does the user want?
│   │
│   ├─ "Connect and keep connection" / "maintain connection"
│   │   → Follow Workflow 4 (Connect + Keep Alive)
│   │
│   ├─ "Connect" (without keep-alive)
│   │   → Follow Workflow 1 (Connect by Name)
│   │
│   ├─ "Read" a characteristic value
│   │   → Follow Workflow 2 (Read Characteristic)
│   │
│   ├─ "Write" to a characteristic
│   │   → Follow Workflow 3 (Write Characteristic)
│   │
│   ├─ "Scan" / "Find" / "Discover" devices
│   │   → Run: `airctl ble scan -t 10`
│   │
│   ├─ "Subscribe" / "Notify" / "Monitor"
│   │   → Follow Workflow 4 Step 3 (Subscribe)
│   │
│   ├─ "Disconnect"
│   │   → Run: `airctl ble disconnect <address>`
│   │
│   ├─ "Battery" / "Heart rate" / "Device info"
│   │   → Use Device Profile commands: `airctl device battery/heart-rate/device-info <address>`
│   │
│   └─ Other BLE operation
│       → Look up the command in the Command Reference section below
│
└─ NO → This skill may not be relevant
```

## Workflow 1: Connect by Name

**When user says:** "connect to Heart Rate device"

**Execute these steps IN ORDER:**

**Step 1:** Scan for the device:
```bash
airctl ble scan -t 10 -n "Heart Rate"
```

**Step 2:** Parse the JSON output to extract the device `address` field. Validate the address format (see Input Validation).

**Step 3:** Connect using the validated address:
```bash
airctl ble connect <address> -a <alias>
```

> **IMPORTANT:** Use underscores (`_`) in aliases, never hyphens (`-`). Validate alias format before use.

## Workflow 2: Read Characteristic

**When user says:** "read Body Sensor Location from Heart Rate device"

**Execute these steps IN ORDER:**

**Step 1:** Check if device is already connected:
```bash
airctl ble list
```

**Step 2:** If NOT connected, scan and connect:
```bash
airctl ble scan -t 10 -n "Heart Rate"
airctl ble connect <address> -a heart_rate
```

**Step 3:** List characteristics to find the UUID:
```bash
airctl ble characteristics heart_rate
```

**Step 4:** Parse the JSON output to find the target characteristic UUID. Validate the UUID format (see Input Validation).

**Step 5:** Read the characteristic using the validated UUID:
```bash
airctl ble read heart_rate -u <uuid> -f hex
```

## Workflow 3: Write Characteristic

**When user says:** "write 0x01 to Alert Level"

**Execute these steps IN ORDER:**

**Step 1:** Check if device is already connected:
```bash
airctl ble list
```

**Step 2:** If NOT connected, scan and connect first (see Workflow 1)

**Step 3:** Validate the UUID and data format (see Input Validation), then write:
```bash
airctl ble write <address> -u <uuid> -d "<data>"
```

## Workflow 4: Connect + Keep Alive

**When user says:** "connect to Heart Rate and keep connection" or "connect and maintain connection"

**Execute these steps IN ORDER. Do not skip any step:**

**Step 1: Scan and Connect**
```bash
airctl ble scan -t 10 -n "Heart Rate"
```
Parse JSON to get address, validate it, then:
```bash
airctl ble connect <address> -a heart_rate
```

**Step 2: Get Characteristics**
```bash
airctl ble characteristics heart_rate
```

**Step 3: Analyze and Choose Keep-Alive Strategy**

Parse the characteristics JSON. Each characteristic has a `properties` array. Follow this priority:

**Priority 1 — If ANY characteristic has `"notify"` or `"indicate"` in properties:**
```bash
airctl ble notify subscribe heart_rate -u <notifiable_uuid>
```
This is the best keep-alive method. The device pushes data and keeps the connection active.

**Priority 2 — If NO notifiable characteristic, find a read-only one (has `"read"` but NO `"write"`):**
```bash
airctl ble task start-read heart_rate -u <readable_uuid> -i 5
```
Read-only characteristics are safe for periodic reads without side effects.

**Priority 3 — If only read-write characteristics exist, pick one known to be safe:**
```bash
airctl ble task start-read heart_rate -u <readable_uuid> -i 5
```
Use caution — reading may have side effects on some devices.

## Workflow 5: LLM Snapshot Polling

**When an AI agent needs to monitor BLE events without streaming:**

**Step 1:** Subscribe to notifications (returns immediately):
```bash
airctl ble notify subscribe <address> -u <uuid>
```

**Step 2:** Poll for recent events using snapshot query (returns immediately):
```bash
airctl ble events --last 5
```

**Step 3:** Repeat step 2 as needed to check for new events.

**Alternative:** Use periodic read tasks with result snapshots:
```bash
airctl ble task start-read <address> -u 2A19 -i 5
# Returns: {"task_id": "abc123", "type": "periodic_read"}

airctl ble task result abc123 --last 5
# Returns: {"task_id": "abc123", "results": [...], "count": 5}
```

## Command Reference

**All common airctl commands are documented below.** If you need a command not listed here, verify it with `airctl --help` or `airctl ble --help`.

### Daemon

```bash
airctl daemon status
airctl daemon start
airctl daemon stop
airctl daemon restart
```

The daemon starts automatically for BLE operations. Use these only for troubleshooting.

### BLE Scan

```bash
airctl ble scan -t 10
airctl ble scan -n "Heart Rate"
airctl ble scan --service-uuids 180D,180F
```

Scan output (JSON):
```json
{"devices": [{"address": "AA:BB:CC:DD:EE:FF", "name": "Heart Rate", "rssi": -45, "service_uuids": ["180D"]}], "count": 1}
```

### BLE Connect / Disconnect / List

```bash
airctl ble connect <address> [-t 30] [-a alias]
airctl ble disconnect <address>
airctl ble list
```

### BLE GATT Exploration

```bash
airctl ble services <address>
airctl ble characteristics <address>
airctl ble characteristics <address> -s <service_uuid>
```

Characteristics output (JSON):
```json
{"characteristics": [{"uuid": "2A37", "handle": 10, "properties": ["notify", "read"], "service_uuid": "180D"}]}
```

### BLE Read

```bash
airctl ble read <address> -u <uuid> [-f hex|base64|text]
airctl ble read <address> -H <handle> [-f hex|base64|text]
```

Both short UUID (`2A19`) and full UUID (`00002a19-0000-1000-8000-00805f9b34fb`) are supported.

### BLE Write

```bash
airctl ble write <address> -u <uuid> -d "hex:010203"
airctl ble write <address> -H <handle> -d "hex:010203"
airctl ble write <address> -u <uuid> -d "hex:01" --response
```

Data format prefixes: `hex:` (e.g., `hex:010203`), `text:` (e.g., `text:hello`), `base64:` (e.g., `base64:AQID`), or no prefix (treated as hex).

### BLE Notifications

```bash
airctl ble notify subscribe <address> -u <uuid>
airctl ble notify unsubscribe <address> -u <uuid>
```

### BLE Event Snapshots (LLM-friendly)

```bash
airctl ble events --last 5                        # Last 5 events (returns immediately)
airctl ble events --last 10 --address <addr>      # Filter by device address
airctl ble events --last 5 --type notification     # Filter by event type
airctl ble events --last 5 -h                     # Human-readable output
```

Event types: `device_connected`, `device_disconnected`, `notification`, `periodic_read`, `periodic_write`, `periodic_scan`, `task_error`

> **Important:** Without `--last`, `airctl ble events` streams continuously and never returns. Always use `--last N` for LLM/agent usage.

### BLE Background Tasks

```bash
airctl ble task start-read <address> -u <uuid> -i 5
airctl ble task start-read <address> -H <handle> -i 5
airctl ble task start-write <address> -u <uuid> -d "hex:01" -i 10
airctl ble task start-scan -i 30 -t 5
airctl ble task list
airctl ble task stop <task_id>
airctl ble task result <task_id> --last 5         # Query task results (snapshot)
```

### Device Profiles

```bash
airctl device battery <address>              # Battery percentage (0x180F)
airctl device device-info <address>           # Device info (0x180A)
airctl device heart-rate <address>            # Heart rate (0x180D)
airctl device heart-rate <address> --subscribe
airctl device heart-rate <address> --duration 60
```

### Configuration

```bash
airctl config list
airctl config alias set <address> <name>
airctl config alias list
airctl config alias remove <name>
airctl config preset list
airctl config preset get uart
airctl config preset set <name> --service <uuid> --char <uuid>
airctl config preset remove <name>
```

## Common GATT UUIDs

| UUID | Name | Description |
|------|------|-------------|
| 180D | Heart Rate | Heart Rate service |
| 180F | Battery | Battery service |
| 180A | Device Information | Device info service |
| 2A37 | Heart Rate Measurement | Heart rate data (notify) |
| 2A38 | Body Sensor Location | Sensor position (read) |
| 2A19 | Battery Level | Battery percentage (read) |
| 2A06 | Alert Level | Alert control (write) |
| 2A29 | Manufacturer Name | Device manufacturer (read) |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Insufficient Authentication" | Device requires pairing | Pair the device with your system first |
| "Characteristic not found" | Wrong UUID | Run `airctl ble characteristics` to verify, or use `-H` handle |
| "Device not connected" | Not connected yet | Run `airctl ble connect` first |
| "Daemon not running" | Daemon stopped | Run `airctl daemon start` or let it auto-start |
| "Command not found" | airctl not installed or outdated | Verify with `airctl --version`, reinstall if needed |
| "Device disconnected unexpectedly" | BLE device dropped connection | Reconnect with `airctl ble connect`, use periodic read task to keep alive |

## Platform Requirements

- **Windows**: Windows 10 v16299+, Bluetooth adapter
- **Linux**: BlueZ 5.55+, Bluetooth adapter
- **macOS**: macOS 10.15+, Bluetooth adapter
