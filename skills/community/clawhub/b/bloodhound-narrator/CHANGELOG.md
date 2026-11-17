# Changelog

## 1.0.2

### Fixed

- **Twelve edge types were scored as zero.** `$Script:DangerousEdges` was declared but never referenced anywhere in the scorer. `GenericWrite`, `WriteOwner`, `AllExtendedRights`, `ForceChangePassword`, `AddMember`, `AddSelf`, `ReadLAPSPassword`, `ReadGMSAPassword`, `GpLink`, `Contains`, `AdminTo` and `HasSession` contributed nothing to severity. A path built purely from these edges was reported as Low. Edge scoring is now table-driven and every weighted label is applied.
- **The most severe findings shipped without remediation.** The classifier emits Tier 0-qualified factors (`GenericAllOnTier0`, `WriteDaclOnTier0`, `OwnsOnTier0`); the appendix looked those up verbatim, found no match, and silently omitted the remediation section. Added `Resolve-RemediationKey` to fall back to the base factor. Unmapped factors are now printed rather than dropped.
- **A malformed `pwdlastset` aborted the entire run.** `[datetime]$pwdlastset` threw on any unparseable value. Replaced with `ConvertTo-DateTimeOrNull`; the path is still scored and the condition is recorded as an `UnparseablePwdLastSet` factor.
- **Edges referencing a node absent from the path caused a null reference.** Truncated exports now render as `<unresolved:id>` instead of failing.
- **Scores could exceed 100.** `path-003` in the bundled fixture scored 105. Capped at 100; `RawScore` and `ScoreCapped` are exposed so the uncapped value is still auditable.
- **`version` in `SKILL.md` frontmatter was stale**, still reading 1.0.0 at the 1.0.1 release.

### Added

- **AD CS detection** — composite BloodHound CE edges `ADCSESC1`, `ADCSESC3`, `ADCSESC4`, `ADCSESC6a/b`, `ADCSESC7`, `ADCSESC9a/b`, `ADCSESC10a/b`, `ADCSESC13`, `GoldenCert`, plus the primitives `ManageCA`, `ManageCertificates`, `WritePKIEnrollmentFlag`, `WritePKINameFlag`, `DelegatedEnrollmentAgent`, `Enroll`. Each carries dedicated remediation guidance.
- **Resource-based constrained delegation** — `AllowedToAct`, `AddAllowedToAct`, `AllowedToDelegate`, with remediation covering the point most often missed: clearing `msDS-AllowedToActOnBehalfOfOtherIdentity` does not close the path if the write permission that set it remains.
- **Shadow credentials** — `AddKeyCredentialLink`.
- **Credential material reads** — `ReadLAPSPassword`, `SyncLAPSPassword`, `ReadGMSAPassword`, `DumpSMSAPassword`.
- **Additional lateral movement edges** — `CanRDP`, `CanPSRemote`, `ExecuteDCOM`, `SQLAdmin`, `WriteSPN`, `WriteAccountRestrictions`.
- **Unknown-edge reporting** — labels that are neither weighted nor explicitly ignored are collected, surfaced as a warning, and retrievable via `Get-UnknownEdgeLabels`. Without this, an export from a newer BloodHound release silently understates severity.
- **`tests/synthetic-adcs.json`** — fixture covering ESC1, ESC4, RBCD, shadow credentials, LAPS read, an unparseable date, and an unrecognised edge label.
- 16 new Pester tests, including a regression guard asserting the five original fixture paths keep their 1.0.1 severities.

### Changed

- **Tier 0 is now two-tier.** Domain Admins, Enterprise Admins, Administrators, Domain Controllers, Schema Admins and Key Admins score +40. Account/Backup/Server/Print Operators and DnsAdmins score +30 — privileged, but reaching them is not the same finding as reaching Domain Admins. Previously all nine scored identically.
- **Kerberoastable accounts are detected anywhere in the path** (+6), not only at the source (+10). Previously a roastable account mid-chain scored nothing.
- Edge scoring is deduplicated on label plus target, so a repeated edge to the same object counts once while the same edge type to distinct targets still counts separately.
- Lateral movement rebalanced: `AdminTo` and `HasSession` now score 3 each individually, and the combination bonus dropped from 10 to 5 to avoid double counting.

### Compatibility

Severity output for the five bundled fixture paths is **unchanged** from 1.0.1 (3 Critical, 2 High) — the new weights were calibrated against that baseline and the regression guard enforces it.

That guarantee covers the fixture, not your data. Paths whose severity was previously understated because they relied on the unscored edge types **will now rate higher**. If you have issued a report to a client from 1.0.1, re-running it on 1.0.2 may produce different severities for the same environment. Note the tool version in the deliverable, and re-baseline before comparing two assessments.
