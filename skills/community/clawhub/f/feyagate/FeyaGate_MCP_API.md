# FeyaGate MCP API 文档

> **适用产品**: miloco-mcp-server (桌面版虚拟网关)
> **协议**: MCP (Model Context Protocol) JSON-RPC 2.0
> **MCP 端点**: `POST http://<网关IP>:38080/mcp/http`
> **协议版本**: `2025-03-26`

---

## 目录

- [1. 连接指南](#1-连接指南)
- [2. JSON-RPC 2.0 规范](#2-json-rpc-20-规范)
- [3. 协议方法](#3-协议方法)
- [4. MCP Tools 总览 (76 个)](#4-mcp-tools-总览-76-个)
- [5. 通用设备工具](#5-通用设备工具)
- [6. 小米 (Xiaomi) 平台](#6-小米-xiaomi-平台)
- [7. 涂鸦 (Tuya) 平台](#7-涂鸦-tuya-平台)
- [8. 美的 (Midea) 平台](#8-美的-midea-平台)
- [9. 易微联 (eWeLink) 平台](#9-易微联-ewelink-平台)
- [10. 小爱音箱控制](#10-小爱音箱控制)
- [11. 小智平台](#11-小智平台)
- [12. 认证与平台管理](#12-认证与平台管理)
- [13. Vision AI](#13-vision-ai)
- [14. 触发规则](#14-触发规则)
- [15. 定时任务](#15-定时任务)
- [16. 技能系统](#16-技能系统)
- [17. 配置管理](#17-配置管理)
- [18. 统计数据](#18-统计数据)
- [19. 授权码管理](#19-授权码管理)
- [20. 网关信息](#20-网关信息)
- [21. 错误码](#21-错误码)
- [附录: 快速示例](#附录-快速示例)

---

## 1. 连接指南

所有 MCP 调用均通过 `POST /mcp/http` 以 JSON-RPC 2.0 格式发送，无需事先握手。

```bash
# 初始化
curl -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"MyClient","version":"1.0.0"}}}'

# 列出所有工具
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

> **无状态**: 服务器不维持 HTTP 会话状态，不返回 `Mcp-Session-Id` header，每次请求均为无状态调用。
>
> **无 WebSocket**: 服务器不提供 inbound WebSocket 端点。`/mcp` WebSocket 路径不存在。服务器作为 WebSocket **客户端**主动连接小智平台，由 `xiaozhi/*` 工具管理。

---

## 2. JSON-RPC 2.0 规范

### 请求结构

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "<工具名>",
    "arguments": { ... }
  }
}
```

### 成功响应

工具返回值被包装为 MCP content 格式：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      { "type": "text", "text": "{\"success\":true,...}" }
    ]
  }
}
```

> 工具返回的 JSON 对象会被序列化为字符串放在 `content[0].text` 中。

### 图片响应

当工具返回含 `images` 数组（含 `data_url` 字段）的结果时，服务器会自动提取图片为独立的 MCP image content：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      { "type": "text", "text": "{\"camera_id\":\"xxx\",\"images\":[...]}" },
      { "type": "image", "data": "<base64>", "mimeType": "image/jpeg" }
    ]
  }
}
```

### 错误响应

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": { "code": -32601, "message": "Tool not found: unknown/tool" }
}
```

### 工具执行异常

当工具 handler 抛出异常时，返回 `isError: true`：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      { "type": "text", "text": "{\"error\":\"exception message\"}" }
    ],
    "isError": true
  }
}
```

---

## 3. 协议方法

| 方法 | 说明 |
|------|------|
| `initialize` | MCP 协议握手 |
| `ping` | 保活心跳 |
| `tools/list` | 列出所有已注册工具 |
| `tools/call` | 调用指定工具 |
| `notifications/initialized` | 初始化完成通知（无响应） |

### initialize

```json
{
  "jsonrpc": "2.0", "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": {},
    "clientInfo": { "name": "MyClient", "version": "1.0.0" }
  }
}
```

**响应**:
```json
{
  "jsonrpc": "2.0", "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",
    "capabilities": { "tools": {}, "resources": {} },
    "serverInfo": { "name": "miloco-mcp-server", "version": "1.0.0" }
  }
}
```

### ping

```json
{ "jsonrpc": "2.0", "id": 1, "method": "ping", "params": {} }
```

**响应**:
```json
{ "jsonrpc": "2.0", "id": 1, "result": {} }
```

### tools/list

```json
{ "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {} }
```

**响应**:
```json
{
  "jsonrpc": "2.0", "id": 1,
  "result": {
    "tools": [
      {
        "name": "device/list",
        "description": "获取所有已认证平台的设备列表...",
        "inputSchema": { "type": "object", "properties": { ... } }
      }
    ]
  }
}
```

### tools/call

```json
{
  "jsonrpc": "2.0", "id": 1,
  "method": "tools/call",
  "params": {
    "name": "device/list",
    "arguments": { "filter": ["客厅", "灯"], "platform": "xiaomi" }
  }
}
```

---

## 4. MCP Tools 总览 (76 个)

> **参数命名规则**:
> - 跨平台统一工具 (`device/list`, `device/specs`) 使用 `snake_case`（如 `device_id`）
> - 平台专属工具使用 `camelCase`（如 `deviceId`, `siid`, `piids`）

| # | 工具名 | 类别 | 必填参数 |
|---|--------|------|----------|
| 1 | `device/list` | 通用设备 | — |
| 2 | `device/specs` | 通用设备 | `device_id` |
| 3 | `xiaomi/auth_status` | 小米认证 | — |
| 4 | `xiaomi/auth_url` | 小米认证 | — |
| 5 | `xiaomi/auth_callback` | 小米认证 | `code` |
| 6 | `xiaomi/refresh` | 小米设备 | — |
| 7 | `xiaomi/get_devices` | 小米设备 | — |
| 8 | `xiaomi/get_area_info` | 小米设备 | — |
| 9 | `xiaomi/get_device_classes` | 小米设备 | — |
| 10 | `get_xiaomi_device_properties` | 小米控制 | `deviceId`, `siid`, `piids` |
| 11 | `set_xiaomi_device_property` | 小米控制 | `deviceId`, `siid`, `piid`, `value` |
| 12 | `execute_xiaomi_device_action` | 小米控制 | `deviceId`, `siid`, `aiid` |
| 13 | `xiaomi/scene_list` | 小米场景 | — |
| 14 | `xiaomi/scene_trigger` | 小米场景 | `sceneId` |
| 15 | `xiaomi/camera_list` | 摄像头 | — |
| 16 | `xiaomi/camera_status` | 摄像头 | — |
| 17 | `xiaomi/camera_connect` | 摄像头 | `camera_id` |
| 18 | `xiaomi/camera_disconnect` | 摄像头 | `camera_id` |
| 19 | `xiaomi/camera_snapshot` | 摄像头 | `camera_id` |
| 20 | `xiaomi/camera_vision_chat` | Vision AI | `camera_id`, `query` |
| 21 | `xiaoai/play_music` | 小爱音箱 | `device_id` |
| 22 | `xiaoai/tts` | 小爱音箱 | `device_id`, `text` |
| 23 | `xiaoai/control` | 小爱音箱 | `device_id`, `command` |
| 24 | `xiaozhi/status` | 小智平台 | — |
| 25 | `xiaozhi/list` | 小智平台 | — |
| 26 | `xiaozhi/add` | 小智平台 | `endpoint` |
| 27 | `xiaozhi/remove` | 小智平台 | `index` |
| 28 | `xiaozhi/set_endpoint` | 小智平台 | — |
| 29 | `auth/platforms` | 平台认证 | — |
| 30 | `auth/tuya_qr` | 涂鸦认证 | `user_code` |
| 31 | `auth/tuya_qr_status` | 涂鸦认证 | `token`, `user_code` |
| 32 | `auth/tuya_logout` | 涂鸦认证 | — |
| 33 | `tuya/refresh` | 涂鸦设备 | — |
| 34 | `get_tuya_device_properties` | 涂鸦控制 | `deviceId` |
| 35 | `set_tuya_device_property` | 涂鸦控制 | `deviceId`, `code`, `value` |
| 36 | `auth/midea_login` | 美的认证 | `account`, `password` |
| 37 | `auth/midea_logout` | 美的认证 | — |
| 38 | `midea/refresh` | 美的设备 | — |
| 39 | `get_midea_device_properties` | 美的控制 | `deviceId` |
| 40 | `set_midea_device_property` | 美的控制 | `deviceId`, `property`, `value` |
| 41 | `auth/ewelink_login` | 易微联认证 | `email`, `password` |
| 42 | `auth/ewelink_logout` | 易微联认证 | — |
| 43 | `ewelink/refresh` | 易微联设备 | — |
| 44 | `get_ewelink_device_properties` | 易微联控制 | `deviceId` |
| 45 | `set_ewelink_device_property` | 易微联控制 | `deviceId`, `property`, `value` |
| 46 | `trigger/create` | 触发规则 | `name`, `cameras`, `condition` |
| 47 | `trigger/list` | 触发规则 | — |
| 48 | `trigger/update` | 触发规则 | `id` |
| 49 | `trigger/delete` | 触发规则 | `id` |
| 50 | `trigger/toggle` | 触发规则 | `id`, `enabled` |
| 51 | `trigger/logs` | 触发规则 | — |
| 52 | `schedule/add` | 定时任务 | `name`, `scheduled_time`, `tool_name`, `tool_args` |
| 53 | `schedule/list` | 定时任务 | — |
| 54 | `schedule/get` | 定时任务 | `id` |
| 55 | `schedule/update` | 定时任务 | `id` |
| 56 | `schedule/delete` | 定时任务 | `id` |
| 57 | `schedule/cancel` | 定时任务 | `id` |
| 58 | `skill/list` | 技能系统 | — |
| 59 | `skill/read` | 技能系统 | `name` |
| 60 | `skill/create` | 技能系统 | `name`, `content` |
| 61 | `skill/update` | 技能系统 | `name`, `content` |
| 62 | `skill/delete` | 技能系统 | `name` |
| 63 | `skill/context` | 技能系统 | — |
| 64 | `skill/reload` | 技能系统 | — |
| 65 | `config/get_vision` | 配置管理 | — |
| 66 | `config/set_vision` | 配置管理 | — |
| 67 | `config/get_trigger` | 配置管理 | — |
| 68 | `config/set_trigger` | 配置管理 | — |
| 69 | `stats/token_usage` | 统计数据 | — |
| 70 | `stats/token_records` | 统计数据 | — |
| 71 | `stats/trigger_summary` | 统计数据 | — |
| 72 | `stats/dashboard` | 统计数据 | — |
| 73 | `license/status` | 授权管理 | — |
| 74 | `license/set` | 授权管理 | `license_key` |
| 75 | `license/clear` | 授权管理 | — |
| 76 | `gateway/info` | 网关信息 | — |

---

## 5. 通用设备工具

### `device/list`

获取所有已认证平台的设备列表（米家/涂鸦/美的/易微联），支持关键词和平台过滤。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `platform` | `string` | ❌ | 平台过滤: `xiaomi` / `tuya` / `midea` / `ewelink` |
| `filter` | `string[]` | ❌ | 关键词过滤数组，匹配设备名称、型号、房间名、家庭名 |

**响应示例**:
```json
{
  "total": 24,
  "devices": [
    {
      "id": "102838844",
      "name": "客厅灯",
      "model": "yeelink.light.lamp22",
      "platform": "xiaomi",
      "online": true,
      "category": "light",
      "home_name": "我的家",
      "room_name": "客厅"
    }
  ]
}
```

```bash
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"device/list","arguments":{"filter":["客厅","灯"],"platform":"xiaomi"}}}'
```

### `device/specs`

获取设备的功能规格定义（跨平台统一）。系统自动识别设备所属平台并路由，返回属性列表、Action 定义及参数格式。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `device_id` | `string` | ✅ | 设备 ID |

**响应示例**:
```json
{
  "success": true,
  "properties": [...],
  "actions": [...]
}
```

---

## 6. 小米 (Xiaomi) 平台

**控制流程**: `device/list` → `device/specs`（获取 siid/piid/aiid）→ `set_xiaomi_device_property` 或 `execute_xiaomi_device_action`

### 6.1 认证

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `xiaomi/auth_status` | 检查米家 OAuth 授权状态及 Token 剩余时间 | — |
| `xiaomi/auth_url` | 获取米家 OAuth 授权 URL | — |
| `xiaomi/auth_callback` | 处理米家 OAuth 授权回调 code | `code` |

**`xiaomi/auth_status` 响应**:
```json
{
  "authorized": true,
  "remaining_seconds": 86400,
  "cloud_server": "cn"
}
```

**`xiaomi/auth_url` 响应**:
```json
{
  "url": "https://account.xiaomi.com/oauth2/authorize?...",
  "message": "请在浏览器中打开此 URL 完成米家账号授权。"
}
```

**`xiaomi/auth_callback` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | `string` | ✅ | OAuth 授权码 |

**米家 OAuth 流程**:

```bash
# 1. 获取授权 URL
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"xiaomi/auth_url","arguments":{}}}'

# 2. 用户在浏览器打开 URL 完成授权，从回调 URL 获取 code

# 3. 提交 code
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"xiaomi/auth_callback","arguments":{"code":"CALLBACK_CODE"}}}'
```

### 6.2 设备查询

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `xiaomi/refresh` | 从云端重新拉取米家设备列表 | — |
| `xiaomi/get_devices` | 获取小米设备列表，支持按区域和类别过滤 | — |
| `xiaomi/get_area_info` | 获取小米智能家居房间/区域列表 | — |
| `xiaomi/get_device_classes` | 获取当前已导入的小米设备类别列表 | — |

**`xiaomi/refresh` 响应**:
```json
{
  "success": true,
  "device_count": 42,
  "camera_count": 3
}
```

**`xiaomi/get_devices` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `area_id` | `string` | ❌ | 区域 ID，从 `xiaomi/get_area_info` 获取 |
| `device_class` | `string` | ❌ | 设备类别，如 `light`、`switch`、`curtain` |

**`xiaomi/get_devices` 响应**:
```json
{
  "devices": [
    {
      "did": "102838844",
      "name": "客厅灯",
      "online": true,
      "home_info": "客厅",
      "device_class": "light",
      "model": "yeelink.light.lamp22"
    }
  ],
  "count": 1
}
```

### 6.3 属性读写

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `get_xiaomi_device_properties` | 获取小米设备属性当前值 | `deviceId`, `siid`, `piids` |
| `set_xiaomi_device_property` | 设置小米设备属性值 | `deviceId`, `siid`, `piid`, `value` |
| `execute_xiaomi_device_action` | 执行小米设备动作 | `deviceId`, `siid`, `aiid` |

**`get_xiaomi_device_properties` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | `string` | ✅ | 设备 ID (did) |
| `siid` | `integer` | ✅ | Service ID |
| `piids` | `integer[]` | ✅ | Property ID 列表，如 `[1, 2]` |

**`set_xiaomi_device_property` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | `string` | ✅ | 设备 ID |
| `siid` | `integer` | ✅ | Service ID |
| `piid` | `integer` | ✅ | Property ID |
| `value` | `any` | ✅ | 属性值（布尔/数字/字符串） |

**响应**: `{"success": true, "data": {...}}`

**`execute_xiaomi_device_action` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | `string` | ✅ | 设备 ID |
| `siid` | `integer` | ✅ | Service ID |
| `aiid` | `integer` | ✅ | Action ID |
| `params` | `array` | ❌ | Action 参数列表 |

**示例 — 开灯**:

```json
{
  "jsonrpc": "2.0", "id": 1, "method": "tools/call",
  "params": {
    "name": "set_xiaomi_device_property",
    "arguments": { "deviceId": "YOUR_DID", "siid": 2, "piid": 1, "value": true }
  }
}
```

### 6.4 场景

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `xiaomi/scene_list` | 获取小米手动场景列表，返回 sceneId 和名称 | — |
| `xiaomi/scene_trigger` | 触发执行小米手动场景 | `sceneId` |

**`xiaomi/scene_trigger` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `sceneId` | `string` | ✅ | 场景 ID，从 `xiaomi/scene_list` 获取 |

### 6.5 摄像头

> 仅支持 macOS 和 Linux。Windows 版本会返回 `{"error": "当前平台不支持摄像头功能"}`。

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `xiaomi/camera_list` | 获取所有已发现的米家摄像头 | — |
| `xiaomi/camera_status` | 获取摄像头流连接状态 | — |
| `xiaomi/camera_connect` | 连接摄像头并开始接收视频流 | `camera_id` |
| `xiaomi/camera_disconnect` | 停止流并断开连接 | `camera_id` |
| `xiaomi/camera_snapshot` | 抓取摄像头 JPEG 截图 | `camera_id` |

**`xiaomi/camera_list` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `filter` | `string[]` | ❌ | 关键词过滤数组（匹配名称/型号/房间） |

**`xiaomi/camera_list` 响应**:
```json
{
  "cameras": [
    {
      "did": "102838844",
      "name": "客厅摄像头",
      "model": "chuangmi.camera.ipc019",
      "home": "我的家",
      "room": "客厅",
      "online": true,
      "channel_count": 1,
      "camera_status": "connected"
    }
  ],
  "count": 1
}
```

**`xiaomi/camera_status` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `camera_id` | `string` | ❌ | 摄像头 DID，不传则返回所有已连接摄像头状态 |

**`xiaomi/camera_status` 响应** (指定 camera_id):
```json
{
  "did": "102838844",
  "camera_id": "102838844",
  "status": "connected",
  "buffered_frames": 5
}
```

**`xiaomi/camera_connect` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `camera_id` | `string` | ✅ | 摄像头设备 ID |

**`xiaomi/camera_connect` 响应**:
```json
{
  "camera_id": "102838844",
  "success": true,
  "status": "connected",
  "message": "Camera connected, streaming started"
}
```

> 连接为异步操作，服务器会等待最多 3 秒轮询连接状态。若超时返回 `"Connection initiated, current status: connecting. Status will update via polling."`。

**`xiaomi/camera_disconnect` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `camera_id` | `string` | ✅ | 摄像头设备 ID |

**`xiaomi/camera_snapshot` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `camera_id` | `string` | ✅ | 摄像头设备 ID |
| `channel` | `integer` | ❌ | 通道号，默认 `0` |
| `count` | `integer` | ❌ | 截图帧数，默认 `1`，最大 `10` |
| `use_subprocess` | `boolean` | ❌ | 强制子进程模式（进程隔离防挂死），默认 `false` |

**`xiaomi/camera_snapshot` 响应** (缓冲区模式):
```json
{
  "camera_id": "102838844",
  "channel": 0,
  "images": [
    {
      "data_url": "data:image/jpeg;base64,/9j/4AAQ...",
      "timestamp": 1716518400000,
      "size_bytes": 45678
    }
  ],
  "count": 1,
  "mode": "buffered"
}
```

**`xiaomi/camera_snapshot` 响应** (子进程模式):
```json
{
  "camera_id": "102838844",
  "channel": 0,
  "images": [
    {
      "data_url": "data:image/jpeg;base64,/9j/4AAQ...",
      "timestamp": 1716518400000,
      "size_bytes": 45678
    }
  ],
  "count": 1,
  "mode": "subprocess"
}
```

> **模式说明**: 默认优先从已连接的帧缓冲区读取；若缓冲区为空或指定 `use_subprocess=true`，则启动独立子进程连接摄像头抓拍，避免原生库挂死影响主服务。

**摄像头使用流程**:

```bash
# 1. 查找摄像头
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"xiaomi/camera_list","arguments":{}}}'

# 2. 连接摄像头（建立 P2P 流）
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"xiaomi/camera_connect","arguments":{"camera_id":"CAMERA_DID"}}}'

# 3. 等待 3-5 秒后截图
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"xiaomi/camera_snapshot","arguments":{"camera_id":"CAMERA_DID","count":1}}}'

# 4. 断开连接
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"xiaomi/camera_disconnect","arguments":{"camera_id":"CAMERA_DID"}}}'
```

---

## 7. 涂鸦 (Tuya) 平台

> 设置设备属性 (`set_tuya_device_property`) 需要设备授权（非免费版）。

### 授权（QR 码扫描）

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `auth/tuya_qr` | 获取涂鸦 QR 码授权，返回 qr_url 和 token | `user_code` |
| `auth/tuya_qr_status` | 查询 QR 码扫码授权状态 | `token`, `user_code` |
| `auth/tuya_logout` | 退出涂鸦平台授权 | — |
| `tuya/refresh` | 刷新涂鸦设备列表（授权后调用） | — |

**QR 码授权流程**:

1. 在涂鸦智能 / Smart Life App 中获取用户代码：**我的 → 设置 → 账号与安全**
2. 调用 `auth/tuya_qr` 传入 `user_code`，获取 `qr_url` 和 `token`（有效期 5 分钟）
3. 将 `qr_url` 转为二维码，用涂鸦 App 扫描并确认
4. 轮询 `auth/tuya_qr_status`，返回 `"status": "success"` 表示授权成功
5. 调用 `tuya/refresh` 同步设备

**`auth/tuya_qr` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_code` | `string` | ✅ | 涂鸦 App 中的用户代码 |

**`auth/tuya_qr_status` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `token` | `string` | ✅ | `auth/tuya_qr` 返回的 token |
| `user_code` | `string` | ✅ | 涂鸦用户代码 |

**`tuya/refresh` 响应**:
```json
{
  "success": true,
  "device_count": 12
}
```

### 设备控制

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `get_tuya_device_properties` | 获取涂鸦设备所有 DP 属性值 | `deviceId` |
| `set_tuya_device_property` | 设置涂鸦设备 DP 属性值（需授权） | `deviceId`, `code`, `value` |

**`get_tuya_device_properties` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | `string` | ✅ | 涂鸦设备 ID |

**`set_tuya_device_property` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | `string` | ✅ | 涂鸦设备 ID |
| `code` | `string` | ✅ | DP 功能点 code（如 `switch_1`, `bright_value`） |
| `value` | `any` | ✅ | 属性值（boolean/number/string） |

**`set_tuya_device_property` 响应**:
```json
{
  "success": true,
  "message": "...",
  "data": { ... }
}
```

---

## 8. 美的 (Midea) 平台

> 设置设备属性 (`set_midea_device_property`) 需要设备授权（非免费版）。

### 授权（账号密码）

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `auth/midea_login` | 美的账号密码登录（美居/MSmartHome） | `account`, `password` |
| `auth/midea_logout` | 退出美的平台授权 | — |
| `midea/refresh` | 刷新美的设备列表 | — |

**`auth/midea_login` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `account` | `string` | ✅ | 手机号或邮箱 |
| `password` | `string` | ✅ | 账号密码 |
| `cloud` | `string` | ❌ | 云端类型: `meiju`（美居，默认）或 `msmart`（MSmartHome） |

**`auth/midea_login` 响应**:
```json
{
  "success": true,
  "device_count": 8,
  "auth_status": { ... }
}
```

**`midea/refresh` 响应**:
```json
{
  "success": true,
  "device_count": 8
}
```

### 设备控制

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `get_midea_device_properties` | 获取美的设备所有属性值 | `deviceId` |
| `set_midea_device_property` | 设置美的设备属性值（需授权） | `deviceId`, `property`, `value` |

**`get_midea_device_properties` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | `string` | ✅ | 美的设备 ID (applianceCode) |

**`set_midea_device_property` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | `string` | ✅ | 美的设备 ID (applianceCode) |
| `property` | `string` | ✅ | 属性名（如 `power`, `temperature`, `mode`, `fan_speed`） |
| `value` | `any` | ✅ | 属性值 |

**`set_midea_device_property` 响应**:
```json
{
  "success": true,
  "message": "...",
  "data": { ... }
}
```

**常用属性值参考**:
- `power`: `0` / `1`（关/开）
- `temperature`: 整数（如 `26`）
- `mode`: `cool` / `heat` / `auto`
- `fan_speed`: `low` / `medium` / `high`

---

## 9. 易微联 (eWeLink) 平台

> 设置设备属性 (`set_ewelink_device_property`) 需要设备授权（非免费版）。

### 授权（账号密码）

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `auth/ewelink_login` | 易微联账号密码登录 | `email`, `password` |
| `auth/ewelink_logout` | 退出易微联平台授权 | — |
| `ewelink/refresh` | 刷新易微联设备列表 | — |

**`auth/ewelink_login` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `email` | `string` | ✅ | 邮箱或手机号 |
| `password` | `string` | ✅ | 账号密码 |
| `country_code` | `string` | ❌ | 国家代码，默认 `+86` |

**`auth/ewelink_login` 响应**:
```json
{
  "success": true,
  "device_count": 5,
  "auth_status": { ... }
}
```

### 设备控制

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `get_ewelink_device_properties` | 获取易微联设备所有属性值 | `deviceId` |
| `set_ewelink_device_property` | 设置易微联设备属性值（需授权） | `deviceId`, `property`, `value` |

**`set_ewelink_device_property` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | `string` | ✅ | 易微联设备 ID |
| `property` | `string` | ✅ | 属性名（如 `switch`, `switches`） |
| `value` | `any` | ✅ | 属性值（boolean/string/array） |

**常用属性**:
- `switch`: `on` / `off`
- `switches`: JSON 数组，如 `[{"switch": "on", "outlet": 0}]`（多路开关）

---

## 10. 小爱音箱控制

> 使用前先通过 `device/list` 获取音箱 `device_id`（model 以 `xiaomi.wifispeaker` 开头）。

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `xiaoai/play_music` | 控制小爱音箱播放音乐/故事/调整音量 | `device_id` |
| `xiaoai/tts` | 通过小爱音箱朗读文本（TTS 语音播报） | `device_id`, `text` |
| `xiaoai/control` | 通过小爱音箱语音指令间接控制设备 | `device_id`, `command` |

**`xiaoai/play_music` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `device_id` | `string` | ✅ | 音箱设备 ID |
| `text` | `string` | ⚠️ | 自然语言指令（如"播放刘德华的歌"、"讲个笑话"、"音量调到50"） |
| `command` | `string` | ⚠️ | `text` 的别名，两者等价。`text` 与 `command` 至少传一个 |

**`xiaoai/tts` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `device_id` | `string` | ✅ | 音箱设备 ID |
| `text` | `string` | ✅ | 播报文本内容 |

**`xiaoai/control` 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `device_id` | `string` | ✅ | 音箱设备 ID |
| `command` | `string` | ✅ | 语音指令（如"打开客厅灯"、"调高空调温度"） |
| `silence` | `boolean` | ❌ | 静默执行（音箱不语音回复），默认 `true` |

---

## 11. 小智平台

FeyaGate 支持多个并行小智 AI WebSocket 连接。

### `xiaozhi/status`

获取所有小智平台连接状态。

**参数**: 无

**响应示例**:
```json
{
  "state": "connected",
  "endpoint": "wss://xxx",
  "connected": true,
  "initialized": true,
  "bridged_tools": 42,
  "enabled": true,
  "clients": [
    {
      "index": 0,
      "endpoint": "wss://xxx",
      "state": "connected",
      "connected": true,
      "initialized": true,
      "bridged_tools": 42
    }
  ],
  "count": 1,
  "max_count": 10
}
```

### `xiaozhi/list`

列出所有已配置的小智连接端点及状态。

**参数**: 无

### `xiaozhi/add`

添加一个新的小智平台 WebSocket 连接。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `endpoint` | `string` | ✅ | WebSocket URL（`ws://` 或 `wss://`） |

**响应示例**:
```json
{
  "success": true,
  "endpoint": "wss://xxx",
  "index": 0,
  "count": 1
}
```

### `xiaozhi/remove`

删除指定索引的小智连接。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `index` | `integer` | ✅ | 连接索引（从 `xiaozhi/list` 获取） |

### `xiaozhi/set_endpoint`

设置第一个小智端点（向后兼容接口）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `endpoint` | `string` | ❌ | WebSocket URL，留空则禁用并删除 |

---

## 12. 认证与平台管理

### `auth/platforms`

列出所有已注册的智能家居平台及认证状态。

**参数**: 无

**响应示例**:
```json
{
  "xiaomi": { "connected": true, "authenticated": true },
  "tuya": { "connected": false, "authenticated": false },
  "midea": { "connected": true, "authenticated": true },
  "ewelink": { "connected": false, "authenticated": false }
}
```

---

## 13. Vision AI

### `xiaomi/camera_vision_chat`

向 Vision AI 提问摄像头画面内容。发送摄像头最近几帧图像和用户问题给 LLM，返回 AI 分析结果。

> 需先在 `config.yaml` 中配置 `vision.enabled=true` 和 `api_key`。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `camera_id` | `string` | ✅ | 摄像头设备 DID |
| `query` | `string` | ✅ | 向 AI 提出的问题（如"现在有几个人？"） |
| `channel` | `integer` | ❌ | 摄像头通道，默认 `0` |
| `count` | `integer` | ❌ | 发送最近几帧，默认 `3`，最大 `10` |

**响应示例**:
```json
{
  "camera_id": "102838844",
  "camera_name": "客厅摄像头",
  "channel": 0,
  "images_used": 3,
  "model": "configured",
  "content": "画面中有2个人，正在客厅看电视...",
  "tokens": {
    "prompt": 1500,
    "completion": 200
  }
}
```

---

## 14. 触发规则

触发引擎监控摄像头画面，当满足自然语言描述的条件时自动执行智能家居动作。

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `trigger/create` | 创建摄像头触发规则 | `name`, `cameras`, `condition` |
| `trigger/list` | 列出所有触发规则 | — |
| `trigger/update` | 更新触发规则 | `id` |
| `trigger/delete` | 删除触发规则 | `id` |
| `trigger/toggle` | 启用或禁用触发规则 | `id`, `enabled` |
| `trigger/logs` | 查看触发规则执行日志 | — |

### `trigger/create`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | `string` | ✅ | 规则名称 |
| `cameras` | `string[]` | ✅ | 关联摄像头 DID 列表 |
| `condition` | `string` | ✅ | 自然语言触发条件（如"有人进入客厅"） |
| `actions` | `array` | ❌ | 触发时执行的动作列表 |
| `notify` | `object` | ❌ | 通知配置 `{title, body}` |
| `filter` | `object` | ❌ | 过滤器 `{interval, period}` |

**响应示例**:
```json
{
  "id": "rule_001",
  "message": "触发规则已创建",
  "rule": { ... }
}
```

### `trigger/update`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | `string` | ✅ | 规则 ID |
| `name` | `string` | ❌ | 新名称 |
| `cameras` | `string[]` | ❌ | 新摄像头列表 |
| `condition` | `string` | ❌ | 新触发条件 |
| `actions` | `array` | ❌ | 新动作列表 |
| `notify` | `object` | ❌ | 新通知配置 |
| `filter` | `object` | ❌ | 新过滤器 |
| `enabled` | `boolean` | ❌ | 启用/禁用 |

### `trigger/toggle`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | `string` | ✅ | 规则 ID |
| `enabled` | `boolean` | ✅ | `true` 启用，`false` 禁用 |

### `trigger/logs`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `limit` | `integer` | ❌ | 返回条数限制，默认 `50` |
| `rule_id` | `string` | ❌ | 按规则 ID 过滤 |

---

## 15. 定时任务

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `schedule/add` | 创建定时任务，到时自动执行指定 MCP 工具 | `name`, `scheduled_time`, `tool_name`, `tool_args` |
| `schedule/list` | 列出定时任务，可按状态筛选 | — |
| `schedule/get` | 获取定时任务详情 | `id` |
| `schedule/update` | 修改任务（仅 pending 状态可修改） | `id` |
| `schedule/delete` | 删除定时任务 | `id` |
| `schedule/cancel` | 取消待执行任务（保留记录，状态变为 cancelled） | `id` |

### `schedule/add`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | `string` | ✅ | 任务名称 |
| `scheduled_time` | `string` | ✅ | 执行时间，ISO 8601 格式（如 `2026-05-24T22:00:00+08:00`） |
| `tool_name` | `string` | ✅ | 要执行的 MCP 工具名（如 `set_xiaomi_device_property`） |
| `tool_args` | `string` | ✅ | 工具参数 JSON 字符串 |
| `repeat` | `string` | ❌ | 重复类型: `none` / `daily` / `weekdays` / `weekends` / `weekly` / `custom` |
| `repeat_days` | `string` | ❌ | 自定义重复天 JSON 数组字符串，如 `"[1,2,3,4,5]"`（0=周日） |

**示例 — 每天晚上 10 点关灯**:

```json
{
  "jsonrpc": "2.0", "id": 1, "method": "tools/call",
  "params": {
    "name": "schedule/add",
    "arguments": {
      "name": "晚上关灯",
      "scheduled_time": "2026-05-24T22:00:00+08:00",
      "tool_name": "set_xiaomi_device_property",
      "tool_args": "{\"deviceId\":\"YOUR_DID\",\"siid\":2,\"piid\":1,\"value\":false}",
      "repeat": "daily"
    }
  }
}
```

### `schedule/list`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `status` | `string` | ❌ | 状态过滤: `pending` / `completed` / `cancelled`，留空返回全部 |

### `schedule/get` / `schedule/delete` / `schedule/cancel`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | `integer` | ✅ | 任务 ID（整数） |

### `schedule/update`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | `integer` | ✅ | 任务 ID（整数） |
| `scheduled_time` | `string` | ❌ | 新执行时间 ISO 8601 |
| `repeat` | `string` | ❌ | 新重复类型 |
| `repeat_days` | `string` | ❌ | 自定义重复天 JSON 数组字符串 |

---

## 16. 技能系统

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `skill/list` | 列出所有技能，可按来源过滤 | — |
| `skill/read` | 读取指定技能的完整内容（含 frontmatter） | `name` |
| `skill/create` | 创建新的自定义技能 | `name`, `content` |
| `skill/update` | 更新已有自定义技能的内容 | `name`, `content` |
| `skill/delete` | 删除指定自定义技能（内置技能不可删除） | `name` |
| `skill/context` | 获取所有常驻技能的上下文内容和技能摘要 | — |
| `skill/reload` | 重新扫描技能目录并刷新缓存 | — |

### `skill/list`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `source` | `string` | ❌ | 来源过滤: `all`（默认）/ `builtin` / `user` |

**响应示例**:
```json
{
  "skills": [
    {
      "name": "smart_light",
      "description": "智能灯光控制技能",
      "source": "builtin",
      "always": false,
      "tags": ["light", "control"],
      "path": "/path/to/skill.md"
    }
  ],
  "count": 1
}
```

### `skill/read`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | `string` | ✅ | 技能名称 |

**响应示例**:
```json
{
  "name": "smart_light",
  "description": "智能灯光控制技能",
  "source": "builtin",
  "always": false,
  "tags": ["light"],
  "path": "/path/to/skill.md",
  "content": "---\nname: smart_light\n---\n# 技能正文",
  "body": "# 技能正文"
}
```

### `skill/create` / `skill/update`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | `string` | ✅ | 技能名称（字母数字和连字符） |
| `content` | `string` | ✅ | 技能内容（Markdown + YAML frontmatter 格式） |

### `skill/delete`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | `string` | ✅ | 技能名称（内置技能不可删除） |

### `skill/context`

**参数**: 无

**响应示例**:
```json
{
  "context": "...",
  "skill_count": 5
}
```

### `skill/reload`

**参数**: 无

**响应示例**:
```json
{
  "success": true,
  "skill_count": 5
}
```

---

## 17. 配置管理

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `config/get_vision` | 获取 Vision AI 当前配置（API Key 脱敏显示） | — |
| `config/set_vision` | 更新 Vision AI 配置并保存到 `config.yaml`，修改后立即生效 | — |
| `config/get_trigger` | 获取触发引擎当前配置 | — |
| `config/set_trigger` | 更新触发引擎配置并保存到 `config.yaml`，修改后立即生效 | — |

### `config/get_vision`

**响应示例**:
```json
{
  "enabled": true,
  "api_key_masked": "sk-x****1234",
  "has_api_key": true,
  "base_url": "https://api.openai.com/v1",
  "model": "gpt-4o",
  "temperature": 0.7,
  "max_tokens": 4096,
  "timeout_seconds": 30
}
```

### `config/set_vision`

所有参数可选，仅传入需要修改的字段。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `enabled` | `boolean` | ❌ | 是否启用 Vision AI |
| `api_key` | `string` | ❌ | Vision AI API 密钥 |
| `base_url` | `string` | ❌ | OpenAI 兼容 API 端点 |
| `model` | `string` | ❌ | 模型名称 |
| `temperature` | `number` | ❌ | 温度参数 (0-2) |
| `max_tokens` | `integer` | ❌ | 最大响应 Token 数 |
| `timeout_seconds` | `integer` | ❌ | HTTP 超时秒数 |

**响应示例**:
```json
{
  "success": true,
  "config_saved": true,
  "message": "Vision AI 配置已保存并生效",
  "enabled": true,
  "api_key_masked": "sk-x****1234",
  "base_url": "https://api.openai.com/v1",
  "model": "gpt-4o",
  "temperature": 0.7,
  "max_tokens": 4096,
  "timeout_seconds": 30
}
```

### `config/get_trigger`

**响应示例**:
```json
{
  "enabled": true,
  "interval_seconds": 30,
  "vision_img_count": 3,
  "motion_threshold": 10,
  "log_ttl_days": 30,
  "min_trigger_interval": 300
}
```

### `config/set_trigger`

所有参数可选，仅传入需要修改的字段。启用/禁用会自动启停引擎。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `enabled` | `boolean` | ❌ | 是否启用触发引擎 |
| `interval_seconds` | `integer` | ❌ | 规则检查间隔（秒） |
| `vision_img_count` | `integer` | ❌ | 每次 LLM 调用使用的帧数 |
| `motion_threshold` | `integer` | ❌ | dHash 运动检测阈值 |
| `log_ttl_days` | `integer` | ❌ | 日志保留天数 |
| `min_trigger_interval` | `integer` | ❌ | 单规则最小触发间隔（秒，防抖） |

---

## 18. 统计数据

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `stats/token_usage` | 获取 Token 消耗统计（按天/按模型/按来源/总览） | — |
| `stats/token_records` | 获取最近的 LLM API 调用记录 | — |
| `stats/trigger_summary` | 获取触发事件聚合统计（每日趋势、规则排名、摄像头分布、热力图） | — |
| `stats/dashboard` | 获取综合看板摘要（系统状态、今日概览） | — |

### `stats/token_usage`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `days` | `integer` | ❌ | 统计最近多少天，默认 `30` |

**响应示例**:
```json
{
  "summary": { "total_tokens": 150000, "total_calls": 300 },
  "daily": [ {"date": "2026-05-20", "tokens": 5000, "calls": 10} ],
  "by_model": [ {"model": "gpt-4o", "tokens": 100000} ],
  "by_source": [ {"source": "vision", "tokens": 80000} ]
}
```

### `stats/token_records`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `limit` | `integer` | ❌ | 返回记录数，默认 `50` |

**响应示例**:
```json
{
  "records": [ ... ]
}
```

### `stats/trigger_summary`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `days` | `integer` | ❌ | 统计最近多少天，默认 `30` |

**响应示例**:
```json
{
  "overview": {
    "today": 5,
    "this_week": 32,
    "total": 150,
    "enabled_rules": 3,
    "total_rules": 5
  },
  "daily": [ {"date": "2026-05-20", "count": 8} ],
  "by_rule": [ {"rule_id": "rule_001", "rule_name": "有人进入", "count": 20} ],
  "by_camera": [ {"camera_id": "102838844", "count": 45} ],
  "heatmap": [ {"weekday": "Mon", "weekday_idx": 0, "hour": 9, "count": 3} ]
}
```

### `stats/dashboard`

**参数**: 无

**响应示例**:
```json
{
  "trigger_engine": {
    "enabled": true,
    "enabled_rules": 3,
    "total_rules": 5
  },
  "today": {
    "ai_calls": 42,
    "triggers": 5,
    "actions_executed": 8,
    "tokens_used": 12000
  },
  "token_summary": { ... },
  "action_ranking": [ {"action": "turn_off_light", "count": 3} ],
  "recent_events": [
    {"time": "2026-05-24T10:30:00", "rule_name": "有人进入", "camera_id": "xxx"}
  ]
}
```

---

## 19. 授权码管理

FeyaGate 免费版仅支持米家平台，授权版支持全平台（涂鸦/美的/易微联）。

| 工具名 | 说明 | 必填参数 |
|--------|------|----------|
| `license/status` | 获取虚拟网关授权状态 | — |
| `license/set` | 写入授权码并触发云端激活 | `license_key` |
| `license/clear` | 清除授权码，恢复免费版 | — |

### `license/status`

**响应示例** (已授权):
```json
{
  "edition": "pro",
  "status": "active",
  "product": "feyagate-linux",
  "device_id": "xxx",
  "key_masked": "FG-xxxx-****-xxxx"
}
```

**响应示例** (免费版):
```json
{
  "edition": "free",
  "status": "inactive",
  "product": "feyagate-linux",
  "device_id": "xxx",
  "key_masked": "",
  "guidance": {
    "message": "当前为免费版，仅支持米家平台。如需使用涂鸦/美的/易微联等平台，请获取授权码。",
    "how_to_authorize": "1. 联系代理商购买授权版虚拟网关\n2. 获取授权码 (格式: FG-XXXX-XXXX-XXXX)\n3. 使用 license/set 工具写入授权码\n4. 系统自动向云端激活",
    "free_features": "米家平台、设备控制、摄像头、小爱音箱、MCP代理、小智AI",
    "licensed_features": "以上全部 + 涂鸦平台 + 美的平台 + 易微联平台"
  }
}
```

### `license/set`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `license_key` | `string` | ✅ | 授权码，格式 `FG-XXXX-XXXX-XXXX` |
| `product` | `string` | ❌ | 产品标识，默认使用配置文件中的值 |

**响应示例**:
```json
{
  "edition": "pro",
  "status": "active",
  "activated": true,
  "message": "授权成功! 全平台功能已解锁。"
}
```

> 授权码绑定设备，一码一机，激活后不可转移。

### `license/clear`

**响应示例**:
```json
{
  "edition": "free",
  "status": "inactive",
  "message": "授权已清除，已恢复为免费版 (仅米家平台)。"
}
```

---

## 20. 网关信息

### `gateway/info`

获取虚拟网关信息，包括版本、平台、设备 ID、授权状态。

**参数**: 无

```bash
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"gateway/info","arguments":{}}}'
```

---

## 21. 错误码

### JSON-RPC 协议错误

| 错误码 | 含义 |
|--------|------|
| `-32700` | 解析错误（Invalid JSON） |
| `-32600` | 非法请求（非 JSON-RPC 2.0） |
| `-32601` | 方法不存在 |
| `-32602` | 参数错误（缺少 `params.name` 或工具不存在） |
| `-32603` | 服务器内部错误 |

### 工具业务错误

工具返回的 JSON 中可能包含以下错误：

| 字段 | 说明 |
|------|------|
| `{"error": "..."}` | 通用业务错误 |
| `{"success": false, "error": "license_required"}` | 需要设备授权（涂鸦/美的/易微联设置操作） |
| `{"error": "当前平台不支持摄像头功能"}` | Windows 平台不支持摄像头 |

---

## 附录: 快速示例

### 查找并控制客厅灯

```bash
# 1. 查找设备
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"device/list","arguments":{"filter":["客厅","灯"]}}}'

# 2. 查询设备规格
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"device/specs","arguments":{"device_id":"YOUR_DID"}}}'

# 3. 开灯
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"set_xiaomi_device_property","arguments":{"deviceId":"YOUR_DID","siid":2,"piid":1,"value":true}}}'
```

### 检查各平台授权状态

```bash
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"auth/platforms","arguments":{}}}'
```

### 创建触发规则（有人进门开灯）

```json
{
  "jsonrpc": "2.0", "id": 1, "method": "tools/call",
  "params": {
    "name": "trigger/create",
    "arguments": {
      "name": "玄关感应开灯",
      "cameras": ["CAMERA_DID"],
      "condition": "有人进入玄关",
      "actions": [
        {
          "tool": "set_xiaomi_device_property",
          "args": { "deviceId": "LIGHT_DID", "siid": 2, "piid": 1, "value": true }
        }
      ]
    }
  }
}
```
