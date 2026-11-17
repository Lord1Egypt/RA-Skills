# Experiment Framework
A Python runtime and agent skill for machine-neutral ML experiment specifications, local/SSH execution, RunPod delegation, durable metrics, and cross-linked provenance bundles.

This is a public export of a working-tree runtime, including safety improvements to atomic Butler budget reservations and outcome reconciliation. It is not a transcript-derived prompt pack. The Python import name remains axiotic_experiments for compatibility. Private machine registries, research runs, provider accounts, logs, repository history and installed environment are not included.

## Install
Python 3.11+ and Git are required. In this repository:
```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/axexp --help
```
Runtime dependencies are declared in pyproject.toml: huggingface-hub, tomli-w and wandb. Use your environment's Python executable when invoking the skill wrapper. For agent discovery, copy skills/experiment-framework to the agent's skills directory after installing the runtime. The root skill entrypoint also supports `npx skills add AntreasAntoniou/experiment-framework`; this optional Node.js installer does not install the Python runtime or external governance tools.

## Start without launching
```sh
axexp validate examples/local-smoke.toml --machines machines.toml
axexp plan examples/local-smoke.toml --machines machines.toml --output /absolute/path/to/private-plan
```
The shipped examples are labelled structural test-only configurations. Account names and commits are placeholders, not real data or working provider setup. Customize them from your own authorized experiment before execution. Planning writes local bundles; it is not a no-write operation.
Use axexp launch --help for launch options. Without --execute, launch produces a plan only. --execute may consume compute and write to external W&B, Hugging Face and GitHub resources.

The flag is specific to launch, not a universal dry-run switch: checkpoint-upload,
dataset-upload and results-replay write to remote services directly and require
explicit authority. checkpoint-fetch downloads data; doctor may contact remote
hosts. Inspect the selected subcommand's help and target before running it.

## Governance and external prerequisites
Every real local/SSH launch resolves the external Butler Python CLI (BUTLER_CLI or a supported skill location); GPU workloads must receive an atomic gpu-reserve result for the exact job, then gpu-reconcile after the outcome. Read-only gpu-gate is not launch authority. This export preserves fail-closed behavior; it does not bundle Butler or create a budget bypass for CPU jobs.
RunPod execution delegates to a compatible runpod-capacity tool, found on PATH or through RUNPOD_CAPACITY_CLI pointing to its Python entrypoint. The delegate must provide its own budget governance and reconciliation contract. It is not included; adapter generation works without it, but real RunPod execution does not. SSH also requires working SSH access, a compatible remote Python/runtime environment and source access.
W&B online telemetry and authenticated W&B/Hugging Face/GitHub destinations are runtime requirements, not optional offline mocks. Credentials are environment-only and are redacted from plans; configure them outside this repository.

## Tests
```sh
python -m unittest discover -s tests -t . -v
python scripts/check_secrets.py
```
The suite uses isolated structural fixtures and mocked services; it does not launch a cloud job. Passing it is not evidence that provider configuration, live dispatch, remote cleanup or scientific results have been verified. No real benchmark/demo dataset is included.

## Limitations
This is an early runtime, not a hosted platform or a complete portable research environment. The artifact graph checks linkage shape, not the truth or availability of every linked remote object. Source hashes and tests are not deployment receipts. Review generated bundles before publishing them; operational paths, metadata and experiment outputs can be sensitive.
