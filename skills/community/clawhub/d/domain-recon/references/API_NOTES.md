# API Notes — domain-recon sources

All sources below are **keyless** (no API key, no account, no auth header). Each
row lists the exact endpoint the helper calls and the fields it normalizes.

## crt.sh + certSpotter — Certificate Transparency (`certs`)
- **Primary — crt.sh:** `https://crt.sh/?q=%25.<domain>&output=json` (`%25` =
  URL-encoded `%`, the CT wildcard). Returns a JSON array of certificate rows.
  `name_value` is **newline-delimited** and may contain wildcard (`*.`) SANs; the
  helper splits, lowercases, strips trailing dots, keeps only names within the
  queried apex, and de-duplicates.
- **Fallback — certSpotter:** `https://api.certspotter.com/v1/issuances?domain=<d>&include_subdomains=true&expand=dns_names&expand=issuer`
  (keyless free tier). Returns a JSON array of issuances; names live in a
  `dns_names` list per issuance and the issuer is a nested object. Normalized
  onto the **same contract** as crt.sh so the two merge cleanly.
- **Fallback logic:** try crt.sh first; on `5xx`/`4xx`/timeout/bad-JSON, fall
  back to certSpotter. A `200` with an empty result set is a *valid answer*
  ("no certs logged") and does **not** trigger fallback — this distinguishes an
  empty CT log from an upstream outage. The result records `sources_used` (which
  answered) and `errors[]` (which failed) so it is always auditable. Only when
  *no* source can be reached does `certs` error out. `--all-ct` queries both and
  merges/dedups for wider coverage.
- Quirk: on **zero results** crt.sh returns an *empty body* (not `[]`) — handled.
- Quirk: crt.sh is frequently slow and can **hard-`502`/`503`** (a full outage,
  not just throttling) under load. The helper retries, then falls back to
  certSpotter; the live smoke test treats a 5xx as a skip, not a failure.

## RDAP / modern WHOIS (`rdap`) — IANA bootstrap + supplement + rdap.org
Domain lookups resolve the authoritative RDAP server in three tiers; the result
records which tier answered in `rdap_source`.
- **Tier 1 — IANA bootstrap (`iana-bootstrap`):** `https://data.iana.org/rdap/dns.json`
  maps each TLD → its authoritative RDAP base URL (~1200 TLDs). The helper
  resolves the TLD's server and queries `<base>/domain/<d>` directly. Fixes most
  ccTLDs / newer TLDs (e.g. `.ai`, `.dev`, `.xyz`, `.uk`). Fetched at most once
  per process (memoized).
- **Tier 2 — curated supplement (`supplement`):** a short static map for TLDs
  that IANA **omits** from the bootstrap yet still run a public RDAP server.
  **This is what fixes `.io`** — `.io` is genuinely absent from `dns.json` (as are
  `.co`, `.me`, `.us`), but Identity Digital serves its RDAP at
  `rdap.identitydigital.services`. Current entries (verified live 2026-07-26):
  `.io`/`.sh`/`.ac` → Identity Digital, `.us` → `rdap.nic.us`. The supplement
  applies even if the bootstrap fetch itself fails.
- **Tier 3 — rdap.org fallback (`rdap.org`):** `https://rdap.org/domain/<d>`,
  `/ip/<ip>`, `/autnum/<asn>`. A **redirector** — it 3xx-redirects to the
  authoritative RDAP server (Verisign, ARIN, RIPE, …); `urllib` follows redirects
  automatically. Used for domains whose TLD is in neither tier 1 nor tier 2, when
  the authoritative server fails, or with `--no-bootstrap`. **IP and ASN lookups
  always use rdap.org** (RIR coverage there is complete; tiers 1–2 are
  domain-only).
- Normalized fields: `handle`, `status[]`, `events{action:date}`, `entities`,
  plus per-kind fields (domain: `ldhName`, `nameservers`, `dnssec`; ip:
  `startAddress`/`endAddress`/`country`; asn: `startAutnum`/`endAutnum`).

## DNS-over-HTTPS — Google + Cloudflare (`dns`)
- Google: `https://dns.google/resolve?name=<n>&type=<T>`.
- Cloudflare: `https://cloudflare-dns.com/dns-query?name=<n>&type=<T>` with
  `Accept: application/dns-json`.
- Supported types: A, AAAA, MX, TXT, NS, CNAME, SOA, CAA.
- Response `Status` is an RCODE (0=NOERROR, 3=NXDOMAIN, …); answers carry numeric
  `type` codes which the helper maps back to mnemonics.

## ip-api.com — IP geolocation / ISP (`ip`)
- Endpoint: `http://ip-api.com/json/<ip>?fields=...` (free tier is HTTP-only).
- **Rate limit: 45 requests/minute** per source IP — respect it (batch, space out).
- API-level failures come back as `{"status":"fail","message":...}` (e.g. reserved
  ranges) — the helper raises a clean error rather than returning junk.

## RIPEstat Data API — ASN / prefix / IP ownership (`asn`)
- ASN: `https://stat.ripe.net/data/as-overview/data.json?resource=AS<n>` plus
  `.../announced-prefixes/data.json?resource=AS<n>`.
- IP: `https://stat.ripe.net/data/network-info/data.json?resource=<ip>` →
  announcing ASN(s) + covering prefix.
- Free, keyless, well-maintained by RIPE NCC. **This replaces BGPView**, which was
  permanently shut down in November 2025 (see `CHANGELOG.md`).

## archive.org Wayback — availability + CDX (`wayback`, bonus)
- Availability fast-path: `http://archive.org/wayback/available?url=<u>` — returns
  the closest snapshot (if any) under `archived_snapshots.closest`.
- Capture history: `https://web.archive.org/cdx/search/cdx?url=<u>&output=json`
  (array-of-arrays; first row is the header). The helper lists the most recent
  captures (`--cdx-limit`, default 10) and can compute active-months with
  `--cdx-count` (an extra, slower scan). `--no-cdx` skips this step entirely.
- Quirk: the CDX endpoint returns an *empty body* for a never-archived URL — the
  parser treats a missing/header-only response as "no captures", not an error.

## Rate limits & gotchas
A consolidated cheat-sheet of the per-source caveats to be a good citizen:

- **ip-api.com** — free tier is **HTTP-only** (no HTTPS) and **non-commercial use
  only**; commercial use requires the paid/keyed plan. Hard limit **45 requests /
  minute** per source IP (HTTP 429 on breach). The `profile` orchestrator spaces
  its `ip` enrichment calls to stay under this; if you script `ip` in a loop, add
  your own delay.
- **crt.sh** — frequently slow and prone to `502`/`503` under load; this can be a
  **hard outage** (every query `502`s, not just throttling), and large domains can
  return very large responses. The helper retries with backoff and then **falls
  back to certSpotter** so subdomain enumeration survives; `sources_used` shows
  which CT source answered. Use `certs --limit` / `--max-certs` to cap output on
  busy domains. The live smoke test treats a 5xx as a *skip* (transient) rather
  than a failure (schema drift).
- **certSpotter** — the CT fallback (`api.certspotter.com`). The keyless free tier
  is **rate-limited** (HTTP `429` when exceeded) and returns a bounded window of
  issuances per query; it is queried only when crt.sh fails (or with `--all-ct`),
  so normal use stays well under its limits.
- **rdap.org** — the RDAP *fallback* redirector; the authoritative server it
  forwards to sets its own (usually generous) limits. Redirects are followed
  automatically. Primary domain lookups now go through the **IANA bootstrap**
  (`data.iana.org/rdap/dns.json`, fetched once per run) plus a curated
  **supplement** for TLDs IANA omits but that run RDAP (notably `.io`); rdap.org
  covers everything else and all IP/ASN lookups. Note the supplement is a small
  static map — extend it if you need a ccTLD it doesn't yet list.
- **DoH (Google / Cloudflare)** — generous public limits; the `dns` command lets
  you switch providers with `--provider` if one is degraded.
- **RIPEstat** — free and well-maintained, but a heavy `announced-prefixes` pull is
  the slow part of an ASN lookup; use `asn --no-prefixes` when you only need the
  holder. This is the **BGPView replacement** (BGPView shut down Nov 2025).
- **Wayback CDX** — `--cdx-count` walks the full capture index and can be slow for
  heavily-archived sites; the default lists only the most recent captures.
- **General courtesy** — every request carries a descriptive `User-Agent`, uses a
  per-request timeout, and backs off on `429`/`5xx` honoring an integer
  `Retry-After`. Nothing here probes the target directly — all lookups are passive
  queries against third-party databases.
