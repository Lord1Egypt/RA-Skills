# ARW config contract

## Current repo-backed defaults

The skill currently runs ARW against a checked-out repository.

Repo location:
- pass `--repo-root /path/to/arw-watchtower`, or
- set `ARW_REPO_ROOT=/path/to/arw-watchtower`, or
- let the wrapper autodetect the repo when the skill lives inside that checkout.

Default repo-relative path:
- artifact root: `artifacts/arw/`

## Important configurable values

The wrapper supports or passes through ARW settings for:
- `out_dir`
- `suite`
- `window_hours`
- `trend_window`
- `trend_flip_threshold`
- `freshness_max_age_seconds`
- `probe_runtime_threshold_ms`
- `max_delivery_latency_seconds`
- `max_probe_evidence_age_seconds`
- `max_alignment_gap_seconds`
- `alert_cooldown_seconds`
- `expected_recipient`
- `actual_recipient`
- `send_ref`
- `send_started_at`
- `confirmation_ref`
- `confirmation_at`

For the wrapper verification flows, blank delivery fields fall back to generic dry-run values so the skill does not depend on a workspace-local Discord channel id.

## Example config

See `assets/example-config.json` for a repo-backed RC1 example with generic dry-run delivery refs.

## RC1 portability rule

Keep the skill-facing config explicit and minimal.

Do not assume operators know hidden workspace paths or hardcoded recipients.
Where repo-specific assumptions remain, document them clearly instead of hiding them.
