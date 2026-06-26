---
name: arduino-cli
description: Provides commands and workflows for Arduino CLI. Use when the user wants to create, compile, or upload Arduino sketches, manage boards (list, attach), install/search/list cores (platforms) and libraries, or configure Arduino CLI. Triggers on phrases like "arduino-cli", "compile sketch", "upload arduino", "install arduino core", or "arduino library".
---

# Arduino CLI Skill

This skill provides guidance for using the `arduino-cli` to manage Arduino projects, boards, cores, and libraries from the command line.

## Quick Reference

### 1. Configuration & Setup
Initialize the configuration file (usually in `~/.arduino15/arduino-cli.yaml`):
```bash
arduino-cli config init
```

Update the local cache of available platforms and libraries (do this first!):
```bash
arduino-cli core update-index
```

### 2. Board Management
List connected boards to find the port and FQBN (Fully Qualified Board Name):
```bash
arduino-cli board list
```

List all supported boards and their FQBN strings:
```bash
arduino-cli board listall <search_term>
```

### 3. Core (Platform) Management
Search for a core:
```bash
arduino-cli core search <keyword>
```

Install a core using its ID (e.g., `arduino:samd`):
```bash
arduino-cli core install <core_id>
```

List installed cores:
```bash
arduino-cli core list
```

### 4. Sketch Workflow
Create a new sketch:
```bash
arduino-cli sketch new <SketchName>
```

Compile a sketch (requires the board's FQBN):
```bash
arduino-cli compile --fqbn <FQBN> <SketchName>
```
*Example:* `arduino-cli compile --fqbn arduino:samd:mkr1000 MyFirstSketch`

Upload a sketch to a connected board:
```bash
arduino-cli upload -p <port> --fqbn <FQBN> <SketchName>
```
*Example:* `arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:samd:mkr1000 MyFirstSketch`

### 5. Library Management
Search for a library:
```bash
arduino-cli lib search <keyword>
```

Install a library:
```bash
arduino-cli lib install "<Library Name>"
```

## Adding 3rd Party Cores (e.g., ESP8266)

To install 3rd party cores, pass the `--additional-urls` flag to your core commands:

```bash
arduino-cli core update-index --additional-urls https://arduino.esp8266.com/stable/package_esp8266com_index.json
arduino-cli core install esp8266:esp8266 --additional-urls https://arduino.esp8266.com/stable/package_esp8266com_index.json
```
*(Alternatively, these URLs can be added to the `board_manager.additional_urls` array in `arduino-cli.yaml`)*
