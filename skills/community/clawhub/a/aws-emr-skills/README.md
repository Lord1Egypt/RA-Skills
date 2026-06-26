[English](README_EN.md) | 中文

# AWS EMR Skills

面向 AI 编程助手的 AWS EMR 技能插件，支持 **EMR Serverless**、**EMR on EC2** 和 **EMR on EKS** 三种部署模式。

这不是一个独立的 CLI 工具。它是为 [OpenCode](https://github.com/opencode-ai/opencode)、[Claude Code](https://code.claude.com)、[OpenClaw](https://openclaw.ai)、[Cursor](https://cursor.com) 等 AI Agent 平台设计的技能（Skill），让 AI 助手能够通过自然语言帮你管理 EMR 集群、提交 Spark/Hive 作业、查看日志。支持 [40+ AI Agent 平台](https://github.com/vercel-labs/skills#supported-agents)。

> **SKILL.md** 是给 AI 读的技能描述文件，本 README 是给人读的。

## 功能特性

项目提供 **32 个 @tool 函数**，覆盖三种 EMR 部署模式：

| 模式 | 工具数 | 能力 |
|------|--------|------|
| **EMR Serverless** | 14 | 应用管理（列出/描述/启动/停止）、作业提交（Spark SQL / JAR / PySpark / Hive，同步/异步）、作业状态查询、取消、日志获取、SQL 结果读取 |
| **EMR on EC2** | 10 | 集群管理（列出/描述/终止）、Step 提交（Spark / PySpark / Hive）、Step 状态查询、取消、日志获取 |
| **EMR on EKS** | 8 | 虚拟集群管理（列出/描述/创建/删除）、作业提交（Spark / Spark SQL）、作业状态查询、取消、日志获取 |

其他特性：

- AWS 凭证通过 boto3 默认凭证链解析，不存储也不记录任何密钥
- 日志输出自动脱敏（屏蔽潜在的 AWS 凭证信息）
- 所有环境变量均为可选，按需校验

## 目录结构

```
aws-emr-skills/
├── SKILL.md                                    # AI Agent 技能描述（LLM 读取）
├── README.md                                   # 中文说明（本文件）
├── README_EN.md                                # English README
├── pyproject.toml                              # 项目元数据
├── .clawhubignore                              # ClawHub 发布排除规则
├── scripts/
│   ├── config/
│   │   └── emr_config.py                       # 统一配置管理（3 种模式）
│   ├── client/
│   │   └── boto_client.py                      # boto3 客户端工厂
│   ├── on_serverless/
│   │   ├── emr_serverless_cli.py               # @tool 函数入口（14 个）
│   │   ├── applications.py                     # 应用管理
│   │   └── jobs.py                             # 作业管理
│   ├── on_ec2/
│   │   ├── emr_on_ec2_cli.py                   # @tool 函数入口（10 个）
│   │   ├── clusters.py                         # 集群管理
│   │   └── steps.py                            # Step 管理
│   └── on_eks/
│       ├── emr_on_eks_cli.py                   # @tool 函数入口（8 个）
│       ├── virtual_clusters.py                 # 虚拟集群管理
│       └── job_runs.py                         # 作业管理
├── references/
│   ├── emr_serverless/
│   │   ├── application_guide.md                # 应用生命周期指南
│   │   └── job_guide.md                        # 作业提交与日志指南
│   ├── emr_on_ec2/
│   │   ├── cluster_guide.md                    # 集群管理指南
│   │   └── step_guide.md                       # Step 提交与日志指南
│   └── emr_on_eks/
│       ├── virtual_cluster_guide.md            # 虚拟集群管理指南
│       └── job_run_guide.md                    # 作业提交与日志指南
├── examples/                                   # 示例脚本（Serverless）
│   ├── sql_job.py
│   ├── pyspark_job.py
│   ├── jar_job.py
│   ├── hive_job.py
│   └── manage_demo.py
└── tests/                                      # 单元测试（49 个）
    ├── test_applications.py                    # Serverless 应用测试
    ├── test_jobs.py / test_jobs_*.py           # Serverless 作业测试
    ├── test_ec2_clusters.py                    # EC2 集群测试
    ├── test_ec2_steps.py                       # EC2 Step 测试
    ├── test_eks_virtual_clusters.py            # EKS 虚拟集群测试
    └── test_eks_job_runs.py                    # EKS 作业测试
```

## 安装方式

### 方式一：通过 npx skills 安装（推荐）

[skills](https://github.com/vercel-labs/skills) 是开放的 Agent Skills 安装工具，支持 [40+ AI Agent 平台](https://github.com/vercel-labs/skills#supported-agents)（OpenCode、Claude Code、OpenClaw、Cursor、Codex 等），一条命令即可安装：

```bash
npx skills add yhyyz/aws-emr-skills
```

可指定目标 Agent 平台：

```bash
# 安装到 Claude Code
npx skills add yhyyz/aws-emr-skills -a claude-code

# 安装到 OpenClaw
npx skills add yhyyz/aws-emr-skills -a openclaw

# 安装到 OpenCode
npx skills add yhyyz/aws-emr-skills -a opencode

# 安装到所有已检测到的 Agent
npx skills add yhyyz/aws-emr-skills --all
```

### 方式二：通过 ClawHub 安装

[ClawHub](https://clawhub.ai) 是 OpenClaw 的技能包管理平台：

```bash
npx clawhub@latest install aws-emr-skills
```

### 方式三：通过 Git 手动安装

```bash
# 克隆仓库
git clone https://github.com/yhyyz/aws-emr-skills.git

# 创建软链接到 skills 目录（以 Claude Code 为例）
ln -s "$(pwd)/aws-emr-skills" ~/.claude/skills/aws-emr-skills
```

### 依赖

确保 Python 环境中已安装 boto3：

```bash
pip install "boto3>=1.26.0"
```

Python 版本要求：**3.8+**

## 配置说明

所有环境变量均为可选。AWS 凭证通过 boto3 默认凭证链（环境变量 → `~/.aws/config` → IAM Role）自动解析。

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `AWS_REGION` | AWS 区域 | `us-east-1` |
| `EMR_SERVERLESS_APP_ID` | Serverless 应用 ID | — |
| `EMR_SERVERLESS_EXEC_ROLE_ARN` | Serverless 执行角色 ARN | — |
| `EMR_SERVERLESS_S3_LOG_URI` | Serverless 日志 S3 路径 | — |
| `EMR_CLUSTER_ID` | EC2 集群 ID | — |
| `EMR_EKS_VIRTUAL_CLUSTER_ID` | EKS 虚拟集群 ID | — |
| `EMR_EKS_EXEC_ROLE_ARN` | EKS 执行角色 ARN | — |

配置优先级：**环境变量 > 配置文件 > 内置默认值**

## 使用示例

安装完成后，在 AI 助手中用自然语言即可触发：

```
"列出所有 EMR Serverless 应用"
"提交一个 Spark SQL 作业到 EMR Serverless"
"查看 EMR 集群 j-XXXXX 的状态"
"给我的 EMR 集群添加一个 PySpark Step"
"取消正在运行的 EMR 作业"
"获取 EMR Step 的日志"
"创建一个 EMR on EKS 虚拟集群"
"提交 PySpark 作业到 EMR Serverless，脚本路径是 s3://my-bucket/scripts/etl.py"
```

AI 助手会自动识别意图，调用对应的工具函数完成操作。

## 开发与测试

```bash
# 运行全部测试（49 个单元测试）
pytest tests/ -v

# 运行特定模块的测试
pytest tests/test_applications.py -v        # Serverless 应用
pytest tests/test_ec2_clusters.py -v         # EC2 集群
pytest tests/test_eks_virtual_clusters.py -v # EKS 虚拟集群
```

## 许可证

MIT License
