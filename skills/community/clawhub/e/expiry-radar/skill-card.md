## Description:

Find artefacts in a repository that will break on a known future date — expired or expiring X.509 certificates (PEM, DER, PKCS#12, PKCS#7, embedded), committed JWTs past their exp claim, and hardcoded valid-until or expires dates in fixtures and config. Use when asked to check a repo for expiring certs or tokens, when a test suite or demo might fail because a fixture certificate expired, before a release, or when asking what breaks by a given date. Not for monitoring live production endpoints or renewing certificates, and not for scanning AI-agent skills (use skillscan).

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can scan a repository before a release or test run to identify certificates, JWTs, and configured dates that have expired or will expire by a chosen date. The tool works offline and reports findings without renewing or replacing artefacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pip installation command fetches code from a remote Git repository, and the scan was partial because a local path-like reference could not be resolved.

Mitigation: Prefer the documented v0.3.0-pinned download when installing, and resolve the reported local path before relying on scan results.

## Reference(s):

- [Expiry Radar project](https://github.com/RakTikoo/expiry-radar)
- [Pinned v0.3.0 download](https://raw.githubusercontent.com/RakTikoo/expiry-radar/v0.3.0/expiry_radar.py)
- [ClawHub skill page](https://clawhub.ai/raktikoo/skills/expiry-radar)

## Skill Output:

**Output Type(s):** [Analysis, JSON, SARIF, Guidance]

**Output Format:** [Text report, JSON, or SARIF 2.1.0]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports artefact kind, file and line, expiry date, and scan status; JWT values are not printed in full.]

## Skill Version(s):

0.3.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
