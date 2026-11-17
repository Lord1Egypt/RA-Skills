# Incremental Monitoring

Use monitoring only after a successful baseline contains `state.json` and `evidence.json`. Run `scripts/monitor_research.py --baseline <run-directory>` for one bounded refresh. It reuses the plan, creates a timestamped snapshot, and writes content-hash changes to `changes.json`.

For a recurring user request, schedule that one-shot command through the host's supported automation mechanism rather than implementing an endless local loop. Alert only on material changes after inspecting the new evidence; a hash change alone is not proof of a pricing or product change.

Preserve every snapshot used for a delivered change claim. Never resubmit a still-running Builder task merely because a monitoring turn ended.
