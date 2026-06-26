---
name: bohrium-image
description: "Manage Bohrium container images via bohr CLI or open.bohrium.com API. Use when: user asks about listing/pulling/creating/deleting Docker images on Bohrium, or finding available public images. NOT for: node management, job submission, or project management."
---

# SKILL: Bohrium Image Management

## Overview

Manage container images on the Bohrium platform. **Prefer `bohr` CLI**; fall back to the API for Dockerfile builds and version search.

Since 2023, Bohrium no longer supports VM jobs — container images are required.

## Authentication

```json
"bohrium-image": {
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

## List Images

```bash
bohr image list                 # Custom images (table)
bohr image list --json          # JSON

# Public images by type
bohr image list -t "Basic Image"
bohr image list -t "DeePMD-kit"
bohr image list -t "LAMMPS"
bohr image list -t "ABACUS"
bohr image list -t "CP2K"
bohr image list -t "GROMACS"
bohr image list -t "Uni-Mol"
```

**JSON fields:** `imageId`, `name`, `url`, `status` (available/building), `creatorName`

---

## Quick Reference: Public Images

### Base Images

| Scenario | Image |
|----------|-------|
| CPU | `registry.dp.tech/dptech/ubuntu:20.04-py3.10` |
| CPU + Intel MPI | `registry.dp.tech/dptech/ubuntu:20.04-py3.10-intel2022` |
| GPU | `registry.dp.tech/dptech/ubuntu:20.04-py3.10-cuda11.6` |
| GPU + Intel MPI | `registry.dp.tech/dptech/ubuntu:20.04-py3.10-intel2022-cuda11.6` |

### Scientific Software

| Software | Image |
|----------|-------|
| DeePMD-kit | `registry.dp.tech/dptech/deepmd-kit:2.1.5-cuda11.6` |
| DPGEN | `registry.dp.tech/dptech/dpgen:0.10.6` |
| LAMMPS | `registry.dp.tech/dptech/lammps:29Sep2021` |
| GROMACS | `registry.dp.tech/dptech/gromacs:2022.2` |
| Quantum-Espresso | `registry.dp.tech/dptech/quantum-espresso:7.1` |
| CP2K | `registry.dp.tech/dptech/cp2k:7.1` |
| ABACUS | `registry.dp.tech/dptech/abacus:3.0.0` |

### Pre-installed Software (All Public Images)

| Category | Software |
|----------|----------|
| Python | python3.10, pip, Anaconda, Jupyter Lab |
| File tools | wget, curl, unzip, rsync, tree, git |
| Editors | emacs, vim |
| Build tools | cmake, build-essential (GNU) |
| Monitoring | htop, ncdu, net-tools |
| DP tools | Bohrium CLI, DP-Dispatcher, dpdata |

---

## VM-to-Container Image Mapping

| VM Image | Container Image |
|----------|----------------|
| `LBG_DeePMD-kit_2.1.4_v1` | `registry.dp.tech/dptech/deepmd-kit:2.1.5-cuda11.6` |
| `LBG_DP-GEN_0.10.6_v3` | `registry.dp.tech/dptech/dpgen:0.10.6` |
| `LBG_LAMMPS_stable_23Jun2022_v1` | `registry.dp.tech/dptech/lammps:29Sep2021` |
| `gromacs-dp:2020.2` | `registry.dp.tech/dptech/gromacs:2022.2` |
| `LBG_Quantum-Espresso_7.1` | `registry.dp.tech/dptech/quantum-espresso:7.1` |
| `LBG_Common_v1/v2` | `registry.dp.tech/dptech/ubuntu:20.04-py3.10-cuda11.6` |
| `LBG_oneapi_2021_v1` | `registry.dp.tech/dptech/ubuntu:20.04-py3.10-intel2022-cuda11.6` |

---

## Pull Image to Local

```bash
bohr image pull registry.dp.tech/dptech/deepmd-kit:3.0.0b3-cuda12.1
```

> Requires Docker running locally. Only public and your own custom images are supported.

### Manual Docker Pull (Alternative)

Replace domain with `registry.bohrium.dp.tech` (not `registry.dp.tech`):

```bash
docker login registry.bohrium.dp.tech
docker pull registry.bohrium.dp.tech/dptech/ubuntu:22.04-py3.10-intel2022
# Push is not supported
```

---

## Delete Custom Images

```bash
bohr image delete 121510
bohr image delete 121510 121395         # Batch
```

---

## Image Cache

| Scenario | Details |
|----------|---------|
| Public images | Persistent cache; no extra pull time |
| New custom images | Cache builds in 10-30 min; wait before using |
| Unused 30 days | Cache expires; re-pull on next use |
| With cache | CPU ~20s boot, GPU ~40s boot |
| Without cache | +10-30 min for image pull |

---

## API Supplement (CLI Unsupported)

### Search Public Image Versions

```python
import os, requests
AK = os.environ.get("ACCESS_KEY", "")
HEADERS = {"accessKey": AK}

r = requests.get("https://open.bohrium.com/openapi/v2/image/public/version/search",
    headers=HEADERS, params={"keyword": "deepmd", "page": 1, "pageSize": 5})
# Returns: {items: [{version, resourceType, size, url, imageName}, ...]}
```

### Browse Public Images

```python
r = requests.get("https://open.bohrium.com/openapi/v2/image/public",
    headers=HEADERS, params={"page": 1, "pageSize": 10})

r = requests.get(f"https://open.bohrium.com/openapi/v2/image/public/{image_id}/version",
    headers=HEADERS, params={"page": 1, "pageSize": 10})
```

### Build from Dockerfile

```python
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}

# Note: dockerfile field must be base64-encoded
import base64
dockerfile_content = "FROM ubuntu:22.04\nRUN apt-get update && apt-get install -y python3"
dockerfile_b64 = base64.b64encode(dockerfile_content.encode()).decode()

r = requests.post("https://open.bohrium.com/openapi/v2/image/private",
    headers=HEADERS_JSON, json={
        "name": "my-image", "projectId": 154, "device": "container",
        "desc": "Custom training image", "buildType": 1,
        "dockerfile": dockerfile_b64,
    })

# Validate Dockerfile (also requires base64)
check_b64 = base64.b64encode(b"FROM ubuntu:22.04\nRUN apt-get update").decode()
requests.post("https://open.bohrium.com/openapi/v2/image/dockerfile/check",
    headers=HEADERS_JSON, json={"dockerfile": check_b64})
```

### Private Image Management

```python
# List (must include device and type parameters)
r = requests.get("https://open.bohrium.com/openapi/v2/image/private",
    headers=HEADERS, params={"device": "container", "type": "private", "page": 1, "pageSize": 10})
# Returns: {items: [{id, name, url, status, buildType, creatorName, projectName, ...}]}

# Share / unshare
requests.post(f"https://open.bohrium.com/openapi/v2/image/{image_id}/share", headers=HEADERS_JSON)
requests.delete(f"https://open.bohrium.com/openapi/v2/image/{image_id}/share?device=container", headers=HEADERS)
```

---

## Custom Image Creation

After installing software on a container node, save the environment as a custom image via the Bohrium web UI. Only the system disk is saved; `/personal` and `/share` are excluded.

## Quotas

| Resource | Limit |
|----------|-------|
| Custom images | 10 per project |

## Unavailable Endpoints

| Endpoint | Version | Reason |
|----------|---------|--------|
| `GET v1/image/public` | v1 | Caught by `/:imageId` route |
| `GET v1/image/private` | v1 | Same |
| `POST v2/image/version/add` | v2 | Not registered |
| `DELETE v2/image/version/{versionId}` | v2 | Not registered |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `bohr image pull` fails | Docker not running | Start Docker Desktop |
| v2 private param error | Missing required params | Add `device=container&type=private` parameters |
| `no permission` | Not image creator | Can only manage own images |
| v1 `/public` parse error | Route conflict | Use v2 endpoints |
| Wrong image address | Used name, not full URL | Must use `registry.dp.tech/dptech/xxx:tag` |
| Slow custom image cache | Cache takes 10-30 min | Wait 30 min after build |
| No Docker in container | Security restriction | Use VM image `LBG_Common_v2` |
| Create returns decode err | dockerfile not base64 encoded | Use `base64.b64encode(content.encode()).decode()` |
