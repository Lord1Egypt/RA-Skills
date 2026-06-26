# DPP Pipeline Runtime

This directory contains the bundled Python runtime for the `dpp-pipeline` skill.

It is not the caller workspace. The skill reads inputs and writes outputs in the directory where the stage scripts are executed, or in `DPP_WORKDIR` when that environment variable is set.

Bundled content:

- `src/dpp_storyboard/`: Python package used by the stage scripts
- `configs/placement_material.json`: material config copied by `scripts/init_workspace.sh`
- `env-example.txt`: sample environment file copied by `scripts/init_workspace.sh` into `.env.example`
- `pyproject.toml`: package metadata used by `scripts/bootstrap_runtime.sh`

Install the runtime dependencies with:

```bash
scripts/bootstrap_runtime.sh
```
