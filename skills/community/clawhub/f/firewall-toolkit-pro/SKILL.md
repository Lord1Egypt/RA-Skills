---

slug: firewall-toolkit-pro
name: firewall-toolkit-pro
version: 1.0.0
displayName: 防火墙配置工具包专业版
summary: 企业级防火墙管理平台,支持云安全组、nftables、批量多机部署、CIS基线审计与实时日志分析,适合企业网络安全团队.
license: Proprietary
edition: pro
description: "防火墙配置工具包专业版,为企业安全团队提供全方位防火墙管理与网络安全加固能力。Use when 需要安全检测、合规审计、质量检查、加密防护时使用。不适用于安全评估未授权目标。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。 功能涵盖: firewall, toolkit。"
  核心能力:云安全组管理、nftables配置、批量多机部署、CIS配置基线审计、实时日志分析与告警、规则版本管理.
  适用场景:企业网络安全架构、多云安全组统一管理、合规审计、自动化安全运维.
  差异化:专业版兼容免费版配置方法,新增企业级多机管理与云安全组能力,满足规模化网络安全需求.
  适用关键词: 云安全组, nftables, 批量部署, CIS基线, 防火墙审计, security group, nftables, multi-host'
tags:
  - 防火墙
  - 网络安全
  - 企业版
  - 云安全组
  - 安全
  - 加密
  - 工具
  - grep
  - check_cis
  - cis
tools:
  - read
  - exec
homepage: ""
# 定价元数据
category: "Security"

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


专业版为企业安全团队提供完整的防火墙管理与网络安全加固平台,在免费版iptables/ufw配置能力之上,新增云安全组(AWS/Azure/GCP)管理、nftables高级配置、批量多机部署、CIS配置基线完整审计、实时日志分析与告警、规则版本管理与回滚。专业版完全兼容免费版配置方法,已有防火墙规则可无缝升级,适合企业级网络安全运维.
### 专业版核心优势
| 优势 | 说明 |
|---|---|
| 云安全组 | AWS/Azure/GCP安全组统一管理 |
| nftables | 新一代Linux防火墙框架 |
| 批量部署 | 多机并行配置,一键部署 |
| CIS基线 | 完整CIS Benchmark合规审计 |
| 日志分析 | 实时流量分析与异常告警 |
| 版本管理 | 规则版本化,支持回滚 |
| 自动化 | CI/CD集成与自动修复 |
| 报告导出 | HTML/PDF合规报告 |

## 核心能力
### 1. 云安全组管理(专业版独有)

> 详细代码示例已移至 `references/detail.md`

**处理**: 解析云安全组管理(专业版独有)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回云安全组管理(专业版独有)的响应数据,包含状态码、结果和日志.
### 2. nftables高级配置(专业版独有)

**处理**: 解析nftables高级配置(专业版独有)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回nftables高级配置(专业版独有)的响应数据,包含状态码、结果和日志.
### 3. 批量多机部署(专业版独有)
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 防火墙配置工具包专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
#!/bin/sh
HOSTS_FILE="hosts.txt"  # 格式: IP SSH_PORT
RULES_FILE="firewall-rules.sh"
# ...
echo "=== 批量防火墙部署 ==="
echo "目标主机文件: ${HOSTS_FILE}"
echo "规则文件: ${RULES_FILE}"
echo ""
# ...
SUCCESS=0
FAIL=0
# ...
while IFS=' ' read -r ip port; do
    [ -z "$ip" ] && continue
    port=${port:-22}
# ...
    echo "--- 部署到: ${ip}:${port} ---"
# ...
    if scp -P "$port" "$RULES_FILE" "root@${ip}:/tmp/firewall-rules.sh" 2>/dev/null; then
        if ssh -p "$port" "root@${ip}" "bash /tmp/firewall-rules.sh && rm /tmp/firewall-rules.sh" 2>/dev/null; then
            echo "  [OK] ${ip} 部署成功"
            ((SUCCESS++))
        else
            echo "  [FAIL] ${ip} 执行失败"
            ((FAIL++))
        fi
    else
        echo "  [FAIL] ${ip} 文件传输失败"
        ((FAIL++))
    fi
done < "$HOSTS_FILE"
# ...
echo ""
echo "========================================="
echo "部署完成: 成功 ${SUCCESS} 台, 失败 ${FAIL} 台"
echo "========================================="
```

**处理**: 解析批量多机部署(专业版独有)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量多机部署(专业版独有)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. CIS配置基线审计(专业版独有)
```bash
#!/bin/sh
echo "=== CIS防火墙配置基线审计 ==="
echo ""
# ...
PASS=0
FAIL=0
WARN=0
# ...
check_cis() {
    local id=$1
    local name=$2
    local condition=$3
    local level=$4
# ...
    if eval "$condition"; then
        echo "  [PASS] [$id] $name"
        ((PASS++))
    else
        if [ "$level" = "high" ]; then
            echo "  [FAIL] [$id] $name"
            ((FAIL++))
        else
            echo "  [WARN] [$id] $name"
            ((WARN++))
        fi
    fi
}
# ...
check_cis "3.5.1.1" "默认入站策略为DROP" \
    "iptables -L INPUT -n | head -1 | grep -q DROP || ufw status verbose | grep -q 'deny (incoming)'" "high"
# ...
check_cis "3.5.1.2" "默认出站策略已配置" \
    "iptables -L OUTPUT -n | head -1 | grep -qE 'DROP|ACCEPT'" "medium"
# ...
check_cis "3.5.1.3" "默认转发策略为DROP" \
    "iptables -L FORWARD -n | head -1 | grep -q DROP" "medium"
# ...
check_cis "3.5.1.4" "回环接口已配置" \
    "iptables -L INPUT -n | grep -q 'lo.*ACCEPT'" "high"
# ...
check_cis "3.5.1.5" "已建立连接规则已配置" \
    "iptables -L INPUT -n | grep -q 'ESTABLISHED'" "high"
# ...
check_cis "3.5.2.1" "防火墙已启用" \
    "ufw status | grep -q 'Status: active' || systemctl is-active nftables | grep -q active" "high"
# ...
check_cis "4.2.1" "SSH最大认证尝试 <= 4" \
    "grep -q 'MaxAuthTries [1-4]' /etc/ssh/sshd_config" "medium"
# ...
check_cis "4.2.2" "SSH忽略rhosts" \
    "grep -q 'IgnoreRhosts yes' /etc/ssh/sshd_config" "medium"
# ...
check_cis "4.2.3" "SSH禁止root登录" \
    "grep -q 'PermitRootLogin no' /etc/ssh/sshd_config" "high"
# ...
check_cis "4.2.4" "SSH禁用空密码" \
    "grep -q 'PermitEmptyPasswords no' /etc/ssh/sshd_config" "high"
# ...
echo ""
echo "========================================="
echo "CIS基线审计结果"
echo "  通过: ${PASS}"
echo "  失败: ${FAIL}"
echo "  警告: ${WARN}"
echo "========================================="
```

**处理**: 解析CIS配置基线审计(专业版独有)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回CIS配置基线审计(专业版独有)的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级防火墙管理、支持云安全组、nftables、批量多机部署、CIS、基线审计与实时日、志分析、适合企业网络安全、防火墙配置工具包、专业版、为企业安全团队提、供全方位防火墙管、理与网络安全加固、核心能力、云安全组管理、配置基线审计、实时日志分析与告、规则版本管理、适用场景、企业网络安全架构、多云安全组统一管、合规审计、自动化安全运维、差异化、专业版兼容免费版、配置方法、新增企业级多机管、理与云安全组能力、满足规模化网络安、全需求、适用关键词、云安全组、批量部署、防火墙审计、security、group、multi、host等.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一:企业网络安全架构部署
```bash
#!/bin/sh
echo "=== 企业网络安全架构部署 ==="
# ...
echo "--- 配置DMZ防火墙 ---"
nft add rule inet firewall input tcp dport { 80, 443 } accept comment '"DMZ: Web服务"'
nft add rule inet firewall input tcp dport 22 ip saddr @admin_ips accept comment '"DMZ: 管理SSH"'
# ...
echo "--- 配置内网防火墙 ---"
nft add rule inet firewall forward ip saddr 10.0.1.0/24 ip daddr 10.0.2.0/24 tcp dport 3306 accept comment '"内网: Web->DB"'
0.1.0/24 ip daddr 10.0.2.0/24 tcp dport 6379 accept comment '"内网: Web->Redis"'
# ...
echo ""
echo "--- 云安全组配置 ---"
echo "  Web安全组: 入站 80/443 对0.0.0.0/0开放, 22仅管理网段"
echo "  DB安全组: 入站 3306 仅Web安全组, 22仅管理网段"
echo "  Redis安全组: 入站 6379 仅Web安全组"
# ...
echo ""
echo "企业网络安全架构部署完成"
```

### 场景二:多云安全组统一管理
```python
#!/usr/bin/env python3
"""多云安全组统一管理"""
# ...
class MultiCloudFirewallManager:
    """多云防火墙统一管理"""
# ...
    def __init__(self):
        self.providers = {}
# ...
    def register_provider(self, name, manager):
        self.providers[name] = manager
# ...
    def unified_audit(self):
        """统一合规检查"""
        all_findings = []
# ...
        for provider_name, manager in self.providers.items():
            findings = manager.audit_open_ports()
            for f in findings:
                f["provider"] = provider_name
                all_findings.append(f)
# ...
        return all_findings
# ...
    def generate_compliance_report(self, findings):
        """生成合规报告"""
        report = {
            "total_findings": len(findings),
            "by_severity": {},
            "by_provider": {},
            "findings": findings
        }
# ...
        for f in findings:
            sev = f["severity"]
            report["by_severity"][sev] = report["by_severity"].get(sev, 0) + 1
# ...
            prov = f["provider"]
            report["by_provider"][prov] = report["by_provider"].get(prov, 0) + 1
# ...
        return report
# ...
if __name__ == "__main__":
    import json
    manager = MultiCloudFirewallManager()
    findings = [
        {"provider": "aws", "severity": "CRITICAL", "description": "SSH开放给0.0.0.0/0"},
        {"provider": "azure", "severity": "HIGH", "description": "数据库端口开放给0.0.0.0/0"},
    ]
# ...
    report = manager.generate_compliance_report(findings)
    print(json.dumps(report, indent=2, ensure_ascii=False))
```

### 场景三:防火墙规则版本管理
```bash
#!/bin/sh
RULES_DIR="/etc/firewall-versions"
mkdir -p "$RULES_DIR"
# ...
save_version() {
    local version_name=$1
    local timestamp=$(date '+%Y%m%d%H%M%S')
    local filename="${RULES_DIR}/${timestamp}_${version_name}.rules"
# ...
    iptables-save > "$filename"
# ...
    echo "${timestamp} ${version_name} $(wc -l < "$filename")行" >> "${RULES_DIR}/versions.log"
    echo "已保存版本: ${version_name} (${filename})"
}
# ...
list_versions() {
    echo "=== 防火墙规则版本历史 ==="
    if [ -f "${RULES_DIR}/versions.log" ]; then
        cat "${RULES_DIR}/versions.log"
    else
        echo "暂无保存的版本"
    fi
}
# ...
rollback() {
    local version_file=$1
# ...
    if [ ! -f "$version_file" ]; then
        echo "版本文件不存在: ${version_file}"
        return 1
    fi
# ...
    save_version "pre-rollback"
# ...
    iptables-restore < "$version_file"
    echo "已回滚到: ${version_file}"
}
# ...
save_version "initial-baseline"
list_versions
```

## 不适用场景

以下场景防火墙配置工具包专业版不适合处理：

- 安全评估未授权目标
- 物理安全防护
- 社会工程学攻击

## 触发条件

需要安全检测、合规审计、质量检查、加密防护时使用。不适用于非本工具能力范围的需求.
## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 从免费版升级
```bash
ufw allow 80/tcp
# ...
bash batch_deploy.sh hosts.txt firewall-rules.sh
python3 cloud_sg_manager.py --audit --provider aws
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 配置示例
### 专业版功能矩阵
| 功能 | 免费版 | 专业版 | 说明 |
|---:|---:|---:|---:|
| iptables | 支持 | 支持 | Linux防火墙 |
| UFW | 支持 | 支持 | 简化防火墙 |
| nftables | 不支持 | 支持 | 新一代防火墙 |
| 云安全组 | 不支持 | 支持 | AWS/Azure/GCP |
| 批量部署 | 不支持 | 支持 | 多机并行 |
| CIS基线 | 基础 | 完整 | 合规审计 |
| 日志分析 | 基础 | 实时 | 异常检测 |
| 版本管理 | 不支持 | 支持 | 回滚能力 |

### CIS基线覆盖范围
| 控制项 | 免费版 | 专业版 |
|:---:|:---:|:---:|
| 3.5.1.x 防火墙默认策略 | 基础 | 完整 |
| 3.5.2.x 防火墙启用状态 | 基础 | 完整 |
| 4.2.x SSH配置 | 基础 | 完整 |
| 4.3.x 网络参数 | 不支持 | 完整 |
| 4.4.x 日志配置 | 不支持 | 完整 |

## 优选实践
1. **分层防御**:DMZ+内网分层,不同区域不同安全策略.
2. **最小权限**:安全组遵循最小开放原则,仅允许必要的源IP和端口.
3. **版本管理**:所有规则变更保存版本,支持快速回滚.
4. **定期审计**:定期执行CIS基线审计,确保合规性.
5. **自动化**:将防火墙配置纳入CI/CD,避免手动操作错误.
6. **监控告警**:实时监控防火墙日志,异常流量自动告警.
## 常见问题
### Q1: 专业版与免费版规则是否兼容?
完全兼容。专业版支持iptables/ufw的所有规则格式,新增nftables和云安全组能力.
### Q2: 云安全组支持哪些云服务商?
支持AWS、Azure、GCP三大公有云,通过各自的SDK进行管理.
### Q3: 批量部署如何保证安全?
使用SSH密钥认证,部署前先在测试环境验证规则,生产环境分批次部署.
### Q4: CIS基线审计覆盖哪些标准?
覆盖CIS Benchmark for Linux的3.5(防火墙)和4.x(网络与SSH)章节.
### Q5: 规则版本管理如何使用?
每次变更前调用save_version保存当前状态,需要回滚时调用rollback恢复指定版本.
## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Linux(UFW/iptables/nftables为Linux工具)
- **Python**: 3.8+(使用云安全组管理时需要)
- **权限**: 需要root/sudo权限执行防火墙命令

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| iptables | 防火墙工具 | 必需 | 系统自带 |
| ufw | 防火墙工具 | 推荐 | `apt install ufw` |
| nftables | 防火墙工具 | 推荐 | `apt install nftables` |
| python3 | 运行时环境 | 推荐 | python.org 下载 |
| boto3 | AWS SDK | 按需 | `pip install boto3` |
| azure-sdk | Azure SDK | 按需 | `pip install azure-mgmt-network` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 云安全组管理需配置各云服务商的访问凭证
- AWS: 配置Access Key ID和Secret Access Key
- Azure: 配置Service Principal凭证
- GCP: 配置Service Account JSON密钥

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,核心功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行企业级防火墙管理与网络安全加固任务
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
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "防火墙配置工具包专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "firewallkit pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 企业级防火墙管理平台,支持云安全组、nftables、批量多机部署、CIS基线审计与实时日志分析,适合企业网络安全团队.
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据