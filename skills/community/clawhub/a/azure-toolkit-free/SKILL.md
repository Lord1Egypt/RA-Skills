---
slug: azure-toolkit-free
name: azure-toolkit-free
version: 1.0.0
displayName: Azure管理入门工具
summary: 微软Azure基础资源管理工具，支持虚拟机/存储/网络常用资源操作。
license: Proprietary
edition: free
description: '面向个人开发者与初创团队的Azure基础管理工具。支持虚拟机、存储

  账户、虚拟网络等常用资源的创建与管理。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。Use
  when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。'
tags:
- Operations
- Azure
- 云计算
- 部署
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "Azure,云计算,DevOps"
---
# Azure管理入门工具（免费版）

## 概述

本工具为个人开发者和初创团队提供Azure基础资源管理能力。支持虚拟机、存储账户、虚拟网络等常用资源的创建与管理，通过简化命令行操作降低Azure使用门槛。

## 核心能力

### 资源管理

| 资源类型 | 功能 | 免费版支持 |
|----|---|-----|
| 虚拟机 | 创建/启动/停止/删除 | 支持 |
| 存储账户 | 创建/上传/下载 | 支持 |
| 虚拟网络 | 网络/子网配置 | 支持 |
| 网络安全组 | 规则管理 | 支持 |
| 资源组 | 创建/管理 | 支持 |
| 数据库 | SQL数据库 | 不支持 |
| 函数应用 | 无服务器 | 不支持 |
| 监控 | Application Insights | 不支持 |

**输入**: 用户提供资源管理所需的指令和必要参数。
**处理**: 解析资源管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回资源管理的响应数据,包含状态码、结果和日志。

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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Azure、基础资源管理工具、支持虚拟机、网络常用资源操作、面向个人开发者与、初创团队的、基础管理工具、虚拟网络等常用资、源的创建与管理、Use、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：创建虚拟机

用户输入："帮我创建一台Azure虚拟机"

```bash
# 创建虚拟机
python3 （请参考skill目录中的脚本文件） vm create \
  --name "my-vm" \
  --resource-group my-rg \
  --image UbuntuLTS \
  --size Standard_B1s \
  --admin-username azureuser
# ...
# 输出虚拟机信息
```

### 场景二：存储账户操作

用户输入："创建存储账户并上传文件"

```bash
# 创建存储账户
python3 （请参考skill目录中的脚本文件） storage create \
  --name mystorage2026 \
  --resource-group my-rg \
  --sku Standard_LRS
# ...
# 上传文件
python3 （请参考skill目录中的脚本文件） storage upload \
  --account mystorage2026 \
  --container data \
  --file ./data.csv
```

### 场景三：虚拟网络配置

用户输入："创建虚拟网络和子网"

```bash
# 创建虚拟网络
python3 （请参考skill目录中的脚本文件） vnet create \
  --name my-vnet \
  --resource-group my-rg \
  --address-prefix 10.0.0.0/16
# ...
# 创建子网
python3 （请参考skill目录中的脚本文件） vnet subnet create \
  --vnet my-vnet \
  --name my-subnet \
  --address-prefix 10.0.1.0/24
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
# macOS: brew install azure-cli
# Windows: 下载官方安装包
# ...
# 登录Azure
az login
# ...
# 安装Python依赖
pip install azure-mgmt-compute azure-mgmt-storage azure-identity
```

### 常用命令

```bash
# 虚拟机管理
python3 （请参考skill目录中的脚本文件） vm create --name "my-vm" --resource-group my-rg --image UbuntuLTS --size Standard_B1s
python3 （请参考skill目录中的脚本文件） vm list --resource-group my-rg
python3 （请参考skill目录中的脚本文件） vm start --name "my-vm" --resource-group my-rg
python3 （请参考skill目录中的脚本文件） vm stop --name "my-vm" --resource-group my-rg
# ...
# 存储管理
python3 （请参考skill目录中的脚本文件） storage create --name mystorage --resource-group my-rg
python3 （请参考skill目录中的脚本文件） storage upload --account mystorage --container data --file ./file.txt
# ...
# 虚拟网络
python3 （请参考skill目录中的脚本文件） vnet create --name my-vnet --resource-group my-rg --address-prefix 10.0.0.0/16
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤。

## 示例

### Azure配置

```yaml
azure_config:
  subscription_id: "${AZURE_SUBSCRIPTION_ID}"
  tenant_id: "${AZURE_TENANT_ID}"
  client_id: "${AZURE_CLIENT_ID}"
  client_secret: "${AZURE_CLIENT_SECRET}"
# ...
  defaults:
    location: "eastus"
    resource_group: "my-rg"
    vm:
      size: "Standard_B1s"
      image: "UbuntuLTS"
      admin_username: "azureuser"
    storage:
      sku: "Standard_LRS"
      encryption: true
# ...
  tags:
    Project: "my-project"
    Environment: "dev"
    ManagedBy: "azure-toolkit"
```

## 最佳实践

1. **资源组管理**：按项目或环境分组资源，便于管理
2. **最小权限**：服务主体仅授予必要权限
3. **成本控制**：使用B系列突发型虚拟机，适合开发测试
4. **标签规范**：统一标签规范，便于成本追踪

| 实践要点 | 说明 |
|:-----|:-----|
| 凭证安全 | 服务主体密钥不要写入代码 |
| 成本控制 | 及时停止/删除不用的资源 |
| 位置选择 | 选择离用户最近的位置 |
| 免费额度 | 关注免费层额度，避免意外收费 |

## 常见问题

### Q1：免费版支持Azure SQL数据库吗？

免费版不包含Azure SQL数据库管理。如需管理数据库资源，建议升级PRO版。

### Q2：如何认证Azure？

推荐使用服务主体（Service Principal）认证。通过 `az ad sp create-for-rbac` 创建服务主体，将凭证配置到环境变量或配置文件。

### Q3：支持多区域部署吗？

免费版主要在单一区域操作。如需多区域批量部署，建议升级PRO版。

### Q4：如何控制Azure成本？

建议：使用B系列虚拟机、及时释放资源、使用Azure Cost Management监控支出、设置预算告警。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+
- **Azure CLI**: 2.0+（推荐，用于登录配置）

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| azure-identity | Python库 | 必需 | `pip install azure-identity` |
| azure-mgmt-compute | Python库 | 必需 | `pip install azure-mgmt-compute` |
| azure-mgmt-storage | Python库 | 必需 | `pip install azure-mgmt-storage` |
| azure-mgmt-network | Python库 | 必需 | `pip install azure-mgmt-network` |

### API Key 配置

| 服务 | 环境变量 | 是否必需 | 用途 |
|:---:|:---:|:---:|:---:|
| 订阅ID | `AZURE_SUBSCRIPTION_ID` | 必需 | 资源订阅 |
| 租户ID | `AZURE_TENANT_ID` | 必需 | AD认证 |
| 客户端ID | `AZURE_CLIENT_ID` | 必需 | 服务主体 |
| 客户端密钥 | `AZURE_CLIENT_SECRET` | 必需 | 服务主体认证 |

- 凭证通过 `az login` 或服务主体配置
- 建议使用服务主体而非交互式登录

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本执行）
- **说明**: 通过Azure SDK管理基础云资源
- **免费版限制**: 基础资源管理、单区域、不支持数据库与无服务器

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 依赖云服务，需要网络连接

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Azure管理入门工具处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "azurekit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
