# Risk and problem management

These optional management registries distinguish uncertain future exposure
(risks) from observed defects or other problems. They extend the skill's local
engineering controls; their states and scoring are project conventions, not
official SPICE assessment criteria or a certification claim.

## Authoritative records and integration

| Engine | Registry | Generated view | ID |
|---|---|---|---|
| `risk_manager.py` | `09-risks/RISKS.json` | `09-risks/RISKS.md` | `RISK-0001` |
| `problem_manager.py` | `07-quality/PROBLEMS.json` | `07-quality/PROBLEMS.md` | `PRB-0001` |

Each version 1 registry contains `records`, a monotonic `next_id`, and a
replayable history of actor, action, before-state hash and after-state snapshot.
IDs are never reused or deleted through the CLI. Updates are locked and written
atomically. Rejected validation or lifecycle operations leave the authoritative
JSON unchanged. Do not hand-edit records or history.

The Markdown view is rebuildable and is written after the JSON commit. If view
writing fails, the mutation reports that the registry was committed and the view
needs rebuilding. Concurrent writers preserve JSON integrity; a Markdown view
may lag behind the latest record. Run `render` after concurrent work if needed.
The history detects inconsistent edits; a person who can rewrite the whole
registry and its history can recompute hashes. Reviewed Git history, protected
access and backups remain the external trust boundary. Actor and owner strings
are labels, not authentication or proof of reviewer independence.

Legacy projects with neither registry are skipped by these managers. Opt in
explicitly; `init` preserves an existing valid registry. Existing risk documents
and old task, requirement, change, baseline and evidence schemas are unchanged.
The combined project audit is responsible for detecting deletion of a previously
enabled registry.

All paths below are relative to the project. Run from the installed skill
directory, or use the copied script location in a generated project:

```sh
python3 scripts/risk_manager.py --project PROJECT init --actor coordinator
python3 scripts/problem_manager.py --project PROJECT init --actor coordinator
```

Both engines support `create`, `update`, `transition`, `audit`, `list` and
`render`; risk management also supports `review`. Every mutation requires an
actor. Updates and transitions require a rationale. `list` returns JSON.
Exit codes are 0 for success, 1 for audit errors, and 2 for rejected commands.

## Risk model

Every risk has title, owner, description, probability and impact. Probability
and impact are integers from 1 to 5. Initial exposure is their product; this
skill treats scores of 15 or greater as high. Define the qualitative meaning
of each rating for the project before comparing different risks. The score is
an ordinal prioritization aid, not a quantitative probability or financial loss.

Optional links identify existing tasks, exact requirement revisions and Change
Requests. A mitigation plan and review due date can be recorded. A lower residual
score applies only when supported by sealed mitigation evidence. Merely accepting
a risk does not lower its score.

| Transition | Required decision or proof |
|---|---|
| Create → `OPEN` | Description, owner and initial ratings |
| `OPEN` → `MITIGATING` | Nonempty mitigation plan and rationale |
| `MITIGATING` → `MITIGATED` | Residual probability/impact and one or more sealed evidence artifacts |
| `OPEN`, `MITIGATING`, `MITIGATED` → `ACCEPTED` | Explicit accepting actor, rationale and review date not in the past |
| `ACCEPTED` → `ACCEPTED` | Explicit renewal with actor, rationale and new review date |
| `MITIGATED`, `ACCEPTED` → `CLOSED` | Closure rationale and sealed evidence that the exposure is resolved or no longer applicable |
| Any later state → `OPEN` | Reopening rationale; prior assessments remain in history |

Reopening clears current residual results, acceptance and closure metadata; the
initial score becomes effective again. Content can be updated only in `OPEN`
or `MITIGATING`. Reopen assessed risks before changing their ratings, owner,
description, links or mitigation. This prevents old acceptance from silently
covering a changed risk.

```sh
python3 scripts/risk_manager.py --project PROJECT create --actor risk-owner \
  --title "Response budget exposure" --owner systems \
  --description "Interface load may exceed the response budget" \
  --probability 4 --impact 5 --mitigation "Measure load and tune scheduling" \
  --task TASK-001 --requirement DEMO_SWE1_REQ_001@R1 --change CR-001
python3 scripts/risk_manager.py --project PROJECT transition RISK-0001 \
  --actor systems --to MITIGATING --reason "Mitigation work is ready"
python3 scripts/risk_manager.py --project PROJECT transition RISK-0001 \
  --actor verifier --to MITIGATED --reason "Measured response meets the target" \
  --residual-probability 2 --residual-impact 3 \
  --evidence 05-verification/results/response-test.txt
```

Create the genuine evidence file and referenced engineering records before
running these examples. The engine hashes existing files; it does not invent
test outcomes or retrieve external evidence.

To accept residual exposure, replace `YYYY-MM-DD` with the agreed review deadline:

```sh
python3 scripts/risk_manager.py --project PROJECT transition RISK-0001 \
  --actor risk-acceptance-owner --to ACCEPTED \
  --reason "Residual exposure accepted within the documented operating limits" \
  --review-date YYYY-MM-DD
python3 scripts/risk_manager.py --project PROJECT review RISK-0001 \
  --actor risk-owner --reason "Assumptions and mitigation remain applicable" \
  --next-review-date YYYY-MM-DD
```

The `review` command records a review and its next due date. It **does not renew
acceptance**. Acceptance is current through its recorded UTC calendar date.
Expired high-risk acceptance blocks release until explicitly renewed, mitigated
with evidence, or closed with proof. Overdue ordinary reviews are warnings.

## Problem model

Each problem has title, owner, description, severity (`LOW`, `MEDIUM`, `HIGH`,
`CRITICAL`) and an explicit `release_blocking` boolean, which defaults to true.
Severity records impact; the release-blocking decision is a separate project
decision. Changing that decision requires an actor and rationale and remains
visible in history.

The normal lifecycle is:

```text
NEW → TRIAGED → IN_PROGRESS → RESOLVED → VERIFIED → CLOSED
```

Triage records an actor and rationale. Resolution requires a disposition and
sealed evidence. A fixed problem must pass through `IN_PROGRESS`. A triaged
problem can proceed directly to `RESOLVED` only with a `DUPLICATE` or `REJECTED`
disposition, rationale and evidence such as a reviewed triage report.

| Disposition | Meaning and required context |
|---|---|
| `FIXED` | An implemented correction with supporting evidence |
| `DUPLICATE` | Another existing problem is authoritative; `--duplicate-of PRB-xxxx` is required |
| `REJECTED` | A documented decision that the reported item requires no correction |

Self-duplicates, missing targets and duplicate-reference cycles are rejected.
Duplicate or rejected dispositions do not bypass verification: every closure
requires `VERIFIED`, an explicit verification actor/rationale and sealed
verification evidence. The tool validates records and artifact integrity; the
reviewer must evaluate whether the evidence genuinely supports the disposition.

```sh
python3 scripts/problem_manager.py --project PROJECT create --actor reporter \
  --title "Response timeout observed" --owner software --severity HIGH \
  --description "The integration run exceeded the response limit" \
  --release-blocking true --task TASK-001
python3 scripts/problem_manager.py --project PROJECT transition PRB-0001 \
  --actor triage-owner --to TRIAGED --reason "Reproduced with the recorded input"
python3 scripts/problem_manager.py --project PROJECT transition PRB-0001 \
  --actor developer --to IN_PROGRESS --reason "Correction is assigned"
python3 scripts/problem_manager.py --project PROJECT transition PRB-0001 \
  --actor developer --to RESOLVED --disposition FIXED \
  --reason "Scheduling correction implemented" --evidence 05-verification/results/fix.txt
python3 scripts/problem_manager.py --project PROJECT transition PRB-0001 \
  --actor verifier --to VERIFIED --reason "Regression confirms acceptance criteria" \
  --evidence 05-verification/results/regression.txt
python3 scripts/problem_manager.py --project PROJECT transition PRB-0001 \
  --actor quality-owner --to CLOSED --reason "Verification reviewed and closure authorized"
```

`RESOLVED`, `VERIFIED` and `CLOSED` can reopen to `IN_PROGRESS` with a rationale.
The current resolution, verification and closure are cleared; previous evidence
and decisions remain in history. Updates are allowed only in `NEW`, `TRIAGED`
or `IN_PROGRESS`, so changing assessed content requires reopening first.

## Links, audits and recovery

Use repeatable `--task`, `--requirement` and `--change` arguments for links. An
update replaces a supplied link list; `--clear-tasks`, `--clear-requirements` or
`--clear-changes` explicitly removes that link class. Exact requirement revisions
are required. These managers do not modify requirements or propagate changes
automatically.

```sh
python3 scripts/risk_manager.py --project PROJECT audit --release
python3 scripts/problem_manager.py --project PROJECT audit --release
python3 scripts/risk_manager.py --project PROJECT list
python3 scripts/problem_manager.py --project PROJECT render
```

Normal audits validate schema, replayable history, links and evidence. Release
audits also block high unaccepted exposure and every release-blocking problem
that is not `CLOSED`, including `RESOLVED` or `VERIFIED` problems. A low residual
score without sealed mitigation proof cannot satisfy the risk gate.

Evidence is a project-relative regular file plus SHA-256. Missing files,
changed content, traversal and paths into Git metadata are rejected. Current
evidence remains checked after closure. Retain controlled evidence files rather
than overwriting them with later runs.

If evidence or registry integrity fails, ordinary mutations fail closed instead
of clearing the damaged record. Preserve the failing files, compare reviewed Git
history and backups, and repair through a controlled recovery decision. Never
erase history, reset IDs or delete an enabled registry to obtain a passing gate.
