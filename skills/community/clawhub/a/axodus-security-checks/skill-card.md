## Description:

Perform security reviews of code to detect secrets exposure, authentication and authorization issues, injection risks, unsafe dependencies, and improper execution paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before deployment, after authentication or authorization changes, or when adding dependencies and integrations to produce evidence-based security review findings with remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaging trigger metadata may cause the skill to be invoked unexpectedly or not invoked when intended.

Mitigation: Verify and correct trigger metadata before relying on automatic invocation.

Risk: Security reviews may encounter secrets or sensitive configuration values.

Mitigation: Keep review scope limited to intended files and redact any discovered secrets in outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/axodus-security-checks)
- [ClawHub publisher profile](https://clawhub.ai/user/mzfshark)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Configuration, Guidance]

**Output Format:** [Markdown security report with YAML-style findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include a summary, severity, issue, location, and remediation; secrets should be redacted.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
