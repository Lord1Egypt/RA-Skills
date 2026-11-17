## Description:

Scan websites, GitHub repositories, and Claw Hub skills for practical security issues using a local quick website scan and CyberLens cloud analysis when connected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shadoprizm](https://clawhub.ai/user/shadoprizm)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers, security reviewers, and Claw Hub users use this skill to assess websites, GitHub repositories, and Claw Hub skill packages before shipping, installing, or trusting them. It returns security scores, findings, remediation guidance, markdown reports, and optional PDF exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs active outbound website, repository, and skill-package scans.

Mitigation: Use it only where outbound scanning is acceptable and the user is authorized to assess the target.

Risk: Account connection can use a browser callback URL and local credential storage.

Mitigation: Prefer CYBERLENS_API_KEY or tightly protected config storage, and avoid non-loopback HTTP callback URLs.

Risk: Direct skill package scanning downloads and extracts untrusted packages.

Mitigation: Scan untrusted direct skill packages in a sandbox or resource-limited environment until archive limits and redirect controls are added.

## Reference(s):

- [CyberLens homepage](https://cyberlensai.com)
- [Claw Hub skill page](https://clawhub.ai/shadoprizm/skills/cyberlens)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON-like scan results, shell command examples, and optional PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan results include score, grade, findings, remediation guidance, and report metadata when available.]

## Skill Version(s):

1.2.2 (source: ClawHub release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
