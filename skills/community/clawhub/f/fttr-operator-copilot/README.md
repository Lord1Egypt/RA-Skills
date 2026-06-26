# FTTR Operator Copilot OpenClaw Skill

This skill connects OpenClaw to FTTRAI Operator ConnectRPC APIs.

## Configuration

Required:

- `FTTRAI_OPERATOR_AUTH_TOKEN`: Operator bearer token for FTTRAI APIs.

Optional:

- `FTTRAI_RPC_URL`: backend base URL, default `https://fms-main.fttrai.com/api/`.
- `FTTRAI_TIMEOUT_MS`: request timeout in milliseconds, default `30000`.
- `FTTRAI_MAX_RETRIES`: retry count for transient failures, default `2`.

## Quick Test

```bash
export FTTRAI_OPERATOR_AUTH_TOKEN="your-operator-token"
node src/cli.js list_devices '{"limit":5}'
node src/cli.js get_device_stats '{"region_code":"440000"}'
node src/cli.js list_device_alerts '{"event_type":"ALARM","limit":20}'
```

## Publish

```bash
clawhub skill publish ./fttr-operator-copilot \
  --slug fttr-operator-copilot \
  --name "FTTR Operator Copilot" \
  --owner <org-handle> \
  --version 0.1.0 \
  --changelog "Initial Operator skill with managed-device, alert, stats, diagnostics, and command tools" \
  --clawscan-note "Uses network access only to call the FTTR Copilot Operator ConnectRPC endpoint. Defaults to https://fms-main.fttrai.com/api/ and can be overridden by FTTRAI_RPC_URL. Real-time command tools call Operator-authorized device query commands and may return sequence_id when results are pending." \
  --dry-run
```
