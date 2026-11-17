# Milestone management

Milestones record dated acceptance decisions across project tasks. Their stable
identifiers (`MS-0001`, `MS-0002`, …) belong to an independent registry. Task IDs,
task states and requirement syntax are unchanged.

The authoritative file is `00-project/management/MILESTONES.json`. Its generated
`MILESTONES.md` view is rebuildable and must not be edited as authoritative data.
Mutations use the common exclusive lock, atomic JSON replacement and replayable
hash-chained history. A rejected operation leaves the registry and existing view
unchanged. History hashes and evidence hashes detect inconsistency; they are not
signatures, identity verification or certification.

## Define a milestone

Specify a title, accountable owner, calendar due date (`YYYY-MM-DD`), at least one
acceptance criterion, existing task links, and any milestone dependencies. Mark
the milestone `release_required` when release must depend on its acceptance. An
optional milestone never independently blocks release merely because it is open.

```sh
python scripts/milestone_manager.py --project /path/to/project init --actor "Project Manager"
python scripts/milestone_manager.py --project /path/to/project create --actor "Project Manager" --title "Verification complete" --owner "Verification Owner" --due-date 2027-06-30 --criterion "Required verification has passed" --criterion "Evidence has been reviewed" --task TASK-001 --release-required
python scripts/milestone_manager.py --project /path/to/project create --actor "Project Manager" --title "Release approval" --owner "Release Owner" --due-date 2027-07-01 --criterion "Release evidence is accepted" --depends-on MS-0001 --release-required
```

The manager validates task and milestone references and rejects duplicate links,
self-dependencies and dependency cycles. Dependencies identify milestones that
must actually reach `ACHIEVED`; cancelling or waiving a dependency does not satisfy
that relationship.

`update` accepts the same descriptive fields. Repeated `--criterion`, `--task` or
`--depends-on` options replace that entire list. Use `--clear-tasks` or
`--clear-dependencies` explicitly to remove a list; an omitted flag leaves it
unchanged. Criteria cannot be empty. Only `PLANNED`, `ACTIVE` and `BLOCKED`
milestones can be edited. Once a milestone is marked release-required, `update`
cannot remove that obligation; an explicit reviewed cancellation waiver is needed.

## Progress and acceptance

Allowed state transitions are:

| Current state | Next states |
|---|---|
| PLANNED | ACTIVE, BLOCKED, CANCELLED |
| ACTIVE | BLOCKED, ACHIEVED, CANCELLED |
| BLOCKED | ACTIVE, ACHIEVED, CANCELLED |
| ACHIEVED | None |
| CANCELLED | No state change; an absent release waiver may be added once |

Blocking requires a reason. Activating a blocked milestone clears its current
blocker while preserving the prior blocked record in history.

```sh
python scripts/milestone_manager.py --project /path/to/project transition MS-0001 ACTIVE --actor "Project Manager"
python scripts/milestone_manager.py --project /path/to/project transition MS-0001 BLOCKED --actor "Project Manager" --reason "Verification environment unavailable"
python scripts/milestone_manager.py --project /path/to/project transition MS-0001 ACTIVE --actor "Project Manager"
```

To achieve a milestone, every linked task must be `DONE`, every dependent milestone
must be `ACHIEVED`, and **every acceptance criterion** needs at least one existing
local proof artifact. The transition requires a review note and a reviewer label
different from its actor label. Actor and reviewer labels record declared
responsibility; they do not authenticate either person or establish an independent
review by themselves. Apply the project's actual approval and identity controls.

`--criterion-evidence INDEX=relative/path` uses the one-based order of the current
acceptance criteria. Repeat it to supply multiple artifacts for a criterion. The
same reviewed report can support multiple criteria when that report actually
addresses them. Each criterion is recorded alongside its artifact paths and
SHA-256 hashes. A hash proves which bytes were recorded, not that the evidence
proves the criterion; the designated reviewer must assess its substance.

```sh
python scripts/milestone_manager.py --project /path/to/project transition MS-0001 ACHIEVED --actor "Project Manager" --reviewer "Independent Reviewer" --review-note "Verification results and evidence reviewed against both acceptance criteria" --criterion-evidence 1=05-verification/verification-report.md --criterion-evidence 2=07-quality/review-record.md
```

The command neither changes tasks nor rewrites engineering artifacts. Proof must
already exist inside the project; absolute paths, traversal and references outside
the project are rejected. The milestone registry, view and lock cannot serve as
their own acceptance proof. There is no network download. After achievement, editing
or deleting proof, deleting a task, reopening a linked task, or invalidating a
dependency makes subsequent audits fail. Restore the approved evidence or manage
the changed scope through the project's change process; do not rewrite milestone
history to conceal it.

## Cancellation and release waivers

Every cancellation needs an explicit rationale. Cancelling a release-required
milestone **continues to block release** until an explicit waiver has a rationale,
recorded actor, distinct reviewer and review timestamp. Waiver acceptance belongs
to the project's authorized decision maker; supplying a label is not authorization.

```sh
python scripts/milestone_manager.py --project /path/to/project transition MS-0001 CANCELLED --actor "Project Manager" --reason "Scope removed through an approved change"
python scripts/milestone_manager.py --project /path/to/project transition MS-0001 CANCELLED --actor "Project Manager" --waiver-reviewer "Project Sponsor" --waiver-rationale "Sponsor accepted the documented scope removal and its release consequences"
```

The waiver can also be supplied during the original cancellation. When adding it
later, omit `--reason`: the prior cancellation rationale remains immutable. A
waived milestone stays `CANCELLED`, never `ACHIEVED`, and release audits retain an
explicit warning about the waiver. Optional milestones do not require a release
waiver and cannot carry one.

## Read, audit and rebuild

```sh
python scripts/milestone_manager.py --project /path/to/project list
python scripts/milestone_manager.py --project /path/to/project audit
python scripts/milestone_manager.py --project /path/to/project audit --release
python scripts/milestone_manager.py --project /path/to/project render
```

Normal audit checks the registry schema, common history, milestone history actions,
references, dependency graph and sealed proof. Release audit additionally blocks
unmet release-required milestones without a valid explicit waiver. A past due date
on an unfinished milestone produces a warning based on the local system date.
Audits and `list` do not write files. `render` rebuilds only the Markdown view.
Exit codes are `0` for success, `1` for audit findings and `2` for invalid commands
or rejected mutations. Legacy projects without a milestone registry are skipped
by this module; the integrated project audit separately detects deletion of a
previously enabled registry.

## Python integration

`initialize(project, actor)`, `create(project, *, actor, title, owner, due_date,
acceptance_criteria, tasks=None, depends_on=None, release_required=False)`,
`update(project, identifier, *, actor, ...)`, and
`transition(project, identifier, status, *, actor, ...)` return the complete
registry after a successful operation. The new record's ID is in the last record
returned by `create`. `transition` takes `criterion_evidence` as a dictionary from
integer criterion index to a list of relative artifact paths, plus `reviewer` and
`review_note` for achievement, or `waiver_rationale` and `waiver_reviewer` for waivers.

`audit(project, release=False)` returns `(errors, warnings)`.
`validate_registry(project, data)` includes both `Store.errors(data)` and milestone
semantics. `render(project, data)` writes the derived view. Integration must use
these APIs rather than editing the JSON directly. Run
`python -B scripts/milestone_tests.py` for the behavioral regression suite.
