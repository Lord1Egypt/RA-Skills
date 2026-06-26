# EKS Workload Best Practice Assessment

Assess Kubernetes workloads running on Amazon EKS against best practices from the K8s official
documentation and the [EKS Best Practices Guide](https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html).

## What It Does

This skill evaluates **workload-level** configurations — the items that require `kubectl` and
in-cluster inspection. It complements [aws-best-practice-research](../aws-best-practice-research/)
which covers the EKS **infrastructure layer** (control plane, node groups, addons, etc.).

### 8 Assessment Dimensions

| # | Dimension | Prefix | What It Checks |
|---|-----------|--------|----------------|
| 1 | Workload Configuration | WL- | Resource requests/limits, probes, PDB, HPA/VPA, topology spread |
| 2 | Security | SEC- | PSA, pod security context, RBAC, IRSA, NetworkPolicy, secrets |
| 3 | Observability | OBS- | Container Insights, logging, metrics, tracing |
| 4 | Networking | NET- | Service types, Ingress/ALB, CoreDNS, VPC CNI, service mesh |
| 5 | Storage | STR- | PVC/StorageClass, CSI drivers, encryption, backup |
| 6 | EKS Platform Integration | EKS- | Addon versions, Karpenter/CA, Pod Identity, GuardDuty |
| 7 | CI/CD & GitOps | CICD- | Deployment strategy, image management, ArgoCD/Flux |
| 8 | Image Security | IMG- | ECR scanning, CVE findings, lifecycle policies, base images |

### Key Features

- **Dynamic research** — queries latest best practices from context7 (K8s docs) and aws-knowledge-mcp-server (EKS docs) each time
- **Version-aware** — detects K8s/EKS version and filters checks accordingly (e.g., PSA for 1.25+, PSP for <1.25)
- **Baseline framework** — minimum check set ensures no critical area is missed
- **Infrastructure integration** — optionally invokes `aws-best-practice-research` and merges results
- **Per-workload granularity** — reports findings for each Deployment/StatefulSet individually

### Report Outputs

Reports are saved directly to local markdown files (not printed to terminal). File names
use the format `YYYY-mm-dd-HH-MM-SS-{cluster}-{type}.md`:

1. **Compliance Scorecard** → `{timestamp}-{cluster}-scorecard.md`
2. **Structured Assessment Report** → `{timestamp}-{cluster}-assessment-report.md`
3. **Detailed Markdown Report** → `{timestamp}-{cluster}-detailed-report.md`

A brief summary (file paths, overall score, PASS/FAIL/WARN counts) is printed to the terminal.

## Prerequisites

- **aws-knowledge-mcp-server** — for EKS documentation search
- **context7 MCP** — for K8s official documentation
- **AWS CLI** — configured with access to the target EKS cluster and ECR
- **kubectl** — configured to access the target EKS cluster
- **jq** — for parsing JSON output from AWS CLI and kubectl commands

### Enable EKS API Authentication Mode

Some assessment checks and FIS Pod fault injection actions require the EKS cluster to support API-based authentication. Set the authentication mode to `API_AND_CONFIG_MAP` so that both `aws-auth` ConfigMap and EKS Access Entry work:

```bash
aws eks update-cluster-config \
  --name <cluster-name> \
  --access-config authenticationMode=API_AND_CONFIG_MAP
```

> **Why both?** `API_AND_CONFIG_MAP` maintains backward compatibility with existing `aws-auth` ConfigMap mappings while enabling the newer Access Entry API used by FIS and CloudFormation (`AWS::EKS::AccessEntry`).

### Grant EC2 Instance Role Access to EKS

If you run these skills from an EC2 instance (e.g., Cloud9, bastion host), the instance's IAM role needs permission to interact with the EKS cluster. Create an EKS Access Entry for the EC2 role:

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

> Adjust the access policy and scope as needed. `AmazonEKSClusterAdminPolicy` with cluster scope is shown for simplicity — in production, use a more restrictive policy (e.g., `AmazonEKSEditPolicy` scoped to specific namespaces).

## Usage

Trigger this skill with phrases like:
- "Assess my EKS workloads against best practices"
- "Check K8s best practices for my cluster"
- "Assess container workloads in my EKS cluster"
- "Evaluate pod security configuration"

Provide:
- Cluster name and AWS region
- (Optional) Specific namespaces or workloads to assess
- (Optional) Whether to include infrastructure-layer assessment

## File Structure

```
eks-workload-best-practice-assessment/
  SKILL.md                              # Main workflow
  README.md                             # This file
  README_CN.md                          # Chinese version
  references/
    check-dimensions.md                 # 8 dimensions with baseline check items
    kubectl-assessment-commands.md           # kubectl command reference
    search-queries.md                   # context7 + aws-knowledge-mcp queries
    output-template.md                  # Detailed report template
    assessment-output-template.md            # Structured assessment template
    scorecard-template.md               # Scorecard template
```

## Related Skills

- [aws-best-practice-research](../aws-best-practice-research/) — Infrastructure-layer assessment (control plane, node groups, addons)
- [aws-service-chaos-research](../aws-service-chaos-research/) — Chaos engineering scenarios for resilience testing
- [aws-fis-experiment-prepare](../aws-fis-experiment-prepare/) — FIS experiment configuration generation
