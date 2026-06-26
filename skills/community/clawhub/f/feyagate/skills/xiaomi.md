---
name: feyagate-xiaomi
description: Xiaomi/Mi Home platform tools. MIOT device control, OAuth auth, camera P2P, XiaoAI speaker TTS/music. Use when controlling Xiaomi devices, cameras, or XiaoAI speakers.
version: 1.2.31
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# Xiaomi Platform Tools

> **Parent skill:** [SKILL.md](../SKILL.md) — provides cross-platform tools (`device/list`, `device/specs`, `platform/status`, `gateway/info`) and MCP endpoint config.

## Device Control

| Tool | Arguments | Returns |
|------|-----------|---------|
| `xiaomi/get_properties` | `device_id` (string), `siid` (int/string), `piids` (int[]) | Property values |
| `xiaomi/set_property` | `device_id` (string), `siid` (int/string), `piid` (int/string), `value` | Control result |
| `xiaomi/execute_action` | `device_id` (string), `siid` (int/string), `aiid` (int/string), `params` (opt) | Action result |

**Workflow (step 1-2 use parent skill tools):**
1. `device/list` with `{"filter": ["keyword"], "platform": "xiaomi"}` → find target device
2. `device/specs` with `{"deviceId": "xxx"}` → get `siid`/`piid`/`aiid` definitions
3. `xiaomi/get_properties` → read current values
4. `xiaomi/set_property` → set property value

**`xiaomi/set_property` example:**
```json
{
  "name": "xiaomi/set_property",
  "arguments": {"device_id": "1234567890", "siid": "2", "piid": "1", "value": true}
}
```

## Auth & Device Management (PC proxy extensions)

| Tool | Arguments | Returns |
|------|-----------|---------|
| `xiaomi/auth_status` | — | `authorized`, `remaining_seconds`, `cloud_server` |
| `xiaomi/auth_url` | — | OAuth login URL |
| `xiaomi/auth_callback` | `code` | Token exchange result |
| `xiaomi/refresh` | — | Re-fetch devices from cloud |
| `xiaomi/get_area_info` | — | `areas[]`, `total_areas` |
| `xiaomi/get_device_classes` | — | `device_classes[]` with counts |
| `xiaomi/get_devices` | `area_id`, `device_class` (opt) | `devices[]`, `count` |

### OAuth Flow

```bash
# 1. Get OAuth URL
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"xiaomi/auth_url","arguments":{}}}'

# 2. Open URL in browser → login → copy redirect URL → extract code

# 3. Submit code
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"xiaomi/auth_callback","arguments":{"code":"YOUR_CODE"}}}'

# 4. Verify
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"xiaomi/auth_status","arguments":{}}}'

# Or use auth.py script
python3 scripts/auth.py              # Interactive
python3 scripts/auth.py --status     # Check status
```

## Camera Control (PC proxy extensions)

| Tool | Arguments | Returns |
|------|-----------|---------|
| `xiaomi/camera_list` | — | `cameras[]` with metadata |
| `xiaomi/camera_status` | `camera_id` (opt) | Connection status, `buffered_frames` |
| `xiaomi/camera_connect` | `camera_id` | Start P2P stream |
| `xiaomi/camera_disconnect` | `camera_id` | Stop stream |
| `xiaomi/camera_snapshot` | `camera_id`, `channel` (opt), `count` (opt) | `images[]` (base64 JPEG) |
| `xiaomi/camera_vision_chat` | `camera_id`, `query` | AI vision analysis |

**Camera workflow:**
1. `xiaomi/camera_list` → discover cameras
2. `xiaomi/camera_connect` → establish P2P connection (wait 3-5s)
3. `xiaomi/camera_snapshot` → capture JPEG frames
4. `xiaomi/camera_disconnect` → release connection when done

## XiaoAI Speaker Control

| Tool | Arguments | Returns |
|------|-----------|---------|
| `xiaoai/tts` | `device_id`, `text` | TTS playback result |
| `xiaoai/play_music` | `device_id`, `text` | Music playback result |
| `xiaoai/control` | `device_id`, `command`, `silence` (opt) | Voice command result |

```json
{"name": "xiaoai/control", "arguments": {"device_id": "xxx", "command": "打开客厅灯", "silence": true}}
```
