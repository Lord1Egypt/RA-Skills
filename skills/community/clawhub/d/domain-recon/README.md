# domain-recon 🛰️

Passive domain/infra OSINT as an [OpenClaw](https://openclaw.ai) skill — one
standard-library-only Python CLI wrapping **five keyless public APIs** (no keys,
no accounts, no secrets). Everything is *passive*: it only queries public
third-party databases and never connects to or probes the target host directly.

| Subcommand | Source | What it does |
|------------|--------|--------------|
| `certs`   | crt.sh (Certificate Transparency) | Subdomain enumeration + certificate history |
| `rdap`    | rdap.org | Modern WHOIS for a domain, IP, or ASN (auto-detected) |
| `dns`     | Google / Cloudflare DoH | Resolve A/AAAA/MX/TXT/NS/CNAME/SOA/CAA/PTR |
| `ip`      | ip-api.com | IP → geo, ISP, ASN, proxy/hosting flags |
| `asn`     | RIPEstat Data API | ASN → holder + prefixes; IP → owning ASN + prefix |
| `wayback` | archive.org | Snapshot availability + CDX capture history |
| `profile` | all of the above | One-shot orchestration into a single merged report |

## Quick start

```bash
python3 scripts/recon.py certs example.com --human
python3 scripts/recon.py profile example.com --human
```

JSON by default; add `--human` for a compact readable summary. See
[`SKILL.md`](SKILL.md) for the full agent-facing docs,
[`references/API_NOTES.md`](references/API_NOTES.md) for endpoint details and the
"Rate limits & gotchas" cheat-sheet, and
[`references/CHANGELOG.md`](references/CHANGELOG.md) for notable decisions.

## Tests

Offline, deterministic pytest suite (HTTP mocked — no network):

```bash
python3 -m pip install pytest
python3 -m pytest scripts/tests/test_recon.py -q
```

Opt-in live smoke test (hits real endpoints to catch upstream schema drift):

```bash
RECON_LIVE=1 python3 -m pytest scripts/tests/test_live_smoke.py -q
```

## License

[MIT](LICENSE).
