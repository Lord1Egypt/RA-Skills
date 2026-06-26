---
name: binance-proxy-cn
description: 在中国大陆服务器通过代理访问币安API的完整配置指南。涵盖代理选型、mihomo安装配置、vmess连接、币安域名路由、API签名调用。当用户在中国大陆需要调用币安API、配置币安代理、解决币安API连接问题（Connection reset、HTTP 451区域限制、DNS污染）时使用此技能。
metadata:
  version: 1.0.0
  author: openclaw-community
  license: MIT
  tags: [binance, proxy, china, mihomo, clash, crypto]
---

# 币安代理配置技能（中国大陆）

在大陆服务器上通过代理访问币安API的完整方案。

## 核心问题

| 问题 | 现象 | 原因 |
|------|------|------|
| 直连失败 | Connection reset by peer | 防火墙阻断 |
| 美国代理 | HTTP 451 区域限制 | 币安禁止美国IP |
| DNS污染 | 解析到错误IP | DNS被篡改 |

## 网络架构

```
大陆服务器 → mihomo(本地代理) → 海外VPS(vmess) → 币安API
                                         ├─ 币安域名 → VPS所在国直连 ✅
                                         └─ 其他流量 → 按需路由
```

## 关键原则

1. **出口IP不能是美国** — 币安封禁美国IP，返回 HTTP 451
2. **推荐出口地区** — 日本、香港、新加坡、欧洲
3. **币安流量必须走代理** — 直连会被防火墙阻断
4. **代理规则优先级** — 币安规则必须放在 GEOIP,CN 之前

## 安装步骤

### 1. 安装 mihomo (Clash Meta)

```bash
# 下载（选一个镜像）
curl -sL "https://ghfast.top/https://github.com/MetaCubeX/mihomo/releases/download/v1.19.0/mihomo-linux-amd64-v1.19.0.gz" -o /tmp/mihomo.gz
cd /tmp && gunzip -f mihomo.gz && chmod +x mihomo && mv mihomo /usr/local/bin/mihomo
mihomo -v  # 验证安装
```

### 2. 编写配置文件

```bash
mkdir -p /etc/mihomo
cat > /etc/mihomo/config.yaml << 'YAML'
mixed-port: 7890
allow-lan: false
mode: rule
log-level: info
external-controller: 127.0.0.1:9090

dns:
  enable: true
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - 119.29.29.29
    - 223.5.5.5
    - 8.8.8.8

proxies:
  - name: "proxy-node"
    type: vmess
    server: <YOUR_VPS_IP>
    port: <YOUR_VPS_PORT>
    uuid: <YOUR_UUID>
    alterId: 0
    cipher: auto
    network: tcp
    tls: false

proxy-groups:
  - name: "proxy-select"
    type: select
    proxies:
      - "proxy-node"
      - DIRECT

rules:
  # 币安走代理（必须在GEOIP之前）
  - DOMAIN-SUFFIX,binance.com,proxy-select
  - DOMAIN-SUFFIX,binance.org,proxy-select
  - DOMAIN-SUFFIX,binance.us,proxy-select
  - DOMAIN-SUFFIX,bnbstatic.com,proxy-select
  - DOMAIN-SUFFIX,binance.cloud,proxy-select
  - DOMAIN-SUFFIX,binance2.com,proxy-select
  # 其他默认直连（节省流量）
  - MATCH,DIRECT
YAML
```

### 3. 测试配置并启动

```bash
mihomo -d /etc/mihomo -t  # 测试配置
# 测试币安API连通性
curl -s --proxy http://127.0.0.1:7890 https://api.binance.com/api/v3/time
# 预期返回: {"serverTime":1773828714609}
```

### 4. 设为系统服务

```bash
cat > /etc/systemd/system/mihomo.service << 'EOF'
[Unit]
Description=Mihomo Proxy Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/mihomo -d /etc/mihomo
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable mihomo
systemctl start mihomo
```

## VPS 端配置要点

如果VPS上跑的是 Xray/X-UI，需要确保币安流量**直连**而不是转发到其他国家：

```json
{
  "outbounds": [
    { "protocol": "freedom", "tag": "direct" },
    { "protocol": "vmess", "tag": "to-other-vps", "settings": { "vnext": [...] } }
  ],
  "routing": {
    "rules": [
      {
        "domain": ["binance.com", "api.binance.com", "binance.org"],
        "outboundTag": "direct",
        "type": "field"
      },
      {
        "inboundTag": ["api"],
        "outboundTag": "to-other-vps",
        "type": "field"
      }
    ]
  }
}
```

**关键**：币安域名的路由规则必须在默认转发规则**之前**。

## 币安 API 签名调用示例

```bash
API_KEY="<YOUR_API_KEY>"
SECRET="<YOUR_SECRET>"
TIMESTAMP=$(($(date +%s)*1000))
QUERY="timestamp=${TIMESTAMP}"
SIG=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $NF}')

# 查询账户（需签名）
curl -s --proxy http://127.0.0.1:7890 \
  -H "X-MBX-APIKEY: $API_KEY" \
  "https://api.binance.com/api/v3/account?$QUERY&signature=$SIG"

# 查询价格（无需签名）
curl -s --proxy http://127.0.0.1:7890 \
  "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
```

## 环境变量方式

设置 `https_proxy` 让所有 HTTPS 请求走代理：

```bash
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
```

注意：需要配合 mihomo 的规则配置，确保只有币安域名走代理，其他流量直连，否则会影响其他网络请求。

## 常见问题排查

| 症状 | 检查方法 | 解决方案 |
|------|----------|----------|
| 连接超时 | `curl -v --proxy http://127.0.0.1:7890 https://api.binance.com/api/v3/time` | 检查mihomo是否运行、VPS是否可达 |
| HTTP 451 | `curl -s --proxy http://127.0.0.1:7890 https://ipinfo.io` 查看出口IP | 更换非美国VPS |
| DNS污染 | `nslookup api.binance.com` 检查解析结果 | mihomo的fake-ip会自动处理 |
| 签名错误 -1102 | 检查timestamp是否为毫秒级 | 确保timestamp为13位毫秒时间戳 |
| 规则不生效 | 检查rules顺序 | 币安规则必须在GEOIP,CN之前 |

## 推荐VPS地区

- ✅ 日本（Vultr大阪、东京）
- ✅ 香港
- ✅ 新加坡
- ✅ 韩国
- ✅ 欧洲各国
- ❌ 美国（被币安封禁）
- ❌ 加拿大（受限）
- ❌ 中国大陆（被墙）
