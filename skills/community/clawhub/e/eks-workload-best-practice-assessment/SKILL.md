---
name: eks-workload-best-practice-assessment
description: >
  Use when assessing or reviewing Kubernetes workloads running on Amazon EKS
  for best practice compliance, including pod configuration, security posture, observability,
  networking, storage, image security, and CI/CD practices. Requires kubectl and awscli access
  to the target cluster. Triggers on "assess my EKS workloads", "check k8s best practices",
  "assess container workloads", "evaluate pod security", "workload compliance check",
  "EKS workload assessment", "检查 K8s 工作负载", "评估容器最佳实践",
  "审计 EKS 应用", "检查 Pod 配置", "容器安全评估", "工作负载合规检查".
---

# EKS Workload Best Practice Assessment

Assess Kubernetes workloads on Amazon EKS against best practices from K8s official documentation
and the EKS Best Practices Guide. Covers 8 dimensions: workload configuration, security,
observability, networking, storage, EKS platform integration, CI/CD, and image security.

## Prerequisites

This skill requires:

- **[aws knowledge mcp server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server)** tools:
  - `aws___search_documentation` — search AWS documentation
  - `aws___read_documentation` — read full documentation pages
  - `aws___recommend` — get related documentation
- **[context7 MCP](https://github.com/upstash/context7)** tools:
  - `context7_resolve-library-id` — resolve K8s library ID
  - `context7_query-docs` — query K8s documentation
- **AWS CLI** (`aws`) — configured with read access to the target EKS cluster and ECR
- **kubectl** — configured to access the target EKS cluster
- **jq** — for parsing JSON output from AWS CLI and kubectl commands

## Scope Boundary

This skill focuses on **workload-level** checks — items that require `kubectl` or in-cluster
inspection. It complements `aws-best-practice-research` which covers the **infrastructure layer**
(control plane, node groups, addons, etc.).

| This Skill (Workload Layer) | aws-best-practice-research (Infra Layer) |
|-----------------------------|------------------------------------------|
| Pod resource requests/limits | Control plane configuration |
| Probes (liveness/readiness/startup) | Node group sizing and AZ distribution |
| PDB, topology constraints | Addon versions |
| Pod security context, PSA | Secrets envelope encryption |
| Network Policies | Cluster networking (VPC, subnets) |
| Service Accounts, RBAC | Authentication mode, Access Entries |
| Container image scanning | GuardDuty EKS protection |
| HPA/VPA/Karpenter workload config | Karpenter/CA infrastructure config |

## Workflow

### Step 1: Confirm Assessment Scope

Determine from user input:
- **Cluster name** and **AWS Region**
- **Assessment scope**:
  - **Full cluster** — assess all namespaces (excluding `kube-system`, `kube-public`, `kube-node-lease` by default)
  - **Specific namespaces** — user-specified list
  - **Specific workloads** — user-specified Deployments/StatefulSets
- **Include infrastructure layer?** — whether to also invoke `aws-best-practice-research` for
  the EKS infrastructure layer and merge results (default: yes)

If the user provides only a cluster name, default to full cluster assessment.

### Step 2: Environment Detection & Version Awareness

Run the following commands to detect the environment:

```bash
# Cluster info via AWS CLI
aws eks describe-cluster --name {CLUSTER} --region {REGION}

# K8s version
kubectl version --output=json

# Node distribution
kubectl get nodes -o wide --no-headers
```

Record:
- **K8s server version** (e.g., 1.30) — used for version-aware filtering
- **EKS platform version** (e.g., eks.15)
- **Node count and AZ distribution**
- **Node instance types**

**Version-aware filtering rules** (apply in Step 3):
- K8s >= 1.25: Check Pod Security Admission (PSA), skip PodSecurityPolicy (PSP)
- K8s < 1.25: Check PSP, note PSA as upgrade recommendation
- K8s >= 1.20: Check Startup Probes
- K8s >= 1.19: Check Topology Spread Constraints
- K8s >= 1.29 + VPC CNI >= 1.21.1: Check Admin Network Policies
- EKS with Pod Identity available: Prefer Pod Identity over IRSA

### Step 3: Dynamic Best Practice Research

Research the latest best practices using **context7** and **aws-knowledge-mcp-server**.
Run all queries **sequentially** (one at a time) to avoid rate limiting.

For each of the 8 assessment dimensions, execute the search queries defined in
`references/search-queries.md`. The general flow per dimension is:

1. Query **context7** (`/websites/kubernetes_io`) for K8s official best practices
2. Query **aws-knowledge-mcp-server** for EKS-specific best practices
3. Read key documentation pages from search results (max 2-3 pages per dimension)
4. Extract check items with specific thresholds and conditions

After all research is complete, merge results with the **baseline framework** in
`references/check-dimensions.md` to ensure no critical dimension is missed.

Apply version-aware filtering from Step 2 to remove inapplicable items and add
version-specific recommendations.

**Rate limit protection**: If any MCP request returns "Too many requests", wait 5 seconds
and retry once. If it fails again, skip and continue. Sequential execution is mandatory.

### Step 4: Infrastructure Layer Assessment (Optional)

If infrastructure layer assessment is included (default: yes):

1. Invoke the `aws-best-practice-research` skill for the EKS cluster
2. Store the infrastructure-layer checklist and assessment results
3. These will be merged into the final report in Step 7

If the user opts out, skip this step.

### Step 5: Workload Data Collection

Collect workload configurations using `kubectl`. Independent commands **can run in parallel**
(they are not subject to MCP rate limits).

See `references/kubectl-assessment-commands.md` for the complete command list. Key data to collect:

```bash
# Core workloads
kubectl get deployments,statefulsets,daemonsets,jobs,cronjobs --all-namespaces -o json

# Pod specifications (within workloads above)
# Already included in the -o json output

# Disruption and scaling
kubectl get pdb,hpa --all-namespaces -o json

# Networking
kubectl get networkpolicies,services,ingresses --all-namespaces -o json

# Security
kubectl get serviceaccounts --all-namespaces -o json
kubectl get clusterrolebindings,rolebindings -o json

# Storage
kubectl get pvc,storageclass -o json

# Namespace labels (for PSA)
kubectl get namespaces -o json

# Events (recent issues)
kubectl get events --all-namespaces --sort-by='.lastTimestamp' -o json
```

For **ECR image scanning** (if images are from ECR):
```bash
# For each unique ECR image found in workloads
aws ecr describe-image-scan-findings --repository-name {REPO} --image-id imageTag={TAG}
aws ecr describe-repositories --repository-names {REPO}
aws ecr get-lifecycle-policy --repository-name {REPO}
```

Filter collected data to the assessment scope (namespaces/workloads from Step 1).

### Step 6: Per-Dimension Assessment

For each check item from the research phase (Step 3), evaluate every in-scope workload:

| Status | Meaning |
|--------|---------|
| **PASS** | The workload configuration meets or exceeds the recommendation |
| **FAIL** | The workload configuration does not meet the recommendation |
| **WARN** | Cannot be fully verified, or partially meets the recommendation |
| **N/A** | The check does not apply (e.g., storage checks for stateless workloads) |

For each finding, record:
- Check item ID and name
- Status (PASS/FAIL/WARN/N/A)
- **Actual value** observed (not just "not configured")
- The specific workload(s) affected
- Version relevance notes (if any)

### Step 7: Generate Report and Save to Local File

Generate a single comprehensive report using the template in `references/output-template.md`
and **write it directly to a local markdown file**.

**IMPORTANT — File Writing Rules**:
- Use the **Write/file tool** (not bash heredoc/echo/cat) to create the report file
- If the report is too large for a single write, **split into sections**: write the
  file with the first half, then use an append/edit operation to add the remaining sections
- Do NOT output the full report content to the terminal

Use the following file naming convention:

```bash
TIMESTAMP=$(TZ=Asia/Shanghai date +%Y-%m-%d-%H-%M-%S)
CLUSTER_SLUG=$(echo "{CLUSTER_NAME}" | tr '[:upper:]' '[:lower:]' | tr ' :/' '-')
```

**Assessment Report** — see `references/output-template.md`
- Full cluster overview
- Compliance scorecard with rating scale, top 3 priorities, and quick stats
- Dimension-by-dimension assessment tables
- Per-workload detail section
- Critical issues and prioritized remediation
- Data sources and reference links
- **Save to:** `${TIMESTAMP}-${CLUSTER_SLUG}-assessment-report.md`

If infrastructure layer results exist from Step 4, merge them into the report.

After saving, print a brief summary to the terminal listing only:
- The file path of the generated report
- Overall compliance score
- Number of PASS / FAIL / WARN findings

### Step 8: Remediation Guidance & Next Steps

After saving the reports, offer:
- "I can help fix specific FAIL items — which ones would you like to address?"
- "I can re-run the assessment after remediation to verify improvements."

For Critical Issues (FAIL + High priority), provide:
- Specific remediation commands or manifest changes
- Whether the fix requires workload restart or is in-place
- Impact assessment of the change

## Important Guidelines

- **Be comprehensive**: The value of this skill is thoroughness. Better to include a check
  and mark it N/A than to miss it.
- **Always cite sources**: Every check item must reference its source (EKS Best Practices Guide,
  K8s official docs, etc.).
- **Sequential MCP queries**: All context7 and aws-knowledge-mcp requests must be sequential.
  kubectl commands can be parallel.
- **Rate limit protection**: Wait 5s and retry once on "Too many requests". Skip on second failure.
- **Version awareness**: Always filter checks by detected K8s/EKS version. Never recommend
  features unavailable in the cluster's version.
- **Actual values in findings**: Always report what was observed, not just "not configured".
  Good: "`resources.requests.memory: not set` — container has no memory request"
  Bad: "Memory request missing"
- **Per-workload granularity**: Report findings at the individual Deployment/StatefulSet level,
  not just cluster-wide summaries.
- **Exclude system namespaces by default**: Skip `kube-system`, `kube-public`, `kube-node-lease`
  unless the user explicitly includes them.
- **Respect language**: Output in the same language as the user's conversation.
- **Infrastructure vs workload boundary**: Never duplicate checks from `aws-best-practice-research`.
  This skill handles ONLY what requires kubectl/in-cluster access.
