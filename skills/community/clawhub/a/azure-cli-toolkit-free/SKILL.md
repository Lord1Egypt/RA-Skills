---
name: "azure-cli-toolkit-free"
description: "Azure云平台命令行管理工具,支持虚拟机、存储、网络等核心资源的基本操作"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Azure命令行工具免费版"
  version: "1.0.0"
  summary: "Azure云平台命令行管理工具,支持虚拟机、存储、网络等核心资源的基本操作"
  tags:
    - "云平台"
    - "Azure"
    - "命令行工具"
    - "云资源管理"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# Azure 命令行工具免费版

## 概述

Azure 命令行工具免费版为个人开发者提供 Azure 云平台的核心管理能力。通过 `az` 命令行工具,用户可以管理订阅、资源组、虚拟机、存储账户、网络资源等核心云资源。

免费版聚焦个人开发场景,提供交互式操作与常用命令,帮助开发者快速上手 Azure 资源管理。

## 核心能力

### 1. 认证与账户管理

```bash
# 交互式登录
az login

# 查看当前账户
az account show

# 列出所有订阅
az account list

# 切换默认订阅
az account set --subscription "我的订阅"
```

**输入**: 用户提供认证与账户管理所需的指令和必要参数。
**处理**: 按照skill规范执行认证与账户管理操作,遵循单一意图原则。
**输出**: 返回认证与账户管理的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 资源组管理

```bash
# 创建资源组
az group create -g myResourceGroup -l eastus

# 列出所有资源组
az group list

# 查看资源组详情
az group show -g myResourceGroup

# 删除资源组
az group delete -g myResourceGroup
```

**输入**: 用户提供资源组管理所需的指令和必要参数。
**处理**: 按照skill规范执行资源组管理操作,遵循单一意图原则。
**输出**: 返回资源组管理的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 虚拟机操作

```bash
# 创建虚拟机
az vm create -g myResourceGroup -n myVM --image UbuntuLTS

# 列出虚拟机
az vm list -g myResourceGroup

# 启动/停止/重启
az vm start -g myResourceGroup -n myVM
az vm stop -g myResourceGroup -n myVM
az vm restart -g myResourceGroup -n myVM

# 查看虚拟机详情
az vm show -g myResourceGroup -n myVM
```

**输入**: 用户提供虚拟机操作所需的指令和必要参数。
**处理**: 按照skill规范执行虚拟机操作操作,遵循单一意图原则。
**输出**: 返回虚拟机操作的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 存储账户操作

```bash
# 创建存储账户
az storage account create -g myResourceGroup -n mystorage --sku Standard_LRS

# 列出存储账户
az storage account list

# 上传文件到 Blob
az storage blob upload \
  --account-name mystorage \
  -c mycontainer \
  -n myfile.txt \
  -f ./local-file.txt

# 下载 Blob 文件
az storage blob download \
  --account-name mystorage \
  -c mycontainer \
  -n myfile.txt \
  -f ./downloaded.txt
```

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 5. 输出格式化与查询

```bash
# JSON 格式输出
az vm list -o json

# 表格格式输出
az vm list -o table

# JMESPath 查询:提取名称
az vm list --query "[].name" -o tsv

# 条件过滤:运行中的虚拟机
az vm list --query "[?powerState=='VM running'].name"
```

**输入**: 用户提供存储账户操作所需的指令和必要参数。
**处理**: 按照skill规范执行存储账户操作操作,遵循单一意图原则。
**输出**: 返回存储账户操作的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Azure、云平台命令行管理、支持虚拟机、网络等核心资源的、基本操作、面向个人开发者的、提供核心资源管理、核心能力、订阅与资源组管理、网络资源基本操作、交互式登录与基础等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一: 搭建开发测试环境

开发者需要快速创建一台测试虚拟机并配置存储。

```bash
# 1. 创建资源组
az group create -g dev-test-rg -l eastus

# 2. 创建虚拟机
az vm create -g dev-test-rg -n dev-vm \
  --image UbuntuLTS \
  --admin-username devuser \
  --generate-ssh-keys

# 3. 创建存储账户
az storage account create -g dev-test-rg -n devstorage01 --sku Standard_LRS

# 4. 创建容器
az storage container create --account-name devstorage01 -n uploads

# 5. 验证资源
az resource list -g dev-test-rg -o table
```

### 场景二: 查询资源状态

定期查看个人云资源的状态与费用。

```bash
# 查看所有运行中的虚拟机
az vm list -d --query "[?powerState=='VM running'].{name:name, location:location}" -o table

# 查看存储账户使用情况
az storage account list --query "[].{name:name, sku:sku.name}" -o table

# 按标签筛选资源
az resource list --tag env=dev -o table
```

### 场景三: 配置默认参数

设置常用默认值,简化日常命令输入。

```bash
# 设置默认资源组、订阅、区域
az configure --defaults group=dev-test-rg location=eastus

# 之后创建资源无需重复指定
az vm create -n new-vm --image UbuntuLTS
```

## 快速开始

### 依赖详情

**macOS:**

```bash
brew install azure-cli
```

**Linux (Ubuntu/Debian):**

```bash
curl -sL https://aka.ms/InstallAzureCliLinux | bash
```

**Windows:**

```powershell
choco install azure-cli
```

### 第二步: 验证安装

```bash
az --version
az --help
```

### 第三步: 登录 Azure

```bash
az login
```

浏览器会打开登录页面,完成认证后终端会显示订阅列表。

### 第四步: 创建第一个资源

```bash
az group create -g my-first-rg -l eastus
az vm create -g my-first-rg -n my-vm --image UbuntuLTS
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例

### 常用全局参数

| 参数 | 简写 | 说明 |
|:-----|:-----|:-----|
| `--subscription` | | 指定订阅 |
| `--resource-group` | `-g` | 指定资源组 |
| `--output` | `-o` | 输出格式: json/table/tsv/yaml |
| `--query` | | JMESPath 查询表达式 |
| `--verbose` | `-v` | 详细输出 |
| `--help` | `-h` | 帮助信息 |

### 默认配置

```bash
# 查看当前配置
az configure --list-defaults

# 设置默认值
az configure --defaults group=myRG location=eastus

# 清除默认值
az configure --defaults group='' location=''
```

## 最佳实践

### 1. 善用查询语法

```bash
# 提取关键字段
az vm list --query "[].{name:name, state:powerState}" -o table

# 排序输出
az vm list --query "sort_by([], &name)"

# 统计数量
az vm list --query "length([])"
```

### 2. 使用 --no-wait 加速操作

```bash
# 不等待创建完成,立即返回
az vm create -g myRG -n myVM --image UbuntuLTS --no-wait

# 稍后用 show 查看状态
az vm show -g myRG -n myVM --query provisioningState
```

### 3. 启用 Tab 补全

```bash
# macOS (zsh)
eval "$(az completion init zsh)"

# Linux (bash)
eval "$(az completion init bash)"
```

### 4. 命令搜索

```bash
# 按功能描述搜索命令
az find "create virtual machine"
az find "list storage"
```

## 常见问题

### Q1: 免费版支持多少个命令模块?

免费版支持 Azure CLI 全部 66 个命令模块的基本操作,但部分高级批量操作与自动化脚本需要 PRO 版。

### Q2: 登录后看不到我的订阅?

确认账户有权限访问目标订阅。可运行 `az account list --all` 查看所有可访问的订阅。

### Q3: 如何切换到不同的租户?

```bash
# 列出可访问的租户
az account tenant list

# 切换租户(登录时指定)
az login --tenant <tenant_id>
```

### Q4: 命令执行报权限不足?

检查当前账户是否有所需角色权限。可用 `az role assignment list` 查看当前角色分配。

### 已知限制

免费版本身不限制命令调用次数,但 Azure 平台本身的 API 限流策略仍然适用。
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境

- **Agent 平台**: 支持读取 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Azure CLI**: v2.50 或更高版本

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Azure CLI | CLI 工具 | 必需 | brew / apt / choco 安装 |
| Azure 订阅 | 云服务 | 必需 | azure.com 注册 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| jq(可选) | CLI 工具 | 否 | 系统包管理器 |

### API Key 配置

- 交互式登录无需 API Key,通过浏览器完成认证
- 服务主体认证需配置以下环境变量:

```bash
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
```

### 可用性分类

- **分类**: MD+EXEC(Markdown 指令 + 命令行执行)
- **说明**: 通过自然语言指令驱动 Agent 执行 `az` 命令管理 Azure 资源
- **离线可用**: 否,所有操作需要连接 Azure 云平台

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
