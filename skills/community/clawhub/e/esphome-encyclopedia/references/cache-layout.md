# `.ESPHome-Encyclopedia/` Cache Layout

Use this directory as the workspace-local data root for the skill.

## Directory tree

```text
.ESPHome-Encyclopedia/
  docs/
    esphome.io/
      ... cached official ESPHome docs pages ...
  notes/
    devices/
      ... per-device notes ...
    components/
      ... per-component notes ...
    patterns/
      ... reusable ESPHome notes ...
  inventory/
    access.md
    topology.md
    doc-index.md
```

## Placement rules

### `docs/`
Store cached copies of official ESPHome docs pages here.

Mirror the official path as much as practical.
Example:

```text
https://esphome.io/components/sensor/index.html
->
.ESPHome-Encyclopedia/docs/esphome.io/components/sensor/index.md
```

### `notes/devices/`
Store environment-specific node/device notes here.

Suggested filenames:
- `garage-door.md`
- `living-room-display.md`
- `weather-station.md`

### `notes/components/`
Store component-specific observations here.

Suggested filenames:
- `wifi.md`
- `api.md`
- `esp32.md`
- `logger.md`
- `packages.md`

### `notes/patterns/`
Store reusable operational notes here.

Examples:
- `ota-recovery.md`
- `substitutions-patterns.md`
- `wifi-fallback-ap.md`
- `sensor-filter-gotchas.md`

### `inventory/`
Store environment-wide inventories here.

Suggested files:
- `access.md`
- `topology.md`
- `doc-index.md`

## Cache philosophy

Do not mirror the whole docs site eagerly.
Cache only the pages you actually consulted and expect to be useful later.
