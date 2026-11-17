# compliance-aiops setup & security guide

> Evidence, not certification. Reads the local audit trails governed
> AIops tools already write, read-only. **No external API, no network, no
> platform credentials.**

## 1. Install

```bash
uv tool install compliance-aiops
```

## 2. Onboard

```bash
compliance-aiops init
```

The `init` wizard:

- **Auto-discovers sibling audit DBs** by globbing `~/.*-aiops/audit.db` (e.g.
  `~/.nutanix-aiops/audit.db`, `~/.<tool>-aiops/audit.db`). These are the local
  `audit_log` trails your governed AIops tools already write. Each discovered
  source can be included and tagged.
- **Records an organization name** and the selected sources into
  `~/.compliance-aiops/config.yaml`.
- **Optionally stores a bundle-signing key** — encrypted, Fernet (AES-128-CBC +
  HMAC) with a scrypt-derived key. This is the *only* secret the tool uses, and
  it is optional: if you never sign bundles you need no secret at all.

No platform credentials are collected, because the tool never connects to any
platform — its inputs are on-disk audit databases opened **read-only**.

Example `~/.compliance-aiops/config.yaml`:

```yaml
organization: Acme Health, Inc.
sources:
  - name: nutanix
    path: ~/.nutanix-aiops/audit.db
    tag: infra
  - name: k8s
    path: ~/.k8s-aiops/audit.db
    tag: platform
```

## 3. Non-interactive use (MCP server / CI / cron)

Only needed if you **sign** bundles. Export the master password so the encrypted
signing-key store can be unlocked without a prompt:

```bash
export COMPLIANCE_AIOPS_MASTER_PASSWORD='your-master-password'
```

## Signing-key security

- The signing key is **never** written to disk in plaintext. It lives only in
  `~/.compliance-aiops/secrets.enc`, encrypted with Fernet, the key derived from
  your master password via scrypt. Only a per-store random salt and the
  ciphertext are on disk (chmod 600); the master password itself is never stored.
- A legacy plaintext key is honoured as a fallback with a deprecation warning —
  migrate with `compliance-aiops secret migrate`.
- The key is held only in memory during a session and is never logged or echoed.

## State & outputs

State lives under `~/.compliance-aiops/` (relocate with `COMPLIANCE_AIOPS_HOME`):

- `config.yaml` — organization name + selected audit sources
- `secrets.enc` — the optional encrypted signing key
- `bundles/` — generated evidence bundles (**the only files the tool writes**)
- `audit.db` — this tool's own governance audit log (every tool call recorded)

The source `~/.<tool>-aiops/audit.db` trails are opened **read-only** and never
modified.

## Integrity notes

- **Reproducible `chainHead`.** The hash chain is over evidence records only, so
  the same `(framework, period, sources)` reproduces the same `chainHead`. Record
  it out-of-band to create an independent anchor.
- **Tamper-EVIDENT, not tamper-PROOF.** The chain and optional signature let an
  auditor *detect* alteration; the source `audit.db` remains the system of record.
- `verify_bundle` re-derives the chain and checks the seal head + signature;
  `verify_source_chain` flags **row-id gaps** in a source (a sign of deleted rows).

## Verify

```bash
compliance-aiops doctor
```

`doctor` reports which sibling audit DBs are present and readable, and whether the
config and (optional) signing-key store are in place.
