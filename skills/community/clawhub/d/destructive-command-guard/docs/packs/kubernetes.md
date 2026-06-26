# Kubernetes Packs

This document describes packs in the `kubernetes` category.

## Packs in this Category

- [kubectl](#kuberneteskubectl)
- [Helm](#kuberneteshelm)
- [Kustomize](#kuberneteskustomize)

---

## kubectl

**Pack ID:** `kubernetes.kubectl`

Protects against destructive kubectl operations like delete namespace, drain, and mass deletion

### Keywords

Commands containing these keywords are checked against this pack:

- `kubectl`
- `delete`
- `drain`
- `cordon`
- `taint`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `kubectl-get` | `kubectl\s+get` |
| `kubectl-describe` | `kubectl\s+describe` |
| `kubectl-logs` | `kubectl\s+logs` |
| `kubectl-dry-run` | `kubectl\s+.*--dry-run(?:=(?:client\|server\|none))?` |
| `kubectl-diff` | `kubectl\s+diff` |
| `kubectl-explain` | `kubectl\s+explain` |
| `kubectl-top` | `kubectl\s+top` |
| `kubectl-config` | `kubectl\s+config` |
| `kubectl-api` | `kubectl\s+api-(?:resources\|versions)` |
| `kubectl-version` | `kubectl\s+version` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `delete-namespace` | kubectl delete namespace removes the entire namespace and ALL resources within it. | high |
| `delete-all` | kubectl delete --all removes ALL resources of that type. Use --dry-run=client first. | high |
| `delete-all-namespaces` | kubectl delete with -A/--all-namespaces affects ALL namespaces. Very dangerous! | high |
| `drain-node` | kubectl drain evicts all pods from a node. Ensure proper pod disruption budgets. | high |
| `cordon-node` | kubectl cordon marks a node unschedulable. Existing pods continue running. | high |
| `taint-noexecute` | kubectl taint with NoExecute evicts existing pods that don't tolerate the taint. | high |
| `delete-workload` | kubectl delete deployment/statefulset/daemonset removes the workload. Use --dry-run first. | high |
| `delete-pvc` | kubectl delete pvc may permanently delete data if ReclaimPolicy is Delete. | high |
| `delete-pv` | kubectl delete pv may permanently delete the underlying storage. | high |
| `scale-to-zero` | kubectl scale --replicas=0 stops all pods for the workload. | high |
| `delete-force` | kubectl delete --force --grace-period=0 immediately removes resources without graceful shutdown. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "kubernetes.kubectl:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "kubernetes.kubectl:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Helm

**Pack ID:** `kubernetes.helm`

Protects against destructive Helm operations like uninstall and rollback without dry-run

### Keywords

Commands containing these keywords are checked against this pack:

- `helm`
- `uninstall`
- `delete`
- `rollback`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `helm-list` | `helm\s+list` |
| `helm-status` | `helm\s+status` |
| `helm-history` | `helm\s+history` |
| `helm-show` | `helm\s+show` |
| `helm-inspect` | `helm\s+inspect` |
| `helm-get` | `helm\s+get` |
| `helm-search` | `helm\s+search` |
| `helm-repo` | `helm\s+repo` |
| `helm-dry-run` | `helm\s+.*--dry-run` |
| `helm-template` | `helm\s+template` |
| `helm-lint` | `helm\s+lint` |
| `helm-diff` | `helm\s+diff` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `uninstall` | helm uninstall removes the release and all its resources. Use --dry-run first. | high |
| `rollback` | helm rollback reverts to a previous release. Use --dry-run to preview changes. | high |
| `upgrade-force` | helm upgrade --force deletes and recreates resources, causing downtime. | high |
| `upgrade-reset-values` | helm upgrade --reset-values discards all previously set values. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "kubernetes.helm:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "kubernetes.helm:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Kustomize

**Pack ID:** `kubernetes.kustomize`

Protects against destructive Kustomize operations when combined with kubectl delete or applied without review

### Keywords

Commands containing these keywords are checked against this pack:

- `kustomize`
- `kubectl`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `kustomize-build` | `kustomize\s+build(?!\s*\\|)` |
| `kubectl-kustomize` | `kubectl\s+kustomize(?!\s*\\|)` |
| `kustomize-diff` | `kustomize\s+build\s+.*\\|\s*kubectl\s+diff` |
| `kustomize-dry-run` | `kustomize\s+build\s+.*\\|\s*kubectl\s+.*--dry-run` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `kustomize-delete` | kustomize build \| kubectl delete removes all resources in the kustomization. | high |
| `kubectl-kustomize-delete` | kubectl kustomize \| kubectl delete removes all resources in the kustomization. | high |
| `kubectl-delete-k` | kubectl delete -k removes all resources defined in the kustomization. Use --dry-run first. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "kubernetes.kustomize:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "kubernetes.kustomize:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

