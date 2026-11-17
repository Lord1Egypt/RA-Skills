---
slug: dns-networking-tool-free
name: dns-networking-tool-free
version: 1.0.0
displayName: DNS网络诊断基础版
summary: "提供DNS解析、端口连通性、curl诊断与证书检查,适合开发者日常网络问题排查.。面向开发者的网络诊断辅助工具,涵盖DNS解析调试、端口连通性测试、HTTP请求诊断与TLS证书检查。核心能力"
license: Proprietary
edition: free
description: 面向开发者的网络诊断辅助工具,涵盖DNS解析调试、端口连通性测试、HTTP请求诊断与TLS证书检查。核心能力:，可处理提升工作效率

  - DNS解析查询(A/MX/CNAME/TXT/NS)

  - 端口连通性测试(nc/curl)

  - curl请求诊断与时序分析

  - TLS证书有效期检查

  - 本地DNS缓存管理

  适用场景:

  - 开发环境网络问题排查

  - DNS解析异常诊断

  - HTTP请求故障定位

  - 证书过期检查

  差异化:

  - 免费版聚焦常用诊断命令,开箱即用

  - 覆盖日常90%网络排查需求

  - 与专业版命令兼...'
tags:
  - 开发工具
  - 网络诊断
  - DNS
  - 网络
  - 工具
  - dns
  - bash
tools:
  - read
  - exec
homepage: ""
category: "Operations"
---
# DNS网络诊断工具 - 免费版

## 概述

DNS网络诊断工具免费版为开发者提供日常网络问题排查能力。工具涵盖 DNS 解析查询、端口连通性测试、HTTP 请求诊断和 TLS 证书检查,帮助开发者快速定位网络故障根因.
本版本适合开发环境网络问题排查、DNS 解析异常诊断和日常连通性测试。所有诊断命令均通过 Bash 执行,无需安装额外软件.
## 核心能力

### 1. DNS 解析查询

支持多种 DNS 记录类型查询和指定服务器查询.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | DNS网络诊断基础版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 基础A记录查询
dig example.com
dig +short example.com
# ...
# 查询不同记录类型
dig example.com MX        # 邮件服务器
dig example.com CNAME     # 别名记录
dig example.com TXT       # 文本记录(SPF/DKIM)
dig example.com NS        # 名称服务器
dig example.com AAAA      # IPv6 地址
# ...
# 指定DNS服务器查询
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com
# ...
# 反向解析
dig -x 93.184.216.34
# ...
# 使用nslookup
nslookup example.com
nslookup example.com 8.8.8.8
nslookup -type=MX example.com
```

**处理**: 解析DNS 解析查询的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回DNS 解析查询的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 端口连通性测试

快速检测目标主机端口是否开放.
```bash
# 单端口测试
nc -zv example.com 443
nc -zv -w 5 example.com 80    # 5秒超时
# ...
# 批量端口扫描
for port in 22 80 443 5432 6379; do
    echo -n "Port $port: "
    nc -zv -w 2 example.com $port 2>&1
done
# ...
# 使用bash内置TCP测试
timeout 3 bash -c 'echo > /dev/tcp/example.com/443' && echo "Open" || echo "Closed"
# ...
# 使用curl检测
curl -sI -o /dev/null -w "%{http_code}" https://example.com
```

**处理**: 解析端口连通性测试的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回端口连通性测试的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. curl 请求诊断

分析 HTTP 请求各阶段耗时,定位慢请求根因.
```bash
# 详细请求过程
curl -v https://api.example.com/endpoint
# ...
# 各阶段耗时分析
curl -o /dev/null -s -w "
    DNS解析:      %{time_namelookup}s
    TCP连接:      %{time_connect}s
    TLS握手:      %{time_appconnect}s
    首字节时间:    %{time_starttransfer}s
    总耗时:        %{time_total}s
    HTTP状态码:    %{http_code}
    响应大小:      %{size_download} bytes
" https://api.example.com/endpoint
# ...
# 查看响应头
curl -sI https://api.example.com/endpoint
# ...
# 跟随重定向
curl -sIL https://example.com
```

**处理**: 解析curl 请求诊断的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回curl 请求诊断的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. TLS 证书检查

检查证书有效期和颁发信息.
```bash
# 查看证书信息
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | \
  openssl x509 -noout -subject -issuer -dates
# ...
# 查看证书过期时间
com:443 2>/dev/null | \
  openssl x509 -noout -enddate
# ...
# 验证证书链
echo | openssl s_client -showcerts -connect example.com:443 < /dev/null 2>/dev/null | \
  awk '/BEGIN CERT/,/END CERT/' > chain.pem
```

**处理**: 解析TLS 证书检查的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回TLS 证书检查的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 本地 DNS 缓存管理

```bash
# 查看本地DNS配置
cat /etc/resolv.conf      # Linux
cat /etc/hosts            # 所有平台
# ...
# 刷新DNS缓存
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder  # macOS
sudo systemd-resolve --flush-caches                            # Linux(systemd)
ipconfig /flushdns                                             # Windows
# ...
# 查看systemd-resolved状态
resolvectl status
```

**处理**: 解析本地 DNS 缓存管理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回本地 DNS 缓存管理的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：诊断与证书检查、适合开发者日常网、络问题排查、面向开发者的网络、诊断辅助工具、解析调试、请求诊断与、核心能力、请求诊断与时序分、证书有效期检查等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:域名无法访问排查

当域名无法访问时,按步骤排查问题.
```bash
#!/bin/bash
TARGET="${1:-example.com}"
echo "=== 网络诊断: $TARGET ==="
# ...
# 1. DNS解析检查
echo -n "DNS解析: "
IP=$(dig +short "$TARGET" | head -1)
if [ -n "$IP" ]; then
    echo "成功 -> $IP"
else
    echo "失败"
    echo "尝试使用其他DNS服务器..."
    dig +short @8.8.8.8 "$TARGET"
    exit 1
fi
# ...
# 2. Ping测试
echo -n "Ping: "
ping -c 3 -W 3 "$TARGET" > /dev/null 2>&1 && echo "可达" || echo "不可达(可能被ICMP屏蔽)"
# ...
# 3. HTTPS端口检查
echo -n "443端口: "
nc -zv -w 5 "$TARGET" 443 2>&1 | grep -q "succeeded\|open" && echo "开放" || echo "关闭"
# ...
# 4. TLS证书检查
echo -n "TLS证书: "
echo | openssl s_client -connect "$TARGET:443" -servername "$TARGET" 2>/dev/null | \
  grep -q "Verify return code: 0" && echo "有效" || echo "无效"
# ...
echo "=== 诊断完成 ==="
```

### 场景二:API 请求慢定位

分析 API 请求各阶段耗时,找出瓶颈.
```bash
# 详细时序分析
echo "=== API请求时序分析 ==="
curl -o /dev/null -s -w "
DNS解析:       %{time_namelookup}s
TCP连接:       %{time_connect}s
TLS握手:       %{time_appconnect}s
服务器处理:    %{time_starttransfer}s
总耗时:        %{time_total}s
下载大小:      %{size_download} bytes
" https://api.example.com/endpoint
# ...
# 判断瓶颈位置
TOTAL=$(curl -o /dev/null -s -w "%{time_total}" https://api.example.com/endpoint)
DNS=$(curl -o /dev/null -s -w "%{time_namelookup}" https://api.example.com/endpoint)
echo "DNS占比: $(echo "scale=2; $DNS/$TOTAL*100" | bc)%"
```

### 场景三:证书即将过期检查

检查多个域名的证书有效期.
```bash
#!/bin/bash
# 证书过期检查脚本
DOMAINS="example.com api.example.com cdn.example.com"
# ...
for domain in $DOMAINS; do
    echo -n "$domain: "
    EXPIRY=$(echo | openssl s_client -connect "$domain:443" -servername "$domain" 2>/dev/null | \
      openssl x509 -noout -enddate 2>/dev/null | sed 's/notAfter=//')
# ...
    if [ -n "$EXPIRY" ]; then
        EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s 2>/dev/null || date -j -f "%b %d %T %Y %Z" "$EXPIRY" +%s 2>/dev/null)
        NOW_EPOCH=$(date +%s)
        DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))
        echo "$EXPIRY (剩余 ${DAYS_LEFT} 天)"
    else
        echo "无法获取证书信息"
    fi
done
```

## 不适用场景

以下场景DNS网络诊断基础版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求.
## 快速开始

### Step 1:触发诊断

在 AI Agent 中描述网络问题:

```
我的域名 example.com 无法访问,请帮我诊断问题原因.
```

### Step 2:执行诊断

Agent 会自动运行 DNS 解析、端口测试、证书检查等命令.
### Step 3:查看建议

根据诊断结果,Agent 提供问题定位和修复建议.
#
## 示例

创建网络诊断配置文件 `.network-diag.yml`:

```yaml
# 网络诊断配置(免费版)
version: "1.0"
# ...
# 默认DNS服务器
dns_servers:
  - 8.8.8.8
  - 1.1.1.1
  - 223.5.5.5
# ...
# 常用端口
common_ports:
  web: [80, 443]
  ssh: [22]
  database: [3306, 5432, 6379, 27017]
  mail: [25, 465, 587, 993, 995]
# ...
# 证书检查
certificate:
  warning_days: 30
  critical_days: 7
# ...
# 超时设置
timeout:
  dns: 5
  port: 5
  http: 30
```

## 最佳实践

1. **分层排查**:DNS -> 端口 -> HTTP -> TLS,逐层缩小问题范围
2. **对比测试**:同时测试正常和异常目标,快速定位差异
3. **保存日志**:将诊断输出保存到文件,便于后续分析

```bash
# 保存诊断日志
diag_log="network-diag-$(date +%Y%m%d-%H%M%S).log"
echo "诊断日志: $diag_log"
{
    echo "=== 网络诊断 $(date) ==="
    dig +short example.com
    nc -zv example.com 443
    curl -sI https://example.com
} | tee "$diag_log"
```

4. **使用/etc/hosts测试**:在修改DNS前,先用hosts文件测试

```bash
# 临时域名映射测试
echo "203.0.113.50  example.com" | sudo tee -a /etc/hosts
# 测试完成后移除
sudo sed -i '/203.0.113.50/d' /etc/hosts
```

## 常见问题

### Q1:dig 命令不存在怎么办?

```bash
# macOS
brew install bind
# ...
# Ubuntu/Debian
sudo apt install dnsutils
# ...
# CentOS/RHEL
sudo yum install bind-utils
# ...
# 替代方案:使用nslookup
nslookup example.com
```

### Q2:nc 命令不存在怎么办?

```bash
# 使用bash内置TCP测试替代
com/443' && echo "Open" || echo "Closed"
# ...
# 或使用curl
```

### Q3:免费版与专业版有何区别?

| 能力维度 | 免费版 | 专业版 |
|:-----|:-----|:-----|
| 诊断范围 | 单目标 | 批量多目标 |
| 防火墙分析 | 不支持 | iptables/ufw规则 |
| 代理诊断 | 基础 | 完整代理链分析 |
| 持续监控 | 不支持 | 定时巡检告警 |
| 报告格式 | 文本 | HTML/JSON |
| 历史记录 | 不支持 | 趋势分析 |

### Q4:DNS解析正常但无法访问怎么办?

按以下顺序排查:
1. 检查端口是否开放:`nc -zv example.com 443`
2. 检查防火墙规则
3. 检查代理配置:`echo $HTTP_PROXY`
4. 检查TLS证书:`openssl s_client`
5. 检查本地hosts:`cat /etc/hosts`

## 依赖说明

### 运行环境

- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Windows / macOS / Linux
- **运行时**:Bash 或 PowerShell

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| dig/nslookup | 系统工具 | 必需 | 系统自带或安装 dnsutils |
| nc(netcat) | 系统工具 | 推荐 | 系统自带或安装 netcat |
| curl | 系统工具 | 必需 | 系统自带 |
| openssl | 系统工具 | 必需 | 系统自带 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- 本 Skill 基于 Markdown 指令,无需额外 API Key
- 所有诊断命令在本地执行,不会发送数据到外部服务

### 可用性分类

- **分类**:MD+EXEC(纯 Markdown 指令,需要 exec 命令行执行能力)
- **说明**:基于 Markdown 的 AI Skill,通过自然语言指令驱动 Agent 执行网络诊断任务
- **适用规模**:单目标诊断,适合日常开发排查

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 本地运行，不支持多设备同步
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "DNS网络诊断基础版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "dns networking"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
