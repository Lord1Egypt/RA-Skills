# Advanced CLI reference (0.8.0)

CLI-only capabilities beyond the core survey/contract/validate flow.
Get exact flags from `fitctl <command> --help` on the installed version —
never copy flags across releases. Config paths below assume
`fitctl config export --out-dir fitctl-config` (see installation.md).

## Command tiers (0.8.0 help)

Stable: survey, contract, classify, state, validate, diff, redact, sign,
verify, config, inspect. Experimental: bundle, bundle-config, export,
completion, storage, thermal, inspect-config (`resolve-config` alias),
lock-policy-pack, recommend. Experimental means the interface is marked
experimental, not absent.

## Live CUDA extension

```bash
fitctl survey --live --enable-extension fitctl.runtime.cuda > reports/cuda.survey.json
fitctl contract --survey reports/cuda.survey.json --policy fitctl-config/configs/policy/general_compute_default.v1.json \
  --enable-extension fitctl.runtime.cuda > reports/cuda.contract.json
fitctl state --live --collect cuda-runtime > reports/cuda.cuda-state.json
fitctl validate --contract reports/cuda.contract.json \
  --profile fitctl-config/configs/service_profiles/general_compute_cuda_runtime_allocatable_memory_required.v2.json \
  --state reports/cuda.cuda-state.json --validation-mode state_required --max-state-age 60s \
  > reports/cuda.validation.json
```

Report driver version, driver-supported CUDA level, toolkit, and runtime
availability as separate observations (`extension_contract."fitctl.runtime.cuda"`:
`driver_version`, `driver_supported_cuda_version`, `runtime_available`,
per-probe `probe_status`). A driver can be observed while the toolkit is
`source_unavailable` and the runtime is `library_unavailable`. Preserve
these distinct outcomes and read the resulting validation report. Do not
"fix" availability by installing toolkits
unless the task authorizes it. `allocatable_memory_bytes` in
`state.extension_state` is a point-in-time allocatable value.

Environment catalogues: `--cuda-environment-catalogue` +
`--cuda-environment-id` (live) / `--cuda-selected-environment-input`
(replay) exist in 0.8.0.

## Storage checks and probes

```bash
fitctl state --live --path-check "workspace=$PWD" --probe-path-health workspace > reports/storage.state.json
fitctl storage profile init --path "workspace=$PWD" --profile-id workspace_storage --out reports/storage.profile.json
```

`probe_links` / `link_pairs` create and remove temporary entries in the
inspected paths: explicit authorization for those paths is required, and
you must inspect the reported cleanup outcome, not just link support. The
generated storage profile is an operator-review skeleton — never assign
application roles (cache/scratch) from mount names alone.

## Batch, sharing, and bundles

```bash
fitctl classify --contract C --profile P1 --profile P2 > reports/batch.json
fitctl inspect --input reports/batch.json --view matrix
fitctl classify --contract C --profile P1 --export-view rows_csv > reports/batch.csv
fitctl redact --profile external --input reports/host.state.json > reports/shared.state.json
fitctl diff --left A.json --right B.json        # semantic comparison; compact JSON view optional
```

- Recommendations: `fitctl recommend --validation-report V --recommendation-pack fitctl-config/configs/recommendations/...`
  — advisory only.
- Decision bundles: `fitctl bundle --validation-report V --contract C [--state S ...]`
  — bundle only artifacts from the SAME decision (matching hashes); a
  filename match proves nothing. Use fresh run directories so reruns don't
  overwrite retained evidence.
- Adapter exports: `fitctl export` emits `kubernetes_labels`,
  `nomad_attributes`, `gating_summary`, `identity_summary` — it emits,
  never deploys.
- Redaction reduces disclosure and clears signatures; it is not anonymity
  proof. Inspect output before sharing; never auto-upload live artifacts.

## Signing and verification

`fitctl sign --key <supplied-private-key> --input <artifact>` attaches a
signature; `fitctl verify --input <artifact> --policy <trust-policy>`
verifies under an EXPLICIT trust policy. Creating identities or promoting
trust is a deliberate operation, never a side effect of inspection. 0.8
changed semantic encoding (`fitctl.semantic_cbor.v2`): hashes/locks/
signatures from pre-0.8 encodings need coordinated regeneration; changing
a version label never updates a stored hash.

## Other commands

- `fitctl completion bash|zsh|fish` prints completions; installing them is
  a separate shell-local action.
- `fitctl inspect-config` (alias `resolve-config`) resolves policy/
  profile/catalogue/extension/trust selections.
- `fitctl lock-policy-pack`, `bundle-config`: experimental config packing.
- Exit codes: 0 = completed and the configured gate did not reject (with no
  gate flags, a rejecting verdict prints with exit 0 — read
  `.report.verdict`); 1 = a configured verdict gate rejected
  (`--fail-on-unfit` accepts fit+fit_with_degradation, `--require-fit`
  accepts only fit; the validation report stays on stdout, rejection note
  on stderr); 2 = usage, input, or operational failure (verified on CLI
  0.8.0: unreadable survey, corrupt JSON, and `--validation-mode
  state_required` without `--state`/`--live-state`/`--thermal-evidence`
  all exit 2 — inspect stderr; no report may exist). Note this differs
  from Python: `validate(mode="state_required")` without state returns an
  `indeterminate` report, not an argument error.
