---
name: bohrium-dataset
description: "Manage Bohrium datasets via bohr CLI or open.bohrium.com API. Use when: user asks about creating/listing/deleting datasets on Bohrium, uploading data, or managing dataset versions. NOT for: file management, job submission, or node management."
---

# SKILL: Bohrium Dataset Management

## Overview

Manage datasets on the Bohrium platform. **Prefer `bohr` CLI**; fall back to the API for version management, quota checks, etc.

`bohr dataset create` advantages over web upload: **no size limit** and **resumable upload**.

Datasets solve common pain points:
- Repeated file upload on every job submission -> mount datasets to avoid re-upload
- Large input files with slow upload -> datasets support resumable upload
- Need to share data with collaborators -> datasets support project-level sharing

## Authentication

```json
"bohrium-dataset": {
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
export OPENAPI_HOST=https://open.bohrium.com
```

---

## List Datasets

```bash
bohr dataset list                       # Default: recent 50
bohr dataset list -n 10 --json          # JSON, top 10
bohr dataset list -p 154                # Filter by project ID
bohr dataset list -t "my-dataset"       # Search by title
```

**JSON fields:** `id`, `title`, `path` (mount path like `/bohr/my-dataset/v1`), `projectName`, `creatorName`, `updateTime`, `desc`

---

## Create Dataset (Upload Data)

```bash
bohr dataset create \
  -n "my-dataset" \
  -p "my-dataset" \
  -i 154 \
  -l "/path/to/local/data"
```

| Parameter | Short | Required | Description |
|-----------|-------|----------|-------------|
| `--name` | `-n` | Yes | Dataset name |
| `--path` | `-p` | Yes | Dataset path identifier (alphanumeric) |
| `--pid` | `-i` | Yes | Project ID |
| `--lp` | `-l` | Yes | Local data directory path |
| `--comment` | `-m` | No | Description |

> **Resumable upload**: If interrupted (network issues, etc.), re-run the same command and enter `y` to resume from breakpoint.

---

## Using Datasets

### Mount in Compute Jobs

Add `dataset_path` to `job.json`:

```json
{
  "job_name": "DeePMD-kit test",
  "command": "cd se_e2_a && dp train input.json",
  "project_id": 154,
  "machine_type": "c4_m15_1 * NVIDIA T4",
  "job_type": "container",
  "image_address": "registry.dp.tech/dptech/deepmd-kit:2.1.5-cuda11.6",
  "dataset_path": ["/bohr/my-dataset/v1", "/bohr/another-dataset/v2"]
}
```

> `dataset_path` and `-p` (input directory) can be used simultaneously.

### Mount on Dev Nodes

Select datasets when creating a container node; access via path (e.g. `/bohr/my-dataset/v1`).

- Adds 2-4s boot delay (regardless of count)
- Use `df -a | grep bohr` to view mount points

### Use in Notebooks

1. Expand side panel in Notebook editor -> Select existing datasets
2. Hover dataset name -> click copy to get path
3. Use in code: `cd /bohr/testdataset-6xwt/v1/`

> Datasets must be added **before** connecting to the node. Adding afterward requires a node restart.

---

## Version Management

Datasets support multi-version management. Files within a version are immutable once created.

### Create New Version

Via Web UI: Dataset details -> "New Version" -> system imports latest version files -> add/remove files -> Create.

Via API:
```python
requests.post(f"{BASE}/{dataset_id}/version", headers=HEADERS_JSON,
    json={"versionDesc": "v2 update"})
```

Preparation time depends on file size and count.

---

## Delete Datasets

```bash
bohr dataset delete 138201              # Single
bohr dataset delete 138201 108601       # Batch
```

> Deleted versions cannot be recovered.

---

## Permission Model

| Permission | Description | Default holders |
|-----------|-------------|-----------------|
| Manageable | Edit, delete, create versions | Dataset creator, project creator/admin |
| Usable | View and use | All project members |

> "Usable" permission can be granted to other projects or users via editing.

---

## API Supplement (CLI Unsupported)

```python
import os, requests

AK = os.environ.get("ACCESS_KEY", "")
BASE = "https://open.bohrium.com/openapi/v1/ds"
HEADERS = {"accessKey": AK}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}

# Dataset details
r = requests.get(f"{BASE}/{dataset_id}", headers=HEADERS)

# Version list
r = requests.get(f"{BASE}/{dataset_id}/version", headers=HEADERS)
# Returns: [{version, totalCount, totalSize, downloadUri, datasetPath, ...}]

# Specific version
r = requests.get(f"{BASE}/{dataset_id}/version/{version_id}", headers=HEADERS)

# Create via API
r = requests.post(f"{BASE}/", headers=HEADERS_JSON, json={
    "title": "my-dataset", "projectId": 154,
    "identifier": "my-dataset",  # Required, unique ID
})
# Returns: {datasetId, tiefbluePath, requestId}
# Then upload files via tiefblue, then call commit

# Commit
requests.put(f"{BASE}/commit", headers=HEADERS_JSON,
    json={"datasetId": dataset_id})

# New version
requests.post(f"{BASE}/{dataset_id}/version", headers=HEADERS_JSON,
    json={"versionDesc": "v2 update"})

# Update info
requests.put(f"{BASE}/{dataset_id}", headers=HEADERS_JSON,
    json={"title": "new-title"})

# Delete version
requests.delete(f"{BASE}/{dataset_id}/version/{version_id}", headers=HEADERS)

# Check quota
r = requests.get(f"{BASE}/quota/check", headers=HEADERS,
    params={"projectId": 154})
# Returns: {result: true, limit: 30, used: 5}

# Upload token (for tiefblue)
r = requests.get(f"{BASE}/input/token", headers=HEADERS,
    params={"projectId": 154, "path": "/bohr/my-dataset"})

# Permissions
r = requests.get(f"{BASE}/{dataset_id}/permission", headers=HEADERS)

# Associated projects
r = requests.get(f"{BASE}/project", headers=HEADERS)
```

**Important**: The dataset list API path is `GET /v1/ds/` (**with trailing slash**), not `/v1/ds/list` (`/list` gets caught by the `/:id` route).

---

## Status Codes

| status | Meaning |
|--------|---------|
| 1 | Creating / uncommitted |
| 2 | Committed / available |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Upload interrupted | Network instability | Re-run same command, enter `y` to resume |
| Dataset path not found | Wrong mount path | Check `path` with `bohr dataset list --json` |
| Job can't access dataset | Not in job.json | Add `"dataset_path": ["/bohr/xxx/v1"]` |
| `/ds/list` returns error | Route caught by `/:id` | Use `GET /ds/` (root path) |
| Missing `identifier` error | Required field | Add `identifier` (alphanumeric) |
| Version preparing (~5 min) | Files being copied | Large files take time; contact support on failure |
| Dataset unavailable in Notebook | Added after node connection | Restart node to take effect |
