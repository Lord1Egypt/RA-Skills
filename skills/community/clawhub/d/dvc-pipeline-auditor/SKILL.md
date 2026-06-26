---
name: cm-dvc-pipeline-auditor
description: Audit DVC (Data Version Control) pipelines for reproducibility, storage efficiency, and tracking correctness. Checks dvc.yaml, dvc.lock, .dvc files, remote storage configuration, pipeline stage dependencies, parameter management, and metric tracking. Use when asked to review DVC setup, audit data pipelines, check reproducibility, analyze DVC storage, review pipeline stages, or troubleshoot DVC issues. Triggers on "dvc", "data version control", "dvc pipeline", "dvc.yaml", "dvc remote", "dvc push", "dvc pull", "dvc repro", "data versioning", "ml pipeline", "dvc metrics", "dvc params".
metadata:
  tags: ["dvc", "data-versioning", "mlops", "pipeline", "reproducibility", "data-engineering", "version-control", "ml-pipeline", "experiment-tracking", "data-management"]
---

# DVC Pipeline Auditor

Audit DVC (Data Version Control) pipelines for reproducibility, storage efficiency, and operational correctness. Reviews dvc.yaml pipeline definitions, .dvc file tracking, remote storage configuration, parameter management, metric collection, and dependency chains. Acts as a senior ML engineer auditing your data versioning and pipeline infrastructure.

## Usage

**Basic:** `Audit the DVC pipeline in /path/to/project/`
**Focused:** `Check pipeline stage dependencies` | `Find .dvc files out of sync` | `Analyze DVC storage usage` | `Review params.yaml structure`

## How It Works

### Step 1: Discover DVC Project Structure

```bash
find /path/to/project -name ".dvc" -type d
cat /path/to/project/.dvc/config
find /path/to/project -name "dvc.yaml" -o -name "dvc.lock" -o -name "*.dvc"
find /path/to/project -name "params.yaml" -o -name "params.json"
```

Parses pipeline stages (cmd, deps, outs, params, metrics, plots), lock file hashes, .dvc tracking metadata, and remote configuration.

### Step 2: Audit Pipeline Stages

```
  Stage: prepare
    PASS: Script in deps — changes trigger re-run
    PASS: Params explicitly listed, output directory tracked

  Stage: train
    PASS: Dependencies chain from prepare outputs
    PASS: Metrics with cache:false — committed to git

  FAIL: No evaluation stage defined
    Pipeline trains but never evaluates on holdout set
    FIX: Add evaluate stage with model + test data as deps

  FAIL: Stage "featurize" missing dependency
    cmd uses config.yaml but it's NOT listed in deps
    RISK: config changes won't trigger re-run
    FIX: Add "config.yaml" to deps

  FAIL: Stage "train" has undeclared output
    Script writes logs/training.log but not listed in outs
    FIX: Add to outs or explicitly exclude
```

### Step 3: Validate Dependency Graph

```
  prepare -> featurize -> train -> evaluate -> export_model
  Depth: 4 | No circular deps | No orphan stages

  FAIL: Implicit dependency — "train" reads data/prepared/features.csv
    produced by "featurize", but deps reference data/prepared/ (from prepare)
    FIX: Change dep to data/features/ (featurize output)

  WARN: "export_model" has no downstream consumers — verify terminal stage
```

### Step 4: Check Lock File Integrity

```
  FAIL: dvc.lock is STALE
    Stage "prepare" lock hash doesn't match current src/prepare.py
    RISK: Pipeline results don't reflect current code
    FIX: Run `dvc repro prepare`

  FAIL: dvc.lock references deleted file src/old_featurize.py
    FIX: Update dvc.yaml dep, run `dvc repro featurize`

  WARN: dvc.lock not committed to git
    RISK: Collaborators can't reproduce exact pipeline state
    FIX: Ensure dvc.lock is tracked (NOT in .gitignore)
```

### Step 5: Audit .dvc File Tracking

```
  8 tracked files, 4.7 GB total

  FAIL: data/raw/users.csv — hash mismatch
    Local file modified but .dvc not updated
    FIX: `dvc add data/raw/users.csv`

  FAIL: models/model_v2.pkl — .dvc exists but file missing locally
    Not in cache either. FIX: `dvc pull models/model_v2.pkl`

  WARN: 3 large files (1.4 GB total) NOT tracked by DVC
    data/embeddings/vectors.npy (890 MB)
    models/backup_model.pkl (320 MB)
    data/external/reference.parquet (180 MB)
    RISK: Committed to git (bloating) or untracked (lost on clone)
    FIX: `dvc add <file>` for each

  WARN: data/raw/transactions.csv — 2.1 GB CSV
    Consider Parquet for 60-80% size reduction
```

### Step 6: Review Remote Storage

```
  Remotes: "storage" (default, s3://ml-data-bucket/dvc-store/),
           "backup" (gs://backup-bucket/dvc/)

  FAIL: No authentication configured for "storage"
    .dvc/config.local missing. `dvc push`/`pull` will fail.
    FIX: `dvc remote modify --local storage access_key_id <KEY>`

  FAIL: Remote "backup" has never been pushed to
    Disaster recovery not functioning.
    FIX: `dvc push -r backup`

  WARN: No shared cache configured
    FIX: `dvc cache dir /shared/dvc-cache` on shared machines

  Storage: 4.7 GB tracked, 3.2 GB remote (32% dedup savings)
  RECOMMEND: `dvc gc -c` to clean ~800 MB unused cache
```

### Step 7: Audit Parameters and Metrics

```
  FAIL: Duplicate parameter "learning_rate" in params.yaml AND params/train.yaml
    Values differ (0.01 vs 0.001). FIX: Single source of truth

  FAIL: Unused param "model.dropout" — no stage references it
    FIX: Remove or wire into training script

  WARN: Hardcoded values in src/train.py
    batch_size=64, num_epochs=100 should be in params.yaml

  WARN: Only 1 plot defined. Add confusion matrix, ROC, feature importance.
  WARN: No `dvc exp` usage — switch to `dvc exp run` for experiment tracking
```

### Step 8: Check Reproducibility

```
  FAIL: Python version not pinned (no .python-version)
  FAIL: Deps not fully pinned: "scikit-learn>=1.0", "pandas" (any version)
    FIX: `pip freeze > requirements.txt` for exact versions

  FAIL: Random seed only set for numpy, not Python random or torch
    RISK: Non-deterministic results across runs

  WARN: System dep (ffmpeg) not documented — affects output but untracked
  WARN: No CI/CD running `dvc repro --dry` on PRs

  Reproducibility Score: 45/100
```

### Step 9: Final Report

```
# DVC Pipeline Audit Report

## Overall Health Score: 54/100
  Pipeline structure: 7/10    Lock integrity: 4/10
  Data tracking: 5/10         Remote storage: 5/10
  Parameters: 5/10            Metrics/plots: 4/10
  Reproducibility: 3/10       Stage deps: 6/10

## Critical Issues
  1. Lock file stale — results don't match current code
  2. Hash mismatch on users.csv — data change not versioned
  3. 1.4 GB of large files not tracked by DVC
  4. No remote authentication — push/pull will fail
  5. Dependencies not pinned — non-reproducible environment

## High Priority
  6. Missing evaluation stage
  7. Duplicate parameter definitions
  8. No CI/CD pipeline validation on PRs
  9. Hardcoded hyperparameters
  10. Partial random seeds — non-deterministic results
```

## Output

- **Pipeline graph** with dependency validation and issue annotations
- **Lock file integrity** check with staleness detection
- **Data tracking audit** covering hash mismatches and untracked large files
- **Remote storage review** for auth, efficiency, and backup status
- **Parameter audit** for duplicates, hardcoded values, unused params
- **Reproducibility score** covering deps, seeds, CI/CD validation
- **Health score** 0-100 with per-category breakdown and remediation commands

## Tips for Best Results

- Point the agent at your project root (where .dvc/ directory lives)
- Include source code (src/) to detect hardcoded values
- Share requirements.txt for dependency analysis
- Run after adding new pipeline stages to catch dependency issues
- Combine with mlops-experiment-tracker for full ML workflow audit
