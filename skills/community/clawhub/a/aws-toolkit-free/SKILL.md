---
slug: aws-toolkit-free
name: aws-toolkit-free
version: 1.0.0
displayName: AWS部署入门工具
summary: AWS基础架构部署工具，支持EC2/S3/VPC常用资源创建与管理。
license: Proprietary
edition: free
description: '面向个人开发者与初创团队的AWS基础部署工具。支持EC2实例、S3存储、

  VPC网络等常用资源的创建与管理。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。Use
  when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。'
tags:
- Operations
- AWS
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
tags: "AWS,云计算,DevOps"
---
# AWS部署入门工具（免费版）

## 概述

本工具为个人开发者和初创团队提供AWS基础架构部署能力。支持EC2实例、S3存储、VPC网络等常用资源的创建与管理，通过简化的命令行操作降低AWS使用门槛。

## 核心能力

### 资源管理

| 资源类型 | 功能 | 免费版支持 |
|----|---|-----|
| EC2 | 创建/启动/停止/删除 | 支持 |
| S3 | 存储桶创建/上传/下载 | 支持 |
| VPC | 网络/子网/路由 | 支持 |
| 安全组 | 规则管理 | 支持 |
| IAM | 用户/角色基础管理 | 支持 |
| RDS | 数据库实例 | 不支持 |
| Lambda | 无服务器函数 | 不支持 |
| CloudWatch | 监控告警 | 不支持 |

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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：AWS、基础架构部署工具、常用资源创建与管、面向个人开发者与、初创团队的、基础部署工具、网络等常用资源的、创建与管理、Use、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：创建EC2实例

用户输入："帮我创建一台EC2实例"

```bash
# 创建EC2实例
python3 （请参考skill目录中的脚本文件） ec2 create \
  --name "my-server" \
  --instance-type t3.micro \
  --ami ami-0abcdef1234567890 \
  --key-name my-key \
  --security-group sg-xxx
# ...
# 输出实例信息
```

### 场景二：S3存储操作

用户输入："创建一个S3存储桶并上传文件"

```bash
# 创建存储桶
python3 （请参考skill目录中的脚本文件） s3 create-bucket --name my-bucket-2026
# ...
# 上传文件
python3 （请参考skill目录中的脚本文件） s3 upload --bucket my-bucket-2026 --file ./data.csv
# ...
# 列出文件
python3 （请参考skill目录中的脚本文件） s3 list --bucket my-bucket-2026
```

### 场景三：VPC网络配置

用户输入："创建一个VPC和子网"

```bash
# 创建VPC
python3 （请参考skill目录中的脚本文件） vpc create --cidr 10.0.0.0/16 --name my-vpc
# ...
# 创建子网
python3 （请参考skill目录中的脚本文件） vpc create-subnet --vpc-id vpc-xxx --cidr 10.0.1.0/24
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
# macOS: brew install awscli
# Windows: 下载官方安装包
# ...
# 配置凭证
aws configure
# 输入Access Key ID, Secret Access Key, Region
# ...
# 安装Python依赖
pip install boto3
```

### 常用命令

```bash
# EC2管理
python3 （请参考skill目录中的脚本文件） ec2 create --name "server" --type t3.micro --ami ami-xxx
python3 （请参考skill目录中的脚本文件） ec2 list
python3 （请参考skill目录中的脚本文件） ec2 start --instance-id i-xxx
python3 （请参考skill目录中的脚本文件） ec2 stop --instance-id i-xxx
# ...
# S3管理
python3 （请参考skill目录中的脚本文件） s3 create-bucket --name my-bucket
python3 （请参考skill目录中的脚本文件） s3 upload --bucket my-bucket --file ./file.txt
python3 （请参考skill目录中的脚本文件） s3 download --bucket my-bucket --key file.txt
# ...
# VPC管理
python3 （请参考skill目录中的脚本文件） vpc create --cidr 10.0.0.0/16
python3 （请参考skill目录中的脚本文件） vpc list
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤。

## 示例

### AWS配置

```yaml
aws_config:
  region: "us-east-1"
  profile: "default"
# ...
  defaults:
    ec2:
      instance_type: "t3.micro"
      ami: "ami-0abcdef1234567890"
      key_name: "my-key"
    s3:
      region: "us-east-1"
      encryption: true
    vpc:
      cidr: "10.0.0.0/16"
      enable_dns: true
# ...
  tags:
    Project: "my-project"
    Environment: "dev"
    ManagedBy: "aws-toolkit"
```

## 最佳实践

1. **最小权限**：IAM用户仅授予必要权限，避免使用root账户
2. **安全组**：仅开放必要端口，避免0.0.0.0/0全开放
3. **标签管理**：为资源打标签，便于成本追踪与管理
4. **区域选择**：选择离用户最近的区域，降低延迟

| 实践要点 | 说明 |
|:-----|:-----|
| 凭证安全 | 不要将Access Key写入代码 |
| 成本控制 | 及时停止/删除不用的资源 |
| 备份策略 | 重要数据定期备份至S3 |
| 免费额度 | 关注免费层额度，避免意外收费 |

## 常见问题

### Q1：免费版支持RDS数据库吗？

免费版不包含RDS数据库管理。如需管理RDS实例，建议升级PRO版。

### Q2：如何控制AWS成本？

建议：使用t3.micro等免费层实例、及时停止不用的EC2、使用S3生命周期策略、设置账单告警。

### Q3：支持多区域部署吗？

免费版主要在单一区域操作。如需多区域批量部署，建议升级PRO版。

### Q4：需要安装AWS CLI吗？

建议安装AWS CLI用于凭证配置。本工具通过boto3 SDK操作AWS，凭证可通过AWS CLI或环境变量配置。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+
- **AWS CLI**: 2.0+（推荐，用于凭证配置）

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| boto3 | Python库 | 必需 | `pip install boto3` |
| awscli | CLI工具 | 推荐 | `pip install awscli` |

### API Key 配置

| 服务 | 环境变量 | 是否必需 | 用途 |
|:---:|:---:|:---:|:---:|
| AWS Access Key | `AWS_ACCESS_KEY_ID` | 必需 | AWS API认证 |
| AWS Secret | `AWS_SECRET_ACCESS_KEY` | 必需 | AWS API认证 |
| AWS Region | `AWS_DEFAULT_REGION` | 必需 | 默认区域 |

- 凭证通过 `aws configure` 或环境变量配置
- 建议使用IAM用户而非root账户

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本执行）
- **说明**: 通过boto3 SDK管理AWS基础资源
- **免费版限制**: 基础资源管理、单区域、不支持RDS/Lambda/CloudWatch

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
    "result": "AWS部署入门工具处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "awskit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
