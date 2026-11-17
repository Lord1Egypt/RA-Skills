# Project AI working agreement

Read the ai-sdlc repository contract (the README in the generated ai-sdlc document directory) before major changes. Follow the repository's higher-priority policies and existing contributing standards.

- For new features, interfaces, data or permission changes: record Intent, a risk-appropriate Spec, Plan and Acceptance under the per-change record folder of the ai-sdlc document directory.
- For small low-risk fixes: a concise change record and actual verification are sufficient.
- Do not implement a significant change before the plan is reviewed. Treat agent recommendations as proposals, not human approval.
- Run the generated local check entrypoint (`check.py`) after configuring and verifying actual project checks in the generated candidate-check manifest. Until configured, report BLOCKED; never claim PASS.
- Do not skip failing tests, fabricate evidence, print credentials, alter production data, deploy, approve/merge PRs or overwrite user changes without separate authorization.
- Before code changes: inspect Git status, protected paths, dependencies, existing CI, tests and rollback scope. Preserve existing behavior and release contracts.
- For security or production-sensitive work (R2/R3), stop at an evidence-backed proposal and obtain separate explicit authorization.
- Report changed files, test commands + exit codes, regressions, risks, rollback and outstanding approvals. See the generated Acceptance template in the ai-sdlc document directory.

This document is guidance, not a production permission boundary; enforce critical constraints at CI / deployment credentials / server-side policy.
