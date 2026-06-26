# Clash Verge / mihomo API 参考

完整的 RESTful API 文档，基于 mihomo (Clash.Meta) 内核。

## 认证

所有需要认证的请求携带以下请求头：

```
Authorization: Bearer ${secret}
```

`${secret}` 为配置文件中设置的密钥。

---

## 请求示例

```bash
curl -H 'Authorization: Bearer ${secret}' \
     http://127.0.0.1:9090/configs?force=true \
     -d '{"path": "", "payload": ""}' -X PUT
```

---

## 日志

### GET /logs

获取实时日志（HTTP 轮询或 WebSocket）

**参数：**
- `?level=info|warning|error|debug` - 日志级别过滤

**WebSocket：**
```bash
ws://127.0.0.1:9090/logs?level=info
```

---

## 流量信息

### GET /traffic

获取实时流量（WebSocket）

**返回：** 流量单位为 kbps

```bash
ws://127.0.0.1:9090/traffic
```

---

## 内存信息

### GET /memory

获取实时内存占用

**返回：** 内存单位为 kb

```bash
curl http://127.0.0.1:9090/memory
```

---

## 版本信息

### GET /version

获取 mihomo 版本信息

```bash
curl http://127.0.0.1:9090/version
```

---

## 缓存

### POST /cache/fakeip/flush

清除 FakeIP 缓存

```bash
curl -X POST http://127.0.0.1:9090/cache/fakeip/flush \
  -H "Authorization: Bearer ${secret}"
```

### POST /cache/dns/flush

清除 DNS 缓存

```bash
curl -X POST http://127.0.0.1:9090/cache/dns/flush \
  -H "Authorization: Bearer ${secret}"
```

---

## 运行配置

### GET /configs

获取基本配置

```bash
curl http://127.0.0.1:9090/configs
```

### PUT /configs

重新加载基本配置

**参数：**
- `?force=true` - 强制重新加载

```bash
curl -X PUT "http://127.0.0.1:9090/configs?force=true" \
  -H "Authorization: Bearer ${secret}" \
  -H "Content-Type: application/json" \
  -d '{"path": "", "payload": ""}'
```

### PATCH /configs

更新基本配置（部分更新）

```bash
curl -X PATCH http://127.0.0.1:9090/configs \
  -H "Authorization: Bearer ${secret}" \
  -H "Content-Type: application/json" \
  -d '{"mixed-port": 7890}'
```

### POST /configs/geo

更新 GEO 数据库

```bash
curl -X POST http://127.0.0.1:9090/configs/geo \
  -H "Authorization: Bearer ${secret}" \
  -H "Content-Type: application/json" \
  -d '{"path": "", "payload": ""}'
```

---

## 内核管理

### POST /restart

重启内核

```bash
curl -X POST http://127.0.0.1:9090/restart \
  -H "Authorization: Bearer ${secret}" \
  -H "Content-Type: application/json" \
  -d '{"path": "", "payload": ""}'
```

### POST /upgrade

更新内核

```bash
curl -X POST http://127.0.0.1:9090/upgrade \
  -H "Authorization: Bearer ${secret}" \
  -H "Content-Type: application/json" \
  -d '{"path": "", "payload": ""}'
```

### POST /upgrade/ui

更新用户界面

```bash
curl -X POST http://127.0.0.1:9090/upgrade/ui \
  -H "Authorization: Bearer ${secret}"
```

### POST /upgrade/geo

更新 GEO 数据库

```bash
curl -X POST http://127.0.0.1:9090/upgrade/geo \
  -H "Authorization: Bearer ${secret}" \
  -H "Content-Type: application/json" \
  -d '{"path": "", "payload": ""}'
```

---

## 策略组

### GET /group

获取所有策略组信息

```bash
curl http://127.0.0.1:9090/group
```

### GET /group/{group_name}

获取指定策略组信息

```bash
curl http://127.0.0.1:9090/group/Proxy
```

### DELETE /group/{group_name}

清除自动策略组的 fixed 选择

```bash
curl -X DELETE http://127.0.0.1:9090/group/Auto%20Group \
  -H "Authorization: Bearer ${secret}"
```

### GET /group/{group_name}/delay

对策略组内节点进行延迟测试

**参数：**
- `?url=xxx` - 测试 URL
- `?timeout=5000` - 超时时间(毫秒)

```bash
curl "http://127.0.0.1:9090/group/Proxy/delay?url=https://www.google.com&timeout=5000"
```

---

## 代理

### GET /proxies

获取所有代理信息

```bash
curl http://127.0.0.1:9090/proxies
```

### GET /proxies/{name}

获取指定代理信息

```bash
curl http://127.0.0.1:9090/proxies/%E9%A6%96%E6%B8%B8%E8%8A%82%E7%82%B9
```

### PUT /proxies/{name}

选择代理

```bash
curl -X PUT http://127.0.0.1:9090/proxies/Proxy \
  -H "Authorization: Bearer ${secret}" \
  -H "Content-Type: application/json" \
  -d '{"name": "香港节点"}'
```

### GET /proxies/{name}/delay

测试代理延迟

```bash
curl "http://127.0.0.1:9090/proxies/%E9%A6%96%E6%B8%B8/delay?url=https://www.google.com&timeout=5000"
```

---

## 代理集合

### GET /providers/proxies

获取所有代理集合信息

```bash
curl http://127.0.0.1:9090/providers/proxies
```

### GET /providers/proxies/{name}

获取指定代理集合信息

```bash
curl http://127.0.0.1:9090/providers/proxies/provider-name
```

### PUT /providers/proxies/{name}

更新代理集合

```bash
curl -X PUT http://127.0.0.1:9090/providers/proxies/provider-name \
  -H "Authorization: Bearer ${secret}" \
  -H "Content-Type: application/json" \
  -d '{"path": "", "payload": ""}'
```

### GET /providers/proxies/{name}/healthcheck

触发代理集合健康检查

```bash
curl http://127.0.0.1:9090/providers/proxies/provider-name/healthcheck
```

### GET /providers/proxies/{name}/{proxy}/healthcheck

测试代理集合内指定代理延迟

```bash
curl "http://127.0.0.1:9090/providers/proxies/provider-name/proxy-name/healthcheck?url=https://www.google.com&timeout=5000"
```

---

## 规则

### GET /rules

获取所有规则信息

```bash
curl http://127.0.0.1:9090/rules
```

### PATCH /rules/disable

禁用/启用规则

**请求数据：**
```json
{"0": false, "1": true}
```
key 为规则索引，value 为是否禁用（临时操作，重启后失效）

```bash
curl -X PATCH http://127.0.0.1:9090/rules/disable \
  -H "Authorization: Bearer ${secret}" \
  -H "Content-Type: application/json" \
  -d '{"0": false, "1": true}'
```

---

## 规则集合

### GET /providers/rules

获取所有规则集合信息

```bash
curl http://127.0.0.1:9090/providers/rules
```

### PUT /providers/rules/{name}

更新规则集合

```bash
curl -X PUT http://127.0.0.1:9090/providers/rules/ruleset-name \
  -H "Authorization: Bearer ${secret}" \
  -H "Content-Type: application/json" \
  -d '{"path": "", "payload": ""}'
```

---

## 连接

### GET /connections

获取连接信息

**参数：**
- `?interval=1000` - 刷新间隔(毫秒)

**WebSocket：**
```bash
ws://127.0.0.1:9090/connections?interval=1000
```

```bash
curl "http://127.0.0.1:9090/connections?interval=1000"
```

### DELETE /connections

关闭所有连接

```bash
curl -X DELETE http://127.0.0.1:9090/connections \
  -H "Authorization: Bearer ${secret}"
```

### DELETE /connections/{id}

关闭指定连接

```bash
curl -X DELETE http://127.0.0.1:9090/connections/conn-id \
  -H "Authorization: Bearer ${secret}"
```

---

## DNS 查询

### GET /dns/query

查询指定域名的 DNS 数据

**参数：**
- `?name=example.com` - 查询的域名
- `?type=A|AAAA|CNAME|MX|...` - 记录类型

```bash
curl "http://127.0.0.1:9090/dns/query?name=example.com&type=A"
```

---

## DEBUG 接口

> ⚠️ 需要内核启动时日志级别为 debug

### PUT /debug/gc

主动触发垃圾回收

```bash
curl -X PUT http://127.0.0.1:9090/debug/gc \
  -H "Authorization: Bearer ${secret}"
```

### GET /debug/pprof

性能分析（需安装 Graphviz 查看图形化）

```bash
# 查看 heap 信息
go tool pprof -http=:8080 http://127.0.0.1:9090/debug/pprof/heap

# 查看 allocs 信息
go tool pprof -http=:8080 http://127.0.0.1:9090/debug/pprof/allocs

# 下载原始数据
curl -o heap.prof "http://127.0.0.1:9090/debug/pprof/heap?raw=true"
```

---

## 响应格式

### 成功响应

```json
{
  "name": "香港节点",
  "type": "ss",
  "history": [...]
}
```

### 延迟测试响应

```json
{
  "delay": 120,
  "loss": 0
}
```

### 连接列表响应

```json
{
  "connections": [
    {
      "id": "conn-uuid",
      "metadata": {
        "network": "tcp",
        "type": "HTTP",
        "sourceIP": "192.168.1.100",
        "destinationIP": "8.8.8.8",
        "destinationPort": 80,
        "host": "example.com"
      },
      "upload": 1024,
      "download": 2048,
      "start": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

## 错误处理

常见错误码：

| 状态码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未授权（缺少或错误的 secret） |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
