---
slug: firewall-toolkit-free
name: firewall-toolkit-free
version: 1.0.1
displayName: 防火墙配置工具包免费版
summary: 服务器防火墙配置助手,支持iptables/uffw基础规则、端口管理与安全基线检查,适合个人开发者服务器安全防护.
license: MIT
edition: free
description: "防火墙配置工具包免费版,为个人开发者包含服务器防火墙配置与安全加固能力. 适用于需要firewall toolkit相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量. 适用于需要firewall toolkit相关能力的开发场景,包含结构化的工作流程和配置指引."
tags:
  - 防火墙
  - firewall
  - toolkit
  - automation
  - productivity
  - 网络安全
  - iptables
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
# 防火墙配置工具包免费版

## 概述

本工具为个人开发者提供服务器防火墙配置与安全加固能力,涵盖iptables/ufw规则配置、端口管理、安全基线检查与防火墙状态诊断。免费版支持Linux主流防火墙工具,帮助开发者快速完成服务器初始安全加固,适合个人服务器与小型项目使用.
### 免费版与专业版对比

| 能力维度 | 免费版 | 专业版 |
|----|---|---|
| 防火墙类型 | iptables/ufw | +云安全组+nftables |
| 规则管理 | 手动配置 | 模板化+批量部署 |
| 安全基线 | 基础检查 | 完整CIS基线 |
| 日志分析 | 基础日志 | 实时分析+告警 |
| 多机管理 | 单机 | 批量多机 |
| 自动化 | 脚本 | CI/CD集成 |
| 报告导出 | 文本 | HTML/PDF |

## 核心能力

### 1. UFW防火墙配置

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 防火墙配置工具包免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
#!/bin/bash
# UFW基础安全配置脚本
# ...
echo "=== UFW防火墙基础配置 ==="
# ...
# 重置防火墙规则
ufw --force reset
# ...
# 设置默认策略
ufw default deny incoming     # 默认拒绝所有入站
ufw default allow outgoing    # 默认允许所有出站
# ...
# 允许SSH连接(重要:先放行SSH避免锁死)
ufw allow 22/tcp comment 'SSH'
# ...
# 允许HTTP/HTTPS
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
# ...
# 已知限制
ufw limit 22/tcp comment 'SSH限速'
# ...
# 启用防火墙
ufw --force enable
# ...
# 显示状态
echo ""
echo "=== 当前防火墙规则 ==="
ufw status numbered
# ...
echo ""
echo "防火墙配置完成"
```

**处理**: 解析UFW防火墙配置的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回UFW防火墙配置的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. iptables高级规则

```bash
#!/bin/bash
# iptables安全加固脚本
# ...
echo "=== iptables安全加固 ==="
# ...
# 清除现有规则
iptables -F
iptables -X
iptables -Z
# ...
# 设置默认策略
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
# ...
# 允许回环接口
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
# ...
# 允许已建立的连接
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
# ...
# 允许SSH(限制速率:每分钟最多5次新连接)
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 5 -j DROP
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
# ...
# 允许HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
# ...
# 防止SYN Flood攻击
iptables -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j ACCEPT
iptables -A INPUT -p tcp --syn -j DROP
# ...
# 防止端口扫描
iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
# ...
# 记录被拒绝的连接(限速避免日志洪水)
iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-dropped: " --log-level 4
iptables -A INPUT -j DROP
# ...
# 保存规则
iptables-save > /etc/iptables/rules.v4
# ...
echo "iptables安全加固完成"
echo ""
echo "=== 当前规则 ==="
iptables -L -n -v --line-numbers
```

**处理**: 解析iptables高级规则的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回iptables高级规则的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 端口管理与检查

```bash
#!/bin/bash
# 端口安全检查脚本
# ...
echo "=== 端口安全检查 ==="
echo ""
# ...
# 1. 检查监听端口
echo "--- 1. 监听端口列表 ---"
ss -tlnp | awk 'NR>1 {printf "  %-8s %-20s %s\n", $4, $6, $7}' | sort
# ...
echo ""
echo "--- 2. 危险端口检查 ---"
HIGHRISK_PORTS="21 23 25 53 69 110 143 161 389 445 636 873 993 995 1433 1521 2375 3306 3389 5432 5900 6379 9200 11211 27017"
for port in $HIGHRISK_PORTS; do
    if ss -tlnp | grep -q ":${port} "; then
        SERVICE=$(ss -tlnp | grep ":${port} " | awk '{print $7}' | head -1)
        echo "  [!] 端口 ${port} 正在监听: ${SERVICE}"
    fi
done
# ...
echo ""
echo "--- 3. 外部可达端口检查 ---"
echo "  以下端口对外开放(0.0.0.0):"
ss -tlnp | grep "0.0.0.0:" | awk '{print "    " $4}' | sort -u
# ...
echo ""
echo "--- 4. 防火墙规则中的开放端口 ---"
if command -v ufw &> /dev/null; then
    ufw status | grep "ALLOW" | awk '{print "    " $1}'
elif command -v iptables &> /dev/null; then
    iptables -L INPUT -n | grep "dpt:" | awk '{print "    " $NF}'
fi
```

**处理**: 解析端口管理与检查的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回端口管理与检查的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 安全基线检查

```bash
#!/bin/bash
# 防火墙安全基线检查
# ...
echo "=== 防火墙安全基线检查 ==="
echo ""
# ...
step_done=0
FAIL=0
# ...
check() {
    local name=$1
    local condition=$2
    if eval "$condition"; then
        echo "  [step_done] $name"
        ((step_done++))
    else
        echo "  [FAIL] $name"
        ((FAIL++))
    fi
}
# ...
# 1. 防火墙是否启用
if command -v ufw &> /dev/null; then
    check "UFW防火墙已启用" "ufw status | grep -q 'Status: active'"
elif command -v iptables &> /dev/null; then
    check "iptables INPUT策略为DROP" "iptables -L INPUT -n | head -1 | grep -q DROP"
fi
# ...
# 2. SSH是否限制
check "SSH端口已配置规则" "ss -tlnp | grep -q ':22 '"
# ...
# 3. 默认入站策略
if command -v ufw &> /dev/null; then
    check "默认拒绝入站" "ufw status verbose | grep -q 'Default: deny (incoming)'"
fi
# ...
# 4. 仅必要端口开放
check "无Telnet端口(23)" "! ss -tlnp | grep -q ':23 '"
check "无FTP端口(21)" "! ss -tlnp | grep -q ':21 '"
check "无Redis端口(6379)对外" "! ss -tlnp | grep '0.0.0.0:6379'"
check "无数据库端口(3306/5432)对外" "! ss -tlnp | grep -E '0.0.0.0:(3306|5432)'"
# ...
echo ""
echo "========================================="
echo "基线检查完成: 通过 ${step_done} 项, 失败 ${FAIL} 项"
echo "========================================="
```

**处理**: 解析安全基线检查的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回安全基线检查的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：服务器防火墙配置、iptables、uffw、基础规则、端口管理与安全基、线检查、适合个人开发者服、务器安全防护、防火墙配置工具包、免费版、为个人开发者提供、与安全加固能力、核心能力、ufw、规则配置、端口管理、安全基线检查、防火墙状态诊断、适用场景、服务器初始安全加、端口访问控制、基础防火墙规则管、差异化、免费版聚焦单机防、火墙配置、Linux、主流防火墙工具、适合个人服务器快、速加固、适用关键词、防火墙、安全基线、firewall、security、group、network等.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
- 不适用: 需要人工判断的复杂决策场景

### 场景一:新服务器初始加固

```bash
#!/bin/bash
# 新服务器完整安全加固脚本
# ...
echo "=== 新服务器安全加固 ==="
echo "服务器: $(hostname)"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
# ...
# 1. 配置防火墙
echo "--- 1. 配置UFW防火墙 ---"
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw limit 22/tcp      # SSH限速
ufw allow 80/tcp      # HTTP
ufw allow 443/tcp     # HTTPS
ufw --force enable
echo "防火墙已启用"
# ...
# 2. 关闭危险服务
echo ""
echo "--- 2. 关闭危险服务 ---"
for service in telnet rsh rlogin rexec; do
    systemctl stop "$service" 2>/dev/null
    systemctl disable "$service" 2>/dev/null
    echo "  已关闭: ${service}"
done
# ...
# 3. SSH安全加固
echo ""
echo "--- 3. SSH安全加固 ---"
SSH_CONFIG="/etc/ssh/sshd_config"
if [ -f "$SSH_CONFIG" ]; then
    # 禁止root登录
    sed -i 's/#PermitRootLogin.*/PermitRootLogin no/' "$SSH_CONFIG"
    # 禁止密码认证(确保已配置密钥认证)
    # sed -i 's/#PasswordAuthentication.*/PasswordAuthentication no/' "$SSH_CONFIG"
    # 修改默认端口(可选)
    # sed -i 's/#Port 22/Port 2222/' "$SSH_CONFIG"
    systemctl restart sshd
    echo "SSH配置已加固"
fi
# ...
# 依赖说明
echo ""
echo "--- 4. 安装Fail2Ban ---"
if ! command -v fail2ban-client &> /dev/null; then
    apt-get update -qq && apt-get install -y -qq fail2ban
    systemctl status fail2ban
    systemctl start fail2ban
    echo "Fail2Ban已安装"
fi
# ...
echo ""
echo "=== 服务器加固完成 ==="
ufw status
```

### 场景二:Web服务器防火墙配置

```bash
#!/bin/bash
# Web服务器专用防火墙配置
# ...
echo "=== Web服务器防火墙配置 ==="
# ...
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
# ...
# SSH(限速防暴力破解)
ufw limit 22/tcp
# ...
# Web服务
ufw allow 80/tcp       # HTTP
ufw allow 443/tcp      # HTTPS
# ...
# 仅允许指定IP访问管理端口
# ufw allow from ${SERVER_HOST} to any port 8080  # 管理后台
# ...
# 拒绝数据库端口外部访问
ufw deny 3306/tcp      # MySQL
ufw deny 5432/tcp      # `PostgreSQL`数据库端口
ufw deny 6379/tcp      # Redis
ufw deny 27017/tcp     # MongoDB
# ...
ufw --force enable
echo "Web服务器防火墙配置完成"
ufw status
```

### 场景三:防火墙规则审计

```bash
#!/bin/bash
# 防火墙规则审计
# ...
echo "=== 防火墙规则审计 ==="
echo ""
# ...
echo "--- 1. UFW规则列表 ---"
ufw status numbered 2>/dev/null || echo "UFW未安装"
# ...
echo ""
echo "--- 2. iptables规则 ---"
iptables -L -n --line-numbers 2>/dev/null
# ...
echo ""
echo "--- 3. 规则数量统计 ---"
INPUT_RULES=$(iptables -L INPUT -n 2>/dev/null | wc -l)
OUTPUT_RULES=$(iptables -L OUTPUT -n 2>/dev/null | wc -l)
echo "  INPUT规则: ${INPUT_RULES}"
echo "  OUTPUT规则: ${OUTPUT_RULES}"
# ...
echo ""
echo "--- 4. 开放端口统计 ---"
OPEN_PORTS=$(ufw status 2>/dev/null | grep "ALLOW" | wc -l)
echo "  开放端口数: ${OPEN_PORTS}"
```

## 快速开始

### 领先步:检查防火墙状态

```bash
# 检查UFW状态
sudo ufw status verbose
# ...
# 检查iptables状态
sudo iptables -L -n
```

### 第二步:运行基础加固

```bash
# 使用UFW快速加固
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw limit 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```

### 第三步:验证配置

```bash
# 查看规则
sudo ufw status numbered
# ...
# 测试端口连通性
curl -s -o /dev/null -w "%{http_code}" http://localhost
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 优秀实践

1. **默认拒绝**:所有入站流量默认拒绝,仅开放必要端口.
2. **最小开放**:仅开放业务必需的端口,减少攻击面.
3. **SSH限速**:对SSH端口使用limit规则,防止暴力破解.
4. **数据库隔离**:数据库端口不对外暴露,仅允许本地访问.
5. **定期审计**:定期检查防火墙规则,清理过期规则.
```bash
# 优秀实践:防火墙变更流程
safe_firewall_change() {
    local action=$1
    local rule=$2
# ...
    echo "变更前规则:"
    ufw status numbered
# ...
    echo ""
    echo "执行: ufw ${action} ${rule}"
    ufw "$action" "$rule"
# ...
    echo ""
    echo "变更后规则:"
    ufw status numbered
# ...
    echo ""
    echo "请验证服务是否正常,如异常请执行回滚:"
    echo "  ufw delete ${rule}"
}
```

## 已知限制

- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Linux(UFW/iptables为Linux工具)
- **权限**: 需要root/sudo权限执行防火墙命令

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| ufw | 防火墙工具 | 推荐 | `apt install ufw` |
| iptables | 防火墙工具 | 必需 | 系统自带 |
| ss | 端口检查 | 必需 | `apt install iproute2` |
| fail2ban | 入侵防护 | 推荐 | `apt install fail2ban` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 免费版为纯本地操作,无需API Key
- 需要root/sudo权限执行防火墙配置命令

### 可用性分类
- **分类**: MD+EXEC模式纯Markdown指令,核心功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行服务器防火墙配置与安全加固任务

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "防火墙配置工具包免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "firewallkit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
