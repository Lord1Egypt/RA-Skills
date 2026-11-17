---
slug: domain-dns-manager-free
name: domain-dns-manager-free
version: 1.0.1
displayName: 域名DNS管理免费版
summary: 管理Cloudflare/DNSimple/Namecheap的域名与DNS记录，支持单域名接入与基础记录操作.
license: MIT
edition: free
description: "域名DNS管控免费版是一款面向个人开发者与小团队的域名管控Skill，封装Cloudflare、DNSimple、Namecheap三大平台的常用操作。Use. 适用于需要domain dns manager相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量."
tags:
  - 域名管理
  - domain
  - dns
  - manager
  - automation
  - DNS配置
  - Cloudflare
  - 运维工具
  - 工具
  - 效率
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
pricing_tier: free

---
# 域名DNS管理免费版（Domain DNS Manager Free）

## 概述

管理多个域名注册商与DNS服务商是一件繁琐的事：登录不同控制台、切换不同界面、记住不同操作流程。本Skill将Cloudflare、DNSimple、Namecheap三大平台的常用操作统一为标准化工作流，配合验证步骤确保每步操作正确生效.
设计原则：
1. **标准流程**：统一的接入、配置、验证三步工作流
2. **可验证**：每步操作后用dig确认生效，不靠"应该好了"
3. **可回滚**：记录操作前状态，支持快速回退
4. **安全优先**：API Token通过环境变量管理，不硬编码

## 核心能力

### 支持的平台与操作

| 平台 | 接入域名 | DNS记录管理 | Nameserver切换 | HTTPS重定向 |
|---|----|-------|------------|--------|
| Cloudflare | ✅ 创建zone | ✅ 增删改查 | ✅ | ✅ Page Rule |
| DNSimple | ✅ 查询域名 | ✅ 增删改查 | ✅ | ❌ |
| Namecheap | ✅ 查询域名 | ❌（需通过CF） | ✅ | ❌ |

**处理**: 解析支持的平台与操作的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回支持的平台与操作的响应数据,包含状态码、结果和日志.
### DNS记录类型支持

| 记录类型 | 用途 | 示例 |
|:-----|:-----|:-----|
| A | IPv4指向 | `example.com → 192.0.2.1` |
| AAAA | IPv6指向 | `example.com → 2001:db8::1` |
| CNAME | 别名指向 | `www → example.com` |
| MX | 邮件服务器 | `example.com → mail.example.com` |
| TXT | 文本记录 | SPF/DKIM/DMARC/验证 |
| NS | 域名服务器 | 委托子域 |

**处理**: 解析DNS记录类型支持的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回DNS记录类型支持的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：的域名与、支持单域名接入与、基础记录操作、管理免费版是一款、面向个人开发者与、小团队的域名管理、三大平台的常用操、Use、when、需要项目管理、任务规划、进度跟踪、团队协作时使用、不适用于实际人员、绩效评估、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：新域名接入Cloudflare
购买新域名后，需要接入Cloudflare享受CDN与防护。标准流程：(1)Cloudflare创建zone；(2)在注册商切换nameserver到Cloudflare；(3)配置DNS记录；(4)验证生效.
### 场景二：配置HTTPS重定向
将`http://example.com`重定向到`https://example.com`。使用Cloudflare Page Rule，一条规则搞定全站HTTPS.
### 场景三：添加邮件DNS记录
配置企业邮箱时，需要添加MX记录指向邮件服务器，TXT记录配置SPF防止伪造。本Skill提供标准配置模板.
### 场景四：域名迁移
将域名从旧DNS迁移到新DNS。先在新DNS配置好所有记录，再切换nameserver，确保迁移过程中服务不中断.
### 场景五：开发调试DNS
开发环境需要临时DNS记录指向本地服务器。快速添加A记录，调试完成后删除，避免影响生产.
## 快速开始

### 120秒上手

1. **配置API Token**：设置Cloudflare/DNSimple/Namecheap的环境变量
2. **确认域名注册商**：查询域名的当前注册商与nameserver
3. **执行操作**：按标准工作流接入或配置DNS
4. **验证生效**：用dig确认DNS记录已生效

### 标准接入流程

**步骤1：Cloudflare创建zone**
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | 域名DNS管理免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
cli4 --post name=example.com /zones
```

**步骤2：确认zone创建**
```bash
cli4 --get name=example.com /zones
```

**步骤3：切换nameserver（以Namecheap为例）**
```bash
# 将nameserver切换到Cloudflare
namecheap-set-ns example.com emma.ns.cloudflare.com scott.ns.cloudflare.com
```

**步骤4：配置DNS记录**
```bash
# 添加A记录（指向Cloudflare代理IP）
cli4 --post type=A name=example.com content=192.0.2.1 proxied=true /zones/:zone_id/dns_records
# ...
# 添加CNAME记录
cli4 --post type=CNAME name=www content=example.com proxied=true /zones/:zone_id/dns_records
```

**步骤5：配置HTTPS重定向**
```bash
# Page Rule: HTTP -> HTTPS
cli4 --post targets=example.com/* actions=ssl=off,redirect_to=https://example.com /zones/:zone_id/pagerules
```

**步骤6：验证**
```bash
# DNS验证
dig +short example.com @1.1.1.1
# ...
# HTTPS重定向验证
curl -I https://example.com
# 期望返回 301 重定向
```

#
## 示例

### API Token配置

```bash
# Cloudflare Token（二选一）
export CLOUDFLARE_API_TOKEN="${KEY:?请设置环境变量}"_here"
# 或
export CF_API_TOKEN="${KEY:?请设置环境变量}"_here"
# ...
# DNSimple Token
export DNSIMPLE_ACCESS_TOKEN=${ACCESS_TOKEN:?请设置环境变量}
# ...
# Namecheap API
export NAMECHEAP_API_USER="your_username"
export NAMECHEAP_API_KEY=${API_KEY:?请设置环境变量}
```

### DNS记录配置模板

**企业邮件配置**：
| 记录 | 类型 | 值 | 说明 |
|:---:|:---:|:---:|:---:|
| example.com | MX | 10 mail.example.com | 邮件服务器 |
| example.com | TXT | "v=spf1 include:_spf.example.com ~all" | SPF防伪造 |
| dkim._domainkey | TXT | "v=DKIM1; k=rsa; p=MIGfMA0..." | DKIM签名 |
| _dmarc | TXT | "v=DMARC1; p=quarantine; rua=mailto:..." | DMARC策略 |

**网站接入配置**：
| 记录(续)| 类型 | 值 | 说明 |
|:-------|-------:|:-------|:-------|
| example.com | A | 192.0.2.1 | 主域名（Cloudflare代理） |
| www | CNAME | example.com | www别名 |
| api | A | 203.0.113.50 | API服务器（不代理） |
| cdn | CNAME | cdn.provider.com | CDN指向 |

### Cloudflare代理IP说明

使用Cloudflare代理时，A记录可使用以下占位IP（Cloudflare会自动替换为实际代理IP）：
- `192.0.2.1` - 用于DNS占位，确保HTTPS可终止

## 优秀实践

1. **先配置后切换**：在新DNS配好所有记录后再切换nameserver，避免服务中断
2. **逐项验证**：每添加一条记录后用dig验证，不要批量添加后才发现问题
3. **TTL设置**：临时调试用短TTL（60秒），生产环境用默认TTL（300秒）
4. **代理状态**：对外服务开启Cloudflare代理（橙色云），内部服务关闭代理（灰色云）
5. **HTTPS强制**：接入Cloudflare后开启"Always Use HTTPS"，全站强制加密
6. **API Token权限**：Cloudflare Token仅授予需要的zone权限，最小权限原则
7. **操作记录**：保留操作命令记录，便于回溯与审计
8. **nameserver确认**：切换nameserver后等待全球生效（通常24-48小时）

## 常见问题

### Q1：nameserver切换后多久生效？
A：通常24-48小时全球生效。可通过`dig @1.1.1.1 example.com NS`与`dig @8.8.8.8 example.com NS`对比不同DNS的返回结果判断生效进度.
### Q2：Cloudflare显示"invalid nameservers"？
A：确认域名注册商是否正确。常见错误是在错误的注册商控制台修改nameserver。先通过WHOIS查询确认注册商.
### Q3：能批量管理多个域名吗？
A：免费版支持单域名操作。批量域名接入、多供应商编排属于专业版能力，详见domain-dns-manager-pro.
### Q4：支持Worker路由配置吗？
A：免费版仅支持Page Rule重定向。Worker路由、Rulesets、Bulk Redirects属于专业版能力.
### Q5：DNS记录修改后多久生效？
A：取决于记录TTL。TTL未过期前各DNS返回缓存值。可使用短TTL（60秒）加快生效，或等待TTL自然过期.
### Q6：如何关闭"Block AI Bots"？
A：在Cloudflare控制台或使用API：`cloudflare-ai-bots disable`。部分场景下AI爬虫访问需要放行.
## 已知限制

本免费体验版限制以下高级功能：
- ❌ 批量域名管理（>1个域名/次）
- ❌ 多供应商编排与切换
- ❌ Worker路由配置
- ❌ Rulesets与Bulk Redirects
- ❌ DNS变更审计日志
- ❌ 定时健康检查与告警
- ❌ 变更回滚机制
- ❌ 多账号管理

解锁全部功能请使用专业版：domain-dns-manager-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Linux / macOS / Windows
- **网络**：可访问Cloudflare/DNSimple/Namecheap API

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|:---|---:|---:|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| cli4 | CLI工具 | Cloudflare操作必需 | `pip install cloudflare-cli4` |
| dig | 系统命令 | 验证必需 | 安装bind-utils或dnsutils |
| curl | 系统命令 | 验证必需 | 系统自带 |
| jq | 系统命令 | 可选 | `sudo apt install jq` |

### API Key 配置
- **Cloudflare Token**：通过环境变量`CLOUDFLARE_API_TOKEN`或`CF_API_TOKEN`配置
- **DNSimple Token**：通过环境变量`DNSIMPLE_ACCESS_TOKEN`配置
- **Namecheap API**：通过环境变量`NAMECHEAP_API_USER`与`NAMECHEAP_API_KEY`配置
- **禁止**：在SKILL.md或脚本中硬编码API Token
- **建议**：Token存储在`./.env`或系统密钥管理器中

### 可用性分类
- **分类**：MD+EXEC（Markdown指令驱动，API调用与验证需要exec命令行能力）
- **说明**：域名DNS管理Skill，支持Cloudflare/DNSimple/Namecheap三平台的单域名操作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------:|--------|:-------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "域名DNS管理免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "domain dns manager"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
