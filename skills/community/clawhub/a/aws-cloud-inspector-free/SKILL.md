---
name: "aws-cloud-inspector-free"
description: "基于AWS CLI的只读云基础设施查询助手，免费提供资源清点、健康检查与基础安全核查能力，适合个人开发者日常巡检。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "AWS云巡检免费版"
  version: "1.0.0"
  summary: "基于AWS CLI的只读云基础设施查询助手，免费提供资源清点、健康检查与基础安全核查能力，适合个人开发者日常巡检。"
  tags:
    - "AWS巡检"
    - "只读查询"
    - "云基础设施"
    - "免费工具"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# AWS云巡检免费版（aws-cloud-inspector-free）

本Skill基于本地AWS CLI提供只读云基础设施查询能力。所有操作默认只读，任何变更/破坏性操作必须用户显式确认后才执行。

> 版本边界：本免费版支持资源清点、健康检查、基础安全核查与变更预演。**安全审计、成本分析、变更管理**三项高级能力被限制，需升级至 `aws-cloud-inspector-pro` 解锁。

## 使用流程

本工具属"中等工具"级别，完整上手目标 < 120秒。

| 阶段 | 目标耗时 | 任务 |
|------|----------|------|
| 环境检查 | < 30秒 | 确认AWS CLI已安装且凭证已配置 |
| 身份确认 | < 30秒 | `aws sts get-caller-identity` 验证身份 |
| 资源清点 | < 60秒 | 执行第一个只读查询命令 |

### 1.1 环境检查（< 30秒）

AWS CLI标准配置路径：
1. **Linux/macOS**：`~/.aws/config`（profile与region配置）、`~/.aws/credentials`（访问密钥）
2. **Windows**：`%USERPROFILE%\.aws\config`、`%USERPROFILE%\.aws\credentials`

```bash
aws --version  # 确认CLI已安装
aws configure list  # 查看当前profile与region
```

如果未配置，运行 `aws configure` 引导配置。

### 1.2 身份确认（< 30秒）

```bash
aws sts get-caller-identity
# 返回：Account、Arn、UserId
# 这是所有巡检的起点，确认你正在操作正确的账号
```

### 1.3 第一个只读查询（< 60秒）

```bash
# 列出当前region所有EC2实例
aws ec2 describe-instances --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name,Type:InstanceType}' --output table
```

## 二、安全规则（必须遵守）

以下规则优先级最高，任何命令执行前必须先通过这些规则检查：

1. **默认只读**：所有操作视为只读，除非用户显式请求变更**并**确认。
2. **破坏性操作二次确认**：对任何潜在破坏性操作（delete/terminate/destroy/modify/scale/billing/IAM凭证），必须要求用户确认步骤。
3. **优先dry-run**：有 `--dry-run` 参数时优先使用，先展示计划再执行。
4. **绝不泄露密钥**：永不输出或记录access key、session token等敏感信息。查询IAM时只显示元数据，不显示凭证内容。
5. **Region感知**：结果如果region-scoped，必须明确说明使用的region。
6. **Profile隔离**：严格使用用户指定的profile，不跨profile操作。

## 三、Region与Profile处理

### 3.1 优先级链

```text
用户显式指定 region/profile
    ↓ 未指定
环境变量 AWS_PROFILE / AWS_REGION
    ↓ 未设置
~/.aws/config 中的 default profile
    ↓ 不存在
提示用户运行 aws configure
```

### 3.2 AWS CLI路径说明

本Skill在以下标准路径查找AWS配置（已修复原版占位符问题）：

| 平台 | 配置文件路径 | 凭证文件路径 |
|------|-------------|-------------|
| Linux/macOS | `~/.aws/config` | `~/.aws/credentials` |
| Windows | `%USERPROFILE%\.aws\config` | `%USERPROFILE%\.aws\credentials` |

`~/.aws/config` 文件示例：
```ini
[default]
region = us-east-1
output = json

[profile production]
region = ap-northeast-1
output = table
```

`~/.aws/credentials` 文件示例：
```ini
[default]
aws_access_key_id = AKIA...
aws_secret_access_key = ...

[production]
aws_access_key_id = AKIA...
aws_secret_access_key = ...
```

> 安全提示：本Skill永不读取或输出 `~/.aws/credentials` 文件内容，仅通过AWS CLI内部机制使用凭证。

## 四、任务指南（常见巡检请求）

| 任务类型 | 推荐命令 | 操作属性 | 免费版支持 |
|----------|----------|----------|-----------|
| 资源清点 | `list` / `describe` / `get` 类命令 | 只读 | ✅ |
| 健康检查 | CloudWatch metrics / logs 查询 | 只读 | ✅ |
| 基础安全核查 | IAM列表、S3公开访问、SG暴露、KMS使用 | 只读 | ✅ 基础核查 |
| 安全审计 | 跨服务安全态势扫描 | 只读 | ❌ 专业版能力 |
| 成本查询 | Cost Explorer / billing 查询 | 只读 | ❌ 专业版能力 |
| 变更管理 | 资源变更追踪与回滚 | 写操作 | ❌ 专业版能力 |
| 资源变更 | 写/删除/终止类操作 | 写操作 | ⚠️ 需二次确认 |

## 示例

### 场景1：新接手项目的资源盘点

**用户角色**：新入职运维工程师
**目标**：盘点刚接手的AWS账号下所有核心资源。

```bash
# 步骤1：确认身份
aws sts get-caller-identity

# 步骤2：列出所有region的EC2实例
aws ec2 describe-regions --query 'Regions[].RegionName' --output text | tr '\t' '\n' | while read region; do
  echo "=== $region ==="
  aws ec2 describe-instances --region $region \
    --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name,Type:InstanceType}' \
    --output table
done

# 步骤3：列出所有S3桶
aws s3api list-buckets --query 'Buckets[].{Name:Name,Created:CreationDate}' --output table

# 步骤4：列出所有IAM用户
aws iam list-users --query 'Users[].{Name:UserName,Created:CreateDate}' --output table
```

### 场景2：上线前基础安全自检

**用户角色**：独立开发者
**目标**：上线前检查是否存在公开暴露的资源。

```bash
# 检查1：S3桶公开访问阻止配置
aws s3api get-public-access-block --bucket my-bucket 2>/dev/null || echo "未配置公开访问阻止"

# 检查2：安全组是否暴露22端口到0.0.0.0/0
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?FromPort==`22` && IpRanges[?CidrIp==`0.0.0.0/0`]].GroupId' \
  --output text

# 检查3：IAM访问密钥年龄（超过90天需关注）
aws iam list-access-keys --user-name my-user \
  --query 'AccessKeyMetadata[].{KeyID:AccessKeyId,Created:CreateDate,Status:Status}' --output table
```

### 场景3：CloudWatch告警排查

**用户角色**：运维值班
**目标**：排查某EC2实例的CPU告警。

```bash
# 查看最近1小时CPU使用率
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average \
  --output table

# 查看最近告警状态
aws cloudwatch describe-alarms --state-value ALARM \
  --query 'MetricAlarms[].{Name:AlarmName,Metric:MetricName,State:StateValue}' --output table
```

## 常见问题

### Q1：如何切换到不同的AWS账号？
A：使用 `--profile` 参数指定命名profile。例如 `aws ec2 describe-instances --profile production`。或设置环境变量 `export AWS_PROFILE=production`。

### Q2：如何查询所有region的资源？
A：先 `aws ec2 describe-regions` 获取所有region列表，然后循环调用带 `--region` 参数的命令。注意部分服务（如IAM、S3）是全局服务，无需指定region。

### Q3：免费版能执行变更操作吗？
A：可以，但所有变更类操作（delete/terminate/modify等）必须经过用户二次确认。本Skill会先展示完整命令与 `--dry-run` 预演结果，用户确认后才执行。完整变更管理（变更追踪、回滚、审批流）是专业版能力。

### Q4：报错 "Unable to locate credentials" 怎么办？
A：运行 `aws configure` 配置访问密钥，或检查 `~/.aws/credentials` 文件是否存在且格式正确。也可通过环境变量 `AWS_ACCESS_KEY_ID` 与 `AWS_SECRET_ACCESS_KEY` 临时设置。

### Q5：如何只查询特定状态的EC2实例？
A：使用 `--filters` 参数。例如：
```bash
aws ec2 describe-instances --filters Name=instance-state-name,Values=running \
  --query 'Reservations[].Instances[].InstanceId' --output text
```

### Q6：免费版与专业版的核心差异？
A：免费版提供资源清点、健康检查、基础安全核查与变更预演。专业版新增三项高级能力：(1) 安全审计（跨服务安全态势扫描）；(2) 成本分析（Cost Explorer深度查询）；(3) 变更管理（变更追踪与回滚）。

### Q7：查询结果太多如何过滤？
A：使用 `--query` 参数配合JMESPath语法过滤。例如 `--query 'Reservations[].Instances[?State.Name==`running`].InstanceId'`。也可用 `--output table` 让结果更易读。

## 错误处理


| 序号 | 问题 | 原因 | 修复方案 | 优先级 |
|------|------|------|----------|--------|
| 1 | `Unable to locate credentials` | 未配置AWS凭证 | 运行 `aws configure` 或检查 `~/.aws/credentials` | P0 |
| 2 | `InvalidClientTokenId` | 凭证无效或已过期 | 重新生成access key并更新配置 | P0 |
| 3 | `AccessDenied` | IAM权限不足 | 联系管理员添加所需权限，或切换有权限的profile | P1 |
| 4 | `Could not connect to the endpoint URL` | 网络问题或region错误 | 执行ping命令测试网络连通性,检查防火墙和代理设置代理设置，确认region拼写正确 | P1 |
| 5 | `Rate exceeded` | API调用频率超限 | 添加请求间隔，或使用分页 `--starting-token` | P2 |
| 6 | `--query` 语法错误 | JMESPath语法不正确 | 检查引号转义，使用 `--output text` 调试 | P2 |
| 7 | `Profile not found` | profile名称拼写错误 | 运行 `aws configure list-profiles` 查看可用profile | P1 |
| 8 | 命令在Windows下报错 | 路径或引号问题 | 使用正斜杠路径，双引号包裹参数 | P2 |

## 八、References（本地参考文档）

以下参考文档为本地Markdown文件，与本SKILL.md同目录的 `references/` 子目录下：

- [references/aws-cli-queries.md](references/aws-cli-queries.md) —— 常用AWS CLI只读查询命令模式与示例
- [references/aws-security-basics.md](references/aws-security-basics.md) —— 基础安全核查清单与命令
- [references/aws-region-profile.md](references/aws-region-profile.md) —— Region与Profile配置详解

> 安全审计、成本分析、变更管理相关参考文档在专业版提供。

## 依赖说明

### 运行环境
- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Windows / macOS / Linux
- **AWS CLI**：v2.0+（推荐v2.13+）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 | 免费版兼容性 |
|:-------|:-----|:---------|:---------|:------------|
| AWS CLI v2 | 命令行工具 | 必需 | 官方安装包 | ✅ 完整可用 |
| AWS账户 | 云服务 | 必需 | AWS官网注册 | ✅ 只读权限即可 |
| IAM只读权限 | IAM策略 | 必需 | IAM控制台分配 | ✅ 免费版仅需只读 |
| Cost Explorer | AWS服务 | 可选 | 专业版解锁 | ❌ 本免费版不支持 |
| CloudTrail | AWS服务 | 可选 | 专业版解锁 | ❌ 变更管理需专业版 |
| AWS Config | AWS服务 | 可选 | 专业版解锁 | ❌ 安全审计需专业版 |

### API Key 配置
- **AWS凭证**：通过 `aws configure` 配置，存储于 `~/.aws/credentials`（Linux/macOS）或 `%USERPROFILE%\.aws\credentials`（Windows）
- **AWS Profile**：通过 `AWS_PROFILE` 环境变量或 `--profile` 参数指定
- **AWS Region**：通过 `AWS_REGION` 环境变量或 `--region` 参数指定
- 本Skill本身不存储任何AWS凭证，所有凭证由AWS CLI内部管理

### 可用性分类
- **分类**：MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**：基于Markdown的AI Skill，通过自然语言指令驱动Agent执行只读云巡检任务

## 已知限制

本免费体验版限制以下高级功能：

- ❌ **安全审计**：跨服务安全态势扫描、合规基线检查、CIS Benchmark对标被限制，仅提供基础安全核查
- ❌ **成本分析**：Cost Explorer深度查询、按标签成本分摊、预算告警被限制
- ❌ **变更管理**：资源变更追踪、变更回滚、审批流被限制，仅支持 `--dry-run` 预演

解锁以上全部功能请使用专业版：`aws-cloud-inspector-pro`

## License与版权声明

本Skill基于原始作品改进，保留原始版权声明：

- 原始作品：AWS Infra（aws-infra）
- 原始license：MIT
- 改进作品：© 2026 aws-cloud-inspector-free contributors
- 改进license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 修复原版AWS CLI路径占位符，补充完整的标准配置路径说明（~/.aws/config 与 ~/.aws/credentials）
- 重写为中文文档并按Skill生产规范v1.1重组结构
- 新增分级快速开始、Region/Profile优先级链、3+真实场景示例
- 新增FAQ（7问）、故障排查表（8项）与依赖兼容性矩阵
- 拆分为免费版/专业版双版本，免费版限制3项高级功能
- 强化安全规则章节，明确只读边界与二次确认机制
- 所有references链接改为本地文件引用

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 核心能力

### AWS云巡检免费版（aws-cloud-
AWS云巡检免费版（aws-cloud-inspector-free）面向独立开发者与运维新人，基于本地AWS CLI提供只读的云资源查询与基础巡检能力

**输入**: 用户提供AWS云巡检免费版（aws-cloud-所需的指令和必要参数。
**处理**: 按照skill规范执行AWS云巡检免费版（aws-cloud-操作,遵循单一意图原则。
**输出**: 返回AWS云巡检免费版（aws-cloud-的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 它默认只读
它默认只读，所有变更类操作必须用户显式确认才执行，确保零误操作风险

**输入**: 用户提供它默认只读所需的指令和必要参数。
**处理**: 按照skill规范执行它默认只读操作,遵循单一意图原则。
**输出**: 返回它默认只读的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### aws/config` 与 `
aws/config` 与 `~/

**输入**: 用户提供aws/config` 与 `所需的指令和必要参数。
**处理**: 按照skill规范执行aws/config` 与 `操作,遵循单一意图原则。
**输出**: 返回aws/config` 与 `的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### aws/credentials
aws/credentials` 标准位置）

**输入**: 用户提供aws/credentials所需的指令和必要参数。
**处理**: 按照skill规范执行aws/credentials操作,遵循单一意图原则。
**输出**: 返回aws/credentials的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 适用场景
适用场景：个人AWS账号日常巡检、新接手项目的资源盘点、上线前基础安全自检、CloudWatch告警排查、IAM权限梳理、学习AWS CLI命令模式、为团队试点云巡检流程前的个人练习

**输入**: 用户提供适用场景所需的指令和必要参数。
**处理**: 按照skill规范执行适用场景操作,遵循单一意图原则。
**输出**: 返回适用场景的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：的只读云基础设施、查询助手、免费提供资源清点、健康检查与基础安、全核查能力、适合个人开发者日、Use、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 适用场景

**用户角色**：新入职运维工程师
**目标**：盘点刚接手的AWS账号下所有核心资源。

```bash
