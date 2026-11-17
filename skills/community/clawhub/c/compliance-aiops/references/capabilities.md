# compliance-aiops capabilities

> Evidence, not certification. 19 MCP tools (14 read, 3 write, 2 undo). Data
> source: the local `audit_log` trails governed AIops tools write, discovered via
> `~/.*-aiops/audit.db` and read **read-only**. No external API, no network, no
> platform credentials. `since` / `until` accept ISO-8601 timestamps.

## Read / analysis tools (12)

### Audit reads

| Tool | Inputs | Returns |
|------|--------|---------|
| `list_audit_sources` | — | discovered sources: `name`, `path`, `tool`, `readable`, `rowCount` |
| `query_audit_events` | `source?`, `skill?`, `tool?`, `status?`, `risk_level?`, `approved?`, `selector?`, `since?`, `until?`, `limit=100` | matched events (cross-tool), normalised audit rows |
| `activity_timeline` | `since?`, `until?`, `bucket="day"` (`hour`\|`day`) | event counts per time bucket |

### Framework mapping

| Tool | Inputs | Returns |
|------|--------|---------|
| `list_frameworks` | — | frameworks + control counts (`hipaa`, `pci_dss`, `soc2`, `gdpr`, `iso27001`, `djcp_l3`) |
| `coverage_summary` | `framework`, `since?`, `until?` | per-control `covered`/`weak`/`uncovered`, evidence counts, strength labels |
| `control_evidence` | `framework`, `control_id`, `since?`, `until?`, `sample_size=20` | evidence rows + population size + the reproducible query for ONE control |
| `gap_analysis` | `framework`, `since?`, `until?` | controls with no/weak evidence + honest `strong`/`partial` caveat + remediation hint |

### Assurance reports

| Tool | Inputs | Returns |
|------|--------|---------|
| `approval_report` | `since?`, `until?`, `high_only=True` | high-risk write ops + who approved + rationale (CC8.1 / PCI 7-8 / HIPAA §312(a) artifact) |
| `exceptions_report` | `since?`, `until?` | denied / error / budget_exceeded ops — enforcement + anomaly evidence |

### Integrity

| Tool | Inputs | Returns |
|------|--------|---------|
| `verify_source_chain` | `source`, `since?`, `until?` | chain head + row-id gap detection (flags deletions) for one source |
| `verify_bundle` | `bundle_path` | verifies chain + seal head + optional signature; `ok` + any mismatch detail |
| `list_bundles` | — | bundles under `~/.compliance-aiops/bundles/` |
| `oscal_assessment_results` | `bundle_path` | the bundle as a NIST **OSCAL 1.2.3** Assessment Results document, returned inline with a `summary` (satisfied / not-satisfied / **satisfiedOnPartialEvidence** / scanTruncated) and an explicit `limitations` list. Deterministic: v5 UUIDs derived from the chain head, so re-export is byte-identical |
| `bundle_schedule_hint` | `framework`, `cron="0 2 * * 1"`, `period="7d"`, `sign=False` | ready-to-paste 5-field cron line + non-interactive command for periodic sealing; **writes nothing, no daemon** |

## Write / artifact tools (3 — no external mutation)

| Tool | Risk | Inputs | Returns / effect |
|------|:---:|--------|------------------|
| `generate_evidence_bundle` | **medium** | `framework`, `period_start?`, `period_end?`, `out_path?`, `sign=False`, `period?` (relative window e.g. `7d`) | one call: coverage + approval trail + exceptions + sealed records → a bundle `.json` under `~/.compliance-aiops/bundles/`; returns path + `chainHead` |
| `export_bundle` | **medium** | `bundle_path`, `fmt="markdown"` (`markdown`\|`csv`\|`json`\|`oscal`), `out_path?` | renders a bundle to the chosen format; `oscal` writes `<bundle>.oscal.json` |
| `sign_bundle` | **medium** | `bundle_path` | adds an HMAC signature over the seal using the stored signing key |

## Integrity model

- Each record hash = `SHA-256(prev_hash ‖ canonical_json(record))`; genesis
  `prev` = 64 zeros. The `chainHead` is the last record hash.
- Seal = `{framework, period, sources (+ per-db SHA-256), recordCount, chainHead,
  generatedAt, generator, optional signature}`.
- The chain is over **evidence records only**, so `chainHead` is **reproducible**
  for the same (framework, period, sources).
- **Tamper-EVIDENT, not tamper-PROOF** — the source `audit.db` remains the system
  of record; record `chainHead` out-of-band as an anchor.

## Out of scope (by design)

- Scanning or operating infrastructure (use the other AIops-tools)
- Acting as a GRC platform / policy-management system
- OSCAL export (documented v0.2 roadmap; v0.1 emits JSON / Markdown / CSV)

Want another framework, control mapping, or export format? Open an issue or PR —
feedback and contributions welcome.
