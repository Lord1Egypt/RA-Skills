---
name: fttr-copilot
description: Connect OpenClaw to the FTTR Copilot cloud-control system through ConnectRPC for device lookup, alert triage, network diagnostics, and FTTR operations.
version: 0.1.6
metadata:
  openclaw:
    requires:
      env:
        - FTTRAI_AUTH_TOKEN
      bins:
        - node
    primaryEnv: FTTRAI_AUTH_TOKEN
    envVars:
      - name: FTTRAI_RPC_URL
        required: false
        description: Base URL of the FTTR Copilot ConnectRPC backend. Defaults to https://fms-main.fttrai.com/api/.
      - name: FTTRAI_AUTH_TOKEN
        required: true
        description: Customer bearer token used to call FTTRAI APIs.
      - name: FTTRAI_TIMEOUT_MS
        required: false
        description: RPC timeout in milliseconds. Defaults to 30000.
      - name: FTTRAI_MAX_RETRIES
        required: false
        description: Retry count for transient RPC failures. Defaults to 2.
---

# FTTR Copilot

Use this skill when a user asks OpenClaw to query or diagnose FTTR Copilot terminal cloud-control data.

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

Failed calls use:

```json
{
  "ok": false,
  "error": {
    "code": "...",
    "message": "...",
    "procedure": "..."
  }
}
```

## Available Tools

Current implementation:

- `list_my_devices`: List devices bound to the authenticated customer.
- `get_device_detail`: Get device detail by device ID, MAC address, or alias.
- `get_device_online_status`: Get online status by device ID, MAC address, or alias.
- `update_device_alias`: Update a device alias. This writes to FTTRAI state.
- `list_device_alerts`: List alerts for devices bound to the authenticated customer, optionally filtered by event type, event code, cursor, and limit.
- `get_network_topology`: Get gateway and station topology for a master gateway.
- `get_station_stats`: Get station metrics for all stations or one station.
- `get_station_metrics`: Alias of `get_station_stats` for detailed station metrics.
- `get_network_experience`: Get network score and experience trends.
- `get_station_experience`: Get RSSI history for one station.
- `get_device_stats`: Summarize devices bound to the authenticated customer, including online/offline and fault-code counts.
- `get_device_load`: Get basic device load and profile data from device detail, including CPU, memory, reset/offline reason, and fault codes.
- `get_fault_counter`: Count fault codes across devices bound to the authenticated customer.
- `get_master_gateway_info`: Send a Customer-authorized real-time command to query FMU information.
- `get_slave_gateway_info`: Send a Customer-authorized real-time command to query FSU information.
- `get_agent_version`: Send a Customer-authorized real-time command to query Agent version.
- `diagnose_device_offline`: Combine detail, online status, and customer-scope alerts for offline diagnosis.
- `diagnose_network_slow`: Combine detail, topology, network experience, and station metrics for network-slow diagnosis.
- `explain_fttrai_copilot_usage`: Explain available capabilities, required user inputs, and example prompts.

## Usage Guidance

- Prefer device ID, MAC address, or user-visible alias when asking follow-up questions.
- Treat real-time command tools as device commands; they may return a `sequence_id` when the device has not returned a result yet.
- Do not invent FTTR operating procedures. If live FTTRAI data is insufficient, say what is missing and ask for the next identifier or symptom.
- Keep answers in Chinese unless the user asks otherwise.

## Examples

List bound devices:

```bash
node src/cli.js list_my_devices
```

Equivalent explicit empty arguments:

```bash
node src/cli.js list_my_devices '{}'
```

Get device detail:

```bash
node src/cli.js get_device_detail '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
```

Update alias:

```bash
node src/cli.js update_device_alias '{"device_identifier":"AA:BB:CC:DD:EE:FF","new_alias":"客厅主网关"}'
```

List alerts:

```bash
node src/cli.js list_device_alerts '{"event_type":"ALARM","limit":20}'
```

Get topology and network experience:

```bash
node src/cli.js get_network_topology '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_station_stats '{"device_identifier":"AA:BB:CC:DD:EE:FF","sta_mac":"11:22:33:44:55:66"}'
node src/cli.js get_network_experience '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_station_experience '{"device_identifier":"AA:BB:CC:DD:EE:FF","sta_mac":"11:22:33:44:55:66"}'
```

Get customer-scope stats and run diagnostics:

```bash
node src/cli.js get_device_stats
node src/cli.js get_fault_counter
node src/cli.js get_device_load '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js diagnose_device_offline '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js diagnose_network_slow '{"device_identifier":"AA:BB:CC:DD:EE:FF","symptom":"卧室网慢"}'
```

Run real-time device commands:

```bash
node src/cli.js get_master_gateway_info '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_slave_gateway_info '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_agent_version '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
```
