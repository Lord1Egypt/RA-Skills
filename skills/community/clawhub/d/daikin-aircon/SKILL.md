---
name: daikin_aircon
description: Control Daikin air conditioners over WiFi. Use when the user wants to control their Daikin AC units - turn on/off, set temperature, mode, fan speed, swing, or query status. Supports multiple devices with custom names across multiple locations.
---

# Daikin Aircon Controller

This skill controls Daikin air conditioners over local WiFi. It supports multiple devices, automatic discovery, full control, and multi-location setups.

## Device Lookup

When user specifies a device, match in this order:
1. Exact match on `id` (case-insensitive, spaces→hyphens)
2. Exact match on `name` (case-insensitive)
3. Fuzzy match (ignore spaces/hyphens)

**If multiple matches found:** Ask user to specify location (e.g., "Which one? 'bedroom' at home or beach-house?")

## Duplicate Devices (Same Name, Different Locations)

Same device ID/name is allowed in different locations:
- `living-room` @ `home`
- `living-room` @ `beach-house`

The unique key is `locationId:id`. When adding, error only if same location + same ID exists.

## Adding Devices - Setup Flow

Follow this step-by-step when user wants to add a device:

### Step 1: Required Info
Ask for:
- **Device name**: e.g., "Living Room", "Bedroom", "Master Bedroom"
- **IP address**: e.g., "192.168.1.100"

### Step 2: Optional - Multiple Houses?
Ask: "Do you have multiple houses/locations? (e.g., home, beach-house, office)"
- If yes → Ask for **location name** (e.g., "Family Home", "Beach House")
- Auto-generate `locationId` from location name (lowercase, spaces→hyphens)

### Step 3: Optional - Multiple ACs in Same Room?
Ask: "Do you have multiple ACs in the same room?"
- If yes → Append to device name (e.g., "Living Room - Ceiling", "Living Room - Floor")

### Step 4: Optional - Device Type
Ask: "Do you know your device type?"
- Options: BRP069, BRP072C, BRP084, AirBase, SkyFi
- If BRP072C → Ask for **API key** (printed on adapter inside unit)
- If SkyFi → Ask for **password**

### Step 5: Verify & Add
Show summary, confirm with user, then call daikin_add.

## Device Management

### Adding a Device

1. **Discovery** - Scan network: "discover daikin devices" → shows found devices
2. **Manual** - "add living room AC at 192.168.1.100"

### Device Types

| Type | Description | Authentication |
|------|-------------|----------------|
| brp069 | Standard WiFi adapter | None |
| brp072C | WiFi adapter with HTTPS | API key required |
| brp084 | Firmware 2.8.0+ adapters | None |
| airbase | Devices with zone support | None |
| skyfi | Legacy SkyFi devices | Password required |

### Finding the API Key (BRP072C)

For BRP072C devices, the API key is printed inside the unit:
1. Remove front grille from indoor unit
2. Find circuit board with WiFi adapter
3. API key is on a label

## Available Tools

### Discovery & Management

- **daikin_discover**: Scan network for Daikin devices (UDP broadcast). Returns IP, MAC, name.

- **daikin_list**: List all configured devices with names, IPs, locations, status.

- **daikin_add**: Add new device. Parameters:
  - `name` (required): Display name (e.g., "Living Room")
  - `ip` (required): IP address
  - `locationId` (optional): Location key (e.g., "home", "beach-house")
  - `locationName` (optional): Location display (e.g., "Family Home")
  - `type` (optional): Device type
  - `key` (optional): API key for BRP072C
  - `password` (optional): Password for SkyFi

- **daikin_remove**: Remove device. If duplicate names exist, use `locationId` to specify.

- **daikin_update**: Update device settings (IP, name, type, key, location).

- **daikin_set_default**: Set default device for commands.

### Status & Control

All control tools accept optional `device` and `locationId` parameters. If only one device matches, use it automatically.

- **daikin_status**: Get status (power, mode, temp, fan, etc.)

- **daikin_power**: Turn on/off.
  - `device`: Device name
  - `locationId`: Location (if needed)
  - `power`: "on" or "off"

- **daikin_mode**: Set mode.
  - `mode`: "auto", "cool", "heat", "dry", "fan"

- **daikin_temperature**: Set target temp (10-32°C, use decimal like 22.5).

- **daikin_fan**: Set fan speed ("auto", "silence", "1"-"5").

- **daikin_swing**: Set swing ("off", "vertical", "horizontal", "3d").

- **daikin_powerful**: Toggle powerful mode.

- **daikin_econo**: Toggle econo mode.

- **daikin_streamer**: Toggle streamer air purifier.

- **daikin_holiday**: Toggle holiday/away mode.

## Usage Examples

### First Time Setup

```
User: Set up my Daikin AC
Agent: Let's add your AC! What's a name for it? (e.g., living-room, bedroom)
User: Living room
Agent: What's the IP address?
User: 192.168.1.101
Agent: Do you have multiple houses or locations?
User: Yes, at the beach
Agent: What's the location name? (e.g., Beach House)
User: Beach House
Agent: Adding "Living Room" at 192.168.1.101 (Beach House)... Done!
```

### Multi-Location

```
User: Add bedroom at the beach house too
Agent: What's the IP for the beach house bedroom?
User: 192.168.1.201
Agent: Adding "Bedroom" at 192.168.1.201 (Beach House)... Done!

User: Turn off bedroom
Agent: You have "bedroom" at both "Family Home" and "Beach House". Which one?
User: Beach house
Agent: Turning off Bedroom at Beach House...
```

### Controlling Devices

```
User: Set living room to 22 degrees
Agent: [Sets Living Room to 22°C]

User: Turn off
Agent: [Turns off default device]

User: What's the temperature in bedroom?
Agent: [Shows bedroom status - if multiple, asks which location]
```

## Temperature Format

- ✅ Correct: "22.5", "23.0"
- ❌ May not work: "22"

## Troubleshooting

- **Device not found**: Check IP, ensure same network subnet
- **Connection timeout**: Verify IP with ping
- **Authentication failed**: Check API key (BRP072C)
- **Multiple matches**: Specify location with `locationId`

## State

Configuration stored in `data/devices.json`. Persists across sessions.
