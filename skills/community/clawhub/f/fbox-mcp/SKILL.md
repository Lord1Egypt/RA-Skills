---
name: fboxmcp
description: >
  管理 FBox 工业物联网设备。
  查看设备在线状态和统计信息，实时读写 PLC 监控点数据，处理和确认设备报警，查询历史采集数据趋势，远程打开 VNC 监控画面。
  当用户提到 FBox、盒子、设备状态、LC、监控点、温度/压力/电流等传感器数据、报警告警、历史数据、远程监控、VNC、设备运维时使用此技能。
compatibility: >
  Requires network access to FBox MCP Server (Streamable HTTP).
  Requires FBOXMCP_API_KEY environment variable.
metadata:
  version: "0.1.4"
  author: flexem
  homepage: https://fbox360.com
  openclaw:
    requires:
      env:
        - FBOXMCP_API_KEY
    primaryEnv: FBOXMCP_API_KEY
    os:
      - darwin
      - linux
      - win32
---

# FBox MCP Server 技能

通过 MCP 工具管理 FBox 工业物联网设备。安装和配置详见 [README.md](README.md)。

## 核心规则

### 数据真实性
- **所有数据必须来自工具调用的实时返回**，禁止凭记忆、推测或编造任何设备信息、数值或状态
- 不得复用之前对话中获取的数据作为当前结果，每次查询必须重新调用工具
- 如果工具调用失败或返回异常，如实告知用户，禁止用虚构数据填充

### 时间处理
- 服务端所有时间均为 **UTC 时间**
- 展示给用户时**必须转为北京时间（UTC+8）**，仅精确到秒
- **禁止假设当前时间**，必须通过 `utc_now` 工具获取服务器实时时间
- 历史数据和报警历史中的 `Timestamp` 为 UTC 毫秒级时间戳

### 参数处理
- `BoxNo`（设备序列号）和 `BoxAlias`（设备别名）**二选一**即可定位设备
- 用户说出的设备名称优先作为 `BoxAlias` 传入
- 缺少必填参数时设为 `null` 调用工具，服务端会返回候选列表
- **禁止自动猜测或补全参数**，必须从候选列表中让用户选择

### 在线设备优先
- 除非用户明确说"所有设备"或"离线设备"，默认 `OnlyOnline = true`
- `ConnState` 为 `Online` 或 `TimedOut` 视为在线

### 数据展示
- `bool` 值展示为"是"或"否"
- 报警历史和历史数据默认以**表格形式**展示
- 监控点、报警、历史数据条目之间**逻辑上没有强制关联性**，不要假设名称一致

### 写操作安全
- `write_user_box_dmon_value` 和 `confirm_current_alarm` 是写操作
- **必须获得用户明确确认后才能执行**
- 写入前先读取当前值展示给用户对比

## 响应格式

所有业务工具返回统一结构：

```json
{
  "success": true,
  "code": 0,
  "message": null,
  "data": { "..." },
  "suggestedParameters": null
}
```

| Code | 含义 | 处理方式 |
|------|------|---------|
| 0 | 成功 | 解析 `data` 展示给用户 |
| 300 | 参数需要选择 | 解析 `suggestedParameters` 候选列表让用户选择，选择后用 `value` 字段（非 `label`）重新调用 |
| 400 | 请求错误 | 展示 `message` 错误信息 |
| 401 | 未认证 | 提示用户检查认证配置 |
| 404 | 未找到 | 提示目标资源不存在 |
| 500 | 服务器错误 | 提示系统异常，建议稍后重试 |

## 典型工作流

### 设备状态概览
```
get_user_box_stats → get_user_box_list(OnlyOnline=true) → get_user_box_info(BoxAlias=xxx)
```

### 查看监控点数据
```
get_user_box_dmon_group_list(BoxAlias=xxx)
  → [如返回 300，让用户选择设备]
get_user_box_dmon_list(BoxNo=xxx, GroupName=xxx)
  → [如返回 300，让用户选择分组]
get_user_box_dmon_value(BoxNo=xxx, GroupName=xxx, Name=xxx)
```

### 处理设备报警
```
get_user_box_stats → 确认存在报警
get_current_alarm_list(BoxAlias=xxx) → 展示当前报警
confirm_current_alarm(BoxNo=xxx, AlarmName=xxx) → 用户确认后执行
```

### 查询历史趋势
```
utc_now → 获取服务器时间
get_history_data_define_list(BoxAlias=xxx) → 了解可查数据
get_history_data_list(BoxNo=xxx, ItemName=xxx, BeginTime=..., EndTime=...)
  → 以表格形式展示，时间转北京时间
```

### 写入监控点
```
get_user_box_dmon_value → 读取当前值展示给用户
  → 用户确认 "将 [监控点] 从 [当前值] 修改为 [目标值]"
write_user_box_dmon_value(Confirmed=true)
```
