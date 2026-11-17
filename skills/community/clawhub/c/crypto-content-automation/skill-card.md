## Description:

Crypto Content Automation helps agents scan AI, crypto, and AI-plus-crypto topics and draft content plans with practical guidance and risk notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hemalylas381-rgb](https://clawhub.ai/user/hemalylas381-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and operators use this skill to create crypto-focused topic scans and draft content plans for social platforms. Review outputs before use because the security evidence says publishing support is overstated and the package depends on scanner modules that are not included locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says scripts/run.py loads code from a hard-coded local workspace path, which may run unreviewed code outside the released artifact.

Mitigation: Remove or review the external workspace import path before execution, and package the required scanner modules locally.

Risk: The skill describes publishing to social platforms using cookies, and those cookies should be treated as account credentials.

Mitigation: Do not provide platform cookies unless the integration is reviewed, expected publishing behavior is confirmed, and credentials are isolated to appropriate accounts.

Risk: Crypto content plans may become misleading, time-sensitive, or unsuitable as financial advice if published without review.

Mitigation: Manually fact-check generated topics and add appropriate editorial, compliance, and risk review before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hemalylas381-rgb/skills/crypto-content-automation)
- [ClawHub publisher profile](https://clawhub.ai/user/hemalylas381-rgb)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON files, with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Python execution; node is listed as a package binary requirement.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
