---
name: agentor
description: Use agenTOR for Tor-routed browser sessions with receipts, HTML capture, screenshots, and compact research runs. It is suited for privacy-framed browsing work where agents should leave a local artifact trail.
---

# agenTOR

Use this skill when a task needs:

- a Tor-routed or proxy-routed browser session
- a local receipt for what the browser saw
- page HTML capture
- a viewport screenshot
- a quick research pass over a page with artifacts

## Commands

```bash
agentor doctor
agentor fetch <url>
agentor shot <url>
agentor screenshot <url>
agentor research <url> --prompt "research this page"
agentor run <url> --prompt "research this page"
agentor setup tor
agentor test tor
```

## Notes

- Default proxy is `socks5://127.0.0.1:9050`
- `agentor setup tor` checks install state and SOCKS reachability
- `agentor doctor` audits browser, Tor, port, and output directory
- Profiles can store recurring proxy/output defaults
- Pass `--no-proxy` for direct browsing
- Artifacts are written under `artifacts/<timestamp>-<slug>` unless `--out` is set
- every run also writes `summary.txt`
- `run` writes `report.md` in addition to HTML, text, screenshot, and `receipt.json`

## Verification

```bash
npm test
npm pack --json --dry-run
```

## Safety

- Tor routing improves path hygiene, not identity guarantees
- Avoid logged-in browser state if the goal is separation
- Keep the receipt directory; it is the proof of what happened
