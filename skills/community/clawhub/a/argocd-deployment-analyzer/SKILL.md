---
name: argocd-deployment-analyzer
description: Analyze ArgoCD application sync status, detect configuration drift, review manifests for security and best practices, and diagnose sync failures.
metadata:
  tags: ["argocd", "gitops", "kubernetes", "deployment", "drift-detection", "sync", "devops", "cd"]
---

# ArgoCD Deployment Analyzer

Deep-dive analysis of ArgoCD-managed applications — detect sync drift, diagnose failed syncs, audit manifest security, review sync policies, and validate ArgoCD configurations against production best practices. Turns ArgoCD operational noise into actionable findings.

Use when: "analyze argocd apps", "why is my argocd app out of sync", "review argocd config", "audit gitops deployments", "diagnose sync failure", or when ArgoCD applications are degraded, drifting, or misconfigured.

## Prerequisites

The agent checks for access to ArgoCD:

```bash
# CLI access
argocd version --client

# Logged in
argocd account get-user-info

# Or: kubectl access to ArgoCD namespace
kubectl get applications.argoproj.io -n argocd

# Or: ArgoCD API access
curl -s https://argocd.example.com/api/v1/applications \
  -H "Authorization: Bearer $ARGOCD_TOKEN" | jq '.items | length'
```

## Usage

Provide one or more of:

- **Application name** — specific ArgoCD app to analyze (e.g., `production/api-server`)
- **Project name** — analyze all apps in an ArgoCD project
- **Scope** — `all` to analyze every application
- **Focus area** — `sync`, `security`, `health`, `drift`, `config`, or `all`

Example invocations:

> Analyze why the `payments-service` ArgoCD app keeps going OutOfSync.

> Security audit all ArgoCD applications in the `production` project.

> Review our ArgoCD ApplicationSet configurations for best practices.

## How It Works

### Step 1: Application Inventory

Gather the full picture of all ArgoCD-managed applications:

```bash
# List all applications with status
argocd app list -o json | jq '[.[] | {
  name: .metadata.name,
  project: .spec.project,
  syncStatus: .status.sync.status,
  healthStatus: .status.health.status,
  repo: .spec.source.repoURL,
  path: .spec.source.path,
  targetRevision: .spec.source.targetRevision,
  destination: .spec.destination.server,
  namespace: .spec.destination.namespace,
  syncPolicy: .spec.syncPolicy
}]'

# Or via kubectl
kubectl get applications.argoproj.io -n argocd -o json | jq '[.items[] | {
  name: .metadata.name,
  sync: .status.sync.status,
  health: .status.health.status
}]'
```

Classify applications into categories:

- **Healthy + Synced** — no action needed
- **Healthy + OutOfSync** — drift detected, needs investigation
- **Degraded** — health check failing
- **Progressing** — sync in progress, check if stuck
- **Missing** — target resources don't exist
- **Unknown** — ArgoCD can't determine state

### Step 2: Sync Drift Analysis

For each OutOfSync application, identify what drifted and why:

```bash
# Get the diff between live and desired state
argocd app diff <app-name> --local-repo-root /path/to/repo

# Detailed sync status with resource-level breakdown
argocd app get <app-name> -o json | jq '{
  syncStatus: .status.sync.status,
  revision: .status.sync.revision,
  comparedTo: .status.sync.comparedTo,
  resources: [.status.resources[] | select(.status != "Synced") | {
    kind: .kind,
    name: .name,
    namespace: .namespace,
    status: .status,
    health: .health.status,
    message: .health.message
  }]
}'

# Check sync history for patterns
argocd app get <app-name> -o json | jq '[.status.history[] | {
  revision: .revision[:8],
  deployedAt: .deployedAt,
  source: .source.path
}]'
```

**Common drift causes the agent checks:**

1. **Manual kubectl edits** — someone modified a resource directly, bypassing GitOps
2. **Mutating webhooks** — admission controllers injecting sidecars, labels, or annotations
3. **Horizontal Pod Autoscaler** — HPA changes replica count, conflicts with Git-declared replicas
4. **Controller-managed fields** — Kubernetes controllers (e.g., EndpointSlice controller) update fields
5. **CRD defaults** — CRD defaulting webhooks adding fields not in the Git source
6. **Helm value drift** — values.yaml in Git doesn't match what was rendered

### Step 3: Sync Failure Diagnosis

When sync operations fail, diagnose the root cause:

```bash
# Get sync operation result
argocd app get <app-name> -o json | jq '.status.operationState | {
  phase: .phase,
  message: .message,
  startedAt: .startedAt,
  finishedAt: .finishedAt,
  syncResult: .syncResult.resources | map(select(.status != "Synced"))
}'

# Check for resource-level errors
argocd app resources <app-name> --orphaned

# Check events on the target namespace
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20
```

**Failure categories the agent identifies:**

| Category | Symptoms | Typical Fix |
|----------|----------|-------------|
| RBAC | `forbidden` errors in sync | Fix ArgoCD service account permissions |
| Schema validation | `validation failed` | Fix manifest against CRD/API schema |
| Namespace missing | `namespace not found` | Create namespace or enable auto-create |
| Resource conflict | `already exists` | Check for duplicate resource management |
| Quota exceeded | `exceeded quota` | Request quota increase or reduce resource requests |
| Immutable field | `field is immutable` | Delete and recreate the resource |
| Dependency order | `resource X not found` | Add sync waves or sync ordering |
| Timeout | `deadline exceeded` | Increase sync timeout or fix health check |

### Step 4: Health Check Analysis

Evaluate application health and identify degraded components:

```bash
# Health of each resource in the app
argocd app get <app-name> -o json | jq '[.status.resources[] | {
  kind: .kind,
  name: .name,
  health: .health.status,
  message: .health.message
}] | group_by(.health) | map({status: .[0].health, count: length, resources: map(.name)})'

# Pod-level issues for Degraded deployments
kubectl get pods -n <namespace> -l app=<app-label> -o json | jq '[.items[] | {
  name: .metadata.name,
  phase: .status.phase,
  ready: ([.status.conditions[] | select(.type=="Ready")] | .[0].status),
  restarts: ([.status.containerStatuses[].restartCount] | add),
  waiting: [.status.containerStatuses[] | select(.state.waiting) | .state.waiting.reason]
}]'
```

### Step 5: Configuration Audit

Review ArgoCD Application and Project configurations for security and best practices:

**Sync policy analysis:**

```bash
# Check for dangerous sync policies
argocd app list -o json | jq '[.[] | select(
  .spec.syncPolicy.automated.prune == true and
  .spec.syncPolicy.automated.selfHeal == true
) | {name: .metadata.name, warning: "auto-prune + self-heal enabled"}]'
```

**Checks performed:**

- **Auto-sync without prune protection** — accidental resource deletion risk
- **Self-heal on production** — could mask legitimate manual hotfixes
- **Missing sync windows** — production should have maintenance windows
- **No retry policy** — transient failures won't self-recover
- **Wildcard project destinations** — `*` server or namespace defeats RBAC
- **No resource whitelist/blacklist** — project can deploy any resource type
- **Plaintext secrets in Git** — secrets not managed by Sealed Secrets / SOPS / ESO
- **Missing ignoreDifferences** — known benign drift causing noise
- **No notification triggers** — sync failures go unnoticed
- **Orphaned resources** — resources in the namespace not managed by any app

### Step 6: Security Review

Audit manifests managed by ArgoCD applications for security issues:

```bash
# Extract rendered manifests
argocd app manifests <app-name> --source live > /tmp/live-manifests.yaml
argocd app manifests <app-name> --source git > /tmp/git-manifests.yaml
```

**Security checks:**

- Containers running as root or with `privileged: true`
- Missing SecurityContext, `readOnlyRootFilesystem`, `runAsNonRoot`
- Missing resource limits (CPU/memory) — noisy neighbor risk
- `hostNetwork`, `hostPID`, `hostIPC` enabled
- ServiceAccount token auto-mounting when not needed
- Missing NetworkPolicies
- Images using `:latest` tag or no tag
- Secrets mounted as environment variables instead of files
- Missing PodDisruptionBudgets for critical services

### Step 7: ApplicationSet Analysis

If ApplicationSets are used, validate their generators and templates:

```bash
kubectl get applicationsets -n argocd -o json | jq '[.items[] | {
  name: .metadata.name,
  generators: [.spec.generators[] | keys[0]],
  template: .spec.template.spec.source.repoURL,
  syncPolicy: .spec.template.spec.syncPolicy
}]'
```

**Checks:**

- Git generator with overly broad directory patterns
- Missing `preserveResourcesOnDeletion` (deleting the AppSet deletes all apps)
- Cluster generator without label selectors (deploys to ALL clusters)
- Template overrides that bypass project restrictions
- No `goTemplate` validation (template injection risk)

## Output

The agent produces a structured report:

1. **Dashboard summary** — total apps, sync status distribution, health distribution
2. **Drift report** — each OutOfSync app with specific resources and fields that drifted, with root cause
3. **Failure diagnosis** — for each failed sync: root cause, specific error, and remediation steps
4. **Health issues** — degraded resources with pod-level diagnostics
5. **Configuration findings** — ranked by severity (Critical / High / Medium / Low) with fix recommendations
6. **Security findings** — manifest-level security issues with remediation
7. **Recommended ignoreDifferences** — for known benign drift patterns (HPA replicas, annotation mutations, etc.)
8. **Action items** — prioritized list of changes to make, with example YAML patches

## Common Remediation Patterns

**HPA replica drift:**
```yaml
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
```

**Mutating webhook annotations:**
```yaml
spec:
  ignoreDifferences:
    - group: ""
      kind: Service
      jqPathExpressions:
        - .metadata.annotations["webhook.example.com/injected"]
```

**Sync wave ordering for dependencies:** Use `argocd.argoproj.io/sync-wave` annotations: `-1` for namespaces, `0` for ConfigMaps/Secrets, `1` for Deployments/Services.
