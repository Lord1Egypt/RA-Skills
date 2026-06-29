---
name: asusctl-usage
description: Use when controlling ASUS ROG laptop hardware after asusctl / asusd / rog-control-center have been compiled and installed. Covers the asusctl CLI command tree, common tasks (profiles, fan curves, aura LEDs, battery charge limit, armoury BIOS settings), GUI, user-daemon custom effects, keybinds, verification, and troubleshooting.
version: 0.1.1
emoji: 🎮
author: Hermes Agent (based on official asusctl project)
license: MIT
metadata:
  hermes:
    tags: [asus, rog, hardware, cli, usage, gaming, fan, aura, profile, battery]
    related_skills: []
  openclaw:
    # Pure knowledge skill for runtime usage of the compiled executables.
---

# asusctl Runtime Usage Guide

## Overview
After `asusctl` (the suite) is built and installed via `make` + `sudo make install`, the main executables are:

- `asusd` — system daemon (must be running; auto-started via udev rule + systemd unit)
- `asusctl` — primary CLI for querying and controlling hardware features
- `rog-control-center` — GUI (tray + full interface)
- `asusd-user` — user-level daemon for custom per-key / anime effects (optional but powerful)

`asusctl` queries the daemon for the laptop's supported features and only exposes relevant commands. Most features (LEDs, fans, charge limit, profiles, BIOS settings) are exposed safely over D-Bus.

The skill focuses on **using the compiled binaries**.

## When to Use
- Daily hardware control on ASUS ROG / TUF / Zephyrus laptops (profiles, fan curves, RGB, battery limit, MUX switch, etc.).
- Binding Fn keys or creating scripts/aliases.
- Setting up custom LED sequences or AniMe animations.
- Checking what the current laptop actually supports.
- Troubleshooting "feature not available" or daemon issues after a build/install.

**Do not use for:**
- Building or installing the tools themselves (refer to the project README and Makefile for build instructions).
- Distro-packaged versions (commands are the same, but paths may differ slightly).

## Prerequisites
- `asusd` daemon running:
  ```sh
  systemctl status asusd
  ```
  If not: `sudo systemctl enable --now asusd`

- `asusctl` and `rog-control-center` in PATH (installed to /usr/bin by `sudo make install`).

- For full features: recent kernel (latest recommended), correct udev rules and D-Bus policy installed.

## asusctl CLI Structure
```sh
asusctl <command> [subcommand] [options]
```

Get help anywhere:
```sh
asusctl --help
asusctl <command> --help
asusctl <command> <subcommand> --help
```

**Top-level commands** (from source):

- `profile` — thermal/fan profiles (Balanced, Performance, Quiet, ...)
- `fan-curve` — custom fan curves per profile/CPU/GPU
- `aura` — RGB keyboard, lightbar, logo, lid, etc. (effect, power)
- `anime` — AniMe Matrix display control (on supported G14/G16/M16 etc.)
- `battery` — charge limit + one-shot full charge
- `armoury` — firmware/BIOS attributes (POST sound, GPU MUX, etc.)
- `brightness` (or `leds`) — keyboard backlight brightness
- `backlight` — screenpad brightness / gamma / sync (on supported models)
- `slash` / `scsi` — device-specific (ROG Slash, SCSI Aura on some models)
- `info` — version + `asusctl info --show-supported` (critical for discovering available features)

Default command is `info`.

## Most Useful Everyday Commands

### Profiles (Fn+F5 keybind classic)
```sh
asusctl profile list
asusctl profile get
asusctl profile next          # cycle
asusctl profile set Performance
asusctl profile set Quiet -a   # set for AC power
asusctl profile set Balanced -b  # set for battery
```

### Fan Curves (on supported laptops)
```sh
asusctl fan-curve --get-enabled
asusctl fan-curve --mod-profile Balanced --fan CPU --data "30c:0%,40c:5%,50c:10%,60c:20%,70c:35%,80c:55%,90c:65%,100c:65%"
asusctl fan-curve --mod-profile Performance --default   # reset to EC default
asusctl fan-curve --mod-profile Balanced --enable-fan-curves true
```

Data format: `temp:percent%` or raw 0-255 values. Order is fixed low-to-high.

### Aura / RGB LEDs
```sh
asusctl aura effect --help
asusctl aura -n          # next built-in mode (great for keybind)
asusctl aura -p          # previous

# Power control (newer models)
asusctl aura power ...

# Older/TUF models
asusctl aura power-tuf --awake true --keyboard --lightbar ...
```

Keyboard brightness (separate from aura modes):
```sh
asusctl leds set high
asusctl leds get
asusctl leds next
```

### Battery / Charge Limit
```sh
asusctl battery limit 80
asusctl battery info
asusctl battery oneshot 100   # one-time full charge
```

### Armoury Crate BIOS settings (asus-armoury)
```sh
asusctl armoury list
asusctl armoury get <property>
asusctl armoury set <property> <value>

# Common examples (model-dependent):
# asusctl armoury set post_sound 0
# asusctl armoury set gpu_mux_mode 0   # or 1 for discrete only
```

### AniMe Matrix (lid display on supported models)
```sh
asusctl anime --help
asusctl anime --brightness high
asusctl anime --clear
```

### Info & Discovery (always run first on new hardware)
```sh
asusctl info
asusctl info --show-supported   # shows exactly what this laptop exposes
```

## GUI
```sh
rog-control-center
```
Launches the full Slint-based interface with tabs for System, Aura, Fans, Anime, GPU, etc. Also provides tray icon + notifications.

## Advanced: User Daemon Custom Effects (`asusd-user`)
For per-user custom Aura sequences and AniMe without affecting system defaults, edit `~/.config/rog/rog-user.cfg` and individual `.ron` / `.json` files in the same directory.

See `MANUAL.md` (installed or in source) for full RON/JSON examples of Breathe, Static, DoomFlicker, ImageAnimation, AsusAnimation, Pause, etc.

After editing:
```sh
# Restart user daemon if needed
systemctl --user restart asusd-user   # or just log out/in
```

## Recommended Keybinds (Sway/i3/Hyprland/GNOME etc.)
- Fan profile cycle: `asusctl profile -n`
- Aura next/prev: `asusctl aura -n` / `asusctl aura -p`
- Keyboard brightness: `asusctl leds next`

## Verification & Health Checks
After any change or on login:
```sh
systemctl status asusd
asusctl info --show-supported
asusctl profile get
asusctl battery info
asusctl leds get
```

Check logs for daemon issues:
```sh
journalctl -u asusd -b -f
journalctl --user -u asusd-user -b
```

## Common Pitfalls & Fixes
- "Command not found" or limited options → `asusctl info --show-supported` (your model may not support the feature, or daemon not running / udev rules missing).
- Changes don't persist → Restart daemon after major upgrades: `sudo systemctl daemon-reload && sudo systemctl restart asusd`
- Fan curves ignored → Ensure `--enable-fan-curves true` and the profile is active.
- No RGB or partial zones → Use `asusctl aura power ...` or check laptop is in `aura_support.ron`.
- GUI won't start → Missing runtime deps for Slint/GTK (rare after proper `make install`).
- Permission denied on hardware → Usually fixed by correct udev rule + D-Bus policy from the install step.

Always start with `asusctl info --show-supported` on a new machine or after kernel update.

## One-Shot Recipes
**Cycle profile + verify:**
```sh
asusctl profile next && asusctl profile get
```

**Set aggressive fan curve on Performance + charge limit:**
```sh
asusctl profile set Performance
asusctl fan-curve --mod-profile Performance --fan CPU --data "30c:10%,50c:30%,70c:60%,90c:100%"
asusctl battery limit 60
```

**Discover + control everything available:**
```sh
asusctl info --show-supported
asusctl armoury list
asusctl aura effect --help
```

## References
- `asusctl --help` and per-command help (the source of truth after install)
- `MANUAL.md` (in source or `/usr/share/doc/...`) — detailed config file formats and user-daemon examples
- `README.md` — high-level feature list
- Source (for exact flags): `asusctl/src/cli_opts.rs`, `fan_curve_cli.rs`, `aura_cli.rs`, `anime_cli.rs`, etc.

This skill ensures agents (and users) get the most out of the compiled `asusctl` / `rog-control-center` executables using the real command surface and best practices.
