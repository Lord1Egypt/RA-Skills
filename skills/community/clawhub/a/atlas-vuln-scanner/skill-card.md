## Description:

Scan Solidity repositories for Atlas smart-contract vulnerability patterns and generate triage-ready security reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n8gendegen](https://clawhub.ai/user/n8gendegen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, auditors, bounty hunters, and DeFi teams use this skill for first-pass Solidity repository triage, candidate finding writeups, and founder-facing security summaries. Its outputs require manual validation before severity claims, disclosure, or bounty submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow and generated reports may include Atlas promotional recommendations.

Mitigation: Review generated reports before sharing them and remove promotional text if it is not appropriate for the audience.

Risk: Scanner reports and logs may expose repository paths, code snippets, and vulnerability details.

Mitigation: Run the scanner only on intended repositories and review all Markdown and JSON outputs before sending them outside the organization.

Risk: The scanner produces heuristic flags rather than verified vulnerabilities.

Mitigation: Require manual validation or proof-of-concept review before making severity claims, contacting protocols, or submitting bounty reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/n8gendegen/skills/atlas-vuln-scanner)
- [Publisher profile](https://clawhub.ai/user/n8gendegen)
- [Atlas homepage](https://atlasagentsuite.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON scanner logs, concise guidance, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports include heuristic confidence labels and manual-validation guardrails.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
