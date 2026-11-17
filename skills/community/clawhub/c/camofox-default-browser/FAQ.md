# Camoufox Default Browser — Frequently Asked Questions

> **Last updated:** 2026-07-30
> **Scope:** Common questions from operators using Camoufox in OpenClaw. For deeper detail, see `SKILL.md`, `CONFIGURATION.md`, `SECURITY.md`, `TROUBLESHOOTING.md`, and `EXAMPLES.md`.

---

## General Questions

### What is Camoufox?

Camoufox is a Firefox fork purpose-built for anti-detection browser automation. It spoofs browser fingerprints (User-Agent, WebGL renderer, AudioContext, screen geometry, WebRTC stack, hardware concurrency) at the C++ level — before JavaScript even executes. This makes it harder for websites to flag automated traffic compared to standard Chromium-based browsers or stealth plugins. See [SKILL.md](./SKILL.md) for the full overview.

### How does it differ from standard browser automation?

Standard tools like Playwright's built-in Chromium expose telltale signals: `navigator.webdriver = true`, consistent WebGL renderer strings, and predictable JS environments. Stealth plugins try to hide those signals *after* they're exposed. Camoufox, by contrast, ships with fingerprint spoofing baked into the engine itself, so the browser presents a natural-looking identity from the moment it loads. The trade-off is you lose some of Playwright's broader ecosystem; Camoufox provides its own tooling (`camofox_*` tools) for navigation, interaction, and snapshot capture instead.

### Is it legal to use?

Yes — Camoufox is a legitimate browser just like any other. Legality depends entirely on **how** you use it. Automating access to services where you have explicit authorization is fine. Scraping data you're not entitled to, bypassing authentication mechanisms, or violating a site's Terms of Service may violate laws such as the CFAA (US), GDPR (EU), or UU ITE Art. 30 (Indonesia). Always review the target platform's ToS before automating. See [SECURITY.md — Authorized Use Only](./SECURITY.md#2-authorized-use-only) for details.

### What sites does it work with?

Camoufox excels against sites known for aggressive bot detection: Google Search, LinkedIn, Amazon, X/Twitter, Instagram, TikTok, YouTube, Reddit, Yelp, Spotify, Netflix, and Twitch. All of these are supported via search macros (`@google_search`, `@linkedin_search`, etc.) documented in [SKILL.md](./SKILL.md#available-tools). Sites without WAFs or JS-heavy rendering are trivially handled. If a site still blocks you, that's covered below in "What if I get blocked anyway?"

---

## Technical Questions

### Why use Camoufox over Playwright stealth plugins?

Stealth plugins (e.g., `puppeteer-extra-plugin-stealth`) patch values *after* the browser has already been identified. They can be fingerprinted themselves. Camoufox manages identities at the native level — no patches needed post-launch. In practice this means fewer detection triggers on login walls, reCAPTCHAs, and behavioral checks. That said, Playwright still wins for headless reliability on simple pages, deep DOM inspection, and rich CI workflows. See [SKILL.md — Reason](./SKILL.md#reason) for a side-by-side comparison.

### How does fingerprint spoofing work?

When Camoufox launches, it generates randomized but internally consistent values for every identifiable field: canvas hash, audio context, language headers, timezone, screen resolution, and GPU renderer string. These values are coherent — meaning a user reported as having a 15-inch MacBook would also show macOS Chrome UA and matching device pixel ratio. The randomization happens in compiled C++ code that runs before any web content loads, so there's nothing for scripts to catch mid-execution. Configuration details are in [CONFIGURATION.md](./CONFIGURATION.md).

### Can I use it with existing Playwright scripts?

Not directly. Camoufox speaks its own HTTP API (default port 9377) rather than exposing a WebDriver/CDP endpoint. You'll need to rewrite interactions to use `camofox_navigate`, `camofox_snapshot`, `camofox_click`, `camofox_type`, and `camofox_evaluate` instead of Playwright's page object model. However, the overall pattern stays the same: navigate → inspect → interact → cleanup. Working examples are available in [EXAMPLES.md](./EXAMPLES.md).

### What happens when the browser crashes?

Camoufox runs as a separate server process. If the browser tab dies, subsequent commands on that tab will error out. The fix is to close the stale tab, create a fresh one, and resume. Idle browsers shut down after a configurable timeout (default 5 minutes) to save memory (~200 MB active, ~40 MB idle). Crash telemetry — anonymized stack traces sent upstream — is optional and can be disabled with `CAMOUFOX_CRASH_REPORT_ENABLED=false`. Log files for debugging are listed in [TROUBLESHOOTING.md — Getting Help](./TROUBLESHOOTING.md#getting-help).

---

## Usage Questions

### How do I import cookies?

Use the `camofox_import_cookies` tool. Pass a Netscape-format cookie file path and optionally filter by domain suffix:

```
camofox_import_cookies(cookiesPath="/path/to/cookies.txt", domainSuffix=".linkedin.com")
```

The file must follow the Netscape format (one cookie per line with `.domain .flag .path .secure .expiration .name .value`). Cookie permissions should be `600` only. See [SECURITY.md — Cookie Security](./SECURITY.md#1-cookie-security) and [TROUBLESHOOTING.md — Cookie import fails](./TROUBLESHOOTING.md#4-cookie-import-fails) for validation tips. Note: importing cookies grants full account access — treat them like passwords.

### Can I run multiple tabs?

Yes. Each `camofox_create_tab()` call returns a unique `tabId` that you use for all subsequent operations on that tab. Memory scales roughly +50 MB per additional tab. Manage tabs explicitly: always call `camofox_close_tab(tabId)` when finished, and verify state with `camofox_list_tabs()`. Leaving orphaned tabs consumes memory unnecessarily. See [TROUBLESHOOTING.md — Tabs not closing](./TROUBLESHOOTING.md#5-tabs-not-closing).

### How do I handle CAPTCHAs?

Camoufox doesn't solve CAPTCHAs automatically. If a challenge appears, your options are:

1. **Avoid triggering them** — pace requests naturally, use real session cookies (not raw credential logins), and don't hammer endpoints.
2. **Manual intervention** — pause automation, let a human complete the CAPTCHA, then resume.
3. **Third-party solver services** — integrate an external CAPTCHA-solving API if your workflow requires it (out of scope for Camoufox itself).

If you find yourself hitting CAPTCHAs frequently, check your request rate and fingerprint quality. See [TROUBLESHOOTING.md — Connection Timeouts](./TROUBLESHOOTING.md#connection-timeouts) for pacing guidance.

### What if I get blocked anyway?

First, verify it's actually a block vs. a slow-rendering page (take a `snapshot` or `screenshot` to confirm). Common causes and fixes:

| Cause | Fix |
|-------|-----|
| Request rate too high | Slow down between actions; add random delays |
| Expired/fresh cookies | Regenerate cookies; use `domainSuffix` for selective import |
| New fingerprint detected | Clear cache, launch fresh browser instance |
| IP reputation | Switch network or rotate IPs if available |
| Target site policy change | Review current ToS — may need alternative approach |

For persistent issues, enable verbose logging (`CAMOUFOX_LOG_LEVEL=verbose`) and share diagnostic output with the maintainers. See [TROUBLESHOOTING.md — Debug Mode](./TROUBLESHOOTING.md#debug-mode).

---

## Security Questions

### Are my cookies safe?

Cookies are stored as bearer tokens — whoever reads the file controls the account. Protect them by:

- Keeping file permissions at `600` (owner read/write only)
- Never committing cookie files to git (add `*.cookies`, `*cookies.txt` to `.gitignore`)
- Using dedicated files per account, never mixing sessions
- Deleting cookies immediately when access is no longer needed
- Restricting server binding to `127.0.0.1` with firewall rules

See [SECURITY.md — Cookie Security](./SECURITY.md#1-cookie-security) for the full checklist and incident response procedures.

### Does it collect my browsing data?

Under normal operation, **no**. Camoufox processes everything locally in the browser engine. The following are **NOT** collected: page content, cookies/values, personal messages, IP addresses, form inputs, or screenshots unless explicitly captured.

If crash telemetry is enabled (default: `true`), anonymized metadata may include User-Agent strings, viewport sizes, timestamps, and error stack traces. Nothing personally identifiable. Disable with `CAMOUFOX_CRASH_REPORT_ENABLED=false`. See [SKILL.md — Resource Management](./SKILL.md#resource-management) and [SECURITY.md — Data Protection](./SECURITY.md#3-data-protection).

### Can sites detect I'm using Camoufox?

In general, no — that's the entire point. Fingerprint spoofing at the C++ level means the browser presents as an ordinary Firefox installation with randomized but coherent attributes. Detection risk is significantly lower than standard stealth plugins. However, no solution is perfect: behavioral analysis (mouse movements, click timing, typing speed) can still raise flags on sophisticated platforms. Combine Camoufox with realistic pacing and proper session management for best results.

### How do I opt out of telemetry?

Set the environment variable before starting the gateway:

```bash
export CAMOUFOX_CRASH_REPORT_ENABLED=false
openclaw gateway restart
```

You can also verify what, if anything, is being transmitted by monitoring network connections during test runs:

```bash
ss -tulnp | grep 9377
```

Full opt-out guidance is in [SECURITY.md — Opt-Out Procedures](./SECURITY.md#3-opt-out-procedures).

---

## Troubleshooting Questions

### Why is installation failing?

Most failures fall into three buckets:

1. **Missing binary** — `CAMOUFOX_EXECUTABLE` isn't set or points to a non-existent file. Verify with `ls -la "$CAMOUFOX_EXECUTABLE"`.
2. **Missing system libraries** — GTK, X11, ATK bridge, etc. Install all dependencies listed under [SKILL.md — System Dependencies](./SKILL.md#system-dependencies-linux-debian-based). On Docker containers, install `xvfb` and set `DISPLAY=:99`.
3. **Port conflict** — Port 9377 already occupied. Check with `lsof -i :9377` and kill the conflicting process.

For step-by-step fix instructions, see [TROUBLESHOOTING.md](./TROUBLESHOOTING.md).

### How do I update Camoufox?

Updates happen through the package manager — whatever installed Camoufox originally handles updates:

```bash
npm update -g @jo-inc/camofox   # if installed globally via npm
# or reinstall from source:
rm -rf /root/.cache/camoufox/*
npm install -g @jo-inc/camofox
openclaw gateway restart
```

After updating, restart the OpenClaw Gateway so the new binary takes effect. The server version is tracked in [SKILL.md](./SKILL.md#dependencies--system-requirements) alongside the current version number.

### Where are the logs?

Log locations depend on what you're looking for:

| Purpose | Path |
|---------|------|
| General operation | `~/.openclaw/workspace/log/camofox*.log` |
| Crash dumps | `~/.local/share/camofox/logs/crash.log` |
| Browser cache | `/root/.cache/camofox/` |
| Gateway journal | `journalctl -u openclaw-gateway --since "1 hour ago"` |
| Socket file | `/tmp/camofox-server.sock` |

To increase verbosity, set `CAMOUFOX_LOG_LEVEL=verbose` and restart. See [TROUBLESHOOTING.md — Debug Mode](./TROUBLESHOOTING.md#debug-mode).

### How do I get help?

Steps, in order of preference:

1. **Check existing docs first** — SKILL.md, CONFIGURATION.md, SECURITY.md, TROUBLESHOOTING.md, EXAMPLES.md
2. **Run diagnostics** — the five commands in [TROUBLESHOOTING.md — Diagnostic Commands](./TROUBLESHOOTING.md#diagnostic-commands)
3. **Check health endpoint** — `curl http://localhost:9377/health`
4. **Enable verbose logging** — `CAMOUFOX_LOG_LEVEL=verbose` for full trace output
5. **Search GitHub issues** — https://github.com/jo-inc/camofox-browser/issues
6. **Ask the team** — Share diagnostic output, steps to reproduce, and platform details

Always include: Camoufox version, OS/distro, dependency list, log excerpts, and exact command that failed.

---

## Quick Reference

| Topic | Go here |
|-------|---------|
| Overview & tool list | [SKILL.md](./SKILL.md) |
| Environment variables & setup | [CONFIGURATION.md](./CONFIGURATION.md) |
| Cookie security & compliance | [SECURITY.md](./SECURITY.md) |
| Error fixes & debug steps | [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) |
| Code examples & patterns | [EXAMPLES.md](./EXAMPLES.md) |
| Installation guide | [INSTALL.md](./INSTALL.md) |
