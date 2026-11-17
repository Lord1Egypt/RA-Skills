## Description:

Scans AI Agent and Skill code for sensitive data exposure, API key leaks, injection risks, permission issues, and data security vulnerabilities, with optional AI-assisted analysis and fix guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g620710](https://clawhub.ai/user/g620710)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use this skill to audit AI Agent and Skill repositories before release, installation, or periodic security review. It reports suspected vulnerabilities and provides remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default AI analysis can send scan findings and source snippets, which may include sensitive code, secrets, local paths, or related context, to the configured AI endpoint.

Mitigation: Use --no-ai for sensitive or proprietary repositories unless external AI analysis is explicitly approved.

Risk: A custom API base URL can redirect AI analysis data to an endpoint outside the expected DeepSeek service.

Mitigation: Use only trusted and controlled base URLs, and review endpoint configuration before running AI analysis.

Risk: Static pattern scanning and AI-generated analysis can produce false positives, false negatives, or incomplete remediation advice.

Mitigation: Treat results as review inputs and have qualified reviewers confirm high-impact findings and fixes before deployment.

## Reference(s):

- [AI Agent Security Checklist](references/security_checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/g620710/skills/ai-agent-security-scanner)
- [ClawHub Publisher Profile](https://clawhub.ai/user/g620710)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Plain text or JSON security audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write reports to a file with -o and filter by severity; AI analysis requires DeepSeek API credentials unless --no-ai is used.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
