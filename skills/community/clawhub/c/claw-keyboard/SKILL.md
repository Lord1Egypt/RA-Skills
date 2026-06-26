---
name: claw-keyboard
description: Control keyboard RGB backlight, custom LEDs, macros, key mapping, and profile settings via USB HID. Use when the user asks to control keyboard lighting, manage macros, remap keys, adjust profile parameters, render KLE layouts, or interact with compatible USB keyboards (e.g. LUXSWH R68pro).
version: 1.0.4
homepage: https://github.com/clawdevice/claw-keyboard
metadata:
  openclaw:
    emoji: "⌨️"
    version: "1.0.3"
    requires:
      bins:
        - claw-keyboard
    os:
      - darwin
      - linux
      - win32
    install:
      - id: darwin-arm64
        kind: download
        url: https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-darwin-arm64
        bins: [claw-keyboard]
        label: macOS Apple Silicon
        os: [darwin]
      - id: darwin-amd64
        kind: download
        url: https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-darwin-amd64
        bins: [claw-keyboard]
        label: macOS Intel
        os: [darwin]
      - id: linux-amd64
        kind: download
        url: https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-linux-amd64
        bins: [claw-keyboard]
        label: Linux x86_64
        os: [linux]
      - id: linux-arm64
        kind: download
        url: https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-linux-arm64
        bins: [claw-keyboard]
        label: Linux ARM64
        os: [linux]
      - id: windows-amd64
        kind: download
        url: https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-windows-amd64.exe
        bins: [claw-keyboard]
        label: Windows x86_64
        os: [win32]
      - id: windows-arm64
        kind: download
        url: https://github.com/clawdevice/claw-keyboard/releases/latest/download/claw-keyboard-windows-arm64.exe
        bins: [claw-keyboard]
        label: Windows ARM64
        os: [win32]
---

# claw-keyboard

Use `claw-keyboard` to discover and control USB keyboards that support the vendor HID protocol (UsagePage `0xFF60`, Usage `0x61`). Tested with LUXSWH R68pro. Supports RGB backlight, custom per-key LEDs, macros, key remapping, profile tuning, KLE layout rendering, and multi-keyboard management.

## Quick start

- `claw-keyboard discover` — scan for connected keyboards
- `claw-keyboard info` — show keyboard details (rows, cols, firmware, mode, RGB state)
- `claw-keyboard rgb color red` — set backlight to red
- `claw-keyboard rgb brightness 128` — set brightness (0-255)
- `claw-keyboard rgb effect 1` — set lighting effect mode (0-20)
- `claw-keyboard rgb save` — persist current settings to flash

## Device selection

When multiple keyboards are connected, use `--device <path>` to target a specific one. Run `discover` to list available paths.

## RGB control

- `claw-keyboard rgb status` — show current brightness, effect, speed, color
- `claw-keyboard rgb color <name|hue>` — set color by name (red, green, blue, cyan, purple, orange, yellow, white) or hue value (0-255)
- `claw-keyboard rgb brightness <0-255>` — set LED brightness
- `claw-keyboard rgb effect <0-20>` — set lighting effect mode (0 = rainbow, 1 = solid, 2-20 = animations)
- `claw-keyboard rgb speed <0-5>` — set animation speed (0 = slowest, 5 = fastest)
- `claw-keyboard rgb save` — write current config to flash (avoid frequent calls — flash has limited write cycles)

## Custom LED control

- `claw-keyboard led on <row> <col>` — turn on a single LED at row/col position
- `claw-keyboard led off <row> <col>` — turn off a single LED
- `claw-keyboard led clear` — turn off all LEDs
- `claw-keyboard led list` — list currently lit LED positions
- `claw-keyboard led sync-start` — start onboard LED effect sync (keyboard reports LED data to PC)
- `claw-keyboard led sync-stop` — stop onboard LED effect sync

## Key mapping

- `claw-keyboard keymap read` — dump current key layout (all layers)
- `claw-keyboard keymap layers` — show number of supported layers
- `claw-keyboard keymap get <layer> <row> <col>` — read the 2-byte HID key value at a position
- `claw-keyboard keymap set <layer> <row> <col> <keyvalue>` — set a single key (4-digit hex, e.g. `0029` = Escape). **Requires user confirmation** — this changes a physical key binding on the keyboard.
- `claw-keyboard keymap write <file>` — write complete keymap from hex file. **Requires user confirmation** — this overwrites all key bindings.

## Macro management

- `claw-keyboard macro list` — show macro count, storage usage, and parsed macros
- `claw-keyboard macro clear` — erase all macros. **Requires user confirmation** — this deletes all macros permanently.
- `claw-keyboard macro dump` — hex dump of raw macro storage data
- `claw-keyboard macro set <actions> [<actions>...]` — configure macros from action strings (replaces all existing macros). **Requires user confirmation**.
  - Action format: `tap:<keycode>`, `press:<keycode>`, `release:<keycode>`, `delay:<ms>` separated by commas
  - Example: `claw-keyboard macro set "press:0xE0,tap:0x06,release:0xE0"` (Ctrl+C)

## Profile parameters

- `claw-keyboard profile get` — read profile parameters (debounce, TAP layer, sleep, power-down)
- `claw-keyboard profile set` — configure profile parameters (use `--debounce`, `--tap`, `--sleep`, `--powerdown` flags)

## KLE layout tools

- `claw-keyboard kle info <file.json>` — show parsed KLE layout summary
- `claw-keyboard kle render <file.json>` — render KLE JSON layout to SVG

## Other

- `claw-keyboard reset` — factory reset keyboard. **Requires explicit user confirmation** — this permanently erases all settings, key mappings, and macros from the keyboard, restoring it to factory defaults. Only run when the user explicitly requests a factory reset.

## Safety

The following commands modify keyboard hardware state and should only be run with explicit user confirmation. Never run these autonomously:
- `reset` — factory reset (irreversible, erases everything)
- `macro clear` / `macro set` — erases or replaces all macros
- `keymap set` / `keymap write` — changes key bindings
- `rgb save` — writes to flash (limited write cycles)

Read-only commands (`discover`, `info`, `rgb status`, `keymap read`, `macro list`, `profile get`, `kle info`) are always safe to run.

## Notes

- The tool auto-discovers keyboards by scanning for HID interfaces with UsagePage `0xFF60` and Usage `0x61`, then verifying via a challenge-response handshake.
- Not all keyboards expose the vendor HID interface. If `discover` finds nothing, the keyboard may not support this protocol.
- On macOS, you may need to grant HID access permission to the terminal application in System Settings > Privacy & Security > Input Monitoring.
- On Linux, you may need udev rules to access USB HID devices without root. Create `/etc/udev/rules.d/99-claw-keyboard.rules` with `SUBSYSTEM=="hidraw", ATTRS{idVendor}=="1a86", MODE="0666"` and run `sudo udevadm control --reload-rules`.
- SHA256 checksums for all binaries are available in the `SHA256SUMS` file on the GitHub Releases page. Verify after downloading: `shasum -a 256 -c SHA256SUMS`.
- Use `--json` flag for machine-readable output.
