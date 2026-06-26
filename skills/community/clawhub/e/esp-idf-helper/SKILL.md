---
name: esp-idf-helper
description: Help develop, build, flash, and debug ESP32/ESP8266 firmware using Espressif ESP-IDF on Linux/WSL. Use when the user asks about ESP-IDF project setup, configuring targets, menuconfig, building, flashing via esptool/idf.py, serial monitor, partition tables, sdkconfig, troubleshooting build/flash/monitor errors, or automating common idf.py workflows from the command line.
homepage: https://github.com/espressif/esp-idf
metadata:
  {
    "esp-idf-helper":
      {
        "emoji": "🤖",
        "requires": { "bins": ["idf.py"], "env": ["IDF_PATH"] },
        "primaryEnv": "IDF_PATH",
      },
  }
---

# esp-idf-helper Skill

Provide a repeatable, command-line-first workflow for ESP-IDF development on Linux/WSL: configure → build → flash → monitor → debug/troubleshoot.

## Quick Reference

```bash
# 1) Source the ESP-IDF environment (once per terminal session)
. $IDF_PATH/export.sh

# 1.1) Enable ccache to speed up compilation (recommended)
export IDF_CCACHE_ENABLE=1

# 2) Go to your project and build
cd /path/to/your/project
idf.py set-target <target>    # Set target chip (once per project)
idf.py build                 # Compile

# 3) flash
idf.py -p <PORT> -b <BAUD> flash  # Flash to device (optional)
```

### Common commands
- `idf.py --help` — Help
- `idf.py set-target <target>` — Set chip target: esp32, esp32s2, esp32s3, esp32c3, esp32p4
- `idf.py menuconfig` — Configure project settings (**must run in a new terminal window**)
- `idf.py build` — Build the project
- `idf.py update-dependencies` — Update project component dependencies
- `idf.py partition-table` — Build partition table and print partition entries
- `idf.py partition-table-flash` — Flash partition table to device
- `idf.py storage-flash` — Flash storage filesystem partition
- `idf.py size` — Show firmware size information
- `idf.py -p <PORT> -b <BAUD> flash` — Flash firmware (default baud: 460800)
- `idf.py -p <PORT> monitor` — Open serial monitor
- `idf.py -p <PORT> -b <BAUD> monitor` — Open serial monitor with specific baud (e.g. 460800)
- `idf.py -p <PORT> -b <BAUD> flash monitor` — Flash then monitor

## Component Management

ESP-IDF projects can include external components from the **ESP Component Registry**.

- **Registry Website:** https://components.espressif.com/components
- **Search components:** Browse or search for components on the registry website

### Component Commands
- `idf.py add-dependency "<component>"` — Add a component dependency to `idf_component.yml`
- `idf.py update-dependencies` — Download and update all project dependencies

### Component Management Workflow
```bash
# 1) Add a dependency to your project
idf.py add-dependency "<component>"

# 2) Update dependencies (downloads components to managed_components/)
idf.py update-dependencies

```

**Note:** Dependencies are recorded in `idf_component.yml` in your project's main component directory (`main/`).

## Bundled resources
### references/
- `references/esp-idf-cli.md` — concise command patterns + what to paste back when reporting errors.
- `references/idf-py-help.txt` — captured `idf.py --help` output for quick lookup/search.

To refresh the help text for your installed ESP-IDF version, run:
- `scripts/capture_idf_help.sh`

### assets/
Not used by default.

## Serial Port Management (WSL2)

For WSL2 users, USB serial devices need to be attached via **usbipd** to be accessible in WSL.

### List Available Serial Devices
```bash
scripts/usbipd_attach_serial.sh --list
```
Shows all connected USB serial devices (CH340, CH343, CP210, FTDI, etc.).

**Note:** This script runs in WSL2 and uses `powershell.exe` to communicate with Windows usbipd.

### Bind/Attach All Serial Devices
```bash
# Bind and attach all COM port devices
scripts/usbipd_attach_serial.sh --keyword "COM"

# Or attach specific device by busid
scripts/usbipd_attach_serial.sh --busid 3-2

# Or filter by device type
scripts/usbipd_attach_serial.sh --keyword "CH343"
scripts/usbipd_attach_serial.sh --keyword "ESP32"
```

### Serial Port Script Options
- `--list` — List all matching serial devices and exit
- `--busid <BUSID>` — Specify device bus ID (e.g., `3-2`)
- `--keyword <TEXT>` — Filter devices by keyword (e.g., `COM`, `CH343`, `ESP32`)
- `--bind` — Bind only (skip attach), useful for first-time setup with admin privileges
- `--distro <DISTRO>` — Specify WSL distribution name
- `--dry-run` — Print commands without executing

### Typical Workflow
```bash
# 1. Check available devices
scripts/usbipd_attach_serial.sh --list

# 2. Attach all serial devices
scripts/usbipd_attach_serial.sh --keyword "COM"

# 3. Verify devices in WSL
ls -la /dev/ttyACM* /dev/ttyUSB*

# 4. Use with idf.py
idf.py -p /dev/ttyACM0 flash monitor
```

**Note:** This script runs in WSL2 and internally uses `powershell.exe` to communicate with Windows usbipd service.

### Troubleshooting: powershell.exe not found

If you encounter `powershell.exe: command not found`, the Windows paths are not in your PATH environment variable.

**Quick Fix (current session only):**
```bash
export PATH="$PATH:/mnt/c/Windows/System32:/mnt/c/Windows/System32/WindowsPowerShell/v1.0"
~/skills/esp-idf-helper/scripts/usbipd_attach_serial.sh --list
```

**Permanent Fix (add to ~/.bashrc):**
```bash
echo 'export PATH="$PATH:/mnt/c/Windows/System32:/mnt/c/Windows/System32/WindowsPowerShell/v1.0:/mnt/c/Windows/SysWOW64"' >> ~/.bashrc
source ~/.bashrc
```

## Firmware Packaging

Pack ESP-IDF build output into a distributable firmware package with cross-platform flash scripts.

### Usage
```bash
scripts/pack_firmware.sh <build_directory>
```

### Example
```bash
# After building your project
idf.py build

# Create firmware package
scripts/pack_firmware.sh ./build

# Output: build/firmware_package/ and build/esp_firmware_YYYYMMDD_HHMMSS.zip
```

### Generated Package Contents
| File | Description |
|------|-------------|
| `flash.sh` | Linux/Mac flash script with retry and parallel support |
| `flash.bat` | Windows multi-port flash launcher |
| `flash_one.bat` | Windows single-port flash with retry |
| `mac_addresses.txt` | Recorded MAC addresses (deduplicated) |
| `*.bin` | Firmware binary files |
| `tools/esptool/esptool.exe` | Windows esptool executable |
| `README.txt` | Usage instructions |

### Flash Script Features
- **Auto-retry**: 3 attempts on failure
- **Parallel flashing**: Multiple devices simultaneously
- **MAC recording**: Automatic MAC address extraction and deduplication
- **Cross-platform**: Linux/Mac/Windows support

### Production Workflow
```bash
# 1. Build the project
idf.py build

# 2. Package firmware
scripts/pack_firmware.sh ./build

# 3. Distribute the ZIP to production line
# Production team runs: flash.bat all  (Windows) or ./flash.sh /dev/ttyUSB*  (Linux)
```