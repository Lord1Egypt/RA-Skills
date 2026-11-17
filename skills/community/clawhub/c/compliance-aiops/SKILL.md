---
name: compliance-aiops
slug: compliance-aiops
displayName: "Compliance AIops"
summary: "Compliance evidence from AIops audit trails: HIPAA/PCI/SOC2/GDPR, OSCAL export, 19 tools."
license: MIT
homepage: https://github.com/AIops-tools/Compliance-AIops
tags: [aiops, mcp, governance, compliance]
description: >
  Use this skill whenever the user needs compliance evidence from the audit trails their governed AIops agents already write — mapping AI-agent infra-ops activity to HIPAA §164.312, PCI-DSS v4.0, SOC 2 TSC, or GDPR controls, producing a change-approval report, a gap analysis, an exceptions/anomaly report, or a hash-chain-sealed, tamper-evident evidence bundle.
  Always use this skill for "compliance evidence", "HIPAA / PCI-DSS / SOC 2 / GDPR evidence", "audit trail report", "coverage for control X", "which controls are we short on / gap analysis", "who approved this change / change-management evidence", "denied or errored ops / anomaly evidence", "seal / sign an evidence bundle", "prove this bundle wasn't altered", or "detect deleted audit rows".
  Do NOT use to scan or operate infrastructure and do NOT treat it as a GRC platform — it reads the local audit databases the OTHER AIops-tools write and converts them to evidence; for platform operations use those other AIops-tools.
  Evidence, not certification. Reads sibling audit trails read-only; no external API, no network, no platform credentials. Fully offline and deterministic.
installer:
  kind: uv
  package: compliance-aiops
argument-hint: "[framework (hipaa|pci_dss|soc2|gdpr|iso27001|djcp_l3) or describe your evidence task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["compliance-aiops","uvx"]},"optional":{"env":["COMPLIANCE_AIOPS_CONFIG","COMPLIANCE_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Compliance-AIops","emoji":"📋","os":["macos","linux"]}}
compatibility: >
  Standalone compliance-evidence tooling. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  Data source: the LOCAL audit databases the other governed AIops tools already write, discovered by glob at ~/.*-aiops/audit.db (one shared audit_log schema). These are read READ-ONLY. There is NO external API, NO network, and NO platform credentials.
  The only optional secret is a bundle-signing key, stored ENCRYPTED in ~/.compliance-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk, unlocked by a master password from COMPLIANCE_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). If you never sign bundles you need no secret at all.
  Outputs: evidence bundles written to ~/.compliance-aiops/bundles/ (the only files written). All tool calls are themselves audited to a local SQLite DB under ~/.compliance-aiops/ (relocatable via COMPLIANCE_AIOPS_HOME). Write tools (generate_evidence_bundle, export_bundle: low risk; sign_bundle: medium) pass through the @governed_tool decorator but perform NO external mutation.
  Integrity: bundles are hash-chain-sealed (SHA-256 over ordered records; reproducible chainHead) with an optional HMAC signature. Tamper-EVIDENT, not tamper-PROOF — the source audit.db remains the system of record.
  Webhooks: none — no outbound network calls at all.
  Transitive dependencies: the MCP SDK and cryptography (Fernet). No post-install scripts or background services.
  Evidence, not certification. Fully offline and deterministic; the integrity claims are covered by deterministic offline tests (see docs/VERIFICATION.md). OSCAL export is a v0.2 roadmap item (v0.1 emits JSON/Markdown/CSV).
---

# Compliance AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by any framework body or GRC vendor.** HIPAA, PCI-DSS, SOC 2, GDPR and OSCAL are referenced descriptively; trademarks belong to their owners. Source at [github.com/AIops-tools/Compliance-AIops](https://github.com/AIops-tools/Compliance-AIops) under the MIT license.

Governed **compliance-evidence** tooling — **19 MCP tools**. It **reads the audit
trails your governed AIops agents already write** (`~/.<tool>-aiops/audit.db`, one
shared `audit_log` schema, discovered via `~/.*-aiops/audit.db`) **read-only**,
and turns that activity into **framework-mapped, hash-chain-sealed compliance
evidence**. It does **not** scan infrastructure and does **not** replace a GRC
platform.

> **Standalone**: the governance harness is bundled (`compliance_aiops.governance`).
> **Not a platform wrapper** — no external API, no network, no platform
> credentials. **Evidence, not certification**; fully offline and deterministic.

## What This Skill Does

| Group | Tools | Count | Read/Write |
|-------|-------|:-----:|:----------:|
| **Audit reads** | `list_audit_sources`, `query_audit_events`, `activity_timeline` | 3 | read |
| **Framework mapping** | `list_frameworks`, `coverage_summary`, `control_evidence`, `gap_analysis` | 4 | read |
| **Assurance reports** | `approval_report`, `exceptions_report` | 2 | read |
| **Integrity** | `verify_source_chain`, `verify_bundle`, `list_bundles`, `bundle_schedule_hint`, `oscal_assessment_results` | 5 | read |
| **Artifacts** | `generate_evidence_bundle` (low), `export_bundle` (low), `sign_bundle` (medium) | 3 | write (no external mutation) |
| **Undo** | `undo_list`, `undo_apply` | 2 | undo |

## Frameworks & sample controls

| Framework | Sample controls (strength) |
|-----------|----------------------------|
| **HIPAA** §164.312 | 164.312(b) Audit controls (strong), 164.312(a)(1) Access control (strong), 164.312(c)(1) Integrity (strong) |
| **PCI-DSS v4.0** | 10.2 Audit log content (strong), 10.3 Protect audit logs (strong), 7-8 Least privilege / authn (partial) |
| **SOC 2 TSC** | CC6.1 Logical access (strong), CC7.2 Monitoring (strong), CC8.1 Change management (strong) |
| **GDPR** | Art.30 Records of processing (partial), Art.32 Security of processing (strong) |
| **ISO/IEC 27001:2022** (Annex A) | A.5.15 Access control (strong), A.5.16 Identity mgmt (strong), A.5.18 Access rights (partial), A.8.2 Privileged access (partial), A.8.15 Logging (strong), A.8.16 Monitoring (strong), A.8.32 Change management (strong) |
| **等保2.0 (DJCP L3)** GB/T 22239-2019 三级 | 8.1.5.4 安全审计 (strong), 8.1.4.2 访问控制 (partial), 8.1.5 安全管理中心/集中审计 (strong) |

Audit trails prove *operating effectiveness* strongly but *control design /
configuration* only partially — each control is labelled `strong` or `partial`,
and `gap_analysis` surfaces the caveat rather than overclaiming.

## Quick Install

```bash
uv tool install compliance-aiops
compliance-aiops init       # discover sibling ~/.*-aiops/audit.db, set org name, optional signing key
compliance-aiops doctor     # which sibling audit DBs are present/readable
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/compliance-aiops
openclaw skills info compliance-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Map AI-agent infra-ops activity to a framework's controls (`coverage_summary`)
- Pull the evidence rows + population for one control (`control_evidence`)
- Find controls with no or weak evidence, with the honest caveat (`gap_analysis`)
- Produce a change-approval artifact — who approved which high-risk write and why
  (`approval_report`)
- Produce enforcement / anomaly evidence — denied / errored / budget-tripped ops
  (`exceptions_report`)
- Seal a tamper-evident evidence bundle (`generate_evidence_bundle`,
  `sign_bundle`) and later prove it wasn't altered (`verify_bundle`)
- Detect deleted / missing audit rows in a source trail (`verify_source_chain`)

**Do NOT use** to scan or operate infrastructure, or as a GRC platform. It reads
the audit DBs the *other* AIops-tools write; for platform operations use those
other AIops-tools.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| Compliance evidence from existing AIops audit trails | **compliance-aiops** (this skill) |
| To actually operate a platform (VMs, storage, clusters, network, …) | the relevant platform **AIops-tools** skill |
| OT / industrial edge (Modbus, OPC-UA, PLC) | the **industrial-aiops** line |
| A full GRC platform / policy management | out of scope — this is evidence, not GRC |

## Common Workflows

### 1. "The SOC 2 auditor wants Q3 change-approval evidence by Friday"

1. `compliance-aiops doctor` → confirm the source audit trails are discoverable
   and readable before you promise a delivery date
2. `compliance-aiops report sources` (MCP: `list_audit_sources`) → which sibling
   audit trails were found, and the event count and date range in each. If a
   source you expected is missing, the bundle would be silently incomplete —
   fix discovery first
3. `compliance-aiops report coverage soc2` → confirm CC8.1 is actually covered by
   the evidence you have, before generating anything
4. `compliance-aiops report approvals` → the high-risk write operations with
   their named approver and rationale — this is the population CC8.1 is asking
   about
5. `compliance-aiops bundle generate soc2 --since 2026-07-01 --until 2026-10-01 --sign`
   → a hash-chain-sealed bundle under `~/.compliance-aiops/bundles/`
6. `compliance-aiops bundle export <path> --format markdown` → the
   auditor-facing report (also `json` / `csv`)
7. **Failure branch**: if `report coverage` shows CC8.1 thin, **do not generate
   anyway and hope** — run workflow 2 first and hand the auditor the honest gap
   statement. A bundle asserts what the audit trail contains; it cannot
   manufacture evidence that was never recorded.

### 2. "Which controls are we actually short on?" (gap analysis)

1. `compliance-aiops report sources` → establish the evidence base and its date
   coverage; a gap caused by a *missing source* is a different problem from a
   gap caused by *missing activity*
2. `compliance-aiops report gaps hipaa` (also `pci_dss`, `soc2`, `gdpr`) →
   controls with no or weak evidence, each with an honest caveat and a
   remediation suggestion
3. `compliance-aiops report exceptions` → the operations that ran **without** an
   approver or rationale — usually the fastest-to-fix category of gap
4. Drill into one control's population with `control_evidence` (MCP) to see the
   **reproducible query** behind the coverage number, so the figure can be
   defended rather than merely quoted
5. `compliance-aiops report coverage <framework>` again after remediation to
   confirm the gap actually closed
6. **Failure branch**: if `list_frameworks` does not carry the framework or
   control the auditor named, say so — this tool maps to HIPAA / PCI-DSS /
   SOC 2 / GDPR and does not silently substitute a near-miss control.

### 3. Prove a delivered bundle was not altered

1. `compliance-aiops bundle list` → locate the bundle and its recorded
   `chainHead`
2. `compliance-aiops bundle verify <path>` → re-derives the hash chain, compares
   it to the seal's `chainHead`, and checks the optional signature
3. Because the chain is computed over evidence records only, the **same**
   (framework, period, sources) reproduces the **same** `chainHead` — regenerate
   and compare to prove reproducibility
4. Record the `chainHead` **out-of-band** (ticket, email to the auditor, WORM
   store) at delivery time; that out-of-band copy is what makes later
   verification meaningful
5. `verify_source_chain` (MCP) on each source → returns the source chain head and
   flags **row-id gaps**, a sign that rows were deleted from that `audit.db`
6. **Failure branch**: a `chainHead` mismatch or a row-id gap means the evidence
   is **not** trustworthy — escalate, and treat the source `audit.db` as the
   system of record. Do not re-seal a fresh bundle to make the mismatch go away;
   the tool is **tamper-evident, not tamper-proof**, and its whole value is that
   it reports this rather than papering over it.

### 4. 定期封存 — schedule periodic sealed bundles (no daemon)

This tool ships **no scheduler**; it emits a cron line for you to install.

1. `compliance-aiops report sources` → confirm the sources you want sealed are
   discoverable from the account cron will run as (a common failure: cron sees a
   different `$HOME`)
2. `compliance-aiops bundle schedule soc2 --cron "0 2 * * 1" --period 7d --sign`
   (MCP: `bundle_schedule_hint`) → returns a `cronLine` plus the exact
   non-interactive command. **It writes nothing.**
3. Paste the `cronLine` into `crontab -e`, e.g.
   `0 2 * * 1 compliance-aiops bundle generate soc2 --period 7d --sign`
4. Export `COMPLIANCE_AIOPS_MASTER_PASSWORD` in the cron environment so the
   signing key unlocks non-interactively — never inline the real password in the
   crontab
5. After the first scheduled run, `compliance-aiops bundle list` and
   `bundle verify` the newest bundle to confirm the unattended path really works
6. **Failure branch**: if the cron run produces no bundle, the usual causes are
   an unset master password (signing cannot unlock) or `COMPLIANCE_AIOPS_HOME`
   not being set in cron's environment, so sources resolve elsewhere. Verify by
   running the emitted command by hand with a clean environment before trusting
   the schedule.

## Governance & Safety

The skill reads audit trails and writes evidence bundles and records what it
does; it does **not** decide whether producing or signing a bundle is permitted.
That is your agent's judgement, or the filesystem permissions of the account it
runs as. There is no read-only switch, policy file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.compliance-aiops/audit.db` (relocatable via `COMPLIANCE_AIOPS_HOME`): params, outcome summary, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- The source audit trails are opened **read-only**; the tool never mutates them. The only files written are bundles under `~/.compliance-aiops/bundles/`.
- `COMPLIANCE_AUDIT_APPROVED_BY` / `COMPLIANCE_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Tamper-EVIDENT, not tamper-PROOF** — the source `audit.db` remains the system
  of record.

## References

- `references/capabilities.md` — full tool → inputs → returns reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — source discovery, org name, optional signing key, integrity notes
