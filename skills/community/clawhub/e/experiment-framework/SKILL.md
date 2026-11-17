---
name: experiment-framework
description: Validate, plan and explicitly dispatch provenance-linked ML experiments using the bundled Python runtime, with budget reservations and durable result bundles.
---
# Experiment Framework
The runtime lives in this repository's src directory. Install into an isolated Python environment as described in README.md. A nested installable skill is in skills/experiment-framework.
Start with axexp --help and axexp validate SPEC --machines MACHINES. Planning and launch without --execute write local bundles but do not dispatch workloads. Never describe this as a no-write preview.
Before real execution, confirm the exact source commit, machine, external repositories, credentials, owning budget project and user authorization. Do not weaken the online telemetry, secret handling or atomic reservation/reconciliation checks to make a run succeed.
Butler is an external required CLI for execution; its Python entrypoint can be selected by BUTLER_CLI. RunPod execution also requires a compatible runpod-capacity delegate, selected on PATH or by RUNPOD_CAPACITY_CLI. Neither companion is bundled. Missing dependencies are a blocker to execution, not permission to bypass governance.
Read README.md for dependencies and limits. Do not treat test-only example specs, a planned artifact graph, or passing unit tests as scientific results or a completed remote run.
