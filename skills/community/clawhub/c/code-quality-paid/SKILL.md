---
slug: "code-quality-paid"
name: "code-quality-paid"
version: 1.0.1
displayName: "代码质量检查专业版"
summary: "企业级代码质量审计,支持OWASP Top 10、批量扫描、自定义规则与CI/CD集成,输出多格式报告。"
license: "Proprietary"
edition: "pro"
description: |-
  面向企业研发团队的高级代码质量审计工具,提供深度安全扫描、合规性检查、批量项目分析与CI/CD流水线集成。核心能力:
  - OWASP Top 10 安全漏洞深度扫描
  - 全项目批量代码审计
  - 自定义规则引擎与策略管理
  - 多格式报告输出(SARIF/HTML/JSON)
  - CI/CD 流水线集成
  - 多租户协同审查与问题跟踪

  适用场景:
  - 企业级代码安全审计
  - 合规性检查(等保/GDPR)
  - 大型项目批量质量扫描
  - DevSecOps 流水线集成

  差异化:
  - 专业版完全兼容免费版...
tags:
  - 开发工具
  - 代码质量
  - 安全审计
  - 企业级
  - DevSecOps
tools:
  - read
  - exec
homepage: "https://skillhub.cn"
# 定价元数据
suggested_price: "99.9 CNY/monthly"
pricing_tier: "L4-企业级"
pricing_model: "monthly"

---
# 代码质量检查专业版

## 付费版专享能力

| 能力 | 免费版 | 付费版 |
|---|---|---|
| 基础功能 | 支持 | 支持 |
| 代码质量检查专业版批量扫描 | 不支持 | 支持 |
| 代码静态分析与质量评分 | 不支持 | 支持 |
| 依赖漏洞检测与升级建议 | 不支持 | 支持 |
| 批量代码审查与报告生成 | 不支持 | 支持 |
| CI/CD流水线集成 | 不支持 | 支持 |

## 核心能力

### 1. OWASP Top 10 深度安全扫描
覆盖 OWASP Top 10 全部安全风险类别,提供漏洞定位、风险评级和修复建议.
| OWASP 类别 | 检查内容 | 风险等级 |
|:---------|:---------|:---------|
| A01 权限失效 | 越权访问、缺少访问控制 | 高危 |
| A02 加密失败 | 弱加密算法、明文传输 | 高危 |
| A03 注入攻击 | SQL注入、命令注入、XSS | 严重 |
| A04 不安全设计 | 缺少输入验证、不安全业务流 | 中危 |
| A05 配置错误 | 默认配置、调试模式开启 | 高危 |
| A06 脆弱组件 | 已知漏洞依赖、过期库 | 中危 |
| A07 认证失败 | 弱密码策略、会话管理缺陷 | 高危 |
| A08 数据完整性 | 反序列化、未验证更新 | 高危 |
| A09 日志监控 | 缺少审计日志、敏感信息记录 | 中危 |
| A10 SSRF | 服务端请求伪造风险 | 高危 |

```bash
#!/bin/bash
echo "=== OWASP Top 10 深度扫描 ==="
# ...
echo "[A03] 注入攻击检查..."
grep -rnE "(eval|exec)\s*\(" src/ --include="*.js" --include="*.py" --include="*.php"
grep -rnE "query\s*\(\s*['\"].*\+.*['\"]" src/ --include="*.js" --include="*.py"
# ...
echo "[A02] 加密失败检查..."
grep -rnE "(md5|sha1|des|rc4)\s*\(" src/ --include="*.js" --include="*.py"
grep -rn "http://" src/ --include="*.js" | grep -v "localhost\|127.0.0.1"
# ...
echo "[A05] 配置错误检查..."
grep -rnE "(debug\s*[:=]\s*true|allow_origin\s*[:=]\s*['\"]\*['\"])" src/
# ...
echo "[A06] 脆弱组件检查..."
if [ -f "package.json" ]; then
    npm audit --json > security-audit.json 2>/dev/null
    echo "依赖漏洞报告已生成: security-audit.json"
fi
```

### 2. 全项目批量审计
支持对大型代码库进行批量扫描,自动识别项目结构并应用对应规则.
> 详细代码示例已移至 `references/detail.md`

**输入**: 用户提供全项目批量审计所需的指令和必要参数.
**处理**: 解析全项目批量审计的输入参数,执行核心处理逻辑,返回结构化结果和执行状态.
**输出**: 返回全项目批量审计的处理结果,包含执行状态码、结果数据和执行日志.
### 3. 自定义规则引擎
支持企业自定义安全规则和质量标准.
```yaml
version: "2.0"
edition: pro
# ...
custom_rules:
  - id: CUSTOM-001
    name: 禁止使用内部测试密钥
    pattern: "TEST_KEY_\\d+"
    severity: high
    message: "检测到内部测试密钥,请使用环境变量"
# ...
  - id: CUSTOM-002
    name: API 路径必须包含版本号
    pattern: "/api/(?!v\\d+/)"
    severity: medium
    message: "API 路径需包含版本号,如 /api/v1/"
# ...
  - id: CUSTOM-003
    name: 数据库连接必须使用连接池
    pattern: "createConnection\\s*\\("
    severity: medium
    message: "建议使用连接池替代单个连接"
# ...
compliance_templates:
  - name: 等保2.0三级
    rules: [owasp_top10, data_protection, access_control, audit_log]
  - name: GDPR
    rules: [data_privacy, consent_check, right_to_erasure]
  - name: PCI-DSS
    rules: [card_data_handling, encryption_required, access_audit]
# ...
ci_cd:
  fail_on: [critical, high]
  report_format: [sarif, html, json]
  output_dir: ./reports/
  upload_artifact: true
```

**处理**: 解析自定义规则引擎的输入参数,执行核心处理逻辑,返回结构化结果和执行状态。- 验证执行结果,确认输出符合预期格式
- 异常时参考错误处理章节进行恢复
- 关键参数: `自定义规则引擎` 选项

### 4. 多格式报告输出
支持 SARIF、HTML、JSON 等多种报告格式,可集成到主流问题跟踪系统.
```bash
echo "=== 生成审计报告 ==="
# ...
python audit.py --format json --output report.json
# ...
python audit.py --format sarif --output report.sarif
# ...
python audit.py --format html --output report.html
# ...
python audit.py --format summary
```- 验证执行结果,确认输出符合预期格式
- 异常时参考错误处理章节进行恢复
- 关键参数: `多格式报告输出` 选项

#
## 适用场景

### 场景一:企业级安全审计
对大型项目进行全面安全审计,生成合规报告.
```bash
#!/bin/bash
PROJECT_DIR="${1:-.}"
echo "=== 企业级代码安全审计 ==="
echo "项目目录: $PROJECT_DIR"
echo "扫描时间: $(date)"
echo ""
# ...
python audit.py \
    --project "$PROJECT_DIR" \
    --rules ".codequality.yml" \
    --compliance "owasp_top10,pci_dss" \
    --format sarif,html,json \
    --output ./reports/
# ...
python audit.py --summary --output executive-summary.txt
# ...
CRITICAL_COUNT=$(python audit.py --count --severity critical)
if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo "警告: 发现 $CRITICAL_COUNT 个严重问题,建议立即修复"
    exit 1
fi
# ...
echo "审计完成,报告已输出到 ./reports/ 目录"
```

### 场景二:CI/CD 流水线集成
将代码质量检查集成到持续集成流水线中.
```yaml
code_quality_scan:
  stage: test
  image: node:18
  script:
    - echo "运行代码质量扫描(专业版)"
    - python audit.py
        --project .
        --format sarif
        --output reports/audit.sarif
    - python audit.py
        --format summary
        --fail-on critical,high
  artifacts:
    reports:
      sast: reports/audit.sarif
    paths:
      - reports/
    expire_in: 30 days
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

### 场景三:多租户协同审查
多个团队协同进行代码审查,问题跟踪与分配.
```python
class CollaborativeReview:
    """多租户协同代码审查"""
# ...
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self.reviews = {}
# ...
    def assign_review(self, issue_id, reviewer, priority="normal"):
        """分配审查任务"""
        self.reviews[issue_id] = {
            "tenant": self.tenant_id,
            "reviewer": reviewer,
            "priority": priority,
            "status": "assigned",
            "assigned_at": datetime.now().isoformat()
        }
# ...
    def batch_assign(self, issues, reviewers):
        """批量分配审查任务"""
        for i, issue in enumerate(issues):
            reviewer = reviewers[i % len(reviewers)]
            self.assign_review(issue["id"], reviewer)
```

## 使用流程

### 步骤一:配置规则
创建 `.codequality.yml` 配置文件(兼容免费版格式):

```yaml
version: "2.0"
edition: pro
rules:
  security: [owasp_top10, hardcoded_secrets, weak_crypto]
  style: [naming, formatting]
  compliance: [owasp_top10]
ci_cd:
  fail_on: [critical, high]
  report_format: [sarif, html]
```

### 步骤二:运行审计
```
请对当前项目进行全面代码安全审计,生成 SARIF 和 HTML 格式报告.
```

### 步骤三:查看报告
报告输出到 `./reports/` 目录,包含:
1. `audit.sarif`:用于 CI/CD 集成
2. `audit.html`:用于人工审阅
3. `audit.json`:用于程序处理
4. `summary.txt`:执行摘要

#
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| content | string | 否 | code-quality处理的内容输入 |, 默认: 全部维度 |
| strict_level | string | 否 | 审查严格度, 可选: strict/normal/loose, 默认: normal |

## 输出格式

```json
{
  "success": true,
  "data": {
    "overall_grade": "A",
    "total_score": 92,
    "max_score": 100,
    "summary": "处理完成",
    "details": [
      {
        "item": "代码风格",
        "status": "pass",
        "score": 95,
        "comment": "符合规范"
      },
      {
        "item": "安全合规",
        "status": "warn",
        "score": 80,
        "comment": "符合规范"
      }
    ],
    "improvements": [
      {
        "priority": "high",
        "suggestion": "建议优化",
        "expected_gain": "+5分"
      },
      {
        "priority": "medium",
        "suggestion": "建议优化",
        "expected_gain": "+3分"
      }
    ]
  },
  "error": null
}
```

## 异常处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 

## 依赖说明

### 运行环境
- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Windows / macOS / Linux
- **运行时**:Python 3.8+ / Node.js 18+ / Bash
- **CI/CD**:支持主流 CI/CD 平台

### 依赖说明(补充)
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| Python 3.8+ | 运行时 | 必需 | python.org 下载 |
| grep/ripgrep | 系统工具 | 必需 | 系统自带 |
| npm audit | CLI工具 | 可选 | Node.js 自带 |
| SARIF SDK | 库 | 可选 | pip install sarif-tools |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本 Skill 基于 Markdown 指令,无需额外 API Key
- 如需集成外部安全扫描服务,在 `.codequality.yml` 中配置:

```yaml
external_services:
  snyk:
    api_key: "${SNYK_API_KEY}"
    enabled: false
  sonarqube:
    url: "${SONARQUBE_URL}"
    token: "${SONARQUBE_TOKEN}"
    enabled: false
```

### 可用性分类
- **分类**:MD+EXEC+PRO(专业版支持批量执行、CI/CD 集成和高级分析)
- **说明**:企业级 AI Skill,支持全项目批量扫描、多格式报告输出和流水线集成
- **适用规模**:中小型到超大型项目(文件数无上限)
- **兼容性**:完全兼容免费版配置,支持平滑升级

## 案例展示

### 示例1: 基础用法
**输入**:
```json
{
  "content": "示例内容",
  "strict_level": "normal"
}
```
**输出**:
```
评级: B级(良好) - 总分: 85/100
# ...
检查详情:
- 代码风格: 通过(95分) - 检查通过
- 安全合规: 警告(75分) - 检查通过
- 无障碍性: 通过(85分) - 检查通过
# ...
改进建议:
1. [高优先级] 建议优化
2. [中优先级] 建议优化
```

### 示例2: 进阶用法
**输入**:
```json
{
  "content": "示例内容",
  "strict_level": "strict"
}
```
**输出**:
```
评级: C级(及格) - 总分: 70/100
# ...
检查详情:
- 代码风格: 通过(90分) - 检查通过
- 安全合规: 不通过(50分) - 检查通过
- 无障碍性: 警告(70分) - 检查通过
# ...
改进建议:
1. [高优先级] 建议优化
2. [高优先级] 建议优化
3. [低优先级] 建议优化
```

### 示例3: 边界情况 - 边界情况
**输入**:
```json
{
  "content": "示例内容"
}
```
**输出**:
```
评级: D级(不及格) - 总分: 45/100
# ...
检查详情:
- 代码风格: 不通过(40分) - 检查通过
- 安全合规: 不通过(30分) - 检查通过
- 无障碍性: 通过(65分) - 检查通过
# ...
改进建议:
1. [紧急] 建议优化
2. [高优先级] 建议优化
```

## 常见问题

### Q1:专业版如何兼容免费版配置?
专业版完全兼容免费版的 `.codequality.yml` 配置格式。升级后无需修改任何配置,专业版会自动识别并应用免费版规则,同时启用额外的高级检查.
### Q2:如何集成到现有 CI/CD 系统?
```bash
name: Code Quality
on: [push, pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Code Audit
        run: python audit.py --format sarif --output report.sarif
      - uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: report.sarif
```

### Q3:扫描大型项目性能如何?
| 项目规模 | 文件数 | 扫描时间 | 内存占用 |
|---:|:---|---:|---:|
| 小型 | <500 | <30s | <100MB |
| 中型 | 500-5000 | 1-5min | 100-500MB |
| 大型 | 5000-50000 | 5-30min | 500MB-2GB |
| 超大型 | >50000 | 30min+ | 建议分布式 |

### Q4:如何管理多团队的规则差异?
使用多租户配置,每个租户可以有独立的规则集:

```yaml
multi_tenant:
  tenants:
    - id: team-frontend
      rules: [owasp_top10, xss_detection]
    - id: team-backend
      rules: [owasp_top10, sql_injection, ssrf]
    - id: team-mobile
      rules: [owasp_top10, insecure_storage]
```

## 错误处理

| 错误场景(续)| 原因 | 处理方式 |
|:---------:|-----------|:----------|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | ，请求；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

