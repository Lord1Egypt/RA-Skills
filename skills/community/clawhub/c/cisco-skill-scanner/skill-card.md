## Description:

Scan agent skills for security threats using the Cisco AI skill-scanner CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godsboy](https://clawhub.ai/user/godsboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan agent skill directories before installation or publication for prompt-injection, data-exfiltration, credential-harvesting, and malicious-code risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the scanner package can create supply-chain exposure.

Mitigation: Install it in an isolated environment such as pipx or a virtualenv, and pin the package version where possible.

Risk: Full LLM scan mode may send scanned skill content to the configured provider.

Mitigation: Avoid full LLM scans on private or proprietary skills unless sharing the scanned content with that provider is approved.

## Reference(s):

- [Cisco AI Skill Scanner on ClawHub](https://clawhub.ai/godsboy/skills/cisco-skill-scanner)
- [Cisco AI skill-scanner project](https://github.com/cisco-ai-defense/skill-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and scanner report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default scans use static and behavioral analysis; full scans can use an LLM analyzer when an API key is configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
