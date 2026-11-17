# v1.5 Release Notes

## Added

- `references/end-to-end-orchestration.md`
- `scripts/seedance_client.py`
- safe dry-run mode
- explicit paid-submit confirmation
- task state ledger
- polling and download
- local reference embedding via `--embed-local-refs`
- full chain from script creation to generated video

## Changed

- `SKILL.md` now includes a numbered full-chain execution path.
- `build_seedance_tasks.py` keeps local reference paths in `meta.reference_paths` instead of silently dropping them.
- `seedance_client.py dry-run` warns when tasks lack an image reference or need local embedding.
- Project completion now requires provider task IDs, statuses and downloaded files in the state ledger.

## Safety

- Paid submission requires both `--execute` and `--confirm-paid`.
- `--limit` controls the maximum number of tasks in one batch.
- API keys are read from `ARK_API_KEY` and never written to state files.
- Local images are only embedded when explicitly requested.

## Validation

- Skill validation: passed.
- Fire Monkey project validation: passed.
- Retention audit: passed.
- Seedance dry-run: 45 tasks, 360 seconds total video.
- Local reference embedding: tested.
