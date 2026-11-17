---
name: camofox-default-browser
description: Advanced browser automation via Camoufox Firefox fork — handles anti-bot protection for authorized automation tasks
version: 1.2.0
user-invocable: true
homepage: "https://github.com/jo-inc/camofox-browser"
metadata:
  openclaw:
    requires:
      bins: ["node"]
    primaryEnv: CAMOUFOX_EXECUTABLE
---

# Camofox Default Browser

Use Camoufox browser (Firefox fork with advanced fingerprint management) as OpenClaw's browser automation engine. The `camofox_*` tools handle anti-bot protection that standard Chromium/Playwright automation may trigger, enabling reliable automation for authorized tasks.

## When to Use

- **Use `camofox_*` when the built-in `browser` tool encounters blocking** — for external public websites with anti-bot protection
- The built-in `browser` tool (Playwright/Chromium) may be detected by Google, LinkedIn, Amazon, Cloudflare, and most WAFs. Camoufox manages fingerprints at the C++ implementation level, reducing detection risk.

## Reason
Camoufox manages browser fingerprints at the C++ implementation level: navigator.hardwareConcurrency, WebGL renderer, AudioContext, screen geometry, WebRTC — all handled before JavaScript evaluation. This provides more reliable automation compared to standard stealth plugins that can themselves be fingerprinted.

## Available Tools

| Tool | Purpose |
|------|---------|
| camofox_create_tab | Open a new anti-detection browser tab with isolated context |
| camofox_snapshot | Accessibility tree snapshot (~90% smaller than raw HTML) with stable element refs (e1, e2, e3) plus optional base64 screenshot |
| camofox_click | Click element by ref (e.g. "e3") or CSS selector |
| camofox_type | Type text into form field. Set pressEnter=true to submit |
| camofox_navigate | Navigate to URL or use search macro: @google_search, @youtube_search, @amazon_search, @reddit_search, @linkedin_search, @wikipedia_search, @twitter_search, @yelp_search, @spotify_search, @instagram_search, @tiktok_search, @twitch_search, @netflix_search |
| camofox_scroll | Scroll page up/down by pixel amount |
| camofox_screenshot | Capture screenshot of current page |
| camofox_close_tab | Close tab to free resources |
| camofox_evaluate | Execute JavaScript in page context |
| camofox_list_tabs | List all open tabs |
| camofox_import_cookies | Import Netscape cookie file for authenticated browsing (requires CAMOFOX_API_KEY) |

## Workflow

1. `camofox_create_tab(url="https://example.com")` → tabId
2. `camofox_snapshot(tabId="<id>")` → accessibility tree
3. `camofox_click/type(tabId="<id>", ref="e3")` → interact
4. `camofox_close_tab(tabId="<id>")` → cleanup

## Resource Management

- Server auto-starts with OpenClaw Gateway (default port 9377)
- Browser engine launches lazily on first tab request
- Idle browser shuts down after configurable timeout (default 5 min)
- ~40MB memory when idle, ~200MB with active browser session
- Session isolation: separate cookies/storage per user
- Health endpoint: GET http://localhost:9377/health
- Crash telemetry: anonymized (no page content, cookies, IPs). Opt out via CAMOFOX_CRASH_REPORT_ENABLED=false

## ⚠️ Security & Usage Guidelines

- **Cookie Import**: Session cookies are bearer tokens that grant full account access. Treat imported cookie files as live credentials. Only import cookies you own or have explicit authorization to use.
- **Authorized Use Only**: This tool is designed for legitimate automation tasks where you have permission to access the target service. Do not use to circumvent access controls on sites where you lack authorization.
- **Legal Compliance**: Ensure your automation complies with target site Terms of Service, applicable laws, and regulations. Unauthorized scraping or access may violate computer fraud laws.
- **Privacy**: Do not automate access to accounts or data you do not own or have explicit permission to access.
- **Risk Awareness**: Imported session cookies may bypass normal login safeguards. Mishandling can lead to unauthorized account actions or session hijacking.

## Dependencies & System Requirements

### System Dependencies (Linux / Debian-based)

The following packages are required for Camoufox to render pages correctly, handle UI elements, and operate in both headful and headless environments.

| Package | Purpose |
|---------|---------|
| `libgtk-3-0` | GTK+ 3 toolkit — handles window management, widgets, and UI rendering. Required for all GUI operations including snapshot screenshot capture. |
| `libgdk-pixbuf2.0-0` | Image loading library — supports PNG, JPEG, WebP, and SVG rendering for page images, favicons, and CSS background assets. |
| `libdbus-glib-1-2` | D-Bus GLib bindings — enables IPC communication between browser processes, desktop integration, and system service discovery (e.g., notification daemon). |
| `libxt6` | X11 Toolkit library — legacy X11 client support needed by certain embedded XPCOM components and older extensions. |
| `libxcomposite1` | X Composite Extension — compositing manager support required for GPU-accelerated layer composition and correct rendering of overlaid elements. |
| `libxdamage1` | X Damage Tracking Extension — notifies compositor of painted regions for incremental redraws; critical for correct snapshot captures on accelerated surfaces. |
| `libxfixes3` | X11 Extension Fixes — provides cursor shape, region, and atom operations needed by WebGL canvas and pointer events. |
| `libxrandr2` | X Resize and Rotate — monitors display mode changes (DPI scaling, rotation, multi-monitor hotplug); required for responsive layout rendering. |
| `libatk-bridge2.0-0` | ATK Accessibility Bridge — translates accessibility tree data from Firefox's internal AT-SPI layer into format consumed by Playwright snapshots. Without this, accessibility tree output is incomplete or empty. |
| `libdrm2` | Direct Rendering Manager — DRM/KMS interface used by hardware video decode pipelines and OpenGL ES context creation on supported GPUs. |
| `libgbm1` | Graphics Buffer Manager — abstraction layer over DRM/GLES for buffer allocation; required for offscreen rendering, headless snapshots, and WebGPU compute fallbacks. |
| `xvfb` | X Virtual Framebuffer — provides a headless X11 server so Camoufox can run without physical display hardware. Essential for CI/CD, cron jobs, and containerized deployments. Start with `Xvfb :99 -screen 0 1920x1080x24` and set `DISPLAY=:99`. |

All libraries above are available via standard Debian/Ubuntu package repositories (`apt`). For Alpine Linux, equivalents exist but must be cross-compiled alongside Camoufox since pre-built binaries target glibc distributions.

### Node.js Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Version | Node.js 16 LTS | Node.js 20 LTS |
| npm | 8.x+ | 10.x+ |
| Architecture | x64 (amd64), arm64 | Same as Camoufox binary |
| Memory overhead | ~15 MB per worker process | — |

Camoufox is distributed as a **native C++ server** — there are no npm dependencies. The only JavaScript requirement is Node.js itself to bootstrap the OpenClaw tool integrations. Both global (`npm i -g`) and local installation paths work identically since the server communicates via HTTP localhost API.

### Browser Engine

| Aspect | Specification |
|--------|---------------|
| Base engine | Mozilla Firefox fork (ESR-aligned) |
| Binary path | Default: `/root/.cache/camoufox/camoufox` |
| Supported architectures | `linux-x64` (primary), `linux-arm64` (secondary) |
| Download URL | https://github.com/jo-inc/camofox/releases |
| Idle memory footprint | ~40 MB (browser process, no tabs) |
| Active memory footprint | ~200 MB (one tab loaded, JS evaluated) |
| Multi-tab scaling | +~50 MB per additional tab |
| Crash telemetry | Enabled by default (anonymized, no cookies/IPs). Disable via env var. |

The Camoufox binary is downloaded and cached automatically by the `camofox_*` tool runtime on first use. To force re-download, delete the cache directory before next session start.

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CAMOUFOX_EXECUTABLE` | **Yes** | — | Absolute path to the Camoufox binary. Must point to an executable file. Without this, the server cannot launch the browser engine. |
| `CAMOFOX_API_KEY` | No | — | API key for authenticated cookie import operations (`camofox_import_cookies`). Required when importing session cookies from Netscape-format files. |
| `CAMOFOX_CRASH_REPORT_ENABLED` | No | `true` | Toggle anonymized crash telemetry. Set to `false` to disable crash reports sent to the upstream collector. |
| `PORT` | No | `9377` | TCP port on which the Camoufox HTTP API server listens. The server binds to `0.0.0.0` by default. |
| `DISPLAY` | Conditional | `:0` | X11 display variable. Only required when running outside WSL/container where auto-detection fails. Set explicitly if headless mode doesn't activate. |
| `XDG_RUNTIME_DIR` | Conditional | — | XDG runtime directory for D-Bus socket discovery. Required in containerized environments (e.g., Docker, Kubernetes pods) where systemd isn't present. |

### Optional Dependencies

These packages are not strictly required for basic browsing automation but improve compatibility:

- **Font packages** (`fonts-liberation`, `fonts-noto-color-emoji`, `fonts-wqy-microhei`): Provide proper CJK, emoji, and Western text rendering. Without fonts, PDF exports may show blank boxes and some websites fall back to generic monospace.
- **Shared MIME info** (`shared-mime-info`): Enables correct MIME-type detection for downloaded files (PDFs, images, archives).
- **Alsa / PulseAudio** (`libasound2`, `libpulse0`): Audio playback support needed for sites with embedded video/audio that attempt to initialize audio contexts.
- **Video codecs** (`libavcodec-extra`, `libavformat-extra`): H.264/AAC decoding for HTML5 video players. Firefox ships with open formats (VP8/VP9, Ogg Vorbis) by default; proprietary codecs require additional packages.
- **Cups** (`cups-client`, `libcupsys2`): Print-to-PDF functionality. Required if automation involves printing web pages.

---

## Dependencies

```bash
# System (Linux)
apt-get install -y libgtk-3-0 libgdk-pixbuf2.0-0 libdbus-glib-1-2 \
  libxt6 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
  libatk-bridge2.0-0 libdrm2 libgbm1 xvfb

# Environment
export CAMOUFOX_EXECUTABLE=/root/.cache/camoufox/camoufox
```
