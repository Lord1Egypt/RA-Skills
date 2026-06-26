# Script Contract Migration

Use this when upgrading an older 1.x install that still uses the prepare/render contract. The current presence path is wrapper-first and prepare-only; this file is a legacy upgrade note, not the active runtime contract.

## What Changed

The old 1.x flow had one live runner with two stages:

```text
companion_run.py --stage prepare
  -> structured life_context
  -> agent executes render instructions
  -> agent writes activity_text
companion_run.py --stage render
  -> final_message_contract
  -> delivery/media/state contracts
```

Current presence output no longer contains `render_spec`. Writing constraints live in the cron template and integration docs.

## Migration Steps To Current Presence

1. Snapshot current local config, state files, and cron job payloads.
2. Convert life-like cron intent into `life_schedule.day_schedule.required_events`.
3. Replace visible cron payloads with the `companion-presence` wrapper-first flow from [presence-integration.md](./presence-integration.md).
4. Remove obsolete live-chain artifacts:
   - removed helper-script calls from the old multi-script chain
   - legacy life-prompt, selected-context, task-material, or final-render intermediate fields
   - duplicated top-level prepare `primary_goal`
   - `render_spec` in current prepare output
   - local runbook fields in runner output or local runbook paths in runner output
5. Remove `--stage render`, `final_message_contract`, custom render spec files, and media async runner assumptions from default presence payloads.
6. Run `python3 scripts/validate_release.py --root <SKILL_DIR> --config <CONFIG>`.
7. Run one real presence prepare/delivery test before declaring the upgrade complete.

## Acceptance

- Prepare output contains structured `life_context`.
- Prepare output contains no `render_spec` and no top-level `primary_goal`.
- There is no render output in the current default path.
- `media_contract` remains generic and contains no local runbook fields.
- No user-visible message exposes scripts, JSON, cron, tools, models, or routing internals.
- Presence commits state only after visible text delivery. Media completion only sends generated media and does not own event completion state.
