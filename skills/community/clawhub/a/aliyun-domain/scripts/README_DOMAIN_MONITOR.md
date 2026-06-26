# 域名监控工具使用说明

## 功能简介

域名监控工具（`domain_monitor.py`）是一个专门用于监控域名状态的工具，适合站长和域名投资者使用。

### 主要功能

- ⏰ **域名到期监控**：实时监控域名到期时间，提前告警
- 📋 **WHOIS 信息追踪**：记录注册商、DNS 等关键信息变化
- 🔒 **SSL 证书监控**：检查证书有效性和到期时间
- 📊 **状态变化告警**：重要变更及时提醒
- 📜 **监控历史查询**：查看域名监控记录和告警历史

## 快速开始

### 1. 添加域名监控

```bash
# 添加单个域名
python3 scripts/domain_monitor.py add example.com

# 添加多个域名
python3 scripts/domain_monitor.py add example.com
python3 scripts/domain_monitor.py add mysite.cn
python3 scripts/domain_monitor.py add test.net
```

**输出示例：**
```
🔍 正在获取 example.com 的初始信息...
✅ 已添加域名：example.com
   ✅ 到期时间：2027-01-15 (剩余 300 天)
```

### 2. 查看域名状态

```bash
# 查看单个域名详细信息
python3 scripts/domain_monitor.py status example.com
```

**输出示例：**
```
🔍 查询：example.com
============================================================

📋 WHOIS 信息:
   到期时间：2027-01-15
   注册商：Alibaba Cloud Computing Ltd.
   注册日期：2020-01-15
   DNS 服务器：dns1.hichina.com, dns2.hichina.com
   ✅ 正常：剩余 300 天

🔒 SSL 证书状态:
   ✅ 证书有效
   主题：subject=CN=example.com
   颁发者：issuer=CN=Let's Encrypt
   证书到期：Apr 15 12:00:00 2026 GMT

📊 监控状态:
   添加时间：2026-03-17
   最后检查：2026-03-17
```

### 3. 列出所有监控域名

```bash
# 列出所有监控的域名
python3 scripts/domain_monitor.py list
```

**输出示例：**
```
📋 监控列表:
============================================================
域名                             添加日期         最后检查         状态
------------------------------------------------------------
example.com                     2026-03-17   2026-03-17   ✅ 正常
mysite.cn                       2026-03-17   2026-03-17   ⚠️  25 天
test.net                        2026-03-17   2026-03-17   ✅ 正常
------------------------------------------------------------
共 3 个域名
```

### 4. 检查所有域名

```bash
# 检查所有监控域名的状态
python3 scripts/domain_monitor.py check
```

**输出示例：**
```
🔄 检查所有域名...
============================================================

📌 example.com:
   到期：2027-01-15
   ✅ 剩余 300 天
   SSL: ✅ 有效

📌 mysite.cn:
   到期：2026-04-10
   ⚠️  剩余 25 天
   SSL: ✅ 有效

============================================================
🚨 告警汇总:
   • mysite.cn 即将到期 (剩余 25 天)

✅ 检查完成
```

### 5. 查看监控历史

```bash
# 查看域名的监控历史记录
python3 scripts/domain_monitor.py history example.com
```

**输出示例：**
```
📊 example.com 监控历史:
============================================================
添加时间：2026-03-17T10:30:00
最后检查：2026-03-17T15:45:00

初始 WHOIS:
   到期时间：2027-01-15
   注册商：Alibaba Cloud Computing Ltd.
   注册日期：2020-01-15
   DNS: dns1.hichina.com, dns2.hichina.com

最新 WHOIS:
   到期时间：2027-01-15
   注册商：Alibaba Cloud Computing Ltd.
   注册日期：2020-01-15
   DNS: dns1.hichina.com, dns2.hichina.com
```

### 6. 移除域名监控

```bash
# 移除不再需要监控的域名
python3 scripts/domain_monitor.py remove example.com
```

**输出示例：**
```
确认要移除域名 example.com 的监控吗？(y/N): y
✅ 已移除域名：example.com
```

## 命令速查表

| 命令 | 说明 | 示例 |
|:---|:---|:---|
| `add` | 添加域名到监控 | `python3 scripts/domain_monitor.py add example.com` |
| `status` | 查看域名详细状态 | `python3 scripts/domain_monitor.py status example.com` |
| `list` | 列出所有监控域名 | `python3 scripts/domain_monitor.py list` |
| `check` | 检查所有域名状态 | `python3 scripts/domain_monitor.py check` |
| `remove` | 移除域名监控 | `python3 scripts/domain_monitor.py remove example.com` |
| `history` | 查看监控历史 | `python3 scripts/domain_monitor.py history example.com` |
| `--help` | 查看帮助信息 | `python3 scripts/domain_monitor.py --help` |

## 告警级别说明

### 域名到期告警

| 剩余天数 | 告警级别 | 说明 |
|:---|:---|:---|
| < 0 天 | ❌ 已过期 | 域名已过期，需要立即赎回 |
| < 30 天 | ⚠️ 紧急 | 域名即将到期，需要尽快续费 |
| < 90 天 | ⚠️ 注意 | 域名剩余时间不多，建议安排续费 |
| ≥ 90 天 | ✅ 正常 | 域名状态正常 |

### SSL 证书告警

| 状态 | 说明 |
|:---|:---|
| ✅ valid | 证书有效 |
| ⚠️ invalid_or_not_found | 未找到有效证书或证书无效 |
| ❌ error | 检查失败（可能是网络问题或域名未启用 HTTPS） |

## 数据存储

监控数据存储在用户主目录下：

```
~/.domain_monitor.json
```

数据结构：
```json
{
  "domains": {
    "example.com": {
      "added_at": "2026-03-17T10:30:00",
      "last_check": "2026-03-17T15:45:00",
      "initial_whois": {...},
      "last_whois": {...},
      "alerts": []
    }
  }
}
```

## 系统要求

### 必需工具

1. **Python 3.6+**
2. **whois 命令**（用于查询 WHOIS 信息）
   - macOS: `brew install whois`
   - Ubuntu/Debian: `sudo apt-get install whois`
   - CentOS/RHEL: `sudo yum install whois`
3. **openssl 命令**（用于检查 SSL 证书，通常系统已预装）

### 检查是否已安装

```bash
# 检查 Python
python3 --version

# 检查 whois
whois --version

# 检查 openssl
openssl version
```

## 最佳实践

### 1. 定期执行检查

建议每天或每周执行一次检查：

```bash
# 添加到 crontab（每天上午 9 点执行）
0 9 * * * cd /path/to/skill-aliyun-domain && python3 scripts/domain_monitor.py check
```

### 2. 批量添加域名

可以创建域名列表文件，然后批量添加：

```bash
# domains.txt 文件内容
example.com
mysite.cn
test.net

# 批量添加（使用循环）
while read domain; do
  python3 scripts/domain_monitor.py add "$domain"
done < domains.txt
```

### 3. 监控关键域名

对于重要域名，建议：
- 设置多个提醒时间点（90 天、60 天、30 天、7 天）
- 定期检查 WHOIS 信息变化
- 关注 SSL 证书到期时间

### 4. 结合告警系统

可以将检查脚本与告警系统集成：

```bash
#!/bin/bash
# check_and_alert.sh

cd /path/to/skill-aliyun-domain
output=$(python3 scripts/domain_monitor.py check)

# 检查是否有告警
if echo "$output" | grep -q "🚨 告警汇总"; then
  # 发送邮件告警
  echo "$output" | mail -s "域名监控告警" admin@example.com
  
  # 或发送钉钉/企业微信消息
  # curl -X POST "webhook_url" -d "$output"
fi
```

## 常见问题

### Q: WHOIS 查询超时怎么办？

A: WHOIS 查询超时可能是网络问题或 WHOIS 服务器响应慢。稍后重试即可，不影响其他功能。

### Q: SSL 证书检查失败？

A: 可能原因：
1. 域名未启用 HTTPS（443 端口）
2. 防火墙阻止了 443 端口
3. 域名 DNS 未正确解析

### Q: 如何修改监控数据？

A: 可以直接编辑 `~/.domain_monitor.json` 文件，但建议先备份。

### Q: 可以监控多少个域名？

A: 理论上没有数量限制，但建议将重要域名优先监控。

## 与其他工具集成

### 与阿里云域名 API 结合

本工具可以与阿里云域名 API 配合使用：

1. 使用 `domain_monitor.py` 监控域名到期时间
2. 使用 `aliyun_domain.py` 执行续费操作
3. 使用 `domain_hotspot_analyzer.py` 分析投资机会

```bash
# 1. 检查即将过期域名
python3 scripts/domain_monitor.py check

# 2. 使用阿里云 API 续费
python3 scripts/aliyun_domain.py renew --domain example.com --years 1
```

## 版本历史

- **v1.0.0** (2026-03-17): 初始版本，支持域名到期监控、WHOIS 信息追踪、SSL 证书监控

## 技术支持

如有问题或建议，请参考：
- [SKILL.md](../SKILL.md) - 完整技能文档
- [阿里云域名帮助文档](https://help.aliyun.com/product/35836.html)
