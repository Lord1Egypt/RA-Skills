---
name: dfs-reset
description: Detect DFS radar events and reset Ubiquiti airOS devices to restore configured frequencies, managed by UISP NMS. Use when checking whether WISP APs were forced off their configured DFS channels, listing devices from UISP, inspecting AP health or clients, or rebooting a DFS-affected AP after operator confirmation.
---

# DFS Reset

Use the MCP endpoint configured for this deployment. Placeholder example:

`https://example.invalid:8443`

Source project for this MCP server:

`https://github.com/wispnet/wisp-reset-airos-mcp/`

This MCP server uses streamable HTTP with session-based MCP initialization.

## Expected workflow

1. Initialize an MCP session.
2. Send `notifications/initialized`.
3. Call tools on the same session.

## Core workflow

1. Detect: use `detect_dfs` on an AP to compare configured vs actual frequency.
2. Report: tell the operator which APs shifted and what channels they moved to.
3. Reset: use `reset_device` only after operator confirmation.
4. Verify: re-run `detect_dfs` after about 60 seconds.

## Tool reference

### `list_devices(site=None)`
List UISP-managed devices, optionally filtered by site.

### `get_device(identifier)`
Get detailed device information by name, IP, or UISP device ID.

### `detect_dfs(ip)`
Compare UISP configured frequency with the device's actual operating frequency.

### `reset_device(identifier)`
Reboot a device through UISP. Always confirm with the operator first.

### `get_clients(ip)`
Fetch connected stations for an AP.

### `get_device_stats(ip)`
Fetch AP health details including uptime, CPU, memory, and temperature.

### `sweep_clients(site=None)`
Collect client tables across APs concurrently.

## Safety rules

1. Never call `reset_device` without explicit operator confirmation.
2. Do not mix broad sweep actions with reset actions in one step.
3. Treat DFS shifts as informational until the operator wants corrective action.
4. Verify every reset with a follow-up `detect_dfs`.
5. Expect partial sweep results when some APs are unreachable.

## Signal interpretation

- Better than -65 dBm: good
- -65 to -75 dBm: fair
- -75 to -80 dBm: poor
- Worse than -80 dBm: unusable

Typical clean noise floor is around -90 to -95 dBm. Noise above -85 dBm suggests interference.
