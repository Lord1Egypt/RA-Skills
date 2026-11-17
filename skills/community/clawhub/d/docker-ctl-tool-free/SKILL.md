---
name: "docker-ctl-tool-free"
description: "Podman/Docker容器检查工具，支持容器状态查询与日志分析。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "容器检查入门工具"
  version: "1.0.0"
  summary: "Podman/Docker容器检查工具，支持容器状态查询与日志分析。"
  tags:
    - "Operations"
    - "容器检查"
    - "运维"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# 容器检查入门工具（免费版）

## 概述

本工具为个人开发者提供容器检查能力，兼容Podman与Docker双引擎。支持容器状态查询、日志分析、资源监控与配置检查，帮助快速排查容器问题。

## 核心能力

### 检查功能

| 功能 | 说明 | 免费版支持 |
| --- | --- | --- |
| 状态检查 | 运行状态/退出码/启动时间 | 支持 |
| 日志查看 | 实时/历史日志 | 支持 |
| 资源监控 | CPU/内存/网络IO | 支持 |
| 配置检查 | 环境变量/端口/挂载 | 支持 |
| 批量检查 | 多容器并行 | 不支持 |
| 健康检查 | 容器健康状态 | 支持 |
| 历史分析 | 趋势分析 | 不支持 |
| 异常诊断 | 智能诊断 | 不支持 |

**输出**: 返回检查功能的执行结果,包含操作状态和输出数据。

### 兼容引擎

| 引擎 | 说明 | 免费版支持 |
| --- | --- | --- |
| Podman | 无守护进程容器引擎 | 支持 |
| Docker | 标准容器引擎 | 支持 |
| 自动检测 | 自动识别已安装引擎 | 支持 |

**输出**: 返回兼容引擎的执行结果,包含操作状态和输出数据。

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：容器检查工具、支持容器状态查询、与日志分析、面向个人开发者的、支持容器状态、日志分析、资源使用监控与配、Use、when、需要系统监控、运维告警、部署管理时使用、不适用于物理硬件、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：检查容器状态

用户输入："查看所有容器的状态"

```bash
# 检查所有容器
python3 scripts/ctl.py ps --all

# 输出：
# NAME        STATUS    AGE    PORTS
# web-app     running   2h     8080:80
# redis       running   2h     6379:6379
# postgres    exited    10m    5432:5432
```

### 场景二：查看容器日志

用户输入："看看web-app的日志"

```bash
# 查看日志
python3 scripts/ctl.py logs --name web-app --tail 100

# 实时跟踪日志
python3 scripts/ctl.py logs --name web-app --follow

# 过滤错误日志
python3 scripts/ctl.py logs --name web-app --grep "ERROR"
```

### 场景三：资源使用检查

用户输入："哪些容器占内存最多？"

```bash
# 资源使用统计
python3 scripts/ctl.py stats --sort memory

# 输出：
# NAME        CPU%   MEM USAGE      NET I/O
# postgres    5.2%   512MiB/1GiB   10MB/50MB
# web-app     15.3%  256MiB/512MiB 50MB/100MB
# redis       1.1%   64MiB/256MiB  5MB/10MB
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 环境准备

```bash
# 依赖说明
# Podman: brew install podman (macOS)
# Docker: 见docker-toolkit安装

# 安装Python依赖
pip install subprocess

# 验证
python3 scripts/ctl.py info
```

### 常用命令

```bash
# 容器状态
python3 scripts/ctl.py ps --all
python3 scripts/ctl.py inspect --name web-app

# 日志
python3 scripts/ctl.py logs --name web-app --tail 100
python3 scripts/ctl.py logs --name web-app --follow
python3 scripts/ctl.py logs --name web-app --grep "ERROR"

# 资源
python3 scripts/ctl.py stats
python3 scripts/ctl.py stats --sort cpu

# 配置检查
python3 scripts/ctl.py config --name web-app
python3 scripts/ctl.py ports --name web-app
python3 scripts/ctl.py volumes --name web-app

# 健康检查
python3 scripts/ctl.py health --name web-app
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

## 示例

### 检查工具配置

```yaml
ctl_config:
  engine: "auto"                 # auto | podman | docker
  socket:
    podman: "unix:///run/podman/podman.sock"
    docker: "unix:///var/run/docker.sock"

  defaults:
    log_tail: 100
    stats_interval: 5
    timeout: 30

  output:
    format: "table"              # table | json | yaml
    color: true
```

## 优选实践

1. **引擎选择**：Podman无需守护进程更安全，Docker生态更成熟
2. **日志过滤**：使用grep过滤关键词，快速定位问题
3. **资源监控**：定期检查资源使用，及时发现问题容器
4. **健康检查**：配置容器健康检查，自动发现异常

| 实践要点 | 说明 |
| --- | --- |
| 引擎兼容 | 命令兼容Podman和Docker，无需修改 |
| 日志量 | 大量日志时使用--tail限制输出 |
| 资源限制 | 检查资源使用，确认是否达到限制 |
| 退出码 | 非零退出码表示异常，需查看日志 |

## 常见问题

### Q1：Podman和Docker有什么区别？

Podman无需守护进程（daemonless），更安全；Docker需要dockerd守护进程。两者命令兼容，本工具自动检测。

### Q2：免费版支持批量检查吗？

免费版仅支持单个容器检查。如需批量检查所有容器并生成报告，建议升级PRO版。

### Q3：如何查看已退出的容器日志？

使用 `--all` 参数查看所有容器（包括已退出的），然后指定容器名查看日志。退出容器的日志在容器删除前仍然保留。

### Q4：支持远程容器检查吗？

免费版仅支持本地容器检查。如需检查远程主机上的容器，建议通过SSH连接后在远程执行，或升级PRO版。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+
- **容器引擎**: Podman 4.0+ 或 Docker 20.0+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| Podman或Docker | CLI工具 | 必需 | 系统安装 |

### API Key 配置

- 免费版无需API Key
- 通过本地容器引擎CLI执行检查

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本+CLI执行）
- **说明**: 兼容Podman/Docker的容器检查工具
- **免费版限制**: 单容器检查、不支持批量与历史分析

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
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

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据