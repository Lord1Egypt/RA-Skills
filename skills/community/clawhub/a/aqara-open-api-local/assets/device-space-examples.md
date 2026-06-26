# Aqara Open API — Device And Space CLI Examples

This file provides CLI examples related to devices and spaces. Explanations and reasoning should be written in English, while field names, paths, and code examples must remain in their original English form.

All examples assume `AQARA_ENDPOINT_URL` and `AQARA_OPEN_API_TOKEN` are available for the current command chain.

If either value is missing, configure the CLI first with `aqara config` or export the environment variables for the current shell. Do not write secrets into persistent shell profile files.

```bash
export AQARA_OPEN_API_TOKEN="your-bearer-token"
export AQARA_ENDPOINT_URL="https://aiot-open-3rd.aqara.cn/open/api"
```

## Device Management

### Load All Devices (cached to file)

This is the primary data source for device queries. Run the cache refresh once; later device and state queries should read `data/devices.json` locally.

The cache file stores the `data` array from `GetAllDevicesWithSpaceRequest`, so the root JSON value is an array of device objects rather than the full API response envelope.

For totals or grouped summaries, scan the full cached device array and count by `deviceId`. Do not count endpoints or traits as devices.

```bash
# Preferred: fetch API data and write data/devices.json
aqara devices cache refresh
```

Do not replace the CLI flow with a direct HTTP call. The package rule is: full-device loading only goes through `aqara devices cache refresh`.

### Get All Device Types

```bash
aqara devices types --json
```

Example response data:

```json
[
  { "deviceType": "Light", "name": "Light" },
  { "deviceType": "Switch", "name": "Switch" },
  { "deviceType": "TemperatureSensor", "name": "Temperature Sensor" }
]
```

### Device Status / Trait Values

No extra API call is needed. Read current values from `data/devices.json` under `endpoints[].functions[].traits[].value`.

Interpret status in layers:

- device level: identity, room, and online or availability fields from the device object
- endpoint or trait level: switch state, brightness, sensor values, and other concrete readings from the matching endpoint/function/trait path

If an `OnOff` trait is `false`, treat the relevant controlled endpoint as off and do not describe brightness or color temperature as if they were actively applied.

### Control Device — Turn On

```bash
aqara devices execute "Living Room Light" \
  --endpoint-id 1 \
  --function-code Output \
  --trait-code OnOff \
  --value true \
  --json
```

### Control Device — Turn Off

```bash
aqara devices execute "Living Room Light" \
  --endpoint-id 1 \
  --function-code Output \
  --trait-code OnOff \
  --value false \
  --json
```

### Control Device — Set Brightness

```bash
aqara devices execute "Living Room Light" \
  --endpoint-id 1 \
  --function-code LevelControl \
  --trait-code CurrentLevel \
  --value 80 \
  --json
```

## Space Management

### List Spaces

```bash
aqara spaces list --json
```

### Create a Top-Level Space

```bash
aqara spaces create --name "My Home" --json
```

### Create a Sub-Space

```bash
aqara spaces create --name "Living Room" --parent-space-id "space_id_123" --spatial-marking living_room --json
```

### Update Space

```bash
aqara spaces update --space-id "space_id_123" --name "New Room Name" --json
```

```bash
aqara spaces update --space-id "space_id_123" --spatial-marking bedroom --json
```

### Assign Devices to Space

```bash
aqara spaces associate --space-id "space_id_123" --device-id "lumi.device.abc123" --device-id "lumi.device.def456" --json
```
