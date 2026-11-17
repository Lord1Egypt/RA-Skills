# domain-recon — TODO / roadmap

Working notes for the recon skill. Newest priorities first.

> **Status 2026-07-28 (v0.6.0):** the RDAP outcome taxonomy is now a **quint-state**.
> On top of v0.5.0's `unreachable`, a delegated endpoint that *responds unusably*
> (untrusted/self-signed TLS cert, or HTTP 4xx/5xx) is now the first-class
> **`rdap_source: "broken"`** state — `cause` (`bad-cert` / `http-<status>`),
> `http_status`, and `retryable` (false for cert/4xx, true for 5xx). Exit code by
> retryability: **4** non-retryable (bad-cert / 4xx), **3** retryable (5xx, shared
> with `unreachable`). The 13 former KNOWN-ISSUE TLDs were re-run one-at-a-time →
> **12 `broken`, 1 (`.mg`) recovered to PASS**; KNOWN-ISSUE is now **0**. `broken`
> fires only after both the authoritative server and the rdap.org redirector are
> exhausted, and is mutually-exclusive with `unreachable` (cert-verify failure vs.
> transport reset) — proven by an offline truth-table (suite 143 → 168 green) and
> live re-runs (`--retries 0`, sequential). No TLS-verify disabling; pure labelling.
> Full contract in `SKILL.md` (Exit codes); reclassification in
> `docs/tld-target-test-results.md`.
>
> **Status 2026-07-27 (v0.4.0):** items #1, #2, and #3 below are **DONE**.
> - #1 graceful degradation → `rdap` returns a first-class `unsupported`
>   (`supported: false`, `rdap_source: "none"`) at exit 0; `profile` treats it as
>   a clean signal, not an `errors[]` entry. Tests + live-verified.
> - #2 coverage map → `docs/tld-rdap-coverage.md` (1,200 bootstrap / 18
>   supplement / 220 none across 1,438 TLDs), regenerable via
>   `scripts/gen_coverage.py`. 13 ccTLDs added to `_RDAP_SUPPLEMENT` (verified live).
> - #3 `--human` handle-redaction header nit → fixed.
>
> Original entries preserved below for context.

## 1. Graceful degradation — the interface must tell the caller when a query isn't supported for a TLD

**Goal:** an agent calling this skill should never get an opaque failure that *looks*
like the tool is broken when the real cause is "this data source has no coverage for
this TLD." The interface should respond back, in a structured/legible way, that the
specific query is **unsupported for that TLD** — so the skill *degrades gracefully*
instead of erroring out.

Concretely:
- When a per-TLD lookup has **no available upstream** (e.g. RDAP for a TLD whose
  registry runs no public RDAP server), the tool should surface a clear
  `unsupported` / `no coverage for .<tld>` signal — not a raw `rdap.org 404` or a
  bare exception. The caller (agent) can then skip that field and move on.
- Distinguish the three cases so the caller can reason about them:
  1. **Supported + answered** — real data returned.
  2. **Supported but transiently down** — upstream 5xx/timeout; retryable (already
     handled for CT/Wayback via `errors[]` + fallback).
  3. **Unsupported for this TLD** — no public endpoint exists at all; *not* an error,
     a permanent capability gap. This is the case that currently reads as a failure
     and should instead be a first-class "unsupported" response.
- Applies most to **RDAP** (the only per-TLD-variable query — see below), but the
  same "tell the caller cleanly" discipline covers any source outage.

## 2. Full per-TLD recon-coverage map (all ~1,438 IANA-delegated TLDs)

Enumerate **every** delegated TLD (authoritative list:
`https://data.iana.org/TLD/tlds-alpha-by-domain.txt`, ~1,438 as of 2026-07-26) and
record, per TLD, which recon queries have upstream support.

Key simplification — **only `rdap` is TLD-variable.** The other subcommands are
TLD-agnostic and work for any registrable name / IP:
- `dns` (DoH) — universal.
- `certs` (crt.sh → certSpotter CT fallback) — universal.
- `ip` / `asn` — operate on IPs/ASNs, not the TLD.
- `wayback` — universal.

So the map is effectively an **RDAP-server-per-TLD** table. Method:
1. IANA RDAP bootstrap (`data.iana.org/rdap/dns.json`) already maps ~1,200 TLDs to
   authoritative RDAP servers — those are covered automatically.
2. For each TLD **absent** from the bootstrap, determine whether a public RDAP
   server nonetheless exists (→ add to `_RDAP_SUPPLEMENT`, contract: **verified live
   HTTP 200 with real data**) or whether the registry is **WHOIS-only / no public
   RDAP** (→ mark unsupported, feeds item #1's graceful "unsupported" response).
3. Emit a coverage table: `TLD | rdap_source (bootstrap/supplement/none) | notes`.

### Prior art — 20-TLD live sweep (2026-07-26)
16/20 clean. Confirmed the bootstrap-first design generalizes across a diverse
spread (uk, fr, nl, ca, au all via bootstrap). Findings on the misses:
- `.de` — **fixed**: DENIC runs RDAP (`rdap.denic.de`), just not in IANA's bootstrap;
  added to `_RDAP_SUPPLEMENT` (verified 200).
- `.co` — no registry-level RDAP (per-registrar only); not bootstrappable by TLD →
  **unsupported**.
- `.jp` — JPRS RDAP is gTLD-only; `.jp` is WHOIS-only → **unsupported**.
- `.eu` / `.ru` — a server reportedly exists but was unreachable from the test
  sandbox (IPv6-only / no route). Not added on unverified grounds — needs a retry
  from a different network before any supplement entry.

The supplement's discipline stays: **only add endpoints verified live (200 + real
data).** Anything unverified is left to fall through, never hardcoded blind.

> **Updated (v0.5.0):** the "unreachable" and "unsupported" cases are now
> **distinct**. A bootstrap/supplement-delegated endpoint that resets the
> connection / TLS-RSTs / read-times-out (errno 104 class) is reported as the
> first-class **`rdap_source: "unreachable"` (supported:true, retryable:true, exit 3)** —
> *the server exists, we just couldn't reach it.* Only a TLD **absent** from both
> the bootstrap and the supplement is reported as case #3 **`unsupported`**
> (`rdap_source: "none"`, exit 0 — no server exists). The `.eu`/`.ru` "reportedly
> exists but unreachable (no route)" note above is the spirit of the new state,
> though a hard no-route (`gaierror`) stays a fall-through, not `unreachable` —
> the trigger is scoped to transport-level reset/timeout against a *delegated*
> endpoint.

## 3. Minor
- `rdap <domain> --human` prints `RDAP (domain) — None` when the registry omits a
  top-level `handle` (registry redaction, e.g. `.io`/`.de`). JSON is complete;
  it's a display-header nit. Batch with the next `recon.py` change.
