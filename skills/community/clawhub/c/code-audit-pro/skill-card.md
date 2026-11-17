## Description:

Reviews code for security, performance, logic, style, and AI-generated-code issues, with modes for full reviews, PR reviews, security-focused checks, and quick checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g1776933879](https://clawhub.ai/user/g1776933879)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review source code, diffs, pull requests, and snippets for likely security, quality, performance, and AI-code reliability issues before merging or deploying changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill's security-audit claims are broader than its local regex-based scanner.

Mitigation: Use it as an initial review aid only, and keep human review plus established security tooling for complete audits and PR gates.

Risk: The installer changes the Python environment with unpinned packages.

Mitigation: Review install.sh before running it and install dependencies in a disposable or isolated virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g1776933879/skills/code-audit-pro)
- [Publisher profile](https://clawhub.ai/user/g1776933879)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports and terminal text with severity labels, issue summaries, locations, and remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable shell commands and code snippets for local scanning or fixes.]

## Skill Version(s):

2.2.2 (source: release evidence and OpenClaw frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
