---
name: fttr-operator-copilot
description: Connect OpenClaw to the FTTR Copilot operator cloud-control APIs through ConnectRPC for managed-device lookup, alert operations, regional stats, network diagnostics, and real-time FTTR query commands.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env:
        - FTTRAI_OPERATOR_AUTH_TOKEN
      bins:
        - node
    primaryEnv: FTTRAI_OPERATOR_AUTH_TOKEN
    envVars:
      - name: FTTRAI_RPC_URL
        required: false
        description: Base URL of the FTTR Copilot ConnectRPC backend. Defaults to https://fms-main.fttrai.com/api/.
      - name: FTTRAI_OPERATOR_AUTH_TOKEN
        required: true
        description: Operator bearer token used to call FTTRAI operator APIs.
      - name: FTTRAI_TIMEOUT_MS
        required: false
        description: RPC timeout in milliseconds. Defaults to 30000.
      - name: FTTRAI_MAX_RETRIES
        required: false
        description: Retry count for transient RPC failures. Defaults to 2.
---

# FTTR Operator Copilot

Use this skill when a user asks OpenClaw to query or operate FTTR Copilot data with an Operator identity.

## Runtime

Run the bundled CLI from this skill directory:

```bash
node src/cli.js <tool> [json-arguments]
```

The CLI always prints JSON. Successful calls use:

```json
{
  "ok": true,
  "title": "...",
  "summary": "...",
  "data": {},
  "suggestions": [],
  "trace": []
}
```

## Available Tools

- `list_devices`: List Operator-managed devices with filters such as region, MAC, SN, online status, kind, activation state, and fault code.
- `get_device_detail`: Get Operator device detail by device ID, MAC address, or SN.
- `get_device_online_status`: Get online status by device ID, MAC address, or SN.
- `list_device_alerts`: List Operator-visible alerts, optionally filtered by device, region, event type, event code, cursor, and limit.
- `get_alert_detail`: Get one alert detail by alert ID.
- `calculate_alert_number`: Count total and unread alerts for one or more devices.
- `mark_alerts_as_read`: Mark alert IDs as read. This writes to FTTRAI state.
- `get_network_topology`: Get gateway and station topology for a master gateway.
- `get_station_stats`: Get station metrics for all stations or one station.
- `get_station_metrics`: Alias of `get_station_stats` for detailed station metrics.
- `get_network_experience`: Get network score and experience trends.
- `get_station_experience`: Get RSSI history for one station.
- `get_device_stats`: Get Operator regional device summary stats.
- `get_device_load`: Get device load trends through admin charts. Supported `load_type`: `basic`, `optic`, `wireless_rssi`, `wireless_loads`, `station_rssi`, `station_counter`.
- `get_fault_counter`: Get Operator regional fault stats.
- `get_master_gateway_info`: Send an Operator-authorized real-time query command for FMU information.
- `get_slave_gateway_info`: Send an Operator-authorized real-time query command for FSU information.
- `get_agent_version`: Send an Operator-authorized real-time query command for Agent version.
- `diagnose_device_offline`: Combine detail, online status, and Operator-visible alerts for offline diagnosis.
- `diagnose_network_slow`: Combine detail, topology, network experience, and station metrics for network-slow diagnosis.
- `explain_fttrai_copilot_usage`: Explain available Operator capabilities, required inputs, and example prompts.

## Usage Guidance

- Prefer device ID, MAC address, SN, or region code when asking follow-up questions.
- Operator tools are scoped by the token user's region and permissions.
- `mark_alerts_as_read` writes state; confirm intent before using it.
- Real-time command tools send device query commands and may return a `sequence_id` when the device has not returned a result yet.
- Do not invent FTTR operating procedures. If live FTTRAI data is insufficient, say what is missing and ask for the next identifier or symptom.
- Keep answers in Chinese unless the user asks otherwise.

## Examples

```bash
node src/cli.js list_devices '{"region_code":"440000","online_status":"OFFLINE","limit":20}'
node src/cli.js get_device_detail '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js list_device_alerts '{"region_code":"440000","event_type":"ALARM","limit":20}'
node src/cli.js get_alert_detail '{"alert_id":"00000000-0000-4000-8000-000000000000"}'
node src/cli.js calculate_alert_number '{"device_identifiers":["AA:BB:CC:DD:EE:FF"]}'
node src/cli.js mark_alerts_as_read '{"alert_ids":["00000000-0000-4000-8000-000000000000"]}'
node src/cli.js get_device_stats '{"region_code":"440000"}'
node src/cli.js get_fault_counter '{"region_code":"440000"}'
node src/cli.js get_device_load '{"device_identifier":"AA:BB:CC:DD:EE:FF","load_type":"basic"}'
node src/cli.js get_network_topology '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_master_gateway_info '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js diagnose_network_slow '{"device_identifier":"AA:BB:CC:DD:EE:FF","symptom":"卧室网慢"}'
```
