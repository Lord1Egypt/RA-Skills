# Decision flow details

These procedures target Python 0.1.1/core 0.8.0 and CLI 0.8.0.

All calls synchronous. Verdicts: `fit`, `fit_with_degradation`, `unfit`,
`indeterminate`. A non-fit verdict is a report, never an exception.

## Loading inputs

```python
import fitctl, pathlib

policy  = fitctl.Policy.from_json(pathlib.Path("policy.json").read_text())
profile = fitctl.Artifact.from_json(pathlib.Path("profile.json").read_text())
survey  = fitctl.Artifact.from_json(pathlib.Path("host.survey.json").read_text())
state   = fitctl.Artifact.from_json(pathlib.Path("host.state.json").read_text())
```

- `fitctl.builtin_config("policy", "general_compute_default.v1.json")` returns
  a dict of a bundled config for `Policy.from_dict`; only built-in ids resolve.
  Categories: `policy`, `service_profiles`, `extensions`,
  `invocation_contexts`; ids include the `.json` filename suffix.
  Profiles come back as dictionaries for `Artifact.from_dict`.
- Bundled fixture files have no envelope: load them with
  `fitctl.replay_survey(corpus_dir, fixture_id)` / `fitctl.replay_state(...)`
  where `corpus_dir` contains the corpus `manifest.v1.json`.

## Derive and validate

```python
# These fixed timestamps are for replay examples only.
# A live decision must pass the actual evaluation time.
contract = fitctl.derive_contract(survey, policy, at="2026-09-28T12:00:00Z")
report   = fitctl.validate(contract, profile, at="2026-09-28T12:00:00Z")
report.verdict, report.primary_reason_code
```

Modes (`mode=`): `contract_only` (default), `state_advisory`, `state_required`.

State-dependent requirements (accelerator visibility, allocatable memory,
path capacity) need:

```python
report = fitctl.validate(contract, profile, at=at, state=state,
                         mode="state_required", max_state_age_seconds=60)
```

Freshness validation checks `core_state.freshness.freshness_state`
(`stale` → `state_stale`); with `max_state_age_seconds` it also compares
`at` against `core_state.freshness.observed_at`.
Without state, `state_required`/`state_advisory` give
`indeterminate` / `state_missing`. Stale state gives
`indeterminate` / `state_stale`.

## Verdict vs operational error

| Situation | Outcome |
|---|---|
| Requirements not met | report with `unfit` + reason code (valid result) |
| Missing/stale state in state modes | report with `indeterminate` + `state_missing`/`state_stale` |
| Malformed artifact JSON | `fitctl.DecodeError` |
| Core validation of inputs fails | `fitctl.CoreError` (has `reason_code`, e.g. `validation_input_invalid` for a bad age with supplied state) |
| Bad Python arguments | `TypeError` / `ValueError` / `OverflowError` |
| Export / native panic | `SerializationError` / `NativeError` |

`FitctlError` is the base. Catch `FitctlError` for operational failures;
verdicts are properties, never exceptions.

## Artifacts are immutable

`to_dict()` returns an independent dict; `to_json()` JSON text.
`semantic_hash()`/`semantic_bytes()` (encoding `fitctl.semantic_cbor.v2`)
are stable across JSON roundtrips. For redaction,
`survey.redact("external", at=at)` (profiles `local`, `fleet`, `auditor`,
`external`) replaces `provenance.correlation_id` with the redacted artifact
id and `provenance.source` with `redacted:<profile>:source`, and changes
the semantic hash. Redaction reduces disclosure and clears signatures; it
is NOT anonymity proof — inspect before sharing and never auto-upload.

## CLI route (fitctl 0.8.0)

Install the CLI as described in `installation.md`. Config comes from the
installed binary, no checkout:

```bash
fitctl config export --out-dir fitctl-config    # -> fitctl-config/configs/...
fitctl survey --live > reports/host.survey.json
fitctl state  --live --path-check "workspace=$PWD" > reports/host.state.json
fitctl contract --survey reports/host.survey.json \
  --policy fitctl-config/configs/policy/general_compute_default.v1.json > reports/host.contract.json
# live decision: --live-state collects fresh state; no --max-state-age with it in 0.8.0
fitctl validate --contract reports/host.contract.json \
  --profile fitctl-config/configs/service_profiles/cpu_small_state_required.v2.json \
  --live-state --validation-mode state_required \
  --state-out reports/decision.state.json --validation-out reports/validation.json --require-fit
fitctl inspect --input reports/validation.json      # text view; JSON is the interface
```

Saved-state variant: replace `--live-state --state-out ...` with
`--state reports/host.state.json --max-state-age 60s`.
`--fail-on-unfit` accepts fit + fit_with_degradation; `--require-fit`
accepts only fit; the report stays on stdout and a gate rejection uses
exit 1. Input/operational failures (unreadable or corrupt artifacts,
missing state source for `state_required`) exit 2 with stderr detail and
possibly no report — unlike Python, where the same missing-state case
yields an `indeterminate` report. `validate --survey ... --policy ...
--profile ...` is a supported convenience chain. Batch, CUDA, redact, diff
and the experimental commands are covered in `advanced-cli.md`. Record the
exact `fitctl --version` whenever you rely on CLI behavior.
