# CleanApp Report Submission 0.3.0

Canonical onboarding: **https://www.cleanapp.io/agents**.

This client-side skill sends one approved observation to CleanApp's public intake and keeps a private receipt. It needs Python3 and outbound HTTPS; no account or CleanApp API key is required. A connected MCP client can instead use the server named on the onboarding page.

Create `approved-report.json` from a real observation, containing at least `description`. Then preview before sending:

```bash
python3 report.py --input approved-report.json --dry-run
python3 report.py --input approved-report.json --submit --receipt-file private-receipt.json
python3 report.py --status --receipt-file private-receipt.json
```

`--dry-run` makes no network calls. `--discover` reads the canonical page and its linked `agents.txt` without submitting. Submission saves a random UUIDv4 before its first request; exact retries use the same file/input with `--retry --submit`. A private receipt file contains a bearer tracking token and must not be posted, committed or placed in shared logs. The client prints no tracking token.

A report starts in private quarantine. Omitted handling preserves private publication and no notices. For explicitly approved automatic handling, add `"handling":{"publication":"automatic","notices":"automatic"}` to the report JSON before previewing; the same permissions are part of exact-retry identity. Backend privacy and eligibility checks can hold an action. The private receipt exposes recorded processing, decisions/reasons, public canonical links, cluster candidates, notice evidence and next action. Related observations retain independent evidence and attribution. Pending is not sent; final is not fixed. Neither publication nor delivery is guaranteed, and no financial reward is promised. See [SKILL.md](SKILL.md) and [API reference](references/API_REFERENCE.md).

## Upgrade from 0.1.x

The default package now targets public **single-report** intake; it no longer requires a Fetcher key or accepts the old bulk `items` envelope. `run.sh`, `ingest.py` and `scripts/submit_report.sh` route to this public client. Existing authenticated bulk integrations and `@cleanapp/cli` remain supported through the separate Wire API; migrate deliberately using the API reference rather than passing a token to this client.

Build an uploadable bundle with `./build_zip.sh`. Publishing is a separate release action; building the archive does not upload or post anything.

## 0.3.0 outcome support

This prospective source version adds explicit optional handling and full report-scoped outcome output. It does not change omission to automatic permission or upgrade older receipts. `--status --receipt-file ...` reads the same private receipt and displays only whitelisted decision/action fields, never tracking tokens or provider message bodies. Poll when needed while `outcome.final` is false; there is no background paid analysis loop in this client. Building this version does not publish it to ClawHub.
