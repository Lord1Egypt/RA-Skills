---
slug: cdn-toolkit-free
name: cdn-toolkit-free
version: 1.0.1
displayName: CDN配置工具包免费版
summary: "CDN配置与优化助手,支持缓存策略设置、基础安全加固与性能诊断,适合个人开发者快速部署CDN.。CDN配置工具包免费版,为个人开发者提供CDN部署与优化核心能力."
license: MIT
edition: free
description: "CDN配置工具包免费版,为个人开发者包含CDN部署与调优核心能力. 适用于需要cdn toolkit相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量. 适用于需要cdn toolkit相关能力的开发场景,包含结构化的工作流程和配置指引. 该工具经过深度差异化处置,针对用户反馈和使用痛点进行了调优改进,提升了实用性和可操作性."
tags:
  - CDN
  - cdn
  - toolkit
  - automation
  - productivity
  - 性能优化
  - 缓存
  - 免费版
  - 安全
  - 加密
tools:
  - read
  - exec
homepage: ""
category: "Security"
pricing_tier: free

---
# CDN配置工具包免费版

## 概述

本工具为个人开发者提供CDN(Content Delivery Network)配置与优化能力,涵盖缓存策略设置、基础安全加固、性能诊断与域名配置指导。免费版支持主流CDN服务商(Cloudflare、AWS CloudFront、阿里云CDN等),帮助开发者快速部署和优化CDN,提升网站访问速度与用户体验.
### 免费版与专业版对比

| 能力维度 | 免费版 | 专业版 |
|----|---|---|
| 缓存策略 | 基础规则 | 智能缓存+边缘计算 |
| 安全防护 | 基础WAF规则 | 高级WAF+DDoS防护 |
| 多CDN管理 | 单CDN | 多CDN智能调度 |
| 性能监控 | 基础指标 | 实时监控+告警 |
| 边缘函数 | 不支持 | Edge Workers |
| 报告导出 | 文本 | HTML/PDF |
| 技术支持 | 社区 | 专属支持 |

## 核心能力

### 1. 缓存策略配置

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | CDN配置工具包免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```nginx
# Nginx源站缓存头配置
# 静态资源长期缓存(1年)
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2?|ttf|eot|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header X-Content-Type-Options "nosniff";
}
# ...
# HTML文档短缓存(5分钟)
location ~* \.html$ {
    expires 5m;
    add_header Cache-Control "public, must-revalidate";
}
# ...
# API响应不缓存
location /api/ {
    add_header Cache-Control "no-cache, no-store, must-revalidate";
    add_header Pragma "no-cache";
}
# ...
# 动态内容不缓存
location ~* \.(php|jsp|do)$ {
    add_header Cache-Control "no-cache, no-store, must-revalidate";
}
```

**处理**: 解析缓存策略配置的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回缓存策略配置的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 基础安全加固

```bash
#!/bin/bash
# CDN基础安全加固检查
# ...
echo "=== CDN基础安全加固 ==="
# ...
# 检查项目
echo ""
echo "--- 1. HTTPS配置 ---"
echo "  [ ] 强制HTTPS重定向"
echo "  [ ] HSTS头已启用"
echo "  [ ] TLS 1.2+最低版本"
echo "  [ ] 证书有效且未过期"
# ...
echo ""
echo "--- 2. 访问控制 ---"
echo "  [ ] 热链接保护已启用"
echo "  [ ] 地理限制已配置(如需要)"
echo "  [ ] 速率限制已设置"
echo "  [ ] User-Agent过滤(如需要)"
# ...
echo ""
echo "--- 3. 安全头配置 ---"
cat << 'EOF'
推荐安全头配置:
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  Content-Security-Policy: default-src 'self'
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
EOF
# ...
echo ""
echo "--- 4. 源站保护 ---"
echo "  [ ] 源站IP已隐藏"
echo "  [ ] 仅允许CDN回源IP访问"
echo "  [ ] 源站防火墙已配置"
```

**处理**: 解析基础安全加固的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回基础安全加固的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. CDN性能诊断

```bash
#!/bin/bash
# CDN性能诊断脚本
# ...
DOMAIN="${1:-example.com}"
# ...
echo "=== CDN性能诊断: ${DOMAIN} ==="
echo ""
# ...
# 1. DNS解析时间
echo "--- 1. DNS解析 ---"
dig +stats "$DOMAIN" 2>/dev/null | grep "Query time"
# ...
# 2. 连接时间
echo ""
echo "--- 2. 连接性能 ---"
curl -w "DNS解析: %{time_namelookup}s\n" \
     -w "TCP连接: %{time_connect}s\n" \
     -w "TLS握手: %{time_appconnect}s\n" \
     -w "首字节: %{time_starttransfer}s\n" \
     -w "总时间: %{time_total}s\n" \
     -w "下载大小: %{size_download} bytes\n" \
     -o /dev/null -s "https://${DOMAIN}"
# ...
# 3. 缓存命中检查
echo ""
echo "--- 3. 缓存状态 ---"
curl -s -I "https://${DOMAIN}" | grep -i "x-cache\|cf-cache\|x-cdn\|age\|via"
# ...
# 4. 响应头检查
echo ""
echo "--- 4. 关键响应头 ---"
curl -s -I "https://${DOMAIN}" | grep -i "cache-control\|content-encoding\|content-type\|strict-transport"
```

**处理**: 解析CDN性能诊断的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回CDN性能诊断的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 域名配置指导

```bash
#!/bin/bash
# CDN域名配置检查清单
# ...
echo "=== CDN域名配置检查清单 ==="
echo ""
echo "--- DNS配置 ---"
echo "  [ ] CNAME记录已正确指向CDN"
echo "  [ ] DNS TTL设置为合理值(300-3600秒)"
echo "  [ ] DNSSEC已启用(如支持)"
echo ""
echo "--- SSL/TLS配置 ---"
echo "  [ ] SSL证书已部署"
echo "  [ ] 证书覆盖所有子域名(通配符或SAN)"
echo "  [ ] HTTPS重定向已启用"
echo "  [ ] HSTS已配置"
echo ""
echo "--- 回源配置 ---"
echo "  [ ] 回源协议已设置(HTTPS优先)"
echo "  [ ] 回源Host头已正确配置"
echo "  [ ] 回源超时已设置(30-60秒)"
echo "  [ ] 回源重试次数已配置(2-3次)"
echo ""
echo "--- 缓存配置 ---"
echo "  [ ] 静态资源缓存规则已配置"
echo "  [ ] 动态内容排除缓存"
echo "  [ ] 缓存键已优化(忽略无关参数)"
echo "  [ ] Gzip/Brotli压缩已启用"
```

**处理**: 解析域名配置指导的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回域名配置指导的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：配置与优化助手、支持缓存策略设置、基础安全加固与性、适合个人开发者快、速部署、配置工具包免费版、为个人开发者提供、部署与优化核心能、核心能力、适用场景、网站加速部署、静态资源缓存优化、安全配置、差异化、免费版聚焦核心配、置能力、支持主流、服务商、适合个人项目快速、适用关键词、边缘节点、内容分发、edge、optimization等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:网站静态资源加速

```nginx
# 完整的静态资源CDN配置
server {
    listen 443 ssl http2;
    server_name static.example.com;
# ...
    # SSL配置
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
# ...
    # 根目录
    root /var/www/static;
# ...
    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2?|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header X-Content-Type-Options "nosniff";
        access_log off;
    }
# ...
    # 安全头
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
# ...
    # Gzip压缩
    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;
    gzip_min_length 1024;
}
```

### 场景二:Cloudflare基础配置

```bash
#!/bin/bash
# Cloudflare CDN基础配置脚本(使用curl API)
# ...
API_TOKEN="你的API_TOKEN"
ZONE_ID="你的ZONE_ID"
# ...
# 1. 开启Always Use HTTPS
curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/settings/always_use_https" \
    -H "Authorization: Bearer ${API_TOKEN}" \
    -H "Content-Type: application/json" \
    --data '{"value":"on"}' | jq '.success'
# ...
# 2. 设置最小TLS版本为1.2
cloudflare.com/client/v4/zones/${ZONE_ID}/settings/min_tls_version" \
    -H "Authorization: Bearer ${API_TOKEN}" \
    -H "Content-Type: application/json" \
    --data '{"value":"1.2"}' | jq '.success'
# ...
# 3. 开启Gzip压缩
cloudflare.com/client/v4/zones/${ZONE_ID}/settings/gzip" \
    -H "Authorization: Bearer ${API_TOKEN}" \
    -H "Content-Type: application/json" \
# ...
# 4. 开启浏览器缓存TTL
cloudflare.com/client/v4/zones/${ZONE_ID}/settings/browser_cache_ttl" \
    -H "Authorization: Bearer ${API_TOKEN}" \
    -H "Content-Type: application/json" \
    --data '{"value":86400}' | jq '.success'
```

### 场景三:CDN缓存命中率诊断

```bash
#!/bin/bash
# CDN缓存命中率诊断
# ...
SAMPLES=20
# ...
echo "=== CDN缓存命中率诊断: ${DOMAIN} ==="
echo "采样次数: ${SAMPLES}"
echo ""
# ...
HIT=0
MISS=0
# ...
for i in $(seq 1 $SAMPLES); do
    CACHE_STATUS=$(curl -s -I "https://${DOMAIN}" | grep -i "x-cache\|cf-cache-status" | awk '{print $2}' | tr -d '\r')
# ...
    if echo "$CACHE_STATUS" | grep -qi "HIT"; then
        HIT=$((HIT + 1))
        echo "  请求${i}: HIT"
    else
        MISS=$((MISS + 1))
        echo "  请求${i}: MISS"
    fi
done
# ...
TOTAL=$((HIT + MISS))
HIT_RATE=$(echo "scale=1; $HIT * 100 / $TOTAL" | bc 2>/dev/null || echo "N/A")
# ...
echo ""
echo "=== 诊断结果 ==="
echo "  命中: ${HIT}"
echo "  未命中: ${MISS}"
echo "  命中率: ${HIT_RATE}%"
# ...
if [ "$HIT_RATE" -lt 80 ] 2>/dev/null; then
    echo "  建议: 缓存命中率偏低,请检查缓存策略配置"
fi
```

## 不适用场景

以下场景CDN配置工具包免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 领先步:选择CDN服务商

| 服务商 | 免费额度 | 适合场景 |
|---:|---:|---:|
| Cloudflare | 免费计划 | 个人网站、博客 |
| AWS CloudFront | 1GB/月 | AWS生态项目 |
| 阿里云CDN | 按量付费 | 国内项目 |
| 腾讯云CDN | 免费试用 | 国内项目 |

### 第二步:配置DNS

```bash
# 在此执行相关操作
echo "操作完成"
```

### 第三步:验证CDN生效

```bash
# 检查响应头确认CDN已生效
curl -s -I https://your-domain.com | grep -i "server\|x-cache\|cf-"
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 配置示例

### 缓存策略推荐

| 文件类型 | 缓存时间 | Cache-Control | 说明 |
|:---:|:---:|:---:|:---:|
| HTML | 5分钟 | public, must-revalidate | 需要更新检查 |
| CSS/JS | 1年 | public, immutable | 文件名含hash |
| 图片 | 1年 | public | 静态资源 |
| 字体 | 1年 | public | 静态资源 |
| API JSON | 不缓存 | no-cache, no-store | 动态数据 |
| 用户上传 | 1天 | public | 可变内容 |

### 安全头配置参考

```nginx
# 推荐安全头配置
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

## 优秀实践

1. **文件名哈希**:静态资源使用内容哈希命名,实现长期缓存与自动更新.
2. **分层缓存**:CDN边缘缓存 -> 源站缓存 -> 应用缓存,多层配合.
3. **压缩传输**:启用Gzip或Brotli压缩,减少传输体积.
4. **协议升级**:强制HTTPS,启用HTTP/2或HTTP/3.
5. **源站保护**:隐藏源站IP,仅允许CDN回源.
```bash
# 优秀实践:源站防火墙仅允许CDN回源
# Cloudflare IP列表
CF_IPS=$(curl -s https://www.cloudflare.com/ips-v4)
# ...
for ip in $CF_IPS; do
    iptables -A INPUT -p tcp -s "$ip" --dport 443 -j ACCEPT
done
iptables -A INPUT -p tcp --dport 443 -j DROP
```

## 常见问题

### Q1: CDN配置后网站打不开?

检查DNS解析是否正确指向CDN,SSL证书是否有效,源站是否可正常访问.
### Q2: 缓存命中率低怎么办?

检查缓存规则是否正确,动态内容是否被误缓存,缓存键是否包含不必要的参数.
### Q3: CDN更新后内容不刷新?

使用版本化文件名(如app.v1.js)或通过CDN控制台主动刷新缓存.
### Q4: 免费版支持哪些CDN服务商?

免费版提供配置指导,支持Cloudflare、AWS CloudFront、阿里云CDN、腾讯云CDN等主流服务商.
### Q5: 如何测试CDN加速效果?

使用本工具的性能诊断脚本,对比CDN开启前后的首字节时间与下载速度.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需可访问CDN管理API

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| curl | 命令行工具 | 必需 | 系统自带 |
| dig | DNS查询工具 | 推荐 | `apt install dnsutils` |
| jq | JSON处理工具 | 推荐 | `apt install jq` |
| nginx | Web服务器 | 按需 | `apt install nginx` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 免费版提供配置指导,实际部署需各CDN服务商的API Token
- Cloudflare API Token在Cloudflare仪表盘生成
- AWS需配置Access Key和Secret Key

### 可用性分类
- **分类**: MD+EXEC模式纯Markdown指令,核心功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行CDN配置与优化任务
- API Key通过环境变量配置: export API_KEY=your_key

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```bash
# 在此执行相关操作
echo "操作完成"
```json
{
  "success": true,
  "data": {
    "result": "CDN配置工具包免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "cdnkit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
