# Desktop Pilot — computer use for OpenClaw (Windows · macOS · Linux · WSL)

Let your OpenClaw agent **see and drive your desktop**: screenshots, window list, **click buttons by name**, close/focus apps, type Unicode text, key combos and coordinate clicks.

- 🎯 **Click by name, not by pixels** — uses the OS accessibility layer (UI Automation, macOS Accessibility, AT-SPI), so it survives moved windows, DPI scaling and themes.
- 🪟 **Works from WSL2** — the common "OpenClaw Gateway in WSL, apps on Windows" setup just works.
- 📦 **Built-in desktop backends** — PowerShell / JXA. The CLI requires Bash 4+ (Git Bash on native Windows; modern Bash on macOS).
- ⌨️ **Layout-proof typing** — Unicode input on Windows (ñ, €, 漢字, emoji) regardless of keyboard layout.
- 🛡️ **Targeted input (Windows)** — when a target is supplied, focus is checked before input; failure aborts with `FOCUS_FAILED`. This does not eliminate focus races.
- ✨ **"Agent is working" overlay** — glow around the screen + status pill with a **Stop** button (Windows/WSL), with optional physical input blocking for short supervised bursts. The separate browser overlay is informational only; use trusted host cancellation, never page state.
- 🔁 **One CLI, same flags on every OS.**

```bash
clawhub install desktop-pilot
```

```bash
scripts/desktop.sh screenshot --out /tmp/screen.png
scripts/desktop.sh buttons --process notepad
scripts/desktop.sh click --process notepad --name "Save"
scripts/desktop.sh type --process notepad --text "Hello from OpenClaw"
scripts/desktop.sh key --process notepad --keys ctrl+s
scripts/desktop.sh overlay start --text "Filling the form..."   # Windows/WSL; overlay stop when done
```

See `SKILL.md` for the full workflow, platform notes and safety rules. MIT-0 licensed.

## 1.0.2 migration
Native Stop persists through overlay restarts; only explicit, user-authorized `overlay clear` resumes. Native PowerShell entry points also check Stop. Browser `stopped()` and `clear()` were removed: pages cannot safely own agent cancellation. Use the host's cancellation control outside the webpage.

No network transport or dependency download is required by the runtime scripts. Input lock is opt-in, system-wide physical keyboard/mouse suppression on Windows; it is not key recording. Timeouts and emergency release are documented in SKILL.md. Test only on a supervised scratch window before relying on an unfamiliar platform.
