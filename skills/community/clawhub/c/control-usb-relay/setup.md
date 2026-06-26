# Setup — Control USB Relay

## Prerequisites

- USB Relay module connected to `/dev/ttyUSB1`
- Python 3 with `pyserial` installed
- User in `dialout` group (for serial port access)
- External power supply (if required by relay module)

## Quick Start

```bash
# Install dependencies
pip3 install pyserial

# Add user to dialout group (if needed)
sudo usermod -a -G dialout $USER

# Test relay
python3 relay.py
```

## Usage Examples

### Basic Control

```python
from relay import Relay

relay = Relay(port='/dev/ttyUSB1')
if relay.connect():
    relay.turn_on()      # Turn on
    relay.turn_off()     # Turn off
    relay.disconnect()
```

### Toggle State

```python
from relay import Relay

relay = Relay()
relay.connect()

relay.toggle()  # Switch to opposite state
print(f"Relay is now: {'ON' if relay.is_on() else 'OFF'}")

relay.disconnect()
```

### Automated Control with Sensor

```python
from sensor import Sensor
from relay import Relay
import time

sensor = Sensor(port='/dev/ttyUSB0')
relay = Relay(port='/dev/ttyUSB1')

sensor.connect()
relay.connect()

try:
    while True:
        lux = sensor.read_lux()

        if lux < 100:  # Dark
            relay.turn_on()
        elif lux > 500:  # Bright
            relay.turn_off()

        time.sleep(1)
except KeyboardInterrupt:
    sensor.disconnect()
    relay.disconnect()
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No click sound | Verify protocol matches your device |
| `Permission denied` | `sudo usermod -a -G dialout $USER`, logout/login |
| `Connection failed` | Check `ls /dev/ttyUSB*` for device |
| Relay doesn't stay | Check external power supply |

## Relay Protocol

This skill uses the 4-byte command format:

| Command | Hex Bytes | Action |
|---------|-----------|--------|
| ON | `A0 01 01 A2` | Close relay |
| OFF | `A0 01 00 A1` | Open relay |

**Note:** Different relay modules may use different protocols. Verify your device compatibility.

## Hardware Notes

- **JQC-3FF-S-Z** — Relay component rating (5V coil)
- **USB Module** — May need external 5V/12V power
- **CH340** — Common USB-to-serial chip in relay modules
