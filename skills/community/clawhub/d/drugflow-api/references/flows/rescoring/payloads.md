# Rescoring Payload Notes

## Job Type
1. `rescoring`

## `/api/jobs` Required Form Fields
1. `name`
2. `type` (`rescoring`)
3. `args` (JSON string)
4. `pdb` (protein dataset id)
5. `ligands` (ligands dataset id, uploaded from `.sdf`)
6. `smiles_col` (smiles column name inside ligands dataset)
7. `ws_id`
8. `expect_tokens`, `avail_tokens` (required in non-private mode)

## Input Constraint
1. Upstream input must be `pdb + sdf` files.
2. Skill script uploads the two files first, then uses returned dataset ids to create rescoring job.

## `args` Fields
1. `mode` (required): currently stable mode is `semi`
2. `rescoring_functions` (required): list, e.g. `["RTMS"]`
3. `account` (optional): `person` or `team`

## Minimal Stable Template
```json
{
  "mode": "semi",
  "rescoring_functions": ["RTMS"],
  "account": "person"
}
```

## Token Estimate Mapping
Use `/api/token/estimate` with:
1. `task_type = rescoring`
2. `input_amount = ligands count`
3. `extra_multiples = 1`

Backend billing logic is `ligands_count * task_token_map['rescoring']`.

## Common Errors
1. `no pdb found in request`: missing top-level `pdb` form field
2. `no ligands found in request`: missing top-level `ligands` form field
3. `parmaters process failed`: malformed `args` JSON or invalid `smiles_col`
4. `Insufficient account balance`: balance is lower than rescoring expected consumption
5. `${field} must be provided`: missing required top-level field in `/api/jobs`
