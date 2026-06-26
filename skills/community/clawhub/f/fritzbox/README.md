# FRITZ!Box Skill

Control your AVM FRITZ!Box router and Smarthome devices via Python.

## Features

- ✅ **WLAN Control** - Turn WiFi on/off, check status
- ✅ **Network Devices** - List all connected devices (LAN/WLAN)
- ✅ **Router Info** - Get model, firmware version
- ✅ **Internet Reconnect** - Force WAN reconnect
- ✅ **Smarthome** - Control FRITZ!DECT devices (switches, power meters, thermostats)

## Installation

```bash
# Clone repository
git clone https://github.com/first-it-consulting/fritzbox-skill.git
cd fritzbox-skill

# Install dependency
pip install requests

# Copy and edit environment file
cp .env.example .env
# Edit .env with your FRITZ!Box credentials
```

## Configuration

Create a `.env` file in the project directory:

```bash
FRITZBOX_USER=your_username
FRITZBOX_PASSWORD=your_password
FRITZBOX_HOST=fritz.box
```

Or set environment variables:
```bash
export FRITZBOX_USER=your_username
export FRITZBOX_PASSWORD=your_password
export FRITZBOX_HOST=fritz.box
```

## Usage

### Basic Commands

```bash
# Router info
python3 fritzbox.py info

# WLAN control
python3 fritzbox.py wlan status
python3 fritzbox.py wlan on
python3 fritzbox.py wlan off

# List connected devices
python3 fritzbox.py hosts

# Internet reconnect
python3 fritzbox.py reconnect
```

### Smarthome Commands

```bash
# List smarthome devices
python3 fritzbox.py smarthome list

# Switch device on/off (use quotes for AIN with spaces!)
python3 fritzbox.py smarthome switch "08761 0311726" on
python3 fritzbox.py smarthome switch "08761 0311726" off
```

### With explicit credentials

```bash
python3 fritzbox.py --user admin --password secret --host 192.168.178.1 info
```

## Smarthome Device Info

When listing devices, you'll see:
- **Name** - Device name
- **AIN** - Device identifier (needed for switching)
- **State** - ON/OFF
- **Power** - Current power consumption in Watts
- **Voltage** - Current voltage
- **Temp** - Device temperature

## Supported Devices

### Router Functions
- All FRITZ!Box models with TR-064 support
- WLAN 2.4 GHz, 5 GHz, and Guest network
- Connected device monitoring

### Smarthome Devices
- FRITZ!DECT 200/210 (smart plugs with power monitoring)
- FRITZ!DECT 301 (radiator thermostats)
- FRITZ!DECT 500 (smart bulbs)
- FRITZ!DECT 440/450 (buttons)
- Comet DECT devices

## Troubleshooting

**"401 Unauthorized" error:**
- Check username and password in `.env`
- Default user is often empty or "admin"

**"No smarthome devices found":**
- Ensure DECT devices are paired with FRITZ!Box
- Check device is present (within DECT range)

**Switching fails:**
- Use quotes around AIN: `"08761 0311726"`
- Check device is present in device list

## API Reference

This tool uses:
- **TR-064** - For router functions (WLAN, hosts, device info)
- **Homeautoswitch API** - For smarthome device control

## License

MIT License - Feel free to use and modify.

## Contributing

Pull requests welcome! Please test your changes before submitting.
