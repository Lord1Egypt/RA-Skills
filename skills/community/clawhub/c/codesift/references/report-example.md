# Sample review report

This is a format example for a fictional project. Its paths, commands and outputs
are invented to show structure; never cite them as evidence or reuse them as
findings. Scale the sections to the request: a small change review needs only the
summary, the findings and the limits.

## Contents

- Report: scope, summary, findings, hypotheses, optional improvements, gates,
  falsification record, coverage ledger, validation and limits, remediation plan
- Machine-readable findings (optional)
- SARIF export notes

## Report

### Scope and snapshot

- Request: deep audit of the `orders` monorepo for contract, gate and unused-code defects.
- Revision: `a1b2c3d`, clean worktree. Excluded: `vendor/` and generated `api/gen/`.
- Units from collect_facts.sh, with tiers: `services/api` (Python, 142 files,
  Focused), `crates/ledger` (Rust, 18 files, Deep), `web` (TypeScript, 310 files,
  Surgical: checkout and refund flows only).
- Risk order: `crates/ledger` (money), `services/api` (authorization, persistence), `web`.
- Local rules: root AGENTS.md, plus `crates/ledger/AGENTS.md` (no panics across FFI).

### Summary

| ID | Title | Severity | Evidence |
|---|---|---|---|
| R1 | Refund amount scaled to minor units twice | Critical | reproduced |
| R2 | Required CI test job cannot fail | High | confirmed_static |
| R3 | `legacy_export` task module may be unused | Low | hypothesis |
| O1 | Client-side currency list can drift from the server list | n/a | optional improvement |

### Confirmed findings

**R1. Refund amount scaled to minor units twice**

- Severity: Critical. Every partial refund books 100 times the amount, and
  reconciliation runs only nightly.
- Evidence: reproduced.
- Chain: `services/api/refunds.py:88` `to_minor_units()` converts 12.34 to 1234 →
  JSON field `amount` → `crates/ledger/src/refund.rs:41` `Amount::from_major()`
  multiplies by 100 again.
- Expected: the ledger receives minor units unchanged (`docs/api.md`: "amount is in minor units").
- Actual: a 12.34 refund is booked as 123400 minor units.
- Reproduction in a disposable copy:
  `pytest tests/test_refund_contract.py::test_partial_refund -q` →
  `AssertionError: 123400 != 1234`.
- Ruled out: client-side conversion (the request body carries 12.34) and ledger
  configuration (no unit setting exists).
- Root cause: the boundary has no stated unit contract, so both sides convert.
- Correction: the ledger accepts minor units as integers at this call site, and a
  contract test pins the unit across the boundary.
- Verification: the contract test fails before the change and passes after it;
  `cargo test -p ledger refund`.

**R2. Required CI test job cannot fail**

- Severity: High. A failing `services/api` test still produces a green required check.
- Evidence: confirmed_static.
- Location: `.github/workflows/ci.yml:57`, where the test step ends in
  `pytest || true`, so the step and the job report success for any test result.
- Expected: a failing test fails the required check (CONTRIBUTING.md: "CI must pass").
- Remaining assumption: no other required check runs these tests. The workflow
  files show only `lint` and `test`; branch-protection settings were not visible.
- Correction: let the step propagate pytest's exit status. If flaky tests
  motivated the masking, quarantine them by marker instead.
- Verification: on a disposable branch, a seeded failing test turns the check red.

### Hypotheses

**R3. `legacy_export` task module may be unused**

- Severity if it holds: Low (maintenance cost only).
- Evidence: hypothesis. Graph and text search found no import or call.
- Open counterevidence: tasks are registered by name, and `deploy/beat.yaml`
  lists task names from a deployment repository that was not available.
- To resolve: check that scheduler configuration, or task-execution logs, for
  `legacy_export.run`. No deletion is proposed until then.

### Optional improvements

**O1.** `web/src/money.ts:12` and `services/api/money.py:30` hold separate ISO 4217
code lists. They agree today; the server check is the authority and the client
check only improves feedback. Generating the client list from the server list
would prevent drift. No change is required.

### Gates

| Gate | Classification | Evidence |
|---|---|---|
| `ci.yml` test job | ineffective | the test step ignores pytest's exit status (R2) |
| `ci.yml` lint job | effective | a seeded lint error fails it on a disposable branch |
| Second schema validation in `refunds.py:52` | redundant | same parsed body and schema as the middleware check, no mutation in between |
| `REFUND_V2` flag | obsolete | true in every environment file; the false branch no longer exists |
| `MAX_EXPORT_ROWS` cap | unresolved | no stated requirement; owner asked |

### Falsification record

Falsification ran in a separate subagent that saw only the evidence packets and
the cited code.

| Candidate | Lens | Outcome | Reason |
|---|---|---|---|
| C4: fast path skipped for batch refunds | contracts and data flow | dropped | `docs/batch.md` requires the slow path above 100 items to keep per-item audit logs |
| C7: unbounded retry in the ledger client | errors, validation and gates | downgraded to hypothesis, then merged into the limits | the cap comes from `LEDGER_RETRIES`, whose deployed value is not visible here |
| R1, R2 | as reported | kept | no counterevidence found |

### Coverage ledger

| Unit | Lens | Status | Note |
|---|---|---|---|
| crates/ledger | all six lenses | done | Deep tier |
| services/api | contracts, errors and gates, tests and oracles | done | |
| services/api | concurrency, resources and lifecycle | partial | retry settings live in the deployment repository |
| services/api | reachability | partial | task names resolved only within this repository |
| api to ledger | cross-boundary | done | produced R1 |
| web | contracts and data flow | partial | Surgical tier: checkout and refund flows only |
| web | remaining lenses | skipped | outside the agreed risk order; not reviewed |

Stop rule: a second full round over the ranked units found nothing new.

### Validation and limits

- Executed: the R1 reproduction (1 test, failed as expected); `cargo test -p ledger`
  (34 executed, 0 failed); run_correctness_test.sh for `services/api`
  (212 executed, 3 skipped, failure_kind absent, no workspace mutations).
- Not executed: `web` tests (outside the reviewed flows) and the R2 check, which
  needs a disposable branch.
- Dependency names were checked against a mirror; two are `mirror_not_found` and
  stay undetermined until checked upstream.
- Not reviewed: most of `web`, the deployment repository and runtime configuration.

### Remediation plan

| ID | Change | Files | Validation |
|---|---|---|---|
| R1 | Pass minor units unchanged; add a cross-boundary contract test | `crates/ledger/src/refund.rs`, `tests/test_refund_contract.py` | the contract test fails before and passes after; `cargo test -p ledger` |
| R2 | Make the test step propagate pytest's exit status | `.github/workflows/ci.yml` | a seeded failing test turns the check red on a disposable branch |

R3 and O1 need no change now. Reply with the IDs to approve, for example
"approve R1 R2"; nothing is edited before that.

## Machine-readable findings (optional)

Use JSON when several lenses, subagents or rounds must be merged, or when a
baseline of accepted risks is kept between reviews. The human report stays the
primary output; the JSON mirrors it.

```json
{
  "schema": "codesift-findings/1",
  "revision": "a1b2c3d",
  "findings": [
    {
      "id": "R1",
      "kind": "finding",
      "title": "Refund amount scaled to minor units twice",
      "severity": "critical",
      "evidence": "reproduced",
      "lens": "cross-boundary",
      "locations": [
        {"path": "services/api/refunds.py", "line": 88, "symbol": "to_minor_units"},
        {"path": "crates/ledger/src/refund.rs", "line": 41, "symbol": "Amount::from_major"}
      ],
      "root_cause": "No unit contract at the API/ledger boundary; both sides convert.",
      "fix": "The ledger accepts minor units unchanged at this call site.",
      "validation": "pytest tests/test_refund_contract.py::test_partial_refund",
      "fingerprint": "cross-boundary:crates/ledger/src/refund.rs:Amount::from_major:double-unit-conversion"
    }
  ]
}
```

Field rules:

- `kind` is `finding` or `improvement`. `evidence` is `reproduced`,
  `confirmed_static` or `hypothesis`. `severity` is `critical`, `high`, `medium`,
  `low`, or null for improvements.
- `fingerprint` is a readable, line-independent key: lens, primary path, symbol
  and a short root-cause slug. The same defect found by two passes then merges,
  and the key survives unrelated line shifts. Do not hash it or include line numbers.
- Merging: findings with the same fingerprint merge into one, keeping the union of
  locations and the strongest evidence actually recorded. Two passes agreeing
  never upgrades the evidence state.
- Baseline: store accepted risks by fingerprint with a reason and an owner, and
  report a baseline match as accepted rather than new.

## SARIF export notes

Export SARIF 2.1.0 only when a consumer needs it, such as GitHub code scanning.

- `ruleId` names the lens or dimension. Map `level` as error for critical and
  high, warning for medium, and note for low and for improvements.
- SARIF has no evidence-state field: put the evidence state and the stable ID in
  `properties`, for example `properties.evidence` and `properties.codesiftId`.
- Leave `partialFingerprints` empty. Microsoft's guidance for AI-generated SARIF
  advises against model-written fingerprints. GitHub uses them to track alerts
  across runs and tries to populate missing ones from the source files when the
  upload-sarif action uploads the file.
- Export hypotheses as `note` with `properties.evidence` set to `hypothesis`, or
  leave them out when the consumer would treat every result as a defect.

Sources consulted for the November 2026 revision:
[SARIF 2.1.0](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html),
[GitHub SARIF support](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning),
[Generating SARIF with AI](https://github.com/microsoft/sarif-sdk/blob/main/docs/ai/generating-sarif.md).
