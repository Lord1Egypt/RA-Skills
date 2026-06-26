---
name: extension
description: Hardware extension tools. Serial (RS485/UART), GPIO, Xiaozhi AI, license, config, stats.
version: 1.2.31
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# Hardware Extension & Integration Tools

> **Parent skill:** [SKILL.md](../SKILL.md) — provides cross-platform tools and MCP endpoint config.

## Serial Extension

| Tool | Arguments | Returns |
|------|-----------|---------|
| `serial/get_properties` | `device_id`, `siid`, `piids` | Property values |
| `serial/set_property` | `device_id`, `siid`, `piid`, `value` | Set result |
| `serial/execute_action` | `device_id`, `siid`, `aiid` | Action result |

## GPIO Extension

| Tool | Arguments | Returns |
|------|-----------|---------|
| `gpio/get_properties` | `device_id`, `siid`, `piids` | Property values |
| `gpio/set_property` | `device_id`, `siid`, `piid`, `value` | Set result |
| `gpio/execute_action` | `device_id`, `siid`, `aiid` | Action result |

## Xiaozhi AI Platform

| Tool | Arguments | Returns |
|------|-----------|---------|
| `xiaozhi/status` | — | Connection state |
| `xiaozhi/set_endpoint` | `endpoint` | Set WebSocket URL |

## System Tools

### License

| Tool | Arguments | Returns |
|------|-----------|---------|
| `license/status` | — | `edition`, `status`, `guidance` |
| `license/set` | `license_key`, `product` (opt) | Activation result |
| `license/clear` | — | Clear result |

### Configuration

| Tool | Arguments | Returns |
|------|-----------|---------|
| `config/get_vision` | — | Vision AI settings |
| `config/set_vision` | `enabled`, `api_key`, `model`, etc. | Update result |
| `config/get_trigger` | — | Trigger engine settings |
| `config/set_trigger` | `enabled`, `interval_seconds`, etc. | Update result |

### Statistics

| Tool | Arguments | Returns |
|------|-----------|---------|
| `stats/token_usage` | `days` (opt) | Token usage summary |
| `stats/token_records` | `limit` (opt) | Recent records |
| `stats/trigger_summary` | `days` (opt) | Trigger statistics |
| `stats/dashboard` | — | Full dashboard data |
