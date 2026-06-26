# Workflows

This skill is optimized for financial planning flows where the agent should prefer verified embedded data and deterministic local compute over freeform reasoning.

## Reference Data

Use `entropyfa data coverage` when the user asks what reference data exists or when you need to discover the right key.

Use `entropyfa data lookup` when the user needs:

- current embedded federal planning thresholds or tables
- source URLs
- verification status
- a trustable answer for tax, retirement, estate, IRMAA, Social Security, or pension reference data

When `data lookup` returns a result, preserve:

- `verification_status`
- `pipeline_reviewed`
- `sources`
- `value`

Do not replace those values with unsupported paraphrases when the raw lookup already answers the question.

## Compute Commands

Use `entropyfa compute <command> --schema` when:

- the user has not provided all required fields
- you need to know the expected JSON shape
- you need to confirm which command is appropriate

Use `entropyfa compute <command> --json ...` when the required inputs are known. Favor these commands for:

- `federal-tax`
- `estate-tax`
- `rmd`
- `rmd-schedule`
- `roth-conversion`
- `roth-conversion-strategy`
- `pension-comparison`
- `projection`
- `goal-solver`

## Projection Output

`compute projection` should default to JSON-only output.

Use `--visual` only when the user explicitly wants a terminal dashboard or human-facing chart-like output. Do not enable it for machine-only or agent-only flows.

## Trust Rules

- Prefer official embedded reference data over recollection.
- If a lookup exists, do not invent yearly thresholds from memory.
- If a topic is not covered by the shipped dataset, say so plainly.
- If the user asks for provenance, cite the returned `sources` rather than hand-waving the answer.
