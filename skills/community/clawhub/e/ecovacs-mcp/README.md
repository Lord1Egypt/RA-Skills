# skill-ecovacs-mcp

Control your **Ecovacs robot vacuum** (DEEBOT series) directly from your AI assistant via the [official Ecovacs MCP server](https://github.com/ecovacs-ai/ecovacs-mcp).

## Features

- List all robots bound to your Ecovacs account
- Start, pause, resume, and stop cleaning
- Send the robot back to its charging dock
- Query real-time cleaning, charging, and dock station status
- Fuzzy nickname matching — no need for exact device names

## Prerequisites

1. An Ecovacs robot set up via the official Ecovacs mobile app
2. An API key (AK) from [open.ecovacs.com](https://open.ecovacs.com)
3. `uvx` installed (or `pip install ecovacs-robot-mcp`)

## Installation

```bash
clawhub install f-liva/skill-ecovacs-mcp
```

Or clone this repo into your skills directory:

```bash
git clone https://github.com/f-liva/skill-ecovacs-mcp.git skills/ecovacs-mcp
```

## Configuration

### 1. Get an API Key

1. Go to [open.ecovacs.com](https://open.ecovacs.com)
2. Sign in with the same Ecovacs account used in the mobile app
3. Create an API Key (AK) in the console

### 2. Configure the MCP Server

Add the following to your MCP server configuration:

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

| Region | Endpoint |
|--------|----------|
| International | `https://open.ecovacs.com` |
| China mainland | `https://open.ecovacs.cn` |

## Usage Examples

Once installed, your assistant can handle natural language commands:

- **"Start cleaning"** → lists devices, picks the robot, sends start command
- **"Send the vacuum back to the dock"** → returns to charging station
- **"What's the vacuum doing?"** → queries real-time working status
- **"Pause the vacuum"** → pauses current cleaning session
- **"Is it charging?"** → checks charging and dock status

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `get_device_list` | List all robots bound to the account |
| `start_cleaning` | Start, pause, resume, or stop cleaning |
| `control_recharging` | Send robot to dock or cancel return |
| `query_working_status` | Get real-time cleaning, charging, and dock status |

## Credits

This skill wraps the [official Ecovacs MCP server](https://github.com/ecovacs-ai/ecovacs-mcp) by Ecovacs AI.

## License

MIT
