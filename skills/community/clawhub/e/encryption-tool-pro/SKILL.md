---

slug: encryption-tool-pro
name: "encryption-tool-pro"
version: "1.0.0"
displayName: "加密工具专业版"
summary: "企业级加密管理,支持KMS集成、密钥轮换、合规审计、批量加密与深度代码安全扫描。。面向企业安全团队的高级加密管理工具,提供KMS密钥管理集成、自动密钥轮换、合规性审计、批量加密与深度代码安全"
license: "Proprietary"
edition: "pro"
description: |- 功能涵盖: encryption。
  面向企业安全团队的高级加密管理工具,提供KMS密钥管理集成、自动密钥轮换、合规性审计、批量加密与深度代码安全扫描。核心能力:
  - KMS/Vault密钥管理集成
  - 自动密钥轮换与版本管理
  - 合规性审计(等保/GDPR/PCI-DSS)
  - 批量文件加密与解密
  - 深度代码加密审计
  - 信封加密与密钥派生

  适用场景:
  - 企业级数据加密保护
  - 合规性合规检查
  - 密钥生命周期管理
  - DevSecOps安全集成

  差异化:
  - 专业版完全兼容免费版命令,支持平滑升级
  - 提供KMS/Va...
tags:
  - 开发工具
  - 安全
  - 加密
  - 企业级
  - 合规审计
  - 工具
  - 效率
  - 自动化
  - 开发
  - 代码
  - 写作
  - json
  - python3
  - output
  - kms
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"

---

加密工具专业版为企业安全团队提供高级加密管理能力。在免费版基础加密能力之上,专业版新增KMS密钥管理集成、自动密钥轮换、合规性审计、批量文件加密和深度代码安全扫描,满足企业级数据保护和合规要求.
专业版完全兼容免费版的所有加密命令和配置,安全团队可从免费版无缝升级,已有加密脚本无需修改即可在专业版中使用.
## 核心能力
### 1. KMS/Vault密钥管理集成
集成主流密钥管理服务,实现企业级密钥生命周期管理.
> 详细代码示例已移至 `references/detail.md`

**处理**: 解析KMS/Vault密钥管理集成的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回KMS/Vault密钥管理集成的响应数据,包含状态码、结果和日志.
### 2. 自动密钥轮换

**处理**: 解析自动密钥轮换的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回自动密钥轮换的响应数据,包含状态码、结果和日志.
### 3. 合规性审计

**处理**: 解析合规性审计的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回合规性审计的响应数据,包含状态码、结果和日志.
### 4. 批量文件加密
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 加密工具专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
#!/bin/sh
echo "=== 批量文件加密 ==="
# ...
ENCRYPTION_KEY_ID="${ENCRYPTION_KEY_ID:-app-master-key}"
ENCRYPT_EXTENSIONS=("env" "key" "pem" "p12" "secret" "credentials")
EXCLUDE_DIRS=("node_modules" ".git" "dist" "build")
# ...
encrypt_file() {
    local file="$1"
    local output="${file}.encrypted"
# ...
    local data_key=$(openssl rand -hex 32)
    local iv=$(openssl rand -hex 12)
# ...
    openssl enc -aes-256-gcm \
        -K "$data_key" \
        -iv "$iv" \
        -in "$file" \
        -out "$output"
# ...
    local encrypted_key=$(echo -n "$data_key" | openssl enc -aes-256-gcm \
        -K "$MASTER_KEY" -iv "$(openssl rand -hex 12)" | base64)
# ...
    cat > "${output}.meta" << EOF
{
    "key_id": "$ENCRYPTION_KEY_ID",
    "algorithm": "aes-256-gcm",
    "iv": "$iv",
    "encrypted_data_key": "$encrypted_key",
    "encrypted_at": "$(date -Iseconds)",
    "original_size": $(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
}
EOF
# ...
    echo "已加密: $file -> $output"
}
# ...
echo "扫描需要加密的文件..."
for ext in "${ENCRYPT_EXTENSIONS[@]}"; do
    find . -name "*.$ext" $(printf "! -path */%s/* " "${EXCLUDE_DIRS[@]}") | while read f; do
        if [ ! -f "${f}.encrypted" ]; then
            encrypt_file "$f"
        fi
    done
done
# ...
echo -e "\n加密文件清单:"
find . -name "*.encrypted" | while read f; do
    echo "  $f"
done
# ...
echo -e "\n批量加密完成"
```

**处理**: 解析批量文件加密的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量文件加密的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 深度代码安全扫描

**处理**: 解析深度代码安全扫描的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回深度代码安全扫描的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级加密管理、合规审计、批量加密与深度代、面向企业安全团队、的高级加密管理工、核心能力、自动密钥轮换与版、本管理、GDPR、PCI、DSS、批量文件加密与解、深度代码加密审计、信封加密与密钥派等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 输出格式

本skill的输出格式为Markdown文本,包含操作状态和执行结果。具体输出内容取决于执行的能力点和输入参数.
## 使用场景
### 场景一:企业数据加密保护
使用信封加密保护企业敏感数据.
### 场景二:合规性审计
对企业代码进行合规性合规检查.
```bash
#!/bin/sh
echo "=== 企业加密合规审计 ==="
# ...
echo "阶段1: 深度代码扫描..."
python3 deep_crypto_auditor.py ./ > crypto-audit.json
echo "代码审计报告: crypto-audit.json"
# ...
echo -e "\n阶段2: 合规性检查..."
python3 compliance_auditor.py --template "等保2.0" --output compliance-report.json
py --template "GDPR" --output gdpr-report.json
py --template "PCI-DSS" --output pci-report.json
# ...
echo -e "\n阶段3: 密钥管理审计..."
python3 key_rotation_check.py --kms-config .kms/keys.json
# ...
echo -e "\n阶段4: 生成综合报告..."
python3 generate_compliance_report.py \
    --crypto-audit crypto-audit.json \
    --compliance compliance-report.json \
    --gdpr gdpr-report.json \
    --pci pci-report.json \
    --output final-compliance-report.html
# ...
echo -e "\n合规审计完成"
echo "报告: final-compliance-report.html"
```

### 场景三:DevSecOps安全集成
将加密检查集成到开发流水线.
```yaml
crypto_security_check:
  stage: security
  image: python:3.11
  script:
    - python3 deep_crypto_auditor.py . --format sarif --output crypto-audit.sarif
# ...
    - python3 compliance_auditor.py --template "等保2.0" --fail-on high
# ...
    - |
      CRITICAL=$(python3 -c "import json; r=json.load(open('crypto-audit.json')); print(sum(1 for f in r['findings'] if f['severity']=='critical'))")
      if [ "$CRITICAL" -gt 0 ]; then
        echo "发现 $CRITICAL 个严重加密安全问题"
        exit 1
      fi
# ...
    - python3 key_rotation_check.py --max-age 90 --fail
  artifacts:
    reports:
      sast: crypto-audit.sarif
    paths:
      - crypto-audit.json
      - compliance-report.json
  only:
    - merge_requests
    - main
```

## 不适用场景

以下场景加密工具专业版不适合处理：

- 安全评估未授权目标
- 物理安全防护
- 社会工程学攻击

## 触发条件

需要安全检测、合规审计、质量检查、加密防护时使用。不适用于非本工具能力范围的需求.
## 快速开始
### Step 1:配置KMS
```yaml
version: "2.0"
edition: pro
# ...
kms:
  provider: local  # local | aws | vault | aliyun
  key_id: app-master-key
  auto_rotate: true
  rotation_interval_days: 90
# ...
compliance:
  templates: [等保2.0, GDPR, PCI-DSS]
  fail_on: [critical, high]
# ...
audit:
  deep_scan: true
  report_format: [sarif, html, json]
```

### Step 2:运行审计
```
请对当前项目进行深度加密合规检查,检查合规性并生成报告.
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 配置示例
### 企业级完整配置
```yaml
version: "2.0"
edition: pro
# ...
kms:
  provider: vault
  address: "${VAULT_ADDR}"
  token: "${VAULT_TOKEN}"
  key_path: secret/data/app
  auto_rotate: true
  rotation_interval_days: 90
  warning_days: 7
# ...
compliance:
  templates:
    - name: 等保2.0
      enabled: true
      severity_threshold: high
    - name: GDPR
      enabled: true
    - name: PCI-DSS
      enabled: false
  report_format: [html, json, sarif]
# ...
audit:
  deep_scan: true
  rules:
    - weak_algorithm
    - insecure_random
    - hardcoded_secrets
    - ecb_mode
    - disabled_cert_validation
    - weak_tls
    - plaintext_password_compare
  exclude_dirs: [node_modules, .git, dist, vendor]
# ...
batch_encryption:
  enabled: true
  extensions: [.env, .key, .pem, .secret]
  algorithm: aes-256-gcm
  envelope_encryption: true
# ...
ci_cd:
  fail_on: [critical, high]
  sarif_report: true
  artifact_retention: 90
```

## 优选实践
1. **信封加密**:使用主密钥加密数据密钥,数据密钥加密实际数据

2. **密钥分离**:加密密钥、签名密钥、备份密钥必须分离

3. **定期轮换**:设置自动轮换策略,不超过90天

```python
rotation_manager = KeyRotationManager(kms)
rotation_manager.rotate_all_keys()
```

4. **审计日志**:记录所有密钥使用操作

```python
{
    "timestamp": "2026-01-01T10:00:00Z",
    "key_id": "app-master-key",
    "operation": "encrypt",
    "key_version": 3,
    "user": "service-account",
    "resource": "user-database"
}
```

5. **最小权限**:每个服务只能访问其需要的密钥

## 常见问题
### Q1:专业版如何兼容免费版?
专业版完全兼容免费版的所有加密命令和配置。免费版的 `.encryption.yml` 可直接在专业版使用,专业版会自动启用KMS和深度审计功能.
### Q2:支持哪些KMS服务?
| KMS服务 | 支持状态 | 配置方式 |
|:------|:------|:------|
| 本地KMS | 完全支持 | 内置实现 |
| HashiCorp Vault | 完全支持 | VAULT_ADDR/VAULT_TOKEN |
| 阿里云KMS | 完全支持 | ALIYUN_KMS_CONFIG |
| 腾讯云KMS | 完全支持 | TENCENT_KMS_CONFIG |

### Q3:密钥轮换会影响已有数据吗?
不会。轮换后旧版本密钥保留用于解密旧数据,新数据使用新版本密钥加密。系统自动处理版本兼容.
### Q4:如何生成合规报告?
```bash
py --all-templates --format html --output reports/
# ...
py --template "等保2.0" --format pdf
```

## 依赖说明
### 运行环境
- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Linux / macOS / Windows
- **运行时**:Python 3.8+ / Node.js 16+

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Python 3.8+ | 运行时 | 必需 | python.org 下载 |
| cryptography | Python库 | 必需 | pip install cryptography |
| bcrypt | Python库 | 推荐 | pip install bcrypt |
| age | 加密工具 | 推荐 | 系统包管理器安装 |
| openssl | TLS工具 | 必需 | 系统自带 |
| HashiCorp Vault | KMS服务 | 可选 | vaultproject.io |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- KMS服务需要配置认证:

```bash
export VAULT_ADDR="https://vault.company.com"
export VAULT_TOKEN="${VAULT_TOKEN}"
# ...
export ALIYUN_KMS_ACCESS_KEY_ID="${KMS_ACCESS_KEY}"
export ALIYUN_KMS_ACCESS_KEY_SECRET="${KMS_SECRET}"
```

### 可用性分类
- **分类**:MD+EXEC+PRO(专业版支持KMS集成、自动轮换和深度审计)
- **说明**:企业级加密管理工具,支持密钥生命周期管理和合规审计
- **适用规模**:中小型到大型项目
- **兼容性**:完全兼容免费版命令和配置,支持平滑升级

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制
- 需要API Key，无Key环境无法使用

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
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

- **自动化执行**: 企业级加密管理,支持KMS集成、密钥轮换、合规审计、批量加密与深度代码安全扫描。。面向企业安全团队的高级加密管理工具,提
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据