# EKS 工作负载最佳实践评估

评估运行在 Amazon EKS 上的 Kubernetes 工作负载是否符合 K8s 官方文档和
[EKS 最佳实践指南](https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html) 的建议。

## 功能说明

此 skill 评估**工作负载层**的配置 — 需要 `kubectl` 和集群内检查才能验证的项目。
它与 [aws-best-practice-research](../aws-best-practice-research/) 互补，后者覆盖 EKS
**基础设施层**（控制平面、节点组、Addon 等）。

### 8 个评估维度

| # | 维度 | 前缀 | 检查内容 |
|---|------|------|----------|
| 1 | 工作负载配置 | WL- | 资源请求/限制、探针、PDB、HPA/VPA、拓扑分布 |
| 2 | 安全 | SEC- | PSA、Pod 安全上下文、RBAC、IRSA、网络策略、密钥管理 |
| 3 | 可观测性 | OBS- | Container Insights、日志、指标、链路追踪 |
| 4 | 网络 | NET- | Service 类型、Ingress/ALB、CoreDNS、VPC CNI、服务网格 |
| 5 | 存储 | STR- | PVC/StorageClass、CSI 驱动、加密、备份 |
| 6 | EKS 平台集成 | EKS- | Addon 版本、Karpenter/CA、Pod Identity、GuardDuty |
| 7 | CI/CD 与 GitOps | CICD- | 部署策略、镜像管理、ArgoCD/Flux |
| 8 | 镜像安全 | IMG- | ECR 扫描、CVE 发现、生命周期策略、基础镜像 |

### 核心特性

- **动态研究** — 每次执行时通过 context7（K8s 文档）和 aws-knowledge-mcp-server（EKS 文档）查询最新最佳实践
- **版本感知** — 检测 K8s/EKS 版本，自动过滤不适用的检查项（如 1.25+ 检查 PSA，<1.25 检查 PSP）
- **基准框架** — 最小检查项集合确保不遗漏关键检查
- **基础设施集成** — 可选调用 `aws-best-practice-research` 并合并结果
- **工作负载粒度** — 按 Deployment/StatefulSet 逐一报告检查结果

### 报告输出

1. **合规记分卡** — 各维度百分比得分及总体评级
2. **结构化审计报告** — 按维度分表，含 PASS/FAIL/WARN/N/A 状态
3. **详细 Markdown 报告** — 完整的逐工作负载检查结果、关键问题、修复建议

## 前置要求

- **aws-knowledge-mcp-server** — 用于 EKS 文档搜索
- **context7 MCP** — 用于 K8s 官方文档搜索
- **AWS CLI** — 已配置对目标 EKS 集群和 ECR 的访问权限
- **kubectl** — 已配置对目标 EKS 集群的访问权限

### 启用 EKS API 认证模式

部分评估检查和 FIS Pod 故障注入 Action 要求 EKS 集群支持 API 认证。将认证模式设置为 `API_AND_CONFIG_MAP`，同时兼容 `aws-auth` ConfigMap 和 EKS Access Entry：

```bash
aws eks update-cluster-config \
  --name <cluster-name> \
  --access-config authenticationMode=API_AND_CONFIG_MAP
```

> **为什么选两者兼容？** `API_AND_CONFIG_MAP` 保持与已有 `aws-auth` ConfigMap 映射的向后兼容，同时启用 FIS 和 CloudFormation（`AWS::EKS::AccessEntry`）所需的新版 Access Entry API。

### 授予 EC2 实例角色访问 EKS 的权限

如果从 EC2 实例（如 Cloud9、堡垒机）运行这些 Skills，实例的 IAM 角色需要 EKS 集群的访问权限。为 EC2 角色创建 EKS Access Entry：

```bash
aws eks create-access-entry \
  --cluster-name <cluster-name> \
  --principal-arn arn:aws:iam::<account-id>:role/<ec2-role-name> \
  --type STANDARD

aws eks associate-access-policy \
  --cluster-name <cluster-name> \
  --principal-arn arn:aws:iam::<account-id>:role/<ec2-role-name> \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy \
  --access-scope type=cluster
```

> 请根据实际需要调整访问策略和范围。此处使用 `AmazonEKSClusterAdminPolicy` + cluster 范围仅为演示 — 生产环境建议使用更严格的策略（如 `AmazonEKSEditPolicy` 并限定到特定命名空间）。

## 使用方式

使用以下触发短语：
- "评估我的 EKS 工作负载是否符合最佳实践"
- "检查 K8s 最佳实践"
- "审计 EKS 集群中的容器工作负载"
- "评估 Pod 安全配置"

需要提供：
- 集群名称和 AWS Region
- （可选）指定要评估的 namespace 或工作负载
- （可选）是否包含基础设施层评估

## 文件结构

```
eks-workload-best-practice-assessment/
  SKILL.md                              # 主工作流
  README.md                             # 英文说明
  README_CN.md                          # 本文件
  references/
    check-dimensions.md                 # 8 个维度及基准检查项
    kubectl-assessment-commands.md           # kubectl 命令参考
    search-queries.md                   # context7 + aws-knowledge-mcp 查询清单
    output-template.md                  # 详细报告模板
    assessment-output-template.md            # 结构化评估模板
    scorecard-template.md               # 记分卡模板
```

## 相关 Skill

- [aws-best-practice-research](../aws-best-practice-research/) — 基础设施层评估（控制平面、节点组、Addon）
- [aws-service-chaos-research](../aws-service-chaos-research/) — 混沌工程场景研究
- [aws-fis-experiment-prepare](../aws-fis-experiment-prepare/) — FIS 实验配置生成
