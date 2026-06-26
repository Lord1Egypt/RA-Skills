# FeyaGate HTTP API 文档

> **适用产品**: miloco-mcp-server (桌面版虚拟网关 / ESP32 物理网关)
> **基础 URL**: `http://<网关IP>:<port>` (桌面版默认 `38080`)
> **协议**: HTTP REST + MCP JSON-RPC 2.0
> **CORS**: 全局开放 `Access-Control-Allow-Origin: *`

---

## 目录

- [1. 概述](#1-概述)
- [2. HTTP REST 接口](#2-http-rest-接口)
  - [2.1 健康检查](#21-健康检查)
  - [2.2 OAuth 授权回调](#22-oauth-授权回调)
  - [2.3 网关信息](#23-网关信息)
  - [2.4 授权管理](#24-授权管理)
- [3. MCP JSON-RPC 接口](#3-mcp-json-rpc-接口)
  - [3.1 协议说明](#31-协议说明)
  - [3.2 协议方法](#32-协议方法)
- [4. 米家平台](#4-米家平台)
- [5. 小爱音箱](#5-小爱音箱)
- [6. 小智平台](#6-小智平台)
- [7. 授权与网关](#7-授权与网关)
- [8. Vision AI](#8-vision-ai)
- [9. 触发规则](#9-触发规则)
- [10. 配置管理](#10-配置管理)
- [11. 统计数据](#11-统计数据)
- [12. 多平台设备](#12-多平台设备)
- [13. 定时任务](#13-定时任务)
- [14. 技能管理](#14-技能管理)

---

## 1. 概述

FeyaGate 网关提供两类 HTTP 接口：

1. **HTTP REST 接口** — 标准 GET/POST/DELETE 端点，主要用于健康检查、OAuth 授权回调、网关信息和授权管理。
2. **MCP JSON-RPC 接口** — 所有智能家居控制、设备管理等核心功能通过 `POST /mcp/http` 以 JSON-RPC 2.0 协议调用。

---

## 2. HTTP REST 接口

### 2.1 健康检查

```
GET /health
```

**响应示例**:
```json
{"status": "ok"}
```

### 2.2 OAuth 授权回调

#### 2.2.1 OAuth 回调

```
GET /auth/callback?code=xxx&source=browser
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | string | 是 | OAuth 授权码 |
| `source` | string | 否 | 来源标识，`browser` 时触发页面重定向 |

**响应**: 成功时返回 HTML 页面显示授权结果；失败时返回错误提示。

#### 2.2.2 浏览器 OAuth 回调

```
GET /auth/browser-callback?code=xxx
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | string | 是 | OAuth 授权码 |

**响应**: 重定向到 `/#/?auth=success` 或 `/#/?auth=failed`。

#### 2.2.3 浏览器 OAuth 启动页

```
GET /auth/browser-start?oauth_url=xxx&callback=xxx
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `oauth_url` | string | 是 | OAuth 授权 URL |
| `callback` | string | 是 | 回调地址 |

**响应**: 返回 HTML 页面，含小米登录按钮，500ms 后自动跳转授权。

### 2.3 网关信息

```
GET /api/v1/gateway/info
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "version": "v1.2.14",
    "platform": "linux",
    "device_id": "xxx",
    "edition": "pro",
    "licensed": true
  }
}
```

### 2.4 授权管理

#### 获取授权状态

```
GET /api/v1/gateway/license
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "edition": "pro",
    "status": "active",
    "product": "feyagate-linux",
    "license_key": "FG-xxxx-****-xxxx"
  }
}
```

#### 写入授权码

```
POST /api/v1/gateway/license
Content-Type: application/json
```

**请求体**:
```json
{
  "license_key": "FG-XXXX-XXXX-XXXX",
  "product": "feyagate-linux"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `license_key` | string | 是 | 授权码，格式 `FG-XXXX-XXXX-XXXX` |
| `product` | string | 否 | 产品标识，默认使用配置文件中的值 |

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "edition": "pro",
    "status": "active",
    "activated": true
  }
}
```

#### 清除授权

```
DELETE /api/v1/gateway/license
```

**响应示例**:
```json
{
  "code": 0,
  "data": { "edition": "free", "status": "inactive" },
  "message": "授权已清除, 恢复免费版"
}
```

---

## 3. MCP JSON-RPC 接口

### 3.1 协议说明

所有 MCP 工具通过单一端点调用：

```
POST /mcp/http
Content-Type: application/json
```

**请求格式** (JSON-RPC 2.0):
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

**响应格式**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": { ... }
}
```

> **注意**: `GET /mcp/http` 返回 `{"error": "SSE stream not supported yet. Use POST for JSON-RPC."}`，暂不支持 SSE。

### 3.2 协议方法

| 方法 | 说明 |
|------|------|
| `initialize` | MCP 协议握手 |
| `ping` | 保活心跳 |
| `tools/list` | 列出所有已注册工具 |
| `tools/call` | 调用指定工具 |
| `notifications/initialized` | 初始化完成通知（无响应） |

---

## 4. 米家平台

### 4.1 xiaomi/auth_status

检查米家 OAuth 授权状态。

**参数**: 无

**响应示例**:
```json
{
  "authorized": true,
  "remaining_seconds": 86400,
  "cloud_server": "cn"
}
```

### 4.2 xiaomi/auth_url

获取米家 OAuth 授权 URL。

**参数**: 无

**响应示例**:
```json
{
  "url": "https://account.xiaomi.com/oauth2/authorize?...",
  "message": "请在浏览器中打开此 URL 完成米家账号授权。"
}
```

### 4.3 xiaomi/auth_callback

处理 OAuth 授权回调 code。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | string | 是 | OAuth 授权码 |

### 4.4 xiaomi/refresh

刷新米家 Token。

**参数**: 无

### 4.5 xiaomi/camera_list

获取米家摄像头列表。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `filter` | string[] | 否 | 关键词过滤数组 |

**响应示例**:
```json
[
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
]
```

### 4.6 xiaomi/camera_status

查询摄像头连接状态。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `camera_id` | string | 否 | 摄像头 DID，留空返回所有 |

### 4.7 xiaomi/camera_connect

连接摄像头。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `camera_id` | string | 是 | 摄像头 DID |

### 4.8 xiaomi/camera_disconnect

断开摄像头连接。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `camera_id` | string | 是 | 摄像头 DID |

### 4.9 xiaomi/camera_snapshot

抓拍摄像头画面。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `camera_id` | string | 是 | 摄像头 DID |
| `channel` | integer | 否 | 通道号，默认 `0` |
| `count` | integer | 否 | 抓拍帧数，默认 `1`，最大 `10` |
| `use_subprocess` | boolean | 否 | 是否使用子进程抓拍 |

### 4.10 xiaomi/get_area_info

获取米家家庭/房间信息。

**参数**: 无

### 4.11 xiaomi/get_device_classes

获取米家设备分类列表。

**参数**: 无

### 4.12 xiaomi/get_devices

获取米家设备列表。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `area_id` | string | 否 | 按房间 ID 过滤 |
| `device_class` | string | 否 | 按设备分类过滤 |

### 4.13 get_xiaomi_device_properties

获取米家设备属性值。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | string | 是 | 设备 DID |
| `siid` | integer | 是 | 服务 ID |
| `piids` | integer[] | 是 | 属性 ID 数组 |

### 4.14 set_xiaomi_device_property

设置米家设备属性。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | string | 是 | 设备 DID |
| `siid` | integer | 是 | 服务 ID |
| `piid` | integer | 是 | 属性 ID |
| `value` | any | 是 | 属性值 |

### 4.15 execute_xiaomi_device_action

执行米家设备动作。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | string | 是 | 设备 DID |
| `siid` | integer | 是 | 服务 ID |
| `aiid` | integer | 是 | 动作 ID |
| `params` | array | 否 | 动作参数 |

### 4.16 xiaomi/scene_list

获取米家场景列表。

**参数**: 无

### 4.17 xiaomi/scene_trigger

触发米家场景。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `sceneId` | string | 是 | 场景 ID |

---

## 5. 小爱音箱

### 5.1 xiaoai/play_music

控制小爱音箱播放音乐/语音。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `device_id` | string | 是 | 小爱音箱设备 ID |
| `text` | string | 是 | 播放内容 |
| `command` | string | 否 | 播放命令（`text` 的别名） |

### 5.2 xiaoai/tts

小爱音箱 TTS 语音播报。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `device_id` | string | 是 | 小爱音箱设备 ID |
| `text` | string | 是 | 播报文本 |

### 5.3 xiaoai/control

发送小爱音箱控制命令。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `device_id` | string | 是 | 小爱音箱设备 ID |
| `command` | string | 是 | 控制命令 |
| `silence` | boolean | 否 | 是否静音执行，默认 `true` |

---

## 6. 小智平台

> 小智平台支持多连接（最多由 `XIAOZHI_MAX_CONNECTIONS` 常量定义）。

### 6.1 xiaozhi/status

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
  "max_count": 3
}
```

### 6.2 xiaozhi/list

列出所有已配置的小智连接端点。

**参数**: 无

### 6.3 xiaozhi/add

添加新的小智平台 WebSocket 连接。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `endpoint` | string | 是 | WebSocket URL (`ws://` 或 `wss://`) |

### 6.4 xiaozhi/remove

删除指定索引的小智连接。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `index` | integer | 是 | 连接索引（0-based） |

### 6.5 xiaozhi/set_endpoint

设置第一个小智平台端点（向后兼容接口）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `endpoint` | string | 否 | WebSocket URL，留空禁用 |

---

## 7. 授权与网关

### 7.1 license/status

获取设备授权状态。

**参数**: 无

**响应示例**:
```json
{
  "edition": "pro",
  "status": "active",
  "product": "feyagate-linux",
  "device_id": "xxx",
  "key_masked": "FG-xxxx-****-xxxx"
}
```

> 免费版时额外返回 `guidance` 字段，包含授权指引信息。

### 7.2 license/set

写入授权码并激活。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `license_key` | string | 是 | 授权码，格式 `FG-XXXX-XXXX-XXXX` |
| `product` | string | 否 | 产品标识，默认使用配置文件中的值 |

**响应示例**:
```json
{
  "edition": "pro",
  "status": "active",
  "activated": true,
  "message": "授权成功! 全平台功能已解锁。"
}
```

### 7.3 license/clear

清除授权码，恢复免费版。

**参数**: 无

### 7.4 gateway/info

获取网关信息（MCP 版本，对应 REST 的 `GET /api/v1/gateway/info`）。

**参数**: 无

---

## 8. Vision AI

### 8.1 xiaomi/camera_vision_chat

向 Vision AI 提问摄像头画面内容。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `camera_id` | string | 是 | 摄像头设备 DID |
| `query` | string | 是 | 向 AI 提出的问题 |
| `channel` | integer | 否 | 摄像头通道，默认 `0` |
| `count` | integer | 否 | 发送最近几帧，默认 `3`，最大 `10` |

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

> 需先在 `config.yaml` 中配置 `vision.enabled=true` 和 `api_key`。

---

## 9. 触发规则

### 9.1 trigger/create

创建摄像头触发规则。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 规则名称 |
| `cameras` | string[] | 是 | 关联摄像头 DID 列表 |
| `condition` | string | 是 | 自然语言触发条件 |
| `actions` | array | 否 | 触发时执行的动作列表 |
| `notify` | object | 否 | 通知配置 `{title, body}` |
| `filter` | object | 否 | 过滤器 `{interval, period}` |

**响应示例**:
```json
{
  "id": "rule_001",
  "message": "触发规则已创建",
  "rule": { ... }
}
```

### 9.2 trigger/list

列出所有触发规则。

**参数**: 无

### 9.3 trigger/update

更新触发规则。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 规则 ID |
| `name` | string | 否 | 新名称 |
| `cameras` | string[] | 否 | 新摄像头列表 |
| `condition` | string | 否 | 新触发条件 |
| `actions` | array | 否 | 新动作列表 |
| `notify` | object | 否 | 新通知配置 |
| `filter` | object | 否 | 新过滤器 |
| `enabled` | boolean | 否 | 启用/禁用 |

### 9.4 trigger/delete

删除触发规则。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 规则 ID |

### 9.5 trigger/toggle

启用或禁用触发规则。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 规则 ID |
| `enabled` | boolean | 是 | `true` 启用，`false` 禁用 |

### 9.6 trigger/logs

查看触发规则执行日志。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `limit` | integer | 否 | 返回数量限制，默认 `50` |
| `rule_id` | string | 否 | 按规则 ID 过滤 |

---

## 10. 配置管理

### 10.1 config/get_vision

获取 Vision AI 当前配置。

**参数**: 无

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

### 10.2 config/set_vision

更新 Vision AI 配置并保存到 `config.yaml`，修改后立即生效。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `enabled` | boolean | 否 | 是否启用 Vision AI |
| `api_key` | string | 否 | LLM API Key |
| `base_url` | string | 否 | OpenAI 兼容 API 端点 |
| `model` | string | 否 | 模型名称 |
| `temperature` | number | 否 | 温度参数 (0-2) |
| `max_tokens` | integer | 否 | 最大响应 Token 数 |
| `timeout_seconds` | integer | 否 | HTTP 超时秒数 |

### 10.3 config/get_trigger

获取触发引擎当前配置。

**参数**: 无

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

### 10.4 config/set_trigger

更新触发引擎配置并保存到 `config.yaml`，修改后立即生效。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `enabled` | boolean | 否 | 是否启用触发引擎 |
| `interval_seconds` | integer | 否 | 规则检查间隔（秒） |
| `vision_img_count` | integer | 否 | 每次 LLM 调用使用的帧数 |
| `motion_threshold` | integer | 否 | dHash 运动检测阈值 |
| `log_ttl_days` | integer | 否 | 日志保留天数 |
| `min_trigger_interval` | integer | 否 | 单规则最小触发间隔（秒） |

---

## 11. 统计数据

### 11.1 stats/token_usage

获取 Token 消耗统计。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `days` | integer | 否 | 统计最近多少天，默认 `30` |

**响应示例**:
```json
{
  "summary": { "total_tokens": 150000, "total_calls": 300 },
  "daily": [ {"date": "2026-05-20", "tokens": 5000, "calls": 10} ],
  "by_model": [ {"model": "gpt-4o", "tokens": 100000} ],
  "by_source": [ {"source": "vision", "tokens": 80000} ]
}
```

### 11.2 stats/token_records

获取最近 LLM API 调用记录。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `limit` | integer | 否 | 返回记录数，默认 `50` |

### 11.3 stats/trigger_summary

获取触发事件聚合统计（每日趋势、规则排名、摄像头分布、时间热力图）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `days` | integer | 否 | 统计最近多少天，默认 `30` |

**响应示例**:
```json
{
  "overview": {
    "today": 5, "this_week": 32, "total": 150,
    "enabled_rules": 3, "total_rules": 5
  },
  "daily": [ {"date": "2026-05-20", "count": 8} ],
  "by_rule": [ {"rule_id": "rule_001", "rule_name": "有人进入", "count": 20} ],
  "by_camera": [ {"camera_id": "102838844", "count": 45} ],
  "heatmap": [ {"weekday": "Mon", "weekday_idx": 0, "hour": 9, "count": 3} ]
}
```

### 11.4 stats/dashboard

获取综合看板摘要数据。

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

## 12. 多平台设备

### 12.1 auth/platforms

列出所有已注册的智能家居平台及认证状态。

**参数**: 无

### 12.2 device/list

获取所有已认证平台的设备列表（跨平台统一）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `platform` | string | 否 | 按平台过滤: `xiaomi` / `tuya` / `midea` / `ewelink` |
| `filter` | string[] | 否 | 关键词过滤数组，匹配设备名称、型号、房间名 |

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

### 12.3 device/specs

获取设备功能规格定义（跨平台统一）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `device_id` | string | 是 | 设备 ID |

### 12.4 涂鸦平台

| 工具名 | 必填参数 | 说明 |
|--------|----------|------|
| `auth/tuya_qr` | `user_code` | 获取涂鸦 QR 码授权 |
| `auth/tuya_qr_status` | `token`, `user_code` | 查询扫码状态 |
| `auth/tuya_logout` | 无 | 退出涂鸦授权 |
| `tuya/refresh` | 无 | 刷新涂鸦设备列表 |
| `get_tuya_device_properties` | `deviceId` | 获取设备 DP 属性 |
| `set_tuya_device_property` | `deviceId`, `code`, `value` | 设置设备 DP 属性（需授权） |

**set_tuya_device_property 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | string | 是 | 设备 ID |
| `code` | string | 是 | DP Code（如 `switch_1`, `bright_value`） |
| `value` | any | 是 | DP 值（boolean/number/string） |

### 12.5 美的平台

| 工具名 | 必填参数 | 说明 |
|--------|----------|------|
| `auth/midea_login` | `account`, `password` | 美的平台登录 |
| `auth/midea_logout` | 无 | 退出美的授权 |
| `midea/refresh` | 无 | 刷新美的设备列表 |
| `get_midea_device_properties` | `deviceId` | 获取设备属性 |
| `set_midea_device_property` | `deviceId`, `property`, `value` | 设置设备属性（需授权） |

**auth/midea_login 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `account` | string | 是 | 手机号或邮箱 |
| `password` | string | 是 | 密码 |
| `cloud` | string | 否 | 云端类型: `meiju`(默认) 或 `msmart` |

**set_midea_device_property 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | string | 是 | 设备 ID (applianceCode) |
| `property` | string | 是 | 属性名（如 `power`, `temperature`, `mode`） |
| `value` | any | 是 | 属性值 |

### 12.6 易微联 (eWeLink)

| 工具名 | 必填参数 | 说明 |
|--------|----------|------|
| `auth/ewelink_login` | `email`, `password` | 易微联平台登录 |
| `auth/ewelink_logout` | 无 | 退出易微联授权 |
| `ewelink/refresh` | 无 | 刷新易微联设备列表 |
| `get_ewelink_device_properties` | `deviceId` | 获取设备属性 |
| `set_ewelink_device_property` | `deviceId`, `property`, `value` | 设置设备属性（需授权） |

**auth/ewelink_login 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `email` | string | 是 | 邮箱或手机号 |
| `password` | string | 是 | 密码 |
| `country_code` | string | 否 | 国家代码，默认 `+86` |

**set_ewelink_device_property 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | string | 是 | 设备 ID |
| `property` | string | 是 | 属性名（如 `switch`, `switches`） |
| `value` | any | 是 | 属性值（boolean/string/array） |

---

## 13. 定时任务

### 13.1 schedule/add

创建定时任务。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 任务名称 |
| `scheduled_time` | string | 是 | 执行时间 ISO 8601，如 `2026-05-24T08:00:00+08:00` |
| `tool_name` | string | 是 | 要执行的 MCP 工具名 |
| `tool_args` | string | 是 | 工具参数 JSON 字符串 |
| `repeat` | string | 否 | 重复类型: `none`/`daily`/`weekdays`/`weekends`/`weekly`/`custom` |
| `repeat_days` | string | 否 | 自定义重复天 JSON 数组，如 `[1,2,3,4,5]` (周一到周五) |

### 13.2 schedule/list

列出定时任务。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `status` | string | 否 | 筛选状态: `pending`/`completed`/`cancelled`，留空返回全部 |

### 13.3 schedule/get

获取定时任务详情。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | integer | 是 | 任务 ID |

### 13.4 schedule/update

更新定时任务（仅 pending 状态可修改）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | integer | 是 | 任务 ID |
| `scheduled_time` | string | 否 | 新执行时间 ISO 8601 |
| `repeat` | string | 否 | 新重复类型 |
| `repeat_days` | string | 否 | 新自定义重复天 |

### 13.5 schedule/delete

删除定时任务。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | integer | 是 | 任务 ID |

### 13.6 schedule/cancel

取消定时任务（保留记录，状态变为 `cancelled`）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | integer | 是 | 任务 ID |

---

## 14. 技能管理

### 14.1 skill/list

列出所有技能。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `source` | string | 否 | 来源过滤: `all`(默认) / `builtin` / `user` |

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

### 14.2 skill/read

读取指定技能的完整内容。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 技能名称 |

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

### 14.3 skill/create

创建新的自定义技能。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 技能名称（字母数字和连字符） |
| `content` | string | 是 | 技能内容（Markdown + YAML frontmatter） |

### 14.4 skill/update

更新已有自定义技能内容。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 技能名称 |
| `content` | string | 是 | 新的技能内容 |

### 14.5 skill/delete

删除指定自定义技能（内置技能不可删除）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 技能名称 |

### 14.6 skill/context

获取所有常驻技能的上下文内容。

**参数**: 无

**响应示例**:
```json
{
  "context": "...",
  "skill_count": 5
}
```

### 14.7 skill/reload

重新扫描技能目录并刷新缓存。

**参数**: 无
