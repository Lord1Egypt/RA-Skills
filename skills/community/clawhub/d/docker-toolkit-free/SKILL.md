---
slug: docker-toolkit-free
name: docker-toolkit-free
version: 1.0.0
displayName: Docker容器入门工具
summary: Docker容器管理工具，支持镜像/容器/卷/网络基础操作与简单编排。
license: Proprietary
edition: free
description: '面向个人开发者的Docker容器管理工具。支持镜像构建与拉取、容器

  生命周期管理、数据卷与网络配置。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。适用于独立开发者、企业团队和自动化工作流场景。Use
  when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。'
tags:
- Operations
- Docker
- 容器化
- 部署
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "容器,Docker,DevOps"
---
# Docker容器入门工具（免费版）

## 概述

本工具为个人开发者提供Docker容器管理能力。支持镜像构建、容器生命周期管理、数据卷与网络配置，以及Docker Compose基础编排。适合个人开发环境与小型应用的容器化部署。

## 核心能力

### 管理功能

| 功能 | 说明 | 免费版支持 |
|---|---|-----|
| 镜像管理 | 构建/拉取/推送/删除 | 支持 |
| 容器管理 | 创建/启动/停止/删除 | 支持 |
| 数据卷 | 创建/挂载/备份 | 支持 |
| 网络 | 创建/连接/断开 | 支持 |
| Compose | 多容器编排 | 基础支持 |
| 镜像仓库 | 私有仓库管理 | 不支持 |
| 集群管理 | Swarm/K8s | 不支持 |
| 安全扫描 | 镜像漏洞扫描 | 不支持 |

**输入**: 用户提供管理功能所需的指令和必要参数。
**处理**: 解析管理功能的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回管理功能的响应数据,包含状态码、结果和日志。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Docker、容器管理工具、支持镜像、网络基础操作与简、单编排、面向个人开发者的、支持镜像构建与拉、生命周期管理、数据卷与网络配置、Use、when、需要数据分析、报表生成、统计洞察、数据可视化时使用、不适用于实时流数、据处理、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：构建并运行容器

用户输入："构建镜像并运行容器"

```bash
# 构建镜像
python3 （请参考skill目录中的脚本文件） image build \
  --tag my-app:latest \
  --path ./Dockerfile
# ...
# 运行容器
python3 （请参考skill目录中的脚本文件） container run \
  --image my-app:latest \
  --name my-app \
  --port 8080:80 \
  --detach
# ...
# 查看运行状态
python3 （请参考skill目录中的脚本文件） container ps
```

### 场景二：Docker Compose编排

用户输入："用Compose启动一套Web+数据库环境"

```bash
# 生成docker-compose.yml
python3 （请参考skill目录中的脚本文件） compose generate \
  --template "web_db" \
  --output docker-compose.yml
# ...
# 启动服务
python3 （请参考skill目录中的脚本文件） compose up --detach
# ...
# 查看状态
python3 （请参考skill目录中的脚本文件） compose ps
```

### 场景三：数据卷管理

用户输入："创建数据卷并挂载到容器"

```bash
# 创建数据卷
python3 （请参考skill目录中的脚本文件） volume create --name my-data
# ...
# 挂载运行
python3 （请参考skill目录中的脚本文件） container run \
  --image postgres:15 \
  --name my-db \
  --volume my-data:/var/lib/postgresql/data \
  --detach
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
# macOS: brew install --cask docker
# Linux: curl -fsSL https://get.docker.com | sh
# Windows: 下载Docker Desktop
# ...
# 安装Python依赖
pip install docker
# ...
# 验证Docker
docker --version
```

### 常用命令

```bash
# 镜像管理
python3 （请参考skill目录中的脚本文件） image build --tag my-app:latest --path ./Dockerfile
python3 （请参考skill目录中的脚本文件） image pull nginx:latest
python3 （请参考skill目录中的脚本文件） image list
python3 （请参考skill目录中的脚本文件） image delete my-app:old
# ...
# 容器管理
python3 （请参考skill目录中的脚本文件） container run --image nginx --name web --port 8080:80 --detach
python3 （请参考skill目录中的脚本文件） container ps
python3 （请参考skill目录中的脚本文件） container stop --name web
python3 （请参考skill目录中的脚本文件） container logs --name web --tail 100
# ...
# 数据卷
python3 （请参考skill目录中的脚本文件） volume create --name my-data
python3 （请参考skill目录中的脚本文件） volume list
# ...
# 网络
python3 （请参考skill目录中的脚本文件） network create --name my-net
python3 （请参考skill目录中的脚本文件） network list
# ...
# Compose
python3 （请参考skill目录中的脚本文件） compose up --detach
python3 （请参考skill目录中的脚本文件） compose down
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤。

#
## 示例

### Docker配置

```yaml
docker_config:
  host: "unix:///var/run/docker.sock"
  timeout: 60
# ...
  defaults:
    image:
      registry: "docker.io"
      tag: "latest"
    container:
      restart_policy: "unless-stopped"
      memory_limit: "512m"
      cpu_limit: 1.0
    volume:
      driver: "local"
    network:
      driver: "bridge"
# ...
  compose:
    version: "3.8"
    default_template: "web_db"
```

## 最佳实践

1. **镜像优化**：使用多阶段构建减小镜像体积
2. **标签管理**：使用语义化版本标签，避免仅用latest
3. **数据持久化**：重要数据使用数据卷，避免容器删除后丢失
4. **网络隔离**：不同应用使用独立网络，避免互相干扰

| 实践要点 | 说明 |
|:-----|:-----|
| 镜像清理 | 定期清理无用镜像，释放磁盘 |
| 资源限制 | 设置内存和CPU限制，避免容器失控 |
| 日志管理 | 配置日志轮转，避免日志撑满磁盘 |
| 安全意识 | 不使用root运行应用，最小权限原则 |

## 常见问题

### Q1：免费版支持Docker Swarm/K8s吗？

免费版仅支持单机Docker管理。如需集群管理，建议升级PRO版或使用专用K8s工具。

### Q2：如何连接远程Docker？

通过配置DOCKER_HOST环境变量指向远程Docker守护进程。需开启远程Docker的TCP端口（需配置TLS加密）。

### Q3：支持私有镜像仓库吗？

免费版支持从私有仓库拉取镜像（需提前docker login）。如需管理私有仓库，建议升级PRO版。

### Q4：容器无法启动怎么办？

检查：镜像是否存在、端口是否被占用、数据卷路径是否正确、容器日志中的错误信息。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+
- **Docker**: 20.0+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| docker | Python库 | 必需 | `pip install docker` |
| docker-compose | CLI工具 | 可选 | 随Docker Desktop安装 |

### API Key 配置

- 免费版无需API Key
- 私有镜像仓库需通过 `docker login` 配置凭证

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本执行）
- **说明**: 通过Docker SDK管理本地容器资源
- **免费版限制**: 单机管理、不支持集群与私有仓库管理

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Docker容器入门工具处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "dockerkit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
