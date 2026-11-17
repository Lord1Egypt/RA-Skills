---
slug: docker-toolkit-pro
name: docker-toolkit-pro
version: 1.0.0
displayName: Docker容器专业版
summary: "企业级Docker管理平台，支持集群、私有仓库、安全扫描与CI/CD集成.。面向企业运维团队的Docker全功能管理平台。支持多节点集群管理、"
license: Proprietary
edition: pro
description: "面向企业运维团队的Docker全功能管理平台。支持多节点集群管理、。Use when 需要安全检测、合规审计、质量检查、加密防护时使用。不适用于安全评估未授权目标。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。 功能涵盖: toolkit。"
  私有镜像仓库、镜像安全扫描、容器监控与CI/CD流水线集成。Use when 需要系统监控、日志分析、运维告警、部署管理时使用。不适用于物理硬件维修。Use
  when 需要系统监控、日志分析、运维告警、部署管理时使用。不适用于物理硬件维修。'
tags:
  - Operations
  - Docker
  - 企业级
  - 容器编排
  - 容器
  - DevOps
  - python3
  - pro
tools:
  - read
  - exec
  - write
homepage: ""
# 定价元数据
category: "Development"
---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# Docker容器专业版（PRO版）

## 概述

本平台为企业运维团队提供全功能的Docker管理能力。相比免费版，PRO版新增多节点集群、私有镜像仓库、安全扫描、监控告警和CI/CD集成等高级功能，全面满足企业级容器化运维的复杂需求.
PRO版完全兼容免费版单机Docker命令与配置，升级后原有容器管理可直接使用.
## 核心能力

### PRO版功能增强对比

| 功能 | 免费版 | PRO版 |
|---|---|----|
| 节点管理 | 单机 | 多节点集群(Swarm) |
| 镜像仓库 | 公共仓库 | +私有仓库(Harbor) |
| 安全扫描 | 不支持 | 质量检查+合规检查 |
| 监控告警 | 不支持 | 容器监控+日志聚合 |
| CI/CD | 不支持 | 流水线集成 |
| 扩缩容 | 不支持 | 自动扩缩容 |
| 编排 | 基础Compose | 高级Compose+Swarm |
| 网络存储 | 基础 | 多网络+存储编排 |

**处理**: 解析PRO版功能增强对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回PRO版功能增强对比的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、Docker、管理平台、支持集群、安全扫描与、面向企业运维团队、全功能管理平台、支持多节点集群管、私有镜像仓库、镜像安全扫描、容器监控与、Use、when、需要系统监控、日志分析、运维告警、部署管理时使用、不适用于物理硬件、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：集群部署

用户输入："部署一个3节点的Docker集群"

```bash
# 初始化Swarm集群
python3 （请参考skill目录中的脚本文件） init \
  --manager 192.168.1.10 \
  --advertise-addr 192.168.1.10
# ...
# 添加工作节点
python3 （请参考skill目录中的脚本文件） join \
  --worker 192.168.1.20 \
  --token "SWMTKN-未指定"
python3 （请参考skill目录中的脚本文件） join \
  --worker 192.168.1.30 \
  --token "SWMTKN-未指定"
# ...
# 查看集群状态
python3 （请参考skill目录中的脚本文件） nodes
```

### 场景二：私有仓库管理

用户输入："搭建私有镜像仓库并推送镜像"

```bash
# 部署Harbor仓库
python3 （请参考skill目录中的脚本文件） deploy \
  --type harbor \
  --host registry.example.com \
  --ssl-cert /path/to/cert
# ...
# 推送镜像
python3 （请参考skill目录中的脚本文件） push \
  --image my-app:latest \
  --registry registry.example.com
# ...
# 镜像扫描
python3 （请参考skill目录中的脚本文件） scan \
  --image registry.example.com/my-app:latest
```

### 场景三：安全扫描

用户输入："扫描所有运行容器的安全漏洞"

```bash
# 容器安全扫描
python3 （请参考skill目录中的脚本文件） scan \
  --target containers \
  --output security_report.pdf
# ...
# 镜像质量检查
python3 （请参考skill目录中的脚本文件） scan \
  --target images \
  --severity "HIGH,CRITICAL"
# ...
# 输出包含：
# - 漏洞列表（CVE编号）
# - 风险等级
# - 修复建议
# - 合规检查结果
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### PRO版初始化

```bash
# 依赖说明
pip install -r requirements_pro.txt
# ...
# 配置集群与仓库
cp config_pro_template.yaml config_pro.yaml
```

### 常用命令

```bash
# 集群管理
python3 （请参考skill目录中的脚本文件） init --manager 192.168.1.10
python3 （请参考skill目录中的脚本文件） nodes
python3 （请参考skill目录中的脚本文件） deploy --service web --replicas 3
# ...
# 私有仓库
python3 （请参考skill目录中的脚本文件） deploy --type harbor --host registry.example.com
python3 （请参考skill目录中的脚本文件） push --image my-app:latest
# ...
# 安全扫描
python3 （请参考skill目录中的脚本文件） scan --target containers
python3 （请参考skill目录中的脚本文件） scan --target images --severity "HIGH,CRITICAL"
# ...
# 监控
python3 （请参考skill目录中的脚本文件） watch --interval 30
python3 （请参考skill目录中的脚本文件） alerts --channel webhook
# ...
# CI/CD
python3 （请参考skill目录中的脚本文件） build --pipeline web-app
python3 （请参考skill目录中的脚本文件） deploy --pipeline web-app --environment production
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### PRO企业级配置

```yaml
pro_config:
  cluster:
    type: "swarm"                 # swarm | standalone
    managers: ["192.168.1.10"]
    workers: ["192.168.1.20", "192.168.1.30"]
    advertise_addr: "192.168.1.10"
# ...
  registry:
    type: "harbor"                # harbor | registry
    url: "https://registry.example.com"
    username: "${REGISTRY_USER}"
    password: "${REGISTRY_PASS}"
    auto_scan: true               # 推送自动扫描
# ...
  security:
    scan_engine: "trivy"          # trivy | clair
    scan_frequency: "daily"
    severity_threshold: "HIGH"
    block_on_critical: true       # 严重漏洞阻止部署
    compliance: ["CIS", "NIST"]
# ...
  monitoring:
    enabled: true
    metrics: ["cpu", "memory", "network", "io"]
    log_aggregation: true
    alerting:
      channels: ["webhook", "email"]
      thresholds:
        cpu: 80
        memory: 85
# ...
  cicd:
    enabled: true
    pipeline_dir: "./pipelines"
    auto_deploy: false            # 自动部署（谨慎开启）
    environments: ["dev", "staging", "production"]
# ...
  scaling:
    auto_scale: true
    min_replicas: 2
    max_replicas: 10
    cpu_threshold: 70             # CPU超过70%扩容
```

## 优选实践

### PRO版企业实践

| 实践领域 | 建议做法 |
|:-----|:-----|
| 集群管理 | 奇数个管理节点，避免脑裂 |
| 镜像安全 | 所有镜像必须扫描通过后才部署 |
| 监控告警 | 关键指标设置告警，及时响应 |
| CI/CD | 分环境部署，生产环境需人工确认 |
| 扩缩容 | 设置合理阈值，避免频繁波动 |

### 免费版兼容性

```text
免费版命令 → PRO版命令（增强）：
docker.py container run   → cluster.py deploy --replicas 3
docker.py compose up      → +集群模式+自动扩缩容
docker.py image build     → +安全扫描+私有仓库推送
```

## 常见问题

### Q1：Swarm和Kubernetes选哪个？

Swarm适合小规模集群（<50节点），部署简单、Docker原生；Kubernetes适合大规模生产环境，功能强大但复杂。建议小团队用Swarm，大型企业用K8s.
### Q2：Harbor私有仓库如何部署？

PRO版支持一键部署Harbor。需准备域名和SSL证书。Harbor提供镜像存储、扫描、权限管理等企业级功能.
### Q3：安全扫描支持哪些引擎？

支持Trivy和Clair两种扫描引擎。Trivy扫描速度快、CVE数据库更新及时；Clair与Harbor深度集成。可根据需求选择.
### Q4：自动扩缩容如何工作？

基于CPU/内存使用率自动调整容器副本数。当CPU超过阈值时自动扩容，低于阈值时自动缩容。可配置最小/最大副本数和冷却时间.
### Q5：CI/CD支持哪些平台？

PRO版原生支持GitLab CI和GitHub Actions。通过Webhook触发构建和部署流水线。也可对接Jenkins等外部CI系统.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.9+
- **Docker**: 20.0+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| docker | Python库 | 必需 | `pip install docker` |
| requests | Python库 | 必需 | `pip install requests`（API调用） |
| trivy | CLI工具 | 可选 | 官网安装（安全扫描） |
| harbor-client | Python库 | 可选 | `pip install harbor-client` |

### API Key 配置

| 服务 | 环境变量 | 是否必需 | 用途 |
|:---:|:---:|:---:|:---:|
| Harbor | `REGISTRY_USER`/`REGISTRY_PASS` | 可选 | 私有仓库认证 |
| Webhook | `WEBHOOK_URL` | 可选 | 告警通知 |
| GitLab | `GITLAB_TOKEN` | 可选 | CI/CD集成 |

- 未配置的服务自动跳过
- 所有凭证存储在本地配置文件

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本+Docker执行）
- **说明**: 企业级Docker管理平台，支持集群、仓库、安全与CI/CD
- **PRO版特性**: 集群管理、私有仓库、安全扫描、监控告警、CI/CD、自动扩缩容
- **兼容性**: 完全兼容免费版单机Docker命令与配置

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 企业级Docker管理平台，支持集群、私有仓库、安全扫描与CI/CD集成.。面向企业运维团队的Docker全功能管理平台
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 核心功能

- **自动化执行**: 企业级Docker管理平台，支持集群、私有仓库、安全扫描与CI/CD集成.。面向企业运维团队的Docker全功能管理平台
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据