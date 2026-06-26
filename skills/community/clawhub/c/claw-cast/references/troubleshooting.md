# Troubleshooting

## Browser source blank on remote OBS

1. Confirm OBS host can reach `http://<agent-lan-ip>:8787/...`
2. Prefer HTTP URLs over `file://` for remote OBS
3. Recreate source with cache-busted URL (`?v=<timestamp>`)
4. In OBS UI, disable browser-source hardware acceleration if rendering is unstable

## Recording start says success but output is not running

- Check OBS is not blocked by open settings dialogs
- Verify Recording path/format in OBS settings
- Run one manual start/stop in OBS, then retry automation

## Audio not present in recordings

- Verify source exists and is unmuted
- Verify source volume is not zero
- Verify track routing in Advanced Audio Properties
- For multi-scene music continuity, use one shared source duplicated across scenes

## OBS connection failures

- Confirm OBS is running and WebSocket is enabled
- Verify host/port in `obs_target_switch.sh`
- Retry with `mcporter call 'obs.get_obs_status()'`
