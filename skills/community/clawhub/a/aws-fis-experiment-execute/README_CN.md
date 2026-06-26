[English](README.md) | [中文](README_CN.md)

# AWS FIS 实验执行

一个 Agent Skill，用于验证 CloudFormation Stack 已部署、运行 AWS FIS 实验、监控进度并生成结果报告。从已准备好的实验目录读取配置。

## 问题背景

在准备完成后运行 AWS FIS 实验仍然涉及手动验证步骤：

- **Stack 部署验证** — 运行实验前需要确认 CloudFormation Stack 已成功部署且处于 `CREATE_COMPLETE` 状态。
- **模板 ID 提取** — 必须从 Stack 输出中提取 FIS 实验模板 ID 才能启动实验。
- **安全至关重要** — FIS 实验影响**真实的生产资源**。未经确认、影响评估或 Stop Condition 就启动，可能造成意外损害。
- **实验期间的监控是手动的** — 轮询实验状态、查看 CloudWatch Dashboard、对比实际行为与预期行为必须同时进行。
- **结果收集分散** — 实验状态、Action 结果、时间和恢复验证需要从不同的 CLI 命令查询，必须手动汇总。

## 核心功能

1. **加载并验证** 已准备好的实验目录（来自 [aws-fis-experiment-prepare](../aws-fis-experiment-prepare/) 或手动创建）。支持**通过实验模板 ID 自动查找目录** — 如果用户提供模板 ID（如 `EXT1a2b3c4d5e6f7`），skill 会在当前目录下搜索匹配的实验目录。**从目录名提取模板 ID**（目录名以模板 ID 结尾）。
2. **读取 README.md** 提取实验元数据（场景、Region、AZ、时长、受影响资源、Stack 名称）。
3. **展示实验操作** — 通过 AWS CLI 查询已部署的 FIS 实验模板，提取并展示所有 action ID。日志收集始终启用。
4. **实验前资源健康检查** — 在启动任何日志收集或实验之前，验证 FIS 模板中每个目标资源（RDS、MSK、ElastiCache、EKS、EC2 等）均处于所属服务的健康基线状态。交互式会话下，不健康资源需要用户显式 override；非交互式会话下每 60 秒轮询一次、最长等待 10 分钟后中止。
5. **跨集群发现 EKS 应用并启动日志收集** — 加载 `app-service-log-analysis` skill，发现目标 Region 中所有 EKS 集群，为每个集群生成独立的 kubeconfig 文件（绝不覆盖 `~/.kube/config`），并行深度扫描所有可访问集群的应用依赖（环境变量、ConfigMap、Secret、ExternalName 等），在**实验启动前**启动后台 `kubectl logs -f`。如果 kubectl 不可用，跳过应用日志但仍通过 AWS CLI 收集托管服务日志。
6. **强制安全确认** — 展示清晰的影响警告（受影响资源、监控应用列表、托管服务日志状态、实验后基线时长），要求用户明确确认后才启动。
7. **启动实验** — 仅在用户明确确认后执行。
8. **监控进度** — 每 30-60 秒轮询实验状态，记录每次状态变更和各服务事件的时间戳。每次轮询同时显示各应用错误/警告计数和恢复信号。
9. **收集实验后基线并分析** — 实验结束后等待 3 分钟以捕获恢复行为，然后遵循 `app-service-log-analysis` 步骤 7-8 分析错误模式、峰值速率和恢复时间。
10. **保存结果报告** — 将实验结果写入**实验目录**中的 Markdown 文件，包含**按服务拆分的影响分析**和**应用日志分析**。终端仅打印简要摘要。

**注意：** 本 Skill **不会**部署基础设施。它仅验证 Stack 已部署，然后执行实验。

## 工作流程概览

```
步骤 1:  解析实验目录（从路径或模板 ID）
          ├── 提供完整路径 → 直接验证
          ├── 提供模板 ID → 在当前目录搜索以 *-{ID} 结尾的目录
          │   ├── 找到 1 个匹配 → 使用该目录
          │   ├── 找到多个匹配 → 让用户选择
          │   └── 未找到匹配 → 让用户提供完整路径
          ├── 从目录名提取模板 ID
          └── 验证必需文件
          ↓
步骤 2:  读取 README.md → 提取实验元数据
          ↓
步骤 3:  展示实验操作（用目录名中的模板 ID 查询 FIS API）
          ↓
步骤 3.5: 实验前资源健康检查（遍历 FIS 模板 targets）
          ├── 全部健康 → 继续
          ├── 交互式：警告用户，等待 proceed/abort/retry
          └── 非交互式：每 60 秒轮询一次，最多 10 分钟后中止
          ↓
步骤 4:  发现 EKS 应用 + 启动日志收集 [实验启动前完成]
          ├── 检查 kubectl 是否可用
          ├── kubectl 可用 → 加载 app-service-log-analysis skill，执行其：
          │   ├── Multi-Cluster EKS Discovery and Kubeconfig Isolation
          │   ├── Step 3（深度扫描应用依赖）
          │   ├── Step 3.5（托管服务日志检测）
          │   └── Step 4（实时日志收集）
          └── kubectl 不可用 → 跳过应用日志，仍收集托管服务日志
          ↓
步骤 5:  启动实验 [关键 — 需要用户明确确认]
          ├── 展示影响警告（资源、时长、Stop Condition、监控应用）
          ├── 用户确认 → 启动实验
          └── 用户拒绝 → 中止（清理日志）
          ↓
步骤 6:  监控实验 + 日志洞察
          ├── 前 5 分钟每 30 秒轮询，之后每 60 秒
          ├── 记录每次状态变更和 Action 转换的时间戳
          ├── 显示各应用错误/警告计数（无 kubectl 时仅显示托管服务日志）
          └── 提醒用户：查看 Dashboard
          ↓
步骤 7:  实验后基线（3 分钟）+ 停止日志收集 + 分析
          ├── 等待 3 分钟以捕获恢复行为
          └── 通过 app-service-log-analysis 步骤 7-8 分析
          ↓
步骤 8:  保存结果报告到实验目录 (YYYY-mm-dd-HH-MM-SS-{scenario}-experiment-results.md)
```

## 安全规则

| 规则 | 说明 |
|---|---|
| **绝不自动启动** | 启动实验前必须获得用户明确确认 |
| **展示每条命令** | 执行前先显示 CLI 命令 |
| **影响警告** | 启动前展示受影响资源、Region、AZ、时长 |
| **随时可中止** | 全流程提供中止说明 |
| **不静默删除** | 删除资源前必须获得用户确认 |
| **不部署基础设施** | 本 Skill 仅检查现有部署，不会部署基础设施 |
| **建议预审** | 建议用户在启动前审查所有文件 |

## Stack 状态处理

| 状态 | 操作 |
|---|---|
| `CREATE_COMPLETE` | Stack 已就绪，继续执行实验 |
| `UPDATE_COMPLETE` | Stack 已就绪（已更新），继续执行实验 |
| `CREATE_IN_PROGRESS` | Stack 仍在部署中，等待并重新检查 |
| `CREATE_FAILED` | Stack 部署失败，显示失败原因并中止 |
| `ROLLBACK_COMPLETE` | Stack 创建失败并已回滚，显示原因并中止 |
| `DELETE_COMPLETE` 或未找到 | Stack 不存在，通知用户先部署 |

## 实验状态值

| 状态 | 含义 |
|---|---|
| `initiating` | 实验正在启动 |
| `running` | 实验进行中 |
| `completed` | 实验成功完成 |
| `stopping` | 正在停止（用户或 Stop Condition 触发） |
| `stopped` | 完成前被停止 |
| `failed` | 实验失败 |

## 结果报告

实验到达终态后，结果报告保存为实验目录中的本地 Markdown 文件，文件名格式：

```
YYYY-mm-dd-HH-MM-SS-{scenario}-experiment-results.md
```

报告包含：
- 实验 ID、模板 ID、Stack 名称、最终状态
- 开始时间、结束时间、实际时长（所有时间戳使用 ISO 8601 格式带时区）
- 各 Action 结果表（含 Action ID、状态和持续时间）
- Stop Condition 告警状态表
- **各服务影响分析** — 针对每个受影响的服务，生成独立子章节，包含：
  - **关键时间线** — 仅列出与该服务相关的事件（时间戳使用 UTC 时间格式），方便直接对照 CloudWatch Dashboard 指标，无需离开当前章节
  - **观察结果** — 实验期间和实验后的观察行为
  - **关键发现** — 发生了什么、为什么、恢复行为如何
- **应用日志分析** — 针对每个监控的 EKS 应用：
  - 错误时间线（含时间戳和消息）
  - 关键错误模式（计数、首次和末次出现时间）
  - 关键错误日志样本（5-10 行）
  - 将应用错误与基础设施事件关联的洞察
- 恢复状态总结表
- 需要关注的问题（含修复命令）
- 原始日志文件位置（附录）
- 清理说明

终端打印简要摘要，包含各服务恢复状态。

## 必需文件

实验目录必须包含：

| 文件 | 必需 | 用途 |
|---|---|---|
| `cfn-template.yaml` | 是 | CloudFormation 模板（参考） |
| `README.md` | 是 | 实验概览，含 CFN Stack 名称 |

**关键：** `README.md` 必须包含 `**CFN Stack:** {STACK_NAME}` 字段，填入实际部署的 Stack 名称。此字段由 `aws-fis-experiment-prepare` 在成功部署后设置。

## 前置条件

- **AWS CLI** (`aws`) — FIS、CloudWatch、CloudFormation 操作。需要相关服务的权限。
- **kubectl**（可选）— 已配置目标 EKS 集群访问权限。如果不可用，跳过应用日志收集，但仍通过 AWS CLI 收集托管服务日志。
- **已准备好的实验目录** — 配置来源，来自 aws-fis-experiment-prepare 或手动创建。

## 关键 CLI 命令

### 检查 Stack 状态
```bash
aws cloudformation describe-stacks \
  --stack-name "{STACK_NAME}" \
  --region {REGION} \
  --query 'Stacks[0].{StackStatus: StackStatus, Outputs: Outputs}'
```

### 从 Stack 输出提取模板 ID
```bash
TEMPLATE_ID=$(aws cloudformation describe-stacks \
  --stack-name "{STACK_NAME}" \
  --query 'Stacks[0].Outputs[?OutputKey==`ExperimentTemplateId`].OutputValue' \
  --output text --region {REGION})
```

### 启动实验
```bash
aws fis start-experiment \
  --experiment-template-id "{TEMPLATE_ID}" \
  --region {REGION}
```

### 获取实验状态
```bash
aws fis get-experiment \
  --id "{EXPERIMENT_ID}" \
  --region {REGION} \
  --query 'experiment.state.status'
```

### 停止实验（紧急）
```bash
aws fis stop-experiment --id "{EXPERIMENT_ID}" --region {REGION}
```

## 清理指南

### CFN 清理（推荐）
```bash
aws cloudformation delete-stack --stack-name "{STACK_NAME}" --region {REGION}
aws cloudformation wait stack-delete-complete --stack-name "{STACK_NAME}" --region {REGION}
```

### 手动资源清理（如需要）
```bash
aws fis delete-experiment-template --id "{TEMPLATE_ID}" --region {REGION}
aws cloudwatch delete-alarms --alarm-names "FIS-StopCondition-{SCENARIO}-{SERVICE}" --region {REGION}
aws cloudwatch delete-dashboards --dashboard-names "FIS-{SCENARIO}" --region {REGION}
```

## 错误处理

| 错误 | 原因 | 解决方法 |
|---|---|---|
| README 中未找到 Stack 名称 | README 缺少 `**CFN Stack:**` 字段 | 检查是否使用最新版本的 aws-fis-experiment-prepare |
| Stack 未找到 (`ValidationError`) | Stack 不存在或已删除 | 先使用 aws-fis-experiment-prepare 部署 Stack |
| Stack 处于 `CREATE_FAILED` | Stack 部署失败 | 检查 Stack 事件了解失败原因，修复并重新部署 |
| `ExperimentTemplateId` 不在输出中 | Stack 模板缺少输出 | 检查 cfn-template.yaml 中的输出定义 |
| `AccessDeniedException` | 权限不足 | 检查 FIS、CloudWatch、CloudFormation 的 IAM 权限 |
| `ResourceNotFoundException` 目标未找到 | 标签资源不存在 | 验证资源标签与实验模板匹配 |
| 实验卡在 `initiating` | IAM 角色传播延迟 | 等待 30 秒再检查 |

## 使用示例

```
"Execute the FIS experiment in ./2025-03-27-10-30-00-az-power-interruption-my-cluster-EXT1a2b3c4d5e6f7/"
"Run the chaos experiment I just prepared"
"启动 FIS 实验"
"检查 Stack 是否已部署并运行实验"
"运行混沌实验，目录在 ./2025-03-27-rds-failover-prod-db-EXTa1b2c3d4e5f6g/"
"执行实验 EXT1a2b3c4d5e6f7"
"run experiment EXTabc123def456"
```

## 关键设计决策

1. **不部署 — 仅验证。** 本 Skill 假设 CloudFormation Stack 已部署（由 `aws-fis-experiment-prepare` 或手动部署）。它在执行前验证 Stack 状态。

2. **通过模板 ID 自动查找目录。** 当用户仅提供模板 ID（如 `EXT1a2b3c4d5e6f7`）时，skill 在当前工作目录搜索以该 ID 结尾的目录。这支持用户记住 prepare 阶段的模板 ID 但不记得完整目录名的常见场景。未找到匹配时，提示用户输入完整路径。

3. **从 README 获取 Stack 名称。** Stack 名称从实验目录的 README.md 中的 `**CFN Stack:**` 字段提取，确保与 prepare skill 的输出一致。

4. **明确确认不可妥协。** FIS 实验产生真实影响。Skill 绝不自动启动 — 始终展示具体资源细节的警告，要求用户输入确认。

5. **操作展示透明化。** 在继续前，skill 通过 `aws fis get-experiment-template` 查询已部署的 FIS 实验模板，提取所有 action ID 并展示。这让用户可以验证将运行哪些故障操作。

6. **应用发现在实验启动前完成。** 选择收集日志时，EKS 应用依赖在实验开始前发现，日志收集也在实验前启动。这防止实验开始后才找应用，导致早期日志被轮转或覆盖而丢失。

7. **日志收集始终启用。** 每次实验默认收集应用日志和托管服务日志。如果 kubectl 不可用，应用日志收集优雅降级 — 跳过应用日志，但托管服务日志（EKS 控制面、RDS 等）仍通过 AWS CLI 收集。无需用户选择。

8. **实验后基线自动收集。** 实验结束后，日志收集继续 3 分钟以捕获恢复行为。此基线始终收集 — 无需用户选择。

9. **监控中包含日志洞察。** 实验期间，每次轮询同时展示实验状态和各应用错误/警告计数，让操作者实时了解应用受影响情况。

10. **结果保存到文件。** 实验结果报告写入带时间戳的本地 Markdown 文件，终端输出保持简洁，同时保留完整记录。

11. **清理建议但不强制。** 实验结束后提供清理命令，但绝不在未确认的情况下执行。

## 目录结构

```
aws-fis-experiment-execute/
├── SKILL.md                              # Skill 主定义文件（Agent 执行指令）
├── README.md                             # 英文版 PRD / 用户文档
├── README_CN.md                          # 本文件（中文版）
└── references/
    ├── cli-commands.md                   # AWS CLI 命令参考
    └── report-template.md               # 实验结果报告模板
```

## 已知限制

- 需要 AWS CLI 并具有 FIS、CloudWatch、CloudFormation 权限。
- 需要 kubectl 已配置目标 EKS 集群访问权限（用于日志收集）。
- **不部署基础设施** — 期望 Stack 已部署。
- 监控依赖 CLI 轮询；实时 Dashboard 需要用户打开 CloudWatch 控制台。
- 应用日志收集使用 `kubectl logs -f`，仅能捕获运行中 Pod 的日志。实验期间被终止的 Pod 的日志可能丢失，除非启用了 Container Insights。
- 应用依赖自动发现依赖 Pod 环境变量和 ConfigMap 中的端点引用 — 使用服务发现或 DNS 解析的应用可能无法自动检测。

## 相关 Skill

- [aws-fis-experiment-prepare](../aws-fis-experiment-prepare/) — 生成并部署实验配置（本 Skill 之前运行）
- [aws-service-chaos-research](../aws-service-chaos-research/) — 为任意 AWS 服务研究混沌测试场景
- [app-service-log-analysis](../app-service-log-analysis/) — 独立的事后应用日志分析（本 Skill 现已集成实时日志分析）
- [eks-workload-best-practice-assessment](../eks-workload-best-practice-assessment/) — 评估 EKS 工作负载配置
