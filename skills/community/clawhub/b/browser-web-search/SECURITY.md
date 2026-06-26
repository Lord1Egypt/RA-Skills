# Security model — `browser-web-search-skill`

> **Skill version:** 0.4.10 (this launcher + docs + gating policy)
> **Audited upstream:** `browser-web-search@0.4.3` (pinned, SHA-512 enforced)
> **Latest external review:** ClawScan, May 2026

This document is the human-readable map between external security reviews
and the file-by-file evidence in this repository. It is intentionally
**code-linked** rather than aspirational: every claim below points at a
specific function or field that anyone can audit.

The launcher does **not** spawn subprocesses, **does not** invoke a shell,
and is the only code that touches the third-party `browser-web-search` npm
package. All hardening described here lives in `scripts/run.js` and
`config.json`.

---

## 1. Threat model in one paragraph

`browser-web-search` is a third-party npm package that executes JavaScript
inside an authenticated OpenClaw browser tab. Once invoked, that JavaScript
inherits the user's full login state for the visited domain (DMs,
favorites, profile, orders) and — depending on browser configuration —
can reach other open tabs in the same profile. This skill's launcher
cannot constrain the package's behavior in-process; it can only:

1. refuse to load the package when its identity or bytes deviate from a
   pinned audit, and
2. interpose deny-by-default policy gates so the package is not invoked
   at all unless an operator has *consciously and recently* authorized
   the specific (site, audited bytes) combination, and
3. record every decision in an append-only audit log so any unauthorized
   call can be detected after the fact.

These three layers are the launcher's entire contribution; the skill
**does not** claim to sandbox the package's runtime behavior.

---

## 2. ClawScan May 2026 verdict — line-by-line

> *Source: ClawScan, analyzed May 11 2026, type "OpenClaw Skill",
> name `browser-web-search`, version 0.4.10.*

### Verdict text (verbatim)

> The skill provides a high-risk capability by executing JavaScript within
> authenticated browser sessions to scrape data from 55+ platforms,
> including private areas like DMs, orders, and profiles. While the
> launcher (`scripts/run.js`) is exceptionally defensive — implementing a
> mandatory SHA-512 integrity check on the 'browser-web-search' npm
> package, rejecting symbolic links, and enforcing a three-tier
> authorization gate that is sealed by default — the core functionality
> inherently relies on a third-party dependency to handle sensitive
> session data. This high-risk access to authenticated browser states,
> despite the robust mitigations and audit logging, warrants a
> suspicious classification.

### Claim ↔ evidence map

| ClawScan claim | Where it lives | Notes |
|---|---|---|
| "executes JavaScript within authenticated browser sessions to scrape data from 55+ platforms" | `SKILL.md` adapter table; `scripts/run.js` `ALWAYS_SENSITIVE_SITES`, `SENSITIVE_SUFFIX_RE`, `PUBLIC_SITES` | The launcher only forwards args; the third-party package is what runs the JS. |
| "mandatory SHA-512 integrity check on the 'browser-web-search' npm package" | `scripts/run.js` `verifyBwsIntegrity()` (size + name + version + SHA-512); constants `ENTRY_SHA512_BASE64`, `ENTRY_EXPECTED_SIZE`, `REQUIRED_VERSION`; mirrored in `config.json` `install.verification.integrity` and `capabilities.supplyChain.runtimeIntegrityGate` | Timing-safe compare via `crypto.timingSafeEqual`. **No environment override.** Failure is denied + audited under `adapter="(integrity)"`. |
| "rejecting symbolic links" | `scripts/run.js` `pathHasSymlinkUnder()` invoked from `resolveBwsEntry()` | Rejects any component from the candidate root down to `dist/index.js`. Missing components are treated as untrusted (deny). |
| "three-tier authorization gate that is sealed by default" | `scripts/run.js` `enforcePreIntegrityGates()` (Gates 1-3) | Gate 2 (`BWS_ENABLE_SENSITIVE_TIER` sealed) was added in v0.4.4 in direct response to a prior ClawScan finding ("Identity and Privilege Abuse"). |
| "the core functionality inherently relies on a third-party dependency" — *the residual concern* | This is **inherent to the capability** and cannot be removed by the launcher. v0.4.10 adds the three mitigations in §3 to reduce the operator's information asymmetry rather than constrain the dependency. | See §3 below. |
| "warrants a suspicious classification" | n/a (verdict) | Acknowledged. The recommended runtime profile in `config.json` makes `BWS_PUBLIC_ONLY=1` the production default specifically to reflect this classification. |

---

## 3. Residual mitigations introduced in v0.4.10

The v0.4.10 release adds three layered measures on top of the v0.4.4
sealed-tier model. None of them constrains the third-party package's
runtime behavior — that is impossible from in-process — but together they
make a silent or accidental sensitive invocation unreachable.

### 3.1 Gate 4 — Platform consent ledger

| Property | Value |
|---|---|
| Where | `scripts/run.js:enforceConsentAndEmitTransparency()` |
| Store | `~/.bws/consents.json` (mode 0600) |
| Bound to | `(site, pkgVersion, entrySha512)` |
| First-call flag | `--accept-platform-consent` |
| Bypass env (with loud stderr) | `BWS_SKIP_PLATFORM_CONSENT=1` |
| Auto-invalidation | Any drift in `pkgVersion` OR `entrySha512` invalidates the record for that site and forces re-consent |
| Audit log reason on deny | `no-platform-consent:no-record` / `:pkg-version-changed` / `:pkg-integrity-changed` |

**Why this exists.** The v0.4.4 SHA-512 integrity gate guarantees that the
launcher imports the bytes we audited, but the *operator's* trust decision
is implicit: "I once enabled `BWS_ENABLE_SENSITIVE_TIER=1` and never
revisited that decision." When the upstream package is re-audited and the
launcher's pinned constants are bumped in lockstep, the integrity gate
still passes and previously consented sites would silently re-open. Gate 4
binds consent to the audited bytes, so any drift invalidates the record.

**What it does not do.** Gate 4 does not prevent a consented call from
exfiltrating data through the package's own network egress. That is
covered by **§4 — Defenses outside this skill**.

### 3.2 Transparency block

| Property | Value |
|---|---|
| Where | `scripts/run.js:emitTransparencyBlock()` |
| Format | `[bws] transparency:` + JSON, single stderr line |
| Fields | `adapter`, `site`, `primaryDomain`, `classification`, `pkg`, `pkgEntrySha512`, `gate`, `dryRun`, `auditLog`, `consentLedger` |
| Always emitted for | `classification === 'sensitive'` |
| Optional for public | `BWS_TRANSPARENCY=1` |

The block contains no request payloads, no response bodies, and no raw
args (only the SHA-256 prefix from the audit hash). It is emitted *before*
the package is imported, so it appears even when the package crashes or
hangs immediately after start.

**Adversary model.** A wrapping AI agent or shell script cannot suppress
the line without editing `scripts/run.js`. Downstream consumers always
see the (audited bytes, gate path) tuple for any sensitive call.

### 3.3 `--dry-run` launcher flag

| Property | Value |
|---|---|
| Where | `scripts/run.js:safeRunBws()` Step 5 |
| Behavior | Runs Gates 1-4 + symlink rejection + integrity verification + audit + transparency, then exits **without** importing the package |
| Exit code | 0 = would allow; non-zero = denied (audit log shows reason) |
| Audit record marker | `dryRun: true`, `decision: dry-run-allow` or `deny` |

`--dry-run` is the CI / agent dispatch primitive. A scheduler can verify
that gates will allow a planned sensitive call (and observe the
transparency block) before committing real browser session.

---

## 4. Defenses outside this skill — operator responsibilities

The launcher cannot enforce these; they must be configured at the
host / OpenClaw / browser layer:

1. **Dedicated OpenClaw browser profile.** Do not reuse your daily
   profile. Bank, email, SSO sessions must not coexist with adapters that
   could touch the same browser.
2. **Single-target-domain tab policy.** Close every tab unrelated to the
   adapter you are about to call. The launcher cannot tell the package to
   stay in one tab.
3. **Production posture: `BWS_PUBLIC_ONLY=1`.** If you never need
   authenticated access, leave it set permanently. Gate 1 then denies
   every sensitive call regardless of opt-in.
4. **Re-audit on every upstream version bump.** Bumping
   `REQUIRED_VERSION` requires inspecting the new source on GitHub *and*
   recomputing `ENTRY_SHA512_BASE64` + `ENTRY_EXPECTED_SIZE`. Gate 4's
   consent ledger will auto-invalidate all prior consents once the new
   `entrySha512` is in effect.

---

## 5. Audit log schema (`~/.bws/audit.log`)

Append-only JSON Lines, mode 0600, 1 MiB rotation to `audit.log.1`.

| Field | Meaning |
|---|---|
| `ts` | UTC RFC3339 |
| `pid` | Launcher PID |
| `adapter` | Adapter name (e.g. `weixin/search`) or `(integrity)` / `(meta)` |
| `site` | Adapter prefix |
| `primaryDomain` | Known top-level domain (null for unknown) |
| `argHash` | SHA-256 prefix of args (never the args themselves) |
| `classification` | `public` / `sensitive` |
| `decision` | `allow` / `deny` / `dry-run-allow` |
| `reason` | One of: `public`, `tier+opt-in:flag`, `tier+opt-in:env`, `…+consent:granted`, `…+consent:cached`, `…+consent:skipped-env`, `BWS_PUBLIC_ONLY=1`, `sensitive-tier-sealed`, `tier-enabled-but-no-opt-in`, `no-platform-consent:*`, `entry-sha512-mismatch`, `entry-sha512-match`, `meta-subcommand` |
| `pkgVersion` | (sensitive allow records only) The verified `package.json.version` |
| `dryRun` | (when applicable) `true` |

The audit log never contains payloads, responses, raw args, cookies, or
session identifiers.

---

## 6. Out of scope for this skill

The following are **not** in this skill's threat model. They are
acknowledged but not mitigated:

- Behavior of `browser-web-search` *within* its audited bytes (e.g. an
  audited build that has a benign-looking but excessive scrape function).
  Gate 4 binds consent to the audited bytes, but does not inspect them.
- Browser-internal sandboxing between tabs. That is OpenClaw / Chromium's
  responsibility. The skill recommends (§4) but does not enforce it.
- Operator's secret hygiene (shell history, env-var dumps in CI logs).
  We log only hashes and metadata; we cannot control what the operator's
  surrounding tooling does.
- Network-level traffic shaping. Egress destinations are listed in
  `config.json:permissions.network.domains`; enforcement is the host's
  responsibility.

---

## 7. Reporting a vulnerability

If you find a way to:

- bypass any of Gates 1-4 without editing `scripts/run.js`, or
- cause `verifyBwsIntegrity()` to admit non-audited bytes, or
- read or alter `~/.bws/audit.log` / `~/.bws/consents.json` via the
  launcher's normal control flow,

please open a private issue on
<https://github.com/sipingme/browser-web-search-skill> with a minimal
reproduction. The third-party package itself is tracked separately at
<https://github.com/sipingme/browser-web-search>.

---

## 8. Change log

| Version | Date | Summary |
|---|---|---|
| 0.4.10 | 2026-05-11 | Gate 4 platform consent ledger + transparency block + `--dry-run`. Responds to ClawScan May 2026 residual "suspicious" classification. **npm pin unchanged at 0.4.3.** |
| 0.4.4 | 2026-05-07 | Sensitive tier sealed by default (`BWS_ENABLE_SENSITIVE_TIER` required). SHA-512 integrity gate without env override. Symlink rejection. CWD / launcher-local node_modules disabled by default. |
| 0.4.3 | 2026-04-29 | Expanded to 55 platforms / 91+ commands. |
