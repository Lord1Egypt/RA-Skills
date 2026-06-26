[English](README.md) | [中文](README_CN.md)

# AWS 最佳实践研究 Skill

一个 Agent Skill，用于从 AWS 官方文档中研究、汇编任意 AWS 服务的最佳实践检查清单，并可选对线上资源进行合规评估。

## 问题背景

在为生产环境配置 AWS 服务时，工程师需要对照数十项最佳实践建议来验证配置是否合理。这些建议分散在 AWS 官方文档、Well-Architected Lens、Security Hub 控制项、re:Post 文章和官方博客中。手动收集和交叉比对这些来源既耗时又容易遗漏。

## 核心功能

1. **研究** — 通过 [aws-knowledge-mcp-server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) 搜索 AWS 官方文档，查找目标服务的最佳实践。
2. **汇编** — 将搜索结果整理成分类检查清单表，包含 5 个固定分类、来源标注和优先级。
3. **评估（可选）** — 如果用户提供了 AWS 凭证和资源标识符，则通过 AWS CLI 命令采集线上资源配置，逐项对比检查清单，生成包含 PASS/FAIL/WARN/N/A 状态的评估报告。

## 前置条件

| 依赖 | 用于 | 说明 |
|------|------|------|
| [aws-knowledge-mcp-server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) | 检查清单编译（步骤 1-7） | 提供 `aws___search_documentation`、`aws___read_documentation`、`aws___recommend` 工具 |
| AWS CLI (`aws`) | 仅线上评估（步骤 8） | 需配置对目标服务的只读访问权限 |
| AWS 凭证 + Region + 资源 ID | 仅线上评估（步骤 8） | 可通过环境变量、Profile 或凭证文件提供 |

## 工作流程概览

```
步骤 1: 确定目标 AWS 服务和评估范围
         ↓
步骤 2: 搜索文档（5 个顺序查询）
         ↓
步骤 3: 阅读关键文档页面（3-5 页）
         ↓
步骤 4: 提取并分类检查项
         ↓
步骤 5: 编译来源标注
         ↓
步骤 6: 生成检查清单输出（5 分类表格，保存到本地 .md 文件）
         ↓
步骤 7: 提供后续建议
         ↓
步骤 8: 线上资源评估（可选，仅在提供凭证时执行）
         ├── 8.1 准备环境
         ├── 8.2 采集资源配置
         ├── 8.3 逐项对比检查清单
         ├── 8.4 生成评估报告（保存到本地 .md 文件）
         └── 8.5 提供修复建议
```

## 检查清单分类

每份生成的检查清单都包含以下 5 个固定分类：

| # | 分类 | 示例检查项 |
|---|------|-----------|
| 1 | **高可用架构** | 集群模式、副本数量、Multi-AZ、可用区分布、节点类型 |
| 2 | **灾难恢复** | 自动/手动备份、保留策略、RPO/RTO、跨区域复制 |
| 3 | **故障转移规划** | Test Failover API、FIS 弹性测试、客户端超时配置、SNS 通知 |
| 4 | **安全配置** | 静态/传输加密、身份认证（AUTH/RBAC/IAM）、子网组、KMS |
| 5 | **其他** | 自动升级、监控、预留内存、连接池、成本标签 |

每个检查项包含：ID（内嵌优先级）、名称、描述、来源标注、优先级（High/Medium/Low）。

## 检查项 ID 格式

```
{分类前缀}-{序号}-{优先级}

示例：
  HA-01-hi   → 高可用架构，第 1 项，高优先级
  DR-02-md   → 灾难恢复，第 2 项，中优先级
  SEC-03-lo  → 安全配置，第 3 项，低优先级
  OT-05-md   → 其他，第 5 项，中优先级
```

## 来源标注对照表

| 缩写 | 来源 |
|------|------|
| `WA-REL` / `WA-RELn` | Well-Architected Lens — 可靠性支柱 |
| `WA-SEC` / `WA-SECn` | Well-Architected Lens — 安全性支柱 |
| `WA-PE` / `WA-PEn` | Well-Architected Lens — 性能效率支柱 |
| `WA-OE` / `WA-OEn` | Well-Architected Lens — 卓越运营支柱 |
| `WA-CO` | Well-Architected Lens — 成本优化支柱 |
| `Security Hub [{Service}.N]` | AWS Security Hub CSPM 控制项 |
| `re:Post` | AWS re:Post 知识中心文章 |
| `Official Docs` | 服务用户指南 / 官方文档 |
| `AWS Blog` | AWS 官方博客文章 |
| `Whitepaper` | AWS 白皮书 |

## 评估状态定义

执行线上评估时，每个检查项会获得以下状态之一：

| 状态 | 含义 |
|------|------|
| PASS | 资源配置达到或超出建议标准 |
| FAIL | 资源配置不满足建议标准 |
| WARN | 无法仅从基础设施层面完全验证（如客户端配置），或部分满足 |
| N/A | 该检查项不适用于当前资源 |

## 支持的服务

本 Skill 适用于 aws-knowledge-mcp-server 索引覆盖的**任意 AWS 服务**。以下服务已预置评估命令映射：

- **ElastiCache Redis / Valkey** — 完整的 CLI 命令集和检查项到字段的映射
- **Amazon RDS / Aurora** — 主要 describe 命令
- **Amazon MSK** — 集群和配置相关命令
- **Amazon DynamoDB** — 表、备份和全局表命令
- **Amazon EKS** — 集群、节点组、插件、Access Entries 和升级洞察命令（仅基础设施层；详见下方"容器/编排平台的评估范围边界"）

其他服务支持检查清单编译；线上评估命令根据该服务的 AWS CLI 参考文档动态推导。

## 容器/编排平台的评估范围边界

当目标服务是**容器或编排平台**（EKS、ECS、Fargate、App Runner、Elastic Beanstalk）时，本 Skill **仅关注 AWS 基础设施层** — 即通过 AWS API（`aws eks`、`aws ecs`、`aws ec2`、`aws iam` 等）可验证的检查项。

需要 `kubectl`、ECS Exec 或任何集群内/任务内检查才能验证的检查项**不在评估范围内**，属于专门的工作负载层评估 Skill。

### EKS 示例：范围内 vs 范围外

| 范围内（AWS API 可验证） | 范围外（需要 kubectl / 工作负载上下文） |
|--------------------------|------------------------------------------|
| 控制平面配置（K8s 版本、API 端点访问、日志） | Pod Disruption Budget (PDB) |
| 节点组配置（实例类型、扩缩容、AMI、AZ 分布） | Topology Spread Constraints |
| 集群网络（VPC、子网、安全组） | 存活/就绪/启动探针 |
| 插件（Add-on）安装及版本 | 容器资源 requests / limits |
| Secrets 信封加密（KMS） | Pod securityContext（runAsNonRoot、capabilities） |
| 认证模式和 Access Entries | Pod Security Admission (PSA) 命名空间标签 |
| 控制平面审计日志 | Network Policies（K8s 资源层面） |
| 集群删除保护 | Pod 优雅终止（terminationGracePeriodSeconds） |
| OIDC Provider 配置（用于 IRSA） | OPA Gatekeeper / Kyverno 策略 |
| GuardDuty EKS 保护 | Service Mesh（mTLS）配置 |

生成的检查清单末尾会包含一个**评估范围声明**，引导用户使用工作负载层评估 Skill 来覆盖范围外的检查项。

## 目录结构

```
aws-bestpractice-research/
├── SKILL.md                              # Skill 主定义文件（Agent 执行指令）
├── README.md                             # 英文版 PRD / 用户文档
├── README_CN.md                          # 本文件（中文版 PRD / 用户文档）
└── references/
    ├── search-queries.md                 # 5 个搜索查询模板 + 页面阅读优先级
    ├── output-template.md                # 检查清单输出格式规范
    ├── assessment-workflow.md              # 各服务评估命令和字段映射
    └── assessment-output-template.md       # 评估报告输出格式规范
```

## 使用示例

**仅生成检查清单：**
```
"帮我查找 ElastiCache Redis 的最佳实践"
"总结 Amazon MSK 的 HA/DR/安全最佳实践"
"编译一份 Aurora PostgreSQL 的检查清单"
```

**检查清单 + 线上评估：**
```
"帮我检查 us-west-2 区域的 ElastiCache Redis 集群 my-redis-cluster"
"评估一下我的 RDS 实例，region 是 ap-southeast-1，实例 ID 是 prod-db-01"
"检查我的 DynamoDB 表 orders-table 是否符合最佳实践"
```

## 关键设计决策

1. **顺序执行 MCP 请求** — 所有文档搜索和页面读取均逐一顺序执行，避免 aws-knowledge-mcp-server 的速率限制。速度较慢但可靠。

2. **5 分类固定结构** — 无论目标服务是什么，检查清单始终使用相同的 5 个分类，确保跨服务的一致评估框架。

3. **ID 内嵌优先级** — 检查项 ID 中的 `-hi`/`-md`/`-lo` 后缀支持快速视觉扫描，无需逐行阅读优先级列。

4. **评估为可选步骤** — 检查清单本身就是完整的、独立的交付物。线上评估仅在用户明确提供凭证和资源标识符时触发，Skill 永远不会因缺少凭证而阻塞。

5. **语言跟随用户** — 所有输出均使用与用户对话相同的语言（中文、英文等）。

6. **容器平台仅覆盖基础设施层** — 对于 EKS、ECS 等服务，本 Skill 严格限制评估范围在 AWS API 可验证的内容。工作负载层面的关注点（Pod、Task、容器）需要不同的工具（`kubectl`、ECS Exec）和应用上下文，本 Skill 不假设具有这些访问权限。

## 已知限制

- 依赖 aws-knowledge-mcp-server 的可用性；如果 MCP 服务器未配置，Skill 无法运行。
- MCP 服务器速率限制意味着文档采集需要约 30-60 秒（5 次查询 + 3-5 次页面读取）。
- 线上评估仅需目标服务的只读 IAM 权限，不需要写入权限。
- 评估字段映射仅为部分服务预置；其他服务的评估命令为动态推导。
- 客户端配置（连接池、重试逻辑、超时设置）在线上评估时只能标记为 WARN，因为需要应用层面的验证。
- 对于容器/编排平台（EKS、ECS），本 Skill 仅覆盖基础设施层最佳实践。工作负载层检查项（PDB、拓扑约束、探针、资源限制、Pod 安全）需要专门的工作负载评估 Skill 配合 `kubectl` 使用。
