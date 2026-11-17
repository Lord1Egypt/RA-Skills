## Description:

Automated vulnerability scanner for agent platforms that performs dependency scanning, multi-database CVE lookup, SAST analysis, and agent-specific static hook inspection for OpenClaw hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Developers and security engineers use this skill to scan agent skill directories and OpenClaw installations for dependency vulnerabilities, CVE context, SAST findings, and hook inspection results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The continuous hook can inject untrusted scan findings as system-level messages.

Mitigation: Review hook behavior before installation and keep continuous hook mode disabled until system-role reporting is fixed.

Risk: A broad scan target can expose more local skill or dependency content than intended.

Mitigation: Set CLAWSEC_SCANNER_TARGET to the narrow directory that should be scanned.

Risk: Some stated security coverage does not match the code behavior.

Mitigation: Treat DAST results as static inspection rather than runtime validation and review listed static signals manually.

Risk: Unpinned or unsigned installation paths increase supply-chain review burden.

Mitigation: Prefer the signed manual installation path or exact pinned package versions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davida-ps/skills/clawsec-scanner)
- [ClawSec Homepage](https://clawsec.prompt.security)
- [ClawSec Scanner Documentation](https://clawsec.prompt.security/scanner)
- [OSV API Documentation](https://osv.dev/docs/)
- [NVD Vulnerabilities API](https://nvd.nist.gov/developers/vulnerabilities)
- [Semgrep Registry](https://semgrep.dev/explore)
- [Bandit Documentation](https://bandit.readthedocs.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON or text scan reports and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write JSON report files when configured; continuous hook mode can add severity summaries to conversation messages.]

## Skill Version(s):

0.0.7 (source: frontmatter, skill.json, changelog released 2026-06-23, evidence release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
