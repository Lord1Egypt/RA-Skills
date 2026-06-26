# Flipper Zero Control Skill

Control a Flipper Zero hardware hacking tool via **USB serial CLI** or **Bluetooth Low Energy (BLE)** — no Android device or intermediary app required. Direct machine-to-Flipper communication with full access to SubGHz, IR, NFC, RFID, BadUSB, GPIO, file system, screen capture, and input control.

Inspired by [V3SP3R](https://github.com/elder-plinius/V3SP3R) but without the Android dependency. Four Python scripts, two transports, complete Flipper control from your desk.

## Requirements

- **Flipper Zero** with USB-C cable and/or Bluetooth enabled
- **Firmware:** Tested with Momentum (mntm-008). Should work with official and other community firmwares.
- **Python 3.10+** with a virtual environment
- **Python packages:** `pyserial`, `bleak`, `protobuf`, `grpcio-tools`, `Pillow`
- **macOS or Linux** (BLE via bleak works on both; Windows may need adjustments)
- **Optional:** External CC1101 module (e.g., Rabbit Labs Flux Capacitor) for amplified SubGHz

### Quick Setup

```bash
# Create a dedicated Python environment
python3 -m venv ~/flipper-env
~/flipper-env/bin/pip install pyserial bleak protobuf grpcio-tools Pillow
```

## Transport Comparison

| Feature | USB (`flipper_cli.py`) | BLE (`flipper_ble.py`) |
|---------|----------------------|----------------------|
| SubGHz RX/TX | ✅ Full CLI access | ❌ Not in Protobuf RPC |
| File system | ✅ Text-based | ✅ Structured protobuf |
| GPIO | ✅ Basic | ✅ Full (pin mode, OTG) |
| Device info | ✅ | ✅ |
| App launch | ❌ | ✅ |
| LED/Vibro | ✅ Direct | ✅ Via alert |
| Screen capture | ❌ | ✅ PNG + ASCII art |
| D-pad input | ❌ | ✅ Full navigation |
| Wireless | ❌ | ✅ |
| Latency | ~50ms | ~200ms |

**Recommendation:** Use **USB** for SubGHz/IR operations and raw CLI access. Use **BLE** for wireless file management, GPIO, app control, screen streaming, and input automation.

## Scripts

### `flipper_cli.py` — USB Serial CLI

Direct plaintext CLI over USB. Best for SubGHz and IR operations.

```bash
~/flipper-env/bin/python3 scripts/flipper_cli.py <command> [args...]
```

**Commands:**
```bash
flipper_cli.py info                              # Device info + storage
flipper_cli.py detect                            # Quick connection check
flipper_cli.py storage list /ext/subghz          # List directory
flipper_cli.py storage read /ext/file.sub        # Read file contents
flipper_cli.py storage write /ext/path "data"    # Write file
flipper_cli.py storage mkdir /ext/new_dir        # Create directory
flipper_cli.py storage remove /ext/old_file      # Delete (⚠️ HIGH RISK)
flipper_cli.py storage info /ext                 # Storage stats
flipper_cli.py subghz rx 433920000 0 10          # Listen 433.92MHz, internal, 10sec
flipper_cli.py subghz rx 433920000 1 15          # Listen with external CC1101, 15sec
flipper_cli.py subghz tx AABBCC 433920000 400 3 1  # Transmit (⚠️ HIGH RISK)
flipper_cli.py subghz tx_from_file /ext/subghz/file.sub 1 0  # Transmit .sub (⚠️ HIGH RISK)
flipper_cli.py subghz rx_raw 433920000 10        # Raw capture
flipper_cli.py scan_subghz 433920000 30 1        # Scan for 30sec with external
flipper_cli.py ir tx /ext/infrared/remote.ir     # Transmit IR
flipper_cli.py gpio set PA7 1                    # Set GPIO pin
flipper_cli.py led b 255                         # Set blue LED (r|g|b|bl channel)
flipper_cli.py led off                           # All LEDs off
flipper_cli.py vibro 1                           # Vibration on
flipper_cli.py power 5v 1                        # Enable 5V GPIO (external modules)
flipper_cli.py raw "any flipper cli command"     # Raw passthrough
```

**Environment:**
- `FLIPPER_PORT` — Serial port override (default: auto-detect `/dev/cu.usbmodemflip_*`)
- `FLIPPER_BAUD` — Baud rate (default: 230400)

### `flipper_ble.py` — BLE Protobuf RPC

Wireless control via Flipper's BLE serial service and Protobuf RPC protocol.

```bash
~/flipper-env/bin/python3 scripts/flipper_ble.py <command> [args...]
```

**Commands:**
```bash
flipper_ble.py scan                              # Find Flipper devices
flipper_ble.py ping                              # Connection test
flipper_ble.py info                              # Full device info
flipper_ble.py power_info                        # Battery/power status
flipper_ble.py protobuf_version                  # Protocol version
flipper_ble.py alert                             # LED + vibro + sound alert
flipper_ble.py datetime                          # Get date/time
flipper_ble.py storage list /ext/subghz          # List directory
flipper_ble.py storage read /ext/file.txt        # Read file
flipper_ble.py storage write /ext/path local.txt # Upload file
flipper_ble.py storage mkdir /ext/new_dir        # Create directory
flipper_ble.py storage delete /ext/file          # Delete (⚠️ HIGH RISK)
flipper_ble.py storage info /ext                 # Storage stats
flipper_ble.py storage md5 /ext/file             # File checksum
flipper_ble.py storage rename /ext/old /ext/new  # Rename/move
flipper_ble.py gpio read PA7                     # Read GPIO pin
flipper_ble.py gpio write PA7 1                  # Write GPIO pin
flipper_ble.py gpio mode PA7 output              # Set pin mode
flipper_ble.py gpio otg on                       # Enable 5V OTG power
flipper_ble.py app start SubGHz                  # Launch Flipper app
flipper_ble.py app exit                          # Exit current app
flipper_ble.py reboot                            # Reboot (⚠️ HIGH RISK)
```

**Environment:**
- `FLIPPER_BLE_ADDRESS` — Skip scan, connect directly to address
- `FLIPPER_BLE_NAME` — Device name to search for (default: auto-detect)

**Note:** BLE requires USB cable to be **unplugged** — Flipper can't do both simultaneously.

### `flipper_screen.py` — Screen Capture & Input

Captures the Flipper's 128×64 monochrome display and provides D-pad navigation over BLE.

```bash
~/flipper-env/bin/python3 scripts/flipper_screen.py <command> [args...]
```

**Commands:**
```bash
flipper_screen.py screenshot [output.png]        # 4x scaled PNG (Flipper orange on black)
flipper_screen.py ascii                          # Unicode half-block ASCII art
flipper_screen.py press <key> [short|long]       # Button: up/down/left/right/ok/back
flipper_screen.py navigate ok down down ok       # Key sequence
flipper_screen.py watch 10 [output_dir]          # Stream frames for N seconds
flipper_screen.py app_control SubGHz wait:1 screenshot  # Launch app + actions
```

**Actions for `app_control` and `navigate`:**
- Button names: `up`, `down`, `left`, `right`, `ok`, `back`
- Long press: `ok:long`, `back:long`
- Wait: `wait:1.0` (seconds)
- Screenshot: `screenshot` or `ascii`

### `flipper_subghz_ble.py` — SubGHz over BLE

Performs SubGHz operations wirelessly by launching the SubGHz app, navigating menus via button presses, and reading results from screen captures.

```bash
~/flipper-env/bin/python3 scripts/flipper_subghz_ble.py <command> [args...]
```

**Commands:**
```bash
flipper_subghz_ble.py read [duration_sec]        # Read mode (protocol decoder)
flipper_subghz_ble.py read_raw [duration_sec]    # Read RAW mode
flipper_subghz_ble.py frequency_analyzer [dur]   # Frequency Analyzer
flipper_subghz_ble.py saved                      # Browse saved signals
flipper_subghz_ble.py transmit <filename>        # Open saved file (⚠️ HIGH RISK)
flipper_subghz_ble.py status                     # Screenshot current screen
```

**Note:** Results are visual (PNG/ASCII screenshots) rather than parsed data. For structured SubGHz data, use USB transport.

## Risk Classification

Every command is risk-classified following a safety model:

| Risk | Actions | Behavior |
|------|---------|----------|
| **Low** | Read-only: info, list, read, scan, bt info | Execute freely |
| **Medium** | Write, mkdir, copy, IR, NFC/RFID emulate, GPIO | Execute with note |
| **High** | Delete, SubGHz transmit, power off/reboot | **Confirm with user first** |

**Rule:** NEVER execute HIGH risk commands without explicit user confirmation.

## Protobuf Definitions

The `scripts/proto/` directory contains compiled Python protobuf modules from the [Flipper Zero protobuf repo](https://github.com/flipperdevices/flipperzero-protobuf). To regenerate:

```bash
git clone --depth 1 https://github.com/flipperdevices/flipperzero-protobuf.git
cd flipperzero-protobuf
python3 -m grpc_tools.protoc --proto_path=. --python_out=<output_dir> \
    flipper.proto storage.proto system.proto gpio.proto \
    application.proto gui.proto property.proto desktop.proto
```

## External CC1101 Module Support

If you have an external CC1101 module (like the Rabbit Labs Flux Capacitor):
- Use `device=1` in any SubGHz command for the external module
- Use `gpio otg on` (BLE) or `power 5v 1` (USB) to power it via GPIO
- **Always use an antenna** — transmitting without one damages the module
- The external module typically offers better range and sensitivity

## Troubleshooting

- **USB port not found:** Check `ls /dev/cu.usbmodem*` — Flipper may need reconnect
- **BLE device not found:** Wake the Flipper (press any button), ensure BLE is ON in Settings
- **BLE drops after use:** Normal — Flipper sleeps after idle. Just reconnect.
- **Timeout/no response:** Flipper might be in an app — press Back to return to CLI
- **Screen capture empty:** Display only sends frames on change; static screens won't produce new frames
- **SubGHz no packets:** Normal if nothing is transmitting nearby. Try pressing a remote during a scan.
