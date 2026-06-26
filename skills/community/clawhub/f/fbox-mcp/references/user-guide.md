# FBox MCP Server 用户接入指南

## 简介

FBox MCP Server 是 FBox 物联网设备管理平台的 AI 接口服务，遵循 [MCP（Model Context Protocol）](https://modelcontextprotocol.io/) 协议。接入后，你的 AI 助手可以：

- 查看设备状态、统计信息、地理位置、SIM 卡流量
- 实时读写 PLC 监控点数据
- 管理设备报警（查看、确认、查询历史）
- 查询历史采集数据（支持多粒度聚合）
- 远程打开设备 VNC 监控画面
- 查阅 FBox 官方文档

**服务信息：**

| 项目 | 值 |
|------|-----|
| 服务名称 | @fboxmcp |
| 协议 | MCP 1.0（Streamable HTTP） |
| 端点 | `POST /` |
| 健康检查 | `GET /health` |
| 官网 | https://fbox360.com |

---

## 前置条件

1. **FBox 账号** — 拥有 FBox 平台账号并绑定了设备
2. **API 凭证** — 由 FBox 平台管理员分配 `clientId` 和 `clientSecret`
3. **MCP 客户端** — 任意支持 MCP 协议的 AI 客户端（OpenClaw、Claude Code、Claude Desktop、Cursor、Windsurf 等）

> **快速开始：** 如果你使用 Claude Code 或 OpenClaw，可直接参考 [INSTALL.md](../INSTALL.md) 快速安装。

---

## 第 1 步：获取 API Key

向 FBox MCP Server 发送请求生成 API Key：

```http
POST https://<fboxmcp-host>/api/apikey/generate
Content-Type: application/json

{
  "clientId": "your-client-id",
  "clientSecret": "your-client-secret"
}
```

成功响应：

```json
{
  "apiKey": "sk-abc123...",
  "usage": "Authorization: Bearer sk-abc123..."
}
```

> API Key 以 `sk-` 开头，长期有效。服务端自动管理底层 JWT Token 的刷新和缓存，无需手动续期。

---

## 第 2 步：配置 MCP 客户端

将 API Key 设为环境变量：

```bash
# Linux / macOS
export FBOXMCP_API_KEY="sk-your-api-key-here"

# Windows PowerShell
$env:FBOXMCP_API_KEY = "sk-your-api-key-here"
```

然后在你的 MCP 客户端中添加服务器配置。

### OpenClaw

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "mcpServers": {
    "fboxmcp": {
      "transport": "streamable-http",
      "url": "https://<fboxmcp-host>",
      "headers": {
        "Authorization": "Bearer ${FBOXMCP_API_KEY}"
      }
    }
  }
}
```

### Claude Desktop

编辑 Claude Desktop 配置文件（`Settings → Developer → Edit Config`）：

```json
{
  "mcpServers": {
    "fboxmcp": {
      "transport": "streamable-http",
      "url": "https://<fboxmcp-host>",
      "headers": {
        "Authorization": "Bearer ${FBOXMCP_API_KEY}"
      }
    }
  }
}
```

### Cursor / Windsurf

在 MCP 设置中添加：

```json
{
  "mcpServers": {
    "fboxmcp": {
      "transport": "streamable-http",
      "url": "https://<fboxmcp-host>",
      "headers": {
        "Authorization": "Bearer ${FBOXMCP_API_KEY}"
      }
    }
  }
}
```

### mcporter CLI

```bash
mcporter config add fboxmcp https://<fboxmcp-host> --allow-http
# 编辑 ~/.mcporter/mcporter.json 添加 Authorization header
```

> 将 `<fboxmcp-host>` 替换为实际的服务地址。本地开发时通常为 `localhost:5151`。

---

## 第 3 步（推荐）：安装 ClawHub Skill

如果你使用 OpenClaw，强烈建议安装配套的 ClawHub Skill：

```bash
clawhub install fboxmcp
```

### 安装 Skill 前后对比

| 场景 | 未安装 Skill | 已安装 Skill |
|------|-------------|-------------|
| 工具调用 | 能调用，但 Agent 不了解业务规则 | Agent 严格按规范调用 |
| 时间展示 | 可能直接显示 UTC 时间 | 自动转为北京时间（UTC+8） |
| 参数补全 | 可能自动猜测参数 | 缺参数时返回候选列表让用户选择 |
| 写操作 | 可能不经确认直接写入 | 先展示当前值，获得用户确认后才执行 |
| 设备筛选 | 可能返回所有设备（含离线） | 默认只显示在线设备 |
| 数据展示 | 格式不统一 | 表格展示、bool 转"是/否"、时间格式化 |
| 调用链 | 可能跳步或乱序 | 按正确的工作流逐步调用 |

**原理：** MCP Server 提供工具能力，Skill 提供使用指导。两者配合才能获得最佳体验。

---

## 第 4 步：验证连接

配置完成后，重启 MCP 客户端，然后尝试对话：

```
你：我有哪些设备？
```

如果配置正确，AI 助手会调用 `get_user_box_stats` 和 `get_user_box_list` 工具，返回你的设备统计和列表。

### 验证健康检查

```bash
curl https://<fboxmcp-host>/health
```

返回 `200 OK` 表示服务正常。

### 验证工具发现

```bash
curl -X POST https://<fboxmcp-host> \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

应返回 20 个工具的列表。

---

## 可用工具一览

| 分类 | 工具 | 说明 |
|------|------|------|
| **设备管理** | get_user_box_stats | 设备统计（总数、在线、报警） |
| | get_user_box_list | 设备列表（按分组） |
| | get_user_box_info | 单设备详情 |
| | get_user_box_settings | 设备系统配置 |
| | get_user_box_location | 设备地理位置 |
| | get_sim_card_info | SIM 卡流量信息 |
| | get_user_box_plc_list | PLC 设备列表 |
| **监控点** | get_user_box_dmon_group_list | 监控点分组 |
| | get_user_box_dmon_list | 监控点列表 |
| | get_user_box_dmon_info | 监控点详情 |
| | get_user_box_dmon_value | 读取实时值 |
| | write_user_box_dmon_value | 写入值 ⚠️ |
| **报警** | get_alarm_define_list | 报警规则定义 |
| | get_current_alarm_list | 当前活跃报警 |
| | confirm_current_alarm | 确认报警 ⚠️ |
| | get_alarm_history_list | 报警历史记录 |
| **历史数据** | get_history_data_define_list | 数据条目定义 |
| | get_history_data_list | 历史数据查询 |
| **远程控制** | open_vnc | 打开 VNC 远程画面 |
| **系统** | utc_now | 服务器当前时间 |

> ⚠️ 标记的工具为写操作，AI 助手会在执行前要求你确认。

---

## 认证方式说明

本服务支持两种认证方式，通过 `Authorization` 头中 Token 的前缀自动区分：

| 方式 | 格式 | 适用场景 |
|------|------|---------|
| API Key（推荐） | `Bearer sk-xxxxxx` | AI 客户端、第三方集成。长期有效，免维护 |
| JWT Token | `Bearer eyJhbGci...` | 已有 OAuth2 体系的应用。需自行管理 Token 续期 |

两种方式完全兼容，互不影响。

---

## 常见问题

### 连接后看不到工具

- 检查 `url` 是否以 `/` 结尾
- 检查 `transport` 是否为 `streamable-http`
- 确认服务健康检查 `GET /health` 返回 200

### 返回 401 未认证

- 确认 API Key 以 `sk-` 开头
- 确认环境变量 `FBOXMCP_API_KEY` 已正确设置
- 确认 `Authorization` 头格式为 `Bearer sk-xxx`（注意 Bearer 后有空格）
- 如果使用 JWT，检查 Token 是否过期

### 返回 401 "无效的 API Key"

- API Key 可能已损坏，重新通过 `/api/apikey/generate` 生成
- 服务端 `EncryptionKey` 配置可能已变更，所有旧 Key 会失效

### 工具调用返回 Code=300

这不是错误。表示你提供的设备名称/分组名称不够精确，服务返回了候选列表。AI 助手会将选项展示给你，选择后会自动重新调用。

### 时间显示不对

所有时间字段均为 UTC 时间。安装 ClawHub Skill 后，AI 助手会自动转为北京时间（UTC+8）展示。未安装 Skill 时可能直接显示 UTC。

---

## 安全建议

1. **使用 HTTPS** — 生产环境必须启用 HTTPS，API Key 在传输层是明文
2. **保管好 API Key** — 不要将 API Key 提交到代码仓库或公开分享
3. **最小权限** — 为不同用途创建不同的 API Key
4. **定期轮换** — 建议定期重新生成 API Key
