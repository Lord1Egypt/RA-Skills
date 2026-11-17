---
name: 3x-ui
description: 3x-ui面板REST API交互。用于管理Xray代理面板的入站/出站配置、客户端(用户)管理、节点管理、服务器状态监控、订阅管理、备份等功能。当用户需要操作3x-ui面板、查询代理服务器状态、管理用户/流量/订阅链接时使用。支持Bearer Token和Session Cookie两种认证方式。
---

# 3x-ui Panel API Skill

3x-ui 是一个 Xray 代理管理面板，提供完整的 REST API 进行管理操作。

## 认证

### Bearer Token（推荐）
在面板 Settings → Security 中创建 API Token，然后：

```
Authorization: Bearer <token>
```

### Session Cookie
```
POST /panel/api/login
Body: { "username": "admin", "password": "***" }
```

## 基础 URL
```
https://<panel-host>:<port>/panel/api/
```

所有 API 返回统一格式：
```json
{ "success": true/false, "msg": "...", "obj": ... }
```

## 核心 API 速查

### Inbounds（入站管理）

| 操作 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | `inbounds/list` | 所有入站（含完整配置） |
| 精简列表 | GET | `inbounds/list/slim` | 不含完整client详情 |
| 下拉选项 | GET | `inbounds/options` | 仅id/remark/protocol/port，轻量 |
| 详情 | GET | `inbounds/get/:id` | 单个入站完整信息 |
| 新增 | POST | `inbounds/add` | Body含完整config（settings/streamSettings/sniffing为嵌套JSON） |
| 删除 | POST | `inbounds/del/:id` | |
| 修改 | POST | `inbounds/update/:id` | 全量替换 |
| 开关 | POST | `inbounds/setEnable/:id` | 仅传 `{ "enable": true/false }` |
| 重置流量 | POST | `inbounds/:id/resetTraffic` | 重置单入站上下行 |
| 重置全部 | POST | `inbounds/resetAllTraffics` | |
| 批量导入 | POST | `inbounds/import` | form格式，`data`字段传JSON |
| 回退规则 | GET/POST | `inbounds/:id/fallbacks` | 查看/替换fallback规则 |

### Clients（客户端管理）

| 操作 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | `clients/list` | 所有客户端 |
| 分页列表 | GET | `clients/list/paged` | 支持search/filter/sort/page |
| 详情 | GET | `clients/get/:email` | 按email查 |
| 新增 | POST | `clients/add` | Body: `{ client: {...}, inboundIds: [...] }`，UUID/密码自动生成 |
| 修改 | POST | `clients/update/:email` | 全量替换 |
| 删除 | POST | `clients/del/:email` | 可选 `?keepTraffic=1` 保留流量记录 |
| 关联入站 | POST | `clients/:email/attach` | `{ inboundIds: [...] }` |
| 解除关联 | POST | `clients/:email/detach` | `{ inboundIds: [...] }` |
| 批量调整 | POST | `clients/bulkAdjust` | `{ emails, addDays, addBytes }` 批量续期/加流量 |
| 重置流量 | POST | `clients/resetTraffic/:email` | 单个重置 |
| 修改流量 | POST | `clients/updateTraffic/:email` | 手动调上下行计数 |
| 查看IP | POST | `clients/ips/:email` | 连过的IP列表 |
| 清空IP | POST | `clients/clearIps/:email` | |
| 在线用户 | POST | `clients/onlines` | 当前在线邮箱列表 |
| 最后在线 | POST | `clients/lastOnline` | email→timestamp映射 |
| 流量查询 | GET | `clients/traffic/:email` | 单用户流量 |
| 订阅链接 | GET | `clients/subLinks/:subId` | JSON格式订阅链接 |
| 完整链接 | GET | `clients/links/:email` | 所有协议URL |

### Server（服务器管理）

| 操作 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 状态 | GET | `server/status` | CPU/内存/磁盘/Xray运行状态等 |
| CPU历史 | GET | `server/cpuHistory/:bucket` | 已废弃，用history替代 |
| 历史指标 | GET | `server/history/:metric/:bucket` | 6小时聚合数据；metric: cpu/mem/netUp/netDown/online/load1/load5/load15 |
| Xray指标 | GET | `server/xrayMetricsState` | Xray运行时指标状态 |
| Xray历史 | GET | `server/xrayMetricsHistory/:metric/:bucket` | Xray指标6小时历史 |
| 观测状态 | GET | `server/xrayObservatory` | 出站延迟/健康状态 |
| 版本列表 | GET | `server/getXrayVersion` | 可选安装的Xray版本 |
| 面板更新 | GET | `server/getPanelUpdateInfo` | 检查面板更新 |
| 运行配置 | GET | `server/getConfigJson` | 当前运行的Xray配置 |
| 下载DB | GET | `server/getDb` | 下载SQLite数据库备份 |
| 生成UUID | GET | `server/getNewUUID` | 生成UUID v4 |
| 生成X25519 | GET | `server/getNewX25519Cert` | 用于Reality的密钥对 |
| 停止Xray | POST | `server/stopXrayService` | |
| 重启Xray | POST | `server/restartXrayService` | 修改配置后需要调用 |
| 安装Xray | POST | `server/installXray/:version` | |
| 更新面板 | POST | `server/updatePanel` | |
| 更新Geo | POST | `server/updateGeofile` | |
| 面板日志 | POST | `server/logs/:count` | 面板自身日志 |
| Xray日志 | POST | `server/xraylogs/:count` | 支持filter/showDirect/showBlocked/showProxy过滤 |
| 恢复DB | POST | `server/importDB` | multipart上传SQLite文件 |
| DCV证书 | POST | `server/getNewEchCert` | `sni=example.com` |

### Nodes（节点管理 - 多服务器集群）

| 操作 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | `nodes/list` | 所有节点（含连接状态/延迟/版本等） |
| 详情 | GET | `nodes/get/:id` | |
| 新增 | POST | `nodes/add` | `{ scheme, address, port, basePath, apiToken, enable }` |
| 修改 | POST | `nodes/update/:id` | |
| 删除 | POST | `nodes/del/:id` | |
| 开关 | POST | `nodes/setEnable/:id` | `{ enable: true/false }` |
| 测试 | POST | `nodes/test` | 不保存只探测节点状态 |
| 探测 | POST | `nodes/probe/:id` | 更新已保存节点的缓存状态 |
| 历史 | GET | `nodes/history/:id/:metric/:bucket` | 节点指标历史 |

### Settings（面板设置）

| 操作 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 全部设置 | POST | `setting/all` | 返回所有面板设置 |
| 默认设置 | POST | `setting/defaultSettings` | 预览新安装的默认配置 |
| 更新设置 | POST | `setting/update` | 保存所有设置 |
| 修改密码 | POST | `setting/updateUser` | 需提供旧密码验证 `{ oldUsername, oldPassword, newUsername, newPassword }` |
| 重启面板 | POST | `setting/restartPanel` | 3秒后重启 |
| 默认配置 | GET | `setting/getDefaultJsonConfig` | 内置默认Xray配置模板 |
| Token列表 | GET | `setting/apiTokens` | |
| 创建Token | POST | `setting/apiTokens/create` | `{ name }` |
| 删除Token | POST | `setting/apiTokens/delete/:id` | |
| 开关Token | POST | `setting/apiTokens/setEnabled/:id` | `{ enabled }` |

### Xray Configuration

| 操作 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 配置模板 | POST | `xray/` | Xray配置模板+入站标签+出站测试URL |
| 默认配置 | GET | `xray/getDefaultJsonConfig` | |
| 出站流量 | GET | `xray/getOutboundsTraffic` | 各出站流量统计 |
| Xray输出 | GET | `xray/getXrayResult` | 最近stdout/stderr |
| 更新配置 | POST | `xray/update` | 保存Xray JSON模板+出站测试URL |
| Warp管理 | POST | `xray/warp/:action` | action: data/del/config/reg/license |
| Nord管理 | POST | `xray/nord/:action` | action: countries/servers/reg/setKey/data/del |
| 重置出站 | POST | `xray/resetOutboundsTraffic` | `tag=proxy` |
| 测试出站 | POST | `xray/testOutbound` | `outbound={...}&mode=tcp` |

### 订阅服务器
运行在独立端口（默认10882），返回base64/JSON/Clash格式订阅。

| 路径 | 说明 |
|------|------|
| `/{subPath}:subid` | 标准base64订阅，`?html=1` 显示信息页 |
| `/{jsonPath}:subid` | JSON格式 |
| `/{clashPath}:subid` | Clash YAML格式 |

### WebSocket
`ws://<panel>/ws` 获取实时推送（需Session Cookie认证）：
- `type: status` — 每2秒服务器快照
- `type: xrayState` — Xray状态变更
- `type: notification` — 面板通知
- `type: invalidate` — 数据变更通知

## 常用工作流脚本

见 `scripts/` 目录，包含：
- `list_users.sh` — 列出所有用户
- `add_user.sh` — 添加用户
- `server_status.sh` — 查看服务器状态
- `toggle_inbound.sh` — 开关入站

## 完整 API 参考

见 `references/api_reference.md`
