## Description:

Security audit tool for ClawHub/OpenClaw skills using static analysis and reputation scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emeraldring3134-netizen](https://clawhub.ai/user/emeraldring3134-netizen)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill publishers use this skill to review ClawHub/OpenClaw skill directories for static-risk patterns, reputation scoring, and pre-publish security guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit verdicts may be misleading because a self-named target is automatically marked safe.

Mitigation: Do not rely on this skill as the sole security decision point; remove or review the self-whitelist behavior before trusting results.

Risk: The skill advertises full, sandbox, and VirusTotal checks that the authoritative security evidence says are not implemented.

Mitigation: Treat those checks as unavailable until the code implements them, or update the documentation and metadata to match actual behavior.

Risk: The release metadata requires a VirusTotal API key and requests dependency even though the security evidence flags that requirement as unnecessary.

Mitigation: Avoid configuring unnecessary credentials and clean up dependency/API-key requirements before broad deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/emeraldring3134-netizen/skills/claw-secure-auditor)
- [Publisher Profile](https://clawhub.ai/user/emeraldring3134-netizen)
- [Declared Homepage](https://github.com/YOURNAME/claw-secure-auditor)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Terminal text report with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports a reputation score, risk level, and findings for a target skill directory.]

## Skill Version(s):

1.1.1 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
