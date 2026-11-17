# camoufox-browse

OpenClaw skill: OpenClaw skill for getting past bot-detection that breaks the normal browser — Cloudflare, Datadome, fingerprint bans. Drives [Camoufox](https://camoufox.com), a real anti-fingerprinting Firefox, for authorized access to sites that flag standard automation.

> ⚠️ **Use responsibly.** This tool reduces bot-detection signals. Only use it where automated access is permitted by the site's terms and applicable law. It is not for evading bans, bypassing access controls, or impersonating users. You are responsible for compliance.

> **Full usage docs live in [`SKILL.md`](./SKILL.md).** This README covers install, local development, and publishing.

## What it's for

Use Camoufox when the built-in browser gets blocked or fingerprinted and you're authorized to automate the site. Typical asks:

- "Open a Cloudflare-protected site the built-in browser can't get past and extract the listing data."
- "Keep a stable logged-in session across runs on a site that fingerprint-bans automation."
- "Log into my own account on a site that flags standard tooling and pull my data."

For anything a normal browser handles, use the built-in tool — this is for the hard, protected cases. Automated access must be permitted by the site's terms; that call is the human's, not the skill's.


## Install (end users)

```bash
openclaw skills install camoufox-browse
```

Then install one runtime. **Node is recommended:**

```bash
# Node (preferred) — pin playwright@1.60.0 (1.61+ breaks newPage() on camoufox)
npm install playwright@1.60.0 camoufox-js
```

```bash
# Python (fallback) — same pin
python3 -m pip install "camoufox[geoip]" playwright==1.60.0
python3 -m camoufox fetch
```

Then ask your agent to open a URL on a fingerprint-sensitive target you're authorized to access. When logging in or handling data, follow the "Operational Safety" guidance in [`SKILL.md`](./SKILL.md): use disposable profiles, never reuse personal/production credentials, keep secrets in env/proxy config, and get human sign-off before any irreversible action.

## Headless vs headed

- Default: **headless** (`headless=true`). Works on servers, CI, anywhere.
- For a visible window: set `headless=false`. Requires an X11/Wayland display server.

## Local development

```bash
# Preview the skill as the agent sees it
openclaw skills list
openclaw skills verify camoufox-browse

# Run SKILL.md through the agent
openclaw agent --message "browse https://example.com and tell me the title"
```

## Publishing

This skill is published to ClawHub under the owner of whoever runs `clawhub login`. See `PUBLISH.md` for the full flow.

## License

MIT-0 (MIT No Attribution) — see [`LICENSE`](./LICENSE). This covers the skill's own docs and examples only. Camoufox itself is a separate MPL-2.0 project installed from PyPI and is not redistributed here.