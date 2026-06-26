# Dashboard Plan

## Goal

Provide a lightweight real-time web page for EDA runs, allowing users to view:

- Current phase and status
- Latest logs
- Generated artifacts
- Preview images
- Final summary

## MVP Features

- Static HTML generated from current run results
- Local HTTP server
- Sections for preview, summary, and raw JSON
- PPA panel with area/utilization/power/timing/DRC-LVS overview

## Next Version

- `progress.json` updated per stage
- Tail view of `flow.log` and `sim.log`
- Links to GDS/DEF/ODB files
- Multiple run selector
- Auto-refresh capability

## Future Productized Version

- Richer OpenClaw-hosted page
- Feishu interactive card with summary and preview link
- Push updates on phase completion
