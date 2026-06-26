# FTTR Copilot OpenClaw Skill

This skill connects OpenClaw to the FTTR Copilot terminal cloud-control system through ConnectRPC.

## Configuration

Required:

- `FTTRAI_AUTH_TOKEN`: Customer bearer token for FTTRAI APIs.

Optional:

- `FTTRAI_RPC_URL`: FTTR Copilot ConnectRPC backend base URL, default `https://fms-main.fttrai.com/api/`.
- `FTTRAI_TIMEOUT_MS`: request timeout in milliseconds, default `30000`.
- `FTTRAI_MAX_RETRIES`: retry count for transient failures, default `2`.

## Quick Test

```bash
export FTTRAI_AUTH_TOKEN="your-token"
node src/cli.js list_my_devices
```

```bash
node src/cli.js get_device_detail '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
```

```bash
node src/cli.js get_device_online_status '{"device_identifier":"客厅主网关"}'
```

`update_device_alias` writes to FTTRAI state:

```bash
node src/cli.js update_device_alias '{"device_identifier":"AA:BB:CC:DD:EE:FF","new_alias":"客厅主网关"}'
```

Alert tools:

```bash
node src/cli.js list_device_alerts '{"event_type":"ALARM","limit":20}'
```

Network tools:

```bash
node src/cli.js get_network_topology '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_station_stats '{"device_identifier":"AA:BB:CC:DD:EE:FF","sta_mac":"11:22:33:44:55:66"}'
node src/cli.js get_network_experience '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_station_experience '{"device_identifier":"AA:BB:CC:DD:EE:FF","sta_mac":"11:22:33:44:55:66"}'
```

Customer-scope stats and diagnostics:

```bash
node src/cli.js get_device_stats
node src/cli.js get_fault_counter
node src/cli.js get_device_load '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js diagnose_device_offline '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js diagnose_network_slow '{"device_identifier":"AA:BB:CC:DD:EE:FF","symptom":"卧室网慢"}'
node src/cli.js explain_fttrai_copilot_usage '{"user_goal":"排查离线"}'
```

Real-time Customer device commands:

```bash
node src/cli.js get_master_gateway_info '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_slave_gateway_info '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_agent_version '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
```

## Publish

Dry run:

```bash
clawhub skill publish ./fttr-copilot \
  --slug fttr-copilot \
  --name "FTTR Copilot" \
  --owner <org-handle> \
  --version 0.1.6 \
  --changelog "Implement customer-scope stats, diagnostics, and real-time command tools" \
  --clawscan-note "Uses network access only to call the FTTR Copilot ConnectRPC endpoint. Defaults to https://fms-main.fttrai.com/api/ and can be overridden by FTTRAI_RPC_URL." \
  --dry-run
```

Use the ClawHub organization publisher handle for `--owner`. If `fttr-copilot` was already published under a personal publisher and needs to move into the organization while publishing a new version, add `--migrate-owner`.
