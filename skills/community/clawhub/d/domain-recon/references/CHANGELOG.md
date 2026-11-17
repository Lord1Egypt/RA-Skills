# Changelog / Design decisions — domain-recon

## 0.6.0 — RDAP `broken` fourth state (endpoint answered, unusably)

The third state (`unreachable`, 0.5.0) covered a delegated RDAP endpoint that
gave us *no* HTTP response (transport reset/timeout). It left a second gap: an
endpoint that *does* respond but with something unusable — an untrusted /
self-signed TLS certificate, or an HTTP error status — still collapsed to a bare
exit-2 error, indistinguishable from a genuine crash. The former 13 KNOWN-ISSUE
TLDs were exactly this class.

### Added
- **First-class `broken` RDAP result.** A delegated endpoint that answers with a
  bad TLS cert or an HTTP 4xx/5xx now returns
  `{"supported": true, "rdap_source": "broken", "cause": "<slug>",
  "http_status": <int|null>, "retryable": <bool>, "reason": ...}` — distinct from
  both `unsupported` (no server exists) and `unreachable` (no HTTP response). The
  server demonstrably exists (bootstrap/supplement-delegated) and answered; it is
  just serving a fault, surfaced descriptively instead of as an opaque error.
- **Retryability classified by wire behavior, not by bucket** (`_endpoint_fault`):
  a bad TLS cert (untrusted/self-signed → `ssl.SSLCertVerificationError`) and an
  HTTP 4xx are persistent registry-side faults (`retryable:false`); an HTTP 5xx
  is the server-error class that per HTTP semantics warrants a later retry
  (`retryable:true`). The exit code encodes the retryability tier, extending the
  quad-state to a **quint-state**: `0` clean/`unsupported` · `2` crash/429-ban ·
  `3` retryable (`unreachable`, or `broken` 5xx) · `4` non-retryable `broken`
  (bad-cert / 4xx). `rdap_source` names the mechanism; the exit code names the
  actionable tier.
- Human/`profile` renderers gained explicit `broken [cause] (retryable|not
  retryable)` lines.

### Design decisions (flagged)
- **`broken` fires only after BOTH the authoritative server *and* the rdap.org
  redirector are exhausted.** A definitive authoritative fault (bad-cert/4xx/5xx)
  is remembered but the redirector is still tried — it may resolve to a different
  server that answers (the `.io`-style redirector-rescue path). Only if the
  redirector also fails is the *authoritative* cause surfaced as `broken`, so the
  state means "both paths exhausted", not one transient 404. A first cut
  short-circuited on the authoritative fault and regressed redirector-rescue;
  caught and fixed.
- **Re-probed each authoritative endpoint directly** rather than trusting the old
  buckets: `.fj`/`.porn` had been filed as timeouts, but that was the rdap.org
  fallback — at their real endpoints they are bad certs. Classification follows
  the actual wire behavior.
- **Narrow, mutually-exclusive trigger.** `bad-cert` matches only
  `ssl.SSLCertVerificationError` (a distinct subclass — never a plain TLS reset,
  which stays `unreachable`); a 429/ban (`RateLimitError`), a DNS-resolution
  failure, a connection-refused, and a genuine `unsupported` absence can never
  land in `broken`. No TLS verification is ever disabled — this is pure
  classification, not a fetch change.

### Applied to the 13 former KNOWN-ISSUE TLDs
Re-run one-at-a-time (`--retries 0`, sequential): **12 → `broken`** (7 bad-cert:
`.chase .cr .fj .mtr .porn .sr .xxx`; 2 http-426: `.tw .xn--kpry57d`; 2 http-404
apex: `.vg .xn--o3cw4h`; 1 http-500 retryable: `.xn--mxtq1m`) and **1 recovered
to PASS** (`.mg` returned real data this pass). KNOWN-ISSUE **13 → 0**; every one
of the 1,433 corpus inputs now yields an honest, non-crashing, first-class
outcome (this is a statement about *tool behavior*, not registry health — 12
registries remain genuinely faulty, now surfaced descriptively).

### Tests
- Offline suite **143 → 168** (+25): `broken` builder shape, the bad-cert /
  4xx / 5xx truth-table, exit-4 vs exit-3 tiering, the redirector-rescue-not-
  stomped guard, and the boundary tests proving 429/DNS-fail/conn-refused/
  `unsupported` never reclassify. Boundary spot-check live: `google.com` (PASS)
  and `nic.ae` (`unsupported`) both unaffected (exit 0).

## 0.5.0 — RDAP `unreachable` third state (delegated but not fetchable)

A TLD can be *delegated in the IANA RDAP bootstrap yet unreachable from our
egress* — the registry endpoint resets the connection / RSTs the TLS handshake /
times out the read. Previously this collapsed to a bare exit-2 error, visually
identical to a genuine absence. That is the weak sense of "graceful" (not a
crash) but not the honest one (a reachable-but-blocked registry looked the same
as a broken one).

### Added
- **First-class `unreachable` RDAP result.** A transport reset/TLS-RST/read
  timeout against a bootstrap- or supplement-delegated endpoint now returns
  `{"supported": true, "rdap_source": "unreachable", "retryable": true,
  "origin": ..., "endpoint": ..., "reason": ...}` at a new **exit 3** — distinct
  from `unsupported` (`supported:false / rdap_source:none`, "no server exists").
  The signal to a consuming agent: the data exists, we could not fetch it this
  time, skip the field but know it is **retryable** — NOT "this TLD has no RDAP".
- Human/`profile` renderers gained an explicit `unreachable (retryable)` line.

### Design decisions (flagged)
- **Narrow, retryable-only trigger** (`_is_unreachable_signal`): matches only
  connection-reset (`ECONNRESET`/errno 104), read timeouts (`socket.timeout`/
  `TimeoutError`), and TLS handshake resets / unexpected-EOF (`ssl.SSLError`
  signalling a reset). It explicitly **excludes** a 429/ban (`RateLimitError`),
  any HTTP status (`HTTPStatusError`, incl. 426), DNS-resolution failure
  (`socket.gaierror`), and connection-refused — none of those can be misfiled as
  `unreachable`.
- **Short-circuit as unreachable rather than falling to rdap.org.** rdap.org only
  *redirects* the client back to the same authoritative backend, so a reset would
  just recur; surfacing `unreachable` immediately is both faster and more honest.

### Applied to the 10-reset cluster
`.beer .date .flickr .latrobe .praxi .sex .tab .vodka .williamhill
.xn--mgbi4ecexp` — all re-run one-at-a-time (`--retries 0`, sequential) → each
emits `rdap_source: unreachable` / exit 3 cleanly, zero 429s.

### Tests
- Offline suite **126 → 143** (+17): classifier truth-table, the fetch path,
  exit-3, human/`profile` rendering, and the guard that `unreachable` never
  reuses the `unsupported` shape.

## 0.4.1 — send the RFC 7480 RDAP Accept header

Exercising `rdap` against a verified target domain for all 1,438 TLDs surfaced a
real bug: **23 gTLD registry RDAP servers reject `Accept: application/json` with
HTTP 406** (`.cat`, `.barcelona`, `.sap`, `.aco`, `.seat`, `.eus`, `.gmx`, …).

### Fixed
- All RDAP requests now send **`Accept: application/rdap+json, application/json`**
  (RFC 7480 §4.2 — RDAP's registered media type; plain JSON kept as a lenient
  fallback). Verified live: the 406 servers now return 200. Applies to the
  authoritative-server, supplement, rdap.org-redirector, and IP/ASN RDAP paths,
  plus the bootstrap fetch. Offline suite 125 → **126** (new
  `test_rdap_requests_send_rdap_accept_header`).

### Verified (not code changes)
- Full `rdap`-per-TLD sweep: **849 PASS + 23 FIXED + 215 GRACEFUL** correct;
  **0 crashes / malformed output** across 1,433 diverse inputs (every result was
  real data, a clean `unsupported` graceful signal, or a clean exit-2 error).
- **13 genuine registry-side known-issues** (self-signed/untrusted TLS on
  `rdap.nic.xxx`/`.cr`/`.chase`/… , TWNIC HTTP 426, a couple of registry 404/
  timeout edges): recon errors cleanly; these are upstream, not ours to "fix"
  (disabling TLS verification would be a security regression). See
  `docs/tld-target-test-results.md`.

## 0.4.0 — RDAP graceful degradation + full per-TLD coverage map

An agent calling `rdap` on a domain whose registry runs no public RDAP server
previously got an opaque `rdap.org` 404 that *looked* like the tool was broken.
`rdap` is the only TLD-variable query — `dns`/`certs`/`ip`/`asn`/`wayback` are
TLD-agnostic — so this only affects RDAP, but it affected it confusingly.

### Added
- **First-class `unsupported` RDAP result (graceful degradation).** When the
  IANA bootstrap is consulted successfully and the TLD is absent from *both* the
  bootstrap and the curated supplement, no public RDAP server exists — rdap.org
  (a bootstrap-backed redirector) would only 404 — so `rdap` now returns
  `{"supported": false, "rdap_source": "none", "tld": ..., "reason": ...}` at
  **exit 0** instead of erroring. A caller reads one field (`supported`) and
  skips RDAP for that TLD while still using the other sources. Real answers now
  carry `"supported": true` symmetrically. Inside `profile`, an unsupported apex
  RDAP is a clean signal under `apex.rdap`, **not** an entry in `errors[]`.
  - Three cases are now distinguishable: *supported+answered*, *supported but
    transiently down* (5xx/timeout → `errors[]`/fallback, retryable), and
    *unsupported for this TLD* (permanent capability gap, not an error).
  - Bootstrap **unreachable** ≠ unsupported: if the bootstrap itself can't be
    fetched we fall back to rdap.org rather than falsely claim "unsupported".
    `--no-bootstrap` likewise never emits `unsupported`.
- **`docs/tld-rdap-coverage.md`** — a per-TLD RDAP coverage map over all 1,438
  IANA-delegated TLDs (`TLD | rdap_source | notes` + summary counts), plus
  **`scripts/gen_coverage.py`** to regenerate it from authoritative IANA data.
  Current split: **1,200 bootstrap / 18 supplement / 220 none.**
- **13 ccTLDs added to `_RDAP_SUPPLEMENT`** (`ch, af, aw, ci, ga, kn, kz, mr,
  mz, sb, so, td, tl`) — registries that run a public RDAP server IANA omits.
  Each verified live 2026-07-27 with a two-part check: HTTP 200 + real RDAP data
  for the registry's own domain **and** a clean 404 for a bogus name in the same
  TLD (proving a genuine general-purpose server, not a one-off). Candidates that
  turned out to be *already in the bootstrap* (`.br/.cz/.nl/.no/.pl`) were **not**
  duplicated — bootstrap always wins.

### Fixed
- `rdap <domain> --human` no longer prints `RDAP (domain) — None` when a registry
  redacts the top-level `handle` (e.g. `.io`/`.de`); the header falls back to the
  domain name (prior roadmap item #3).

### Tests
- Offline suite 117 → **124**: unsupported builder shape, `supported` flag on
  normal results, bootstrap-known-absent → unsupported (no spurious rdap.org
  fetch), bootstrap-unreachable → rdap.org fallback, `--no-bootstrap` never
  reports unsupported, `--human` + `profile` rendering of the unsupported case.

## 0.3.1 — bound the Wayback step so `profile` can't read as hung

Live QA (2026-07-26) ran the full surface against `groupvault.io` and
`kraken.com`. Both round-3 fixes (CT fallback + IANA/supplement RDAP bootstrap)
fired correctly on real infra, but the `profile` orchestrator on a large domain
(`kraken.com`, 90 subdomains) repeatedly ran **past 2 minutes** — long enough to
read as a hang.

### Fixed
- **`profile` now bounds the Wayback CDX step** (`run_profile` gains
  `wayback_timeout=8.0`, `wayback_retries=0`). Root cause: the profile passed its
  full `timeout=20, retries=3` budget to the Wayback step, and the Wayback CDX
  index is by far the slowest source (a single subdomain lookup was measured at
  **38 s**), so three archive targets could consume several minutes on their own.
  Wayback is the lowest-value part of a profile and is already fault-isolated, so
  it now runs on a tight single-attempt budget. Measured effect on `kraken.com`:
  **>120 s → ~78 s**; `groupvault.io` ~92 s, both completing cleanly (exit `0`).
  Documented the expected 1–1.5 min profile runtime in SKILL.md so it doesn't
  read as hung; `--no-wayback` / `--ip-limit` remain available to go faster.
- Regression test `test_wayback_step_runs_on_bounded_budget` locks the tight
  budget (offline suite 116 → 117 tests, all green).

## 0.3.0 — source-outage resilience

Both changes were driven by a live run that hit two real upstream failures at
once: crt.sh returning `HTTP 502` on every query (a hard outage), and rdap.org
`404`ing a `.io` domain (its bootstrap doesn't cover several ccTLDs/newer TLDs).

### Added
- **CT fallback (crt.sh → certSpotter)** — `certs` now tries crt.sh first and,
  on any failure (`5xx`/`4xx`/timeout/bad-JSON), falls back to **certSpotter**
  (`api.certspotter.com`, keyless) so subdomain enumeration survives a crt.sh
  outage. Names from every source that answered are merged + de-duplicated. The
  result records `sources_used` (which answered) and `errors[]` (which failed)
  for auditability, and a `200` with an empty set is treated as a genuine "no
  certs logged" answer (**not** an outage → no needless fallback). `--all-ct`
  queries both sources and merges for wider coverage. The `profile` orchestrator
  surfaces a partial CT failure under its own `errors[]` and reports `ct_sources`.
- **RDAP three-tier resolution** — `rdap` domain lookups now resolve the
  authoritative RDAP server via the **IANA bootstrap registry**
  (`data.iana.org/rdap/dns.json`, fetched once per run and memoized) for the
  ~1200 TLDs it lists (e.g. `.ai`/`.dev`/`.xyz`/`.uk`), a curated **supplement**
  for TLDs IANA omits, and rdap.org last. `rdap_source` records which tier
  answered (`iana-bootstrap` / `supplement` / `rdap.org`). IP/ASN lookups stay on
  rdap.org (complete RIR coverage). `--no-bootstrap` forces rdap.org.

### Decision (solo, flagged): certSpotter as the CT fallback
Candidates were certSpotter, Cloudflare merklemap, and crt.sh mirrors.
**certSpotter** was chosen: it is keyless, passive, has a clean documented JSON
schema (`/v1/issuances` with `expand=dns_names`), and covers the same CT ground.
merklemap and the mirrors were rejected as less stable / less documented for a
publish-ready skill. Kept stdlib-only. **Verified live** on 2026-07-26 during a
real crt.sh hard-`502` outage: `certs example.com` fell back to certSpotter and
returned subdomains, with the crt.sh `502` recorded in `errors[]`.

### Decision (solo, flagged): the IANA bootstrap alone does NOT fix `.io` — a supplement does
This is the important one. The obvious fix ("use the IANA bootstrap") turned out
to be **insufficient for the exact reported case**: a live pull of
`data.iana.org/rdap/dns.json` shows `.io` is **not in it at all** (nor are `.co`,
`.me`, `.us`). The bootstrap fixes many other TLDs (`.ai`, `.dev`, `.xyz`, `.uk`,
…), but not `.io`. Identity Digital *does* serve `.io` RDAP at
`rdap.identitydigital.services`, so the real fix is a small **curated supplement**
of TLD→RDAP-base for IANA-omitted TLDs, tried after the bootstrap and before
rdap.org. Current entries, each verified live (HTTP 200 for a real domain) on
2026-07-26: `.io`/`.sh`/`.ac` → Identity Digital, `.us` → `rdap.nic.us`.
`.co`/`.me` were left out (no public RDAP endpoint found on the obvious hosts) —
extend the map when one is confirmed. Caught only because the live smoke test
exercised the real `.io` path; the first cut (bootstrap-only) shipped green
offline but failed live.

### Decision (solo, flagged): domain-only resolution
The live failure was a `.io` **domain**; IP/ASN RDAP via rdap.org worked. IANA
also publishes `ipv4.json`/`ipv6.json`/`asn.json`, but adding them was out of
scope for the reported problem and would add fetch cost + fixtures for a path
that already works. Domains use the bootstrap+supplement; IP/ASN stay on rdap.org.

### Tests
- Offline suite expanded to **116 deterministic tests** (+24): certSpotter parse
  (scope/dedup/wildcards/error-object), CT fallback (crt.sh-down→certSpotter,
  both-down→clean error, empty-200-is-an-answer, `--all-ct` merge/dedup, profile
  surfacing); RDAP three-tier (bootstrap parse, `.ai` via bootstrap, `.io` via
  supplement, supplement-works-when-bootstrap-down, unmapped-TLD → rdap.org,
  authoritative-`404` → rdap.org, caching, `--no-bootstrap`, IP/ASN still via
  rdap.org). Live smoke: `certs` source-agnostic + `.io` (supplement) + `.ai`
  (bootstrap) — all verified passing live on 2026-07-26 under a real crt.sh
  outage.

## 0.2.0 — orchestration, archive history, hardening

### Added
- **`profile` subcommand** — a one-shot orchestrator that chains `certs → dns →
  ip → asn → wayback` for a domain into a single merged report. Deduplicates
  resolved IPs, isolates per-source failures (records them under `errors[]`
  instead of aborting), bounds each stage (`--cert-limit`/`--resolve-limit`/
  `--ip-limit`), and spaces `ip` enrichment calls to respect ip-api's 45/min.
- **Wayback CDX capture history** (`wayback`) — beyond the availability
  fast-path, the command now lists recent captures from the CDX API
  (`web.archive.org/cdx/search/cdx`), with `--cdx-limit`, optional `--cdx-count`
  (active-months scan), and `--no-cdx` to skip.
- **`certs` hardening** — `--limit` / `--max-certs` to cap subdomain and
  cert-history output on busy domains (full counts still reported), and richer
  per-cert fields (issuer, common name, validity window, serial, entry time).

### Docs
- Consolidated **"Rate limits & gotchas"** section in `API_NOTES.md` (crt.sh
  flakiness, ip-api HTTP-only + non-commercial free tier, RIPEstat prefix cost,
  CDX scan cost).
- `homepage` moved to `github.com/maggiedev-bot/domain-recon`; `metadata` block
  normalized (single-line JSON, `version`).

### Tests
- Offline suite expanded to **92 deterministic tests** (added profile
  orchestration: wiring/dedup, fault isolation, per-source failure, ip-limit
  truncation, rate-limit spacing, human render; plus CDX parse/fetch paths).

## 0.1.0 — initial build

### Sources
Five keyless sources plus a bonus, each a subcommand of `scripts/recon.py`:
`certs` (crt.sh), `rdap` (rdap.org), `dns` (Google/Cloudflare DoH), `ip`
(ip-api.com), `asn` (RIPEstat), and `wayback` (archive.org, bonus).

### Decision: BGPView → RIPEstat Data API
The original spec named **BGPView** (`api.bgpview.io`) for ASN/prefix/IP
ownership. During the build, `api.bgpview.io` was found to be **NXDOMAIN**, and
research confirmed BGPView was **permanently shut down (~November 2025, after
acquisition by Recorded Future)**. Rather than ship a dead dependency or drop the
capability, the `asn` subcommand was pointed at the **RIPEstat Data API**
(`stat.ripe.net`) — a free, keyless, well-maintained RIPE NCC service that covers
the same ASN / prefix / IP-ownership ground:
- ASN lookup → `as-overview` (holder, announced) + `announced-prefixes`.
- IP lookup → `network-info` (announcing ASN(s) + covering prefix).

This keeps the skill at five sources and preserves the intended capability.

### Design choices
- **Zero third-party runtime deps** — standard-library `urllib`/`json` only, so
  the skill gates on nothing but `python3`. `pytest` is a *tests-only* dependency.
- **Pure parse functions** (`parse_*`) split from **fetch functions** (`fetch_*`)
  so normalization is unit-testable offline against captured fixtures.
- **Single HTTP seam** (`_open` / `http_get_json`) so tests can deterministically
  simulate 429s, 5xx, timeouts, DNS failures, and malformed JSON without a network.
- **Safety:** inputs validated and IDNA/punycode-encoded; passed only as URL-
  encoded parameters; no shell is ever invoked. Descriptive User-Agent, per-
  request timeouts, and exponential backoff honoring `Retry-After`.
