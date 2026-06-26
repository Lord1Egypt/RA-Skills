---
name: cluster-upgrade-planner
description: Plan Kubernetes cluster upgrades with API deprecation checks, addon compatibility verification, and rollback-safe runbooks
---

# Cluster Upgrade Planner

Systematically plan Kubernetes cluster upgrades by analyzing the current cluster state, detecting deprecated API usage, verifying addon and workload compatibility with the target version, and producing a step-by-step upgrade runbook with rollback procedures. This skill prevents upgrade failures caused by unnoticed deprecations, incompatible controllers, or workload disruption.

Use when: "plan cluster upgrade", "upgrade kubernetes", "check k8s deprecations", "upgrade readiness", "pre-upgrade check", "upgrade runbook"

## Commands

### 1. `preflight` --- Check compatibility before upgrading

Gather cluster facts and compare them against the target Kubernetes version to surface blockers.

**Step 1 -- Identify current state**

```bash
# Current server and client versions
kubectl version -o yaml 2>/dev/null || kubectl version --short

# Node versions and status
kubectl get nodes -o wide

# Control-plane component versions (kubeadm clusters)
kubectl -n kube-system get pods -l tier=control-plane -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[0].image}{"\n"}{end}'
```

Record `CURRENT_VERSION` (e.g. 1.28) and ask the user for `TARGET_VERSION` if not provided.

**Step 2 -- Detect deprecated and removed APIs**

```bash
# Scan all manifests stored in the cluster for deprecated apiVersions
# Uses kubectl to fetch every resource and check apiVersion fields
for api in $(kubectl api-resources --verbs=list -o name); do
  kubectl get "$api" --all-namespaces -o jsonpath='{range .items[*]}{.apiVersion}{"\t"}{.kind}{"\t"}{.metadata.namespace}/{.metadata.name}{"\n"}{end}' 2>/dev/null
done | sort -u > /tmp/cluster-api-usage.txt
```

```bash
# Cross-reference against known removals for the target version
# Key removals by version:
# 1.25: policy/v1beta1 PodSecurityPolicy removed
# 1.26: flowcontrol.apiserver.k8s.io/v1beta1 removed
# 1.27: storage.k8s.io/v1beta1 CSIStorageCapacity removed
# 1.29: flowcontrol.apiserver.k8s.io/v1beta2 removed
# 1.32: autoscaling/v2beta1 removed

# Check for problematic apiVersions in the usage dump
rg 'v1beta1|v1beta2|v1alpha1' /tmp/cluster-api-usage.txt || echo "No deprecated beta APIs found"
```

**Step 3 -- Check addon compatibility**

```bash
# List all Helm releases and their chart versions
helm list -A -o json 2>/dev/null | python3 -c "
import json, sys
releases = json.load(sys.stdin)
for r in releases:
    print(f\"{r['namespace']}/{r['name']}\tChart: {r['chart']}\tApp: {r.get('app_version','?')}\tStatus: {r['status']}\")
"

# List non-Helm workloads in kube-system (operators, CNI, etc.)
kubectl -n kube-system get deployments,daemonsets -o custom-columns=NAME:.metadata.name,IMAGE:.spec.template.spec.containers[0].image
```

For each addon, verify the installed version supports `TARGET_VERSION` by checking the upstream compatibility matrix. Key addons to verify:
- CNI plugin (Calico, Cilium, Flannel)
- Ingress controller (nginx, Traefik)
- cert-manager
- metrics-server
- CoreDNS
- CSI drivers

**Step 4 -- Assess workload disruption risk**

```bash
# Pods without PodDisruptionBudgets
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.metadata.ownerReferences[0].kind}{"\n"}{end}' > /tmp/all-pods.txt
kubectl get pdb --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.spec.selector.matchLabels}{"\n"}{end}' > /tmp/all-pdbs.txt

echo "=== Namespaces with pods but no PDB ==="
awk '{print $1}' /tmp/all-pods.txt | sort -u > /tmp/ns-with-pods.txt
awk '{print $1}' /tmp/all-pdbs.txt | sort -u > /tmp/ns-with-pdbs.txt
comm -23 /tmp/ns-with-pods.txt /tmp/ns-with-pdbs.txt

# Single-replica deployments (high disruption risk)
kubectl get deployments --all-namespaces -o jsonpath='{range .items[?(@.spec.replicas==1)]}{.metadata.namespace}/{.metadata.name}{"\n"}{end}'
```

**Report template:**

```
## Preflight Report: Upgrade from {CURRENT} to {TARGET}

### Blockers (must fix before upgrade)
- [ ] {list removed APIs still in use}
- [ ] {incompatible addons}

### Warnings (should fix, not blocking)
- [ ] {deprecated APIs that will be removed in next version}
- [ ] {single-replica deployments without PDB}

### Addon Compatibility
| Addon | Current Version | Target K8s Supported | Action |
|-------|----------------|----------------------|--------|

### Node Readiness
- Total nodes: {N}
- Nodes at current version: {N}
- Nodes with issues: {list}
```

---

### 2. `plan` --- Generate an upgrade runbook

Produce a step-by-step, copy-pasteable upgrade plan based on preflight findings.

**Step 1 -- Determine upgrade strategy**

Decide based on cluster type:
- **kubeadm**: sequential control-plane then worker upgrade
- **EKS/GKE/AKS**: managed control-plane upgrade, then node group rolling update
- **k3s/RKE2**: binary replacement strategy

```bash
# Detect cluster type
PROVIDER="unknown"
kubectl get nodes -o jsonpath='{.items[0].spec.providerID}' 2>/dev/null | grep -qi 'aws' && PROVIDER="eks"
kubectl get nodes -o jsonpath='{.items[0].spec.providerID}' 2>/dev/null | grep -qi 'gce' && PROVIDER="gke"
kubectl get nodes -o jsonpath='{.items[0].spec.providerID}' 2>/dev/null | grep -qi 'azure' && PROVIDER="aks"
kubectl get nodes -o jsonpath='{.items[0].metadata.labels}' 2>/dev/null | grep -q 'node.kubernetes.io/instance-type' || PROVIDER="kubeadm"
echo "Detected provider: $PROVIDER"
```

**Step 2 -- Generate the runbook**

For kubeadm clusters, the runbook follows this structure:

```
## Upgrade Runbook: {CURRENT} -> {TARGET}
Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)

### Pre-upgrade checklist
1. Confirm etcd backup exists:
   ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-pre-upgrade-$(date +%s).db
2. Back up all cluster manifests:
   kubectl get all -A -o yaml > /backup/cluster-state-pre-upgrade.yaml
3. Verify all preflight blockers resolved

### Phase 1: Upgrade first control-plane node
   sudo apt-get update && sudo apt-get install -y kubeadm={TARGET_PATCH}
   sudo kubeadm upgrade plan
   sudo kubeadm upgrade apply v{TARGET}
   sudo apt-get install -y kubelet={TARGET_PATCH} kubectl={TARGET_PATCH}
   sudo systemctl daemon-reload && sudo systemctl restart kubelet

### Phase 2: Upgrade remaining control-plane nodes
   (repeat for each additional CP node, using `kubeadm upgrade node`)

### Phase 3: Upgrade worker nodes (one at a time)
   kubectl drain {NODE} --ignore-daemonsets --delete-emptydir-data
   # On the node:
   sudo apt-get install -y kubeadm={TARGET_PATCH} kubelet={TARGET_PATCH}
   sudo kubeadm upgrade node
   sudo systemctl daemon-reload && sudo systemctl restart kubelet
   # From control plane:
   kubectl uncordon {NODE}
   # Verify node healthy before proceeding to next

### Phase 4: Post-upgrade validation
   kubectl get nodes  # all nodes at new version
   kubectl get pods -A | grep -v Running | grep -v Completed
   kubectl run upgrade-test --image=busybox --rm -it -- echo "cluster healthy"

### Rollback procedure
   If control-plane upgrade fails:
   1. Restore etcd: etcdctl snapshot restore /backup/etcd-pre-upgrade-*.db
   2. Downgrade kubeadm/kubelet packages to {CURRENT} version
   3. Restart kubelet

   If worker node fails after drain:
   1. kubectl uncordon {NODE}
   2. Downgrade kubelet on the node
   3. Restart kubelet
```

**Step 3 -- Estimate timing and risk**

```bash
# Count resources to estimate upgrade duration
NODES=$(kubectl get nodes --no-headers | wc -l)
CP_NODES=$(kubectl get nodes -l node-role.kubernetes.io/control-plane --no-headers 2>/dev/null | wc -l)
WORKER_NODES=$((NODES - CP_NODES))
echo "Estimated time: ~$((CP_NODES * 10 + WORKER_NODES * 8)) minutes"
echo "Control plane nodes: $CP_NODES (~10 min each)"
echo "Worker nodes: $WORKER_NODES (~8 min each with drain/uncordon)"
```

---

### 3. `deprecations` --- Find deprecated APIs in local manifests

Scan local YAML/Helm files for deprecated apiVersions, not just the live cluster.

**Step 1 -- Scan manifest files**

```bash
# Find all YAML manifests in the repository
TARGET_DIR="${1:-.}"

# Known deprecated/removed apiVersions mapped to removal version
python3 << 'PYEOF'
import os, re, sys, yaml

DEPRECATIONS = {
    "extensions/v1beta1": {"removed": "1.22", "replacement": "apps/v1 or networking.k8s.io/v1"},
    "apps/v1beta1": {"removed": "1.16", "replacement": "apps/v1"},
    "apps/v1beta2": {"removed": "1.16", "replacement": "apps/v1"},
    "networking.k8s.io/v1beta1": {"removed": "1.22", "replacement": "networking.k8s.io/v1"},
    "policy/v1beta1": {"removed": "1.25", "replacement": "policy/v1"},
    "rbac.authorization.k8s.io/v1beta1": {"removed": "1.22", "replacement": "rbac.authorization.k8s.io/v1"},
    "admissionregistration.k8s.io/v1beta1": {"removed": "1.22", "replacement": "admissionregistration.k8s.io/v1"},
    "apiextensions.k8s.io/v1beta1": {"removed": "1.22", "replacement": "apiextensions.k8s.io/v1"},
    "storage.k8s.io/v1beta1": {"removed": "1.27", "replacement": "storage.k8s.io/v1"},
    "flowcontrol.apiserver.k8s.io/v1beta1": {"removed": "1.26", "replacement": "flowcontrol.apiserver.k8s.io/v1"},
    "flowcontrol.apiserver.k8s.io/v1beta2": {"removed": "1.29", "replacement": "flowcontrol.apiserver.k8s.io/v1"},
    "autoscaling/v2beta1": {"removed": "1.26", "replacement": "autoscaling/v2"},
    "autoscaling/v2beta2": {"removed": "1.32", "replacement": "autoscaling/v2"},
    "batch/v1beta1": {"removed": "1.25", "replacement": "batch/v1"},
}

target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
findings = []

for root, dirs, files in os.walk(target_dir):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "vendor")]
    for fname in files:
        if not fname.endswith((".yaml", ".yml")):
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath) as f:
                content = f.read()
            for doc in yaml.safe_load_all(content):
                if not isinstance(doc, dict):
                    continue
                api = doc.get("apiVersion", "")
                kind = doc.get("kind", "")
                name = doc.get("metadata", {}).get("name", "unknown")
                if api in DEPRECATIONS:
                    d = DEPRECATIONS[api]
                    findings.append({
                        "file": fpath,
                        "apiVersion": api,
                        "kind": kind,
                        "name": name,
                        "removed_in": d["removed"],
                        "replacement": d["replacement"],
                    })
        except Exception:
            pass

if not findings:
    print("No deprecated APIs found in manifest files.")
else:
    print(f"Found {len(findings)} deprecated API usage(s):\n")
    for f in findings:
        print(f"  {f['file']}")
        print(f"    {f['kind']}/{f['name']}: {f['apiVersion']} -> removed in {f['removed_in']}")
        print(f"    Replace with: {f['replacement']}")
        print()
PYEOF
```

**Step 2 -- Scan Helm templates**

```bash
# Render Helm charts and scan the output
for chart in $(find "${TARGET_DIR}" -name Chart.yaml -exec dirname {} \;); do
  echo "=== Scanning Helm chart: $chart ==="
  helm template test-scan "$chart" 2>/dev/null | \
    python3 -c "
import sys, yaml
for doc in yaml.safe_load_all(sys.stdin):
    if not isinstance(doc, dict): continue
    api = doc.get('apiVersion','')
    if 'beta' in api:
        print(f\"  WARNING: {doc.get('kind','?')}/{doc.get('metadata',{}).get('name','?')} uses {api}\")
" || echo "  (helm template failed -- check values)"
done
```

**Step 3 -- Generate migration patches**

```bash
# For each finding, suggest a sed command to fix the apiVersion
# Example output:
# sed -i 's|apiVersion: policy/v1beta1|apiVersion: policy/v1|' path/to/file.yaml
```

**Report template:**

```
## API Deprecation Scan Report

### Summary
- Files scanned: {N}
- Deprecated APIs found: {N}
- Already removed in current version: {N} (CRITICAL)
- Will be removed in target version: {N} (MUST FIX)
- Deprecated but not yet removed: {N} (SHOULD FIX)

### Findings
| File | Kind/Name | Current API | Removed In | Replacement |
|------|-----------|-------------|------------|-------------|

### Auto-fix commands
{list of sed/yq commands to apply fixes}
```
