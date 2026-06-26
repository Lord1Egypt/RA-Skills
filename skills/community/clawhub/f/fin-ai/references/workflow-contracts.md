# Workflow Contracts

## holdings_sync

### Inputs

- `source_payload`
- `current_holdings`
- `current_lot_ledger` (optional)
- `sync_context` (optional)
- `mode`

### Outputs

- `updated_holdings`
- `updated_lot_ledger` (optional)
- `sync_result`

### Rule

Return a full authoritative holdings payload, not a patch fragment.
`replace_groups` 表示只替换输入里出现的账户组；`overwrite_all` 表示用输入整份覆盖当天 holdings。

## portfolio_analysis

### Inputs

- `holdings`
- `market_context`
- `fx_context`
- `analysis_context` (optional)
- `lot_ledger` (optional)

### Outputs

- `analysis_result`
- `analysis_meta`

### Rule

Produce a current authoritative result aligned with retained snapshot semantics.

## persist_snapshot

### Inputs

- `analysis_result`
- `snapshot_date`
- `existing_snapshot_state` (optional)
- `existing_history_state` (optional)

### Outputs

- `written_snapshot`
- `history_update` (optional)
- `persist_result`

### Rule

Persist a dated derived artifact from `analysis_result` without promoting snapshot to the truth source.

## refresh_portfolio

### Inputs

- `source_payload` (optional)
- `date`
- `portfolio_dir`
- `update_history_csv` (optional)
- `confirm_write` (optional)

### Outputs

- `holdings_sync` (optional)
- `analysis_result`
- `persist_result`
- `warnings`

### Rule

Act only as a thin phase-1 runner over `holdings_sync -> portfolio_analysis -> persist_snapshot`.
Do not add new business logic or redefine source-of-truth boundaries.
Default to a safe temporary working copy when the target points at the real repo portfolio directory.
For user-facing usage, default to preview mode in a temporary working copy even for non-repo data directories.
Only write to the real target directory after explicit confirmation.
For released usage, support a user data root outside the repo as the default portfolio storage location.
If the target user data directory does not exist yet, bootstrap it before the main workflow runs.
Persist the user-selected default data directory in a user settings file so later runs do not need the path again.
