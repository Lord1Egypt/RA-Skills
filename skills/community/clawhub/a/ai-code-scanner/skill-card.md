## Description:

AI-powered code review skill that scans source code for security vulnerabilities, quality issues, and best-practice violations using a remote API backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review code for security and quality issues before merging, shipping, or auditing changes. It combines automated API scan results with agent-written recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed source code and filenames are uploaded to an external API.

Mitigation: Use only with code that may be shared with the external service; avoid proprietary code, secrets, credentials, private keys, and environment files.

Risk: The security assessment reports an unsafe script bug that can execute attacker-controlled code locally.

Mitigation: Inspect and fix the script's JSON construction before running it on untrusted input or sample files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/ai-code-scanner)
- [Code scanner API base](https://1341839497-kvq7g9wk8p.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown code review report with CLI scan output and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a numeric score, approve or reject recommendation, issue counts, severity groups, and line-level findings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
