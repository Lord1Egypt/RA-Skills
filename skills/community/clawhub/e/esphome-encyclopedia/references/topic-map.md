# ESPHome Topic Map

Use this as a quick orientation aid when deciding what official docs page to look up.

## Core areas

- Core YAML structure (`esphome:`, `esp32:`, `esp8266:`, `packages:`, `substitutions:`)
- Connectivity (`wifi:`, `api:`, `ota:`, `web_server:`)
- Logging and diagnostics (`logger:`, `captive_portal:`)
- Sensors, binary sensors, switches, lights, outputs, displays
- Pin mappings, board/framework selection, hardware integration
- Build/compile behavior and dashboard/node operations
- Secrets handling and reusable config patterns

## Typical lookup prompts

When the task is about...

### Core config structure
Look for:
- ESPHome configuration reference pages
- `esphome:` / platform docs (`esp32`, `esp8266`, `bk72xx`, etc.)
- substitutions/packages docs when config reuse matters

### Connectivity / management
Look for:
- `wifi:`
- `api:`
- `ota:`
- `web_server:`
- `captive_portal:`

### Sensors / actuators / entities
Look for:
- the specific component page under `components/`
- platform-specific variants for that component
- filter/interval/calibration docs when behavior tuning matters

### Build / troubleshooting
Look for:
- dashboard docs
- logger docs
- board/framework docs
- compile/upload/OTA troubleshooting references

### Reuse / organization
Look for:
- `packages:`
- `substitutions:`
- `secrets:` handling in official docs

## Trigger boundary reminder

Use this skill for ESPHome-specific authoring, review, troubleshooting, and node/dashboard operations.
Do not trigger it for generic YAML or generic embedded questions unless ESPHome-specific behavior materially matters.
