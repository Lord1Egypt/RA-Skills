# Search Queries — context7 & aws-knowledge-mcp-server

Run these queries **sequentially** (one at a time) to research best practices for each dimension.
Replace `{K8S_VERSION}` with the detected K8s version from Step 2.

**Rules**:
- All queries must execute one at a time. **Never send multiple MCP requests in parallel.**
- Wait for each query to complete before sending the next one.
- If a query returns "Too many requests", wait 5 seconds and retry once. Skip on second failure.
- Limit: 5-8 results per query to keep within rate limits.

---

## context7 Queries

Use library ID: `/websites/kubernetes_io`

### Dimension 1: Workload Configuration
```
Query C7-WL-1: "Kubernetes best practices for pod resource requests and limits, QoS classes"
Query C7-WL-2: "Configure liveness readiness startup probes for production pods"
Query C7-WL-3: "Pod Disruption Budget configuration and topology spread constraints"
Query C7-WL-4: "Horizontal Pod Autoscaler and Vertical Pod Autoscaler configuration"
```

### Dimension 2: Security
```
Query C7-SEC-1: "Pod Security Standards and Pod Security Admission enforce baseline restricted"
Query C7-SEC-2: "Kubernetes RBAC best practices service account security"
Query C7-SEC-3: "Container security context runAsNonRoot readOnlyRootFilesystem capabilities"
Query C7-SEC-4: "Kubernetes Network Policy best practices default deny"
```

### Dimension 3: Observability
```
Query C7-OBS-1: "Kubernetes monitoring and logging best practices for production clusters"
Query C7-OBS-2: "Configure Prometheus metrics collection in Kubernetes"
```

### Dimension 4: Networking
```
Query C7-NET-1: "Kubernetes service types ClusterIP LoadBalancer best practices"
Query C7-NET-2: "Kubernetes DNS CoreDNS configuration and autoscaling"
Query C7-NET-3: "Kubernetes Network Policy examples ingress egress default deny"
```

### Dimension 5: Storage
```
Query C7-STR-1: "Kubernetes persistent volume storage class best practices WaitForFirstConsumer"
Query C7-STR-2: "Kubernetes volume snapshot and backup strategies"
```

### Dimension 7: CI/CD & GitOps
```
Query C7-CICD-1: "Kubernetes deployment strategies rolling update blue-green canary"
Query C7-CICD-2: "Kubernetes image pull policy and revision history best practices"
```

---

## aws-knowledge-mcp-server Queries

### Dimension 1: Workload Configuration
```
Query AWS-WL-1:
  search_phrase: "EKS best practices running highly available applications pod disruption budget probes"
  topics: ["general"]
  limit: 5

Query AWS-WL-2:
  search_phrase: "EKS best practices resource requests limits right-sizing HPA VPA Karpenter"
  topics: ["general"]
  limit: 5
```

### Dimension 2: Security
```
Query AWS-SEC-1:
  search_phrase: "EKS best practices pod security admission RBAC service account"
  topics: ["general"]
  limit: 5

Query AWS-SEC-2:
  search_phrase: "EKS best practices network security network policy encryption mTLS"
  topics: ["general"]
  limit: 5

Query AWS-SEC-3:
  search_phrase: "EKS IRSA Pod Identity IAM roles for service accounts"
  topics: ["general", "reference_documentation"]
  limit: 5
```

### Dimension 3: Observability
```
Query AWS-OBS-1:
  search_phrase: "EKS best practices observability Container Insights logging monitoring ADOT"
  topics: ["general"]
  limit: 5

Query AWS-OBS-2:
  search_phrase: "Amazon EKS observability best practices CloudWatch Prometheus distributed tracing"
  topics: ["general"]
  limit: 5
```

### Dimension 4: Networking
```
Query AWS-NET-1:
  search_phrase: "EKS best practices networking VPC CNI prefix delegation ALB ingress"
  topics: ["general"]
  limit: 5

Query AWS-NET-2:
  search_phrase: "EKS network policy admin network policy application network policy"
  topics: ["general", "current_awareness"]
  limit: 5
```

### Dimension 5: Storage
```
Query AWS-STR-1:
  search_phrase: "EKS best practices persistent storage EBS CSI EFS CSI storage class encryption"
  topics: ["general", "reference_documentation"]
  limit: 5
```

### Dimension 6: EKS Platform Integration
```
Query AWS-EKS-1:
  search_phrase: "EKS best practices addon management Karpenter cluster autoscaler node auto-repair"
  topics: ["general"]
  limit: 5

Query AWS-EKS-2:
  search_phrase: "EKS cluster upgrades version support GuardDuty runtime monitoring"
  topics: ["general"]
  limit: 5

Query AWS-EKS-3:
  search_phrase: "EKS Auto Mode security data plane management"
  topics: ["general"]
  limit: 5
```

### Dimension 7: CI/CD & GitOps
```
Query AWS-CICD-1:
  search_phrase: "EKS deployment strategies rolling update blue green canary GitOps ArgoCD"
  topics: ["general"]
  limit: 5
```

### Dimension 8: Image Security
```
Query AWS-IMG-1:
  search_phrase: "ECR image scanning lifecycle policy image security best practices"
  topics: ["general", "reference_documentation"]
  limit: 5

Query AWS-IMG-2:
  search_phrase: "EKS container image security scanning CVE minimal base images"
  topics: ["general"]
  limit: 5
```

---

## Key Documentation Pages to Read

After search, prioritize reading these pages (if found in results) using `aws___read_documentation`:

1. `https://docs.aws.amazon.com/eks/latest/best-practices/reliability.html`
2. `https://docs.aws.amazon.com/eks/latest/best-practices/security.html`
3. `https://docs.aws.amazon.com/eks/latest/best-practices/application.html`
4. `https://docs.aws.amazon.com/eks/latest/best-practices/networking.html`
5. `https://docs.aws.amazon.com/eks/latest/best-practices/cost-opt-compute.html`
6. `https://docs.aws.amazon.com/eks/latest/best-practices/data-plane.html`
7. `https://docs.aws.amazon.com/eks/latest/best-practices/network-security.html`

Read each with `max_length: 10000`. Read **one at a time, sequentially**.
