## Description:

网络安全评估引擎免费版 helps individual developers perform lightweight security self-checks, basic OWASP Top 10 review, threat modeling, and vulnerability triage before release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review project directories for common security risks, draft basic STRIDE threat models, and produce text or JSON-style security assessment outputs for pre-release self-checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run shell commands and dependency audit tools against local project files.

Mitigation: Review the generated commands before execution and run them only in project directories intended for scanning.

Risk: The skill may write files or install hooks when following workflow examples.

Mitigation: Allow file writes or hooks only when those side effects are explicitly desired.

Risk: Secret-scan output can expose credentials or private code paths.

Mitigation: Handle scan output as sensitive and avoid sharing it outside the trusted review context.

Risk: Optional callback URLs can introduce unintended external communication.

Mitigation: Do not provide callback URLs unless the receiving endpoint and data handling are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cybersecurity-engine-tool-free)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with bash, YAML, text, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include security findings, execution logs, threat registers, remediation priorities, and configuration snippets.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
