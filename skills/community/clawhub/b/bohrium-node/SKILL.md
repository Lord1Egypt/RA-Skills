---
name: bohrium-node
description: "Manage Bohrium dev nodes (containers/VMs) via bohr CLI or open.bohrium.com API. Use when: user asks about creating/starting/stopping/deleting dev machines on Bohrium, checking available resources and pricing, or managing node lifecycle. NOT for: job submission, image management, or project management."
---

# SKILL: Bohrium Dev Node Management

## Overview

Manage dev nodes (container/VM instances) on the Bohrium platform. **Prefer `bohr` CLI**; fall back to the API for unsupported operations.

Dev nodes are used for data preparation, compilation, debugging, and post-processing. They support Web Shell and SSH connections.

## Authentication

```json
"bohrium-node": {
  "enabled": true,
  "apiKey": "YOUR_ACCESS_KEY",
  "env": { "ACCESS_KEY": "YOUR_ACCESS_KEY" }
}
```

## Prerequisites: Install bohr CLI

```bash
# macOS
/bin/bash -c "$(curl -fsSL https://dp-public.oss-cn-beijing.aliyuncs.com/bohrctl/1.0.0/install_bohr_mac_curl.sh)"
# Linux
/bin/bash -c "$(curl -fsSL https://dp-public.oss-cn-beijing.aliyuncs.com/bohrctl/1.0.0/install_bohr_linux_curl.sh)"
source ~/.bashrc && export PATH="$HOME/.bohrium:$PATH"
```

---

## List Nodes

```bash
bohr node list                  # All nodes (table)
bohr node list --json           # JSON
bohr node list -s               # Running only
bohr node list -p               # Paused only
bohr node list -d               # Pending only
bohr node list -w               # Waiting only
bohr node list -q               # ID and name only
```

**JSON fields:** `nodeId`, `nodeName`, `status` (Started/Paused/Pending/Waiting), `cpu`/`memory`/`gpu`, `ip`, `imageName`, `cost`

---

## Create Node

```bash
bohr node create    # Interactive: Project -> Image -> Machine -> Name -> Disk
```

> `bohr node create` is interactive. For automation, use the API (see below).

**Recommended images:**

| Scenario | Image |
|----------|-------|
| CPU basic | `registry.dp.tech/dptech/ubuntu:20.04-py3.10` |
| CPU + Intel MPI | `registry.dp.tech/dptech/ubuntu:20.04-py3.10-intel2022` |
| GPU basic | `registry.dp.tech/dptech/ubuntu:20.04-py3.10-cuda11.6` |
| GPU + Intel MPI | `registry.dp.tech/dptech/ubuntu:20.04-py3.10-intel2022-cuda11.6` |

---

## Connect to Node

```bash
bohr node connect 1431145       # Passwordless SSH via nodeId
```

Alternative: **Web Shell** via the Bohrium web UI (auto-login as root), or manual SSH using credentials from the API.

---

## Stop / Delete

```bash
bohr node stop 1431145          # Stop (pause billing, data preserved)
bohr node delete 1431145        # Delete (irreversible)
```

> **Important**: Nodes are billed continuously while running. Stop or delete when not in use.

---

## Storage & Networking

| Item | Details |
|------|---------|
| **System disk** | Selected at creation (max 100GB); stores OS packages |
| **Personal disk /personal** | 500GB per user per project; persists after node release |
| **Shared disk /share** | 1TB per project; read/write for all members |
| **Public ports** | 50001-50005 open by default |
| **GPU driver** | v525 default; cannot upgrade |
| **Docker** | **Not supported** inside container nodes (security) |

---

## Dataset Mounting

Mount datasets when creating a container node; access via path (e.g. `/bohr/my-dataset/v1`).

- Adds 2-4s boot delay (regardless of dataset count)
- Use `df -a | grep bohr` to view mount points

---

## Boot Time & Image Cache

| Scenario | Boot time |
|----------|-----------|
| Cached CPU machine | ~20s |
| Cached GPU machine | ~40s |
| GPU under resource pressure | 1-5 min |
| No cache (new/expired image) | 10-30 min (image pull) |

**Cache rules:**
- Public images have persistent cache
- Custom images: cache builds in 10-30 min after creation; wait before using
- Custom images unused for 30 days: cache expires, re-pull required
- Billing starts from resource allocation, even during image pull

---

## API Supplement (CLI Unsupported)

```python
import os, requests

AK = os.environ.get("ACCESS_KEY", "")
BASE = "https://open.bohrium.com/openapi/v1/node"
HEADERS = {"accessKey": AK}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}

# Programmatic node creation (non-interactive)
r = requests.post(f"{BASE}/add", headers=HEADERS_JSON, json={
    "projectId": 154, "name": "my-node", "imageId": 2168,
    "machineConfig": {"type": 0, "value": 388, "label": "c2_m4_cpu"},
    "diskSize": 20,
})
# Returns: {"code": 0, "data": {"machineId": 1427300}}

# Available resources
r = requests.get(f"{BASE}/resources", headers=HEADERS)
# Returns: {disks, cpuList, gpuList} — value = skuId

# Resource pricing
r = requests.get(f"{BASE}/resources/price", headers=HEADERS,
    params={"skuId": 388, "projectId": 154})
# Returns: {"data": {"price": "0.4"}}  (CNY/hour)

# Node details (includes SSH password)
r = requests.get(f"{BASE}/{machine_id}", headers=HEADERS)
# Returns: {nodeId, nodeName, status, ip, nodeUser, nodePwd, domainName, ...}

# Restart (must stop first)
requests.post(f"{BASE}/restart/{machine_id}", headers=HEADERS)

# Rename
requests.post(f"{BASE}/modify/{machine_id}", headers=HEADERS_JSON,
    json={"name": "new-name"})

# View/bind datasets
r = requests.get(f"{BASE}/ds", headers=HEADERS, params={"nodeId": node_id})
requests.post(f"{BASE}/ds/bind", headers=HEADERS_JSON,
    json={"nodeId": node_id, "datasetId": dataset_id})
```

---

## Status Codes

| status | Meaning | CLI Display |
|--------|---------|-------------|
| 2 | Running | Started |
| -1 | Stopped/Released | Paused |

## Quotas

| Resource | Limit |
|----------|-------|
| Nodes | 4 per user per project |
| System disk | Max 100GB |
| Personal disk | 500GB per user per project |
| Shared disk | 1TB per project |

## SSH vs Web Shell Environment

| Method | Env var source |
|--------|---------------|
| Web Shell | System env + `/root/.bashrc` |
| SSH | `/root/.bashrc` only (overwrites globals) |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `No resource for selected machine` | Out of stock | Try another spec or retry later |
| `record not found` | Invalid machineId | Verify with `bohr node list --json` |
| Restart fails | Node not stopped | `bohr node stop` first, wait for Paused |
| `nodeId` vs `machineId` | Two different IDs | CLI uses `nodeId`; API uses `machineId`; dataset API uses `nodeId` |
| SSH fails | Image lacks SSH | DockerHub images need manual sshd install |
| Domain not resolving | Stopped >7 days | Restart; wait 10-30 min for DNS; use Web Shell meanwhile |
| Slow terminal | VPN/network or browser memory | Disable VPN; refresh page |
| Cannot run Docker | Container security | Use VM image `LBG_Common_v2` |
| Image pulling | Cache not ready or expired | Wait 10-30 min after build |
