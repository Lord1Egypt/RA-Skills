# ADMET Payload Notes

## Job Types
1. `admet-dl`

## `/api/jobs` Required Form Fields
1. `name`
2. `type` (`admet-dl`)
3. `args` (JSON string)
4. `ws_id`
5. `expect_tokens`, `avail_tokens` (required in non-private mode)

## Input Modes

### Mode A: direct smiles
1. Add form field `smiles` as JSON array string
2. Example:
```text
smiles=["CCO","CCN","c1ccccc1"]
```
3. `args` can be minimal:
```json
{
  "account": "person"
}
```

### Mode B: dataset reference
1. Do not send `smiles` form field
2. Include in `args`:
- `dataset_id` (string)
- `smiles_col` (string)
3. Example:
```json
{
  "dataset_id": "YOUR_DATASET_ID",
  "smiles_col": "cs-smiles",
  "account": "person"
}
```

## `args` Fields
1. `account`: `person` or `team` (controls token account pool)
2. `dataset_id`: required in dataset mode
3. `smiles_col`: required in dataset mode
4. `sme` (bool): only for `admet-dl`
5. `is_calc_vis` (bool): optional for `admet-dl` SME mode

## Token Estimate Mapping
Use `/api/token/estimate` task_type:
1. `admet-dl` + `sme=false` => `admet_mert`
2. `admet-dl` + `sme=true` => `admet_mga`

## Minimal Stable Templates

### `admet-dl` dataset mode
```json
{
  "dataset_id": "DATASET_ID",
  "smiles_col": "cs-smiles",
  "account": "person",
  "sme": false
}
```

### `admet-dl` direct smiles + SME
```json
{
  "account": "person",
  "sme": true,
  "is_calc_vis": true
}
```

## Common Errors
1. `${field} must be provided`: missing top-level form field (`name/type/args/ws_id/expect_tokens/avail_tokens`)
2. `no dataset_id found in args`: dataset mode missing required args
3. `no valid smiles`: direct smiles list invalid or empty after parsing
4. `Insufficient account balance`: account tokens are not enough
