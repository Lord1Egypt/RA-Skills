# Domain Research Protocols Reference

## RDAP — Registration Data Access Protocol

### RFC 文档

| RFC | 标题 | 说明 |
|-----|------|------|
| RFC 7480 | HTTP Usage in RDAP | RDAP 的 HTTP 传输层 |
| RFC 7481 | Security Services for RDAP | 安全机制 |
| RFC 7482 | RDAP Query Format | 查询格式定义 |
| RFC 7483 | JSON Responses for RDAP | JSON 响应结构 |
| RFC 7484 | Finding the RDAP Server | 服务发现(Bootstrap) |

### RDAP vs WHOIS 对比

| 特性 | RDAP | WHOIS |
|------|------|-------|
| 数据格式 | 结构化 JSON | 非结构化文本 |
| 国际化 | 原生支持 | 有限支持 |
| 访问控制 | 支持差异化访问 | 不支持 |
| 标准化 | IETF RFC | 无正式标准 |
| 查询类型 | domain/nameserver/entity/ip | domain/ip |
| 重定向 | 标准化 Bootstrap | 无标准 |
| 错误处理 | HTTP 状态码 | 文本描述 |

### RDAP Bootstrap 流程

1. 解析域名的 TLD
2. 查询 IANA RDAP Bootstrap (https://data.iana.org/rdap/)
3. 获取该 TLD 的 RDAP 服务 URL
4. 向该 URL 发起 domain 查询
5. 解析 JSON 响应

### RDAP 实体角色 (entity roles)

- `registrant` — 域名注册人
- `administrative` — 管理联系人
- `technical` — 技术联系人
- `billing` — 账单联系人
- `registrar` — 注册商
- `reseller` — 分销商
- `sponsor` — 赞助注册商

### RDAP 域名状态 (status)

- `active` — 正常活动
- `inactive` — 非活动
- `pending create/delete/transfer/update` — 待处理操作
- `server hold` — 服务器冻结
- `client hold` — 客户端冻结
- `server delete prohibited` — 禁止删除
- `client delete prohibited` — 客户端禁止删除
- `server transfer prohibited` — 禁止转移
- `client transfer prohibited` — 客户端禁止转移
- `server update prohibited` — 禁止更新
- `client update prohibited` — 客户端禁止更新
- `redemption period` — 赎回期
- `pending restore` — 待恢复

## WHOIS — Legacy Protocol

### WHOIS 的局限性

- 数据格式不统一，各注册局各有格式
- 不支持国际化字符
- 缺乏标准化的错误处理
- 无法区分"域名不存在"和"域名未注册"
- GDPR 后大量字段被遮蔽（Redacted for Privacy）
- 无结构化数据，需要正则解析

### 常见 WHOIS 字段

- `Domain Name` — 域名
- `Registry Domain ID` — 注册局域名 ID
- `Registrar WHOIS Server` — 注册商 WHOIS 服务器
- `Registrar URL` — 注册商网址
- `Updated Date` — 最后更新日期
- `Creation Date` — 创建日期
- `Registry Expiry Date` — 到期日期
- `Registrar` — 注册商
- `Registrar IANA ID` — 注册商 IANA 编号
- `Domain Status` — 域名状态
- `Name Server` — 域名服务器
- `DNSSEC` — DNSSEC 状态

### WHOIS 查询端口

- 标准端口: TCP 43
- 各注册局 WHOIS 服务器不同
- 常见: whois.verisign-grs.com (com/net), whois.pir.org (org)

## DNS — Domain Name System

### 记录类型详解

| 类型 | RFC | 用途 |
|------|-----|------|
| A | RFC 1035 | IPv4 地址映射 |
| AAAA | RFC 3596 | IPv6 地址映射 |
| CNAME | RFC 1035 | 规范名称(别名) |
| MX | RFC 1035 | 邮件交换服务器 |
| NS | RFC 1035 | 权威名称服务器 |
| PTR | RFC 1035 | 反向指针(IP→域名) |
| SOA | RFC 1035 | 授权区域起始 |
| TXT | RFC 1035 | 文本记录(SPF/DKIM/DMARC) |
| SRV | RFC 2782 | 服务定位 |
| CAA | RFC 6844 | 证书颁发机构授权 |
| DS | RFC 4034 | 委派签名者(DNSSEC) |
| DNSKEY | RFC 4034 | DNS 公钥(DNSSEC) |
| RRSIG | RFC 4034 | 资源记录签名(DNSSEC) |
| NSEC | RFC 4034 | 下一安全记录(DNSSEC) |
| TLSA | RFC 6698 | TLS 关联(DANE) |

### 常见 TXT 记录用途

- **SPF** (Sender Policy Framework): `v=spf1 ...`
- **DKIM** (DomainKeys Identified Mail): `v=DKIM1; k=rsa; p=...`
- **DMARC** (Domain-based Message Authentication): `v=DMARC1; p=...`
- **Google Site Verification**: `google-site-verification=...`
- **Microsoft 365**: `MS=ms...`

### DNS 传播时间

- TTL (Time To Live) 决定缓存时间
- 常见 TTL: 300s (5分钟) ~ 86400s (24小时)
- 更改 DNS 后最多等待 TTL * 2 时间全球生效

### 公共 DNS 解析器

| 名称 | IPv4 | IPv6 | 特点 |
|------|------|------|------|
| Cloudflare | 1.1.1.1 | 2606:4700:4700::1111 | 隐私优先 |
| Google | 8.8.8.8 | 2001:4860:4860::8888 | 全球覆盖 |
| Quad9 | 9.9.9.9 | 2620:fe::fe | 安全过滤 |
| 阿里 DNS | 223.5.5.5 | 2400:3200::1 | 国内优化 |
| DNSPod | 119.29.29.29 | — | 腾讯 |
| 百度 DNS | 180.76.76.76 | — | 国内 |

## SSL/TLS 证书

### 证书字段

- **Subject CN** — 证书主体通用名称
- **Issuer** — 证书颁发机构
- **Serial Number** — 序列号
- **Valid From / To** — 有效期
- **SAN** (Subject Alternative Names) — 额外域名
- **Fingerprint** — SHA-256 指纹
- **Public Key** — 公钥算法及强度

### 证书生命周期

- DV (域名验证): 90天 (Let's Encrypt) ~ 398天
- OV (组织验证): 1-2年
- EV (扩展验证): 1-2年

### 到期前提醒阈值

- **< 7天**: 🔴 紧急，必须立即更新
- **< 30天**: 🟡 警告，尽快安排更新
- **< 90天**: 计划更新
- **> 90天**: ✅ 正常

## 域名可用性判断策略

综合多源信号判断：

| 信号 | 指示已注册 | 指示可能可用 |
|------|-----------|-------------|
| DNS 有 A 解析 | ✅ | — |
| DNS 返回 NXDOMAIN | — | ✅ |
| RDAP 返回 404 | — | ✅ |
| RDAP 有数据 | ✅ | — |
| WHOIS 有记录 | ✅ | — |
| WHOIS 查询异常 | — | ✅ |

注意：多源信号可能矛盾，综合判断 > 单一信号。

## 子域名枚举

### 内置词表 (70+ 常见子域名)

www, mail, ftp, smtp, pop, ns1, ns2, webmail, webdisk,
cpanel, whm, autodiscover, autoconfig, m, mobile,
blog, shop, api, dev, staging, test, admin, portal,
cdn, media, static, images, img, assets, docs, support,
status, monitor, git, wiki, jira, confluence, jenkins,
vpn, remote, secure, login, sso, auth, account, accounts,
app, apps, dashboard, beta, demo, store, pay, billing,
calendar, contact, help, info, news, jobs, careers

### 局限性

- 字典枚举仅覆盖常见名称
- DNS 暴力枚举不被包含（可能触发安全告警）
- 需要目标域名有通配符解析时结果不准确
