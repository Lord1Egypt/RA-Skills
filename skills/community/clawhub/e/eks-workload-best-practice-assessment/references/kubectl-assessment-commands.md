# kubectl Assessment Commands

Commands for collecting workload configuration data from the EKS cluster.
Replace `{NAMESPACE_FILTER}` with `--all-namespaces` for full cluster assessment
or `--namespace {NS}` for targeted assessment.

**Rules**:
- These kubectl commands **can be run in parallel** (they are not subject to MCP rate limits).
- Group independent commands together for efficiency.
- Exclude system namespaces by default: `kube-system`, `kube-public`, `kube-node-lease`.

---

## Core Workload Data

```bash
# All workload controllers (Deployments, StatefulSets, DaemonSets, Jobs, CronJobs)
kubectl get deployments {NAMESPACE_FILTER} -o json
kubectl get statefulsets {NAMESPACE_FILTER} -o json
kubectl get daemonsets {NAMESPACE_FILTER} -o json
kubectl get jobs {NAMESPACE_FILTER} -o json
kubectl get cronjobs {NAMESPACE_FILTER} -o json
```

## Disruption & Scaling

```bash
# Pod Disruption Budgets
kubectl get pdb {NAMESPACE_FILTER} -o json

# Horizontal Pod Autoscalers
kubectl get hpa {NAMESPACE_FILTER} -o json

# Vertical Pod Autoscalers (if VPA CRD exists)
kubectl get vpa {NAMESPACE_FILTER} -o json 2>/dev/null || echo '{"items":[]}'
```

## Security

```bash
# Namespace labels (for PSA enforcement)
kubectl get namespaces -o json

# Service Accounts (check automountServiceAccountToken, annotations)
kubectl get serviceaccounts {NAMESPACE_FILTER} -o json

# RBAC - Cluster-level bindings
kubectl get clusterrolebindings -o json
kubectl get clusterroles -o json

# RBAC - Namespace-level bindings
kubectl get rolebindings {NAMESPACE_FILTER} -o json

# Pod Security Policies (for K8s < 1.25)
kubectl get podsecuritypolicies -o json 2>/dev/null || echo '{"items":[]}'
```

## Networking

```bash
# Network Policies
kubectl get networkpolicies {NAMESPACE_FILTER} -o json

# Admin Network Policies (if CRD exists)
kubectl get adminnetworkpolicies -o json 2>/dev/null || echo '{"items":[]}'

# Services (check types, selectors)
kubectl get services {NAMESPACE_FILTER} -o json

# Ingresses
kubectl get ingresses {NAMESPACE_FILTER} -o json

# CoreDNS deployment
kubectl get deployment coredns -n kube-system -o json

# CoreDNS HPA (if exists)
kubectl get hpa coredns -n kube-system -o json 2>/dev/null || echo '{}'

# NodeLocal DNSCache (if exists)
kubectl get daemonset node-local-dns -n kube-system -o json 2>/dev/null || echo '{}'

# VPC CNI config (prefix delegation, custom networking)
kubectl get daemonset aws-node -n kube-system -o json
```

## Storage

```bash
# Persistent Volume Claims
kubectl get pvc {NAMESPACE_FILTER} -o json

# Storage Classes
kubectl get storageclasses -o json

# Volume Snapshots (if CRD exists)
kubectl get volumesnapshots {NAMESPACE_FILTER} -o json 2>/dev/null || echo '{"items":[]}'

# Volume Snapshot Classes (if CRD exists)
kubectl get volumesnapshotclasses -o json 2>/dev/null || echo '{"items":[]}'
```

## Observability Components

```bash
# Check for common observability DaemonSets/Deployments
# Fluent Bit
kubectl get daemonset -n amazon-cloudwatch -o json 2>/dev/null || \
kubectl get daemonset -n logging -o json 2>/dev/null || \
kubectl get daemonset -l app=fluent-bit --all-namespaces -o json 2>/dev/null || echo '{"items":[]}'

# CloudWatch Agent / ADOT
kubectl get daemonset -l app.kubernetes.io/name=cloudwatch-agent --all-namespaces -o json 2>/dev/null || echo '{"items":[]}'
kubectl get deployment -l app.kubernetes.io/name=adot-collector --all-namespaces -o json 2>/dev/null || echo '{"items":[]}'

# kube-state-metrics
kubectl get deployment -l app.kubernetes.io/name=kube-state-metrics --all-namespaces -o json 2>/dev/null || echo '{"items":[]}'

# Prometheus (check for operator or standalone)
kubectl get prometheus --all-namespaces -o json 2>/dev/null || echo '{"items":[]}'

# Container Insights (check via addon or agent)
kubectl get daemonset cloudwatch-agent -n amazon-cloudwatch -o json 2>/dev/null || echo '{}'
```

## CI/CD & GitOps Components

```bash
# ArgoCD (if installed)
kubectl get applications.argoproj.io --all-namespaces -o json 2>/dev/null || echo '{"items":[]}'

# Flux (if installed)
kubectl get kustomizations.kustomize.toolkit.fluxcd.io --all-namespaces -o json 2>/dev/null || echo '{"items":[]}'
kubectl get helmreleases.helm.toolkit.fluxcd.io --all-namespaces -o json 2>/dev/null || echo '{"items":[]}'
```

## Cluster-Level Info

```bash
# Node information
kubectl get nodes -o json

# Cluster events (recent, for detecting issues)
kubectl get events --all-namespaces --sort-by='.lastTimestamp' --field-selector type=Warning -o json

# Karpenter NodePools (if Karpenter installed)
kubectl get nodepools.karpenter.sh -o json 2>/dev/null || echo '{"items":[]}'
kubectl get ec2nodeclasses.karpenter.k8s.aws -o json 2>/dev/null || echo '{"items":[]}'

# Cluster Autoscaler (if installed)
kubectl get deployment -l app=cluster-autoscaler -n kube-system -o json 2>/dev/null || echo '{"items":[]}'
```

## ECR Image Security (via AWS CLI)

```bash
# List unique images from all workloads, then for each ECR image:

# Check repository scan configuration
aws ecr describe-repositories --repository-names {REPO_NAME} --region {REGION} \
  --query 'repositories[0].{scanOnPush:imageScanningConfiguration.scanOnPush,tagImmutability:imageTagMutability}'

# Get scan findings for the running image
aws ecr describe-image-scan-findings \
  --repository-name {REPO_NAME} \
  --image-id imageTag={TAG} \
  --region {REGION} \
  --query 'imageScanFindings.findingSeverityCounts'

# Check lifecycle policy
aws ecr get-lifecycle-policy --repository-name {REPO_NAME} --region {REGION} 2>/dev/null || echo 'No lifecycle policy'

# Container Insights status (via CloudWatch)
aws cloudwatch describe-anomaly-detectors --namespace ContainerInsights --region {REGION} 2>/dev/null || echo '{}'
```

---

## Processing Notes

1. **Filtering**: After collecting data, filter out system namespaces (`kube-system`,
   `kube-public`, `kube-node-lease`) unless the user explicitly included them.
2. **Image extraction**: Parse all container specs from workload JSON to build the unique
   image list for ECR scanning.
3. **Error handling**: Commands that fail (CRD not installed, etc.) should default to
   empty results, not block the assessment. The `2>/dev/null || echo` pattern handles this.
4. **Large clusters**: For clusters with 100+ workloads, consider namespace-by-namespace
   collection to avoid memory issues with large JSON outputs.
