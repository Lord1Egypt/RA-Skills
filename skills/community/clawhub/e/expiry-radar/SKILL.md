---
name: expiry-radar
description: Find artefacts in a repository that will break on a known future date — expired or expiring X.509 certificates (PEM, DER, PKCS#12, PKCS#7, embedded), committed JWTs past their exp claim, and hardcoded valid-until or expires dates in fixtures and config. Use when asked to check a repo for expiring certs or tokens, when a test suite or demo might fail because a fixture certificate expired, before a release, or when asking what breaks by a given date. Not for monitoring live production endpoints or renewing certificates, and not for scanning AI-agent skills (use skillscan).
license: MIT
compatibility: Requires Python 3.9+. Nothing to install beyond the single file; scanning is fully offline and uses only the Python standard library.
---

# Expiry Radar

## What this tool does

Expiry Radar scans a repository for things that stop working on a known
date: X.509 certificates, committed JWTs with an `exp` claim, and
hardcoded expiry dates in fixtures and config files. It reports each
artefact and its expiry date. It only reads the repo — it never
connects to a server, and never renews or replaces anything.

## Install

Expiry Radar is a single file. Get it pinned to the v0.3.0 release:

```bash
curl -O https://raw.githubusercontent.com/RakTikoo/expiry-radar/v0.3.0/expiry_radar.py
```

Or install it as a command with pip (same single file):

```bash
pip install git+https://github.com/RakTikoo/expiry-radar
```

The pip route provides the `expiry-radar` command, with the same flags.

The same command via pipx or uv:

```bash
pipx install git+https://github.com/RakTikoo/expiry-radar
uv tool install git+https://github.com/RakTikoo/expiry-radar
```

## Run

Scan a repository:

```bash
python3 expiry_radar.py /path/to/repo
```

Machine-readable report:

```bash
python3 expiry_radar.py . --json
```

Useful flags: `--days 30` narrows the warning window (default 90),
`--now 2027-01-01` asks "what breaks by this date?", `--show-safe`
lists safe artefacts too, `--sarif` emits SARIF 2.1.0 (not with `--json`),
`--max-file-size N` skips files larger than N bytes (default 5 MiB);
skipped files are reported as unscanned.

## Reading the results

The exit code is the verdict:

- `0` — clean: nothing expired, and nothing expiring within the window.
- `1` — at least one artefact expires within the window (90 days by
  default), marked `[EXPIRING]` with the date and days remaining.
- `2` — at least one artefact is already expired (`[EXPIRED ]`).
- `3` — usage error: bad arguments, an invalid `--now`, or a path that
  is not a directory. Never a finding — a broken invocation, not expiry.

Findings name the artefact kind, file and line, expiry instant, and
the certificate subject/issuer where there is one. JWTs are never
printed in full (first 8 characters only; `iss`/`sub`/`aud` never).
Files the scan could not read are listed as unscanned, never silently
passed. Files matched by an `expiry-radar.ignore` file in the scan root
(one glob or substring per line) are skipped the same way, with the
ignore file named as the reason. The JSON report carries `findings`, `summary`, `exit_code`,
`files_scanned`, `unscanned` and `suppressed_in_docs`.

## Limits

- Repo artefacts only: no live-endpoint probing, nothing connects out.
- No signature verification, no chain building, no revocation checks.
- Certificates inside a password-encrypted PKCS#12 container cannot be
  read; the scan reports the container with a warning instead of
  passing it silently.
- Date formats: ISO `YYYY-MM-DD`, epoch-seconds on expiry keys,
  OpenSSL `notAfter` text. `MM/DD/YYYY` and prose dates are out.
- Not a secret scanner: a JWT is reported for its expiry, not as a leak.
