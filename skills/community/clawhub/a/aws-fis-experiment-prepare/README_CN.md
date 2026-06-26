[English](README.md) | [中文](README_CN.md)

# AWS FIS 实验准备

一个 Agent Skill，用于生成运行 AWS FIS（Fault Injection Service）实验所需的全部配置文件，然后**通过 CloudFormation 部署并自动修复迭代**，直到 Stack 创建成功。

## 问题背景

手动准备 AWS FIS 实验涉及多个容易出错且繁琐的步骤：

- **资源与 Action 的兼容性不直观** — 例如 `aws:rds:failover-db-cluster` 需要 Aurora 集群（`aws:rds:cluster`），不支持独立 RDS 实例。不匹配问题往往在实验启动时才被发现，浪费了之前所有的准备工作。
- **多个文件必须生成且保持一致** — 实验模板 JSON、IAM 策略、CloudFormation 模板、CloudWatch 告警、Dashboard 以及预期行为文档都引用相同的资源 ARN 和参数。
- **CloudFormation 部署经常失败** — 属性校验错误、IAM 传播延迟、Region 资源限制等需要反复调试，手动处理非常耗时。
- **Scenario Library 场景很复杂** — 复合场景（如 AZ 电力中断）编排多个 sub-action，有特定的标签要求和目标类型，容易配错。
- **Scenario Library 模板无法通过 API 生成** — 与自定义单个 FIS Action 不同，4 个 Scenario Library 场景没有 CLI/API 命令来自动生成实验模板。JSON 模板必须从 AWS 文档中提取。

## 核心功能

1. **识别场景** — 判断用户需要 Scenario Library 预定义场景（AZ 电力中断、AZ 应用慢速等）还是自定义单个 FIS Action。
2. **读取 Scenario Library 文档** — 对于 Scenario Library 场景，读取 AWS 文档页面以提取 JSON 实验模板（这些模板无法通过 API 生成）。文档 URL：
   - [AZ 电力中断](https://docs.aws.amazon.com/en_us/fis/latest/userguide/az-availability-scenario.html)
   - [AZ 应用慢速](https://docs.aws.amazon.com/en_us/fis/latest/userguide/az-application-slowdown-scenario.html)
   - [跨 AZ 流量慢速](https://docs.aws.amazon.com/en_us/fis/latest/userguide/cross-az-traffic-slowdown-scenario.html)
   - [跨 Region 连接](https://docs.aws.amazon.com/en_us/fis/latest/userguide/cross-region-scenario.html)
3. **发现目标资源** — 查询用户实际的 AWS 资源，收集目标标识。对于 ElastiCache 集群模式启用的复制组，通过 CloudWatch `IsMaster` 指标检测分片主备分布（因为 `CurrentRole` 在集群模式启用时返回 null）。
4. **验证兼容性** — 通过 AWS CLI 检查实际资源（如 `describe-db-instances`、`describe-db-clusters`），与 FIS Action 的 `resourceType` 要求交叉校验，在生成任何文件之前完成。
5. **确定监控配置** — 默认使用 `source: "none"`（不绑定 Stop Condition 告警）。仅在用户明确提供告警时才创建 CloudWatch Alarm。生成包含各服务可用性、性能和错误/延迟指标的综合 CloudWatch Dashboard。
6. **读取 CFN 资源文档** — 在生成 CFN 模板之前，读取 `AWS::FIS::ExperimentTemplate` CloudFormation 文档，确保模板使用当前的属性 schema。
7. **生成配置文件** — 生成包含 2 个文件的自包含目录：CFN 模板和 README。
8. **自动修复部署** — 部署 CFN 模板，若部署失败则自动分析错误、修复模板、删除失败 Stack、重试（最多 5 次）。
9. **目录重命名追加模版 ID** — 部署成功后，将实验模版 ID 追加到输出目录名（如 `2026-04-11-pod-net-pktloss-payment-redis-EXT1a2b3c4d5e6f7/`），方便用户查找。

## 支持的场景

### Scenario Library（复合、多 Action）

| 场景 | 主要 Sub-Action |
|---|---|
| AZ 可用性：电力中断 | EC2 停止、RDS 故障转移、ElastiCache AZ 断电、EBS 暂停、网络中断 |
| AZ：应用慢速 | Pod 网络延迟、EBS 延迟、网络中断 |
| 跨 AZ：流量慢速 | 跨 AZ 网络延迟 / 丢包 |
| 跨 Region：连接 | 跨 Region 网络中断 |
| EC2 压力测试 | 实例故障、CPU、内存、磁盘、网络延迟 |
| EKS 压力测试 | Pod 删除、CPU、磁盘、内存、网络延迟 |
| EBS 延迟 | 持续、递增、间歇、递减 |

### 自定义 FIS Action（单个 Action）

任何有效的 FIS Action ID，例如：
- `aws:rds:failover-db-cluster`
- `aws:ec2:stop-instances`
- `aws:elasticache:replicationgroup-interrupt-az-power`
- `aws:eks:pod-network-latency`

### 服务专属指南（无原生 FIS Action 的服务通过 SSM Automation 实现）

对于**没有原生 FIS Action** 的 AWS 服务，Skill 使用 `aws:ssm:start-automation-execution`
调用 SSM Automation Runbook，直接调用目标服务的 API。SSM Automation 文档和 FIS 实验模板
都在单个 CFN Stack 中部署。

当前已支持：
- **Amazon MSK** — `kafka:RebootBroker` 测试 Kafka 消费者/生产者的弹性。详见 `references/msk-guide.md`。
- **Amazon ElastiCache**（主节点重启）— `elasticache:RebootCacheCluster` 测试 Redis/Valkey 连接池和重试逻辑的弹性。详见 `references/elasticache-redis-guide.md`。
- **Amazon ElastiCache**（复制组主备切换）— `elasticache:TestFailover` 触发指定分片的自动故障转移，将副本提升为主节点。同时支持集群模式禁用和集群模式启用。详见 `references/elasticache-redis-guide.md`。

其他服务（Redshift、Neptune、OpenSearch、MemoryDB 等）可按相同模式扩展——
`ssm-auto-<service>-<operation>` slug 命名规范和双角色 IAM 设计已记录在
`references/slug-conventions.md` 和 `references/msk-guide.md` 中。

## 输出目录结构

```
./{yyyy-mm-dd-HH-MM-SS}-{scenario-slug}-{target-slug}[-{context-slug}]-{TEMPLATE_ID}/
├── README.md                          # 实验概览和执行说明
└── cfn-template.yaml                  # 全包 CloudFormation 模板
```

可选的 `{context-slug}` 用于区分相同场景和 target 但不同下游服务的实验
（如 `redis`、`msk`）。适用于网络故障注入 Action（延迟、丢包、端口黑洞）。

`{TEMPLATE_ID}` 是 FIS 实验模版 ID（如 `EXT1a2b3c4d5e6f7`），在 CFN 部署成功后追加到目录名，方便用户查找。

场景 slug 使用标准缩写（如 `pod-net-pktloss`、`az-power-int`、`ec-rg-az-power`），
以确保 CFN Stack 名称和资源名称简洁可读。完整缩写表和命名规则见
`references/slug-conventions.md`。

## 资源-Action 兼容性验证

本 Skill 的关键特性：在生成任何文件**之前**验证资源兼容性。

| FIS Action | 要求的 resourceType | 不兼容的情况 |
|---|---|---|
| `aws:rds:failover-db-cluster` | `aws:rds:cluster` | 独立 RDS 实例（非 Aurora） |
| `aws:rds:reboot-db-instances` | `aws:rds:db` | Aurora 集群（应使用 failover） |
| `aws:elasticache:replicationgroup-interrupt-az-power` | `aws:elasticache:replicationgroup` | 独立 ElastiCache 节点 |
| `aws:ec2:stop-instances` | `aws:ec2:instance` | Spot 实例（可能终止而非停止） |
| `aws:eks:pod-network-latency` | `aws:eks:pod` | 缺少所需插件的集群 |

发现不兼容时，Skill 会解释不匹配的原因并建议替代方案。

## 自动修复 CFN 部署

生成文件后，Skill 立即部署 CloudFormation 模板：

1. **权限预检** — 检查调用者 IAM 策略中 CreateStack/UpdateStack/DeleteStack 是否有 `cloudformation:RoleArn` 条件。如有，提取 CFN 服务角色 ARN 并在后续所有 CFN 命令中自动添加 `--role-arn`。如未找到条件，使用 IAM 策略模拟（`simulate-principal-policy`）验证调用者是否有 CloudFormation 权限 — 权限不足时提前终止并提供指导。
2. **验证** — `aws cloudformation validate-template`
3. **部署** — `aws cloudformation deploy --capabilities CAPABILITY_NAMED_IAM`（如需要则带 `--role-arn`）
4. **失败时** — 从 Stack 事件提取错误、分析根因、修复模板、删除失败 Stack、重试
5. **最多 5 次重试** — 仍然失败则报告所有尝试过的修复
6. **成功后** — 用 Stack 输出中的真实 ARN 更新本地文件

## 前置条件

- **AWS CLI** (`aws`) — 资源发现、FIS Action 验证、CFN 部署。需要 FIS、IAM、CloudWatch、CloudFormation 权限。
- [**aws-knowledge-mcp-server**](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) — Scenario Library 文档研究（`aws___search_documentation`、`aws___read_documentation`）
- **jq** — JSON 处理（`scripts/` 下的脚本依赖）

**EKS Pod 故障注入前置条件：**
- EKS 集群认证模式必须为 **`API_AND_CONFIG_MAP`** 或 **`API`**
  - 检查：`aws eks describe-cluster --name {CLUSTER} --query 'cluster.accessConfig.authenticationMode'`
  - 如果模式为 `CONFIG_MAP`，用户需先更新集群到 `API_AND_CONFIG_MAP`
- K8s RBAC 资源（ServiceAccount、Role、RoleBinding）通过 Lambda-backed CFN Custom Resource **自动管理** — 无需手动 `kubectl apply`
- CFN 模板包含一个 Lambda 函数，幂等创建 K8s RBAC 资源（先检查是否已存在，存在则跳过）。Lambda 使用 `botocore.signers.RequestSigner` 并携带 `x-k8s-aws-id` header 生成 EKS token — 这是 EKS API server 认证所必需的（普通的 `sts_client.generate_presigned_url` 缺少此 header，会导致 401 Unauthorized）。`ensure_resource` 辅助函数包含日志记录和错误检查，防止静默失败。
- RBAC 资源使用**固定标准化名称**（`fis-sa`、`fis-experiment-role`、`fis-experiment-role-binding`），同一 namespace 下所有 FIS 实验共享
- 删除 Stack 时**不会删除** RBAC 资源 — 它们是共享的，可能被其他实验使用
- **强制要求：** 使用任何 `aws:eks:pod-*` Action 时，必须遵循 `references/eks-pod-action-guide.md`

### 创建 CloudFormation 服务角色

本 Skill 通过 CloudFormation 部署 Stack，其中包含 IAM 角色、CloudWatch 资源和 FIS 实验模板。建议创建专用的 CloudFormation 服务角色，而不是使用自身的宽泛权限。

参见配置指南：https://panlm.github.io/others/cfn-service-role-for-fis-experiment-setup-guide/

部署 Stack 时传入 `--role-arn`：

```bash
aws cloudformation deploy \
  --template-file cfn-template.yaml \
  --stack-name <stack-name> \
  --role-arn arn:aws:iam::<account-id>:role/CloudFormationFISServiceRole \
  --capabilities CAPABILITY_NAMED_IAM \
  --region <region>
```

> **好处：** 调用者只需 `cloudformation:*` 和 `iam:PassRole` 权限，所有资源创建都委托给服务角色，缩小影响范围。

## 工作流程概览

```
步骤 1: 识别场景 + Region
         ↓
步骤 2: 发现目标资源
         ├── Scenario Library → 必须先读取 AWS 文档（JSON 模板无法通过 API 获取）
         └── 自定义 FIS Action → 通过 `aws fis get-action` 查询
         ↓
步骤 2.5: EKS Pod Action 设置（如适用）
         └── CFN 模板自动包含 Lambda + Custom Resource 管理 K8s RBAC
         ↓
步骤 3: 验证资源-Action 兼容性 [关键门控]
         ├── 兼容 → 继续
         └── 不兼容 → 建议替代方案 → 用户确认或中止
         ↓
步骤 4: 确定监控配置（Stop Condition + Dashboard 指标）
         ↓
步骤 5: 在输出目录中生成配置文件（README.md + cfn-template.yaml）
         ↓
步骤 5.5: CFN 权限预检（检测 cloudformation:RoleArn 条件）
         ↓
步骤 6: 部署 CFN 模板并自动修复（最多 5 次重试）
         ├── ExperimentName 包含随机后缀 → 所有物理资源名全局唯一
         ├── 成功 → 用真实 ARN 更新本地文件
         └── 失败 → 报告错误和所有尝试过的修复
         ↓
步骤 7: 重命名输出目录（追加实验模版 ID，方便用户查找）
```

## 使用示例

```
"Prepare an AZ Power Interruption experiment for us-east-1a"
"Create FIS experiment for aws:rds:failover-db-cluster targeting my Aurora cluster"
"准备 FIS 实验，测试 AZ 断电对 EKS 和 RDS 的影响"
"测试 AZ 断电对 RDS 的影响"
"生成 EC2 CPU 压力测试的混沌实验配置"
"为 ap-southeast-1 的 ElastiCache 故障转移配置故障注入测试"
"只测试 AZ 断电对 EC2 和 ElastiCache 的影响"
"重启 MSK broker，测试 Kafka 消费者的弹性"
"准备 MSK broker 重启的故障注入实验"
"测试 ElastiCache Redis 在 us-west-2a 的故障转移"
"重启 Redis 主节点，测试连接池弹性"
"准备 ElastiCache Redis 主节点重启的实验"
"测试 ElastiCache 复制组分片 0001 的主备切换"
"准备 ElastiCache 复制组主备切换实验"
```

## 关键设计决策

1. **先验证再生成。** 在生成任何文件之前检查资源-Action 兼容性。避免常见的反模式：生成完整配置、部署 Stack，结果在实验启动时才发现不匹配。

2. **Scenario Library 模板来自文档。** 4 个 Scenario Library 场景（AZ 电力中断、AZ 应用慢速、跨 AZ 流量慢速、跨 Region 连接）无法通过 FIS API 生成。Skill 读取 AWS 官方文档页面提取 JSON 实验模板，这是正确的多 Action 模板结构的唯一权威来源。

3. **自动修复部署循环。** CFN 错误自动分析并修复，而非报告给用户。目标是交付一个可用的、已部署的实验模板，不只是可能能用的文件。

4. **全包 CFN 模板。** `cfn-template.yaml` 包含 IAM 角色、告警、Dashboard 和实验模板。一次 `cloudformation deploy` 即可完成所有部署。

5. **本地文件保持同步。** 部署成功后，`README.md` 会用真实 ARN 和 Stack 输出更新，使目录成为已部署实验的准确记录。

6. **绝不启动实验。** 本 Skill 只准备和部署基础设施。启动实际实验由 [aws-fis-experiment-execute](../aws-fis-experiment-execute/) 或用户手动完成。

7. **目录名包含实验模版 ID。** 部署成功后，输出目录名自动追加实验模版 ID（如 `EXT1a2b3c4d5e6f7`），用户可以直接通过目录名识别对应的实验模版。

8. **EKS RBAC 通过 CFN Custom Resource 管理。** EKS Pod Action 所需的 K8s RBAC 资源（ServiceAccount、Role、RoleBinding）由 Lambda-backed CFN Custom Resource 自动管理。使用固定标准化名称（`fis-sa`、`fis-experiment-role`、`fis-experiment-role-binding`），同一 namespace 下所有实验共享。Lambda 执行幂等创建（已存在则跳过），删除 Stack 时不会删除 RBAC 资源，因为其他实验可能仍在使用。Lambda 使用 `botocore.signers.RequestSigner` 并携带 `x-k8s-aws-id` header 生成 EKS bearer token，这是 EKS API server 正确认证所必需的。

9. **AZ 电力中断：每个 AZ 一个 Stack，标签共享。** 目标 AZ 在实验模板的多个位置写死（filter、action 参数）。要测试不同 AZ 需删除 Stack 重建。资源标签（`AzImpairmentPower`）不区分 AZ — 由实验模板内部的 AZ filter 处理。标签通过同一 CFN Stack 中的 Lambda-backed Custom Resource 打上，EC2 Instance Profile 无需额外权限。详见 `references/az-power-interruption-guide.md`。

10. **AZ 电力中断：按服务范围裁剪子动作。** 当用户提到特定服务（如"测试 AZ 断电对 RDS 的影响"），实验模板仅包含与该服务相关的子动作，而非全部 10 个子动作。这可以防止对同一 AZ 中其他业务应用的意外影响。强制性基础设施子动作（网络中断、ARC Zonal Autoshift）始终包含，除非用户明确排除。Agent 在生成文件前会与用户确认最终的子动作列表。

11. **默认实验持续时间为 10 分钟。** 所有实验场景和子动作的默认持续时间为 `PT10M`，除非用户另行指定。这比 AWS 文档默认的 `PT30M` 更短，但对大多数验证场景已经足够，同时缩短了影响范围窗口。时间相关参数（如 ARC Zonal Autoshift 时间）按比例调整。

12. **服务专属指南（无原生 FIS Action 的服务）。** Amazon MSK 没有原生 FIS Action，Skill 使用 `aws:ssm:start-automation-execution` 调用 SSM Automation Runbook，直接调用 `kafka:RebootBroker`。这需要双角色 IAM 模式：FIS 实验角色（信任 `fis.amazonaws.com`）将 SSM Automation 角色（信任 `ssm.amazonaws.com`）传递给 SSM，后者拥有 MSK API 权限。SSM 文档和 FIS 实验模板都在单个 CFN Stack 中部署。详见 `references/msk-guide.md`。其他服务（Redshift、Neptune、OpenSearch 等）可按相同模式以独立的服务专属指南扩展。

13. **Redis 集群实验前分片角色检测。** 对于 ElastiCache 集群模式启用的复制组，`describe-replication-groups` 返回的 `CurrentRole` 为 null。Skill 使用 CloudWatch `IsMaster` 指标检测每个节点的角色，并将分片分布记录为实验前基线。这使得 README 的"预期行为"部分能够精确描述：哪些分片的主节点在目标 AZ 中（会发生故障转移），哪些分片只会丢失副本（不会故障转移）。

## 目录结构

```
aws-fis-experiment-prepare/
├── SKILL.md                              # Skill 主定义文件（Agent 执行指令）
├── README.md                             # 英文版 PRD / 用户文档
├── README_CN.md                          # 本文件（中文版）
├── references/
│   ├── output-format.md                  # 目录布局、slug 命名、README 模板
│   ├── cfn-base-template.md              # CFN 骨架（Parameters、IAM Role、Dashboard、FIS Template、Outputs）
│   ├── slug-conventions.md               # 场景/context slug 缩写表、资源命名、长度预算
│   ├── eks-pod-action-guide.md           # EKS Pod Action 指南（Lambda + Custom Resource 管理 K8s RBAC、认证模式、memory stress 计算）
│   ├── az-power-interruption-guide.md    # AZ 电力中断场景指南（标签策略、权限、设计决策）
│   ├── elasticache-redis-guide.md        # ElastiCache Redis/Valkey 指南（原生 AZ 断电 action + 通过 SSM 实现主节点重启 + 复制组主备切换）
│   └── msk-guide.md                      # Amazon MSK FIS 实验指南（通过 SSM Automation 实现 broker 重启）
└── scripts/
    ├── precheck-cfn-permissions.sh       # 检测是否需要 CFN 服务角色
    ├── deploy-with-retry.sh              # 验证 + 部署 + 失败时删除
    └── rename-output-dir.sh              # 将 FIS 模板 ID 追加到目录名
```

## 已知限制

- 依赖具有足够权限的 AWS CLI 访问（FIS、IAM、CloudWatch、CloudFormation）。
- Scenario Library 文档在执行时读取；新增场景需要重新运行。
- 自动修复循环处理常见 CFN 错误，但可能无法解决权限或账号级配额限制。
- 复合场景要求资源预先打好场景专用标签（如 `AzImpairmentPower: StopInstances`）。
- 顺序 MCP 文档研究调用需要约 10-20 秒。

## 相关 Skill

- [aws-service-chaos-research](../aws-service-chaos-research/) — 为任意 AWS 服务研究混沌测试场景（本 Skill 之前运行）
- [aws-fis-experiment-execute](../aws-fis-experiment-execute/) — 部署并运行已准备好的实验（本 Skill 之后运行）
- [eks-workload-best-practice-assessment](../eks-workload-best-practice-assessment/) — 评估 EKS 工作负载配置
