---
name: fritzbox
description: Control AVM FRITZ!Box routers and Smarthome devices via TR-064 and Web API. Use when the user wants to manage their FRITZ!Box router (WLAN, connected devices, reconnect) or control FRITZ!DECT smarthome devices (smart plugs, thermostats). Triggers on phrases like "fritzbox", "fritz box", "router", "wlan", "wifi", "smarthome", "dect", "smart plug", "steckdose".
metadata: {"clawdbot":{"emoji":"📡","requires":{"bins":["python3"],"env":["FRITZBOX_PASSWORD","FRITZBOX_HOST"]},"primaryEnv":"FRITZBOX_HOST"}}
---

# FRITZ!Box Skill

Control your AVM FRITZ!Box router and Smarthome devices.

## When to Use

✅ **USE this skill when:**
- "Turn WLAN/WiFi on/off"
- "List connected devices"
- "Show router info"
- "Reconnect internet"
- "List smarthome devices"
- "Switch smart plug on/off"
- "Check who's on the network"

❌ **DON'T use this skill when:**
- Non-AVM routers
- Advanced firewall configuration
- Firmware updates

## ⚠️ Confirmation Required

The following commands make high-impact, hard-to-reverse changes to the network or connected devices.
**Always ask the user for explicit confirmation before running them:**

| Command | Impact |
|---------|--------|
| `wlan off` / `wlan on` | Disables or enables Wi-Fi — may cut network access |
| `reconnect` | Forces internet disconnection and re-dial |
| `smarthome switch <ain> off` / `on` | Turns a physical device on or off |
| `smarthome toggle <ain>` | Inverts the current device state |

Only invoke these after the user has clearly and explicitly requested the specific action.

## Prerequisites

- FRITZ!Box must be accessible on the local network
- For router functions: TR-064 must be enabled
- For smarthome: DECT devices must be paired

## Authentication

### Option 1: .env File (Recommended)

Create a `.env` file:

```bash
FRITZBOX_USER=your_username
FRITZBOX_PASSWORD=your_password
FRITZBOX_HOST=fritz.box
```

### Option 2: Command Line

```bash
python3 fritzbox.py --user admin --password YOURPASS wlan status
```

## Common Commands

### Router Control

```bash
# Router info
python3 fritzbox.py info

# WLAN on/off/status
python3 fritzbox.py wlan on
python3 fritzbox.py wlan off
python3 fritzbox.py wlan status

# List connected network devices
python3 fritzbox.py hosts

# Reconnect internet
python3 fritzbox.py reconnect
```

### Smarthome Control

```bash
# List all smarthome devices
python3 fritzbox.py smarthome list

# Switch device on/off (AIN with spaces needs quotes!)
python3 fritzbox.py smarthome switch "08761 0311726" on
python3 fritzbox.py smarthome switch "08761 0311726" off
```

**Note:** The AIN (identifier) is shown in the device list. Use quotes if it contains spaces!

## Smarthome Device Output

```
FRITZ!Smart Energy 200 #1
  AIN: 08761 0311726
  State: ON, Power: 84.4W, Voltage: 237.3V, Temp: 20.5°C
```

## Troubleshooting

**"401 Unauthorized":**
- Check credentials in `.env`
- Ensure user exists in FRITZ!Box

**"No smarthome devices found":**
- Check DECT devices are paired
- Verify device is within range

**Switch command fails:**
- Always use quotes around AIN: `"08761 0311726"`
- Check device is present (green DECT icon in FRITZ!Box UI)

## Custom Host

If your FRITZ!Box is on a different IP:

```bash
python3 fritzbox.py --host 192.168.178.1 info
```

## API Used

- **TR-064** - Router functions (WLAN, hosts, device info)
- **Homeautoswitch API** - Smarthome device control

## Security Guidance

- **Least privilege:** Create a dedicated FRITZ!Box user with limited permissions for agent use rather than using the admin account.
- **Protect credentials:** Keep `.env` outside version control (it is listed in `.gitignore`). Restrict file permissions: `chmod 600 .env`.
- **Verify the host:** Ensure `FRITZBOX_HOST` points to your own local router. Do not route credentials through untrusted hosts.
- **Scope of access:** The configured account can authorize all router and smarthome changes supported by this skill. Treat the credentials with the same care as router admin credentials.
