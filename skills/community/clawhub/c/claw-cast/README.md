# clawcast (OpenClaw Skill)

## Start here: Install from GitHub (agent-facing)

If your agent is not using ClawHub yet, install ClawCast directly from this GitHub repo.

Tell your OpenClaw agent:
1. "Clone `https://github.com/ironystock/clawcast` into my workspace skills folder as `skills/clawcast`."
2. "Run `./skills/clawcast/scripts/obs_target_switch.sh <obs-host-ip> 4455 \"$HOME/.agentic-obs/db.sqlite\" --allow-cross-component-write`."
3. "Run `./skills/clawcast/scripts/start_overlay_server.sh` (serves only this skill folder, not workspace root)."
4. "Run `./skills/clawcast/scripts/rebuild_scenes.sh`."
5. "Run `./skills/clawcast/scripts/smoke_test_walkthrough.sh`."

Reusable, boilerplate-first skill for helping OpenClaw agents stand up and automate OBS scenes for **any** project (streams, demos, recordings, walkthroughs).

## Install via chat (quickest path)

Use these chat instructions with your OpenClaw agent:

1. "Install the clawcast skill"
2. "Target OBS at `<obs-host-ip>:4455`"
3. "Run the clawcast baseline rebuild"
4. "Run a recording smoke walkthrough"

Equivalent CLI path:

```bash
# from workspace root
openclaw skills install clawcast
# then run scripts shown in Quick start below
```

## North star

This project is intentionally generic:
- no creator-specific branding required
- no fixed scene story required
- no dependency on one specific stream theme

Use defaults to bootstrap quickly, then customize scenes/sources for your own workflow.

## What it automates

- target local or remote OBS WebSocket hosts
- host overlay files over LAN-safe HTTP
- create/recreate a baseline scene pack
- apply transition defaults
- optional audio baseline tuning
- run recording smoke walkthroughs
- optional stream dry-run

## Prerequisites

- OBS Studio running with WebSocket enabled (default port `4455`)
- `mcporter` installed and configured with an `obs` MCP server
- `python3`
- `sqlite3` (for OBS target switch script)
- `iproute2` (`ss`) for local server checks
- standard shell tools (`awk`, `grep`, `hostname`)

## Prerequisite 0 (required): validate mcporter + OBS MCP before running scripts

```bash
# Must show mcporter is installed
mcporter --help >/dev/null

# Must show an obs-capable server in your setup
mcporter list

# Must succeed before any ClawCast workflow scripts
mcporter call 'obs.get_obs_status()'
```

If the last command fails, finish your `mcporter`/OBS MCP setup first. ClawCast scripts now fail fast with this exact check.

## Quick start

### Mode A: Installed as an OpenClaw skill

Run from your OpenClaw workspace root.

```bash
# 1) Point to target OBS host (explicit cross-component write acknowledgement required)
./skills/clawcast/scripts/obs_target_switch.sh <obs-host-ip> 4455 \
  "$HOME/.agentic-obs/db.sqlite" --allow-cross-component-write

# 2) Start local overlay server (serves clawcast skill directory only)
./skills/clawcast/scripts/start_overlay_server.sh

# 3) Build baseline scenes + overlays
./skills/clawcast/scripts/rebuild_scenes.sh

# 4) Optional transition defaults
./skills/clawcast/scripts/apply_transition_preset.sh Fade 300

# 5) Optional audio baseline (set your own OBS input names)
export OBS_AUDIO_INPUTS="Mic/Aux,Desktop Audio"
./skills/clawcast/scripts/apply_audio_baseline.sh

# 6) Smoke recording walkthrough
./skills/clawcast/scripts/smoke_test_walkthrough.sh

# 7) Optional short streaming dry-run
./skills/clawcast/scripts/stream_dry_run.sh 15 "Intro" "Main Live"
```

### Mode B: Running from a cloned GitHub repo

Run from the cloned repo root.

```bash
# 1) Point to target OBS host (explicit cross-component write acknowledgement required)
./scripts/obs_target_switch.sh <obs-host-ip> 4455 \
  "$HOME/.agentic-obs/db.sqlite" --allow-cross-component-write

# 2) Start local overlay server (serves clawcast repo directory only)
./scripts/start_overlay_server.sh

# 3) Build baseline scenes + overlays
./scripts/rebuild_scenes.sh

# 4) Optional transition defaults
./scripts/apply_transition_preset.sh Fade 300

# 5) Optional audio baseline
export OBS_AUDIO_INPUTS="Mic/Aux,Desktop Audio"
./scripts/apply_audio_baseline.sh

# 6) Smoke recording walkthrough
./scripts/smoke_test_walkthrough.sh

# 7) Optional short streaming dry-run
./scripts/stream_dry_run.sh 15 "Intro" "Main Live"
```

## Security & data transmission

- **No bundled credentials:** This skill does not require API keys, tokens, or passwords in the repo.
- **OBS transport:** Control traffic uses OBS WebSocket on the host/port you set (default `4455`).
- **Overlay transport:** Overlay pages are served over local HTTP (default `:8787`) for OBS Browser Sources.
- **Scope lock:** `start_overlay_server.sh` serves the ClawCast skill/repo directory only (not workspace root).
- **Cross-component write guard:** `obs_target_switch.sh` requires an explicit DB path argument plus `--allow-cross-component-write` before writing DB config.
- **Trust boundary:** Run on trusted LAN/VPN only. Do not expose overlay HTTP or OBS WebSocket ports to the public internet.
- **Secrets handling:** Do not commit `.env` files, tokens, or private endpoint credentials into this repo.
- **Data profile:** The skill orchestrates scene/source configuration and local recording/stream actions; it does not phone home to third-party services by default.

## Runtime environment variables (intentional use)

- `OVERLAY_PORT` (optional): HTTP port for overlay server (default `8787`)
- `OVERLAY_BASE_PATH` (optional): overlay URL path used by rebuild script (default `/assets/overlays`)
- `OBS_AUDIO_INPUTS` (optional): comma-separated OBS inputs for `apply_audio_baseline.sh`
- `MIC_MUL` / `DESKTOP_MUL` (optional): volume multipliers for audio baseline helper

`obs_target_switch.sh` uses explicit positional arguments for DB path and cross-component-write acknowledgement (no required env vars).

All workflow scripts perform a fail-fast `mcporter call 'obs.get_obs_status()'` check before doing work.

## Asset packaging (required vs optional)

### Required (kept generic)
- `assets/overlays/intro.html`
- `assets/overlays/live-dashboard.html`
- `assets/overlays/work_status.html`
- `assets/overlays/presentation.html`
- `assets/overlays/control-panel.html`
- `assets/overlays/analytics.html`
- `assets/overlays/chat.html`
- `assets/overlays/brb.html`
- `assets/overlays/outro.html`

These power the default baseline scene map used by `scripts/rebuild_scenes.sh`.

### Optional examples (project-specific)
- `examples/project-specific/*`

These are not required for the baseline workflow and are provided only as adaptation references.

## Notes

- Installed mode defaults to overlays under `skills/clawcast/assets/overlays/`.
- Repo mode expects overlays under `assets/overlays/` in the cloned repo.
- For remote OBS, HTTP URLs are usually more reliable than `file://` local-file browser sources.
- You can replace baseline overlays with your own URLs/files after bootstrap.

## License

MIT
