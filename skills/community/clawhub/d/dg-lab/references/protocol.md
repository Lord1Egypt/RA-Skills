# DG-LAB WebSocket 协议参考

> 源自 [DG-LAB-OPENSOURCE socket/v2](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/socket/v2/README.md)。
> 仅适用于 **郊狼脉冲主机 3.0**。

## 目录

- [架构](#架构)
- [消息通用格式](#消息通用格式)
- [连接配对流程](#连接配对流程)
- [前端→服务端消息](#前端服务端消息)
- [服务端→APP消息](#服务端app消息)
- [APP→前端消息](#app前端消息)
- [服务端控制消息](#服务端控制消息)
- [二维码格式](#二维码格式)
- [错误码](#错误码)

---

## 架构

```
N(第三方终端) ↔ WebSocket 服务 ↔ N(APP 终端)
```

N 对 N 模式，多个控制端可同时连接多个 APP。

## 消息通用格式

所有消息为 JSON，包含以下字段：

```json
{"type": "xxx", "clientId": "xxx", "targetId": "xxx", "message": "xxx"}
```

| 字段 | 说明 |
|------|------|
| `type` | 消息类型 |
| `clientId` | 第三方终端 ID |
| `targetId` | APP 端 ID |
| `message` | 消息内容/指令 |

**约束：**
- JSON 最大长度 **1950** 字符，超长 APP 会丢弃
- 除首次连接返回的 clientId 消息外，所有字段必须非空
- ID 建议使用 UUID v4

---

## 连接配对流程

```
1. 前端连接 WS      → 服务端返回 {"type":"bind", "clientId":"uuid", "targetId":"", "message":"targetId"}
2. 前端用 clientId 生成二维码
3. APP 扫码连接 WS   → 服务端分配 targetId
4. APP 发送 bind 请求 (clientId + targetId)
5. 服务端绑定成功     → 双方收到 {"type":"bind", ..., "message":"200"}
6. 通信就绪
```

---

## 前端→服务端消息

> 前端协议消息不能直接发给 APP，需由服务端转换。

### 强度减少 (type: 1)

```json
{"type": 1, "channel": 1, "message": "set channel", "clientId": "xxx", "targetId": "xxx"}
```
- `channel`: `1` = A, `2` = B
- 服务端转换: `strength-通道+0+1`

### 强度增加 (type: 2)

```json
{"type": 2, "channel": 1, "message": "set channel", "clientId": "xxx", "targetId": "xxx"}
```
- 服务端转换: `strength-通道+1+1`

### 强度设为指定值 (type: 3)

```json
{"type": 3, "channel": 2, "strength": 35, "message": "set channel", "clientId": "xxx", "targetId": "xxx"}
```
- `strength`: 0 ~ 200
- 服务端转换: `strength-通道+2+值`

### 直接转发 APP 指令 (type: 4)

```json
{"type": 4, "message": "clear-1", "clientId": "xxx", "targetId": "xxx"}
```
- `message` 直接转发给 APP（如 `clear-1` 清空 A 通道波形队列）

### 发送波形 (type: "clientMsg")

```json
{
  "type": "clientMsg",
  "channel": "A",
  "time": 5,
  "message": "A:[\"0A0A0A0A64646464\",...]",
  "clientId": "xxx",
  "targetId": "xxx"
}
```
- `channel`: `"A"` 或 `"B"`
- `time`: 持续发送时长（秒），默认 5
- `message`: `通道:波形HEX数组JSON`
- 服务端按频率定时发送给 APP，加 `pulse-` 前缀

---

## 服务端→APP消息

统一格式: `{"type": "msg", "clientId": "xxx", "targetId": "xxx", "message": "指令"}`

### 强度指令

`message`: `strength-通道+模式+数值`

| 字段 | 值 |
|------|-----|
| 通道 | `1`=A, `2`=B |
| 模式 | `0`=减少, `1`=增加, `2`=设为指定值 |
| 数值 | 0 ~ 200 |

示例: `strength-1+2+35` → A 通道设为 35

### 波形指令

`message`: `pulse-通道:["HEX",...]`

- 每条 HEX 为 8 字节（16 hex 字符），代表 100ms
- 数组最大 100 条（10 秒）
- APP 波形队列缓存最大 500 条（50 秒）

### 清空波形队列

`message`: `clear-通道` (`clear-1` = A, `clear-2` = B)

---

## APP→前端消息

### 强度回传

APP 强度/上限变化时自动上报，服务端转发给前端：

`message`: `strength-A强度+B强度+A上限+B上限`

```json
{"type": "msg", ..., "message": "strength-11+7+100+35"}
```

解读: A 强度=11, B 强度=7, A 上限=100, B 上限=35 (范围 0~200)

### 反馈按钮

APP 用户点击反馈图标: `message`: `feedback-角标`

| 角标 | 位置 |
|------|------|
| 0~4 | A 通道 5 个按钮 |
| 5~9 | B 通道 5 个按钮 |

---

## 服务端控制消息

### bind

| message | 含义 |
|---------|------|
| `"targetId"` | 首次连接，分配 clientId |
| `"200"` | 配对成功 |
| `"400"` | 配对失败（已被绑定） |

### break

`{"type":"break", ..., "message":"209"}` — 对方已断开

### error

`{"type":"error", ..., "message":"错误码"}`

### heartbeat

`{"type":"heartbeat", ..., "message":"200"}` — 默认 60 秒一次

---

## 二维码格式

```
https://www.dungeon-lab.com/app-download.php#DGLAB-SOCKET#ws://服务器地址:端口/终端ID
```

**规则：**
1. 必须包含 APP 官网: `https://www.dungeon-lab.com/app-download.php`
2. 标签: `DGLAB-SOCKET`
3. WS 地址 + 终端 ID，中间无额外路径
4. 有且仅有 **2 个 `#`** 分隔三部分
5. 正式环境推荐 `wss://`

正确: `https://www.dungeon-lab.com/app-download.php#DGLAB-SOCKET#wss://ws.example.com/xxxx`
错误: `...#wss://ws.example.com/path/xxxx` (多了路径)

---

## 错误码

| 码 | 说明 |
|----|------|
| 200 | 成功 |
| 209 | 对方已断开 |
| 210 | 二维码无有效 clientID |
| 211 | 连接成功但未下发 APP ID |
| 400 | ID 已被其他客户端绑定 |
| 401 | 目标客户端不存在 |
| 402 | 收信方与寄信方非绑定关系 |
| 403 | 内容不是标准 JSON |
| 404 | 收信人未找到（离线） |
| 405 | message 长度 > 1950 |
| 406 | 缺少 channel 字段 |
| 500 | 服务器内部异常 |
