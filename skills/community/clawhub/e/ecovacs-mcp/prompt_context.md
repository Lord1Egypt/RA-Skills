# Ecovacs Robot Vacuum Control

Control Ecovacs robot vacuums through the [official Ecovacs MCP server](https://github.com/ecovacs-ai/ecovacs-mcp). This is the first official MCP integration for robotic cleaning devices.

## Prerequisites

- **API Key** (`ECO_API_KEY`) from [open.ecovacs.com](https://open.ecovacs.com)
- **`uvx`** (recommended) or `python3` with `ecovacs-robot-mcp` installed
- A robot registered in the Ecovacs mobile app, bound to the same account

## MCP Server Configuration

The MCP server entry should look like this in your settings:

```json
{
  "ecovacs_mcp": {
    "command": "uvx",
    "args": ["--from", "ecovacs-robot-mcp", "python", "-m", "ecovacs_robot_mcp"],
    "env": {
      "ECO_API_KEY": "YOUR_API_KEY",
      "ECO_API_URL": "https://open.ecovacs.com"
    }
  }
}
```

**Regional endpoints:**
- International: `https://open.ecovacs.com`
- China mainland: `https://open.ecovacs.cn`

## MCP Tools Reference

The server exposes four tools. All device operations use a `nickname` parameter that supports **fuzzy matching** — you don't need the exact name.

### get_device_list
Lists all robots bound to the account. No parameters. **Always call this first** to discover available robots and their nicknames.

### start_cleaning
Controls cleaning operations.

| Parameter | Values | Description |
|-----------|--------|-------------|
| `nickname` | string | Robot name (fuzzy match) |
| `act` | `s` | Start cleaning |
| `act` | `p` | Pause cleaning |
| `act` | `r` | Resume cleaning |
| `act` | `h` | Stop cleaning |

### control_recharging
Controls dock/charging operations.

| Parameter | Values | Description |
|-----------|--------|-------------|
| `nickname` | string | Robot name (fuzzy match) |
| `act` | `go-start` | Return to charging dock |
| `act` | `stopGo` | Cancel return to dock |

### query_working_status
Returns real-time robot state. No input besides `nickname`. Returns three status fields:

- **`cleanSt`** — Cleaning state (sweeping, mopping, paused, idle, mapping)
- **`chargeSt`** — Charging state (returning to dock, docking, charging, idle)
- **`stationSt`** — Dock station state (washing mop, drying, dust collection, idle)

## Operating Guidance

1. **Always list devices first** — call `get_device_list` before any operation to get the correct nickname. Cache the nickname for the session.
2. **Confirm actions** — after starting or stopping cleaning, call `query_working_status` to verify the command took effect.
3. **Standard workflows:**
   - *Start cleaning:* list devices → `start_cleaning` (act: `s`) → check status
   - *Send home:* `control_recharging` (act: `go-start`) → check status
   - *Pause and resume:* `start_cleaning` (act: `p`) → later (act: `r`)
4. **Natural language mapping:**
   - "vacuum the house" / "clean the floor" / "start cleaning" → `start_cleaning` act: `s`
   - "send it back" / "dock" / "go home" / "charge" → `control_recharging` act: `go-start`
   - "stop" / "pause" → `start_cleaning` act: `p` or `h`
   - "what's it doing?" / "is it charging?" → `query_working_status`

## Troubleshooting

- **No devices found** — robot must be set up in the Ecovacs app and bound to the same account used for the API key
- **Authentication errors** — verify `ECO_API_KEY` is correct and `ECO_API_URL` matches your region
- **Server won't start** — ensure `uvx` is available (`pip install uv`), or install directly: `pip install ecovacs-robot-mcp`