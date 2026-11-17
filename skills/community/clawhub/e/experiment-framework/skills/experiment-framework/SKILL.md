---
name: experiment-framework
description: Validate and plan provenance-linked experiment specifications, then dispatch only with explicit authorization and working budget governance.
---
# Experiment Framework
Use scripts/axexp.py as a portable entrypoint to the installed axiotic_experiments runtime. Install the repository first in an isolated Python environment; this skill folder alone is not the runtime.
Run the wrapper with --help, then validate SPEC --machines MACHINES. plan and launch without --execute create local bundles but do not launch workloads.
Before --execute, verify user authority, the source commit, provider resources, external storage destinations and the owning budget project. Keep atomic Butler reservations and outcome reconciliation enabled. Butler is external (BUTLER_CLI); RunPod also needs the external runpod-capacity delegate (PATH or RUNPOD_CAPACITY_CLI). Stop when unavailable.
Credentials belong only in process environments and encrypted in-memory transport, never specs or bundles. Online W&B is required. All shipped examples are test-only structural inputs, not ready-to-run workloads or scientific results.
