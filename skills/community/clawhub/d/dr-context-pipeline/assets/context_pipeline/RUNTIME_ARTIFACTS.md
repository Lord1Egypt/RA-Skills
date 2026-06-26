# Runtime Artifacts — dr-context-pipeline

Runtime artifacts make pipeline claims inspectable without forcing every normal response to dump JSON into the transcript.

## Scope
Artifacts are required for `debug` and `audit` mode.

`normal` mode may build the same objects internally but should expose only the compact evidence summary unless the user asks for more detail.

## Run folder
Use one folder per pipeline run:

```text
.openclaw/context-runs/<run_id>/
```

`run_id` should be stable enough to connect all artifacts from one turn. Prefer:

```text
YYYYMMDDTHHMMSSZ-<short-random-or-session-suffix>
```

If the host already provides a run ID, use that instead.

## Required artifacts
For `debug` and `audit`, write these files when the corresponding step is reached:

```text
retrieval_bundle.json
context_pack.json
lint_result.json
reasoning_input_summary.json
```

For `audit`, also write:

```text
receipt_ledger.json
```

## Artifact meanings
- `retrieval_bundle.json`: the Retrieval Bundle object conforming to `schemas/retrieval_bundle.schema.json`.
- `context_pack.json`: the Context Pack object conforming to `schemas/context_pack.schema.json`, or the attempted pack when lint fails.
- `lint_result.json`: lint status, errors, and whether fallback was used.
- `reasoning_input_summary.json`: compact summary of what was passed into the reasoning step; do not duplicate full user-private context unless needed.
- `receipt_ledger.json`: audit-mode Receipt Ledger conforming to `schemas/receipt_ledger.schema.json`.

## Hashes
When an artifact is referenced in a Receipt Ledger entry, include:

- `proof.artifact_path`
- `proof.artifact_sha256`

Use SHA-256 over the exact bytes written to disk.

## Failure behavior
In `audit` mode, if a required artifact cannot be written or hashed, the run must fail closed with:

```text
NOT EXECUTED: <reason>
```

In `debug` mode, if artifact persistence fails but the pipeline can still answer safely, report the artifact failure explicitly before answering. Do not pretend the artifact exists.

## Transcript behavior
- `normal`: do not expose artifact paths unless asked.
- `debug`: include artifact paths with full Retrieval Bundle and Context Pack output.
- `audit`: include artifact paths, hashes, and Receipt Ledger.
