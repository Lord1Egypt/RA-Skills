---
name: china-ip
description: IP地址归属地与网络信息查询。Use when the user wants to look up the geographic location, ISP, or network details of an IP address. Supports both Chinese and international IPs. No API key required — uses free public endpoints (ip-api.com, ipinfo.io). Works with any IP address including IPv4, IPv6, and domain names.
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins:
        - curl
---

# IP 地址查询 IP Lookup

查询任意 IP 地址的归属地、运营商、网络信息。无需 API key，仅需 curl。

## 触发时机

- "这个IP是哪里的" / "查一下 8.8.8.8"
- "我的服务器IP归属地是哪里"
- "这个访问来自哪个运营商"
- "帮我查一下这个IP是不是中国的"
- "这个域名解析到哪里"
- 排查异常访问来源、验证代理节点位置

---

## 查询接口（无需 API key，按优先级使用）

### 接口 A：ip-api.com（主力，中文友好）

```bash
# 查询指定IP（支持IPv4/IPv6）
curl -s "http://ip-api.com/json/{IP}?lang=zh-CN&fields=status,message,country,regionName,city,isp,org,as,query,mobile,proxy,hosting"

# 查询本机公网IP
curl -s "http://ip-api.com/json/?lang=zh-CN"

# 批量查询（最多100个，POST方式）
curl -s -X POST "http://ip-api.com/batch?lang=zh-CN" \
  -H "Content-Type: application/json" \
  -d '[{"query":"8.8.8.8"},{"query":"114.114.114.114"}]'
```

响应示例：
```json
{
  "status": "success",
  "country": "中国",
  "regionName": "广东省",
  "city": "深圳市",
  "isp": "中国联通",
  "org": "China Unicom Guangdong",
  "as": "AS17816 China Unicom IP network China169 Guangdong Province",
  "query": "113.108.x.x",
  "mobile": false,
  "proxy": false,
  "hosting": false
}
```

字段说明：
- `country` / `regionName` / `city`：国家、省份、城市
- `isp`：互联网服务提供商（运营商）
- `org`：组织名称
- `as`：ASN 自治系统号
- `mobile`：是否移动网络
- `proxy`：是否代理/VPN
- `hosting`：是否托管/数据中心IP

限制：免费版每分钟45次请求，HTTP（非HTTPS）

### 接口 B：ipinfo.io（备用，支持HTTPS）

```bash
curl -s "https://ipinfo.io/{IP}/json"

# 查询本机IP
curl -s "https://ipinfo.io/json"
```

响应示例：
```json
{
  "ip": "8.8.8.8",
  "city": "Mountain View",
  "region": "California",
  "country": "US",
  "loc": "37.3861,-122.0839",
  "org": "AS15169 Google LLC",
  "timezone": "America/Los_Angeles"
}
```

限制：免费版每天50,000次请求，支持HTTPS

### 接口 C：纯离线判断（无网络时降级）

无法访问外部接口时，根据IP段提供基础判断：

```
中国常见IP段（仅供参考，不完整）：
- 1.0.0.0/8      中国电信
- 14.0.0.0/8     中国移动
- 36.0.0.0/8     中国移动
- 58.0.0.0/8     中国电信/联通
- 101.0.0.0/8    中国移动/联通
- 112.0.0.0/8    中国移动
- 114.0.0.0/8    中国电信
- 117.0.0.0/8    中国移动
- 120.0.0.0/8    中国电信
- 121.0.0.0/8    中国联通
- 182.0.0.0/8    中国移动
- 183.0.0.0/8    中国移动
- 202.0.0.0/8    亚太地区
- 221.0.0.0/8    中国电信

特殊保留地址：
- 10.x.x.x       私有网络
- 172.16-31.x.x  私有网络
- 192.168.x.x    私有网络
- 127.0.0.1      本机回环
```

---

## 格式化输出

### 单IP查询

```
🌐 IP 查询结果
━━━━━━━━━━━━━━━━━━━━
IP 地址：113.108.x.x
归属地：🇨🇳 中国 广东省 深圳市
运营商：中国联通
组织：China Unicom Guangdong
ASN：AS17816
网络类型：宽带（非移动、非代理、非数据中心）
```

### 代理/VPN 检测结果

```
🌐 IP 查询结果
━━━━━━━━━━━━━━━━━━━━
IP 地址：x.x.x.x
归属地：🇺🇸 美国 加利福尼亚州 洛杉矶
运营商：Cloudflare Inc
⚠️  检测到：疑似代理/VPN 或 托管服务器IP
```

### 批量查询汇总

```
🌐 批量 IP 查询（3个）
━━━━━━━━━━━━━━━━━━━━
1. 8.8.8.8        🇺🇸 美国 · Google LLC
2. 114.114.114.114 🇨🇳 中国 江苏 · 中国移动
3. 1.1.1.1        🇦🇺 澳大利亚 · Cloudflare
━━━━━━━━━━━━━━━━━━━━
中国IP：1个 / 海外IP：2个
```

### 本机公网IP查询

```
🌐 本机公网 IP
━━━━━━━━━━━━━━━━━━━━
IP 地址：x.x.x.x
归属地：🇨🇳 中国 北京市
运营商：中国电信
提示：此为 OpenClaw 所在机器的出口IP
```

---

## 执行流程

```
用户输入IP地址/域名/本机
  ↓
[验证] 判断输入类型（IPv4/IPv6/域名/本机）
  ↓
[查询] curl ip-api.com（主力接口）
  ↓ 失败（限速/网络问题）
[查询] curl ipinfo.io（备用接口）
  ↓ 全部失败
[降级] 离线IP段基础判断 + 提示用户
  ↓
[输出] 格式化结果 + 异常标注
```

---

## 注意事项

- ip-api.com 免费版使用 HTTP（非 HTTPS），不要在请求中携带敏感信息
- 查询结果为地理数据库匹配，精确到城市级别，不代表用户实际物理位置
- `proxy: true` 仅为启发式判断，不能100%确定是否使用了代理
- 私有IP（10.x/192.168.x/172.16-31.x）无法查询，直接告知用户
- IPv6查询两个接口均支持
