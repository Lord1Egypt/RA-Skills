# Control USB Relay

A skill for controlling USB relay modules with on/off switching, state tracking, and automation support.

## Features

- **On/Off Control** - Turn relay on or off with simple commands
- **Toggle Function** - Switch to opposite state
- **State Tracking** - Track last known relay state
- **Automation Ready** - Integrate with sensors for automated control

## Requirements

- Python 3
- USB relay module connected to `/dev/ttyUSB1`
- `pyserial` package
- User in `dialout` group (Linux)

## Installation

```bash
npx clawhub install control-usb-relay
```

## Quick Start

```python
from relay import Relay

# Initialize and connect
relay = Relay(port='/dev/ttyUSB1')
relay.connect()

# Control the relay
relay.turn_on()    # Turn on
relay.turn_off()   # Turn off
relay.toggle()     # Toggle state

# Check status
print(f"Relay is: {'ON' if relay.is_on() else 'OFF'}")

# Disconnect when done
relay.disconnect()
```

## API Reference

### Class: `Relay`

#### Constructor

```python
Relay(port='/dev/ttyUSB1', baudrate=9600, timeout=1)
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `port` | `/dev/ttyUSB1` | Serial port |
| `baudrate` | `9600` | Baud rate |
| `timeout` | `1` | Timeout in seconds |

#### Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `connect()` | Connect to relay | `bool` |
| `disconnect()` | Disconnect from relay | `None` |
| `turn_on()` | Turn relay on | `bool` |
| `turn_off()` | Turn relay off | `bool` |
| `toggle()` | Toggle relay state | `bool` |
| `is_on()` | Check if relay is on | `bool` |
| `is_off()` | Check if relay is off | `bool` |
| `get_status()` | Get current state | `bool` |

## Protocol

This skill uses the 4-byte command format:

| Command | Hex Bytes | Action |
|---------|-----------|--------|
| ON | `A0 01 01 A2` | Close relay |
| OFF | `A0 01 00 A1` | Open relay |

> **Note:** Different relay modules may use different protocols. Verify your device compatibility.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No click sound | Verify protocol matches your device |
| `Permission denied` | Run `sudo usermod -a -G dialout $USER`, then logout/login |
| `Connection failed` | Check `ls /dev/ttyUSB*` for device |
| Relay doesn't stay | Check external power supply |

## Hardware Notes

- **JQC-3FF-S-Z** — Relay component rating (5V coil)
- **USB Module** — May need external 5V/12V power
- **CH340** — Common USB-to-serial chip in relay modules

## License

MIT
