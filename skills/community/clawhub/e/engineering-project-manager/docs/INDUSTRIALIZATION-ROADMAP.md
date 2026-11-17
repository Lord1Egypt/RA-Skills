# Capability and industrialization roadmap

Status date: 2026-09-16. This is a product capability inventory, not a SPICE
assessment. A document template is not an implemented process or an assessment
result. See [SPICE scope](SPICE-SCOPE.md).

## Implemented foundations

| Capability | Working support | Practical limit / next work |
|---|---|---|
| Initialization | Missing-information questionnaire, validated setup file, review digest, portable bootstrap, GitHub/GitLab configuration and resumable steps | Real remote provisioning depends on host permissions and credentials; review before execution |
| Project tailoring | SYS, SWE, HWE, MLE, CYBER and MECH archetypes and domain documents | Organization-specific applicability and process choices remain a human decision |
| Tasks | Locked/atomic JSON state, dependencies, readiness, WIP, blockers, review, evidence and history | Assignee labels are not authenticated identities; acceptance remains with the coordinator |
| Delegation | Explicit workers, scope, concurrency, retries, approval policy and read-only assignment contracts | The agent discovers and invokes available delegation tools; the planner does not dispatch or enforce an OS sandbox |
| Requirements | Stable identities, exact revisions, one downstream allocation, verification strategy, legacy French compatibility | Quality of engineering content requires review; malformed blocks and duplicated metadata fail checks |
| Traceability | Exact revision links, stale links, self-links and cycles checked | Documentary links alone do not demonstrate implementation or successful verification |
| Changes | CR lifecycle, owners/history, impact analysis, manual impacts and controlled revision creation | No independent authorization service or atomic multi-file transaction journal |
| Baselines | DRAFT/FROZEN/RELEASED/SUPERSEDED, immutable snapshots, hashes and release gates | External Git/hosting governance and recovery from interrupted multi-file operations remain operational responsibilities |
| Verification evidence | Unified test/verification registry, exact revision coverage, results, artifact hashes and supersession | Evidence existence and integrity are checked; truth of externally reported results is not independently established |
| Risks | Versioned registry, scoring, owners, mitigation, explicit acceptance/review dates, closure and release blockers | Real-world risk discovery and authorized acceptance remain accountable decisions |
| Problems | Versioned lifecycle, dispositions, evidence, verified closure, duplicates and release blocking | Reported observations and sufficiency of corrective work require review |
| Milestones | Owners/dates, criteria, dependencies, task links, hashed proofs, reviewed completion and waivers | Setup targets must be deliberately converted to actionable records |
| External intake | Provenance, versioned/hash-protected artifacts, rights/confidentiality labels, reviewed inventory and supersession | No document download, automatic extraction, rights grant or access control |
| Obligation coverage | Applicability, exact source/revision/proof links, inventory completeness and compatible PASS coverage | Coverage is not conformity; source interpretation and exclusions need review |
| Release | Requirements, domains, tasks, configuration, evidence and management checks plus a real integration fixture | Formal sign-off and release artifact manifest remain document workflows |
| Migration | Read-only compatibility assessment with proposed next actions | No automatic rewrite of legacy requirements or live project history |
| Reporting | Read-only consolidated task, requirement, change, baseline, evidence and management status; explicit release gate option | No invented aggregate health score; missing/invalid inputs are surfaced |
| Generated projects | Audits, task engine, migration, reporting and delegation tooling copied into each project | Resume preserves existing tools; updating a generated project's tooling requires an explicit reviewed upgrade |
| Public distribution | Tracked subtree export, privacy checks, external denylist, optional history audit, deterministic ZIP and SHA-256 manifest | Human contextual review and a rights-holder-selected license remain necessary; private development history must not be mirrored |
| CI and testing | One full Linux check command, behavioral suites, portable GitHub/GitLab workflows | Mocked recovery tests are not a live test of every hosting service, runner or archetype |

Version 1.1.3 introduced the unified verification/test evidence model. Version
1.2.0 strengthened its integrity checks. Version 1.3.0 adds the five approved,
separate management registries, linked to existing records without changing
their schemas or creating a competing verification evidence registry.

## Document workflows and decision-gated extensions

The following capabilities are deliberately not advertised as complete automation.
Existing documents remain usable while further designs are reviewed. The approved
problem, risk, milestone, intake and compliance data models are implemented above.
Further authoritative models require an explicit architecture decision.

| Area | Current support | Proposed next step | Priority |
|---|---|---|---|
| Gates G0–G3 | Defined documentary gates; G3 checked by release command | Decide gate record and sign-off semantics before adding workflow state | P2 |
| Decisions and document approvals | Templates and Git review history | Agree identity, authorization and ID policies before automating approvals | P2 |
| MLE lineage / domain depth | Data/model cards and six domain-specific templates/audits | Representative real fixtures, dataset/model/configuration lineage and richer integration evidence | P2 |
| Metrics | Inventory counts and documented status | Agree meaningful definitions and denominators before introducing KPIs | P2 |
| Recovery | Git snapshots, atomic individual registry writes, tested rejection/recovery and documented repair | Evaluate a transaction journal if multi-registry atomic operations become a requirement | P2 |

P1 means core product work; P2 means further industrialization. Known integrity
defects take precedence over both. Do not silently change established requirement
IDs, process mappings, CR states, baseline semantics or evidence structure while
implementing these extensions.

## Validation and release discipline

From the full source repository, run `python3 -B tools/run_checks.py` on Linux. The command discovers shipped
behavioral test suites, validates Python syntax without writing bytecode, checks
package structure and runs the self-check. Publication checks and contextual
review apply to the exact final snapshot separately. Maintain release notes with
the tested version and remaining limits; do not infer maturity from test counts.
