# Check Dimensions — Baseline Framework

This file defines the 8 assessment dimensions with their **minimum check item sets**.
These serve as a fallback to ensure no critical area is missed even if dynamic research
returns incomplete results.

**This is NOT an exhaustive list.** The dynamic research phase (Step 3) may discover
additional check items. Items here are the baseline that must always be evaluated.

**Version tags**: Items marked with `[K8s >= X.Y]` only apply to clusters running that
version or later. Items marked `[DEPRECATED in X.Y]` should be skipped for those versions.

---

## Dimension 1: Workload Configuration (WL-)

Covers resource management, probes, disruption budgets, scaling, and pod scheduling.

| ID | Check Item | Description | Priority | Version Notes |
|----|------------|-------------|----------|---------------|
| WL-01-hi | **Resource requests set** | Every container must have CPU and memory `requests` defined. Without requests, the scheduler cannot make informed decisions and pods may be evicted under pressure. | High | |
| WL-02-hi | **Resource limits set** | Every container should have CPU and memory `limits` defined. Memory limits prevent OOM kills of other pods; CPU limits prevent noisy neighbors. | High | |
| WL-03-hi | **Readiness probe configured** | All containers serving traffic must have a `readinessProbe`. Without it, pods receive traffic before they are ready. | High | |
| WL-04-hi | **Liveness probe configured** | Long-running containers should have a `livenessProbe` to detect and restart deadlocked processes. Avoid probes that check downstream dependencies. | High | |
| WL-05-md | **Startup probe for slow-starting apps** | Use `startupProbe` for containers that take a long time to initialize, to avoid premature liveness probe failures. | Medium | [K8s >= 1.20] |
| WL-06-hi | **PDB exists for critical workloads** | Every Deployment/StatefulSet with >= 2 replicas should have a PodDisruptionBudget. Without PDB, voluntary disruptions (node drain, upgrades) can take all pods offline. | High | |
| WL-07-hi | **No singleton pods** | Production workloads should have `replicas >= 2`. A single replica means zero availability during any disruption. | High | |
| WL-08-hi | **Topology spread constraints** | Use `topologySpreadConstraints` to spread pods across nodes and AZs. Prevents single-AZ failure from taking down a service. | High | [K8s >= 1.19] |
| WL-09-hi | **Pod anti-affinity** | For critical services, configure `podAntiAffinity` to avoid co-locating replicas on the same node. | High | |
| WL-10-md | **HPA or VPA configured** | Workloads with variable load should have Horizontal or Vertical Pod Autoscaler. Static replica counts waste resources or risk overload. | Medium | |
| WL-11-md | **Graceful termination** | Verify `terminationGracePeriodSeconds` is appropriate (not the default 30s for services needing longer shutdown). Configure `preStop` hooks for connection draining. | Medium | |
| WL-12-lo | **QoS class distribution** | Review the distribution of Guaranteed vs Burstable vs BestEffort pods. Production workloads should be Guaranteed (requests == limits) or at minimum Burstable. BestEffort pods are first to be evicted. | Low | |
| WL-13-md | **Requests-to-limits ratio** | CPU/memory requests should be close to limits (e.g., within 2x). Large gaps indicate poor right-sizing. Use VPA recommendations or tools like Goldilocks/KRR for guidance. | Medium | |

---

## Dimension 2: Security (SEC-)

Covers pod security, RBAC, service accounts, secrets management, and namespace isolation.

| ID | Check Item | Description | Priority | Version Notes |
|----|------------|-------------|----------|---------------|
| SEC-01-hi | **Pod Security Admission enforced** | Namespaces should have PSA labels (`pod-security.kubernetes.io/enforce`) set to at least `baseline`, ideally `restricted`. | High | [K8s >= 1.25] |
| SEC-02-hi | **PodSecurityPolicy configured** | Clusters must have PSP configured to prevent privileged containers. | High | [DEPRECATED in 1.25, removed in 1.25+] |
| SEC-03-hi | **runAsNonRoot enforced** | All containers should set `securityContext.runAsNonRoot: true`. Running as root inside containers is a privilege escalation risk. | High | |
| SEC-04-hi | **No privileged containers** | No container should set `securityContext.privileged: true` unless absolutely necessary (and documented). | High | |
| SEC-05-hi | **allowPrivilegeEscalation disabled** | Set `securityContext.allowPrivilegeEscalation: false` for all containers. | High | |
| SEC-06-md | **Drop ALL capabilities** | Set `securityContext.capabilities.drop: ["ALL"]` and only add back specific capabilities needed. | Medium | |
| SEC-07-md | **Read-only root filesystem** | Set `securityContext.readOnlyRootFilesystem: true` where possible. Use `emptyDir` for writable paths. | Medium | |
| SEC-08-hi | **automountServiceAccountToken disabled** | Set `automountServiceAccountToken: false` on ServiceAccounts and pods that don't need K8s API access. | High | |
| SEC-09-hi | **IRSA or Pod Identity for AWS access** | Pods accessing AWS services must use IRSA (IAM Roles for Service Accounts) or EKS Pod Identity — never hardcoded credentials or node-level IAM roles. | High | |
| SEC-10-md | **RBAC least privilege** | ClusterRoleBindings should not grant `cluster-admin` to non-admin ServiceAccounts. Check for overly broad wildcard permissions. | Medium | |
| SEC-11-md | **NetworkPolicy exists** | Every namespace should have at least a default-deny ingress/egress NetworkPolicy. Open network is a lateral movement risk. | Medium | |
| SEC-12-md | **Secrets not in env vars** | Prefer mounting Secrets as volumes or using external secrets managers (CSI Secret Store, External Secrets Operator) over environment variables. Env vars appear in `kubectl describe pod`. | Medium | |
| SEC-13-md | **Image from trusted registry** | Container images should come from a trusted registry (e.g., ECR, official registries). No images from unverified public registries. | Medium | |
| SEC-14-md | **Image uses digest, not :latest** | Images should use SHA256 digest or specific version tags, never `:latest`. Ensures reproducibility and prevents supply chain attacks. | Medium | |
| SEC-15-lo | **Seccomp profile set** | For enhanced security, set `securityContext.seccompProfile.type: RuntimeDefault` or a custom profile. | Low | [K8s >= 1.19] |

---

## Dimension 3: Observability (OBS-)

Covers logging, metrics, tracing, and monitoring configuration.

| ID | Check Item | Description | Priority | Version Notes |
|----|------------|-------------|----------|---------------|
| OBS-01-hi | **Container Insights enabled** | Amazon CloudWatch Container Insights should be enabled for cluster-level monitoring (CPU, memory, disk, network metrics). | High | |
| OBS-02-md | **Log collection DaemonSet** | A log collection agent (Fluent Bit, CloudWatch Agent, ADOT) should be running as a DaemonSet to collect container logs. | Medium | |
| OBS-03-md | **Structured logging** | Application containers should output structured logs (JSON). Unstructured text logs are harder to query and alert on. | Medium | |
| OBS-04-md | **Prometheus metrics collection** | Workloads should expose metrics endpoints. A Prometheus-compatible scraper (ADOT, Amazon Managed Prometheus, or self-hosted) should be collecting them. | Medium | |
| OBS-05-md | **kube-state-metrics deployed** | kube-state-metrics should be running to expose K8s object state as Prometheus metrics (deployment replicas, pod status, etc.). | Medium | |
| OBS-06-lo | **Distributed tracing** | For microservice architectures, distributed tracing (X-Ray, ADOT, Jaeger) should be configured to trace requests across services. | Low | |
| OBS-07-lo | **CoreDNS monitoring** | CoreDNS metrics should be collected and monitored for DNS resolution latency and errors. | Low | |
| OBS-08-md | **Resource usage alerts** | Alerts should be configured for pod restarts, high CPU/memory usage, and PVC capacity. | Medium | |

---

## Dimension 4: Networking (NET-)

Covers service configuration, ingress, DNS, network policies, and service mesh.

| ID | Check Item | Description | Priority | Version Notes |
|----|------------|-------------|----------|---------------|
| NET-01-md | **Service type appropriate** | Use ClusterIP for internal services, LoadBalancer only for external-facing services. Avoid NodePort in production. | Medium | |
| NET-02-md | **ALB Ingress Controller** | For HTTP(S) workloads, use AWS Load Balancer Controller with ALB. Prefer IP mode for direct pod routing (reduces hops). | Medium | |
| NET-03-hi | **Default deny NetworkPolicy** | Each namespace should have a default-deny ingress and egress NetworkPolicy, with explicit allow rules. | High | |
| NET-04-md | **CoreDNS autoscaling** | CoreDNS should have HPA or proportional autoscaler enabled. DNS is a single point of failure if undersized. | Medium | |
| NET-05-lo | **NodeLocal DNSCache** | Consider running NodeLocal DNSCache DaemonSet to reduce CoreDNS load and improve DNS latency. | Low | |
| NET-06-md | **VPC CNI prefix delegation** | For high-pod-density clusters, enable VPC CNI prefix delegation to avoid IP exhaustion. Check ENABLE_PREFIX_DELEGATION env var. | Medium | |
| NET-07-lo | **Topology-aware routing** | Enable topology-aware routing (`service.kubernetes.io/topology-mode: Auto`) to reduce cross-AZ traffic costs. | Low | |
| NET-08-md | **Service Mesh mTLS** | If using a service mesh (App Mesh, Istio, Linkerd), verify mTLS is enabled for service-to-service communication. | Medium | |
| NET-09-md | **Admin Network Policies** | For multi-tenant clusters, use Admin Network Policies for cluster-wide security rules. | Medium | [K8s >= 1.29, VPC CNI >= 1.21.1] |
| NET-10-lo | **DNS Policy set** | Pods should have appropriate `dnsPolicy` (ClusterFirst for most workloads). Custom DNS configs should be reviewed. | Low | |

---

## Dimension 5: Storage (STR-)

Covers persistent volumes, storage classes, CSI drivers, and backup strategies.

| ID | Check Item | Description | Priority | Version Notes |
|----|------------|-------------|----------|---------------|
| STR-01-md | **PVC with appropriate StorageClass** | PVCs should reference a StorageClass with appropriate performance characteristics (gp3 vs io2 vs efs). | Medium | |
| STR-02-md | **Reclaim policy** | StorageClass `reclaimPolicy` should be `Retain` for production data (not `Delete`). | Medium | |
| STR-03-md | **WaitForFirstConsumer binding** | StorageClass should use `volumeBindingMode: WaitForFirstConsumer` to ensure PVs are provisioned in the same AZ as the pod. | Medium | |
| STR-04-hi | **Volume encryption** | EBS volumes should be encrypted. Check StorageClass for `encrypted: "true"` parameter. | High | |
| STR-05-md | **EBS CSI / EFS CSI driver version** | CSI drivers should be up-to-date. Outdated drivers may have security vulnerabilities or missing features. | Medium | |
| STR-06-md | **Backup strategy** | Stateful workloads should have Velero or equivalent backup/snapshot strategy. Check for VolumeSnapshot resources. | Medium | |
| STR-07-lo | **PVC capacity monitoring** | Alerts should be configured for PVC usage approaching capacity. | Low | |

---

## Dimension 6: EKS Platform Integration (EKS-)

Covers addon management, autoscaling, IAM integration, and platform features.

| ID | Check Item | Description | Priority | Version Notes |
|----|------------|-------------|----------|---------------|
| EKS-01-hi | **EKS Addon versions current** | All EKS-managed addons (VPC CNI, CoreDNS, kube-proxy, EBS CSI) should be on supported versions. Use `aws eks describe-addon-versions`. | High | |
| EKS-02-md | **Karpenter or CA configured** | A node autoscaler (Karpenter recommended, or Cluster Autoscaler) should be running and configured. | Medium | |
| EKS-03-md | **Karpenter consolidation** | If using Karpenter, verify consolidation policy is configured to remove underutilized nodes. | Medium | |
| EKS-04-hi | **IRSA / Pod Identity configured** | Workloads needing AWS access should use IRSA or Pod Identity. Check for ServiceAccount annotations (`eks.amazonaws.com/role-arn`). | High | |
| EKS-05-md | **GuardDuty EKS Runtime** | Amazon GuardDuty EKS Runtime Monitoring should be enabled for threat detection. | Medium | |
| EKS-06-hi | **K8s version in support window** | The cluster K8s version must be within the EKS support window (standard or extended support). | High | |
| EKS-07-md | **Upgrade Insights clean** | Check `aws eks list-insights` for deprecation warnings or upgrade blockers. | Medium | |
| EKS-08-md | **Fargate profiles** | If using Fargate, verify profiles match expected namespaces and selectors. | Medium | |
| EKS-09-lo | **EKS Auto Mode** | Consider whether EKS Auto Mode is appropriate for reducing operational overhead. | Low | |

---

## Dimension 7: CI/CD & GitOps (CICD-)

Covers deployment strategies, image management, and GitOps practices.

| ID | Check Item | Description | Priority | Version Notes |
|----|------------|-------------|----------|---------------|
| CICD-01-md | **Deployment strategy defined** | Deployments should have an explicit `strategy` (RollingUpdate with appropriate maxSurge/maxUnavailable). | Medium | |
| CICD-02-md | **Rollout history preserved** | `revisionHistoryLimit` should be >= 5 (default 10) to allow rollbacks. | Medium | |
| CICD-03-md | **Image pull policy** | `imagePullPolicy: Always` for mutable tags; `IfNotPresent` for immutable digest-based references. Never use `:latest` with `IfNotPresent`. | Medium | |
| CICD-04-md | **Image tag immutability** | ECR repositories should have image tag immutability enabled to prevent tag overwriting. | Medium | |
| CICD-05-lo | **GitOps controller** | For production clusters, consider GitOps (ArgoCD, Flux) for declarative, auditable deployments. | Low | |
| CICD-06-md | **No kubectl apply in production** | Production deployments should use CI/CD pipelines or GitOps, not manual `kubectl apply`. Check for ArgoCD/Flux presence as indicator. | Medium | |

---

## Dimension 8: Image Security (IMG-)

Covers image scanning, base images, CVE management, and supply chain security.

| ID | Check Item | Description | Priority | Version Notes |
|----|------------|-------------|----------|---------------|
| IMG-01-hi | **ECR image scanning enabled** | ECR repositories should have scan-on-push enabled (basic or enhanced scanning). | High | |
| IMG-02-hi | **No Critical/High CVEs** | Running images should have no Critical or High severity CVEs. Check ECR scan findings. | High | |
| IMG-03-md | **ECR lifecycle policy** | ECR repositories should have lifecycle policies to clean up old/untagged images. | Medium | |
| IMG-04-md | **Minimal base images** | Prefer minimal/distroless base images over full OS images. Smaller attack surface. | Medium | |
| IMG-05-lo | **Image signing** | For high-security environments, verify image signatures using Notation or Cosign. | Low | |
| IMG-06-md | **No latest tag** | No workload should reference `:latest` tag. Use specific version tags or SHA256 digests. | Medium | |
| IMG-07-md | **Private registry only** | All production images should come from private registries (ECR). No direct pulls from Docker Hub or other public registries. | Medium | |
