# Change and Baseline Management

Version: 1.1

## Enablement and Compatibility

Configuration Management V1.1 is enabled when
`08-configuration/CONFIGURATION-MANAGEMENT.json` exists, contains
`"enabled": true`, and declares model version `1.1`.

New projects receive the model automatically. Existing projects enable it
explicitly with both initialization commands:

```text
python3 tools/project-audit/change_manager.py --project . init
python3 tools/project-audit/baseline_manager.py --project . init --actor <actor>
```

Legacy projects without the marker remain valid. Configuration audit reports
that the subsystem was skipped and does not invent missing controlled data.

## Change Request Model

The authoritative registry is `08-configuration/CHANGE-REQUESTS.json`.
`CHANGE-REQUESTS.md` and `changes/CR-NNN.md` are generated views.
Registry revision checking, an advisory lock, temporary-file writes, `fsync`,
and atomic replacement protect updates from partial or silent overwrite.

Identifiers are allocated monotonically as `CR-001`, `CR-002`, and so on.
The next number is stored separately and is never derived from the current
list, so removed records cannot cause identifier reuse.

The workflow is:

```text
DRAFT -> SUBMITTED -> UNDER_ANALYSIS -> ANALYZED
ANALYZED + IMPLEMENT -> IMPLEMENTING
ANALYZED + REJECT -> REJECTED
ANALYZED + DEFER -> DEFERRED
ANALYZED + MORE_INFORMATION_REQUIRED -> UNDER_ANALYSIS
IMPLEMENTING -> IMPLEMENTED -> VERIFIED -> CLOSED
DEFERRED -> UNDER_ANALYSIS
```

REJECTED, CANCELLED, and CLOSED are terminal. `Analysis_Result` is independent
from workflow status. Every transition records timestamp, actor, previous and
new status, assignee, role, analysis result, and an optional comment.
Assignee and role are free-form non-empty strings and may change at each stage.

`Changed_Items` identifies configuration items explicitly intended to change.
`Impacted_Items` separately identifies direct, transitive, and manually added
consequences. The `impact` command recomputes graph-derived impacts while
preserving explicit `--manual-impact` entries; `--clear-manual-impact` removes
those entries. A non-requirement Changed Item is never silently reclassified as
manual impact.

### Change Manager CLI

Run `change_manager.py --help` for exact arguments. Commands are:

- `init`, `create`, `list`, `show`, and `render`;
- `assign`, `transition`, and `start-analysis`;
- `set-result` and `impact`;
- `revise-requirement`;
- `validate`.

Impact analysis traverses the active revision-aware `Upstream` graph
recursively. It reports direct and transitive downstream requirements without
rewriting them. References to older revisions remain stale until engineering
disposition updates them explicitly.

`revise-requirement` accepts the latest exact requirement revision. It appends
the next revision to the same specification, preserves the historical block,
sets the new revision to DRAFT, and assigns the Change Request identifier.
Verification evidence and downstream references are never migrated
automatically.

## Baseline Model

The baseline registry is `08-configuration/BASELINE-REGISTRY.json`. Exact
records are stored under `08-configuration/baselines/BL-NNN.json`, with
generated Markdown views and an index in `BASELINES.md`.

Identifiers are monotonically allocated as `BL-001`, `BL-002`, and so on.
The lifecycle is:

```text
DRAFT -> FROZEN -> RELEASED -> SUPERSEDED
DRAFT -> CANCELLED
```

A DRAFT captures Git HEAD, the latest active non-CANCELLED requirement
revision for every stable identity, configuration items, related Change
Requests, deviations, and accepted problems. A DRAFT may be refreshed.

Freezing requires a clean Git worktree, an existing commit, current rather
than stale requirement revisions, RELEASED included requirements, and no
blocking Change Request affecting baseline content. The freeze operation
refreshes the immutable candidate from that exact clean commit and selects the
new FROZEN record as `Current Baseline` in `STATUS.md`. Commit the generated
baseline metadata before running the release gate. Deferred changes are always
reported and require an accepted deviation to proceed.

The candidate `Git_Commit` identifies the engineering-content commit before
its generated freeze metadata. Release validation permits only the controlled
baseline registry, baseline record/view, and `STATUS.md` to differ between that
candidate commit and the validated HEAD. Any other changed path invalidates the
candidate. Historical FROZEN, RELEASED, or SUPERSEDED snapshots remain valid
when later requirement revisions become active; exact historical revisions
must remain present and the immutable hash must still match.

The SHA-256 covers only the immutable payload: identity, purpose, creation
metadata, Git commit, requirements snapshot, configuration items, related
changes, deviations, and accepted problems. Lifecycle status and history are
excluded so legitimate FROZEN-to-RELEASED and RELEASED-to-SUPERSEDED
transitions do not invalidate the snapshot.

### Baseline Manager CLI

Run `baseline_manager.py --help` for exact arguments. Commands are:

- `init`, `create`, `list`, `show`, and `render`;
- `refresh` and `validate`;
- `freeze`, `release`, `supersede`, and `cancel`.

## Configuration Audit and Release Gate

`configuration_audit.py` is the source of truth for cross-record rules. It
checks Change Request identifiers, fields, transitions, history, analysis
result consistency, impact results, requirement references, R2+ Change
Request linkage, baseline identifiers, lifecycle history, Git commits,
requirement currency, frozen integrity, blocking changes, supersession, and
`STATUS.md` Current Baseline consistency.

The strict release gate invokes configuration audit after the existing
project, requirement, traceability, and domain audits. A selected FROZEN
baseline is mandatory when Configuration Management V1.1 is enabled; it need
not already be RELEASED. The gate validates its exact candidate commit and
rejects engineering-content drift. `baseline_manager.py release` invokes this
full gate and performs the controlled FROZEN-to-RELEASED transition only after
the gate succeeds.
