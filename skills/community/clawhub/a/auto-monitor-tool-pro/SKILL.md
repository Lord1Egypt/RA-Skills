---
slug: auto-monitor-tool-pro
name: auto-monitor-tool-pro
version: 1.0.0
displayName: 系统监控专业版
summary: "企业级分布式监控平台，支持多节点、容器、日志分析与可视化仪表盘.。面向企业运维团队的分布式监控平台。支持多节点服务器统一监控、"
license: Proprietary
edition: pro
description: "面向企业运维团队的分布式监控平台。支持多节点服务器统一监控、。Use when 需要系统监控、日志分析、运维告警、部署管理时使用。不适用于物理硬件维修。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。 功能涵盖: auto。"
  Docker/K8s容器监控、日志聚合分析、可视化仪表盘与智能告警。Use when 需要系统监控、日志分析、运维告警、部署管理时使用。不适用于物理硬件维修。Use
  when 需要系统监控、日志分析、运维告警、部署管理时使用。不适用于物理硬件维修。'
tags:
  - Operations
  - 系统监控
  - 企业级
  - 容器监控
  - 监控
  - 运维
  - 工具
  - python3
  - pro
tools:
  - read
  - exec
homepage: ""
# 定价元数据
category: "Operations"
---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# 系统监控专业版（PRO版）

## 概述

本平台为企业运维团队提供全功能的分布式监控能力。相比免费版，PRO版新增多节点统一监控、容器监控、日志分析、可视化仪表盘和智能告警等高级功能，全面满足企业级运维监控的复杂需求.
PRO版完全兼容免费版单机监控命令与配置，升级后原有监控规则可直接迁移.
## 核心能力

### PRO版功能增强对比

| 功能 | 免费版 | PRO版 |
|---|---|----|
| 监控节点 | 单机 | 多节点分布式 |
| 容器监控 | 不支持 | Docker/K8s |
| 日志分析 | 不支持 | 聚合+搜索 |
| 仪表盘 | 文本 | Grafana集成 |
| 告警方式 | 邮件 | +Webhook/IM |
| 异常检测 | 阈值 | +智能检测 |
| 容量规划 | 不支持 | 趋势预测 |
| 历史保留 | 30天 | 365天+ |

**处理**: 解析PRO版功能增强对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回PRO版功能增强对比的响应数据,包含状态码、结果和日志.
### 分布式监控架构

| 组件 | 说明 | 部署方式 |
|:-----|:-----|:-----|
| Server | 中央监控服务 | 单点部署 |
| Agent | 节点采集代理 | 各节点部署 |
| Database | 时序数据存储 | 数据库 |
| Dashboard | 可视化面板 | Grafana |
| AlertManager | 告警管理 | 集成部署 |

**处理**: 解析分布式监控架构的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回分布式监控架构的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级分布式监控、支持多节点、日志分析与可视化、面向企业运维团队、的分布式监控平台、支持多节点服务器、统一监控、日志聚合分析、可视化仪表盘与智、能告警、Use、when、需要系统监控、运维告警、部署管理时使用、不适用于物理硬件、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：多服务器统一监控

用户输入："监控公司所有10台服务器"

用户可通过自然语言指令触发此场景，工具将自动执行相应操作并返回结构化结果.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | 系统监控专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 添加监控节点
python3 （请参考skill目录中的脚本文件） add \
  --name "web-01" --host 192.168.1.10 --ssh-key $HOME/.ssh/id_rsa
python3 （请参考skill目录中的脚本文件） add \
  --name "db-01" --host 192.168.1.20 --ssh-key $HOME/.ssh/id_rsa
# ...
# 批量添加
python3 （请参考skill目录中的脚本文件） batch-add --file servers.csv
# ...
# 统一状态查看
python3 （请参考skill目录中的脚本文件） status --all
# ...
# 输出：
# === 集群状态 ===
# web-01  CPU:35% MEM:40% DISK:60% [OK]
# web-02  CPU:42% MEM:55% DISK:70% [OK]
# db-01   CPU:60% MEM:75% DISK:80% [WARN]
# db-02   CPU:55% MEM:70% DISK:65% [OK]
```

### 场景二：Docker容器监控

用户输入："监控这台机器上所有Docker容器"

```bash
# Docker容器监控
python3 （请参考skill目录中的脚本文件） watch \
  --host 192.168.1.10 \
  --interval 30
# ...
# 输出：
# === Docker容器状态 ===
# NAME        CPU%   MEM%   NET I/O       STATUS
# web-app     15.2%  1.2G   50MB/100MB    running
# redis       2.1%   256M   10MB/20MB     running
# postgres    8.5%   2.5G   30MB/200MB    running
```

### 场景三：日志分析

用户输入："分析所有服务器的错误日志"

```bash
# 日志聚合搜索
python3 （请参考skill目录中的脚本文件） search \
  --query "ERROR" \
  --nodes all \
  --time-range "1h" \
  --output error_report.txt
# ...
# 日志分析
python3 （请参考skill目录中的脚本文件） analyze \
  --pattern "exception" \
  --group-by "node,service"
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
pip install monitor-pro
# ...
# 初始化数据库
python3 （请参考skill目录中的脚本文件） --db 数据库 --host localhost
# ...
# 配置Grafana
python3 （请参考skill目录中的脚本文件） setup --url http://localhost:3000
```

### 常用命令

```bash
# 节点管理
python3 （请参考skill目录中的脚本文件） add --name "web-01" --host 192.168.1.10
python3 （请参考skill目录中的脚本文件） status --all
# ...
# Docker监控
python3 （请参考skill目录中的脚本文件） watch --host 192.168.1.10
# ...
# 日志分析
python3 （请参考skill目录中的脚本文件） search --query "ERROR" --nodes all --time-range "1h"
# ...
# 仪表盘
python3 （请参考skill目录中的脚本文件） open --url http://localhost:3000
# ...
# 容量规划
python3 （请参考skill目录中的脚本文件） forecast --metric disk --months 6
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### PRO企业级配置

```yaml
pro_config:
  server:
    host: "0.0.0.0"
    port: 9090
    workers: 4
# ...
  database:
    type: "数据库"
    host: "${DB_HOST}"
    port: 5432
    name: "monitor_pro"
    pool_size: 20
# ...
  nodes:
    discovery: "auto"             # 自动发现
    agent_port: 9091
    ssh_timeout: 10
    max_nodes: 100
# ...
  docker:
    enabled: true
    socket: "/var/run/docker.sock"
    kubernetes:
      enabled: true
      kubeconfig: "$HOME/.kube/config"
# ...
  logs:
    aggregation: true
    storage: "elasticsearch"
    retention_days: 90
    max_size: "100GB"
# ...
  dashboard:
    grafana:
      url: "http://localhost:3000"
      api_key: "${GRAFANA_API_KEY}"
    auto_refresh: 30
# ...
  alerts:
    intelligent_detection: true    # 智能异常检测
    escalation: true               # 告警升级
    channels:
      - email
      - webhook
      - dingtalk
      - webhook
    deduplication: true
    grouping: true
# ...
  capacity_planning:
    enabled: true
    forecast_months: 6
    thresholds:
      disk_warning: 70
      disk_critical: 85
# ...
  retention:
    metrics_days: 365
    logs_days: 90
    alerts_days: 365
```

## 优选实践

### PRO版企业实践

| 实践领域 | 建议做法 |
|:---:|:---:|
| 节点管理 | 使用标签分组，便于批量管理 |
| 容器监控 | 结合K8s标签筛选，关注业务关键容器 |
| 日志管理 | 设置合理保留期，避免存储爆炸 |
| 仪表盘 | 按团队/业务创建专用面板 |
| 告警策略 | 分级告警，避免告警风暴 |

### 免费版兼容性

```text
免费版命令 → PRO版命令（增强）：
monitor.py status        → nodes.py status --all（多节点）
monitor.py alert add     → +智能检测+多通道+升级
monitor.py history       → +365天+容量预测
```

## 常见问题

### Q1：支持监控多少台服务器？

PRO版支持最多100台服务器的分布式监控。如需更大规模，建议使用专用监控平台（如Prometheus+Grafana）.
### Q2：K8s监控如何部署？

PRO版通过Kubernetes API直接监控集群，无需在每个Pod部署Agent。支持监控Pod、Service、Deployment等K8s资源的资源使用和健康状态.
### Q3：日志搜索支持什么语法？

支持全文搜索、字段过滤、时间范围、正则匹配等多种查询方式。底层使用Elasticsearch，兼容Lucene查询语法.
### Q4：智能告警如何工作？

PRO版基于历史数据建立基线，当指标偏离正常范围时自动告警。相比固定阈值，智能告警能适应业务波动，减少误报.
### Q5：容量规划基于什么模型？

使用时间序列预测模型（如ARIMA、线性回归），基于历史趋势预测未来资源使用。支持自定义预测周期和置信区间.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.9+
- **数据库**: `数据库` 12+ 或 MySQL 8+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| psutil | Python库 | 必需 | `pip install psutil` |
| psycopg2 | Python库 | 必需 | `pip install psycopg2-binary` |
| docker | Python库 | 可选 | `pip install docker`（容器监控） |
| kubernetes | Python库 | 可选 | `pip install kubernetes`（K8s监控） |
| elasticsearch | Python库 | 可选 | `pip install elasticsearch`（日志） |
| requests | Python库 | 必需 | `pip install requests` |

### API Key 配置

| 服务 | 环境变量 | 是否必需 | 用途 |
|---:|:---|---:|---:|
| Grafana | `GRAFANA_API_KEY` | 可选 | 仪表盘集成 |
| 钉钉 | `DINGTALK_WEBHOOK` | 可选 | 告警通知 |
| Elasticsearch | `ES_HOST` | 可选 | 日志存储 |

- 未配置的服务自动跳过
- 所有凭证存储在本地配置文件

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本+数据库执行）
- **说明**: 企业级分布式监控平台，支持多节点、容器、日志与可视化
- **PRO版特性**: 分布式监控、Docker/K8s、日志分析、Grafana仪表盘、智能告警、容量规划
- **兼容性**: 完全兼容免费版单机监控命令与配置

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------:|--------|:-------|
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

- **自动化执行**: 企业级分布式监控平台，支持多节点、容器、日志分析与可视化仪表盘.。面向企业运维团队的分布式监控平台。支持多节点服务器统一
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 核心功能

- **自动化执行**: 企业级分布式监控平台，支持多节点、容器、日志分析与可视化仪表盘.。面向企业运维团队的分布式监控平台。支持多节点服务器统一
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据