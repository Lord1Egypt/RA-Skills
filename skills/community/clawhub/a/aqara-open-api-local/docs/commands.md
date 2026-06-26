# Aqara Open API CLI Commands

## Global Behavior

- `--json`: emit machine-readable JSON.
- `--raw`: include request/response envelope details for HTTP-backed commands.
- Credentials are resolved from the current shell first, then from the AQARA CLI config file.
- Full device cache refresh is handled inside the Node CLI.

## config

```bash
aqara config show
aqara config set-endpoint "https://aiot-open-3rd.aqara.cn/open/api"
aqara config set-token "your-token"
aqara config clear-endpoint
aqara config clear-token
```

Behavior:

- default config file path: `~/.aqa/config.json`
- environment variables `AQARA_ENDPOINT_URL` and `AQARA_OPEN_API_TOKEN` still have higher priority than the config file
- `config show` masks the token instead of printing the raw secret

## doctor

```bash
aqara doctor
aqara doctor --json
aqara doctor --ping --json
```

Checks:

- Node runtime
- package root
- config file path
- whether endpoint/token are configured
- whether built-in `fetch` is available
- whether `data/devices.json` exists

`--ping` additionally sends `GetSpacesRequest`.

## devices

### Cache

```bash
aqara devices cache refresh
aqara devices cache info --json
```

Behavior:

- `aqara devices cache refresh` sends `GetAllDevicesWithSpaceRequest`
- the CLI validates that `response.data` is a JSON array
- the CLI writes the array directly to `data/devices.json`

### List devices

```bash
aqara devices list
aqara devices list --room "Living Room"
aqara devices list --type Light --trait-code OnOff
aqara devices list --writable --json
aqara devices list --online true --refresh --json
```

Supported filters:

- `--room`
- `--type`
- `--name`
- `--online true|false`
- `--trait-code`
- `--writable`
- `--readable`
- `--reportable`
- `--refresh`

### Inspect one device

```bash
aqara devices inspect "Living Room Light"
aqara devices inspect lumi.device.abc123 --json
aqara devices inspect "Living Room Light" --room "Living Room" --raw --json
```

### List traits on one device

```bash
aqara devices traits "Living Room Light"
aqara devices traits "Living Room Light" --writable --json
aqara devices traits "Living Room Light" --trait-code CurrentLevel --json
```

### Get device type catalog

```bash
aqara devices types --json
```

### Execute trait

```bash
aqara devices execute "Living Room Light" \
  --trait-code OnOff \
  --value true

aqara devices execute "Desk Lamp" \
  --endpoint-id 1 \
  --function-code LevelControl \
  --trait-code CurrentLevel \
  --value 80 \
  --json
```

Rules:

- device selection still comes from cache
- the CLI resolves the target trait tuple from cache before sending `ExecuteTraitRequest`
- when `traitCode` is unique on the device, `--function-code` and `--endpoint-id` may be omitted
- if multiple tuples match the same `traitCode`, provide `--function-code` and/or `--endpoint-id`
- `--value` accepts JSON literals, booleans, numbers, or plain strings

## spaces

### List

```bash
aqara spaces list --json
```

### Create

```bash
aqara spaces create --name "Living Room"
aqara spaces create --name "Master Bedroom" --spatial-marking bedroom --parent-space-id home_id_123 --json
```

### Update

```bash
aqara spaces update --space-id space_id_123 --name "Study Room"
aqara spaces update --space-id space_id_123 --spatial-marking study --json
```

### Associate devices

```bash
aqara spaces associate --space-id space_id_123 --device-id lumi.device.abc123
aqara spaces associate --space-id space_id_123 --device-id lumi.device.abc123 --device-id lumi.device.def456 --json
```

## automations

### Capabilities

```bash
aqara automations capabilities --json
aqara automations capabilities --data-json "{}" --raw --json
aqara automations capabilities --data-file ./payloads/capabilities.json --json
```

### List and inspect

```bash
aqara automations list --json
aqara automations list --page-num 2 --page-size 20 --order-by "createTime desc" --json
aqara automations get auto_abc123 --json
```

### Create

```bash
aqara automations validate --config-file ./references/stand.automation-instance.json --json
aqara automations validate --config-file ./references/manual-instance.json --json
aqara automations create --config-file ./references/stand.automation-instance.json --json
aqara automations create --config-json "{\"metadata\":{\"name\":\"Demo\"},\"automations\":[]}" --definition-type SCRIPT_JSON --json
```

### Generate from intent

```bash
aqara automations generate motion-light --room "Study" --json
aqara automations generate motion-light --room "Study" --sensor "Study Motion Sensor" --light "Study Ceiling Light" --after 18:00 --before 06:00 --output-file ./tmp/study-motion-light.json --json
aqara automations generate manual-scene --room "Living Room" --value true --scene-name "Arrive Home" --json
aqara automations generate manual-scene-off --room "Living Room" --json
aqara automations generate manual-scene-off --room "Living Room" --target "Desk Lamp" --target "Wall Switch" --scene-name "Leave Home" --output-file ./tmp/living-room-off.json --json
aqara automations create-from-intent motion-light --room "Study" --json
aqara automations create-from-intent manual-scene --room "Living Room" --value false --scene-name "Leave Home" --json
aqara automations create-from-intent manual-scene-off --room "Living Room" --json
```

Behavior:

- currently supports the `motion-light` template
- currently supports the `manual-scene` template
- currently supports the `manual-scene-off` template
- only uses already retrieved device evidence from `data/devices.json`; it must not guess missing rooms or devices
- resolves the motion source from `OccupancySensing/Occupancy`
- resolves controllable targets from `Output/OnOff`
- prefers `Light` devices in the room; if none are present, falls back to any room device that supports `Output/OnOff`
- `manual-scene` writes a manual starter and applies the requested `--value` to room targets that support `Output/OnOff`
- `manual-scene-off` targets every room device that supports `Output/OnOff` unless you pass explicit `--target` selectors
- `manual-scene-off` creates a `starters: [{ \"type\": \"manual\", \"name\": ... }]` branch and does not require `metadata.scope`
- `generate` only builds JSON locally and can optionally write it via `--output-file`
- `create-from-intent` runs generation, validation, and then submits `CreateAutomationRequest`
- `--after` and `--before` apply a `time.between` condition to the occupied -> lights on branch
- when multiple motion sensors match the room, pass `--sensor` explicitly
- pass repeated `--light` flags or a comma-separated value list to target specific devices
- pass repeated `--target` flags or a comma-separated value list to constrain `manual-scene-off` targets
- if the requested room is absent from retrieved evidence, the command fails instead of falling back to a different room
- if the requested room has no matching occupancy sensor or no eligible targets, the command fails and asks for clarification instead of rewriting the intent

### Validate config

```bash
aqara automations validate --config-file ./references/stand.automation-instance.json --json
aqara automations validate --config-file ./references/manual-instance.json --json
aqara automations validate --config-json "{\"metadata\":{\"name\":\"Demo\",\"scope\":[]},\"automations\":[]}" --json
```

Validation behavior:

- checks the schema-first subset used by the current automation skill
- rejects forbidden fields such as `operator` and `fieldCode`
- validates `metadata.scope` and action targets against real identifiers from `data/devices.json`
- supports `starters.type = "manual"` with a required starter `name`
- allows `metadata.scope` to be omitted for pure manual-trigger automations that do not use `data.ref`
- validates generated configs from `generate` / `create-from-intent` with the same rules
- `create` and `update` run this validation automatically before submission

### Update config

```bash
aqara automations update auto_abc123 --config-file ./references/stand.automation-instance.json --json
```

### Rename

```bash
aqara automations rename auto_abc123 --name "Night Mode" --json
```

### Enable / disable

```bash
aqara automations enable auto_abc123 auto_def456 --json
aqara automations disable auto_abc123 --json
```

### Delete

```bash
aqara automations delete auto_abc123 --json
aqara automations delete auto_abc123 auto_def456 --json
```

## traits

### List trait catalog

```bash
aqara traits list
aqara traits list --writable --json
aqara traits list --value-type number --reportable --json
```

### Search trait catalog

```bash
aqara traits search OnOff
aqara traits search Temperature --json
```

The `traits` command reads `assets/trait-codes.md` as a reference catalog. It is a display and filtering layer, not a runtime truth source.
