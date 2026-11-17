# Desktop Pilot — computer use for OpenClaw (Windows · macOS · Linux · WSL)

Let your OpenClaw agent **see and drive your desktop**: screenshots, window list, **click buttons by name**, close/focus apps, type Unicode text, key combos and coordinate clicks.

- 🎯 **Click by name, not by pixels** — uses the OS accessibility layer (UI Automation, macOS Accessibility, AT-SPI), so it survives moved windows, DPI scaling and themes.
- 🪟 **Works from WSL2** — the common "OpenClaw Gateway in WSL, apps on Windows" setup just works.
- 📦 **Zero installs on Windows and macOS** — only built-in PowerShell / JXA.
- ⌨️ **Layout-proof typing** — Unicode input on Windows (ñ, €, 漢字, emoji) regardless of keyboard layout.
- 🛡️ **Never types blind (Windows)** — the target window is brought to the foreground and verified before any keystroke; otherwise it aborts with `FOCUS_FAILED`.
- ✨ **"Agent is working" overlay** — glow around the screen + status pill with a **Stop** button (Windows/WSL, and an in-page version for browser automation), optional input lock for short supervised bursts.
- 🔁 **One CLI, same flags on every OS.**

```bash
clawhub install desktop-pilot
```

```bash
scripts/desktop.sh screenshot --out /tmp/screen.png
scripts/desktop.sh buttons --process notepad
scripts/desktop.sh click --process notepad --name "Save"
scripts/desktop.sh type --process notepad --text "Hello from OpenClaw"
scripts/desktop.sh key --keys ctrl+s
scripts/desktop.sh overlay start --text "Filling the form..."   # Windows/WSL; overlay stop when done
```

See `SKILL.md` for the full workflow, platform notes and safety rules. MIT licensed.
