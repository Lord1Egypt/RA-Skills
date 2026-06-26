---
name: bohrium-job
description: "Manage Bohrium compute jobs via bohr CLI or open.bohrium.com API. Use when: user asks about submitting/listing/killing/deleting compute jobs on Bohrium, checking job logs, or monitoring job status. NOT for: node management, image management, or project management."
---

# SKILL: Bohrium Job Management

## Overview

Manage compute jobs on the Bohrium platform. **Prefer `bohr` CLI**; fall back to the API only for advanced operations not supported by the CLI.

## Authentication

ACCESS_KEY and PROJECT_ID are read from the OpenClaw config `~/.openclaw/openclaw.json`:

```json
"bohrium-job": {
  "enabled": true,
  "apiKey": "YOUR_ACCESS_KEY",
  "env": {
    "ACCESS_KEY": "YOUR_ACCESS_KEY",
    "PROJECT_ID": "YOUR_PROJECT_ID"
  }
}
```

OpenClaw automatically injects `env` variables into the runtime. The `bohr` CLI authenticates via the `ACCESS_KEY` environment variable.

## Prerequisites: Install bohr CLI

```bash
# macOS
/bin/bash -c "$(curl -fsSL https://dp-public.oss-cn-beijing.aliyuncs.com/bohrctl/1.0.0/install_bohr_mac_curl.sh)"

# Linux
/bin/bash -c "$(curl -fsSL https://dp-public.oss-cn-beijing.aliyuncs.com/bohrctl/1.0.0/install_bohr_linux_curl.sh)"

# Verify
source ~/.bashrc  # or source ~/.zshrc
export PATH="$HOME/.bohrium:$PATH"
bohr version
```

> The installer auto-configures `OPENAPI_HOST` and `TIEFBLUE_HOST`. If they don't take effect, set manually:
> ```bash
> export OPENAPI_HOST=https://open.bohrium.com
> export TIEFBLUE_HOST=https://tiefblue.dp.tech
> ```

---

## Submit Jobs

### Method 1: CLI Arguments (Recommended)

```bash
bohr job submit \
  -m "registry.dp.tech/dptech/deepmd-kit:3.1.1" \
  -t "c4_m15_1 * NVIDIA T4" \
  -c "python train.py" \
  -p ./input_dir/ \
  --project_id 154 \
  -n "my-job-name"
```

**Parameters:**

| Parameter | Short | Required | Description |
|-----------|-------|----------|-------------|
| `--image_address` | `-m` | Yes | Full image URL (e.g. `registry.dp.tech/dptech/xxx:tag`) |
| `--machine_type` | `-t` | Yes | Machine spec |
| `--command` | `-c` | Yes | Command to execute |
| `--input_directory` | `-p` | No | Input file directory (default `./`) |
| `--project_id` | | Yes | Project ID |
| `--job_name` | `-n` | No | Job name |
| `--log_file` | `-l` | No | Log file path |
| `--result_path` | `-r` | No | Auto-download results path (only `/data`, `/personal`, `/share`) |
| `--job_group_id` | `-g` | No | Job group ID (create with `bohr job_group create`) |
| `--max_run_time` | | No | Max run time (minutes); auto-terminates on timeout |
| `--max_reschedule_times` | | No | Auto-retry count after abnormal interruption |
| `--nnode` | | No | Parallel compute node count (default 1) |

### Method 2: Config File (For Complex Scenarios)

```bash
bohr job submit -i job.json -p ./input_dir/
```

**Full job.json example:**

```json
{
  "job_name": "my-training-job",
  "command": "python train.py --epochs 10",
  "log_file": "train.log",
  "backward_files": ["model.pt", "results/"],
  "project_id": 154,
  "machine_type": "c4_m15_1 * NVIDIA T4",
  "image_address": "registry.dp.tech/dptech/deepmd-kit:3.1.1",
  "job_type": "container",
  "disk_size": 50,
  "dataset_path": ["/bohr/my-dataset/v1"],
  "result_path": "/personal",
  "max_reschedule_times": 2,
  "max_run_time": 120,
  "nnode": 1
}
```

**job.json field reference:**

| Field | Description | Example |
|-------|-------------|---------|
| `job_name` | Job name | `"DeePMD-kit test"` |
| `command` | Command; use **relative paths** | `"cd se_e2_a && dp train input.json"` |
| `log_file` | Log viewable in real-time | `"train.log"` |
| `backward_files` | Files to download; empty = keep all | `["model.pt", "results/"]` |
| `project_id` | Project ID | `154` |
| `machine_type` | Machine spec | `"c4_m15_1 * NVIDIA T4"` |
| `image_address` | Full image URL (not just name) | `"registry.dp.tech/dptech/deepmd-kit:2.1.5-cuda11.6"` |
| `job_type` | Must be `"container"` | `"container"` |
| `dataset_path` | Mounted dataset paths | `["/bohr/my-dataset/v1"]` |
| `result_path` | Auto-collect results to data disk | `"/personal"` |
| `max_run_time` | Max run time (minutes) | `120` |
| `max_reschedule_times` | Retry count on interruption | `2` |
| `disk_size` | Disk size (GB) | `50` |

### Important Notes

| Topic | Details |
|-------|---------|
| **Working directory** | Bohrium auto-`cd`s into the extracted input dir; use **relative paths** |
| **Do NOT** `cd /root/input` | Actual path is `/home/input_lbg-{userId}-{jobId}/`, unpredictable |
| **image_address format** | Must be full URL `registry.dp.tech/dptech/xxx:tag` |
| **machine_type format** | CPU: `c2_m4_cpu`; GPU: `c4_m15_1 * NVIDIA T4` |
| **WAF blocking** | If command triggers Alibaba Cloud WAF (405), write to script, use `bash run.sh` |
| **Large files in -p** | No output? Check for large hidden files causing slow compression |
| **Auto-retry** | `max_reschedule_times` retries on interruption (full re-run) |
| **job_type** | Must be `"container"`; VM jobs deprecated since 2023 |

---

## View Jobs

```bash
bohr job list -n 10              # Recent 10
bohr job list -n 5 --json        # JSON output
bohr job list -r                 # Running only
bohr job list -f                 # Failed only
bohr job list -i                 # Finished only
bohr job list -p                 # Pending only
bohr job list -j 15954383        # Jobs in a specific group
```

### Job Details

```bash
bohr job describe -j 22153612 --json
bohr job describe -j 22153612 -l        # Full details
```

### View/Download Logs

```bash
bohr job log -j 22153612                # View
bohr job log -j 22153612 -o ./logs/     # Download
```

### Download Results

```bash
bohr job download -j 22153612 -o ./results/
bohr job_group download -j 15954383 -o ./results/
```

---

## Manage Jobs

```bash
bohr job terminate 22153612             # Terminate (keep results -> completed)
bohr job kill 22153612                  # Force stop (discard results, keep record)
bohr job delete 22153612                # Delete (remove everything)
bohr job terminate 22153612 22153613    # Batch terminate
bohr job delete 22153612 22153613       # Batch delete
```

**terminate vs kill vs delete:**

| Action | Result files | Record | Status |
|--------|-------------|--------|--------|
| `terminate` | Kept | Kept | -> completed |
| `kill` | Discarded | Kept | -> failed |
| `delete` | Removed | Removed | Disappears |

---

## Job Group Management

```bash
bohr job_group list -n 10 --json
bohr job_group list -s 2026-01-01 -e 2026-03-14     # Date range
bohr job_group create -n "experiment-v1" -p 154
bohr job_group terminate 15954383
bohr job_group delete 15954383
bohr job_group download -j 15954383 -o ./results/
```

> **Note**: `job_group_id` from `bohr job_group create` is for CLI only (`bohr job submit -g <id>`). It differs from the web UI job group ID.

---

## Scientific Software Examples

### DeePMD-kit Training

```json
{
  "job_name": "DeePMD-kit test",
  "command": "cd se_e2_a && dp train input.json > tmp_log 2>&1 && dp freeze -o graph.pb",
  "log_file": "se_e2_a/tmp_log",
  "backward_files": ["se_e2_a/lcurve.out", "se_e2_a/graph.pb"],
  "project_id": 154,
  "machine_type": "c4_m15_1 * NVIDIA T4",
  "job_type": "container",
  "image_address": "registry.dp.tech/dptech/deepmd-kit:2.1.5-cuda11.6"
}
```

### LAMMPS Molecular Dynamics

```json
{
  "job_name": "lammps_tutorial",
  "command": "mpirun -n 32 lmp_mpi -i in.shear > log",
  "log_file": "log",
  "backward_files": [],
  "project_id": 154,
  "machine_type": "c32_m64_cpu",
  "job_type": "container",
  "image_address": "registry.dp.tech/dptech/lammps:29Sep2021"
}
```

### ABACUS First-Principles

```json
{
  "job_name": "ABACUS test",
  "command": "OMP_NUM_THREADS=1 mpirun -np 8 abacus > log",
  "log_file": "log",
  "backward_files": [],
  "project_id": 154,
  "machine_type": "c16_m32_cpu",
  "job_type": "container",
  "image_address": "registry.dp.tech/dptech/abacus:3.0.0"
}
```

### GROMACS Molecular Simulation

```json
{
  "job_name": "bohrium-gmx-example",
  "command": "bash rungmx.sh > log",
  "log_file": "log",
  "backward_files": [],
  "project_id": 154,
  "machine_type": "c16_m62_1 * NVIDIA T4",
  "job_type": "container",
  "image_address": "registry.dp.tech/dptech/gromacs:2022.2"
}
```

### CP2K Quantum Chemistry

```json
{
  "job_name": "CP2K_Si_opt",
  "command": "source /cp2k-7.1/tools/toolchain/install/setup && mpirun -n 16 --allow-run-as-root --oversubscribe cp2k.popt -i input.inp -o output.log",
  "log_file": "output.log",
  "backward_files": ["output.log"],
  "project_id": 154,
  "machine_type": "c16_m32_cpu",
  "job_type": "container",
  "image_address": "registry.dp.tech/dptech/cp2k:7.1"
}
```

---

## Container / VM Image Mapping

| Software | VM Image | Container Image |
|----------|----------|----------------|
| DeePMD-kit | LBG_DeePMD-kit_2.1.4_v1 | `registry.dp.tech/dptech/deepmd-kit:2.1.5-cuda11.6` |
| DPGEN | LBG_DP-GEN_0.10.6_v3 | `registry.dp.tech/dptech/dpgen:0.10.6` |
| LAMMPS | LBG_LAMMPS_stable_23Jun2022_v1 | `registry.dp.tech/dptech/lammps:29Sep2021` |
| GROMACS | gromacs-dp:2020.2 | `registry.dp.tech/dptech/gromacs:2022.2` |
| Quantum-Espresso | LBG_Quantum-Espresso_7.1 | `registry.dp.tech/dptech/quantum-espresso:7.1` |
| CP2K | - | `registry.dp.tech/dptech/cp2k:7.1` |
| ABACUS | - | `registry.dp.tech/dptech/abacus:3.0.0` |
| Base (CPU) | LBG_Common_v1/v2 | `registry.dp.tech/dptech/ubuntu:20.04-py3.10` |
| Base (GPU) | LBG_base_image_ubun20.04 | `registry.dp.tech/dptech/ubuntu:20.04-py3.10-cuda11.6` |
| Intel OneAPI | LBG_oneapi_2021_v1 | `registry.dp.tech/dptech/ubuntu:20.04-py3.10-intel2022-cuda11.6` |

---

## API Supplement (CLI Unsupported Operations)

```python
import os, requests

AK = os.environ.get("ACCESS_KEY", "")
BASE = "https://open.bohrium.com/openapi/v1"
HEADERS = {"accessKey": AK}

# Filter by status (0=pending, 1=running, 2=finished, 3=scheduling, -1=failed)
r = requests.get(f"{BASE}/job/list", headers=HEADERS,
    params={"page": 1, "pageSize": 10, "status": 1})

# Job config (includes file access token)
r = requests.get(f"{BASE}/job/view/conf/{job_id}", headers=HEADERS)
# Returns: {state, baseDir, tempDir, token, host, expires}

# View snapshot
r = requests.get(f"{BASE}/job/{job_id}/snapshot", headers=HEADERS)

# Rename job
requests.post(f"{BASE}/job/{job_id}/modify",
    headers={**HEADERS, "Content-Type": "application/json"},
    json={"name": "new-name"})

# Rename job group
requests.post(f"{BASE}/job_group/{job_group_id}/modify",
    headers={**HEADERS, "Content-Type": "application/json"},
    json={"name": "new-group-name"})
```

---

## Job Status Codes

| status | Meaning | CLI Display |
|--------|---------|-------------|
| 0 | Pending | Pending |
| 1 | Running | Running |
| 2 | Finished | Finished |
| 3 | Scheduling | Scheduling |
| -1 | Failed | Failed |

## Common Machine Types

| machine_type | Description |
|--------------|-------------|
| `c2_m4_cpu` | 2 cores, 4G RAM |
| `c4_m8_cpu` | 4 cores, 8G RAM |
| `c8_m32_cpu` | 8 cores, 32G RAM |
| `c16_m32_cpu` | 16 cores, 32G RAM |
| `c32_m64_cpu` | 32 cores, 64G RAM |
| `c4_m15_1 * NVIDIA T4` | 4 cores, 15G + 1x T4 |
| `c16_m62_1 * NVIDIA T4` | 16 cores, 62G + 1x T4 |
| `c8_m32_1 * NVIDIA V100` | 8 cores, 32G + 1x V100 |
| `c32_m128_4 * NVIDIA V100` | 32 cores, 128G + 4x V100 |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `cd /root/input: No such file` | Absolute path in command | Use **relative paths** |
| `unsupported protocol scheme ""` | Missing env vars | Set `OPENAPI_HOST` and `TIEFBLUE_HOST` |
| `(200, '/account/login', None)` | Old pip lbg | Use Go CLI (`~/.bohrium/bohr`) |
| WAF 405 | Shell keywords in command | Write to script, use `bash run.sh` |
| `Permission error` | Wrong user | Verify ACCESS_KEY |
| `jobId` vs `jobGroupId` | Different concepts | CLI uses `jobId` for kill/terminate/delete |
| No output after submit | Large hidden files in `-p` dir | Check dir size |
| Variable performance | ~30% algorithm variance | Normal |
| Long scheduling | Image caching or resource shortage | Wait or contact support |
| System disk full | Output to system disk | Write to working directory |
| Abnormal interruption | Machine reclaim (rare) | Set `max_reschedule_times` |
