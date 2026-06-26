# Security & Safety (Publishing Skills)

This skill package is designed to help publish content to a public registry. Treat publishing as **data exfiltration** risk unless confirmed otherwise.

## Never Publish

- `.env` and any file containing secrets
- API keys, passwords, tokens, session cookies
- private keys (`id_rsa`, `*.pem`, `*.pfx`)
- cloud credentials (AWS/GCP/Azure)
- internal-only URLs, hostnames, IPs, or infrastructure details
- customer data, logs, datasets, or any proprietary artifacts you are not authorized to share

## Recommended Hygiene

- Keep skill folders minimal: `SKILL.md`, `reference/`, small `scripts/`, small `assets/`
- Prefer **text assets** (Markdown, SVG) over large binaries
- Before publish/sync, manually review the folder tree for accidental inclusions

## Preflight Checklist

Before `clawhub publish` or `clawhub sync`:

- confirm login status (`clawhub login`)
- confirm slug + version + tags
- run a dry-run if supported (check `clawhub sync --help`)
- verify the folder contains no secrets

