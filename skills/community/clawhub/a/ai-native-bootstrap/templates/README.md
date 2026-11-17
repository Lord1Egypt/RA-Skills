# AI-Native SDLC — repository contract

- Governance source: the existing repository policy, or `AGENTS.md` if created by bootstrap. This folder holds **change evidence**, not an alternative master policy.
- Scope: no business changes, dependencies, remote operations, production release, or database migrations are authorized by installing these files.
- Paths: `templates/` contains draft input formats; `changes/<CHANGE-ID>/` is created per actual change (not filled with fictional examples).
- Risk: R0 docs/read-only; R1 safe local checks and templates; R2 identity/payment/db/infrastructure requires separate approval; R3 production operations require independent release authorization.
- Checks: the generated candidate-check manifest lists *observed candidates*, not proven safe commands; enable them only after project owner review. Run the generated local check entrypoint (`check.py`), keep exit codes and logs as evidence.
- CI/branch protection: investigate the actual platform; local files are not proof of remote gating.
- Evals: add cases from genuine historical tasks and accepted outputs; do not manufacture success evidence.
- State: after initial scaffold status is CONDITIONAL until at least one genuine regression, real checks, independent review and applicable external permissions are verified.

Workflow: Intent → Spec (risk-dependent) → Plan → Implementation → Test/Eval → Independent Review → Authorized Release → Feedback into next Intent.

The human product owner approves requirements and release risk; agents can propose and prepare, not self-authorize production.

- Deterministic Evals: the generated cases file is empty until authentic test cases exist. Review and enable genuine cases, then run the generated evaluation entrypoint (`eval.py`). Empty suite exits BLOCKED (2); this is not a substitute for model-quality or human creative evaluation.
