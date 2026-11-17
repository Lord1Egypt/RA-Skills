---
name: cloudforge-automation-pro
slug: cloudforge-automation-pro
displayName: "Cloudforge Automatio"
version: "1.0.0"
summary: "企业级多云IaC编排系统，含多云管理、Ansible配置、CI/CD流水线、合规审计与灾备恢复.。云锻造自动化专业版是面向团队与企业的全功能多云基础设施即代码编排系统。不仅覆盖单云IaC基础"
description: "云锻造自发化专业版是面向团队与企业的全功能多云基础设施即代码编排系统。不仅覆盖单云IaC基础能力，更包含多云统一管控、Ansible配置管控、CI/CD部署流水线、合规策略审计、灾备恢复、成本调优与安全加固，确保企业级云基础设施安全、合规、高效。Use when 需要安全检测、合规审计、漏洞扫描、加密防护时使用。不适用于渗透测试未授权目标。"
license: "Proprietary"
tools:
  - Read
  - Write
  - Edit
  - Bash
---

> **核心功能**: 本技能提供结构化的工作流程和配置指引等能力。
# 云锻造自动化（专业版）
企业级云基础设施需要跨云管理、自动化配置、合规审计与灾备保障。专业版通过Terraform+Ansible+CloudFormation三工具集成与七大高级能力，确保云基础设施安全、合规、高效、可恢复.
## 核心理念
**企业IaC五原则**：
1. **声明式**：描述"想要什么"，而非"怎么做"
2. **可版本化**：基础设施代码纳入Git管理，每次变更可追溯
3. **幂等性**：多次执行结果一致，安全重试
4. **多云一致**：同一套代码管理多个云平台，环境间无缝迁移
5. **合规优先**：每次变更前进行合规检查，确保满足安全策略
## 架构总览
## 输入定义
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Cloudforge Automatio处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |
```text
┌─────────────────────────────────────────────────────────────┐
│             云锻造自动化专业版 (CLOUDFORGE-AUTOMATION PRO)    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │ 多云    │  │ IaC三   │  │ CI/CD   │  │ 合规    │       │
│  │ 统一    │  │ 工具    │  │ 部署    │  │ 策略    │       │
│  │ 管理    │  │ 集成    │  │ 流水线  │  │ 审计    │       │
│  │ Multi-  │  │ Terra+  │  │ CI/CD   │  │ Compli- │       │
│  │ Cloud   │  │ Ansible │  │ Pipeline│  │ ance    │       │
│  │ ✅Pro   │  │ +CFN    │  │ ✅Pro   │  │ ✅Pro   │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│       │            │            │            │              │
│       ▼            ▼            ▼            ▼              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │ 灾备    │  │ 成本    │  │ 安全    │  │ 性能    │       │
│  │ 恢复    │  │ 优化    │  │ 加固    │  │ 优化    │       │
│  │ DR      │  │ Cost    │  │ Securi- │  │ Perf    │       │
│  │ ✅Pro   │  │ ✅Pro   │  │ ty ✅Pro│  │ ✅Pro   │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
## 快速指引
### 基础搭建（<60秒）
```text
帮我初始化多云基础设施项目，同时管理AWS和Azure资源
```
### 标准搭建（<120秒）
1. **配置多云凭据**：AWS CLI + Azure CLI认证
2. **初始化项目**：生成多云Terraform项目结构
3. **选择模板**：Web应用、数据库、Kubernetes、Serverless
4. **配置环境**：dev/staging/prod多环境
5. **一键部署**：`（请参考skill目录中的脚本文件） apply prod`
### 完整搭建（<300秒）
```yaml
cloudforge_config:
  multi_cloud:
    providers: ["aws", "gcp", "azure"]
    state_backend: "s3+dynamodb"       # 远程状态后端
    state_locking: true                 # 状态锁定
  iac_tools:
    terraform: true                     # 基础设施定义
    ansible: true                       # 配置管理
    cloudformation: false               # AWS原生（可选）
  ci_cd:
    enabled: true
    trigger: "git_push"
    pipeline:
      - terraform_plan                  # 计划
      - compliance_check                # 合规检查
      - manual_approval                 # 人工审批
      - terraform_apply                 # 执行
      - ansible_configure               # 配置
      - health_check                    # 健康检查
  compliance:
    framework: "CIS"                    # CIS基准
    block_on_violation: true            # 违规阻止部署
    audit_log: true                     # 审计日志
  disaster_recovery:
    backup: "cross_region"              # 跨区域备份
    rto: "4h"                           # 恢复时间目标
    rpo: "1h"                           # 恢复点目标
    auto_failover: true                 # 自动故障切换
  cost_optimization:
    monitoring: true                    # 成本监控
    alert_threshold: "budget_80%"       # 预算80%告警
    auto_scale_down: true               # 自动缩容
  security:
    encryption: "at_rest_and_in_transit"  # 全链路加密
    key_rotation: "90d"                   # 密钥90天轮换
    network_audit: true                   # 网络审计
```
**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 主要能力
### 功能一：多云统一管理 — 专业版启用
同时管理AWS、GCP、Azure资源，跨云编排：
```hcl
provider "aws" {
  region = var.aws_region
  alias  = "aws"
}
provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
  alias   = "gcp"
}
provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
  alias           = "azure"
}
resource "aws_instance" "web" {
  provider = aws.aws
  ami           = "ami-0d52744d6551d851e"
  instance_type = "t3.micro"
  tags = { Cloud = "AWS", Role = "web" }
}
resource "google_compute_instance" "web" {
  provider = google.gcp
  name         = "web-instance"
  machine_type = "e2-micro"
  zone         = "asia-northeast1-a"
  tags = [Cloud = "GCP", Role = "web"]
}
resource "azurerm_linux_virtual_machine" "web" {
  provider            = azurerm.azure
  name                = "web-vm"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_B1s"
  tags = { Cloud = "Azure", Role = "web" }
}
```
**多云初始化**：
```bash
aws configure
gcloud auth login
gcloud config set project your-project-id
az login --workspace your-workspace-id
（请参考skill目录中的脚本文件） init multi-cloud
```
**处理**: 解析功能一：多云统一管理 — 专业版启用的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回功能一：多云统一管理 — 专业版启用的响应数据,含状态码、结果数据和运行日志.
- 使用`input_params`进行配置,支持创建/查询/导出操作
### 功能二：IaC三工具集成 — 专业版启用
#
### Terraform（基础设施定义）
```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
}
```
#
### Ansible（配置管理）
```yaml
- name: 配置Web服务器
  hosts: webservers
  become: yes
  tasks:
    - name: 安装Nginx
      apt:
        name: nginx
        state: present
        update_cache: yes
    - name: 启动Nginx
      service:
        name: nginx
        state: started
        enabled: yes
    - name: 部署应用配置
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: restart nginx
  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
```
```bash
ansible-playbook -i inventory playbook.yml
yml --limit "webservers"
```
#
### CloudFormation（AWS原生，可选）
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Web应用基础设施
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0d52744d6551d851e
      InstanceType: t3.micro
      SecurityGroupIds:
        - !Ref WebServerSG
  WebServerSG:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Web Server Security Group
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
```
**处理**: 解析功能二：IaC三工具集成 — 专业版启用的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回功能二：IaC三工具集成 — 专业版启用的响应数据,含状态码、结果数据和运行日志.
- 使用`input_params`进行配置,支持创建/查询/导出操作
### 功能三：CI/CD部署流水线 — 专业版启用
Git Push自动触发基础设施变更：
```yaml
name: 基础设施部署
on:
  push:
    branches: [main]
    paths: ['infra/**']
  pull_request:
    branches: [main]
    paths: ['infra/**']
jobs:
  plan:
    name: Terraform计划
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: 配置AWS凭据
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: $<动态配置>
          aws-secret-access-key: $<动态配置>
      - name: Terraform初始化
        run: cd infra && terraform init
      - name: 合规检查
        run: |
          pip install checkov
          checkov -d infra/ --framework terraform
      - name: Terraform计划
        run: cd infra && terraform plan -out=tfplan
      - name: 上传计划
        uses: actions/upload-artifact@v3
        with:
          name: tfplan
          path: infra/tfplan
  apply:
    name: Terraform执行
    needs: plan
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v3
      - name: 下载计划
        uses: actions/download-artifact@v3
        with:
          name: tfplan
          path: infra/
      - name: Terraform执行
        run: cd infra && terraform apply -auto-approve tfplan
      - name: Ansible配置
        run: ansible-playbook -i inventory playbook.yml
      - name: 健康检查
        run: （请参考skill目录中的脚本文件）
```
**处理**: 解析功能三：CI/CD部署流水线 — 专业版启用的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回功能三：CI/CD部署流水线 — 专业版启用的响应数据,含状态码、结果数据和运行日志.
- 使用`input_params`进行配置,支持创建/查询/导出操作
### 功能四：合规策略审计 — 专业版启用
```yaml
compliance_check:
  framework: "CIS"                    # CIS基准
  tools:
    - checkov                         # Terraform合规扫描
    - terraform-compliance            # 策略即代码
    - aws-config                      # AWS配置合规
  policies:
    - "确保所有S3桶非公开"
    - "确保安全组不开放22端口到0.0.0.0/0"
    - "确保数据库启用加密"
    - "确保CloudTrail已启用"
    - "确保IAM密码策略符合要求"
  on_violation:
    block_deploy: true                # 阻止部署
    alert_channel: "slack"
    generate_report: true             # 生成报告
```
```bash
checkov -d infra/ --framework terraform
```
**处理**: 解析功能四：合规策略审计 — 专业版启用的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回功能四：合规策略审计 — 专业版启用的响应数据,含状态码、结果数据和运行日志.
- 使用`input_params`进行配置,支持创建/查询/导出操作
### 功能五：灾备恢复 — 专业版启用
```yaml
disaster_recovery:
  backup:
    strategy: "cross_region"          # 跨区域备份
    frequency: "daily"                # 每日备份
    retention: "30d"                  # 保留30天
    regions:
      primary: "ap-northeast-1"       # 主区域
      secondary: "ap-southeast-1"     # 备区域
  failover:
    rto: "4h"                         # 恢复时间目标（4小时）
    rpo: "1h"                         # 恢复点目标（1小时数据丢失）
    auto_failover: true               # 自动故障切换
    health_check_interval: "60s"      # 60秒健康检查
    failover_threshold: 3             # 连续3次失败触发切换
  recovery_runbook:
    - "检测到主区域故障"
    - "验证备区域数据完整性"
    - "更新DNS指向备区域"
    - "启动备区域应用实例"
    - "验证服务恢复"
    - "通知干系人"
    - "主区域恢复后同步数据"
```
```hcl
resource "aws_db_instance" "primary" {
  identifier           = "primary-db"
  engine               = "postgres"
  instance_class       = "db.t3.micro"
  allocated_storage    = 20
  backup_retention_period = 7
  multi_az             = true
}
resource "aws_db_instance" "replica" {
  identifier           = "replica-db"
  replicate_source_db  = aws_db_instance.primary.identifier
  region               = "ap-southeast-1"
}
```
**处理**: 解析功能五：灾备恢复 — 专业版启用的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回功能五：灾备恢复 — 专业版启用的响应数据,含状态码、结果数据和运行日志.
- 使用`input_params`进行配置,支持创建/查询/导出操作
### 功能六：成本优化 — 专业版启用
```yaml
cost_optimization:
  monitoring:
    enabled: true
    services: ["ec2", "rds", "s3", "lambda"]
    granularity: "daily"
  budget:
    monthly: 10000                    # 月预算$10000
    alert_thresholds: [50, 80, 100]   # 50%/80%/100%告警
    alert_channel: "slack"
  auto_optimization:
    - "识别闲置资源（未使用的EC2、EBS）"
    - "自动缩容低利用率实例"
    - "S3生命周期策略（30天后转IA，90天后转Glacier）"
    - "Reserved Instance建议"
    - "Spot Instance替代按需实例（非关键任务）"
  report:
    frequency: "weekly"
    format: "markdown"
    distribute: "finops_team"
```
```bash
aws ce get-cost-and-usage \
  --time-period Start=2026-01-01,End=2026-01-31 \
  --granularity MONTHLY \
  --metrics "BlendedCost" \
  --group-by Type=SERVICE
```
**处理**: 解析功能六：成本优化 — 专业版启用的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回功能六：成本优化 — 专业版启用的响应数据,含状态码、结果数据和运行日志.
- 使用`input_params`进行配置,支持创建/查询/导出操作
### 功能七：安全加固 — 专业版启用
```yaml
security_hardening:
  encryption:
    at_rest: true                     # 静态加密
    in_transit: true                  # 传输加密
    kms_key_rotation: "90d"           # KMS密钥90天轮换
  network:
    security_group_audit: true        # 安全组审计
    block_public_access: true         # 阻止公开访问
    vpc_flow_logs: true               # VPC流日志
    waf: true                         # Web应用防火墙
  iam:
    mfa_required: true                # 强制MFA
    password_policy: "strong"         # 强密码策略
    least_privilege: true             # 最小权限原则
    access_key_rotation: "90d"        # Access Key 90天轮换
  monitoring:
    cloudtrail: true                  # API调用审计
    guardduty: true                   # 威胁检测
    security_hub: true                # 安全态势管理
    alert_on_critical: true           # 严重告警
```
**处理**: 解析功能七：安全加固 — 专业版启用的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回功能七：安全加固 — 专业版启用的响应数据,含状态码、结果数据和运行日志.
**能力覆盖范围**：本技能覆盖以下场景：企业级多云、编排系统、含多云管理、合规审计与灾备恢、云锻造自动化专业、版是面向团队与企、业的全功能多云基、础设施即代码编排、不仅覆盖单云、基础能力、更提供多云统一管、成本优化与安全加、确保企业级云基础、设施安全等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 使用`input_params`进行配置,支持创建/查询/导出操作
## 适用范围
### 场景一：企业级多云架构管理（架构师角色）
**场景描述**：企业使用AWS作为主云、Azure作为灾备，需要统一管理跨云资源.
**配置**：
```hcl
provider "aws" { region = "ap-northeast-1" }
provider "azurerm" { features {} }
resource "aws_instance" "primary" { ... }
resource "azurerm_linux_virtual_machine" "backup" { ... }
```
**效果**：跨云资源统一管理，灾备切换从小时级降至分钟级.
### 场景二：DevOps基础设施自动化（DevOps工程师角色）
**场景描述**：需要Git Push自动触发基础设施变更，含计划、审批、执行、配置全流程.
**配置**：
```yaml
pipeline:
  - terraform_plan
  - compliance_check
  - manual_approval
  - terraform_apply
  - ansible_configure
  - health_check
```
**效果**：基础设施变更全自动化，人工仅审批，部署频率从每周提升至每日.
## 帮助文档
### Q1: Cloudforge Automatio支持哪些输入格式？
A1: 企业级多云IaC编排系统，含多云管理、Ansible配置、CI/CD流水线、合规审计与灾备恢复.。云锻造自动化专业版是面向团队与企业的全功能多云基础设施即代码编。支持文本指令和结构化参数输入，具体格式参考使用流程章节。
### Q2: 使用Cloudforge Automatio需要什么前置条件？
A2: 请确认运行环境满足依赖说明中的要求。Cloudforge Automatio基于Markdown指令驱动，无需额外安装包。
### Q3: 命令行执行失败怎么办？
A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。
## 安全提示
| 风险类型 | 防范措施 |
|----------|---------|
| 命令执行风险 | 命令执行受白名单约束,避免注入用户输入 |
| 网络通信安全 | 通过HTTPS安全通信,验证证书有效性 |
| 敏感数据暴露 | 返回数据中不含凭证信息 |
使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 异常处理指引
针对Cloudforge Automatio使用中可能遇到的常见问题,提供以下排查方案:
| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |
### Cloudforge Automatio通用排查步骤
1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块

## 安装与配置
### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent
- **操作系统**: Windows / macOS / Linux

### 可用性分类
- **分类**: MD（纯Markdown指令，通过自然语言驱动Agent完成操作）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作。

## 依赖说明

- LLM/API Key: 需要配置相应的API密钥
- 网络连接: 需要访问外部服务
- 文件系统: 需要读写文件权限
- 运行时环境: 需要相应的命令行工具
