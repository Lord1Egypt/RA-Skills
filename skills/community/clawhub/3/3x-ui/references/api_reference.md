# 3x-ui API 完整参考

## 认证方式

两种认证方式皆可用于 `/panel/api/*` 下的所有端点：

### Bearer Token（推荐）
```
Authorization: Bearer <token>
```
在 Settings → Security → API Token 中创建/管理。Token认证跳过了CSRF。

### Session Cookie
```
POST /panel/login
Body: { "username": "admin", "password": "***", "twoFactorCode": "123456" }
```

### 统一响应格式
```json
{ "success": true, "msg": "", "obj": ... }
```

---

## 1. Inbounds（入站管理）

所有端点位于 `/panel/api/inbounds`

### GET /panel/api/inbounds/list
列出所有入站含客户端流量统计。settings/streamSettings/sniffing 为嵌套JSON对象。

### GET /panel/api/inbounds/list/slim
精简列表，settings.clients[] 仅保留 {email, enable, comment}。

### GET /panel/api/inbounds/options
轻量下拉选项，返回 {id, remark, protocol, port, tlsFlowCapable}。

### GET /panel/api/inbounds/get/:id
单个入站详情。

### POST /panel/api/inbounds/add
新增入站。Body示例：
```json
{
  "enable": true,
  "remark": "VLESS-443",
  "port": 443,
  "protocol": "vless",
  "settings": { "clients": [], "decryption": "none", "fallbacks": [] },
  "streamSettings": { "network": "tcp", "security": "reality", "realitySettings": { "show": false, "dest": "..." } },
  "sniffing": { "enabled": true, "destOverride": ["http", "tls"] },
  "expiryTime": 0,
  "total": 0,
  "listen": ""
}
```

### POST /panel/api/inbounds/del/:id
删除入站。同时删除关联的客户端统计。

### POST /panel/api/inbounds/update/:id
全量替换入站配置。Body形状同 add。

### POST /panel/api/inbounds/setEnable/:id
仅开关：`{ "enable": false }`。大量用户时推荐此方式而非update全量。

### POST /panel/api/inbounds/:id/resetTraffic
重置单入站上下行计数器。

### POST /panel/api/inbounds/resetAllTraffics
重置所有入站计数器。

### POST /panel/api/inbounds/import
批量导入，form编码，字段名 `data`，值为JSON字符串。

### GET /panel/api/inbounds/:id/fallbacks
查看fallback规则列表。返回 {id, masterId, childId, name, alpn, path, xver, sortOrder}。

### POST /panel/api/inbounds/:id/fallbacks
替换fallback规则。Body: `{ "fallbacks": [{childId, name, alpn, path, xver, sortOrder}] }`。

---

## 2. Clients（客户端管理）

所有端点位于 `/panel/api/clients`。客户端用 email 作为唯一标识符。

### GET /panel/api/clients/list
所有客户端。含 {id, email, subId, uuid, totalGB, expiryTime, enable, reverse, inboundIds, traffic}。

### GET /panel/api/clients/list/paged
分页查询。参数：page, pageSize(默认25,上限200), search(模糊匹配email/subId/comment), filter(online/active/deactive/depleted/expiring), protocol(vless/vmess/trojan/...), sort(enable/email/inboundIds/traffic/remaining/expiryTime), order(ascend/descend)。返回含 summary {total, active, online, depleted, expiring, deactive}。

### GET /panel/api/clients/get/:email
单个客户端详情，含关联的 inboundIds。

### POST /panel/api/clients/add
新增客户端并关联入站。UUID/密码等服务端自动生成。
```json
{
  "client": { "email": "...", "totalGB": 53687091200, "expiryTime": 1735689600000, "tgId": 0, "limitIp": 0, "enable": true },
  "inboundIds": [3, 5]
}
```

### POST /panel/api/clients/update/:email
全量替换客户端信息（不是patch，是replace）。

### POST /panel/api/clients/del/:email
删除客户端。可选 `?keepTraffic=1` 保留流量记录。

### POST /panel/api/clients/:email/attach
关联到更多入站：`{ "inboundIds": [7, 9] }`

### POST /panel/api/clients/:email/detach
解除入站关联：`{ "inboundIds": [5] }`

### POST /panel/api/clients/resetAllTraffics
全局重置所有客户端上下行。

### POST /panel/api/clients/delDepleted
删除所有流量耗尽/过期的客户端。返回 `{ deleted: N }`，触发Xray重启。

### POST /panel/api/clients/bulkAdjust
批量调整。支持负数。过期Time=0或totalGB=0的跳过。
```json
{ "emails": ["alice", "bob"], "addDays": 30, "addBytes": 53687091200 }
```
返回 {adjusted, skipped[{email, reason}]}

### POST /panel/api/clients/resetTraffic/:email
重置单客户端流量，自动重新启用并推送到Xray/节点。

### POST /panel/api/clients/updateTraffic/:email
手动调流量：`{ "upload": 1073741824, "download": 5368709120 }`

### POST /panel/api/clients/ips/:email
查看客户端连接IP列表。

### POST /panel/api/clients/clearIps/:email
清空IP记录。

### POST /panel/api/clients/onlines
当前在线用户邮箱列表。

### POST /panel/api/clients/lastOnline
email→lastSeenTimestamp映射。

### GET /panel/api/clients/traffic/:email
单用户流量统计：{email, up, down, total, expiryTime}

### GET /panel/api/clients/subLinks/:subId
JSON格式订阅链接数组（非base64）。

### GET /panel/api/clients/links/:email
完整多协议URL列表（vless:// vmess:// trojan:// ss:// hysteria:// hy2://）。不支持URL形式的协议（socks/http/wireguard等）不返回。

---

## 3. Server（服务器管理）

所有端点位于 `/panel/api/server`

### GET /panel/api/server/status
实时系统快照，每2秒缓存刷新。
```json
{ "cpu": 12.5, "mem": {"current": 2147483648,"total": 8589934592}, "swap": {...}, "disk": {...}, "netIO": {"up":...,"down":...}, "xray": {"state":"running","version":"v25.10.31"}, "tcpCount": 42, "load": {"load1":0.5,"load5":0.3,"load15":0.2} }
```

### GET /panel/api/server/cpuHistory/:bucket
已废弃，用 `/history/cpu/:bucket`。bucket允许值：2,30,60,120,180,300。

### GET /panel/api/server/history/:metric/:bucket
6小时聚合时序数据。metric: cpu/mem/netUp/netDown/online/load1/load5/load15。返回 [{t, v}]。

### GET /panel/api/server/xrayMetricsState
Xray运行时指标。当xray配置没有metrics块时返回空。

### GET /panel/api/server/xrayMetricsHistory/:metric/:bucket
Xray指标历史。metric: xrAlloc/xrSys/xrHeapObjects/xrNumGC/xrPauseNs。

### GET /panel/api/server/xrayObservatory
探测结果快照（需配置observatory）。

### GET /panel/api/server/xrayObservatoryHistory/:tag/:bucket
单出站tag的探测历史。

### GET /panel/api/server/getXrayVersion
可选安装版本列表。

### GET /panel/api/server/getPanelUpdateInfo
检查面板更新。

### GET /panel/api/server/getConfigJson
当前运行的Xray完整配置。

### GET /panel/api/server/getDb
下载SQLite数据库文件。

### GET /panel/api/server/getNewUUID
生成新UUID v4。

### GET /panel/api/server/getNewX25519Cert
生成X25519密钥对（Reality用）。返回 {privateKey, publicKey}。

### GET /panel/api/server/getNewmldsa65
生成ML-DSA-65密钥对（后量子签名）。返回 {privateKey, publicKey, seed}。

### GET /panel/api/server/getNewmlkem768
生成ML-KEM-768密钥对（后量子KEM）。返回 {clientKey, serverKey}。

### GET /panel/api/server/getNewVlessEnc
生成VLESS加密认证选项。返回 {auths: [{id, label, encryption, decryption}]}。

### POST /panel/api/server/stopXrayService
停止Xray。

### POST /panel/api/server/restartXrayService
重启Xray。配置修改后需调用。

### POST /panel/api/server/installXray/:version
下载安装指定版本。`latest` 为最新版。

### POST /panel/api/server/updatePanel
面板自更新。

### POST /panel/api/server/updateGeofile
刷新GeoIP/GeoSite。支持 `fileName` 参数指定单个文件。

### POST /panel/api/server/updateGeofile/:fileName
刷新指定Geo文件。

### POST /panel/api/server/logs/:count
面板日志最后N行。Body: `{ "level": "info", "syslog": false }`

### POST /panel/api/server/xraylogs/:count
Xray日志最后N行。支持过滤。
Body参数: filter(关键词), showDirect(true/false), showBlocked(true/false), showProxy(true/false)

### POST /panel/api/server/importDB
恢复数据库。multipart form，field name="db"。

### POST /panel/api/server/getNewEchCert
生成ECH密钥对。Body: `sni=example.com`。返回 {echKeySet, echServerKeys, echConfigList}。

---

## 4. Nodes（节点管理）

所有端点位于 `/panel/api/nodes`

### GET /panel/api/nodes/list
节点列表。含 {id, name, address, port, scheme, apiToken, status, lastHeartbeat, latencyMs, xrayVersion, panelVersion, cpuPct, memPct, uptimeSecs, inboundCount, clientCount, onlineCount, depletedCount}。

### GET /panel/api/nodes/get/:id
单节点详情。

### POST /panel/api/nodes/add
新增节点。Body:
```json
{ "name": "de-fra-1", "scheme": "https", "address": "node1.example.com", "port": 2053, "basePath": "/", "apiToken": "...", "enable": true, "allowPrivateAddress": false }
```

### POST /panel/api/nodes/update/:id
更新节点。

### POST /panel/api/nodes/del/:id
删除节点（入站不会迁移）。

### POST /panel/api/nodes/setEnable/:id
开关节点：`{ "enable": true/false }`

### POST /panel/api/nodes/test
测试连接但不保存。Body同add结构，返回 {status, latencyMs, xrayVersion, panelVersion, cpuPct, memPct, uptimeSecs, error}。

### POST /panel/api/nodes/probe/:id
探测已有节点，更新缓存状态。

### GET /panel/api/nodes/history/:id/:metric/:bucket
节点指标历史，metric: cpu/mem。

---

## 5. Custom Geo

位于 `/panel/api/custom-geo`

- `GET /list` — 自定义geo源列表
- `GET /aliases` — 可用geo别名（含自带）
- `POST /add` — 新增 {type, alias, url}
- `POST /update/:id` — 修改
- `POST /delete/:id` — 删除
- `POST /download/:id` — 重新下载
- `POST /update-all` — 全部重新下载

---

## 6. Backup

### POST /panel/api/backuptotgbot
发送DB备份到Telegram。

---

## 7. Settings（面板设置）

位于 `/panel/setting`

- `POST /all` — 所有面板设置（含web/tgBot/sub/security）
- `POST /defaultSettings` — 默认设置预览
- `POST /update` — 保存所有设置
- `POST /updateUser` — 改管理员密码 `{oldUsername, oldPassword, newUsername, newPassword}`
- `POST /restartPanel` — 重启面板
- `GET /getDefaultJsonConfig` — 内置默认Xray配置
- `GET /apiTokens` — Token列表
- `POST /apiTokens/create` — 创建Token `{name}`
- `POST /apiTokens/delete/:id` — 删除Token
- `POST /apiTokens/setEnabled/:id` — 开关Token `{enabled}`

---

## 8. Xray Settings

位于 `/panel/xray`

- `POST /` — Xray模板+入站标签+出站测试URL
- `GET /getDefaultJsonConfig` — 默认配置
- `GET /getOutboundsTraffic` — 出站流量
- `GET /getXrayResult` — Xray进程输出
- `POST /update` — 保存模板
- `POST /warp/:action` — Warp管理（data/del/config/reg/license）
- `POST /nord/:action` — NordVPN管理（countries/servers/reg/setKey/data/del）
- `POST /resetOutboundsTraffic` — 重置出站 `tag=proxy`
- `POST /testOutbound` — 测试出站 `outbound={...}&mode=tcp`

---

## 9. Subscription（订阅服务器）

独立端口，默认10882。路由可配置。

响应头：Subscription-Userinfo(upload/download/total/expire), Profile-Title, Profile-Web-Page-Url, Support-Url, Profile-Update-Interval, Announce, Routing-Enable, Routing

- `GET /{subPath}:subid` — 标准base64订阅，`?html=1` 显示信息页
- `GET /{jsonPath}:subid` — JSON格式
- `GET /{clashPath}:subid` — Clash YAML格式

---

## 10. WebSocket

### GET /ws
实时推送（需Session Cookie，不支持Bearer Token）。

消息类型：
| type | 说明 | data |
|------|------|------|
| status | 服务器快照(每2秒) | 同 /server/status |
| xrayState | Xray状态变更 | "running"/"stopped" |
| notification | 面板通知 | {title, body, severity} |
| invalidate | 数据变更通知 | {resource: "inbounds"} |
