---
name: browser-setup
description: "Install and configure headless Chrome for OpenClaw browser tool in environments without root/sudo access (cloud containers, VPS, sandboxed hosts). Use when: (1) browser tool fails with No supported browser found, (2) Chrome crashes with Page crashed or missing library errors, (3) setting up browser automation on a fresh server or container, (4) user asks to install or fix the browser for OpenClaw. NOT for macOS/Windows desktops with Chrome already installed, or Chrome extension relay setup."
---

# Browser Setup (No-Root Linux)

Install headless Google Chrome for OpenClaw's `browser` tool on Linux without root access.

## When to Use

- `browser start` fails with "No supported browser found"
- Chrome starts but pages crash ("Page crashed", "Target page closed")
- Running on a cloud container, VPS, or sandboxed environment without `sudo`

## Quick Start

```bash
bash scripts/install-browser.sh
```

The script downloads Chrome, extracts ~40 shared library packages, installs Liberation fonts, creates a wrapper script, and verifies the installation. Takes ~2 minutes.

Then configure OpenClaw:

```bash
openclaw config set browser.executablePath "$HOME/local-libs/chrome-wrapper.sh"
openclaw config set browser.headless true
openclaw config set browser.noSandbox true
openclaw config set browser.attachOnly true
```

Set the CDP port for the openclaw profile (edit `~/data/openclaw.json` or equivalent config):

```json
{
  "browser": {
    "executablePath": "~/local-libs/chrome-wrapper.sh",
    "headless": true,
    "noSandbox": true,
    "attachOnly": true,
    "profiles": {
      "openclaw": { "cdpPort": 18800, "color": "#FF4500" }
    }
  }
}
```

## Critical: attachOnly Must Be true

OpenClaw has two internal paths for browser operations:

- **CDP path** (start/stop/tabs): communicates directly with Chrome's CDP port
- **Playwright path** (navigate/snapshot/act): uses `playwright-core` bundled with OpenClaw

When `attachOnly: false`, Playwright calls `launchOpenClawChrome()` which checks `ensurePortAvailable(cdpPort)`. Since Chrome is already listening on that port, it throws `PortInUseError` on every navigate/snapshot/act call.

When `attachOnly: true`, Playwright uses `connectOverCDP()` to attach to the running Chrome instance. No port conflict.

**Always set `attachOnly: true` when using a wrapper script or manually-started Chrome.**

## Usage Flow

### Starting Chrome

Chrome must be started before OpenClaw can use it. Start it manually:

```bash
~/local-libs/chrome-wrapper.sh \
  --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage \
  --remote-debugging-port=18800 \
  --user-data-dir=~/data/browser/openclaw/user-data \
  --no-first-run --disable-setuid-sandbox \
  about:blank &
```

Or let OpenClaw start it (if `attachOnly: false` — but this causes PortInUseError on Playwright operations, so not recommended).

### Browser Tool Flow

```
browser start (profile=openclaw)   → detects running Chrome via CDP
browser navigate (targetUrl)       → Playwright connectOverCDP → loads page
browser snapshot                   → accessibility tree (structured page data)
browser screenshot                 → PNG capture
browser act (ref=e12, kind=click)  → interact via ref from snapshot
```

## Common Issues

### Missing Shared Libraries

**Symptom:** `error while loading shared libraries: libXXX.so: cannot open shared object file`

**Fix:** The install script handles this. If new libraries are missing after a Chrome update, check with:

```bash
LD_LIBRARY_PATH=~/local-libs/lib ldd ~/chrome-install/opt/google/chrome/chrome | grep "not found"
```

Then `apt-get download <package>`, extract with `dpkg-deb -x`, copy `.so` files to `~/local-libs/lib/`.

### Page Crashed

**Symptom:** `page.goto: Page crashed` or `Target page, context or browser has been closed`

**Cause:** Missing fonts. Chrome's renderer crashes when no fonts are available.

**Fix:** Install fonts (the script does this). Verify `~/.fonts/` has `.ttf` files and `~/.config/fontconfig/fonts.conf` exists. The wrapper script must export `FONTCONFIG_FILE`.

### PortInUseError

**Symptom:** `PortInUseError: Port 18800 is already in use`

**Cause:** `attachOnly` is `false` — Playwright tries to launch a new Chrome on the same port.

**Fix:** Set `browser.attachOnly: true` in OpenClaw config.

### CDP Timeout / Backlog

**Symptom:** `browser start` succeeds but subsequent calls timeout.

**Cause:** Failed Playwright connections accumulate in Chrome's TCP listen backlog (CLOSE-WAIT state), blocking new connections.

**Fix:** Kill Chrome (`pkill -9 -f chrome`), wait a few seconds, restart cleanly.

### Small /dev/shm

**Symptom:** Renderer crashes on complex pages in containers.

**Cause:** Default container `/dev/shm` is 64MB, too small for Chrome.

**Fix:** `--disable-dev-shm-usage` flag (included in the wrapper). For Docker, also add `--shm-size=256m` to the container.

## What the Install Script Does

1. Downloads Google Chrome stable `.deb` from Google
2. Extracts Chrome binary to `~/chrome-install/` using `dpkg-deb -x` (no root needed)
3. Identifies missing shared libraries via `ldd`
4. Downloads ~40 library `.deb` packages via `apt-get download` (no root needed)
5. Extracts all `.so` files to `~/local-libs/lib/`
6. Downloads `fonts-liberation` and installs `.ttf` files to `~/.fonts/`
7. Creates fontconfig config mapping sans-serif/serif/monospace → Liberation fonts
8. Creates `~/local-libs/chrome-wrapper.sh` that sets `LD_LIBRARY_PATH` + `FONTCONFIG_FILE`
9. Verifies Chrome can start and report its version

## Package List Reference

Libraries downloaded (Ubuntu/Debian names, may vary by distro):

libglib2.0, libnss3, libnspr4, libatk1.0, libatk-bridge2.0, libcups2, libdrm2,
libxkbcommon0, libxcomposite1, libxdamage1, libxfixes3, libxrandr2, libgbm1,
libasound2, libatspi2.0, libdbus-1-3, libxcb1, libx11-6, libxext6, libcairo2,
libpango-1.0, libpangocairo-1.0, libffi8, libpcre2-8-0, libxau6, libxdmcp6,
libxi6, libxrender1, libpng16-16, libfontconfig1, libfreetype6, libxcb-render0,
libxcb-shm0, libpixman-1-0, libfribidi0, libthai0, libharfbuzz0b,
libavahi-common3, libavahi-client3, libdatrie1, libgraphite2-3
