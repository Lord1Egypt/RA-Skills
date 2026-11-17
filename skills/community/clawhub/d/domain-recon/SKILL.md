---
name: domain-recon
description: Passive domain/infra OSINT over five keyless public APIs — subdomains, RDAP/WHOIS, DNS-over-HTTPS, IP geo/ISP, and ASN/prefix ownership.
metadata: {"openclaw": {"requires": {"bins": ["python3"]}, "emoji": "🛰️"}, "homepage": "https://github.com/maggiedev-bot/domain-recon", "version": "0.6.0"}
---

# domain-recon

Passive reconnaissance for a domain, IP, or ASN using **five keyless public
APIs** — no API keys, no accounts, no secrets. Everything is *passive*: the skill
only queries public third-party databases; it never connects to or probes the
target host directly.

Use this when the user wants to investigate a domain or IP's public footprint:
enumerate subdomains, look up WHOIS/RDAP registration, resolve DNS records, geo-
locate an IP, or identify which network/ASN owns an address.

All work runs through one Python helper (standard library only — no `pip install`):

```bash
python3 {baseDir}/scripts/recon.py <subcommand> <target> [options]
```

Output is JSON by default (easy to parse and chain); add `--human` for a compact
readable summary.

## Subcommands

| Subcommand | Source | What it does |
|------------|--------|--------------|
| `certs <domain>`   | crt.sh + certSpotter (Certificate Transparency) | Enumerate subdomains + certificate history; falls back to certSpotter when crt.sh is down |
| `rdap <resource>`  | IANA bootstrap + supplement → authoritative server (rdap.org fallback) | Modern WHOIS for a domain, IP, or ASN (auto-detected); resolves ccTLDs like `.ai` (bootstrap) and `.io`/`.sh`/`.ac`/`.us` (supplement) that rdap.org 404s |
| `dns <name>`       | Google / Cloudflare DoH | Resolve DNS records (A, AAAA, MX, TXT, NS, CNAME, SOA, CAA) |
| `ip <ip>`          | ip-api.com | IP → geo, ISP, ASN, and proxy/hosting flags |
| `asn <resource>`   | RIPEstat Data API | ASN → holder + announced prefixes; IP → owning ASN + prefix |
| `wayback <url>`    | archive.org | Wayback snapshot availability + CDX capture history |
| `profile <domain>` | all of the above | One-shot orchestration: certs → dns → ip → asn → wayback into a single report |

### Common options

- `--human` — readable text instead of JSON.
- `--timeout <sec>` — per-request timeout (default 20).
- `--retries <n>` — retry attempts on 429/5xx/network errors (default 3).
- `certs --no-wildcards` — drop `*.` wildcard subdomains.
- `dns --type A,MX,TXT` — comma-separated record types in one call.
- `dns --provider cloudflare` — use Cloudflare DoH instead of Google (default).
- `rdap --kind domain|ip|asn` — force the resource kind instead of auto-detecting.
- `asn --no-prefixes` — skip the announced-prefixes list for a faster ASN lookup.
- `certs --limit <n>` / `certs --max-certs <n>` — cap the returned subdomains / cert-history rows (full counts still reported).
- `certs --all-ct` — query **both** CT sources (crt.sh + certSpotter) and merge, instead of stopping at the first that answers (wider coverage).
- `rdap --no-bootstrap` — skip the IANA bootstrap and query rdap.org directly (domains only).
- `wayback --no-cdx` — availability only; `wayback --cdx-limit <n>` — number of recent captures to list.
- `profile --cert-limit <n>` / `--resolve-limit <n>` / `--ip-limit <n>` — bound how much of each stage the orchestrator pulls; `--no-wayback` to skip the archive step.

## Example invocations

```bash
# Subdomains + cert history for a domain
python3 {baseDir}/scripts/recon.py certs example.com --human

# WHOIS/RDAP (auto-detects domain vs IP vs ASN)
python3 {baseDir}/scripts/recon.py rdap example.com
python3 {baseDir}/scripts/recon.py rdap 8.8.8.8
python3 {baseDir}/scripts/recon.py rdap AS15169

# DNS records — several types at once, via Cloudflare
python3 {baseDir}/scripts/recon.py dns example.com --type A,AAAA,MX,TXT --provider cloudflare

# IP geolocation / ISP / hosting flags
python3 {baseDir}/scripts/recon.py ip 8.8.8.8 --human

# Who owns this network? (ASN or IP)
python3 {baseDir}/scripts/recon.py asn AS15169
python3 {baseDir}/scripts/recon.py asn 8.8.8.8

# Is it archived? (availability + recent capture history)
python3 {baseDir}/scripts/recon.py wayback example.com

# One-shot: profile a domain across every source in a single report
python3 {baseDir}/scripts/recon.py profile example.com --human
```

A typical "profile this domain" flow: run `certs` for subdomains, `rdap` for
registration, `dns` for the live records, then `ip` + `asn` on the resolved
address to see who hosts it. The `profile` subcommand chains exactly this
sequence for you (respecting ip-api's rate limit between enrichment calls) and
returns one merged JSON/`--human` report.

## Behavior & safety notes

- **Passive only.** No port scans, no direct connections to the target — just
  public database lookups.
- **Keyless.** No credentials are ever required, read, or transmitted.
- **No shell injection surface.** Inputs are validated (domains IDNA/punycode-
  encoded, IPs and ASNs parsed) and passed only as URL-encoded query parameters;
  the helper never invokes a shell.
- **Courteous.** Sends a descriptive User-Agent, uses per-request timeouts, and
  backs off with retries on `429`/`5xx` (honoring `Retry-After`). ip-api.com is
  rate-limited to 45 requests/minute — batch and space out calls.
- **Resilient to source outages.** `certs` falls back from crt.sh (which
  frequently hard-`502`s under load) to certSpotter so subdomain enumeration
  survives, recording which source answered in `sources_used`. `rdap` resolves
  the authoritative RDAP server via the **IANA bootstrap**, plus a small curated
  **supplement** for TLDs IANA omits but that still run RDAP (e.g. `.io`, which
  the rdap.org redirector `404`s), then falls back to rdap.org for anything else.
  The winning source is recorded in `rdap_source`.
- **Graceful degradation — `rdap` tells you when a TLD isn't supported.** `rdap`
  is the only TLD-variable query (dns/certs/ip/asn/wayback are TLD-agnostic).
  When a domain's TLD has no public RDAP server anywhere (absent from both the
  IANA bootstrap and the supplement — many ccTLDs are WHOIS-only), `rdap` returns
  a first-class **`{"supported": false, "rdap_source": "none", "reason": ...}`**
  result at exit `0`, *not* a 404 or an exception. A calling agent should check
  `supported` and skip RDAP for that domain while still using the other sources;
  inside `profile` this appears as a clean signal under `apex.rdap`, never in
  `errors[]`. Real answers carry `"supported": true`. See
  `docs/tld-rdap-coverage.md` for the full per-TLD map (which of the 1,438
  delegated TLDs are `bootstrap` / `supplement` / `none`), regenerable with
  `python3 {baseDir}/scripts/gen_coverage.py`.
- **Third state — `rdap` distinguishes "unreachable" from "unsupported".** A TLD
  can be *delegated in the IANA bootstrap yet unreachable from our egress*: the
  registry's authoritative RDAP server resets the connection / RSTs the TLS
  handshake / read-times-out (errno 104 class). This is neither a clean answer
  nor a real capability gap, so `rdap` emits a distinct
  **`{"supported": true, "rdap_source": "unreachable", "retryable": true, "reason": ...}`**
  result. The signal to a caller: *the data exists, we could not fetch it — skip
  the field but know it is retryable*, NOT "this TLD has no RDAP server". The
  trigger is deliberately narrow (connection reset / TLS RST / read timeout
  against a bootstrap- or supplement-listed endpoint); a `429`/ban or a genuine
  absence never lands here. Because the fetch did not succeed, this outcome
  carries its **own exit code `3`** (see Exit codes) rather than collapsing into
  `0`. Inside `profile` it appears as a clean `unreachable` signal under
  `apex.rdap`, never in `errors[]`.
- **Fourth state — `rdap` distinguishes "broken" from "unreachable".** A
  delegated endpoint can *respond, but with an unusable response*: an
  untrusted/self-signed TLS certificate that fails verification, or an HTTP
  error status (4xx / 5xx). This is neither a clean answer, a real capability
  gap, nor a transport reset, so `rdap` emits a distinct
  **`{"supported": true, "rdap_source": "broken", "cause": "<slug>", "http_status": <int|null>, "retryable": <bool>, "reason": ...}`**
  result. `cause` is `bad-cert` or `http-<status>` (e.g. `http-426`, `http-404`,
  `http-500`); `retryable` is `false` for a bad cert / 4xx (a persistent
  registry-side fault) and `true` for a 5xx (a server error a later attempt may
  clear). The signal to a caller: *the endpoint is faulty — skip the field;
  `retryable` says whether trying later helps.* recon does **not** disable TLS
  verification or fake a fetch — it only *labels* the fault honestly. The
  trigger is narrow and mutually-exclusive with `unreachable`: a `429`/ban, a
  DNS-resolution failure, a connection-refused, and a genuine absence never land
  here, and `broken` is only emitted after **both** the authoritative server and
  the rdap.org redirector are exhausted (so it never fires where the redirector
  could still rescue the lookup). Exit code is driven by `retryable` (see Exit
  codes). Inside `profile` it appears as a clean `broken` signal under
  `apex.rdap`, never in `errors[]`.
- **`profile` runtime is bounded, not instant.** A full profile fans out across
  ~6 sources and multiple hosts with courtesy rate-limit spacing, so a large
  domain (dozens of subdomains) takes roughly **1–1.5 min** — it is working, not
  hung. The slowest source, the Wayback CDX index (single lookups seen in the
  tens of seconds), runs on a deliberately tight budget (short timeout, no
  retry) so it can never dominate; a timed-out archive lookup is fault-isolated
  into `errors[]` like any other. Use `--no-wayback` or a lower `--ip-limit` to
  make a profile faster.
- **Exit codes (quint-state).** The code encodes the *actionable retryability
  tier*; the JSON `rdap_source` names the mechanism. A caller branching on exit
  status can tell "clean result" from "skip, retry later" from "skip, don't
  bother":
  - `0` — success: a real answer **or** a definitive `unsupported`/WHOIS-only TLD
    (a terminal, non-retryable capability gap, `rdap_source:"none"`).
  - `2` — a handled error (bad input, upstream failure, **429/ban**) with a
    message on stderr.
  - `3` — **retryable** RDAP failure: the endpoint is delegated (a server exists)
    but we could not get usable data this time and a later attempt may succeed —
    either `rdap_source:"unreachable"` (transport reset / TLS-RST / read timeout)
    or `rdap_source:"broken"` with a 5xx (`retryable:true`).
  - `4` — **non-retryable** endpoint fault: `rdap_source:"broken"` with an
    untrusted/self-signed TLS cert or an HTTP 4xx (`retryable:false`) — the
    server answered definitively; retrying will not help until the registry fixes
    it.
  Neither `3` nor `4` is folded into `0`: the field was not fetched, so the
  distinction (retry later vs. don't bother vs. clean) is preserved.

## For maintainers — running the tests

The parsing/normalization logic is covered by an offline, deterministic pytest
suite (fixtures in `scripts/tests/fixtures/`, HTTP mocked — no network):

```bash
python3 -m pip install pytest        # only dependency, tests-only
python3 -m pytest {baseDir}/scripts/tests/test_recon.py -q
```

An opt-in live smoke test verifies the real endpoints still match the expected
schema (never part of the normal gate):

```bash
RECON_LIVE=1 python3 -m pytest {baseDir}/scripts/tests/test_live_smoke.py -q
```

See `references/API_NOTES.md` for endpoint details and `references/CHANGELOG.md`
for notable decisions (including the BGPView → RIPEstat swap).
