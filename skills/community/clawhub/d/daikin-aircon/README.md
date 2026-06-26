# Daikin Aircon OpenClaw Skill

Control Daikin air conditioners over WiFi using OpenClaw. This skill supports multiple devices, automatic discovery, and full control of all AC features including power, mode, temperature, fan, swing, powerful, econo, streamer, and holiday modes.

## Features

- **Multi-device support**: Manage multiple Daikin AC units with custom names
- **Automatic discovery**: Scan your network for Daikin devices using UDP broadcast
- **Full control**: Power, mode, temperature, fan speed, swing direction
- **Advanced modes**: Powerful, Econo, Streamer air purifier, Holiday/Away mode
- **Status monitoring**: Current temperature, humidity, compressor frequency, filter status
- **OS-independent**: Credentials stored in JSON configuration file

## Supported Devices

| Type | Description | Authentication |
|------|-------------|----------------|
| BRP069 | Standard WiFi adapter | None |
| BRP072C | WiFi adapter with HTTPS | API key required |
| BRP084 | Firmware 2.8.0+ adapters | None |
| AirBase | Devices with zone support | None |
| SkyFi | Legacy SkyFi devices | Password required |

## Installation

### Prerequisites

- [OpenClaw](https://openclaw.ai) installed
- Node.js 18+
- Daikin air conditioner with WiFi adapter

### Install the Skill

1. Clone or copy this skill to your OpenClaw workspace:

```bash
cd ~/.openclaw/workspace/skills
git clone <this-repo> daikin-aircon
```

2. Install dependencies:

```bash
cd daikin-aircon
npm install
```

3. Build the TypeScript:

```bash
npm run build
```

4. Restart OpenClaw or refresh skills to load the new skill.

## Finding Your Device IP

### Method 1: Router

Check your router's connected devices list. The Daikin device is usually named "Daikin" or similar.

### Method 2: Mobile App

The Daikin Online Controller app shows the device IP in settings.

### Method 3: Discovery

Use the skill's discovery feature:

```
discover daikin devices
```

## Finding the API Key (BRP072C)

For BRP072C/HTTPS adapters:

1. Remove the front grille from the indoor unit
2. Find the circuit board with the WiFi adapter
3. The API key is printed on a label on the adapter

## Usage Examples

### First Time Setup

```
User: Discover my Daikin aircons
Agent: Scanning network... Found 2 devices:
  - 192.168.1.101 (MAC: AABBCCDDEEFF)
  - 192.168.1.102 (MAC: 112233445566)

User: Add the first one as living room
Agent: Device "living-room" added at 192.168.1.101

User: Add the second one as bedroom  
Agent: Device "bedroom" added at 192.168.1.102
```

### Basic Control

```
User: Set living room to 22 degrees
Agent: [Sets living-room AC to 22°C in cool mode]

User: Turn off bedroom
Agent: [Turns off bedroom AC]

User: What's the temperature in living room?
Agent: [Shows current status including inside temperature]
```

### Advanced Features

```
User: Turn on powerful mode in living room
Agent: [Enables powerful mode for maximum cooling/heating]

User: Enable econo mode in bedroom
Agent: [Enables energy-efficient mode]

User: Turn on streamer in living room
Agent: [Enables streamer air purifier]
```

### Holiday Mode

```
User: Set living room to holiday mode
Agent: [Enables holiday/away mode - maintains energy-saving temperature]
```

## Command Reference

### Device Management

| Command | Description |
|---------|-------------|
| `daikin_discover` | Scan network for devices |
| `daikin_list` | List all configured devices |
| `daikin_add` | Add a new device |
| `daikin_remove` | Remove a device |
| `daikin_set_default` | Set default device |

### Control

| Command | Parameters | Description |
|---------|------------|-------------|
| `daikin_status` | device? | Get device status |
| `daikin_power` | device, on/off | Power on/off |
| `daikin_mode` | device, auto/cool/heat/dry/fan | Set mode |
| `daikin_temperature` | device, 10-32 | Set temperature |
| `daikin_fan` | device, auto/silence/1-5 | Set fan speed |
| `daikin_swing` | device, off/vertical/horizontal/3d | Set swing |
| `daikin_powerful` | device, on/off | Toggle powerful |
| `daikin_econo` | device, on/off | Toggle econo |
| `daikin_streamer` | device, on/off | Toggle streamer |
| `daikin_holiday` | device, on/off | Toggle holiday mode |

## Configuration

Devices are stored in `data/devices.json`:

```json
{
  "devices": [
    {
      "id": "living-room",
      "name": "living-room",
      "ip": "192.168.1.101",
      "type": "brp072c",
      "key": "YOUR_API_KEY"
    }
  ],
  "defaultDevice": "living-room"
}
```

### File Location

The configuration file is stored in the skill's `data/` directory. To change its location, modify the `configPath` in `src/config.ts`.

## Temperature Format

When setting temperature, always use decimal format:

- ✅ Correct: `22.5`, `23.0`
- ❌ May not work: `22`

## Troubleshooting

### Device not found during discovery

- Ensure the device is powered on
- Check it's on the same network subnet
- Some routers block UDP broadcasts; try manual IP entry

### Connection timeout

- Verify the IP address is correct
- Check the device is reachable: `ping <device-ip>`

### Authentication failed (BRP072C)

- Verify the API key is correct
- The key is printed inside the unit (see Finding API Key section)

### "No device specified" error

- Add a device first using `daikin_add`
- Or set a default device: `daikin_set_default`

## Publishing to ClawHub

```bash
# Install CLI if needed
npm i -g clawhub

# Login
clawhub login

# Publish
clawhub publish ./daikin-aircon \
  --slug daikin-aircon \
  --name "Daikin Aircon Controller" \
  --tags smart-home,ac,hvac,daikin \
  --version 1.0.0
```

## License

GPL-3.0 - See LICENSE file

## Credits

- [daikin-ts](https://github.com/leroylim/daikin-ts) - TypeScript library for Daikin AC control
- [pydaikin](https://github.com/fredrike/pydaikin) - Python library this is based on
