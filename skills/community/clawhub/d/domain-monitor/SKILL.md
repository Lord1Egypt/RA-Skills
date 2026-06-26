---
name: domain-monitor
version: 1.0.0
description: 域名监控工具。监控域名到期时间、WHOIS信息变化、SSL证书状态。适合站长和域名投资者。
author: 你的名字
triggers:
  - "域名监控"
  - "WHOIS"
  - "域名到期"
  - "SSL证书"
---

# Domain Monitor 🌐

监控域名状态，到期和 WHOIS 变化时提醒。

## 功能

- ⏰ 域名到期提醒
- 📋 WHOIS 信息监控
- 🔒 SSL 证书监控
- 📊 状态变化通知

## 使用方法

### 添加域名

```bash
python3 scripts/domain.py add example.com
```

### 查看状态

```bash
python3 scripts/domain.py status example.com
```

### 列出监控

```bash
python3 scripts/domain.py list
```

### 检查所有

```bash
python3 scripts/domain.py check
```

## 示例

```bash
# 添加域名监控
python3 scripts/domain.py add example.com
python3 scripts/domain.py add mysite.io

# 查看状态
python3 scripts/domain.py status example.com

# 检查所有
python3 scripts/domain.py check
```
