---
name: project-manager
description: "Manage substantial engineering and software projects end to end: discover or bootstrap the canonical project, define scope and work breakdown, coordinate agents, maintain requirements and traceability, control changes and baselines, audit quality, and enforce release readiness. Use for project planning, status, execution, recovery, change control, or release-gate requests."
user-invocable: true
license: MIT-0
compatibility: "Linux, Python 3.10+ and Git. GitHub/GitLab bootstrap additionally needs authenticated gh/glab; SSH remotes need SSH access."
metadata: {"openclaw":{"requires":{"bins":["python3","git"]},"os":["linux"],"homepage":"https://github.com/aminekhettat/engineering-project-manager"}}
---

# Project Manager

Independent SPICE-like workflow assistance; **not SPICE or Automotive SPICE
certified**, endorsed or approved. Checks do not establish formal conformity or
a capability level. Read `docs/SPICE-SCOPE.md` when explaining the process basis.

Manage one canonical project space per real project. Reuse an existing matching
project before creating anything. Main remains accountable for scope, decisions,
coordination, evidence, and communication with the user.

Resolve the installed skill directory from this file before running commands.
Commands below run from that directory; replace `PROJECT` with the absolute
canonical project path. Do not assume the skill is inside the project.

## 1. Discover or establish the project

1. Search the project index and repositories for an existing matching project.
2. Read `00-project/PROJECT.md`, `PROCESS-SCOPE.md`, `STATUS.md`, task state,
   risks, decisions, requirements, and configuration records when present.
3. If no project exists, follow `references/project-initialization.md`. Ask the
   missing questions in manageable groups: objective, scope, disciplines,
   owners, constraints, repository, infrastructure, CI, delegation and delivery.
   Reuse already-known answers. Never request secret values.
4. Confirm the archetype's default disciplines and any additions among SYS,
   SWE, HWE, MLE, MECH and CYBER. Do not silently remove mapped domains.
5. Prepare and review the resolved setup, then use the canonical bootstrap:

```bash
python3 scripts/bootstrap_project.py --help
python3 scripts/project_setup.py --help
```

Do not declare bootstrap complete until its canonical Git remote is reachable,
the expected branch is synchronized, and `BOOTSTRAP-STATUS.json` says COMPLETE.

**Done when:** one canonical project root and repository are identified, or the
missing decision/access is explicitly blocked.

For an existing project, use read-only `scripts/migration_assess.py` and
`scripts/project_report.py`. Keep Git canonical for engineering state; Drive
is optional complementary document storage. Do not reinitialize existing records.

## 2. Plan executable work

Build the hierarchy objective → outcomes → workstreams → phases → milestones →
tasks. Give substantial tasks a stable identifier, owner, priority, dependencies,
acceptance criteria, expected deliverable, and blocker state. Use
`BACKLOG`, `READY`, `IN_PROGRESS`, `BLOCKED`, `REVIEW`, `REWORK`, `DONE`, or `CANCELLED`.
`DONE` always means acceptance evidence has been checked.

Use the task-state engine for deterministic transitions:

```bash
python3 scripts/project_state.py --help
```

Keep work in progress small. Never start work whose dependencies, acceptance
criteria, access, or mandatory safety decision are unresolved.

**Done when:** the next executable tasks are READY and ownership is unambiguous.

## 3. Execute and coordinate

For each cycle:

1. refresh project state;
2. select the highest-priority READY work without conflicts;
3. move it to IN_PROGRESS;
4. delegate to the appropriate specialist when useful;
5. collect the concrete result and evidence;
6. move it to REVIEW;
7. apply the relevant Definition of Done and engineering gates;
8. accept to DONE only on verified evidence, otherwise REWORK or BLOCKED;
9. update status, traceability, risks, decisions, and configuration records.

Use `references/execution-engine.md` for transitions and
`references/agent-delegation.md` for capability discovery, bounded contracts,
isolated work, monitoring, retries and reviewed integration. Prepare a contract
with `scripts/delegation_plan.py`; it does not dispatch or grant access. Configured
agent/worker labels must be verified against the runtime. Main accepts work as
DONE only after review; reviewer names in records are labels, not access controls.

**Done when:** state, evidence, and user-facing status agree.

## 4. Maintain engineering control

For requirement syntax and revision-aware traceability, read
`docs/REQUIREMENT-DATA-MODEL.md`. For domain-specific work products, read only
the relevant reference:

- SYS: `references/system-engineering.md`
- SWE: `references/software-engineering.md`
- HWE: `references/hardware-engineering.md`
- MLE: `references/machine-learning-engineering.md`
- MECH: `references/mechanical-engineering.md`
- CYBER: `references/cybersecurity-engineering.md`

Templates under `templates/` are canonical source assets used by bootstrap.
Do not edit generated project copies when the intent is to change the skill.

Run project checks during development:

```bash
python3 scripts/project_audit.py PROJECT
python3 scripts/requirements_lint.py PROJECT
python3 scripts/traceability_check.py PROJECT
python3 scripts/domain_audit.py PROJECT
```

**Done when:** required work products exist and traceability is internally
consistent for the current lifecycle state.

## 5. Control changes and baselines

Read `docs/CHANGE-BASELINE-MANAGEMENT.md` and
`references/document-configuration-management.md` before changing released
requirements or configuration items.

Use the deterministic CLIs rather than editing registries manually:

```bash
python3 scripts/change_manager.py --help
python3 scripts/baseline_manager.py --help
python3 scripts/configuration_audit.py PROJECT --strict
```

Released requirement revisions and frozen baseline snapshots are immutable.
Use a Change Request and a new requirement revision; change baseline lifecycle
metadata only through its CLI, preserving history and supersession links.

**Done when:** the authoritative registries validate and affected baselines are
consistent.

## 6. Record verification evidence

Read `docs/VERIFICATION-EVIDENCE.md` before planning or recording
verification proof. The authoritative registry is machine-readable; Markdown
views are generated, never edited by hand:

```bash
python3 scripts/verification_evidence.py --help
python3 scripts/verification_evidence_audit.py PROJECT --strict
```

Evidence attaches to an exact requirement revision, follows the requirement's
prescribed verification strategy, and only a compatible PASS record covers
that revision at the release gate. Truly legacy projects without management
records or prior enablement are skipped; deleting an existing marker cannot
disable its audit. Opt in explicitly with `init` and review `assess` before
recording anything.

**Done when:** every active requirement revision has compatible PASS
evidence, or uncovered revisions are known release blockers.

## 7. Gate a release

Before release, manage risks, problems, milestones and external obligations using
`docs/MANAGEMENT-EXTENSIONS.md`. New projects initialize these registries; existing
projects opt in explicitly using `scripts/management_init.py`. Preserve legacy
documents and do not infer completed work from empty registries.

Read `docs/RISK-PROBLEM-MANAGEMENT.md` for risk acceptance and verified problem
closure; `docs/MILESTONE-MANAGEMENT.md` for task/criterion evidence and milestone
waivers; `docs/INTAKE-COMPLIANCE.md` for reviewed source versions and obligation
coverage. Use the CLIs, never edit JSON or generated Markdown by hand. Risk
acceptance and exclusions require an accountable decision already authorized by
the user; an agent must not invent acceptance to make the gate green.

```bash
python3 scripts/management_audit.py PROJECT
python3 scripts/management_audit.py PROJECT --release
```

Resolve release-blocking problems, high unaccepted risks, required milestones
and uncovered external obligations before freezing the candidate. New management
records are controlled content: changes after a freeze need a new candidate.
Record IDs remain stable; history and sealed evidence must remain auditable.

A release candidate must pass the complete gate:

```bash
python3 scripts/release_check.py PROJECT
```

Do not represent bootstrap success as release readiness. A release requires
valid governance, requirements, traceability, domain evidence, configuration
control, verification evidence coverage, a clean Git state, commit
consistency, and G3 readiness.

**Done when:** the release gate exits 0 for the exact candidate commit, or the
blocking findings are recorded.

## 8. Deeper guidance and maintenance

The detailed governance rules and Definitions of Done remain in
`references/project-manager-handbook.md`; consult only the sections needed for
the current project. Remaining capability gaps are tracked in
`docs/INDUSTRIALIZATION-ROADMAP.md`.

For changes to the skill itself, use the source repository's
[contribution guide](https://github.com/aminekhettat/engineering-project-manager/blob/main/CONTRIBUTING.md).
Contributor tests and publication tools live in that repository, outside the
installed runtime. Never publish a project workspace or private Git history.
