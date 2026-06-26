# Consul CLI Reference

完整的命令行参考文档。

## Table of Contents

- [Global Options](#global-options)
- [Environment Variables](#environment-variables)
- [Agent Command](#agent-command)
- [KV Commands](#kv-commands)
- [Catalog Commands](#catalog-commands)
- [Services Commands](#services-commands)
- [ACL Commands](#acl-commands)
- [Operator Commands](#operator-commands)
- [Snapshot Commands](#snapshot-commands)
- [Connect Commands](#connect-commands)
- [Debug Commands](#debug-commands)
- [TLS Commands](#tls-commands)
- [Other Commands](#other-commands)

---

## Global Options

```
consul [--version] [--help] <command> [<args>]
```

**Global Flags:**
- `-autocomplete-install` - 安装 shell 自动补全
- `-autocomplete-uninstall` - 卸载 shell 自动补全
- `-h, -help` - 显示帮助
- `-v, -version` - 显示版本

---

## Environment Variables

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `CONSUL_HTTP_ADDR` | Agent HTTP 地址 | `http://127.0.0.1:8500` |
| `CONSUL_HTTP_TOKEN` | ACL Token | - |
| `CONSUL_HTTP_TOKEN_FILE` | Token 文件路径 | - |
| `CONSUL_HTTP_AUTH` | HTTP Basic 认证 (user:pass) | - |
| `CONSUL_HTTP_SSL` | 启用 HTTPS | `false` |
| `CONSUL_HTTP_SSL_VERIFY` | SSL 证书验证 | `true` |
| `CONSUL_CACERT` | CA 证书路径 | - |
| `CONSUL_CAPATH` | CA 证书目录 | - |
| `CONSUL_CLIENT_CERT` | 客户端证书路径 | - |
| `CONSUL_CLIENT_KEY` | 客户端私钥路径 | - |
| `CONSUL_TLS_SERVER_NAME` | TLS SNI 主机名 | - |
| `CONSUL_GRPC_ADDR` | gRPC 地址 | `127.0.0.1:8502` |
| `CONSUL_NAMESPACE` | 命名空间 (Enterprise) | - |

---

## Agent Command

```
consul agent [options]
```

### 核心选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-dev` | 开发模式 | - |
| `-server` | 服务器模式 | `false` |
| `-bootstrap` | Bootstrap 模式 | - |
| `-bootstrap-expect=<N>` | 期望服务器数量 | - |
| `-data-dir=<path>` | 数据目录 | - |
| `-datacenter=<name>` | 数据中心名称 | `dc1` |
| `-node=<name>` | 节点名称 | 主机名 |
| `-node-id=<id>` | 节点 UUID | 自动生成 |
| `-node-meta=<key:value>` | 节点元数据 | - |

### 网络选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-bind=<IP>` | 集群通信绑定地址 | `0.0.0.0` |
| `-advertise=<IP>` | 广播地址 | bind 地址 |
| `-advertise-wan=<IP>` | WAN 广播地址 | - |
| `-client=<IP>` | 客户端接口地址 | `127.0.0.1` |
| `-serf-lan-bind=<IP>` | Serf LAN 绑定地址 | - |
| `-serf-wan-bind=<IP>` | Serf WAN 绑定地址 | - |

### 端口选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-http-port=<port>` | HTTP API 端口 | `8500` |
| `-https-port=<port>` | HTTPS API 端口 | `-1` (禁用) |
| `-grpc-port=<port>` | gRPC 端口 | `-1` (禁用) |
| `-dns-port=<port>` | DNS 端口 | `8600` |
| `-server-port=<port>` | Server RPC 端口 | `8300` |
| `-serf-lan-port=<port>` | Serf LAN 端口 | `8301` |
| `-serf-wan-port=<port>` | Serf WAN 端口 | `8302` |

### 集群加入选项

| 选项 | 说明 |
|------|------|
| `-retry-join=<addr>` | 重试加入的地址 (可多次指定) |
| `-retry-interval=<duration>` | 加入重试间隔 | `30s` |
| `-retry-max=<N>` | 最大重试次数 | `0` (无限) |
| `-retry-join-wan=<addr>` | WAN 加入地址 |
| `-rejoin` | 启动时忽略之前的 leave |

### 安全选项

| 选项 | 说明 |
|------|------|
| `-encrypt=<key>` | Gossip 加密密钥 (32字节 Base64) |
| `-encrypt-verify-incoming` | 验证传入消息 |
| `-encrypt-verify-outgoing` | 验证传出消息 |
| `-ca-file=<path>` | CA 证书文件 |
| `-cert-file=<path>` | 服务器证书 |
| `-key-file=<path>` | 服务器私钥 |
| `-verify-incoming` | 验证客户端证书 |
| `-verify-outgoing` | 验证服务器证书 |

### 配置选项

| 选项 | 说明 |
|------|------|
| `-config-file=<path>` | 配置文件 (可多次指定) |
| `-config-dir=<path>` | 配置目录 (可多次指定) |
| `-config-format=<json|hcl>` | 配置文件格式 |
| `-hcl=<config>` | HCL 配置片段 (可多次指定) |

### 日志选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-log-level=<level>` | 日志级别 | `info` |
| `-log-file=<path>` | 日志文件 | - |
| `-log-rotate-bytes=<N>` | 日志轮转大小 | - |
| `-log-rotate-duration=<duration>` | 轮转间隔 | `24h` |
| `-log-rotate-max-files=<N>` | 最大日志文件数 | `0` |
| `-log-json` | JSON 格式日志 | `false` |
| `-syslog` | 输出到 syslog | `false` |

### 其他选项

| 选项 | 说明 |
|------|------|
| `-ui` | 启用 Web UI |
| `-ui-dir=<path>` | UI 资源目录 |
| `-ui-content-path=<path>` | UI 路径 |
| `-pid-file=<path>` | PID 文件 |
| `-disable-host-node-id` | 禁用基于主机的节点 ID |
| `-enable-script-checks` | 启用脚本检查 |
| `-enable-local-script-checks` | 启用本地脚本检查 |

### Cloud Auto-Join

```bash
# AWS
consul agent -retry-join "provider=aws tag_key=consul tag_value=server"

# Azure
consul agent -retry-join "provider=azure tag_name=consul tag_value=server tenant_id=xxx client_id=xxx subscription_id=xxx secret_access_key=xxx"

# GCE
consul agent -retry-join "provider=gce project_name=my-project tag_value=consul"

# DigitalOcean
consul agent -retry-join "provider=digitalocean region=nyc1 tag_name=consul api_token=xxx"
```

---

## KV Commands

```
consul kv <subcommand> [options] [args]
```

### kv put
```
consul kv put [options] <key> <value>
```

| 选项 | 说明 |
|------|------|
| `-flags=<N>` | 附加标志位 |
| `-cas` | Check-And-Set 操作 |
| `-acquire=<session>` | 获取锁 |
| `-release=<session>` | 释放锁 |
| `-base64` | 值为 Base64 编码 |
| `-modify-index=<N>` | 修改索引 (配合 -cas) |

```bash
consul kv put redis/config/connections 5
consul kv put -flags=100 mykey myvalue
consul kv put -acquire=$SESSION mykey locked
consul kv put -base64 mykey dGVzdA==
```

### kv get
```
consul kv get [options] <key>
```

| 选项 | 说明 |
|------|------|
| `-detailed` | 显示详细信息 |
| `-recurse` | 递归读取 |
| `-keys` | 只返回 key 列表 |
| `-separator=<char>` | Key 分隔符 |
| `-base64` | 输出 Base64 编码 |

```bash
consul kv get redis/config/connections
consul kv get -detailed redis/config/connections
consul kv get -recurse redis/
consul kv get -keys -separator=/ config/
```

### kv delete
```
consul kv delete [options] <key>
```

| 选项 | 说明 |
|------|------|
| `-recurse` | 递归删除 |
| `-cas` | Check-And-Set 操作 |
| `-modify-index=<N>` | 修改索引 |

```bash
consul kv delete redis/config/connections
consul kv delete -recurse redis/
```

### kv export
```
consul kv export [options] <prefix>
```

```bash
consul kv export redis/ > backup.json
```

### kv import
```
consul kv import [options] <data>
```

```bash
consul kv import @backup.json
cat backup.json | consul kv import -
```

---

## Catalog Commands

```
consul catalog <subcommand> [options]
```

### catalog datacenters
```
consul catalog datacenters [options]
```

```bash
consul catalog datacenters
```

### catalog nodes
```
consul catalog nodes [options]
```

| 选项 | 说明 |
|------|------|
| `-detailed` | 详细信息 |
| `-near=<node>` | 按延迟排序 |
| `-service=<name>` | 过滤服务 |
| `-node-meta=<k:v>` | 过滤节点元数据 |
| `-filter=<expr>` | 过滤表达式 |
| `-dc=<name>` | 数据中心 |

```bash
consul catalog nodes
consul catalog nodes -service=redis
consul catalog nodes -near=_agent
```

### catalog services
```
consul catalog services [options]
```

| 选项 | 说明 |
|------|------|
| `-node=<name>` | 列出节点上的服务 |
| `-node-meta=<k:v>` | 过滤节点元数据 |
| `-dc=<name>` | 数据中心 |
| `-ns=<namespace>` | 命名空间 |

```bash
consul catalog services
consul catalog services -node=web-01
```

---

## Services Commands

```
consul services <subcommand> [options]
```

### services register
```
consul services register [options] [config-file]
```

| 选项 | 说明 |
|------|------|
| `-name=<name>` | 服务名称 |
| `-id=<id>` | 服务 ID |
| `-tag=<tag>` | 标签 (可多次指定) |
| `-address=<addr>` | 服务地址 |
| `-port=<port>` | 服务端口 |
| `-meta=<k:v>` | 元数据 (可多次指定) |
| `-check` | 健康检查定义 |

```bash
# 命令行注册
consul services register -name=web -port=8080 -tag=v1

# 配置文件注册
cat > service.json << 'EOF'
{
  "Service": {
    "Name": "web",
    "ID": "web-01",
    "Tags": ["v1", "production"],
    "Address": "192.168.1.10",
    "Port": 8080,
    "Meta": {
      "version": "1.0"
    },
    "Check": {
      "HTTP": "http://localhost:8080/health",
      "Interval": "10s",
      "Timeout": "1s"
    }
  }
}
EOF
consul services register service.json
```

### services deregister
```
consul services deregister [options] [config-file]
```

| 选项 | 说明 |
|------|------|
| `-id=<id>` | 服务 ID |

```bash
consul services deregister -id=web-01
consul services deregister service.json
```

---

## ACL Commands

```
consul acl <subcommand> [options]
```

### acl bootstrap
```
consul acl bootstrap [options]
```

```bash
consul acl bootstrap
# 返回:
# AccessorID: xxx
# SecretID: xxx (root token)
```

### acl policy
```
consul acl policy <subcommand> [options]
```

**子命令:** `create`, `read`, `update`, `delete`, `list`

| 选项 | 说明 |
|------|------|
| `-name=<name>` | 策略名称 |
| `-description=<desc>` | 描述 |
| `-rules=<rules>` | 规则 (字符串或 @file) |
| `-datacenter=<dc>` | 数据中心 (可多次指定) |
| `-ns=<namespace>` | 命名空间 |

```bash
# 创建策略
consul acl policy create -name "service-read" -rules @policy.hcl

# 列出策略
consul acl policy list

# 读取策略
consul acl policy read -name "service-read"

# 更新策略
consul acl policy update -name "service-read" -rules @new-policy.hcl

# 删除策略
consul acl policy delete -name "service-read"
```

### acl token
```
consul acl token <subcommand> [options]
```

**子命令:** `create`, `read`, `update`, `delete`, `list`, `clone`, `self`

| 选项 | 说明 |
|------|------|
| `-accessor-id=<id>` | Token 访问器 ID |
| `-secret-id=<id>` | Token 密钥 ID |
| `-description=<desc>` | 描述 |
| `-policy-id=<id>` | 关联策略 ID |
| `-policy-name=<name>` | 关联策略名称 |
| `-role-id=<id>` | 关联角色 ID |
| `-role-name=<name>` | 关联角色名称 |
| `-ttl=<duration>` | Token 有效期 |
| `-local` | 本地 Token |
| `-format=<format>` | 输出格式 |

```bash
# 创建 Token
consul acl token create \
  -description "My token" \
  -policy-name "service-read"

# 列出 Token
consul acl token list

# 读取 Token
consul acl token read -accessor-id=<id>

# 当前 Token 信息
consul acl token self

# 克隆 Token
consul acl token clone -accessor-id=<id>

# 删除 Token
consul acl token delete -accessor-id=<id>
```

### acl role
```
consul acl role <subcommand> [options]
```

```bash
consul acl role create -name="my-role" -policy-name="service-read"
consul acl role list
consul acl role read -name="my-role"
consul acl role update -name="my-role" -description="Updated"
consul acl role delete -name="my-role"
```

### acl set-agent-token
```
consul acl set-agent-token <token-type> <secret-id>
```

**Token 类型:** `default`, `config-reload`, `service-registration`, `agent-replication`

```bash
consul acl set-agent-token default <secret-id>
```

### acl auth-method
```
consul acl auth-method <subcommand> [options]
```

```bash
consul acl auth-method create -name="kubernetes" -type="kubernetes"
consul acl auth-method list
consul acl auth-method read -name="kubernetes"
consul acl auth-method delete -name="kubernetes"
```

### acl binding-rule
```
consul acl binding-rule <subcommand> [options]
```

```bash
consul acl binding-rule create -method="kubernetes" -bind-type=role -bind-name="my-role" -selector='serviceaccount.namespace=="default"'
```

---

## Operator Commands

```
consul operator <subcommand> [options]
```

### operator raft
```
consul operator raft <subcommand> [options]
```

**子命令:** `list-peers`, `remove-peer`

```bash
# 列出 Raft 节点
consul operator raft list-peers

# 移除 Raft 节点
consul operator raft remove-peer -id=<node-id>
```

### operator autopilot
```
consul operator autopilot <subcommand> [options]
```

**子命令:** `get-config`, `set-config`

```bash
# 获取配置
consul operator autopilot get-config

# 设置配置
consul operator autopilot set-config -cleanup-dead-servers=true
```

### operator area
```
consul operator area <subcommand> [options]
```

```bash
consul operator area list
consul operator area create -name="us-west" -retry-join="provider=aws..."
```

### operator segment
```
consul operator segment list
```

---

## Snapshot Commands

```
consul snapshot <subcommand> [options]
```

### snapshot save
```
consul snapshot save [options] <file>
```

```bash
consul snapshot save backup.snap
consul snapshot save -http-addr=http://192.168.1.1:8500 backup.snap
```

### snapshot restore
```
consul snapshot restore [options] <file>
```

```bash
consul snapshot restore backup.snap
```

### snapshot inspect
```
consul snapshot inspect <file>
```

```bash
consul snapshot inspect backup.snap
```

---

## Connect Commands

```
consul connect <subcommand> [options]
```

### intention
```
consul intention <subcommand> [options]
```

**子命令:** `create`, `update`, `delete`, `get`, `list`, `check`, `match`

| 选项 | 说明 |
|------|------|
| `-source=<name>` | 源服务 |
| `-destination=<name>` | 目标服务 |
| `-deny` | 拒绝意图 |
| `-allow` | 允许意图 |
| `-id=<id>` | 意图 ID |
| `-meta=<k:v>` | 元数据 |

```bash
# 创建允许意图
consul intention create web db

# 创建拒绝意图
consul intention create -deny web malicious

# 列出意图
consul intention list

# 检查意图
consul intention check web db

# 删除意图
consul intention delete web db
```

### proxy-config
```
consul connect proxy-config [options]
```

```bash
consul connect proxy-config -service=web
```

---

## Debug Commands

### members
```
consul members [options]
```

| 选项 | 说明 |
|------|------|
| `-detailed` | 详细信息 |
| `-wan` | WAN 成员 |
| `-status=<regex>` | 过滤状态 |
| `-segment=<name>` | 网络分段 |
| `-filter=<expr>` | 过滤表达式 |

```bash
consul members
consul members -detailed
consul members -wan
consul members -status=alive
```

### monitor
```
consul monitor [options]
```

| 选项 | 说明 |
|------|------|
| `-log-level=<level>` | 日志级别 |
| `-include-events` | 包含事件日志 |

```bash
consul monitor
consul monitor -log-level=debug
```

### info
```
consul info [options]
```

```bash
consul info
```

### debug
```
consul debug [options]
```

| 选项 | 说明 |
|------|------|
| `-duration=<duration>` | 收集时长 | `1m` |
| `-interval=<duration>` | 采样间隔 | `30s` |
| `-output=<path>` | 输出目录 | - |
| `-archive` | 创建压缩归档 | - |
| `-capture-profile` | 捕获 pprof | - |

```bash
consul debug -duration=30s -output=/tmp/consul-debug
```

### rtt
```
consul rtt <node1> [node2]
```

```bash
consul rtt node1 node2
consul rtt dc1.node1 dc2.node2
```

---

## TLS Commands

```
consul tls <subcommand> [options]
```

### tls ca create
```
consul tls ca create [options]
```

| 选项 | 说明 |
|------|------|
| `-name=<name>` | CA 名称 | `Consul CA` |
| `-domain=<domain>` | 域名 | `consul` |
| `-key=<path>` | 密钥输出路径 | - |
| `-cert=<path>` | 证书输出路径 | - |
| `-days=<N>` | 有效期 (天) | `3650` |

```bash
consul tls ca create
consul tls ca create -name="My CA" -domain=consul
```

### tls cert create
```
consul tls cert create [options]
```

| 选项 | 说明 |
|------|------|
| `-server` | 创建服务器证书 |
| `-client` | 创建客户端证书 |
| `-dc=<name>` | 数据中心名称 |
| `-domain=<domain>` | 域名 |
| `-ca=<path>` | CA 证书路径 |
| `-key=<path>` | CA 密钥路径 |
| `-additional-dnsname=<name>` | 额外 DNS 名称 |
| `-additional-ipaddress=<ip>` | 额外 IP 地址 |
| `-days=<N>` | 有效期 (天) |

```bash
# 创建服务器证书
consul tls cert create -server -dc=dc1

# 创建客户端证书
consul tls cert create -client -dc=dc1

# 指定 CA
consul tls cert create -server -dc=dc1 -ca=consul-agent-ca.pem -key=consul-agent-ca-key.pem
```

---

## Other Commands

### event
```
consul event [options] <name> [payload]
```

| 选项 | 说明 |
|------|------|
| `-name=<name>` | 事件名称 |
| `-node=<name>` | 目标节点 (正则) |
| `-service=<name>` | 目标服务 |
| `-tag=<tag>` | 目标标签 |
| `-token=<token>` | ACL Token |
| `-list` | 列出事件 |

```bash
consul event -name=deploy "deploy v1.2.3"
consul event -service=web -name=restart "restart now"
```

### exec
```
consul exec [options] <command>
```

| 选项 | 说明 |
|------|------|
| `-node=<name>` | 目标节点 (正则) |
| `-service=<name>` | 目标服务 |
| `-tag=<tag>` | 目标标签 |
| `-wait=<duration>` | 等待时间 |
| `-timeout=<duration>` | 超时时间 |
| `-verbose` | 详细输出 |

```bash
consul exec -service=web "uptime"
consul exec -node="web-*" "systemctl restart nginx"
```

### lock
```
consul lock [options] <key> <command>
```

| 选项 | 说明 |
|------|------|
| `-name=<name>` | 锁名称 |
| `-timeout=<duration>` | 超时 |
| `-monitor-retry=<N>` | 监控重试次数 |
| `-try=<duration>` | 尝试获取时间 |
| `-child-timeout=<duration>` | 子命令超时 |

```bash
consul lock my-lock "echo 'doing work'"
consul lock -timeout=30s my-lock "my-command"
```

### watch
```
consul watch [options] <handler>
```

| 选项 | 说明 |
|------|------|
| `-type=<type>` | 监视类型 |
| `-key=<key>` | 监视的 key |
| `-service=<name>` | 监视的服务 |
| `-tag=<tag>` | 服务标签 |
| `-state=<state>` | 健康状态 |
| `-token=<token>` | ACL Token |

**监视类型:** `key`, `keyprefix`, `services`, `nodes`, `service`, `checks`, `event`

```bash
consul watch -type=key -key=my-key "echo 'changed'"
consul watch -type=services "echo 'services changed'"
consul watch -type=service -service=web "echo 'web changed'"
```

### validate
```
consul validate [options] <path>
```

```bash
consul validate /etc/consul.d/
consul validate config.json
```

### version
```
consul version
```

### keygen
```
consul keygen
# 输出: 32字节 Base64 加密密钥
```

### keyring
```
consul keyring <subcommand> [options]
```

**子命令:** `list`, `install`, `use`, `remove`

```bash
consul keyring list
consul keyring install -key=<new-key>
consul keyring use -key=<key>
consul keyring remove -key=<old-key>
```

### force-leave
```
consul force-leave [options] <node>
```

```bash
consul force-leave web-01
consul force-leave -prune web-01
consul force-leave -wan web-01
```

### leave
```
consul leave [options]
```

```bash
consul leave
consul leave -self
```

### reload
```
consul reload [options]
```

```bash
consul reload
```

### login
```
consul login [options]
```

```bash
consul login -method=kubernetes -bearer-token-file=/var/run/secrets/kubernetes.io/serviceaccount/token
```

### logout
```
consul logout [options]
```

```bash
consul logout
```

---

## Exit Codes

| 代码 | 说明 |
|------|------|
| 0 | 成功 |
| 1 | 命令错误 |
| 2 | 连接错误 |
| 3 | 速率限制 |

---

## Common Patterns

### 服务健康检查脚本
```bash
#!/bin/bash
SERVICE=$1

# 获取健康实例
HEALTHY=$(consul catalog nodes -service=$SERVICE 2>/dev/null | wc -l)

if [ $HEALTHY -eq 0 ]; then
  echo "CRITICAL: No healthy $SERVICE instances"
  exit 2
fi

echo "OK: $HEALTHY healthy $SERVICE instances"
exit 0
```

### 动态服务发现
```bash
#!/bin/bash
SERVICE=$1

# 获取服务地址
consul catalog nodes -service=$SERVICE -detailed | \
  awk '/Address/ {addr=$3} /ServicePort/ {port=$2; print addr":"port}'
```

### 集群健康监控
```bash
#!/bin/bash

# 检查 leader
LEADER=$(consul operator raft list-peers | grep leader)
if [ -z "$LEADER" ]; then
  echo "CRITICAL: No leader"
  exit 2
fi

# 检查节点数
NODES=$(consul members -status=alive | wc -l)
echo "OK: $NODES alive nodes, Leader: $(echo $LEADER | awk '{print $3}')"
```

### KV 配置同步
```bash
#!/bin/bash
# 从 KV 导出配置

consul kv get -recurse config/ | while read line; do
  KEY=$(echo $line | awk '{print $1}')
  VALUE=$(echo $line | awk '{print $2}')
  echo "$KEY=$VALUE" >> /etc/app/config.env
done
```