# Clash VPN 配置模板

## 配置说明

此文件包含 Clash VPN 的配置模板和示例。

## 最小配置示例

```yaml
port: 7890
socks-port: 7891
mixed-port: 7893
allow-lan: true
mode: rule
log-level: info
external-controller: 0.0.0.0:9090

dns:
  enable: true
  listen: 0.0.0.0:53
  nameserver:
    - 119.29.29.29
    - 223.5.5.5

proxies:
  - {name: "节点1", server: server1.example.com, port: 443, type: ss, cipher: chacha20-ietf-poly1305, password: password1}
  - {name: "节点2", server: server2.example.com, port: 443, type: ss, cipher: chacha20-ietf-poly1305, password: password2}

proxy-groups:
  - name: 🚀 节点选择
    type: select
    proxies:
      - 节点1
      - 节点2

rules:
  - DOMAIN-SUFFIX,local,DIRECT
  - IP-CIDR,127.0.0.0/8,DIRECT
  - IP-CIDR,192.168.0.0/16,DIRECT
  - MATCH,🚀 节点选择
```

## 支持的代理类型

- `ss`: Shadowsocks
- `ssr`: ShadowsocksR
- `vmess`: VMess (V2Ray)
- `trojan`: Trojan
- `http`: HTTP 代理
- `socks5`: SOCKS5 代理

## 配置字段说明

### 基础配置

| 字段 | 说明 | 默认值 |
|------|------|--------|
| port | HTTP 代理端口 | 7890 |
| socks-port | SOCKS5 代理端口 | 7891 |
| mixed-port | 混合代理端口 (HTTP+SOCKS) | - |
| allow-lan | 允许局域网连接 | false |
| mode | 代理模式 (rule/global/direct) | rule |
| log-level | 日志级别 (debug/info/warning/error) | info |

### DNS 配置

```yaml
dns:
  enable: true
  listen: 0.0.0.0:53
  nameserver:
    - 119.29.29.29      # 腾讯 DNS
    - 223.5.5.5         # 阿里 DNS
    - 8.8.8.8           # Google DNS
```

### 代理节点配置

Shadowsocks 示例:
```yaml
proxies:
  - name: "香港节点"
    type: ss
    server: hk.example.com
    port: 443
    cipher: chacha20-ietf-poly1305
    password: your_password
    plugin: obfs
    plugin-opts:
      mode: http
      host: bing.com
```

VMess 示例:
```yaml
proxies:
  - name: "美国节点"
    type: vmess
    server: us.example.com
    port: 443
    uuid: your_uuid
    alterId: 0
    cipher: auto
    tls: true
    network: ws
    ws-opts:
      path: /path
```

### 规则配置

常见规则类型:
```yaml
rules:
  # 域名规则
  - DOMAIN,google.com,PROXY
  - DOMAIN-SUFFIX,google.com,PROXY
  - DOMAIN-KEYWORD,google,PROXY
  
  # IP 规则
  - IP-CIDR,127.0.0.0/8,DIRECT
  - IP-CIDR,192.168.0.0/16,DIRECT
  - GEOIP,CN,DIRECT
  
  # 兜底规则
  - MATCH,PROXY
```

## 配置验证

使用以下命令验证配置:
```bash
clash -t -f /root/.config/clash/config.yaml
```

## 获取配置的方式

1. **机场订阅**: 从服务商获取订阅链接
2. **自建节点**: 手动编写配置文件
3. **转换工具**: 使用订阅转换服务
