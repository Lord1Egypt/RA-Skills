# Verification Evidence Management

Authoritative model for verification and test evidence introduced in
Project Manager 1.1.3. It implements the approved unified minimal registry
architecture: one machine-readable registry is the authority, and all
Markdown views are generated from it.

## Purpose

Before 1.1.3, verification proof was scattered across Markdown reports,
free-form task fields and links. Audits could not mechanically answer:

- which exact requirement revision was verified;
- with which prescribed verification strategy;
- by which test case and execution;
- with which result, on which configuration and Git commit;
- and which artifacts prove it.

Verification Evidence Management closes that gap without turning the skill
into a full test-management suite.

## Canonical locations

Evidence lives under `05-verification/`:

| Path | Role |
|---|---|
| `EVIDENCE-MANAGEMENT.json` | Enablement marker (explicit activation) |
| `EVIDENCE.json` | Authoritative registry (JSON) |
| `EVIDENCE.md` | Generated index view |
| `evidence/EV-<nnn>.md` | Generated per-record views |
| `.evidence.lock` | Runtime lock (Git-ignored) |

New bootstrapped projects are initialized automatically. Existing projects
opt in explicitly and non-destructively:

```bash
python3 scripts/verification_evidence.py --project PROJECT init --actor "Verification Engineer"
python3 scripts/verification_evidence.py --project PROJECT assess
```

`assess` only reports existing task evidence references and verification
reports; it never creates or modifies records. Legacy projects without the
marker are skipped by the audit (warning in normal mode, silent in strict
mode) and never fail the release gate.

## Evidence record model

Identifiers: `EV-001`, `EV-002`, ... Numbers are never reused, enforced by
registry validation against `next_number`.

Each record contains:

- `Evidence_ID` — permanent identity.
- `Requirement_ID` — exact requirement revision, for example
  `M5_SYS2_REQ_001@R3`. Evidence never attaches to a base ID alone.
- `Verification_Method`, `Verification_Scope`, `Verification_Activity`,
  `Verification_Process` — the strategy under which the evidence runs. By
  default it is inferred from the requirement and any override must stay
  consistent with the prescribed requirement strategy.
- `Configuration_Baseline` — optional `BL-<nnn>` reference; the referenced
  baseline record must exist.
- `Test_Case` — `Test_Case_ID`, `Title`, `Objective`, optional
  `Environment`, optional `Procedure` steps, `Expected_Result`.
- `Execution` — empty until a result is recorded, then `Execution_ID`,
  `Executed_At`, `Executed_By`, `Environment`, `Git_Commit`, `Result`,
  `Result_Summary`. The Git commit must exist in the project repository.
- `Artifacts` — project-relative paths with type and SHA-256. Traversal and
  absolute paths are rejected; content tampering is detected at validation.
- `Status` — see lifecycle below.
- `Created_At`, `Created_By`, `Superseded_By`.
- `History` — ordered audit events; the first event must be `CREATED`.

## Lifecycle

```text
PLANNED → IN_PROGRESS → PASS | FAIL | BLOCKED | SKIPPED
```

- `start` requires `PLANNED` and produces `IN_PROGRESS`.
- `record-result` is allowed from `PLANNED`, `IN_PROGRESS`, `FAIL`,
  `BLOCKED` or `SKIPPED` (re-execution) and sets the status to the result.
- A terminal record keeps its `Execution` forever, including after
  supersession.
- `supersede` is only allowed on `PASS` records, and the replacement must
  itself be a `PASS` record. The old record becomes `SUPERSEDED` with a
  `Superseded_By` link; history is preserved.

## Coverage rule

An active requirement revision is covered when at least one evidence record:

1. references that exact revision;
2. has status `PASS` (not superseded);
3. matches the requirement's prescribed verification strategy.

Cancelled requirements and superseded revisions never require coverage.
Evidence recorded against revision `R1` does **not** cover `R2`: a new
revision needs its own evidence, as agreed in the requirement model.

## CLI

```bash
python3 scripts/verification_evidence.py --project PROJECT init --actor ACTOR
python3 scripts/verification_evidence.py --project PROJECT create \
  --requirement-id M5_SYS2_REQ_001@R3 --title TITLE --objective OBJ \
  --expected-result RESULT --actor ACTOR [--procedure STEP ...] \
  [--artifact PATH --artifact-type REPORT]
python3 scripts/verification_evidence.py --project PROJECT start EV-001 --actor ACTOR
python3 scripts/verification_evidence.py --project PROJECT record-result EV-001 \
  --result PASS --actor ACTOR --summary SUMMARY [--baseline BL-001] [--artifact PATH ...]
python3 scripts/verification_evidence.py --project PROJECT supersede EV-001 --by EV-002 --actor ACTOR
python3 scripts/verification_evidence.py --project PROJECT list|show EV-001|validate|coverage [--strict]|assess|render
```

Writes are atomic, serialized by an exclusive lock, and validated before
persistence; an invalid mutation is rejected without touching the registry.

## Audit and release gate

`verification_evidence_audit.py PROJECT [--strict]` checks the marker,
validates the registry, and fails for every active requirement revision
without compatible `PASS` evidence. The release gate
(`release_check.py`) invokes it after `configuration_audit.py`; any failure
blocks the release.

Evidence records are verification metadata produced **against** a frozen
release candidate, not part of its immutable requirement snapshot. The
release-candidate delta therefore tolerates committed changes limited to
`EVIDENCE-MANAGEMENT.json`, `EVIDENCE.json`, `EVIDENCE.md` and
`evidence/EV-*.md` between the candidate commit and the release check,
exactly like baseline lifecycle metadata. Requirement content still cannot
change after freezing.

## Validation guarantees

Registry validation rejects: malformed or duplicate IDs; `next_number`
reuse; unknown, cancelled or strategy-mismatched requirements; missing test
case fields; results without a complete execution; Status/Result
disagreement; nonexistent execution commits; unknown baselines; unsafe or
tampered artifacts; broken history ordering; and supersession without an
existing PASS replacement.

## Tests

`verification_evidence_tests.py` proves the positive lifecycle, negative
inputs, tamper detection, revision and cancellation rules, legacy skip
behavior, and release-gate propagation. `release_fixture_test.py` proves a
complete project passing the real gate with evidence recorded after the
baseline freeze.
