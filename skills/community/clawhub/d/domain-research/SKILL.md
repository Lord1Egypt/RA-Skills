---
name: domain-research
description: "全功能域名研究工具。支持 RDAP (RFC 7480-7484) 结构化查询、WHOIS 传统查询、DNS 多类型记录解析 (A/AAAA/MX/NS/TXT/CNAME/SOA/CAA/SRV/PTR)、SSL/TLS 证书检查、域名可用性判断、多解析器 DNS 传播检测、子域名枚举、批量域名分析和交互式 HTML 可视化报告。触发词：查域名、域名查询、域名信息、WHOIS、RDAP、DNS查询、域名可用性、域名研究、SSL证书、子域名、domain lookup、domain research、check domain、dig DNS、whois lookup、domain availability、域名分析。"
---

# Domain Research Tool — 全功能域名研究

覆盖 RDAP / WHOIS / DNS / SSL / 子域名枚举的域名信息全面研究工具。

## 触发场景

- 查询域名的注册信息（注册商、注册日期、过期日期）
- 检查域名是否可用/可注册
- 查询域名的 DNS 记录（A, AAAA, MX, NS, TXT, CNAME, SOA, CAA, SRV）
- 检查域名的 SSL/TLS 证书状态和到期时间
- 检测 DNS 在全球解析器上的传播情况
- 枚举常见子域名
- 批量分析多个域名
- IP 反向 DNS 查询
- 生成格式化的域名研究报告

## 前置依赖

运行脚本前安装依赖：

```bash
pip install dnspython python-whois requests cryptography
```

推荐使用清华镜像加速：
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ dnspython python-whois requests cryptography
```

## 工作流程

### Phase 1: 理解用户需求

确定用户要查询什么：
- 单个域名 → 使用 `--type all` (默认)
- 仅查注册信息 → `--type rdap` 或 `--type whois`
- 仅查 DNS → `--type dns`，可指定 `--dns-types`
- 查 SSL 证书 → `--type ssl`
- 判断域名可用性 → `--type availability`
- 批量分析 → `--batch domains.txt`

### Phase 2: 执行查询

使用 `scripts/domain_lookup.py` 执行查询。

**单域名完整研究：**
```bash
python scripts/domain_lookup.py example.com --type all --output result.json
```

**批量域名分析：**
```bash
python scripts/domain_lookup.py --batch domains.txt --output batch_results.json
```

**仅 DNS 查询（指定记录类型）：**
```bash
python scripts/domain_lookup.py example.com --type dns --dns-types A,MX,TXT,NS
```

**SSL 证书检查：**
```bash
python scripts/domain_lookup.py example.com --type ssl
```

**域名可用性检查：**
```bash
python scripts/domain_lookup.py example.com --type availability
```

**子域名枚举：**
```bash
python scripts/domain_lookup.py example.com --type subdomains
```

**多解析器 DNS 传播检测：**
```bash
python scripts/domain_lookup.py example.com --type multi-dns
```

**反向 DNS（IP → 域名）：**
```bash
python scripts/domain_lookup.py 8.8.8.8 --type reverse
```

### Phase 3: 生成可视化报告

将查询结果转换为交互式 HTML 报告：

```bash
python scripts/generate_report.py result.json --output report.html
```

或从 stdin 流水线处理：

```bash
python scripts/domain_lookup.py example.com | python scripts/generate_report.py --stdin --output report.html
```

## 支持的查询类型

| 查询类型 | `--type` 值 | 说明 |
|---------|-------------|------|
| RDAP | `rdap` | RFC 7480-7484 结构化域名注册数据，现代化 WHOIS 替代方案 |
| WHOIS | `whois` | 传统域名 WHOIS 查询 |
| DNS | `dns` | DNS 记录查询，默认 A/AAAA/MX/NS/TXT/CNAME/SOA |
| SSL | `ssl` | TLS/SSL 证书详情、到期时间、SAN 列表 |
| 可用性 | `availability` | 综合 RDAP+WHOIS+DNS 多源判断域名是否可注册 |
| 反查 | `reverse` | 给定 IP 地址，查询 PTR 记录 |
| 子域名 | `subdomains` | 枚举 70+ 常见子域名并检查是否解析 |
| 多解析器 | `multi-dns` | 通过 Cloudflare/Google/Quad9/AliDNS 对比 DNS 结果 |
| 全部 | `all` | 运行所有上述检查 |

### DNS 记录类型

通过 `--dns-types` 参数指定，逗号分隔：

| 类型 | 说明 |
|------|------|
| A | IPv4 地址 |
| AAAA | IPv6 地址 |
| MX | 邮件服务器 |
| NS | 域名服务器 |
| TXT | 文本记录（SPF/DKIM 等） |
| CNAME | 别名记录 |
| SOA | 授权起始记录 |
| CAA | 证书颁发机构授权 |
| SRV | 服务定位记录 |
| PTR | 反向指针记录 |

## RDAP 支持

RDAP（Registration Data Access Protocol）是 IETF 定义的 WHOIS 现代化替代协议。
本工具预配置了以下 TLD 的 RDAP 服务器：

- 通用 TLD: com, net, org, info, biz, io, co, ai, app, dev, xyz, online, shop, top, site, icu, me, tv, cc, us, pw
- 国家/地区 TLD: cn, de, uk, fr, jp, ru, br, in, ca, au, eu

对于未预配置的 TLD，工具会自动通过 IANA RDAP Bootstrap 寻找对应的 RDAP 服务器。

## 报告说明

生成的 HTML 报告包含：

1. **域名注册状态** — 多源综合判断（RDAP + WHOIS + DNS）
2. **SSL 证书概览** — 到期倒计时、颁发者、状态
3. **DNS 解析摘要** — A/AAAA/NS 记录
4. **邮件配置** — MX 记录
5. **详细标签页** — DNS 记录表 / RDAP 结构化数据 / WHOIS 原始数据 / SSL 详情 / 子域名 / 多解析器对比

## 批量分析

批量文件格式（每行一个域名，`#` 开头为注释）：

```
example.com
google.com
# 这是注释
github.com
myshopify.com
```

## 注意事项

- RDAP 查询不保证对所有 TLD 都可用——部分注册局尚未部署 RDAP 服务
- WHOIS 查询结果格式因注册局而异，字段名不统一
- DNS 查询依赖本地 DNS 解析器，结果可能受缓存影响
- SSL 检查需要目标域名开放 443 端口
- 子域名枚举基于 70+ 常见子域名词表，不保证完整性
- 某些注册局的 RDAP/WHOIS 有速率限制，批量查询可能被限流
