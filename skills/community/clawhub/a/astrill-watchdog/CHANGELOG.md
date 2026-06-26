# astrill-watchdog Changelog

## 2.0.0 — 2026-03-07

### Changed (breaking — complete reconnect redesign)
- **Replaced three-method escalating reconnect with a single full restart.**
  Testing on Ubuntu/GNOME/Wayland revealed all three original methods were
  non-functional:
  - Method 1 (`astrill /reconnect`): silently ignored — it is a single-instance
    handoff argument, not a runtime control command.
  - Method 2 (kill `asovpnc`/`asproxy`): both child processes run as root;
    `pkill` without sudo returns exit 1 and does nothing.
  - Method 3 (`nohup /autostart`): Astrill requires a Wayland display session
    to initialize its GUI stack; `nohup` in a systemd service context lacks
    `WAYLAND_DISPLAY`, causing silent launch failure.

  The new single method: `pkill astrill` + `setsid /autostart` with the full
  desktop environment (`DISPLAY`, `DBUS_SESSION_BUS_ADDRESS`, `XDG_SESSION_TYPE`,
  `WAYLAND_DISPLAY`). Confirmed working on Ubuntu 24/GNOME/Wayland.

- **`run_as_astrill` user-enforcement wrapper removed.**
  The watchdog always runs as the desktop user; the wrapper added complexity
  and introduced a silent failure mode when `ASTRILL_USER` was unresolvable
  at startup (e.g. Astrill not yet running), causing the relaunch to abort
  without logging a useful error.

### Removed
- `MAX_ATTEMPTS`, `RECONNECT_WAIT_1/2/3` config vars → replaced by `RECONNECT_WAIT=60`
- `_method_reconnect_builtin`, `_method_kill_children`, `_method_full_restart` functions
- `run_as_astrill` function
- WireGuard (Tier 2) — deferred to next version

---

## 1.x — 2026-02

- StealthVPN monitoring with `set -uo pipefail` fix (removed `set -e`)
- 3-method reconnect cascade
- Log rotation, PID file, systemd user unit
- Initial WireGuard Tier 2 implementation
