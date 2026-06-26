---
name: consul-cli
description: >
  Consul CLI command reference for service discovery, key-value store, health checks,
  cluster management, and service mesh operations. Use when executing Consul commands
  via the command line for: (1) Starting and managing agents, (2) KV store operations,
  (3) Service registration and discovery, (4) ACL management, (5) Cluster operations,
  (6) Snapshot backup/restore, or any Consul CLI tasks.
---

# Consul CLI

HashiCorp Consul 命令行工具参考指南。

## Quick Start

```bash
# 查看所有命令
consul

# 查看命令帮助
consul <command> -h
consul <command> <subcommand> -h

# 启用自动补全
consul -autocomplete-install
```

## Global Options

```bash
consul [--version] [--help] <command> [<args>]
```

**常用全局环境变量：**
- `CONSUL_HTTP_ADDR` - Agent 地址 (默认 `http://127.0.0.1:8500`)
- `CONSUL_HTTP_TOKEN` - ACL Token
- `CONSUL_HTTP_TOKEN_FILE` - Token 文件路径
- `CONSUL_HTTP_SSL` - 启用 HTTPS
- `CONSUL_HTTP_SSL_VERIFY` - SSL 证书验证 (默认 true)
- `CONSUL_CACERT` - CA 证书路径
- `CONSUL_NAMESPACE` - 命名空间 (Enterprise)

## Agent Commands

### 启动 Agent
```bash
# 开发模式 (快速测试)
consul agent -dev

# 开发模式 + 允许外部访问
consul agent -dev -client='0.0.0.0'

# 服务器模式
consul agent -server \
  -bootstrap-expect=3 \
  -data-dir=/opt/consul/data \
  -bind=192.168.1.1 \
  -client=0.0.0.0 \
  -ui

# 加入集群
consul agent -config-dir=/etc/consul.d \
  -retry-join="provider=aws tag_key=consul tag_value=server"
```

**Agent 常用参数：**
| 参数 | 说明 |
|------|------|
| `-dev` | 开发模式 |
| `-server` | 服务器模式 |
| `-bootstrap-expect=N` | 期望服务器数量 |
| `-data-dir=<path>` | 数据目录 |
| `-bind=<IP>` | 绑定地址 |
| `-client=<IP>` | 客户端接口地址 |
| `-ui` | 启用 Web UI |
| `-join=<addr>` | 加入集群 (已弃用，用 -retry-join) |
| `-retry-join=<addr>` | 重试加入集群 |
| `-datacenter=<name>` | 数据中心名称 |
| `-node=<name>` | 节点名称 |
| `-config-dir=<path>` | 配置目录 |
| `-config-file=<path>` | 配置文件 |
| `-encrypt=<key>` | 加密密钥 |

### 管理操作
```bash
# 重载配置
consul reload

# 优雅停止
consul leave

# 强制节点离开
consul force-leave <node>

# 查看成员
consul members
consul members -detailed
consul members -wan
consul members -status=alive

# 查看信息
consul info
```

## KV Commands

```bash
consul kv <subcommand> [options] [args]
```

### 子命令
```bash
# 写入
consul kv put <key> <value>
consul kv put redis/config/connections 5
consul kv put -flags=123 mykey myvalue  # 附加 flags

# 读取
consul kv get <key>
consul kv get redis/config/connections
consul kv get -detailed <key>  # 详细信息

# 递归读取
consul kv get -recurse
consul kv get -recurse redis/

# 删除
consul kv delete <key>
consul kv delete -recurse <prefix>

# 导出/导入
consul kv export <prefix> > backup.json
consul kv import @backup.json

# 锁操作
consul kv put -acquire=<session-id> <key> <value>
consul kv put -release=<session-id> <key>
```

## Catalog Commands

```bash
consul catalog <subcommand> [options]
```

### 子命令
```bash
# 列出数据中心
consul catalog datacenters

# 列出节点
consul catalog nodes
consul catalog nodes -service=redis
consul catalog nodes -detailed

# 列出服务
consul catalog services
consul catalog services -node=<node-name>
```

## Services Commands

```bash
consul services <subcommand> [options]
```

### 子命令
```bash
# 注册服务 (命令行)
consul services register -name=web
consul services register -name=redis -tag=primary -port=6379

# 注册服务 (配置文件)
cat > web.json << 'EOF'
{
  "Service": {
    "Name": "web",
    "Tags": ["v1", "production"],
    "Port": 8080,
    "Check": {
      "HTTP": "http://localhost:8080/health",
      "Interval": "10s"
    }
  }
}
EOF
consul services register web.json

# 注销服务
consul services deregister -id=web
consul services deregister web.json
```

## ACL Commands

```bash
consul acl <subcommand> [options]
```

### Bootstrap
```bash
# 初始化 ACL 系统
consul acl bootstrap
# 返回: AccessorID, SecretID (root token)
```

### Policy 管理
```bash
# 创建策略
consul acl policy create \
  -name "service-read" \
  -description "Read access to services" \
  -rules @policy.hcl

# 列出策略
consul acl policy list

# 读取策略
consul acl policy read -name "service-read"

# 更新策略
consul acl policy update -name "service-read" -rules @new-policy.hcl

# 删除策略
consul acl policy delete -name "service-read"
```

**策略规则示例：**
```hcl
# policy.hcl
service_prefix "" {
  policy = "read"
}
key_prefix "config/" {
  policy = "write"
}
node "" {
  policy = "read"
}
```

### Token 管理
```bash
# 创建 Token
consul acl token create \
  -description "My token" \
  -policy-name "service-read"

# 列出 Token
consul acl token list

# 读取 Token
consul acl token read -accessor-id=<id>

# 更新 Token
consul acl token update -accessor-id=<id> -description "Updated"

# 删除 Token
consul acl token delete -accessor-id=<id>

# 设置 Agent Token
consul acl set-agent-token default <secret-id>
```

### Role 管理
```bash
consul acl role create -name="my-role" -policy-name="service-read"
consul acl role list
consul acl role read -name="my-role"
consul acl role delete -name="my-role"
```

## Operator Commands

```bash
consul operator <subcommand> [options]
```

### Raft 管理
```bash
# 列出 Raft 节点
consul operator raft list-peers

# 移除 Raft 节点
consul operator raft remove-peer <node-id>

# 集群状态
consul operator autopilot get-config
```

### 区域管理
```bash
# 列出区域
consul operator area list

# 创建区域
consul operator area create -name="us-west"
```

## Snapshot Commands

```bash
# 创建快照
consul snapshot save backup.snap

# 从 Agent 保存
consul snapshot save -http-addr=http://192.168.1.1:8500 backup.snap

# 恢复快照
consul snapshot restore backup.snap

# 检查快照
consul snapshot inspect backup.snap
```

## Connect / Service Mesh Commands

```bash
consul connect <subcommand> [options]
```

### Intention 管理
```bash
# 列出意图
consul intention list

# 创建意图
consul intention create web db
consul intention create -deny web malicious

# 删除意图
consul intention delete web db

# 检查意图
consul intention check web db
```

### 代理配置
```bash
# 生成代理配置
consul connect proxy-config -service=web
```

## Debug & Monitoring Commands

### Monitor
```bash
# 实时日志
consul monitor

# 指定日志级别
consul monitor -log-level=debug
```

### Debug
```bash
# 收集调试信息
consul debug -duration=30s -output=/tmp/consul-debug
```

### Info
```bash
# 运行时信息
consul info
```

### RTT
```bash
# 网络延迟估算
consul rtt <node1> <node2>
consul rtt dc1.node1 dc2.node2
```

## Event & Exec Commands

### Event
```bash
# 触发自定义事件
consul event -name="deploy" -node="web-*" "deploy v1.2.3"

# 列出事件
consul event -name="deploy" -list
```

### Exec
```bash
# 在节点上执行命令
consul exec -service=web "uptime"
consul exec -node="web-01" "systemctl restart nginx"

# 注意: 需要启用 enable_script_checks
```

## Lock Command

```bash
# 持有锁执行命令
consul lock my-lock "echo 'doing work'"

# 带超时
consul lock -timeout=30s my-lock "my-command"

# 监听模式
consul lock -monitor-retry=5 my-lock "my-command"
```

## Watch Command

```bash
# 监听变更
consul watch -type=key -key=my-key "echo 'key changed'"
consul watch -type=services "echo 'services changed'"
consul watch -type=nodes "echo 'nodes changed'"
consul watch -type=checks -service=web "echo 'checks changed'"
```

## TLS Commands

```bash
consul tls <subcommand> [options]
```

### 生成证书
```bash
# 创建 CA
consul tls ca create

# 创建服务器证书
consul tls cert create -server -dc=dc1

# 创建客户端证书
consul tls cert create -client -dc=dc1

# 指定域名
consul tls cert create -server -dc=dc1 -domain=consul -additional-dnsname=server.dc1.consul
```

## Validate Command

```bash
# 验证配置文件
consul validate /etc/consul.d/

# 验证单个文件
consul validate config.json
```

## Common Patterns

### 健康检查脚本
```bash
#!/bin/bash
# 检查服务健康状态
SERVICE=$1
STATUS=$(consul kv get -detailed "service/$SERVICE/health" | grep "Value" | awk '{print $2}')
if [ "$STATUS" != "passing" ]; then
  echo "Service $SERVICE is unhealthy"
  exit 1
fi
```

### 服务发现
```bash
# 获取服务地址
consul catalog nodes -service=web | tail -n +2 | awk '{print $3}'

# 获取服务端口
consul kv get service/web/port
```

### 集群启动脚本
```bash
#!/bin/bash
# 启动 3 节点集群
for i in 1 2 3; do
  mkdir -p /tmp/consul/node$i
  consul agent -server \
    -bootstrap-expect=3 \
    -data-dir=/tmp/consul/node$i \
    -bind=127.0.0.1 \
    -port=$((8300 + i - 1)) \
    -http-port=$((8500 + i - 1)) \
    -node=node$i &
done
```

## Exit Codes

| 代码 | 说明 |
|------|------|
| 0 | 成功 |
| 1 | 错误 |
| 2 | 连接错误 |
| 3 | 速率限制 |

## References

For detailed command reference, see:
- [cli-reference.md](references/cli-reference.md) - Complete CLI command reference