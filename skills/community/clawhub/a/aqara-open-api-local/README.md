# Aqara Open API CLI

Node.js CLI for Aqara Open Platform devices, spaces, automations, and trait catalog workflows.

## Features

- Covers the current Aqara Open API surface already modeled by this package:
  - device cache refresh and cache-driven device inspection
  - trait execution via `ExecuteTraitRequest`
  - space list/create/update/associate
  - automation capabilities, generate, create-from-intent, list/get/create/update/rename/enable/disable/delete
  - local trait catalog search based on `assets/trait-codes.md`
- Reuses the package's existing runtime contract:
  - `AQARA_ENDPOINT_URL`
  - `AQARA_OPEN_API_TOKEN`
  - fallback to the AQARA CLI config file
- Handles full device cache refresh inside the Node CLI and writes `data/devices.json` directly.

## Requirements

- Node.js `>=18`

## Credentials

The CLI resolves credentials in this order:

1. `AQARA_ENDPOINT_URL` and `AQARA_OPEN_API_TOKEN` from the current shell
2. the AQARA CLI config file at `~/.aqa/config.json`

Recommended method-based setup:

```bash
aqara config set-endpoint "https://aiot-open-3rd.aqara.cn/open/api"
aqara config set-token "your-token"
aqara config show
```

## Quick Start

```bash
aqara doctor
aqara config show
aqara devices cache refresh
aqara devices list --json
aqara devices traits "Living Room Light" --writable
aqara spaces list --json
aqara automations list --json
```

### Config

```bash
aqara config show
aqara config set-endpoint "https://aiot-open-3rd.aqara.cn/open/api"
aqara config set-token "your-token"
aqara config clear-token
```

## Common Commands

### Device cache

```bash
aqara devices cache refresh
aqara devices cache info --json
```

`aqara devices cache refresh` calls `GetAllDevicesWithSpaceRequest` inside the CLI and writes the returned `data` array into `data/devices.json`.

### Device discovery and inspection

```bash
aqara devices list --room "Living Room" --type Light
aqara devices inspect "Living Room Light" --json
aqara devices traits "Living Room Light" --writable --json
aqara traits search OnOff
```

### Device control

```bash
aqara devices execute "Living Room Light" \
  --trait-code OnOff \
  --value true
```

When `traitCode` is unique on the target device, the CLI can auto-resolve `endpointId` and `functionCode` from cache. If the trait is ambiguous, add `--function-code` and/or `--endpoint-id`.

### Spaces

```bash
aqara spaces create --name "Living Room" --spatial-marking living_room --json
aqara spaces update --space-id space_id_123 --name "Study Room" --json
aqara spaces associate --space-id space_id_123 --device-id lumi.device.abc123 --device-id lumi.device.def456 --json
```

### Automations

```bash
aqara automations validate --config-file ./references/stand.automation-instance.json --json
aqara automations validate --config-file ./references/manual-instance.json --json
aqara automations generate motion-light --room "Study" --json
aqara automations generate manual-scene --room "Living Room" --value true --scene-name "Arrive Home" --json
aqara automations generate manual-scene-off --room "Living Room" --json
aqara automations create-from-intent motion-light --room "Study" --json
aqara automations create-from-intent manual-scene --room "Living Room" --value false --scene-name "Leave Home" --json
aqara automations create-from-intent manual-scene-off --room "Living Room" --json
aqara automations capabilities --json
aqara automations list --page-size 20 --json
aqara automations get auto_abc123 --json
aqara automations create --config-file ./references/stand.automation-instance.json --json
aqara automations update auto_abc123 --config-file ./references/stand.automation-instance.json --json
aqara automations rename auto_abc123 --name "Night Mode" --json
aqara automations enable auto_abc123 auto_def456 --json
aqara automations delete auto_abc123 --json
```

`aqara automations generate motion-light` builds a cache-backed automation config for the common occupied-on / unoccupied-off lighting pattern. It auto-selects an `OccupancySensing/Occupancy` sensor and `Output/OnOff` light targets from the given room unless you override them with `--sensor` and `--light`.

`aqara automations generate manual-scene` builds a manual-trigger scene for room devices exposing `Output/OnOff`, using the requested `--value true|false`.

`aqara automations generate manual-scene-off` builds a manual-trigger scene that turns off every room device exposing `Output/OnOff`, unless you override the target set with `--target`.

`aqara automations create-from-intent motion-light` runs the same generation flow, validates the generated config locally, and then submits `CreateAutomationRequest`.

`aqara automations create-from-intent manual-scene` does the same for a generic manual On/Off scene.

`aqara automations create-from-intent manual-scene-off` does the same for a manual-trigger off scene.

The generator is evidence-gated: it only uses rooms and devices already present in retrieved device evidence. If the requested room is missing, has no devices, or has no eligible trigger/target devices, the command fails instead of silently falling back to another room.

`aqara automations validate`, `create`, and `update` also support manual-trigger automations with `starters.type = "manual"`. For pure manual-trigger automations, `metadata.scope` may be omitted when no `data.ref` starter source is used.

`aqara automations create` and `aqara automations update` still validate the submitted config against the CLI's schema-first rules and cache-backed identifier checks before sending the final API request.

## Command Reference

See `docs/commands.md` for the full command catalog.
